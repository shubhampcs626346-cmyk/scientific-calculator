"""
Example: Social Network Analysis
Demonstrates graph algorithms on a social network
"""

from src.graph import Graph
from src.pathfinding import dijkstra
from src.pathfinding.dijkstra import reconstruct_path


def create_social_network():
    """
    Create a social network graph
    Vertices represent people, edges represent friendships with interaction strength
    """
    g = Graph(directed=False, weighted=True)
    
    # Friendships with interaction strength (inverse: lower = stronger)
    friendships = [
        (0, 1, 1),   # Alice - Bob (close friends)
        (0, 2, 2),   # Alice - Carol
        (0, 3, 3),   # Alice - David
        (1, 2, 1),   # Bob - Carol (close friends)
        (1, 4, 2),   # Bob - Eve
        (2, 3, 2),   # Carol - David
        (2, 5, 1),   # Carol - Frank (close friends)
        (3, 5, 2),   # David - Frank
        (4, 5, 1),   # Eve - Frank (close friends)
        (4, 6, 3),   # Eve - Grace
        (5, 6, 2),   # Frank - Grace
        (5, 7, 1),   # Frank - Henry (close friends)
        (6, 7, 1),   # Grace - Henry (close friends)
    ]
    
    for u, v, w in friendships:
        g.add_edge(u, v, w)
    
    return g


def main():
    """Demonstrate social network analysis"""
    print("=" * 80)
    print("SOCIAL NETWORK ANALYSIS")
    print("=" * 80)
    
    # Person names
    people = {
        0: "Alice",
        1: "Bob",
        2: "Carol",
        3: "David",
        4: "Eve",
        5: "Frank",
        6: "Grace",
        7: "Henry"
    }
    
    # Create network
    network = create_social_network()
    
    print(f"\nSocial Network: {network.get_vertex_count()} people, {network.get_edge_count()} friendships")
    
    # Find connection path between two people
    person1 = 0  # Alice
    person2 = 7  # Henry
    
    print(f"\nFinding connection path from {people[person1]} to {people[person2]}...")
    
    distances, predecessors, steps = dijkstra(network, person1, person2)
    path = reconstruct_path(predecessors, person1, person2)
    
    print("\n--- Connection Path ---")
    connection_names = [people[i] for i in path]
    print(" -> ".join(connection_names))
    print(f"\nConnection strength: {distances[person2]} (lower is stronger)")
    
    # Find all connection strengths from Alice
    print(f"\n--- Connection Strengths from {people[person1]} ---")
    for person_id in sorted(people.keys()):
        if person_id != person1:
            strength = distances[person_id]
            if strength == float('inf'):
                print(f"{people[person_id]}: Not connected")
            else:
                print(f"{people[person_id]}: {strength}")
    
    # Find most central person (lowest average distance to others)
    print("\n--- Network Centrality Analysis ---")
    centrality_scores = {}
    
    for person_id in people.keys():
        distances, _, _ = dijkstra(network, person_id)
        avg_distance = sum(d for d in distances.values() if d != float('inf')) / (len(people) - 1)
        centrality_scores[person_id] = avg_distance
    
    most_central = min(centrality_scores, key=centrality_scores.get)
    print(f"Most central person: {people[most_central]}")
    print(f"Average connection strength: {centrality_scores[most_central]:.2f}")
    
    print("\nCentrality Rankings:")
    for person_id, score in sorted(centrality_scores.items(), key=lambda x: x[1]):
        print(f"{people[person_id]}: {score:.2f}")


if __name__ == '__main__':
    main()
