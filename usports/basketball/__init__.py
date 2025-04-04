"""Functions:
- usports_players_stats: Fetch player statistics.
- usports_team_stats: Fetch team statistics.

These functions return pandas DataFrames with the requested statistics.

Examples:
>>> from usports.basketball import usports_bball_players, usports_bball_teams

>>> men_player_stats_df = usports_bball_players('m') # men's team regular season players stats

>>> women_player_stats_df = usports_bball_players('w', 'championship') # women's players in U Sports championship Final 8

>>> women_team_stats_df = usports_bball_teams('w', 'playoffs') # women's team playoffs stats

Author:
    OJ Adeyemi

Date Created:
    February 1, 2025
"""

from .player_stats import usports_bball_players
from .team_stats import usports_bball_teams

__all__ = ["usports_bball_players", "usports_bball_teams"]
