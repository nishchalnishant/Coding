---
tags: [coding, algorithms, graph-algorithms]
topic: Graph Algorithms
difficulty: mixed
---

# Graph Algorithms — Problem Deep Dives

---

## Dijkstra's Algorithm

### Network Delay Time

> [!example] Problem
> Directed weighted graph, `n` nodes, edges `[u, v, w]`. Signal sent from `k` — find the time for the signal to reach all nodes. Return `-1` if unreachable.

> [!info] Approach
> - **WHY:** Shortest paths from a single source with non-negative weights. Each node's final distance must be optimal before we use it to relax neighbors.
> - **WHAT:** Greedy SSSP — always expand the globally cheapest unvisited node.
> - **HOW:** Min-heap of `(dist, node)`. Lazy deletion guard `if d > dist[u]: continue` discards stale heap entries. Answer = `max(dist.values())`; if any node has `inf` distance, return `-1`.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> 
> def networkDelayTime(times: list[list[int]], n: int, k: int) -> int:
>     graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
>     for u, v, w in times:
>         graph[u].append((w, v))
> 
>     dist = {i: float('inf') for i in range(1, n + 1)}
>     dist[k] = 0
>     heap = [(0, k)]
> 
>     while heap:
>         d, u = heapq.heappop(heap)
>         if d > dist[u]:
>             continue  # stale entry
>         for w, v in graph[u]:
>             if dist[u] + w < dist[v]:
>                 dist[v] = dist[u] + w
>                 heapq.heappush(heap, (dist[v], v))
> 
>     max_dist = max(dist.values())
>     return max_dist if max_dist < float('inf') else -1
> ```

> [!success] Complexity
> Time O((V + E) log V), Space O(V + E).

> [!tip] Alternatives
> Bellman-Ford O(VE) — overkill but handles negative weights. SPFA — average O(E) but O(VE) worst case.

---

### Swim in Rising Water

> [!example] Problem
> N×N grid, `grid[i][j]` = elevation. At time `t`, can swim in any cell with elevation ≤ t. Find minimum `t` to swim from `(0,0)` to `(N-1,N-1)`.

> [!info] Approach
> - **WHY:** We want to minimize the maximum elevation encountered along a path — a min-bottleneck path problem.
> - **WHAT:** Dijkstra where `dist[cell]` = minimum possible max-elevation to reach that cell.
> - **HOW:** Heap entry `(max_elevation_on_path, r, c)`. At each step, `cost(u→v) = max(current_max, grid[v])`. The first time we pop `(N-1,N-1)` is the answer.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def swimInWater(grid: list[list[int]]) -> int:
>     n = len(grid)
>     dist = [[float('inf')] * n for _ in range(n)]
>     dist[0][0] = grid[0][0]
>     heap = [(grid[0][0], 0, 0)]
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     while heap:
>         t, r, c = heapq.heappop(heap)
>         if t > dist[r][c]:
>             continue
>         if r == n - 1 and c == n - 1:
>             return t
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < n and 0 <= nc < n:
>                 new_t = max(t, grid[nr][nc])
>                 if new_t < dist[nr][nc]:
>                     dist[nr][nc] = new_t
>                     heapq.heappush(heap, (new_t, nr, nc))
> 
>     return dist[n-1][n-1]
> ```

> [!success] Complexity
> Time O(N² log N), Space O(N²).

> [!tip] Alternatives
> Binary search on `t` + BFS/DFS for feasibility — O(N² log N) same asymptotic. DSU: union cells with elevation ≤ t while incrementing t — O(N²α).

---

### Path with Maximum Probability

> [!example] Problem
> Undirected graph, edges with success probabilities. Find the path from `start` to `end` maximizing product of probabilities.

> [!info] Approach
> - **WHY:** Maximize a product along a path — same structure as shortest path but with max-product instead of min-sum.
> - **WHAT:** Dijkstra variant with max-heap; `dist[v]` = max probability to reach `v`.
> - **HOW:** Negate heap values for max-heap (or use `-prob`). Relaxation: `prob[u] * w > prob[v]` → update. All probabilities in [0,1] — no negative-weight issues.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> 
> def maxProbability(n: int, edges: list[list[int]], succProb: list[float],
>                    start: int, end: int) -> float:
>     graph: dict[int, list[tuple[float, int]]] = defaultdict(list)
>     for (u, v), p in zip(edges, succProb):
>         graph[u].append((p, v))
>         graph[v].append((p, u))
> 
>     prob = [0.0] * n
>     prob[start] = 1.0
>     heap = [(-1.0, start)]  # max-heap via negation
> 
>     while heap:
>         neg_p, u = heapq.heappop(heap)
>         p = -neg_p
>         if p < prob[u]:
>             continue
>         if u == end:
>             return p
>         for edge_p, v in graph[u]:
>             new_p = prob[u] * edge_p
>             if new_p > prob[v]:
>                 prob[v] = new_p
>                 heapq.heappush(heap, (-new_p, v))
> 
>     return 0.0
> ```

> [!success] Complexity
> Time O((V + E) log V), Space O(V + E).

> [!tip] Alternatives
> Log transform `−log(p)` → additive min-cost shortest path with standard Dijkstra. BFS won't work (weighted graph).

---

### Evaluate Division (LC 399)

> [!example] Problem
> Given equations like `["a/b"=2.0, "b/c"=3.0]` and queries like `"a/c"`, `"b/a"`, return the division results. Return `-1.0` if the answer doesn't exist.

> [!info] Approach
> - **WHY:** Division is transitive — `a/c = (a/b) * (b/c)`. Model as a weighted directed graph: edge `a→b` with weight `2.0` and `b→a` with weight `0.5`.
> - **WHAT:** Build weighted graph. For each query `(src, dst)`, run BFS/DFS from `src` to `dst` multiplying edge weights. If `dst` is unreachable, return `-1.0`.
> - **HOW:** Build adjacency list `{node: [(neighbor, weight)]}`. BFS with `(node, product)` in queue. Track visited. Return product when `dst` found.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def calcEquation(equations: list[list[str]], values: list[float],
>                  queries: list[list[str]]) -> list[float]:
>     graph: dict[str, list[tuple[str, float]]] = defaultdict(list)
>     for (u, v), w in zip(equations, values):
>         graph[u].append((v, w))
>         graph[v].append((u, 1.0 / w))
> 
>     def bfs(src: str, dst: str) -> float:
>         if src not in graph or dst not in graph:
>             return -1.0
>         if src == dst:
>             return 1.0
>         visited = {src}
>         q: deque[tuple[str, float]] = deque([(src, 1.0)])
>         while q:
>             node, product = q.popleft()
>             for nb, w in graph[node]:
>                 if nb == dst:
>                     return product * w
>                 if nb not in visited:
>                     visited.add(nb)
>                     q.append((nb, product * w))
>         return -1.0
> 
>     return [bfs(s, t) for s, t in queries]
> ```

