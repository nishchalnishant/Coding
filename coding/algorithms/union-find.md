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

## Directed Graph Union-Find

### Redundant Connection II

> [!example] Problem
> Directed graph built from a tree by adding exactly one extra directed edge. Return the redundant edge. Each node has in-degree ≤ 2. If multiple answers, return the one appearing last.

> [!info] Approach
> - **WHY:** In a directed tree (rooted), every non-root has in-degree 1. The extra edge creates either (a) a node with in-degree 2, or (b) a cycle with all in-degrees 1, or (c) both. These three cases need separate handling.
> - **WHAT:** First detect any node with in-degree 2 — candidates `cand1` (first edge into it) and `cand2` (second edge). Then run DSU on all edges, skipping `cand2` if it exists. If a cycle forms, the redundant edge is `cand1` (if cand2 exists) or the cycle-forming edge (if no cand2).
> - **HOW:** Pass 1: record in-degree-2 candidates. Pass 2: DSU union excluding `cand2`. If no cycle detected with `cand2` excluded → return `cand2`. If cycle detected and `cand1` exists → return `cand1`. If cycle and no candidate → return the cycle edge.

> [!note]- Python Solution
> ```python
> def findRedundantDirectedConnection(edges: list[list[int]]) -> list[int]:
>     n = len(edges)
>     in_degree = [0] * (n + 1)
>     for u, v in edges:
>         in_degree[v] += 1
> 
>     # Identify candidates: edges pointing to a node with in-degree 2
>     cand1 = cand2 = None
>     for u, v in edges:
>         if in_degree[v] == 2:
>             if cand1 is None:
>                 cand1 = [u, v]
>             else:
>                 cand2 = [u, v]
> 
>     def has_cycle_excluding(skip: list[int] | None) -> list[int] | None:
>         dsu = DSU(n + 1)
>         for u, v in edges:
>             if [u, v] == skip:
>                 continue
>             if not dsu.union(u, v):
>                 return [u, v]
>         return None
> 
>     if cand2:
>         # Try excluding cand2; if no cycle → cand2 is answer, else cand1
>         if has_cycle_excluding(cand2) is None:
>             return cand2
>         else:
>             return cand1
>     else:
>         # No in-degree-2 node; the cycle-forming edge is the answer
>         return has_cycle_excluding(None)
> ```

> [!success] Complexity
> Time O(N·α(N)) ≈ O(N), Space O(N).

> [!tip] Alternatives
> Tarjan's SCC — overkill. DFS cycle detection on the directed graph — works but messier to get all three cases right. DSU with two-pass candidate detection is the cleanest.

---

## Grid / Coordinate Union-Find

### Swim in Rising Water

> [!example] Problem
> `n×n` grid where `grid[r][c]` is the elevation. At time `t`, you can swim to adjacent cells with elevation ≤ `t`. Find minimum `t` to swim from `(0,0)` to `(n-1,n-1)`.

> [!info] Approach
> - **WHY:** Sort all cells by elevation. Process them in order, unioning each cell with already-processed adjacent cells. The answer is the elevation of the last cell processed when `(0,0)` and `(n-1,n-1)` first become connected.
> - **WHAT:** Kruskal-style: sort cells by elevation, add them one by one, union with processed neighbors. Stop when start and end are connected.
> - **HOW:** Create list of `(elevation, r, c)`, sort it. Maintain `visited` set. For each cell in order, mark visited, union with adjacent visited cells, check connectivity.

> [!note]- Python Solution
> ```python
> def swimInWater(grid: list[list[int]]) -> int:
>     n = len(grid)
>     cells = sorted((grid[r][c], r, c) for r in range(n) for c in range(n))
>     dsu = DSU(n * n)
>     visited = set()
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     for elev, r, c in cells:
>         visited.add((r, c))
>         idx = r * n + c
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if (nr, nc) in visited:
>                 dsu.union(idx, nr * n + nc)
>         if dsu.connected(0, (n-1)*n + (n-1)):
>             return elev
>     return grid[n-1][n-1]
> ```

> [!success] Complexity
> Time O(N²·log N) for sort, Space O(N²).

> [!tip] Alternatives
> Binary search + BFS/DFS — O(N²·log N). Dijkstra (min-heap over max elevation on path) — O(N²·log N), arguably more intuitive. DSU is elegant for the "when do two cells become connected" framing.

---

### Most Stones Removed with Same Row or Column

> [!example] Problem
> Stones on a 2D grid (at most one per cell). A stone can be removed if it shares a row or column with another stone. Return max stones removable.

