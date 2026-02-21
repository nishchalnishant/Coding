# Graph

#### Graphs: Detailed Summary

Graphs are a fundamental data structure used to model relationships between pairs of objects. They consist of vertices (or nodes) and edges (connections between the vertices). Graphs can be directed or undirected, weighted or unweighted, and cyclic or acyclic. Understanding graph theory and algorithms is essential for solving many real-world problems, including network routing, social network analysis, and resource allocation.

***

#### Key Concepts in Graph Theory:

1. **Graph Representation**:
   * **Adjacency Matrix**: A 2D array where the cell at row (i) and column (j) indicates the presence (1) or absence (0) of an edge between vertices (i) and (j). Suitable for dense graphs.

```python
class GraphAdjacencyMatrix:
    def __init__(self, vertices):
        self.V = vertices
        self.matrix = [[0] * vertices for _ in range(vertices)]

    def add_edge(self, u, v, weight=1):
        self.matrix[u][v] = weight
        self.matrix[v][u] = weight  # Uncomment this for an undirected graph.

    def display(self):
        print("Adjacency Matrix:")
        for row in self.matrix:
            print(row)

# Example
g = GraphAdjacencyMatrix(4)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 2)
g.add_edge(1, 3)
g.display()
```

1.
   * **Adjacency List**: An array of lists where each list corresponds to a vertex and contains the list of adjacent vertices. More space-efficient for sparse graphs.

```python
class GraphAdjacencyList:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_list = {i: [] for i in range(vertices)}

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)  # Uncomment this for an undirected graph.

    def display(self):
        print("Adjacency List:")
        for vertex, neighbors in self.adj_list.items():
            print(f"{vertex}: {neighbors}")

# Example
g = GraphAdjacencyList(4)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 2)
g.add_edge(1, 3)
g.display()
```



1.
   * E**dge List**: A list of edges represented as pairs (or tuples) of vertices.

```python
class GraphEdgeList:
    def __init__(self):
        self.edges = []

    def add_edge(self, u, v, weight=1):
        self.edges.append((u, v, weight))

    def display(self):
        print("Edge List:")
        for u, v, weight in self.edges:
            print(f"({u}, {v}) -> Weight: {weight}")

# Example
g = GraphEdgeList()
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 2)
g.add_edge(1, 3)
g.display()
```



| Representation   | Memory complexity | Best for            |
| ---------------- | ----------------- | ------------------- |
| Adjecency Matrix | O(V^2)            | Dense graphs        |
| Adjecency List   | O(V+E)            | Sparse graphs       |
| Edge List        | O(E)              | Edge centric graphs |

1. **Types of Graphs**:
   * **Directed Graph**: Edges have a direction, indicating a one-way relationship.
   * **Undirected Graph**: Edges have no direction; the relationship is two-way.
   * **Weighted Graph**: Edges have weights (costs), representing distances, costs, or capacities.
   * **Unweighted Graph**: All edges are treated equally, without weights.
   * **Cyclic Graph**: Contains at least one cycle (a path that starts and ends at the same vertex).
   * **Acyclic Graph**: Contains no cycles; a tree is a special case of an acyclic graph.
2. **Graph Traversal Algorithms**:
   * **Depth-First Search (DFS)**: Explores as far as possible along each branch before backtracking. Can be implemented using recursion or an explicit stack.

```python
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_list = {i: [] for i in range(vertices)}

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)  # For an undirected graph.

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start, end=" ")  # Process the current node

        for neighbor in self.adj_list[start]:
            if neighbor not in visited:
                self.dfs(neighbor, visited)

    def display(self):
        print("Graph (Adjacency List):")
        for vertex, neighbors in self.adj_list.items():
            print(f"{vertex}: {neighbors}")

# Example Usage
g = Graph(5)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(2, 4)

print("Depth First Search starting from node 0:")
g.dfs(0)
```

1.
   * **Breadth-First Search (BFS)**: Explores all neighbors of a vertex before moving on to their neighbors. Typically implemented using a queue.

```python
from collections import deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_list = {i: [] for i in range(vertices)}

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)  # For an undirected graph.

    def bfs(self, start):
        visited = set()
        queue = deque([start])  # Initialize the queue with the starting node
        visited.add(start)

        print("Breadth First Search:")
        while queue:
            node = queue.popleft()
            print(node, end=" ")  # Process the current node

            for neighbor in self.adj_list[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

    def display(self):
        print("Graph (Adjacency List):")
        for vertex, neighbors in self.adj_list.items():
            print(f"{vertex}: {neighbors}")

# Example Usage
g = Graph(5)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(2, 4)

print("Breadth First Search starting from node 0:")
g.bfs(0)
```

