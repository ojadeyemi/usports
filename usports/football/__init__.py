"""Functions:
- usports_football_team_stats: Fetch team statistics.
- usports_football_players_stats: Fetch player statistics.

These functions return pandas DataFrames with the requested statistics.

Examples:
>>> from usports.football import usports_football_team_stats, usports_football_players_stats

>>> regular_season_team_stats = usports_football_team_stats('regular_season')
>>> playoff_team_stats = usports_football_team_stats('playoffs')
>>> championship_team_stats = usports_football_team_stats('championship')

>>> regular_season_player_stats = usports_football_players_stats('regular_season')
>>> playoff_player_stats = usports_football_players_stats('playoffs')
>>> championship_player_stats = usports_football_players_stats('championship')

Author:
    OJ Adeyemi

Date Created:
     March 21, 2025
"""

from .player_stats import usports_football_players_stats
from .team_stats import usports_football_team_stats

__all__ = ["usports_football_team_stats", "usports_football_players_stats"]
