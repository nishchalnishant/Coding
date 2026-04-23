# Union-Find (Disjoint Set Union) — SDE-3 Gold Standard

Near-O(1) amortized connectivity. SDE-3 focus: correct optimizations (path compression + union by rank), DSU variants (weighted ratios, rollback), Kruskal's MST, and distributed dynamic connectivity.

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
- **[Redundant Connection](../../google-sde2/PROBLEM_DETAILS.md#redundant-connection)** — Process edges; return the first where `find(u) == find(v)` before union.
- **[Accounts Merge](../../google-sde2/PROBLEM_DETAILS.md#accounts-merge)** — Union emails within each account; group by DSU root; sort emails per group.
- **Graph Valid Tree** — n nodes, n-1 edges, single component ↔ tree.
- **Satisfiability of Equations** — Union all `==` pairs first; then check all `!=` pairs.

### Hard
- **Number of Islands II** — Dynamic: add land cells one-by-one; union 4-neighbors; return component count after each addition.
- **Minimize Malware Spread** — DSU for component sizes; remove the node whose unique malware source covers the largest component.
- **[Evaluate Division](../../google-sde2/PROBLEM_DETAILS.md#evaluate-division)** — Weighted DSU; ratios as edge weights; query accumulates product path.
- **Smallest String With Swaps** — DSU on index pairs; sort characters lexicographically within each component.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Redundant Connection](../../google-sde2/PROBLEM_DETAILS.md#redundant-connection)** | "Undirected tree + one extra edge = cycle" | Process edges; first where `find(u)==find(v)` before union is the answer | Return **last** such edge in input order; directed variant (Course Schedule) uses topo sort. |
| **Number of Islands II** | "Dynamic land additions; track component count" | DSU over 2D grid → 1D index `r*cols+c`; union 4-neighbors each add | Check bounds before union. Duplicate queries (same cell added twice) must not double-decrement count. |
| **Accounts Merge** | "Same email = same person across accounts" | Union all emails within each account; group by DSU root; sort | Email is the DSU element (not account name). Map `email → integer index` first. |
| **Kruskal MST** | "Min cost to connect all nodes" | Sort edges by weight; add edge if `union(u,v)` succeeds; stop at n-1 edges | Disconnected graph → return -1. Parallel edges → take cheapest; DSU handles duplicates naturally. |
| **Satisfiability of Equations** | "Equality constraints + inequality checks" | Union all `==` pairs; then verify no `!=` pair shares a root | **Two-pass is mandatory**: process all `==` before any `!=`. Single-pass fails on ordering. |
| **Largest Component by Common Factor** | "Numbers sharing a prime factor → same group" | Sieve + DSU: for each prime factor, union all indices divisible by it | `value=1` has no prime factors — isolated node. Sieve factorization O(N log log N). |
| **Smallest String With Swaps** | "Swap any indices in a given pair repeatedly" | DSU on index pairs; sort chars within each connected component lexicographically | Transitivity: if (0,1) and (1,2) are pairs, indices 0,1,2 are all in the same component. |
| **Graph Valid Tree** | "Is this graph a tree?" | DSU: n nodes, n-1 edges, no cycle ↔ tree | Check **both**: no cycle (n-1 successful unions) **and** connected (`components == 1`). |

---

## See also

- [Graph Algorithms](graph.md) — Kruskal; when DSU vs BFS/DFS for connectivity
- [Sorting](sorting.md) — edge sorting for Kruskal
- [Patterns Master](../../../reference/patterns/patterns-master.md) — DSU pattern recognition triggers
