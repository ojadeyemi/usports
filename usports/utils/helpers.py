import re
import unicodedata
from typing import Any, Literal

import httpx
import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame

from usports.base.constants import BS4_PARSER, DEFAULT_SCHOOL_CONFERENCES, LEAGUE_CONFERENCE_OVERRIDES, TIMEOUT
from usports.base.exceptions import DataFetchError, ParsingError

from .headers import get_random_header


async def fetch_page_html(url: str) -> list[str]:
    """
    Fetch the HTML of all  tables from a page using HTTPX.
    Returns a list of cleaned HTML strings for each table.
    """
    headers = get_random_header()
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, BS4_PARSER)
    tables = soup.find_all("table")

    if not tables:
        raise DataFetchError(f"No <table> elements found at {url}")

    return [str(table).replace("\n", "").replace("\t", "") for table in tables]


def split_made_attempted(value: str) -> tuple[int, int]:
    """
    Split a string of the form 'made-attempted' into a tuple of two integers.
    Handles cases where multiple dashes appear (e.g., '1--31' is normalized to '1-31').
    """

    # Normalize the value by replacing multiple dashes with a single dash.
    normalized_value = re.sub(r"-+", "-", value)
    try:
        made, attempted = normalized_value.split("-")
        return int(made), int(attempted)
    except (ValueError, TypeError) as e:
        raise ParsingError(f"Error splitting made and attempted values from '{value}': {e}") from e


def clean_text(text: str) -> str:
    """Remove non-ASCII characters and extra spaces from text."""
    # Normalize Unicode characters to a standard form
    normalized_text = unicodedata.normalize("NFKC", text)

    # Remove non-printable and non-ASCII characters using regex
    sanitized_text = re.sub(r"[^\x00-\x7F]", "", normalized_text)

    # Remove unwanted whitespace characters
    cleaned_text = re.sub(r"[\n\t]+", " ", sanitized_text)
    cleaned_text = re.sub(r"\s{2,}", " ", cleaned_text)

    return cleaned_text.strip()


def convert_types(df: DataFrame, type_mapping: dict[str, type]) -> DataFrame:
    """Convert DataFrame columns to specified types, handling missing values correctly."""
    for column, dtype in type_mapping.items():
        if column in df.columns:
            if dtype in [int, float]:
                df[column] = df[column].astype(str).replace(["-", "nan", ""], "0")

                # Convert to numeric type, forcing errors to NaN before casting
                df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

            df[column] = df[column].astype(dtype)

    return df


def normalize_gender_arg(arg: Literal["m", "men", "w", "women"]) -> str:
    """Normalize the 'arg' input to 'men' or 'women'."""
    arg_lower = arg.lower()

    if arg_lower in ["m", "men"]:
        return "m"

    if arg_lower in ["w", "women"]:
        return "w"

    raise ValueError("The argument 'arg' should be either 'men', 'm', 'w', or 'women'")


def validate_season_option(season_option: str, available_options: dict) -> str:
    """Validate the season option and return the corresponding URL fragment."""
    season_option_lower = season_option.lower()
    if season_option_lower not in available_options:
        options = ", ".join(available_options.keys())
        raise ValueError(f"Invalid season_option: {season_option}. Must be one of {options}")

    return available_options[season_option_lower]


def _merge_team_data(existing_data: list[dict[str, Any]], new_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge existing and new team data stats"""

    def key_func(d: dict[str, Any]) -> str:
        return f"{d['team_name']}"

    data_dict = {key_func(item): item for item in existing_data}

    for new_item in new_data:
        key = key_func(new_item)

        if key in data_dict:
            data_dict[key].update(new_item)
        else:
            data_dict[key] = new_item

    return list(data_dict.values())


def get_conference_mapping_for_league(league: str) -> dict[str, str]:
    """Maps team name (school) to conference where school plays for specific league"""
    mapping = DEFAULT_SCHOOL_CONFERENCES.copy()
    overrides = LEAGUE_CONFERENCE_OVERRIDES.get(league, {})
    mapping.update(overrides)

    return mapping