> [!success] Complexity
> Time O(Q·(V+E)) where Q = number of queries, Space O(V+E).

> [!tip] Alternatives
> Floyd-Warshall for all-pairs O(V³) — good if queries are many and V is small. Union-Find with weighted ranks — tracks ratios relative to a root representative per component.

---

### Cheapest Flights Within K Stops (Dijkstra variant)

> [!info] Approach
> See also Bellman-Ford section — that is the canonical approach. Dijkstra with state `(cost, node, stops_used)`:
> - **WHY:** Dijkstra expands cheapest cost first, but ignores stop count — must encode stops in state.
> - **WHAT:** State space is `(node, stops_used)`. Prune if stops exceeded.
> - **HOW:** Heap `(cost, node, stops)`. Mark visited as `(node, stops)` pair. Bellman-Ford is simpler for this problem; Dijkstra works but requires careful pruning.

See full Bellman-Ford solution in the next section.

---

## Bellman-Ford

### Cheapest Flights Within K Stops

> [!example] Problem
> `n` cities, directed flights `[from, to, price]`. Find cheapest price from `src` to `dst` with at most `k` stops (= at most `k+1` edges).

> [!info] Approach
> - **WHY:** Standard Dijkstra doesn't track hop count. Bellman-Ford runs exactly `k+1` relaxation rounds — round `i` gives optimal cost using ≤ `i` edges.
> - **WHAT:** Bounded Bellman-Ford: `k+1` rounds, each relaxing all edges.
> - **HOW:** Critical — use a copy of `prices` each round (`temp = prices[:]`). Without the copy, a single round might chain multiple hops, violating the hop bound.

> [!note]- Python Solution
> ```python
> def findCheapestPrice(n: int, flights: list[list[int]],
>                       src: int, dst: int, k: int) -> int:
>     prices = [float('inf')] * n
>     prices[src] = 0
> 
>     for _ in range(k + 1):
>         temp = prices[:]          # snapshot: prevent chaining within one round
>         for u, v, w in flights:
>             if prices[u] != float('inf') and prices[u] + w < temp[v]:
>                 temp[v] = prices[u] + w
>         prices = temp
> 
>     return prices[dst] if prices[dst] != float('inf') else -1
> ```

> [!success] Complexity
> Time O(k × E), Space O(V).

> [!tip] Alternatives
> Dijkstra with state `(cost, node, stops)` — O(E·k·log(Vk)). BFS layer-by-layer (same logic as Bellman-Ford). Standard Dijkstra without stop tracking is incorrect.

---

### Find the City with the Smallest Number of Neighbors at a Threshold Distance (Floyd-Warshall)

> [!example] Problem
> `n` cities, undirected weighted edges, distance threshold. Find the city with the fewest reachable cities (within threshold); if tie, return largest city index.

> [!info] Approach
> - **WHY:** Need all-pairs shortest paths. Running Dijkstra from each city is O(V·E·log V); Floyd-Warshall is O(V³) which is cleaner for small V (≤ 100 here).
> - **WHAT:** Floyd-Warshall DP: `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])` for all intermediates `k`.
> - **HOW:** Initialize diagonal to 0, direct edges to weight, rest to inf. `k` must be the outermost loop. After running, count neighbors within threshold for each city.

> [!note]- Python Solution
> ```python
> def findTheCity(n: int, edges: list[list[int]], distanceThreshold: int) -> int:
>     dist = [[float('inf')] * n for _ in range(n)]
>     for i in range(n):
>         dist[i][i] = 0
>     for u, v, w in edges:
>         dist[u][v] = dist[v][u] = w
> 
>     for k in range(n):          # k MUST be outermost
>         for i in range(n):
>             for j in range(n):
>                 if dist[i][k] + dist[k][j] < dist[i][j]:
>                     dist[i][j] = dist[i][k] + dist[k][j]
> 
>     result, min_count = -1, n
>     for city in range(n):
>         count = sum(1 for j in range(n) if j != city and dist[city][j] <= distanceThreshold)
>         if count <= min_count:  # >= city index wins ties
>             min_count, result = count, city
> 
>     return result
> ```

> [!success] Complexity
> Time O(V³), Space O(V²).

> [!tip] Alternatives
> Dijkstra from each city O(V·E·log V) — worse for dense graphs. Acceptable if V > 500.

---

