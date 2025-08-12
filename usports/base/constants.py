"""Shared constants across all sports."""

# Base URL
BASE_URL = "https://universitysport.prestosports.com/sports"

# Current season
SEASON = "2024-25"

# Season URL mappings
SEASON_URLS = {
    "regular": SEASON,
    "playoffs": f"{SEASON}p",
    "championship": f"{SEASON}c",
}

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

BS4_PARSER = "html.parser"
# Season identifier, update this when the season changes
SEASON = "2024-25"

# Mapping of season options to their corresponding URL fragments
SEASON_URLS = {
    "regular": SEASON,
    "playoffs": f"{SEASON}p",
    "championship": f"{SEASON}c",
}


BASKETBALL = "basketball"
FOOTBALL = "football"
ICE_HOCKEY = "ice_hockey"
SOCCER = "soccer"
VOLLEYBALL = "volleyball"

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
    "Sherbooke": RSEQ,
    "StFX": AUS,
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
    # other leagues can be added as needed
}
