"""Volleyball API tests."""

import pandas as pd
import pytest

from usports.volleyball import usports_vball_players, usports_vball_standings, usports_vball_teams

from .test_data import (
    expected_volleyball_players_columns,
    expected_volleyball_standings_columns,
    expected_volleyball_team_stats_columns,
    should_test_playoffs,
)


class TestVolleyballStandings:
    def test_standings_data_structure(self):
        df = usports_vball_standings("m")
        # Test DataFrame structure
        assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_volleyball_standings_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in standings: {missing_columns}"


class TestVolleyballTeams:
    def test_teams_data_structure(self):
        # Test regular season data
        regular_df = usports_vball_teams("m", "regular")
        assert isinstance(regular_df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not regular_df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = regular_df.columns.tolist()
        missing_columns = [col for col in expected_volleyball_team_stats_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in team stats: {missing_columns}"

    @pytest.mark.skipif(
        not should_test_playoffs("volleyball"), reason="Playoff data only available in February and March"
    )
    def test_playoff_data_structure(self):
        # Test playoffs data and column consistency
        regular_df = usports_vball_teams("m", "regular")
        playoffs_df = usports_vball_teams("m", "playoffs")

        assert isinstance(playoffs_df, pd.DataFrame), "Should return a pandas DataFrame"

        if not playoffs_df.empty:
            regular_cols = set(regular_df.columns)
            playoffs_cols = set(playoffs_df.columns)
            assert regular_cols == playoffs_cols, (
                f"Column mismatch: Regular has {regular_cols - playoffs_cols}, "
                f"Playoffs has {playoffs_cols - regular_cols}"
            )


class TestVolleyballPlayers:
    def test_players_data_structure_and_types(self):
        # Test DataFrame structure
        df = usports_vball_players("m", "regular")
        assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_volleyball_players_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in player stats: {missing_columns}"

        # Test numeric columns
        numeric_cols = ["matches_played", "sets_played", "kills", "digs", "blocks_per_set", "service_aces"]
        for col in numeric_cols:
            if col in df.columns:
                assert df[col].dtype in ["int64", "float64"], f"{col} should be numeric, got {df[col].dtype}"


class TestVolleyballSportSpecific:
    def test_matches_vs_sets_consistency(self):
        """Volleyball specific test - ensure matches and sets are properly tracked"""
        # Test in teams data
        teams_df = usports_vball_teams("m", "regular")
        assert "matches_played" in teams_df.columns, "Teams should track matches"
        assert "sets_played" in teams_df.columns, "Teams should track sets"

        if not teams_df.empty:
            valid_data = teams_df[(teams_df["matches_played"] > 0) & (teams_df["sets_played"] > 0)]
            if not valid_data.empty:
                assert all(valid_data["sets_played"] >= valid_data["matches_played"]), (
                    "Sets played should be >= matches played"
                )

        # Test in players data
        players_df = usports_vball_players("m", "regular")
        assert "matches_played" in players_df.columns, "Players should track matches"
        assert "sets_played" in players_df.columns, "Players should track sets"

        if not players_df.empty:
            valid_data = players_df[(players_df["matches_played"] > 0) & (players_df["sets_played"] > 0)]
            if not valid_data.empty:
                assert all(valid_data["sets_played"] >= valid_data["matches_played"]), (
                    "Player sets played should be >= matches played"
                )
