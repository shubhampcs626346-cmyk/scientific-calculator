"""
TSP Dynamic Programming Implementation (Held-Karp Algorithm)
Time Complexity: O(2^n * n^2)
Space Complexity: O(2^n * n)
"""

from typing import List, Tuple, Dict
from ..graph import Graph


def tsp_dp(graph: Graph) -> Tuple[List[int], float, List[Dict]]:
    """
    Traveling Salesman Problem using Dynamic Programming (Held-Karp)
    
    Args:
        graph: Complete graph with all vertices connected
        
    Returns:
        tour: Optimal tour visiting all vertices
        cost: Total cost of the tour
        steps: List of algorithm steps for visualization
    """
    vertices = sorted(graph.vertices)
    n = len(vertices)
    
    if n > 20:
        raise ValueError("DP approach not recommended for graphs with > 20 vertices")
    
    # Convert to adjacency matrix
    dist = [[float('inf')] * n for _ in range(n)]
    for i, u in enumerate(vertices):
        for j, v in enumerate(vertices):
            if i == j:
                dist[i][j] = 0
            else:
                weight = graph.get_edge_weight(u, v)
                if weight is not None:
                    dist[i][j] = weight
    
    # DP table: dp[mask][i] = min cost to visit vertices in mask ending at i
    dp = [[float('inf')] * n for _ in range(1 << n)]
    parent = [[None] * n for _ in range(1 << n)]
    steps = []
    
    # Start from vertex 0
    dp[1][0] = 0
    
    # Iterate through all subsets
    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            
            if dp[mask][last] == float('inf'):
                continue
            
            # Try to extend to next vertex
            for next_v in range(n):
                if mask & (1 << next_v):
                    continue
                
                new_mask = mask | (1 << next_v)
                new_cost = dp[mask][last] + dist[last][next_v]
                
                if new_cost < dp[new_mask][next_v]:
                    dp[new_mask][next_v] = new_cost
                    parent[new_mask][next_v] = last
                    
                    steps.append({
                        'type': 'update',
                        'mask': bin(new_mask),
                        'vertex': vertices[next_v],
                        'cost': new_cost
                    })
    
    # Find minimum cost to complete the tour
    full_mask = (1 << n) - 1
    min_cost = float('inf')
    last_vertex = -1
    
    for i in range(n):
        cost = dp[full_mask][i] + dist[i][0]
        if cost < min_cost:
            min_cost = cost
            last_vertex = i
    
    # Reconstruct tour
    tour = []
    mask = full_mask
    current = last_vertex
    
    while current is not None:
        tour.append(vertices[current])
        next_current = parent[mask][current]
        if next_current is not None:
            mask ^= (1 << current)
        current = next_current
    
    tour.reverse()
    tour.append(vertices[0])  # Return to start
    
    return tour, min_cost, steps
