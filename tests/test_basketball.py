"""Basketball API tests."""

import pandas as pd
import pytest

from usports.basketball import usports_bball_players, usports_bball_standings, usports_bball_teams

from .test_data import (
    expected_basketball_players_columns,
    expected_basketball_standings_columns,
    expected_basketball_team_stats_columns,
    should_test_playoffs,
)


class TestBasketballStandings:
    def test_standings_data_structure(self):
        df = usports_bball_standings("m")
        # Test DataFrame structure
        assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_basketball_standings_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in standings: {missing_columns}"


class TestBasketballTeams:
    def test_teams_data_structure(self):
        # Test regular season data
        regular_df = usports_bball_teams("m", "regular")
        assert isinstance(regular_df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not regular_df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = regular_df.columns.tolist()
        missing_columns = [col for col in expected_basketball_team_stats_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in team stats: {missing_columns}"

    @pytest.mark.skipif(
        not should_test_playoffs("basketball"), reason="Playoff data only available in February and March"
    )
    def test_playoff_data_structure(self):
        # Test playoffs data and column consistency
        regular_df = usports_bball_teams("m", "regular")
        playoffs_df = usports_bball_teams("m", "playoffs")

        assert isinstance(playoffs_df, pd.DataFrame), "Should return a pandas DataFrame"

        if not playoffs_df.empty:
            regular_cols = set(regular_df.columns)
            playoffs_cols = set(playoffs_df.columns)
            assert regular_cols == playoffs_cols, (
                f"Column mismatch: Regular has {regular_cols - playoffs_cols}, "
                f"Playoffs has {playoffs_cols - regular_cols}"
            )


class TestBasketballPlayers:
    def test_players_data_structure_and_types(self):
        # Test DataFrame structure
        df = usports_bball_players("m", "regular")
        assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_basketball_players_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in player stats: {missing_columns}"

        # Test numeric columns
        numeric_cols = ["games_played", "total_points", "field_goal_percentage", "assists", "steals", "blocks"]
        for col in numeric_cols:
            if col in df.columns:
                assert df[col].dtype in ["int64", "float64"], f"{col} should be numeric, got {df[col].dtype}"

    def test_separation_of_concerns(self):
        standings_df = usports_bball_standings("m")
        teams_df = usports_bball_teams("m", "regular")

        standings_exclusive = {"total_wins", "total_losses", "win_percentage", "total_points", "total_points_against"}
        stats_exclusive = {
            "points_per_game",
            "field_goal_percentage",
            "assists_per_game",
            "steals_per_game",
            "blocks_per_game",
        }

        for col in standings_exclusive:
            assert col in standings_df.columns, f"Standings missing: {col}"
            assert col not in teams_df.columns, f"Stats shouldn't have: {col}"

        for col in stats_exclusive:
            assert col in teams_df.columns, f"Stats missing: {col}"
            assert col not in standings_df.columns, f"Standings shouldn't have: {col}"
