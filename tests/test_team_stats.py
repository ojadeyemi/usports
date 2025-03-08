"""Test for team stats to work as expected"""

from pandas import DataFrame

from usports.basketball import usport_team_stats

from .test_data import expected_playoffs_season_column_names, expected_reg_season_column_names


def test_usports_team_stats():
    """Test if usport_team_stats returns a valid DataFrame with expected columns and matching row data."""

    team_stats_df = usport_team_stats("men")

    assert isinstance(team_stats_df, DataFrame), "Expected a pandas DataFrame."
    assert not team_stats_df.empty, "DataFrame is empty."

    actual_columns = team_stats_df.columns.tolist()
    for column in expected_reg_season_column_names:
        assert column in actual_columns, f"Column '{column}' missing."


def test_usports_playoffs_team_stats():
    """Test if usport_team_stats returns a valid DataFrame with expected columns and matching row data."""

    team_stats_df = usport_team_stats("men", "playoffs")

    assert isinstance(team_stats_df, DataFrame), "Expected a pandas DataFrame."
    assert not team_stats_df.empty, "DataFrame is empty."

    actual_columns = team_stats_df.columns.tolist()
    for column in expected_playoffs_season_column_names:
        assert column in actual_columns, f"Column '{column}' missing."
