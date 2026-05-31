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

### Number of Islands (BFS)

> [!example] Problem
> Given a 2D grid of '1' (land) and '0' (water), count the number of islands (connected components of land, 4-directional).

> [!info] Approach
> - **WHY:** Each island is a connected component. BFS naturally fans out level-by-level from a source cell, marking all reachable land as visited.
> - **WHAT:** Iterate every cell; when '1' found, BFS to mark all connected land as visited ('0'), increment count.
> - **HOW:** Seed the queue with the trigger cell; mark visited on enqueue (not dequeue) to prevent duplicate entries. Mutating the grid avoids an extra visited array.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def numIslands(grid):
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
> Time O(M×N), Space O(min(M,N)) queue width worst case.

> [!tip] Alternatives
> - DFS sinking: same logic recursively; simpler code but risks recursion depth on large grids.
> - Union-Find: union adjacent '1' cells; count unique roots. O(M×N·α). Better for dynamic updates.

---

### Walls and Gates (LC 286)

> [!example] Problem
> Given a grid of INF (empty room), -1 (wall), 0 (gate), fill each empty room with the distance to its nearest gate. If unreachable, leave as INF.

> [!info] Approach
> - **WHY:** Multi-source BFS from all gates simultaneously guarantees every room is reached via the shortest path to any gate in O(M×N) rather than O(M×N × gates) from separate BFS per room.
> - **WHAT:** Seed queue with all gates (value 0); BFS outward; assign `dist[gate] + 1` to unvisited INF neighbors.
> - **HOW:** Only enqueue cells that are INF — this acts as the visited guard. The first time a room is reached is always via its nearest gate.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def wallsAndGates(rooms):
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

### 01 Matrix (LC 542)

> [!example] Problem
> Given a binary matrix, return a matrix where each cell contains the distance to the nearest 0.

> [!info] Approach
> - **WHY:** Multi-source BFS from all 0-cells simultaneously propagates shortest distances outward in O(M×N). The alternative (BFS from each 1-cell) is O(M²×N²).
> - **WHAT:** Seed queue with all 0-positions (distance 0); mark 1-cells as unvisited (distance INF); BFS expanding to unvisited neighbors with distance + 1.
> - **HOW:** Initialize dist matrix with 0 for zeroes, INF for ones. Enqueue all zeroes at start. Only update a cell if current dist > neighbor dist + 1.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def updateMatrix(mat):
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

### Number of Provinces (LC 547)

> [!example] Problem
> Given an n×n adjacency matrix `isConnected`, return the number of provinces (connected components of cities).

> [!info] Approach
> - **WHY:** Each province is a connected component of an undirected graph. DFS marks all cities in a component as visited in one pass.
> - **WHAT:** Iterate each city; if unvisited, DFS to mark all reachable cities, increment province count.
> - **HOW:** Use a visited array instead of mutating the matrix. The matrix is symmetric but you only need to follow one direction per city.

> [!note]- Python Solution
> ```python
> def findCircleNum(isConnected):
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

### Number of Enclaves (LC 1020)

> [!example] Problem
> Given a binary grid (0=sea, 1=land), return the number of land cells that cannot "walk off" the boundary in any number of moves (4-directional).

> [!info] Approach
> - **WHY:** Any land cell connected to the border can reach the sea — it is NOT an enclave. Mirror of Surrounded Regions: mark all border-reachable land, then count remaining interior land.
> - **WHAT:** DFS/BFS from every border land cell, mark visited. Count unvisited land cells in the interior.
> - **HOW:** Walk all 4 borders; DFS from each '1' encountered, sinking to 0. After traversal, sum remaining 1-cells.

> [!note]- Python Solution
> ```python
> def numEnclaves(grid):
>     rows, cols = len(grid), len(grid[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
>             return
>         grid[r][c] = 0
>         dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)
> 
>     for r in range(rows):
>         dfs(r, 0); dfs(r, cols-1)
>     for c in range(cols):
>         dfs(0, c); dfs(rows-1, c)
> 
>     return sum(grid[r][c] for r in range(rows) for c in range(cols))
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N) recursion stack.

