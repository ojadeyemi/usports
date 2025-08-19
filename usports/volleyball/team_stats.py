"""Volleyball team performance stats (no W/L)."""

import asyncio
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup, Tag

from usports.base.constants import BASE_URL, BS4_PARSER, VOLLEYBALL, get_season_urls
from usports.base.exceptions import DataFetchError
from usports.base.types import LeagueType, SeasonType
from usports.utils import (
    _merge_team_data,
    clean_text,
    convert_types,
    fetch_page_html,
    normalize_gender_arg,
    setup_logging,
    validate_season_option,
)
from usports.utils.helpers import get_conference_mapping_for_league

from .constants import VOLLEYBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING
from .standings import _get_sport_identifier

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
            matches = clean_text(cols[2].get_text())
            sets = clean_text(cols[3].get_text())

            row_data["team_name"] = team_name
            row_data["matches_played"] = matches
            row_data["sets_played"] = sets

            for j, col in enumerate(columns):
                col_index = j + 4
                if col_index < len(cols):
                    value = cols[col_index].get_text().strip()

                    if "percentage" in col or col == "hitting_percentage":
                        value = value.replace("%", "")

                    row_data[col] = value

            table_data.append(row_data)

    return table_data


async def _fetching_team_stats(url: str) -> list[dict[str, Any]]:
    """Fetch team stats data from a given URL."""
    try:
        tables_html = await fetch_page_html(url)

        all_data = []

        for i, column_mapping in enumerate(VOLLEYBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING):
            if i < len(tables_html):
                soup = BeautifulSoup(tables_html[i], BS4_PARSER)
                table_data = _parse_team_stats_table(soup, list(column_mapping.keys()))
                all_data = _merge_team_data(all_data, table_data)

        return all_data

    except Exception as e:
        raise DataFetchError(f"Error fetching volleyball team stats: {e}") from e


async def _get_team_stats_df(stats_url: str) -> pd.DataFrame:
    """Process team stats into a pandas DataFrame"""
    team_stats = await _fetching_team_stats(stats_url)
    df = pd.DataFrame(team_stats)

    combined_type_mapping: dict[str, type] = {
        "team_name": str,
        "matches_played": int,
        "sets_played": int,
    }

    for mapping in VOLLEYBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING:
        combined_type_mapping.update(mapping)

    if not team_stats or df.empty:
        return pd.DataFrame(columns=combined_type_mapping.keys())  # type: ignore

    invalid_rows_count = df[df["matches_played"] == "-"].shape[0]
    if invalid_rows_count > 0:
        logger.debug(f"\nDropping {invalid_rows_count} rows with invalid 'matches_played' values\n")
        df = df[df["matches_played"] != "-"]

    df = convert_types(df, combined_type_mapping)

    conference_map = get_conference_mapping_for_league(VOLLEYBALL)
    df["conference"] = df["team_name"].map(conference_map).astype(str)
    # drop service attempts dolumn
    if "serve_attempts" in df.columns:
        df.drop(columns=["serve_attempts"], inplace=True)

    return df


async def _fetch_team_stats(league: LeagueType, season: SeasonType) -> pd.DataFrame:
    """Fetch team performance stats."""
    gender = normalize_gender_arg(league)
    sport = _get_sport_identifier(gender)
    season_urls = get_season_urls(VOLLEYBALL)
    season_url = validate_season_option(season, season_urls)
    team_stats_url = f"{BASE_URL}/{sport}/{season_url}/teams"

    logger.debug(f"FETCHING {gender.upper()} VOLLEYBALL {season.upper()} TEAM STATISTICS")

    return await _get_team_stats_df(team_stats_url)


def usports_vball_teams(
    league: LeagueType,
    season_option: SeasonType = "regular",
) -> pd.DataFrame:
    """
    Get volleyball team stats.

    Args:
        league: 'm' or 'w'
        season_option: 'regular', 'playoffs', or 'championship'

    Returns:
        DataFrame with team stats including offensive, defensive, and serve/receive statistics
    """
    season_option = season_option.lower()  # type: ignore
    return asyncio.run(_fetch_team_stats(league, season_option))
