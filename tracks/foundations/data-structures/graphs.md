# Graphs (Data Structure) — SDE-3 Gold Standard

Vertices (nodes) + Edges (connections). SDE-3 focus: correct representation choice, clean traversal templates, multi-source BFS, topological sort, and knowing when each algorithm applies.

---

## 1. Representation Choice

> [!IMPORTANT]
> **The Click Moment**: Before coding any graph problem, state the representation. **Adjacency list** is the default for sparse graphs (most interview problems). **Adjacency matrix** only when you need O(1) edge existence checks and N ≤ 1000.

| Representation | Space | Edge Lookup | Best For |
| :--- | :--- | :--- | :--- |
| Adjacency list | O(V + E) | O(degree) | Sparse graphs, BFS/DFS, interview problems |
| Adjacency matrix | O(V²) | O(1) | Dense graphs, Floyd-Warshall, N ≤ 1000 |
| Edge list | O(E) | O(E) | Kruskal's MST (sort edges), union-find problems |
| Implicit (grid) | O(1) extra | O(1) | Grid problems — no explicit graph construction needed |

```python
from collections import defaultdict

def build_adjacency_list(n: int, edges: list[tuple[int, int]], directed: bool = False) -> dict:
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj

# Grid as implicit graph — no explicit construction needed
DIRS_4 = [(1,0), (-1,0), (0,1), (0,-1)]
DIRS_8 = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

def get_neighbors_grid(r: int, c: int, rows: int, cols: int) -> list[tuple[int,int]]:
    return [(r+dr, c+dc) for dr, dc in DIRS_4 if 0 <= r+dr < rows and 0 <= c+dc < cols]
```

---

## 2. Core Patterns & Click Moments

### BFS — Shortest Path in Unweighted Graph

> [!IMPORTANT]
> **The Click Moment**: "**Shortest path** in unweighted graph" — OR — "**minimum steps/moves**" — OR — "**multi-source** spread (rot, distance to nearest X)" — OR — "**level-order** traversal". BFS guarantees the first time you reach a node is via the shortest path. Weighted graphs → Dijkstra instead.

```python
from collections import deque

def bfs_shortest_path(adj: dict, start: int, target: int) -> int:
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

def multi_source_bfs(grid: list[list[int]], sources: list[tuple[int,int]]) -> list[list[int]]:
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r, c in sources:
        dist[r][c] = 0
        queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for nr, nc in get_neighbors_grid(r, c, rows, cols):
            if dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist
```

> [!TIP]
> **Multi-source BFS**: Add all source nodes to the queue at distance 0 before starting. The queue processes them in round-robin, so BFS naturally expands all fronts simultaneously. This is the correct approach for "rotting oranges", "distance to nearest 0", and "walls and gates" — don't run BFS from each source separately (O(S × (V+E)) vs O(V+E)).

---

### DFS — Components, Reachability, Cycle Detection

> [!IMPORTANT]
> **The Click Moment**: "Count **connected components**" — OR — "check if **path exists**" — OR — "**flood fill** / mark a region" — OR — "detect **cycle** in undirected graph". DFS explores as deep as possible before backtracking.

```python
def dfs_iterative(adj: dict, start: int) -> set:
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen

def count_connected_components(n: int, edges: list[tuple[int,int]]) -> int:
    adj = build_adjacency_list(n, edges, directed=False)
    visited = set()
    count = 0
    for node in range(n):
        if node not in visited:
            visited |= dfs_iterative(adj, node)
            count += 1
    return count

def grid_dfs_flood_fill(grid: list[list[int]], r: int, c: int, target: int, fill: int) -> None:
    if not (0 <= r < len(grid) and 0 <= c < len(grid[0])) or grid[r][c] != target:
        return
    grid[r][c] = fill  # mark in-place
    for dr, dc in DIRS_4:
        grid_dfs_flood_fill(grid, r+dr, c+dc, target, fill)
```

> [!CAUTION]
> For large grids (200×200 = 40,000 cells), recursive DFS will hit Python's recursion limit. Use **iterative DFS** (explicit stack) or increase `sys.setrecursionlimit` — mention this trade-off to the interviewer. Iterative DFS is always preferable in production.

