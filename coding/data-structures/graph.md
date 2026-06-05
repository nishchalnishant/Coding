---
tags: [coding, data-structures, graph]
topic: graph
difficulty: mixed
---

# Graph Problems — Deep Dive

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop. Do not move on until these are reflexive.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Highly probable; know the core patterns cold. Edge cases matter less.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Know what it is conceptually; skip deep implementation practice.


**Pattern map**: Graph problems collapse into five patterns — BFS (shortest path, multi-source spread), DFS (connectivity, flood fill, cycle detection), Topological Sort (dependency ordering on DAGs), Shortest Path / Weighted (Dijkstra, modified BFS), Bipartite coloring, and Advanced (Union-Find / MST / DAG DP). Pick BFS when you need minimum steps; DFS when you need reachability or ordering; Union-Find when you need dynamic connectivity with no full traversal needed.

**Interview checklist**: First classify the graph — directed or undirected, weighted or unweighted, connected or disconnected, and whether you need a path, ordering, component count, or just a yes/no query. Then look for the standard lever: multi-source BFS for simultaneous spread, DFS for flood-fill and cycle detection, Kahn's for DAG ordering, Dijkstra for non-negative weights, Bellman-Ford for hop-limited or negative-weight cases, Union-Find for connectivity, and two-coloring for bipartite checks.

**Edge cases worth checking**: empty graph, single node, disconnected components, duplicate edges, self-loops, cycles in a "tree" input, and recursion depth on large grids/graphs. For grid problems, confirm whether diagonals count, whether borders are included, and whether you can mutate the input to mark visited.




---

## BFS on Graphs

### Rotting Oranges `⚡ T1`

> [!example] Problem
> You are given an m x n grid where each cell can have one of three values:
> Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.
> Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.
> 
> **Example 1:**
> ```
> Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
> Output: 4
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
> Output: -1
> Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.
> ```
> 
> **Example 3:**
> ```
> Input: grid = [[0,2]]
> Output: 0
> Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 10
> - grid[i][j] is 0, 1, or 2.

> [!info] Approach
> **Multi-source BFS — simultaneous spread from all rotten sources.** Rotting spreads simultaneously from all rotten sources. BFS levels naturally correspond to time steps; the first time a fresh orange is reached gives the minimum time to rot it. Seed queue with all initially rotten oranges at time 0, count fresh oranges. BFS level-by-level; each time a fresh orange is rotted, decrement fresh counter; track max time seen. Multi-source start avoids O(R × M×N) repeated BFS. Return max_time if fresh == 0, else -1.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def oranges_rotting(grid):
>     rows, cols = len(grid), len(grid[0])
>     queue = deque()
>     fresh = 0
> 
>     for r in range(rows):
>         for c in range(cols):
>             if grid[r][c] == 2:
>                 queue.append((r, c, 0))
>             elif grid[r][c] == 1:
>                 fresh += 1
> 
>     if fresh == 0:
>         return 0
> 
>     max_time = 0
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
>     while queue:
>         r, c, t = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
>                 grid[nr][nc] = 2
>                 fresh -= 1
>                 max_time = max(max_time, t + 1)
>                 queue.append((nr, nc, t + 1))
> 
>     return max_time if fresh == 0 else -1
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N).

> [!tip] Alternatives
> - BFS with level-counting loop (`for _ in range(len(queue))`): cleaner separation of time steps but identical logic.
> - DFS: can't guarantee minimum time — BFS is canonical for shortest path.
> - Simulation (repeat until stable): O((M×N)²), wasteful.

---

### Number of Islands (BFS) `⚡ T1`

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
> Each island is a connected component. BFS naturally fans out level-by-level from a source cell, marking all reachable land as visited. Iterate every cell; when '1' found, BFS to mark all connected land as visited ('0'), increment count. Seed the queue with the trigger cell; mark visited on enqueue (not dequeue) to prevent duplicate entries. Mutating the grid avoids an extra visited array.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def num_islands(grid):
>     if not grid:
>         return 0
>     rows, cols = len(grid), len(grid[0])
>     count = 0
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     for r in range(rows):
>         for c in range(cols):
>             if grid[r][c] == '1':
>                 count += 1
>                 grid[r][c] = '0'
>                 queue = deque([(r, c)])
>                 while queue:
>                     cr, cc = queue.popleft()
>                     for dr, dc in dirs:
>                         nr, nc = cr+dr, cc+dc
>                         if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
>                             grid[nr][nc] = '0'
>                             queue.append((nr, nc))
>     return count
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N) worst case for the queue/visited cells.

> [!tip] Alternatives
> - DFS sinking: same logic recursively; simpler code but risks recursion depth on large grids.
> - Union-Find: union adjacent '1' cells; count unique roots. O(M×N·α). Better for dynamic updates.

---

### Walls and Gates (LC 286) `⚡ T1`

> [!example] Problem
> You are given an `m x n` grid `rooms` initialized with these three possible values.
> 
> 	
> - `-1` A wall or an obstacle.
> 	
> - `0` A gate.
> 	
> - `INF` Infinity means an empty room. We use the value `2^31 - 1 = 2147483647` to represent `INF` as you may assume that the distance to a gate is less than `2147483647`.
> 
> Fill each empty room with the distance to *its nearest gate*. If it is impossible to reach a gate, it should be filled with `INF`.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** rooms = [[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]]
> **Output:** [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** rooms = [[-1]]
> **Output:** [[-1]]
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `m == rooms.length`
> 	
> - `n == rooms[i].length`
> 	
> - `1 <= m, n <= 250`
> 	
> - `rooms[i][j]` is `-1`, `0`, or `2^31 - 1`.

> [!info] Approach
> Multi-source BFS from all gates simultaneously guarantees every room is reached via the shortest path to any gate in O(M×N) rather than O(M×N × gates) from separate BFS per room. Seed queue with all gates (value 0); BFS outward; assign `dist[gate] + 1` to unvisited INF neighbors. Only enqueue cells that are INF — this acts as the visited guard. The first time a room is reached is always via its nearest gate.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def walls_and_gates(rooms):
>     if not rooms:
>         return
>     rows, cols = len(rooms), len(rooms[0])
>     INF = float('inf')
>     queue = deque()
>     for r in range(rows):
>         for c in range(cols):
>             if rooms[r][c] == 0:
>                 queue.append((r, c))
> 
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
>     while queue:
>         r, c = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
>                 rooms[nr][nc] = rooms[r][c] + 1
>                 queue.append((nr, nc))
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N).

> [!tip] Alternatives
> - BFS from each gate separately: O(M×N × G) where G = number of gates — valid but far slower.
> - DFS from each gate: same O(M×N × G) issue; also won't guarantee shortest distance without revisit tracking.

---

### 01 Matrix (LC 542) `⚡ T1`

> [!example] Problem
> Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell.
> The distance between two cells sharing a common edge is 1.
> 
> **Example 1:**
> ```
> Input: mat = [[0,0,0],[0,1,0],[0,0,0]]
> Output: [[0,0,0],[0,1,0],[0,0,0]]
> ```
> 
> **Example 2:**
> ```
> Input: mat = [[0,0,0],[0,1,0],[1,1,1]]
> Output: [[0,0,0],[0,1,0],[1,2,1]]
> ```
> 
> **Constraints:**
> - m == mat.length
> - n == mat[i].length
> - 1 <= m, n <= 10^4
> - 1 <= m * n <= 10^4
> - mat[i][j] is either 0 or 1.
> - There is at least one 0 in mat.

> [!info] Approach
> Multi-source BFS from all 0-cells simultaneously propagates shortest distances outward in O(M×N). The alternative (BFS from each 1-cell) is O(M²×N²). Seed queue with all 0-positions (distance 0); mark 1-cells as unvisited (distance INF); BFS expanding to unvisited neighbors with distance + 1. Initialize dist matrix with 0 for zeroes, INF for ones. Enqueue all zeroes at start. Only update a cell if current dist > neighbor dist + 1.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def update_matrix(mat):
>     rows, cols = len(mat), len(mat[0])
>     dist = [[0 if mat[r][c] == 0 else float('inf') for c in range(cols)] for r in range(rows)]
>     queue = deque((r, c) for r in range(rows) for c in range(cols) if mat[r][c] == 0)
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     while queue:
>         r, c = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] > dist[r][c] + 1:
>                 dist[nr][nc] = dist[r][c] + 1
>                 queue.append((nr, nc))
>     return dist
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N).

> [!tip] Alternatives
> - DP two-pass (top-left then bottom-right): O(M×N) time, O(1) extra space. Elegant but harder to reason about correctness.
> - DFS: can reach the same cell multiple times before finding minimum — not correct without full relaxation.

---

### Word Ladder `⚡ T1`

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
> **BFS on implicit word graph — L×26 mutation enumeration.** Shortest path in an implicit unweighted graph → BFS. Don't build the graph explicitly (O(N²) pairs); generate all L×26 single-character mutations of the current word and check against the word set — O(L×26) per word instead of O(N×L) pairwise comparison. BFS from `beginWord`; remove words from the set as soon as they are enqueued to prevent revisits. For each word dequeued, try all single-char mutations; if mutation == endWord, return. Otherwise enqueue if the word is still in the set and then delete it.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def ladder_length(beginWord, endWord, wordList):
>     word_set = set(wordList)
>     if endWord not in word_set:
>         return 0
> 
>     queue = deque([(beginWord, 1)])
> 
>     while queue:
>         word, length = queue.popleft()
>         for i in range(len(word)):
>             for c in 'abcdefghijklmnopqrstuvwxyz':
>                 next_word = word[:i] + c + word[i+1:]
>                 if next_word == endWord:
>                     return length + 1
>                 if next_word in word_set:
>                     word_set.remove(next_word)
>                     queue.append((next_word, length + 1))
> 
>     return 0
> ```