> [!info] Approach
> - **WHY:** Stones in the same connected component (row/column sharing is transitive) can all be reduced to 1 stone. Answer = total stones − number of components.
> - **WHAT:** DSU where stones sharing a row or column are in the same component. Use coordinate compression: treat row `r` and column `c` as separate nodes with an offset to avoid collision.
> - **HOW:** Map rows to `[0, 10000]` and cols to `[10001, 20001]`. Union `row_r` with `col_c` for each stone. Count distinct roots among only the stone positions.

> [!note]- Python Solution
> ```python
> def removeStones(stones: list[list[int]]) -> int:
>     parent: dict[int, int] = {}
> 
>     def find(x: int) -> int:
>         if x not in parent:
>             parent[x] = x
>         if parent[x] != x:
>             parent[x] = find(parent[x])
>         return parent[x]
> 
>     def union(x: int, y: int) -> None:
>         px, py = find(x), find(y)
>         if px != py:
>             parent[px] = py
> 
>     for r, c in stones:
>         union(r, c + 10001)   # offset columns to separate namespace
> 
>     roots = {find(r) for r, c in stones}
>     return len(stones) - len(roots)
> ```

> [!success] Complexity
> Time O(N·α(N)) ≈ O(N), Space O(N).

> [!tip] Alternatives
> DFS on adjacency list built from row/col buckets — O(N²) build, O(N) DFS. DSU with coordinate trick is cleaner and O(N).

---

## Weighted / Partial Swap Union-Find

### Minimize Hamming Distance After Swap Operations

> [!example] Problem
> Arrays `source` and `target`, list of allowed index swap pairs (transitive). Minimize total Hamming distance (positions where `source[i] != target[i]`).

> [!info] Approach
> - **WHY:** Swap pairs define groups of indices that can be freely rearranged among themselves. Within each group, match `source` values to `target` values optimally (minimize mismatches = maximize matches).
> - **WHAT:** DSU to find index groups. For each group, build frequency maps of `source` and `target` values; match greedily.
> - **HOW:** For each DSU component, count how many `source[i]` values can be matched to `target[i]` values in the group. Unmatched positions contribute 1 each to Hamming distance.

> [!note]- Python Solution
> ```python
> from collections import Counter, defaultdict
> 
> def minimizeHammingDistance(source: list[int], target: list[int],
>                              allowedSwaps: list[list[int]]) -> int:
>     n = len(source)
>     dsu = DSU(n)
>     for u, v in allowedSwaps:
>         dsu.union(u, v)
> 
>     root_to_indices: dict[int, list[int]] = defaultdict(list)
>     for i in range(n):
>         root_to_indices[dsu.find(i)].append(i)
> 
>     hamming = 0
>     for indices in root_to_indices.values():
>         src_count = Counter(source[i] for i in indices)
>         tgt_count = Counter(target[i] for i in indices)
>         matched = sum((src_count & tgt_count).values())  # intersection
>         hamming += len(indices) - matched
> 
>     return hamming
> ```

> [!success] Complexity
> Time O((N + E)·α(N) + N), Space O(N).

> [!tip] Alternatives
> BFS/DFS to find components, same counting logic. DSU is more concise.

---

## Connectivity With Constraints

### Minimum Cost to Make at Least One Valid Path in a Grid

> [!example] Problem
> `m×n` grid, each cell has a direction (1=right, 2=left, 3=down, 4=up). Moving in the cell's direction costs 0; changing direction costs 1. Find minimum cost to reach `(m-1, n-1)` from `(0,0)`.

