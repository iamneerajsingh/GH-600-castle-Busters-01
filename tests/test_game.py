import math

import pytest

from castle_busters.game import Game, func_intersection, func_launch


def test_pull_sets_angle_and_caps_power():
    var_shot = func_launch(-100, 100)
    assert var_shot.angle_deg == pytest.approx(45)
    assert var_shot.power == 50
    assert func_launch(-30, 40).power == 25


@pytest.mark.parametrize(
    "var_x,var_y", [(0, 40), (-40, 0), (40, 40), (-1, 1), (-math.inf, 40), (-40, math.nan)]
)
def test_invalid_pull_does_not_consume_shot(var_x, var_y):
    var_game = Game()
    with pytest.raises(ValueError):
        var_game.func_fire(var_x, var_y)
    assert var_game.func_state()["shots"] == 0


def test_collision_catches_segment_crossing_but_not_high_shots():
    assert func_intersection((140, 5), (160, 5), 150, 154, 12) is not None
    assert func_intersection((140, 30), (160, 30), 150, 154, 12) is None


def test_hit_topples_defender_and_does_not_score_twice():
    var_game = Game()
    var_pull = math.sqrt(155 * 9.8) * math.sqrt(2)
    var_result = var_game.func_fire(-var_pull, var_pull)
    assert var_result["hit"] == "Sir Clanks"
    assert var_result["score"] == 10
    assert not var_result["targets"][0]["standing"]
    assert var_result["path"][-1][0] < 155
    var_repeat = var_game.func_fire(-var_pull, var_pull)
    assert var_repeat["hit"] is None
    assert var_repeat["score"] == 5


def test_round_limit_and_reset():
    var_game = Game()
    for var_index in range(8):
        var_game.func_fire(-20, 20)
    assert var_game.func_state()["over"]
    with pytest.raises(ValueError, match="finished"):
        var_game.func_fire(-20, 20)
    var_state = var_game.func_reset()
    assert var_state["remaining"] == 8
    assert not var_state["over"]
    assert all(var_target["standing"] for var_target in var_state["targets"])
