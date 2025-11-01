"""
Unit tests for pathfinding algorithms
"""

import pytest
from src.graph import Graph
from src.pathfinding import dijkstra, astar, bellman_ford, floyd_warshall
from src.pathfinding.dijkstra import reconstruct_path


def create_test_graph():
    """Create a simple test graph"""
    g = Graph(directed=False, weighted=True)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 2)
    g.add_edge(1, 2, 1)
    g.add_edge(1, 3, 5)
    g.add_edge(2, 3, 8)
    g.add_edge(2, 4, 10)
    g.add_edge(3, 4, 2)
    return g


def test_dijkstra():
    """Test Dijkstra's algorithm"""
    g = create_test_graph()
    distances, predecessors, steps = dijkstra(g, 0, 4)
    
    assert distances[4] == 12  # 0->2->1->3->4
    assert len(steps) > 0
    
    path = reconstruct_path(predecessors, 0, 4)
    assert path[0] == 0
    assert path[-1] == 4


def test_astar():
    """Test A* algorithm"""
    g = create_test_graph()
    positions = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1), 4: (2, 1)}
    
    path, cost, steps = astar(g, 0, 4, positions)
    
    assert path[0] == 0
    assert path[-1] == 4
    assert cost > 0
    assert len(steps) > 0


def test_bellman_ford():
    """Test Bellman-Ford algorithm"""
    g = create_test_graph()
    distances, predecessors, has_neg_cycle, steps = bellman_ford(g, 0)
    
    assert not has_neg_cycle
    assert distances[0] == 0
    assert distances[4] == 12


def test_bellman_ford_negative_cycle():
    """Test Bellman-Ford with negative cycle"""
    g = Graph(directed=True, weighted=True)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, -3)
    g.add_edge(2, 0, 1)
    
    distances, predecessors, has_neg_cycle, steps = bellman_ford(g, 0)
    
    assert has_neg_cycle


def test_floyd_warshall():
    """Test Floyd-Warshall algorithm"""
    g = create_test_graph()
    dist_matrix, next_matrix, steps = floyd_warshall(g)
    
    vertices = sorted(g.vertices)
    vertex_to_idx = {v: i for i, v in enumerate(vertices)}
    
    # Check distance from 0 to 4
    distance = dist_matrix[vertex_to_idx[0]][vertex_to_idx[4]]
    assert distance == 12


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
