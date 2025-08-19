"""Functions:
- usports_vball_teams: Fetch team statistics.
- usports_vball_players: Fetch player statistics.
- usports_vball_standings: Fetch team standings.

These functions return pandas DataFrames with the requested statistics.

Examples:
>>> from usports.volleyball import usports_vball_teams, usports_vball_players, usports_vball_standings

>>> men_team_stats = usports_vball_teams('m', 'regular')
>>> women_playoff_stats = usports_vball_teams('w', 'playoffs')
>>> men_championship_players = usports_vball_players('m', 'championship')

>>> women_players = usports_vball_players('w')
>>> men_standings = usports_vball_standings('m')
>>> women_standings = usports_vball_standings('w')

Author:
    OJ Adeyemi

Date Created:
    August 2025
"""

from .player_stats import usports_vball_players
from .standings import usports_vball_standings
from .team_stats import usports_vball_teams

__all__ = ["usports_vball_teams", "usports_vball_players", "usports_vball_standings"]
