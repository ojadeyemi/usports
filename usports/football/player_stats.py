"""Football player stats"""

import asyncio
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup, Tag
from pandas.errors import EmptyDataError

from usports.base.constants import BASE_URL, BS4_PARSER, FOOTBALL, FOOTBALL_PLAYER_STATS_OFFSET, get_season_urls
from usports.base.exceptions import DataFetchError
from usports.base.types import SeasonType
from usports.utils import (
    clean_text,
    convert_types,
    fetch_page_html,
    setup_logging,
    validate_season_option,
)

from .constants import FBALL_PLAYER_STATS_COLUMNS_TYPE_MAPPING, PLAYER_SORT_CATEGORIES

logger = setup_logging()


def _parse_player_stats_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse player stats data from an HTML table for football."""
    table_data: list[dict[str, Any]] = []
    rows: list[Tag] = soup.find_all("tr")  # type: ignore

    for row in rows:
        cols: list[Tag] = row.find_all("td")  # type: ignore
        if len(cols) > 1:
            row_data = {
                "player_name": clean_text(cols[1].get_text()),
                "school": clean_text(cols[2].get_text()),
            }

            for i, col_name in enumerate(columns):
                col_index = i + FOOTBALL_PLAYER_STATS_OFFSET
                if col_index < len(cols):
                    value = clean_text(cols[col_index].get_text())
                    row_data[col_name] = value

            table_data.append(row_data)

    return table_data


def _merge_player_data(existing_data: list[dict[str, Any]], new_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge existing and new player data by (name, school)."""

    def key_func(d: dict[str, Any]) -> str:
        return f"{d['player_name']}_{d['school']}"

    data_dict = {key_func(item): item for item in existing_data}

    for new_item in new_data:
        key = key_func(new_item)

        if key in data_dict:
            data_dict[key].update(new_item)
        else:
            data_dict[key] = new_item

    return list(data_dict.values())


async def _fetching_player_stats(url: str) -> list[dict[str, Any]]:
    """Fetch and parse football player stats from a URL."""
    try:
        tables_html = await fetch_page_html(url)

        all_data = []
        for i, column_mapping in enumerate(FBALL_PLAYER_STATS_COLUMNS_TYPE_MAPPING):
            soup = BeautifulSoup(tables_html[i], BS4_PARSER)
            table_data = _parse_player_stats_table(soup, columns=list(column_mapping.keys()))
            all_data = _merge_player_data(all_data, table_data)

        return all_data

    except Exception as e:
        raise DataFetchError(f"Error fetching player_stats: {e}") from e


# -------------------------------------------------------------------
# DataFrame Assembly
# -------------------------------------------------------------------
async def _get_players_stats_df(stats_url: str) -> pd.DataFrame:
    """Fetch football player stats from a page and return a cleaned DataFrame."""
    logger.debug(f"Fetching football player stats from: {stats_url[-5:]}")

    player_stats = await _fetching_player_stats(stats_url)

    # Define type mappings for football stats
    combined_type_mapping = {
        "player_name": str,
        "school": str,
        "games_played": int,
    }
    for mapping in FBALL_PLAYER_STATS_COLUMNS_TYPE_MAPPING:
        combined_type_mapping.update(mapping)

    df = pd.DataFrame(player_stats)

    if not player_stats or df.empty:
        return pd.DataFrame(columns=combined_type_mapping.keys())  # type: ignore

    # Remove rows where player_name is empty or null
    df = df[df["player_name"].notna() & (df["player_name"].str.strip() != "")]

    if "player_name" in df.columns:
        df[["lastname_initials", "first_name"]] = df["player_name"].str.split(" ", n=1, expand=True)

    df = convert_types(df, combined_type_mapping)

    # Drop the old column
    df = df.drop(columns=["player_name"], errors="ignore")

    return df


def _construct_player_urls(season: SeasonType) -> list[str]:
    season_urls = get_season_urls(FOOTBALL)
    season_url = validate_season_option(season, season_urls)
    player_stats_url_template = f"{BASE_URL}/fball/{season_url}/players?pos={{sort_position}}&sort={{sort_category}}"

    urls = [
        player_stats_url_template.format(sort_position=position, sort_category=category)
        for position, category in PLAYER_SORT_CATEGORIES
    ]

    return urls


async def _fetch_and_merge_player_stats(urls: list[str]) -> pd.DataFrame:
    all_df: list[pd.DataFrame] = []
    tasks = [_get_players_stats_df(url) for url in urls]
    results = await asyncio.gather(*tasks)
    all_df.extend(results)

    if not all_df:
        raise EmptyDataError("No player stats data found.")

    # Remove rows that are all NA from each DataFrame
    cleaned_dfs = [df.dropna(how="all", axis=0).dropna(how="all", axis=1) for df in all_df]

    merged_df = pd.concat(cleaned_dfs, ignore_index=True).drop_duplicates().reset_index(drop=True)
    return merged_df


def usports_fball_players(season_option: SeasonType = "regular") -> pd.DataFrame:
    """
    Get football player stats for a given season.

    Args:
        season_option: 'regular', 'playoffs', or 'championship'

    Returns:
        DataFrame containing player stats
    """
    season_option = season_option.lower()  # type: ignore
    urls = _construct_player_urls(season_option)
    df = asyncio.run(_fetch_and_merge_player_stats(urls))
    return df
