# Day 19: Advanced Graph Problems

Here are detailed notes for **Day 19: Advanced Graph Problems**. This day focuses on solving more complex problems involving graphs, such as topological sorting and strongly connected components.

***

#### 1. **Graph Basics Recap**

Before diving into advanced problems, let's briefly recap key graph concepts:

**1.1 Graph Representations**

* **Adjacency Matrix**: A 2D array where `matrix[i][j]` is `1` if there is an edge from vertex `i` to vertex `j`, otherwise `0`.
* **Adjacency List**: An array of lists where each list at index `i` contains all the vertices adjacent to vertex `i`.

**1.2 Graph Traversal Algorithms**

* **Depth-First Search (DFS)**: Explores as far as possible along a branch before backtracking.
* **Breadth-First Search (BFS)**: Explores all neighbors at the present depth before moving on to nodes at the next depth level.

#### 2. **Topological Sorting**

**2.1 Definition**

Topological sorting of a directed acyclic graph (DAG) is a linear ordering of its vertices such that for every directed edge ( u \to v ), vertex ( u ) comes before ( v ) in the ordering.

**2.2 Properties**

* Only possible for directed acyclic graphs (DAGs).
* Can have multiple valid topological sorts.

**2.3 Algorithms for Topological Sorting**

1. **Kahn's Algorithm (BFS-based)**:
   * Count the in-degrees of all vertices.
   * Start with vertices that have an in-degree of 0.
   * For each vertex, remove it from the graph and decrease the in-degree of its neighbors. If any neighbor's in-degree becomes 0, add it to the queue.
2. **DFS-based Approach**:
   * Perform a DFS traversal.
   * After visiting a vertex, add it to a stack.
   * Once all vertices are processed, pop vertices from the stack to get the topological ordering.

**2.4 Implementation Example (DFS-based)**

```python
def topological_sort_dfs(graph):
    visited = set()
    stack = []

    def dfs(v):
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(v)

    for vertex in graph:
        if vertex not in visited:
            dfs(vertex)

    return stack[::-1]  # Return reversed stack

# Example Usage
graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}
print(topological_sort_dfs(graph))  # Output: ['A', 'B', 'C', 'D']
```

#### 3. **Strongly Connected Components (SCC)**

**3.1 Definition**

A strongly connected component of a directed graph is a maximal subgraph where every vertex is reachable from every other vertex in the subgraph.

**3.2 Algorithms to Find SCCs**

1. **Kosaraju’s Algorithm**:
   * Perform a DFS on the original graph to determine the finishing order of vertices.
   * Reverse the graph.
   * Perform DFS on the reversed graph in the order of decreasing finishing times.
2. **Tarjan’s Algorithm**:
   * Uses a single DFS traversal and a stack to keep track of visited nodes and their discovery times.

**3.3 Implementation Example (Kosaraju’s Algorithm)**

```python
def kosaraju_scc(graph):
    # Step 1: Perform DFS to determine the finishing order
    visited = set()
    stack = []

    def dfs(v):
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(v)

    for vertex in graph:
        if vertex not in visited:
            dfs(vertex)

    # Step 2: Reverse the graph
    reversed_graph = {v: [] for v in graph}
    for v in graph:
        for neighbor in graph[v]:
            reversed_graph[neighbor].append(v)

    # Step 3: Perform DFS on reversed graph
    visited.clear()
    sccs = []

    def dfs_reversed(v, component):
        visited.add(v)
        component.append(v)
        for neighbor in reversed_graph[v]:
            if neighbor not in visited:
                dfs_reversed(neighbor, component)

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            component = []
            dfs_reversed(vertex, component)
            sccs.append(component)

    return sccs

# Example Usage
graph = {
    'A': ['B'],
    'B': ['C'],
    'C': ['A', 'D'],
    'D': []
}
print(kosaraju_scc(graph))  # Output: [['D'], ['A', 'B', 'C']]
```

#### 4. **Common Advanced Graph Problems**

1. **Finding Bridges in a Graph**: Use DFS to identify edges that, if removed, would increase the number of connected components.
2. **Finding Articulation Points**: Identify vertices whose removal increases the number of connected components in a graph.
3. **Minimum Spanning Tree**: Implement algorithms like Prim’s or Kruskal’s to find the minimum spanning tree in a weighted graph.

#### 5. **Practice Problems**

1. **Course Schedule**: Given a list of prerequisites, determine if you can finish all courses.
2. **Clone Graph**: Clone an undirected graph given a reference to a node.
3. **Number of Islands**: Given a grid of `1`s (land) and `0`s (water), count the number of islands.

#### 6. **Tips for Mastering Advanced Graph Problems**

* **Understand Graph Theory**: Familiarize yourself with key concepts and terminology in graph theory.
* **Practice Different Algorithms**: Implement various algorithms for graph traversal, shortest path, and connected components.
* **Visualize Graphs**: Drawing graphs can help you understand the relationships and properties of vertices and edges.

By mastering advanced graph problems and their algorithms, you'll significantly improve your problem-solving skills, which will be invaluable in coding interviews and competitive programming.
