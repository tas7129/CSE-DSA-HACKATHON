"""CSV import/export for directed flights and computed journey results."""
import csv
from graph_model import Flight, FlightGraph


def load_graph(path, city_count):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"source", "destination", "price"}
        if not reader.fieldnames or not required.issubset({h.strip().lower() for h in reader.fieldnames}):
            raise ValueError("CSV must include source,destination,price columns.")
        names = {h.strip().lower(): h for h in reader.fieldnames}
        flights = []
        for line, row in enumerate(reader, 2):
            try:
                if any(row[names[k]] is None or not row[names[k]].strip() for k in required):
                    raise ValueError("missing value")
                vals = [int(row[names[k]]) for k in ("source", "destination", "price")]
                flights.append(Flight(*vals))
            except (ValueError, TypeError) as exc:
                raise ValueError(f"Malformed CSV row {line}: expected integer source, destination, price.") from exc
    return FlightGraph(city_count, flights)


def export_results(path, graph, solution):
    selected = {}
    if solution:
        for order, step in enumerate(solution.route, 1):
            # Flight identity is preserved, including parallel flights.
            idx = next(i for i, f in enumerate(graph.flights) if f is step.flight and i not in selected)
            selected[idx] = (order, step)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "destination", "original_price", "coupon_used", "final_price", "on_path", "route_order"])
        for idx, flight in enumerate(graph.flights):
            entry = selected.get(idx)
            step = entry[1] if entry else None
            writer.writerow([flight.source, flight.destination, flight.price,
                             step.coupon_used if step else False,
                             step.final_price if step else flight.price,
                             "x" if step else "", entry[0] if entry else ""])
