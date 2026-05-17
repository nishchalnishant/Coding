# Union-Find (Disjoint Set Union) — SDE-3 Gold Standard

Near-O(1) amortized connectivity. SDE-3 focus: correct optimizations (path compression + union by rank), DSU variants (weighted ratios, rollback), Kruskal's MST, and distributed dynamic connectivity.

---

## Theory & Mental Models

**What it is.** Disjoint Set Union (DSU) is a data structure tracking which elements belong to the same connected component, supporting two operations: `find` (which component does x belong to?) and `union` (merge the components of x and y). Core invariant: each component is represented as a tree; the root is the component ID.

**Why it exists.** BFS/DFS answers connectivity in O(V + E) per query — expensive when connectivity is queried repeatedly after dynamic edge additions. DSU answers each union/find in amortized O(α(N)) ≈ O(1) by maintaining a compact forest structure with two optimizations.

**The mental model.** Each component is a tree; `find` walks to the root (component representative). Path compression flattens the tree so future `find` calls jump directly to the root. Union by rank attaches the shorter tree under the taller one to keep trees flat.

**Complexity at a glance.**

| Operation | Without optimizations | With path compression + union by rank |
| :--- | :--- | :--- |
| find(x) | O(N) worst | O(α(N)) ≈ O(1) |
| union(x, y) | O(N) worst | O(α(N)) ≈ O(1) |
| N operations total | O(N²) | O(N α(N)) ≈ O(N) |

α is the inverse Ackermann function — effectively ≤ 4 for all practical N.

**When to reach for it.**
- Detecting cycles in undirected graphs (if `find(u) == find(v)` before union → cycle).
- Connected components with dynamic edge additions.
- Kruskal's MST — greedily add cheapest edge that doesn't create a cycle.
- Checking if two nodes are in the same group after a series of merges.
- Grouping elements by shared properties (accounts merge, satisfiability of equations).

**When NOT to use it.**
- Edges are removed — standard DSU doesn't support deletions (use DSU with rollback for offline queries, or link-cut trees for fully dynamic).
- Directed graphs — DSU is for undirected connectivity; use DFS/topological sort for SCCs.
- You need the actual path between nodes — DSU only answers "same component?", not "what is the path?".

**Common mistakes.**
- Calling `find` without path compression — correct but degrades to O(N) without it; always use both optimizations together.
- Union by value rather than by rank — degrades tree balance to O(N) height.
- Not initializing `parent[i] = i` for all nodes — uninitialized parent causes infinite loops in `find`.
- Forgetting to check `find(u) != find(v)` before union in Kruskal — adding a cycle edge inflates MST cost.

---

## 1. Representation Choice

> [!IMPORTANT]
> **The Click Moment**: "Merge **groups**" — OR — "are two elements in the **same set**?" — OR — "**add edge, query connectivity** repeatedly" — OR — "**minimum spanning tree** (Kruskal)" — OR — "detect **cycle in undirected graph** without BFS/DFS". DSU is the choice when you need many union/find operations incrementally. Prefer DFS only for one-shot component counting with no subsequent updates.

| Approach | Find | Union | Best For |
| :--- | :--- | :--- | :--- |
| DSU (path compression + rank) | O(α(n)) ≈ O(1) | O(α(n)) | Dynamic connectivity, MST, grouping |
| DFS / BFS | O(V + E) per query | N/A | One-shot component counting |
| Adjacency matrix | O(V²) | O(1) | Dense, static graphs with edge lookups |

α(n) is the inverse Ackermann function — practically constant (≤ 4) for any n that fits in memory.

```python
class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # already connected — cycle detected in undirected graph
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def component_size(self, x: int) -> int:
        return self.size[self.find(x)]

#### Common Variants & Twists
1. **Longest Consecutive Sequence**:
   - **What (The Problem & Goal):** Given an unsorted array, find the length of the longest consecutive elements sequence.
   - **How (Intuition & Mental Model):** For each `x` in the array, if `x+1` exists, `union(x, x+1)`. After processing all elements, the size of the largest component is the answer. (Note: Hash Set is the standard O(N) approach, but DSU is a valid alternative).
2. **Number of Provinces**:
   - **What (The Problem & Goal):** Given an adjacency matrix, find the total number of connected components.
   - **How (Intuition & Mental Model):** Iterate through the upper triangle of the matrix. If `matrix[i][j] == 1`, `union(i, j)`. The number of components remaining in the DSU is the answer.
```

