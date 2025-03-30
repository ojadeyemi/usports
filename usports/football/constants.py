"""Contains football related constants"""

FBALL_TEAM_STATS_COLUMNS_TYPE_MAPPING: list[dict[str, type]] = [
    # Table 1: Scoring/Offensive Scoring Breakdown
    {
        "touchdowns": int,
        "field_goals": int,
        "extra_points": int,
        "two_point_conversions": int,
        "defensive_extra_points": int,
        "safeties": int,
        "points": int,
        "points_per_game": float,
    },
    # Table 2: Overall Offensive Yards (Rushing & Passing Totals)
    {
        "rushing_yards": int,
        "passing_yards": int,
        "total_offense": int,
        "yards_per_game": float,
    },
    # Table 3: Detailed Passing Stats
    {
        "passing_yards": int,  # Redundant with table 2 if both exist but thats ok
        "pass_completions": int,  # Left part of comp-att-int format
        "passing_yards_per_game": float,
        "yards_per_attempt": float,
        "yards_per_completion": float,
        "passing_touchdowns": int,
    },
    # Table 4: Detailed Rushing Stats
    {
        "rushing_yards": int,
        "rushing_attempts": int,
        "rushing_yards_per_game": float,
        "rushing_average": float,
        "rushing_touchdowns": int,
    },
    # Table 5: First Downs Breakdown
    {
        "total_first_downs": int,
        "rushing_first_downs": int,
        "passing_first_downs": int,
        "penalty_first_downs": int,  # First downs awarded by penalties
        "first_downs_per_game": float,
    },
    # Table 6: Third and Fourth Down Conversions
    {
        "third_down_conversions_made": int,  # From format like "8-11"
        "third_down_conversion_percentage": float,
        "fourth_down_conversions_made": int,
        "fourth_down_conversion_percentage": float,
    },
    # Table 7: Return Stats (Kick Returns & Punt Returns)
    {
        "kick_return_count": int,  # From format like "22-576"
        "kickoff_return_average": float,
        "punt_return_count": int,
        "punt_return_average": float,
    },
    # Table 8: Kicking Stats (Field Goals, Extra Points, Punts, Kickoffs)
    {
        "field_goal_made": int,  # From format like "20-22"
        "field_goal_percentage": float,
        "extra_point_made": int,
        "extra_point_percentage": float,
        "punt_count": int,
        "punt_average": float,
        "kickoff_count": int,
        "kickoff_average": float,
    },
    # Table 9: Scoring & Red Zone Efficiency
    {
        "scores_made": int,  # From format like "23-23"
        "red_zone_percentage": float,
        "touchdowns_made": int,  # From format like "17-23"
        "touchdown_percentage": float,
    },
    # Table 10: Turnovers and Defensive Plays
    {
        "fumbles": int,  # From format like "10-5"
        "fumble_recoveries": int,
        "interceptions": int,
        "interception_yards": int,
        "interception_average": float,
        "interception_touchdowns": int,
        "tackles": float,
        "sacks": int,
    },
    # Table 11: Penalty Stats
    {
        "penalties": int,
        "penalties_per_game": float,
        "penalty_yards": int,
        "penalty_yards_per_game": float,
    },
    # Table 12: Overall Aggregated Stats
    {
        "points_per_game": float,
        "points": int,
        "yards_per_game": float,
        "passing_yards_per_game": float,
        "rushing_yards_per_game": float,
        "tackles_per_game": float,
        "interceptions": int,
        "fumble_recoveries": int,
        "sacks": int,
        "touchdowns": int,
    },
    # Table 13: Time of Possession and Attendance
    {
        "time_of_possession": int,  # Format example: "33:30" to seconds only
        "home_attendance": int,  # Looks like this "10,000" but changes to int after
        "average_home_attendance": int,
    },
]


STANDINGS_COLUMNS_TYPE_MAPPING: dict[str, type] = {
    "team_name": str,
    "games_played": int,
    "total_wins": int,
    "total_losses": int,
    "ties": int,
    "win_percentage": float,
    "total_points": int,
    "total_points_against": int,
}

