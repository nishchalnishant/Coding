---
tags: [coding, algorithms, union-find]
topic: Union-Find (DSU)
difficulty: mixed
---

# Union-Find — Problem Deep Dives

---

## DSU Template

> [!note]- DSU Class (Python)
> ```python
> class DSU:
>     def __init__(self, n: int) -> None:
>         self.parent = list(range(n))
>         self.rank = [0] * n
>         self.size = [1] * n
>         self.components = n
> 
>     def find(self, x: int) -> int:
>         if self.parent[x] != x:
>             self.parent[x] = self.find(self.parent[x])  # path compression
>         return self.parent[x]
> 
>     def union(self, x: int, y: int) -> bool:
>         rx, ry = self.find(x), self.find(y)
>         if rx == ry:
>             return False          # already connected; cycle in undirected graph
>         if self.rank[rx] < self.rank[ry]:
>             rx, ry = ry, rx
>         self.parent[ry] = rx
>         self.size[rx] += self.size[ry]
>         if self.rank[rx] == self.rank[ry]:
>             self.rank[rx] += 1
>         self.components -= 1
>         return True
> 
>     def connected(self, x: int, y: int) -> bool:
>         return self.find(x) == self.find(y)
> 
>     def component_size(self, x: int) -> int:
>         return self.size[self.find(x)]
> ```

> [!info] Core Invariants
> All nodes in the same component share the same root after `find`. Path compression + union by rank gives amortized O(α(n)) ≈ O(1) per operation.

---

## Basic Union-Find

### Number of Connected Components in an Undirected Graph

> [!example] Problem
> `n` nodes, list of undirected edges. Return number of connected components.

> [!info] Approach
> - **WHY:** BFS/DFS counts components in O(V+E) per call — fine for one-shot. DSU enables incremental edge-addition with O(α) per union/query. Here they're equivalent; DSU is the canonical pattern.
> - **WHAT:** Union all edges; answer = `dsu.components`.
> - **HOW:** Initialize `components = n`; decrement by 1 on each successful union.

> [!note]- Python Solution
> ```python
> def countComponents(n: int, edges: list[list[int]]) -> int:
>     dsu = DSU(n)
>     for u, v in edges:
>         dsu.union(u, v)
>     return dsu.components
> ```

> [!success] Complexity
> Time O((V + E)·α(V)) ≈ O(V + E), Space O(V).

> [!tip] Alternatives
> DFS/BFS — same time, simpler for one-shot. DSU preferred when edges arrive dynamically.

---

### Number of Provinces (Matrix Form)

> [!example] Problem
> `n` cities, adjacency matrix `isConnected`. Return number of provinces (connected components).

> [!info] Approach
> - **WHY:** Adjacency matrix encodes undirected edges. Treat `isConnected[i][j] == 1` as edge `(i, j)`.
> - **WHAT:** Iterate upper triangle, union connected pairs; count components.
> - **HOW:** Only process upper triangle (`j > i`) to avoid redundant unions and double-decrementing.

> [!note]- Python Solution
> ```python
> def findCircleNum(isConnected: list[list[int]]) -> int:
>     n = len(isConnected)
>     dsu = DSU(n)
>     for i in range(n):
>         for j in range(i + 1, n):    # upper triangle only
>             if isConnected[i][j] == 1:
>                 dsu.union(i, j)
>     return dsu.components
> ```

> [!success] Complexity
> Time O(V²·α(V)) ≈ O(V²), Space O(V).

> [!tip] Alternatives
> DFS on adjacency matrix — same O(V²). DSU more explicit about component counting.

---

### Graph Valid Tree

> [!example] Problem
> `n` nodes, list of undirected edges. Determine if the graph forms a valid tree.

> [!info] Approach
> - **WHY:** A valid tree on `n` nodes has exactly `n-1` edges and no cycles — equivalently, it is connected and acyclic.
> - **WHAT:** DSU cycle detection + single-component check.
> - **HOW:** Short-circuit if `len(edges) != n-1`. Process edges; if any union returns `False` (cycle) → not a tree.

> [!note]- Python Solution
> ```python
> def validTree(n: int, edges: list[list[int]]) -> bool:
>     if len(edges) != n - 1:
>         return False            # necessary condition
>     dsu = DSU(n)
>     for u, v in edges:
>         if not dsu.union(u, v):
>             return False        # cycle detected
>     return dsu.components == 1
> ```

