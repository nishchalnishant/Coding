# Graphs (Algorithms) — SDE-3 Gold Standard

Vertices and edges; directed/undirected, weighted/unweighted. SDE-3 expects: correct algorithm selection, Dijkstra implementation with lazy deletion guard, Bellman-Ford for negative weights, and distributed graph thinking.

---

## Theory & Mental Models

**What it is.** Graph algorithms operate on vertices and edges to answer reachability, shortest-path, ordering, and connectivity questions. Core invariant: the correct algorithm depends entirely on the graph's edge-weight structure — wrong algorithm = wrong answer regardless of implementation quality.

**Why it exists.** Many real-world problems are graphs in disguise: course prerequisites (DAG + topological sort), network routing (shortest path), social connectivity (union-find / BFS components), infrastructure cost (MST). Graph algorithms formalize "how do nodes relate?" into efficient traversal and optimization procedures.

**The mental model.** Think of the graph as a city map. BFS finds the fewest-turn driving route (unweighted). Dijkstra finds the fastest route (weighted, non-negative). DFS checks if two cities are connected at all. Topological sort gives the prerequisite order for course enrollment. Algorithm selection is the core SDE-3 graph skill.

**Complexity at a glance.**

| Algorithm | Time | Space | Use When |
| :--- | :--- | :--- | :--- |
| BFS / DFS | O(V + E) | O(V) | Unweighted shortest path / connectivity |
| Dijkstra | O((V + E) log V) | O(V) | Non-negative weighted shortest path |
| Bellman-Ford | O(V × E) | O(V) | Negative weights; negative cycle detection |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest path, V ≤ ~500 |
| Kruskal / Prim | O(E log E) | O(V) | Minimum spanning tree |
| Kahn's (topo sort) | O(V + E) | O(V) | Ordering with dependencies; cycle detection |

