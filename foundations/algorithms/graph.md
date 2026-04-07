# Graphs — SDE-2+ Level

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

SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/graphs.py` (BFS/topo/islands) and `../../google-sde2/snippets/python/union_find.py` (DSU).

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
| **[Dijkstra](../../google-sde2/PROBLEM_DETAILS.md#dijkstra)** | Non-negative weights | `O((V+E) log V)` with heap |
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

## 7. Trade-offs & Scaling (optional)

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

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **[Course Schedule](../../google-sde2/PROBLEM_DETAILS.md#course-schedule)** | Build graph: edge `b→a` if **b** before **a**; topo (Kahn/DFS) detects cycle; order = valid semester plan. | **Reverse** graph mistakes; **multiple** components—run from all nodes with indegree calc. |
| **[Network Delay Time](../../google-sde2/PROBLEM_DETAILS.md#network-delay-time)** | **[Dijkstra](../../google-sde2/PROBLEM_DETAILS.md#dijkstra)** from `K`: `dist[u]+w < dist[v]` relax; min-heap by distance. | **Unreachable** nodes stay ∞; **self-loop** / **multi-edge** clarify. |
| **Path With Minimum Effort** | **[Dijkstra](../../google-sde2/PROBLEM_DETAILS.md#dijkstra)** on grid with edge cost = abs height diff; effort = **max** diff on path (minimax). | **State** is min max-diff—not sum of diffs. |
| **[Cheapest Flights Within K Stops](../../google-sde2/PROBLEM_DETAILS.md#cheapest-flights-within-k-stops)** | **Bellman-Ford** k iterations from `src`; or **BFS** level = stops with **state** `(city, stops_used)`. | **Off-by-one:** k stops vs k edges; **negative** prices need BF care. |
| **[Number of Islands](../../google-sde2/PROBLEM_DETAILS.md#number-of-islands)** | DFS/BFS on `1`s; mark visited/`0`. | **8-dir** vs 4; **in-place** marking. |
| **Pacific Atlantic Water Flow** | Multi-source **reverse** flood from both oceans; **intersection**. | Why reverse: avoid repeated climbs from each cell. |
| **Redundant Connection II** | **Directed** graph: case (1) one node indegree 2, (2) no indegree 2 but cycle—remove wrong edge. | Harder than undirected; **root** of tree + cycle. |
| **[Redundant Connection](../../google-sde2/PROBLEM_DETAILS.md#redundant-connection)** | **DSU**: for each edge `u-v`, if `find(u)==find(v)` → redundant; else `union`. | **Undirected**; return **last** edge in problem statement order. |
| **Critical Connections** | **Tarjan**: bridge iff `low[v] > disc[u]` for tree edge `u→v`. | **Back edge** updates `low`; **multiple** edges between same nodes (parallel). |
| **Minimum Cost to Connect All Points** | **MST**: Kruskal on complete graph of Manhattan distances **or** Prim with heap. | **O(n²)** edges—use implicit edges / Prim. |
| **Swim in Rising Water** | **[Dijkstra](../../google-sde2/PROBLEM_DETAILS.md#dijkstra)** / **Union-Find** by sorting cells by height; merge until path exists. | Minimize **max** height along path—same minimax flavor. |

---

## See also

- [Union Find](union-find.md) — DSU for Kruskal and connectivity  
- [data-structures/graphs.md](../data-structures/graphs.md) — extended walkthroughs (BFS problems, Striver-style)  
- [advanced-graphs.md](../../advanced-dsa/advanced-graphs.md) — Tarjan SCC, bridges  
- [patterns/leetcode-patterns.md](../../patterns/leetcode-patterns.md)
