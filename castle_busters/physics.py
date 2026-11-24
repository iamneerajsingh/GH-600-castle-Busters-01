"""Projectile physics for Castle Busters (no graphics, easy to test)."""

import math
from dataclasses import dataclass

GRAVITY = 9.8  # metres per second squared
MAX_POWER = 100  # the slider in the game goes from 1 to 100


@dataclass
class Shot:
    """One launch from the catapult."""

    angle_deg: float  # 0 = flat, 90 = straight up
    power: float  # 1..MAX_POWER, used as launch speed in m/s


def validate_shot(shot: Shot) -> None:
    """Raise ValueError when the shot is outside the allowed range."""
    if not 0 < shot.angle_deg < 90:
        raise ValueError("angle_deg must be between 0 and 90 (exclusive)")
    if not 0 < shot.power <= MAX_POWER:
        raise ValueError(f"power must be between 1 and {MAX_POWER}")


def position_at(shot: Shot, t: float) -> tuple[float, float]:
    """Return the (x, y) position of the boulder t seconds after launch."""
    validate_shot(shot)
    rad = math.radians(shot.angle_deg)
    x = shot.power * math.cos(rad) * t
    y = shot.power * math.sin(rad) * t - 0.5 * GRAVITY * t * t
    return x, y


def flight_time(shot: Shot) -> float:
    """Seconds until the boulder lands back on the ground (y = 0)."""
    validate_shot(shot)
    return 2 * shot.power * math.sin(math.radians(shot.angle_deg)) / GRAVITY


def landing_distance(shot: Shot) -> float:
    """Horizontal distance (metres) where the boulder lands."""
    x, _ = position_at(shot, flight_time(shot))
    return round(x, 2)


def max_range(power: float) -> float:
    """Maximum range in metres, rounded to two decimals, at 45 degrees.

    Raise ValueError unless 0 < power <= MAX_POWER.
    """
    return landing_distance(Shot(45, power))


def trajectory(shot: Shot, steps: int = 50) -> list[tuple[float, float]]:
    """Return a list of points along the flight path, ending on the ground."""
    total = flight_time(shot)
    return [position_at(shot, total * i / steps) for i in range(steps + 1)]
