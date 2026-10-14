"""Matplotlib views for results and the actual top-level divide-and-conquer strip."""
from __future__ import annotations
from typing import Sequence
from brute_force import ClosestResult


def plot_closest(points: Sequence[tuple[float,float]], brute: ClosestResult, divide: ClosestResult):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter([p[0] for p in points],[p[1] for p in points],s=28,c="#64748b",label="Input points",zorder=2)
    for result, color, label in ((brute,"#e11d48","Brute force"),(divide,"#2563eb","Divide and conquer")):
        (x1,y1),(x2,y2)=result.pair
        ax.plot([x1,x2],[y1,y2],"o-",color=color,linewidth=2.4,markersize=7,
                label=f"{label}: {result.distance:.6g}",zorder=4)
    ax.set(title="Closest Pair of Points",xlabel="X",ylabel="Y"); ax.grid(alpha=.25); ax.legend()
    fig.tight_layout(); return fig


def plot_divide_step(points: Sequence[tuple[float,float]], trace: dict):
    import matplotlib.pyplot as plt
    fig, ax=plt.subplots(figsize=(8,6))
    ax.scatter([p[0] for p in points],[p[1] for p in points],c="#64748b",label="All points",zorder=2)
    sx=trace["split_x"]; d=trace["half_distance"]
    ax.axvspan(sx-d,sx+d,color="#f59e0b",alpha=.18,label=f"Strip (width 2d = {2*d:.4g})")
    ax.axvline(sx,color="#7c3aed",linestyle="--",label="Top-level dividing line")
    strip=trace["strip"]
    if strip:
        ax.scatter([points[i][0] for i in strip],[points[i][1] for i in strip],facecolors="none",edgecolors="#d97706",s=100,label="Strip points")
    cand=trace["candidates"]
    if cand:
        seen=set()
        for i,j in cand:
            ax.plot([points[i][0],points[j][0]],[points[i][1],points[j][1]],color="#0f766e",alpha=.35,lw=1)
            seen.update((i,j))
        ax.scatter([points[i][0] for i in seen],[points[i][1] for i in seen],c="#0f766e",marker="x",label="Candidate points considered")
    ax.set(title="Divide and Conquer: Top-Level Strip",xlabel="X",ylabel="Y"); ax.grid(alpha=.25); ax.legend()
    fig.tight_layout(); return fig
