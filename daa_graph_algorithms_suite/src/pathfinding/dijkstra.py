"""
Dijkstra's Algorithm Implementation
Single-source shortest path for non-negative weighted graphs
Time Complexity: O((V + E) log V) with binary heap
Space Complexity: O(V)
"""

from typing import Dict, List, Tuple, Optional
import heapq
from ..graph import Graph


def dijkstra(graph: Graph, source: int, target: Optional[int] = None) -> Tuple[Dict[int, float], Dict[int, Optional[int]], List[Dict]]:
    """
    Dijkstra's shortest path algorithm
    
    Args:
        graph: Input graph
        source: Starting vertex
        target: Optional target vertex (if None, computes to all vertices)
        
    Returns:
        distances: Dictionary of shortest distances from source
        predecessors: Dictionary of predecessors for path reconstruction
        steps: List of algorithm steps for visualization
    """
    distances = {vertex: float('inf') for vertex in graph.vertices}
    distances[source] = 0
    predecessors = {vertex: None for vertex in graph.vertices}
    
    # Priority queue: (distance, vertex)
    pq = [(0, source)]
    visited = set()
    steps = []
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
            
        visited.add(current)
        
        # Record step for visualization
        steps.append({
            'type': 'visit',
            'vertex': current,
            'distance': current_dist,
            'visited': list(visited)
        })
        
        # Early termination if target found
        if target is not None and current == target:
            break
        
        # Relax edges
        for neighbor, weight in graph.get_neighbors(current):
            if neighbor in visited:
                continue
                
            new_dist = current_dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
                
                steps.append({
                    'type': 'relax',
                    'from': current,
                    'to': neighbor,
                    'distance': new_dist
                })
    
    return distances, predecessors, steps


def reconstruct_path(predecessors: Dict[int, Optional[int]], source: int, target: int) -> List[int]:
    """
    Reconstruct shortest path from source to target
    
    Args:
        predecessors: Dictionary of predecessors from dijkstra
        source: Starting vertex
        target: Target vertex
        
    Returns:
        List of vertices in the shortest path
    """
    path = []
    current = target
    
    while current is not None:
        path.append(current)
        current = predecessors[current]
        
    path.reverse()
    
    # Check if path is valid
    if path[0] != source:
        return []
        
    return path