> [!success] Complexity
> Time O(E·α(V)) ≈ O(E), Space O(V).

> [!tip] Alternatives
> DFS — check connected + no cycle. Both correct; DSU is more declarative.

---

### Redundant Connection

> [!example] Problem
> Undirected tree + one extra edge (exactly one cycle). Return the redundant edge.

> [!info] Approach
> - **WHY:** The redundant edge is the first edge where both endpoints are already connected when processed in input order. That is a DSU cycle-detection query.
> - **WHAT:** Process edges in order; return the first `(u, v)` where `find(u) == find(v)` before union.
> - **HOW:** `union` returns `False` when already connected → that's the answer.

> [!note]- Python Solution
> ```python
> def findRedundantConnection(edges: list[list[int]]) -> list[int]:
>     n = len(edges)
>     dsu = DSU(n + 1)
>     for u, v in edges:
>         if not dsu.union(u, v):
>             return [u, v]
>     return []
> ```

> [!success] Complexity
> Time O(N·α(N)) ≈ O(N), Space O(N).

> [!tip] Alternatives
> DFS cycle detection — O(N²) overall. DSU is O(N) and canonical.

---

### Satisfiability of Equality Equations

> [!example] Problem
> Equations like `"a==b"` and `"a!=b"`. Determine if all can be simultaneously satisfied.

> [!info] Approach
> - **WHY:** `==` is transitive. Must union all equal pairs before checking inequalities — single-pass fails on ordering.
> - **WHAT:** Pass 1: union all `==` pairs. Pass 2: verify no `!=` pair has both sides in the same component.
> - **HOW:** 26 lowercase letters → DSU of size 26. If `find(x) == find(y)` for a `!=` constraint → contradiction.

> [!note]- Python Solution
> ```python
> def equationsPossible(equations: list[str]) -> bool:
>     dsu = DSU(26)   # 26 lowercase letters
> 
>     for eq in equations:
>         if eq[1] == '=':    # "a==b"
>             dsu.union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))
> 
>     for eq in equations:
>         if eq[1] == '!':    # "a!=b"
>             if dsu.connected(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a')):
>                 return False
> 
>     return True
> ```

> [!success] Complexity
> Time O(26·α(26)) = O(1), Space O(26) = O(1).

> [!tip] Alternatives
> Graph coloring / BFS — build equality groups then check inequality constraints. DSU is cleaner.

---

## Weighted / Ranked Union-Find

### Accounts Merge

> [!example] Problem
> List of accounts `[name, email1, email2, ...]`. Merge accounts sharing at least one email. Return sorted merged accounts.

> [!info] Approach
> - **WHY:** Emails are the identity key, not names. Accounts sharing any email are the same person — transitive merging is DSU.
> - **WHAT:** DSU over all unique emails (map each to integer index). Union all emails within an account. Group by DSU root; sort per group.
> - **HOW:** Map `email → index`. For each account, union the first email with all subsequent ones. After all unions, group indices by root.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def accountsMerge(accounts: list[list[str]]) -> list[list[str]]:
>     email_to_idx: dict[str, int] = {}
>     email_to_name: dict[str, str] = {}
> 
>     for account in accounts:
>         name = account[0]
>         for email in account[1:]:
>             if email not in email_to_idx:
>                 email_to_idx[email] = len(email_to_idx)
>             email_to_name[email] = name
> 
>     dsu = DSU(len(email_to_idx))
> 
>     for account in accounts:
>         first_idx = email_to_idx[account[1]]
>         for email in account[2:]:
>             dsu.union(first_idx, email_to_idx[email])
> 
>     root_to_emails: dict[int, list[str]] = defaultdict(list)
>     for email, idx in email_to_idx.items():
>         root_to_emails[dsu.find(idx)].append(email)
> 
>     result: list[list[str]] = []
>     for root, emails in root_to_emails.items():
>         name = email_to_name[emails[0]]
>         result.append([name] + sorted(emails))
> 
>     return result
> ```

> [!success] Complexity
> Time O(N·K·log(N·K)) dominated by sorting, Space O(N·K).

> [!tip] Alternatives
> BFS on email adjacency graph — build `email → [co-account emails]` map, BFS for components. Same complexity, more code.

---

### Smallest String With Swaps

> [!example] Problem
> String `s`, list of index pairs that can be swapped any number of times. Return lexicographically smallest string achievable.

> [!info] Approach
> - **WHY:** Swap pairs are transitive — if `(0,1)` and `(1,2)` are pairs, all three indices form one free-rearrangement group. DSU finds these components.
> - **WHAT:** Union all paired indices. Within each component, sort characters, assign smallest first.
> - **HOW:** Group indices by DSU root. For each group, collect and sort characters; assign back to sorted index positions.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def smallestStringWithSwaps(s: str, pairs: list[list[int]]) -> str:
>     n = len(s)
>     dsu = DSU(n)
>     for u, v in pairs:
>         dsu.union(u, v)
> 
>     root_to_indices: dict[int, list[int]] = defaultdict(list)
>     for i in range(n):
>         root_to_indices[dsu.find(i)].append(i)
> 
>     result = list(s)
>     for indices in root_to_indices.values():
>         chars = sorted(s[i] for i in indices)
>         for i, c in zip(sorted(indices), chars):
>             result[i] = c
> 
>     return "".join(result)
> ```

