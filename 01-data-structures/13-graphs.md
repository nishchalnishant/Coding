---
module: 01-data-structures
topic: Graphs
tags: [data-structures, graphs]
---

← [Data structures index](./README.md) · [DS decision tree](./ds_tree.md)
## First-Principles Map

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop. Do not move on until these are reflexive.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Highly probable; know the core patterns cold. Edge cases matter less.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Know what it is conceptually; skip deep implementation practice.


```
WHY graphs exist → WHAT they are → HOW they work → WHEN to use → WHAT can go wrong
       │                 │                │               │               │
  [Many real problems   [V vertices +    [adjacency list: [social networks,[DFS on cyclic
   are pairwise         E edges; directed O(V+E) space;    route finding,  graph infinite
   relationships —       or undirected;   matrix: O(V²)   dependency      loops without
   no hierarchy,         weighted or      space O(1) edge  resolution,     visited set;
   no fixed order;       unweighted;      check; traversal: course schedule, adjacency matrix
   trees are just        can have cycles] BFS/DFS from     network flow]   too large for
   restricted graphs]                     any start node]                  sparse graphs]
       │                 │                │
  [real-world:          [invariant:      [BFS: O(V+E), level order,
   road map — cities     all edges must   shortest path (unweighted);
   as nodes,             connect vertices DFS: O(V+E), cycle detect,
   roads as edges]       in V; no self-   topological sort (DAG);
                         loops (usually)] connected components: union-find O(α)]
       ↓
[Decision: Adjacency List vs Matrix vs alternatives]
  ├── vs Adj Matrix  → list O(V+E) space for sparse; matrix O(1) edge check
  ├── vs Tree        → tree = acyclic connected graph; add cycle → graph
  └── vs Union-Find  → UF for connected components only; graph for full traversal
```

## First-Principles Breakdown
- **Root problem**: Pairwise relationships (friendships, roads, dependencies) can't be modeled by trees or flat arrays — need arbitrary connectivity.
- **Core insight**: Separating vertices (entities) from edges (relationships) lets you model any network topology.
- **Invariant**: Every edge connects two vertices in V; directed edges have a defined source and sink.
- **Why it's fast**: Adjacency list stores only existing edges — O(V+E) space instead of O(V²), critical for sparse real-world graphs.
- **Where it breaks**: Cycle detection requires explicit visited tracking; DFS on large graphs overflows the call stack; dense graphs make adjacency lists slower than matrices for edge lookups.

# Graphs (Data Structure) — L3 Core

