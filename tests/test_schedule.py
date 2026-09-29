"""Regression tests for the pure local Tata Steel roster engine."""

from __future__ import annotations

from datetime import date, datetime, timedelta
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "custom_components" / "tata_steel_shift_calendar"
PACKAGE_NAME = "tata_steel_shift_calendar"

package = types.ModuleType(PACKAGE_NAME)
package.__path__ = [str(PACKAGE_DIR)]
sys.modules.setdefault(PACKAGE_NAME, package)


def _load_module(name: str):
    full_name = f"{PACKAGE_NAME}.{name}"
    if full_name in sys.modules:
        return sys.modules[full_name]
    spec = importlib.util.spec_from_file_location(full_name, PACKAGE_DIR / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[full_name] = module
    spec.loader.exec_module(module)
    return module


const = _load_module("const")
schedule = _load_module("schedule")


def test_manifest_domain_and_version_match_constants() -> None:
    manifest = json.loads((PACKAGE_DIR / "manifest.json").read_text())
    assert manifest["domain"] == const.DOMAIN == "tata_steel_shift_calendar"
    assert manifest["version"] == const.VERSION == "2.1.5"


def test_full_supplied_ics_period_matches_golden_digest() -> None:
    start = date(2026, 3, 30)
    end = date(2027, 8, 2)
    lines: list[str] = []
    day = start
    while day <= end:
        morning, afternoon, night = schedule.colors_for_date(day)
        lines.append(f"{day:%Y%m%d}|{morning}|{afternoon}|{night}")
        day += timedelta(days=1)

    assert len(lines) == 491
    digest = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    assert digest == "3eea27af8b377cfaa8399ce31a7b5ebb9eea6eeac5c39e01b4b649ed0c2bb45b"


def test_internal_states_are_language_neutral() -> None:
    valid = {"morning", "afternoon", "night", "off"}
    for team_color in const.TEAM_COLORS:
        info = schedule.shift_for_date(date(2026, 9, 22), team_color)
        assert info.shift in valid


def test_non_leap_february_march_correction_matches_reference() -> None:
    assert schedule.colors_for_date(date(2027, 2, 28)) == ("white", "blue", "red")
    assert schedule.colors_for_date(date(2027, 3, 1)) == ("green", "white", "blue")


def test_leap_day_does_not_apply_non_leap_skip() -> None:
    assert schedule.cycle_day(date(2024, 2, 28)) == 16
    assert schedule.cycle_day(date(2024, 2, 29)) == 17
    assert schedule.cycle_day(date(2024, 3, 1)) == 18


def test_night_shift_remains_active_after_midnight() -> None:
    tz = schedule.TATA_TIME_ZONE
    info = schedule.active_shift(datetime(2026, 9, 22, 2, 0, tzinfo=tz), "red")
    assert info is not None
    assert info.day == date(2026, 9, 21)
    assert info.shift == "night"


def test_dst_fall_back_preserves_local_shift_times() -> None:
    info = schedule.shift_for_date(date(2026, 10, 24), "blue")
    assert info.shift == "night"
    start, end = schedule.shift_datetimes(info)
    assert start.hour == 22
    assert end.hour == 6
    assert start.utcoffset() == timedelta(hours=2)
    assert end.utcoffset() == timedelta(hours=1)


def test_next_refresh_uses_only_roster_boundaries() -> None:
    tz = schedule.TATA_TIME_ZONE
    assert schedule.next_refresh_time(
        datetime(2026, 9, 22, 13, 59, tzinfo=tz)
    ) == datetime(2026, 9, 22, 14, 0, tzinfo=tz)
    assert schedule.next_refresh_time(
        datetime(2026, 9, 22, 22, 0, tzinfo=tz)
    ) == datetime(2026, 9, 23, 0, 0, tzinfo=tz)


def test_all_five_team_colors_are_supported() -> None:
    for team_color in ("red", "green", "blue", "yellow", "white"):
        assert schedule.shift_for_date(date(2026, 3, 30), team_color).team_color == team_color


def test_invalid_team_color_is_rejected() -> None:
    try:
        schedule.shift_for_date(date(2026, 3, 30), "purple")
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid team color should raise ValueError")


def test_year_transition_matches_reference_period() -> None:
    assert schedule.colors_for_date(date(2026, 12, 31)) == ("green", "white", "red")
    assert schedule.colors_for_date(date(2027, 1, 1)) == ("green", "white", "blue")


def test_calendar_query_includes_overlapping_night_shift() -> None:
    tz = schedule.TATA_TIME_ZONE
    results = schedule.shifts_overlapping(
        datetime(2026, 9, 22, 1, 0, tzinfo=tz),
        datetime(2026, 9, 22, 7, 0, tzinfo=tz),
        "red",
    )
    assert len(results) == 1
    info, start, end = results[0]
    assert info.shift == "night"
    assert start == datetime(2026, 9, 21, 22, 0, tzinfo=tz)
    assert end == datetime(2026, 9, 22, 6, 0, tzinfo=tz)


def test_next_shift_and_start_refer_to_same_shift_including_later_today() -> None:
    tz = schedule.TATA_TIME_ZONE
    info, start, end = schedule.next_upcoming_shift(
        datetime(2026, 9, 22, 13, 0, tzinfo=tz),
        "white",
    )
    assert info.shift == "afternoon"
    assert start == datetime(2026, 9, 22, 14, 0, tzinfo=tz)
    assert end == datetime(2026, 9, 22, 22, 0, tzinfo=tz)


def test_translations_cover_all_shift_states_and_team_colors() -> None:
    for language in ("nl", "en"):
        data = json.loads((PACKAGE_DIR / "translations" / f"{language}.json").read_text())
        selector_options = data["selector"]["team_color"]["options"]
        assert set(selector_options) == set(const.TEAM_COLORS)
        for key in ("today_shift", "tomorrow_shift", "current_shift"):
            assert set(data["entity"]["sensor"][key]["state"]) == set(const.SHIFT_STATES)
        assert set(data["entity"]["sensor"]["next_shift"]["state"]) == set(
            const.WORK_SHIFT_STATES
        )


def test_hacs_metadata_has_minimum_home_assistant_version() -> None:
    hacs = json.loads((ROOT / "hacs.json").read_text())
    assert hacs["homeassistant"] == "2026.8.0"


def test_removed_next_free_period_is_not_exposed() -> None:
    sensor_source = (PACKAGE_DIR / "sensor.py").read_text()
    assert "NextFreePeriodSensor" not in sensor_source
    for language in ("nl", "en"):
        data = json.loads((PACKAGE_DIR / "translations" / f"{language}.json").read_text())
        assert "next_free_period" not in data["entity"]["sensor"]


def test_obsolete_next_free_period_registry_cleanup_is_kept() -> None:
    init_source = (PACKAGE_DIR / "__init__.py").read_text()
    assert f'{{entry.entry_id}}_next_free_period' in init_source


def test_public_display_name_matches_release_text() -> None:
    manifest = json.loads((PACKAGE_DIR / "manifest.json").read_text())
    hacs = json.loads((ROOT / "hacs.json").read_text())
    assert manifest["name"] == "Tata Steel ploegendienstkalender"
    assert hacs["name"] == manifest["name"]


def test_no_personal_author_name_is_bundled_in_component_source() -> None:
    for path in PACKAGE_DIR.rglob("*"):
        if path.is_file() and path.suffix in {".py", ".json"}:
            assert "Thom Hof" not in path.read_text()


def test_shift_sensors_are_enum_entities_for_automation_editor() -> None:
    sensor_source = (PACKAGE_DIR / "sensor.py").read_text()
    assert "SensorDeviceClass.ENUM" in sensor_source
    assert "_attr_options = list(SHIFT_STATES)" in sensor_source
    assert "_attr_options = list(WORK_SHIFT_STATES)" in sensor_source


def test_automation_facing_entities_do_not_expose_extra_state_attributes() -> None:
    for filename in ("sensor.py", "binary_sensor.py"):
        source = (PACKAGE_DIR / filename).read_text()
        assert "extra_state_attributes" not in source


def test_timestamp_and_calendar_automation_entities_are_kept() -> None:
    sensor_source = (PACKAGE_DIR / "sensor.py").read_text()
    calendar_source = (PACKAGE_DIR / "calendar.py").read_text()
    assert "SensorDeviceClass.TIMESTAMP" in sensor_source
    assert "class NextShiftStartSensor" in sensor_source
    assert "class TataSteelShiftCalendar" in calendar_source


def test_binary_automation_entities_are_kept_simple() -> None:
    source = (PACKAGE_DIR / "binary_sensor.py").read_text()
    assert "class WorkingTodayBinarySensor" in source
    assert "class CurrentlyWorkingBinarySensor" in source
    assert "BinarySensorDeviceClass" not in source


def test_calendar_public_name_and_object_id_use_agenda() -> None:
    nl = json.loads((PACKAGE_DIR / "translations" / "nl.json").read_text())
    assert nl["entity"]["calendar"]["calendar"]["name"] == "Agenda"
    calendar_source = (PACKAGE_DIR / "calendar.py").read_text()
    assert 'self._set_suggested_object_id("agenda")' in calendar_source


def test_pre_release_calendar_entity_id_migration_is_kept() -> None:
    init_source = (PACKAGE_DIR / "__init__.py").read_text()
    assert "_async_migrate_calendar_entity_id" in init_source
    assert 'for old_suffix in ("_rooster", "_roster")' in init_source
    assert 'new_object_id = f"{object_id[:-len(old_suffix)]}_agenda"' in init_source
