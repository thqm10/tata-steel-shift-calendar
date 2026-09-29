"""Tata Steel ploegendienst kalender integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN
from .runtime import RosterRuntime

PLATFORMS: tuple[Platform, ...] = (
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.CALENDAR,
)


def _async_remove_obsolete_entities(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove entities that were dropped during the pre-public development cycle."""
    registry = er.async_get(hass)
    obsolete = (
        (Platform.SENSOR, f"{entry.entry_id}_next_free_period"),
    )

    for platform, unique_id in obsolete:
        entity_id = registry.async_get_entity_id(platform, DOMAIN, unique_id)
        if entity_id is not None:
            registry.async_remove(entity_id)


def _async_migrate_calendar_entity_id(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Rename the pre-release calendar entity ID from roster/rooster to agenda."""
    registry = er.async_get(hass)
    unique_id = f"{entry.entry_id}_calendar"
    entity_id = registry.async_get_entity_id(Platform.CALENDAR, DOMAIN, unique_id)
    if entity_id is None:
        return

    domain, object_id = entity_id.split(".", 1)
    for old_suffix in ("_rooster", "_roster"):
        if not object_id.endswith(old_suffix):
            continue

        new_object_id = f"{object_id[:-len(old_suffix)]}_agenda"
        new_entity_id = f"{domain}.{new_object_id}"
        if registry.async_get(new_entity_id) is None:
            registry.async_update_entity(entity_id, new_entity_id=new_entity_id)
        return


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a Tata Steel shift calendar config entry."""
    _async_remove_obsolete_entities(hass, entry)
    _async_migrate_calendar_entity_id(hass, entry)
    runtime = RosterRuntime(hass)
    entry.runtime_data = runtime
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    runtime.start()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Tata Steel shift calendar config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded and isinstance(entry.runtime_data, RosterRuntime):
        entry.runtime_data.stop()
    return unloaded