```
[GRAPH]
├── WHY IT EXISTS
│   ├── Problem it solves: model pairwise relationships with no hierarchy constraint
│   ├── Trees can't express: cycles, multiple parents, bidirectional peer links
│   └── Real-world analogy: road network — cities = vertices, roads = edges, one-way = directed
├── WHAT IT IS (First Principles)
│   ├── Core definition: G = (V, E) — set of vertices V, set of edges E ⊆ V × V
│   ├── Directed (digraph): edges have direction; A→B ≠ B→A
│   ├── Undirected: edges are symmetric; A-B means both can reach each other
│   ├── Weighted: each edge carries a cost/distance
│   ├── DAG (Directed Acyclic Graph): directed + no cycles → enables topological sort
│   └── Degree: undirected = edge count; directed = in-degree + out-degree
├── REPRESENTATIONS
│   ├── Adjacency List: dict/array of neighbor lists
│   │   ├── Space: O(V + E) — efficient for sparse graphs
│   │   └── Neighbor iteration: O(degree) — preferred in interviews
│   ├── Adjacency Matrix: V×V boolean/weight matrix
│   │   ├── Space: O(V²) — only for dense graphs
│   │   └── Edge existence check: O(1)
│   └── Edge List: flat list of (u, v, w) tuples — used in Kruskal's MST
├── HOW IT WORKS — CORE ALGORITHMS
│   ├── BFS (Breadth-First Search)
│   │   ├── Queue-based, explores layer by layer
│   │   ├── Guarantees shortest path in UNWEIGHTED graphs
│   │   ├── Multi-source BFS: seed queue with all sources simultaneously
│   │   └── Time: O(V + E)
│   ├── DFS (Depth-First Search)
│   │   ├── Stack/recursion, explores as deep as possible first
│   │   ├── Used for: cycle detection, connected components, topological sort
│   │   └── Time: O(V + E)
│   ├── Topological Sort (DAG only)
│   │   ├── Kahn's (BFS): in-degree array + queue; detects cycles if not all processed
│   │   └── DFS-based: push to stack on finish; reverse for order
│   ├── Shortest Path
│   │   ├── BFS: unweighted O(V + E)
│   │   ├── Dijkstra: non-negative weights, O((V + E) log V) with min-heap
│   │   ├── Bellman-Ford: negative weights, O(VE), detects negative cycles
│   │   └── Floyd-Warshall: all-pairs, O(V³), dense graphs
│   ├── MST (Minimum Spanning Tree)
│   │   ├── Kruskal's: sort edges, union-find → O(E log E)
│   │   └── Prim's: grow from seed with min-heap → O((V + E) log V)
│   └── Union-Find: disjoint set structure for connectivity, O(α(N)) per op
├── COMPLEXITY SUMMARY
│   ├── BFS / DFS: O(V + E) time, O(V) space
│   ├── Dijkstra: O((V + E) log V)
│   ├── Topological sort: O(V + E)
│   └── Floyd-Warshall: O(V³)
└── WHEN TO USE vs ALTERNATIVES
    ├── Use BFS when: shortest path, level-order, multi-source spread
    ├── Use DFS when: cycle detection, topological order, connected components, backtracking
    ├── Use Dijkstra when: weighted shortest path (no negative edges)
    ├── Use Bellman-Ford when: negative edge weights or need cycle detection
    ├── Use tree instead when: data is strictly hierarchical with one parent per node
    └── Avoid adjacency matrix when: graph is sparse (V > 10³ and E << V²)
```

Vertices (nodes) + Edges (connections). L3 focus: correct representation choice, clean traversal templates, multi-source BFS, topological sort, and knowing when each algorithm applies.




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

> [!TIP]
> BFS expands nodes in order of increasing distance from the source — like ripples in a pond. All nodes at distance 1 are processed before any at distance 2. The critical rule: mark a node visited **before enqueue** (not after dequeue). Marking after dequeue allows the same node to be queued multiple times from different neighbors, causing both duplicate work and incorrect distance counting.

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
1. **Word Ladder `⚡ T1`**:
   - **What (The Problem & Goal):** Find the shortest transformation sequence from a `beginWord` to an `endWord`, changing only one letter at a time.
   - **How (Intuition & Mental Model):** The implicit graph twist. Nodes are words, and edges exist if two words differ by exactly one character. Use BFS from the `beginWord`. To find neighbors, iterate through each character of the current word and replace it with 'a' through 'z', checking if the new word is in the dictionary.
2. **Minimum Knight Moves `⚡ T1`**:
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
> **The Click Moment**: "Count **connected components**" — OR — "check if **path exists**" — OR — "**flood fill `⚡ T1`** / mark a region" — OR — "detect **cycle** in undirected graph". DFS explores as deep as possible before backtracking.

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
1. **Max Area of Island `⚡ T1`**:
   - **What (The Problem & Goal):** Find the maximum area of an island (a connected component of 1s).
   - **How (Intuition & Mental Model):** Instead of just counting components, return the size of the component. The DFS function should return `1 + sum(dfs(neighbor))`. Track the maximum size returned across all starting 1s.
2. **Number of Closed Islands**:
   - **What (The Problem & Goal):** Count islands (0s) that are completely surrounded by water (1s) — meaning they don't touch the grid boundary.
   - **How (Intuition & Mental Model):** First, run DFS on all 0s on the perimeter of the grid and mark them as non-closed (or turn them into 1s). Then, run a standard DFS component count on the remaining interior 0s to find the closed islands.
