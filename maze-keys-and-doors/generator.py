"""Random solvable maze generation."""
import random
from maze import Maze, KEY_TO_DOOR
from solver import shortest_path

def minimum_size(types):
    if not 1 <= types <= 6: raise ValueError('Key-and-door count T must be from 1 to 6.')
    return max(5, 2*types+2)

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
    # The corridor ensures a valid route, with each key placed before its door.
    route=route[:max(2*types+2, min(len(route), n*n//2))]
    for r,c in route: grid[r][c]='.'
    sr,sc=route[0]; er,ec=route[-1]; grid[sr][sc]='S'; grid[er][ec]='E'
    for i in range(types):
        grid[route[1+2*i][0]][route[1+2*i][1]]=chr(97+i)
        door=KEY_TO_DOOR[chr(97+i)]
        grid[route[2+2*i][0]][route[2+2*i][1]]=door
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
    # The top row contains matched pairs but a solid wall barrier isolates the exit.
    cells=list(range(1, 2*types+1)); rng.shuffle(cells)
    for i in range(types):
        key_col=1+2*i; door_col=2+2*i
        grid[0][key_col]=chr(97+i)
        grid[0][door_col]=KEY_TO_DOOR[chr(97+i)]
    maze=Maze.from_rows(grid)
    if shortest_path(maze) is not None:
        raise RuntimeError('Generated unsolvable maze unexpectedly has a route.')
    return maze