## Topological Sort (BFS — Kahn's)

### Course Schedule

> [!example] Problem
> `numCourses` courses, prerequisites `[a, b]` meaning must take `b` before `a`. Can you finish all courses?

> [!info] Approach
> - **WHY:** A valid schedule exists iff the dependency graph is a DAG. Cycle = impossible.
> - **WHAT:** Kahn's BFS topological sort — process zero-in-degree nodes first; if all nodes processed → DAG.
> - **HOW:** Build adjacency list and in-degree array. BFS from zero-in-degree nodes; decrement neighbors. If `processed == numCourses` → no cycle.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
>     graph: dict[int, list[int]] = defaultdict(list)
>     indegree = [0] * numCourses
> 
>     for a, b in prerequisites:
>         graph[b].append(a)      # b must come before a
>         indegree[a] += 1
> 
>     q = deque(i for i in range(numCourses) if indegree[i] == 0)
>     processed = 0
> 
>     while q:
>         u = q.popleft()
>         processed += 1
>         for v in graph[u]:
>             indegree[v] -= 1
>             if indegree[v] == 0:
>                 q.append(v)
> 
>     return processed == numCourses
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> DFS with 3-color marking (white/gray/black) — gray→gray back edge = cycle. Same complexity. Kahn's is preferred for clear cycle detection via count check.

---

### Course Schedule II

> [!example] Problem
> Same as Course Schedule — return a valid ordering of courses, or `[]` if impossible.

> [!info] Approach
> - **WHY:** Need an actual topological ordering, not just feasibility.
> - **WHAT:** Kahn's BFS — nodes dequeued in topological order.
> - **HOW:** Collect dequeued nodes into `order`. If `len(order) == numCourses` → valid. Otherwise cycle exists.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
>     graph: dict[int, list[int]] = defaultdict(list)
>     indegree = [0] * numCourses
> 
>     for a, b in prerequisites:
>         graph[b].append(a)
>         indegree[a] += 1
> 
>     q = deque(i for i in range(numCourses) if indegree[i] == 0)
>     order: list[int] = []
> 
>     while q:
>         u = q.popleft()
>         order.append(u)
>         for v in graph[u]:
>             indegree[v] -= 1
>             if indegree[v] == 0:
>                 q.append(v)
> 
>     return order if len(order) == numCourses else []
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> DFS post-order reversal — add node to result after all descendants processed; reverse at end.

---

### Alien Dictionary

> [!example] Problem
> Sorted list of words in alien language. Derive character ordering. Return valid order or `""` if contradictory.

