---
tags: [l3-google, matrix, grid, bfs, dfs, dp]
topic: Matrix / Grid Problems
---

← [Data Structures index](../../01-data-structures/README.md)

# Matrix / Grid — Problem Walkthroughs

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **Must Master**: Appear in nearly every Google loop.
> `🎯 T2` — **Build Fluency**: Important but less frequent.
> `💤 T3` — **Skip at L3**: Overkill.

Grid problems are graphs in disguise. Every cell is a node; edges connect 4-directional (or 8-directional) neighbors. BFS = shortest path (unweighted); DFS = connectivity, exhaustive search.

---

## Traversal Foundations

### 4-Directional BFS Template
```python
from collections import deque

def bfs_grid(grid, start_r, start_c):
    ROWS, COLS = len(grid), len(grid[0])
    visited = set()
    queue = deque([(start_r, start_c, 0)])   # (row, col, dist)
    visited.add((start_r, start_c))
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while queue:
        r, c, dist = queue.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
```

**Mark visited on enqueue, not dequeue** — prevents the same cell from being added to the queue multiple times.

---

## Number of Islands `⚡ T1`

> Given a 2D grid of `'1'` (land) and `'0'` (water), count the number of islands (connected groups of `'1'`).

> [!example] Example
> ```
> Input:  [["1","1","0"],
>          ["0","1","0"],
>          ["0","0","1"]]
> Output: 2
> ```

> [!info] Approach
> DFS / BFS flood fill. Iterate every cell; when you find an unvisited `'1'`, increment count and flood-fill (mark all connected `'1'`s as visited). Classic connected-components pattern.

> [!note]- Python Solution
> ```python
> def numIslands(grid):
>     if not grid:
>         return 0
>     ROWS, COLS = len(grid), len(grid[0])
>     visited = set()
>     count = 0
>
>     def dfs(r, c):
>         if r < 0 or r >= ROWS or c < 0 or c >= COLS:
>             return
>         if (r, c) in visited or grid[r][c] == '0':
>             return
>         visited.add((r, c))
>         dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)
>
>     for r in range(ROWS):
>         for c in range(COLS):
>             if grid[r][c] == '1' and (r, c) not in visited:
>                 dfs(r, c)
>                 count += 1
>     return count
> ```

> [!success] Complexity
> Time O(M·N) — every cell visited once. Space O(M·N) worst case recursion stack.

**Follow-up**: Max area of island → track size during DFS. Surrounded regions → BFS from borders first.

---

## Walls and Gates `⚡ T1`

> Given a grid with `INF` (empty rooms), `-1` (walls), and `0` (gates), fill each empty room with distance to its nearest gate. If impossible, leave as `INF`.

