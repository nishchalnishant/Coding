# Graphs (Data Structure) — SDE-3 Gold Standard

Vertices (nodes) + Edges (connections). SDE-3 focus: correct representation choice, clean traversal templates, multi-source BFS, topological sort, and knowing when each algorithm applies.

---

## Theory & Mental Models

**What it is:** A set of vertices (nodes) V and edges (connections) E between pairs of vertices. Variants: directed vs undirected; weighted vs unweighted; cyclic vs acyclic (DAG). Core property: connectivity — what can reach what.

**Why it exists:** Solves the problem of modeling arbitrary relationships between entities. Real-world analogy: a road network — cities are nodes, roads are edges, one-way streets are directed edges, and traffic jams are edge weights.

**Memory layout:** Two main representations — (1) Adjacency list: `dict[node → list[neighbor]]`, O(V+E) space, O(degree) edge lookup — default for sparse graphs. (2) Adjacency matrix: `matrix[u][v] = weight`, O(V²) space, O(1) edge lookup — only for dense graphs (N ≤ 1000).

**Key invariants:**
- Undirected graph: each edge stored twice (u→v and v→u) in adjacency list.
- Directed graph: edge u→v exists only in `adj[u]`; `adj[v]` does not include u.
- DAG (Directed Acyclic Graph): topological ordering exists iff no cycles — Kahn's algorithm verifies this.
- Visited set must be maintained to avoid infinite loops in graphs with cycles.

**Complexity at a glance:**

| Operation | Adj List | Adj Matrix | Notes |
| :--- | :--- | :--- | :--- |
| Space | O(V+E) | O(V²) | List is sparse-efficient |
| Add edge | O(1) | O(1) | Both O(1) |
| Check edge u→v | O(degree(u)) | O(1) | Matrix wins for edge checks |
| BFS/DFS | O(V+E) | O(V²) | List wins for traversal |
| All neighbors of u | O(degree(u)) | O(V) | List wins for iteration |

**When to reach for it:**
- Relationships between entities — social networks, dependency graphs, road maps.
- Shortest path problems — BFS (unweighted), Dijkstra (weighted positive), Bellman-Ford (negative weights).
- Network flow, dependency ordering (topological sort), cluster detection (connected components).
- Grid problems — treat each cell as a node, 4/8 neighbors as edges (implicit graph).
- Cycle detection in directed graphs (build order, deadlock detection).

**Common mistakes:**
- Forgetting to handle disconnected graphs — always iterate over all nodes to start BFS/DFS from each unvisited one.
- Recursive DFS stack overflow on large graphs (>10K nodes) — use iterative DFS with explicit stack.
- Treating undirected graph as directed — adding edge only one direction causes connectivity bugs.
- Marking visited after dequeue (BFS) instead of before enqueue — causes duplicate processing and TLE.

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

#### Common Variants & Twists
1. **Word Ladder**:
   - **What (The Problem & Goal):** Find the shortest transformation sequence from a `beginWord` to an `endWord`, changing only one letter at a time.
   - **How (Intuition & Mental Model):** The implicit graph twist. Nodes are words, and edges exist if two words differ by exactly one character. Use BFS from the `beginWord`. To find neighbors, iterate through each character of the current word and replace it with 'a' through 'z', checking if the new word is in the dictionary.
2. **Minimum Knight Moves**:
   - **What (The Problem & Goal):** Find the minimum number of knight moves to reach a target cell on an infinite chessboard.
   - **How (Intuition & Mental Model):** Graph is an infinite chessboard. Use BFS to find the shortest path. To optimize, use bidirectional BFS, or leverage symmetry (working only in the first quadrant `(abs(x), abs(y))` since moves are symmetric).
3. **Shortest Path in a Grid with Obstacles Elimination**:
   - **What (The Problem & Goal):** Find the shortest path from top-left to bottom-right, but you can eliminate at most `k` obstacles.
   - **How (Intuition & Mental Model):** The state space twist. Your BFS `visited` set must track `(row, col, obstacles_eliminated)` because reaching the same cell with a different number of remaining eliminations is a different state. If you hit an obstacle and have eliminations left, increment the elimination count and proceed.

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