3. **Regions Cut By Slashes**:
   - **What (The Problem & Goal):** A grid consists of `/`, `\`, or blank spaces. Count the number of isolated regions they divide the grid into.
   - **How (Intuition & Mental Model):** Thealing twist. A single cell can contain multiple disconnected regions. Upscale the `n x n` grid into a `3n x 3n` grid. Represent slashes with 1s and empty space with 0s. Then, run standard DFS/BFS flood fill to count the components of 0s.

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
1. **Alien Dictionary `⚡ T1`**:
   - **What (The Problem & Goal):** Given a sorted list of alien words, derive the lexicographical order of their alphabet.
   - **How (Intuition & Mental Model):** The implicit dependency twist. Compare adjacent words to find the *first* differing character. That difference implies a directed edge (e.g., if "ab" comes before "ac", then 'b' -> 'c'). Build the graph, then run Kahn's algorithm. If a cycle is detected, no valid ordering exists.
2. **Course Schedule II `⚡ T1`**:
   - **What (The Problem & Goal):** Return the actual ordering in which you should take courses to finish all of them.
   - **How (Intuition & Mental Model):** Instead of just boolean cycle detection, return the ordering. Kahn's algorithm naturally builds this ordering in its `result` array. If `len(result) == numCourses`, return `result`; otherwise, return an empty array (cycle).
3. **Sequence Reconstruction `⚡ T1`**:
   - **What (The Problem & Goal):** Check if a given sequence is the *only* valid topological sort possible from a set of subsequences.
   - **How (Intuition & Mental Model):** Uniqueness twist. A topological sort is unique if and only if the queue size never exceeds 1 at any point during Kahn's algorithm. If the queue has 2 or more elements, multiple valid choices exist.

> [!CAUTION]
> **Edge direction is the #1 topo sort bug**: For "course A requires B as prerequisite", the edge is `B → A` (B must come before A), **not** `A → B`. Getting this backwards causes wrong orderings that look plausible. Always confirm: "edge u→v means u must come before v in the final order."

---

> [!TIP]
> For weighted shortest path algorithms (Dijkstra, Bellman-Ford, 0-1 BFS) and MST (Kruskal's), see the advanced algorithms section below.

---

## 3. Production Context (L3 Note)

> [!NOTE]
> Distributed systems details (consistent hashing, lock-free structures, bloom filters, skip lists, etc.) are **L3+ system design** topics. For Google L3 coding interviews, focus on the patterns in sections 1–2 and the interview problems below.

---

## 4. Common Interview Problems

### Easy / Medium (High Frequency)
- Number of Islands — DFS/BFS flood fill; count calls to unvisited `1`.
- **Flood Fill `⚡ T1`** — BFS/DFS from `(sr, sc)`; recolor connected component.
- Rotting Oranges — Multi-source BFS from all rotten oranges at distance 0; count levels.
- Course Schedule — Kahn's topo sort; cycle ⟺ `len(order) < n`.
- Clone Graph — DFS/BFS with `old → clone` map; create before traversing to handle cycles.
- **Surrounded Regions `⚡ T1`** — Flood fill from border `O`s to mark safe; flip remaining interior `O`→`X`.
- **Max Area of Island `⚡ T1`** — DFS/BFS; return max area across all components.

### Hard / Stretch (Common at Google)
- Word Ladder — BFS; neighbors = one-letter edits in word set; remove visited words.
- Alien Dictionary — Build directed edges from adjacent word pairs; topo sort all characters.
- **Pacific Atlantic Water Flow `⚡ T1`** — Reverse BFS: which cells can reach Pacific? Atlantic? Intersect.
- **Network Delay Time** — Dijkstra from source; answer = max dist if all nodes reached.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **Number of Islands `⚡ T1`** | "Count connected components in grid" | DFS/BFS; mark visited by sinking (`'1'→'0'`) | 4-dir vs 8-dir neighbors — confirm with interviewer. Recursion overflow on large grids. |
| **Flood Fill `⚡ T1`** | "Recolor connected region" | BFS/DFS from `(sr,sc)`; only spread to same original color | Skip if `newColor == oldColor` — avoids infinite loop. |
| **Rotting Oranges `⚡ T1`** | "Simultaneous spread, minimum time" | Multi-source BFS; count fresh oranges; return levels-1 | Track fresh count — if fresh remain after BFS, return -1 (unreachable). |
| **Course Schedule `⚡ T1`** | "Detect cycle in prerequisites" | Kahn's topo; cycle ⟺ `len(order) < n` | Edge direction: `prereq → course`, not `course → prereq`. |
| **Clone Graph `⚡ T1`** | "Deep copy graph with cycles" | Map `old→clone`; DFS/BFS; create clone before recursing | Cycles require the map before recursion — avoids infinite loop. |
| **Surrounded Regions `⚡ T1`** | "Flip interior isolated regions" | BFS from border O's to mark safe; flip rest | Don't BFS from every interior `O` — O(R²C²) vs O(RC) from borders. |
| **Word Ladder `⚡ T1`** | "Shortest transformation sequence" | BFS; each word's neighbors = one-letter edits in dict | Remove words from set as visited — prevents revisit. Bidirectional BFS for follow-up. |
| **Alien Dictionary `⚡ T1`** | "Infer char ordering from sorted words" | Extract edges from first mismatch in adjacent words; topo | Invalid input: `"abc"` before `"ab"` — detect and return `""`. |
| **Pacific Atlantic Flow** | "Which cells reach both oceans?" | Reverse BFS from each ocean's border; intersect reachable sets | Reverse means: "can water flow here from the border?" — go uphill. |
| **Find if Path Exists `⚡ T1`** [E] | "Is there a path from source to destination?" | BFS/DFS or Union-Find; mark visited | Union-Find: check `find(source) == find(destination)` after all union ops. |
| **Find Center of Star Graph** [E] | "Node connected to all others in star" | Center appears in both of the first two edges | Any common node in `edges[0]` and `edges[1]` is the center — O(1). |
| **Employee Importance** [E] | "Total importance of employee and all subordinates" | BFS/DFS from root employee; accumulate importance | Build id→employee map first; then BFS on subordinate ids. |
| **All Paths From Source to Target `⚡ T1`** [M] | "All paths in DAG from 0 to n-1" | DFS with backtracking; no visited set needed (DAG guarantees no cycles) | No cycle → no need for visited set; append path on reaching target. |
| **Is Graph Bipartite? `⚡ T1`** [M] | "2-color graph with no monochromatic edge" | BFS/DFS; alternate colors; conflict = not bipartite | Disconnected graph: run BFS/DFS from every unvisited node. |
| **Minimum Number of Vertices to Reach All Nodes `⚡ T1`** [M] | "In DAG, find nodes with no incoming edges" | Count in-degrees; nodes with in-degree 0 are the answer | Any node reachable from another has in-degree ≥ 1 — not a required start. |
| **Network Delay Time** [M] | "All nodes reachable in shortest time" | Dijkstra from source; answer = max of all shortest distances | Return -1 if any node unreachable (`dist == inf`). |
| **Find Eventual Safe States `⚡ T1`** [M] | "Nodes that don't lead to a cycle" | Reverse edges; topo sort via Kahn's; nodes in topo = safe | Alternatively: DFS with 3-color (white/gray/black); gray = cycle. |
| **Redundant Connection `⚡ T1`** [M] | "Edge creating cycle in undirected graph" | Union-Find; first edge where `find(u) == find(v)` is redundant | If multiple redundant edges exist, return the last one (rightmost in input). |
| **Minimum Spanning Tree (Kruskal's) `⚡ T1`** [M] | "Min total edge weight connecting all nodes" | Sort edges by weight; add if no cycle (Union-Find) | Edge count of MST = N-1; stop early when you've added N-1 edges. |
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



## Advanced Graph Algorithms

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
```

