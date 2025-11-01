"""
Bellman-Ford Algorithm Implementation
Single-source shortest path with negative weight support
Time Complexity: O(VE)
Space Complexity: O(V)
"""

from typing import Dict, List, Tuple, Optional
from ..graph import Graph


def bellman_ford(graph: Graph, source: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]], bool, List[Dict]]:
    """
    Bellman-Ford shortest path algorithm
    
    Args:
        graph: Input graph
        source: Starting vertex
        
    Returns:
        distances: Dictionary of shortest distances from source
        predecessors: Dictionary of predecessors for path reconstruction
        has_negative_cycle: True if negative cycle detected
        steps: List of algorithm steps for visualization
    """
    distances = {vertex: float('inf') for vertex in graph.vertices}
    distances[source] = 0
    predecessors = {vertex: None for vertex in graph.vertices}
    steps = []
    
    # Relax edges V-1 times
    for iteration in range(graph.get_vertex_count() - 1):
        updated = False
        
        for u, v, weight in graph.edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u
                updated = True
                
                steps.append({
                    'type': 'relax',
                    'iteration': iteration,
                    'from': u,
                    'to': v,
                    'distance': distances[v]
                })
        
        # Early termination if no updates
        if not updated:
            break
    
    # Check for negative cycles
    has_negative_cycle = False
    for u, v, weight in graph.edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            has_negative_cycle = True
            steps.append({
                'type': 'negative_cycle',
                'edge': (u, v)
            })
            break
    
    return distances, predecessors, has_negative_cycle, steps