> [!info] Approach
> - **WHY:** Adjacent sorted words reveal one ordering constraint each (first differing character). Build a DAG of character constraints, topological sort.
> - **WHAT:** Extract edges from adjacent word pairs; Kahn's on the character graph.
> - **HOW:** For each pair `(words[i], words[i+1])`, find first differing character — adds directed edge. Invalid: if word A is a proper prefix of word B but A appears after B. Cycle in graph → `""`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def alienOrder(words: list[str]) -> str:
>     graph: dict[str, list[str]] = defaultdict(list)
>     indegree: dict[str, int] = {c: 0 for word in words for c in word}
> 
>     for i in range(len(words) - 1):
>         w1, w2 = words[i], words[i + 1]
>         min_len = min(len(w1), len(w2))
>         if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
>             return ""                    # invalid: longer word is prefix of shorter
>         for j in range(min_len):
>             if w1[j] != w2[j]:
>                 graph[w1[j]].append(w2[j])
>                 indegree[w2[j]] += 1
>                 break
> 
>     q = deque(c for c in indegree if indegree[c] == 0)
>     result: list[str] = []
> 
>     while q:
>         c = q.popleft()
>         result.append(c)
>         for nb in graph[c]:
>             indegree[nb] -= 1
>             if indegree[nb] == 0:
>                 q.append(nb)
> 
>     return "".join(result) if len(result) == len(indegree) else ""
> ```

> [!success] Complexity
> Time O(C) where C = total characters across all words, Space O(1) (at most 26 nodes).

> [!tip] Alternatives
> DFS topo sort with cycle coloring. Both O(C).

---

### Sequence Reconstruction (Check Unique Topo Order)

> [!example] Problem
> Given `nums = [1..n]` and sequences, check if `nums` is the only shortest supersequence.

> [!info] Approach
> - **WHY:** `nums` is the unique shortest supersequence iff the topological order derived from all constraints is unique — meaning at every step, exactly one node has in-degree 0.
> - **WHAT:** Build dependency graph from consecutive pairs in each sequence. Run Kahn's; check uniqueness at every BFS step.
> - **HOW:** If at any point the queue has more than one element → multiple valid orderings → not unique. Also verify the final order equals `nums`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def sequenceReconstruction(nums: list[int], sequences: list[list[int]]) -> bool:
>     n = len(nums)
>     graph: dict[int, set[int]] = defaultdict(set)
>     indegree = {i: 0 for i in range(1, n + 1)}
> 
>     for seq in sequences:
>         for i in range(len(seq) - 1):
>             u, v = seq[i], seq[i + 1]
>             if v not in graph[u]:
>                 graph[u].add(v)
>                 indegree[v] += 1
> 
>     q = deque(node for node in indegree if indegree[node] == 0)
>     order: list[int] = []
> 
>     while q:
>         if len(q) > 1:
>             return False            # multiple choices → not unique
>         u = q.popleft()
>         order.append(u)
>         for v in graph[u]:
>             indegree[v] -= 1
>             if indegree[v] == 0:
>                 q.append(v)
> 
>     return order == nums
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> DFS — harder to check uniqueness cleanly. Kahn's is the natural fit.

---

### Find All Possible Recipes from Given Supplies

> [!example] Problem
> Recipes require ingredients. Ingredients can be supplies (always available) or other recipes. Find all recipes that can be made.

> [!info] Approach
> - **WHY:** Recipe dependencies form a DAG. A recipe is achievable iff all its dependencies are achievable — topological order.
> - **WHAT:** Kahn's BFS — supplies have in-degree 0. Process in topological order; when a recipe's in-degree reaches 0, it can be made.
> - **HOW:** Treat recipes and supplies as nodes. Edges: ingredient → recipe (ingredient must precede recipe). Initialize queue with all supply nodes.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def findAllRecipes(recipes: list[str], ingredients: list[list[str]],
>                    supplies: list[str]) -> list[str]:
>     graph: dict[str, list[str]] = defaultdict(list)
>     indegree: dict[str, int] = defaultdict(int)
> 
>     recipe_set = set(recipes)
> 
>     for recipe, ing_list in zip(recipes, ingredients):
>         for ing in ing_list:
>             graph[ing].append(recipe)
>             indegree[recipe] += 1
> 
>     q = deque(supplies)
>     result: list[str] = []
> 
>     while q:
>         item = q.popleft()
>         if item in recipe_set:
>             result.append(item)
>         for dep in graph[item]:
>             indegree[dep] -= 1
>             if indegree[dep] == 0:
>                 q.append(dep)
> 
>     return result
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> DFS memoization — mark each recipe as possible/impossible/unknown. Same complexity but Kahn's handles cycles automatically.

---

## Strongly Connected Components / Bridges

### Critical Connections in a Network (Tarjan's Bridges)

> [!example] Problem
> Undirected connected graph. Find all edges whose removal disconnects the graph.

> [!info] Approach
> - **WHY:** A bridge is an edge with no alternative path — its removal increases connected components.
> - **WHAT:** Tarjan's bridge-finding: DFS assigns `disc[]` (discovery time) and `low[]` (earliest disc reachable from subtree). Edge `(u,v)` is a bridge iff `low[v] > disc[u]`.
> - **HOW:** DFS from any node. When backtracking from child `v` to parent `u`: `low[u] = min(low[u], low[v])`. For already-visited back edges (non-parent): `low[u] = min(low[u], disc[v])`. Bridge condition: `low[v] > disc[u]`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def criticalConnections(n: int, connections: list[list[int]]) -> list[list[int]]:
>     graph: dict[int, list[int]] = defaultdict(list)
>     for u, v in connections:
>         graph[u].append(v)
>         graph[v].append(u)
> 
>     disc = [-1] * n
>     low = [-1] * n
>     timer = [0]
>     bridges: list[list[int]] = []
> 
>     def dfs(u: int, parent: int) -> None:
>         disc[u] = low[u] = timer[0]
>         timer[0] += 1
>         for v in graph[u]:
>             if v == parent:
>                 continue
>             if disc[v] == -1:
>                 dfs(v, u)
>                 low[u] = min(low[u], low[v])
>                 if low[v] > disc[u]:        # bridge condition
>                     bridges.append([u, v])
>             else:
>                 low[u] = min(low[u], disc[v])
> 
>     dfs(0, -1)
>     return bridges
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> Naive — remove each edge, check connectivity: O(E·(V+E)). Articulation-point variant for cut vertices. Multi-edge graphs: track parent edge index, not node.

---

### Strongly Connected Components (Kosaraju's Algorithm)

> [!example] Problem
> Directed graph with `n` nodes and `edges`. Find all strongly connected components (SCCs) — maximal subgraphs where every node is reachable from every other node.

> [!info] Approach
> - **WHY:** SCC decomposition reveals the "condensation DAG" of a graph — each SCC collapses into one node. Essential for dependency analysis, 2-SAT, and reachability.
> - **WHAT:** Kosaraju's two-pass DFS: first pass on original graph records finish order; second pass on reversed graph processes in reverse finish order — each DFS tree in pass 2 is one SCC.
> - **HOW:** Pass 1 — DFS original graph, push nodes to stack in finish order. Pass 2 — reverse all edges, pop from stack, DFS the reversed graph; each connected component found = one SCC.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def kosaraju_sccs(n: int, edges: list[list[int]]) -> list[list[int]]:
>     graph: dict[int, list[int]] = defaultdict(list)
>     rev_graph: dict[int, list[int]] = defaultdict(list)
>     for u, v in edges:
>         graph[u].append(v)
>         rev_graph[v].append(u)
> 
>     visited: set[int] = set()
>     order: list[int] = []          # finish order
> 
>     def dfs1(u: int) -> None:
>         visited.add(u)
>         for v in graph[u]:
>             if v not in visited:
>                 dfs1(v)
>         order.append(u)            # post-order
> 
>     for node in range(n):
>         if node not in visited:
>             dfs1(node)
> 
>     visited.clear()
>     sccs: list[list[int]] = []
> 
>     def dfs2(u: int, component: list[int]) -> None:
>         visited.add(u)
>         component.append(u)
>         for v in rev_graph[u]:
>             if v not in visited:
>                 dfs2(v, component)
> 
>     while order:
>         node = order.pop()
>         if node not in visited:
>             comp: list[int] = []
>             dfs2(node, comp)
>             sccs.append(comp)
> 
>     return sccs
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> Tarjan's SCC — single-pass DFS using a stack and low-link values; same O(V + E). Kosaraju's is simpler to reason about; Tarjan's uses less memory (one pass).

---

### Find Eventual Safe States (Reverse Graph / Kahn's)

> [!example] Problem
> Directed graph. A node is "safe" if every path from it leads to a terminal (no cycle). Return all safe nodes sorted.

> [!info] Approach
> - **WHY:** Unsafe nodes are those on or leading to cycles. In the reversed graph, terminal nodes (out-degree 0 in original) have in-degree 0. Topological sort on the reversed graph pulls in nodes that only lead to "safe" destinations.
> - **WHAT:** Reverse all edges. Kahn's BFS — nodes with out-degree 0 in original become sources.
> - **HOW:** `outdegree[u]` = original out-degree. Initialize queue with `outdegree[u] == 0`. When a node is processed safe, decrement predecessors' outdegree; add them if 0.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def eventualSafeNodes(graph: list[list[int]]) -> list[int]:
>     n = len(graph)
>     reverse: dict[int, list[int]] = defaultdict(list)
>     outdegree = [0] * n
> 
>     for u, neighbors in enumerate(graph):
>         for v in neighbors:
>             reverse[v].append(u)
>             outdegree[u] += 1
> 
>     q = deque(i for i in range(n) if outdegree[i] == 0)
>     safe: set[int] = set()
> 
>     while q:
>         node = q.popleft()
>         safe.add(node)
>         for nb in reverse[node]:
>             outdegree[nb] -= 1
>             if outdegree[nb] == 0:
>                 q.append(nb)
> 
>     return sorted(safe)
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> DFS with 3-color marking — node is safe iff all successors are safe. Memoize per node. Same O(V + E) but Kahn's is cleaner.

---

## Cycle Detection in Directed Graph

### Detect Cycle in Directed Graph (DFS 3-Color)

> [!example] Problem
> Given a directed graph, determine whether it contains a cycle.

> [!info] Approach
> - **WHY:** Kahn's BFS detects cycles implicitly via count, but DFS 3-color is the canonical O(V+E) approach that also identifies the cycle. In a directed graph, a cycle exists iff a DFS discovers a back edge — an edge to an ancestor currently on the DFS stack.
> - **WHAT:** 3-color DFS: WHITE (unvisited), GRAY (in current DFS path), BLACK (fully processed). A gray→gray edge is a back edge = cycle.
> - **HOW:** For each unvisited node, run DFS. Mark GRAY on entry, BLACK on exit. If we ever encounter a GRAY neighbor, we've found a cycle.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def hasCycle(n: int, edges: list[list[int]]) -> bool:
>     WHITE, GRAY, BLACK = 0, 1, 2
>     graph: dict[int, list[int]] = defaultdict(list)
>     for u, v in edges:
>         graph[u].append(v)
>     color = [WHITE] * n
> 
>     def dfs(u: int) -> bool:
>         color[u] = GRAY
>         for v in graph[u]:
>             if color[v] == GRAY:
>                 return True          # back edge → cycle
>             if color[v] == WHITE and dfs(v):
>                 return True
>         color[u] = BLACK
>         return False
> 
>     return any(dfs(node) for node in range(n) if color[node] == WHITE)
> ```