#### Common Variants & Twists
1. **Path With Maximum Probability**:
   - **What (The Problem & Goal):** Find the path from start to end with the highest product of edge probabilities.
   - **How (Intuition & Mental Model):** Probabilities are in `[0, 1]`, so their product decreases as the path length increases. This is equivalent to Dijkstra, but you want to **maximize** the product. Use a Max-Heap. Or, transform it into a shortest path problem by taking `-log(probability)` (which makes it additive and non-negative).
2. **Smallest Number of Neighbors at a Threshold Distance**:
   - **What (The Problem & Goal):** Find the city that has the smallest number of other cities reachable within a certain distance `threshold`.
   - **How (Intuition & Mental Model):** Run Dijkstra from every single city (O(V * E log V)) to find all-pairs distances. Count how many cities are within the threshold for each source.

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

#### Common Variants & Twists
1. **Cheapest Flights Within K Stops**:
   - **What (The Problem & Goal):** Find the cheapest price from source to destination with at most `k` stops.
   - **How (Intuition & Mental Model):** This is a bounded shortest path problem. Run Bellman-Ford for exactly `k+1` iterations. Each iteration `i` represents the minimum cost to reach nodes with at most `i-1` stops. Crucially, use a copy of the distance array to ensure you're only using distances from the *previous* iteration (to avoid using more than `k` edges in a single pass).

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
```

#### Common Variants & Twists
1. **Transitive Closure**:
   - **What (The Problem & Goal):** For every pair of nodes `(u, v)`, determine if `v` is reachable from `u`.
   - **How (Intuition & Mental Model):** Use a modified Floyd-Warshall where the update is `reachable[i][j] = reachable[i][j] or (reachable[i][k] and reachable[k][j])`. This is often more efficient than running V BFS/DFS calls if the graph is dense.

> [!TIP]
> **Negative cycle detection**: After running the algorithm, if `dist[i][i] < 0` for any `i`, the graph contains a negative cycle.

---

### Topological Sort — Kahn's Algorithm

> [!IMPORTANT]
> **The Click Moment**: "**Ordering with dependencies**" — OR — "**build order**" — OR — "**course schedule `⚡ T1`** (can all courses be taken?)" — OR — "detect cycle in directed graph". Kahn's: maintain in-degree; process zero-in-degree nodes; cycle exists if not all nodes are processed.

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

#### Common Variants & Twists
1. **Alien Dictionary**:
   - **What (The Problem & Goal):** Deriving character ordering from a sorted list of words in an alien language.
   - **How (Intuition & Mental Model):** Compare adjacent words to find the first character mismatch (e.g., "word1[i]" vs "word2[i]"). This gives a directed edge `word1[i] -> word2[i]`. Build the graph of characters and run Kahn's algorithm. If the number of sorted characters is less than the number of unique characters, a cycle exists (invalid dictionary).

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

#### Common Variants & Twists
1. **Minimum Cost to Make at Least One Valid Path in a Grid**:
   - **What (The Problem & Goal):** You are given a grid where each cell has an arrow pointing to a neighbor. You can change the arrow's direction with cost 1. Find the min cost to reach bottom-right.
   - **How (Intuition & Mental Model):** Edges to the neighbor pointed at by the arrow have cost 0. Edges to all other 3 neighbors have cost 1. Use 0-1 BFS with a deque.

---

### Minimum Spanning Tree — Kruskal's and Prim's

> [!IMPORTANT]
> **The Click Moment**: "**Minimum cost to connect** all nodes" — OR — "**minimum spanning tree `⚡ T1`**". Kruskal: sort edges, use DSU to greedily add cheapest non-cycle edge. Prim: from any node, greedily grow the MST by adding the cheapest edge from the frontier (min-heap).

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
```

