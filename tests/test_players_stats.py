"""Test for players function to worek as expected"""

from pandas import DataFrame

from usports.basketball import usport_bball_players_stats

from .test_data import expected_basketball_players_df_columns


def test_usports_bball_player_stats():
    """Test if usport_players_stats function returns a non-empty pandas DataFrame."""

    player_stats_df = usport_bball_players_stats("women")

    assert isinstance(player_stats_df, DataFrame), "Player statistics should be a pandas DataFrame"
    assert not player_stats_df.empty, "Player statistics DataFrame is empty"

    actual_columns = player_stats_df.columns.tolist()
    for column in expected_basketball_players_df_columns:
        assert column in actual_columns, f"Expected column '{column}' not found in player_stats_df"


def test_usports_bball_playoffs_player_stats():
    """Test if usport_players_stats function returns a non-empty pandas DataFrame."""

    player_stats_df = usport_bball_players_stats("men", "playoffs")

    assert isinstance(player_stats_df, DataFrame), "Player statistics should be a pandas DataFrame"
    assert not player_stats_df.empty, "Player statistics DataFrame is empty"

    actual_columns = player_stats_df.columns.tolist()
    for column in expected_basketball_players_df_columns:
        assert column in actual_columns, f"Expected column '{column}' not found in player_stats_df"
