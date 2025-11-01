"""
Unit tests for Minimum Spanning Tree algorithms
"""

import pytest
from src.graph import Graph
from src.mst import kruskal, prim


def create_test_graph():
    """Create a simple test graph"""
    g = Graph(directed=False, weighted=True)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 3)
    g.add_edge(1, 2, 1)
    g.add_edge(1, 3, 2)
    g.add_edge(2, 3, 4)
    g.add_edge(3, 4, 2)
    g.add_edge(2, 4, 5)
    return g


def test_kruskal():
    """Test Kruskal's algorithm"""
    g = create_test_graph()
    mst_edges, total_weight, steps = kruskal(g)
    
    # MST should have V-1 edges
    assert len(mst_edges) == g.get_vertex_count() - 1
    
    # Check total weight
    assert total_weight == 8  # 1+2+2+3
    
    # Check steps recorded
    assert len(steps) > 0


def test_prim():
    """Test Prim's algorithm"""
    g = create_test_graph()
    mst_edges, total_weight, steps = prim(g, 0)
    
    # MST should have V-1 edges
    assert len(mst_edges) == g.get_vertex_count() - 1
    
    # Check total weight (should be same as Kruskal)
    assert total_weight == 8
    
    # Check steps recorded
    assert len(steps) > 0


def test_kruskal_prim_equivalence():
    """Test that Kruskal and Prim produce same MST weight"""
    g = create_test_graph()
    
    kruskal_edges, kruskal_weight, _ = kruskal(g)
    prim_edges, prim_weight, _ = prim(g, 0)
    
    assert kruskal_weight == prim_weight


def test_mst_directed_graph_error():
    """Test that MST algorithms reject directed graphs"""
    g = Graph(directed=True, weighted=True)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 2)
    
    with pytest.raises(ValueError):
        kruskal(g)
    
    with pytest.raises(ValueError):
        prim(g)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
