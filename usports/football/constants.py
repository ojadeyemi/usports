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
