"""Coupon- and stop-aware shortest path using Dijkstra on expanded states."""
from dataclasses import dataclass
import heapq
from itertools import count
from graph_model import FlightGraph


@dataclass(frozen=True)
class RouteStep:
    flight: object
    coupon_used: bool
    final_price: int


@dataclass
class Solution:
    cost: int
    route: list
    flights_used: int
    coupons_used: int
    original_total: int

    @property
    def savings(self):
        return self.original_total - self.cost


def solve(graph: FlightGraph, max_stops: int, coupons: int, start=1, destination=None):
    """Return the cheapest feasible journey, or None when there is no route.

    A state is (city, flights used, coupons used). Keeping flights in the state
    enforces the stop limit; coupon count distinguishes otherwise different
    future options. A unique heap tie-breaker permits parallel/equal-cost paths.
    """
    if isinstance(max_stops, bool) or not isinstance(max_stops, int) or max_stops < 0:
        raise ValueError("Maximum stops K must be a nonnegative integer.")
    if isinstance(coupons, bool) or not isinstance(coupons, int) or coupons < 0:
        raise ValueError("Coupon count C must be a nonnegative integer.")
    destination = graph.city_count if destination is None else destination
    for label, city in (("start", start), ("destination", destination)):
        if isinstance(city, bool) or not isinstance(city, int) or not 1 <= city <= graph.city_count:
            raise ValueError(f"{label.title()} city must be between 1 and {graph.city_count}.")
    if start == destination:
        return Solution(0, [], 0, 0, 0)
    limit = max_stops + 1
    origin = (start, 0, 0)
    distances = {origin: 0}
    previous = {}
    serial = count()
    queue = [(0, next(serial), origin)]
    best = None
    while queue:
        cost, _, state = heapq.heappop(queue)
        if cost != distances.get(state):
            continue
        city, used, spent = state
        if city == destination:
            best = state
            break
        if used >= limit:
            continue
        for flight_index, flight in graph.adjacency[city]:
            transitions = [(False, flight.price, spent)]
            if spent < coupons:
                transitions.append((True, flight.price // 2, spent + 1))
            for discounted, price, next_spent in transitions:
                next_state = (flight.destination, used + 1, next_spent)
                next_cost = cost + price
                if next_cost < distances.get(next_state, float("inf")):
                    distances[next_state] = next_cost
                    previous[next_state] = (state, flight_index, discounted, price)
                    heapq.heappush(queue, (next_cost, next(serial), next_state))
    if best is None:
        return None
    steps = []
    cursor = best
    while cursor != origin:
        prior, idx, discounted, final_price = previous[cursor]
        steps.append(RouteStep(graph.flights[idx], discounted, final_price))
        cursor = prior
    steps.reverse()
    return Solution(distances[best], steps, len(steps), sum(s.coupon_used for s in steps),
                     sum(s.flight.price for s in steps))
