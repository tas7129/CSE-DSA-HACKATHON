"""Validated directed flight network data model."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Flight:
    source: int
    destination: int
    price: int


class FlightGraph:
    def __init__(self, city_count: int, flights):
        if isinstance(city_count, bool) or not isinstance(city_count, int) or city_count < 1:
            raise ValueError("Number of cities N must be a positive integer.")
        self.city_count = city_count
        self.flights = []
        self.adjacency = [[] for _ in range(city_count + 1)]
        for flight in flights:
            f = flight if isinstance(flight, Flight) else Flight(*flight)
            if not (1 <= f.source <= city_count and 1 <= f.destination <= city_count):
                raise ValueError(f"City identifiers must be between 1 and {city_count}: {f}.")
            if isinstance(f.price, bool) or not isinstance(f.price, int) or f.price < 0:
                raise ValueError("Ticket prices must be nonnegative integers.")
            self.flights.append(f)
            self.adjacency[f.source].append((len(self.flights) - 1, f))

    @property
    def flight_count(self):
        return len(self.flights)
