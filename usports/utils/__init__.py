"""Utilities package for the USports library.

This package provides utility functions for processing player and team statistics data.
"""

from .headers import get_random_header
from .helpers import (
    _merge_team_data,
    clean_text,
    convert_types,
    fetch_page_html,
    normalize_gender_arg,
    split_made_attempted,
    validate_season_option,
)
from .logger import setup_logging

__all__ = [
    "_merge_team_data",
    "clean_text",
    "convert_types",
    "fetch_page_html",
    "get_random_header",
    "setup_logging",
    "split_made_attempted",
    "normalize_gender_arg",
    "validate_season_option",
]
