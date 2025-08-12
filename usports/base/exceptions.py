"""Custom exceptions for USports library."""


class USportsError(Exception):
    """Base exception for USports library."""

    pass


class DataFetchError(USportsError):
    """Raised when data fetching fails."""

    pass


class ParsingError(USportsError):
    """Raised when data parsing fails."""

    pass