1. **Shortest Path Algorithms**:
   * **Dijkstra’s Algorithm**: Finds the shortest path from a source vertex to all other vertices in a weighted graph with non-negative weights.

```python
import heapq

class GraphDijkstra:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_list = {i: [] for i in range(vertices)}

    def add_edge(self, u, v, weight):
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))  # For undirected graph.

    def dijkstra(self, src):
        distances = [float('inf')] * self.V
        distances[src] = 0

        priority_queue = [(0, src)]  # (distance, node)
        visited = set()

        while priority_queue:
            current_distance, u = heapq.heappop(priority_queue)

            if u in visited:
                continue
            visited.add(u)

            for neighbor, weight in self.adj_list[u]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        print("Shortest distances from source node", src)
        for i, dist in enumerate(distances):
            print(f"Node {i}: {dist}")

# Example Usage
g = GraphDijkstra(5)
g.add_edge(0, 1, 2)
g.add_edge(0, 2, 4)
g.add_edge(1, 2, 1)
g.add_edge(1, 3, 7)
g.add_edge(2, 4, 3)
g.add_edge(3, 4, 1)

g.dijkstra(0)
```

1.
   * **Bellman-Ford Algorithm**: Computes shortest paths from a single source vertex, capable of handling graphs with negative weights.

```python
class GraphBellmanFord:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []

    def add_edge(self, u, v, weight):
        self.edges.append((u, v, weight))

    def bellman_ford(self, src):
        distances = [float('inf')] * self.V
        distances[src] = 0

        # Relax edges |V| - 1 times
        for _ in range(self.V - 1):
            for u, v, weight in self.edges:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

        # Check for negative weight cycle
        for u, v, weight in self.edges:
            if distances[u] + weight < distances[v]:
                print("Graph contains a negative weight cycle!")
                return

        print("Shortest distances from source node", src)
        for i, dist in enumerate(distances):
            print(f"Node {i}: {dist}")

# Example Usage
g = GraphBellmanFord(5)
g.add_edge(0, 1, -1)
g.add_edge(0, 2, 4)
g.add_edge(1, 2, 3)
g.add_edge(1, 3, 2)
g.add_edge(1, 4, 2)
g.add_edge(3, 2, 5)
g.add_edge(3, 1, 1)
g.add_edge(4, 3, -3)

g.bellman_ford(0)
```

1.
   * **Floyd-Warshall Algorithm**: Finds shortest paths between all pairs of vertices, suitable for dense graphs.

```python
class GraphFloydWarshall:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[float('inf')] * vertices for _ in range(vertices)]
        for i in range(vertices):
            self.graph[i][i] = 0

    def add_edge(self, u, v, weight):
        self.graph[u][v] = weight  # Directed graph

    def floyd_warshall(self):
        dist = [row[:] for row in self.graph]  # Copy the graph matrix

        for k in range(self.V):
            for i in range(self.V):
                for j in range(self.V):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        print("Shortest distances between every pair of vertices:")
        for row in dist:
            print(" ".join(f"{cell:7}" if cell != float('inf') else "   INF" for cell in row))

# Example Usage
g = GraphFloydWarshall(4)
g.add_edge(0, 1, 5)
g.add_edge(0, 3, 10)
g.add_edge(1, 2, 3)
g.add_edge(2, 3, 1)

g.floyd_warshall()

```



| Algorithm      | Use case                                | Time complexity   |
| -------------- | --------------------------------------- | ----------------- |
| Dijkstra       | Single source, non-negative weights     | O((V + E) \log V) |
| Bellman-Ford   | Single source, handles negative weights | O(V . E)          |
| Floyd-Warshall | All pairs, handles negative weights     | O(V^3)            |

1. **Minimum Spanning Tree (MST)**:
   * A subgraph that connects all vertices with the minimum possible total edge weight. Common algorithms:
     * **Kruskal’s Algorithm**: Builds the MST by adding edges in order of increasing weight and ensuring no cycles are formed.

```python
class DisjointSet:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1


class GraphKruskal:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []

    def add_edge(self, u, v, weight):
        self.edges.append((weight, u, v))  # Edge: (weight, vertex1, vertex2)

    def kruskal_mst(self):
        mst = []
        self.edges.sort()  # Sort edges by weight
        dsu = DisjointSet(range(self.V))

        for weight, u, v in self.edges:
            if dsu.find(u) != dsu.find(v):  # Check for cycle
                dsu.union(u, v)
                mst.append((u, v, weight))

        print("Edges in the Minimum Spanning Tree (Kruskal's Algorithm):")
        for u, v, weight in mst:
            print(f"{u} -- {v} == {weight}")


# Example Usage
g = GraphKruskal(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 6)
g.add_edge(0, 3, 5)
g.add_edge(1, 3, 15)
g.add_edge(2, 3, 4)

g.kruskal_mst()
```

