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
> You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target.
> We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.
> 
> **Example 1:**
> ```
> Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: times = [[1,2,1]], n = 2, k = 1
> Output: 1
> ```
> 
> **Example 3:**
> ```
> Input: times = [[1,2,1]], n = 2, k = 2
> Output: -1
> ```
> 
> **Constraints:**
> - 1 <= k <= n <= 100
> - 1 <= times.length <= 6000
> - times[i].length == 3
> - 1 <= ui, vi <= n
> - ui != vi
> - 0 <= wi <= 100
> - All the pairs (ui, vi) are unique. (i.e., no multiple edges.)

> [!info] Approach
> Shortest paths from a single source with non-negative weights. Each node's final distance must be optimal before we use it to relax neighbors. Greedy SSSP — always expand the globally cheapest unvisited node. Min-heap of `(dist, node)`. Lazy deletion guard `if d > dist[u]: continue` discards stale heap entries. Answer = `max(dist.values())`; if any node has `inf` distance, return `-1`.


> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> 
> def network_delay_time(times, n, k):
>     graph = defaultdict(list)
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
> You are given an n x n integer matrix grid where each value grid[i][j] represents the elevation at that point (i, j).
> It starts raining, and water gradually rises over time. At time t, the water level is t, meaning any cell with elevation less than equal to t is submerged or reachable.
> You can swim from a square to another 4-directionally adjacent square if and only if the elevation of both squares individually are at most t. You can swim infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.
> Return the minimum time until you can reach the bottom right square (n - 1, n - 1) if you start at the top left square (0, 0).
> 
> **Example 1:**
> ```
> Input: grid = [[0,2],[1,3]]
> Output: 3
> Explanation:
> At time 0, you are in grid location (0, 0).
> You cannot go anywhere else because 4-directionally adjacent neighbors have a higher elevation than t = 0.
> You cannot reach point (1, 1) until time 3.
> When the depth of water is 3, we can swim anywhere inside the grid.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
> Output: 16
> Explanation: The final route is shown.
> We need to wait until time 16 so that (0, 0) and (4, 4) are connected.
> ```
> 
> **Constraints:**
> - n == grid.length
> - n == grid[i].length
> - 1 <= n <= 50
> - 0 <= grid[i][j] < n2
> - Each value grid[i][j] is unique.

> [!info] Approach
> We want to minimize the maximum elevation encountered along a path — a min-bottleneck path problem. Dijkstra where `dist[cell]` = minimum possible max-elevation to reach that cell. Heap entry `(max_elevation_on_path, r, c)`. At each step, `cost(u→v) = max(current_max, grid[v])`. The first time we pop `(N-1,N-1)` is the answer.


