#!/usr/bin/env python3
"""Shortest path in a keys-and-doors maze; CSV input/output and guaranteed generator."""
from __future__ import annotations

import argparse
import csv
import random
from collections import deque
from pathlib import Path


def read_csv(path: str | Path) -> list[list[str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = [[cell.strip() for cell in row] for row in csv.reader(f) if row]
    if rows and len(rows[0]) == 1 and rows[0][0].isdigit():
        n = int(rows.pop(0)[0])
        rows = [list(row[0].replace(" ", "")) for row in rows]
    if not rows or any(len(row) != len(rows) for row in rows):
        raise ValueError("CSV must contain a non-empty square grid (cells separated by commas or characters).")
    return rows


def validate(grid: list[list[str]], t: int | None = None) -> None:
    n = len(grid)
    if n == 0 or any(len(row) != n for row in grid):
        raise ValueError("Grid must be square.")
    allowed = set(".#SEabcdefABCDEF")
    if any(c not in allowed for row in grid for c in row):
        raise ValueError("Cells must be '.', '#', 'S', 'E', or a-f/A-F.")
    flat = sum(grid, [])
    if flat.count("S") != 1 or flat.count("E") != 1:
        raise ValueError("Grid must contain exactly one S and one E.")
    keys = {c for c in flat if c in "abcdef"}
    doors = {c.lower() for c in flat if c in "ABCDEF"}
    if keys != doors:
        raise ValueError("Each door must have exactly one matching key type present, and vice versa.")
    if t is not None and len(keys) != t:
        raise ValueError(f"Expected {t} distinct key/door types; found {len(keys)}.")


def shortest_path(grid: list[list[str]]) -> list[tuple[int, int]] | None:
    """BFS on (row, col, key-mask); return path including S and E, or None."""
    validate(grid)
    n = len(grid)
    start = next((r, c) for r in range(n) for c in range(n) if grid[r][c] == "S")
    q = deque([(start[0], start[1], 0)])
    parent: dict[tuple[int, int, int], tuple[int, int, int] | None] = {(start[0], start[1], 0): None}
    goal = None
    while q:
        r, c, mask = q.popleft()
        if grid[r][c] == "E":
            goal = (r, c, mask)
            break
        for nr, nc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            tile = grid[nr][nc]
            if tile == "#":
                continue
            if tile in "ABCDEF" and not mask & (1 << (ord(tile.lower()) - ord("a"))):
                continue
            nm = mask | (1 << (ord(tile) - ord("a"))) if tile in "abcdef" else mask
            state = (nr, nc, nm)
            if state not in parent:
                parent[state] = (r, c, mask)
                q.append(state)
    if goal is None:
        return None
    path = []
    state = goal
    while state is not None:
        path.append(state[:2])
        state = parent[state]
    return path[::-1]


def generate(n: int, t: int, seed: int | None = None) -> list[list[str]]:
    """Make a random connected open corridor with each key before its door."""
    if not 2 <= n or not 1 <= t <= 6:
        raise ValueError("N must be at least 2 and T must be 1..6.")
    rng = random.Random(seed)
    # Construct a self-avoiding walk; random walls elsewhere preserve a known solution.
    for _ in range(2000):
        cells = [(rng.randrange(n), rng.randrange(n))]
        used = set(cells)
        while len(cells) < n*n:
            r,c = cells[-1]
            options = [(r+dr,c+dc) for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))
                       if 0 <= r+dr < n and 0 <= c+dc < n and (r+dr,c+dc) not in used]
            if not options:
                break
            nxt = rng.choice(options); cells.append(nxt); used.add(nxt)
        if len(cells) >= 2*t+2:
            break
    else:
        raise ValueError("Could not generate a corridor; increase N.")
    g = [[("." if rng.random() < 0.68 else "#") for _ in range(n)] for _ in range(n)]
    # Keep the guaranteed route open. Put keys and doors in route order.
    route = cells[:max(2*t+2, min(len(cells), n*n//2))]
    for r,c in route: g[r][c] = "."
    g[route[0][0]][route[0][1]] = "S"
    g[route[-1][0]][route[-1][1]] = "E"
    # Place a-f pairs interleaved on the route; a key precedes its door.
    for i in range(t):
        g[route[1+2*i][0]][route[1+2*i][1]] = chr(ord("a")+i)
        g[route[2+2*i][0]][route[2+2*i][1]] = chr(ord("A")+i)
    return g


def write_csv(grid: list[list[str]], path: str | Path, marked: list[tuple[int,int]] | None = None) -> None:
    marked_set = set(marked or [])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for r,row in enumerate(grid):
            w.writerow([("x" if tile == "." else f"x({tile})") if (r,c) in marked_set else tile
                        for c,tile in enumerate(row)])


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--csv", help="input CSV grid")
    src.add_argument("--generate", action="store_true", help="generate a solvable random grid")
    p.add_argument("-t", "--types", type=int, help="number of key/door types (required with --generate)")
    p.add_argument("-n", "--size", type=int, default=12, help="generated grid side length")
    p.add_argument("--seed", type=int)
    p.add_argument("--grid-out", default="maze.csv")
    p.add_argument("--path-out", default="maze_path.csv")
    args = p.parse_args()
    grid = generate(args.size, args.types, args.seed) if args.generate and args.types is not None else read_csv(args.csv) if args.csv else None
    if grid is None:
        p.error("--types is required with --generate")
    validate(grid, args.types if args.generate else args.types)
    path = shortest_path(grid)
    print(-1 if path is None else len(path)-1)
    if args.generate:
        write_csv(grid, args.grid_out)
    if path is not None:
        write_csv(grid, args.path_out, path)


if __name__ == "__main__":
    main()
