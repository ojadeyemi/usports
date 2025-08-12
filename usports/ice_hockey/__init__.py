"""Functions
- usports_ice_hockey_teams: Fetch team statistics.
- usports_ice_hockey_players: Fetch player statistics.
- usports_ice_hockey_standings: Fetch team standings.

These functions return pandas DataFrames with the requested statistics.

Examples:
>>> from usports.ice_hockey import usports_ice_hockey_teams, usports_ice_hockey_players, usports_ice_hockey_standings

>>> regular_season_team_stats = usports_ice_hockey_teams('m','regular_season')
>>> womens_playoff_team_stats = usports_ice_hockey_teams('w','playoffs')
>>> womens_championship_team_stats = usports_ice_hockey_teams('w','championship')
"""

from .player_stats import usports_ice_hockey_players
from .standings import usports_ice_hockey_standings
from .team_stats import usports_ice_hockey_teams

__all__ = ["usports_ice_hockey_standings", "usports_ice_hockey_teams", "usports_ice_hockey_players"]
