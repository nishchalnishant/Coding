# Union Find (Disjoint Set Union) — SDE-3 Level

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

## 6. SDE-3 Level Thinking

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

## See also

- [Graph](graph.md) — Kruskal, connectivity  
- [Sorting](sorting.md) — edge sorting for Kruskal  
- [advanced-graphs.md](../../advanced-dsa/advanced-graphs.md) — bridges (different technique)
