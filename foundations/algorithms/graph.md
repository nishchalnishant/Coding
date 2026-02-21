# Graphs

A data structure consisting of vertices (nodes) and edges (connections). Graphs can be directed/undirected, weighted/unweighted, and cyclic/acyclic.

## Graph Representations
1. **Adjacency List**: Most common. Space $O(V + E)$. Best for sparse graphs.
2. **Adjacency Matrix**: 2D array. Space $O(V^2)$. Best for very dense graphs or when quick edge lookups $O(1)$ are needed.
3. **Edge List**: List of `(u, v, weight)`. Space $O(E)$. Useful for algorithms like Kruskal's or Bellman-Ford.

## Core Traversals
- **BFS (Breadth-First Search)**: Uses a Queue. Explores level-by-level. Ideal for finding the *shortest path* in unweighted graphs. Time $O(V+E)$.
- **DFS (Depth-First Search)**: Uses recursion (Call Stack) or an explicit Stack. Explores as deep as possible. Ideal for cycle detection, connected components, and topological sorting. Time $O(V+E)$.

## Advanced Graph Algorithms
- **Dijkstra's**: Shortest path in graphs with *non-negative* weights. Uses a Min-Heap. Time $O(E \log V)$.
- **Bellman-Ford**: Shortest path in graphs with *negative* weight edges. Detects negative cycles. Time $O(V \times E)$.
- **Floyd-Warshall**: All-pairs shortest path. Time $O(V^3)$.
- **Kruskal's**: Minimum Spanning Tree (MST). Greedily sorts edges by weight and uses Union-Find to avoid cycles. Time $O(E \log E)$.
- **Prim's**: Minimum Spanning Tree (MST). Grows tree from a node using a Min-Heap. Time $O(E \log V)$.
- **Topological Sort**: Linear ordering of a Directed Acyclic Graph (DAG) such that for every directed edge $u \to v$, $u$ comes before $v$. Kahn's Algorithm (In-degree BFS) or DFS.
- **Disjoint Set Union (Union-Find)**: Tracks connected components. Uses path compression and union by rank. Time $\approx O(1)$ per operation.

## Common SDE-3 Graph Problems
- *Easy*: Flood Fill, Find Center of Star Graph, Find the Town Judge.
- *Medium*: Number of Islands, Rotting Oranges (Multi-source BFS), Course Schedule (Topo Sort), Clone Graph, Minimum Height Trees.
- *Hard*: Word Ladder, Cheapest Flights Within K Stops (Dijkstra/Bellman-Ford), Alien Dictionary (Topo Sort), Swim in Rising Water.
