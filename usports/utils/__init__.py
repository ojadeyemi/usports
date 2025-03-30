"""
Utilities Package

This package provides utility functions for processing player and team statistics data.

Modules:
- helpers: General functions for data processing
  - clean_text: Remove extra spaces and newlines
  - convert_types: Convert DataFrame columns to correct types
  - fetch_page_html: Retrieve HTML content from a URL
  - split_made_attempted: Split "made-attempted" format into separate values
  - _merge_team_data: Combine team stats from multiple sources
  - normalize_gender_arg: Standardize gender parameter input
  - validate_season_option: Ensure season parameter is valid

- headers: HTTP header configurations
  - get_random_header: Get random HTTP header to avoid blocking

- logging: Logging setup and configuration
  - setup_logging: Configure logging with custom settings
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
