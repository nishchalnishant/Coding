---
tags: [coding, algorithms, union-find]
topic: Union-Find (DSU)
difficulty: mixed
---

# Union-Find (DSU) — Amazon SDE-2

---

## DSU Template

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False          # already connected — cycle in undirected graph
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx      # union by rank
        self.size[rx] += self.size[ry]
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def component_size(self, x):
        return self.size[self.find(x)]
```

**Key invariants**:
- Path compression: `find` flattens tree to root. Each subsequent `find` is near-O(1).
- Union by rank: always attach smaller tree under larger. Keeps tree height at O(log n).
- Combined: amortized O(α(n)) per operation — effectively O(1) for all practical n.

---

## When to Use DSU vs BFS/DFS

| Situation | Use DSU | Use BFS/DFS |
|---|---|---|
| Edges arrive dynamically (online) | Yes | No — re-running is O(V+E) each time |
| Static graph, one-shot component count | Either | Simpler code |
| Need shortest path | No | Yes (BFS) |
| Cycle detection (undirected) | Yes — `union` returns False | Yes |
| Connected components count | Yes — `components` counter | Yes |
| Need path (not just connectivity) | No | Yes |

---

## Core Operations

### Path Compression

`find` with path compression: every node on the find-path points directly to the root after the call. Recursive form:

```python
def find(self, x):
    if self.parent[x] != x:
        self.parent[x] = self.find(self.parent[x])
    return self.parent[x]
```

Iterative (avoids recursion stack):

```python
def find(self, x):
    root = x
    while self.parent[root] != root:
        root = self.parent[root]
    while self.parent[x] != root:
        self.parent[x], x = root, self.parent[x]
    return root
```

### Union by Rank

Always attach the tree with smaller rank under the one with larger rank. Rank is an upper bound on tree height. Only increases rank when two trees of equal rank merge.

---

## Cycle Detection in Undirected Graph

`union(u, v)` returns `False` when `u` and `v` are already in the same component — meaning edge `(u, v)` would create a cycle.

```python
def has_cycle(n, edges):
    dsu = DSU(n)
    for u, v in edges:
        if not dsu.union(u, v):
            return True   # cycle detected
    return False
```

---

## Number of Connected Components

### Number of Connected Components in an Undirected Graph

> [!example] Problem
> Given n nodes and a list of edges, return the number of connected components. LeetCode 323.

> [!note]- Python Solution
> ```python
> def count_components(n, edges):
>     dsu = DSU(n)
>     for u, v in edges:
>         dsu.union(u, v)
>     return dsu.components
> ```

> [!success] Complexity
> Time O((V + E)·α(V)) | Space O(V).

---

### Number of Provinces

> [!example] Problem
> Given n×n adjacency matrix `isConnected`, return the number of provinces (connected components). LeetCode 547.

> [!info] Approach
> Iterate upper triangle, union connected pairs. Only upper triangle to avoid double-counting.

> [!note]- Python Solution
> ```python
> def find_circle_num(isConnected):
>     n = len(isConnected)
>     dsu = DSU(n)
>     for i in range(n):
>         for j in range(i + 1, n):
>             if isConnected[i][j] == 1:
>                 dsu.union(i, j)
>     return dsu.components
> ```

> [!success] Complexity
> Time O(V²·α(V)) | Space O(V).

---

### Graph Valid Tree

> [!example] Problem
> Given n nodes and edges, return true if they form a valid tree. LeetCode 261.

> [!info] Approach
> A valid tree on n nodes has exactly n-1 edges, is connected, and has no cycles. Short-circuit: if `len(edges) != n-1`, return False immediately. Then DSU: any cycle → False; must end with 1 component.

> [!note]- Python Solution
> ```python
> def valid_tree(n, edges):
>     if len(edges) != n - 1:
>         return False
>     dsu = DSU(n)
>     for u, v in edges:
>         if not dsu.union(u, v):
>             return False        # cycle detected
>     return dsu.components == 1
> ```

> [!success] Complexity
> Time O(E·α(V)) | Space O(V).

---

## DSU for Practical Amazon Problems

---

### Accounts Merge

> [!example] Problem
> Merge accounts that share any email address. Return sorted email lists per merged account. LeetCode 721.

> [!info] Approach
> Emails are the identity key. Union all emails within an account under the first email. After all unions, group emails by DSU root.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def accounts_merge(accounts):
>     email_to_idx = {}
>     email_to_name = {}
>     for account in accounts:
>         name = account[0]
>         for email in account[1:]:
>             if email not in email_to_idx:
>                 email_to_idx[email] = len(email_to_idx)
>             email_to_name[email] = name
>
>     dsu = DSU(len(email_to_idx))
>     for account in accounts:
>         first_idx = email_to_idx[account[1]]
>         for email in account[2:]:
>             dsu.union(first_idx, email_to_idx[email])
>
>     root_to_emails = defaultdict(list)
>     for email, idx in email_to_idx.items():
>         root_to_emails[dsu.find(idx)].append(email)
>
>     return [[email_to_name[emails[0]]] + sorted(emails)
>             for emails in root_to_emails.values()]
> ```