> [!info] Approach
> **Multi-source BFS** — enqueue all gates simultaneously. BFS propagates distance layer by layer. No need for per-cell Dijkstra; BFS on unweighted grids is optimal.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def wallsAndGates(rooms):
>     if not rooms:
>         return
>     ROWS, COLS = len(rooms), len(rooms[0])
>     INF = float('inf')
>     queue = deque()
>     for r in range(ROWS):
>         for c in range(COLS):
>             if rooms[r][c] == 0:
>                 queue.append((r, c))
>     dirs = [(0,1),(0,-1),(1,0),(-1,0)]
>     while queue:
>         r, c = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < ROWS and 0 <= nc < COLS and rooms[nr][nc] == INF:
>                 rooms[nr][nc] = rooms[r][c] + 1
>                 queue.append((nr, nc))
> ```

> [!success] Complexity
> Time O(M·N). Space O(M·N).

**Key insight**: Multi-source BFS ≡ single source BFS on a super-node connected to all gates. Each cell is processed exactly once.

---

## Shortest Path in Binary Matrix `⚡ T1`

> Given an n×n binary matrix, return the length of the shortest clear path from top-left `(0,0)` to bottom-right `(n-1,n-1)`. A clear path uses only `0` cells and moves 8-directionally. Return -1 if no clear path.

> [!info] Approach
> BFS with 8-directional movement. Path length = number of cells in path. BFS finds minimum hops in unweighted grid.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def shortestPathBinaryMatrix(grid):
>     n = len(grid)
>     if grid[0][0] == 1 or grid[n-1][n-1] == 1:
>         return -1
>     queue = deque([(0, 0, 1)])   # (row, col, path_length)
>     grid[0][0] = 1               # mark visited by mutating grid
>     dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
>     while queue:
>         r, c, length = queue.popleft()
>         if r == n-1 and c == n-1:
>             return length
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
>                 grid[nr][nc] = 1   # mark visited
>                 queue.append((nr, nc, length + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(N²). Space O(N²).

**Edge case**: If `n == 1` and `grid[0][0] == 0`, return 1 (already at destination).

---

## Rotting Oranges `⚡ T1`

> Grid has `0` (empty), `1` (fresh orange), `2` (rotten orange). Each minute, every fresh orange adjacent to a rotten one becomes rotten. Return minimum minutes until no fresh oranges, or -1 if impossible.

> [!info] Approach
> Multi-source BFS from all initially rotten oranges. Track time as BFS level. After BFS, check if any fresh oranges remain.

> [!note]- Python Solution
> ```python
> from collections import deque
>
> def orangesRotting(grid):
>     ROWS, COLS = len(grid), len(grid[0])
>     queue = deque()
>     fresh = 0
>     for r in range(ROWS):
>         for c in range(COLS):
>             if grid[r][c] == 2:
>                 queue.append((r, c, 0))
>             elif grid[r][c] == 1:
>                 fresh += 1
>     if fresh == 0:
>         return 0
>     dirs = [(0,1),(0,-1),(1,0),(-1,0)]
>     time = 0
>     while queue:
>         r, c, t = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 1:
>                 grid[nr][nc] = 2
>                 fresh -= 1
>                 time = t + 1
>                 queue.append((nr, nc, t + 1))
>     return time if fresh == 0 else -1
> ```

> [!success] Complexity
> Time O(M·N). Space O(M·N).

---

## Spiral Matrix `🎯 T2`

> Return all elements of an m×n matrix in spiral order.

> [!info] Approach
> Shrinking boundaries. Maintain `top`, `bottom`, `left`, `right` pointers. Traverse right → down → left → up, then shrink. Stop when boundaries cross.

> [!note]- Python Solution
> ```python
> def spiralOrder(matrix):
>     result = []
>     top, bottom = 0, len(matrix) - 1
>     left, right = 0, len(matrix[0]) - 1
>     while top <= bottom and left <= right:
>         for c in range(left, right + 1):
>             result.append(matrix[top][c])
>         top += 1
>         for r in range(top, bottom + 1):
>             result.append(matrix[r][right])
>         right -= 1
>         if top <= bottom:
>             for c in range(right, left - 1, -1):
>                 result.append(matrix[bottom][c])
>             bottom -= 1
>         if left <= right:
>             for r in range(bottom, top - 1, -1):
>                 result.append(matrix[r][left])
>             left += 1
>     return result
> ```

> [!success] Complexity
> Time O(M·N). Space O(1) extra.

**Guard the inner left and up traversals** with `if top <= bottom` and `if left <= right` — without these, non-square matrices double-count rows/columns.

---

## Rotate Image `🎯 T2`

> Rotate an n×n matrix 90° clockwise in-place.

> [!info] Approach
> Two-step: (1) Transpose (swap `matrix[i][j]` with `matrix[j][i]`), (2) Reverse each row.

> [!note]- Python Solution
> ```python
> def rotate(matrix):
>     n = len(matrix)
>     # Transpose
>     for i in range(n):
>         for j in range(i + 1, n):
>             matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
>     # Reverse each row
>     for row in matrix:
>         row.reverse()
> ```

> [!success] Complexity
> Time O(N²). Space O(1).

**Counter-clockwise 90°**: reverse each row first, then transpose.

---

## Set Matrix Zeroes `🎯 T2`

> If any cell `matrix[i][j] == 0`, set its entire row and column to 0 in-place.

> [!info] Approach
> O(1) space: use first row and first column as markers. First pass: mark which rows/cols need zeroing. Second pass: zero out cells. Handle first row and column separately with boolean flags.

> [!note]- Python Solution
> ```python
> def setZeroes(matrix):
>     ROWS, COLS = len(matrix), len(matrix[0])
>     first_row_zero = any(matrix[0][c] == 0 for c in range(COLS))
>     first_col_zero = any(matrix[r][0] == 0 for r in range(ROWS))
>
>     for r in range(1, ROWS):
>         for c in range(1, COLS):
>             if matrix[r][c] == 0:
>                 matrix[r][0] = 0
>                 matrix[0][c] = 0
>
>     for r in range(1, ROWS):
>         for c in range(1, COLS):
>             if matrix[r][0] == 0 or matrix[0][c] == 0:
>                 matrix[r][c] = 0
>
>     if first_row_zero:
>         for c in range(COLS):
>             matrix[0][c] = 0
>     if first_col_zero:
>         for r in range(ROWS):
>             matrix[r][0] = 0
> ```

> [!success] Complexity
> Time O(M·N). Space O(1).

---

## Unique Paths `⚡ T1`

> Count paths from top-left to bottom-right in an m×n grid, moving only right or down.

> [!info] Approach
> DP: `dp[r][c] = dp[r-1][c] + dp[r][c-1]`. Base case: first row and first column are all 1. Optimize to O(n) space using a 1D array.

> [!note]- Python Solution
> ```python
> def uniquePaths(m, n):
>     dp = [1] * n
>     for r in range(1, m):
>         for c in range(1, n):
>             dp[c] += dp[c - 1]
>     return dp[n - 1]
> ```

> [!success] Complexity
> Time O(M·N). Space O(N).

**Alternative**: `math.comb(m + n - 2, n - 1)` — choose which steps are "right" from all steps.

**Follow-up — Unique Paths II** (with obstacles):
```python
def uniquePathsWithObstacles(grid):
    COLS = len(grid[0])
    dp = [0] * COLS
    dp[0] = 1
    for row in grid:
        for c in range(COLS):
            if row[c] == 1:
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c - 1]
    return dp[-1]
