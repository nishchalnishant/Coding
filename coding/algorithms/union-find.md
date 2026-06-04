---
tags: [coding, algorithms, union-find]
topic: Union-Find (DSU)
difficulty: mixed
---

# Union-Find — Problem Deep Dives


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## DSU Template

> [!note]- DSU Class (Python)
> ```python
> class DSU:
>     def __init__(self, n):
>         self.parent = list(range(n))
>         self.rank = [0] * n
>         self.size = [1] * n
>         self.components = n
> 
>     def find(self, x):
>         if self.parent[x] != x:
>             self.parent[x] = self.find(self.parent[x])  # path compression
>         return self.parent[x]
> 
>     def union(self, x, y):
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
>     def connected(self, x, y):
>         return self.find(x) == self.find(y)
> 
>     def component_size(self, x):
>         return self.size[self.find(x)]
> ```

> [!info] Core Invariants
> All nodes in the same component share the same root after `find`. Path compression + union by rank gives amortized O(α(n)) ≈ O(1) per operation.

---

## Basic Union-Find

### Number of Connected Components in an Undirected Graph `🔥 Google`

> [!example] Problem
> You have a graph of `n` nodes. You are given an integer `n` and an array `edges` where `edges[i] = [a_i, b_i]` indicates that there is an edge between `a_i` and `b_i` in the graph.
> 
> Return *the number of connected components in the graph*.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** n = 5, edges = [[0,1],[1,2],[3,4]]
> **Output:** 2
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
> **Output:** 1
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= n <= 2000`
> 	
> - `1 <= edges.length <= 5000`
> 	
> - `edges[i].length == 2`
> 	
> - `0 <= a_i <= b_i < n`
> 	
> - `a_i != b_i`
> 	
> - There are no repeated edges.

> [!info] Approach
> BFS/DFS counts components in O(V+E) per call — fine for one-shot. DSU enables incremental edge-addition with O(α) per union/query. Here they're equivalent; DSU is the canonical pattern. Union all edges; answer = `dsu.components`. Initialize `components = n`; decrement by 1 on each successful union.

> [!note]- Python Solution
> ```python
> def count_components(n, edges):
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

### Number of Provinces (Matrix Form) `⭐ Google`

> [!example] Problem
> There are n cities. Some of them are connected, while some are not. If city a is connected directly with city b, and city b is connected directly with city c, then city a is connected indirectly with city c.
> A province is a group of directly or indirectly connected cities and no other cities outside of the group.
> You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.
> Return the total number of provinces.
> 
> **Example 1:**
> ```
> Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= n <= 200
> - n == isConnected.length
> - n == isConnected[i].length
> - isConnected[i][j] is 1 or 0.
> - isConnected[i][i] == 1
> - isConnected[i][j] == isConnected[j][i]

> [!info] Approach
> Adjacency matrix encodes undirected edges. Treat `isConnected[i][j] == 1` as edge `(i, j)`. Iterate upper triangle, union connected pairs; count components. Only process upper triangle (`j > i`) to avoid redundant unions and double-decrementing.

> [!note]- Python Solution
> ```python
> def find_circle_num(isConnected):
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

### Graph Valid Tree `⭐ Google`

> [!example] Problem
> You have a graph of `n` nodes labeled from `0` to `n - 1`. You are given an integer n and a list of `edges` where `edges[i] = [a_i, b_i]` indicates that there is an undirected edge between nodes `a_i` and `b_i` in the graph.
> 
> Return `true` *if the edges of the given graph make up a valid tree, and* `false` *otherwise*.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
> **Output:** true
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
> **Output:** false
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= n <= 2000`
> 	
> - `0 <= edges.length <= 5000`
> 	
> - `edges[i].length == 2`
> 	
> - `0 <= a_i, b_i < n`
> 	
> - `a_i != b_i`
> 	
> - There are no self-loops or repeated edges.

> [!info] Approach
> A valid tree on `n` nodes has exactly `n-1` edges and no cycles — equivalently, it is connected and acyclic. DSU cycle detection + single-component check. Short-circuit if `len(edges) != n-1`. Process edges; if any union returns `False` (cycle) → not a tree.

> [!note]- Python Solution
> ```python
> def valid_tree(n, edges):
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

### Satisfiability of Equality Equations `⭐ Google`

> [!example] Problem
> You are given an array of strings equations that represent relationships between variables where each string equations[i] is of length 4 and takes one of two different forms: "xi==yi" or "xi!=yi".Here, xi and yi are lowercase letters (not necessarily different) that represent one-letter variable names.
> Return true if it is possible to assign integers to variable names so as to satisfy all the given equations, or false otherwise.
> 
> **Example 1:**
> ```
> Input: equations = ["a==b","b!=a"]
> Output: false
> Explanation: If we assign say, a = 1 and b = 1, then the first equation is satisfied, but not the second.
> There is no way to assign the variables to satisfy both equations.
> ```
> 
> **Example 2:**
> ```
> Input: equations = ["b==a","a==b"]
> Output: true
> Explanation: We could assign a = 1 and b = 1 to satisfy both equations.
> ```
> 
> **Constraints:**
> - 1 <= equations.length <= 500
> - equations[i].length == 4
> - equations[i][0] is a lowercase letter.
> - equations[i][1] is either '=' or '!'.
> - equations[i][2] is '='.
> - equations[i][3] is a lowercase letter.

> [!info] Approach
> `==` is transitive. Must union all equal pairs before checking inequalities — single-pass fails on ordering. Pass 1: union all `==` pairs. Pass 2: verify no `!=` pair has both sides in the same component. 26 lowercase letters → DSU of size 26. If `find(x) == find(y)` for a `!=` constraint → contradiction.

