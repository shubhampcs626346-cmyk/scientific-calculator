"""
Prim's Algorithm Implementation
Minimum Spanning Tree using Priority Queue
Time Complexity: O((V + E) log V)
Space Complexity: O(V)
"""

from typing import List, Tuple, Optional
import heapq
from ..graph import Graph


def prim(graph: Graph, start_vertex: Optional[int] = None) -> Tuple[List[Tuple[int, int, float]], float, List[Dict]]:
    """
    Prim's Minimum Spanning Tree algorithm
    
    Args:
        graph: Input graph (must be undirected)
        start_vertex: Starting vertex (if None, uses arbitrary vertex)
        
    Returns:
        mst_edges: List of edges in the MST
        total_weight: Total weight of the MST
        steps: List of algorithm steps for visualization
    """
    if graph.directed:
        raise ValueError("Prim's algorithm requires an undirected graph")
    
    if not graph.vertices:
        return [], 0, []
    
    # Start from arbitrary vertex if not specified
    if start_vertex is None:
        start_vertex = min(graph.vertices)
    
    visited = set()
    mst_edges = []
    total_weight = 0
    steps = []
    
    # Priority queue: (weight, from_vertex, to_vertex)
    pq = [(0, start_vertex, start_vertex)]
    
    while pq and len(visited) < graph.get_vertex_count():
        weight, from_vertex, to_vertex = heapq.heappop(pq)
        
        if to_vertex in visited:
            continue
        
        visited.add(to_vertex)
        
        # Add edge to MST (skip the first dummy edge)
        if from_vertex != to_vertex:
            mst_edges.append((from_vertex, to_vertex, weight))
            total_weight += weight
            
            steps.append({
                'type': 'add',
                'edge': (from_vertex, to_vertex),
                'weight': weight,
                'total_weight': total_weight
            })
        
        # Add all edges from newly added vertex
        for neighbor, edge_weight in graph.get_neighbors(to_vertex):
            if neighbor not in visited:
                heapq.heappush(pq, (edge_weight, to_vertex, neighbor))
                
                steps.append({
                    'type': 'consider',
                    'edge': (to_vertex, neighbor),
                    'weight': edge_weight
                })
    
    return mst_edges, total_weight, steps