> [!info] Approach
> - **WHY:** Edge weights are 0 (follow direction) or 1 (change direction). This is a 0-1 BFS problem — but can also be viewed as DSU on "0-cost" groups followed by checking connectivity.
> - **WHAT:** 0-1 BFS: use deque; free (0-cost) moves go to front, cost-1 moves go to back. Process in Dijkstra-like order.
> - **HOW:** For cell `(r,c)`, the free neighbor is determined by `grid[r][c]`. All other neighbors cost 1. Track `dist` array initialized to infinity.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def minCost(grid: list[list[int]]) -> int:
>     m, n = len(grid), len(grid[0])
>     # direction map: 1=right, 2=left, 3=down, 4=up
>     dir_map = {1: (0,1), 2: (0,-1), 3: (1,0), 4: (-1,0)}
>     dirs = [(0,1,1),(0,-1,2),(1,0,3),(-1,0,4)]  # (dr, dc, code)
> 
>     dist = [[float('inf')] * n for _ in range(m)]
>     dist[0][0] = 0
>     dq: deque[tuple[int,int,int]] = deque([(0, 0, 0)])  # (cost, r, c)
> 
>     while dq:
>         cost, r, c = dq.popleft()
>         if cost > dist[r][c]:
>             continue
>         for dr, dc, code in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < m and 0 <= nc < n:
>                 new_cost = cost + (0 if grid[r][c] == code else 1)
>                 if new_cost < dist[nr][nc]:
>                     dist[nr][nc] = new_cost
>                     if grid[r][c] == code:
>                         dq.appendleft((new_cost, nr, nc))
>                     else:
>                         dq.append((new_cost, nr, nc))
> 
>     return dist[m-1][n-1]
> ```

> [!success] Complexity
> Time O(M·N), Space O(M·N).

> [!tip] Alternatives
> Dijkstra — O(M·N·log(M·N)), overkill for 0/1 weights. DSU grouping: union all 0-cost reachable cells first (like BFS layers), then count layers to destination — less standard. 0-1 BFS is canonical.

---

### Remove Max Number of Edges to Keep Graph Fully Traversable

> [!example] Problem
> Graph with 3 edge types: type 1 (Alice only), type 2 (Bob only), type 3 (both). Find max edges to remove such that both Alice and Bob can still traverse the full graph.

> [!info] Approach
> - **WHY:** We want minimal spanning forest for Alice and Bob independently. Shared edges (type 3) are doubly valuable — use them first. Any edge that doesn't reduce components is redundant.
> - **WHAT:** Run two DSUs (Alice, Bob). Process type-3 edges first (union in both). Then type-1 in Alice's DSU, type-2 in Bob's. Count edges used; answer = total edges − edges used.
> - **HOW:** An edge is removable if its union returns `False` in both relevant DSUs. Final check: both DSUs must reach 1 component, else return -1.

> [!note]- Python Solution
> ```python
> def maxNumEdgesToRemove(n: int, edges: list[list[int]]) -> int:
>     alice, bob = DSU(n + 1), DSU(n + 1)
>     used = 0
> 
>     # Type 3 first: shared edges are most valuable
>     for t, u, v in edges:
>         if t == 3:
>             a = alice.union(u, v)
>             b = bob.union(u, v)
>             if a or b:   # useful to at least one
>                 used += 1
> 
>     for t, u, v in edges:
>         if t == 1 and alice.union(u, v):
>             used += 1
>         elif t == 2 and bob.union(u, v):
>             used += 1
> 
>     if alice.components != 2 or bob.components != 2:
>         # components starts at n+1; after connecting n nodes → 1 real component = components==2 (node 0 unused)
>         return -1
> 
>     return len(edges) - used
> ```

> [!success] Complexity
> Time O(E·α(V)) ≈ O(E), Space O(V).

> [!tip] Alternatives
> No simpler alternative — DSU with two-graph reasoning is the canonical approach here.

---

### Making a Large Island

> [!example] Problem
> Binary grid. Flip exactly one 0 to 1. Return the size of the largest island after the flip.

> [!info] Approach
> - **WHY:** After flipping a 0, the new cell connects up to 4 adjacent islands. Island sizes are needed instantly → DSU component sizes.
> - **WHAT:** Build DSU over existing 1-cells. For each 0-cell, sum sizes of distinct adjacent components + 1. Track overall max.
> - **HOW:** Label each cell's DSU root. For each 0-cell, collect unique roots of neighboring 1-cells (avoid double-counting same component), sum their sizes.

> [!note]- Python Solution
> ```python
> def largestIsland(grid: list[list[int]]) -> int:
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
>     best = max((dsu.component_size(r*n+c) for r in range(n)
>                 for c in range(n) if grid[r][c] == 1), default=0)
> 
>     for r in range(n):
>         for c in range(n):
>             if grid[r][c] == 0:
>                 seen_roots: set[int] = set()
>                 gain = 1
>                 for dr, dc in dirs:
>                     nr, nc = r + dr, c + dc
>                     if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
>                         root = dsu.find(nr*n+nc)
>                         if root not in seen_roots:
>                             gain += dsu.component_size(nr*n+nc)
>                             seen_roots.add(root)
>                 best = max(best, gain)
> 
>     return best
> ```

> [!success] Complexity
> Time O(N²·α(N²)) ≈ O(N²), Space O(N²).

> [!tip] Alternatives
> BFS to label islands and record sizes — O(N²). Same idea, slightly more setup. DSU makes the component-size lookup natural.

---

### Number of Good Paths

> [!example] Problem
> Tree with `n` nodes and node values. A "good path" starts and ends at nodes of equal value, with all intermediate nodes having value ≤ that value. Count all good paths (including single nodes).

> [!info] Approach
> - **WHY:** Process nodes in increasing order of value. When adding a node, union it with already-processed neighbors. Two same-value nodes in the same component form `count*(count-1)/2` new paths.
> - **WHAT:** Sort nodes by value. Process batches of equal value. Union nodes in each batch with lower-valued neighbors. Count pairs within the merged component.
> - **HOW:** Group nodes by value. For each value group, union all nodes of that value with their neighbors (which have ≤ current value). Count same-value nodes per component root; add `k*(k+1)/2` where `k` = count.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def numberOfGoodPaths(vals: list[int], edges: list[list[int]]) -> int:
>     n = len(vals)
>     adj: list[list[int]] = defaultdict(list)
>     for u, v in edges:
>         adj[u].append(v)
>         adj[v].append(u)
> 
>     dsu = DSU(n)
>     # For each root, track count of nodes in component with the max value
>     val_count = [1] * n  # val_count[root] = # nodes in component equal to vals[root]
> 
>     sorted_nodes = sorted(range(n), key=lambda x: vals[x])
>     result = n   # each node is a good path by itself
> 
>     i = 0
>     while i < n:
>         j = i
>         # Process all nodes with same value together
>         while j < n and vals[sorted_nodes[j]] == vals[sorted_nodes[i]]:
>             j += 1
>         batch = sorted_nodes[i:j]
> 
>         for node in batch:
>             for nb in adj[node]:
>                 if vals[nb] <= vals[node]:
>                     rn, rnb = dsu.find(node), dsu.find(nb)
>                     if rn != rnb:
>                         cn = val_count[rn] if vals[rn] == vals[node] else 0
>                         cnb = val_count[rnb] if vals[rnb] == vals[node] else 0
>                         dsu.union(node, nb)
>                         new_root = dsu.find(node)
>                         val_count[new_root] = cn + cnb
>                         result += cn * cnb
>         i = j
> 
>     return result
> ```

