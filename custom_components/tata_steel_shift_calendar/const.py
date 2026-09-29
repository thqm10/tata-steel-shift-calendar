"""Constants for the Tata Steel shift calendar integration."""

from __future__ import annotations

from datetime import date, time
from typing import Final
from zoneinfo import ZoneInfo

DOMAIN: Final = "tata_steel_shift_calendar"
VERSION: Final = "2.1.5"

CONF_TEAM: Final = "team"

DEVICE_MODEL: Final = "Tata Steel 5-ploegenrooster"

# The reference date and February/March correction are part of the validated
# roster model. Do not change them without re-validating against a known roster.
REFERENCE_DATE: Final = date(2023, 1, 30)

TATA_TIME_ZONE_NAME: Final = "Europe/Amsterdam"
TATA_TIME_ZONE: Final = ZoneInfo(TATA_TIME_ZONE_NAME)
REFRESH_HOURS: Final = (0, 6, 14, 22)

TEAM_COLORS: Final = ("red", "green", "blue", "yellow", "white")
TEAM_NAMES_NL: Final = {
    "red": "Rood",
    "green": "Groen",
    "blue": "Blauw",
    "yellow": "Geel",
    "white": "Wit",
}
TEAM_NAMES_EN: Final = {
    "red": "Red",
    "green": "Green",
    "blue": "Blue",
    "yellow": "Yellow",
    "white": "White",
}

SHIFT_MORNING: Final = "morning"
SHIFT_AFTERNOON: Final = "afternoon"
SHIFT_NIGHT: Final = "night"
SHIFT_OFF: Final = "off"
SHIFT_STATES: Final = (SHIFT_MORNING, SHIFT_AFTERNOON, SHIFT_NIGHT, SHIFT_OFF)
WORK_SHIFT_STATES: Final = (SHIFT_MORNING, SHIFT_AFTERNOON, SHIFT_NIGHT)

SHIFT_BY_INDEX: Final = {
    0: SHIFT_MORNING,
    1: SHIFT_AFTERNOON,
    2: SHIFT_NIGHT,
}

SHIFT_ICONS: Final = {
    SHIFT_MORNING: "mdi:weather-sunset-up",
    SHIFT_AFTERNOON: "mdi:white-balance-sunny",
    SHIFT_NIGHT: "mdi:weather-night",
    SHIFT_OFF: "mdi:home-clock",
}

SHIFT_TIMES: Final = {
    SHIFT_MORNING: (time(6, 0), time(14, 0)),
    SHIFT_AFTERNOON: (time(14, 0), time(22, 0)),
    SHIFT_NIGHT: (time(22, 0), time(6, 0)),
}


def language_code(language: str) -> str:
    """Normalize a Home Assistant language code for bundled translations."""
    return "nl" if language.lower().startswith("nl") else "en"


def team_display_name(team_color: str, language: str) -> str:
    """Return a localized team-color display name."""
    names = TEAM_NAMES_NL if language_code(language) == "nl" else TEAM_NAMES_EN
    return names[team_color]


def roster_title(team_color: str, language: str) -> str:
    """Return the config-entry/device title for a team color."""
    if language_code(language) == "nl":
        return f"Ploegendienst rooster {team_display_name(team_color, language)}"
    return f"Shift roster {team_display_name(team_color, language)}"
