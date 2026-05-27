---
tags: [coding, data-structures, graph]
topic: graph
difficulty: mixed
---

# Graph Problems — Deep Dive

**Pattern map**: Graph problems collapse into five patterns — BFS (shortest path, multi-source spread), DFS (connectivity, flood fill, cycle detection), Topological Sort (dependency ordering on DAGs), Shortest Path / Weighted (Dijkstra, modified BFS), Bipartite coloring, and Advanced (Union-Find / MST / DAG DP). Pick BFS when you need minimum steps; DFS when you need reachability or ordering; Union-Find when you need dynamic connectivity with no full traversal needed.

---

## BFS on Graphs

### Rotting Oranges

> [!example] Problem
> A grid contains 0 (empty), 1 (fresh), 2 (rotten). Each minute, fresh oranges 4-adjacent to rotten become rotten. Return minimum minutes to rot all oranges, -1 if impossible.

> [!info] Approach
> **Multi-source BFS — simultaneous spread from all rotten sources.**
> WHY: Rotting spreads simultaneously from all rotten sources. BFS levels naturally correspond to time steps; the first time a fresh orange is reached gives the minimum time to rot it.
> WHAT: Seed queue with all initially rotten oranges at time 0, count fresh oranges. BFS level-by-level; each time a fresh orange is rotted, decrement fresh counter; track max time seen.
> HOW: Multi-source start avoids O(R × M×N) repeated BFS. Return max_time if fresh == 0, else -1.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def orangesRotting(grid):
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

### Word Ladder

> [!example] Problem
> Find the length of the shortest transformation sequence from `beginWord` to `endWord`, changing one letter at a time; each intermediate word must be in `wordList`. Return 0 if no path.

> [!info] Approach
> **BFS on implicit word graph — L×26 mutation enumeration.**
> WHY: Shortest path in an implicit unweighted graph → BFS. Don't build the graph explicitly (O(N²) pairs); generate all L×26 single-character mutations of the current word and check against the word set — O(L×26) per word instead of O(N×L) pairwise comparison.
> WHAT: BFS from `beginWord`; remove words from the set as visited to prevent revisits.
> HOW: For each word dequeued, try all single-char mutations; if mutation == endWord, return. Otherwise enqueue if in word set and unvisited.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def ladderLength(beginWord, endWord, wordList):
>     word_set = set(wordList)
>     if endWord not in word_set:
>         return 0
> 
>     queue = deque([(beginWord, 1)])
>     visited = {beginWord}
> 
>     while queue:
>         word, length = queue.popleft()
>         for i in range(len(word)):
>             for c in 'abcdefghijklmnopqrstuvwxyz':
>                 next_word = word[:i] + c + word[i+1:]
>                 if next_word == endWord:
>                     return length + 1
>                 if next_word in word_set and next_word not in visited:
>                     visited.add(next_word)
>                     queue.append((next_word, length + 1))
> 
>     return 0
> ```

> [!success] Complexity
> Time O(M²×N) where M = word length, N = wordList size. Space O(M²×N).

> [!tip] Alternatives
> - Bidirectional BFS: expand from both `beginWord` and `endWord` simultaneously; reduces explored nodes from O(b^d) to O(b^(d/2)). Follow-up standard.
> - Preprocessed adjacency via patterns: build `"h*t" → [hot, hit]` map; O(M×N) preprocessing, then O(M²×N) BFS — same asymptotic but faster in practice.

---

### Shortest Path in Binary Matrix

> [!example] Problem
> Given an n×n binary matrix, find the shortest clear path from top-left (0,0) to bottom-right (n-1,n-1). A clear path uses only 0-cells, 8-directionally. Return -1 if no path. Path length = number of cells visited.

> [!info] Approach
> **BFS from (0,0) — 8-directional, mark on enqueue.**
> WHY: Shortest path in unweighted grid → BFS. 8-directional: diagonals allowed.
> WHAT: BFS from (0,0) if grid[0][0] == 0; track distance.
> HOW: Mark cells visited by setting to 1 as you enqueue (not after dequeue) to prevent duplicate enqueueing; return distance when (n-1, n-1) is dequeued.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def shortestPathBinaryMatrix(grid):
>     n = len(grid)
>     if grid[0][0] == 1 or grid[n-1][n-1] == 1:
>         return -1
> 
>     dirs = [(dr,dc) for dr in [-1,0,1] for dc in [-1,0,1] if (dr,dc) != (0,0)]
>     queue = deque([(0, 0, 1)])
>     grid[0][0] = 1  # mark visited
> 
>     while queue:
>         r, c, dist = queue.popleft()
>         if r == n-1 and c == n-1:
>             return dist
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
>                 grid[nr][nc] = 1
>                 queue.append((nr, nc, dist + 1))
> 
>     return -1
> ```

