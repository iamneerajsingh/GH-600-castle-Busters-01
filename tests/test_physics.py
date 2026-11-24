import pytest

from castle_busters.physics import Shot, flight_time, landing_distance, max_range, trajectory


def test_45_degrees_goes_furthest():
    assert landing_distance(Shot(45, 40)) > landing_distance(Shot(30, 40))
    assert landing_distance(Shot(45, 40)) > landing_distance(Shot(60, 40))


def test_known_landing_distance():
    # range = v^2 * sin(2*angle) / g = 40*40*1/9.8
    assert landing_distance(Shot(45, 40)) == pytest.approx(163.27, abs=0.01)


@pytest.mark.parametrize("var_power,var_expected", [(1, 0.10), (40, 163.27), (100, 1020.41)])
def test_max_range(var_power, var_expected):
    assert max_range(var_power) == pytest.approx(var_expected, abs=0.001)
    assert max_range(var_power) >= landing_distance(Shot(30, var_power))
    assert max_range(var_power) >= landing_distance(Shot(60, var_power))


@pytest.mark.parametrize("var_power", [-1, 0, 101, float("nan"), float("inf")])
def test_max_range_rejects_invalid_power(var_power):
    with pytest.raises(ValueError):
        max_range(var_power)


def test_trajectory_starts_and_ends_on_ground():
    path = trajectory(Shot(45, 40))
    assert path[0] == (0.0, 0.0)
    assert path[-1][1] == pytest.approx(0.0, abs=1e-9)


def test_flight_time_is_positive():
    assert flight_time(Shot(30, 20)) > 0


@pytest.mark.parametrize("angle,power", [(0, 40), (90, 40), (45, 0), (45, 101)])
def test_invalid_shots_are_rejected(angle, power):
    with pytest.raises(ValueError):
        landing_distance(Shot(angle, power))
