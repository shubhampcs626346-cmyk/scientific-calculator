"""
A* Algorithm Implementation
Heuristic-based pathfinding algorithm
Time Complexity: O(E) in best case, O(b^d) in worst case
Space Complexity: O(V)
"""

from typing import Dict, List, Tuple, Callable, Optional
import heapq
from ..graph import Graph


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """Manhattan distance heuristic for grid-based graphs"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def euclidean_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """Euclidean distance heuristic"""
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5


def astar(
    graph: Graph,
    source: int,
    target: int,
    positions: Dict[int, Tuple[int, int]],
    heuristic: Callable = manhattan_distance
) -> Tuple[List[int], float, List[Dict]]:
    """
    A* pathfinding algorithm
    
    Args:
        graph: Input graph
        source: Starting vertex
        target: Target vertex
        positions: Dictionary mapping vertices to (x, y) coordinates
        heuristic: Heuristic function for distance estimation
        
    Returns:
        path: Shortest path from source to target
        cost: Total cost of the path
        steps: List of algorithm steps for visualization
    """
    # g_score: actual cost from source
    g_score = {vertex: float('inf') for vertex in graph.vertices}
    g_score[source] = 0
    
    # f_score: g_score + heuristic
    f_score = {vertex: float('inf') for vertex in graph.vertices}
    f_score[source] = heuristic(positions[source], positions[target])
    
    # Priority queue: (f_score, vertex)
    open_set = [(f_score[source], source)]
    came_from = {}
    closed_set = set()
    steps = []
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        
        if current in closed_set:
            continue
        
        steps.append({
            'type': 'visit',
            'vertex': current,
            'g_score': g_score[current],
            'f_score': current_f
        })
        
        if current == target:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(source)
            path.reverse()
            return path, g_score[target], steps
        
        closed_set.add(current)
        
        for neighbor, weight in graph.get_neighbors(current):
            if neighbor in closed_set:
                continue
            
            tentative_g = g_score[current] + weight
            
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(positions[neighbor], positions[target])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
                steps.append({
                    'type': 'relax',
                    'from': current,
                    'to': neighbor,
                    'g_score': tentative_g,
                    'f_score': f_score[neighbor]
                })
    
    return [], float('inf'), steps