> [!success] Complexity
> Time O(N × M² × 26) ≈ O(N × M²), where M = word length and N = wordList size. Space O(N × M) for the word set and queue.

> [!tip] Alternatives
> - Bidirectional BFS: expand from both `beginWord` and `endWord` simultaneously; reduces explored nodes from O(b^d) to O(b^(d/2)). Follow-up standard.
> - Preprocessed adjacency via patterns: build `"h*t" → [hot, hit]` map; O(M×N) preprocessing, then O(M²×N) BFS — same asymptotic but faster in practice.

---

### Employee Importance

> [!example] Problem
> You have a data structure of employee information, including the employee's unique ID, importance value, and direct subordinates' IDs.
> You are given an array of employees employees where:
> Given an integer id that represents an employee's ID, return the total importance value of this employee and all their direct and indirect subordinates.
> 
> **Example 1:**
> ```
> Input: employees = [[1,5,[2,3]],[2,3,[]],[3,3,[]]], id = 1
> Output: 11
> Explanation: Employee 1 has an importance value of 5 and has two direct subordinates: employee 2 and employee 3.
> They both have an importance value of 3.
> Thus, the total importance value of employee 1 is 5 + 3 + 3 = 11.
> ```
> 
> **Example 2:**
> ```
> Input: employees = [[1,2,[5]],[5,-3,[]]], id = 5
> Output: -3
> Explanation: Employee 5 has an importance value of -3 and has no direct subordinates.
> Thus, the total importance value of employee 5 is -3.
> ```
> 
> **Constraints:**
> - 1 <= employees.length <= 2000
> - 1 <= employees[i].id <= 2000
> - All employees[i].id are unique.
> - -100 <= employees[i].importance <= 100
> - One employee has at most one direct leader and may have several subordinates.
> - The IDs in employees[i].subordinates are valid IDs.

> [!info] Approach
> **Hash map + BFS over subordinate ids.** Tree/DAG reachability with value aggregation. Hash map first: direct subordinate ids require O(N) linear scan per lookup without a map; O(1) with a map. BFS/DFS from target employee id, sum importance values. Build `{id: employee}` map; BFS — dequeue id, add importance, enqueue all subordinate ids.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def get_importance(employees, id):
>     emp_map = {e.id: e for e in employees}
>     total = 0
>     queue = deque([id])
>     while queue:
>         eid = queue.popleft()
>         e = emp_map[eid]
>         total += e.importance
>         queue.extend(e.subordinates)
>     return total
> ```

> [!success] Complexity
> Time O(N), Space O(N).

> [!tip] Alternatives
> - DFS recursive: `return emp.importance + sum(getImportance(..., sub) for sub in emp.subordinates)`. Clean but risks recursion depth for deep hierarchies.
> - Without hash map: O(N²) — linear scan per id lookup, avoid.

---

### Find if Path Exists in a Graph `⚡ T1`

> [!example] Problem
> Given n nodes, a list of bidirectional edges, source and destination, determine if a valid path exists.

> [!info] Approach
> **Union-Find — reachability in O(E α(N)).** Union-Find answers "are they connected?" in near O(1) per query after O(E) union operations — no traversal needed. Union all edges; check if `find(source) == find(destination)`. Path compression + union by rank for optimal performance.

> [!note]- Python Solution
> ```python
> def valid_path(n, edges, source, destination):
>     parent = list(range(n))
>     rank = [0] * n
> 
>     def find(x):
>         while parent[x] != x:
>             parent[x] = parent[parent[x]]  # path compression
>             x = parent[x]
>         return x
> 
>     def union(a, b):
>         ra, rb = find(a), find(b)
>         if ra == rb:
>             return
>         if rank[ra] < rank[rb]:
>             ra, rb = rb, ra
>         parent[rb] = ra
>         if rank[ra] == rank[rb]:
>             rank[ra] += 1
> 
>     for a, b in edges:
>         union(a, b)
> 
>     return find(source) == find(destination)
> ```

> [!success] Complexity
> Time O(E·α(N)) ≈ O(E), Space O(N).

> [!tip] Alternatives
> - BFS/DFS: O(V+E), correct but does more work than needed for pure reachability.
> - Bidirectional BFS: useful if graph is large and path likely exists — meets in the middle.

---

### Find Center of Star Graph

> [!example] Problem
> There is an undirected star graph consisting of n nodes labeled from 1 to n. A star graph is a graph where there is one center node and exactly n - 1 edges that connect the center node with every other node.
> You are given a 2D integer array edges where each edges[i] = [ui, vi] indicates that there is an edge between the nodes ui and vi. Return the center of the given star graph.
> 
> **Example 1:**
> ```
> Input: edges = [[1,2],[2,3],[4,2]]
> Output: 2
> Explanation: As shown in the figure above, node 2 is connected to every other node, so 2 is the center.
> ```
> 
> **Example 2:**
> ```
> Input: edges = [[1,2],[5,1],[1,3],[1,4]]
> Output: 1
> ```
> 
> **Constraints:**
> - 3 <= n <= 10^5
> - edges.length == n - 1
> - edges[i].length == 2
> - 1 <= ui, vi <= n
> - ui != vi
> - The given edges represent a valid star graph.

> [!info] Approach
> **O(1) — center appears in both the first and second edges.** The center appears in every edge. The center is the only node common to both the first and second edges — no traversal needed. Find the intersection of `edges[0]` and `edges[1]`. Check if `edges[0][0]` is in `edges[1]`; if so, it's the center; otherwise `edges[0][1]` is the center.

> [!note]- Python Solution
> ```python
> def find_center(edges):
>     a, b = edges[0]
>     c, d = edges[1]
>     return a if a == c or a == d else b
> ```

> [!success] Complexity
> Time O(1), Space O(1).

> [!tip] Alternatives
> - Degree count: node with degree n-1 is center. O(E) — massively over-engineered.
> - `set(edges[0]) & set(edges[1])` → pop(): Pythonic O(1) using set intersection.

---

## DFS on Graphs

### Number of Islands `⚡ T1`

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
> **DFS sinking — flood-fill each component, count triggers.** Each island is a connected component of '1' cells. DFS marks all cells in a component as visited in one pass. Iterate every cell; when a '1' is found, DFS to sink all connected land (set to '0'), increment count. Sinking avoids a separate visited array — the mutation is the visit mark. Increment count only on the initial call, not within DFS.

> [!note]- Python Solution
> ```python
> def num_islands(grid):
>     if not grid:
>         return 0
>     rows, cols = len(grid), len(grid[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
>             return
>         grid[r][c] = '0'
>         dfs(r+1, c)
>         dfs(r-1, c)
>         dfs(r, c+1)
>         dfs(r, c-1)
> 
>     count = 0
>     for r in range(rows):
>         for c in range(cols):
>             if grid[r][c] == '1':
>                 dfs(r, c)
>                 count += 1
>     return count
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N) recursion stack worst case.

> [!tip] Alternatives
> - BFS: use queue; identical complexity, avoids deep recursion stack on large inputs — prefer for 200×200+ grids.
> - Union-Find: union adjacent '1' cells; count roots. O(M×N·α). Better if grid changes dynamically.
> - Iterative DFS with explicit stack: avoids Python recursion limit.

---

### Flood Fill `⚡ T1`

> [!example] Problem
> You are given an image represented by an m x n grid of integers image, where image[i][j] represents the pixel value of the image. You are also given three integers sr, sc, and color. Your task is to perform a flood fill on the image starting from the pixel image[sr][sc].
> To perform a flood fill:
> Return the modified image after performing the flood fill.
> 
> **Example 1:**
> ```
> Input: image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2
> Output: [[2,2,2],[2,2,0],[2,0,1]]
> Explanation:
> 
> From the center of the image with position (sr, sc) = (1, 1) (i.e., the red pixel), all pixels connected by a path of the same color as the starting pixel (i.e., the blue pixels) are colored with the new color.
> Note the bottom corner is not colored 2, because it is not horizontally or vertically connected to the starting pixel.
> ```
> 
> **Example 2:**
> ```
> Input: image = [[0,0,0],[0,0,0]], sr = 0, sc = 0, color = 0
> Output: [[0,0,0],[0,0,0]]
> Explanation:
> The starting pixel is already colored with 0, which is the same as the target color. Therefore, no changes are made to the image.
> ```
> 
> **Constraints:**
> - m == image.length
> - n == image[i].length
> - 1 <= m, n <= 50
> - 0 <= image[i][j], color < 216
> - 0 <= sr < m
> - 0 <= sc < n

> [!info] Approach
> **DFS recolor — guard against same-color infinite loop.** Connected-component traversal. Early return if original == new color: recursion would infinitely revisit cells (no termination condition). DFS from (sr, sc); recolor cells matching the original color. Guard with `if original == color: return image` before DFS.

> [!note]- Python Solution
> ```python
> def flood_fill(image, sr, sc, color):
>     original = image[sr][sc]
>     if original == color:
>         return image
>     rows, cols = len(image), len(image[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or image[r][c] != original:
>             return
>         image[r][c] = color
>         dfs(r+1, c)
>         dfs(r-1, c)
>         dfs(r, c+1)
>         dfs(r, c-1)
> 
>     dfs(sr, sc)
>     return image
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N) recursion stack.

> [!tip] Alternatives
> - BFS with deque: iterative, avoids recursion depth issues on large images.
> - Separate `visited` set instead of in-place mutation: same complexity but extra O(M×N) space.

---

### Max Area of Island `⚡ T1`

> [!example] Problem
> You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.
> The area of an island is the number of cells with a value 1 in the island.
> Return the maximum area of an island in grid. If there is no island, return 0.
> 
> **Example 1:**
> ```
> Input: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
> Output: 6
> Explanation: The answer is not 11, because the island must be connected 4-directionally.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[0,0,0,0,0,0,0,0]]
> Output: 0
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 50
> - grid[i][j] is either 0 or 1.

