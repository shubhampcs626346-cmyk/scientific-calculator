#!/usr/bin/env python3
"""
Main entry point for DAA Graph Algorithms Suite
Demonstrates all implemented algorithms with performance analysis
"""

import sys
import argparse
from src.graph import Graph
from src.pathfinding import dijkstra, astar, bellman_ford, floyd_warshall
from src.mst import kruskal, prim
from src.tsp import tsp_dp, tsp_branch_bound, tsp_greedy
from src.utils.performance import benchmark_algorithm, PerformanceTracker
from src.utils.visualization import (
    print_results, print_table, print_path, print_graph_info,
    format_time, format_memory, export_to_json
)


def create_sample_graph() -> Graph:
    """Create a sample weighted undirected graph"""
    g = Graph(directed=False, weighted=True)
    
    # Add edges (creating a connected graph)
    edges = [
        (0, 1, 4), (0, 2, 3),
        (1, 2, 1), (1, 3, 2),
        (2, 3, 4), (2, 4, 5),
        (3, 4, 1), (3, 5, 6),
        (4, 5, 2)
    ]
    
    for u, v, w in edges:
        g.add_edge(u, v, w)
    
    return g


def create_complete_graph(n: int) -> Graph:
    """Create a complete graph for TSP"""
    g = Graph(directed=False, weighted=True)
    
    # Create complete graph with random-like weights
    for i in range(n):
        for j in range(i + 1, n):
            weight = ((i + 1) * (j + 1) * 7) % 20 + 1
            g.add_edge(i, j, weight)
    
    return g


