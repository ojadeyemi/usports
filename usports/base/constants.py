"""Shared constants across all sports."""

# Base URL
BASE_URL = "https://universitysport.prestosports.com/sports"

# Season identifiers
FALL_SEASON = "2025-26"
WINTER_SEASON = "2024-25"

BASKETBALL = "basketball"
FOOTBALL = "football"
ICE_HOCKEY = "ice_hockey"
SOCCER = "soccer"
VOLLEYBALL = "volleyball"


# Current season based on sport type
def get_current_season(sport: str) -> str:
    """Get current season based on sport type."""
    fall_sports = [FOOTBALL, SOCCER]

    if any(s in sport.lower() for s in fall_sports):
        return FALL_SEASON
    return WINTER_SEASON


# Parser settings
BS4_PARSER = "html.parser"
TIMEOUT = 60000

OUA = "OUA"
RSEQ = "RSEQ"
CW = "CW"
AUS = "AUS"

# Stats table offsets
PLAYER_SEASON_TOTALS_STATS_START_INDEX = 3
BASKETBALL_PLAYER_STATS_OFFSET = 5
FOOTBALL_PLAYER_STATS_OFFSET = 3


# Conference mappings (shared across all sports)
DEFAULT_SCHOOL_CONFERENCES = {
    "Acadia": AUS,
    "Alberta": CW,
    "Algoma": OUA,
    "Bishop's": RSEQ,
    "Brandon": CW,
    "Brock": OUA,
    "Calgary": CW,
    "Cape Breton": AUS,
    "Carleton": OUA,
    "Concordia": RSEQ,
    "ETS": RSEQ,
    "Dalhousie": AUS,
    "Guelph": OUA,
    "Lakehead": OUA,
    "Laurentian": OUA,
    "Laurier": OUA,
    "Laval": RSEQ,
    "Lethbridge": CW,
    "MacEwan": CW,
    "Manitoba": CW,
    "McGill": RSEQ,
    "McMaster": OUA,
    "Memorial": AUS,
    "Moncton": AUS,
    "Montreal": RSEQ,
    "Mount Allison": AUS,
    "Mount Royal": CW,
    "Nipissing": OUA,
    "Ontario Tech": OUA,
    "Ottawa": OUA,
    "Queen's": OUA,
    "Regina": CW,
    "RMC": OUA,
    "Saint Mary's": AUS,
    "Saskatchewan": CW,
    "Sherbrooke": RSEQ,
    "StFX": AUS,
    "St. Thomas": AUS,
    "Thompson Rivers": CW,
    "Toronto": OUA,
    "Toronto Metropolitan": OUA,
    "Trent": OUA,
    "Trinity Western": CW,
    "UBC": CW,
    "UBC Okanagan": CW,
    "UFV": CW,
    "UNB": AUS,
    "UNBC": CW,
    "UPEI": AUS,
    "UQAC": RSEQ,
    "UQAM": RSEQ,
    "UQTR": RSEQ,
    "Victoria": CW,
    "Waterloo": OUA,
    "Western": OUA,
    "Windsor": OUA,
    "Winnipeg": CW,
    "York": OUA,
}

LEAGUE_CONFERENCE_OVERRIDES = {
    ICE_HOCKEY: {
        "McGill": OUA,  # McGill is normally RSEQ, but in hockey they're OUA
        "UQTR": OUA,
        "Concordia": OUA,  # Concordia is normally RSEQ, but in hockey they're OUA
    },
    FOOTBALL: {},
    VOLLEYBALL: {
        "Dalhousie": RSEQ,  # Dalhousie is normally AUS, but in volleyball they're RSEQ
        "UNB": RSEQ,
    },
    SOCCER: {},
}


def get_season_urls(sport: str) -> dict[str, str]:
    """Get season URL mappings based on sport."""
    season = get_current_season(sport)
    return {
        "regular": season,
        "playoffs": f"{season}p",
        "championship": f"{season}c",
    }