> [!note]- Python Solution
> ```python
> import heapq
> 
> def swim_in_water(grid):
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
> Maximize a product along a path — same structure as shortest path but with max-product instead of min-sum. Dijkstra variant with max-heap; `dist[v]` = max probability to reach `v`. Negate heap values for max-heap (or use `-prob`). Relaxation: `prob[u] * w > prob[v]` → update. All probabilities in [0,1] — no negative-weight issues.


> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> 
> def max_probability(n: int, edges: list[list[int]], succProb: list[float],
>                    start: int, end: int) -> float:
>     graph = defaultdict(list)
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
> Division is transitive — `a/c = (a/b) * (b/c)`. Model as a weighted directed graph: edge `a→b` with weight `2.0` and `b→a` with weight `0.5`. Build weighted graph. For each query `(src, dst)`, run BFS/DFS from `src` to `dst` multiplying edge weights. If `dst` is unreachable, return `-1.0`. Build adjacency list `{node: [(neighbor, weight)]}`. BFS with `(node, product)` in queue. Track visited. Return product when `dst` found.


> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def calc_equation(equations: list[list[str]], values: list[float],
>                  queries: list[list[str]]) -> list[float]:
>     graph = defaultdict(list)
>     for (u, v), w in zip(equations, values):
>         graph[u].append((v, w))
>         graph[v].append((u, 1.0 / w))
> 
>     def bfs(src, dst):
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
> Bellman-Ford (next section) is the usual answer. Dijkstra also works if state is `(cost, node, stops_used)` — you can't ignore stop count. Push `(cost, node, stops)` on a heap, skip when stops exceed K, and mark visited per `(node, stops)` pair.

See full Bellman-Ford solution in the next section.

---

## Bellman-Ford

### Cheapest Flights Within K Stops

> [!example] Problem
> There are n cities connected by some number of flights. You are given an array flights where flights[i] = [fromi, toi, pricei] indicates that there is a flight from city fromi to city toi with cost pricei.
> You are also given three integers src, dst, and k, return the cheapest price from src to dst with at most k stops. If there is no such route, return -1.
> 
> **Example 1:**
> ```
> Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1
> Output: 700
> Explanation:
> The graph is shown above.
> The optimal path with at most 1 stop from city 0 to 3 is marked in red and has cost 100 + 600 = 700.
> Note that the path through cities [0,1,2,3] is cheaper but is invalid because it uses 2 stops.
> ```
> 
> **Example 2:**
> ```
> Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1
> Output: 200
> Explanation:
> The graph is shown above.
> The optimal path with at most 1 stop from city 0 to 2 is marked in red and has cost 100 + 100 = 200.
> ```
> 
> **Example 3:**
> ```
> Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0
> Output: 500
> Explanation:
> The graph is shown above.
> The optimal path with no stops from city 0 to 2 is marked in red and has cost 500.
> ```
> 
> **Constraints:**
> - 1 <= n <= 100
> - 0 <= flights.length <= (n * (n - 1) / 2)
> - flights[i].length == 3
> - 0 <= fromi, toi < n
> - fromi != toi
> - 1 <= pricei <= 10^4
> - There will not be any multiple flights between two cities.
> - 0 <= src, dst, k < n
> - src != dst

> [!info] Approach
> Standard Dijkstra doesn't track hop count. Bellman-Ford runs exactly `k+1` relaxation rounds — round `i` gives optimal cost using ≤ `i` edges. Bounded Bellman-Ford: `k+1` rounds, each relaxing all edges. Critical — use a copy of `prices` each round (`temp = prices[:]`). Without the copy, a single round might chain multiple hops, violating the hop bound.


> [!note]- Python Solution
> ```python
> def find_cheapest_price(n: int, flights: list[list[int]],
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
> There are n cities numbered from 0 to n-1. Given the array edges where edges[i] = [fromi, toi, weighti] represents a bidirectional and weighted edge between cities fromi and toi, and given the integer distanceThreshold.
> Return the city with the smallest number of cities that are reachable through some path and whose distance is at most distanceThreshold, If there are multiple such cities, return the city with the greatest number.
> Notice that the distance of a path connecting cities i and j is equal to the sum of the edges' weights along that path.
> 
> **Example 1:**
> ```
> Input: n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4
> Output: 3
> Explanation: The figure above describes the graph. 
> The neighboring cities at a distanceThreshold = 4 for each city are:
> City 0 -> [City 1, City 2] 
> City 1 -> [City 0, City 2, City 3] 
> City 2 -> [City 0, City 1, City 3] 
> City 3 -> [City 1, City 2] 
> Cities 0 and 3 have 2 neighboring cities at a distanceThreshold = 4, but we have to return city 3 since it has the greatest number.
> ```
> 
> **Example 2:**
> ```
> Input: n = 5, edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]], distanceThreshold = 2
> Output: 0
> Explanation: The figure above describes the graph. 
> The neighboring cities at a distanceThreshold = 2 for each city are:
> City 0 -> [City 1] 
> City 1 -> [City 0, City 4] 
> City 2 -> [City 3, City 4] 
> City 3 -> [City 2, City 4]
> City 4 -> [City 1, City 2, City 3] 
> The city 0 has 1 neighboring city at a distanceThreshold = 2.
> ```
> 
> **Constraints:**
> - 2 <= n <= 100
> - 1 <= edges.length <= n * (n - 1) / 2
> - edges[i].length == 3
> - 0 <= fromi < toi < n
> - 1 <= weighti, distanceThreshold <= 10^4
> - All pairs (fromi, toi) are distinct.

> [!info] Approach
> Need all-pairs shortest paths. Running Dijkstra from each city is O(V·E·log V); Floyd-Warshall is O(V³) which is cleaner for small V (≤ 100 here). Floyd-Warshall DP: `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])` for all intermediates `k`. Initialize diagonal to 0, direct edges to weight, rest to inf. `k` must be the outermost loop. After running, count neighbors within threshold for each city.


> [!note]- Python Solution
> ```python
> def find_the_city(n, edges, distanceThreshold):
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
> There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.
> Return true if you can finish all courses. Otherwise, return false.
> 
> **Example 1:**
> ```
> Input: numCourses = 2, prerequisites = [[1,0]]
> Output: true
> Explanation: There are a total of 2 courses to take. 
> To take course 1 you should have finished course 0. So it is possible.
> ```
> 
> **Example 2:**
> ```
> Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
> Output: false
> Explanation: There are a total of 2 courses to take. 
> To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.
> ```
> 
> **Constraints:**
> - 1 <= numCourses <= 2000
> - 0 <= prerequisites.length <= 5000
> - prerequisites[i].length == 2
> - 0 <= ai, bi < numCourses
> - All the pairs prerequisites[i] are unique.

> [!info] Approach
> A valid schedule exists iff the dependency graph is a DAG. Cycle = impossible. Kahn's BFS topological sort — process zero-in-degree nodes first; if all nodes processed → DAG. Build adjacency list and in-degree array. BFS from zero-in-degree nodes; decrement neighbors. If `processed == numCourses` → no cycle.


> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def can_finish(numCourses, prerequisites):
>     graph = defaultdict(list)
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
> There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.
> Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.
> 
> **Example 1:**
> ```
> Input: numCourses = 2, prerequisites = [[1,0]]
> Output: [0,1]
> Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1].
> ```
> 
> **Example 2:**
> ```
> Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
> Output: [0,2,1,3]
> Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
> So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].
> ```
> 
> **Example 3:**
> ```
> Input: numCourses = 1, prerequisites = []
> Output: [0]
> ```
> 
> **Constraints:**
> - 1 <= numCourses <= 2000
> - 0 <= prerequisites.length <= numCourses * (numCourses - 1)
> - prerequisites[i].length == 2
> - 0 <= ai, bi < numCourses
> - ai != bi
> - All the pairs [ai, bi] are distinct.

> [!info] Approach
> Need an actual topological ordering, not just feasibility. Kahn's BFS — nodes dequeued in topological order. Collect dequeued nodes into `order`. If `len(order) == numCourses` → valid. Otherwise cycle exists.


> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def find_order(numCourses, prerequisites):
>     graph = defaultdict(list)
>     indegree = [0] * numCourses
> 
>     for a, b in prerequisites:
>         graph[b].append(a)
>         indegree[a] += 1
> 
>     q = deque(i for i in range(numCourses) if indegree[i] == 0)
>     order = []
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
> There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you.
> 
> You are given a list of strings `words` from the alien language's dictionary. Now it is claimed that the strings in `words` are **sorted lexicographically** by the rules of this new language.
> 
> If this claim is incorrect, and the given arrangement of string in `words` cannot correspond to any order of letters, return `"".`
> 
> Otherwise, return *a string of the unique letters in the new alien language sorted in **lexicographically increasing order** by the new language's rules**. *If there are multiple solutions, return* **any of them***.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** words = ["wrt","wrf","er","ett","rftt"]
> **Output:** "wertf"
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** words = ["z","x"]
> **Output:** "zx"
> 
> ```
> 
> Example 3:
> 
> ```
> 
> **Input:** words = ["z","x","z"]
> **Output:** ""
> **Explanation:** The order is invalid, so return `""`.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= words.length <= 100`
> 	
> - `1 <= words[i].length <= 100`
> 	
> - `words[i]` consists of only lowercase English letters.