> [!success] Complexity
> Time O(N·K·log(N·K)) dominated by sorting | Space O(N·K).

> [!tip] Alternatives
> BFS on email adjacency graph — same complexity, more setup.

---

### Satisfiability of Equality Equations

> [!example] Problem
> Given equations like `"a==b"` and `"a!=b"`, return true if all can be satisfied simultaneously. LeetCode 990.

> [!info] Approach
> Two passes: first union all `==` pairs (transitivity), then verify no `!=` pair has both sides in the same component.

> [!note]- Python Solution
> ```python
> def equations_possible(equations):
>     dsu = DSU(26)
>     for eq in equations:
>         if eq[1] == '=':
>             dsu.union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))
>     for eq in equations:
>         if eq[1] == '!':
>             if dsu.connected(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a')):
>                 return False
>     return True
> ```

> [!success] Complexity
> Time O(1) (26 letters) | Space O(1).

---

### Smallest String With Swaps

> [!example] Problem
> Given string s and swap-allowed index pairs, return the lexicographically smallest string achievable. LeetCode 1202.

> [!info] Approach
> Swap pairs are transitive — connected indices form a free-rearrangement group. Union all paired indices. Within each component, sort characters and assign them to sorted index positions.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def smallest_string_with_swaps(s, pairs):
>     n = len(s)
>     dsu = DSU(n)
>     for u, v in pairs:
>         dsu.union(u, v)
>
>     root_to_indices = defaultdict(list)
>     for i in range(n):
>         root_to_indices[dsu.find(i)].append(i)
>
>     result = list(s)
>     for indices in root_to_indices.values():
>         chars = sorted(s[i] for i in indices)
>         for i, c in zip(sorted(indices), chars):
>             result[i] = c
>     return "".join(result)
> ```

> [!success] Complexity
> Time O((N + E)·α(N) + N·log N) | Space O(N).

---

### Making a Large Island

> [!example] Problem
> n×n binary grid; flip at most one 0 to 1. Return the largest island size. LeetCode 827.

> [!info] Approach
> Build DSU over existing 1-cells. For each 0-cell, collect unique DSU roots of neighboring 1-cells, sum their sizes + 1. Use DSU component sizes for O(1) lookup.

> [!note]- Python Solution
> ```python
> def largest_island(grid):
>     n = len(grid)
>     dsu = DSU(n * n)
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
>
>     for r in range(n):
>         for c in range(n):
>             if grid[r][c] == 1:
>                 for dr, dc in dirs:
>                     nr, nc = r + dr, c + dc
>                     if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
>                         dsu.union(r*n+c, nr*n+nc)
>
>     best = max((dsu.component_size(r*n+c)
>                 for r in range(n) for c in range(n) if grid[r][c] == 1), default=0)
>
>     for r in range(n):
>         for c in range(n):
>             if grid[r][c] == 0:
>                 seen = set()
>                 gain = 1
>                 for dr, dc in dirs:
>                     nr, nc = r + dr, c + dc
>                     if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
>                         root = dsu.find(nr*n+nc)
>                         if root not in seen:
>                             gain += dsu.component_size(nr*n+nc)
>                             seen.add(root)
>                 best = max(best, gain)
>     return best
> ```

> [!success] Complexity
> Time O(N²·α(N²)) ≈ O(N²) | Space O(N²).

---

### Redundant Connection (Undirected)

> [!example] Problem
> Given a tree of n nodes with one extra edge added, find the redundant edge. LeetCode 684.

> [!info] Approach
> Process edges in order. The first edge whose `union` returns False (both nodes already connected) is the redundant one.

> [!note]- Python Solution
> ```python
> def find_redundant_connection(edges):
>     n = len(edges)
>     dsu = DSU(n + 1)
>     for u, v in edges:
>         if not dsu.union(u, v):
>             return [u, v]
>     return []
> ```

> [!success] Complexity
> Time O(N·α(N)) | Space O(N).

---

## MST with Kruskal's (DSU Application)

Kruskal's algorithm builds MST by sorting edges and greedily adding the cheapest edge that doesn't form a cycle — the cycle check is `dsu.union`.

### Min Cost to Connect All Points

> [!example] Problem
> Connect all points with minimum total Manhattan distance. LeetCode 1584.

> [!note]- Python Solution
> ```python
> def min_cost_connect_points(points):
>     n = len(points)
>     edges = []
>     for i in range(n):
>         for j in range(i + 1, n):
>             dist = abs(points[i][0]-points[j][0]) + abs(points[i][1]-points[j][1])
>             edges.append((dist, i, j))
>     edges.sort()
>     dsu = DSU(n)
>     total = edges_used = 0
>     for dist, i, j in edges:
>         if dsu.union(i, j):
>             total += dist
>             edges_used += 1
>             if edges_used == n - 1:
>                 break
>     return total
> ```

> [!success] Complexity
> Time O(N²·log N) dominated by sorting | Space O(N²).

> [!tip] Alternatives
> Prim's with simple array — O(N²), avoids materializing all edges. Better for large N.

---

## See Also

[[graph]] | [[graph-algorithms]] | [[sorting]]
