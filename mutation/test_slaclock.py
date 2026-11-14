# ai-generated: 100% - Codex wrote behavioural tests from the course slaclock docstrings, including calendar and threshold boundaries.
"""Exercise public SLA behaviour independently of the module's implementation text."""

from datetime import datetime, timedelta

import pytest

import slaclock


@pytest.mark.parametrize("impact,urgency,expected", [
    (1, 1, "P1"), (1, 2, "P2"), (1, 3, "P3"),
    (2, 1, "P2"), (2, 2, "P3"), (2, 3, "P4"),
    (3, 1, "P3"), (3, 2, "P4"), (3, 3, "P4"),
])
def test_priority_matrix_and_vip(impact, urgency, expected):
    assert slaclock.priority_of(impact, urgency) == expected
    assert slaclock.priority_of(impact, urgency, False) == expected
    vip_expected = "P2" if expected in ("P3", "P4") else expected
    assert slaclock.priority_of(impact, urgency, True) == vip_expected


@pytest.mark.parametrize("invalid", [-5, 0, 4, 99, 1.0, 2.0, True, False, "1", None])
def test_priority_rejects_invalid_values_in_each_position(invalid):
    with pytest.raises(ValueError):
        slaclock.priority_of(invalid, 1)
    with pytest.raises(ValueError):
        slaclock.priority_of(1, invalid)
    with pytest.raises(ValueError):
        slaclock.priority_of(invalid, 1, True)


@pytest.mark.parametrize("priority,expected", [
    ("P1", (15, 240)), ("P2", (60, 480)),
    ("P3", (240, 1440)), ("P4", (480, 4320)),
])
def test_exact_sla_targets(priority, expected):
    assert slaclock.targets(priority) == expected


@pytest.mark.parametrize("priority", ["", "p1", "p4", " P1", "P1 ", "P0", "P5", "P10"])
def test_unknown_priority_is_rejected(priority):
    with pytest.raises(ValueError):
        slaclock.targets(priority)
    with pytest.raises(ValueError):
        slaclock.escalation_tier(priority, False, 0)


@pytest.mark.parametrize("elapsed,target,expected", [
    (0, 1, "ok"), (1, 1, "warning"), (2, 1, "breached"),
    (2, 4, "ok"), (3, 4, "warning"), (4, 4, "warning"), (5, 4, "breached"),
    (11, 15, "ok"), (12, 15, "warning"), (14, 15, "warning"),
    (15, 15, "warning"), (16, 15, "breached"),
    (44, 60, "ok"), (45, 60, "warning"), (60, 60, "warning"), (61, 60, "breached"),
    (179, 240, "ok"), (180, 240, "warning"), (240, 240, "warning"), (241, 240, "breached"),
    (359, 480, "ok"), (360, 480, "warning"), (480, 480, "warning"), (481, 480, "breached"),
    (0, 10000, "ok"), (7499, 10000, "ok"), (7500, 10000, "warning"),
])
def test_sla_thresholds(elapsed, target, expected):
    assert slaclock.sla_state(elapsed, target) == expected


@pytest.mark.parametrize("elapsed,target", [(-1, 15), (-100, 1), (0, 0), (1, 0), (0, -1), (-1, -1)])
def test_invalid_sla_clock(elapsed, target):
    with pytest.raises(ValueError):
        slaclock.sla_state(elapsed, target)


@pytest.mark.parametrize("day,business_day", [(5, True), (6, True), (7, True), (8, True), (9, True), (10, False), (11, False)])
@pytest.mark.parametrize("hour,minute,inside", [(0, 0, False), (7, 59, False), (8, 0, True), (12, 0, True), (15, 59, True), (16, 0, False), (23, 59, False)])
def test_business_window(day, business_day, hour, minute, inside):
    moment = datetime(2026, 1, day, hour, minute, 59, 999999)
    assert slaclock.is_business_time(moment) is (business_day and inside)


@pytest.mark.parametrize("start,minutes,expected", [
    ("2026-01-05T08:00", 0, "2026-01-05T08:00"),
    ("2026-01-05T07:59:59", 0, "2026-01-05T08:00"),
    ("2026-01-05T07:59:59", 1, "2026-01-05T08:01"),
    ("2026-01-05T08:00:59.999999", 0, "2026-01-05T08:00"),
    ("2026-01-05T08:00", 479, "2026-01-05T15:59"),
    ("2026-01-05T08:00", 480, "2026-01-05T16:00"),
    ("2026-01-05T08:00", 481, "2026-01-06T08:01"),
    ("2026-01-05T15:59:59", 1, "2026-01-05T16:00"),
    ("2026-01-05T15:59", 2, "2026-01-06T08:01"),
    ("2026-01-05T16:00", 0, "2026-01-06T08:00"),
    ("2026-01-05T16:00", 1, "2026-01-06T08:01"),
    ("2026-01-09T15:59", 2, "2026-01-12T08:01"),
    ("2026-01-09T16:00", 0, "2026-01-12T08:00"),
    ("2026-01-10T10:00", 0, "2026-01-12T08:00"),
    ("2026-01-11T07:00", 480, "2026-01-12T16:00"),
    ("2026-01-05T08:00", 2400, "2026-01-09T16:00"),
    ("2026-01-05T08:00", 2401, "2026-01-12T08:01"),
    ("2026-12-31T15:59", 2, "2027-01-01T08:01"),
    ("2028-02-28T15:59", 2, "2028-02-29T08:01"),
])
def test_business_due_dates(start, minutes, expected):
    beginning = datetime.fromisoformat(start)
    due = slaclock.add_business_minutes(beginning, minutes)
    assert due == datetime.fromisoformat(expected)
    assert slaclock.business_minutes_between(beginning, due) == minutes