> [!info] Approach
> **DFS returning component size — sink inline.** Variation on Number of Islands where we need the maximum component size. DFS function returns the count of cells in the component instead of just marking. `1 + sum of returns from 4 neighbors`. Sink cells inline; DFS returns 0 for non-land or out-of-bounds. `max(dfs(r,c) for all r,c)` — zero-cost for water cells.

> [!note]- Python Solution
> ```python
> def max_area_of_island(grid):
>     rows, cols = len(grid), len(grid[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
>             return 0
>         grid[r][c] = 0
>         return 1 + dfs(r+1,c) + dfs(r-1,c) + dfs(r,c+1) + dfs(r,c-1)
> 
>     return max(dfs(r, c) for r in range(rows) for c in range(cols))
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N).

> [!tip] Alternatives
> - BFS: count cells as dequeued. Same complexity.
> - Union-Find with size tracking: O(M×N·α); useful for dynamic grid updates.

---

### Surrounded Regions `⚡ T1`

> [!example] Problem
> You are given an m x n matrix board containing letters 'X' and 'O', capture regions that are surrounded:
> To capture a surrounded region, replace all 'O's with 'X's in-place within the original board. You do not need to return anything.
> 
> **Example 1:**
> ```
> Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
> Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
> Explanation:
> In the above diagram, the bottom region is not captured because it is on the edge of the board and cannot be surrounded.
> ```
> 
> **Example 2:**
> ```
> Input: board = [["X"]]
> Output: [["X"]]
> ```
> 
> **Constraints:**
> - m == board.length
> - n == board[i].length
> - 1 <= m, n <= 200
> - board[i][j] is 'X' or 'O'.

> [!info] Approach
> **Reverse DFS — mark border-safe 'O's, then flip interior.** Directly checking if an 'O' region is surrounded requires backtracking to undo if DFS touches a border. Instead: find all border-connected 'O's first (safe cells), then flip everything else. DFS from every border 'O', mark safe cells with sentinel 'S'. Then: interior 'O' → 'X', 'S' → 'O'. Walk all 4 borders, DFS from each 'O' found there.

> [!note]- Python Solution
> ```python
> def solve(board):
>     if not board:
>         return
>     rows, cols = len(board), len(board[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
>             return
>         board[r][c] = 'S'
>         dfs(r+1, c)
>         dfs(r-1, c)
>         dfs(r, c+1)
>         dfs(r, c-1)
> 
>     for r in range(rows):
>         dfs(r, 0)
>         dfs(r, cols-1)
>     for c in range(cols):
>         dfs(0, c)
>         dfs(rows-1, c)
> 
>     for r in range(rows):
>         for c in range(cols):
>             if board[r][c] == 'O':   board[r][c] = 'X'
>             elif board[r][c] == 'S': board[r][c] = 'O'
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N) recursion stack.

> [!tip] Alternatives
> - BFS from borders: iterative, avoids recursion stack overflow.
> - Union-Find with virtual border node: union all 'O's; any component containing the border node is safe. Elegant but more code.

---

### Pacific Atlantic Water Flow `⚡ T1`

> [!example] Problem
> There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.
> The island is partitioned into a grid of square cells. You are given an m x n integer matrix heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c).
> The island receives a lot of rain, and the rain water can flow to neighboring cells directly north, south, east, and west if the neighboring cell's height is less than or equal to the current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.
> Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rain water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.
> 
> **Example 1:**
> ```
> Input: heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
> Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
> Explanation: The following cells can flow to the Pacific and Atlantic oceans, as shown below:
> [0,4]: [0,4] -> Pacific Ocean 
>        [0,4] -> Atlantic Ocean
> [1,3]: [1,3] -> [0,3] -> Pacific Ocean 
>        [1,3] -> [1,4] -> Atlantic Ocean
> [1,4]: [1,4] -> [1,3] -> [0,3] -> Pacific Ocean 
>        [1,4] -> Atlantic Ocean
> [2,2]: [2,2] -> [1,2] -> [0,2] -> Pacific Ocean 
>        [2,2] -> [2,3] -> [2,4] -> Atlantic Ocean
> [3,0]: [3,0] -> Pacific Ocean 
>        [3,0] -> [4,0] -> Atlantic Ocean
> [3,1]: [3,1] -> [3,0] -> Pacific Ocean 
>        [3,1] -> [4,1] -> Atlantic Ocean
> [4,0]: [4,0] -> Pacific Ocean 
>        [4,0] -> Atlantic Ocean
> Note that there are other possible paths for these cells to flow to the Pacific and Atlantic oceans.
> ```
> 
> **Example 2:**
> ```
> Input: heights = [[1]]
> Output: [[0,0]]
> Explanation: The water can flow from the only cell to the Pacific and Atlantic oceans.
> ```
> 
> **Constraints:**
> - m == heights.length
> - n == heights[r].length
> - 1 <= m, n <= 200
> - 0 <= heights[r][c] <= 10^5

