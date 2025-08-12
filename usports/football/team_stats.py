"""Football team performance stats (no W/L)."""

import asyncio
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup, Tag

from usports.base.constants import BASE_URL, BS4_PARSER, FOOTBALL, SEASON_URLS
from usports.base.exceptions import DataFetchError
from usports.base.types import SeasonType
from usports.utils import (
    _merge_team_data,
    clean_text,
    convert_types,
    fetch_page_html,
    setup_logging,
    split_made_attempted,
    validate_season_option,
)
from usports.utils.helpers import get_conference_mapping_for_league

from .constants import FBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING

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
    except Exception as e:  # Catch specific exceptions if possible
        raise DataFetchError(f"Error fetching football team_stats: {e}") from e


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
    conference_map = get_conference_mapping_for_league(FOOTBALL)
    df["conference"] = df["team_name"].map(conference_map).astype(str)

    return df


async def _fetch_team_stats(season: SeasonType) -> pd.DataFrame:
    """Fetch team performance stats."""
    season_url = validate_season_option(season, SEASON_URLS)
    team_stats_url = f"{BASE_URL}/fball/{season_url}/teams"

    logger.debug(f"FETCHING FOOTBALL {season.upper()} TEAM STATISTICS")

    return await _get_team_stats_df(team_stats_url)


def usports_fball_teams(season_option: SeasonType = "regular") -> pd.DataFrame:
    """
    Get football team stats.

    Args:
        season_option: 'regular', 'playoffs', or 'championship'

    Returns:
        DataFrame with team stats
    """
    season_option = season_option.lower()  # type: ignore
    return asyncio.run(_fetch_team_stats(season_option))