> [!note]- Python Solution
> ```python
> def equations_possible(equations):
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

### Accounts Merge (Email Graph) `🔥 Google`

> [!example] Problem
> Given a list of accounts where each element accounts[i] is a list of strings, where the first element accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account.
> Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.
> After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order.
> 
> **Example 1:**
> ```
> Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
> Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
> Explanation:
> The first and second John's are the same person as they have the common email "johnsmith@mail.com".
> The third John and Mary are different people as none of their email addresses are used by other accounts.
> We could return these lists in any order, for example the answer [['Mary', 'mary@mail.com'], ['John', 'johnnybravo@mail.com'], 
> ['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com']] would still be accepted.
> ```
> 
> **Example 2:**
> ```
> Input: accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
> Output: [["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]
> ```
> 
> **Constraints:**
> - 1 <= accounts.length <= 1000
> - 2 <= accounts[i].length <= 10
> - 1 <= accounts[i][j].length <= 30
> - accounts[i][0] consists of English letters.
> - accounts[i][j] (for j > 0) is a valid email.

> [!info] Approach
> Emails are the identity key, not names. Accounts sharing any email are the same person — transitive merging is DSU. DSU over all unique emails (map each to integer index). Union all emails within an account. Group by DSU root; sort per group. Map `email → index`. For each account, union the first email with all subsequent ones. After all unions, group indices by root.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def accounts_merge(accounts):
>     email_to_idx = {}
>     email_to_name = {}
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
>     root_to_emails = defaultdict(list)
>     for email, idx in email_to_idx.items():
>         root_to_emails[dsu.find(idx)].append(email)
> 
>     result = []
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
> You are given a string s, and an array of pairs of indices in the string pairs where pairs[i] = [a, b] indicates 2 indices(0-indexed) of the string.
> You can swap the characters at any pair of indices in the given pairs any number of times.
> Return the lexicographically smallest string that s can be changed to after using the swaps.
> 
> **Example 1:**
> ```
> Input: s = "dcab", pairs = [[0,3],[1,2]]
> Output: "bacd"
> Explaination: 
> Swap s[0] and s[3], s = "bcad"
> Swap s[1] and s[2], s = "bacd"
> ```
> 
> **Example 2:**
> ```
> Input: s = "dcab", pairs = [[0,3],[1,2],[0,2]]
> Output: "abcd"
> Explaination: 
> Swap s[0] and s[3], s = "bcad"
> Swap s[0] and s[2], s = "acbd"
> Swap s[1] and s[2], s = "abcd"
> ```
> 
> **Example 3:**
> ```
> Input: s = "cba", pairs = [[0,1],[1,2]]
> Output: "abc"
> Explaination: 
> Swap s[0] and s[1], s = "bca"
> Swap s[1] and s[2], s = "bac"
> Swap s[0] and s[1], s = "abc"
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - 0 <= pairs.length <= 10^5
> - 0 <= pairs[i][0], pairs[i][1] < s.length
> - s only contains lower case English letters.

> [!info] Approach
> Swap pairs are transitive — if `(0,1)` and `(1,2)` are pairs, all three indices form one free-rearrangement group. DSU finds these components. Union all paired indices. Within each component, sort characters, assign smallest first. Group indices by DSU root. For each group, collect and sort characters; assign back to sorted index positions.

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
> You are given an array of variable pairs equations and an array of real numbers values, where equations[i] = [Ai, Bi] and values[i] represent the equation Ai / Bi = values[i]. Each Ai or Bi is a string that represents a single variable.
> You are also given some queries, where queries[j] = [Cj, Dj] represents the jth query where you must find the answer for Cj / Dj = ?.
> Return the answers to all queries. If a single answer cannot be determined, return -1.0.
> Note: The input is always valid. You may assume that evaluating the queries will not result in division by zero and that there is no contradiction.
> Note: The variables that do not occur in the list of equations are undefined, so the answer cannot be determined for them.
> 
> **Example 1:**
> ```
> Input: equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
> Output: [6.00000,0.50000,-1.00000,1.00000,-1.00000]
> Explanation: 
> Given: a / b = 2.0, b / c = 3.0
> queries are: a / c = ?, b / a = ?, a / e = ?, a / a = ?, x / x = ? 
> return: [6.0, 0.5, -1.0, 1.0, -1.0 ]
> note: x is undefined => -1.0
> ```
> 
> **Example 2:**
> ```
> Input: equations = [["a","b"],["b","c"],["bc","cd"]], values = [1.5,2.5,5.0], queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
> Output: [3.75000,0.40000,5.00000,0.20000]
> ```
> 
> **Example 3:**
> ```
> Input: equations = [["a","b"]], values = [0.5], queries = [["a","b"],["b","a"],["a","c"],["x","y"]]
> Output: [0.50000,2.00000,-1.00000,-1.00000]
> ```
> 
> **Constraints:**
> - 1 <= equations.length <= 20
> - equations[i].length == 2
> - 1 <= Ai.length, Bi.length <= 5
> - values.length == equations.length
> - 0.0 < values[i] <= 20.0
> - 1 <= queries.length <= 20
> - queries[i].length == 2
> - 1 <= Cj.length, Dj.length <= 5
> - Ai, Bi, Cj, Dj consist of lower case English letters and digits.

> [!info] Approach
> Variables are nodes; edges are ratios. If `A/B = k` and `B/C = m`, then `A/C = k·m` — path product. Weighted DSU accumulates products along compressed paths. `weight[x]` = `value(x) / value(root(x))`. On `find`, accumulate product. On `union(A, B, k)`, adjust root weights for consistency. Query `C/D`: if same root, answer = `weight[C] / weight[D]`.

> [!note]- Python Solution
> ```python
> def calc_equation(equations: list[list[str]], values: list[float],
>                  queries: list[list[str]]) -> list[float]:
>     parent = {}
>     weight = {}   # weight[x] = x / parent[x]
> 
>     def find(x):
>         if parent[x] != x:
>             root, w = find(parent[x])
>             parent[x] = root
>             weight[x] *= w
>         return parent[x], weight[x]
> 
>     def union(x, y, ratio):
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
>     results = []
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
> You are given an array points representing integer coordinates of some points on a 2D-plane, where points[i] = [xi, yi].
> The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them: |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.
> Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.
> 
> **Example 1:**
> ```
> Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
> Output: 20
> Explanation: 
> 
> We can connect the points as shown above to get the minimum cost of 20.
> Notice that there is a unique path between every pair of points.
> ```
> 
> **Example 2:**
> ```
> Input: points = [[3,12],[-2,5],[-4,1]]
> Output: 18
> ```
> 
> **Constraints:**
> - 1 <= points.length <= 1000
> - -10^6 <= xi, yi <= 10^6
> - All pairs (xi, yi) are distinct.

> [!info] Approach
> Complete graph MST. Kruskal: sort all O(N²) edges, greedily add cheapest non-cycle edge using DSU. Generate all pairwise Manhattan distance edges; sort; apply Kruskal with DSU. Stop early when `n-1` edges are added. Prim's with simple array is O(N²) and avoids generating/sorting edges — better for dense graphs.

> [!note]- Python Solution
> ```python
> def min_cost_connect_points(points):
>     n = len(points)
>     edges = []
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
> An edge is critical if excluding it raises MST cost. Pseudo-critical if forcing its inclusion keeps cost equal to base MST. For each edge, run two Kruskal experiments: exclude it and force-include it. Base MST first. For edge `e`: critical if `MST_without_e > base`. Pseudo-critical if `MST_with_e_forced == base`.

> [!note]- Python Solution
> ```python
> def find_critical_and_pseudo_critical_edges(n: int,
>         edges: list[list[int]]) -> list[list[int]]:
>     indexed = [(w, u, v, i) for i, (u, v, w) in enumerate(edges)]
>     indexed.sort()
> 
>     def kruskal(skip_idx: int = -1,
>                 force_edge = None) -> int:
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

### Number of Islands II `🔥 Google`

> [!example] Problem
> Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.
> An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.
> 
> **Example 1:**
> ```
> Input: grid = [
>   ["1","1","1","1","0"],
>   ["1","1","0","1","0"],
>   ["1","1","0","0","0"],
>   ["0","0","0","0","0"]
> ]
> Output: 1
> ```
> 
> **Example 2:**
> ```
> Input: grid = [
>   ["1","1","0","0","0"],
>   ["1","1","0","0","0"],
>   ["0","0","1","0","0"],
>   ["0","0","0","1","1"]
> ]
> Output: 3
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 300
> - grid[i][j] is '0' or '1'.

> [!info] Approach
> Islands are connected components growing dynamically. Re-running BFS is O(M·N) per operation. DSU handles each addition in O(α) — orders of magnitude faster. DSU on 2D grid encoded as `r*cols + c`. On `addLand`, increment component count, then union with adjacent land cells. Track which cells are land (set). Skip duplicate additions. DSU's `union` automatically decrements component count on merge.

> [!note]- Python Solution
> ```python
> def num_islands2(m, n, positions):
>     dsu = DSU(m * n)
>     dsu.components = 0       # override: start with 0 islands
>     land = set()
>     result = []
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
> You are given a network of n nodes represented as an n x n adjacency matrix graph, where the ith node is directly connected to the jth node if graph[i][j] == 1.
> Some nodes initial are initially infected by malware. Whenever two nodes are directly connected, and at least one of those two nodes is infected by malware, both nodes will be infected by malware. This spread of malware will continue until no more nodes can be infected in this manner.
> Suppose M(initial) is the final number of nodes infected with malware in the entire network after the spread of malware stops. We will remove exactly one node from initial.
> Return the node that, if removed, would minimize M(initial). If multiple nodes could be removed to minimize M(initial), return such a node with the smallest index.
> Note that if a node was removed from the initial list of infected nodes, it might still be infected later due to the malware spread.
> 
> **Example 1:**
> ```
> Input: graph = [[1,1,0],[1,1,0],[0,0,1]], initial = [0,1]
> Output: 0
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[1,0,0],[0,1,0],[0,0,1]], initial = [0,2]
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: graph = [[1,1,1],[1,1,1],[1,1,1]], initial = [1,2]
> Output: 1
> ```
> 
> **Constraints:**
> - n == graph.length
> - n == graph[i].length
> - 2 <= n <= 300
> - graph[i][j] is 0 or 1.
> - graph[i][j] == graph[j][i]
> - graph[i][i] == 1
> - 1 <= initial.length <= n
> - 0 <= initial[i] <= n - 1
> - All the integers in initial are unique.

> [!info] Approach
> Malware spreads to the entire connected component. Removing node `x` only helps if `x` is the sole infected node in its component — otherwise another infected node spreads malware to that component anyway. DSU to find component sizes. For each component, count infected nodes. Only single-infected components are saveable. Build full DSU. Count infected nodes per component root. The best removal candidate is the infected node whose component has exactly 1 infected node and the largest size. Tie-break: smallest index.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def min_malware_spread(graph, initial):
>     n = len(graph)
>     dsu = DSU(n)
>     for i in range(n):
>         for j in range(i + 1, n):
>             if graph[i][j] == 1:
>                 dsu.union(i, j)
> 
>     infected_per_root = defaultdict(list)
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

### Longest Consecutive Sequence (DSU Approach) `🔥 Google`

> [!example] Problem
> Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
> You must write an algorithm that runs in O(n) time.
> 
> **Example 1:**
> ```
> Input: nums = [100,4,200,1,3,2]
> Output: 4
> Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,3,7,2,5,8,4,6,0,1]
> Output: 9
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,0,1,2]
> Output: 3
> ```
> 
> **Constraints:**
> - 0 <= nums.length <= 10^5
> - -10^9 <= nums[i] <= 10^9

> [!info] Approach
> `x` and `x+1` belong to the same consecutive run — union them. The largest component size is the answer. Map each value to an index; union `x` with `x+1` if `x+1` exists. Max component size = answer. Build `val → index` map. For each value, if `val+1` exists, union their indices.

> [!note]- Python Solution
> ```python
> def longest_consecutive(nums):
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
> You are given an undirected weighted graph of n nodes (0-indexed), represented by an edge list where edges[i] = [a, b] is an undirected edge connecting the nodes a and b with a probability of success of traversing that edge succProb[i].
> Given two nodes start and end, find the path with the maximum probability of success to go from start to end and return its success probability.
> If there is no path from start to end, return 0. Your answer will be accepted if it differs from the correct answer by at most 1e-5.
> 
> **Example 1:**
> ```
> Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2
> Output: 0.25000
> Explanation: There are two paths from start to end, one having a probability of success = 0.2 and the other has 0.5 * 0.5 = 0.25.
> ```
> 
> **Example 2:**
> ```
> Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.3], start = 0, end = 2
> Output: 0.30000
> ```
> 
> **Example 3:**
> ```
> Input: n = 3, edges = [[0,1]], succProb = [0.5], start = 0, end = 2
> Output: 0.00000
> Explanation: There is no path between 0 and 2.
> ```
> 
> **Constraints:**
> - 2 <= n <= 10^4
> - 0 <= start, end < n
> - start != end
> - 0 <= a, b < n
> - a != b
> - 0 <= succProb.length == edges.length <= 2*10^4
> - 0 <= succProb[i] <= 1
> - There is at most one edge between every two nodes.