> [!info] Approach
> **Reverse BFS from both ocean borders — intersect reachable sets.** Checking forward from each cell whether it reaches both oceans requires O(M²N²) DFS calls. Reverse: "which cells can be reached from the ocean borders?" — water flows uphill in reverse. BFS from all Pacific border cells (mark reachable); BFS from all Atlantic border cells; intersect. Reverse BFS condition — expand to neighbors with height >= current height (uphill in the reverse direction).

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def pacific_atlantic(heights):
>     rows, cols = len(heights), len(heights[0])
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     def bfs(starts):
>         visited = set(starts)
>         queue = deque(starts)
>         while queue:
>             r, c = queue.popleft()
>             for dr, dc in dirs:
>                 nr, nc = r+dr, c+dc
>                 if (0 <= nr < rows and 0 <= nc < cols
>                         and (nr, nc) not in visited
>                         and heights[nr][nc] >= heights[r][c]):
>                     visited.add((nr, nc))
>                     queue.append((nr, nc))
>         return visited
> 
>     pacific  = bfs([(r, 0) for r in range(rows)] + [(0, c) for c in range(cols)])
>     atlantic = bfs([(r, cols-1) for r in range(rows)] + [(rows-1, c) for c in range(cols)])
>     return [[r, c] for r, c in pacific & atlantic]
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N).

> [!tip] Alternatives
> - DFS from borders: same logic, recursive. Watch recursion depth on large grids.
> - Forward DFS with memoization per cell: O(M×N) with full memoization but harder to implement correctly.

---

### All Paths From Source to Target `⚡ T1`

> [!example] Problem
> Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1, find all possible paths from node 0 to node n - 1 and return them in any order.
> The graph is given as follows: graph[i] is a list of all nodes you can visit from node i (i.e., there is a directed edge from node i to node graph[i][j]).
> 
> **Example 1:**
> ```
> Input: graph = [[1,2],[3],[3],[]]
> Output: [[0,1,3],[0,2,3]]
> Explanation: There are two paths: 0 -> 1 -> 3 and 0 -> 2 -> 3.
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[4,3,1],[3,2,4],[3],[4],[]]
> Output: [[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]
> ```
> 
> **Constraints:**
> - n == graph.length
> - 2 <= n <= 15
> - 0 <= graph[i][j] < n
> - graph[i][j] != i (i.e., there will be no self-loops).
> - All the elements of graph[i] are unique.
> - The input graph is guaranteed to be a DAG.

> [!info] Approach
> **DFS backtracking on DAG — no visited set needed.** It's a DAG — no cycles, so DFS can never revisit a node on the current path. No visited set needed. DFS with backtracking — enumerate all paths. When node n-1 is reached, record a copy of the current path. `path.append(nei)`, recurse, `path.pop()`.

> [!note]- Python Solution
> ```python
> def all_paths_source_target(graph):
>     target = len(graph) - 1
>     result = []
> 
>     def dfs(node, path):
>         if node == target:
>             result.append(list(path))
>             return
>         for nei in graph[node]:
>             path.append(nei)
>             dfs(nei, path)
>             path.pop()
> 
>     dfs(0, [0])
>     return result
> ```

> [!success] Complexity
> Time O(2^V × V) worst case (exponential paths). Space O(V) recursion depth + O(2^V × V) output.

> [!tip] Alternatives
> - BFS with path tracking: store `(node, path)` in queue. More memory (all partial paths in queue simultaneously).
> - Memoization: cache paths from each node to target. Reduces redundant computation when paths converge.

---

### Number of Provinces (LC 547) `⚡ T1`

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
> Each province is a connected component of an undirected graph. DFS marks all cities in a component as visited in one pass. Iterate each city; if unvisited, DFS to mark all reachable cities, increment province count. Use a visited array instead of mutating the matrix. The matrix is symmetric but you only need to follow one direction per city.

> [!note]- Python Solution
> ```python
> def find_circle_num(isConnected):
>     n = len(isConnected)
>     visited = [False] * n
> 
>     def dfs(city):
>         for neighbor in range(n):
>             if isConnected[city][neighbor] == 1 and not visited[neighbor]:
>                 visited[neighbor] = True
>                 dfs(neighbor)
> 
>     provinces = 0
>     for i in range(n):
>         if not visited[i]:
>             visited[i] = True
>             dfs(i)
>             provinces += 1
>     return provinces
> ```

> [!success] Complexity
> Time O(n²), Space O(n) recursion + visited array.

> [!tip] Alternatives
> - Union-Find: union(i, j) for all isConnected[i][j] == 1; count unique roots. O(n²·α). Better if the graph evolves dynamically.
> - BFS: identical logic with a queue; avoids deep recursion on large n.

---

### Number of Enclaves (LC 1020) `⚡ T1`

