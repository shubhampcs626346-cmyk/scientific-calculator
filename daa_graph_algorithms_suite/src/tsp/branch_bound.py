"""
TSP Branch and Bound Implementation
Time Complexity: O(n!) worst case, much better with pruning
Space Complexity: O(n)
"""

from typing import List, Tuple, Dict
import heapq
from ..graph import Graph


class TSPNode:
    """Node in the branch and bound search tree"""
    
    def __init__(self, level: int, path: List[int], bound: float, cost: float):
        self.level = level
        self.path = path
        self.bound = bound
        self.cost = cost
    
    def __lt__(self, other):
        return self.bound < other.bound


def calculate_bound(graph: Graph, node: TSPNode, vertices: List[int], dist: List[List[float]]) -> float:
    """Calculate lower bound for the node"""
    n = len(vertices)
    bound = node.cost
    visited = set(node.path)
    
    # Add minimum outgoing edge cost for each unvisited vertex
    for i in range(n):
        if i not in visited:
            min_edge = min(dist[i][j] for j in range(n) if i != j)
            bound += min_edge
    
    # Add cost to return to start
    if len(node.path) > 0:
        last = node.path[-1]
        bound += min(dist[last][j] for j in range(n) if j not in visited or j == 0)
    
    return bound


def tsp_branch_bound(graph: Graph, max_nodes: int = 10000) -> Tuple[List[int], float, List[Dict]]:
    """
    Traveling Salesman Problem using Branch and Bound
    
    Args:
        graph: Complete graph with all vertices connected
        max_nodes: Maximum nodes to explore (prevents excessive computation)
        
    Returns:
        tour: Best tour found
        cost: Total cost of the tour
        steps: List of algorithm steps for visualization
    """
    vertices = sorted(graph.vertices)
    n = len(vertices)
    
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
    
    # Priority queue for branch and bound
    pq = []
    root = TSPNode(0, [0], 0, 0)
    root.bound = calculate_bound(graph, root, vertices, dist)
    heapq.heappush(pq, root)
    
    best_cost = float('inf')
    best_tour = []
    steps = []
    nodes_explored = 0
    
    while pq and nodes_explored < max_nodes:
        node = heapq.heappop(pq)
        nodes_explored += 1
        
        # Prune if bound is worse than best solution
        if node.bound >= best_cost:
            steps.append({
                'type': 'prune',
                'path': [vertices[i] for i in node.path],
                'bound': node.bound
            })
            continue
        
        # If all vertices visited
        if node.level == n - 1:
            # Complete the tour
            last = node.path[-1]
            total_cost = node.cost + dist[last][0]
            
            if total_cost < best_cost:
                best_cost = total_cost
                best_tour = [vertices[i] for i in node.path] + [vertices[0]]
                
                steps.append({
                    'type': 'update_best',
                    'tour': best_tour,
                    'cost': best_cost
                })
            continue
        
        # Branch to unvisited vertices
        visited = set(node.path)
        current = node.path[-1]
        
        for next_v in range(n):
            if next_v not in visited:
                new_path = node.path + [next_v]
                new_cost = node.cost + dist[current][next_v]
                new_node = TSPNode(node.level + 1, new_path, 0, new_cost)
                new_node.bound = calculate_bound(graph, new_node, vertices, dist)
                
                if new_node.bound < best_cost:
                    heapq.heappush(pq, new_node)
                    
                    steps.append({
                        'type': 'branch',
                        'path': [vertices[i] for i in new_path],
                        'cost': new_cost,
                        'bound': new_node.bound
                    })
    
    return best_tour, best_cost, steps
