"""CSV import and lossless two-file solution export."""
import csv
from pathlib import Path
from maze import Maze

def read_maze(path):
    with open(path, newline='', encoding='utf-8-sig') as f: rows=[row for row in csv.reader(f) if row]
    if not rows: raise ValueError('CSV file is empty.')
    # Accept either comma separated cells or compact rows such as S.#E.
    if any(len(row)==1 and len(row[0])>1 for row in rows): rows=[list(row[0].strip()) for row in rows]
    else: rows=[[cell.strip() for cell in row] for row in rows]
    return Maze.from_rows(rows)

def export_solution(maze, path, filename):
    """Write original grid and separate 0/1 path overlay side-by-side as two CSVs."""
    target=Path(filename); overlay=target.with_name(target.stem+'_path'+target.suffix)
    with target.open('w',newline='',encoding='utf-8') as f: csv.writer(f).writerows(maze.grid)
    with overlay.open('w',newline='',encoding='utf-8') as f:
        csv.writer(f).writerows([['1' if (r,c) in set(path) else '0' for c in range(maze.size)] for r in range(maze.size)])
    return target,overlay