> [!info] Approach
> Adjacent sorted words reveal one ordering constraint each (first differing character). Build a DAG of character constraints, topological sort. Extract edges from adjacent word pairs; Kahn's on the character graph. For each pair `(words[i], words[i+1])`, find first differing character — adds directed edge. Invalid: if word A is a proper prefix of word B but A appears after B. Cycle in graph → `""`.


> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def alien_order(words):
>     graph = defaultdict(list)
>     indegree = {c: 0 for word in words for c in word}
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
>     result = []
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
> You are given an integer array `nums` of length `n` where `nums` is a permutation of the integers in the range `[1, n]`. You are also given a 2D integer array `sequences` where `sequences[i]` is a subsequence of `nums`.
> 
> Check if `nums` is the shortest possible and the only **supersequence**. The shortest **supersequence** is a sequence **with the shortest length** and has all `sequences[i]` as subsequences. There could be multiple valid **supersequences** for the given array `sequences`.
> 
> 	
> - For example, for `sequences = [[1,2],[1,3]]`, there are two shortest **supersequences**, `[1,2,3]` and `[1,3,2]`.
> 	
> - While for `sequences = [[1,2],[1,3],[1,2,3]]`, the only shortest **supersequence** possible is `[1,2,3]`. `[1,2,3,4]` is a possible supersequence but not the shortest.
> 
> Return `true`* if *`nums`* is the only shortest **supersequence** for *`sequences`*, or *`false`* otherwise*.
> 
> A **subsequence** is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** nums = [1,2,3], sequences = [[1,2],[1,3]]
> **Output:** false
> **Explanation:** There are two possible supersequences: [1,2,3] and [1,3,2].
> The sequence [1,2] is a subsequence of both: [**1**,**2**,3] and [**1**,3,**2**].
> The sequence [1,3] is a subsequence of both: [**1**,2,**3**] and [**1**,**3**,2].
> Since nums is not the only shortest supersequence, we return false.
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** nums = [1,2,3], sequences = [[1,2]]
> **Output:** false
> **Explanation:** The shortest possible supersequence is [1,2].
> The sequence [1,2] is a subsequence of it: [**1**,**2**].
> Since nums is not the shortest supersequence, we return false.
> 
> ```
> 
> Example 3:
> 
> ```
> 
> **Input:** nums = [1,2,3], sequences = [[1,2],[1,3],[2,3]]
> **Output:** true
> **Explanation:** The shortest possible supersequence is [1,2,3].
> The sequence [1,2] is a subsequence of it: [**1**,**2**,3].
> The sequence [1,3] is a subsequence of it: [**1**,2,**3**].
> The sequence [2,3] is a subsequence of it: [1,**2**,**3**].
> Since nums is the only shortest supersequence, we return true.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `n == nums.length`
> 	
> - `1 <= n <= 10^4`
> 	
> - `nums` is a permutation of all the integers in the range `[1, n]`.
> 	
> - `1 <= sequences.length <= 10^4`
> 	
> - `1 <= sequences[i].length <= 10^4`
> 	
> - `1 <= sum(sequences[i].length) <= 10^5`
> 	
> - `1 <= sequences[i][j] <= n`
> 	
> - All the arrays of `sequences` are **unique**.
> 	
> - `sequences[i]` is a subsequence of `nums`.

> [!info] Approach
> `nums` is the unique shortest supersequence iff the topological order derived from all constraints is unique — meaning at every step, exactly one node has in-degree 0. Build dependency graph from consecutive pairs in each sequence. Run Kahn's; check uniqueness at every BFS step. If at any point the queue has more than one element → multiple valid orderings → not unique. Also verify the final order equals `nums`.


> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def sequence_reconstruction(nums, sequences):
>     n = len(nums)
>     graph = defaultdict(set)
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
>     order = []
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
> You have information about n different recipes. You are given a string array recipes and a 2D string array ingredients. The ith recipe has the name recipes[i], and you can create it if you have all the needed ingredients from ingredients[i]. A recipe can also be an ingredient for other recipes, i.e., ingredients[i] may contain a string that is in recipes.
> You are also given a string array supplies containing all the ingredients that you initially have, and you have an infinite supply of all of them.
> Return a list of all the recipes that you can create. You may return the answer in any order.
> Note that two recipes may contain each other in their ingredients.
> 
> **Example 1:**
> ```
> Input: recipes = ["bread"], ingredients = [["yeast","flour"]], supplies = ["yeast","flour","corn"]
> Output: ["bread"]
> Explanation:
> We can create "bread" since we have the ingredients "yeast" and "flour".
> ```
> 
> **Example 2:**
> ```
> Input: recipes = ["bread","sandwich"], ingredients = [["yeast","flour"],["bread","meat"]], supplies = ["yeast","flour","meat"]
> Output: ["bread","sandwich"]
> Explanation:
> We can create "bread" since we have the ingredients "yeast" and "flour".
> We can create "sandwich" since we have the ingredient "meat" and can create the ingredient "bread".
> ```
> 
> **Example 3:**
> ```
> Input: recipes = ["bread","sandwich","burger"], ingredients = [["yeast","flour"],["bread","meat"],["sandwich","meat","bread"]], supplies = ["yeast","flour","meat"]
> Output: ["bread","sandwich","burger"]
> Explanation:
> We can create "bread" since we have the ingredients "yeast" and "flour".
> We can create "sandwich" since we have the ingredient "meat" and can create the ingredient "bread".
> We can create "burger" since we have the ingredient "meat" and can create the ingredients "bread" and "sandwich".
> ```
> 
> **Constraints:**
> - n == recipes.length == ingredients.length
> - 1 <= n <= 100
> - 1 <= ingredients[i].length, supplies.length <= 100
> - 1 <= recipes[i].length, ingredients[i][j].length, supplies[k].length <= 10
> - recipes[i], ingredients[i][j], and supplies[k] consist only of lowercase English letters.
> - All the values of recipes and supplies combined are unique.
> - Each ingredients[i] does not contain any duplicate values.

