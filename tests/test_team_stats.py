"""Test for team stats to work as expected"""

from pandas import DataFrame

from usports.basketball import usports_bball_team_stats
from usports.football import usports_football_team_stats

from .test_data import (
    expected_basketball_playoffs_season_column_names,
    expected_basketball_reg_season_column_names,
    expected_football_column_names,
)


def test_usports_bball_team_stats():
    """Test if usports_bball_team_stats returns a valid DataFrame with expected columns and matching row data."""

    team_stats_df = usports_bball_team_stats("men")

    assert isinstance(team_stats_df, DataFrame), "Expected a pandas DataFrame."
    assert not team_stats_df.empty, "DataFrame is empty."

    actual_columns = team_stats_df.columns.tolist()
    for column in expected_basketball_reg_season_column_names:
        assert column in actual_columns, f"Column '{column}' missing."


def test_usports_bball_playoffs_team_stats():
    """Test if usports_bball_team_stats returns a valid DataFrame with expected columns and matching row data."""

    team_stats_df = usports_bball_team_stats("men", "playoffs")

    assert isinstance(team_stats_df, DataFrame), "Expected a pandas DataFrame."
    assert not team_stats_df.empty, "DataFrame is empty."

    actual_columns = team_stats_df.columns.tolist()
    for column in expected_basketball_playoffs_season_column_names:
        assert column in actual_columns, f"Column '{column}' missing."


def test_usports_football_team_stats():
    """Test if usports_footaball_team_stats returns a valid DataFrame with expected columns and matching row data."""

    team_stats_df = usports_football_team_stats("regular")

    assert isinstance(team_stats_df, DataFrame), "Expected a pandas DataFrame."
    assert not team_stats_df.empty, "DataFrame is empty."

    actual_columns = team_stats_df.columns.tolist()
    for column in expected_football_column_names:
        assert column in actual_columns, f"Column '{column}' missing."
