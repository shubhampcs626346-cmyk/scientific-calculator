"""
Example: City Road Network
Demonstrates pathfinding algorithms on a realistic city network
"""

from src.graph import Graph
from src.pathfinding import dijkstra, astar
from src.pathfinding.dijkstra import reconstruct_path
from src.utils.visualization import print_path, print_results


def create_city_network():
    """
    Create a city road network graph
    Vertices represent intersections, edges represent roads with travel times
    """
    g = Graph(directed=False, weighted=True)
    
    # City intersections (0-9)
    # Edge weights represent travel time in minutes
    roads = [
        (0, 1, 5),   # Downtown to North District
        (0, 2, 3),   # Downtown to West District
        (0, 3, 7),   # Downtown to East District
        (1, 4, 4),   # North to Industrial
        (1, 5, 6),   # North to University
        (2, 3, 2),   # West to East
        (2, 6, 8),   # West to Airport
        (3, 4, 3),   # East to Industrial
        (3, 7, 5),   # East to Shopping Mall
        (4, 5, 2),   # Industrial to University
        (5, 8, 4),   # University to Hospital
        (6, 7, 6),   # Airport to Shopping Mall
        (7, 8, 3),   # Shopping Mall to Hospital
        (7, 9, 4),   # Shopping Mall to Stadium
        (8, 9, 2),   # Hospital to Stadium
    ]
    
    for u, v, w in roads:
        g.add_edge(u, v, w)
    
    return g


def main():
    """Demonstrate pathfinding on city network"""
    print("=" * 80)
    print("CITY ROAD NETWORK - PATHFINDING DEMONSTRATION")
    print("=" * 80)
    
    # Location names
    locations = {
        0: "Downtown",
        1: "North District",
        2: "West District",
        3: "East District",
        4: "Industrial Zone",
        5: "University",
        6: "Airport",
        7: "Shopping Mall",
        8: "Hospital",
        9: "Stadium"
    }
    
    # Create network
    city = create_city_network()
    
    print(f"\nCity Network: {city.get_vertex_count()} locations, {city.get_edge_count()} roads")
    
    # Find shortest path from Downtown to Stadium
    source = 0  # Downtown
    target = 9  # Stadium
    
    print(f"\nFinding shortest route from {locations[source]} to {locations[target]}...")
    
    # Using Dijkstra's algorithm
    distances, predecessors, steps = dijkstra(city, source, target)
    path = reconstruct_path(predecessors, source, target)
    
    print("\n--- Route Found ---")
    route_names = [locations[i] for i in path]
    print(" -> ".join(route_names))
    print(f"\nTotal travel time: {distances[target]} minutes")
    
    # Show distances to all locations from Downtown
    print("\n--- Travel Times from Downtown ---")
    for loc_id in sorted(locations.keys()):
        if loc_id != source:
            print(f"{locations[loc_id]}: {distances[loc_id]} minutes")
    
    # Using A* with coordinates
    print("\n--- Using A* Algorithm ---")
    positions = {
        0: (5, 5),   # Downtown (center)
        1: (5, 8),   # North
        2: (2, 5),   # West
        3: (8, 5),   # East
        4: (7, 7),   # Industrial
        5: (6, 9),   # University
        6: (0, 3),   # Airport
        7: (9, 3),   # Shopping Mall
        8: (8, 9),   # Hospital
        9: (10, 8),  # Stadium
    }
    
    path_astar, cost_astar, steps_astar = astar(city, source, target, positions)
    route_names_astar = [locations[i] for i in path_astar]
    
    print(" -> ".join(route_names_astar))
    print(f"\nTotal travel time: {cost_astar} minutes")
    print(f"Nodes explored: {len(steps_astar)}")


if __name__ == '__main__':
    main()