> [!success] Complexity
> Time O(n²), Space O(n²).

> [!tip] Alternatives
> - A* with Chebyshev distance heuristic: faster in practice for large grids with clear paths.
> - DFS: finds a path but not necessarily the shortest.

---

### Minimum Knight Moves

> [!example] Problem
> Find the minimum number of knight moves to reach (x, y) from (0, 0) on an infinite chessboard.

> [!info] Approach
> **BFS with symmetry reduction to first quadrant.**
> WHY: Shortest path in an implicit unweighted graph → BFS. Knight moves are symmetric across axes, so work in the first quadrant `(|x|, |y|)`, reducing the search space.
> WHAT: BFS from (0, 0); 8 knight move offsets.
> HOW: Use a `visited` set; use abs values to exploit symmetry; allow coordinates down to -2 (buffer for (0,0)/(1,1) edge cases).

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def minKnightMoves(x, y):
>     x, y = abs(x), abs(y)  # symmetry
>     MOVES = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
>     queue = deque([(0, 0, 0)])
>     visited = {(0, 0)}
> 
>     while queue:
>         cx, cy, moves = queue.popleft()
>         if cx == x and cy == y:
>             return moves
>         for dx, dy in MOVES:
>             nx, ny = cx+dx, cy+dy
>             if (nx, ny) not in visited and nx >= -2 and ny >= -2:
>                 visited.add((nx, ny))
>                 queue.append((nx, ny, moves + 1))
> 
>     return -1
> ```

> [!success] Complexity
> Time O(max(|x|,|y|)²), Space O(max(|x|,|y|)²).

> [!tip] Alternatives
> - Bidirectional BFS: meet in the middle; reduces to O(sqrt(|x|²+|y|²)) frontier in practice.
> - Mathematical formula: O(1) closed-form solution exists for knight distance, but BFS is expected in interviews.

---

### Employee Importance

> [!example] Problem
> Given employees (id, importance, subordinates list) and a target id, return total importance of that employee and all their subordinates recursively.

> [!info] Approach
> **Hash map + BFS over subordinate ids.**
> WHY: Tree/DAG reachability with value aggregation. Hash map first: direct subordinate ids require O(N) linear scan per lookup without a map; O(1) with a map.
> WHAT: BFS/DFS from target employee id, sum importance values.
> HOW: Build `{id: employee}` map; BFS — dequeue id, add importance, enqueue all subordinate ids.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def getImportance(employees, id):
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

### Find if Path Exists in a Graph

> [!example] Problem
> Given n nodes, a list of bidirectional edges, source and destination, determine if a valid path exists.

> [!info] Approach
> **Union-Find — reachability in O(E α(N)).**
> WHY: Union-Find answers "are they connected?" in near O(1) per query after O(E) union operations — no traversal needed.
> WHAT: Union all edges; check if `find(source) == find(destination)`.
> HOW: Path compression + union by rank for optimal performance.

> [!note]- Python Solution
> ```python
> def validPath(n, edges, source, destination):
>     parent = list(range(n))
> 
>     def find(x):
>         while parent[x] != x:
>             parent[x] = parent[parent[x]]  # path compression
>             x = parent[x]
>         return x
> 
>     def union(a, b):
>         parent[find(a)] = find(b)
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
> A star graph has one center connected to all other nodes. Given the edge list, find the center.

> [!info] Approach
> **O(1) — center appears in both the first and second edges.**
> WHY: The center appears in every edge. The center is the only node common to both the first and second edges — no traversal needed.
> WHAT: Find the intersection of `edges[0]` and `edges[1]`.
> HOW: Check if `edges[0][0]` is in `edges[1]`; if so, it's the center; otherwise `edges[0][1]` is the center.