> [!example] Problem
> You are given an m x n binary matrix grid, where 0 represents a sea cell and 1 represents a land cell.
> A move consists of walking from one land cell to another adjacent (4-directionally) land cell or walking off the boundary of the grid.
> Return the number of land cells in grid for which we cannot walk off the boundary of the grid in any number of moves.
> 
> **Example 1:**
> ```
> Input: grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]
> Output: 3
> Explanation: There are three 1s that are enclosed by 0s, and one 1 that is not enclosed because its on the boundary.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]
> Output: 0
> Explanation: All 1s are either on the boundary or can reach the boundary.
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 500
> - grid[i][j] is either 0 or 1.

> [!info] Approach
> Any land cell connected to the border can reach the sea — it is NOT an enclave. Mirror of Surrounded Regions: mark all border-reachable land, then count remaining interior land. DFS/BFS from every border land cell, mark visited. Count unvisited land cells in the interior. Walk all 4 borders; DFS from each '1' encountered, sinking to 0. After traversal, sum remaining 1-cells.

> [!note]- Python Solution
> ```python
> def num_enclaves(grid):
>     rows, cols = len(grid), len(grid[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
>             return
>         grid[r][c] = 0
>         dfs(r+1, c)
>         dfs(r-1, c)
>         dfs(r, c+1)
>         dfs(r, c-1)
> 
>     for r in range(rows):
>         dfs(r, 0)
>         dfs(r, cols-1)
>     for c in range(cols):
>         dfs(0, c)
>         dfs(rows-1, c)
> 
>     return sum(grid[r][c] for r in range(rows) for c in range(cols))
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N) recursion stack.

> [!tip] Alternatives
> - BFS from borders: iterative, avoids recursion stack overflow on large grids.
> - Union-Find with virtual border node: union all land cells; union border land with a sentinel; count non-sentinel roots. Same complexity, more code.

---

### Clone Graph `⚡ T1`

> [!example] Problem
> Given a reference of a node in a connected undirected graph.
> Return a deep copy (clone) of the graph.
> Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.
> Test case format:
> For simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with val == 1, the second node with val == 2, and so on. The graph is represented in the test case using an adjacency list.
> An adjacency list is a collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a node in the graph.
> The given node will always be the first node with val = 1. You must return the copy of the given node as a reference to the cloned graph.
> 
> **Example 1:**
> ```
> class Node {
>     public int val;
>     public List neighbors;
> }
> ```
> 
> **Example 2:**
> ```
> Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
> Output: [[2,4],[1,3],[2,4],[1,3]]
> Explanation: There are 4 nodes in the graph.
> 1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
> 2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
> 3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
> 4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
> ```
> 
> **Example 3:**
> ```
> Input: adjList = [[]]
> Output: [[]]
> Explanation: Note that the input contains one empty list. The graph consists of only one node with val = 1 and it does not have any neighbors.
> ```
> 
> **Example 4:**
> ```
> Input: adjList = []
> Output: []
> Explanation: This an empty graph, it does not have any nodes.
> ```
> 
> **Constraints:**
> - The number of nodes in the graph is in the range [0, 100].
> - 1 <= Node.val <= 100
> - Node.val is unique for each node.
> - There are no repeated edges and no self-loops in the graph.
> - The Graph is connected and all nodes can be visited starting from the given node.

> [!info] Approach
> **DFS with original→clone map — register before recursing.** Without pre-registration, revisiting a node (via a cycle) creates a new clone instead of returning the existing one — producing duplicates and infinite loops. `{original: clone}` map as memo; DFS from start. Create clone, register in map, then recurse to clone neighbors. Guard `if n in visited: return visited[n]` handles cycles. Register BEFORE recursing into neighbors.

> [!note]- Python Solution
> ```python
> def clone_graph(node):
>     if not node:
>         return None
>     visited = {}
> 
>     def dfs(n):
>         if n in visited:
>             return visited[n]
>         clone = Node(n.val)
>         visited[n] = clone  # register BEFORE recursing — critical for cycle safety
>         for nei in n.neighbors:
>             clone.neighbors.append(dfs(nei))
>         return clone
> 
>     return dfs(node)
> ```

> [!success] Complexity
> Time O(V+E), Space O(V).

> [!tip] Alternatives
> - BFS: use queue; same `visited` map; iterative. O(V+E)/O(V).
> - Two-pass: create all clones (V pass), then wire neighbors (E pass). Cleaner separation, same complexity.

---

### Find Eventual Safe States `⚡ T1`

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
> **Three-color DFS — 0=unvisited, 1=in-progress, 2=safe.** Need to distinguish "currently being explored" (on the DFS path, could be on a cycle) from "confirmed safe" (all paths from it terminate). 0 = unvisited, 1 = in-progress (gray), 2 = confirmed safe (black). DFS reaching a gray node → cycle → current path is unsafe. Mark gray before recursing neighbors; mark black after all neighbors are confirmed safe.

> [!note]- Python Solution
> ```python
> def eventual_safe_nodes(graph):
>     n = len(graph)
>     state = [0] * n  # 0=unvisited, 1=visiting, 2=safe
> 
>     def dfs(node):
>         if state[node] == 1:  return False  # cycle
>         if state[node] == 2:  return True   # already safe
>         state[node] = 1
>         for nei in graph[node]:
>             if not dfs(nei):
>                 return False
>         state[node] = 2
>         return True
> 
>     return [i for i in range(n) if dfs(i)]
> ```

> [!success] Complexity
> Time O(V+E), Space O(V) recursion stack.

> [!tip] Alternatives
> - Reverse graph + Kahn's topo sort: reverse all edges; terminal nodes become sources; run Kahn's; all nodes processed in topo sort are safe. Iterative — avoids recursion depth issues. Often faster in practice.
> - SCC detection (Tarjan/Kosaraju): nodes not in any non-trivial SCC are safe. Overkill here.

---

## Topological Sort

### Course Schedule II `⚡ T1`

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
> **Kahn's topo sort — collect removal order.** Kahn's algorithm naturally produces a topological order — the BFS order of removal. Same algorithm as Course Schedule; collect nodes as they're removed. If `len(order) == numCourses`, it's valid; otherwise a cycle was detected. Append node to `order` as it's dequeued; return order or [].

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def find_order(numCourses, prerequisites):
>     graph = [[] for _ in range(numCourses)]
>     indegree = [0] * numCourses
>     for a, b in prerequisites:
>         graph[b].append(a)
>         indegree[a] += 1
> 
>     queue = deque(c for c in range(numCourses) if indegree[c] == 0)
>     order = []
>     while queue:
>         node = queue.popleft()
>         order.append(node)
>         for nei in graph[node]:
>             indegree[nei] -= 1
>             if indegree[nei] == 0:
>                 queue.append(nei)
> 
>     return order if len(order) == numCourses else []
> ```

> [!success] Complexity
> Time O(V+E), Space O(V+E).

> [!tip] Alternatives
> - DFS post-order: append node after all successors processed; reverse at end. O(V+E). Multiple valid orderings are possible — both Kahn's and DFS may give different correct answers.
> - Edge direction gotcha: for "a requires b", edge is `b → a` (b must come before a), not `a → b`.

---

### Minimum Number of Vertices to Reach All Nodes `⚡ T1`

> [!example] Problem
> Given a directed acyclic graph, with n vertices numbered from 0 to n-1, and an array edges where edges[i] = [fromi, toi] represents a directed edge from node fromi to node toi.
> Find the smallest set of vertices from which all nodes in the graph are reachable. It's guaranteed that a unique solution exists.
> Notice that you can return the vertices in any order.
> 
> **Example 1:**
> ```
> Input: n = 6, edges = [[0,1],[0,2],[2,5],[3,4],[4,2]]
> Output: [0,3]
> Explanation: It's not possible to reach all the nodes from a single vertex. From 0 we can reach [0,1,2,5]. From 3 we can reach [3,4,2,5]. So we output [0,3].
> ```
> 
> **Example 2:**
> ```
> Input: n = 5, edges = [[0,1],[2,1],[3,1],[1,4],[2,4]]
> Output: [0,2,3]
> Explanation: Notice that vertices 0, 3 and 2 are not reachable from any other node, so we must include them. Also any of these vertices can reach nodes 1 and 4.
> ```
> 
> **Constraints:**
> - 2 <= n <= 10^5
> - 1 <= edges.length <= min(10^5, n * (n - 1) / 2)
> - edges[i].length == 2
> - 0 <= fromi, toi < n
> - All pairs (fromi, toi) are distinct.

> [!info] Approach
> **Nodes with in-degree 0 — the only possible starting set.** Any node with an incoming edge is reachable from its predecessor — it doesn't need to be in the starting set. A node with in-degree 0 cannot be reached from any other node, so it must be in the starting set. The answer is exactly the set of nodes with in-degree 0. Collect all destination nodes from edges — these have in-degree ≥ 1; return all nodes not in this set.

> [!note]- Python Solution
> ```python
> def find_smallest_set_of_vertices(n, edges):
>     has_incoming = set(v for _, v in edges)
>     return [i for i in range(n) if i not in has_incoming]
> ```

> [!success] Complexity
> Time O(V+E), Space O(V).

> [!tip] Alternatives
> - In-degree array: equivalent; compute `indegree[i]`, return nodes where it's 0.
> - Note: works only for DAGs. For general directed graphs, minimum vertex cover is NP-hard.

---

## Shortest Path / Weighted

### Network Delay Time (Dijkstra's)

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
> **Dijkstra's — min-heap SSSP with stale-entry skip.** Single-source shortest path on a weighted directed graph. Non-negative weights → Dijkstra: greedily processes nodes in order of increasing tentative distance; first time a node is popped = its shortest distance. Min-heap of `(cost, node)`; dist dict; skip stale entries (`cost > dist[node]`). After Dijkstra, answer = max of all shortest distances; -1 if any node unreached.

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
>     dist = {k: 0}
>     heap = [(0, k)]
> 
>     while heap:
>         cost, node = heapq.heappop(heap)
>         if cost > dist.get(node, float('inf')):
>             continue
>         for w, nei in graph[node]:
>             new_cost = cost + w
>             if new_cost < dist.get(nei, float('inf')):
>                 dist[nei] = new_cost
>                 heapq.heappush(heap, (new_cost, nei))
> 
>     if len(dist) < n:
>         return -1
>     return max(dist.values())
> ```

> [!success] Complexity
> Time O((V+E) log V), Space O(V+E).

> [!tip] Alternatives
> - Bellman-Ford: O(V×E). Handles negative weights; overkill here.
> - Floyd-Warshall: O(V³). All-pairs; wasteful for single-source.
> - BFS: only correct if all weights equal; not applicable here.

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
> **Modified Dijkstra — minimize maximum edge weight (bottleneck path).** Minimize the maximum edge weight on any path → modified Dijkstra. `dist[r][c]` = minimum possible max-elevation to reach (r,c). Min-heap of `(max_elevation_so_far, r, c)`. Cost to reach neighbor = `max(dist[curr], grid[nr][nc])`. The first time we reach (n-1,n-1), we have the answer.

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
>         if r == n-1 and c == n-1:
>             return t
>         if t > dist[r][c]:
>             continue
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < n and 0 <= nc < n:
>                 new_t = max(t, grid[nr][nc])
>                 if new_t < dist[nr][nc]:
>                     dist[nr][nc] = new_t
>                     heapq.heappush(heap, (new_t, nr, nc))
> 
>     return dist[n-1][n-1]
> ```

> [!success] Complexity
> Time O(n² log n), Space O(n²).

> [!tip] Alternatives
> - Binary search on answer T + BFS feasibility check: O(n² log n) total. Binary search over T ∈ [0, n²-1]; for each T, BFS if path exists using only cells ≤ T.
> - Union-Find with sorted cells: sort all cells by elevation; union adjacent cells as elevation rises; stop when (0,0) and (n-1,n-1) are connected. O(n² log n).

---

### Path with Minimum Effort (LC 1631) `⚡ T1`

> [!example] Problem
> You are a hiker preparing for an upcoming hike. You are given heights, a 2D array of size rows x columns, where heights[row][col] represents the height of cell (row, col). You are situated in the top-left cell, (0, 0), and you hope to travel to the bottom-right cell, (rows-1, columns-1) (i.e., 0-indexed). You can move up, down, left, or right, and you wish to find a route that requires the minimum effort.
> A route's effort is the maximum absolute difference in heights between two consecutive cells of the route.
> Return the minimum effort required to travel from the top-left cell to the bottom-right cell.
> 
> **Example 1:**
> ```
> Input: heights = [[1,2,2],[3,8,2],[5,3,5]]
> Output: 2
> Explanation: The route of [1,3,5,3,5] has a maximum absolute difference of 2 in consecutive cells.
> This is better than the route of [1,2,2,2,5], where the maximum absolute difference is 3.
> ```
> 
> **Example 2:**
> ```
> Input: heights = [[1,2,3],[3,8,4],[5,3,5]]
> Output: 1
> Explanation: The route of [1,2,3,4,5] has a maximum absolute difference of 1 in consecutive cells, which is better than route [1,3,5,3,5].
> ```
> 
> **Example 3:**
> ```
> Input: heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
> Output: 0
> Explanation: This route does not require any effort.
> ```
> 
> **Constraints:**
> - rows == heights.length
> - columns == heights[i].length
> - 1 <= rows, columns <= 100
> - 1 <= heights[i][j] <= 10^6

> [!info] Approach
> Minimize the maximum edge weight on a path = bottleneck shortest path. Modified Dijkstra: `dist[r][c]` = minimum possible max-absolute-diff to reach (r,c); greedily process cells in order of current effort. Min-heap of `(effort, r, c)`. Transition: `new_effort = max(current_effort, abs(heights[nr][nc] - heights[r][c]))`. First pop of (rows-1, cols-1) from the heap is the answer. Mark visited on pop to avoid reprocessing.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def minimum_effort_path(heights):
>     rows, cols = len(heights), len(heights[0])
>     dist = [[float('inf')] * cols for _ in range(rows)]
>     dist[0][0] = 0
>     heap = [(0, 0, 0)]  # (effort, r, c)
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     while heap:
>         effort, r, c = heapq.heappop(heap)
>         if r == rows-1 and c == cols-1:
>             return effort
>         if effort > dist[r][c]:
>             continue
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < rows and 0 <= nc < cols:
>                 new_effort = max(effort, abs(heights[nr][nc] - heights[r][c]))
>                 if new_effort < dist[nr][nc]:
>                     dist[nr][nc] = new_effort
>                     heapq.heappush(heap, (new_effort, nr, nc))
> 
>     return dist[rows-1][cols-1]
> ```

> [!success] Complexity
> Time O(M×N log(M×N)), Space O(M×N).

> [!tip] Alternatives
> - Binary search on effort + BFS feasibility: O(M×N log(max_height)). Binary search on answer ∈ [0, 10^6]; BFS checks if path exists using only edges with diff ≤ mid.
> - Union-Find with sorted edges: sort all edges by absolute diff; union endpoints one by one; stop when (0,0) and (M-1,N-1) are connected. O(M×N log(M×N)).

### Shortest Path in a DAG

> [!example] Problem
> Given a directed acyclic graph with weighted edges, find shortest paths from a source node.

> [!info] Approach
> In a DAG, a topological order guarantees that when a node is processed, all incoming dependencies are already finalized. Topologically sort the graph, then relax outgoing edges in that order. Initialize distances, process nodes in topo order, and update `dist[v] = min(dist[v], dist[u] + w)` for each edge.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> >
> def shortest_path_dag(n, edges, int, int]], source):
>     graph = defaultdict(list)
>     indeg = [0] * n
>     for u, v, w in edges:
>         graph[u].append((v, w))
>         indeg[v] += 1
>     q = deque([i for i in range(n) if indeg[i] == 0])
>     topo = []
>     while q:
>         u = q.popleft()
>         topo.append(u)
>         for v, _ in graph[u]:
>             indeg[v] -= 1
>             if indeg[v] == 0:
>                 q.append(v)
>     dist = [float("inf")] * n
>     dist[source] = 0
>     for u in topo:
>         if dist[u] == float("inf"):
>             continue
>         for v, w in graph[u]:
>             dist[v] = min(dist[v], dist[u] + w)
>     return dist
> ```

> [!success] Complexity
> O(V + E) time, O(V + E) space.

> [!tip] Alternatives
> If the graph can have cycles, use Dijkstra for non-negative edges or Bellman-Ford when negative edges are allowed.

---

## Bipartite / Coloring

### Is Graph Bipartite? `⚡ T1`

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
> **BFS 2-coloring — alternating colors, fail on same-color neighbor.** A graph is bipartite iff it contains no odd-length cycle — equivalent to being 2-colorable. BFS/DFS assigning alternating colors (0/1); if any neighbor has the same color as the current node, not bipartite. Must handle disconnected components — run BFS/DFS from every unvisited node. Initialize all colors to -1 (uncolored). For each unvisited node, BFS assigning color 0; assign `1 - color[node]` to unvisited neighbors; return False if neighbor has same color.

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
>         queue = deque([start])
>         color[start] = 0
>         while queue:
>             node = queue.popleft()
>             for nei in graph[node]:
>                 if color[nei] == -1:
>                     color[nei] = 1 - color[node]
>                     queue.append(nei)
>                 elif color[nei] == color[node]:
>                     return False
> 
>     return True
> ```

