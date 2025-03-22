import asyncio
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup, Tag

from usports.utils import (
    _merge_team_data,
    clean_text,
    convert_types,
    fetch_page_html,
    setup_logging,
    split_made_attempted,
    validate_season_option,
)
from usports.utils.constants import BASE_URL, BS4_PARSER, SEASON_URLS, TEAM_CONFERENCES
from usports.utils.types import SeasonType

from .constants import FBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING, STANDINGS_COLUMNS_TYPE_MAPPING

logger = setup_logging()


def _parse_football_team_stats_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """
    Parse football team stats data from an HTML table without casting,
    leaving type conversion to later DataFrame processing.
    """
    table_data: list[dict[str, Any]] = []
    rows: list[Tag] = soup.find_all("tr")[1:]  # type: ignore
    dash_split_mapping = {
        "field_goal_made": "field_goal_attempt",
        "extra_point_made": "extra_point_attempt",
        "third_down_conversions_made": "third_down_attempts",
        "fourth_down_conversions_made": "fourth_down_attempts",
        "kick_return_count": "kick_return_yards",
        "punt_return_count": "punt_return_yards",
        "punt_count": "punt_yards",
        "kickoff_count": "kickoff_yards",
        "scores_made": "scores_attempt",
        "touchdowns_made": "touchdowns_attempt",
        "fumbles": "fumbles_lost",
    }

    for row in rows:
        cols: list[Tag] = row.find_all("td")  # type: ignore
        if len(cols) > 1:
            row_data = {}
            row_data["team_name"] = clean_text(cols[1].get_text())
            row_data["games_played"] = clean_text(cols[2].get_text())

            for j, col in enumerate(columns):
                col_index = j + 3
                if col_index < len(cols):
                    raw_value = cols[col_index].get_text().strip()

                    if col == "pass_completions":
                        parts = raw_value.split("-")
                        if len(parts) == 3:
                            row_data["pass_completions"] = parts[0]
                            row_data["pass_attempts"] = parts[1]
                            row_data["pass_interceptions"] = parts[2]
                        else:
                            row_data["pass_completions"] = raw_value

                    elif col == "interception_yards":
                        if "-" in raw_value:
                            parts = raw_value.split("-")
                            row_data[col] = parts[-1]
                        else:
                            row_data[col] = raw_value

                    elif col in dash_split_mapping:
                        try:
                            made, second_val = split_made_attempted(raw_value)
                            row_data[col] = made
                            derived_key = dash_split_mapping[col]
                            row_data[derived_key] = second_val
                        except ValueError as e:
                            print(f"Error splitting '{raw_value}' for column '{col}': {e}")
                            row_data[col] = raw_value

                    elif col in ["home_attendance", "average_home_attendance"]:
                        try:
                            row_data[col] = int(raw_value.replace(",", ""))
                        except ValueError:
                            row_data[col] = raw_value.replace(",", "")

                    elif col == "time_of_possession":
                        try:
                            minutes, seconds = raw_value.split(":")
                            row_data[col] = int(minutes) * 60 + int(seconds)
                        except Exception:
                            row_data[col] = raw_value

                    elif "%" in raw_value:
                        row_data[col] = raw_value.replace("%", "")

                    else:
                        row_data[col] = raw_value

            table_data.append(row_data)

    return table_data


