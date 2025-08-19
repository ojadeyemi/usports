"""Contains basketball related constants"""

BBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING: list[dict[str, type]] = [
    {
        "field_goal_made": int,
        "field_goal_percentage": float,
        "three_pointers_made": int,
        "three_point_percentage": float,
        "free_throws_made": int,
        "free_throw_percentage": float,
        "points_per_game": float,
    },
    {
        "offensive_rebounds_per_game": float,
        "defensive_rebounds_per_game": float,
        "total_rebounds_per_game": float,
        "rebound_margin": float,
    },
    {
        "turnovers_per_game": float,
        "steals_per_game": float,
        "blocks_per_game": float,
        "assists_per_game": float,
    },
    {
        "team_fouls_per_game": float,
        "offensive_efficiency": float,
        "net_efficiency": float,
    },
    {
        "field_goal_made_against": int,
        "field_goal_percentage_against": float,
        "three_pointers_made_against": int,
        "three_point_percentage_against": float,
        "points_per_game_against": float,
    },
    {
        "offensive_rebounds_per_game_against": float,
        "defensive_rebounds_per_game_against": float,
        "total_rebounds_per_game_against": float,
        "rebound_margin_against": float,
    },
    {
        "turnovers_per_game_against": float,
        "steals_per_game_against": float,
        "blocks_per_game_against": float,
        "assists_per_game_against": float,
    },
    {
        "team_fouls_per_game_against": float,
        "defensive_efficiency": float,
        "net_efficiency_against": float,
    },
]


BBALL_STANDINGS_COLUMNS_TYPE_MAPPING: dict[str, type] = {
    "team_name": str,
    "games_played": int,
    "total_wins": int,
    "total_losses": int,
    "ties": int,
    "win_percentage": float,
    "total_points": int,
    "total_points_against": int,
}

PLAYER_STATS_COLUMNS_TYPE_MAPPING: list[dict[str, type]] = [
    {
        "minutes_played": int,
        "field_goal_made": int,
        "field_goal_percentage": float,
        "three_pointers_made": int,
        "three_pointers_percentage": float,
        "free_throws_made": int,
        "free_throws_percentage": float,
        "total_points": int,
    },
    {
        "offensive_rebounds": int,
        "defensive_rebounds": int,
        "total_rebounds": int,
        "assists": int,
        "turnovers": int,
        "steals": int,
        "blocks": int,
    },
    {
        "personal_fouls": int,
        "disqualifications": int,
        "assist_to_turnover_ratio": float,
    },
]

PLAYER_SORT_CATEGORIES = [
    "pts",
    "min",
    "fgp",
    "fgp3",
    "fgpt3",
    "ftpt",
    "oreb",
    "dreb",
    "treb",
    "ast",
    "to",
    "stl",
    "blk",
    "pf",
    "dq",
    "ato",
]
