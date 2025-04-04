"""Functions:
- usports_fball_teams: Fetch team statistics.
- usports_fball_players: Fetch player statistics.

These functions return pandas DataFrames with the requested statistics.

Examples:
>>> from usports.football import usports_fball_teams, usports_fball_players

>>> regular_season_team_stats = usports_fball_teams('regular_season')
>>> playoff_team_stats = usports_fball_teams('playoffs')
>>> championship_team_stats = usports_fball_teams('championship')

>>> regular_season_player_stats = usports_fball_players('regular_season')
>>> playoff_player_stats = usports_fball_players('playoffs')
>>> championship_player_stats = usports_fball_players('championship')

Author:
    OJ Adeyemi

Date Created:
     March 21, 2025
"""

from .player_stats import usports_fball_players
from .team_stats import usports_fball_teams

__all__ = ["usports_fball_teams", "usports_fball_players"]