> [!tip] Alternatives
> - BFS from borders: iterative, avoids recursion stack overflow on large grids.
> - Union-Find with virtual border node: union all land cells; union border land with a sentinel; count non-sentinel roots. Same complexity, more code.

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

### Path with Minimum Effort (LC 1631)

> [!example] Problem
> Given a 2D grid of heights, find a path from top-left to bottom-right that minimizes the maximum absolute difference between adjacent cells. Return that minimum effort.

> [!info] Approach
> - **WHY:** Minimize the maximum edge weight on a path = bottleneck shortest path. Modified Dijkstra: `dist[r][c]` = minimum possible max-absolute-diff to reach (r,c); greedily process cells in order of current effort.
> - **WHAT:** Min-heap of `(effort, r, c)`. Transition: `new_effort = max(current_effort, abs(heights[nr][nc] - heights[r][c]))`.
> - **HOW:** First pop of (rows-1, cols-1) from the heap is the answer. Mark visited on pop to avoid reprocessing.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def minimumEffortPath(heights):
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

### Possible Bipartition (LC 886)

> [!example] Problem
> Given n people and a list of dislikes pairs, determine if it's possible to split everyone into two groups such that no two people who dislike each other are in the same group.

> [!info] Approach
> - **WHY:** Equivalent to bipartite checking on an undirected graph where edges represent dislikes. 2-colorable iff no odd cycle.
> - **WHAT:** Build adjacency list from dislikes; BFS 2-coloring over all components (graph may be disconnected).
> - **HOW:** People labeled 1..n — initialize color array of size n+1. For each uncolored node, BFS alternating colors; return False if same-color conflict found.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def possibleBipartition(n, dislikes):
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

### Reconstruct Itinerary (LC 332)

> [!example] Problem
> Given a list of airline tickets `[from, to]`, reconstruct the itinerary starting from "JFK" using all tickets exactly once. If multiple valid itineraries exist, return the lexicographically smallest one.

> [!info] Approach
> - **WHY:** Eulerian path problem on a directed multigraph — visit every edge exactly once. Hierholzer's algorithm finds an Eulerian path in O(E log E): greedily follow edges; when stuck (no outgoing edges left), backtrack and prepend the current node.
> - **WHAT:** Build adjacency list with sorted neighbors (for lexicographic order) using a min-heap or sorted list. DFS: always pick the smallest neighbor; when a node has no more outgoing edges, prepend to result.
> - **HOW:** Use a stack-based iterative post-order DFS: push node to result when its adjacency list is exhausted; reverse at the end.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def findItinerary(tickets):
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

### Critical Connections / Bridges (LC 1192)

> [!example] Problem
> Given a network of n servers and connections, find all critical connections — edges whose removal makes some server unreachable (bridges in the graph).

> [!info] Approach
> - **WHY:** Bridge detection requires Tarjan's algorithm. A bridge is an edge (u, v) where no back-edge from v's subtree reaches u or any ancestor of u — detected via `low[v] > disc[u]`.
> - **WHAT:** DFS with two arrays: `disc[u]` = discovery time, `low[u]` = lowest discovery time reachable from u's subtree (via back edges). If `low[v] > disc[u]`, edge (u,v) is a bridge.
> - **HOW:** Track parent to avoid treating the tree edge back to parent as a back-edge. Update `low[u] = min(low[u], low[v])` after recursing into v; `low[u] = min(low[u], disc[v])` for back-edges.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def criticalConnections(n, connections):
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
>     dfs(0, -1)
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
> Given a tree of n nodes, find all roots that produce minimum height trees. Return the list of such root values.

> [!info] Approach
> - **WHY:** The roots of minimum height trees are the "center" nodes of the tree — at most 2 nodes lying on the longest path (diameter). Topological leaf-trimming: iteratively remove all current leaves; the last 1–2 remaining nodes are the answer.
> - **WHAT:** Build adjacency list and degree array. Seed a queue with all leaves (degree == 1). BFS layer-by-layer: remove current leaves, expose new leaves (nodes whose degree drops to 1). Stop when ≤ 2 nodes remain.
> - **HOW:** Decrement `n` by the number of leaves removed each round; stop when `n <= 2` — remaining nodes are the answer.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def findMinHeightTrees(n, edges):
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