*
  * **Prim’s Algorithm**: Starts from a vertex and grows the MST by adding the cheapest edge from the existing tree.

```python
import heapq

class GraphPrims:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_list = {i: [] for i in range(vertices)}

    def add_edge(self, u, v, weight):
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))  # Undirected graph

    def prims_mst(self):
        visited = [False] * self.V
        min_heap = [(0, 0)]  # (weight, vertex)
        mst_cost = 0
        mst_edges = []

        while min_heap:
            weight, u = heapq.heappop(min_heap)
            if visited[u]:
                continue
            visited[u] = True
            mst_cost += weight

            for v, w in self.adj_list[u]:
                if not visited[v]:
                    heapq.heappush(min_heap, (w, v))
                    mst_edges.append((u, v, w))

        print("Edges in the Minimum Spanning Tree (Prim's Algorithm):")
        for u, v, weight in mst_edges:
            print(f"{u} -- {v} == {weight}")
        print(f"Total cost of MST: {mst_cost}")


# Example Usage
g = GraphPrims(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 6)
g.add_edge(0, 3, 5)
g.add_edge(1, 3, 15)
g.add_edge(2, 3, 4)

g.prims_mst()
```

1. **Topological Sorting**:
   * A linear ordering of vertices in a directed acyclic graph (DAG) such that for every directed edge (uv) from vertex (u) to vertex (v), (u) comes before (v) in the ordering. Can be implemented using DFS or Kahn's algorithm.
2. **Graph Cycle Detection**:
   * **Directed Graph**: Use DFS and keep track of visited nodes and recursion stack to detect cycles.
   * **Undirected Graph**: Use DFS or BFS and check for back edges.
3. **Connected Components**:
   * A subgraph in which any two vertices are connected to each other by paths. Can be found using DFS or BFS.
4. **Graph Coloring**:
   * Assign colors to vertices such that no two adjacent vertices share the same color. Used in scheduling problems and register allocation in compilers.
5. **Network Flow**:
   * Models flow in a network with capacities on edges. **Ford-Fulkerson** method is commonly used to find the maximum flow in a flow network.

***

#### Important Questions Related to Graphs:

1. **Graph Traversal**:
   * Implement DFS and BFS for a given graph.
   * **Example**: Given a graph, print the nodes in DFS and BFS order starting from a specified vertex.
2. **Shortest Path Problems**:
   * Given a weighted graph, find the shortest path from a source vertex to all other vertices using Dijkstra's algorithm.
   * **Example**: Input a graph and a source vertex, output the shortest distances to all other vertices.
   * Solve the Single Source Shortest Path problem using the Bellman-Ford algorithm.
3. **Minimum Spanning Tree**:
   * Implement Kruskal’s and Prim’s algorithms to find the MST of a given weighted graph.
   * **Example**: Given a graph, output the edges included in the MST along with their total weight.
4. **Topological Sorting**:
   * Given a directed acyclic graph (DAG), perform a topological sort.
   * **Example**: Input a DAG and output a valid topological ordering of the vertices.
5. **Cycle Detection**:
   * Determine if a directed or undirected graph contains cycles.
   * **Example**: Given a directed graph, check for cycles using DFS.
6. **Connected Components**:
   * Find all connected components in an undirected graph.
   * **Example**: Input a graph and output the connected components.
7. **Graph Coloring**:
   * Implement a graph coloring algorithm to determine if a given graph can be colored with (k) colors.
   * **Example**: Input a graph and (k), output whether it can be colored with (k) colors.
8. **Network Flow**:
   * Solve the maximum flow problem using the Ford-Fulkerson method.
   * **Example**: Given a flow network, find the maximum flow from the source to the sink.
9. **Finding Bridges and Articulation Points**:
   * Implement algorithms to find bridges (edges whose removal increases the number of connected components) and articulation points (vertices whose removal increases the number of connected components) in a graph.
   * **Example**: Input a graph and output the bridges and articulation points.
10. **Eulerian Path and Circuit**:
    * Determine if an Eulerian path or circuit exists in a given graph and find it if it does.
    * **Example**: Given a graph, determine if it has an Eulerian path or circuit and print it.

***

