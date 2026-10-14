"""Repeatable timing experiments and a comparison plot."""
from __future__ import annotations
from statistics import median
from time import perf_counter
from point_generation import generate_points
from brute_force import closest_pair as brute
from divide_conquer import closest_pair as divide


def benchmark(sizes=(10,50,100,250,500,1000,2000), repeats=3, seed=1729):
    rows=[]
    for n in sizes:
        points=generate_points(n,seed=seed+n)
        assert abs(brute(points).distance-divide(points).distance) <= 1e-12
        times=[]
        for algorithm in (brute,divide):
            samples=[]
            for _ in range(repeats):
                start=perf_counter(); algorithm(points); samples.append((perf_counter()-start)*1000)
            times.append(median(samples))
        rows.append((n,*times))
    return rows


def plot_benchmark(rows):
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,5))
    ax.plot([r[0] for r in rows],[r[1] for r in rows],"o-",label="Brute force")
    ax.plot([r[0] for r in rows],[r[2] for r in rows],"o-",label="Divide and conquer")
    ax.set(xlabel="Number of points N",ylabel="Median execution time (ms)",title="Closest Pair Runtime Comparison")
    ax.grid(alpha=.3); ax.legend(); fig.tight_layout(); return fig
