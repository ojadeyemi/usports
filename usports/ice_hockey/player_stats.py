import asyncio
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup, Tag
from pandas.errors import EmptyDataError

from usports.base.constants import (
    BASE_URL,
    BS4_PARSER,
    ICE_HOCKEY,
    PLAYER_SEASON_TOTALS_STATS_START_INDEX,
    get_season_urls,
)
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
    GOALIES_SORT_CATEGORIES,
    ICE_HOCKEY_GOALIE_STATS_COLUMNS_TYPE_MAPPING,
    ICE_HOCKEY_PLAYER_STATS_COLUMNS_TYPE_MAPPING,
    SKATERS_SORT_CATEGORIES,
)

logger = setup_logging()


def _get_sport_identifier(league: str) -> str:
    if league == "m":
        return "mice"
    if league == "w":
        return "wice"
    raise ValueError(f"Invalid league: {league}. Must be one of 'men' or 'women'")


def _parse_player_stats_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    table_data: list[dict[str, Any]] = []
    rows: list[Tag] = soup.find_all("tr")  # type: ignore

    for row in rows:
        cols: list[Tag] = row.find_all("td")  # type: ignore

        if len(cols) > 1:
            row_data = {}
            row_data["player_name"] = clean_text(cols[1].get_text())
            row_data["school"] = clean_text(cols[2].get_text())

            for i, col_name in enumerate(columns):
                col_index = i + PLAYER_SEASON_TOTALS_STATS_START_INDEX
                if col_index < len(cols):
                    value = clean_text(cols[col_index].get_text())
                    if col_name == "minutes_played" and ":" in value:
                        minutes, seconds = value.split(":")
                        row_data[col_name] = float(minutes) + float(seconds) / 60
                    else:
                        row_data[col_name] = value

            table_data.append(row_data)

    return table_data


async def _fetching_player_stats(url: str) -> list[dict[str, Any]]:
    try:
        tables_html = await fetch_page_html(url)
        soup = BeautifulSoup(tables_html[0], BS4_PARSER)

        return _parse_player_stats_table(soup, list(ICE_HOCKEY_PLAYER_STATS_COLUMNS_TYPE_MAPPING.keys()))

    except Exception as e:
        raise DataFetchError(f"Error fetching player stats: {e}") from e


async def _fetching_goalie_stats(url: str) -> list[dict[str, Any]]:
    try:
        tables_html = await fetch_page_html(url)
        soup = BeautifulSoup(tables_html[1], BS4_PARSER)

        return _parse_player_stats_table(soup, list(ICE_HOCKEY_GOALIE_STATS_COLUMNS_TYPE_MAPPING.keys()))

    except Exception as e:
        raise RuntimeError(f"Error fetching goalie stats: {e}") from e


async def _get_player_stats_df(players_stats_url: str) -> pd.DataFrame:
    """Fetch player stats from a page and return cleaned Dataframe"""
    logger.debug(f"Fetching player stats on category: {players_stats_url[-10:]}")

    player_stats = await _fetching_player_stats(players_stats_url)
    df_players = pd.DataFrame(player_stats)

    player_type_mapping = {"player_name": str, "school": str, "role": str}
    player_type_mapping.update(ICE_HOCKEY_PLAYER_STATS_COLUMNS_TYPE_MAPPING)

    if not df_players.empty:
        df_players["role"] = "skater"
        df_players = convert_types(df_players, player_type_mapping)
    else:
        df_players = pd.DataFrame(columns=list(player_type_mapping.keys()))

    if "player_name" in df_players.columns:
        df_players[["lastname_initials", "first_name"]] = df_players["player_name"].str.split(" ", n=1, expand=True)

    df_players = df_players.drop(columns=["player_name"], errors="ignore")

    return df_players


