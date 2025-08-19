"""Volleyball player stats"""

import asyncio
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup, Tag
from pandas.errors import EmptyDataError

from usports.base.constants import BASE_URL, BS4_PARSER, VOLLEYBALL, get_season_urls
from usports.base.exceptions import DataFetchError
from usports.base.types import LeagueType, SeasonType
from usports.utils import (
    clean_text,
    convert_types,
    fetch_page_html,
    normalize_gender_arg,
    setup_logging,
    validate_season_option,
)

from .constants import PLAYER_SORT_CATEGORIES, VOLLEYBALL_PLAYER_STATS_COLUMNS_TYPE_MAPPING
from .standings import _get_sport_identifier

logger = setup_logging()


def _parse_player_stats_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse player stats data from an HTML table"""
    table_data: list[dict[str, Any]] = []
    rows: list[Tag] = soup.find_all("tr")  # type: ignore

    for row in rows:
        cols: list[Tag] = row.find_all("td")  # type: ignore

        if len(cols) > 1:
            row_data = {}
            row_data["player_name"] = clean_text(cols[1].get_text())
            row_data["school"] = clean_text(cols[2].get_text())
            row_data["matches_played"] = clean_text(cols[3].get_text())
            row_data["sets_played"] = clean_text(cols[4].get_text())

            start_index = 5
            for i, col_name in enumerate(columns):
                col_index = i + start_index
                if col_index < len(cols):
                    value = clean_text(cols[col_index].get_text())

                    if "percentage" in col_name or col_name == "hitting_percentage":
                        value = value.replace("%", "")

                    row_data[col_name] = value

            table_data.append(row_data)

    return table_data


def _merge_player_data(existing_data: list[dict[str, Any]], new_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge existing and new player data by (player_name, school, matches_played)."""

    def key_func(d: dict[str, Any]) -> str:
        return f"{d['player_name']}_{d['school']}_{d.get('matches_played', 0)}"

    data_dict = {key_func(item): item for item in existing_data}

    for new_item in new_data:
        key = key_func(new_item)

        if key in data_dict:
            existing_item = data_dict[key]
            for k, v in new_item.items():
                if v not in [None, ""]:
                    existing_item[k] = v
        else:
            data_dict[key] = new_item

    return list(data_dict.values())


async def _fetching_player_stats(url: str) -> list[dict[str, Any]]:
    """Fetch player stats from all three tables (offensive, defensive, serve/receive)"""
    try:
        tables_html = await fetch_page_html(url)

        all_data = []

        for i, column_mapping in enumerate(VOLLEYBALL_PLAYER_STATS_COLUMNS_TYPE_MAPPING):
            if i < len(tables_html):
                soup = BeautifulSoup(tables_html[i], BS4_PARSER)
                table_data = _parse_player_stats_table(soup, list(column_mapping.keys()))
                all_data = _merge_player_data(all_data, table_data)

        return all_data

    except Exception as e:
        raise DataFetchError(f"Error fetching volleyball player stats: {e}") from e


async def _get_players_stats_df(stats_url: str) -> pd.DataFrame:
    """Fetch player stats from a page and return a cleaned DataFrame."""
    logger.debug(f"Fetching player stats from: {stats_url[-15:]}")

    player_stats = await _fetching_player_stats(stats_url)

    combined_type_mapping = {
        "player_name": str,
        "school": str,
        "matches_played": int,
        "sets_played": int,
    }

    for mapping in VOLLEYBALL_PLAYER_STATS_COLUMNS_TYPE_MAPPING:
        combined_type_mapping.update(mapping)

    df = pd.DataFrame(player_stats)

    if not player_stats or df.empty:
        return pd.DataFrame(columns=combined_type_mapping.keys())  # type: ignore

    if "player_name" in df.columns:
        df[["lastname_initials", "first_name"]] = df["player_name"].str.split(" ", n=1, expand=True)

    df = convert_types(df, combined_type_mapping)

    df = df.drop(columns=["player_name"], errors="ignore")

    return df


def _construct_player_urls(gender: str, season_option: str) -> list[str]:
    """Construct URLs for fetching volleyball player stats."""
    sport = _get_sport_identifier(gender)
    season_urls = get_season_urls(VOLLEYBALL)
    season = validate_season_option(season_option, season_urls)

    player_stats_url_template = f"{BASE_URL}/{sport}/{season}/players?pos={{position}}&sort={{sort_category}}"

    urls = [
        player_stats_url_template.format(position=position, sort_category=category)
        for position, category in PLAYER_SORT_CATEGORIES
    ]

    return urls


async def _fetch_and_merge_player_stats(urls: list[str]) -> pd.DataFrame:
    """Fetch and merge player stats from multiple URLs."""
    all_df: list[pd.DataFrame] = []
    tasks = [_get_players_stats_df(url) for url in urls]
    results = await asyncio.gather(*tasks)
    all_df.extend(results)

    if not all_df:
        raise EmptyDataError("No player stats data found.")

    cleaned_dfs = [df.dropna(how="all", axis=0).dropna(how="all", axis=1) for df in all_df]

    merged_df = (
        pd.concat(cleaned_dfs, ignore_index=True)
        .drop_duplicates(
            subset=["lastname_initials", "first_name", "school", "matches_played", "sets_played"], keep="first"
        )
        .reset_index(drop=True)
    )

    return merged_df


def usports_vball_players(
    league: LeagueType,
    season_option: SeasonType = "regular",
) -> pd.DataFrame:
    """
    Fetch and process volleyball player statistics data from the USports website.

    Args:
        league: Gender of the players. Accepts 'm' or 'w' (case insensitive).
        season_option: The season option to fetch data for. Options are:
            - 'regular': Regular season statistics (default).
            - 'playoffs': Playoff season statistics.
            - 'championship': Championship season statistics.

    Returns:
        DataFrame: DataFrame containing processed player statistics with offensive,
                  defensive, and serve/receive stats.
    """
    gender = normalize_gender_arg(league)
    season_option = season_option.lower()  # type: ignore

    urls = _construct_player_urls(gender, season_option)

    logger.debug(f"Fetching {league} volleyball {season_option} player stats")

    df = asyncio.run(_fetch_and_merge_player_stats(urls))

    return df