> [!info] Approach
> Recipe dependencies form a DAG. A recipe is achievable iff all its dependencies are achievable — topological order. Kahn's BFS — supplies have in-degree 0. Process in topological order; when a recipe's in-degree reaches 0, it can be made. Treat recipes and supplies as nodes. Edges: ingredient → recipe (ingredient must precede recipe). Initialize queue with all supply nodes.


> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def find_all_recipes(recipes: list[str], ingredients: list[list[str]],
>                    supplies: list[str]) -> list[str]:
>     graph = defaultdict(list)
>     indegree = defaultdict(int)
> 
>     recipe_set = set(recipes)
> 
>     for recipe, ing_list in zip(recipes, ingredients):
>         for ing in ing_list:
>             graph[ing].append(recipe)
>             indegree[recipe] += 1
> 
>     q = deque(supplies)
>     result = []
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
> There are n servers numbered from 0 to n - 1 connected by undirected server-to-server connections forming a network where connections[i] = [ai, bi] represents a connection between servers ai and bi. Any server can reach other servers directly or indirectly through the network.
> A critical connection is a connection that, if removed, will make some servers unable to reach some other server.
> Return all critical connections in the network in any order.
> 
> **Example 1:**
> ```
> Input: n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]
> Output: [[1,3]]
> Explanation: [[3,1]] is also accepted.
> ```
> 
> **Example 2:**
> ```
> Input: n = 2, connections = [[0,1]]
> Output: [[0,1]]
> ```
> 
> **Constraints:**
> - 2 <= n <= 10^5
> - n - 1 <= connections.length <= 10^5
> - 0 <= ai, bi <= n - 1
> - ai != bi
> - There are no repeated connections.

> [!info] Approach
> A bridge is an edge with no alternative path — its removal increases connected components. Tarjan's bridge-finding: DFS assigns `disc[]` (discovery time) and `low[]` (earliest disc reachable from subtree). Edge `(u,v)` is a bridge iff `low[v] > disc[u]`. DFS from any node. When backtracking from child `v` to parent `u`: `low[u] = min(low[u], low[v])`. For already-visited back edges (non-parent): `low[u] = min(low[u], disc[v])`. Bridge condition: `low[v] > disc[u]`.


> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def critical_connections(n, connections):
>     graph = defaultdict(list)
>     for u, v in connections:
>         graph[u].append(v)
>         graph[v].append(u)
> 
>     disc = [-1] * n
>     low = [-1] * n
>     timer = [0]
>     bridges = []
> 
>     def dfs(u, parent):
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
> SCC decomposition reveals the "condensation DAG" of a graph — each SCC collapses into one node. Essential for dependency analysis, 2-SAT, and reachability. Kosaraju's two-pass DFS: first pass on original graph records finish order; second pass on reversed graph processes in reverse finish order — each DFS tree in pass 2 is one SCC. Pass 1 — DFS original graph, push nodes to stack in finish order. Pass 2 — reverse all edges, pop from stack, DFS the reversed graph; each connected component found = one SCC.


> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def kosaraju_sccs(n, edges):
>     graph = defaultdict(list)
>     rev_graph = defaultdict(list)
>     for u, v in edges:
>         graph[u].append(v)
>         rev_graph[v].append(u)
> 
>     visited = set()
>     order = []          # finish order
> 
>     def dfs1(u):
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
>     sccs = []
> 
>     def dfs2(u, component):
>         visited.add(u)
>         component.append(u)
>         for v in rev_graph[u]:
>             if v not in visited:
>                 dfs2(v, component)
> 
>     while order:
>         node = order.pop()
>         if node not in visited:
>             comp = []
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
> There is a directed graph of n nodes with each node labeled from 0 to n - 1. The graph is represented by a 0-indexed 2D integer array graph where graph[i] is an integer array of nodes adjacent to node i, meaning there is an edge from node i to each node in graph[i].
> A node is a terminal node if there are no outgoing edges. A node is a safe node if every possible path starting from that node leads to a terminal node (or another safe node).
> Return an array containing all the safe nodes of the graph. The answer should be sorted in ascending order.
> 
> **Example 1:**
> ```
> Input: graph = [[1,2],[2,3],[5],[0],[5],[],[]]
> Output: [2,4,5,6]
> Explanation: The given graph is shown above.
> Nodes 5 and 6 are terminal nodes as there are no outgoing edges from either of them.
> Every path starting at nodes 2, 4, 5, and 6 all lead to either node 5 or 6.
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[1,2,3,4],[1,2],[3,4],[0,4],[]]
> Output: [4]
> Explanation:
> Only node 4 is a terminal node, and every path starting at node 4 leads to node 4.
> ```
> 
> **Constraints:**
> - n == graph.length
> - 1 <= n <= 10^4
> - 0 <= graph[i].length <= n
> - 0 <= graph[i][j] <= n - 1
> - graph[i] is sorted in a strictly increasing order.
> - The graph may contain self-loops.
> - The number of edges in the graph will be in the range [1, 4 * 10^4].

