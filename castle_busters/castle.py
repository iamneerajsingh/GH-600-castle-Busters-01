"""Castle blocks and hit detection."""

from dataclasses import dataclass, field

# Points awarded for knocking down each kind of block
BLOCK_POINTS = {"wood": 10, "stone": 25, "tower": 50}


@dataclass
class Block:
    kind: str  # "wood", "stone" or "tower"
    x: float  # left edge in metres
    width: float = 4.0
    standing: bool = True

    def covers(self, x: float) -> bool:
        return self.x <= x <= self.x + self.width


@dataclass
class Castle:
    blocks: list[Block] = field(default_factory=list)

    def hit(self, landing_x: float) -> list[Block]:
        """Knock down every standing block at landing_x. Return the blocks hit."""
        knocked = [b for b in self.blocks if b.standing and b.covers(landing_x)]
        for block in knocked:
            block.standing = False
        return knocked

    @property
    def destroyed(self) -> bool:
        return all(not b.standing for b in self.blocks)


def level_one() -> Castle:
    """The first level: three blocks between 150 m and 170 m."""
    return Castle(
        [
            Block("wood", 150),
            Block("stone", 158),
            Block("tower", 166),
        ]
    )
