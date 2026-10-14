"""Straightforward O(n^2) closest-pair reference algorithm."""
from __future__ import annotations
from dataclasses import dataclass
from math import hypot
from typing import Sequence

Point = tuple[float, float]


@dataclass(frozen=True)
class ClosestResult:
    distance: float
    pair: tuple[Point, Point]
    indices: tuple[int, int]


def closest_pair(points: Sequence[Point]) -> ClosestResult:
    """Check every pair. Ties use the lexicographically smallest input-index pair."""
    if len(points) < 2:
        raise ValueError("At least two points are required to find a pair.")
    best = float("inf")
    best_ids: tuple[int, int] | None = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = hypot(points[i][0] - points[j][0], points[i][1] - points[j][1])
            ids = (i, j)
            if d < best or (d == best and (best_ids is None or ids < best_ids)):
                best, best_ids = d, ids
    assert best_ids is not None
    i, j = best_ids
    return ClosestResult(best, (points[i], points[j]), best_ids)
