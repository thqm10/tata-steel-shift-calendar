"""Sensor platform for Tata Steel ploegendienstkalender."""

from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    SHIFT_ICONS,
    SHIFT_OFF,
    SHIFT_STATES,
    WORK_SHIFT_STATES,
)
from .entity import TataSteelRosterEntity
from .schedule import ShiftInfo, active_shift, next_upcoming_shift, shift_for_date, tata_now


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up work-shift sensors from a config entry."""
    async_add_entities(
        (
            TodayShiftSensor(entry),
            TomorrowShiftSensor(entry),
            NextShiftSensor(entry),
            CurrentShiftSensor(entry),
            NextShiftStartSensor(entry),
        )
    )


class _BaseDateShiftSensor(TataSteelRosterEntity, SensorEntity):
    """Base class for date-based shift sensors."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = list(SHIFT_STATES)
    _date_offset = 0
    _object_id_key = "date_shift"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._set_suggested_object_id(self._object_id_key)

    def _info(self) -> ShiftInfo:
        target = tata_now().date() + timedelta(days=self._date_offset)
        return shift_for_date(target, self._team_color)

    @property
    def native_value(self) -> str:
        return self._info().shift

    @property
    def icon(self) -> str:
        return SHIFT_ICONS[self._info().shift]


class TodayShiftSensor(_BaseDateShiftSensor):
    """Sensor for today's scheduled shift."""

    _attr_translation_key = "today_shift"
    _date_offset = 0
    _object_id_key = "today_shift"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_today_shift"


class TomorrowShiftSensor(_BaseDateShiftSensor):
    """Sensor for tomorrow's scheduled shift."""

    _attr_translation_key = "tomorrow_shift"
    _date_offset = 1
    _object_id_key = "tomorrow_shift"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_tomorrow_shift"


class NextShiftSensor(TataSteelRosterEntity, SensorEntity):
    """Sensor for the next actual shift starting after now."""

    _attr_translation_key = "next_shift"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = list(WORK_SHIFT_STATES)

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_next_shift"
        self._set_suggested_object_id("next_shift")

    def _next(self) -> tuple[ShiftInfo, datetime, datetime]:
        return next_upcoming_shift(tata_now(), self._team_color)

    @property
    def native_value(self) -> str:
        info, _start, _end = self._next()
        return info.shift

    @property
    def icon(self) -> str:
        info, _start, _end = self._next()
        return SHIFT_ICONS[info.shift]


class CurrentShiftSensor(TataSteelRosterEntity, SensorEntity):
    """Sensor showing the shift active at this exact moment."""

    _attr_translation_key = "current_shift"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = list(SHIFT_STATES)

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_current_shift"
        self._set_suggested_object_id("current_shift")

    def _active_info(self) -> ShiftInfo | None:
        return active_shift(tata_now(), self._team_color)

    @property
    def native_value(self) -> str:
        info = self._active_info()
        return info.shift if info is not None else SHIFT_OFF

    @property
    def icon(self) -> str:
        return SHIFT_ICONS[self.native_value]


class NextShiftStartSensor(TataSteelRosterEntity, SensorEntity):
    """Timestamp sensor for the same shift exposed by NextShiftSensor."""

    _attr_translation_key = "next_shift_start"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:calendar-start"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_next_shift_start"
        self._set_suggested_object_id("next_shift_start")

    def _next(self) -> tuple[ShiftInfo, datetime, datetime]:
        return next_upcoming_shift(tata_now(), self._team_color)

    @property
    def native_value(self) -> datetime:
        _info, start, _end = self._next()
        return start
