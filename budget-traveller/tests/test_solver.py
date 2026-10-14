import itertools
import random
import sys
import time
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from graph_model import Flight, FlightGraph
from solver import solve


def exhaustive(graph, k, coupons):
    """Independent layered dynamic program used to cross-check Dijkstra."""
    n = graph.city_count
    states = {(1, 0): 0}  # (city, coupons used) after the current layer
    if n == 1:
        return 0
    answer = None
    for _ in range(k + 1):
        nxt = {}
        for (city, used), cost in states.items():
            for _, f in graph.adjacency[city]:
                for spent, price in ([(used, f.price)] + ([(used + 1, f.price // 2)] if used < coupons else [])):
                    key = (f.destination, spent)
                    nxt[key] = min(nxt.get(key, float("inf")), cost + price)
        states = nxt
        candidates = [cost for (city, _), cost in states.items() if city == n]
        if candidates:
            value = min(candidates)
            answer = value if answer is None else min(answer, value)
    return answer


class SolverTests(unittest.TestCase):
    def check(self, n, flights, k, c, expected):
        graph = FlightGraph(n, flights)
        result = solve(graph, k, c)
        self.assertEqual(None if result is None else result.cost, expected)
        if result:
            self.assertLessEqual(result.flights_used, k + 1)
            self.assertLessEqual(result.coupons_used, c)
            self.assertEqual(sum(s.final_price for s in result.route), result.cost)
            self.assertEqual(sum(s.flight.price for s in result.route), result.original_total)
            self.assertTrue(all(s.final_price == (s.flight.price // 2 if s.coupon_used else s.flight.price) for s in result.route))
        return result

    def test_direct_coupon_and_no_coupon(self):
        self.check(2, [(1,2,101)], 0, 0, 101)
        self.check(2, [(1,2,101)], 0, 1, 50)

    def test_stops_unreachable_and_limit(self):
        self.check(4, [(1,2,1),(2,3,1),(3,4,1)], 2, 0, 3)
        self.check(3, [(1,2,1),(2,3,1)], 0, 1, None)
        self.check(3, [(1,2,1),(2,3,1)], 1, 0, 2)
        self.check(4, [], 5, 4, None)

    def test_coupon_placement_rounding_and_unused(self):
        result = self.check(4, [(1,2,4),(2,4,101),(1,3,60),(3,4,60)], 1, 1, 54)
        self.assertTrue(result.route[-1].coupon_used)
        self.check(2, [(1,2,9)], 0, 4, 4)
        self.check(2, [(1,2,1)], 0, 1, 0)
        self.check(3, [(1,2,0),(2,3,0)], 1, 2, 0)

    def test_cycles_parallel_and_single_city(self):
        self.check(3, [(1,2,0),(2,1,0),(1,3,10),(1,3,7)], 2, 0, 7)
        self.check(1, [], 0, 0, 0)

    def test_invalid_data(self):
        for flights in [[(0,2,3)], [(1,2,-1)]]:
            with self.assertRaises(ValueError):
                FlightGraph(2, flights)
        for k, c in [(-1,0),(0,-1)]:
            with self.assertRaises(ValueError):
                solve(FlightGraph(2, []), k, c)

    def test_random_against_exhaustive_reference(self):
        rng = random.Random(3401)
        for _ in range(120):
            n = rng.randint(2, 6)
            flights = [(rng.randint(1,n), rng.randint(1,n), rng.randint(0,30)) for _ in range(rng.randint(0,15))]
            graph = FlightGraph(n, flights)
            k, c = rng.randint(0,4), rng.randint(0,3)
            reference = exhaustive(graph, k, c)
            result = solve(graph, k, c)
            self.assertEqual(None if result is None else result.cost, reference)

    def test_performance_smoke(self):
        rows = []
        for n in (20, 40, 80):
            rng = random.Random(n)
            flights = [(i, i+1, rng.randint(1,99)) for i in range(1,n)]
            flights += [(rng.randint(1,n), rng.randint(1,n), rng.randint(1,99)) for _ in range(n*5)]
            graph = FlightGraph(n, flights)
            start = time.perf_counter()
            result = solve(graph, min(12,n-1), 3)
            elapsed = time.perf_counter() - start
            rows.append((n, len(flights), result.cost if result else -1, elapsed,
                         n * (min(12,n-1)+2) * 4))
        print("\nPerformance (N, M, cost, seconds, upper-bound states):")
        for row in rows:
            print("%d, %d, %d, %.6f, %d" % row)


if __name__ == "__main__":
    unittest.main()
