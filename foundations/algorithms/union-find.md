# Union Find (Disjoint Set Union) — SDE-2+ Level

Maintain disjoint sets with near O(1) amortized union and find using path compression and union by rank. Essential for connectivity, MST (Kruskal), and dynamic connectivity.

---

## 1. Concept Overview

**Problem space**: Connected components (undirected graph), cycle detection in graph, Kruskal's MST, dynamic connectivity ("add edge", "are u and v connected?"), grouping (accounts merge, etc.).

**When to use**: "Merge sets" / "are two elements in same set?" with many such operations. Prefer over DFS when you need to repeatedly add edges and query connectivity.

---

## 2. Core Algorithms

### Find (with path compression)
- Follow parent until root; optionally set parent[x] = root for all on path (path compression). Amortized O(α(n)) ≈ O(1).

### Union (by rank)
- Find roots of x and y. If same, return. Else attach smaller rank under larger; if equal, increment one rank. Amortized O(α(n)).

### Full DSU

More SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/union_find.py`.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True
```

---

## 3. Advanced Variations

- **Size of component**: Maintain `size[root]`; on union, add smaller size to larger.
- **Count components**: Initially n; decrement on successful union.
- **DSU with rollback**: For "offline" queries (e.g., process in order and undo); keep history of parent changes to revert.
- **Kruskal**: Sort edges by weight; add edge if union(u,v) is true; repeat until n-1 edges. MST weight = sum of added edge weights.

### Edge Cases
- Empty graph; single node; multiple edges same weight (order can affect which MST); disconnected graph (MST not possible, count components).

---

## 4. Common Interview Problems

**Medium**: Number of Connected Components, Redundant Connection, Accounts Merge, Number of Islands (can use DSU instead of DFS).  
**Hard**: Longest Consecutive Sequence (DSU over indices), Critical Connections (bridges — use DFS/Tarjan, not DSU), Minimize Malware Spread.

---

## 5. Pattern Recognition

- **Connectivity**: "Same component" / "merge groups" → DSU. "Count components after adding/removing edges" → DSU or DFS.
- **MST**: Kruskal = sort edges + DSU to avoid cycles.
- **Cycle in undirected graph**: Add edge (u,v); if find(u)==find(v) before union, cycle.

---

## 6. Trade-offs & Scaling (optional)

- **Trade-offs**: DSU vs DFS for connectivity — DSU supports incremental edges and many queries; DFS is simpler for one-shot "count components". Complexity: α(n) ≈ 4 for practical n.
- **Memory**: O(N) for parent and rank. With rollback, store history (stack of (node, old_parent)).

---

## 7. Interview Strategy

- **Identify**: "Merge sets", "connected", "add edge and query" → DSU. "MST" → Kruskal + DSU.
- **Common mistakes**: Forgetting path compression or union by rank (still correct but slower); wrong indexing (0 vs 1-based).

---

## 8. Quick Revision

- **Formulas**: find: follow parent, compress. union: by rank (smaller under larger).
- **Tricks**: Count components = number of roots (parent[i]==i). Kruskal: sort edges, add if union succeeds.
- **Edge cases**: Single node; duplicate edges; disconnected.
- **Pattern tip**: "Same group" / "merge" / "MST" → think DSU.

---

## 9. Java sketch (interviews)

```java
class DSU {
    int[] parent, rank;
    DSU(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    boolean union(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return false;
        if (rank[rx] < rank[ry]) { parent[rx] = ry; }
        else if (rank[rx] > rank[ry]) { parent[ry] = rx; }
        else { parent[ry] = rx; rank[rx]++; }
        return true;
    }
}
```

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **[Redundant Connection](../../google-sde2/PROBLEM_DETAILS.md#redundant-connection)** | Process edges; **union(u,v)**; if already same set → **that edge** closes cycle (undirected tree + one edge). | **Return last** edge in problem order; **directed** variant is harder (see graph.md). |
| **Number of Islands II** | DSU over **water**; as land added, **union** with 4 neighbors; track **component count** delta. | **2D → 1D** index `r*cols+c`; **dynamic** connectivity vs static flood fill. |
| **Accounts Merge** | Union all emails in same account; **map email → root**; collect emails per root; sort. | **Same email** across accounts merges; **disjoint** names handled by union. |
| **Kruskal MST** | Sort edges by weight; add if **find(u)≠find(v)**; **union**; stop when `n-1` edges. | **Disconnected** graph—MST not spanning all; **parallel** edges. |
| **Satisfiability of Equations** | **Union** `a==b`; for `a!=b` check `find(a)==find(b)` → false. | **Path compression** + **union by rank** for α(n) amortized. |
| **Largest Component by Common Factor** | For each prime `p`, union all indices whose value divisible by `p` (or use gcd edges). | **Sieve** factorization; **value 1** has no prime factors—handle alone. |
| **Smallest String With Swaps** | Union **indices** in same pair; each connected component **sort** chars lexicographically. | **Greedy** per component after DSU groups. |
| **Graph Valid Tree** | **n nodes, n-1 edges** and **fully connected** ⇔ tree; DSU verify no cycle and one component. | **Cycle** detection vs **disconnected**. |

---

## See also

- [Graph](graph.md) — Kruskal, connectivity; when DSU vs BFS  
- [Sorting](sorting.md) — edge order for Kruskal  
- [advanced-graphs.md](../../advanced-dsa/advanced-graphs.md) — bridges (Tarjan, not DSU)
