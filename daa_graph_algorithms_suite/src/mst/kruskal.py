"""
Kruskal's Algorithm Implementation
Minimum Spanning Tree using Union-Find
Time Complexity: O(E log E)
Space Complexity: O(V)
"""

from typing import List, Tuple
from ..graph import Graph, UnionFind


def kruskal(graph: Graph) -> Tuple[List[Tuple[int, int, float]], float, List[Dict]]:
    """
    Kruskal's Minimum Spanning Tree algorithm
    
    Args:
        graph: Input graph (must be undirected)
        
    Returns:
        mst_edges: List of edges in the MST
        total_weight: Total weight of the MST
        steps: List of algorithm steps for visualization
    """
    if graph.directed:
        raise ValueError("Kruskal's algorithm requires an undirected graph")
    
    # Get all edges and sort by weight
    edges = graph.get_all_edges()
    edges.sort(key=lambda x: x[2])
    
    # Initialize Union-Find
    max_vertex = max(graph.vertices)
    uf = UnionFind(max_vertex + 1)
    
    mst_edges = []
    total_weight = 0
    steps = []
    
    for u, v, weight in edges:
        steps.append({
            'type': 'consider',
            'edge': (u, v),
            'weight': weight
        })
        
        # Check if adding this edge creates a cycle
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            
            steps.append({
                'type': 'add',
                'edge': (u, v),
                'weight': weight,
                'total_weight': total_weight
            })
            
            # MST complete when we have V-1 edges
            if len(mst_edges) == graph.get_vertex_count() - 1:
                break
        else:
            steps.append({
                'type': 'reject',
                'edge': (u, v),
                'reason': 'creates_cycle'
            })
    
    return mst_edges, total_weight, steps