> [!note]- Python Solution
> ```python
> def findCenter(edges):
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

### Number of Islands

> [!example] Problem
> Given a 2D grid of '1' (land) and '0' (water), count the number of islands (connected components of land, 4-directional).

> [!info] Approach
> **DFS sinking — flood-fill each component, count triggers.**
> WHY: Each island is a connected component of '1' cells. DFS marks all cells in a component as visited in one pass.
> WHAT: Iterate every cell; when a '1' is found, DFS to sink all connected land (set to '0'), increment count.
> HOW: Sinking avoids a separate visited array — the mutation is the visit mark. Increment count only on the initial call, not within DFS.

> [!note]- Python Solution
> ```python
> def numIslands(grid):
>     if not grid:
>         return 0
>     rows, cols = len(grid), len(grid[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
>             return
>         grid[r][c] = '0'
>         dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)
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

### Flood Fill

> [!example] Problem
> Given an image, starting pixel (sr, sc), and new color, recolor the starting pixel and all 4-directionally connected pixels of the same original color.

> [!info] Approach
> **DFS recolor — guard against same-color infinite loop.**
> WHY: Connected-component traversal. Early return if original == new color: recursion would infinitely revisit cells (no termination condition).
> WHAT: DFS from (sr, sc); recolor cells matching the original color.
> HOW: Guard with `if original == color: return image` before DFS.

> [!note]- Python Solution
> ```python
> def floodFill(image, sr, sc, color):
>     original = image[sr][sc]
>     if original == color:
>         return image
>     rows, cols = len(image), len(image[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or image[r][c] != original:
>             return
>         image[r][c] = color
>         dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)
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

### Max Area of Island

> [!example] Problem
> Given a binary 2D grid (0=water, 1=land), return the maximum area of any island (connected 1s, 4-directional). Return 0 if no island.

> [!info] Approach
> **DFS returning component size — sink inline.**
> WHY: Variation on Number of Islands where we need the maximum component size. DFS function returns the count of cells in the component instead of just marking.
> WHAT: `1 + sum of returns from 4 neighbors`. Sink cells inline; DFS returns 0 for non-land or out-of-bounds.
> HOW: `max(dfs(r,c) for all r,c)` — zero-cost for water cells.

> [!note]- Python Solution
> ```python
> def maxAreaOfIsland(grid):
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

### Surrounded Regions

> [!example] Problem
> Given an m×n board of 'X' and 'O', flip all 'O' regions completely surrounded by 'X' to 'X'. 'O's connected to the border are never flipped.

> [!info] Approach
> **Reverse DFS — mark border-safe 'O's, then flip interior.**
> WHY: Directly checking if an 'O' region is surrounded requires backtracking to undo if DFS touches a border. Instead: find all border-connected 'O's first (safe cells), then flip everything else.
> WHAT: DFS from every border 'O', mark safe cells with sentinel 'S'. Then: interior 'O' → 'X', 'S' → 'O'.
> HOW: Walk all 4 borders, DFS from each 'O' found there.

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
>         dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)
> 
>     for r in range(rows):
>         dfs(r, 0); dfs(r, cols-1)
>     for c in range(cols):
>         dfs(0, c); dfs(rows-1, c)
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

### Pacific Atlantic Water Flow

> [!example] Problem
> Given an m×n height matrix, water flows to 4-adjacent cells of equal or lesser height. Find all cells from which water can reach both the Pacific (top/left border) and Atlantic (bottom/right border) oceans.

> [!info] Approach
> **Reverse BFS from both ocean borders — intersect reachable sets.**
> WHY: Checking forward from each cell whether it reaches both oceans requires O(M²N²) DFS calls. Reverse: "which cells can be reached from the ocean borders?" — water flows uphill in reverse.
> WHAT: BFS from all Pacific border cells (mark reachable); BFS from all Atlantic border cells; intersect.
> HOW: Reverse BFS condition — expand to neighbors with height >= current height (uphill in the reverse direction).

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def pacificAtlantic(heights):
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

### All Paths From Source to Target

> [!example] Problem
> Given a DAG (0 to n-1), find and return all paths from node 0 to node n-1.

