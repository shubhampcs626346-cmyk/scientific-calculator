# DAA Project: Advanced Graph Algorithms Suite

## Project Overview
A comprehensive implementation of advanced graph algorithms with performance analysis, visualization data generation, and real-world applications.

## Author
MST Student - Design and Analysis of Algorithms Project

## Features

### 1. Pathfinding Algorithms
- **Dijkstra's Algorithm**: Single-source shortest path for weighted graphs
- **A* Algorithm**: Heuristic-based pathfinding with Manhattan distance
- **Bellman-Ford Algorithm**: Handles negative weights, detects negative cycles
- **Floyd-Warshall Algorithm**: All-pairs shortest paths

### 2. Minimum Spanning Tree
- **Kruskal's Algorithm**: Edge-based MST with Union-Find
- **Prim's Algorithm**: Vertex-based MST with priority queue

### 3. Network Flow
- **Ford-Fulkerson Algorithm**: Maximum flow in flow networks
- **Applications**: Network capacity, bipartite matching

### 4. Graph Coloring
- **Greedy Coloring**: Fast approximation
- **Backtracking**: Optimal solution for small graphs

### 5. Traveling Salesman Problem (TSP)
- **Dynamic Programming**: Held-Karp algorithm
- **Branch and Bound**: Optimized search with pruning
- **Greedy Heuristic**: Fast approximation

### 6. Performance Analysis
- Time complexity measurement
- Space complexity analysis
- Comparative benchmarking
- Visualization data export (JSON format)

## Project Structure
```
daa_graph_algorithms_suite/
├── README.md
├── requirements.txt
├── main.py                          # Main entry point
├── src/
│   ├── __init__.py
│   ├── graph.py                     # Graph data structure
│   ├── pathfinding/
│   │   ├── __init__.py
│   │   ├── dijkstra.py
│   │   ├── astar.py
│   │   ├── bellman_ford.py
│   │   └── floyd_warshall.py
│   ├── mst/
│   │   ├── __init__.py
│   │   ├── kruskal.py
│   │   └── prim.py
│   ├── flow/
│   │   ├── __init__.py
│   │   └── ford_fulkerson.py
│   ├── coloring/
│   │   ├── __init__.py
│   │   ├── greedy.py
│   │   └── backtracking.py
│   ├── tsp/
│   │   ├── __init__.py
│   │   ├── dynamic_programming.py
│   │   ├── branch_bound.py
│   │   └── greedy.py
│   └── utils/
│       ├── __init__.py
│       ├── performance.py
│       └── visualization.py
├── tests/
│   ├── __init__.py
│   ├── test_pathfinding.py
│   ├── test_mst.py
│   └── test_tsp.py
├── examples/
│   ├── city_network.py
│   ├── social_network.py
│   └── logistics_optimization.py
└── output/
    └── .gitkeep
```

## Installation

```bash
# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run All Algorithms
```bash
python main.py
```

### Run Specific Algorithm Category
```bash
python main.py --category pathfinding
python main.py --category mst
python main.py --category tsp
```

### Run with Custom Graph
```bash
python main.py --graph examples/city_network.py
```

### Generate Performance Report
```bash
python main.py --benchmark --output output/performance_report.json
```

## Algorithm Complexity Analysis

| Algorithm | Time Complexity | Space Complexity | Use Case |
|-----------|----------------|------------------|----------|
| Dijkstra | O((V+E)log V) | O(V) | Non-negative weights |
| A* | O(E) | O(V) | Heuristic pathfinding |
| Bellman-Ford | O(VE) | O(V) | Negative weights |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest path |
| Kruskal | O(E log E) | O(V) | Sparse graphs |
| Prim | O((V+E)log V) | O(V) | Dense graphs |
| Ford-Fulkerson | O(E·f) | O(V²) | Max flow (f = max flow) |
| TSP (DP) | O(2ⁿ·n²) | O(2ⁿ·n) | Exact solution |
| TSP (Branch & Bound) | O(n!) worst | O(n) | Optimized exact |

## Real-World Applications

1. **GPS Navigation**: Dijkstra's & A* for route planning
2. **Network Design**: MST for minimal cable/pipeline layout
3. **Traffic Flow**: Max flow for network capacity
4. **Map Coloring**: Graph coloring for frequency assignment
5. **Delivery Routes**: TSP for logistics optimization

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_pathfinding.py -v
```

## Performance Benchmarking

The project includes comprehensive benchmarking tools:
- Execution time measurement
- Memory usage tracking
- Scalability analysis (varying graph sizes)
- Comparative analysis between algorithms

## Visualization Output

All algorithms generate JSON output compatible with visualization tools:
- Node positions
- Edge weights
- Algorithm steps
- Path/tree highlighting
- Performance metrics

## Academic References

1. Cormen, T. H., et al. (2009). Introduction to Algorithms (3rd ed.)
2. Sedgewick, R., & Wayne, K. (2011). Algorithms (4th ed.)
3. Kleinberg, J., & Tardos, É. (2005). Algorithm Design

## License
MIT License - Educational Purpose

## Contributing
This is an academic project. Suggestions and improvements are welcome!

## Contact
For questions or discussions about the implementation, please refer to the code comments and documentation.
