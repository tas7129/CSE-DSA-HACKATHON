# Exam Timetable Scheduling Using Graph Colouring

A Java 17 / JavaFX desktop demonstration of exam scheduling as **capacitated graph colouring**. Each course is a vertex, and an edge means two courses share a student. A colour is a time slot: adjacent courses cannot share a colour, and each slot can hold at most `R` courses (exam halls).

The application compares deterministic DSatur (a fast heuristic) with branch-and-bound search (exact when it completes). The exact solver starts with the DSatur timetable as an upper bound, selects vertices by saturation, breaks colour symmetry, and prunes using the current best and the capacity lower bound. A timeout returns a validated best-known timetable and marks optimality unproven.

## Requirements and launch

Install JDK 17 or later and Maven 3.9 or later. JavaFX dependencies are resolved by Maven; no separate JavaFX installation is required.

```sh
cd exam-timetable
mvn clean test
mvn javafx:run
```

On Windows use `mvnw.cmd` if a Maven wrapper is added, or run the same Maven commands in PowerShell. On macOS use Terminal. A JDK and Maven must be on `PATH`.

## Use

- **Manual option:** enter `N M R` on the first line, followed by `M` one-based conflict pairs, then select **Load manual edges**. For example, `5 4 2` followed by `1 2`, `1 3`, `2 4`, `3 5`.
- **Random option:** enter `N R` on the first line, set the edge density and optional seed, then select **Load random input (N R)**. The **Generate random graph** button also uses the separate course and capacity fields. A seed reproduces the graph.
- Run DSatur, exact search, or both. The exact time limit is configurable in seconds. The selector switches the graph coloring and timetable display.
- The selected timetable is displayed slot by slot. The results line reports each algorithm's slot count, measured runtime, validation status, and whether optimality is proven. DSatur is a heuristic, so its optimality is not guaranteed.
- Export the selected result with **Export selected CSV**. CSV rows are slots; columns are halls and unused positions are blank.
- The Performance tab runs benchmark comparisons for 5–30 courses on a shared graph per algorithm pair, with slot-count and runtime charts.

## Project map

- `src/main/java/edu/demo/exam/model`: conflict graph and immutable timetable result.
- `src/main/java/edu/demo/exam/algorithm`: DSatur and exact branch-and-bound solvers.
- `src/main/java/edu/demo/exam/util`: graph generation, shared validation, and CSV export.
- `src/main/java/edu/demo/exam/Main.java`: JavaFX interface, visualization, and charts.
- `src/test/java`: JUnit 5 solver and input edge-case tests.

Execution times measure solver work only; rendering, export, and chart drawing are excluded. DSatur is never claimed optimal. An exact result is marked proven only when the search completes.