FBALL_PLAYER_STATS_COLUMNS_TYPE_MAPPING: list[dict[str, type]] = [
    # Passing stats
    {
        "games_played": int,  # gp
        "pass_completions": int,  # comp
        "pass_attempts": int,  # att
        "completion_percentage": float,  # pct
        "passing_yards": int,  # yds
        "passing_yards_per_game": float,  # y/g
        "yards_per_attempt": float,  # y/a
        "passing_touchdowns": int,  # td
        "interceptions": int,  # int
        "longest_pass": int,  # lg
        "passing_efficiency": float,  # effic
    },
    # Rushing stats
    {
        "games_played": int,  # gp
        "rushing_attempts": int,  # rush
        "rushing_yards": int,  # yds
        "rushing_yards_per_game": float,  # y/g
        "yards_per_carry": float,  # avg
        "rushing_touchdowns": int,  # td
        "longest_rush": int,  # lg
        "fumbles": int,  # fum
        "fumbles_lost": int,  # lost
    },
    # Receiving stats
    {
        "games_played": int,  # gp
        "receptions": int,  # rec
        "receptions_per_game": float,  # rec/g
        "receiving_yards": int,  # yds
        "receiving_yards_per_game": float,  # y/g
        "yards_per_reception": float,  # avg
        "receiving_touchdowns": int,  # td
        "longest_reception": int,  # lg
    },
    # Kicking stats
    {
        "games_played": int,  # gp
        "field_goals_made": int,  # fgm
        "field_goals_attempted": int,  # fga
        "field_goal_percentage": float,  # pct
        "longest_field_goal": int,  # lg
        "extra_points_made": int,  # xpm
        "extra_points_attempted": int,  # xpa
        "extra_point_percentage": float,  # pct (for extra points)
        "kicking_points": int,  # pts
    },
    # Punting stats
    {
        "games_played": int,  # gp
        "punts": int,  # punt
        "punting_yards": int,  # yds
        "yards_per_punt": float,  # avg
        "longest_punt": int,  # lg
        "punts_inside_20": int,  # in20
        "fair_catches": int,  # fc
        "touchbacks": int,  # tb
        "blocked_punts": int,  # blk
    },
    # Return stats
    {
        "kick_returns": int,  # kr
        "kick_return_yards": int,  # yds
        "yards_per_kick_return": float,  # avg
        "kick_return_touchdowns": int,  # td
        "longest_kick_return": int,  # lg
        "punt_returns": int,  # pr
        "punt_return_yards": int,  # yds
        "yards_per_punt_return": float,  # avg
        "punt_return_touchdowns": int,  # td
        "longest_punt_return": int,  # lg
    },
    # All-Purpose yards stats
    {
        "games_played": int,  # gp
        "rushing_yards": int,  # rush
        "receiving_yards": int,  # rcv
        "punt_return_yards": int,  # pr
        "kick_return_yards": int,  # kr
        "total_yards": int,  # yds
        "yards_per_game": float,  # ypg
    },
    # Scoring stats
    {
        "total_points": int,  # pts
        "points_per_game": float,  # pts/g
        "rushing_touchdowns": int,  # rush
        "receiving_touchdowns": int,  # rec
        "kick_return_touchdowns": int,  # kr
        "punt_return_touchdowns": int,  # pr
        "interception_return_touchdowns": int,  # int
        "fumble_return_touchdowns": int,  # fum
        "extra_points_made": int,  # xpm
        "field_goals_made": int,  # fgm
        "two_point_conversions": int,  # 2pt
        "miscellaneous_touchdowns": int,  # misc
    },
    # Defensive stats
    {
        "games_played": int,  # gp
        "solo_tackles": int,  # tkl
        "assisted_tackles": int,  # ast
        "total_tackles": float,  # tot (some leagues count half tackles)
        "tackles_per_game": float,  # tkl/g
        "sacks": float,  # sck
        "sack_yards": int,  # yds (yards lost from sacks)
        "tackles_for_loss": float,  # tfl
        "tackles_for_loss_yards": int,  # yds
        "forced_fumbles": int,  # ff
        "fumble_recoveries": int,  # fr
        "fumble_recovery_yards": int,  # yds
        "interceptions": int,  # int
        "interception_return_yards": int,  # yds
        "pass_breakups": int,  # brup
        "blocked_kicks": int,  # blk
    },
]

PLAYER_SORT_CATEGORIES = [
    ("qb", "pyd"),
    ("qb", "ptd"),
    ("rb", "ryd"),
    ("rb", "rtd"),
    ("wr", "wyd"),
    ("wr", "wtd"),
    ("k", "fga"),
    ("k", "kpts"),
    ("p", "uyd"),
    ("p", "uya"),
    ("kr", "kryd"),
    ("all", "apyds"),
    ("pts", "pts"),
    ("d", "dtt"),
    ("d", "dst"),
    ("d", "tfl"),
    ("d", "dff"),
    ("d", "dfr"),
    ("d", "di"),
    ("d", "dblk"),
]