> [!info] Approach
> For general graphs Dijkstra (max-heap variant) is canonical and handles multiple alternate paths. Weighted DSU works on trees — only one path exists between any two nodes. Weighted DSU where `weight[x]` = probability of `x` relative to its root. Query: `weight[start] / weight[end]` if same root. `union(A, B, p)`: adjust root weight so `weight[A] / weight[B] = p`. Valid only when graph is a tree.

> [!note]- Python Solution
> ```python
> def max_probability_dsu(n: int, edges: list[list[int]], succProb: list[float],
>                       start: int, end: int) -> float:
>     # Canonical solution: Dijkstra with max-heap (handles general graphs).
>     # DSU shown for tree-structured probability graphs only.
>     parent = list(range(n))
>     weight = [1.0] * n   # weight[x] = prob(x) / prob(root(x))
> 
>     def find(x):
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

### Redundant Connection II `🔥 Google`

> [!example] Problem
> In this problem, a rooted tree is a directed graph such that, there is exactly one node (the root) for which all other nodes are descendants of this node, plus every node has exactly one parent, except for the root node which has no parents.
> The given input is a directed graph that started as a rooted tree with n nodes (with distinct values from 1 to n), with one additional directed edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed.
> The resulting graph is given as a 2D-array of edges. Each element of edges is a pair [ui, vi] that represents a directed edge connecting nodes ui and vi, where ui is a parent of child vi.
> Return an edge that can be removed so that the resulting graph is a rooted tree of n nodes. If there are multiple answers, return the answer that occurs last in the given 2D-array.
> 
> **Example 1:**
> ```
> Input: edges = [[1,2],[1,3],[2,3]]
> Output: [2,3]
> ```
> 
> **Example 2:**
> ```
> Input: edges = [[1,2],[2,3],[3,4],[4,1],[1,5]]
> Output: [4,1]
> ```
> 
> **Constraints:**
> - n == edges.length
> - 3 <= n <= 1000
> - edges[i].length == 2
> - 1 <= ui, vi <= n
> - ui != vi

> [!info] Approach
> In a directed tree (rooted), every non-root has in-degree 1. The extra edge creates either (a) a node with in-degree 2, or (b) a cycle with all in-degrees 1, or (c) both. These three cases need separate handling. First detect any node with in-degree 2 — candidates `cand1` (first edge into it) and `cand2` (second edge). Then run DSU on all edges, skipping `cand2` if it exists. If a cycle forms, the redundant edge is `cand1` (if cand2 exists) or the cycle-forming edge (if no cand2). Pass 1: record in-degree-2 candidates. Pass 2: DSU union excluding `cand2`. If no cycle detected with `cand2` excluded → return `cand2`. If cycle detected and `cand1` exists → return `cand1`. If cycle and no candidate → return the cycle edge.

> [!note]- Python Solution
> ```python
> def find_redundant_directed_connection(edges):
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
>     def has_cycle_excluding(skip):
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