> [!info] Approach
> **DFS backtracking on DAG — no visited set needed.**
> WHY: It's a DAG — no cycles, so DFS can never revisit a node on the current path. No visited set needed.
> WHAT: DFS with backtracking — enumerate all paths. When node n-1 is reached, record a copy of the current path.
> HOW: `path.append(nei)`, recurse, `path.pop()`.

> [!note]- Python Solution
> ```python
> def allPathsSourceTarget(graph):
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

### Clone Graph

> [!example] Problem
> Given a reference to a node in an undirected connected graph, return a deep copy.

> [!info] Approach
> **DFS with original→clone map — register before recursing.**
> WHY: Without pre-registration, revisiting a node (via a cycle) creates a new clone instead of returning the existing one — producing duplicates and infinite loops.
> WHAT: `{original: clone}` map as memo; DFS from start. Create clone, register in map, then recurse to clone neighbors.
> HOW: Guard `if n in visited: return visited[n]` handles cycles. Register BEFORE recursing into neighbors.

> [!note]- Python Solution
> ```python
> def cloneGraph(node):
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

### Find Eventual Safe States

> [!example] Problem
> In a directed graph, a node is "safe" if every path from it eventually terminates (no cycle reachable). Return all safe nodes sorted.

> [!info] Approach
> **Three-color DFS — 0=unvisited, 1=in-progress, 2=safe.**
> WHY: Need to distinguish "currently being explored" (on the DFS path, could be on a cycle) from "confirmed safe" (all paths from it terminate).
> WHAT: 0 = unvisited, 1 = in-progress (gray), 2 = confirmed safe (black). DFS reaching a gray node → cycle → current path is unsafe.
> HOW: Mark gray before recursing neighbors; mark black after all neighbors are confirmed safe.

> [!note]- Python Solution
> ```python
> def eventualSafeNodes(graph):
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

### Course Schedule

> [!example] Problem
> Given `numCourses` and prerequisites `[a, b]` (must take b before a), determine if all courses can be finished (i.e., no circular dependency).

> [!info] Approach
> **Kahn's BFS topo sort — cycle detection via leftover nodes.**
> WHY: A valid course ordering exists iff the dependency graph is a DAG (no directed cycles). Kahn's naturally detects cycles — if all nodes are processed, no cycle; if some remain with nonzero in-degree, they're in a cycle.
> WHAT: Build adjacency list and in-degree array; seed queue with all in-degree-0 nodes; process, decrement neighbors' in-degrees; if neighbor reaches 0, enqueue it.
> HOW: If `completed == numCourses`, no cycle.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def canFinish(numCourses, prerequisites):
>     graph = [[] for _ in range(numCourses)]
>     indegree = [0] * numCourses
>     for a, b in prerequisites:
>         graph[b].append(a)
>         indegree[a] += 1
> 
>     queue = deque(c for c in range(numCourses) if indegree[c] == 0)
>     completed = 0
>     while queue:
>         node = queue.popleft()
>         completed += 1
>         for nei in graph[node]:
>             indegree[nei] -= 1
>             if indegree[nei] == 0:
>                 queue.append(nei)
> 
>     return completed == numCourses
> ```

> [!success] Complexity
> Time O(V+E), Space O(V+E).

> [!tip] Alternatives
> - DFS cycle detection: gray/black coloring; back edge to gray node = cycle. O(V+E)/O(V). Use when you need cycle info per node, not just overall.
> - Union-Find: only for undirected graphs — does not detect directed cycles.

---

### Course Schedule II

> [!example] Problem
> Same as Course Schedule but return one valid ordering, or [] if impossible.

> [!info] Approach
> **Kahn's topo sort — collect removal order.**
> WHY: Kahn's algorithm naturally produces a topological order — the BFS order of removal. Same algorithm as Course Schedule; collect nodes as they're removed.
> WHAT: If `len(order) == numCourses`, it's valid; otherwise a cycle was detected.
> HOW: Append node to `order` as it's dequeued; return order or [].

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def findOrder(numCourses, prerequisites):
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

### Alien Dictionary

> [!example] Problem
> Given a sorted list of words in an alien language, derive a valid character ordering or return "" if contradictory.

