# Day 10: Graph Basics.

Here are detailed notes for **Day 10: Graph Basics**. This day focuses on understanding graph representations and basic traversal techniques, particularly Depth-First Search (DFS) and Breadth-First Search (BFS).

***

#### 1. **What is a Graph?**

A **graph** is a data structure that consists of a set of **vertices** (or nodes) and a set of **edges** that connect pairs of vertices. Graphs can represent various real-world problems, such as social networks, transportation systems, and web page links.

**Types of Graphs**:

* **Directed Graph**: Edges have a direction; they go from one vertex to another.
* **Undirected Graph**: Edges have no direction; the connection is mutual.
* **Weighted Graph**: Edges have weights (costs) associated with them.
* **Unweighted Graph**: All edges are considered equal.
* **Cyclic Graph**: Contains cycles (a path where the first and last vertices are the same).
* **Acyclic Graph**: Contains no cycles.

***

#### 2. **Graph Representations**

Graphs can be represented in multiple ways. The two most common representations are:

**2.1 Adjacency Matrix**

* A 2D array (matrix) where each cell (i, j) indicates the presence or absence of an edge between vertex (i) and vertex (j).
* Space Complexity: (O(V^2)) where (V) is the number of vertices.
* Useful for dense graphs.

**Example**:

```python
# Adjacency Matrix Representation
graph = [
    [0, 1, 0, 0],
    [1, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 0]
]
```

**2.2 Adjacency List**

* An array (or list) of lists. Each index represents a vertex and contains a list of adjacent vertices (neighbors).
* Space Complexity: (O(V + E)) where (E) is the number of edges.
* More efficient for sparse graphs.

**Example**:

```python
# Adjacency List Representation
graph = {
    0: [1],
    1: [0, 2, 3],
    2: [1],
    3: [1]
}
```

***

#### 3. **Graph Traversal Techniques**

Graph traversal is the process of visiting all the nodes in a graph. The two primary methods of graph traversal are **Depth-First Search (DFS)** and **Breadth-First Search (BFS)**.

**3.1 Depth-First Search (DFS)**

DFS explores as far as possible along each branch before backtracking. It can be implemented using recursion or an explicit stack.

**Recursive Implementation**:

```python
def dfs(graph, vertex, visited):
    if vertex not in visited:
        print(vertex)
        visited.add(vertex)
        for neighbor in graph[vertex]:
            dfs(graph, neighbor, visited)

# Usage
visited = set()
dfs(graph, 0, visited)
```

**Iterative Implementation using Stack**:

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            print(vertex)
            visited.add(vertex)
            stack.extend(neighbor for neighbor in graph[vertex] if neighbor not in visited)

# Usage
dfs_iterative(graph, 0)
```

***

**3.2 Breadth-First Search (BFS)**

BFS explores all neighbors at the present depth before moving on to nodes at the next depth level. It is implemented using a queue.

**Implementation using Queue**:

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            print(vertex)
            visited.add(vertex)
            queue.extend(neighbor for neighbor in graph[vertex] if neighbor not in visited)

# Usage
bfs(graph, 0)
```

***

#### 4. **Time Complexity of Traversal**

* **DFS**: O(V + E), where (V) is the number of vertices and (E) is the number of edges.
* **BFS**: O(V + E).

***

#### 5. **Applications of Graph Traversal**

Graph traversal techniques are fundamental for various applications:

* **Finding connected components** in a graph.
* **Topological sorting** in directed acyclic graphs (DAGs).
* **Finding shortest paths** using BFS in unweighted graphs.
* **Cycle detection** in graphs.
* **Solving puzzles** (e.g., finding paths in mazes).

***

#### 6. **Recommended Practice Problems**

1. **LeetCode**:
   * Number of Islands (using DFS/BFS)
   * Course Schedule (Topological Sort)
   * Clone Graph
   * Minimum Depth of Binary Tree (BFS)
2. **HackerRank**:
   * Breadth First Search: Shortest Reach
   * DFS: Connected Cell in a Grid

***

#### 7. **Key Concepts to Remember**

* Understanding different graph representations helps in choosing the right one based on the problem context (sparse vs. dense).
* Mastering DFS and BFS traversal techniques is crucial for solving graph-related problems efficiently.
* Recognizing when to use recursion versus iteration can help in optimizing memory usage and performance.

By mastering graph basics, representations, and traversal techniques, you'll be well-prepared for solving complex graph problems in coding interviews.
