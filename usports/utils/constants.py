"""Constants used across the U Sports  data fetching and processing modules."""

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
    "Mount Royal",
    "Nipissing",
    "Ontario Tech",
    "Ottawa",
    "Queen's",
    "Regina",
    "Saint Mary's",
    "Saskatchewan",
    "StFX",
    "Thompson Rivers",
    "Toronto",
    "Toronto Metropolitan",
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
