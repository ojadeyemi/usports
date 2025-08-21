"""Football team performance stats (no W/L)."""

import asyncio
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup, Tag

from usports.base.constants import BASE_URL, BS4_PARSER, FOOTBALL, get_season_urls
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

from .constants import FBALL_BBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING

logger = setup_logging()


def _process_column_data(row_data: dict[str, Any], cols: list[Tag], columns: list[str]) -> None:
    """Process all column data and add to row_data."""
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

    for j, col in enumerate(columns):
        col_index = j + 3
        if col_index < len(cols):
            raw_value = cols[col_index].get_text().strip()
            processed_value = _process_single_column(col, raw_value, dash_split_mapping, row_data)
            if processed_value is not None:
                row_data[col] = processed_value


def _process_single_column(
    col: str, raw_value: str, dash_split_mapping: dict[str, str], row_data: dict[str, Any]
) -> Any:
    """Process a single column value based on column type."""
    match col:
        case "pass_completions":
            return _process_pass_completions(raw_value, row_data)
        case "interception_yards":
            return _process_interception_yards(raw_value)
        case "time_of_possession":
            return _process_time_of_possession(raw_value)
        case col if col in ["home_attendance", "average_home_attendance"]:
            return _process_attendance(raw_value)
        case col if col in dash_split_mapping:
            return _process_dash_split_column(col, raw_value, dash_split_mapping, row_data)
        case _ if "%" in raw_value:
            return raw_value.replace("%", "")
        case _:
            return raw_value


def _process_pass_completions(raw_value: str, row_data: dict[str, Any]) -> str:
    """Process pass completions field with format: completions-attempts-interceptions."""
    parts = raw_value.split("-")
    if len(parts) == 3:
        row_data["pass_attempts"] = parts[1]
        row_data["pass_interceptions"] = parts[2]
        return parts[0]
    return raw_value


def _process_interception_yards(raw_value: str) -> str:
    """Process interception yards, taking last part if dash-separated."""
    if "-" in raw_value:
        return raw_value.split("-")[-1]
    return raw_value


def _process_dash_split_column(
    col: str, raw_value: str, dash_split_mapping: dict[str, str], row_data: dict[str, Any]
) -> str | int:
    """Process columns that need dash splitting."""
    try:
        made, second_val = split_made_attempted(raw_value)
        derived_key = dash_split_mapping[col]
        row_data[derived_key] = second_val
        return made
    except ValueError as e:
        print(f"Error splitting '{raw_value}' for column '{col}': {e}")
        return raw_value


def _process_attendance(raw_value: str) -> Any:
    """Process attendance fields by removing commas and converting to int."""
    try:
        return int(raw_value.replace(",", ""))
    except ValueError:
        return raw_value.replace(",", "")


def _process_time_of_possession(raw_value: str) -> Any:
    """Convert time format MM:SS to total seconds."""
    try:
        minutes, seconds = raw_value.split(":")
        return int(minutes) * 60 + int(seconds)
    except Exception:
        return raw_value


def _parse_football_team_stats_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse football team stats data from an HTML table without casting."""
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
            _process_column_data(row_data, cols, columns)
            table_data.append(row_data)

    return table_data


async def _fetching_team_stats(url: str) -> list[dict[str, Any]]:
    """
    Fetch and merge football team stats data from the given URL.
    """
    try:
        tables_html = await fetch_page_html(url)

        all_data = []
        for i, column_mapping in enumerate(FBALL_BBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING):
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

    for mapping in FBALL_BBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING:
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
    season_urls = get_season_urls(FOOTBALL)
    season_url = validate_season_option(season, season_urls)
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