> [!success] Complexity
> Time O(V + E), Space O(V) for recursion stack.

> [!tip] Alternatives
> Kahn's BFS — cycle exists iff processed count < V. Iterative DFS with explicit stack — avoids Python recursion limit for large graphs. For undirected graphs: cycle exists iff DFS finds a visited non-parent neighbor.

---

## Eulerian Path

### Reconstruct Itinerary (Hierholzer's)

> [!example] Problem
> List of airline tickets `[from, to]`. Reconstruct itinerary starting from `"JFK"`, using all tickets exactly once, in lexicographic order.

> [!info] Approach
> - **WHY:** "Use every edge exactly once" = Eulerian path in a directed graph. Hierholzer's finds it in O(E).
> - **WHAT:** Post-order DFS — add a node to result only after all its outgoing edges are exhausted.
> - **HOW:** Sort each adjacency list in reverse order so `.pop()` gives the lexicographically smallest destination. DFS; when stuck (no outgoing edges), append to `result`. Reverse `result` at the end.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def findItinerary(tickets: list[list[str]]) -> list[str]:
>     graph: dict[str, list[str]] = defaultdict(list)
>     for src, dst in tickets:
>         graph[src].append(dst)
>     for src in graph:
>         graph[src].sort(reverse=True)   # pop() = smallest lex
> 
>     result: list[str] = []
> 
>     def dfs(node: str) -> None:
>         while graph[node]:
>             dfs(graph[node].pop())
>         result.append(node)             # post-order: dead-end first
> 
>     dfs("JFK")
>     return result[::-1]
> ```

> [!success] Complexity
> Time O(E log E) for sorting, Space O(E).

> [!tip] Alternatives
> Iterative with explicit stack — avoids Python recursion limit on large inputs. Backtracking with validity check — O(E!) worst case, impractical.

---

## 0-1 BFS

### Minimum Cost to Make at Least One Valid Path in a Grid

> [!example] Problem
> Grid where each cell `grid[i][j]` points to a neighbor (1=right,2=left,3=down,4=up). Cost 1 to change a direction. Find min cost to reach `(m-1,n-1)` from `(0,0)`.

> [!info] Approach
> - **WHY:** Moving in the cell's indicated direction costs 0 (already points there); any other direction costs 1. Edge weights are 0 or 1 → 0-1 BFS with a deque is O(V+E), faster than Dijkstra's O(E log V).
> - **WHAT:** 0-1 BFS: cost-0 edges go to front of deque, cost-1 edges go to back.
> - **HOW:** Each cell has one free neighbor (the direction it points). All other 3 neighbors cost 1. Standard Dijkstra also works but 0-1 BFS is asymptotically better.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def minCost(grid: list[list[int]]) -> int:
>     m, n = len(grid), len(grid[0])
>     dirs = [(0,1),(0,-1),(1,0),(-1,0)]  # 1=right,2=left,3=down,4=up
>     dist = [[float('inf')] * n for _ in range(m)]
>     dist[0][0] = 0
>     dq: deque[tuple[int,int,int]] = deque([(0, 0, 0)])
> 
>     while dq:
>         cost, r, c = dq.popleft()
>         if cost > dist[r][c]:
>             continue
>         for d, (dr, dc) in enumerate(dirs):
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < m and 0 <= nc < n:
>                 edge_cost = 0 if grid[r][c] == d + 1 else 1
>                 new_cost = cost + edge_cost
>                 if new_cost < dist[nr][nc]:
>                     dist[nr][nc] = new_cost
>                     if edge_cost == 0:
>                         dq.appendleft((new_cost, nr, nc))
>                     else:
>                         dq.append((new_cost, nr, nc))
> 
>     return dist[m-1][n-1]
> ```

