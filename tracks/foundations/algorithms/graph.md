# Graphs (Algorithms) — SDE-3 Gold Standard

Vertices and edges; directed/undirected, weighted/unweighted. SDE-3 expects: correct algorithm selection, Dijkstra implementation with lazy deletion guard, Bellman-Ford for negative weights, and distributed graph thinking.

---

## 1. Algorithm Selection

| Goal | Algorithm | Complexity |
| :--- | :--- | :--- |
| **Shortest path (unweighted)** | BFS | O(V + E) |
| **Shortest path (non-negative weights)** | Dijkstra | O(E log V) |
| **Shortest path (negative weights, no negative cycle)** | Bellman-Ford | O(VE) |
| **All-pairs shortest path** | Floyd-Warshall | O(V³) |
| **0/1 weight edges** | 0-1 BFS (deque) | O(V + E) |
| **Topological order** | Kahn's (BFS) or DFS postorder | O(V + E) |
| **Connected components** | DFS / Union-Find | O(V + E) |
| **Minimum spanning tree** | Kruskal (sort edges + DSU) / Prim (heap) | O(E log E) |

---

## 2. Core Algorithms & Click Moments

### BFS — Unweighted Shortest Path

> [!IMPORTANT]
> **The Click Moment**: "**Minimum steps/moves** to transform X to Y" — OR — "**minimum hops** in a graph" — OR — "**multi-source** spread (all sources at distance 0)". BFS guarantees the first time you reach a node is the shortest path. For weighted graphs, this guarantee breaks — use Dijkstra.

```python
from collections import deque, defaultdict

def bfs(adj: dict, start: int, target: int) -> int:
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        if u == target:
            return dist[u]
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return -1  # unreachable
```

---

### DFS — Connectivity, Cycle Detection, Topological Order

> [!IMPORTANT]
> **The Click Moment**: "Count **connected components**" — OR — "detect **cycle in directed graph**" — OR — "**topological order** via DFS postorder". For directed graphs, DFS uses 3-color marking (white/gray/black): a back edge (gray→gray) = cycle.

```python
def dfs_topo(adj: dict, n: int) -> list[int]:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    topo = []
    has_cycle = [False]

    def dfs(u: int) -> None:
        if has_cycle[0]:
            return
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                has_cycle[0] = True
                return
            if color[v] == WHITE:
                dfs(v)
        color[u] = BLACK
        topo.append(u)  # postorder

    for u in range(n):
        if color[u] == WHITE:
            dfs(u)

    return [] if has_cycle[0] else topo[::-1]
```

> [!CAUTION]
> **For large graphs**, recursive DFS overflows Python's stack. Convert to iterative DFS using an explicit stack. Alternatively, use Kahn's algorithm (BFS-based topo sort) — it naturally handles large graphs and detects cycles via the unprocessed node count.

---

### Dijkstra — Non-Negative Weighted Shortest Path

> [!IMPORTANT]
> **The Click Moment**: "**Shortest path with edge weights**" — AND — "all weights are **non-negative**". The lazy deletion guard (`if d > dist[u]: continue`) is mandatory — without it, stale heap entries cause incorrect updates and silent bugs.

```python
import heapq

def dijkstra(adj: dict, n: int, start: int) -> list[float]:
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]  # (distance, node)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # stale entry — lazy deletion
        for v, weight in adj[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(heap, (dist[v], v))
    return dist
```

> [!CAUTION]
> Dijkstra **fails with negative weights** — a later-discovered shorter path via a negative edge can undercut an already-finalized node. Use Bellman-Ford for graphs with negative weights. Dijkstra with negative weights produces silently wrong results (not an error).

---

### Bellman-Ford — Negative Weights & Negative Cycle Detection

> [!IMPORTANT]
> **The Click Moment**: "Graph with **negative edge weights**" — OR — "detect a **negative cycle**" — OR — "find shortest path in directed graph where Dijkstra is disallowed". Relax all edges V-1 times; if a V-th relaxation still improves a distance, a negative cycle exists.

```python
def bellman_ford(edges: list[tuple[int,int,int]], n: int, start: int) -> tuple[list[float], bool]:
    dist = [float('inf')] * n
    dist[start] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # Detect negative cycle: if any edge still relaxes, there's a negative cycle
    has_negative_cycle = any(
        dist[u] != float('inf') and dist[u] + w < dist[v]
        for u, v, w in edges
    )
    return dist, has_negative_cycle
```

---

### Topological Sort — Kahn's Algorithm

