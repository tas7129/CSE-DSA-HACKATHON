"""Point creation helpers, kept separate from the algorithms."""
from __future__ import annotations

import random
from typing import Sequence

Point = tuple[float, float]


def generate_points(n: int, *, x_range: tuple[float, float] = (0, 100),
                    y_range: tuple[float, float] = (0, 100), seed: int | None = None) -> list[Point]:
    """Create a reproducible (when seeded) list of points; duplicates are allowed."""
    if n < 0:
        raise ValueError("N cannot be negative")
    if x_range[0] > x_range[1] or y_range[0] > y_range[1]:
        raise ValueError("Coordinate range minimum must not exceed its maximum")
    rng = random.Random(seed)
    return [(rng.uniform(*x_range), rng.uniform(*y_range)) for _ in range(n)]