### Most Stones Removed with Same Row or Column

> [!example] Problem
> On a 2D plane, we place n stones at some integer coordinate points. Each coordinate point may have at most one stone.
> A stone can be removed if it shares either the same row or the same column as another stone that has not been removed.
> Given an array stones of length n where stones[i] = [xi, yi] represents the location of the ith stone, return the largest possible number of stones that can be removed.
> 
> **Example 1:**
> ```
> Input: stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
> Output: 5
> Explanation: One way to remove 5 stones is as follows:
> 1. Remove stone [2,2] because it shares the same row as [2,1].
> 2. Remove stone [2,1] because it shares the same column as [0,1].
> 3. Remove stone [1,2] because it shares the same row as [1,0].
> 4. Remove stone [1,0] because it shares the same column as [0,0].
> 5. Remove stone [0,1] because it shares the same row as [0,0].
> Stone [0,0] cannot be removed since it does not share a row/column with another stone still on the plane.
> ```
> 
> **Example 2:**
> ```
> Input: stones = [[0,0],[0,2],[1,1],[2,0],[2,2]]
> Output: 3
> Explanation: One way to make 3 moves is as follows:
> 1. Remove stone [2,2] because it shares the same row as [2,0].
> 2. Remove stone [2,0] because it shares the same column as [0,0].
> 3. Remove stone [0,2] because it shares the same row as [0,0].
> Stones [0,0] and [1,1] cannot be removed since they do not share a row/column with another stone still on the plane.
> ```
> 
> **Example 3:**
> ```
> Input: stones = [[0,0]]
> Output: 0
> Explanation: [0,0] is the only stone on the plane, so you cannot remove it.
> ```
> 
> **Constraints:**
> - 1 <= stones.length <= 1000
> - 0 <= xi, yi <= 10^4
> - No two stones are at the same coordinate point.