**When to reach for it.**
- Shortest path (unweighted → BFS; weighted non-negative → Dijkstra; negative weights → Bellman-Ford).
- Dependency ordering or cycle detection in directed graphs → topological sort (Kahn's or DFS postorder).
- Connected components with dynamic edge additions → DSU.
- Minimum spanning tree → Kruskal (sparse) or Prim (dense).
- Bridges / articulation points → Tarjan's DFS.

**When NOT to use it.**
- Floyd-Warshall on graphs with V > 1000 — O(V³) is too slow.
- Standard Dijkstra on graphs with negative weights — produces silently wrong results.
- DFS for shortest path in unweighted graphs — BFS guarantees shortest; DFS does not.

**Common mistakes.**
- Not handling disconnected graphs — always run BFS/DFS from every unvisited node.
- Forgetting to mark visited before pushing to the BFS queue — causes TLE from revisiting nodes exponentially.
- Wrong edge direction in directed graphs (prereq → course vs. course → prereq).
- Using Dijkstra without the lazy deletion guard `if d > dist[u]: continue` — stale heap entries corrupt results.

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

#### Common Variants & Twists
1. **Shortest Path in Binary Matrix**:
   - **What (The Problem & Goal):** Find the shortest path from top-left to bottom-right in a grid of 0s and 1s (where 0 is a path).
   - **How (Intuition & Mental Model):** Treat the grid as an unweighted graph. Use BFS. Each state is `(r, c)`. The level of the BFS at which you first reach the target is the answer.
2. **Open the Lock**:
   - **What (The Problem & Goal):** Given a 4-digit lock and a set of "deadends", find the minimum number of turns to reach a target combination.
   - **How (Intuition & Mental Model):** The search space consists of 10,000 combinations (nodes). Each combination has 8 neighbors (turning each of the 4 dials up or down). Use BFS starting from "0000". If a neighbor is a deadend, don't add it to the queue.
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

#### Common Variants & Twists
1. **Critical Connections in a Network (Bridges)**:
   - **What (The Problem & Goal):** Find all edges in an undirected graph that, if removed, would disconnect the graph.
   - **How (Intuition & Mental Model):** Use Tarjan's algorithm or a similar DFS-based approach. Track the `discovery_time` and `lowest_reachable_time` for each node. An edge `(u, v)` is a bridge if the lowest time reachable from `v` is strictly greater than the discovery time of `u`.
2. **Reconstruct Itinerary**:
   - **What (The Problem & Goal):** Given a list of airline tickets, reconstruct the itinerary in order, starting from "JFK". If multiple valid itineraries exist, return the one with the smallest lexicographical order.
   - **How (Intuition & Mental Model):** This is a search for an **Eulerian Path** in a directed graph. Use Hierholzer's algorithm: DFS through neighbors in lexicographical order. When a node has no more outgoing edges, push it to the result stack. The final itinerary is the reversed stack.
```

> [!CAUTION]
> **For large graphs**, recursive DFS overflows Python's stack. Convert to iterative DFS using an explicit stack. Alternatively, use Kahn's algorithm (BFS-based topo sort) — it naturally handles large graphs and detects cycles via the unprocessed node count.

---

### Dijkstra — Non-Negative Weighted Shortest Path

> [!IMPORTANT]
> **The Click Moment**: "**Shortest path with edge weights**" — AND — "all weights are **non-negative**". The lazy deletion guard (`if d > dist[u]: continue`) is mandatory — without it, stale heap entries cause incorrect updates and silent bugs.

> [!TIP]
> Dijkstra is like a GPS that always recalculates from your cheapest unvisited waypoint — always expand the node you can reach most cheaply, not the one you added first. The min-heap enforces this ordering. A "stale entry" arises when you find a cheaper path to a node after it was already pushed onto the heap; the guard `if d > dist[u]: continue` discards those old records rather than re-processing the node at a higher cost.

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

#### Common Variants & Twists
1. **Path With Maximum Probability**:
   - **What (The Problem & Goal):** Find the path from start to end with the highest product of edge probabilities.
   - **How (Intuition & Mental Model):** Probabilities are in `[0, 1]`, so their product decreases as the path length increases. This is equivalent to Dijkstra, but you want to **maximize** the product. Use a Max-Heap. Or, transform it into a shortest path problem by taking `-log(probability)` (which makes it additive and non-negative).
2. **Smallest Number of Neighbors at a Threshold Distance**:
   - **What (The Problem & Goal):** Find the city that has the smallest number of other cities reachable within a certain distance `threshold`.
   - **How (Intuition & Mental Model):** Run Dijkstra from every single city (O(V * E log V)) to find all-pairs distances. Count how many cities are within the threshold for each source.
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

#### Common Variants & Twists
1. **Cheapest Flights Within K Stops**:
   - **What (The Problem & Goal):** Find the cheapest price from source to destination with at most `k` stops.
   - **How (Intuition & Mental Model):** This is a bounded shortest path problem. Run Bellman-Ford for exactly `k+1` iterations. Each iteration `i` represents the minimum cost to reach nodes with at most `i-1` stops. Crucially, use a copy of the distance array to ensure you're only using distances from the *previous* iteration (to avoid using more than `k` edges in a single pass).
```

---

### Floyd-Warshall — All-Pairs Shortest Path

> [!IMPORTANT]
> **The Click Moment**: "Find the shortest path between **all pairs** of nodes" — OR — "graph has V ≤ 400". DP-based approach that iteratively allows nodes 0 to k to act as intermediate hops. O(V³) time, O(V²) space.

```python
def floyd_warshall(n: int, edges: list[tuple[int, int, int]]) -> list[list[float]]:
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)  # handle parallel edges
        # dist[v][u] = min(dist[v][u], w) # uncomment if undirected

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist

#### Common Variants & Twists
1. **Transitive Closure**:
   - **What (The Problem & Goal):** For every pair of nodes `(u, v)`, determine if `v` is reachable from `u`.
   - **How (Intuition & Mental Model):** Use a modified Floyd-Warshall where the update is `reachable[i][j] = reachable[i][j] or (reachable[i][k] and reachable[k][j])`. This is often more efficient than running V BFS/DFS calls if the graph is dense.
```

> [!TIP]
> **Negative cycle detection**: After running the algorithm, if `dist[i][i] < 0` for any `i`, the graph contains a negative cycle.

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

#### Common Variants & Twists
1. **Alien Dictionary**:
   - **What (The Problem & Goal):** Deriving character ordering from a sorted list of words in an alien language.
   - **How (Intuition & Mental Model):** Compare adjacent words to find the first character mismatch (e.g., "word1[i]" vs "word2[i]"). This gives a directed edge `word1[i] -> word2[i]`. Build the graph of characters and run Kahn's algorithm. If the number of sorted characters is less than the number of unique characters, a cycle exists (invalid dictionary).
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

#### Common Variants & Twists
1. **Minimum Cost to Make at Least One Valid Path in a Grid**:
   - **What (The Problem & Goal):** You are given a grid where each cell has an arrow pointing to a neighbor. You can change the arrow's direction with cost 1. Find the min cost to reach bottom-right.
   - **How (Intuition & Mental Model):** Edges to the neighbor pointed at by the arrow have cost 0. Edges to all other 3 neighbors have cost 1. Use 0-1 BFS with a deque.
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

# Prim's (requires Min-Heap)
def prim_mst(n: int, adj: dict) -> int:
    import heapq
    heap = [(0, 0)]  # (cost, node); start arbitrarily from node 0
    visited = set()
    total_cost = 0

    while heap and len(visited) < n:
        cost, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        total_cost += cost
        for v, w in adj[u]:
            if v not in visited:
                heapq.heappush(heap, (w, v))
                
    return total_cost if len(visited) == n else -1

#### Common Variants & Twists
1. **Min Cost to Connect All Points (Manhattan)**:
   - **What (The Problem & Goal):** Connect all points in a 2D plane with minimum cost, where cost between points is Manhattan distance.
   - **How (Intuition & Mental Model):** This is an MST problem on a complete graph (O(V^2) edges). Kruskal's would be O(V^2 log V). Prim's with a simple array (instead of a heap) is O(V^2), which is better for dense graphs.
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
- [Course Schedule](problem-deep-dives.md#course-schedule) — Kahn's topo sort; detect cycle.
- [Course Schedule II](problem-deep-dives.md#course-schedule) — Same; return the order.
- [Network Delay Time](problem-deep-dives.md#network-delay-time) — Dijkstra from source; answer = max(dist) if all nodes reached.
- **Number of Islands** — DFS/BFS flood fill (see graphs.md).
- **Clone Graph** — DFS with `old→clone` map.
- **Rotting Oranges** — Multi-source BFS.
- **Evaluate Division** — Build weighted directed graph; DFS/BFS with accumulated product.

### Hard
- [Word Ladder](problem-deep-dives.md#word-ladder) — BFS; neighbors = one-letter edits in word set.
- [Alien Dictionary](problem-deep-dives.md#alien-dictionary) — Build edges from adjacent word pairs; Kahn's topo.
- [Cheapest Flights Within K Stops](problem-deep-dives.md#cheapest-flights-within-k-stops) — Modified Bellman-Ford (K+1 relaxations) or BFS with state `(node, stops)`.
- **Find the City with Smallest Reachable Neighbors** — Floyd-Warshall; count reachable cities within threshold.
- **Reconstruct Itinerary** — Eulerian path; Hierholzer's algorithm; DFS with lexicographic neighbor ordering.
- **Critical Connections in a Network** — Tarjan's bridge-finding algorithm.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **[Course Schedule](problem-deep-dives.md#course-schedule)** | Topological Sort (Kahn's) | "Detect cycle in DAG" | Kahn's; `len(order) < n` → cycle | Edge direction: `prereq → course`, not reversed. |
| **[Network Delay Time](problem-deep-dives.md#network-delay-time)** | "All-nodes reachable from source, total time?" | Dijkstra; answer = `max(dist)` if all reached | If any node unreachable: `dist[v] = inf` → return -1. |
| **[Word Ladder](problem-deep-dives.md#word-ladder)** | "Minimum transformation steps" | BFS; neighbor = one-letter edit in word set | Remove visited words from set immediately — prevents revisit and cycle. |
| **[Alien Dictionary](problem-deep-dives.md#alien-dictionary)** | "Character order from sorted words" | First mismatch between adjacent words → directed edge; Kahn's | Invalid: `"abc"` before `"ab"` → return `""`. |
| **[Cheapest Flights K Stops](problem-deep-dives.md#cheapest-flights-within-k-stops)** | "Shortest path with at most K intermediate nodes" | Bellman-Ford for K+1 rounds | Standard Dijkstra doesn't work — need to track stop count in state. |
| **Number of Islands** | "Connected components in grid" | DFS/BFS flood-fill; count calls | In-place mark (`'1'→'0'`) avoids visited set. Recursion limit for 200×200 grid. |
| **Evaluate Division** | "Graph: nodes=variables, edges=ratios" | Build weighted graph; BFS/DFS to find path product | Handle disconnected components (query impossible → -1). Bidirectional edges: A/B and B/A. |
| **Reconstruct Itinerary** | "Eulerian path with lexicographic order" | Hierholzer's; DFS with sorted neighbors; post-order reversal | Must visit all edges exactly once — Eulerian, not Hamiltonian. Sort neighbors for lex order. |
| **Critical Connections** | "Bridges in undirected graph" | Tarjan's: discovery time + low value; bridge if `low[v] > disc[u]` | Low[v] = min(disc[v], min low of DFS descendants). Requires tracking parent to avoid trivial back-edge. |
| **Find if Path Exists in Graph [E]** | "Simple reachability check" | BFS/DFS from source; return True if destination visited | DSU also works: union all edges, check `find(src)==find(dst)`. BFS preferred for shortest path guarantee. |
| **Find Center of Star Graph [E]** | "Identify hub node connected to all others" | Center appears in every edge; check first two edges | `edges[0]` and `edges[1]` share exactly one node — that's the center. O(1). |
| **Clone Graph [M]** | "Deep copy a graph with arbitrary structure" | BFS/DFS; map `old→new` node; copy neighbors recursively | Must memoize (old→new) before recursing into neighbors to handle cycles. |
| **Pacific Atlantic Water Flow [M]** | "Cells that can reach both oceans" | Reverse BFS from each ocean's border; find intersection | Multi-source BFS from all Pacific border cells, then all Atlantic border cells; return overlap. |
| **All Paths From Source to Target [M]** | "Enumerate all paths in a DAG" | DFS backtracking; append to result when destination reached | DAG guarantees no cycles — no visited set needed. Backtrack by popping from path after each recursive call. |
| **Is Graph Bipartite [M]** | "Can nodes be 2-colored with no edge within same color?" | BFS/DFS coloring; conflict = not bipartite | Handle disconnected graphs — BFS from every unvisited node. Bipartite ↔ no odd-length cycles. |
| **Course Schedule II [M]** | "Return valid course ordering or [] if cycle exists" | Kahn's topological sort; return order only if `len(order)==n` | DFS topo: post-order reversal. Kahn's is cleaner for detecting cycles. Edge direction: prereq → course. |
| **Find Eventual Safe States [M]** | "Nodes that cannot reach a cycle" | Reverse graph + topological sort; or DFS with 3-color state (unvisited/in-progress/safe) | In DFS: node is safe iff all its neighbors are safe. Memoize safe status to avoid recomputation. |
| **Minimum Height Trees [M]** | "Find roots that minimize tree height" | Iteratively trim leaf nodes (degree 1) until 1 or 2 nodes remain | Same idea as topological sort from leaves inward. At most 2 centroids for any tree. |
| **Dijkstra's Shortest Path [M]** | "Single-source shortest paths in weighted graph with non-negative weights" | Min-heap `(dist, node)`; relax neighbors; skip stale heap entries | Won't work with negative edges (use Bellman-Ford). Stale entry check: `if dist > current best, skip`. |
| **Bus Routes [H]** | "Minimum bus transfers to reach destination" | BFS on bus routes (not stops); each route is a node; stop-to-routes mapping | Build `stop → list of routes` map; BFS expands entire routes, not individual stops. |
| **Shortest Path Visiting All Nodes [H]** | "Shortest path that visits all nodes in undirected graph" | BFS with state `(node, visited_bitmask)`; start from all nodes simultaneously | Multi-source BFS with bitmask state. Goal state = `visited == (1<<n)-1`. State space O(N × 2^N). |

---

## Quick Revision Triggers

- "Shortest path, unweighted graph" → BFS (level-by-level guarantees minimum hops).
- "Shortest path, non-negative weights" → Dijkstra with min-heap, O((V+E) log V).
- "Shortest path with negative weights or detect negative cycles" → Bellman-Ford, O(VE).
- "All-pairs shortest paths, dense graph" → Floyd-Warshall, O(V³).
- "Detect cycle in directed graph / topological order" → DFS with three-color marking or Kahn's BFS.
- "Minimum spanning tree, sparse graph" → Kruskal (sort edges + DSU); dense graph → Prim (min-heap).
- "Graph is really a grid" → treat cells as nodes, 4-directional edges; BFS for shortest path, DFS for components.

---

## See also

- [Union Find](union-find.md) — DSU for Kruskal's MST and connectivity
- [data-structures/graphs.md](../ds/graphs.md) — BFS/DFS templates and grid problems
- [Heap](../ds/heap.md) — Dijkstra uses a min-heap
- [Patterns Master](../../../reference/patterns/patterns-master.md) — graph pattern recognition triggers
