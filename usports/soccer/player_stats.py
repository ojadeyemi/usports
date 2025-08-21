"""Soccer player stats"""

import asyncio
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup, Tag
from pandas.errors import EmptyDataError

from usports.base.constants import BASE_URL, BS4_PARSER, SOCCER, get_season_urls
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

from .constants import (
    FIELD_PLAYER_SORT_CATEGORIES,
    GOALIE_SORT_CATEGORIES,
    SOCCER_PLAYER_STATS_COLUMNS_TYPE_MAPPING,
)
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
            row_data["games_played"] = clean_text(cols[3].get_text())

            start_index = 4  # Start after name, school, games_played
            for i, col_name in enumerate(columns):
                col_index = i + start_index
                if col_index < len(cols):
                    value = clean_text(cols[col_index].get_text())

                    # Handle minutes format MM:SS
                    if col_name == "goalie_minutes_played" and ":" in value:
                        parts = value.split(":")
                        value = str(int(parts[0]) + float(parts[1]) / 60)

                    # Handle shutouts format (e.g., "2/0" -> just take the first number)
                    elif col_name == "goalie_shutouts" and "/" in value:
                        value = value.split("/")[0]

                    row_data[col_name] = value

            table_data.append(row_data)

    return table_data


async def _fetch_goalie_stats(url: str) -> list[dict[str, Any]]:
    """Fetch only goalie tables (last 2 tables)"""
    try:
        tables_html = await fetch_page_html(url)

        # Only get the last 2 tables (goalie tables)
        goalie_tables = tables_html[-2:]

        all_data = []

        # Process goalie tables (indices 3 and 4 in SOCCER_PLAYER_STATS_COLUMNS_TYPE_MAPPING)
        for i, table_html in enumerate(goalie_tables):
            mapping_index = i + 3  # Maps to indices 3 and 4 in the mapping
            if mapping_index < len(SOCCER_PLAYER_STATS_COLUMNS_TYPE_MAPPING):
                soup = BeautifulSoup(table_html, BS4_PARSER)
                column_mapping = SOCCER_PLAYER_STATS_COLUMNS_TYPE_MAPPING[mapping_index]
                table_data = _parse_player_stats_table(soup, list(column_mapping.keys()))
                all_data.extend(table_data)

        return all_data

    except Exception as e:
        raise DataFetchError(f"Error fetching goalie stats: {e}") from e


async def _fetch_field_player_stats(url: str) -> list[dict[str, Any]]:
    """Fetch only field player tables (tables -5, -4, -3)"""
    try:
        tables_html = await fetch_page_html(url)

        # Get tables -5, -4, -3 (the three field player tables)
        field_tables = tables_html[-5:-2]

        all_data = []

        # Process field player tables (indices 0, 1, 2 in SOCCER_PLAYER_STATS_COLUMNS_TYPE_MAPPING)
        for i, table_html in enumerate(field_tables):
            if i < 3:  # Only process first 3 mappings (field player stats)
                soup = BeautifulSoup(table_html, BS4_PARSER)
                column_mapping = SOCCER_PLAYER_STATS_COLUMNS_TYPE_MAPPING[i]
                table_data = _parse_player_stats_table(soup, list(column_mapping.keys()))
                all_data.extend(table_data)

        return all_data

    except Exception as e:
        raise DataFetchError(f"Error fetching field player stats: {e}") from e