> [!success] Complexity
> Time O(V+E), Space O(V).

> [!tip] Alternatives
> - DFS coloring: same logic recursively. O(V+E). Stack overflow risk on deep graphs.
> - Odd-cycle detection: explicitly find cycles and check parity. Equivalent, more complex.

---

### Possible Bipartition (LC 886)

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
> Equivalent to bipartite checking on an undirected graph where edges represent dislikes. 2-colorable iff no odd cycle. Build adjacency list from dislikes; BFS 2-coloring over all components (graph may be disconnected). People labeled 1..n — initialize color array of size n+1. For each uncolored node, BFS alternating colors; return False if same-color conflict found.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def possible_bipartition(n, dislikes):
>     graph = defaultdict(list)
>     for a, b in dislikes:
>         graph[a].append(b)
>         graph[b].append(a)
> 
>     color = [-1] * (n + 1)
>     for start in range(1, n + 1):
>         if color[start] != -1:
>             continue
>         color[start] = 0
>         queue = deque([start])
>         while queue:
>             node = queue.popleft()
>             for nei in graph[node]:
>                 if color[nei] == -1:
>                     color[nei] = 1 - color[node]
>                     queue.append(nei)
>                 elif color[nei] == color[node]:
>                     return False
>     return True
> ```

> [!success] Complexity
> Time O(V+E), Space O(V+E).

> [!tip] Alternatives
> - Union-Find per person: for each person u with dislike-list, union all disliked people together (they must be in the same group) and check u is not in that group. O((V+E)·α).
> - DFS 2-coloring: same logic recursively. Watch recursion depth.

---

## Advanced

### Redundant Connection `⚡ T1`

> [!example] Problem
> In this problem, a tree is an undirected graph that is connected and has no cycles.
> You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented as an array edges of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph.
> Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there are multiple answers, return the answer that occurs last in the input.
> 
> **Example 1:**
> ```
> Input: edges = [[1,2],[1,3],[2,3]]
> Output: [2,3]
> ```
> 
> **Example 2:**
> ```
> Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
> Output: [1,4]
> ```
> 
> **Constraints:**
> - n == edges.length
> - 3 <= n <= 1000
> - edges[i].length == 2
> - 1 <= ai < bi <= edges.length
> - ai != bi
> - There are no repeated edges.
> - The given graph is connected.

> [!info] Approach
> **Union-Find — first edge connecting already-connected nodes is redundant.** Adding one edge to a tree creates exactly one cycle. Process edges in order; if both endpoints share the same root (`find(u) == find(v)`), they're already connected — this edge creates a cycle and is redundant. Union by rank + path compression; return immediately on first cycle-forming edge. For each edge (a, b): if `union(a, b)` returns False (same component), return [a, b].

> [!note]- Python Solution
> ```python
> def find_redundant_connection(edges):
>     parent = list(range(len(edges) + 1))
>     rank   = [0] * (len(edges) + 1)
> 
>     def find(x):
>         while parent[x] != x:
>             parent[x] = parent[parent[x]]
>             x = parent[x]
>         return x
> 
>     def union(a, b):
>         ra, rb = find(a), find(b)
>         if ra == rb:
>             return False
>         if rank[ra] < rank[rb]:
>             ra, rb = rb, ra
>         parent[rb] = ra
>         if rank[ra] == rank[rb]:
>             rank[ra] += 1
>         return True
> 
>     for a, b in edges:
>         if not union(a, b):
>             return [a, b]
>     return []
> ```

> [!success] Complexity
> Time O(N·α(N)) ≈ O(N), Space O(N).

> [!tip] Alternatives
> - DFS cycle detection: for each edge, DFS to check if path already exists between endpoints. O(N²) — inefficient.
> - Note: Union-Find only correct here because the graph is undirected. For directed graphs, DFS back-edge detection or Kahn's is required.

---

### Minimum Spanning Tree (Kruskal's)

> [!example] Problem
> Given a connected undirected weighted graph, find the minimum spanning tree — a subset of edges that connects all nodes with minimum total weight and no cycles.

> [!info] Approach
> **Kruskal's — sort edges by weight, greedily add if no cycle. `⚡ T1`** The cut property — the minimum weight edge crossing any cut belongs to some MST. Kruskal's: sort all edges by weight and greedily add each edge if it doesn't form a cycle. Union-Find for O(α) cycle detection per edge (vs O(V) DFS cycle check). Sort edges by weight; for each edge, union its endpoints if they're in different components; stop after adding V-1 edges.

> [!note]- Python Solution
> ```python
> def kruskal(n, edges):
>     # edges: list of (weight, u, v)
>     parent = list(range(n))
>     rank   = [0] * n
> 
>     def find(x):
>         while parent[x] != x:
>             parent[x] = parent[parent[x]]
>             x = parent[x]
>         return x
> 
>     def union(a, b):
>         ra, rb = find(a), find(b)
>         if ra == rb:
>             return False
>         if rank[ra] < rank[rb]:
>             ra, rb = rb, ra
>         parent[rb] = ra
>         if rank[ra] == rank[rb]:
>             rank[ra] += 1
>         return True
> 
>     edges.sort()
>     mst_cost = 0
>     mst_edges = []
>     for w, u, v in edges:
>         if union(u, v):
>             mst_cost += w
>             mst_edges.append((u, v, w))
>             if len(mst_edges) == n - 1:
>                 break  # MST complete
> 
>     return mst_cost, mst_edges
> ```

> [!success] Complexity
> Time O(E log E) dominated by sort. Space O(V).

> [!tip] Alternatives
> - Prim's: grow MST from a seed node using a min-heap; O((V+E) log V). Better for dense graphs (E close to V²).
> - Borůvka's: O(E log V); each round adds the minimum outgoing edge for each component — parallelizable.

---

### Longest Path in a DAG `⚡ T1`

> [!example] Problem
> Find the length of the longest path in a directed acyclic graph (in terms of number of edges).

> [!info] Approach
> **Kahn's topo sort + DP — relax dp[v] = max(dp[u] + 1).** Only works on DAGs — cycles make the longest path undefined (infinite). Topological sort + DP: process nodes in topological order; `dp[node] = max(dp[predecessor] + 1)` for all incoming edges — no subproblem is accessed before it's solved. Kahn's to get topo order, then one DP pass. `dp[node] = max(dp[node], dp[prev] + 1)` as edges are relaxed during Kahn's.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def longest_path_dag(n, edges):
>     # edges: list of (u, v), directed u → v
>     graph   = [[] for _ in range(n)]
>     indegree = [0] * n
>     for u, v in edges:
>         graph[u].append(v)
>         indegree[v] += 1
> 
>     queue = deque(i for i in range(n) if indegree[i] == 0)
>     dp = [0] * n  # dp[node] = longest path ending at node
> 
>     while queue:
>         u = queue.popleft()
>         for v in graph[u]:
>             dp[v] = max(dp[v], dp[u] + 1)
>             indegree[v] -= 1
>             if indegree[v] == 0:
>                 queue.append(v)
> 
>     return max(dp)
> ```

