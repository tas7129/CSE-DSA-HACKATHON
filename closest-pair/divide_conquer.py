"""O(n log n) closest pair using x division and y-ordered merge."""
from __future__ import annotations
from math import hypot
from typing import Sequence
from brute_force import ClosestResult

Point = tuple[float, float]
_Entry = tuple[float, float, int]


def closest_pair(points: Sequence[Point], *, trace: bool = False):
    """Return ClosestResult; with trace=True, also return the root strip's teaching trace.

    Every point carries its input index, so equal coordinates remain distinct. Recursive
    calls return y-sorted lists, avoiding repeated strip sorting and preserving O(n log n).
    """
    if len(points) < 2:
        raise ValueError("At least two points are required to find a pair.")
    entries = sorted((p[0], p[1], i) for i, p in enumerate(points))
    # A zero distance is globally optimal. Resolve it up front so a large group of
    # identical points cannot make a zero-width strip do quadratic work.
    duplicate_groups: dict[tuple[float, float], list[int]] = {}
    for x, y, i in entries:
        duplicate_groups.setdefault((x, y), []).append(i)
    zero_pairs = [tuple(sorted(ids[:2])) for ids in duplicate_groups.values() if len(ids) > 1]
    zero_pair = min(zero_pairs) if zero_pairs else None

    def solve(xs: list[_Entry]):
        n = len(xs)
        if n <= 3:
            best = float("inf"); ids = None
            for a in range(n):
                for b in range(a + 1, n):
                    p, q = xs[a], xs[b]
                    pair_ids = tuple(sorted((p[2], q[2])))
                    d = hypot(p[0]-q[0], p[1]-q[1])
                    if d < best or (d == best and (ids is None or pair_ids < ids)):
                        best, ids = d, pair_ids
            return best, ids, sorted(xs, key=lambda p: (p[1], p[0], p[2]))
        mid = n // 2
        split_x = (xs[mid-1][0] + xs[mid][0]) / 2
        dl, il, yl = solve(xs[:mid]); dr, ir, yr = solve(xs[mid:])
        best, ids = (dl, il) if (dl < dr or (dl == dr and il < ir)) else (dr, ir)
        merged=[]; a=b=0
        while a < len(yl) and b < len(yr):
            if (yl[a][1], yl[a][0], yl[a][2]) <= (yr[b][1], yr[b][0], yr[b][2]):
                merged.append(yl[a]); a+=1
            else: merged.append(yr[b]); b+=1
        merged.extend(yl[a:]); merged.extend(yr[b:])
        strip = [p for p in merged if abs(p[0]-split_x) <= best]
        # The y-gap bound keeps comparisons constant per point in the planar packing argument.
        for a, p in enumerate(strip):
            b = a + 1
            while b < len(strip) and strip[b][1] - p[1] <= best:
                q = strip[b]
                pair_ids = tuple(sorted((p[2], q[2])))
                d = hypot(p[0]-q[0], p[1]-q[1])
                if d < best or (d == best and pair_ids < ids):
                    best, ids = d, pair_ids
                b += 1
        return best, ids, merged

    if zero_pair is None:
        distance, ids, _ = solve(entries)
    else:
        distance, ids = 0.0, zero_pair
    i, j = ids
    result = ClosestResult(distance, (points[i], points[j]), ids)
    if not trace:
        return result
    # A genuine top-level divide/strip, used to explain the operation in a dedicated plot.
    mid = len(entries)//2
    # For N=2 the left recursive half has one point, but the trace should still
    # show the real root split. Larger inputs also use this same top-level split.
    split_x = (entries[mid-1][0] + entries[mid][0])/2
    left = entries[:mid]; right = entries[mid:]
    from brute_force import closest_pair as brute
    left_distance = brute([points[e[2]] for e in left]).distance if len(left) >= 2 else float("inf")
    right_distance = brute([points[e[2]] for e in right]).distance if len(right) >= 2 else float("inf")
    base = min(left_distance, right_distance)
    # A root containing only two points has no within-half pair; its strip needs
    # to include both points so the visualization can show the sole comparison.
    if base == float("inf"):
        base = distance
    strip = [e for e in sorted(entries, key=lambda p:(p[1],p[0],p[2])) if abs(e[0]-split_x) <= base]
    candidates=[]; best=base
    for a,p in enumerate(strip):
        b=a+1
        while b<len(strip) and strip[b][1]-p[1] <= best:
            q=strip[b]; candidates.append((p[2],q[2]))
            best=min(best,hypot(p[0]-q[0],p[1]-q[1])); b+=1
    return result, {"split_x": split_x, "half_distance": base, "strip": [e[2] for e in strip], "candidates": candidates}