> [!success] Complexity
> Time O((N + E)·α(N) + N·log N), Space O(N).

> [!tip] Alternatives
> BFS/DFS to find connected components of index pairs. Same complexity.

---

### Evaluate Division (Weighted DSU)

> [!example] Problem
> Equations `A/B = k`. Answer queries `C/D = ?`. Return `-1.0` if unknown.

> [!info] Approach
> - **WHY:** Variables are nodes; edges are ratios. If `A/B = k` and `B/C = m`, then `A/C = k·m` — path product. Weighted DSU accumulates products along compressed paths.
> - **WHAT:** `weight[x]` = `value(x) / value(root(x))`. On `find`, accumulate product. On `union(A, B, k)`, adjust root weights for consistency.
> - **HOW:** Query `C/D`: if same root, answer = `weight[C] / weight[D]`.

> [!note]- Python Solution
> ```python
> def calcEquation(equations: list[list[str]], values: list[float],
>                  queries: list[list[str]]) -> list[float]:
>     parent: dict[str, str] = {}
>     weight: dict[str, float] = {}   # weight[x] = x / parent[x]
> 
>     def find(x: str) -> tuple[str, float]:
>         if parent[x] != x:
>             root, w = find(parent[x])
>             parent[x] = root
>             weight[x] *= w
>         return parent[x], weight[x]
> 
>     def union(x: str, y: str, ratio: float) -> None:
>         if x not in parent:
>             parent[x] = x; weight[x] = 1.0
>         if y not in parent:
>             parent[y] = y; weight[y] = 1.0
>         rx, wx = find(x)
>         ry, wy = find(y)
>         if rx != ry:
>             parent[rx] = ry
>             weight[rx] = ratio * wy / wx
> 
>     for (a, b), v in zip(equations, values):
>         union(a, b, v)
> 
>     results: list[float] = []
>     for c, d in queries:
>         if c not in parent or d not in parent:
>             results.append(-1.0)
>         else:
>             rc, wc = find(c)
>             rd, wd = find(d)
>             results.append(wc / wd if rc == rd else -1.0)
> 
>     return results
> ```

> [!success] Complexity
> Time O((E + Q)·α(V)), Space O(V).

> [!tip] Alternatives
> BFS/DFS per query — O(Q·(V+E)). Floyd-Warshall — O(V³) preprocessing, O(1) per query. Weighted DSU is best for many queries after static setup.

---

## MST (Kruskal's)

### Min Cost to Connect All Points

> [!example] Problem
> 2D points. Connect all with minimum total Manhattan distance (any pair can be connected directly).

> [!info] Approach
> - **WHY:** Complete graph MST. Kruskal: sort all O(N²) edges, greedily add cheapest non-cycle edge using DSU.
> - **WHAT:** Generate all pairwise Manhattan distance edges; sort; apply Kruskal with DSU.
> - **HOW:** Stop early when `n-1` edges are added. Prim's with simple array is O(N²) and avoids generating/sorting edges — better for dense graphs.

> [!note]- Python Solution
> ```python
> def minCostConnectPoints(points: list[list[int]]) -> int:
>     n = len(points)
>     edges: list[tuple[int,int,int]] = []
>     for i in range(n):
>         for j in range(i + 1, n):
>             dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
>             edges.append((dist, i, j))
> 
>     edges.sort()
>     dsu = DSU(n)
>     total = edges_used = 0
> 
>     for dist, i, j in edges:
>         if dsu.union(i, j):
>             total += dist
>             edges_used += 1
>             if edges_used == n - 1:
>                 break
> 
>     return total
> ```

