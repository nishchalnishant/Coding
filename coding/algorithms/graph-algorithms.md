---
tags: [coding, algorithms, graph-algorithms]
topic: Graph Algorithms
difficulty: mixed
---

# Graph Algorithms — Amazon SDE-2

Core patterns: BFS (shortest path in unweighted graphs), DFS (connectivity, cycle detection, topological sort), Dijkstra (SSSP with non-negative weights), Kahn's (topological sort + cycle check), Union-Find (connected components, MST), bipartite check.

---

## Dijkstra's Algorithm

### Network Delay Time

> [!example] Problem
> Directed weighted graph of n nodes. Send signal from node k. Return minimum time for all n nodes to receive the signal (max shortest-path distance from k), or -1 if unreachable.
>
> ```
> Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
> Output: 2
> ```

> [!info] Approach
> SSSP with non-negative weights. Min-heap `(dist, node)`. Lazy deletion: `if d > dist[u]: continue`. Answer = `max(dist.values())`.

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
>             continue
>         for w, v in graph[u]:
>             if dist[u] + w < dist[v]:
>                 dist[v] = dist[u] + w
>                 heapq.heappush(heap, (dist[v], v))
>
>     max_dist = max(dist.values())
>     return max_dist if max_dist < float('inf') else -1
> ```

> [!success] Complexity
> O((V + E) log V) time, O(V + E) space.

---

### Path with Maximum Probability

> [!example] Problem
> Undirected weighted graph with edge success probabilities. Find path with maximum probability from start to end.
>
> ```
> Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2
> Output: 0.25
> ```

> [!info] Approach
> Max-product instead of min-sum. Dijkstra with max-heap (negate values). Relaxation: `prob[u] * w > prob[v]` → update.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
>
> def max_probability(n, edges, succProb, start, end):
>     graph = defaultdict(list)
>     for (u, v), p in zip(edges, succProb):
>         graph[u].append((p, v))
>         graph[v].append((p, u))
>
>     prob = [0.0] * n
>     prob[start] = 1.0
>     heap = [(-1.0, start)]
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
> O((V + E) log V) time, O(V + E) space.

---

### Evaluate Division (Weighted BFS)

> [!example] Problem
> Given equations `a/b = k`, answer division queries `c/d = ?` using transitivity.
>
> ```
> Input: equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"]]
> Output: [6.0, 0.5]
> ```

> [!info] Approach
> Division is transitive: `a/c = (a/b) * (b/c)`. Model as weighted directed graph with edge `a→b` weight `k` and `b→a` weight `1/k`. BFS from src to dst, multiplying weights. Return -1.0 if src/dst unknown or unreachable.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
>
> def calc_equation(equations, values, queries):
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
>         q = deque([(src, 1.0)])
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
> O(Q·(V+E)) time, O(V+E) space.

---

## Bellman-Ford and Floyd-Warshall (Awareness)

**Bellman-Ford** — O(VE) SSSP that handles negative edge weights. Relax all edges V-1 times; a V-th relaxation indicates a negative cycle. Use when Dijkstra fails (negative weights) or when you need to detect negative cycles. Practical appearance: Cheapest Flights Within K Stops (relax exactly K+1 times, not V-1).

**Floyd-Warshall** — O(V³) all-pairs shortest paths. `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])` with `k` as outermost loop. Good for dense graphs with small V (≤ ~200). Used in: Find the City with Smallest Number of Neighbors at Threshold Distance (LC 1334).

> [!note]- Bellman-Ford (Cheapest Flights Within K Stops)
> ```python
> def find_cheapest_price(n, flights, src, dst, k):
>     prices = [float('inf')] * n
>     prices[src] = 0
>     for _ in range(k + 1):
>         temp = prices[:]
>         for u, v, w in flights:
>             if prices[u] != float('inf') and prices[u] + w < temp[v]:
>                 temp[v] = prices[u] + w
>         prices = temp
>     return prices[dst] if prices[dst] != float('inf') else -1
> ```

> [!note]- Floyd-Warshall (Find the City)
> ```python
> def find_the_city(n, edges, distanceThreshold):
>     dist = [[float('inf')] * n for _ in range(n)]
>     for i in range(n):
>         dist[i][i] = 0
>     for u, v, w in edges:
>         dist[u][v] = dist[v][u] = w
>     for k in range(n):          # k MUST be outermost
>         for i in range(n):
>             for j in range(n):
>                 if dist[i][k] + dist[k][j] < dist[i][j]:
>                     dist[i][j] = dist[i][k] + dist[k][j]
>     result, min_count = -1, n
>     for city in range(n):
>         count = sum(1 for j in range(n) if j != city and dist[city][j] <= distanceThreshold)
>         if count <= min_count:
>             min_count, result = count, city
>     return result
> ```

---

## Topological Sort (Kahn's BFS)

### Sequence Reconstruction (Unique Topo Order)

> [!example] Problem
> Check if `nums` is the only shortest supersequence for all given sequences. Equivalent to: is the topological order derived from the constraints unique?
>
> ```
> Input: nums = [1,2,3], sequences = [[1,2],[1,3],[2,3]] → Output: true
> Input: nums = [1,2,3], sequences = [[1,2],[1,3]] → Output: false
> ```

> [!info] Approach
> Build dependency graph from consecutive pairs in each sequence. Run Kahn's. At every BFS step, if queue has more than one element → not unique. Verify final order equals `nums`.

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
>             return False
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
> O(V + E) time, O(V + E) space.

---

### Find All Possible Recipes from Given Supplies

> [!example] Problem
> Recipes have ingredient dependencies; ingredients may themselves be recipes. Given initial supplies, return all recipes that can be made.
>
> ```
> Input: recipes = ["bread","sandwich"], ingredients = [["yeast","flour"],["bread","meat"]], supplies = ["yeast","flour","meat"]
> Output: ["bread","sandwich"]
> ```

> [!info] Approach
> Kahn's BFS with supplies as initial sources. Treat ingredients as edges into recipes. When a recipe's in-degree reaches 0, it's achievable and can unlock further recipes.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
>
> def find_all_recipes(recipes, ingredients, supplies):
>     graph = defaultdict(list)
>     indegree = defaultdict(int)
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
> O(V + E) time, O(V + E) space.

---

## Cycle Detection

### Detect Cycle in Directed Graph (DFS 3-Color)

> [!example] Problem
> Given a directed graph, determine whether it contains a cycle.

> [!info] Approach
> 3-color DFS: WHITE (unvisited), GRAY (on current DFS path), BLACK (done). A GRAY→GRAY edge = back edge = cycle. Kahn's alternative: cycle exists iff processed count < V.

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
>                 return True
>             if color[v] == WHITE and dfs(v):
>                 return True
>         color[u] = BLACK
>         return False
>
>     for node in range(n):
>         if color[node] == WHITE:
>             if dfs(node):
>                 return True
>     return False
> ```