> [!info] Approach
> Stones in the same connected component (row/column sharing is transitive) can all be reduced to 1 stone. Answer = total stones − number of components. DSU where stones sharing a row or column are in the same component. Use coordinate compression: treat row `r` and column `c` as separate nodes with an offset to avoid collision. Map rows to `[0, 10000]` and cols to `[10001, 20001]`. Union `row_r` with `col_c` for each stone. Count distinct roots among only the stone positions.

> [!note]- Python Solution
> ```python
> def remove_stones(stones):
>     parent = {}
> 
>     def find(x):
>         if x not in parent:
>             parent[x] = x
>         if parent[x] != x:
>             parent[x] = find(parent[x])
>         return parent[x]
> 
>     def union(x, y):
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
> You are given two integer arrays, source and target, both of length n. You are also given an array allowedSwaps where each allowedSwaps[i] = [ai, bi] indicates that you are allowed to swap the elements at index ai and index bi (0-indexed) of array source. Note that you can swap elements at a specific pair of indices multiple times and in any order.
> The Hamming distance of two arrays of the same length, source and target, is the number of positions where the elements are different. Formally, it is the number of indices i for 0 <= i <= n-1 where source[i] != target[i] (0-indexed).
> Return the minimum Hamming distance of source and target after performing any amount of swap operations on array source.
> 
> **Example 1:**
> ```
> Input: source = [1,2,3,4], target = [2,1,4,5], allowedSwaps = [[0,1],[2,3]]
> Output: 1
> Explanation: source can be transformed the following way:
> - Swap indices 0 and 1: source = [2,1,3,4]
> - Swap indices 2 and 3: source = [2,1,4,3]
> The Hamming distance of source and target is 1 as they differ in 1 position: index 3.
> ```
> 
> **Example 2:**
> ```
> Input: source = [1,2,3,4], target = [1,3,2,4], allowedSwaps = []
> Output: 2
> Explanation: There are no allowed swaps.
> The Hamming distance of source and target is 2 as they differ in 2 positions: index 1 and index 2.
> ```
> 
> **Example 3:**
> ```
> Input: source = [5,1,2,4,3], target = [1,5,4,2,3], allowedSwaps = [[0,4],[4,2],[1,3],[1,4]]
> Output: 0
> ```
> 
> **Constraints:**
> - n == source.length == target.length
> - 1 <= n <= 10^5
> - 1 <= source[i], target[i] <= 10^5
> - 0 <= allowedSwaps.length <= 10^5
> - allowedSwaps[i].length == 2
> - 0 <= ai, bi <= n - 1
> - ai != bi

> [!info] Approach
> Swap pairs define groups of indices that can be freely rearranged among themselves. Within each group, match `source` values to `target` values optimally (minimize mismatches = maximize matches). DSU to find index groups. For each group, build frequency maps of `source` and `target` values; match greedily. For each DSU component, count how many `source[i]` values can be matched to `target[i]` values in the group. Unmatched positions contribute 1 each to Hamming distance.

> [!note]- Python Solution
> ```python
> from collections import Counter, defaultdict
> 
> def minimize_hamming_distance(source: list[int], target: list[int],
>                              allowedSwaps: list[list[int]]) -> int:
>     n = len(source)
>     dsu = DSU(n)
>     for u, v in allowedSwaps:
>         dsu.union(u, v)
> 
>     root_to_indices = defaultdict(list)
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

### Minimum Cost to Make at Least One Valid Path in a Grid `⭐ Google`

