"""Custom exceptions for USports library."""


class USportsError(Exception):
    """Base exception for USports library."""

    pass


class NoStandingsError(USportsError):
    """Raised when standings requested for playoffs/championship."""

    pass


class InvalidLeagueError(USportsError):
    """Raised when invalid league specified."""

    pass


class DataFetchError(USportsError):
    """Raised when data fetching fails."""

    pass