---

## 2. Core Patterns & Click Moments

### Cycle Detection — Undirected Graph

> [!IMPORTANT]
> **The Click Moment**: "Add edge (u, v); check if this **creates a cycle**". Before `union(u, v)`, if `find(u) == find(v)`, they are already in the same component — adding this edge creates a cycle. This is the engine of Kruskal's MST.

```python
def has_cycle_undirected(n: int, edges: list[tuple[int, int]]) -> bool:
    dsu = DSU(n)
    for u, v in edges:
        if not dsu.union(u, v):  # union returns False when already connected
            return True
    return False
```

---

### Kruskal's Minimum Spanning Tree

> [!IMPORTANT]
> **The Click Moment**: "**Minimum cost to connect** all nodes" — OR — "minimum spanning tree" with sparse graph and edge list. Sort edges ascending by weight; greedily add the cheapest edge that doesn't form a cycle. O(E log E) dominated by the sort.

```python
def kruskal_mst(n: int, edges: list[tuple[int, int, int]]) -> int:
    edges.sort(key=lambda e: e[2])
    dsu = DSU(n)
    total_cost = edges_used = 0
    for u, v, w in edges:
        if dsu.union(u, v):
            total_cost += w
            edges_used += 1
            if edges_used == n - 1:
                break
    return total_cost if edges_used == n - 1 else -1  # -1 = disconnected graph

#### Common Variants & Twists
1. **Min Cost to Connect All Points**:
   - **What (The Problem & Goal):** Connect points on a 2D plane with Manhattan distance cost.
   - **How (Intuition & Mental Model):** This is a complete graph where edges exist between every pair of points. Generate all `N*(N-1)/2` edges, sort them, and use Kruskal's with DSU. 
2. **Find Critical and Pseudo-Critical Edges in MST**:
   - **What (The Problem & Goal):** An edge is critical if its removal increases MST weight. It's pseudo-critical if it can be part of *some* MST.
   - **How (Intuition & Mental Model):** For each edge, first force its inclusion and compute MST; then force its exclusion and compute MST. Compare these weights with the original MST weight.
```

---

### Weighted DSU — Variable Ratios (Evaluate Division)

> [!IMPORTANT]
> **The Click Moment**: "Variables with **ratios** (a/b = 2.0)" — OR — "**Evaluate Division** (find a/c given a/b and b/c)". Store a `weight` per node = ratio relative to its root. On `find`, accumulate the product along the path. On `union`, adjust so both roots share a consistent ratio.

```python
class WeightedDSU:
    def __init__(self, keys: list) -> None:
        self.parent = {k: k for k in keys}
        self.weight = {k: 1.0 for k in keys}  # weight[x] = value(x) / value(parent[x])

    def find(self, x) -> tuple:
        if self.parent[x] != x:
            root, w = self.find(self.parent[x])
            self.parent[x] = root
            self.weight[x] *= w
        return self.parent[x], self.weight[x]

    def union(self, x, y, ratio: float) -> None:
        rx, wx = self.find(x)
        ry, wy = self.find(y)
        if rx != ry:
            self.parent[rx] = ry
            self.weight[rx] = ratio * wy / wx

    def query(self, x, y) -> float:
        if x not in self.parent or y not in self.parent:
            return -1.0
        rx, wx = self.find(x)
        ry, wy = self.find(y)
        return wx / wy if rx == ry else -1.0

#### Common Variants & Twists
1. **Path with Maximum Probability**:
   - **What (The Problem & Goal):** Find the path with the maximum product of edge probabilities.
   - **How (Intuition & Mental Model):** While Dijkstra is usually better, for static queries on a tree, a weighted DSU can track products of probabilities relative to the root. If `a/root = p1` and `b/root = p2`, then `a/b = p1/p2`.
```

---

### DSU with Rollback — Offline Dynamic Connectivity

> [!IMPORTANT]
> **The Click Moment**: "**Undo** a union operation" — OR — "offline queries where you need to **revert** some merges". DSU with rollback uses union by rank **without path compression** — compression mutates intermediate parent pointers, making rollback impossible without recording the full chain.

