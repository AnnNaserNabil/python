"""
8. Graph Algorithms with Recursion

Implementing graph algorithms using recursion.
- Graph representations (adjacency list/matrix)
- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- Topological sorting
- Connected components
- Shortest path (Dijkstra's, Bellman-Ford)
"""
from __future__ import annotations
from typing import TypeVar, Generic, List, Dict, Set, Tuple, Optional, Any, Union
from collections import deque, defaultdict
import heapq
import math

T = TypeVar('T')

# 1. Graph Representations
class Graph:
    """Graph implementation using adjacency list."""
    
    def __init__(self, directed: bool = False):
        self.adj_list: Dict[T, List[Tuple[T, int]]] = {}
        self.directed = directed
    
    def add_vertex(self, vertex: T) -> None:
        """Add a vertex to the graph."""
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
    
    def add_edge(self, u: T, v: T, weight: int = 1) -> None:
        """Add an edge between vertices u and v with optional weight."""
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))
    
    def get_vertices(self) -> List[T]:
        """Get all vertices in the graph."""
        return list(self.adj_list.keys())
    
    def get_edges(self) -> List[Tuple[T, T, int]]:
        """Get all edges in the graph as (u, v, weight) tuples."""
        edges = []
        for u in self.adj_list:
            for (v, weight) in self.adj_list[u]:
                if not self.directed and v < u:  # Avoid duplicate edges in undirected graph
                    continue
                edges.append((u, v, weight))
        return edges
    
    def __str__(self) -> str:
        """String representation of the graph."""
        result = []
        for vertex in self.adj_list:
            connections = ", ".join(f"{v}({w})" for v, w in self.adj_list[vertex])
            result.append(f"{vertex} -> {connections}")
        return "\n".join(result)

# 2. Depth-First Search (DFS)
def dfs_recursive(graph: Graph, start: T, visited: Optional[Set[T]] = None) -> List[T]:
    """Recursive DFS traversal of a graph."""
    if visited is None:
        visited = set()
    
    visited.add(start)
    result = [start]
    
    for neighbor, _ in graph.adj_list.get(start, []):
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))
    
    return result

