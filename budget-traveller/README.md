# Budget Traveller with Coupons

A beginner-friendly flight planner that minimizes ticket cost while limiting intermediate stops and applying up to a chosen number of half-price coupons.

See [the detailed algorithm explanation](docs/algorithm-explanation.pdf) for the expanded-state Dijkstra design, correctness reasoning, worked example, and complexity analysis.

Submission files: [output PDF](Budget_traveller_output.pdf) · [algorithm explanation PDF](docs/budget-traveller-algorithm-explanation.pdf).

## Example

For `1 → 2` at 500 and `2 → 4` at 600, with `K=1` and one coupon, the cheapest trip costs `250 + 600 = 850` (or `500 + 300 = 800`, so the solver places the coupon on the more expensive flight). It considers both choices as separate search transitions.

## Install and run

Python 3.10 or newer is recommended. Tkinter is included with most Python installations; on Linux it may be provided by a separate OS package.

```bash
cd budget-traveller
python -m pip install -r requirements.txt
python main.py
```

The graphical app can generate a sample directed graph, import a CSV, solve and animate a journey, and export every original flight with selected-route and coupon markers. Set N, K, and C before loading. CSV headers are `source,destination,price`; duplicate rows are allowed and remain separate flights.

Standard input uses `N M`, `K C`, then M rows of `source destination price`:

```bash
printf '4 4\n2 1\n1 2 500\n1 3 800\n2 4 600\n3 4 300\n' | python main.py --stdin
```

The output is the minimum cost, or `-1` when no route fits. `K` counts intermediate cities, so at most `K+1` flights may be taken. City 1 is the start and city N is the destination.

## Tests and performance

```bash
python -m unittest discover -s tests -v
```

The suite includes edge cases and 120 seeded random comparisons against a separate layered dynamic-programming reference. It also prints a small local timing sample. The upper bound on expanded states is `N × (K+2) × (C+1)` when counting the initial layer; each state scans its outgoing flights and at most two transitions per flight. Heap-based Dijkstra is appropriate because all prices are nonnegative. A plain city-only shortest path loses the number of flights and coupons already used, so it may discard a route that is necessary for the optimal feasible answer.

The solver is independent of Tkinter and Matplotlib. `graph_model.py` validates and stores directed edges; `solver.py` searches and reconstructs the route; `csv_handler.py` handles file interchange; `graph_generator.py` builds examples; `main.py` contains the GUI and console entry point.