> [!info] Approach
> Unsafe nodes are those on or leading to cycles. In the reversed graph, terminal nodes (out-degree 0 in original) have in-degree 0. Topological sort on the reversed graph pulls in nodes that only lead to "safe" destinations. Reverse all edges. Kahn's BFS — nodes with out-degree 0 in original become sources. `outdegree[u]` = original out-degree. Initialize queue with `outdegree[u] == 0`. When a node is processed safe, decrement predecessors' outdegree; add them if 0.


> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def eventual_safe_nodes(graph):
>     n = len(graph)
>     reverse = defaultdict(list)
>     outdegree = [0] * n
> 
>     for u, neighbors in enumerate(graph):
>         for v in neighbors:
>             reverse[v].append(u)
>             outdegree[u] += 1
> 
>     q = deque(i for i in range(n) if outdegree[i] == 0)
>     safe = set()
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
> Kahn's BFS detects cycles implicitly via count, but DFS 3-color is the canonical O(V+E) approach that also identifies the cycle. In a directed graph, a cycle exists iff a DFS discovers a back edge — an edge to an ancestor currently on the DFS stack. 3-color DFS: WHITE (unvisited), GRAY (in current DFS path), BLACK (fully processed). A gray→gray edge is a back edge = cycle. For each unvisited node, run DFS. Mark GRAY on entry, BLACK on exit. If we ever encounter a GRAY neighbor, we've found a cycle.


> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def has_cycle(n, edges):
>     WHITE, GRAY, BLACK = 0, 1, 2
>     graph = defaultdict(list)
>     for u, v in edges:
>         graph[u].append(v)
>     color = [WHITE] * n
> 
>     def dfs(u):
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
> You are given a list of airline tickets where tickets[i] = [fromi, toi] represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it.
> All of the tickets belong to a man who departs from "JFK", thus, the itinerary must begin with "JFK". If there are multiple valid itineraries, you should return the itinerary that has the smallest lexical order when read as a single string.
> You may assume all tickets form at least one valid itinerary. You must use all the tickets once and only once.
> 
> **Example 1:**
> ```
> Input: tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
> Output: ["JFK","MUC","LHR","SFO","SJC"]
> ```
> 
> **Example 2:**
> ```
> Input: tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
> Output: ["JFK","ATL","JFK","SFO","ATL","SFO"]
> Explanation: Another possible reconstruction is ["JFK","SFO","ATL","JFK","ATL","SFO"] but it is larger in lexical order.
> ```
> 
> **Constraints:**
> - 1 <= tickets.length <= 300
> - tickets[i].length == 2
> - fromi.length == 3
> - toi.length == 3
> - fromi and toi consist of uppercase English letters.
> - fromi != toi

> [!info] Approach
> "Use every edge exactly once" = Eulerian path in a directed graph. Hierholzer's finds it in O(E). Post-order DFS — add a node to result only after all its outgoing edges are exhausted. Sort each adjacency list in reverse order so `.pop()` gives the lexicographically smallest destination. DFS; when stuck (no outgoing edges), append to `result`. Reverse `result` at the end.


> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def find_itinerary(tickets):
>     graph = defaultdict(list)
>     for src, dst in tickets:
>         graph[src].append(dst)
>     for src in graph:
>         graph[src].sort(reverse=True)   # pop() = smallest lex
> 
>     result = []
> 
>     def dfs(node):
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
> Moving in the cell's indicated direction costs 0 (already points there); any other direction costs 1. Edge weights are 0 or 1 → 0-1 BFS with a deque is O(V+E), faster than Dijkstra's O(E log V). 0-1 BFS: cost-0 edges go to front of deque, cost-1 edges go to back. Each cell has one free neighbor (the direction it points). All other 3 neighbors cost 1. Standard Dijkstra also works but 0-1 BFS is asymptotically better.


> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def min_cost(grid):
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
> You have a lock in front of you with 4 circular wheels. Each wheel has 10 slots: '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'. The wheels can rotate freely and wrap around: for example we can turn '9' to be '0', or '0' to be '9'. Each move consists of turning one wheel one slot.
> The lock initially starts at '0000', a string representing the state of the 4 wheels.
> You are given a list of deadends dead ends, meaning if the lock displays any of these codes, the wheels of the lock will stop turning and you will be unable to open it.
> Given a target representing the value of the wheels that will unlock the lock, return the minimum total number of turns required to open the lock, or -1 if it is impossible.
> 
> **Example 1:**
> ```
> Input: deadends = ["0201","0101","0102","1212","2002"], target = "0202"
> Output: 6
> Explanation: 
> A sequence of valid moves would be "0000" -> "1000" -> "1100" -> "1200" -> "1201" -> "1202" -> "0202".
> Note that a sequence like "0000" -> "0001" -> "0002" -> "0102" -> "0202" would be invalid,
> because the wheels of the lock become stuck after the display becomes the dead end "0102".
> ```
> 
> **Example 2:**
> ```
> Input: deadends = ["8888"], target = "0009"
> Output: 1
> Explanation: We can turn the last wheel in reverse to move from "0000" -> "0009".
> ```
> 
> **Example 3:**
> ```
> Input: deadends = ["8887","8889","8878","8898","8788","8988","7888","9888"], target = "8888"
> Output: -1
> Explanation: We cannot reach the target without getting stuck.
> ```
> 
> **Constraints:**
> - 1 <= deadends.length <= 500
> - deadends[i].length == 4
> - target.length == 4
> - target will not be in the list deadends.
> - target and deadends[i] consist of digits only.