def _merge_player_data(existing_data: list[dict[str, Any]], new_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge existing and new player data by (player_name, school, games_played)."""

    def key_func(d: dict[str, Any]) -> str:
        return f"{d['player_name']}_{d['school']}_{d['games_played']}"

    data_dict = {key_func(item): item for item in existing_data}

    for new_item in new_data:
        key = key_func(new_item)

        if key in data_dict:
            existing_item = data_dict[key]
            for k, v in new_item.items():
                if v not in [None, ""] and k != "position":
                    existing_item[k] = v
        else:
            data_dict[key] = new_item

    return list(data_dict.values())


async def _get_goalie_stats_df(goalie_urls: list[str]) -> tuple[pd.DataFrame, set[str]]:
    """Fetch goalie stats and return DataFrame and set of goalie identifiers."""
    all_goalie_data: list[dict[str, Any]] = []
    goalie_names: set[str] = set()

    for url in goalie_urls:
        try:
            goalie_data = await _fetch_goalie_stats(url)
            for player in goalie_data:
                player["position"] = "goalie"
                key = f"{player['player_name']}_{player['school']}"
                goalie_names.add(key)
            all_goalie_data = _merge_player_data(all_goalie_data, goalie_data)
        except Exception as e:
            logger.debug(f"Error fetching goalie stats from {url}: {e}")
            continue

    if all_goalie_data:
        df = pd.DataFrame(all_goalie_data)
    else:
        df = pd.DataFrame()

    return df, goalie_names


async def _get_field_players_stats_df(field_urls: list[str], goalie_names: set[str]) -> pd.DataFrame:
    """Fetch field player stats."""
    all_field_data: list[dict[str, Any]] = []

    for url in field_urls:
        try:
            player_data = await _fetch_field_player_stats(url)
            for player in player_data:
                key = f"{player['player_name']}_{player['school']}"
                # Mark position based on whether they're in goalie set (handles edge cases)
                if key in goalie_names:
                    player["position"] = "goalie"
                else:
                    player["position"] = "field"
            all_field_data = _merge_player_data(all_field_data, player_data)
        except Exception as e:
            logger.debug(f"Error fetching field player stats from {url}: {e}")
            continue

    if all_field_data:
        df = pd.DataFrame(all_field_data)
    else:
        df = pd.DataFrame()

    return df


def _construct_urls(gender: str, season_option: str) -> tuple[list[str], list[str]]:
    """Construct separate URLs for goalies and field players."""
    sport = _get_sport_identifier(gender)
    season_urls = get_season_urls(SOCCER)
    season = validate_season_option(season_option, season_urls)

    player_stats_url_template = f"{BASE_URL}/{sport}/{season}/players?pos={{position}}&sort={{sort_category}}"

    goalie_urls = [
        player_stats_url_template.format(position=position, sort_category=category)
        for position, category in GOALIE_SORT_CATEGORIES
    ]

    field_urls = [
        player_stats_url_template.format(position=position, sort_category=category)
        for position, category in FIELD_PLAYER_SORT_CATEGORIES
    ]

    return goalie_urls, field_urls


async def _fetch_and_merge_player_stats(goalie_urls: list[str], field_urls: list[str]) -> pd.DataFrame:
    """Fetch and merge player stats, processing goalies first."""

    # First, fetch goalie stats and identify all goalies
    goalie_df, goalie_names = await _get_goalie_stats_df(goalie_urls)

    # Then fetch field player stats
    field_df = await _get_field_players_stats_df(field_urls, goalie_names)

    # Combine dataframes
    all_dfs = []
    if not goalie_df.empty:
        all_dfs.append(goalie_df)
    if not field_df.empty:
        all_dfs.append(field_df)

    if not all_dfs:
        raise EmptyDataError("No player stats data found.")

    # Merge all data
    merged_df = pd.concat(all_dfs, ignore_index=True)

    # Drop duplicates, keeping first occurrence (preserves goalie designation)
    merged_df = merged_df.drop_duplicates(subset=["player_name", "school", "games_played"], keep="first").reset_index(
        drop=True
    )

    # Clean up - remove rows that are all NA
    merged_df = merged_df.dropna(how="all", axis=0).dropna(how="all", axis=1)

    return merged_df


async def _get_players_stats_df_final(goalie_urls: list[str], field_urls: list[str]) -> pd.DataFrame:
    """Final processing of player stats DataFrame."""

    df = await _fetch_and_merge_player_stats(goalie_urls, field_urls)

    if df.empty:
        return pd.DataFrame()

    # Define combined type mapping
    combined_type_mapping = {
        "player_name": str,
        "school": str,
        "position": str,
        "games_played": int,
    }

    for mapping in SOCCER_PLAYER_STATS_COLUMNS_TYPE_MAPPING:
        combined_type_mapping.update(mapping)

    # Split player name
    if "player_name" in df.columns:
        df[["lastname_initials", "first_name"]] = df["player_name"].str.split(" ", n=1, expand=True)

    # Convert types
    df = convert_types(df, combined_type_mapping)

    # Drop the old column
    df = df.drop(columns=["player_name"], errors="ignore")

    # Fill NaN values with 0 for numeric columns
    numeric_columns = [
        col for col, dtype in combined_type_mapping.items() if dtype in [int, float] and col in df.columns
    ]
    df[numeric_columns] = df[numeric_columns].fillna(0)

    return df


def usports_soccer_players(
    league: LeagueType,
    season_option: SeasonType = "regular",
) -> pd.DataFrame:
    """
    Fetch and process soccer player statistics data from the USports website.

    Args:
        league: Gender of the players. Accepts 'm' or 'w' (case insensitive).
        season_option: The season option to fetch data for. Options are:
            - 'regular': Regular season statistics (default).
            - 'playoffs': Playoff season statistics.
            - 'championship': Championship season statistics.

    Returns:
        DataFrame: DataFrame containing processed player statistics with scoring,
                  shooting, misc, and goalkeeper stats. Players are marked as either
                  'goalie' or 'field' in the position column.
    """
    gender = normalize_gender_arg(league)
    season_option = season_option.lower()  # type: ignore

    goalie_urls, field_urls = _construct_urls(gender, season_option)

    logger.debug(f"Fetching {league} soccer {season_option} player stats")

    df = asyncio.run(_get_players_stats_df_final(goalie_urls, field_urls))

    return df