> [!example] Problem
> Given an m x n grid. Each cell of the grid has a sign pointing to the next cell you should visit if you are currently in this cell. The sign of grid[i][j] can be:
> Notice that there could be some signs on the cells of the grid that point outside the grid.
> You will initially start at the upper left cell (0, 0). A valid path in the grid is a path that starts from the upper left cell (0, 0) and ends at the bottom-right cell (m - 1, n - 1) following the signs on the grid. The valid path does not have to be the shortest.
> You can modify the sign on a cell with cost = 1. You can modify the sign on a cell one time only.
> Return the minimum cost to make the grid have at least one valid path.
> 
> **Example 1:**
> ```
> Input: grid = [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]]
> Output: 3
> Explanation: You will start at point (0, 0).
> The path to (3, 3) is as follows. (0, 0) --> (0, 1) --> (0, 2) --> (0, 3) change the arrow to down with cost = 1 --> (1, 3) --> (1, 2) --> (1, 1) --> (1, 0) change the arrow to down with cost = 1 --> (2, 0) --> (2, 1) --> (2, 2) --> (2, 3) change the arrow to down with cost = 1 --> (3, 3)
> The total cost = 3.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[1,1,3],[3,2,2],[1,1,4]]
> Output: 0
> Explanation: You can follow the path from (0, 0) to (2, 2).
> ```
> 
> **Example 3:**
> ```
> Input: grid = [[1,2],[4,3]]
> Output: 1
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 100
> - 1 <= grid[i][j] <= 4

> [!info] Approach
> Edge weights are 0 (follow direction) or 1 (change direction). This is a 0-1 BFS problem — but can also be viewed as DSU on "0-cost" groups followed by checking connectivity. 0-1 BFS: use deque; free (0-cost) moves go to front, cost-1 moves go to back. Process in Dijkstra-like order. For cell `(r,c)`, the free neighbor is determined by `grid[r][c]`. All other neighbors cost 1. Track `dist` array initialized to infinity.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def min_cost(grid):
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
> Alice and Bob have an undirected graph of n nodes and three types of edges:
> Given an array edges where edges[i] = [typei, ui, vi] represents a bidirectional edge of type typei between nodes ui and vi, find the maximum number of edges you can remove so that after removing the edges, the graph can still be fully traversed by both Alice and Bob. The graph is fully traversed by Alice and Bob if starting from any node, they can reach all other nodes.
> Return the maximum number of edges you can remove, or return -1 if Alice and Bob cannot fully traverse the graph.
> 
> **Example 1:**
> ```
> Input: n = 4, edges = [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]
> Output: 2
> Explanation: If we remove the 2 edges [1,1,2] and [1,1,3]. The graph will still be fully traversable by Alice and Bob. Removing any additional edge will not make it so. So the maximum number of edges we can remove is 2.
> ```
> 
> **Example 2:**
> ```
> Input: n = 4, edges = [[3,1,2],[3,2,3],[1,1,4],[2,1,4]]
> Output: 0
> Explanation: Notice that removing any edge will not make the graph fully traversable by Alice and Bob.
> ```
> 
> **Example 3:**
> ```
> Input: n = 4, edges = [[3,2,3],[1,1,2],[2,3,4]]
> Output: -1
> Explanation: In the current graph, Alice cannot reach node 4 from the other nodes. Likewise, Bob cannot reach 1. Therefore it's impossible to make the graph fully traversable.
> ```
> 
> **Constraints:**
> - 1 <= n <= 10^5
> - 1 <= edges.length <= min(10^5, 3 * n * (n - 1) / 2)
> - edges[i].length == 3
> - 1 <= typei <= 3
> - 1 <= ui < vi <= n
> - All tuples (typei, ui, vi) are distinct.

> [!info] Approach
> We want minimal spanning forest for Alice and Bob independently. Shared edges (type 3) are doubly valuable — use them first. Any edge that doesn't reduce components is redundant. Run two DSUs (Alice, Bob). Process type-3 edges first (union in both). Then type-1 in Alice's DSU, type-2 in Bob's. Count edges used; answer = total edges − edges used. An edge is removable if its union returns `False` in both relevant DSUs. Final check: both DSUs must reach 1 component, else return -1.

> [!note]- Python Solution
> ```python
> def max_num_edges_to_remove(n, edges):
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

### Making a Large Island `⭐ Google`

> [!example] Problem
> You are given an n x n binary matrix grid. You are allowed to change at most one 0 to be 1.
> Return the size of the largest island in grid after applying this operation.
> An island is a 4-directionally connected group of 1s.
> 
> **Example 1:**
> ```
> Input: grid = [[1,0],[0,1]]
> Output: 3
> Explanation: Change one 0 to 1 and connect two 1s, then we get an island with area = 3.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[1,1],[1,0]]
> Output: 4
> Explanation: Change the 0 to 1 and make the island bigger, only one island with area = 4.
> ```
> 
> **Example 3:**
> ```
> Input: grid = [[1,1],[1,1]]
> Output: 4
> Explanation: Can't change any 0 to 1, only one island with area = 4.
> ```
> 
> **Constraints:**
> - n == grid.length
> - n == grid[i].length
> - 1 <= n <= 500
> - grid[i][j] is either 0 or 1.

> [!info] Approach
> After flipping a 0, the new cell connects up to 4 adjacent islands. Island sizes are needed instantly → DSU component sizes. Build DSU over existing 1-cells. For each 0-cell, sum sizes of distinct adjacent components + 1. Track overall max. Label each cell's DSU root. For each 0-cell, collect unique roots of neighboring 1-cells (avoid double-counting same component), sum their sizes.

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
>     best = max((dsu.component_size(r*n+c) for r in range(n)
>                 for c in range(n) if grid[r][c] == 1), default=0)
> 
>     for r in range(n):
>         for c in range(n):
>             if grid[r][c] == 0:
>                 seen_roots = set()
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
> There is a tree (i.e. a connected, undirected graph with no cycles) consisting of n nodes numbered from 0 to n - 1 and exactly n - 1 edges.
> You are given a 0-indexed integer array vals of length n where vals[i] denotes the value of the ith node. You are also given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting nodes ai and bi.
> A good path is a simple path that satisfies the following conditions:
> Return the number of distinct good paths.
> Note that a path and its reverse are counted as the same path. For example, 0 -> 1 is considered to be the same as 1 -> 0. A single node is also considered as a valid path.
> 
> **Example 1:**
> ```
> Input: vals = [1,3,2,1,3], edges = [[0,1],[0,2],[2,3],[2,4]]
> Output: 6
> Explanation: There are 5 good paths consisting of a single node.
> There is 1 additional good path: 1 -> 0 -> 2 -> 4.
> (The reverse path 4 -> 2 -> 0 -> 1 is treated as the same as 1 -> 0 -> 2 -> 4.)
> Note that 0 -> 2 -> 3 is not a good path because vals[2] > vals[0].
> ```
> 
> **Example 2:**
> ```
> Input: vals = [1,1,2,2,3], edges = [[0,1],[1,2],[2,3],[2,4]]
> Output: 7
> Explanation: There are 5 good paths consisting of a single node.
> There are 2 additional good paths: 0 -> 1 and 2 -> 3.
> ```
> 
> **Example 3:**
> ```
> Input: vals = [1], edges = []
> Output: 1
> Explanation: The tree consists of only one node, so there is one good path.
> ```
> 
> **Constraints:**
> - n == vals.length
> - 1 <= n <= 3 * 10^4
> - 0 <= vals[i] <= 10^5
> - edges.length == n - 1
> - edges[i].length == 2
> - 0 <= ai, bi < n
> - ai != bi
> - edges represents a valid tree.

