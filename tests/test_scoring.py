import pytest

from castle_busters.castle import level_one
from castle_busters.scoring import final_score, score_hit


def test_hitting_the_stone_block_scores_25():
    castle = level_one()
    assert score_hit(castle.hit(160)) == 25


def test_block_cannot_be_hit_twice():
    castle = level_one()
    castle.hit(160)
    assert castle.hit(160) == []


def test_castle_destroyed_after_all_blocks_hit():
    castle = level_one()
    for x in (151, 159, 167):
        castle.hit(x)
    assert castle.destroyed


def test_extra_shots_cost_points_but_never_below_zero():
    assert final_score(85, 1) == 85
    assert final_score(85, 3) == 75
    assert final_score(5, 5) == 0


def test_zero_shots_is_invalid():
    with pytest.raises(ValueError):
        final_score(10, 0)