@pytest.mark.parametrize("start,end,expected", [
    ("2026-01-05T08:00", "2026-01-05T08:00", 0),
    ("2026-01-05T08:00:59", "2026-01-05T08:00:01", 0),
    ("2026-01-05T08:00:59", "2026-01-05T08:01:01", 1),
    ("2026-01-05T07:00", "2026-01-05T08:00", 0),
    ("2026-01-05T07:00", "2026-01-05T08:01", 1),
    ("2026-01-05T15:59", "2026-01-05T16:00", 1),
    ("2026-01-05T16:00", "2026-01-06T08:00", 0),
    ("2026-01-05T08:00", "2026-01-05T16:00", 480),
    ("2026-01-09T15:59", "2026-01-12T08:01", 2),
    ("2026-01-10T00:00", "2026-01-12T08:00", 0),
    ("2026-01-10T00:00", "2026-01-11T23:59", 0),
    ("2026-01-05T00:00", "2026-01-12T00:00", 2400),
    ("2028-02-28T15:59", "2028-02-29T08:01", 2),
])
def test_business_elapsed_minutes(start, end, expected):
    assert slaclock.business_minutes_between(datetime.fromisoformat(start), datetime.fromisoformat(end)) == expected


def test_calendar_limit_is_inclusive_on_day_366():
    # Monday plus 366 days is Wednesday, giving 52 full weeks and three weekdays.
    start = datetime(2026, 1, 5, 8)
    end = datetime(2027, 1, 6, 16)
    minutes = 263 * 480
    assert slaclock.add_business_minutes(start, minutes) == end
    assert slaclock.business_minutes_between(start, end) == minutes
    with pytest.raises(ValueError):
        slaclock.add_business_minutes(start, minutes + 1)
    with pytest.raises(ValueError):
        slaclock.business_minutes_between(start, datetime(2027, 1, 7, 8))


def test_invalid_business_intervals():
    start = datetime(2026, 1, 5, 12)
    with pytest.raises(ValueError):
        slaclock.add_business_minutes(start, -1)
    with pytest.raises(ValueError):
        slaclock.business_minutes_between(start, start - timedelta(minutes=1))
    with pytest.raises(ValueError):
        slaclock.business_minutes_between(start, start - timedelta(days=1))


def test_elapsed_minutes_against_minute_calendar():
    # Independent oracle counts the business-minute instants in a short interval.
    start = datetime(2026, 1, 8, 15, 57)
    for length in (0, 1, 3, 4, 60, 963, 1440, 3846, 5765):
        end = start + timedelta(minutes=length)
        cursor = start
        expected = 0
        while cursor < end:
            if cursor.weekday() in (0, 1, 2, 3, 4) and 8 <= cursor.hour < 16:
                expected += 1
            cursor += timedelta(minutes=1)
        assert slaclock.business_minutes_between(start, end) == expected


@pytest.mark.parametrize("priority,breached,without_reopens,with_reopens", [
    ("P1", False, 1, 2), ("P1", True, 3, 3),
    ("P2", False, 1, 2), ("P2", True, 2, 3),
    ("P3", False, 0, 1), ("P3", True, 1, 2),
    ("P4", False, 0, 1), ("P4", True, 1, 2),
])
def test_escalation_tiers_and_saturation(priority, breached, without_reopens, with_reopens):
    for reopens in (0, 1):
        assert slaclock.escalation_tier(priority, breached, reopens) == without_reopens
    for reopens in (2, 3, 100):
        assert slaclock.escalation_tier(priority, breached, reopens) == with_reopens
    with pytest.raises(ValueError):
        slaclock.escalation_tier(priority, breached, -1)


@pytest.mark.parametrize("text,expected", [
    ("1m", 1), ("59m", 59), ("60m", 60), ("90m", 90), ("1440m", 1440),
    ("1h", 60), ("4h", 240), ("1h0m", 60), ("1h30m", 90), ("1h59m", 119),
    ("0h60m", 60), ("0d60m", 60), ("0d0h60m", 60),
    ("1d", 1440), ("2d", 2880), ("1d4h", 1680), ("1d0h5m", 1445),
    ("1d59m", 1499), ("1d24h", 2880), ("0d1h", 60),
    ("01h05m", 65), ("  1h30m\t\n", 90), ("25h", 1500),
])
def test_valid_duration_grammar(text, expected):
    assert slaclock.parse_duration(text) == expected


@pytest.mark.parametrize("text", [
    "", " ", "0m", "0h", "0d", "0d0h0m", "1.5h", "30m1h", "-5m", "+1h",
    "1 h", "1h 5m", "1H", "1D", "1M", "h", "m", "1", "1h1h", "1m1m", "1d1d",
    "1h60m", "1d60m", "1d0h60m", "0d1h60m", "1h99m", "1h\n1m", "x1h", "1hx",
])
def test_invalid_duration_grammar(text):
    with pytest.raises(ValueError):
        slaclock.parse_duration(text)
