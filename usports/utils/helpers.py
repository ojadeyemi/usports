import re
import unicodedata
from typing import Literal

import httpx
from bs4 import BeautifulSoup
from pandas import DataFrame

from .constants import BS4_PARSER, TIMEOUT
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
        raise ValueError(f"No <table> elements found at {url}")

    return [str(table).replace("\n", "").replace("\t", "") for table in tables]


def split_made_attempted(value: str) -> tuple[int, int]:
    """Split shots into made and attempted (e.g., '12-20' to 12 and 20)."""
    try:
        made, attempted = value.split("-")
        return int(made), int(attempted)

    except ValueError as e:
        raise ValueError(f"Error splitting made and attempted values from '{value}': {e}") from e


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
    """Convert DataFrame columns to specified types."""
    for column, dtype in type_mapping.items():
        if dtype in [int, float]:
            df[column] = df[column].astype(str).replace("-", "0")

        df[column] = df[column].astype(dtype)

    return df


def get_sport_identifier(gender: str) -> str:
    """Get the sport identifier based on gender."""
    if gender == "men":
        return "mbkb"

    if gender == "women":
        return "wbkb"

    raise ValueError("Argument must be 'men' or 'women'")


def normalize_gender_arg(arg: Literal["m", "men", "w", "women"]) -> str:
    """Normalize the 'arg' input to 'men' or 'women'."""
    arg_lower = arg.lower()

    if arg_lower in ["m", "men"]:
        return "men"

    if arg_lower in ["w", "women"]:
        return "women"

    raise ValueError("The argument 'arg' should be either 'men', 'm', 'w', or 'women'")


def validate_season_option(season_option: str, available_options: dict) -> str:
    """Validate the season option and return the corresponding URL fragment."""
    season_option_lower = season_option.lower()
    if season_option_lower not in available_options:
        options = ", ".join(available_options.keys())
        raise ValueError(f"Invalid season_option: {season_option}. Must be one of {options}")

    return available_options[season_option_lower]