#### Common Variants & Twists
1. **Min Cost to Connect All Points (Manhattan)**:
   - **What (The Problem & Goal):** Connect all points in a 2D plane with minimum cost, where cost between points is Manhattan distance.
   - **How (Intuition & Mental Model):** This is an MST problem on a complete graph (O(V^2) edges). Kruskal's would be O(V^2 log V). Prim's with a simple array (instead of a heap) is O(V^2), which is better for dense graphs.

---

## 3. Advanced Patterns

> [!TIP]
> **Grid problems**: Each cell is a node; 4-directional neighbors are edges. Don't construct an explicit adjacency list — use a `get_neighbors(r, c)` function inline. Multi-source BFS (all `0`s at once) solves "distance to nearest 0" and "walls and gates" in O(R×C).

> [!TIP]
> **Bidirectional BFS**: For problems with a known source and target (Word Ladder, 6-degrees of separation), expand from both ends simultaneously. Meet in the middle. Explored nodes shrink from O(b^d) to O(b^(d/2)) where b = branching factor. Google Maps uses bidirectional Dijkstra for shortest route queries.

---

## 4. L3 Deep Dives

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



## Bellman-Ford Algorithm

> [!IMPORTANT]
> **When to use:** Dijkstra fails when edges have **negative weights**. Bellman-Ford handles them. Also use for **K-hop shortest paths** (flight problems with at most K stops).

