"""
Floyd-Warshall Algorithm Implementation
All-pairs shortest path algorithm
Time Complexity: O(V³)
Space Complexity: O(V²)
"""

from typing import List, Tuple
from ..graph import Graph


def floyd_warshall(graph: Graph) -> Tuple[List[List[float]], List[List[int]], List[Dict]]:
    """
    Floyd-Warshall all-pairs shortest path algorithm
    
    Args:
        graph: Input graph
        
    Returns:
        distances: 2D matrix of shortest distances
        next_vertex: 2D matrix for path reconstruction
        steps: List of algorithm steps for visualization
    """
    vertices = sorted(graph.vertices)
    n = len(vertices)
    vertex_to_idx = {v: i for i, v in enumerate(vertices)}
    
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]
    next_vertex = [[None] * n for _ in range(n)]
    
    # Distance from vertex to itself is 0
    for i in range(n):
        dist[i][i] = 0
    
    # Initialize with direct edges
    for u, v, weight in graph.edges:
        u_idx = vertex_to_idx[u]
        v_idx = vertex_to_idx[v]
        dist[u_idx][v_idx] = weight
        next_vertex[u_idx][v_idx] = v_idx
    
    steps = []
    
    # Floyd-Warshall main loop
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    new_dist = dist[i][k] + dist[k][j]
                    if new_dist < dist[i][j]:
                        dist[i][j] = new_dist
                        next_vertex[i][j] = next_vertex[i][k]
                        
                        steps.append({
                            'type': 'update',
                            'k': vertices[k],
                            'i': vertices[i],
                            'j': vertices[j],
                            'distance': new_dist
                        })
    
    return dist, next_vertex, steps


def reconstruct_path_floyd_warshall(
    next_vertex: List[List[int]],
    vertices: List[int],
    source: int,
    target: int
) -> List[int]:
    """
    Reconstruct path from Floyd-Warshall next_vertex matrix
    
    Args:
        next_vertex: Next vertex matrix from floyd_warshall
        vertices: List of vertices
        source: Starting vertex
        target: Target vertex
        
    Returns:
        List of vertices in the shortest path
    """
    vertex_to_idx = {v: i for i, v in enumerate(vertices)}
    
    if next_vertex[vertex_to_idx[source]][vertex_to_idx[target]] is None:
        return []
    
    path = [source]
    current = source
    
    while current != target:
        current_idx = vertex_to_idx[current]
        target_idx = vertex_to_idx[target]
        next_idx = next_vertex[current_idx][target_idx]
        current = vertices[next_idx]
        path.append(current)
    
    return path