> [!success] Complexity
> Time O(V+E), Space O(V).

> [!tip] Alternatives
> - DFS with memo dict on node — top-down. O(V+E). Same idea, you just say the cache out loud.
> - Bellman-Ford with negated weights: O(VE) — much slower; use only when you can't confirm DAG property.

---

### Reconstruct Itinerary (LC 332)

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
> Eulerian path problem on a directed multigraph — visit every edge exactly once. Hierholzer's algorithm finds an Eulerian path in O(E log E): greedily follow edges; when stuck (no outgoing edges left), backtrack and prepend the current node. Build adjacency list with sorted neighbors (for lexicographic order) using a min-heap or sorted list. DFS: always pick the smallest neighbor; when a node has no more outgoing edges, prepend to result. Use a stack-based iterative post-order DFS: push node to result when its adjacency list is exhausted; reverse at the end.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def find_itinerary(tickets):
>     graph = defaultdict(list)
>     for src, dst in sorted(tickets, reverse=True):
>         graph[src].append(dst)
>     # sorted(reverse=True) so that pop() gives smallest destination
> 
>     result = []
>     stack = ["JFK"]
>     while stack:
>         while graph[stack[-1]]:
>             stack.append(graph[stack[-1]].pop())
>         result.append(stack.pop())
>     return result[::-1]
> ```

> [!success] Complexity
> Time O(E log E) for sorting. Space O(V+E).

> [!tip] Alternatives
> - Recursive Hierholzer: same logic with the call stack as the DFS stack; risks Python recursion limit with many tickets.
> - Priority queue (min-heap) per node: `heapq` ensures lexicographic order without pre-sorting all tickets. Same O(E log E).

---

### Critical Connections / Bridges (LC 1192) `💤 T3`

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
> Bridge detection requires Tarjan's algorithm. A bridge is an edge (u, v) where no back-edge from v's subtree reaches u or any ancestor of u — detected via `low[v] > disc[u]`. DFS with two arrays: `disc[u]` = discovery time, `low[u]` = lowest discovery time reachable from u's subtree (via back edges). If `low[v] > disc[u]`, edge (u,v) is a bridge. Track parent to avoid treating the tree edge back to parent as a back-edge. Update `low[u] = min(low[u], low[v])` after recursing into v; `low[u] = min(low[u], disc[v])` for back-edges.

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
>     low  = [-1] * n
>     result = []
>     timer = [0]
> 
>     def dfs(node, parent):
>         disc[node] = low[node] = timer[0]
>         timer[0] += 1
>         for nei in graph[node]:
>             if nei == parent:
>                 continue
>             if disc[nei] == -1:
>                 dfs(nei, node)
>                 low[node] = min(low[node], low[nei])
>                 if low[nei] > disc[node]:
>                     result.append([node, nei])
>             else:
>                 low[node] = min(low[node], disc[nei])
> 
>     for node in range(n):
>         if disc[node] == -1:
>             dfs(node, -1)
>     return result
> ```

> [!success] Complexity
> Time O(V+E), Space O(V+E).

> [!tip] Alternatives
> - Naive: remove each edge and run DFS to check connectivity. O(E × (V+E)) — too slow for large graphs.
> - Articulation points (Tarjan variant): `low[v] >= disc[u]` (note: >=, not >) detects articulation points (nodes) rather than bridges (edges).
> - Handle parallel edges: if multiple edges between u and v exist, none is a bridge; track edge index rather than parent node to handle multigraphs.

---

### Minimum Height Trees (LC 310)

