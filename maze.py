"""Maze data validation for the Maze Solver with Keys and Doors."""
from __future__ import annotations

from dataclasses import dataclass

# E is reserved as the exit marker; G is the unambiguous CSV/UI door symbol for key e.
DOOR_TO_KEY = {'A':'a','B':'b','C':'c','D':'d','F':'f','G':'e'}
KEY_TO_DOOR = {v:k for k,v in DOOR_TO_KEY.items()}
ALLOWED = frozenset('.#SEabcdefABCDFG')

@dataclass(frozen=True)
class Maze:
    """Immutable-in-practice grid wrapper; callers receive copies of its rows."""
    grid: tuple[tuple[str, ...], ...]

    @classmethod
    def from_rows(cls, rows):
        normalized = tuple(tuple(str(cell).strip() for cell in row) for row in rows)
        validate_grid(normalized)
        return cls(normalized)

    @property
    def size(self): return len(self.grid)

    def to_rows(self): return [list(row) for row in self.grid]

    @property
    def key_types(self): return tuple(sorted(c for c in {x for row in self.grid for x in row} if c in 'abcdef'))

    @property
    def start(self): return next((r,c) for r,row in enumerate(self.grid) for c,v in enumerate(row) if v == 'S')

    @property
    def exit(self): return next((r,c) for r,row in enumerate(self.grid) for c,v in enumerate(row) if v == 'E')


def validate_grid(grid, expected_types=None):
    n = len(grid)
    if n < 2 or any(len(row) != n for row in grid):
        raise ValueError('Maze must be a square grid with N >= 2.')
    bad = sorted({c for row in grid for c in row if c not in ALLOWED})
    if bad: raise ValueError('Unsupported cell symbol(s): ' + ', '.join(repr(x) for x in bad))
    cells = [c for row in grid for c in row]
    if cells.count('S') != 1: raise ValueError('Maze must contain exactly one S (start).')
    if cells.count('E') != 1: raise ValueError('Maze must contain exactly one E (exit).')
    keys = {c for c in cells if c in 'abcdef'}
    doors = {DOOR_TO_KEY[c] for c in cells if c in DOOR_TO_KEY}
    if keys != doors:
        raise ValueError('Every key must have its matching door and every door must have its key. The door for key e is written G because E is reserved for the exit.')
    if len(keys) > 6: raise ValueError('Maze supports at most six key-and-door types.')
    if expected_types is not None and len(keys) != expected_types:
        raise ValueError(f'Expected {expected_types} key-and-door types; found {len(keys)}.')
    return True
