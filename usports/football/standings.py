"""Football standings"""

import asyncio
from typing import Any

import pandas as pd
from bs4 import BeautifulSoup, Tag

from usports.base.constants import BASE_URL, BS4_PARSER, DEFAULT_SCHOOL_CONFERENCES, SEASON
from usports.base.exceptions import DataFetchError
from usports.utils import (
    clean_text,
    convert_types,
    fetch_page_html,
    setup_logging,
)

from .constants import STANDINGS_COLUMNS_TYPE_MAPPING

logger = setup_logging()


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
        raise DataFetchError(f"Error fetching football standings: {e}") from e


# -------------------------------------------------------------------
# DataFrame Assembly
# -------------------------------------------------------------------
async def _get_standings_df(standings_url: str) -> pd.DataFrame:
    """Function to handle standings data into a pandas DataFrame"""
    standings_data = await _fetching_standings(standings_url)

    standings_df = pd.DataFrame(standings_data)

    if not standings_data or standings_df.empty:
        return pd.DataFrame(columns=STANDINGS_COLUMNS_TYPE_MAPPING.keys())  # type: ignore

    standings_df = convert_types(standings_df, STANDINGS_COLUMNS_TYPE_MAPPING)
    standings_df = standings_df.drop(columns=["ties"])
    standings_df["conference"] = standings_df["team_name"].map(DEFAULT_SCHOOL_CONFERENCES).astype(str)

    return standings_df


async def _fetch_standings() -> pd.DataFrame:
    """Fetch ONLY standings data - no team stats."""
    standings_url = f"{BASE_URL}/fball/{SEASON}/standings"

    logger.debug("FETCHING FOOTBALL STANDINGS")

    return await _get_standings_df(standings_url)


def usports_fball_standings() -> pd.DataFrame:
    """
    Get football standings (regular season only).

    Returns:
        DataFrame with columns: team_name, games_played, total_wins, total_losses,
        win_percentage, total_points, total_points_against, conference
    """
    return asyncio.run(_fetch_standings())