> [!IMPORTANT]
> **The Click Moment**: "**Ordering with dependencies**" — OR — "**build order**" — OR — "**course schedule** (can all courses be taken?)" — OR — "detect cycle in directed graph". Kahn's: maintain in-degree; process zero-in-degree nodes; cycle exists if not all nodes are processed.

```python
def kahn_topo_sort(n: int, edges: list[tuple[int,int]]) -> list[int]:
    adj = defaultdict(list)
    in_degree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    queue = deque(i for i in range(n) if in_degree[i] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return order if len(order) == n else []  # [] = cycle detected
```

---

### 0-1 BFS — Binary-Weight Shortest Path

> [!IMPORTANT]
> **The Click Moment**: "Edges cost **0 or 1**" — OR — "some moves are free, others cost 1" — OR — "minimum cost path where each edge is cheap or expensive". Use a deque: 0-cost edges to front, 1-cost edges to back. O(V+E) — faster than Dijkstra's O(E log V).

```python
def zero_one_bfs(adj: dict, start: int, target: int) -> int:
    dist = {start: 0}
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v, cost in adj[u]:
            new_dist = dist[u] + cost
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                if cost == 0:
                    dq.appendleft(v)  # free move → front
                else:
                    dq.append(v)      # costly move → back
    return dist.get(target, -1)
```

---

### Minimum Spanning Tree — Kruskal's and Prim's

> [!IMPORTANT]
> **The Click Moment**: "**Minimum cost to connect** all nodes" — OR — "**minimum spanning tree**". Kruskal: sort edges, use DSU to greedily add cheapest non-cycle edge. Prim: from any node, greedily grow the MST by adding the cheapest edge from the frontier (min-heap).

```python
# Kruskal's (requires Union-Find / DSU)
def kruskal_mst(n: int, edges: list[tuple[int,int,int]]) -> int:
    edges.sort(key=lambda e: e[2])
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression
            x = parent[x]
        return x

    def union(x: int, y: int) -> bool:
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    total_cost = 0
    edges_used = 0
    for u, v, w in edges:
        if union(u, v):
            total_cost += w
            edges_used += 1
            if edges_used == n - 1:
                break
    return total_cost if edges_used == n - 1 else -1  # -1 if graph is disconnected
```

---

## 3. Advanced Patterns

> [!TIP]
> **Grid problems**: Each cell is a node; 4-directional neighbors are edges. Don't construct an explicit adjacency list — use a `get_neighbors(r, c)` function inline. Multi-source BFS (all `0`s at once) solves "distance to nearest 0" and "walls and gates" in O(R×C).

> [!TIP]
> **Bidirectional BFS**: For problems with a known source and target (Word Ladder, 6-degrees of separation), expand from both ends simultaneously. Meet in the middle. Explored nodes shrink from O(b^d) to O(b^(d/2)) where b = branching factor. Google Maps uses bidirectional Dijkstra for shortest route queries.

---

## 4. SDE-3 Deep Dives

### Scalability: Distributed Shortest Path

> [!TIP]
> **Pregel (Google, 2010)**: Graph computation framework where each vertex computes its state and sends messages to neighbors. Dijkstra's becomes: each vertex maintains `dist`, sends `(dist + edge_weight)` to neighbors, updates if a better value arrives. Converges in O(diameter) supersteps. Handles trillion-edge graphs by partitioning across thousands of machines.
>
> **Delta-stepping**: A parallelizable variant of Dijkstra that processes a "bucket" of vertices with distance in `[d, d+Δ]` simultaneously, then advances to the next bucket. Implemented in Boost Graph Library and used in high-performance computing.

### Scalability: Graph Streaming

> [!TIP]
> When the graph is too large to store (social network with 1 billion edges): use **streaming algorithms** that process each edge once and maintain O(polylog N) state. For connectivity: maintain a random spanning forest using sketches (union-find on the stream). For approximate shortest paths: maintain a distance oracle with O(N^(1+1/k)) space and O(k) query time.

### Concurrency: Lock-Free Graph Traversal

> [!TIP]
> Concurrent BFS: divide the frontier into shards; each thread processes its shard in parallel. Synchronize on the next frontier with a concurrent queue or `ConcurrentLinkedQueue`. Challenge: avoiding duplicate processing — use a `ConcurrentHashMap` as the visited set with `putIfAbsent` as the atomic gate.

### Trade-offs: Graph Algorithm Selection

