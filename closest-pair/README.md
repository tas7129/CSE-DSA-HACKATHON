# Closest Pair of Points: Brute Force vs Divide and Conquer

This project compares two ways to find the nearest pair among two-dimensional points. The browser demo is the submission-ready visual application; the Python implementation is included for source-code study and automated tests. Both algorithms receive the same generated points and return the distance, coordinates, and original input indices. Duplicate coordinates are allowed.

## Open the visual demo

Open [`index.html`](index.html) in any modern browser. It runs entirely in the browser: choose the point count, random seed, and coordinate range, then generate points to see the required three-line result, both closest pairs, the divide-and-conquer strip, and measured runtimes. Use **Run benchmark** to draw a timing comparison across increasing input sizes up to the selected N. The input rejects N < 2. No terminal, Python installation, or server is needed for the visual demo.

To publish it on GitHub, push this folder to a repository and enable **Settings → Pages** for the branch and folder that contain `index.html`. GitHub Pages will serve the interactive demo as a website.

The Python command-line implementation below remains available for source-code study and automated tests.

## Algorithms in simple terms

Brute force measures every pair. It is easy to verify, but the number of comparisons grows quadratically: **O(N²)**.

Divide and conquer sorts points by x, solves the left and right halves, then checks only points near the dividing line. Those strip points are already ordered by y, so the recursive merges keep the total work at **O(N log N)**. Equal-distance ties are settled by the lexicographically smallest pair of original input indices in both algorithms.

## Setup and run

Python 3.10 or newer is recommended. Matplotlib is only needed for plots.

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
```

Enter N when prompted, or provide options directly:

```sh
python3 main.py --count 100 --seed 7 --min -50 --max 50
python3 main.py --count 200 --seed 7 --no-plot
python3 main.py --count 100 --seed 7 --benchmark --max-n 2000
```

Each coordinate is generated uniformly over the configured range. A seed reproduces the data. Measurements use `perf_counter`, median timings across `--repeats` runs, and exclude data generation and plotting. Tiny inputs are dominated by timer and interpreter overhead, so the faster algorithm is not guaranteed to win there.

## What is displayed

The console reports both distances and pairs, median execution times, and a tolerance-based verification. By default, the figures show all points and the two returned closest pairs, plus a separate top-level divide visualization showing the actual x split, width-2d strip, and candidate pairs. `--benchmark` measures increasing input sizes on one shared dataset per size and plots both runtime curves. No timing values are hardcoded.

## Tests

From this folder, run:

```sh
python3 -m unittest discover -s tests -v
```

The tests include invalid sizes, N=2, duplicate points, collinear and aligned points, tied minima, negative and floating coordinates, very close points, uneven distributions, and random datasets checked against brute force.

## Files

- `main.py`: input, console output, verification, and orchestration.
- `point_generation.py`: configurable reproducible point generation.
- `brute_force.py`: reference O(N²) implementation.
- `divide_conquer.py`: O(N log N) recursive algorithm and top-level trace data.
- `visualization.py`: result and strip figures.
- `benchmark.py`: timing trials and performance graph.
- `tests/`: automated edge-case and random tests.

The algorithms themselves do not depend on Matplotlib. Plots are opened together in an interactive Matplotlib window; close the figures to exit.
