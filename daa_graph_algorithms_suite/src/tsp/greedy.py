"""
TSP Greedy Heuristic Implementation (Nearest Neighbor)
Time Complexity: O(n^2)
Space Complexity: O(n)
"""

from typing import List, Tuple, Dict
from ..graph import Graph


def tsp_greedy(graph: Graph, start_vertex: int = None) -> Tuple[List[int], float, List[Dict]]:
    """
    Traveling Salesman Problem using Greedy Nearest Neighbor heuristic
    
    Args:
        graph: Complete graph with all vertices connected
        start_vertex: Starting vertex (if None, uses first vertex)
        
    Returns:
        tour: Approximate tour visiting all vertices
        cost: Total cost of the tour
        steps: List of algorithm steps for visualization
    """
    vertices = sorted(graph.vertices)
    n = len(vertices)
    
    if start_vertex is None:
        start_vertex = vertices[0]
    
    visited = set()
    tour = [start_vertex]
    visited.add(start_vertex)
    total_cost = 0
    steps = []
    
    current = start_vertex
    
    # Greedily select nearest unvisited neighbor
    while len(visited) < n:
        nearest = None
        min_dist = float('inf')
        
        for neighbor, weight in graph.get_neighbors(current):
            if neighbor not in visited and weight < min_dist:
                min_dist = weight
                nearest = neighbor
        
        if nearest is None:
            # No path found
            break
        
        tour.append(nearest)
        visited.add(nearest)
        total_cost += min_dist
        
        steps.append({
            'type': 'add',
            'from': current,
            'to': nearest,
            'cost': min_dist,
            'total_cost': total_cost
        })
        
        current = nearest
    
    # Return to start
    return_cost = graph.get_edge_weight(current, start_vertex)
    if return_cost is not None:
        tour.append(start_vertex)
        total_cost += return_cost
        
        steps.append({
            'type': 'return',
            'from': current,
            'to': start_vertex,
            'cost': return_cost,
            'total_cost': total_cost
        })
    
    return tour, total_cost, steps