#### Common Variants & Twists
1. **Max Area of Island**:
   - **What (The Problem & Goal):** Find the maximum area of an island (a connected component of 1s).
   - **How (Intuition & Mental Model):** Instead of just counting components, return the size of the component. The DFS function should return `1 + sum(dfs(neighbor))`. Track the maximum size returned across all starting 1s.
2. **Number of Closed Islands**:
   - **What (The Problem & Goal):** Count islands (0s) that are completely surrounded by water (1s) — meaning they don't touch the grid boundary.
   - **How (Intuition & Mental Model):** First, run DFS on all 0s on the perimeter of the grid and mark them as non-closed (or turn them into 1s). Then, run a standard DFS component count on the remaining interior 0s to find the closed islands.
3. **Regions Cut By Slashes**:
   - **What (The Problem & Goal):** A grid consists of `/`, `\`, or blank spaces. Count the number of isolated regions they divide the grid into.
   - **How (Intuition & Mental Model):** The upscaling twist. A single cell can contain multiple disconnected regions. Upscale the `n x n` grid into a `3n x 3n` grid. Represent slashes with 1s and empty space with 0s. Then, run standard DFS/BFS flood fill to count the components of 0s.

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

#### Common Variants & Twists
1. **Alien Dictionary**:
   - **What (The Problem & Goal):** Given a sorted list of alien words, derive the lexicographical order of their alphabet.
   - **How (Intuition & Mental Model):** The implicit dependency twist. Compare adjacent words to find the *first* differing character. That difference implies a directed edge (e.g., if "ab" comes before "ac", then 'b' -> 'c'). Build the graph, then run Kahn's algorithm. If a cycle is detected, no valid ordering exists.
2. **Course Schedule II**:
   - **What (The Problem & Goal):** Return the actual ordering in which you should take courses to finish all of them.
   - **How (Intuition & Mental Model):** Instead of just boolean cycle detection, return the ordering. Kahn's algorithm naturally builds this ordering in its `result` array. If `len(result) == numCourses`, return `result`; otherwise, return an empty array (cycle).
3. **Sequence Reconstruction**:
   - **What (The Problem & Goal):** Check if a given sequence is the *only* valid topological sort possible from a set of subsequences.
   - **How (Intuition & Mental Model):** Uniqueness twist. A topological sort is unique if and only if the queue size never exceeds 1 at any point during Kahn's algorithm. If the queue has 2 or more elements, multiple valid choices exist.

> [!CAUTION]
> **Edge direction is the #1 topo sort bug**: For "course A requires B as prerequisite", the edge is `B → A` (B must come before A), **not** `A → B`. Getting this backwards causes wrong orderings that look plausible. Always confirm: "edge u→v means u must come before v in the final order."

---

> [!TIP]
> For weighted shortest path algorithms (Dijkstra, Bellman-Ford, 0-1 BFS) and MST (Kruskal's), see [Graph Algorithms](../algorithms/graph.md). This file covers graph **representation and traversal**; that file covers graph **algorithms on weighted edges**.

---

## 3. SDE-3 Deep Dives

### Scalability: Distributed BFS

> [!TIP]
> For graphs too large for one machine (web graph, social network with billions of nodes):
> - **Pregel model** (Google): vertices compute and communicate via messages. Each BFS level is one superstep. Workers hold a shard of the graph; messages cross shard boundaries. O(diameter × E/P) where P = number of machines.
> - **Bidirectional BFS**: Start BFS simultaneously from source and target. Meet in the middle. Reduces explored nodes from O(b^d) to O(b^(d/2)) where b = branching factor, d = diameter. Used in Google Maps shortest path.

```python
def bidirectional_bfs(adj: dict, start: int, target: int) -> int:
    if start == target:
        return 0
        
    # Maintain two frontiers and their distances
    queue_start, queue_target = deque([start]), deque([target])
    dist_start, dist_target = {start: 0}, {target: 0}
    
    def expand_frontier(queue, dist_this, dist_other):
        # Process one full level of the smaller queue
        for _ in range(len(queue)):
            u = queue.popleft()
            for v in adj[u]:
                if v in dist_other:
                    return dist_this[u] + 1 + dist_other[v]
                if v not in dist_this:
                    dist_this[v] = dist_this[u] + 1
                    queue.append(v)
        return -1
        
    while queue_start and queue_target:
        # Always expand the smaller frontier to minimize branching factor impact
        if len(queue_start) <= len(queue_target):
            ans = expand_frontier(queue_start, dist_start, dist_target)
        else:
            ans = expand_frontier(queue_target, dist_target, dist_start)
            
        if ans != -1:
            return ans
            
    return -1  # unreachable
