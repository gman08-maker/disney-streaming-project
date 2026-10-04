import pytest

from window import SlidingWindowCounter


def test_counts_events_inside_window():
    w = SlidingWindowCounter(window_seconds=60)
    w.add("Bluey", timestamp=0)
    w.add("Bluey", timestamp=10)
    w.add("Andor", timestamp=20)
    assert w.count("Bluey", now=30) == 2
    assert w.count("Andor", now=30) == 1


def test_old_events_expire():
    w = SlidingWindowCounter(window_seconds=60)
    w.add("Bluey", timestamp=0)
    w.add("Bluey", timestamp=50)
    assert w.count("Bluey", now=59) == 2
    assert w.count("Bluey", now=70) == 1


def test_boundary_is_exclusive_on_the_old_end():
    w = SlidingWindowCounter(window_seconds=60)
    w.add("Bluey", timestamp=0)
    assert w.count("Bluey", now=59.9) == 1
    assert w.count("Bluey", now=60) == 0


def test_unknown_key_returns_zero():
    w = SlidingWindowCounter(window_seconds=60)
    assert w.count("Nothing", now=0) == 0


def test_top_orders_by_count():
    w = SlidingWindowCounter(window_seconds=60)
    for t in range(5):
        w.add("Moana 2", timestamp=t)
    for t in range(3):
        w.add("Bluey", timestamp=t)
    w.add("Andor", timestamp=1)
    assert w.top(2, now=10) == [("Moana 2", 5), ("Bluey", 3)]


def test_everything_expires():
    w = SlidingWindowCounter(window_seconds=10)
    w.add("Bluey", timestamp=0)
    assert w.top(5, now=100) == []


def test_invalid_window_raises():
    with pytest.raises(ValueError):
        SlidingWindowCounter(window_seconds=0)
