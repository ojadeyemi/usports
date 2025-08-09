from typing import Literal, TypeAlias

SeasonType: TypeAlias = Literal["regular", "playoffs", "championship"]

LeagueType: TypeAlias = Literal["m", "w"]

SportCode: TypeAlias = Literal["mbkb", "wbkb", "fball", "mice", "wice", "msoc", "wsoc", "mvb", "wvb"]

ConferenceType: TypeAlias = Literal["OUA", "RSEQ", "CW", "AUS"]
