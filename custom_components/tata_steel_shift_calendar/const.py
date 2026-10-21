"""Constants for the Tata Steel shift calendar integration."""

from __future__ import annotations

from datetime import date, time
from typing import Final
from zoneinfo import ZoneInfo

DOMAIN: Final = "tata_steel_shift_calendar"
VERSION: Final = "3.0.0"

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

# Internal roster states. These stay language-neutral because they are part of
# the validated calculation engine and are never exposed as public sensor states.
SHIFT_MORNING: Final = "morning"
SHIFT_AFTERNOON: Final = "afternoon"
SHIFT_NIGHT: Final = "night"
SHIFT_OFF: Final = "off"
SHIFT_STATES: Final = (SHIFT_MORNING, SHIFT_AFTERNOON, SHIFT_NIGHT, SHIFT_OFF)
WORK_SHIFT_STATES: Final = (SHIFT_MORNING, SHIFT_AFTERNOON, SHIFT_NIGHT)

# Public Home Assistant states. These are deliberately Dutch so automations
# never need to use English states such as "morning" or "afternoon".
PUBLIC_SHIFT_MORNING: Final = "ochtenddienst"
PUBLIC_SHIFT_AFTERNOON: Final = "middagdienst"
PUBLIC_SHIFT_NIGHT: Final = "nachtdienst"
PUBLIC_SHIFT_OFF: Final = "vrij"

PUBLIC_SHIFT_STATES: Final = (
    PUBLIC_SHIFT_MORNING,
    PUBLIC_SHIFT_AFTERNOON,
    PUBLIC_SHIFT_NIGHT,
    PUBLIC_SHIFT_OFF,
)
WORK_SHIFT_PUBLIC_STATES: Final = (
    PUBLIC_SHIFT_MORNING,
    PUBLIC_SHIFT_AFTERNOON,
    PUBLIC_SHIFT_NIGHT,
)

SHIFT_PUBLIC_STATE: Final = {
    SHIFT_MORNING: PUBLIC_SHIFT_MORNING,
    SHIFT_AFTERNOON: PUBLIC_SHIFT_AFTERNOON,
    SHIFT_NIGHT: PUBLIC_SHIFT_NIGHT,
    SHIFT_OFF: PUBLIC_SHIFT_OFF,
}

SHIFT_PUBLIC_NAME: Final = {
    SHIFT_MORNING: "Ochtenddienst",
    SHIFT_AFTERNOON: "Middagdienst",
    SHIFT_NIGHT: "Nachtdienst",
    SHIFT_OFF: "Vrij",
}

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


def team_display_name(team_color: str, _language: str | None = None) -> str:
    """Return the Dutch team-color display name."""
    return TEAM_NAMES_NL[team_color]


def roster_title(team_color: str, _language: str | None = None) -> str:
    """Return the Dutch config-entry/device title for a team color."""
    return f"Ploegendienst rooster {team_display_name(team_color)}"


def public_shift_state(shift: str) -> str:
    """Return the Dutch public Home Assistant state for an internal shift."""
    return SHIFT_PUBLIC_STATE[shift]


def public_shift_name(shift: str) -> str:
    """Return the Dutch human-readable name for an internal shift."""
    return SHIFT_PUBLIC_NAME[shift]