def _parse_standings_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse standings data from an HTML table"""
    table_data: list[dict[str, Any]] = []

    # Find all rows in the table
    rows: list[Tag] = soup.find_all("tr")  # type: ignore

    for row in rows:
        row_data = {}

        # Extract the team name from the <th> element
        team_name_th = row.find("th", class_="team-name")
        if team_name_th:
            team_name_tag = team_name_th.find("a")  # type: ignore
            if team_name_tag:
                team_name = clean_text(team_name_tag.get_text())  # type: ignore
                row_data["team_name"] = team_name

        # Extract the column data from <td> elements
        cols: list[Tag] = row.find_all("td")  # type: ignore
        if cols:
            for col, column_name in zip(cols, columns):
                row_data[column_name] = clean_text(col.get_text())

            table_data.append(row_data)

    return table_data


async def _fetching_team_stats(url: str) -> list[dict[str, Any]]:
    """
    Fetch and merge football team stats data from the given URL.
    """
    try:
        tables_html = await fetch_page_html(url)

        all_data = []
        for i, column_mapping in enumerate(FBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING):
            soup = BeautifulSoup(tables_html[i], BS4_PARSER)
            table_data = _parse_football_team_stats_table(soup, list(column_mapping.keys()))
            all_data = _merge_team_data(all_data, table_data)

        return all_data
    except Exception as e:
        raise RuntimeError(f"Error fetching football team_stats: {e}") from e


async def _fetching_standings(url: str) -> list[dict[str, Any]]:
    """
    Fetch standings data from a given URL.
    """
    try:
        tables_html = await fetch_page_html(url)

        all_data = []
        for table_html in tables_html:
            soup = BeautifulSoup(table_html, BS4_PARSER)
            column_names = list(STANDINGS_COLUMNS_TYPE_MAPPING.keys())[1:]
            standings_data = _parse_standings_table(soup, column_names)
            all_data.extend(standings_data)

        return all_data

    except Exception as e:
        raise RuntimeError(f"Error fetching football standings: {e}") from e


# -------------------------------------------------------------------
# DataFrame Assembly
# -------------------------------------------------------------------
async def _get_team_stats_df(stats_url: str) -> pd.DataFrame:
    """Function to handle football teams stats to a pandas DataFrame"""
    team_stats = await _fetching_team_stats(stats_url)
    df = pd.DataFrame(team_stats)
    combined_type_mapping: dict[str, type] = {"team_name": str, "games_played": int}

    for mapping in FBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING:
        combined_type_mapping.update(mapping)

    if not team_stats or df.empty:
        return pd.DataFrame(columns=combined_type_mapping.keys())  # type: ignore

    invalid_rows_count = df[df["games_played"] == "-"].shape[0]

    if invalid_rows_count > 0:
        logger.debug(f"\nDropping {invalid_rows_count} rows with invalid 'games_played' values\n")
        df = df[df["games_played"] != "-"]

    df = convert_types(df, combined_type_mapping)

    return df


async def _get_standings_df(standings_url: str) -> pd.DataFrame:
    """function to handle stadnings data into a pandas DataFrame"""
    standings_data = await _fetching_standings(standings_url)

    standings_df = pd.DataFrame(standings_data)

    if not standings_data or standings_df.empty:
        return pd.DataFrame(columns=STANDINGS_COLUMNS_TYPE_MAPPING.keys())  # type: ignore

    standings_df = convert_types(standings_df, STANDINGS_COLUMNS_TYPE_MAPPING)
    standings_df = standings_df.drop(columns=["ties"])

    return standings_df


def _construct_team_url(season_option: str) -> tuple[str, str]:
    season = validate_season_option(season_option, SEASON_URLS)
    sport = "fball"

    team_stats_url = f"{BASE_URL}/{sport}/{season}/teams"
    standings_url = f"{BASE_URL}/{sport}/{season}/standings"

    return team_stats_url, standings_url


async def _combine_data(season_option: str) -> pd.DataFrame:
    """
    Combine football team stats and standings data into a single DataFrame.
    For playoffs/championship, only team stats are fetched.
    For regular season, standings data is merged with team stats, and games_played from standings takes precedence.
    """
    if season_option not in SEASON_URLS:
        raise ValueError(f"Invalid season_option: {season_option}. Must be one of {', '.join(SEASON_URLS.keys())}")

    team_stats_url, standings_url = _construct_team_url(season_option)

    if season_option in ["playoffs", "championship"]:
        logger.debug(f"FETCHING FBALL {season_option.upper()} SEASON STATISTICS")
        team_stats_df = await _get_team_stats_df(team_stats_url)
        team_stats_df["conference"] = team_stats_df["team_name"].map(TEAM_CONFERENCES).astype(str)
        return team_stats_df

    logger.debug(f"FETCHING FBALL {season_option.upper()} SEASON STANDINGS")
    standings_df = await _get_standings_df(standings_url)
    logger.debug(f"FETCHING FBALL {season_option.upper()} SEASON STATISTICS")
    team_stats_df = await _get_team_stats_df(team_stats_url)

    combined_df = pd.merge(
        standings_df,
        team_stats_df,
        on="team_name",
        how="left",
        suffixes=("_standings", "_team_stats"),
    )
    if not combined_df.empty:
        combined_df["games_played"] = combined_df["games_played_standings"].fillna(
            combined_df["games_played_team_stats"]
        )
        combined_df = combined_df.drop(columns=["games_played_standings", "games_played_team_stats"])
        combined_df["conference"] = combined_df["team_name"].map(TEAM_CONFERENCES).astype(str)
    return combined_df


def usports_football_team_stats(season_option: SeasonType = "regular") -> pd.DataFrame:
    """
    Retrieve U Sports men football team stats.

        Args:
        season_option (str): The season type to fetch data for. Options are:
            - 'regular': Regular season statistics (default).
            - 'playoffs': Playoff season statistics.
            - 'championship': Championship season statistics.

    Returns:
        DataFrame: DataFrame containing the combined team stats.

    """
    season_option = season_option.lower()  # type: ignore
    df = asyncio.run(_combine_data(season_option))
    return df
