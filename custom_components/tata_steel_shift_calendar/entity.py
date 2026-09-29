"""Shared entity helpers for Tata Steel ploegendienstkalender."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo, Entity

from .const import CONF_TEAM, DEVICE_MODEL, DOMAIN, VERSION
from .runtime import RosterRuntime


def suggested_object_id(team_color: str, key: str) -> str:
    """Return a stable language-neutral suggested entity object ID."""
    return f"tata_steel_shift_calendar_{team_color}_{key}"


class TataSteelRosterEntity(Entity):
    """Base entity for Tata Steel ploegendienstkalender."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry
        self._team_color = str(entry.data[CONF_TEAM])
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            model=DEVICE_MODEL,
            sw_version=VERSION,
        )

    def _set_suggested_object_id(self, key: str) -> None:
        """Set a predictable entity ID suggestion for clean installations."""
        self._attr_suggested_object_id = suggested_object_id(self._team_color, key)

    async def async_added_to_hass(self) -> None:
        """Subscribe to the single shared roster refresh timer."""
        await super().async_added_to_hass()
        runtime = self._entry.runtime_data
        if isinstance(runtime, RosterRuntime):
            self.async_on_remove(runtime.subscribe(self.async_write_ha_state))
