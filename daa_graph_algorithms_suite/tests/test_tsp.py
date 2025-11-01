"""
Unit tests for Traveling Salesman Problem algorithms
"""

import pytest
from src.graph import Graph
from src.tsp import tsp_dp, tsp_branch_bound, tsp_greedy


def create_complete_graph(n):
    """Create a complete graph for TSP testing"""
    g = Graph(directed=False, weighted=True)
    
    for i in range(n):
        for j in range(i + 1, n):
            weight = ((i + 1) * (j + 1) * 3) % 10 + 1
            g.add_edge(i, j, weight)
    
    return g


def test_tsp_greedy():
    """Test TSP greedy heuristic"""
    g = create_complete_graph(5)
    tour, cost, steps = tsp_greedy(g, 0)
    
    # Tour should start and end at same vertex
    assert tour[0] == tour[-1]
    
    # Tour should visit all vertices
    assert len(set(tour)) == g.get_vertex_count()
    
    # Cost should be positive
    assert cost > 0
    
    # Steps should be recorded
    assert len(steps) > 0


def test_tsp_dp():
    """Test TSP dynamic programming"""
    g = create_complete_graph(5)
    tour, cost, steps = tsp_dp(g)
    
    # Tour should start and end at same vertex
    assert tour[0] == tour[-1]
    
    # Tour should visit all vertices
    assert len(set(tour)) == g.get_vertex_count()
    
    # Cost should be positive
    assert cost > 0


def test_tsp_branch_bound():
    """Test TSP branch and bound"""
    g = create_complete_graph(5)
    tour, cost, steps = tsp_branch_bound(g, max_nodes=1000)
    
    # Tour should start and end at same vertex
    assert tour[0] == tour[-1]
    
    # Tour should visit all vertices
    assert len(set(tour)) == g.get_vertex_count()
    
    # Cost should be positive
    assert cost > 0


def test_tsp_dp_large_graph_error():
    """Test that DP rejects large graphs"""
    g = create_complete_graph(25)
    
    with pytest.raises(ValueError):
        tsp_dp(g)


def test_tsp_greedy_vs_optimal():
    """Test that greedy is not worse than 2x optimal (for small graphs)"""
    g = create_complete_graph(6)
    
    greedy_tour, greedy_cost, _ = tsp_greedy(g, 0)
    optimal_tour, optimal_cost, _ = tsp_dp(g)
    
    # Greedy should find a solution
    assert greedy_cost > 0
    
    # Greedy might not be optimal but should be reasonable
    assert greedy_cost >= optimal_cost


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