> [!info] Approach
> Each combination is a node; 8 neighbors (each of 4 digits ±1 mod 10). Unweighted BFS finds minimum turns. BFS on the implicit graph of 10,000 states. Encode combinations as strings. Skip deadends. Mark visited by adding to a set. Start with `"0000"` — if it's a deadend, return -1 immediately.


> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def open_lock(deadends, target):
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
> A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:
> Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.
> 
> **Example 1:**
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
> Output: 5
> Explanation: One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> cog", which is 5 words long.
> ```
> 
> **Example 2:**
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
> Output: 0
> Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.
> ```
> 
> **Constraints:**
> - 1 <= beginWord.length <= 10
> - endWord.length == beginWord.length
> - 1 <= wordList.length <= 5000
> - wordList[i].length == beginWord.length
> - beginWord, endWord, and wordList[i] consist of lowercase English letters.
> - beginWord != endWord
> - All the words in wordList are unique.

> [!info] Approach
> Nodes = words, edges = one-letter-apart pairs. Unweighted BFS gives shortest path. The graph is implicit — never enumerate all pairs (O(N²·L)) — instead generate neighbors by substitution. BFS where each level = one transformation. For each word, try replacing each position with `a-z` and check against the word set. Remove visited words from `word_set` immediately (not just a visited set) to prevent revisits efficiently.


> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def ladder_length(beginWord, endWord, wordList):
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
> A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:
> Given two words, beginWord and endWord, and a dictionary wordList, return all the shortest transformation sequences from beginWord to endWord, or an empty list if no such sequence exists. Each sequence should be returned as a list of the words [beginWord, s1, s2, ..., sk].
> 
> **Example 1:**
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
> Output: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
> Explanation: There are 2 shortest transformation sequences:
> "hit" -> "hot" -> "dot" -> "dog" -> "cog"
> "hit" -> "hot" -> "lot" -> "log" -> "cog"
> ```
> 
> **Example 2:**
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
> Output: []
> Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.
> ```
> 
> **Constraints:**
> - 1 <= beginWord.length <= 5
> - endWord.length == beginWord.length
> - 1 <= wordList.length <= 500
> - wordList[i].length == beginWord.length
> - beginWord, endWord, and wordList[i] consist of lowercase English letters.
> - beginWord != endWord
> - All the words in wordList are unique.
> - The sum of all shortest transformation sequences does not exceed 10^5.

> [!info] Approach
> Finding all shortest paths requires BFS to establish the level structure (shortest distance to each node), then backtracking to reconstruct paths — DFS alone is exponential without the level constraint. Two-phase: BFS to build a DAG of "parent → children" edges that lie on shortest paths; then DFS/backtracking on that DAG to enumerate all paths. BFS level-by-level. For each word, generate all 1-letter variants in the word set. Record `parents[new_word].add(word)`. Remove words from the set only after the full level is processed (so multiple parents at the same level can be recorded). Then DFS from `endWord` back to `beginWord` using the `parents` map.


> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def find_ladders(beginWord, endWord, wordList):
>     word_set = set(wordList)
>     if endWord not in word_set:
>         return []
> 
>     parents = defaultdict(set)
>     current_level = {beginWord}
>     found = False
> 
>     while current_level and not found:
>         word_set -= current_level      # remove current level to prevent back-edges
>         next_level = set()
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
>     result = []
> 
>     def backtrack(word, path):
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
> Given an n x n binary matrix grid, return the length of the shortest clear path in the matrix. If there is no clear path, return -1.
> A clear path in a binary matrix is a path from the top-left cell (i.e., (0, 0)) to the bottom-right cell (i.e., (n - 1, n - 1)) such that:
> The length of a clear path is the number of visited cells of this path.
> 
> **Example 1:**
> ```
> Input: grid = [[0,1],[1,0]]
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[0,0,0],[1,1,0],[1,1,0]]
> Output: 4
> ```
> 
> **Example 3:**
> ```
> Input: grid = [[1,0,0],[1,1,0],[1,1,0]]
> Output: -1
> ```
> 
> **Constraints:**
> - n == grid.length
> - n == grid[i].length
> - 1 <= n <= 100
> - grid[i][j] is 0 or 1

> [!info] Approach
> Unweighted grid shortest path = BFS. 8 directions. Mark visited in-place to save memory. BFS from `(0,0)`. First time we reach `(N-1,N-1)` is the shortest path. Check both endpoints are `0` before starting. Distance = BFS level when target is first reached.


> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def shortest_path_binary_matrix(grid):
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
> There is an undirected graph with n nodes, where each node is numbered between 0 and n - 1. You are given a 2D array graph, where graph[u] is an array of nodes that node u is adjacent to. More formally, for each v in graph[u], there is an undirected edge between node u and node v. The graph has the following properties:
> A graph is bipartite if the nodes can be partitioned into two independent sets A and B such that every edge in the graph connects a node in set A and a node in set B.
> Return true if and only if it is bipartite.
> 
> **Example 1:**
> ```
> Input: graph = [[1,2,3],[0,2],[0,1,3],[0,2]]
> Output: false
> Explanation: There is no way to partition the nodes into two independent sets such that every edge connects a node in one and a node in the other.
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[1,3],[0,2],[1,3],[0,2]]
> Output: true
> Explanation: We can partition the nodes into two sets: {0, 2} and {1, 3}.
> ```
> 
> **Constraints:**
> - graph.length == n
> - 1 <= n <= 100
> - 0 <= graph[u].length < n
> - 0 <= graph[u][i] <= n - 1
> - graph[u] does not contain u.
> - All the values of graph[u] are unique.
> - If graph[u] contains v, then graph[v] contains u.

