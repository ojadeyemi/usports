"""
Utilities Package

This package provides utility functions for processing player and team statistics data.

Modules:
- helpers: General functions to assist with data processing.
  - clean_text: Remove extra spaces and newlines from text.
  - convert_types: Convert DataFrame columns to specified types.
  - fetch_table_html: Retrieve HTML content of a table.
  - split_made_attempted: Split a string into made and attempted values.

- headers: Provides HTTP header configurations.
  - get_random_header: Retrieve a random HTTP header from predefined options.

- logging_config: Setup and configure logging.
  - setup_logging: Configure logging with customizable settings.
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