---

### Topological Sort — Dependency Ordering

> [!IMPORTANT]
> **The Click Moment**: "**Order tasks** with dependencies" — OR — "**course prerequisites**" — OR — "detect **cycle in directed graph**" — OR — "**build order** / compilation order". Use Kahn's (BFS-based, in-degree queue) for clean cycle detection; use DFS postorder for smaller implementation.

```python
def topological_sort_kahn(n: int, edges: list[tuple[int,int]]) -> list[int]:
    adj = defaultdict(list)
    in_degree = [0] * n
    for u, v in edges:  # u → v (u must come before v)
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

    return order if len(order) == n else []  # empty list = cycle detected

def has_cycle_directed(n: int, edges: list[tuple[int,int]]) -> bool:
    return len(topological_sort_kahn(n, edges)) < n
```

> [!CAUTION]
> **Edge direction is the #1 topo sort bug**: For "course A requires B as prerequisite", the edge is `B → A` (B must come before A), **not** `A → B`. Getting this backwards causes wrong orderings that look plausible. Always confirm: "edge u→v means u must come before v in the final order."

---

### Dijkstra — Shortest Path with Non-Negative Weights

> [!IMPORTANT]
> **The Click Moment**: "**Minimum cost path**" — OR — "shortest path with **edge weights**" — AND — "all weights are **non-negative**". Dijkstra uses a min-heap to always expand the node with the current shortest known distance. One critical guard: skip stale (distance, node) pairs that are no longer optimal.

```python
import heapq

def dijkstra(n: int, adj: dict, start: int) -> dict[int, float]:
    dist = {start: 0}
    heap = [(0, start)]  # (distance, node)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float('inf')):
            continue  # stale entry — skip
        for v, weight in adj[u]:
            new_dist = d + weight
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
    return dist
```

> [!CAUTION]
> Dijkstra **fails with negative weights** — the greedy invariant breaks. Use Bellman-Ford (O(VE)) for graphs with negative edges. For negative cycles specifically, Bellman-Ford detects them (relaxation still changes after V-1 passes).

---

## 3. SDE-3 Deep Dives

### Scalability: Distributed BFS

> [!TIP]
> For graphs too large for one machine (web graph, social network with billions of nodes):
> - **Pregel model** (Google): vertices compute and communicate via messages. Each BFS level is one superstep. Workers hold a shard of the graph; messages cross shard boundaries. O(diameter × E/P) where P = number of machines.
> - **Bidirectional BFS**: Start BFS simultaneously from source and target. Meet in the middle. Reduces explored nodes from O(b^d) to O(b^(d/2)) where b = branching factor, d = diameter. Used in Google Maps shortest path.

### Scalability: 0-1 BFS

> [!TIP]
> When edge weights are only 0 or 1, use a **deque-based BFS**: push 0-weight neighbors to the **front** of the deque, 1-weight neighbors to the **back**. O(V+E) — faster than Dijkstra's O(E log V) for this special case. Used in problems like "minimum cost to reach destination with some free edges."

### Concurrency: Parallel Graph Traversal

> [!TIP]
> BFS is **level-parallelizable**: all nodes at distance k are independent — they can be processed concurrently. Use a barrier synchronization at each level boundary. In Java: `CountDownLatch` or `Phaser` to coordinate threads at each BFS frontier. In Python: `concurrent.futures.ThreadPoolExecutor` with a `Barrier` from `threading`.

### Trade-offs: BFS vs DFS

| Property | BFS | DFS |
| :--- | :--- | :--- |
| Shortest path | **Yes** (unweighted) | No |
| Memory | O(max level width) | O(max depth) |
| Finds all paths | Implicit (level-by-level) | Natural with backtracking |
| Cycle detection | Via visited set | Via recursion state (white/gray/black) |
| Topological sort | Kahn's (in-degree) | Reverse postorder |
| Grid problems | Better (level = steps) | Works; risk of recursion overflow |

---

## 4. Common Interview Problems

