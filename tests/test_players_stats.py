"""Test for players function to worek as expected"""

from pandas import DataFrame

from usports.basketball import usports_bball_players
from usports.football import usports_fball_players

from .test_data import expected_basketball_players_df_columns, expected_football_players_df_column


def test_usports_bball_player_stats():
    """Test if usports_players_stats function returns a non-empty pandas DataFrame."""

    player_stats_df = usports_bball_players("women")

    assert isinstance(player_stats_df, DataFrame), "Player statistics should be a pandas DataFrame"
    assert not player_stats_df.empty, "Player statistics DataFrame is empty"

    actual_columns = player_stats_df.columns.tolist()
    for column in expected_basketball_players_df_columns:
        assert column in actual_columns, f"Expected column '{column}' not found in player_stats_df"


def test_usports_bball_playoffs_player_stats():
    """Test if usports_players_stats function returns a non-empty pandas DataFrame."""

    player_stats_df = usports_bball_players("men", "playoffs")

    assert isinstance(player_stats_df, DataFrame), "Player statistics should be a pandas DataFrame"
    assert not player_stats_df.empty, "Player statistics DataFrame is empty"

    actual_columns = player_stats_df.columns.tolist()
    for column in expected_basketball_players_df_columns:
        assert column in actual_columns, f"Expected column '{column}' not found in basketball player_stats_df"


def test_usports_football_player_stats():
    player_stats_df = usports_fball_players("regular")
    assert isinstance(player_stats_df, DataFrame), "Player statistics should be a pandas DataFrame"
    assert not player_stats_df.empty, "Player statistics DataFrame is empty"

    actual_columns = player_stats_df.columns.tolist()
    for column in expected_football_players_df_column:
        assert column in actual_columns, f"Expected column '{column}' not found in football player_stats_df"
