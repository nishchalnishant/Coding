# Graphs — SDE-2+ Level

Vertices and edges; directed/undirected, weighted/unweighted. Senior interviews expect correct representation choice, BFS vs DFS, shortest paths, topological order, and connectivity logic.

---

## 1. Concept Overview

### Algorithm Selection
| Goal | Algorithm | Complexity |
| :--- | :--- | :--- |
| **Shortest Path (Unweighted)** | BFS | O(V + E) |
| **Shortest Path (Non-negative weight)** | Dijkstra | O(E log V) |
| **Negative Cycle Detection** | Bellman-Ford | O(VE) |
| **Connectivity / Components** | DFS / Union-Find | O(V + E) |
| **Dependency Order** | Topological Sort | O(V + E) |
| **Minimum Spanning Tree** | Kruskal / Prim | O(E log E) |

---

## 2. Core Algorithms & Click Moments

### BFS (Breadth-First Search)
> [!IMPORTANT]
> **The Click Moment**: "Shortest path in unweighted graph", "Level-by-level traversal", "Multi-source shortest path (enqueue all 0-dist sources)".

```python
queue = collections.deque([start])
visited = {start}
while queue:
    u = queue.popleft()
    for v in adj[u]:
        if v not in visited:
            visited.add(v)
            queue.append(v)
```

### DFS (Depth-First Search)
> [!IMPORTANT]
> **The Click Moment**: "Find any path", "Connected components", "Cycle detection", "Topological order (reverse post-order)".

```python
def dfs(u, visited):
    visited.add(u)
    for v in adj[u]:
        if v not in visited:
            dfs(v, visited)
```

### Dijkstra's Algorithm
> [!IMPORTANT]
> **The Click Moment**: "Shortest path with weights", "Greedy path finding", "Min-heap of distances".

```python
pq = [(0, start)] # (distance, node)
dist = {start: 0}
while pq:
    d, u = heapq.heappop(pq)
    if d > dist.get(u, float('inf')): continue
    for v, w in adj[u]:
        if d + w < dist.get(v, float('inf')):
            dist[v] = d + w
            heapq.heappush(pq, (dist[v], v))
```

---

## 3. Advanced Patterns

- **Topological Sort (Kahn's)**: Use a queue for nodes with in-degree 0.
- **Union-Find (DSU)**: Path compression + Union by rank/size.
- **Multi-source BFS**: Enqueue all starting points (e.g. all '0's in a grid) at once.

> [!TIP]
> For **Grid Problems** (Islands, Word Ladder), think of each cell as a node and neighbors as edges. Don't always build an adjacency list; just use a `get_neighbors(r, c)` helper.

---

## 4. Common Interview Problems

### Medium
- [Number of Islands](../data-structures/graphs.md#number-of-islands) — Mark visited or sink islands.
- [Course Schedule](../google-sde2/PROBLEM_DETAILS.md#course-schedule) — Topological sort for cycle detection.
- [Rotting Oranges](../google-sde2/PROBLEM_DETAILS.md#rotting-oranges) — Multi-source BFS.

### Hard
- [Word Ladder](../google-sde2/PROBLEM_DETAILS.md#word-ladder) — BFS for shortest transformation.
- [Alien Dictionary](../google-sde2/PROBLEM_DETAILS.md#alien-dictionary) — Build graph from sorted words + Topo sort.
- [Cheapest Flights Within K Stops](../google-sde2/PROBLEM_DETAILS.md#cheapest-flights-within-k-stops) — BFS with stops limit or Bellman-Ford.

---

## 5. Pattern Recognition

- **"Shortest path"** → BFS (unweighted) or Dijkstra (weighted).
- **"Valid order"** → Topological sort.
- **"Cycles"** → Topo sort (directed) or DSU/DFS (undirected).
- **"Connectedness"** → DSU or DFS.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Course Schedule](../../google-sde2/PROBLEM_DETAILS.md#course-schedule)** | "Prerequisites" | Kahn's Topo Sort | Detect **cycle** (all nodes processed?). |
| **[Network Delay Time](../../google-sde2/PROBLEM_DETAILS.md#network-delay-time)** | "Total time" | Dijkstra from src | Unreachable nodes stay ∞. |
| **[Number of Islands](../../google-sde2/PROBLEM_DETAILS.md#number-of-islands)** | "Count components" | DFS on each '1' | In-place marking to save space. |
| **Alien Dictionary** | "Order from sorting" | Compare adjacent words | `abc` before `ab` is **invalid**. |

---

## See also

- [Union Find](union-find.md) — DSU for Kruskal and connectivity  
- [data-structures/graphs.md](../data-structures/graphs.md) — extended walkthroughs  
- [Patterns Master](../../patterns/patterns-master.md)
- [Advanced Graphs](../../advanced-dsa/advanced-graphs.md) — Tarjan SCC, bridges  
- [LeetCode Patterns](../../patterns/leetcode-patterns.md)