```

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
- [Number of Islands](../algo/problem-deep-dives.md#number-of-islands) — DFS/BFS flood fill; count calls to unvisited `1`.
- **Flood Fill** — BFS/DFS from `(sr, sc)`; recolor connected component.
- [Rotting Oranges](../algo/problem-deep-dives.md#rotting-oranges) — Multi-source BFS from all rotten oranges at distance 0; count levels.
- [Course Schedule](../algo/problem-deep-dives.md#course-schedule) — Kahn's topo sort; cycle ⟺ `len(order) < n`.
- [Clone Graph](../algo/problem-deep-dives.md#clone-graph) — DFS/BFS with `old → clone` map; create before traversing to handle cycles.
- **Surrounded Regions** — Flood fill from border `O`s to mark safe; flip remaining interior `O`→`X`.
- **Max Area of Island** — DFS/BFS; return max area across all components.

### Hard / Stretch (Common at Google)
- [Word Ladder](../algo/problem-deep-dives.md#word-ladder) — BFS; neighbors = one-letter edits in word set; remove visited words.
- [Alien Dictionary](../algo/problem-deep-dives.md#alien-dictionary) — Build directed edges from adjacent word pairs; topo sort all characters.
- **Pacific Atlantic Water Flow** — Reverse BFS: which cells can reach Pacific? Atlantic? Intersect.
- **Network Delay Time** — Dijkstra from source; answer = max dist if all nodes reached.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Number of Islands](../algo/problem-deep-dives.md#number-of-islands)** | "Count connected components in grid" | DFS/BFS; mark visited by sinking (`'1'→'0'`) | 4-dir vs 8-dir neighbors — confirm with interviewer. Recursion overflow on large grids. |
| **Flood Fill** | "Recolor connected region" | BFS/DFS from `(sr,sc)`; only spread to same original color | Skip if `newColor == oldColor` — avoids infinite loop. |
| **[Rotting Oranges](../algo/problem-deep-dives.md#rotting-oranges)** | "Simultaneous spread, minimum time" | Multi-source BFS; count fresh oranges; return levels-1 | Track fresh count — if fresh remain after BFS, return -1 (unreachable). |
| **[Course Schedule](../algo/problem-deep-dives.md#course-schedule)** | "Detect cycle in prerequisites" | Kahn's topo; cycle ⟺ `len(order) < n` | Edge direction: `prereq → course`, not `course → prereq`. |
| **[Clone Graph](../algo/problem-deep-dives.md#clone-graph)** | "Deep copy graph with cycles" | Map `old→clone`; DFS/BFS; create clone before recursing | Cycles require the map before recursion — avoids infinite loop. |
| **Surrounded Regions** | "Flip interior isolated regions" | BFS from border O's to mark safe; flip rest | Don't BFS from every interior `O` — O(R²C²) vs O(RC) from borders. |
| **[Word Ladder](../algo/problem-deep-dives.md#word-ladder)** | "Shortest transformation sequence" | BFS; each word's neighbors = one-letter edits in dict | Remove words from set as visited — prevents revisit. Bidirectional BFS for follow-up. |
| **[Alien Dictionary](../algo/problem-deep-dives.md#alien-dictionary)** | "Infer char ordering from sorted words" | Extract edges from first mismatch in adjacent words; topo | Invalid input: `"abc"` before `"ab"` — detect and return `""`. |
| **Pacific Atlantic Flow** | "Which cells reach both oceans?" | Reverse BFS from each ocean's border; intersect reachable sets | Reverse means: "can water flow here from the border?" — go uphill. |
| **Find if Path Exists** [E] | "Is there a path from source to destination?" | BFS/DFS or Union-Find; mark visited | Union-Find: check `find(source) == find(destination)` after all union ops. |
| **Find Center of Star Graph** [E] | "Node connected to all others in star" | Center appears in both of the first two edges | Any common node in `edges[0]` and `edges[1]` is the center — O(1). |
| **Employee Importance** [E] | "Total importance of employee and all subordinates" | BFS/DFS from root employee; accumulate importance | Build id→employee map first; then BFS on subordinate ids. |
| **All Paths From Source to Target** [M] | "All paths in DAG from 0 to n-1" | DFS with backtracking; no visited set needed (DAG guarantees no cycles) | No cycle → no need for visited set; append path on reaching target. |
| **Is Graph Bipartite?** [M] | "2-color graph with no monochromatic edge" | BFS/DFS; alternate colors; conflict = not bipartite | Disconnected graph: run BFS/DFS from every unvisited node. |
| **Minimum Number of Vertices to Reach All Nodes** [M] | "In DAG, find nodes with no incoming edges" | Count in-degrees; nodes with in-degree 0 are the answer | Any node reachable from another has in-degree ≥ 1 — not a required start. |
| **Network Delay Time** [M] | "All nodes reachable in shortest time" | Dijkstra from source; answer = max of all shortest distances | Return -1 if any node unreachable (`dist == inf`). |
| **Find Eventual Safe States** [M] | "Nodes that don't lead to a cycle" | Reverse edges; topo sort via Kahn's; nodes in topo = safe | Alternatively: DFS with 3-color (white/gray/black); gray = cycle. |
| **Redundant Connection** [M] | "Edge creating cycle in undirected graph" | Union-Find; first edge where `find(u) == find(v)` is redundant | If multiple redundant edges exist, return the last one (rightmost in input). |
| **Minimum Spanning Tree (Kruskal's)** [M] | "Min total edge weight connecting all nodes" | Sort edges by weight; add if no cycle (Union-Find) | Edge count of MST = N-1; stop early when you've added N-1 edges. |
| **Longest Path in DAG** [H] | "Maximum length path in directed acyclic graph" | Topo sort + DP; `dp[node] = max(dp[neighbor] + 1)` | Only works on DAGs — cycles make this undefined. Use memo + DFS for top-down. |
| **Swim in Rising Water** [H] | "Min time to reach bottom-right as water rises" | Binary search on answer + BFS feasibility; or Dijkstra treating elevation as cost | Dijkstra approach: `dist[r][c]` = min max-elevation path to `(r,c)`. |

---

## Quick Revision Triggers

- If the problem says "shortest path" in an unweighted graph → think BFS; first reach = shortest path by definition.
- If the problem says "count connected components" or "flood fill a region" → think DFS/BFS iterating over all unvisited nodes.
- If the problem says "course schedule", "task ordering", or "detect cycle in directed graph" → think Kahn's Topological Sort; cycle iff `len(order) < n`.
- If the problem says "spread simultaneously from multiple sources" (rotten oranges, walls and gates) → think Multi-Source BFS; enqueue all sources at distance 0.
- If the problem says "all cells reach both ocean/boundary" → think Reverse BFS from each boundary; intersect reachable sets.
- If the problem gives a grid → treat it as implicit graph; no explicit adjacency list needed; use `DIRS_4 = [(1,0),(-1,0),(0,1),(0,-1)]`.
- If DFS risks stack overflow on a large graph → use iterative DFS with explicit stack; mention `sys.setrecursionlimit` tradeoff to interviewer.

## See also

- [Graph (algorithms)](../algorithms/graph.md) — Dijkstra, Bellman-Ford, MST algorithms
- [Union-Find](../algorithms/union-find.md) — DSU for Kruskal and connectivity
- [Patterns Master](../../../reference/patterns/patterns-master.md) — graph pattern recognition triggers