> [!info] Approach
> A graph is bipartite iff it contains no odd-length cycle. 2-coloring detects this: if a neighbor already has the same color → odd cycle found. BFS/DFS coloring. Assign color `0` to start, alternate to neighbors. Must handle disconnected components — start BFS from every unvisited node.


> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def is_bipartite(graph):
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
> We want to split a group of n people (labeled from 1 to n) into two groups of any size. Each person may dislike some other people, and they should not go into the same group.
> Given the integer n and the array dislikes where dislikes[i] = [ai, bi] indicates that the person labeled ai does not like the person labeled bi, return true if it is possible to split everyone into two groups in this way.
> 
> **Example 1:**
> ```
> Input: n = 4, dislikes = [[1,2],[1,3],[2,4]]
> Output: true
> Explanation: The first group has [1,4], and the second group has [2,3].
> ```
> 
> **Example 2:**
> ```
> Input: n = 3, dislikes = [[1,2],[1,3],[2,3]]
> Output: false
> Explanation: We need at least 3 groups to divide them. We cannot put them in two groups.
> ```
> 
> **Constraints:**
> - 1 <= n <= 2000
> - 0 <= dislikes.length <= 10^4
> - dislikes[i].length == 2
> - 1 <= ai < bi <= n
> - All the pairs of dislikes are unique.

> [!info] Approach
> "Split into two groups with no conflicts" = 2-color the conflict graph = bipartite check. Build undirected graph from dislikes pairs. Run bipartite check. Identical to `isBipartite` — just build the graph first from `dislikes`.


> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def possible_bipartition(n, dislikes):
>     graph = defaultdict(list)
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
> MST problem on a dense graph (n² edges). Prim's is natural here — always extend the current MST by the cheapest reachable new node. Greedy — maintain a min-heap of `(cost, node)` for nodes not yet in the MST. Always pick the cheapest edge into the unvisited set. Start from node 0. Min-heap stores `(cost, node)`. Pop cheapest; if already visited, skip. Add its cost to total. Push all unvisited neighbors with Manhattan distance as cost. Repeat until all n nodes visited.


> [!note]- Python Solution
> ```python
> import heapq
> 
> def min_cost_connect_points(points):
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
> Graph coloring is NP-complete in general; backtracking with pruning is the standard approach for exact solutions on small graphs. Assign colors 1..m to nodes one at a time; backtrack if any color assignment conflicts with an already-colored neighbor. Try each color for the current node. Before assigning, check all neighbors — if a neighbor already has that color, skip. If all m colors fail → backtrack. If all nodes assigned → return True.


> [!note]- Python Solution
> ```python
> def graph_coloring(graph, m):
>     """
>     graph: adjacency list (0-indexed)
>     m: number of available colors
>     Returns True if m-coloring is possible.
>     """
>     n = len(graph)
>     color = [0] * n   # 0 = uncolored
> 
>     def is_safe(node, c):
>         return all(color[nb] != c for nb in graph[node])
> 
>     def backtrack(node):
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
> def graph_coloring_assignment(graph, m):
>     n = len(graph)
>     color = [0] * n
> 
>     def is_safe(node, c):
>         return all(color[nb] != c for nb in graph[node])
> 
>     def backtrack(node):
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
> Dijkstra does not work with negative edges. Bellman-Ford relaxes every edge `V-1` times, which is enough for shortest paths in a graph with no negative cycles. Initialize distances to infinity except the source. Repeatedly relax all edges. One more pass detects a negative cycle. If `dist[u] + w < dist[v]`, update `dist[v]`. After `V-1` passes, if any edge can still relax, a negative cycle exists.


