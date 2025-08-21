"""Functions:
- usports_soccer_teams: Fetch team statistics.
- usports_soccer_players: Fetch player statistics.
- usports_soccer_standings: Fetch team standings.

These functions return pandas DataFrames with the requested statistics.

Examples:
>>> from usports.soccer import usports_soccer_teams, usports_soccer_players, usports_soccer_standings

>>> men_team_stats = usports_soccer_teams('m', 'regular')
>>> women_playoff_stats = usports_soccer_teams('w', 'playoffs')
>>> men_championship_players = usports_soccer_players('m', 'championship')

>>> women_players = usports_soccer_players('w')
>>> men_standings = usports_soccer_standings('m')

Author:
    OJ Adeyemi

Date Created:
    August 2025
"""

from .player_stats import usports_soccer_players
from .standings import usports_soccer_standings
from .team_stats import usports_soccer_teams

__all__ = ["usports_soccer_teams", "usports_soccer_players", "usports_soccer_standings"]