> [!success] Complexity
> Time O((N + E)·α(N) + N·log N), Space O(N).

> [!tip] Alternatives
> DFS/BFS per value group — harder to implement correctly. DSU with sorted processing is the standard approach for this problem.

---

### Largest Component Size by Common Factor

> [!example] Problem
> Array of positive integers. Two numbers belong to the same component if they share a common factor > 1. Return the size of the largest component.

> [!info] Approach
> - **WHY:** Shared prime factors link numbers together transitively. Union each number with all its prime factors; then prime factors link all numbers sharing them.
> - **WHAT:** For each number, factorize it, union the number with each of its prime factors. Count max component size.
> - **HOW:** Nodes are both numbers (index) and prime factors (up to max value). Use dict-based DSU. For each `nums[i]`, find primes, union `nums[i]` with each prime, then count component size for each original number.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def largestComponentSize(nums: list[int]) -> int:
>     parent: dict[int, int] = {}
> 
>     def find(x: int) -> int:
>         if x not in parent:
>             parent[x] = x
>         if parent[x] != x:
>             parent[x] = find(parent[x])
>         return parent[x]
> 
>     def union(x: int, y: int) -> None:
>         px, py = find(x), find(y)
>         if px != py:
>             parent[px] = py
> 
>     def prime_factors(n: int) -> list[int]:
>         factors: list[int] = []
>         d = 2
>         while d * d <= n:
>             if n % d == 0:
>                 factors.append(d)
>                 while n % d == 0:
>                     n //= d
>             d += 1
>         if n > 1:
>             factors.append(n)
>         return factors
> 
>     for num in nums:
>         for p in prime_factors(num):
>             union(num, p)
> 
>     comp_size: dict[int, int] = defaultdict(int)
>     for num in nums:
>         comp_size[find(num)] += 1
> 
>     return max(comp_size.values())
> ```

> [!success] Complexity
> Time O(N·√max_val·α(N)), Space O(N + max_val).

> [!tip] Alternatives
> BFS building adjacency from shared factors — O(N²) for brute-force GCD check. Sieve-based approach: for each prime p, group all multiples in nums. DSU with prime factors is the canonical O(N·√V) solution.

---

## See Also

[[graph]] | [[graph-algorithms]] | [[sorting]]