> [!success] Complexity
> Time O(M·N), Space O(M·N).

> [!tip] Alternatives
> Dijkstra with min-heap — O(M·N·log(M·N)). Same correctness, slightly worse complexity.

---

### Open the Lock (Unweighted BFS Variant)

> [!example] Problem
> 4-digit lock `"0000"` to `"9999"`. Deadends are forbidden states. Find minimum turns to reach `target`.

> [!info] Approach
> - **WHY:** Each combination is a node; 8 neighbors (each of 4 digits ±1 mod 10). Unweighted BFS finds minimum turns.
> - **WHAT:** BFS on the implicit graph of 10,000 states.
> - **HOW:** Encode combinations as strings. Skip deadends. Mark visited by adding to a set. Start with `"0000"` — if it's a deadend, return -1 immediately.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def openLock(deadends: list[str], target: str) -> int:
>     dead = set(deadends)
>     if "0000" in dead:
>         return -1
>     if target == "0000":
>         return 0
> 
>     visited = {"0000"}
>     q: deque[tuple[str, int]] = deque([("0000", 0)])
> 
>     while q:
>         state, turns = q.popleft()
>         for i in range(4):
>             d = int(state[i])
>             for delta in (-1, 1):
>                 new_d = (d + delta) % 10
>                 new_state = state[:i] + str(new_d) + state[i+1:]
>                 if new_state == target:
>                     return turns + 1
>                 if new_state not in visited and new_state not in dead:
>                     visited.add(new_state)
>                     q.append((new_state, turns + 1))
> 
>     return -1
> ```

> [!success] Complexity
> Time O(10^4 · 4) = O(1) effectively bounded, Space O(10^4).

> [!tip] Alternatives
> Bidirectional BFS — expand from both `"0000"` and `target`; reduces branching factor from O(b^d) to O(b^(d/2)).

---

## Multi-source BFS / Special BFS

### Word Ladder (BFS on Implicit Graph)

> [!example] Problem
> Transform `beginWord` to `endWord` one letter at a time; each intermediate word must be in `wordList`. Return shortest transformation sequence length.

> [!info] Approach
> - **WHY:** Nodes = words, edges = one-letter-apart pairs. Unweighted BFS gives shortest path. The graph is implicit — never enumerate all pairs (O(N²·L)) — instead generate neighbors by substitution.
> - **WHAT:** BFS where each level = one transformation. For each word, try replacing each position with `a-z` and check against the word set.
> - **HOW:** Remove visited words from `word_set` immediately (not just a visited set) to prevent revisits efficiently.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
>     word_set = set(wordList)
>     if endWord not in word_set:
>         return 0
> 
>     q: deque[tuple[str, int]] = deque([(beginWord, 1)])
>     visited = {beginWord}
> 
>     while q:
>         word, length = q.popleft()
>         for i in range(len(word)):
>             for c in 'abcdefghijklmnopqrstuvwxyz':
>                 new_word = word[:i] + c + word[i+1:]
>                 if new_word == endWord:
>                     return length + 1
>                 if new_word in word_set and new_word not in visited:
>                     visited.add(new_word)
>                     q.append((new_word, length + 1))
> 
>     return 0
> ```

> [!success] Complexity
> Time O(M² · N) where M = word length, N = wordList size. Space O(M · N).

> [!tip] Alternatives
> Bidirectional BFS — expand from both ends; reduces to O(M² · √N) in practice. Preprocessing: bucket words by `*at` pattern (replace each char with `*`) reduces neighbor generation to O(M·N).

---

### Word Ladder II (All Shortest Transformation Sequences)

> [!example] Problem
> Same as Word Ladder, but return **all** shortest transformation sequences from `beginWord` to `endWord`.