> [!success] Complexity
> Time O(N²·log N) dominated by sorting, Space O(N²).

> [!tip] Alternatives
> Prim's with simple array — O(N²), avoids materializing all edges. Better for large N since edge count is O(N²).

---

### Critical Connections / Pseudo-Critical Edges in MST

> [!example] Problem
> Find edges that must appear in every MST (critical) and edges that can appear in some MST (pseudo-critical).

> [!info] Approach
> - **WHY:** An edge is critical if excluding it raises MST cost. Pseudo-critical if forcing its inclusion keeps cost equal to base MST.
> - **WHAT:** For each edge, run two Kruskal experiments: exclude it and force-include it.
> - **HOW:** Base MST first. For edge `e`: critical if `MST_without_e > base`. Pseudo-critical if `MST_with_e_forced == base`.

> [!note]- Python Solution
> ```python
> def findCriticalAndPseudoCriticalEdges(n: int,
>         edges: list[list[int]]) -> list[list[int]]:
>     indexed = [(w, u, v, i) for i, (u, v, w) in enumerate(edges)]
>     indexed.sort()
> 
>     def kruskal(skip_idx: int = -1,
>                 force_edge: tuple | None = None) -> int:
>         dsu = DSU(n)
>         total = 0
>         if force_edge:
>             w, u, v, _ = force_edge
>             dsu.union(u, v)
>             total += w
>         for w, u, v, i in indexed:
>             if i == skip_idx:
>                 continue
>             if dsu.union(u, v):
>                 total += w
>         return total if dsu.components == 1 else float('inf')
> 
>     base = kruskal()
>     critical, pseudo = [], []
> 
>     for edge in indexed:
>         _, _, _, i = edge
>         if kruskal(skip_idx=i) > base:
>             critical.append(i)
>         elif kruskal(force_edge=edge) == base:
>             pseudo.append(i)
> 
>     return [critical, pseudo]
> ```

> [!success] Complexity
> Time O(E²·α(V)) with sort pre-applied, Space O(V).

> [!tip] Alternatives
> Tarjan's bridge-finding adapted to MST edges — more efficient but complex. Matroid intersection — interview-impractical.

---

## Dynamic / Offline Union-Find

### Number of Islands II

> [!example] Problem
> Initially empty `m×n` grid. Receive `addLand(r, c)` operations. After each, return island count.

> [!info] Approach
> - **WHY:** Islands are connected components growing dynamically. Re-running BFS is O(M·N) per operation. DSU handles each addition in O(α) — orders of magnitude faster.
> - **WHAT:** DSU on 2D grid encoded as `r*cols + c`. On `addLand`, increment component count, then union with adjacent land cells.
> - **HOW:** Track which cells are land (set). Skip duplicate additions. DSU's `union` automatically decrements component count on merge.

> [!note]- Python Solution
> ```python
> def numIslands2(m: int, n: int, positions: list[list[int]]) -> list[int]:
>     dsu = DSU(m * n)
>     dsu.components = 0       # override: start with 0 islands
>     land: set[int] = set()
>     result: list[int] = []
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     for r, c in positions:
>         idx = r * n + c
>         if idx in land:
>             result.append(dsu.components)
>             continue
>         land.add(idx)
>         dsu.components += 1          # new land cell = new island
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             nidx = nr * n + nc
>             if 0 <= nr < m and 0 <= nc < n and nidx in land:
>                 dsu.union(idx, nidx)  # merges components; decrements count
>         result.append(dsu.components)
> 
>     return result
> ```

> [!success] Complexity
> Time O(K·α(M·N)) where K = operations, Space O(M·N).

> [!tip] Alternatives
> Re-run BFS after each addition — O(K·M·N). Offline: process in reverse (deletions → additions). DSU is optimal for online queries.

---

### Minimize Malware Spread

> [!example] Problem
> Graph of computers, initial list of infected. Remove exactly one infected node to minimize final malware spread.