### Easy / Medium (High Frequency)
- [Number of Islands](../../google-sde2/PROBLEM_DETAILS.md#number-of-islands) — DFS/BFS flood fill; count calls to unvisited `1`.
- **Flood Fill** — BFS/DFS from `(sr, sc)`; recolor connected component.
- [Rotting Oranges](../../google-sde2/PROBLEM_DETAILS.md#rotting-oranges) — Multi-source BFS from all rotten oranges at distance 0; count levels.
- [Course Schedule](../../google-sde2/PROBLEM_DETAILS.md#course-schedule) — Kahn's topo sort; cycle ⟺ `len(order) < n`.
- [Clone Graph](../../google-sde2/PROBLEM_DETAILS.md#clone-graph) — DFS/BFS with `old → clone` map; create before traversing to handle cycles.
- **Surrounded Regions** — Flood fill from border `O`s to mark safe; flip remaining interior `O`→`X`.
- **Max Area of Island** — DFS/BFS; return max area across all components.

### Hard / Stretch (Common at Google)
- [Word Ladder](../../google-sde2/PROBLEM_DETAILS.md#word-ladder) — BFS; neighbors = one-letter edits in word set; remove visited words.
- [Alien Dictionary](../../google-sde2/PROBLEM_DETAILS.md#alien-dictionary) — Build directed edges from adjacent word pairs; topo sort all characters.
- **Pacific Atlantic Water Flow** — Reverse BFS: which cells can reach Pacific? Atlantic? Intersect.
- **Network Delay Time** — Dijkstra from source; answer = max dist if all nodes reached.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Number of Islands](../../google-sde2/PROBLEM_DETAILS.md#number-of-islands)** | "Count connected components in grid" | DFS/BFS; mark visited by sinking (`'1'→'0'`) | 4-dir vs 8-dir neighbors — confirm with interviewer. Recursion overflow on large grids. |
| **Flood Fill** | "Recolor connected region" | BFS/DFS from `(sr,sc)`; only spread to same original color | Skip if `newColor == oldColor` — avoids infinite loop. |
| **[Rotting Oranges](../../google-sde2/PROBLEM_DETAILS.md#rotting-oranges)** | "Simultaneous spread, minimum time" | Multi-source BFS; count fresh oranges; return levels-1 | Track fresh count — if fresh remain after BFS, return -1 (unreachable). |
| **[Course Schedule](../../google-sde2/PROBLEM_DETAILS.md#course-schedule)** | "Detect cycle in prerequisites" | Kahn's topo; cycle ⟺ `len(order) < n` | Edge direction: `prereq → course`, not `course → prereq`. |
| **[Clone Graph](../../google-sde2/PROBLEM_DETAILS.md#clone-graph)** | "Deep copy graph with cycles" | Map `old→clone`; DFS/BFS; create clone before recursing | Cycles require the map before recursion — avoids infinite loop. |
| **Surrounded Regions** | "Flip interior isolated regions" | BFS from border O's to mark safe; flip rest | Don't BFS from every interior `O` — O(R²C²) vs O(RC) from borders. |
| **[Word Ladder](../../google-sde2/PROBLEM_DETAILS.md#word-ladder)** | "Shortest transformation sequence" | BFS; each word's neighbors = one-letter edits in dict | Remove words from set as visited — prevents revisit. Bidirectional BFS for follow-up. |
| **[Alien Dictionary](../../google-sde2/PROBLEM_DETAILS.md#alien-dictionary)** | "Infer char ordering from sorted words" | Extract edges from first mismatch in adjacent words; topo | Invalid input: `"abc"` before `"ab"` — detect and return `""`. |
| **Pacific Atlantic Flow** | "Which cells reach both oceans?" | Reverse BFS from each ocean's border; intersect reachable sets | Reverse means: "can water flow here from the border?" — go uphill. |

---

## See also

- [Graph (algorithms)](../algorithms/graph.md) — Dijkstra, Bellman-Ford, MST algorithms
- [Union-Find](../algorithms/union-find.md) — DSU for Kruskal and connectivity
- [Patterns Master](../../../reference/patterns/patterns-master.md) — graph pattern recognition triggers