> [!info] Approach
> - **WHY:** Finding all shortest paths requires BFS to establish the level structure (shortest distance to each node), then backtracking to reconstruct paths — DFS alone is exponential without the level constraint.
> - **WHAT:** Two-phase: BFS to build a DAG of "parent → children" edges that lie on shortest paths; then DFS/backtracking on that DAG to enumerate all paths.
> - **HOW:** BFS level-by-level. For each word, generate all 1-letter variants in the word set. Record `parents[new_word].add(word)`. Remove words from the set only after the full level is processed (so multiple parents at the same level can be recorded). Then DFS from `endWord` back to `beginWord` using the `parents` map.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def findLadders(beginWord: str, endWord: str, wordList: list[str]) -> list[list[str]]:
>     word_set = set(wordList)
>     if endWord not in word_set:
>         return []
> 
>     parents: dict[str, set[str]] = defaultdict(set)
>     current_level = {beginWord}
>     found = False
> 
>     while current_level and not found:
>         word_set -= current_level      # remove current level to prevent back-edges
>         next_level: set[str] = set()
>         for word in current_level:
>             for i in range(len(word)):
>                 for c in 'abcdefghijklmnopqrstuvwxyz':
>                     new_word = word[:i] + c + word[i+1:]
>                     if new_word in word_set:
>                         next_level.add(new_word)
>                         parents[new_word].add(word)
>                         if new_word == endWord:
>                             found = True
>         current_level = next_level
> 
>     if not found:
>         return []
> 
>     # Backtrack from endWord to beginWord
>     result: list[list[str]] = []
> 
>     def backtrack(word: str, path: list[str]) -> None:
>         if word == beginWord:
>             result.append(path[::-1])
>             return
>         for parent in parents[word]:
>             path.append(parent)
>             backtrack(parent, path)
>             path.pop()
> 
>     backtrack(endWord, [endWord])
>     return result
> ```

> [!success] Complexity
> Time O(M² · N + P) where M = word length, N = wordList size, P = total characters in all output paths. Space O(M · N).

> [!tip] Alternatives
> BFS + DFS without the parent-map — enumerate during DFS and prune by depth; same complexity but harder to implement correctly. Bidirectional BFS reduces the search space but makes parent tracking trickier.

---

### Shortest Path in Binary Matrix

> [!example] Problem
> N×N binary matrix. Find shortest 8-directional path of `0`-cells from `(0,0)` to `(N-1,N-1)`. Return length or `-1`.

> [!info] Approach
> - **WHY:** Unweighted grid shortest path = BFS. 8 directions. Mark visited in-place to save memory.
> - **WHAT:** BFS from `(0,0)`. First time we reach `(N-1,N-1)` is the shortest path.
> - **HOW:** Check both endpoints are `0` before starting. Distance = BFS level when target is first reached.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def shortestPathBinaryMatrix(grid: list[list[int]]) -> int:
>     n = len(grid)
>     if grid[0][0] == 1 or grid[n-1][n-1] == 1:
>         return -1
>     if n == 1:
>         return 1
> 
>     q: deque[tuple[int,int,int]] = deque([(0, 0, 1)])
>     grid[0][0] = 1          # mark visited in-place
>     dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
> 
>     while q:
>         r, c, dist = q.popleft()
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
>                 if nr == n - 1 and nc == n - 1:
>                     return dist + 1
>                 grid[nr][nc] = 1
>                 q.append((nr, nc, dist + 1))
> 
>     return -1
> ```

> [!success] Complexity
> Time O(N²), Space O(N²).

> [!tip] Alternatives
> A* with Chebyshev distance heuristic — same worst case, faster in practice on sparse grids. DFS doesn't guarantee shortest path.

---

## Bipartite

### Is Graph Bipartite?

> [!example] Problem
> Undirected graph. Can nodes be 2-colored such that no two adjacent nodes share the same color?

> [!info] Approach
> - **WHY:** A graph is bipartite iff it contains no odd-length cycle. 2-coloring detects this: if a neighbor already has the same color → odd cycle found.
> - **WHAT:** BFS/DFS coloring. Assign color `0` to start, alternate to neighbors.
> - **HOW:** Must handle disconnected components — start BFS from every unvisited node.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def isBipartite(graph: list[list[int]]) -> bool:
>     n = len(graph)
>     color = [-1] * n
> 
>     for start in range(n):
>         if color[start] != -1:
>             continue
>         q: deque[int] = deque([start])
>         color[start] = 0
> 
>         while q:
>             node = q.popleft()
>             for nb in graph[node]:
>                 if color[nb] == -1:
>                     color[nb] = 1 - color[node]
>                     q.append(nb)
>                 elif color[nb] == color[node]:
>                     return False            # same color conflict = odd cycle
> 
>     return True
> ```

> [!success] Complexity
> Time O(V + E), Space O(V).

> [!tip] Alternatives
> DFS — same logic recursively. Union-Find: union all neighbors of each node together and verify node is not in the same set as its neighbors (need separate "other side" DSU).

---

### Possible Bipartition

> [!example] Problem
> `n` people, list of `dislikes` pairs. Can you split into two groups with no two people who dislike each other in the same group?

> [!info] Approach
> - **WHY:** "Split into two groups with no conflicts" = 2-color the conflict graph = bipartite check.
> - **WHAT:** Build undirected graph from dislikes pairs. Run bipartite check.
> - **HOW:** Identical to `isBipartite` — just build the graph first from `dislikes`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def possibleBipartition(n: int, dislikes: list[list[int]]) -> bool:
>     graph: dict[int, list[int]] = defaultdict(list)
>     for u, v in dislikes:
>         graph[u].append(v)
>         graph[v].append(u)
> 
>     color = [-1] * (n + 1)
> 
>     for start in range(1, n + 1):
>         if color[start] != -1:
>             continue
>         q: deque[int] = deque([start])
>         color[start] = 0
> 
>         while q:
>             node = q.popleft()
>             for nb in graph[node]:
>                 if color[nb] == -1:
>                     color[nb] = 1 - color[node]
>                     q.append(nb)
>                 elif color[nb] == color[node]:
>                     return False
> 
>     return True
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> DSU approach — for each node, union all its neighbors together and verify the node is never in the same component as itself (requires "enemy" tracking). BFS/DFS is simpler here.

---

## Minimum Spanning Tree — Prim's Algorithm

### Min Cost to Connect All Points (LC 1584)

> [!example] Problem
> Given `points` on a 2D plane, find the minimum cost to connect all points where cost = Manhattan distance `|x1-x2| + |y1-y2|`. All points must be connected.

> [!info] Approach
> - **WHY:** MST problem on a dense graph (n² edges). Prim's is natural here — always extend the current MST by the cheapest reachable new node.
> - **WHAT:** Greedy — maintain a min-heap of `(cost, node)` for nodes not yet in the MST. Always pick the cheapest edge into the unvisited set.
> - **HOW:** Start from node 0. Min-heap stores `(cost, node)`. Pop cheapest; if already visited, skip. Add its cost to total. Push all unvisited neighbors with Manhattan distance as cost. Repeat until all n nodes visited.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def minCostConnectPoints(points: list[list[int]]) -> int:
>     n = len(points)
>     visited = [False] * n
>     heap = [(0, 0)]   # (cost, node index)
>     total = 0
>     count = 0
> 
>     while count < n:
>         cost, u = heapq.heappop(heap)
>         if visited[u]:
>             continue
>         visited[u] = True
>         total += cost
>         count += 1
>         for v in range(n):
>             if not visited[v]:
>                 dist = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
>                 heapq.heappush(heap, (dist, v))
> 
>     return total
> ```

