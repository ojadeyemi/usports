"""Constants used across the U Sports data fetching and processing modules."""

from typing import Literal

BS4_PARSER = "html.parser"
# Season identifier, update this when the season changes
SEASON = "2024-25"

# Mapping of season options to their corresponding URL fragments
SEASON_URLS = {
    "regular": SEASON,
    "playoffs": f"{SEASON}p",
    "championship": f"{SEASON}c",
}

OUA = "OUA"
RSEQ = "RSEQ"
CW = "CW"
AUS = "AUS"

CONFERENCES = Literal["OUA", "RSEQ", "CW", "AUS"]

# Base URL for the U Sports website
BASE_URL = "https://universitysport.prestosports.com/sports"


TIMEOUT = 60000  # 60 seconds
PLAYER_SEASON_TOTALS_STATS_START_INDEX = 3
BASKETBALL_PLAYER_STATS_OFFSET = 5


# Usport teams
TeamName = Literal[
    "Acadia",
    "Alberta",
    "Algoma",
    "Bishop's",
    "Brandon",
    "Brock",
    "Calgary",
    "Cape Breton",
    "Carleton",
    "Concordia",
    "Dalhousie",
    "Guelph",
    "Lakehead",
    "Laurentian",
    "Laurier",
    "Laval",
    "Lethbridge",
    "MacEwan",
    "Manitoba",
    "McGill",
    "McMaster",
    "Memorial",
    "Montreal",
    "Mount Royal",
    "Nipissing",
    "Ontario Tech",
    "Ottawa",
    "Queen's",
    "Regina",
    "RMC",
    "Saint Mary's",
    "Saskatchewan",
    "Sherbooke",
    "StFX",
    "Thompson Rivers",
    "Toronto",
    "Toronto Metropolitan",
    "Trent",
    "Trinity Western",
    "UBC",
    "UBC Okanagan",
    "UFV",
    "UNB",
    "UNBC",
    "UPEI",
    "UQAM",
    "Victoria",
    "Waterloo",
    "Western",
    "Windsor",
    "Winnipeg",
    "York",
]


TEAM_CONFERENCES = {
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
    "Montreal": RSEQ,
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
    "Victoria": CW,
    "Waterloo": OUA,
    "Western": OUA,
    "Windsor": OUA,
    "Winnipeg": CW,
    "York": OUA,
}
