import asyncio
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup, Tag

from usports.base.constants import BASE_URL, BS4_PARSER, SOCCER, get_current_season
from usports.base.exceptions import DataFetchError
from usports.base.types import LeagueType
from usports.utils import (
    clean_text,
    convert_types,
    fetch_page_html,
    normalize_gender_arg,
    setup_logging,
)
from usports.utils.helpers import get_conference_mapping_for_league

from .constants import SOCCER_STANDINGS_COLUMNS_TYPE_MAPPING

logger = setup_logging()


def _get_sport_identifier(league: str) -> str:
    """Get the sport identifier for soccer based on gender."""
    if league == "m":
        return "msoc"
    if league == "w":
        return "wsoc"
    raise ValueError(f"Invalid league: {league}. Must be 'm' or 'w'")


def _parse_standings_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse standings data from an HTML table"""
    table_data: list[dict[str, Any]] = []
    rows: list[Tag] = soup.find_all("tr")  # type: ignore

    for row in rows:
        row_data = {}

        team_name_th = row.find("th", class_="team-name")
        if team_name_th:
            team_name_tag = team_name_th.find("a")  # type: ignore
            if team_name_tag:
                team_name = clean_text(team_name_tag.get_text())  # type: ignore
                row_data["team_name"] = team_name

        cols: list[Tag] = row.find_all("td")  # type: ignore
        if cols:
            for col, column_name in zip(cols, columns):
                row_data[column_name] = clean_text(col.get_text())

            table_data.append(row_data)

    return table_data


async def _fetching_standings(url: str) -> list[dict[str, Any]]:
    """Fetch standings data from a given URL."""
    try:
        tables_html = await fetch_page_html(url)

        all_data = []
        for table_html in tables_html:
            soup = BeautifulSoup(table_html, BS4_PARSER)
            column_names = list(SOCCER_STANDINGS_COLUMNS_TYPE_MAPPING.keys())[1:]
            standings_data = _parse_standings_table(soup, column_names)
            all_data.extend(standings_data)

        return all_data

    except Exception as e:
        raise DataFetchError(f"Error fetching soccer standings: {e}") from e


async def _get_standings_df(standings_url: str) -> pd.DataFrame:
    """Process standings data into a pandas DataFrame"""
    standings_data = await _fetching_standings(standings_url)
    standings_df = pd.DataFrame(standings_data)

    if not standings_data or standings_df.empty:
        return pd.DataFrame(columns=SOCCER_STANDINGS_COLUMNS_TYPE_MAPPING.keys())  # type: ignore

    standings_df = convert_types(standings_df, SOCCER_STANDINGS_COLUMNS_TYPE_MAPPING)

    standings_df = standings_df.dropna(subset=["team_name"])
    standings_df = standings_df[standings_df["team_name"] != "nan"]

    conference_map = get_conference_mapping_for_league(SOCCER)
    standings_df["conference"] = standings_df["team_name"].map(conference_map).astype(str)

    return standings_df


async def _fetch_standings(league: LeagueType) -> pd.DataFrame:
    """Fetch soccer standings data."""
    sport = _get_sport_identifier(normalize_gender_arg(league))
    season = get_current_season(SOCCER)
    standings_url = f"{BASE_URL}/{sport}/{season}/standings"

    logger.debug(f"FETCHING {league.upper()} SOCCER STANDINGS")

    return await _get_standings_df(standings_url)


def usports_soccer_standings(league: LeagueType) -> pd.DataFrame:
    """
    Get soccer standings (regular season only).

    Args:
        league: 'm' or 'w'

    Returns:
        DataFrame with columns: team_name, games_played, total_wins, total_losses,
        ties, goals_for, goals_against, points, conference
    """
    return asyncio.run(_fetch_standings(league))
