"""Random solvable maze generation."""
import random
from maze import Maze, KEY_TO_DOOR
from solver import shortest_path

def minimum_size(types):
    if not 1 <= types <= 6: raise ValueError('Key-and-door count T must be from 1 to 6.')
    return max(5, 2*types+2)

def _spaced_indices(start, end, count):
    """Choose count evenly distributed integer indexes in an inclusive range."""
    if end-start+1 < count:
        raise ValueError('Route is too short for the requested key-and-door count.')
    if count == 1:
        return [(start+end)//2]
    return [round(start+i*(end-start)/(count-1)) for i in range(count)]

def generate_maze(size=12, types=2, seed=None):
    minimum=minimum_size(types)
    if size < minimum: raise ValueError(f'Grid size N must be at least {minimum} for {types} key-and-door types.')
    rng=random.Random(seed); n=size
    # Carve a random self-avoiding corridor into a field of random open cells and walls.
    while True:
        route=[(rng.randrange(n), rng.randrange(n))]; used=set(route)
        while True:
            r,c=route[-1]
            opts=[(r+dr,c+dc) for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))
                  if 0<=r+dr<n and 0<=c+dc<n and (r+dr,c+dc) not in used]
            if not opts: break
            nxt=rng.choice(opts); route.append(nxt); used.add(nxt)
        if len(route) >= 2*types+2: break
    grid=[['.' if rng.random()<0.62 else '#' for _ in range(n)] for _ in range(n)]
    # The corridor ensures a valid route. Spread keys over its first half
    # and their doors over its second half to avoid a cluster near the start.
    route=route[:max(2*types+2, min(len(route), n*n//2))]
    for r,c in route: grid[r][c]='.'
    sr,sc=route[0]; er,ec=route[-1]; grid[sr][sc]='S'; grid[er][ec]='E'
    split=(len(route)-2)//2
    key_slots=_spaced_indices(1, split, types)
    door_slots=_spaced_indices(split+1, len(route)-2, types)
    for i,(key_index,door_index) in enumerate(zip(key_slots,door_slots)):
        grid[route[key_index][0]][route[key_index][1]]=chr(97+i)
        door=KEY_TO_DOOR[chr(97+i)]
        grid[route[door_index][0]][route[door_index][1]]=door
    maze=Maze.from_rows(grid)
    if shortest_path(maze) is None: return generate_maze(size,types,seed=rng.randrange(2**32))
    return maze

def generate_unsolvable_maze(size=12, types=2, seed=None):
    """Generate a valid maze whose isolated exit cannot be reached."""
    minimum=minimum_size(types)
    if size < minimum:
        raise ValueError(f'Grid size N must be at least {minimum} for {types} key-and-door types.')
    rng=random.Random(seed); n=size
    grid=[['#' for _ in range(n)] for _ in range(n)]
    grid[0][0]='S'
    grid[n-1][n-1]='E'
    # Spread keys and doors across the top corridor; a solid wall field still
    # isolates the exit in the opposite corner.
    split=(n-2)//2
    key_slots=_spaced_indices(1,split,types)
    door_slots=_spaced_indices(split+1,n-2,types)
    for i,(key_col,door_col) in enumerate(zip(key_slots,door_slots)):
        grid[0][key_col]=chr(97+i)
        grid[0][door_col]=KEY_TO_DOOR[chr(97+i)]
    maze=Maze.from_rows(grid)
    if shortest_path(maze) is not None:
        raise RuntimeError('Generated unsolvable maze unexpectedly has a route.')
    return maze
