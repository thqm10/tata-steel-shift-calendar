"""Calendar platform for Tata Steel ploegendienst kalender."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import language_code, team_display_name
from .entity import TataSteelRosterEntity
from .schedule import ShiftInfo, shift_datetimes, shift_for_date, shifts_overlapping, tata_now

_SHIFT_NAMES = {
    "nl": {
        "morning": "Ochtenddienst",
        "afternoon": "Middagdienst",
        "night": "Nachtdienst",
    },
    "en": {
        "morning": "Morning shift",
        "afternoon": "Afternoon shift",
        "night": "Night shift",
    },
}


def _time_range(start: datetime, end: datetime) -> str:
    """Format the scheduled local shift times."""
    return f"{start:%H:%M}–{end:%H:%M}"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the locally calculated roster calendar."""
    async_add_entities([TataSteelShiftCalendar(entry)])


class TataSteelShiftCalendar(TataSteelRosterEntity, CalendarEntity):
    """Calendar containing all locally calculated working shifts."""

    _attr_translation_key = "calendar"
    _attr_icon = "mdi:calendar-clock"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_calendar"
        self._set_suggested_object_id("agenda")

    def _event_from_info(self, info: ShiftInfo) -> CalendarEvent | None:
        bounds = shift_datetimes(info)
        if bounds is None:
            return None
        start, end = bounds
        language = language_code(self.hass.config.language)
        shift_name = _SHIFT_NAMES[language][info.shift]
        team_name = team_display_name(info.team_color, language)
        return CalendarEvent(
            start=start,
            end=end,
            summary=f"{shift_name} · {_time_range(start, end)}",
            description=(
                f"Ploeg {team_name}" if language == "nl" else f"Team {team_name}"
            ),
        )

    def _create_event(self, day: date) -> CalendarEvent | None:
        return self._event_from_info(shift_for_date(day, self._team_color))

    @property
    def event(self) -> CalendarEvent | None:
        now = tata_now()
        today = now.date()
        candidates: list[CalendarEvent] = []
        for days_ahead in range(-1, 41):
            event = self._create_event(today + timedelta(days=days_ahead))
            if event is not None and event.end > now:
                candidates.append(event)
        return min(candidates, key=lambda item: item.start) if candidates else None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        events: list[CalendarEvent] = []
        for info, _start, _end in shifts_overlapping(
            start_date,
            end_date,
            self._team_color,
        ):
            event = self._event_from_info(info)
            if event is not None:
                events.append(event)
        return events