```

---

## Minimum Path Sum `⚡ T1`

> Find the path from top-left to bottom-right that minimizes the sum of numbers along the path (right/down only).

> [!info] Approach
> DP: `dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])`. Space-optimized to O(n) using 1D dp.

> [!note]- Python Solution
> ```python
> def minPathSum(grid):
>     ROWS, COLS = len(grid), len(grid[0])
>     dp = grid[0][:]
>     for c in range(1, COLS):
>         dp[c] += dp[c - 1]
>     for r in range(1, ROWS):
>         dp[0] += grid[r][0]
>         for c in range(1, COLS):
>             dp[c] = grid[r][c] + min(dp[c], dp[c - 1])
>     return dp[-1]
> ```

> [!success] Complexity
> Time O(M·N). Space O(N).

---

## Maximal Square `🎯 T2`

> Find the largest square containing only `'1'`s in a binary matrix. Return its area.

> [!info] Approach
> DP: `dp[r][c]` = side length of largest square with bottom-right corner at `(r, c)`.
> Recurrence: `dp[r][c] = min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1]) + 1` when `matrix[r][c] == '1'`.

> [!note]- Python Solution
> ```python
> def maximalSquare(matrix):
>     ROWS, COLS = len(matrix), len(matrix[0])
>     dp = [[0] * (COLS + 1) for _ in range(ROWS + 1)]
>     max_side = 0
>     for r in range(1, ROWS + 1):
>         for c in range(1, COLS + 1):
>             if matrix[r-1][c-1] == '1':
>                 dp[r][c] = min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1]) + 1
>                 max_side = max(max_side, dp[r][c])
>     return max_side * max_side
> ```

> [!success] Complexity
> Time O(M·N). Space O(M·N), reducible to O(N) with rolling array.

**Click moment**: the `min(top, left, diagonal) + 1` recurrence captures that a square is only as big as the smallest square that can extend in all three directions.

---

## 2D Prefix Sum `🎯 T2`

> Efficiently answer range-sum queries on a 2D matrix: sum of all elements in sub-rectangle `(r1,c1)` to `(r2,c2)`.

> [!info] Approach
> Build prefix sum table. `prefix[r][c]` = sum of all elements in rectangle `(0,0)` to `(r-1,c-1)`. Query uses inclusion-exclusion.

> [!note]- Python Solution
> ```python
> class NumMatrix:
>     def __init__(self, matrix):
>         ROWS, COLS = len(matrix), len(matrix[0])
>         self.prefix = [[0] * (COLS + 1) for _ in range(ROWS + 1)]
>         for r in range(1, ROWS + 1):
>             for c in range(1, COLS + 1):
>                 self.prefix[r][c] = (matrix[r-1][c-1]
>                     + self.prefix[r-1][c]
>                     + self.prefix[r][c-1]
>                     - self.prefix[r-1][c-1])
>
>     def sumRegion(self, r1, c1, r2, c2):
>         return (self.prefix[r2+1][c2+1]
>                 - self.prefix[r1][c2+1]
>                 - self.prefix[r2+1][c1]
>                 + self.prefix[r1][c1])
> ```

> [!success] Complexity
> Build O(M·N). Query O(1).

---

## Pattern Summary

| Problem | Pattern | Key insight |
|---------|---------|-------------|
| Number of Islands | DFS/BFS flood fill | Connected components |
| Walls and Gates | Multi-source BFS | All sources simultaneously |
| Rotting Oranges | Multi-source BFS with time | Level = time elapsed |
| Shortest Path (binary) | BFS 8-dir | BFS = min hops |
| Spiral Matrix | Shrinking boundaries | Guard inner traversals |
| Rotate Image | Transpose + reverse rows | 90° CW decomposition |
| Set Matrix Zeroes | First row/col as markers | O(1) space trick |
| Unique Paths | DP (top-down to bottom-right) | Combinatorics or DP |
| Minimum Path Sum | DP with rolling array | `min(top, left)` at each cell |
| Maximal Square | DP `min(3 neighbors) + 1` | Bottleneck = smallest square |
| 2D Prefix Sum | Precompute + inclusion-exclusion | O(1) range query |

## See Also

- Matrix/grid theory: [`01-data-structures/04-matrix.md`](../../01-data-structures/04-matrix.md) (if exists) or [`01-data-structures/13-graphs.md`](../../01-data-structures/13-graphs.md)
- Graph algorithms: [`coding/algorithms/13-graph-algorithms.md`](../algorithms/13-graph-algorithms.md)
- DP patterns: [`coding/algorithms/15-dynamic-programming.md`](../algorithms/15-dynamic-programming.md)
