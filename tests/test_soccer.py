"""Soccer API tests."""

import pandas as pd

from usports.soccer import usports_soccer_players, usports_soccer_standings, usports_soccer_teams

from .test_data import (
    expected_soccer_players_columns,
    expected_soccer_standings_columns,
    expected_soccer_team_stats_columns,
)


class TestSoccerStandings:
    def test_standings_data_structure(self):
        df = usports_soccer_standings("m")
        # Test DataFrame structure
        assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_soccer_standings_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in standings: {missing_columns}"


class TestSoccerTeams:
    def test_teams_data_structure(self):
        # Test regular season data
        regular_df = usports_soccer_teams("m", "regular")
        assert isinstance(regular_df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not regular_df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = regular_df.columns.tolist()
        missing_columns = [col for col in expected_soccer_team_stats_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in team stats: {missing_columns}"

        # Test playoffs data and column consistency
        playoffs_df = usports_soccer_teams("m", "playoffs")
        if not playoffs_df.empty:
            regular_cols = set(regular_df.columns)
            playoffs_cols = set(playoffs_df.columns)
            assert regular_cols == playoffs_cols, (
                f"Column mismatch: Regular has {regular_cols - playoffs_cols}, "
                f"Playoffs has {playoffs_cols - regular_cols}"
            )


class TestSoccerPlayers:
    def test_players_data_structure_and_types(self):
        # Test DataFrame structure
        df = usports_soccer_players("m", "regular")
        assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
        assert not df.empty, "DataFrame should not be empty"

        # Test column completeness
        actual_columns = df.columns.tolist()
        missing_columns = [col for col in expected_soccer_players_columns if col not in actual_columns]
        assert not missing_columns, f"Missing columns in player stats: {missing_columns}"

        # Test numeric columns
        numeric_cols = [
            "games_played",
            "goals",
            "assists",
            "shots",
            "goalie_saves",
            "yellow_cards",
            "goalie_minutes_played",
        ]
        for col in numeric_cols:
            if col in df.columns:
                assert df[col].dtype in ["int64", "float64"], f"{col} should be numeric, got {df[col].dtype}"

        # Test position validation
        assert "position" in df.columns, "Players should have position column"
        if not df.empty:
            positions = df["position"].unique()
            valid_positions = {"goalie", "field"}
            invalid_positions = set(positions) - valid_positions
            assert not invalid_positions, f"Invalid positions found: {invalid_positions}"

        # Test goalie-specific columns
        goalie_specific_cols = [
            "goalie_games_started",
            "goalie_goals_against",
            "goalie_saves",
            "goalie_save_percentage",
            "goalie_wins",
            "goalie_losses",
            "goalie_ties",
            "goalie_shutouts",
            "goalie_minutes_played",
        ]
        for col in goalie_specific_cols:
            assert col in df.columns, f"Missing goalie column: {col}"

        # Test position-specific stats
        if not df.empty:
            # Test goalie stats
            goalies = df[df["position"] == "goalie"]
            if not goalies.empty:
                goalie_stats_cols = ["goalie_games_played", "goalie_saves"]
                for col in goalie_stats_cols:
                    if col in goalies.columns:
                        assert (goalies[col] > 0).any(), f"All goalies have zero {col}"

            # Test field player stats
            field_players = df[df["position"] == "field"]
            if not field_players.empty:
                field_stats_cols = ["games_played", "goals", "assists"]
                for col in field_stats_cols:
                    if col in field_players.columns:
                        assert (field_players[col] > 0).any(), f"All field players have zero {col}"
