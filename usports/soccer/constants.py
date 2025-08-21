"""Contains soccer related constants"""

SOCCER_TEAM_STATS_COLUMNS_TYPE_MAPPING: list[dict[str, type]] = [
    # Offensive stats
    {
        "shots": int,
        "goals": int,
        "goals_per_game": float,
        "assists": int,
        "points": int,
        "shot_percentage": float,
        "shots_per_game": float,
    },
    # Defensive stats
    {
        "goals_against": int,
        "goals_against_average": float,
        "saves": int,
        "shutouts": int,
    },
    # Misc stats
    {
        "yellow_cards": int,
        "red_cards": int,
        "corner_kicks": int,
    },
]

SOCCER_STANDINGS_COLUMNS_TYPE_MAPPING: dict[str, type] = {
    "team_name": str,
    "games_played": int,
    "total_wins": int,
    "total_losses": int,
    "ties": int,
    "goals_for": int,
    "goals_against": int,
    "points": int,
}

SOCCER_PLAYER_STATS_COLUMNS_TYPE_MAPPING: list[dict[str, type]] = [
    # Scoring stats (pos=sc) - Field players (excludes gp, handled separately)
    {
        "games_started": int,
        "goals": int,
        "assists": int,
        "points": int,
    },
    # Shooting stats (pos=sh) - Field players (excludes gp)
    {
        "shots": int,
        "shot_percentage": float,
        "shots_on_goal": int,
        "sog_percentage": float,
    },
    # Misc stats (pos=ms) - Field players (excludes gp)
    {
        "yellow_cards": int,
        "red_cards": int,
        "penalty_kicks": int,
        "game_winning_goals": int,
    },
    # Goalie stats (pos=g) - excludes ggp (handled as games_played)
    {
        "goalie_games_started": int,
        "goalie_goals_against": int,
        "goalie_saves": int,
        "goalie_save_percentage": float,
    },
    # Goalie extended stats (pos=gext) - excludes ggp (handled as games_played)
    {
        "goalie_wins": int,
        "goalie_losses": int,
        "goalie_ties": int,
        "goalie_shutouts": int,
        "goalie_minutes_played": float,
    },
]

# Sort categories for field players
FIELD_PLAYER_SORT_CATEGORIES = [
    ("sc", "p"),  # points
    ("sc", "g"),  # goals
    ("sc", "a"),  # assists
    ("sh", "sh"),  # shots
    ("sh", "sog"),  # shots on goal
    ("ms", "yc"),  # yellow cards
    ("ms", "gw"),  # game winning goals
]

# Sort categories for goalies
GOALIE_SORT_CATEGORIES = [
    ("g", "sv"),  # saves
    ("g", "ga"),  # goals against
    ("gext", "gow"),  # wins
    ("gext", "gm"),  # minutes
]
