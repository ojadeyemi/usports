"""Base module for USports library.

This module contains the base exceptions, constants and types used in the library.
"""

from .exceptions import DataFetchError, ParsingError, USportsError
from .types import ConferenceType, LeagueType, SeasonType, SportCode

__all__ = [
    "USportsError",
    "ParsingError",
    "DataFetchError",
    "SeasonType",
    "LeagueType",
    "SportCode",
    "ConferenceType",
]
