"""Abstract base classes for all sports."""
from abc import ABC, abstractmethod
import pandas as pd
from .types import SeasonType, SportCode


class SportInterface(ABC):
    """Every sport must implement these methods."""
    
    @property
    @abstractmethod
    def sport_codes(self) -> dict[str, SportCode]:
        """Map league to sport code (e.g., {'men': 'mbkb'})"""
        pass
    
    @abstractmethod
    async def fetch_standings(self, league: str) -> pd.DataFrame:
        """
        Fetch W/L records - REGULAR SEASON ONLY.
        
        Returns columns:
        - team_name, games_played, wins, losses, 
        - win_percentage, points_for, points_against, conference
        """
        pass
    
    @abstractmethod
    async def fetch_team_stats(
        self, 
        league: str, 
        season: SeasonType
    ) -> pd.DataFrame:
        """
        Fetch performance stats - ALL SEASONS.
        No W/L columns!
        """
        pass
    
    @abstractmethod
    async def fetch_player_stats(
        self, 
        league: str, 
        season: SeasonType
    ) -> pd.DataFrame:
        """Fetch player statistics."""
        pass