> [!success] Complexity
> Time O(n² log n), Space O(n²).

> [!tip] Alternatives
> Kruskal's O(n² log n) — generate all n² edges, sort, Union-Find; same asymptotic. Prim's with array (no heap) is O(n²) — optimal for dense graphs; track `min_cost[v]` as the minimum edge into v from current MST.

---

## Graph Coloring

### M-Coloring Problem (Backtracking)

> [!example] Problem
> Given an undirected graph and `m` colors, determine whether the graph can be colored using at most `m` colors such that no two adjacent nodes share the same color.

> [!info] Approach
> - **WHY:** Graph coloring is NP-complete in general; backtracking with pruning is the standard approach for exact solutions on small graphs.
> - **WHAT:** Assign colors 1..m to nodes one at a time; backtrack if any color assignment conflicts with an already-colored neighbor.
> - **HOW:** Try each color for the current node. Before assigning, check all neighbors — if a neighbor already has that color, skip. If all m colors fail → backtrack. If all nodes assigned → return True.

> [!note]- Python Solution
> ```python
> def graphColoring(graph: list[list[int]], m: int) -> bool:
>     """
>     graph: adjacency list (0-indexed)
>     m: number of available colors
>     Returns True if m-coloring is possible.
>     """
>     n = len(graph)
>     color = [0] * n   # 0 = uncolored
> 
>     def is_safe(node: int, c: int) -> bool:
>         return all(color[nb] != c for nb in graph[node])
> 
>     def backtrack(node: int) -> bool:
>         if node == n:
>             return True
>         for c in range(1, m + 1):
>             if is_safe(node, c):
>                 color[node] = c
>                 if backtrack(node + 1):
>                     return True
>                 color[node] = 0          # undo
>         return False
> 
>     return backtrack(0)
> 
> 
> # Variant: return one valid coloring or []
> def graphColoringAssignment(graph: list[list[int]], m: int) -> list[int]:
>     n = len(graph)
>     color = [0] * n
> 
>     def is_safe(node: int, c: int) -> bool:
>         return all(color[nb] != c for nb in graph[node])
> 
>     def backtrack(node: int) -> bool:
>         if node == n:
>             return True
>         for c in range(1, m + 1):
>             if is_safe(node, c):
>                 color[node] = c
>                 if backtrack(node + 1):
>                     return True
>                 color[node] = 0
>         return False
> 
>     return color if backtrack(0) else []
> ```

> [!success] Complexity
> Time O(m^V) worst case with pruning reducing practical performance significantly. Space O(V) for color array + O(V) recursion stack.

> [!tip] Alternatives
> Greedy coloring (not optimal — can use up to Δ+1 colors where Δ = max degree). DSatur heuristic — color nodes in order of saturation (most distinct neighbor colors); often near-optimal in practice. For bipartite check (2-coloring): use BFS O(V+E).

---

## See Also

[[graph]] | [[union-find]] | [[dynamic-programming]] | [[binary-search]]
### Bellman-Ford (Negative Weights)

> [!example] Problem
> Given a directed weighted graph that may contain negative edges, find shortest paths from a source and detect negative cycles reachable from it.

> [!info] Approach
> - **WHY:** Dijkstra does not work with negative edges. Bellman-Ford relaxes every edge `V-1` times, which is enough for shortest paths in a graph with no negative cycles.
> - **WHAT:** Initialize distances to infinity except the source. Repeatedly relax all edges. One more pass detects a negative cycle.
> - **HOW:** If `dist[u] + w < dist[v]`, update `dist[v]`. After `V-1` passes, if any edge can still relax, a negative cycle exists.

> [!note]- Python Solution
> ```python
> def bellman_ford(n: int, edges: list[tuple[int, int, int]], source: int) -> tuple[list[float], bool]:
>     dist = [float("inf")] * n
>     dist[source] = 0
>     for _ in range(n - 1):
>         updated = False
>         for u, v, w in edges:
>             if dist[u] != float("inf") and dist[u] + w < dist[v]:
>                 dist[v] = dist[u] + w
>                 updated = True
>         if not updated:
>             break
>     has_negative_cycle = any(
>         dist[u] != float("inf") and dist[u] + w < dist[v] for u, v, w in edges
>     )
>     return dist, has_negative_cycle
> ```

> [!success] Complexity
> O(VE) time, O(V) space.

> [!tip] Alternatives
> For graphs with only non-negative edges, Dijkstra is faster; for DAGs, topological relaxation is linear.
