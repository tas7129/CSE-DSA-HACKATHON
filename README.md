# Maze Solver with Keys and Doors

A beginner-friendly Python 3 desktop application that finds and animates the shortest route through a square maze. It uses Tkinter and Python's standard library; there are no third-party dependencies.

## Project structure

- `main.py` launches the Tkinter application.
- `maze.py` stores and validates the grid independently of the display.
- `solver.py` implements BFS and returns the shortest coordinate path.
- `generator.py` makes random mazes with a carved, guaranteed-solvable route.
- `csv_handler.py` imports mazes and exports the original maze plus a path overlay.
- `visualizer.py` draws the grid and controls movement, key pickups, doors, and animation.
- `tests/test_maze.py` contains solver, validation, generation, and export tests.

## Run

Install Python 3.10 or later. Tkinter is included with the standard Python distribution on Windows and macOS (some Linux distributions package it separately).

```sh
python main.py
```

Run the unit tests:

```sh
python -m unittest discover -s tests -v
```

## Use the application

Set `N` (grid side length) and `T` (number of key/door types, 1–6), then choose **Generate random maze**. Select **Generate an unsolvable maze** first to create a valid maze with the exit isolated behind walls. Generated layouts place keys before their matching doors along a guaranteed clear route; other open cells and walls are randomized. Use **Load maze from CSV** to choose your own maze, then **Solve maze** to show the shortest route or **Animate solution** to watch it. Pause and resume the animation, adjust its speed, or reset the view. The original maze data is never changed by animation.

CSV grids must contain N rows and N cells in every row. Use comma-separated cells (`S,.,#,a,A,E`) or compact character rows (`S.#aAE`). Allowed cells are `.` open, `#` wall, `S` start, `E` exit, lowercase keys `a`–`f`, and matching doors `A`–`D`, `F`, and `G` (`G` represents key `e`'s door because `E` is reserved for the exit). Exactly one start and exit are required; each key type present must have its matching door, and vice versa. Doors cannot be crossed until their key has been collected. Keys stay collected.

**Export convention:** choosing `solved.csv` writes two files next to each other: `solved.csv` retains the exact original grid, while `solved_path.csv` is an N×N overlay containing `1` for each cell on the path (including S and E) and `0` elsewhere. Keeping two files preserves key and door symbols without ambiguity.

## How the algorithm works

BFS explores one move at a time. A search state is `(row, column, key mask)`: up to six bits record which keys have been collected. A move into a wall is rejected, and a door move is rejected unless the matching bit is set. Entering a key turns on its bit. The first exit state reached by BFS has the minimum number of moves. The parent map reconstructs the route. If no exit state is reachable, the distance is `-1`.

For a grid with side length N and T key types, at most `N² × 2ᵀ` states can be visited. Each state checks at most four neighbors, so time and space are `O(N² × 2ᵀ)`. The returned route includes both endpoints; its move count is the number of coordinates minus one.

## CSV and command-line helper

The desktop app is the primary interface. The original `maze_keys.py` command-line prototype remains available for simple batch use:

```sh
python maze_keys.py --csv input.csv --path-out path.csv
python maze_keys.py --generate --size 12 --types 3 --seed 42
```

The GUI export is the recommended lossless format, with a separate overlay file.

## Submission and sample files

The Tkinter project is the primary application; run it with `python3 main.py`. The Java file, command-line Python script, and browser visualizer in the repository root are additional implementations/prototypes. The Python desktop application is the one covered by `tests/`.

Sample input files are available in `samples/`:

- `solvable.csv` contains a solvable maze with three key-and-door types.
- `unsolvable.csv` contains a valid maze whose exit is isolated.

Load either file using **Load maze from CSV** to demonstrate both solver outcomes.