## See Also

[[graph-algorithms]] | [[union-find]] | [[queue]] | [[tree]]
### Shortest Path in a DAG

> [!example] Problem
> Given a directed acyclic graph with weighted edges, find shortest paths from a source node.

> [!info] Approach
> - **WHY:** In a DAG, a topological order guarantees that when a node is processed, all incoming dependencies are already finalized.
> - **WHAT:** Topologically sort the graph, then relax outgoing edges in that order.
> - **HOW:** Initialize distances, process nodes in topo order, and update `dist[v] = min(dist[v], dist[u] + w)` for each edge.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def shortest_path_dag(n: int, edges: list[tuple[int, int, int]], source: int) -> list[float]:
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

## Advanced Graph Algorithms

### Strongly Connected Components — Kosaraju's Algorithm

> [!example] Problem
> Find all strongly connected components (SCCs) in a directed graph. An SCC is a maximal set of nodes where every node is reachable from every other node.

> [!info] Approach
> - **WHY:** Kosaraju's runs two DFS passes. The first pass computes finish-order (equivalent to reverse topological order). The second pass on the reversed graph extracts SCCs in that finish order.
> - **WHAT:** Pass 1 — DFS on original graph, push nodes to a stack in finish order. Pass 2 — pop from the stack, DFS on the transposed graph; each DFS tree in pass 2 is one SCC.
> - **HOW:** Build adjacency list and its transpose. DFS on original, recording finish order in a stack. Then repeatedly pop from the stack and DFS on the transposed graph — all reachable unvisited nodes form one SCC.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def kosaraju(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
>     graph = defaultdict(list)
>     rev_graph = defaultdict(list)
>     for u, v in edges:
>         graph[u].append(v)
>         rev_graph[v].append(u)
>
>     visited = [False] * n
>     finish_order = []
>
>     def dfs1(node: int) -> None:
>         visited[node] = True
>         for neighbour in graph[node]:
>             if not visited[neighbour]:
>                 dfs1(neighbour)
>         finish_order.append(node)
>
>     for i in range(n):
>         if not visited[i]:
>             dfs1(i)
>
>     visited = [False] * n
>     sccs = []
>
>     def dfs2(node: int, component: list) -> None:
>         visited[node] = True
>         component.append(node)
>         for neighbour in rev_graph[node]:
>             if not visited[neighbour]:
>                 dfs2(neighbour, component)
>
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
> - **WHY:** Prim's grows the MST greedily from any starting node, always adding the cheapest edge that connects the current MST to an unvisited node. A min-heap makes this O(E log V).
> - **WHAT:** Use a min-heap of `(weight, node)`. Start with node 0. Greedily pick the smallest weight edge to an unvisited node, add it to the MST, and push all its edges into the heap.
> - **HOW:** `visited` set tracks MST nodes. Pop from heap; if already visited, skip. Otherwise mark visited, add weight to MST cost, push all unvisited neighbours into the heap.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
>
> def prim_mst(n: int, edges: list[tuple[int, int, int]]) -> int:
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
> - **WHY:** Dijkstra's is per-source (O(V * E log V) total for all-pairs). Floyd-Warshall's DP is simpler to implement and handles negative edges. For dense graphs it's competitive.
> - **WHAT:** `dist[i][j]` = shortest path from `i` to `j`. For each intermediate node `k`, check if routing through `k` shortens `dist[i][j]`.
> - **HOW:** Initialize `dist[i][j]` to edge weight if edge exists, 0 if `i == j`, infinity otherwise. Triple loop: for each `k`, for each `i`, for each `j`: `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.

> [!note]- Python Solution
> ```python
> def floyd_warshall(n: int, edges: list[tuple[int, int, int]]) -> list[list[float]]:
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
