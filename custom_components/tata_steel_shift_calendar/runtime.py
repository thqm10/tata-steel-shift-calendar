"""Shared runtime update scheduler for the Tata Steel shift calendar."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers.event import async_track_point_in_utc_time

from .schedule import as_utc, next_refresh_time, tata_now


class RosterRuntime:
    """Maintain one roster-boundary timer per config entry."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._listeners: set[Callable[[], None]] = set()
        self._cancel_timer: CALLBACK_TYPE | None = None
        self._next_refresh: datetime | None = None

    @property
    def next_refresh(self) -> datetime | None:
        """Return the next scheduled local roster refresh."""
        return self._next_refresh

    @callback
    def start(self) -> None:
        """Start the shared roster-boundary timer."""
        self._schedule_next_refresh()

    @callback
    def stop(self) -> None:
        """Stop the shared roster-boundary timer."""
        if self._cancel_timer is not None:
            self._cancel_timer()
            self._cancel_timer = None
        self._next_refresh = None
        self._listeners.clear()

    @callback
    def subscribe(self, listener: Callable[[], None]) -> CALLBACK_TYPE:
        """Subscribe an entity to roster-boundary updates."""
        self._listeners.add(listener)

        @callback
        def unsubscribe() -> None:
            self._listeners.discard(listener)

        return unsubscribe

    @callback
    def _schedule_next_refresh(self) -> None:
        if self._cancel_timer is not None:
            self._cancel_timer()

        self._next_refresh = next_refresh_time(tata_now())
        self._cancel_timer = async_track_point_in_utc_time(
            self._hass,
            self._handle_refresh,
            as_utc(self._next_refresh),
        )

    @callback
    def _handle_refresh(self, _now: datetime) -> None:
        self._cancel_timer = None
        self._next_refresh = None
        for listener in tuple(self._listeners):
            listener()
        self._schedule_next_refresh()
