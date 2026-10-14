# CSE DSA Hackathon Projects

This repository contains four complete DSA project submissions. Each project folder includes its source code, a project README, and a submission output PDF. Algorithm explanations are linked from the relevant project README.

## Projects

- [Budget Traveller with Coupons](budget-traveller/README.md) — Python and Tkinter flight planner using expanded-state Dijkstra; includes the [output PDF](budget-traveller/Budget_traveller_output.pdf) and [algorithm explanation](budget-traveller/docs/budget-traveller-algorithm-explanation.pdf).
- [Closest Pair of Points](closest-pair/README.md) — interactive browser demo and Python implementations comparing brute force with divide and conquer; includes the [output PDF](closest-pair/Closest_Pair_output.pdf) and [analysis PDF](closest-pair/output/pdf/closest-pair-analysis.pdf).
- [Exam Timetable Scheduling](exam-timetable/README.md) — Java 17 and JavaFX graph-colouring application comparing DSatur and exact branch-and-bound; includes the [output PDF](exam-timetable/Exam_timetable_output.pdf) and [best-case analysis PDF](exam-timetable/docs/best-case-analysis.pdf).
- [Maze Solver with Keys and Doors](maze-keys-and-doors/README.md) — Python and Tkinter application with BFS pathfinding, maze generation, CSV import/export, animation, and tests; includes the [output PDF](maze-keys-and-doors/Maze_keys_door_output.pdf) and [design explanation](maze-keys-and-doors/output/pdf/maze-solver-design-explanation.pdf).

## Run the projects

Each project README contains setup and run instructions. For example, to run the maze application:

```sh
cd maze-keys-and-doors
python3 main.py
```

To run its tests:

```sh
cd maze-keys-and-doors
python3 -m unittest discover -s tests -v
```

