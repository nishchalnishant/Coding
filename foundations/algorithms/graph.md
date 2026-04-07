# Graphs — SDE-3 Level

Vertices and edges; directed/undirected, weighted/unweighted. Senior interviews expect correct representation choice, BFS vs DFS, shortest paths (BFS / Dijkstra / Bellman-Ford), topological order, MST, and Union-Find for connectivity.

---

## 1. Concept Overview

**Problem space:** Shortest paths, connectivity, ordering (dependencies), MST, grid as implicit graph, clone graph, word ladder.

**When to use what:**

| Question | Algorithm |
|----------|-----------|
| Shortest path, unweighted | BFS |
| Shortest path, non-negative weights | Dijkstra (min-heap) |
| Negative weights / detect negative cycle | Bellman-Ford |
| All-pairs shortest paths (small V) | Floyd–Warshall |
| Dependencies / valid order | Topological sort (DAG only) |
| Connect all nodes, min edge weight | Kruskal or Prim (MST) |
| Dynamic connectivity / Kruskal | Union-Find |

---

## 2. Graph Representations

1. **Adjacency list** — `O(V + E)` space; default for sparse graphs.
2. **Adjacency matrix** — `O(V²)`; dense graphs or `O(1)` edge lookup.
3. **Edge list** — `O(E)`; Kruskal, Bellman-Ford.

---

## 3. Core Traversals

### BFS (queue)
```
queue = [start]; visited = {start}
while queue:
  u = queue.pop(0)
  for v in adj[u]:
    if v not in visited:
      visited.add(v); queue.append(v)
```
- **Unweighted shortest path:** first time you reach `t` gives minimum edges.
- **Multi-source:** enqueue all sources at distance 0 (e.g. Rotting Oranges).

**Time:** `O(V + E)`; **Space:** `O(V)`.

### DFS (recursion or stack)
```
def dfs(u, visited):
  visited.add(u)
  for v in adj[u]:
    if v not in visited: dfs(v, visited)
```
- **Use for:** connected components, cycle (with parent/color), topological sort (post-order stack, then reverse).

**Time:** `O(V + E)`; **Space:** `O(V)` recursion stack.

### Topological sort (DAG)
- **Kahn:** in-degree 0 in queue; pop, decrement neighbors; if cycle, not all nodes processed.
- **DFS:** post-order on finish, reverse list.

---

## 4. Advanced Graph Algorithms

| Algorithm | When | Time |
|-----------|------|------|
| **Dijkstra** | Non-negative weights | `O((V+E) log V)` with heap |
| **Bellman–Ford** | Negative edges; detect negative cycle | `O(V·E)` |
| **Floyd–Warshall** | All pairs, small `V` | `O(V³)` |
| **Kruskal** | MST | Sort edges `O(E log E)` + DSU |
| **Prim** | MST | `O(E log V)` with heap |
| **Union–Find** | Connectivity, Kruskal | ~`O(1)` amortized per op |

**Dijkstra sketch:** `dist[s]=0`; heap `(0,s)`; pop min; if `d > dist[u]` skip; relax `v`: if `d+w < dist[v]`, update and push.

---

## 5. Common SDE-3 Graph Problems

**Easy:** Flood Fill, Find Center of Star Graph, Town Judge.  
**Medium:** Number of Islands, Rotting Oranges, Course Schedule, Clone Graph, Minimum Height Trees.  
**Hard:** Word Ladder, Cheapest Flights Within K Stops, Alien Dictionary, Swim in Rising Water.

---

## 6. Pattern Recognition

- **BFS shortest path:** Unweighted; level = distance. Multi-source: enqueue all.
- **DFS:** Components, cycle detection, topo (post-order), grid backtrack.
- **Topological sort:** Dependencies, “order of tasks”, Alien Dictionary.
- **Shortest path:** Non-negative → Dijkstra; negative → Bellman–Ford; unweighted → BFS.
- **MST:** Kruskal (sort + DSU); Prim (heap).

---

## 7. SDE-3 Level Thinking

- **Trade-offs:** List vs matrix (space vs edge lookup). BFS for unweighted shortest path. Dijkstra vs Bellman–Ford for negative edges.
- **Scalability:** Adjacency list for sparse graphs; for huge graphs consider bidirectional BFS (meet in middle) when applicable.

---

## 8. Interview Strategy

- **Identify:** “Shortest path” → BFS or Dijkstra. “Order” / “before” → topo. “Connected” → DFS or DSU. “MST” → Kruskal/Prim.
- **Common mistakes:** Forgetting visited; Dijkstra with negative weights; topo only on DAG (detect cycle first).

---

## 9. Quick Revision

- **Formulas:** Dijkstra: extract min, relax. Kruskal: sort edges, add if union. Topo: in-degree 0 queue or DFS post-order reverse.
- **Tricks:** Multi-source BFS = enqueue all sources. 0–1 BFS = deque (0 front, 1 back).
- **Edge cases:** Disconnected, negative cycle, single node.
- **Pattern tip:** “Shortest” unweighted → BFS; weighted → Dijkstra/Bellman–Ford; “order” → topo.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness |
|----------|------------|------------|
| **Course Schedule** | Topo; detect cycle | Prerequisite edge direction |
| **Network Delay Time** | Dijkstra from K | Unreachable → infinity |
| **Cheapest Flights K Stops** | Bellman k rounds or state `(node,stops)` | Off-by-one on stops |
| **Number of Islands** | Flood fill | Visited vs mutate grid |
| **Pacific Atlantic Water Flow** | Multi-source from oceans | Reverse: flow from ocean inward |
| **Redundant Connection** | DSU; first cycle edge | Undirected |
| **Critical Connections** | Tarjan bridges | `low[v] > disc[u]` |

---

## See also

- [Union Find](union-find.md) — DSU for Kruskal and connectivity  
- [data-structures/graphs.md](../data-structures/graphs.md) — extended walkthroughs (BFS problems, Striver-style)  
- [advanced-graphs.md](../../advanced-dsa/advanced-graphs.md) — Tarjan SCC, bridges  
- [patterns/leetcode-patterns.md](../../patterns/leetcode-patterns.md)
