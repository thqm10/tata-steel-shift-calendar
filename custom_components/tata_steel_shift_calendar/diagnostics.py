"""Diagnostics for Tata Steel ploegendienst kalender."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_TEAM, TATA_TIME_ZONE_NAME, VERSION
from .runtime import RosterRuntime
from .schedule import active_shift, next_upcoming_shift, shift_for_date, tata_now


def _info_dict(info) -> dict[str, Any] | None:
    if info is None:
        return None
    return {
        "date": info.day.isoformat(),
        "team_color": info.team_color,
        "shift": info.shift,
        "working": info.working,
        "cycle_day": info.cycle_day,
        "morning_team": info.morning_team,
        "afternoon_team": info.afternoon_team,
        "night_team": info.night_team,
    }


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return non-personal diagnostics for a config entry."""
    now = tata_now()
    team_color = str(entry.data[CONF_TEAM])
    today = shift_for_date(now.date(), team_color)
    current = active_shift(now, team_color)
    next_info, next_start, next_end = next_upcoming_shift(now, team_color)

    runtime = entry.runtime_data
    next_refresh = (
        runtime.next_refresh.isoformat()
        if isinstance(runtime, RosterRuntime) and runtime.next_refresh is not None
        else None
    )

    return {
        "integration": {
            "version": VERSION,
            "timezone": TATA_TIME_ZONE_NAME,
            "offline_calculation": True,
        },
        "config": {"team_color": team_color},
        "runtime": {
            "now": now.isoformat(),
            "next_refresh": next_refresh,
            "today": _info_dict(today),
            "current_shift": _info_dict(current),
            "next_shift": {
                **(_info_dict(next_info) or {}),
                "start": next_start.isoformat(),
                "end": next_end.isoformat(),
            },
        },
    }
