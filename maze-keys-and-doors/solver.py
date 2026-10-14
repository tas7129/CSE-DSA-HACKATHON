"""Breadth-first shortest path search independent of Tkinter."""
from collections import deque
from maze import Maze, validate_grid, DOOR_TO_KEY

DIRECTIONS = ((-1,0),(1,0),(0,-1),(0,1))

def shortest_path(grid):
    """Return coordinate list from S through E, or None if unreachable."""
    if isinstance(grid, Maze): grid = grid.grid
    validate_grid(grid)
    n = len(grid)
    start = next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 'S')
    initial = (*start, 0)
    queue = deque([initial]); parent = {initial: None}; goal = None
    while queue:
        r,c,mask = queue.popleft()
        if grid[r][c] == 'E': goal = (r,c,mask); break
        for dr,dc in DIRECTIONS:
            nr,nc=r+dr,c+dc
            if not (0 <= nr < n and 0 <= nc < n): continue
            tile=grid[nr][nc]
            if tile == '#': continue
            if tile in DOOR_TO_KEY and not (mask & (1 << (ord(DOOR_TO_KEY[tile])-97))): continue
            next_mask = mask | (1 << (ord(tile)-97)) if tile in 'abcdef' else mask
            state=(nr,nc,next_mask)
            if state not in parent:
                parent[state]=(r,c,mask); queue.append(state)
    if goal is None: return None
    path=[]; state=goal
    while state is not None:
        path.append(state[:2]); state=parent[state]
    return path[::-1]

def shortest_distance(grid):
    path=shortest_path(grid)
    return -1 if path is None else len(path)-1