```python
class RollbackDSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self._history: list = []

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            x = self.parent[x]  # NO path compression — breaks rollback
        return x

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            self._history.append(None)
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self._history.append((ry, self.parent[ry], rx, self.rank[rx]))
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True

    def rollback(self) -> None:
        entry = self._history.pop()
        if entry is not None:
            ry, old_parent, rx, old_rank = entry
            self.parent[ry] = old_parent
            self.rank[rx] = old_rank

#### Common Variants & Twists
1. **Number of Islands II**:
   - **What (The Problem & Goal):** Dynamic land additions in a grid; return component count after each.
   - **How (Intuition & Mental Model):** Standard DSU on `r * cols + c`. On each `addLand(r, c)`, check 4-neighbors. If a neighbor is land, `union(current, neighbor)`. This handles the dynamic component counting as the grid evolves.
```

> [!CAUTION]
> **No path compression in rollback DSU.** Without compression, `find` is O(log n) per call (union by rank bounds tree height to log n). This is an acceptable trade-off for offline queries. The O(α(n)) guarantee of the standard DSU requires both optimizations together.

---

## 3. SDE-3 Deep Dives

### Scalability: Parallel DSU

> [!TIP]
> For distributed graphs (billions of nodes): the **Shiloach-Vishkin** algorithm runs DSU in parallel. Each node races to link to a neighbor with a smaller label using atomic compare-and-swap on parent pointers. Converges in O(log n) rounds with O((n + E) / P) work per round where P = processors. Used in graph processing frameworks like GraphX (Spark) and Ligra.

### Scalability: Dynamic Connectivity with Deletions

> [!TIP]
> Standard DSU handles edge additions but not deletions. For **fully dynamic connectivity** (add and delete edges): use **link-cut trees** (O(log n) per operation) or process offline in reverse (deletions become additions when processed right-to-left). For online deletions, the best practical solution is **Et-trees** (Euler tour trees), used in research graph databases.

### Concurrency: Lock-Free DSU

> [!TIP]
> Lock-free DSU uses **CAS (compare-and-swap)** on parent pointers: `parent[x].compareAndSet(x, root)`. Race conditions in path compression are benign — multiple threads may write the same compressed path, but all compressed values are valid roots. Union requires a CAS retry loop: read both roots, attempt to update the smaller-rank root's parent. If the CAS fails, retry. This is the approach in the Ligra parallel graph framework (C++) and is feasible in Java via `AtomicIntegerArray`.

### Trade-offs: DSU vs Alternatives

| Need | DSU | BFS/DFS | Link-Cut Tree |
| :--- | :--- | :--- | :--- |
| Dynamic connectivity (add edge) | ✅ O(α(n)) | ❌ O(V+E) per query | ✅ O(log n) |
| Dynamic connectivity (delete edge) | ❌ Not supported | ❌ O(V+E) per query | ✅ O(log n) |
| One-shot component count | Overkill | ✅ Simpler code | Overkill |
| MST (Kruskal) | ✅ Canonical | ❌ Not applicable | ❌ Complex |
| Rollback / time travel | ✅ With modification | ❌ Not natural | ✅ Native |

---

## 4. Common Interview Problems

