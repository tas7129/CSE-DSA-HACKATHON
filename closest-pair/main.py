"""Interactive command-line entry point for the closest-pair demonstration."""
from __future__ import annotations
import argparse
from math import isclose
from statistics import median
from time import perf_counter
from point_generation import generate_points
from brute_force import closest_pair as brute
from divide_conquer import closest_pair as divide
from visualization import plot_closest, plot_divide_step
from benchmark import benchmark, plot_benchmark


def timed(function, points, repeats):
    values=[]; result=None
    for _ in range(repeats):
        start=perf_counter(); result=function(points); values.append((perf_counter()-start)*1000)
    return result, median(values)


def main():
    parser=argparse.ArgumentParser(description="Compare closest-pair algorithms.")
    parser.add_argument("-n", "--count", type=int, help="number of random points (prompted if omitted)")
    parser.add_argument("--seed", type=int, default=None, help="seed for reproducible points")
    parser.add_argument("--min", dest="low", type=float, default=0, help="minimum coordinate")
    parser.add_argument("--max", dest="high", type=float, default=100, help="maximum coordinate")
    parser.add_argument("--repeats", type=int, default=5, help="timing repetitions")
    parser.add_argument("--no-plot", action="store_true", help="skip interactive result plots")
    parser.add_argument("--benchmark", action="store_true", help="also run the scaling benchmark")
    parser.add_argument("--max-n", type=int, default=2000, help="largest benchmark dataset")
    args=parser.parse_args()
    try:
        n=args.count if args.count is not None else int(input("Enter number of points N (at least 2): "))
    except ValueError:
        parser.error("N must be an integer of at least 2")
    if n < 2: parser.error("N must be at least 2 to find a pair")
    if args.repeats < 1: parser.error("--repeats must be at least 1")
    points=generate_points(n,x_range=(args.low,args.high),y_range=(args.low,args.high),seed=args.seed)
    result_b,time_b=timed(brute,points,args.repeats)
    result_d,time_d=timed(divide,points,args.repeats)
    def display(name,r):
        p,q=r.pair
        print(f"{name}: Distance = {r.distance:.6f}, Pair = ({p[0]:g}, {p[1]:g}) and ({q[0]:g}, {q[1]:g})")
    display("Brute-Force",result_b); display("Divide-and-Conquer",result_d)
    print(f"Execution Time: Brute-Force = {time_b:.3f} ms, Divide-and-Conquer = {time_d:.3f} ms (median of {args.repeats})")
    if isclose(result_b.distance,result_d.distance,rel_tol=1e-12,abs_tol=1e-12):
        print("Verification: PASSED — both algorithms found the same minimum distance.")
    else:
        print("Verification: FAILED — dataset preserved in closest_pair_debug_points.txt")
        with open("closest_pair_debug_points.txt","w",encoding="utf-8") as f:
            f.writelines(f"{x!r}, {y!r}\n" for x,y in points)
    if not args.no_plot:
        _,trace=divide(points,trace=True)
        plot_closest(points,result_b,result_d); plot_divide_step(points,trace)
    if args.benchmark:
        sizes=[n for n in (10,50,100,250,500,1000,2000) if n<=args.max_n]
        if args.max_n not in sizes: sizes.append(args.max_n)
        rows=benchmark(sizes,repeats=args.repeats)
        print("\nBenchmark (N, brute-force ms, divide-and-conquer ms):")
        for row in rows: print(f"{row[0]:>5}: {row[1]:.3f}, {row[2]:.3f}")
        if not args.no_plot: plot_benchmark(rows)
    if not args.no_plot:
        import matplotlib.pyplot as plt
        plt.show()


if __name__ == "__main__": main()