| Constraint | Algorithm | Why |
| :--- | :--- | :--- |
| Unweighted graph | BFS | O(V+E); no heap needed |
| Non-negative weights | Dijkstra | O(E log V); greedy optimal |
| Negative weights | Bellman-Ford | O(VE); relaxes all paths |
| 0/1 weights | 0-1 BFS | O(V+E); deque vs heap |
| All-pairs | Floyd-Warshall | O(V³); simple DP on adjacency matrix |
| Dense graph (E ≈ V²) | Prim with array | O(V²) < O(E log V) for dense |
| Sparse graph (E ≈ V) | Kruskal | O(E log E) = O(V log V) |

---

## 5. Common Interview Problems

### Medium
- [Course Schedule](../../google-sde2/PROBLEM_DETAILS.md#course-schedule) — Kahn's topo sort; detect cycle.
- [Course Schedule II](../../google-sde2/PROBLEM_DETAILS.md#course-schedule) — Same; return the order.
- [Network Delay Time](../../google-sde2/PROBLEM_DETAILS.md#network-delay-time) — Dijkstra from source; answer = max(dist) if all nodes reached.
- **Number of Islands** — DFS/BFS flood fill (see graphs.md).
- **Clone Graph** — DFS with `old→clone` map.
- **Rotting Oranges** — Multi-source BFS.
- **Evaluate Division** — Build weighted directed graph; DFS/BFS with accumulated product.

### Hard
- [Word Ladder](../../google-sde2/PROBLEM_DETAILS.md#word-ladder) — BFS; neighbors = one-letter edits in word set.
- [Alien Dictionary](../../google-sde2/PROBLEM_DETAILS.md#alien-dictionary) — Build edges from adjacent word pairs; Kahn's topo.
- [Cheapest Flights Within K Stops](../../google-sde2/PROBLEM_DETAILS.md#cheapest-flights-within-k-stops) — Modified Bellman-Ford (K+1 relaxations) or BFS with state `(node, stops)`.
- **Find the City with Smallest Reachable Neighbors** — Floyd-Warshall; count reachable cities within threshold.
- **Reconstruct Itinerary** — Eulerian path; Hierholzer's algorithm; DFS with lexicographic neighbor ordering.
- **Critical Connections in a Network** — Tarjan's bridge-finding algorithm.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Course Schedule](../../google-sde2/PROBLEM_DETAILS.md#course-schedule)** | "Detect cycle in DAG" | Kahn's; `len(order) < n` → cycle | Edge direction: `prereq → course`, not reversed. |
| **[Network Delay Time](../../google-sde2/PROBLEM_DETAILS.md#network-delay-time)** | "All-nodes reachable from source, total time?" | Dijkstra; answer = `max(dist)` if all reached | If any node unreachable: `dist[v] = inf` → return -1. |
| **[Word Ladder](../../google-sde2/PROBLEM_DETAILS.md#word-ladder)** | "Minimum transformation steps" | BFS; neighbor = one-letter edit in word set | Remove visited words from set immediately — prevents revisit and cycle. |
| **[Alien Dictionary](../../google-sde2/PROBLEM_DETAILS.md#alien-dictionary)** | "Character order from sorted words" | First mismatch between adjacent words → directed edge; Kahn's | Invalid: `"abc"` before `"ab"` → return `""`. |
| **[Cheapest Flights K Stops](../../google-sde2/PROBLEM_DETAILS.md#cheapest-flights-within-k-stops)** | "Shortest path with at most K intermediate nodes" | Bellman-Ford for K+1 rounds | Standard Dijkstra doesn't work — need to track stop count in state. |
| **Number of Islands** | "Connected components in grid" | DFS/BFS flood-fill; count calls | In-place mark (`'1'→'0'`) avoids visited set. Recursion limit for 200×200 grid. |
| **Evaluate Division** | "Graph: nodes=variables, edges=ratios" | Build weighted graph; BFS/DFS to find path product | Handle disconnected components (query impossible → -1). Bidirectional edges: A/B and B/A. |
| **Reconstruct Itinerary** | "Eulerian path with lexicographic order" | Hierholzer's; DFS with sorted neighbors; post-order reversal | Must visit all edges exactly once — Eulerian, not Hamiltonian. Sort neighbors for lex order. |
| **Critical Connections** | "Bridges in undirected graph" | Tarjan's: discovery time + low value; bridge if `low[v] > disc[u]` | Low[v] = min(disc[v], min low of DFS descendants). Requires tracking parent to avoid trivial back-edge. |

---

## See also

- [Union Find](union-find.md) — DSU for Kruskal's MST and connectivity
- [data-structures/graphs.md](../data-structures/graphs.md) — BFS/DFS templates and grid problems
- [Heap](../data-structures/heap.md) — Dijkstra uses a min-heap
- [Patterns Master](../../../reference/patterns/patterns-master.md) — graph pattern recognition triggers
