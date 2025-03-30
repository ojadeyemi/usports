import asyncio
from typing import Any, Literal

import pandas as pd
from bs4 import BeautifulSoup, Tag

from usports.utils import (
    _merge_team_data,
    clean_text,
    convert_types,
    fetch_page_html,
    normalize_gender_arg,
    setup_logging,
    split_made_attempted,
    validate_season_option,
)
from usports.utils.constants import BASE_URL, BS4_PARSER, SEASON_URLS, TEAM_CONFERENCES
from usports.utils.types import SeasonType

from .constants import STANDINGS_COLUMNS_TYPE_MAPPING, TEAM_STATS_COLUMNS_TYPE_MAPPING
from .player_stats import _get_sport_identifier

logger = setup_logging()


def _parse_team_stats_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse team stats data from an HTML table"""
    table_data: list[dict[str, Any]] = []
    rows: list[Tag] = soup.find_all("tr")[1:]  # type: ignore

    for row in rows:
        cols: list[Tag] = row.find_all("td")  # type: ignore
        if len(cols) > 1:
            row_data = {}
            team_name = clean_text(cols[1].get_text())
            games_played = clean_text(cols[2].get_text())
            row_data["team_name"] = team_name
            row_data["games_played"] = games_played

            for j, col in enumerate(columns):
                if j < len(cols) - 1:
                    value = cols[j + 3].get_text().strip()
                    if col in [
                        "field_goal_made",
                        "three_pointers_made",
                        "free_throws_made",
                        "field_goal_made_against",
                        "three_pointers_made_against",
                    ]:
                        made, attempted = split_made_attempted(value)
                        row_data[col] = made
                        row_data[col.replace("made", "attempted")] = attempted
                    else:
                        row_data[col] = value
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
    Fetch team stats data from a given URL.
    """
    try:
        tables_html = await fetch_page_html(url)

        all_data = []
        for i, column_mapping in enumerate(TEAM_STATS_COLUMNS_TYPE_MAPPING):
            soup = BeautifulSoup(tables_html[i], BS4_PARSER)
            table_data = _parse_team_stats_table(soup, list(column_mapping.keys()))
            all_data = _merge_team_data(all_data, table_data)

        return all_data

    except Exception as e:
        raise RuntimeError(f"Error fetching basketball team_stats: {e}") from e


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
        raise RuntimeError(f"Error fetching basketball standings: {e}") from e


# -------------------------------------------------------------------
# DataFrame Assembly
# -------------------------------------------------------------------
async def _get_team_stats_df(stats_url: str) -> pd.DataFrame:
    """function to handle teams stats to a pandas DataFrame"""
    team_stats = await _fetching_team_stats(stats_url)
    df = pd.DataFrame(team_stats)

    combined_type_mapping: dict[str, type] = {"team_name": str, "games_played": int}

    for mapping in TEAM_STATS_COLUMNS_TYPE_MAPPING:
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


def _construct_team_urls(gender: str, season_option: str) -> tuple[str, str]:
    sport = _get_sport_identifier(gender)
    season = validate_season_option(season_option, SEASON_URLS)

    team_stats_url = f"{BASE_URL}/{sport}/{season}/teams"
    standings_url = f"{BASE_URL}/{sport}/{season}/standings"

    return team_stats_url, standings_url


async def _combine_data(gender: str, season_option: str) -> pd.DataFrame:
    """Combine team stats and standings data into a single DataFrame.
    For playoffs and championship, only fetch team stats since these are
    elimination formats without standings."""
    if season_option not in SEASON_URLS:
        raise ValueError(f"Invalid season_option: {season_option}. Must be one of {', '.join(SEASON_URLS.keys())}")

    team_stats_url, standings_url = _construct_team_urls(gender, season_option)

    # For playoffs and championship, only fetch team stats
    if season_option in ["playoffs", "championship"]:
        logger.debug(f"FETCHING {gender.upper()} {season_option.upper()} SEASON STATISTICS\n")
        team_stats_df = await _get_team_stats_df(team_stats_url)

        # Add conference mapping directly to team stats
        team_stats_df["conference"] = team_stats_df["team_name"].map(TEAM_CONFERENCES).astype(str)

        return team_stats_df

    # For regular season, fetch both standings and team stats
    logger.debug(f"FETCHING {gender.upper()} {season_option.upper()} SEASON STANDINGS")
    standings_df = await _get_standings_df(standings_url)

    logger.debug(f"FETCHING {gender.upper()} {season_option.upper()} SEASON STATISTICS\n")
    team_stats_df = await _get_team_stats_df(team_stats_url)

    # Merge only on "team_name" first, keeping all teams in standings
    combined_df = pd.merge(
        standings_df,
        team_stats_df,
        on="team_name",
        how="left",
        suffixes=("_standings", "_team_stats"),
    )

    if not combined_df.empty:
        # Override "games_played" from team_stats with standings if available
        combined_df["games_played"] = combined_df["games_played_standings"].fillna(
            combined_df["games_played_team_stats"]
        )

        # Drop the extra "games_played_team_stats" column
        combined_df = combined_df.drop(columns=["games_played_standings", "games_played_team_stats"])

        # Add conference mapping
        combined_df["conference"] = combined_df["team_name"].map(TEAM_CONFERENCES).astype(str)

    return combined_df


def usports_bball_teams(
    league: Literal["m", "men", "w", "women"],
    season_option: SeasonType = "regular",
) -> pd.DataFrame:
    """
    Retrieve and combine current U Sports Basketball team stats based on gender and season.

    Args:
        league (str): Gender of the teams. Accepts 'men', 'women', 'm', or 'w' (case insensitive).
        season_option (str): The season type to fetch data for. Options are:
            - 'regular': Regular season statistics (default).
            - 'playoffs': Playoff season statistics.
            - 'championship': Championship season statistics.

    Returns:
        DataFrame: DataFrame containing the combined team stats.
    """
    gender = normalize_gender_arg(league)
    season_option = season_option.lower()  # type: ignore

    df = asyncio.run(_combine_data(gender, season_option))

    return df
