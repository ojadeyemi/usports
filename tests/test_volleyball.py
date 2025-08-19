"""Volleyball API tests."""

import pandas as pd

from usports.volleyball import usports_vball_players, usports_vball_standings, usports_vball_teams

from .test_data import (
    expected_volleyball_players_columns,
    expected_volleyball_standings_columns,
    expected_volleyball_team_stats_columns,
)


class TestVolleyballStandings:
    def test_standings_returns_dataframe(self):
        df = usports_vball_standings("m")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_standings_has_all_expected_columns(self):
        df = usports_vball_standings("m")
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_volleyball_standings_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in standings: {missing_columns}"

    def test_standings_no_performance_stats(self):
        df = usports_vball_standings("w")
        performance_cols = ["kills_per_set", "digs_per_set", "blocks_per_set"]
        unexpected_cols = [col for col in performance_cols if col in df.columns]
        assert not unexpected_cols, f"Standings shouldn't have performance stats: {unexpected_cols}"


class TestVolleyballTeams:
    def test_teams_returns_dataframe(self):
        df = usports_vball_teams("m", "regular")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_teams_has_all_expected_columns(self):
        df = usports_vball_teams("m", "regular")
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_volleyball_team_stats_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in team stats: {missing_columns}"

    def test_teams_no_standings_columns(self):
        df = usports_vball_teams("m", "regular")
        standings_cols = ["total_wins", "total_losses", "win_percentage"]
        unexpected_cols = [col for col in standings_cols if col in df.columns]
        assert not unexpected_cols, f"Team stats shouldn't have W/L columns: {unexpected_cols}"

    def test_teams_all_seasons_return_same_columns(self):
        regular_df = usports_vball_teams("m", "regular")
        playoffs_df = usports_vball_teams("m", "playoffs")

        if not playoffs_df.empty:
            regular_cols = set(regular_df.columns)
            playoffs_cols = set(playoffs_df.columns)
            assert regular_cols == playoffs_cols, (
                f"Column mismatch: Regular has {regular_cols - playoffs_cols}, "
                f"Playoffs has {playoffs_cols - regular_cols}"
            )


class TestVolleyballPlayers:
    def test_players_returns_dataframe(self):
        df = usports_vball_players("w", "regular")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_players_has_all_expected_columns(self):
        df = usports_vball_players("w", "regular")
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_volleyball_players_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in player stats: {missing_columns}"

    def test_players_numeric_columns_are_numeric(self):
        df = usports_vball_players("m", "regular")
        numeric_cols = ["matches_played", "sets_played", "kills", "digs", "blocks_per_set", "service_aces"]
        for col in numeric_cols:
            if col in df.columns and not df.empty:
                assert df[col].dtype in ["int64", "float64"], f"{col} should be numeric, got {df[col].dtype}"


class TestVolleyballDataConsistency:
    def test_standings_and_teams_have_same_teams(self):
        standings_df = usports_vball_standings("m")
        teams_df = usports_vball_teams("m", "regular")

        standings_teams = set(standings_df["team_name"].unique())
        stats_teams = set(teams_df["team_name"].unique())

        teams_only_in_standings = standings_teams - stats_teams
        teams_only_in_stats = stats_teams - standings_teams

        assert not teams_only_in_standings, f"Teams only in standings: {teams_only_in_standings}"
        assert not teams_only_in_stats, f"Teams only in team stats: {teams_only_in_stats}"

    def test_all_functions_have_conference_column(self):
        standings_df = usports_vball_standings("m")
        teams_df = usports_vball_teams("m", "regular")

        assert "conference" in standings_df.columns
        assert "conference" in teams_df.columns

        valid_conferences = {"OUA", "RSEQ", "CW", "AUS", "nan"}
        standings_confs = set(standings_df["conference"].unique())
        teams_confs = set(teams_df["conference"].unique())

        invalid_standings = standings_confs - valid_conferences
        invalid_teams = teams_confs - valid_conferences

        assert not invalid_standings, f"Invalid conferences in standings: {invalid_standings}"
        assert not invalid_teams, f"Invalid conferences in teams: {invalid_teams}"

    def test_matches_vs_sets_consistency(self):
        """Volleyball specific test - ensure matches and sets are properly tracked"""
        teams_df = usports_vball_teams("m", "regular")

        assert "matches_played" in teams_df.columns, "Teams should track matches"
        assert "sets_played" in teams_df.columns, "Teams should track sets"

        if not teams_df.empty:
            valid_data = teams_df[(teams_df["matches_played"] > 0) & (teams_df["sets_played"] > 0)]
            if not valid_data.empty:
                assert all(valid_data["sets_played"] >= valid_data["matches_played"]), (
                    "Sets played should be >= matches played"
                )