### Medium (High Frequency)
- **Number of Connected Components** — DSU; initialize `components = n`; decrement on successful union.
- **[Redundant Connection](problem-deep-dives.md#redundant-connection)** — Process edges; return the first where `find(u) == find(v)` before union.
- **[Accounts Merge](problem-deep-dives.md#accounts-merge)** — Union emails within each account; group by DSU root; sort emails per group.
- **Graph Valid Tree** — n nodes, n-1 edges, single component ↔ tree.
- **Satisfiability of Equations** — Union all `==` pairs first; then check all `!=` pairs.

### Hard
- **Number of Islands II** — Dynamic: add land cells one-by-one; union 4-neighbors; return component count after each addition.
- **Minimize Malware Spread** — DSU for component sizes; remove the node whose unique malware source covers the largest component.
- **[Evaluate Division](problem-deep-dives.md#evaluate-division)** — Weighted DSU; ratios as edge weights; query accumulates product path.
- **Smallest String With Swaps** — DSU on index pairs; sort characters lexicographically within each component.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **[Redundant Connection](problem-deep-dives.md#redundant-connection)** | DSU Cycle Detection | "Undirected tree + one extra edge = cycle" | Process edges; first where `find(u)==find(v)` before union is the answer | Return **last** such edge in input order; directed variant (Course Schedule) uses topo sort. |
| **Number of Islands II** | "Dynamic land additions; track component count" | DSU over 2D grid → 1D index `r*cols+c`; union 4-neighbors each add | Check bounds before union. Duplicate queries (same cell added twice) must not double-decrement count. |
| **Accounts Merge** | "Same email = same person across accounts" | Union all emails within each account; group by DSU root; sort | Email is the DSU element (not account name). Map `email → integer index` first. |
| **Kruskal MST** | "Min cost to connect all nodes" | Sort edges by weight; add edge if `union(u,v)` succeeds; stop at n-1 edges | Disconnected graph → return -1. Parallel edges → take cheapest; DSU handles duplicates naturally. |
| **Satisfiability of Equations** | "Equality constraints + inequality checks" | Union all `==` pairs; then verify no `!=` pair shares a root | **Two-pass is mandatory**: process all `==` before any `!=`. Single-pass fails on ordering. |
| **Largest Component by Common Factor** | "Numbers sharing a prime factor → same group" | Sieve + DSU: for each prime factor, union all indices divisible by it | `value=1` has no prime factors — isolated node. Sieve factorization O(N log log N). |
| **Smallest String With Swaps** | "Swap any indices in a given pair repeatedly" | DSU on index pairs; sort chars within each connected component lexicographically | Transitivity: if (0,1) and (1,2) are pairs, indices 0,1,2 are all in the same component. |
| **Graph Valid Tree** | "Is this graph a tree?" | DSU: n nodes, n-1 edges, no cycle ↔ tree | Check **both**: no cycle (n-1 successful unions) **and** connected (`components == 1`). |
| **Find if Path Exists [E]** | "Is there any path between source and destination?" | DSU: union all edges; check `find(src) == find(dst)` | BFS/DFS also works; DSU is one-liner if already built. |
| **Number of Provinces [E]** | "Count connected components in adjacency matrix" | DSU or DFS; union all `isConnected[i][j]==1` pairs | Adjacency matrix input — iterate upper triangle only to avoid double-unioning. |
| **Largest Component Size by Common Factor [M]** | "Numbers sharing a prime factor belong to same group" | Sieve factorization; DSU union index with each prime factor node | `value=1` has no prime factors — isolated. Map prime factors to a synthetic node range above n. |
| **Regions Cut by Slashes [M]** | "Count regions in grid divided by '/' and '\\' slashes" | Divide each cell into 4 triangles; union based on slash type and adjacency | Expand each cell into 4 sub-cells (top, right, bottom, left); '/' splits top-right from bottom-left. |
| **Number of Operations to Make Network Connected [M]** | "Minimum cable moves to connect all computers" | Count components C and extra edges E; answer = C-1 if E >= C-1 | Need at least n-1 edges total. Extra edges = edges beyond n-1 MST edges. Return -1 if extras < components-1. |
| **Minimize Malware Spread [H]** | "Remove one initial malware node to minimize spread" | DSU for component sizes; pick node whose removal saves the largest component | Only nodes that are the **sole** malware source in their component help. Multiple malware nodes in one component = no savings from removing one. |
| **Swim in Rising Water [H]** | "Minimum time to reach bottom-right as water rises" | Binary search on time + DSU/BFS; or Dijkstra with `max(path)` as cost | Union-Find: at time T, union all cells with elevation ≤ T; check if (0,0) and (n-1,n-1) are connected. |

---

## Quick Revision Triggers

- "Are two elements in the same group after a series of merges?" → DSU `find(x) == find(y)`.
- "Add edges one by one; query connectivity after each addition" → DSU; O(α(N)) per operation.
- "Detect cycle in undirected graph without BFS/DFS" → DSU; `union` returns False when already connected.
- "Minimum spanning tree with sparse edge list" → Kruskal: sort edges, DSU for cycle detection.
- "Group accounts / emails by shared identifier" → DSU on the shared element (email), not the container (account).
- "Need to undo a union (offline queries)" → rollback DSU: union by rank only, no path compression.
- "Variables with ratios (a/b = k)" → weighted DSU storing ratio relative to root; accumulate on path compression.

---

## See also

- [Graph Algorithms](graph.md) — Kruskal; when DSU vs BFS/DFS for connectivity
- [Sorting](sorting.md) — edge sorting for Kruskal
- [Patterns Master](../../../reference/patterns/patterns-master.md) — DSU pattern recognition triggers