async def _get_goalie_stats_df(goalies_stats_url: str) -> pd.DataFrame:
    """Fetch goalie stats from a page and return cleaned Dataframe"""
    logger.debug(f"Fetching goalie stats on category: {goalies_stats_url[-10:]}")

    goalie_stats = await _fetching_goalie_stats(goalies_stats_url)
    df_goalies = pd.DataFrame(goalie_stats)

    goalie_type_mapping = {"player_name": str, "school": str, "role": str}
    goalie_type_mapping.update(ICE_HOCKEY_GOALIE_STATS_COLUMNS_TYPE_MAPPING)

    if not df_goalies.empty:
        df_goalies["role"] = "goalie"
        df_goalies = convert_types(df_goalies, goalie_type_mapping)
    else:
        df_goalies = pd.DataFrame(columns=list(goalie_type_mapping.keys()))

    if "player_name" in df_goalies.columns:
        for index, player_name in df_goalies["player_name"].items():
            try:
                if isinstance(player_name, str) and " " in player_name:
                    split_name = player_name.split(" ", 1)
                else:
                    split_name = [player_name, ""]
            except Exception:
                split_name = ["Unknown", "Unknown"]

            df_goalies.at[index, "lastname_initials"] = split_name[0]
            df_goalies.at[index, "first_name"] = split_name[1] if len(split_name) > 1 else "Unknown"

    df_goalies = df_goalies.drop(columns=["player_name"], errors="ignore")

    return df_goalies


def _construct_urls(gender: str, season_option: str) -> tuple[list[str], list[str]]:
    sport = _get_sport_identifier(gender)
    season_urls = get_season_urls(ICE_HOCKEY)
    season = validate_season_option(season_option, season_urls)

    player_stats_url_template = f"{BASE_URL}/{sport}/{season}/players?sort={{sort_category}}&pos=sk"
    goalie_stats_url_template = f"{BASE_URL}/{sport}/{season}/players?sort={{sort_category}}&pos=g"

    player_stats_urls = [player_stats_url_template.format(sort_category=sort) for sort in SKATERS_SORT_CATEGORIES]
    goalie_stats_urls = [goalie_stats_url_template.format(sort_category=sort) for sort in GOALIES_SORT_CATEGORIES]

    return player_stats_urls, goalie_stats_urls


async def _fetch_and_merge_player_stats(player_stats_urls: list[str], goalie_stats_urls: list[str]) -> pd.DataFrame:
    player_task = [_get_player_stats_df(url) for url in player_stats_urls]
    goalie_task = [_get_goalie_stats_df(url) for url in goalie_stats_urls]

    player_results = await asyncio.gather(*player_task)
    goalie_results = await asyncio.gather(*goalie_task)

    all_df = player_results + goalie_results

    if not all_df:
        raise EmptyDataError("No data fetched from the URLs.")

    cleaned_dfs = [df.dropna(how="all", axis=0).dropna(how="all", axis=1) for df in all_df]

    final_df = pd.concat(cleaned_dfs, ignore_index=True).drop_duplicates(
        subset=["lastname_initials", "first_name", "school", "games_played", "role"]
    )

    final_df.fillna(0, inplace=True)

    return final_df


def usports_ice_hockey_players(
    league: LeagueType,
    season_option: SeasonType = "regular",
) -> pd.DataFrame:
    """
    Fetch and process ice hockey players statistics data from the USPORTS website.

    Args:
        league (str): Gender of the players. Accepts 'm', or 'w' (case insensitive).
        season_option (str): The season option to fetch data for. Options are:
            - 'regular': Regular season statistics (default).
            - 'playoffs': Playoff season statistics.
            - 'championship': Championship season statistics.

    Returns:
        DataFrame: DataFrame containing processed player statistics.
    """
    g = normalize_gender_arg(league)
    season_option = season_option.lower()  # type: ignore

    player_urls, goalie_urls = _construct_urls(g, season_option)

    logger.debug(f"Fetching league:{league}, season:{season_option} ice hockey players\n")

    df = asyncio.run(_fetch_and_merge_player_stats(player_urls, goalie_urls))

    return df