> [!info] Approach
> - **WHY:** Malware spreads to the entire connected component. Removing node `x` only helps if `x` is the sole infected node in its component — otherwise another infected node spreads malware to that component anyway.
> - **WHAT:** DSU to find component sizes. For each component, count infected nodes. Only single-infected components are saveable.
> - **HOW:** Build full DSU. Count infected nodes per component root. The best removal candidate is the infected node whose component has exactly 1 infected node and the largest size. Tie-break: smallest index.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def minMalwareSpread(graph: list[list[int]], initial: list[int]) -> int:
>     n = len(graph)
>     dsu = DSU(n)
>     for i in range(n):
>         for j in range(i + 1, n):
>             if graph[i][j] == 1:
>                 dsu.union(i, j)
> 
>     infected_per_root: dict[int, list[int]] = defaultdict(list)
>     for node in initial:
>         infected_per_root[dsu.find(node)].append(node)
> 
>     best_node = min(initial)     # default if no single-infected component exists
>     best_save = 0
> 
>     for root, infected_nodes in infected_per_root.items():
>         if len(infected_nodes) == 1:
>             save = dsu.component_size(infected_nodes[0])
>             if save > best_save or (save == best_save and infected_nodes[0] < best_node):
>                 best_save = save
>                 best_node = infected_nodes[0]
> 
>     return best_node
> ```

> [!success] Complexity
> Time O(V²·α(V)) for dense adjacency matrix, Space O(V).

> [!tip] Alternatives
> BFS/DFS to find components and simulate removal. Same complexity. DSU makes component size lookup O(1).

---

## DSU for Other Problems

### Longest Consecutive Sequence (DSU Approach)

> [!example] Problem
> Unsorted array. Find the length of the longest consecutive elements sequence in O(N).

> [!info] Approach
> - **WHY:** `x` and `x+1` belong to the same consecutive run — union them. The largest component size is the answer.
> - **WHAT:** Map each value to an index; union `x` with `x+1` if `x+1` exists. Max component size = answer.
> - **HOW:** Build `val → index` map. For each value, if `val+1` exists, union their indices.

> [!note]- Python Solution
> ```python
> def longestConsecutive(nums: list[int]) -> int:
>     if not nums:
>         return 0
>     val_to_idx = {v: i for i, v in enumerate(nums)}
>     dsu = DSU(len(nums))
> 
>     for val, idx in val_to_idx.items():
>         if val + 1 in val_to_idx:
>             dsu.union(idx, val_to_idx[val + 1])
> 
>     return max(dsu.component_size(i) for i in range(len(nums)))
> ```

> [!success] Complexity
> Time O(N·α(N)) ≈ O(N), Space O(N).

> [!tip] Alternatives
> Hash set (canonical) — for each `x` where `x-1` not in set (sequence start), expand right. O(N), simpler. DSU is a valid alternative but hash set is preferred in interviews for this problem.

---

### Path with Maximum Probability (Weighted DSU)

> [!example] Problem
> Undirected graph with edge probabilities. Find the path from `start` to `end` maximizing product of probabilities.

> [!info] Approach
> - **WHY:** For general graphs Dijkstra (max-heap variant) is canonical and handles multiple alternate paths. Weighted DSU works on trees — only one path exists between any two nodes.
> - **WHAT:** Weighted DSU where `weight[x]` = probability of `x` relative to its root. Query: `weight[start] / weight[end]` if same root.
> - **HOW:** `union(A, B, p)`: adjust root weight so `weight[A] / weight[B] = p`. Valid only when graph is a tree.

> [!note]- Python Solution
> ```python
> def maxProbabilityDSU(n: int, edges: list[list[int]], succProb: list[float],
>                       start: int, end: int) -> float:
>     # Canonical solution: Dijkstra with max-heap (handles general graphs).
>     # DSU shown for tree-structured probability graphs only.
>     parent = list(range(n))
>     weight = [1.0] * n   # weight[x] = prob(x) / prob(root(x))
> 
>     def find(x: int) -> tuple[int, float]:
>         if parent[x] != x:
>             root, w = find(parent[x])
>             parent[x] = root
>             weight[x] *= w
>         return parent[x], weight[x]
> 
>     for (u, v), p in zip(edges, succProb):
>         ru, wu = find(u)
>         rv, wv = find(v)
>         if ru != rv:
>             parent[ru] = rv
>             weight[ru] = p * wv / wu
> 
>     ru, wu = find(start)
>     rv, wv = find(end)
>     return wu / wv if ru == rv else 0.0
> ```

> [!success] Complexity
> Time O((V + E)·α(V)), Space O(V).

> [!tip] Alternatives
> Dijkstra with max-heap — handles cycles and multiple alternate paths, O((V + E)·log V). Use Dijkstra for the general case.

---

## See Also

[[graph]] | [[graph-algorithms]] | [[sorting]]