> [!info] Approach
> **Edge extraction from adjacent word pairs + Kahn's topo sort.**
> WHY: The sorted order gives exactly the first differing character between adjacent words — that encodes a directed edge (char_a → char_b). Kahn's topo sort produces the character order; a cycle means the ordering is contradictory.
> WHAT: Compare each adjacent word pair, find first differing char, add directed edge. Then Kahn's BFS.
> HOW: Invalid input detection — if word A is a prefix of word B but A appears after B (e.g., "abc" before "ab"), return "" immediately.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def alienOrder(words):
>     graph = {c: [] for w in words for c in w}
>     indegree = {c: 0 for c in graph}
> 
>     for i in range(len(words) - 1):
>         w1, w2 = words[i], words[i+1]
>         min_len = min(len(w1), len(w2))
>         if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
>             return ""  # invalid: longer word before its prefix
>         for j in range(min_len):
>             if w1[j] != w2[j]:
>                 graph[w1[j]].append(w2[j])
>                 indegree[w2[j]] += 1
>                 break
> 
>     queue = deque(c for c in indegree if indegree[c] == 0)
>     result = []
>     while queue:
>         c = queue.popleft()
>         result.append(c)
>         for nei in graph[c]:
>             indegree[nei] -= 1
>             if indegree[nei] == 0:
>                 queue.append(nei)
> 
>     return "".join(result) if len(result) == len(graph) else ""
> ```

> [!success] Complexity
> Time O(C) where C = total characters. Space O(1) — alphabet ≤ 26 chars.

> [!tip] Alternatives
> - DFS post-order topo sort: cycle detection via gray/black; append in reverse post-order. Same complexity.
> - Watch for duplicate edges: same char pair from multiple word comparisons — deduplicate in adjacency list.

---

### Minimum Number of Vertices to Reach All Nodes

> [!example] Problem
> Given a DAG with n nodes, find the minimum set of vertices from which all nodes are reachable.

> [!info] Approach
> **Nodes with in-degree 0 — the only possible starting set.**
> WHY: Any node with an incoming edge is reachable from its predecessor — it doesn't need to be in the starting set. A node with in-degree 0 cannot be reached from any other node, so it must be in the starting set.
> WHAT: The answer is exactly the set of nodes with in-degree 0.
> HOW: Collect all destination nodes from edges — these have in-degree ≥ 1; return all nodes not in this set.

> [!note]- Python Solution
> ```python
> def findSmallestSetOfVertices(n, edges):
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
> Given n nodes, directed weighted edges `[u, v, w]`, and source `k`, find the time for all nodes to receive a signal from k. Return -1 if any node is unreachable.

> [!info] Approach
> **Dijkstra's — min-heap SSSP with stale-entry skip.**
> WHY: Single-source shortest path on a weighted directed graph. Non-negative weights → Dijkstra: greedily processes nodes in order of increasing tentative distance; first time a node is popped = its shortest distance.
> WHAT: Min-heap of `(cost, node)`; dist dict; skip stale entries (`cost > dist[node]`).
> HOW: After Dijkstra, answer = max of all shortest distances; -1 if any node unreached.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> 
> def networkDelayTime(times, n, k):
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
> Given an n×n grid where `grid[i][j]` is the elevation, find the minimum time T such that there exists a path from (0,0) to (n-1,n-1) where all cells on the path have elevation ≤ T.

> [!info] Approach
> **Modified Dijkstra — minimize maximum edge weight (bottleneck path).**
> WHY: Minimize the maximum edge weight on any path → modified Dijkstra. `dist[r][c]` = minimum possible max-elevation to reach (r,c).
> WHAT: Min-heap of `(max_elevation_so_far, r, c)`. Cost to reach neighbor = `max(dist[curr], grid[nr][nc])`.
> HOW: The first time we reach (n-1,n-1), we have the answer.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def swimInWater(grid):
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

### Cheapest Flights Within K Stops

> [!example] Problem
> Given n cities, directed weighted flights, source `src`, destination `dst`, and max `k` stops, find the cheapest price. Return -1 if impossible.

