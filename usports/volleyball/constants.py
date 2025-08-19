"""Contains volleyball related constants"""

VOLLEYBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING: list[dict[str, type]] = [
    # Offensive stats (pos=of)
    {
        "kills": int,
        "kills_per_set": float,
        "errors": int,
        "total_attacks": int,
        "hitting_percentage": float,
        "assists": int,
        "assists_per_set": float,
        "points": float,
        "points_per_set": float,
    },
    # Defensive stats (pos=df)
    {
        "digs": int,
        "digs_per_set": float,
        "block_solos": int,
        "block_assists": int,
        "total_blocks": float,
        "blocks_per_set": float,
    },
    # Serve/Receive stats (pos=sr)
    {
        "serve_attempts": int,
        "service_aces": int,
        "service_aces_per_set": float,
        "service_errors": int,
        "receptions": int,
        "reception_errors": int,
    },
]

VOLLEYBALL_STANDINGS_COLUMNS_TYPE_MAPPING: dict[str, type] = {
    "team_name": str,
    "games_played": int,
    "total_wins": int,
    "total_losses": int,
    "win_percentage": float,
    "sets_for": int,
    "sets_against": int,
    "points": int,
}

VOLLEYBALL_PLAYER_STATS_COLUMNS_TYPE_MAPPING: list[dict[str, type]] = [
    # Offensive stats
    {
        "kills": int,
        "kills_per_set": float,
        "errors": int,
        "total_attacks": int,
        "total_attacks_per_set": float,
        "hitting_percentage": float,
        "assists": int,
        "assists_per_set": float,
        "points": float,
        "points_per_set": float,
    },
    # Defensive stats
    {
        "digs": int,
        "digs_per_set": float,
        "block_solos": int,
        "block_assists": int,
        "total_blocks": float,
        "blocks_per_set": float,
    },
    # Serve/Receive stats
    {
        "serve_attempts": int,
        "service_aces": int,
        "service_aces_per_set": float,
        "service_errors": int,
        "receptions": int,
        "reception_errors": int,
    },
]

# Sort categories for player stats URLs - based on actual data-key values
PLAYER_SORT_CATEGORIES = [
    ("of", "k"),  # kills
    ("of", "a"),  # assists
    ("of", "pts"),  # points
    ("df", "d"),  # digs
    ("df", "bt"),  # total blocks
    ("sr", "sa"),  # service aces
]