> [!info] Approach
> Process nodes in increasing order of value. When adding a node, union it with already-processed neighbors. Two same-value nodes in the same component form `count*(count-1)/2` new paths. Sort nodes by value. Process batches of equal value. Union nodes in each batch with lower-valued neighbors. Count pairs within the merged component. Group nodes by value. For each value group, union all nodes of that value with their neighbors (which have ≤ current value). Count same-value nodes per component root; add `k*(k+1)/2` where `k` = count.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def number_of_good_paths(vals, edges):
>     n = len(vals)
>     adj = defaultdict(list)
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

### Largest Component Size by Common Factor `⭐ Google`

> [!example] Problem
> You are given an integer array of unique positive integers nums. Consider the following graph:
> Return the size of the largest connected component in the graph.
> 
> **Example 1:**
> ```
> Input: nums = [4,6,15,35]
> Output: 4
> ```
> 
> **Example 2:**
> ```
> Input: nums = [20,50,9,63]
> Output: 2
> ```
> 
> **Example 3:**
> ```
> Input: nums = [2,3,6,7,4,12,21,39]
> Output: 8
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - 1 <= nums[i] <= 10^5
> - All the values of nums are unique.

> [!info] Approach
> Shared prime factors link numbers together transitively. Union each number with all its prime factors; then prime factors link all numbers sharing them. For each number, factorize it, union the number with each of its prime factors. Count max component size. Nodes are both numbers (index) and prime factors (up to max value). Use dict-based DSU. For each `nums[i]`, find primes, union `nums[i]` with each prime, then count component size for each original number.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def largest_component_size(nums):
>     parent = {}
> 
>     def find(x):
>         if x not in parent:
>             parent[x] = x
>         if parent[x] != x:
>             parent[x] = find(parent[x])
>         return parent[x]
> 
>     def union(x, y):
>         px, py = find(x), find(y)
>         if px != py:
>             parent[px] = py
> 
>     def prime_factors(n):
>         factors = []
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
>     comp_size = defaultdict(int)
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
### Accounts Merge `🔥 Google`

> [!example] Problem
> Given a list of accounts where each element accounts[i] is a list of strings, where the first element accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account.
> Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.
> After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order.
> 
> **Example 1:**
> ```
> Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
> Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
> Explanation:
> The first and second John's are the same person as they have the common email "johnsmith@mail.com".
> The third John and Mary are different people as none of their email addresses are used by other accounts.
> We could return these lists in any order, for example the answer [['Mary', 'mary@mail.com'], ['John', 'johnnybravo@mail.com'], 
> ['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com']] would still be accepted.
> ```
> 
> **Example 2:**
> ```
> Input: accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
> Output: [["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]
> ```
> 
> **Constraints:**
> - 1 <= accounts.length <= 1000
> - 2 <= accounts[i].length <= 10
> - 1 <= accounts[i][j].length <= 30
> - accounts[i][0] consists of English letters.
> - accounts[i][j] (for j > 0) is a valid email.

> [!info] Approach
> Shared emails create connected components. If two accounts share any email, they belong to the same merged group. Use DSU to union all emails in the same account. Then group emails by final root. Map each email to the first owner seen. When a new account contains an already-seen email, union the account’s emails together under that root.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def accounts_merge(accounts):
>     parent = {}
> 
>     def find(x):
>         parent.setdefault(x, x)
>         if parent[x] != x:
>             parent[x] = find(parent[x])
>         return parent[x]
> 
>     def union(a, b):
>         parent[find(a)] = find(b)
> 
>     email_to_name = {}
>     for account in accounts:
>         name = account[0]
>         first_email = account[1]
>         for email in account[1:]:
>             email_to_name[email] = name
>             union(first_email, email)
> 
>     groups = defaultdict(list)
>     for email in email_to_name:
>         groups[find(email)].append(email)
> 
>     return [[email_to_name[root]] + sorted(emails) for root, emails in groups.items()]
> ```

> [!success] Complexity
> Roughly O(E α(E)) time for union-find plus sorting within each merged account; O(E) space.

> [!tip] Alternatives
> DFS on the email graph also works; DSU is often simpler to explain for merge-by-connection problems.

---

## Union-Find — More Problems

### Redundant Connection II (LC 685, Directed Graph) `🔥 Google`

> [!example] Problem
> In this problem, a rooted tree is a directed graph such that, there is exactly one node (the root) for which all other nodes are descendants of this node, plus every node has exactly one parent, except for the root node which has no parents.
> The given input is a directed graph that started as a rooted tree with n nodes (with distinct values from 1 to n), with one additional directed edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed.
> The resulting graph is given as a 2D-array of edges. Each element of edges is a pair [ui, vi] that represents a directed edge connecting nodes ui and vi, where ui is a parent of child vi.
> Return an edge that can be removed so that the resulting graph is a rooted tree of n nodes. If there are multiple answers, return the answer that occurs last in the given 2D-array.
> 
> **Example 1:**
> ```
> Input: edges = [[1,2],[1,3],[2,3]]
> Output: [2,3]
> ```
> 
> **Example 2:**
> ```
> Input: edges = [[1,2],[2,3],[3,4],[4,1],[1,5]]
> Output: [4,1]
> ```
> 
> **Constraints:**
> - n == edges.length
> - 3 <= n <= 1000
> - edges[i].length == 2
> - 1 <= ui, vi <= n
> - ui != vi

> [!info] Approach
> In a directed rooted tree, every node except the root has exactly one parent. Adding an edge creates either: (a) a node with two parents, or (b) a cycle, or both. We must identify which case applies and choose the correct redundant edge. First pass: find any node with two incoming edges (`cand1`, `cand2`). If found, one of them is the answer. Second pass: use Union-Find ignoring one candidate. If a cycle forms, the other candidate (or the cycle-forming edge) is the answer.

>   1. Scan edges; track `parent` for each node. If a node already has a parent, record `cand1 = prev_edge`, `cand2 = current_edge` and skip `cand2`.
>   2. Run Union-Find on remaining edges. If a cycle forms and `cand1` exists, return `cand1`; else return the cycle edge. If no cycle and `cand2` exists, return `cand2`.

> [!note]- Python Solution
> ```python
> def find_redundant_directed_connection(edges):
>     n = len(edges)
>     parent = list(range(n + 1))
>     cand1 = cand2 = None
>     node_parent = {}
>     filtered = []
>     for u, v in edges:
>         if v in node_parent:
>             cand1 = [node_parent[v], v]
>             cand2 = [u, v]
>         else:
>             node_parent[v] = u
>             filtered.append([u, v])
> >
>     def find(x):
>         while parent[x] != x:
>             parent[x] = parent[parent[x]]
>             x = parent[x]
>         return x
> >
>     def union(u, v):
>         pu = find(u)
>         pv = find(v)
>         if pu == pv:
>             return False
>         parent[pu] = pv
>         return True
> >
>     for u, v in filtered:
>         if not union(u, v):
>             return cand1 if cand1 else [u, v]
>     return cand2
> ```

> [!success] Complexity
> Time O(E α(E)), Space O(E).

> [!tip] Alternatives
> - Pure DFS cycle detection: works but harder to correctly handle the "two parents" case.
> - Key insight: the two cases (double-parent vs pure cycle) require different edge choices; the filtering step separates them cleanly.

---

### Smallest String With Swaps (LC 1202)

> [!example] Problem
> You are given a string s, and an array of pairs of indices in the string pairs where pairs[i] = [a, b] indicates 2 indices(0-indexed) of the string.
> You can swap the characters at any pair of indices in the given pairs any number of times.
> Return the lexicographically smallest string that s can be changed to after using the swaps.
> 
> **Example 1:**
> ```
> Input: s = "dcab", pairs = [[0,3],[1,2]]
> Output: "bacd"
> Explaination: 
> Swap s[0] and s[3], s = "bcad"
> Swap s[1] and s[2], s = "bacd"
> ```
> 
> **Example 2:**
> ```
> Input: s = "dcab", pairs = [[0,3],[1,2],[0,2]]
> Output: "abcd"
> Explaination: 
> Swap s[0] and s[3], s = "bcad"
> Swap s[0] and s[2], s = "acbd"
> Swap s[1] and s[2], s = "abcd"
> ```
> 
> **Example 3:**
> ```
> Input: s = "cba", pairs = [[0,1],[1,2]]
> Output: "abc"
> Explaination: 
> Swap s[0] and s[1], s = "bca"
> Swap s[1] and s[2], s = "bac"
> Swap s[0] and s[1], s = "abc"
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - 0 <= pairs.length <= 10^5
> - 0 <= pairs[i][0], pairs[i][1] < s.length
> - s only contains lower case English letters.

> [!info] Approach
> Indices connected by swap pairs (directly or transitively) can be rearranged freely. Use Union-Find to group connected indices, then sort each group's characters and reassign them in sorted order to the smallest positions. Union all paired indices. Group indices by root. For each group, collect the characters at those indices, sort them, and reassign the sorted characters to the sorted indices. `collections.defaultdict(list)` — `groups[find(i)].append(i)` for all `i`. For each group, sort both the indices and the characters, then assign characters back.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def smallest_string_with_swaps(s, pairs):
>     n = len(s)
>     parent = list(range(n))
> >
>     def find(x):
>         while parent[x] != x:
>             parent[x] = parent[parent[x]]
>             x = parent[x]
>         return x
> >
>     def union(x, y):
>         parent[find(x)] = find(y)
> >
>     for u, v in pairs:
>         union(u, v)
> >
>     groups = defaultdict(list)
>     for i in range(n):
>         groups[find(i)].append(i)
> >
>     result = list(s)
>     for indices in groups.values():
>         chars = sorted(result[i] for i in indices)
>         for i, ch in zip(sorted(indices), chars):
>             result[i] = ch
>     return ''.join(result)
> ```

> [!success] Complexity
> Time O((N + E) α(N) + N log N), Space O(N).

> [!tip] Alternatives
> - DFS/BFS to find connected components: same idea, same complexity, slightly more code.
> - Key insight: any permutation of characters within a connected component is achievable via adjacent swaps through the union edges.

---

## See Also (Extended)

[[graph]] | [[sorting]] | [[backtracking]] | [[dynamic-programming]]
