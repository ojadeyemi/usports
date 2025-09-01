"""Football API tests."""

import pandas as pd
import pytest

from usports.football import usports_fball_players, usports_fball_standings, usports_fball_teams

from .test_data import (
    expected_football_column_names,
    expected_football_players_df_column,
    expected_football_standings_columns,
    should_test_playoffs,
)


class TestFootballStandings:
    def test_standings_data_structure(self):
        df = usports_fball_standings()
        # Test DataFrame structure
        assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_football_standings_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in standings: {missing_columns}"


class TestFootballTeams:
    def test_teams_data_structure(self):
        # Test regular season data
        regular_df = usports_fball_teams("regular")
        assert isinstance(regular_df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not regular_df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = regular_df.columns.tolist()
        missing_columns = [col for col in expected_football_column_names if col not in actual_columns]
        assert not missing_columns, f"Missing columns in team stats: {missing_columns}"

    @pytest.mark.skipif(
        not should_test_playoffs("football"), reason="Playoff data only available in November and December"
    )
    def test_playoff_data_structure(self):
        # Test playoffs data and column consistency
        regular_df = usports_fball_teams("regular")
        playoffs_df = usports_fball_teams("playoffs")

        assert isinstance(playoffs_df, pd.DataFrame), "Should return a pandas DataFrame"

        if not playoffs_df.empty:
            regular_cols = set(regular_df.columns)
            playoffs_cols = set(playoffs_df.columns)
            assert regular_cols == playoffs_cols, (
                f"Column mismatch: Regular has {regular_cols - playoffs_cols}, "
                f"Playoffs has {playoffs_cols - regular_cols}"
            )


class TestFootballPlayers:
    def test_players_data_structure_and_types(self):
        # Test DataFrame structure
        df = usports_fball_players("regular")
        assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_football_players_df_column if col not in actual_columns]
        assert not missing_columns, f"Missing columns in player stats: {missing_columns}"

        # Test numeric columns
        numeric_cols = ["games_played", "pass_completions", "pass_attempts", "passing_yards", "rushing_yards"]
        for col in numeric_cols:
            if col in df.columns:
                assert df[col].dtype in ["int64", "float64"], f"{col} should be numeric, got {df[col].dtype}"