> [!note]- Python Solution
> ```python
> def bellman_ford(n, edges, int, int]], source):
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

---

## Graph Algorithms — More Problems

### Shortest Path Visiting All Nodes (LC 847)

> [!example] Problem
> You have an undirected, connected graph of n nodes labeled from 0 to n - 1. You are given an array graph where graph[i] is a list of all the nodes connected with node i by an edge.
> Return the length of the shortest path that visits every node. You may start and stop at any node, you may revisit nodes multiple times, and you may reuse edges.
> 
> **Example 1:**
> ```
> Input: graph = [[1,2,3],[0],[0],[0]]
> Output: 4
> Explanation: One possible path is [1,0,2,0,3]
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[1],[0,2,4],[1,3,4],[2],[1,2]]
> Output: 4
> Explanation: One possible path is [0,1,4,2,3]
> ```
> 
> **Constraints:**
> - n == graph.length
> - 1 <= n <= 12
> - 0 <= graph[i].length < n
> - graph[i] does not contain i.
> - If graph[a] contains b, then graph[b] contains a.
> - The input graph is always connected.

> [!info] Approach
> This is TSP-like. With n ≤ 12, use BFS with bitmask state: `(node, visited_mask)`. BFS gives the shortest path. There are `n * 2^n` states — manageable for small n. Initialize queue with all `(node, 1 << node)` for every node (start from any node). BFS until `mask == (1 << n) - 1` (all visited). Visited set: `{(node, mask)}`. Dequeue state, try all neighbours. Update mask with `mask | (1 << neighbour)`.


> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def shortest_path_length(graph):
>     n = len(graph)
>     full_mask = (1 << n) - 1
>     if n == 1:
>         return 0
>     queue = deque()
>     visited = set()
>     for i in range(n):
>         mask = 1 << i
>         queue.append((i, mask, 0))
>         visited.add((i, mask))
>     while queue:
>         node, mask, dist = queue.popleft()
>         for neighbor in graph[node]:
>             new_mask = mask | (1 << neighbor)
>             if new_mask == full_mask:
>                 return dist + 1
>             if (neighbor, new_mask) not in visited:
>                 visited.add((neighbor, new_mask))
>                 queue.append((neighbor, new_mask, dist + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(n * 2^n), Space O(n * 2^n).

> [!tip] Alternatives
> - DP with bitmask (like TSP): `dp[mask][node]` = shortest path visiting exactly the nodes in mask and ending at `node`. Fills in O(n² * 2^n). BFS is simpler for unweighted graphs.

---

### Word Ladder II (LC 126)

> [!example] Problem
> A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:
> Given two words, beginWord and endWord, and a dictionary wordList, return all the shortest transformation sequences from beginWord to endWord, or an empty list if no such sequence exists. Each sequence should be returned as a list of the words [beginWord, s1, s2, ..., sk].
> 
> **Example 1:**
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
> Output: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
> Explanation: There are 2 shortest transformation sequences:
> "hit" -> "hot" -> "dot" -> "dog" -> "cog"
> "hit" -> "hot" -> "lot" -> "log" -> "cog"
> ```
> 
> **Example 2:**
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
> Output: []
> Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.
> ```
> 
> **Constraints:**
> - 1 <= beginWord.length <= 5
> - endWord.length == beginWord.length
> - 1 <= wordList.length <= 500
> - wordList[i].length == beginWord.length
> - beginWord, endWord, and wordList[i] consist of lowercase English letters.
> - beginWord != endWord
> - All the words in wordList are unique.
> - The sum of all shortest transformation sequences does not exceed 10^5.

> [!info] Approach
> BFS finds shortest path length. To reconstruct all paths, store the parent map during BFS (which words at the previous level can reach each word at the current level), then DFS backwards from `endWord` to `beginWord`. BFS layer by layer. For each word at the current layer, generate all one-letter mutations. If mutation is in the word set and not visited, add it to the next layer and record the parent. After BFS, DFS from endWord using the parent map to reconstruct paths. Remove words from `word_set` only after the full layer is processed — prevents cutting off valid same-layer paths.


> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> >
> def find_ladders(beginWord, endWord, wordList):
>     word_set = set(wordList)
>     if endWord not in word_set:
>         return []
>     parents = defaultdict(set)
>     layer = {beginWord}
>     found = False
>     while layer and not found:
>         word_set -= layer
>         next_layer = set()
>         for word in layer:
>             for i in range(len(word)):
>                 for c in 'abcdefghijklmnopqrstuvwxyz':
>                     new_word = word[:i] + c + word[i+1:]
>                     if new_word in word_set:
>                         next_layer.add(new_word)
>                         parents[new_word].add(word)
>                         if new_word == endWord:
>                             found = True
>         layer = next_layer
>     if not found:
>         return []
>     result = []
>     def dfs(word, path):
>         if word == beginWord:
>             result.append(list(reversed(path)))
>             return
>         for parent in parents[word]:
>             path.append(parent)
>             dfs(parent, path)
>             path.pop()
>     dfs(endWord, [endWord])
>     return result
> ```

> [!success] Complexity
> Time O(M² * N) where M = word length, N = wordList size. Space O(M * N).

> [!tip] Alternatives
> - Bidirectional BFS: expand from both ends, meet in the middle. Halves the search depth — significant speedup in practice.
> - Key pitfall: removing words from the set only after the entire layer is processed — otherwise words reachable from multiple same-layer words get cut prematurely.

---

### Travelling Salesman Problem — Bitmask DP

> [!example] Problem
> Given `n` cities and a distance matrix, find the shortest route that visits every city exactly once and returns to the starting city. Classic TSP.

> [!info] Approach
> Brute force is O(n!). Bitmask DP reduces to O(n² * 2^n) — tractable for n ≤ 20. `dp[mask][i]` = minimum cost to reach city `i` having visited exactly the cities in `mask`. Transition: for each unvisited city `j`, `dp[mask | (1<<j)][j] = min(..., dp[mask][i] + dist[i][j])`. Start with `dp[1][0] = 0` (started at city 0). Answer: `min(dp[full_mask][i] + dist[i][0])` for all `i`.


> [!note]- Python Solution
> ```python
> def tsp(dist):
>     n = len(dist)
>     full_mask = (1 << n) - 1
>     INF = float('inf')
>     dp = [[INF] * n for _ in range(1 << n)]
>     dp[1][0] = 0
>     for mask in range(1 << n):
>         for i in range(n):
>             if dp[mask][i] == INF:
>                 continue
>             if not (mask >> i & 1):
>                 continue
>             for j in range(n):
>                 if mask >> j & 1:
>                     continue
>                 new_mask = mask | (1 << j)
>                 if dp[new_mask][j] > dp[mask][i] + dist[i][j]:
>                     dp[new_mask][j] = dp[mask][i] + dist[i][j]
>     return min(dp[full_mask][i] + dist[i][0] for i in range(n))
> ```

> [!success] Complexity
> Time O(n² * 2^n), Space O(n * 2^n).

> [!tip] Alternatives
> - Held-Karp algorithm: same DP, just the classic name. O(n² * 2^n) is optimal for exact TSP.
> - For approximate TSP: Christofides' algorithm (1.5x approximation), or 2-opt local search for large instances.
> - Pattern shared with: Shortest Path Visiting All Nodes (LC 847), painting fence with k colors.

---

## See Also

[[graph]] | [[dynamic-programming]] | [[union-find]] | [[binary-search]]
