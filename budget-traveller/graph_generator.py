"""Reproducible helpers for generating demonstrable flight networks."""
import random
from graph_model import Flight, FlightGraph
from solver import solve


def generate_graph(city_count, max_stops, coupons, solvable=True, seed=None):
    if city_count < 1 or max_stops < 0 or coupons < 0:
        raise ValueError("N must be positive; K and C must be nonnegative.")
    rng = random.Random(seed)
    flights = []
    if city_count > 1 and solvable:
        # Build one guaranteed feasible route. When possible, make it non-direct
        # so generated examples demonstrate the stop limit and route animation.
        max_flights = min(max_stops + 1, city_count - 1)
        min_flights = 2 if max_flights >= 2 else 1
        route_length = rng.randint(min_flights, max_flights)
        middle = rng.sample(range(2, city_count), route_length - 1)
        route = [1, *middle, city_count]
        for source, destination in zip(route, route[1:]):
            flights.append(Flight(source, destination, rng.randint(120, 1100)))
    # Add extra directed flights for alternate routes, cycles, and parallel
    # choices. Avoid 1 -> N when a longer guaranteed route is possible.
    extra_count = max(4, city_count * 3) - len(flights)
    for _ in range(max(0, extra_count)):
        if city_count < 2:
            break
        a = rng.randint(1, city_count)
        b = rng.randint(1, city_count - 1)
        if b >= a:
            b += 1
        if solvable and city_count > 2 and max_stops >= 1 and a == 1 and b == city_count:
            continue
        flights.append(Flight(a, b, rng.randint(0, 1200)))
    graph = FlightGraph(city_count, flights)
    if solvable and city_count > 1 and solve(graph, max_stops, coupons) is None:
        raise RuntimeError("Generated graph unexpectedly has no feasible route.")
    if not solvable and city_count > 1:
        # Removing every outgoing flight from city 1 makes reaching N impossible.
        flights = [f for f in flights if f.source != 1]
        graph = FlightGraph(city_count, flights)
    return graph