> [!example] Problem
> A tree is an undirected graph in which any two vertices are connected by exactly one path. In other words, any connected graph without simple cycles is a tree.
> Given a tree of n nodes labelled from 0 to n - 1, and an array of n - 1 edges where edges[i] = [ai, bi] indicates that there is an undirected edge between the two nodes ai and bi in the tree, you can choose any node of the tree as the root. When you select a node x as the root, the result tree has height h. Among all possible rooted trees, those with minimum height (i.e. min(h))  are called minimum height trees (MHTs).
> Return a list of all MHTs' root labels. You can return the answer in any order.
> The height of a rooted tree is the number of edges on the longest downward path between the root and a leaf.
> 
> **Example 1:**
> ```
> Input: n = 4, edges = [[1,0],[1,2],[1,3]]
> Output: [1]
> Explanation: As shown, the height of the tree is 1 when the root is the node with label 1 which is the only MHT.
> ```
> 
> **Example 2:**
> ```
> Input: n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
> Output: [3,4]
> ```
> 
> **Constraints:**
> - 1 <= n <= 2 * 10^4
> - edges.length == n - 1
> - 0 <= ai, bi < n
> - ai != bi
> - All the pairs (ai, bi) are distinct.
> - The given input is guaranteed to be a tree and there will be no repeated edges.

> [!info] Approach
> The roots of minimum height trees are the "center" nodes of the tree — at most 2 nodes lying on the longest path (diameter). Topological leaf-trimming: iteratively remove all current leaves; the last 1–2 remaining nodes are the answer. Build adjacency list and degree array. Seed a queue with all leaves (degree == 1). BFS layer-by-layer: remove current leaves, expose new leaves (nodes whose degree drops to 1). Stop when ≤ 2 nodes remain. Decrement `n` by the number of leaves removed each round; stop when `n <= 2` — remaining nodes are the answer.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def find_min_height_trees(n, edges):
>     if n == 1:
>         return [0]
>     graph = [set() for _ in range(n)]
>     for u, v in edges:
>         graph[u].add(v)
>         graph[v].add(u)
> 
>     leaves = deque(i for i in range(n) if len(graph[i]) == 1)
>     remaining = n
> 
>     while remaining > 2:
>         leaf_count = len(leaves)
>         remaining -= leaf_count
>         for _ in range(leaf_count):
>             leaf = leaves.popleft()
>             for nei in graph[leaf]:
>                 graph[nei].discard(leaf)
>                 if len(graph[nei]) == 1:
>                     leaves.append(nei)
> 
>     return list(leaves)
> ```

> [!success] Complexity
> Time O(V), Space O(V).

> [!tip] Alternatives
> - Two BFS to find diameter endpoints: find the farthest node from any node (BFS 1), then farthest from that node (BFS 2) — diameter endpoints found. Center of diameter path = answer. O(V) but more complex to implement.
> - DFS with height computation: O(V) per root × O(V) roots = O(V²) — far too slow.

---

## Advanced Graph Algorithms

### Strongly Connected Components — Kosaraju's Algorithm `💤 T3`

> [!example] Problem
> Find all strongly connected components (SCCs) in a directed graph. An SCC is a maximal set of nodes where every node is reachable from every other node.

> [!info] Approach
> Kosaraju's runs two DFS passes. The first pass computes finish-order (equivalent to reverse topological order). The second pass on the reversed graph extracts SCCs in that finish order. Pass 1 — DFS on original graph, push nodes to a stack in finish order. Pass 2 — pop from the stack, DFS on the transposed graph; each DFS tree in pass 2 is one SCC. Build adjacency list and its transpose. DFS on original, recording finish order in a stack. Then repeatedly pop from the stack and DFS on the transposed graph — all reachable unvisited nodes form one SCC.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def kosaraju(n, edges, int]]):
>     graph = defaultdict(list)
>     rev_graph = defaultdict(list)
>     for u, v in edges:
>         graph[u].append(v)
>         rev_graph[v].append(u)
> >
>     visited = [False] * n
>     finish_order = []
> >
>     def dfs1(node):
>         visited[node] = True
>         for neighbour in graph[node]:
>             if not visited[neighbour]:
>                 dfs1(neighbour)
>         finish_order.append(node)
> >
>     for i in range(n):
>         if not visited[i]:
>             dfs1(i)
> >
>     visited = [False] * n
>     sccs = []
> >
>     def dfs2(node, component):
>         visited[node] = True
>         component.append(node)
>         for neighbour in rev_graph[node]:
>             if not visited[neighbour]:
>                 dfs2(neighbour, component)
> >
>     while finish_order:
>         node = finish_order.pop()
>         if not visited[node]:
>             component = []
>             dfs2(node, component)
>             sccs.append(component)
>     return sccs
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> - Tarjan's algorithm: single DFS pass using low-link values and a stack. Also O(V + E) but more complex to implement. Preferred when low-link values are needed for other purposes (bridges, articulation points).
> - Key insight: reversing the graph "flips" the SCC connectivity — nodes reachable in the reverse graph from a root belong to the same SCC.

---

### Minimum Spanning Tree — Prim's Algorithm

> [!example] Problem
> Given a weighted undirected connected graph, find the minimum spanning tree (MST) — the subset of edges that connects all vertices with minimum total weight.

> [!info] Approach
> Prim's grows the MST greedily from any starting node, always adding the cheapest edge that connects the current MST to an unvisited node. A min-heap makes this O(E log V). Use a min-heap of `(weight, node)`. Start with node 0. Greedily pick the smallest weight edge to an unvisited node, add it to the MST, and push all its edges into the heap. `visited` set tracks MST nodes. Pop from heap; if already visited, skip. Otherwise mark visited, add weight to MST cost, push all unvisited neighbours into the heap.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> >
> def prim_mst(n, edges, int, int]]):
>     graph = defaultdict(list)
>     for u, v, w in edges:
>         graph[u].append((w, v))
>         graph[v].append((w, u))
>     visited = set()
>     heap = [(0, 0)]   # (weight, node)
>     total_weight = 0
>     while heap and len(visited) < n:
>         weight, node = heapq.heappop(heap)
>         if node in visited:
>             continue
>         visited.add(node)
>         total_weight += weight
>         for edge_weight, neighbour in graph[node]:
>             if neighbour not in visited:
>                 heapq.heappush(heap, (edge_weight, neighbour))
>     return total_weight if len(visited) == n else -1
> ```

> [!success] Complexity
> Time O(E log V), Space O(V + E).

> [!tip] Alternatives
> - Kruskal's: sort all edges, use Union-Find to pick the smallest edge that doesn't create a cycle. O(E log E). Better for sparse graphs; Prim's is better for dense graphs.
> - Key difference: Prim's grows from a single root; Kruskal's builds components that merge.

---

### All-Pairs Shortest Path — Floyd-Warshall

> [!example] Problem
> Given a weighted directed graph with `n` nodes (possibly with negative edges, but no negative cycles), find the shortest path between every pair of nodes.

> [!info] Approach
> Dijkstra's is per-source (O(V * E log V) total for all-pairs). Floyd-Warshall's DP is simpler to implement and handles negative edges. For dense graphs it's competitive. `dist[i][j]` = shortest path from `i` to `j`. For each intermediate node `k`, check if routing through `k` shortens `dist[i][j]`. Initialize `dist[i][j]` to edge weight if edge exists, 0 if `i == j`, infinity otherwise. Triple loop: for each `k`, for each `i`, for each `j`: `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.

> [!note]- Python Solution
> ```python
> def floyd_warshall(n, edges, int, int]]):
>     INF = float('inf')
>     dist = [[INF] * n for _ in range(n)]
>     for i in range(n):
>         dist[i][i] = 0
>     for u, v, w in edges:
>         dist[u][v] = w
>     for k in range(n):
>         for i in range(n):
>             for j in range(n):
>                 if dist[i][k] + dist[k][j] < dist[i][j]:
>                     dist[i][j] = dist[i][k] + dist[k][j]
>     return dist
> ```

> [!success] Complexity
> Time O(V³), Space O(V²).

> [!tip] Alternatives
> - Run Dijkstra from every source: O(V * E log V) — better for sparse graphs with non-negative edges.
> - Bellman-Ford from every source: O(V² * E) — handles negative edges but much slower.
> - Floyd-Warshall is the go-to when the graph is dense or the input is given as an adjacency matrix.

---

## See Also

[[union-find]] | [[binary-search]] | [[dynamic-programming]] | [[sorting]]
