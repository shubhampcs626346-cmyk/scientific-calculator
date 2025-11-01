"""
Graph data structure implementation with support for various graph types
"""

from typing import List, Dict, Tuple, Set, Optional
from collections import defaultdict
import heapq


class Graph:
    """
    Flexible graph implementation supporting:
    - Directed/Undirected graphs
    - Weighted/Unweighted edges
    - Multiple graph representations
    """
    
    def __init__(self, directed: bool = False, weighted: bool = True):
        self.directed = directed
        self.weighted = weighted
        self.adjacency_list: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
        self.vertices: Set[int] = set()
        self.edges: List[Tuple[int, int, float]] = []
        self.num_vertices = 0
        self.num_edges = 0
        
    def add_vertex(self, vertex: int) -> None:
        """Add a vertex to the graph"""
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.num_vertices += 1
            
    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """Add an edge to the graph"""
        self.add_vertex(u)
        self.add_vertex(v)
        
        self.adjacency_list[u].append((v, weight))
        if not self.directed:
            self.adjacency_list[v].append((u, weight))
            
        self.edges.append((u, v, weight))
        self.num_edges += 1
        
    def get_neighbors(self, vertex: int) -> List[Tuple[int, float]]:
        """Get all neighbors of a vertex with edge weights"""
        return self.adjacency_list.get(vertex, [])
    
    def get_edge_weight(self, u: int, v: int) -> Optional[float]:
        """Get weight of edge between u and v"""
        for neighbor, weight in self.adjacency_list.get(u, []):
            if neighbor == v:
                return weight
        return None
    
    def get_all_edges(self) -> List[Tuple[int, int, float]]:
        """Get all edges in the graph"""
        if self.directed:
            return self.edges
        else:
            # For undirected graphs, return unique edges
            seen = set()
            unique_edges = []
            for u, v, w in self.edges:
                edge = tuple(sorted([u, v]))
                if edge not in seen:
                    seen.add(edge)
                    unique_edges.append((u, v, w))
            return unique_edges
    
    def to_adjacency_matrix(self) -> List[List[float]]:
        """Convert graph to adjacency matrix representation"""
        n = max(self.vertices) + 1 if self.vertices else 0
        matrix = [[float('inf')] * n for _ in range(n)]
        
        # Distance from vertex to itself is 0
        for i in range(n):
            matrix[i][i] = 0
            
        # Fill in edge weights
        for u in self.vertices:
            for v, weight in self.adjacency_list[u]:
                matrix[u][v] = weight
                
        return matrix
    
    def get_vertex_count(self) -> int:
        """Get number of vertices"""
        return self.num_vertices
    
    def get_edge_count(self) -> int:
        """Get number of edges"""
        return self.num_edges if self.directed else self.num_edges
    
    def __str__(self) -> str:
        """String representation of the graph"""
        graph_type = "Directed" if self.directed else "Undirected"
        weight_type = "Weighted" if self.weighted else "Unweighted"
        return f"{graph_type} {weight_type} Graph: {self.num_vertices} vertices, {self.num_edges} edges"


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure
    Used for Kruskal's algorithm and cycle detection
    """
    
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        
    def find(self, x: int) -> int:
        """Find root of element x with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """Union two sets by rank, return True if they were separate"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
            
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            
        return True


class PriorityQueue:
    """
    Min-heap based priority queue for graph algorithms
    """
    
    def __init__(self):
        self.heap = []
        self.entry_finder = {}
        self.counter = 0
        
    def push(self, item: int, priority: float) -> None:
        """Add item with priority"""
        if item in self.entry_finder:
            self.remove(item)
        entry = [priority, self.counter, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.heap, entry)
        self.counter += 1
        
    def pop(self) -> Tuple[int, float]:
        """Remove and return item with lowest priority"""
        while self.heap:
            priority, _, item = heapq.heappop(self.heap)
            if item in self.entry_finder:
                del self.entry_finder[item]
                return item, priority
        raise KeyError('pop from empty priority queue')
    
    def remove(self, item: int) -> None:
        """Mark item as removed"""
        if item in self.entry_finder:
            del self.entry_finder[item]
            
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self.entry_finder) == 0
    
    def __len__(self) -> int:
        return len(self.entry_finder)