> [!info] Approach
> **Bellman-Ford with k+1 rounds — copy dist array each round.**
> WHY: Shortest path with a constraint on the number of hops → Bellman-Ford with k+1 relaxation rounds. Standard Dijkstra can't bound hops.
> WHAT: After i rounds of relaxation, `dist[v]` = cheapest path using at most i edges. Need at most k stops = k+1 edges.
> HOW: Copy dist array each round to prevent using edges discovered in the same round (would allow more than 1 edge per round effectively).

> [!note]- Python Solution
> ```python
> def findCheapestPrice(n, flights, src, dst, k):
>     dist = [float('inf')] * n
>     dist[src] = 0
> 
>     for _ in range(k + 1):
>         temp = dist[:]
>         for u, v, w in flights:
>             if dist[u] != float('inf') and dist[u] + w < temp[v]:
>                 temp[v] = dist[u] + w
>         dist = temp
> 
>     return dist[dst] if dist[dst] != float('inf') else -1
> ```

> [!success] Complexity
> Time O(k × E), Space O(V).

> [!tip] Alternatives
> - Dijkstra with state `(cost, node, stops_remaining)`: requires visited set on `(node, stops)` pairs. O(E log(V×K)).
> - BFS level-by-level (k+1 levels): each level = one hop. O(k × E). Equivalent to Bellman-Ford.

---

## Bipartite / Coloring

### Is Graph Bipartite?

> [!example] Problem
> Given an undirected graph, determine if it can be split into two sets such that every edge connects nodes from different sets (2-colorable).

> [!info] Approach
> **BFS 2-coloring — alternating colors, fail on same-color neighbor.**
> WHY: A graph is bipartite iff it contains no odd-length cycle — equivalent to being 2-colorable. BFS/DFS assigning alternating colors (0/1); if any neighbor has the same color as the current node, not bipartite.
> WHAT: Must handle disconnected components — run BFS/DFS from every unvisited node.
> HOW: Initialize all colors to -1 (uncolored). For each unvisited node, BFS assigning color 0; assign `1 - color[node]` to unvisited neighbors; return False if neighbor has same color.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def isBipartite(graph):
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

## Advanced

### Redundant Connection

> [!example] Problem
> Given a tree of n nodes with one extra edge added (creating exactly one cycle), find the redundant edge. If multiple valid answers, return the last one in the input.

> [!info] Approach
> **Union-Find — first edge connecting already-connected nodes is redundant.**
> WHY: Adding one edge to a tree creates exactly one cycle. Process edges in order; if both endpoints share the same root (`find(u) == find(v)`), they're already connected — this edge creates a cycle and is redundant.
> WHAT: Union by rank + path compression; return immediately on first cycle-forming edge.
> HOW: For each edge (a, b): if `union(a, b)` returns False (same component), return [a, b].

> [!note]- Python Solution
> ```python
> def findRedundantConnection(edges):
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
> **Kruskal's — sort edges by weight, greedily add if no cycle.**
> WHY: The cut property — the minimum weight edge crossing any cut belongs to some MST. Kruskal's: sort all edges by weight and greedily add each edge if it doesn't form a cycle.
> WHAT: Union-Find for O(α) cycle detection per edge (vs O(V) DFS cycle check).
> HOW: Sort edges by weight; for each edge, union its endpoints if they're in different components; stop after adding V-1 edges.

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

### Longest Path in a DAG

> [!example] Problem
> Find the length of the longest path in a directed acyclic graph (in terms of number of edges).

> [!info] Approach
> **Kahn's topo sort + DP — relax dp[v] = max(dp[u] + 1).**
> WHY: Only works on DAGs — cycles make the longest path undefined (infinite). Topological sort + DP: process nodes in topological order; `dp[node] = max(dp[predecessor] + 1)` for all incoming edges — no subproblem is accessed before it's solved.
> WHAT: Kahn's to get topo order, then one DP pass.
> HOW: `dp[node] = max(dp[node], dp[prev] + 1)` as edges are relaxed during Kahn's.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def longestPathDAG(n, edges):
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
> - DFS with memoization: `@lru_cache` on node; top-down. O(V+E). Equivalent but less explicit about ordering.
> - Bellman-Ford with negated weights: O(VE) — much slower; use only when you can't confirm DAG property.

---

## See Also

[[graph-algorithms]] | [[union-find]] | [[queue]] | [[tree]]