def dfs_iterative(graph: Graph, start: T) -> List[T]:
    """Iterative DFS using a stack."""
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            # Push neighbors in reverse order to process them in order
            for neighbor, _ in reversed(graph.adj_list.get(vertex, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result

# 3. Breadth-First Search (BFS)
def bfs_recursive_level(graph: Graph, queue: deque, visited: Set[T], result: List[T]) -> None:
    """Helper function for recursive BFS."""
    if not queue:
        return
    
    level_size = len(queue)
    level_nodes = []
    
    for _ in range(level_size):
        vertex = queue.popleft()
        level_nodes.append(vertex)
        
        for neighbor, _ in graph.adj_list.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    result.append(level_nodes)
    bfs_recursive_level(graph, queue, visited, result)

def bfs_recursive(graph: Graph, start: T) -> List[List[T]]:
    """Recursive BFS that returns nodes level by level."""
    visited = {start}
    queue = deque([start])
    result: List[List[T]] = []
    bfs_recursive_level(graph, queue, visited, result)
    return result

def bfs_iterative(graph: Graph, start: T) -> List[T]:
    """Iterative BFS using a queue."""
    visited = {start}
    queue = deque([start])
    result = []
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        for neighbor, _ in graph.adj_list.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result

# 4. Topological Sorting
def topological_sort_dfs_visit(graph: Graph, vertex: T, visited: Set[T], 
                             temp_marks: Set[T], result: List[T]) -> bool:
    """Helper function for recursive topological sort with cycle detection."""
    if vertex in temp_marks:
        return False  # Cycle detected
    
    if vertex in visited:
        return True
    
    temp_marks.add(vertex)
    
    for neighbor, _ in graph.adj_list.get(vertex, []):
        if not topological_sort_dfs_visit(graph, neighbor, visited, temp_marks, result):
            return False
    
    temp_marks.remove(vertex)
    visited.add(vertex)
    result.append(vertex)
    return True

def topological_sort(graph: Graph) -> Optional[List[T]]:
    """Topological sort using DFS. Returns None if the graph has a cycle."""
    if not graph.directed:
        raise ValueError("Topological sort is only defined for directed acyclic graphs (DAGs)")
    
    visited: Set[T] = set()
    temp_marks: Set[T] = set()
    result: List[T] = []
    
    for vertex in graph.get_vertices():
        if vertex not in visited:
            if not topological_sort_dfs_visit(graph, vertex, visited, temp_marks, result):
                return None  # Cycle detected
    
    return result[::-1]  # Return reversed to get the correct order

# 5. Connected Components
def find_components_dfs(graph: Graph, vertex: T, visited: Set[T], component: List[T]) -> None:
    """Helper function to find connected components using DFS."""
    visited.add(vertex)
    component.append(vertex)
    
    for neighbor, _ in graph.adj_list.get(vertex, []):
        if neighbor not in visited:
            find_components_dfs(graph, neighbor, visited, component)

def connected_components(graph: Graph) -> List[List[T]]:
    """Find all connected components in an undirected graph."""
    if graph.directed:
        raise ValueError("Connected components are typically found in undirected graphs")
    
    visited: Set[T] = set()
    components: List[List[T]] = []
    
    for vertex in graph.get_vertices():
        if vertex not in visited:
            component: List[T] = []
            find_components_dfs(graph, vertex, visited, component)
            components.append(component)
    
    return components

# 6. Shortest Path Algorithms
def dijkstra(graph: Graph, start: T) -> Tuple[Dict[T, int], Dict[T, Optional[T]]]:
    """Dijkstra's algorithm for shortest paths from a single source."""
    # Initialize distances with infinity
    distances: Dict[T, Union[int, float]] = {v: math.inf for v in graph.get_vertices()}
    distances[start] = 0
    
    # Priority queue: (distance, vertex)
    heap = [(0, start)]
    
    # For path reconstruction
    previous: Dict[T, Optional[T]] = {v: None for v in graph.get_vertices()}
    
    while heap:
        current_dist, current = heapq.heappop(heap)
        
        # Skip if we've already found a better path
        if current_dist > distances[current]:
            continue
        
        for neighbor, weight in graph.adj_list.get(current, []):
            distance = current_dist + weight
            
            # If we found a shorter path to the neighbor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(heap, (distance, neighbor))
    
    return distances, previous

def bellman_ford(graph: Graph, start: T) -> Tuple[Dict[T, Union[int, float]], Dict[T, Optional[T]], bool]:
    """Bellman-Ford algorithm for shortest paths from a single source.
    Returns (distances, previous, has_negative_cycle)"""
    # Initialize distances
    distances: Dict[T, Union[int, float]] = {v: math.inf for v in graph.get_vertices()}
    distances[start] = 0
    
    # For path reconstruction
    previous: Dict[T, Optional[T]] = {v: None for v in graph.get_vertices()}
    
    # Relax all edges |V| - 1 times
    for _ in range(len(graph.get_vertices()) - 1):
        updated = False
        for u in graph.get_vertices():
            for v, weight in graph.adj_list.get(u, []):
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    previous[v] = u
                    updated = True
        if not updated:
            break  # No more updates, we can stop early
    
    # Check for negative-weight cycles
    for u in graph.get_vertices():
        for v, weight in graph.adj_list.get(u, []):
            if distances[u] + weight < distances[v]:
                return {}, {}, True  # Negative cycle detected
    
    return distances, previous, False

def get_shortest_path(previous: Dict[T, Optional[T]], target: T) -> List[T]:
    """Reconstruct the shortest path from previous dictionary."""
    path = []
    current = target
    
    while current is not None:
        path.append(current)
        current = previous[current]
    
    return path[::-1]  # Reverse to get from source to target

def demonstrate_graph_algorithms() -> None:
    """Demonstrate graph algorithms."""
    # Create an undirected graph
    print("=== Undirected Graph ===")
    undirected_graph = Graph(directed=False)
    undirected_graph.add_edge('A', 'B')
    undirected_graph.add_edge('A', 'C')
    undirected_graph.add_edge('B', 'D')
    undirected_graph.add_edge('C', 'E')
    undirected_graph.add_edge('D', 'E')
    undirected_graph.add_edge('D', 'F')
    undirected_graph.add_edge('E', 'F')
    
    print("Graph structure:")
    print(undirected_graph)
    
    print("\n=== DFS Traversal ===")
    print(f"Recursive DFS: {dfs_recursive(undirected_graph, 'A')}")
    print(f"Iterative DFS: {dfs_iterative(undirected_graph, 'A')}")
    
    print("\n=== BFS Traversal ===")
    print(f"Recursive BFS (level order): {bfs_recursive(undirected_graph, 'A')}")
    print(f"Iterative BFS: {bfs_iterative(undirected_graph, 'A')}")
    
    print("\n=== Connected Components ===")
    # Add a disconnected component
    undirected_graph.add_edge('X', 'Y')
    undirected_graph.add_edge('Y', 'Z')
    print(f"Connected components: {connected_components(undirected_graph)}")
    
    # Create a directed acyclic graph for topological sort
    print("\n=== Directed Acyclic Graph ===")
    dag = Graph(directed=True)
    dag.add_edge('A', 'B')
    dag.add_edge('A', 'C')
    dag.add_edge('B', 'D')
    dag.add_edge('C', 'D')
    dag.add_edge('D', 'E')
    dag.add_edge('E', 'F')
    
    print("Topological sort:")
    topo_order = topological_sort(dag)
    print(f"Topological order: {topo_order}")
    
    # Create a weighted graph for shortest path algorithms
    print("\n=== Weighted Graph (Dijkstra's Algorithm) ===")
    weighted_graph = Graph(directed=True)
    weighted_graph.add_edge('A', 'B', 4)
    weighted_graph.add_edge('A', 'C', 2)
    weighted_graph.add_edge('B', 'C', 1)
    weighted_graph.add_edge('B', 'D', 5)
    weighted_graph.add_edge('C', 'D', 8)
    weighted_graph.add_edge('C', 'E', 10)
    weighted_graph.add_edge('D', 'E', 2)
    weighted_graph.add_edge('D', 'F', 6)
    weighted_graph.add_edge('E', 'F', 2)
    
    print("Shortest paths from 'A' (Dijkstra's):")
    distances, previous = dijkstra(weighted_graph, 'A')
    for vertex in weighted_graph.get_vertices():
        path = get_shortest_path(previous, vertex)
        print(f"To {vertex}: Distance = {distances[vertex]}, Path = {path}")
    
    # Test Bellman-Ford with a graph that has negative weights but no negative cycles
    print("\n=== Weighted Graph with Negative Weights (Bellman-Ford) ===")
    negative_weight_graph = Graph(directed=True)
    negative_weight_graph.add_edge('A', 'B', 4)
    negative_weight_graph.add_edge('A', 'C', 5)
    negative_weight_graph.add_edge('B', 'C', -2)
    negative_weight_graph.add_edge('B', 'D', 3)
    negative_weight_graph.add_edge('C', 'D', 1)
    negative_weight_graph.add_edge('D', 'E', 2)
    
    print("Shortest paths from 'A' (Bellman-Ford):")
    distances, previous, has_negative_cycle = bellman_ford(negative_weight_graph, 'A')
    
    if has_negative_cycle:
        print("Graph contains a negative weight cycle")
    else:
        for vertex in negative_weight_graph.get_vertices():
            path = get_shortest_path(previous, vertex)
            print(f"To {vertex}: Distance = {distances[vertex]}, Path = {path}")
    
    # Test Bellman-Ford with a graph that has a negative cycle
    print("\n=== Graph with Negative Cycle ===")
    negative_cycle_graph = Graph(directed=True)
    negative_cycle_graph.add_edge('A', 'B', 1)
    negative_cycle_graph.add_edge('B', 'C', 2)
    negative_cycle_graph.add_edge('C', 'D', 1)
    negative_cycle_graph.add_edge('D', 'B', -4)  # Creates a negative cycle B->C->D->B
    
    print("Checking for negative cycles:")
    distances, previous, has_negative_cycle = bellman_ford(negative_cycle_graph, 'A')
    print(f"Has negative cycle: {has_negative_cycle}")

if __name__ == "__main__":
    demonstrate_graph_algorithms()
    
    print("\n=== Key Takeaways ===")
    print("1. Graphs can be represented using adjacency lists or matrices")
    print("2. DFS explores as far as possible along each branch before backtracking")
    print("3. BFS explores all neighbors at the present depth before moving to the next level")
    print("4. Topological sort orders vertices such that for every directed edge (u,v), u comes before v")
    print("5. Dijkstra's algorithm finds shortest paths in graphs with non-negative edge weights")
    print("6. Bellman-Ford can handle graphs with negative weights and detect negative cycles")
