"""Tkinter demonstration app and standard-input command line entry point."""
import argparse
import csv
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from graph_model import Flight, FlightGraph
from solver import solve
from csv_handler import load_graph, export_results
from graph_generator import generate_graph


def solve_stdin():
    """Parse the documented N M / K C / flight rows format from stdin."""
    import sys
    tokens = list(map(int, sys.stdin.read().split()))
    if len(tokens) < 4:
        raise ValueError("Expected N M on line 1 and K C on line 2.")
    n, m, k, c = tokens[:4]
    if m < 0:
        raise ValueError("Flight count M must be nonnegative.")
    if len(tokens) != 4 + 3 * m:
        raise ValueError(f"Expected {m} flight rows (three integers each).")
    graph = FlightGraph(n, [Flight(*tokens[i:i + 3]) for i in range(4, len(tokens), 3)])
    result = solve(graph, k, c)
    print(result.cost if result else -1)


class TravellerApp:
    def __init__(self, root):
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        self.plt = plt
        self.FigureCanvasTkAgg = FigureCanvasTkAgg
        self.root = root
        root.title("Budget Traveller with Coupons")
        root.geometry("1100x720")
        self.graph = None
        self.solution = None
        self.after_id = None
        self.paused = False
        self.step_index = 0
        self.traveler = None
        self.vars = {key: tk.StringVar(value=value) for key, value in
                     (("n", "6"), ("k", "2"), ("c", "1"), ("status", "Load or generate a flight network."))}
        self._build()

    def _build(self):
        toolbar = ttk.Frame(self.root, padding=(10, 10, 10, 4))
        toolbar.pack(side=tk.TOP, fill=tk.X)
        inputs = ttk.Frame(toolbar)
        inputs.pack(side=tk.TOP, fill=tk.X, pady=(0, 7))
        for label, key in (("Cities N", "n"), ("Max stops K", "k"), ("Coupons C", "c")):
            ttk.Label(inputs, text=label).pack(side=tk.LEFT, padx=(0, 4))
            ttk.Entry(inputs, textvariable=self.vars[key], width=6).pack(side=tk.LEFT, padx=(0, 18))
        actions = ttk.Frame(toolbar)
        actions.pack(side=tk.TOP, fill=tk.X)
        for label, command in (("Load CSV", self.load), ("Generate", self.generate), ("Solve", self.solve),
                               ("Animate", self.animate), ("Pause", self.pause), ("Resume", self.resume),
                               ("Reset", self.reset), ("Export CSV", self.export)):
            ttk.Button(actions, text=label, command=command).pack(side=tk.LEFT, padx=(0, 7))
        ttk.Label(actions, text="Speed").pack(side=tk.LEFT, padx=(6, 3))
        self.speed = tk.IntVar(value=700)
        ttk.Scale(actions, from_=150, to=1800, variable=self.speed, orient=tk.HORIZONTAL, length=110).pack(side=tk.LEFT)
        self.figure, self.axis = self.plt.subplots(figsize=(8, 5))
        self.canvas = self.FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)
        self.result = tk.Text(self.root, height=7, wrap=tk.WORD, state=tk.DISABLED)
        self.result.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(4, 10))
        ttk.Label(self.root, textvariable=self.vars["status"], anchor=tk.W).pack(fill=tk.X, padx=12, pady=(0, 8))
        self._draw()

    def _inputs(self):
        n, k, c = (int(self.vars[key].get()) for key in ("n", "k", "c"))
        if n < 1 or k < 0 or c < 0:
            raise ValueError("N must be positive; K and C must be zero or greater.")
        return n, k, c

    def _guard(self, callback):
        try:
            callback()
        except Exception as exc:
            messagebox.showerror("Could not complete action", str(exc), parent=self.root)

    def load(self):
        def action():
            n, _, _ = self._inputs()
            path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if path:
                self.graph = load_graph(path, n)
                self.solution = None
                self.vars["status"].set(f"Loaded {self.graph.flight_count} directed flights from {path}.")
                self._draw()
        self._guard(action)

    def generate(self):
        def action():
            n, k, c = self._inputs()
            self.graph = generate_graph(n, k, c, seed=random.randrange(1 << 30))
            self.solution = None
            self.vars["status"].set(f"Generated {n} cities and {self.graph.flight_count} flights; guaranteed route included.")
            self._draw()
        self._guard(action)

    def solve(self):
        def action():
            n, k, c = self._inputs()
            if self.graph is None or self.graph.city_count != n:
                raise ValueError("Generate or load a graph with the current number of cities first.")
            self.solution = solve(self.graph, k, c)
            self._show_result()
            self._draw()
            self.vars["status"].set("Cheapest valid journey found." if self.solution else "No journey fits the stop limit.")
        self._guard(action)

    def _show_result(self, animation=None):
        self.result.configure(state=tk.NORMAL)
        self.result.delete("1.0", tk.END)
        s = self.solution
        if s is None:
            text = "No valid route exists within the stop limit. Minimum cost: -1."
        else:
            cities = [str(s.route[0].flight.source)] + [str(step.flight.destination) for step in s.route] if s.route else ["1"]
            text = (f"Minimum cost: {s.cost}\nRoute: {' → '.join(cities)}\nFlights: {s.flights_used}   "
                    f"Intermediate stops: {max(0, s.flights_used - 1)}   Coupons used: {s.coupons_used}\n"
                    f"Original ticket total: {s.original_total}   Coupon savings: {s.savings}   Final cost: {s.cost}")
        if animation:
            text = animation + "\n" + text
        self.result.insert(tk.END, text)
        self.result.configure(state=tk.DISABLED)

    def _draw(self, active_step=None):
        import networkx as nx
        self.axis.clear()
        self.axis.set_axis_off()
        if not self.graph:
            self.canvas.draw_idle()
            return
        g = nx.MultiDiGraph()
        g.add_nodes_from(range(1, self.graph.city_count + 1))
        for idx, f in enumerate(self.graph.flights):
            g.add_edge(f.source, f.destination, key=idx, label=str(f.price))
        # A larger spring constant and scale reduce crowding as the graph grows.
        pos = nx.spring_layout(g, seed=12, k=2.0 / max(1, self.graph.city_count) ** 0.5,
                               scale=1.45, iterations=120)
        selected = {}
        route_cities = set()
        if self.solution:
            route_cities.add(1)
            for step in self.solution.route:
                route_cities.update((step.flight.source, step.flight.destination))
                idx = next((i for i, f in enumerate(self.graph.flights) if f is step.flight), None)
                if idx is not None:
                    selected[idx] = "#e8b923" if step.coupon_used else "#2878b5"
        colors = ["#72c77a" if n == 1 else "#ed7777" if n == self.graph.city_count else "#f4a742" if n in route_cities else "#d9e1e8" for n in g.nodes]
        nx.draw_networkx_nodes(g, pos, node_color=colors, node_size=750, ax=self.axis)
        nx.draw_networkx_labels(g, pos, ax=self.axis, font_size=9)
        for idx, f in enumerate(self.graph.flights):
            color = selected.get(idx, "#9aa6b2")
            if active_step == idx:
                # Coupon flights stay gold while active so their discount is clear.
                color = selected.get(idx, "#b21f35")
            rad = .12 * (1 if idx % 2 else -1) if sum(1 for x in self.graph.flights if x.source == f.source and x.destination == f.destination) > 1 else .04
            nx.draw_networkx_edges(g, pos, edgelist=[(f.source, f.destination)], edge_color=color, width=2.5 if idx in selected else 1.1,
                                   arrows=True, arrowsize=17, connectionstyle=f"arc3,rad={rad}", ax=self.axis)
            x1, y1 = pos[f.source]; x2, y2 = pos[f.destination]
            self.axis.text((x1+x2)/2, (y1+y2)/2 + .035 + (idx % 2)*.035, str(f.price), color=color, fontsize=8,
                           bbox={"facecolor":"white", "alpha":.7, "edgecolor":"none", "pad":1})
        self.axis.set_title("Flights (arrows show direction; edge labels show original prices)")
        self.axis.text(.01, .02, "Green: start   Red: destination   Orange: route city   Blue: route flight   Gold: coupon flight",
                       transform=self.axis.transAxes, fontsize=8)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def animate(self):
        if not self.solution:
            self.solve()
        if not self.solution:
            return
        self.reset()
        self.step_index = 0
        self.paused = False
        coupons = int(self.vars["c"].get())
        self._show_result(f"Start: city 1 | Running cost 0 | Flights 0 | Stops 0 | Coupons available {coupons}")
        self.vars["status"].set(f"Start: city 1 | Running cost 0 | Flights 0 | Stops 0 | Coupons available {coupons}")
        self.after_id = self.root.after(max(100, int(self.speed.get())), self._tick)

    def _tick(self):
        if self.paused or self.solution is None:
            return
        if self.step_index >= self.solution.flights_used:
            self._draw()
            self.vars["status"].set(f"Journey complete. Cost {self.solution.cost}; savings {self.solution.savings}.")
            return
        step = self.solution.route[self.step_index]
        flight_index = next(i for i, f in enumerate(self.graph.flights) if f is step.flight)
        self._draw(active_step=flight_index)
        running = sum(s.final_price for s in self.solution.route[:self.step_index + 1])
        remaining = int(self.vars["c"].get()) - sum(s.coupon_used for s in self.solution.route[:self.step_index + 1])
        label = f"Flight {step.flight.source} → {step.flight.destination}: {step.flight.price}"
        if step.coupon_used:
            label += f" → {step.final_price} (coupon)"
        flights_taken = self.step_index + 1
        stops_used = max(0, flights_taken - 1)
        label += f" | Running cost {running} | Flights {flights_taken} | Stops {stops_used} | Coupons left {remaining}"
        self.vars["status"].set(label)
        self._show_result(label)
        self.step_index += 1
        self.after_id = self.root.after(max(100, int(self.speed.get())), self._tick)

    def pause(self):
        self.paused = True
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def resume(self):
        if self.solution and self.paused:
            self.paused = False
            self._tick()

    def reset(self):
        self.paused = True
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.step_index = 0
        self._draw()
        if self.solution:
            self._show_result()
        self.vars["status"].set("Animation reset." if self.graph else "Load or generate a flight network.")

    def export(self):
        def action():
            if self.graph is None:
                raise ValueError("Load or generate a graph before exporting.")
            path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if path:
                export_results(path, self.graph, self.solution)
                self.vars["status"].set(f"Results exported to {path}.")
        self._guard(action)


def gui():
    import matplotlib
    matplotlib.use("TkAgg")
    root = tk.Tk()
    TravellerApp(root)
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdin", action="store_true", help="read N M, K C and flight rows from standard input")
    args = parser.parse_args()
    if args.stdin:
        solve_stdin()
    else:
        gui()