def demo_pathfinding(graph: Graph, tracker: PerformanceTracker):
    """Demonstrate pathfinding algorithms"""
    print("\n" + "=" * 80)
    print("PATHFINDING ALGORITHMS")
    print("=" * 80)
    
    source, target = 0, 5
    
    # Dijkstra's Algorithm
    print("\n--- Dijkstra's Algorithm ---")
    result = benchmark_algorithm(dijkstra, graph, source, target)
    distances, predecessors, steps = result['result']
    
    from src.pathfinding.dijkstra import reconstruct_path
    path = reconstruct_path(predecessors, source, target)
    
    print_path(path, distances[target])
    print(f"Time: {format_time(result['avg_time'])}")
    print(f"Memory: {format_memory(result['avg_memory'])}")
    tracker.track('Dijkstra', result['avg_time'], result['avg_memory'])
    
    # A* Algorithm
    print("\n--- A* Algorithm ---")
    positions = {i: (i % 3, i // 3) for i in graph.vertices}
    result = benchmark_algorithm(astar, graph, source, target, positions)
    path, cost, steps = result['result']
    
    print_path(path, cost)
    print(f"Time: {format_time(result['avg_time'])}")
    print(f"Memory: {format_memory(result['avg_memory'])}")
    tracker.track('A*', result['avg_time'], result['avg_memory'])
    
    # Bellman-Ford Algorithm
    print("\n--- Bellman-Ford Algorithm ---")
    result = benchmark_algorithm(bellman_ford, graph, source)
    distances, predecessors, has_neg_cycle, steps = result['result']
    
    print(f"Has negative cycle: {has_neg_cycle}")
    print(f"Distance to {target}: {distances[target]}")
    print(f"Time: {format_time(result['avg_time'])}")
    print(f"Memory: {format_memory(result['avg_memory'])}")
    tracker.track('Bellman-Ford', result['avg_time'], result['avg_memory'])
    
    # Floyd-Warshall Algorithm
    print("\n--- Floyd-Warshall Algorithm ---")
    result = benchmark_algorithm(floyd_warshall, graph)
    dist_matrix, next_matrix, steps = result['result']
    
    vertices = sorted(graph.vertices)
    vertex_to_idx = {v: i for i, v in enumerate(vertices)}
    distance = dist_matrix[vertex_to_idx[source]][vertex_to_idx[target]]
    
    print(f"Distance from {source} to {target}: {distance}")
    print(f"Time: {format_time(result['avg_time'])}")
    print(f"Memory: {format_memory(result['avg_memory'])}")
    tracker.track('Floyd-Warshall', result['avg_time'], result['avg_memory'])


def demo_mst(graph: Graph, tracker: PerformanceTracker):
    """Demonstrate Minimum Spanning Tree algorithms"""
    print("\n" + "=" * 80)
    print("MINIMUM SPANNING TREE ALGORITHMS")
    print("=" * 80)
    
    # Kruskal's Algorithm
    print("\n--- Kruskal's Algorithm ---")
    result = benchmark_algorithm(kruskal, graph)
    mst_edges, total_weight, steps = result['result']
    
    print(f"MST Weight: {total_weight}")
    print(f"MST Edges: {len(mst_edges)}")
    for u, v, w in mst_edges[:5]:
        print(f"  {u} -- {v} (weight: {w})")
    if len(mst_edges) > 5:
        print(f"  ... and {len(mst_edges) - 5} more edges")
    print(f"Time: {format_time(result['avg_time'])}")
    print(f"Memory: {format_memory(result['avg_memory'])}")
    tracker.track('Kruskal', result['avg_time'], result['avg_memory'])
    
    # Prim's Algorithm
    print("\n--- Prim's Algorithm ---")
    result = benchmark_algorithm(prim, graph, 0)
    mst_edges, total_weight, steps = result['result']
    
    print(f"MST Weight: {total_weight}")
    print(f"MST Edges: {len(mst_edges)}")
    for u, v, w in mst_edges[:5]:
        print(f"  {u} -- {v} (weight: {w})")
    if len(mst_edges) > 5:
        print(f"  ... and {len(mst_edges) - 5} more edges")
    print(f"Time: {format_time(result['avg_time'])}")
    print(f"Memory: {format_memory(result['avg_memory'])}")
    tracker.track('Prim', result['avg_time'], result['avg_memory'])


def demo_tsp(graph: Graph, tracker: PerformanceTracker):
    """Demonstrate Traveling Salesman Problem algorithms"""
    print("\n" + "=" * 80)
    print("TRAVELING SALESMAN PROBLEM ALGORITHMS")
    print("=" * 80)
    
    # Use smaller graph for TSP
    small_graph = create_complete_graph(8)
    
    # Greedy Heuristic
    print("\n--- Greedy (Nearest Neighbor) Heuristic ---")
    result = benchmark_algorithm(tsp_greedy, small_graph, 0)
    tour, cost, steps = result['result']
    
    print_path(tour, cost)
    print(f"Time: {format_time(result['avg_time'])}")
    print(f"Memory: {format_memory(result['avg_memory'])}")
    tracker.track('TSP-Greedy', result['avg_time'], result['avg_memory'])
    
    # Dynamic Programming (for small graphs)
    print("\n--- Dynamic Programming (Held-Karp) ---")
    try:
        result = benchmark_algorithm(tsp_dp, small_graph)
        tour, cost, steps = result['result']
        
        print_path(tour, cost)
        print(f"Time: {format_time(result['avg_time'])}")
        print(f"Memory: {format_memory(result['avg_memory'])}")
        tracker.track('TSP-DP', result['avg_time'], result['avg_memory'])
    except ValueError as e:
        print(f"Skipped: {e}")
    
    # Branch and Bound
    print("\n--- Branch and Bound ---")
    result = benchmark_algorithm(tsp_branch_bound, small_graph, max_nodes=5000)
    tour, cost, steps = result['result']
    
    print_path(tour, cost)
    print(f"Time: {format_time(result['avg_time'])}")
    print(f"Memory: {format_memory(result['avg_memory'])}")
    tracker.track('TSP-BranchBound', result['avg_time'], result['avg_memory'])


def print_performance_summary(tracker: PerformanceTracker):
    """Print performance comparison summary"""
    print("\n" + "=" * 80)
    print("PERFORMANCE SUMMARY")
    print("=" * 80)
    
    comparison = tracker.compare()
    
    headers = ['Algorithm', 'Avg Time', 'Min Time', 'Max Time', 'Avg Memory', 'Runs']
    rows = []
    
    for name, metrics in comparison.items():
        rows.append([
            name,
            format_time(metrics['avg_time']),
            format_time(metrics['min_time']),
            format_time(metrics['max_time']),
            format_memory(metrics['avg_memory']),
            metrics['runs']
        ])
    
    print_table(headers, rows)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='DAA Graph Algorithms Suite - Comprehensive Algorithm Demonstrations'
    )
    parser.add_argument(
        '--category',
        choices=['pathfinding', 'mst', 'tsp', 'all'],
        default='all',
        help='Algorithm category to run'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file for performance metrics (JSON)'
    )
    parser.add_argument(
        '--benchmark',
        action='store_true',
        help='Run comprehensive benchmarks'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("DAA GRAPH ALGORITHMS SUITE")
    print("Advanced Algorithm Implementations with Performance Analysis")
    print("=" * 80)
    
    # Create sample graph
    graph = create_sample_graph()
    print_graph_info(graph)
    
    # Performance tracker
    tracker = PerformanceTracker()
    
    # Run selected algorithms
    if args.category in ['pathfinding', 'all']:
        demo_pathfinding(graph, tracker)
    
    if args.category in ['mst', 'all']:
        demo_mst(graph, tracker)
    
    if args.category in ['tsp', 'all']:
        demo_tsp(graph, tracker)
    
    # Print performance summary
    print_performance_summary(tracker)
    
    # Export results if requested
    if args.output:
        export_to_json(tracker.compare(), args.output)
        print(f"\nPerformance metrics exported to: {args.output}")
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
