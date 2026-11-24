"""Scoring rules for Castle Busters."""

from .castle import BLOCK_POINTS, Block

SHOT_PENALTY = 5  # every boulder after the first costs points


def score_hit(blocks: list[Block]) -> int:
    """Points for the blocks knocked down by one shot."""
    return sum(BLOCK_POINTS[b.kind] for b in blocks)


def final_score(points: int, shots_used: int) -> int:
    """Total score after the level. Never below zero."""
    if shots_used < 1:
        raise ValueError("shots_used must be at least 1")
    return max(0, points - SHOT_PENALTY * (shots_used - 1))