Relax **all** edges exactly **V-1** times. After round `i`, `dist[v]` holds the shortest path using at most `i` edges.

**Negative Cycle Detection**: After V-1 rounds, do one more pass. If any edge can still relax, a negative cycle exists.

```python
def bellman_ford(n, edges, src):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return []   # negative cycle
    return dist
```

**K-Hop variant** (Cheapest Flights in K Stops): run only K+1 rounds and snapshot `dist` before each round (`temp = dist.copy()`) to prevent same-round chaining.

| | Value |
|---|---|
| Time | O(V · E) |
| Space | O(V) |

---

## See also

- [Union-Find](../02-algorithms/14-union-find.md) — DSU for Kruskal and connectivity
- [Patterns Master](../03-patterns/patterns-master.md) — graph pattern recognition triggers

## Flashcards

**Under what graph conditions is BFS guaranteed to find the shortest path, and what is the critical step to avoid redundant queue work?** #flashcard
BFS guarantees the shortest path only in **unweighted graphs** (or graphs with uniform edge weights). The critical step is marking a node as visited **before enqueuing** it (not after dequeuing) to prevent duplicate enqueueing of the same node from different paths.

**How does Kahn's algorithm perform topological sort and detect cycles in a directed graph?** #flashcard
1. Compute the `in_degree` of all vertices.
2. Queue all vertices with `in_degree == 0`.
3. Pop a vertex `u`, add it to the topological order, and decrement the `in_degree` of all its neighbors.
4. If a neighbor's `in_degree` drops to 0, queue it.
5. If the final topological order length is less than the total number of vertices $V$, a cycle exists.

**What is the Bidirectional BFS optimization, and how does it improve search complexity?** #flashcard
Bidirectional BFS runs two simultaneous searches: one forward from the source and one backward from the target, meeting in the middle. At each iteration, it expands the smaller queue's frontier. This reduces the search space size from $O(b^d)$ to $O(b^{d/2})$, where $b$ is the branching factor and $d$ is the distance.

**How does 0-1 BFS operate, and why is it preferred over Dijkstra's algorithm?** #flashcard
0-1 BFS finds the shortest path in $O(V + E)$ when edge weights are strictly 0 or 1. It uses a `deque`:
- If an edge has weight 0, append the neighbor to the **front** of the deque.
- If weight is 1, append to the **back**.
This keeps the deque sorted by distance without a min-heap, outperforming Dijkstra's $O(E \log V)$ time complexity.

**How does the 3-color DFS algorithm detect cycles in a directed graph?** #flashcard
Nodes are categorized into three states:
- **White (0)**: Unvisited.
- **Gray (1)**: Active (currently in the recursion stack).
- **Black (2)**: Fully processed (DFS completed for this node and all its descendants).
A cycle is detected if a neighbor is found in the **Gray** state during traversal.


**Shortest path, unweighted graph — what technique, and why?** #flashcard
BFS (level-by-level guarantees minimum hops).

**Shortest path, non-negative weights — what technique, and why?** #flashcard
Dijkstra with min-heap, O((V+E) log V).

**Shortest path with negative weights or detect negative cycles — what technique, and why?** #flashcard
Bellman-Ford, O(VE).

**All-pairs shortest paths, dense graph — what technique, and why?** #flashcard
Floyd-Warshall, O(V³).

**Detect cycle in directed graph / topological order — what technique, and why?** #flashcard
DFS with three-color marking or Kahn's BFS.

**Minimum spanning tree, sparse graph — what technique, and why?** #flashcard
Kruskal (sort edges + DSU); dense graph → Prim (min-heap).

**Graph is really a grid — what technique, and why?** #flashcard
treat cells as nodes, 4-directional edges; BFS for shortest path, DFS for components.
