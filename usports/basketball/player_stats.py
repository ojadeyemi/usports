import asyncio
from typing import Any, Literal

import pandas as pd
from bs4 import BeautifulSoup, Tag
from pandas import concat
from pandas.errors import EmptyDataError

from usports.utils import (
    clean_text,
    convert_types,
    fetch_page_html,
    get_sport_identifier,
    normalize_gender_arg,
    setup_logging,
    split_made_attempted,
    validate_season_option,
)
from usports.utils.constants import (
    BASE_URL,
    BASKETBALL_PLAYER_STATS_OFFSET,
    BS4_PARSER,
    PLAYER_SEASON_TOTALS_STATS_START_INDEX,
    SEASON_URLS,
)

from .constants import PLAYER_SORT_CATEGORIES, PLAYER_STATS_COLUMNS_TYPE_MAPPING

logger = setup_logging()


def _parse_player_stats_table(
    soup: BeautifulSoup, columns: list[str]
) -> list[dict[str, Any]]:
    """Parse player stats data from an HTML table."""
    table_data: list[dict[str, Any]] = []
    rows: list[Tag] = soup.find_all("tr")

    for row in rows:
        cols: list[Tag] = row.find_all("td")
        if len(cols) > 1:
            row_data = {}
            row_data["player_name"] = clean_text(cols[1].get_text())
            row_data["school"] = clean_text(cols[2].get_text())
            row_data["games_played"] = clean_text(cols[3].get_text())
            row_data["games_started"] = clean_text(cols[4].get_text())

            # Parse the rest of the columns
            for i, col_name in enumerate(columns):
                if i + BASKETBALL_PLAYER_STATS_OFFSET < len(cols):
                    value = clean_text(
                        cols[i + BASKETBALL_PLAYER_STATS_OFFSET].get_text()
                    )

                    if col_name.endswith("_made"):
                        made, attempted = split_made_attempted(value)
                        row_data[col_name] = made
                        row_data[col_name.replace("made", "attempted")] = attempted
                    else:
                        row_data[col_name] = value

            table_data.append(row_data)

    return table_data


def _merge_player_data(
    existing_data: list[dict[str, Any]], new_data: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Merge existing and new player data by (name, school, games_played)."""

    def key_func(d: dict[str, Any]) -> str:
        return f"{d['player_name']}_{d['school']}_{d['games_played']}"

    data_dict = {key_func(item): item for item in existing_data}

    for new_item in new_data:
        key = key_func(new_item)

        if key in data_dict:
            data_dict[key].update(new_item)
        else:
            data_dict[key] = new_item

    return list(data_dict.values())


async def _fetching_player_stats(url: str) -> list[dict[str, Any]]:
    try:
        tables_html = await fetch_page_html(url)

        all_data = []
        for i, column_mapping in enumerate(PLAYER_STATS_COLUMNS_TYPE_MAPPING):
            soup = BeautifulSoup(
                tables_html[i + PLAYER_SEASON_TOTALS_STATS_START_INDEX], BS4_PARSER
            )
            table_data = _parse_player_stats_table(
                soup, columns=list(column_mapping.keys())
            )
            all_data = _merge_player_data(all_data, table_data)

        return all_data

    except Exception as e:
        raise RuntimeError(f"Error fetching player_stats: {e}") from e


# -------------------------------------------------------------------
# DataFrame Assembly
# -------------------------------------------------------------------
async def _get_players_stats_df(stats_url: str) -> pd.DataFrame:
    """Fetch player stats from a page and return a cleaned DataFrame."""
    logger.debug(f"Fetching player stats on category: {stats_url[-5:]}")
    player_stats = await _fetching_player_stats(stats_url)
    df = pd.DataFrame(player_stats)

    # Split the player_name into (lastname_initials, first_name)
    if not df.empty:
        df[["lastname_initials", "first_name"]] = df["player_name"].str.split(
            " ", n=1, expand=True
        )

    combined_type_mapping = {
        "player_name": str,
        "school": str,
        "games_played": int,
        "games_started": int,
    }
    for mapping in PLAYER_STATS_COLUMNS_TYPE_MAPPING:
        combined_type_mapping.update(mapping)

    df = convert_types(df, combined_type_mapping)

    # Drop the old column
    df = df.drop(columns=["player_name"], errors="ignore")

    return df


def _construct_player_urls(gender: str, season_option: str) -> list[str]:
    sport = get_sport_identifier(gender)
    season = validate_season_option(season_option, SEASON_URLS)
    player_stats_url_template = (
        f"{BASE_URL}/{sport}/{season}/players?pos=sh&r=0&sort={{sort_category}}"
    )

    urls = [
        player_stats_url_template.format(sort_category=category)
        for category in PLAYER_SORT_CATEGORIES
    ]

    return urls


async def _fetch_and_merge_player_stats(urls: list[str]) -> pd.DataFrame:
    all_df = []
    tasks = [_get_players_stats_df(url) for url in urls]
    results = await asyncio.gather(*tasks)
    all_df.extend(results)

    if not all_df:
        raise EmptyDataError("No player stats data found.")

    merged_df = (
        concat(all_df, ignore_index=True).drop_duplicates().reset_index(drop=True)
    )

    return merged_df


def usport_players_stats(
    league: Literal["m", "men", "w", "women"],
    season_option: Literal["regular", "playoffs", "championship"] = "regular",
) -> pd.DataFrame:
    """
    Fetch and process player statistics data from the USports website.

    Args:
        league (str): Gender of the players. Accepts 'men', 'women', 'm', or 'w' (case insensitive).
        season_option (str): The season option to fetch data for. Options are:
            - 'regular': Regular season statistics (default).
            - 'playoffs': Playoff season statistics.
            - 'championship': Championship season statistics.

    Returns:
        DataFrame: DataFrame containing processed player statistics.
    """

    gender = normalize_gender_arg(league)
    season_option = season_option.lower()  # type: ignore

    urls = _construct_player_urls(gender, season_option)

    # Actually fetch the DataFrame
    df = asyncio.run(_fetch_and_merge_player_stats(urls))

    return df