#### Conclusion

Graphs are an essential structure in computer science, and mastering their properties and algorithms is crucial for solving a wide range of problems. From traversing a graph to finding shortest paths, minimum spanning trees, and understanding complex relationships, the concepts in graph theory provide powerful tools for algorithm design and analysis. Proficiency in graph algorithms can greatly enhance your problem-solving capabilities in competitive programming and software development.





Here are some tips and tricks for mastering graph algorithms in software engineering interviews:

#### 1. **Understand Graph Basics**

* Familiarize yourself with basic graph terminology, such as vertices (nodes), edges (connections), directed vs. undirected graphs, weighted vs. unweighted graphs, and cycles.
* Understand the representation of graphs: adjacency list, adjacency matrix, and edge list.

#### 2. **Common Graph Traversal Algorithms**

* **Depth-First Search (DFS)**:
  * Use a stack (or recursion) to explore as far as possible along each branch before backtracking.
  * Useful for tasks like topological sorting, finding connected components, and solving puzzles like mazes.
* **Breadth-First Search (BFS)**:
  * Use a queue to explore all neighbors at the present depth prior to moving on to nodes at the next depth level.
  * Useful for finding the shortest path in unweighted graphs and checking bipartiteness.

#### 3. **Shortest Path Algorithms**

* **Dijkstra’s Algorithm**: Efficiently finds the shortest path from a single source to all other nodes in a weighted graph with non-negative weights.
* **Bellman-Ford Algorithm**: Handles graphs with negative weights and detects negative cycles.
* **Floyd-Warshall Algorithm**: Computes shortest paths between all pairs of vertices.

#### 4. **Minimum Spanning Tree (MST) Algorithms**

* **Prim’s Algorithm**: Grows the MST from a starting vertex, adding edges with the smallest weights that connect to the tree.
* **Kruskal’s Algorithm**: Sorts all edges and adds them one by one, ensuring no cycles are formed using a union-find data structure.

#### 5. **Graph Representations**

* Choose the appropriate representation based on the problem. Adjacency lists are generally more space-efficient, especially for sparse graphs, while adjacency matrices can be easier for certain operations in dense graphs.
* Be prepared to convert between representations if necessary.

#### 6. **Cycle Detection**

* Use DFS to detect cycles in directed graphs by tracking visited nodes and recursion stack.
* For undirected graphs, use BFS or DFS to check if a back edge exists.

#### 7. **Topological Sorting**

* Use DFS to perform topological sorting in directed acyclic graphs (DAGs). The result can be obtained by pushing nodes onto a stack after all their neighbors have been visited.
* Alternatively, use Kahn’s algorithm, which involves in-degree counting and processing nodes with zero in-degrees.

#### 8. **Connected Components**

* Use DFS or BFS to find all connected components in an undirected graph.
* Each time you initiate a traversal from an unvisited node, you discover a new connected component.

#### 9. **Graph Algorithms Practice**

* Regularly practice common graph algorithms on platforms like LeetCode, HackerRank, and CodeSignal. Focus on a variety of problems, such as:
  * Finding shortest paths.
  * Detecting cycles.
  * Performing traversals.
  * Solving connectivity problems.

#### 10. **Time and Space Complexity**

* Analyze the time and space complexity of the graph algorithms you implement. For example:
  * BFS and DFS typically run in O(V + E) time, where V is the number of vertices and E is the number of edges.
  * Dijkstra’s algorithm runs in O((V + E) log V) with a priority queue.

#### 11. **Debugging Techniques**

* If your graph algorithm isn’t producing the expected results, use print statements to trace the values of variables and the traversal paths.
* Validate your approach with small graphs to ensure correctness.

#### 12. **Edge Cases and Constraints**

* Consider edge cases, such as graphs with no edges, graphs with only one vertex, or graphs that are fully connected.

#### 13. **Communicate Your Thought Process**

* Clearly articulate your approach during interviews, especially the choice of algorithm and data structures.
* Explain how you would handle edge cases and what assumptions you’re making.

#### 14. **Refine Your Solution**

* After arriving at a solution, take time to review it for possible optimizations or clearer implementations.
* Discuss how you could improve the efficiency or clarity of your graph algorithm.

#### 15. **Key Takeaways for Interviews**

* Be prepared to explain the rationale behind your choice of algorithm for a specific problem.
* If you encounter difficulties, talk through your thought process and consider alternative approaches.

By mastering these principles and practicing various graph problems, you'll be well-prepared for relevant questions in your software engineering interviews. If you want to explore specific graph problems or concepts, feel free to ask!
