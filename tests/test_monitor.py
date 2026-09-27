import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from monitor import check_health


def test_health_is_healthy():
    warnings = check_health(
        20,
        30,
        40,
        80,
        90
    )

    assert warnings == []


def test_health_warning():
    warnings = check_health(
        85,
        30,
        40,
        80,
        90
    )

    assert warnings == ["WARNING: CPU usage is 85%"]


def test_health_critical():
    warnings = check_health(
        95,
        30,
        40,
        80,
        90
    )

    assert warnings == ["CRITICAL: CPU usage is 95%"]


def test_custom_thresholds():
    warnings = check_health(
        75,
        30,
        40,
        70,
        85
    )

    assert warnings == ["WARNING: CPU usage is 75%"]


def test_multiple_health_warnings():
    warnings = check_health(
        85,
        92,
        95,
        80,
        90
    )

    assert warnings == [
        "WARNING: CPU usage is 85%",
        "CRITICAL: Memory usage is 92%",
        "CRITICAL: Disk usage is 95%"
    ]


def test_threshold_boundaries():
    warning = check_health(
        80,
        30,
        40,
        80,
        90
    )

    critical = check_health(
        90,
        30,
        40,
        80,
        90
    )

    assert warning == ["WARNING: CPU usage is 80%"]
    assert critical == ["CRITICAL: CPU usage is 90%"]