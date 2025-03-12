"""Functions:
- usport_players_stats: Fetch player statistics.
- usport_team_stats: Fetch team statistics.

These functions return pandas DataFrames with the requested statistics.

Examples:
>>> from usports.basketball import usport_players_stats, usport_team_stats

>>> men_player_stats_df = usport_players_stats('m') # men's team regular season players stats

>>> women_player_stats_df = usport_players_stats('w', 'championship') # women's players in U Sports championship Final 8

>>> women_team_stats_df = usport_team_stats('w', 'playoffs') # women's team playoffs stats

Author:
    OJ Adeyemi

Date Created:
    February 1, 2025
"""

from .player_stats import usport_players_stats
from .team_stats import usport_team_stats

__all__ = ["usport_players_stats", "usport_team_stats"]
