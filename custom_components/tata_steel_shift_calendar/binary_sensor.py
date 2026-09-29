"""Binary sensor platform for Tata Steel ploegendienstkalender."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import SHIFT_ICONS, SHIFT_OFF
from .entity import TataSteelRosterEntity
from .schedule import active_shift, shift_for_date, tata_now


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up roster binary sensors."""
    async_add_entities(
        (
            WorkingTodayBinarySensor(entry),
            CurrentlyWorkingBinarySensor(entry),
        )
    )


class WorkingTodayBinarySensor(TataSteelRosterEntity, BinarySensorEntity):
    """Indicate whether the selected team is scheduled to work today."""

    _attr_translation_key = "working_today"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_working_today"
        self._set_suggested_object_id("working_today")

    def _info(self):
        return shift_for_date(tata_now().date(), self._team_color)

    @property
    def is_on(self) -> bool:
        return self._info().working

    @property
    def icon(self) -> str:
        return SHIFT_ICONS[self._info().shift]


class CurrentlyWorkingBinarySensor(TataSteelRosterEntity, BinarySensorEntity):
    """Indicate whether the selected team is working at this exact moment."""

    _attr_translation_key = "currently_working"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_currently_working"
        self._set_suggested_object_id("currently_working")

    def _info(self):
        return active_shift(tata_now(), self._team_color)

    @property
    def is_on(self) -> bool:
        return self._info() is not None

    @property
    def icon(self) -> str:
        info = self._info()
        return SHIFT_ICONS[info.shift] if info is not None else SHIFT_ICONS[SHIFT_OFF]
