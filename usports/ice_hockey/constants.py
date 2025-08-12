"""Contains ice hockey related constants"""

ICE_HOCKEY_BBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING: dict[str, type] = {
    "goals": int,
    "assists": int,
    "goals_per_game": float,
    "shots": int,
    "penalty_minutes": int,
    "power_play_goals": int,
    "power_play_opportunities": int,
    "power_play_percentage": float,
    "power_play_goals_against": int,
    "times_short_handed": int,
    "penalty_kill_percentage": float,
    "short_handed_goals": int,
    "short_handed_goals_against": int,
    "goals_against": int,
    "goals_against_average": float,
    "saves": int,
    "save_percentage": float,
    "empty_net_goals_against": int,
}


ICE_HOCKEY_PLAYER_STATS_COLUMNS_TYPE_MAPPING: dict[str, type] = {
    "games_played": int,
    "goals": int,
    "assists": int,
    "points": int,
    "penalty_minutes": int,
    "plus_minus": int,
    "power_play_goals": int,
    "short_handed_goals": int,
    "empty_net_goals": int,
    "game_winning_goals": int,
    "game_tying_goals": int,
    "hat_tricks": int,
    "shots_on_goal": int,
}

ICE_HOCKEY_GOALIE_STATS_COLUMNS_TYPE_MAPPING: dict[str, type] = {
    "games_played": int,
    "games_started": int,
    "minutes_played": int,
    "goals_against": int,
    "goals_against_average": float,
    "saves": int,
    "save_percentage": float,
    "wins": int,
    "losses": int,
    "ties": int,
    "win_percentage": float,
}

ICE_HOCKEY_FBALL_STANDINGS_COLUMNS_TYPE_MAPPING: dict[str, type] = {
    "team_name": str,
    "games_played": int,
    "total_wins": int,
    "total_losses": int,
    "ties": int,
    "goals_for": int,
    "goals_against": int,
    "total_points": int,
}

SKATERS_SORT_CATEGORIES = ["g", "a", "p", "pim", "plusminus", "ppg", "shg", "gw", "gt", "hat"]
GOALIES_SORT_CATEGORIES = ["ggs", "gm", "ga", "gaa", "sv", "svpt", "gow", "gol", "got", "gpwpt"]