> [!success] Complexity
> O(V + E) time, O(V) space.

> [!tip] Undirected graphs
> Cycle exists iff DFS finds a visited non-parent neighbor. Track parent or use edge index.

---

### Find Eventual Safe States (Reverse Graph + Kahn's)

> [!example] Problem
> A node is "safe" if every path from it leads to a terminal node (no outgoing edges). Return all safe nodes sorted.
>
> ```
> Input: graph = [[1,2],[2,3],[5],[0],[5],[],[]]
> Output: [2,4,5,6]
> ```

> [!info] Approach
> Unsafe nodes are on or lead to cycles. Reverse all edges; terminal nodes become sources. Kahn's on the reversed graph — a node is safe iff it propagates through.

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
> O(V + E) time, O(V + E) space.

---

## Multi-source BFS / Implicit Graphs

### Word Ladder (BFS on Implicit Graph)

> [!example] Problem
> Minimum transformation sequence from beginWord to endWord changing one letter at a time, using only words in wordList.
>
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
> Output: 5
> ```

> [!info] Approach
> Nodes = words, edges = one-letter-apart pairs. Generate neighbors by substituting each position with 'a'-'z' and checking the word set. Remove visited words from set immediately. BFS gives shortest transformation count.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def ladder_length(beginWord, endWord, wordList):
>     word_set = set(wordList)
>     if endWord not in word_set:
>         return 0
>
>     q = deque([(beginWord, 1)])
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
> O(M² · N) time, O(M · N) space where M = word length, N = wordList size.

---

### Open the Lock (BFS on State Graph)

> [!example] Problem
> 4-wheel lock, each digit 0-9, wraps. Start at "0000". Find minimum turns to reach target avoiding deadends.
>
> ```
> Input: deadends = ["0201","0101","0102","1212","2002"], target = "0202" → Output: 6
> ```

> [!info] Approach
> Each of 10,000 states is a node with 8 neighbors (4 digits × ±1). BFS on string states. Skip deadends. Mark visited.

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
>     q = deque([("0000", 0)])
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
> O(10^4 · 4) effectively bounded time, O(10^4) space.

---

## Bipartite Check

### Possible Bipartition

> [!example] Problem
> Split n people into two groups where no two people who dislike each other are in the same group. Return true if possible.
>
> ```
> Input: n = 4, dislikes = [[1,2],[1,3],[2,4]] → Output: true
> ```

> [!info] Approach
> 2-color the undirected conflict graph. BFS: assign color 0 to start, alternate colors. If a neighbor has the same color → not bipartite.

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
>         q = deque([start])
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
> O(V + E) time, O(V + E) space.

---

## Eulerian Path

### Reconstruct Itinerary (Hierholzer's)

> [!example] Problem
> Use all airline tickets exactly once. Start from "JFK". Return lexicographically smallest valid itinerary.
>
> ```
> Input: tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
> Output: ["JFK","ATL","JFK","SFO","ATL","SFO"]
> ```

> [!info] Approach
> "Use every edge exactly once" = Eulerian path. Hierholzer's post-order DFS: add a node to result only after all outgoing edges are exhausted. Sort adjacency lists in reverse; `.pop()` gives lexicographically smallest. Reverse result at end.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def find_itinerary(tickets):
>     graph = defaultdict(list)
>     for src, dst in tickets:
>         graph[src].append(dst)
>     for src in graph:
>         graph[src].sort(reverse=True)
>
>     result = []
>
>     def dfs(node):
>         while graph[node]:
>             dfs(graph[node].pop())
>         result.append(node)
>
>     dfs("JFK")
>     return result[::-1]
> ```

> [!success] Complexity
> O(E log E) for sorting, O(E) space.

---

## Minimum Spanning Tree (Prim's)

### Min Cost to Connect All Points

> [!example] Problem
> Connect all points with minimum total Manhattan distance (MST of complete graph).
>
> ```
> Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]] → Output: 20
> ```

> [!info] Approach
> Dense graph (n² edges) — Prim's with min-heap. Always extend MST by cheapest reachable new node. Start from node 0. Push all unvisited neighbors with Manhattan distance. Skip already-visited nodes.

> [!note]- Python Solution
> ```python
> import heapq
>
> def min_cost_connect_points(points):
>     n = len(points)
>     visited = [False] * n
>     heap = [(0, 0)]
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
> O(n² log n) time, O(n²) space. Kruskal's is equivalent. Prim's array (no heap) is O(n²) — optimal for dense graphs.

---

## See Also

[[backtracking]] | [[dynamic-programming]] | [[greedy]] | [[union-find]]
