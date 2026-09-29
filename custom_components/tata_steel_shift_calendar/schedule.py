"""Pure Tata Steel 5-shift roster calculations.

The cycle, reference date and non-leap-year February/March correction are
intentionally preserved. They were compared with the supplied Shifts.ics for
2026-03-30 through 2027-08-02 (491 calendar days / 1,473 calendar events)
without roster mismatches.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from .const import (
    REFERENCE_DATE,
    REFRESH_HOURS,
    SHIFT_BY_INDEX,
    SHIFT_NIGHT,
    SHIFT_OFF,
    SHIFT_TIMES,
    TATA_TIME_ZONE,
    TEAM_COLORS,
)

CYCLE: tuple[tuple[str, str, str], ...] = (
    ("blue", "red", "green"),
    ("blue", "red", "yellow"),
    ("white", "blue", "yellow"),
    ("white", "blue", "red"),
    ("green", "white", "red"),
    ("green", "white", "blue"),
    ("yellow", "green", "blue"),
    ("yellow", "green", "white"),
    ("red", "yellow", "white"),
    ("red", "yellow", "green"),
) * 2


@dataclass(frozen=True, slots=True)
class ShiftInfo:
    """Calculated shift information for one roster date and team color."""

    day: date
    team_color: str
    shift: str
    shift_index: int | None
    working: bool
    cycle_day: int
    morning_team: str
    afternoon_team: str
    night_team: str



def tata_now() -> datetime:
    """Return the current time in the fixed Tata Steel roster timezone."""
    return datetime.now(TATA_TIME_ZONE)


def _as_tata_time(value: datetime) -> datetime:
    """Normalize an aware datetime to Europe/Amsterdam."""
    if value.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")
    return value.astimezone(TATA_TIME_ZONE)


def _validate_team_color(team_color: str) -> None:
    """Validate a stable internal team color."""
    if team_color not in TEAM_COLORS:
        raise ValueError(f"Unsupported team color: {team_color}")


def _app_day_offset(target: date) -> int:
    """Reproduce the validated staalrooster date-offset calculation exactly."""
    raw = (REFERENCE_DATE - target).days
    offset = abs(raw) + 1 if raw < 0 else raw

    correction = 0
    marker = date(2023, 2, 28)
    while True:
        next_day = marker + timedelta(days=1)
        if target > marker and next_day.day != 29:
            correction += 1
        marker = marker.replace(year=marker.year + 1)
        if marker >= target:
            break

    return offset + correction


def cycle_day(target: date) -> int:
    """Return the 1-based day inside the validated 20-day cycle."""
    if target == REFERENCE_DATE:
        return 1

    offset = _app_day_offset(target)
    position = offset % 20 or 20

    if target > REFERENCE_DATE:
        return position

    return 20 - position + 1


def colors_for_date(target: date) -> tuple[str, str, str]:
    """Return morning, afternoon and night team colors for a roster date."""
    return CYCLE[cycle_day(target) - 1]


def shift_for_date(target: date, team_color: str) -> ShiftInfo:
    """Return shift information for one team color on a roster date."""
    _validate_team_color(team_color)

    colors = colors_for_date(target)
    index = colors.index(team_color) if team_color in colors else None
    shift = SHIFT_BY_INDEX[index] if index is not None else SHIFT_OFF

    return ShiftInfo(
        day=target,
        team_color=team_color,
        shift=shift,
        shift_index=index,
        working=index is not None,
        cycle_day=cycle_day(target),
        morning_team=colors[0],
        afternoon_team=colors[1],
        night_team=colors[2],
    )


def shift_datetimes(info: ShiftInfo) -> tuple[datetime, datetime] | None:
    """Return Europe/Amsterdam start/end datetimes for a working shift."""
    if not info.working:
        return None

    start_time, end_time = SHIFT_TIMES[info.shift]
    start = datetime.combine(info.day, start_time, tzinfo=TATA_TIME_ZONE)
    end_day = info.day + timedelta(days=1) if info.shift == SHIFT_NIGHT else info.day
    end = datetime.combine(end_day, end_time, tzinfo=TATA_TIME_ZONE)
    return start, end


def active_shift(at: datetime, team_color: str) -> ShiftInfo | None:
    """Return the shift active at an instant, including overnight work."""
    _validate_team_color(team_color)
    local = _as_tata_time(at)

    for target in (local.date() - timedelta(days=1), local.date()):
        info = shift_for_date(target, team_color)
        bounds = shift_datetimes(info)
        if bounds is None:
            continue
        start, end = bounds
        if start <= local < end:
            return info

    return None


def next_upcoming_shift(
    at: datetime,
    team_color: str,
) -> tuple[ShiftInfo, datetime, datetime]:
    """Return the next shift whose start is strictly after ``at``."""
    _validate_team_color(team_color)
    local = _as_tata_time(at)

    for days_ahead in range(0, 41):
        info = shift_for_date(local.date() + timedelta(days=days_ahead), team_color)
        bounds = shift_datetimes(info)
        if bounds is None:
            continue
        start, end = bounds
        if start > local:
            return info, start, end

    raise RuntimeError("No upcoming shift found within 40 days")


def shifts_overlapping(
    start: datetime,
    end: datetime,
    team_color: str,
) -> list[tuple[ShiftInfo, datetime, datetime]]:
    """Return locally calculated shifts overlapping a datetime range."""
    _validate_team_color(team_color)
    if end <= start:
        return []

    start_local = _as_tata_time(start)
    end_local = _as_tata_time(end)
    result: list[tuple[ShiftInfo, datetime, datetime]] = []

    day = start_local.date() - timedelta(days=1)
    final_day = end_local.date()

    while day <= final_day:
        info = shift_for_date(day, team_color)
        bounds = shift_datetimes(info)
        if bounds is not None:
            shift_start, shift_end = bounds
            if shift_end > start_local and shift_start < end_local:
                result.append((info, shift_start, shift_end))
        day += timedelta(days=1)

    return result


def next_refresh_time(at: datetime) -> datetime:
    """Return the next roster boundary in Europe/Amsterdam."""
    local = _as_tata_time(at)

    for days_ahead in (0, 1):
        target_day = local.date() + timedelta(days=days_ahead)
        for hour in REFRESH_HOURS:
            candidate = datetime(
                target_day.year,
                target_day.month,
                target_day.day,
                hour,
                tzinfo=TATA_TIME_ZONE,
            )
            if candidate > local:
                return candidate

    return (local + timedelta(days=1)).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


def as_utc(value: datetime) -> datetime:
    """Return an aware datetime converted to UTC."""
    return value.astimezone(timezone.utc)
