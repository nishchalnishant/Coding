# Grid DP — 2D Dynamic Programming on Grids

DP problems on M×N grids where movement is constrained (usually right/down) or where you optimize paths, counts, or regions. For the broader guide see [README.md](README.md).

---

## Theory & Mental Model

**Why grid DP?** Grid problems have a natural 2D state: `dp[i][j]` = the answer for the subgrid ending at cell `(i, j)`. Because you move only right/down (or from some fixed start), all dependencies flow from smaller indices — perfect for bottom-up tabulation.

**State definition.** `dp[i][j]` typically means:
- *Count* problems: "number of ways to reach `(i,j)`"
- *Optimization* problems: "minimum/maximum cost to reach `(i,j)`"
- *Region* problems: "best region ending at `(i,j)` as bottom-right corner"

**Base cases.** Always initialize:
- Top row (`i=0`): depends only on leftward accumulation
- Left column (`j=0`): depends only on downward accumulation

**Space optimization.** Most grid DPs only need the previous row → reduce O(M×N) to O(N) with a rolling 1D array.

---

## Pattern 1 — Unique Paths (Count Paths)

### Unique Paths I (LeetCode 62)

**Problem:** M×N grid. Start top-left, reach bottom-right. Only right or down moves. Count paths.

**Recurrence:** `dp[i][j] = dp[i-1][j] + dp[i][j-1]`

```python
def unique_paths(m: int, n: int) -> int:
    dp = [1] * n          # base: top row all 1s (only rightward path)
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]   # dp[j] = from above; dp[j-1] = from left
    return dp[n-1]
```

> [!TIP]
> **Math shortcut:** `C(m+n-2, m-1)` = number of ways to arrange `(m-1)` down-moves and `(n-1)` right-moves. Use `math.comb(m+n-2, m-1)` in Python for O(1).

### Unique Paths II — With Obstacles (LeetCode 63)

**Problem:** Same grid but some cells are blocked (`obstacleGrid[i][j] = 1`). Blocked cells contribute 0 paths.

```python
def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = 1 if grid[0][0] == 0 else 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dp[j] = 0         # blocked cell
            elif j > 0:
                dp[j] += dp[j-1]
    return dp[n-1]
```

> [!CAUTION]
> Initialize `dp[0] = 0` if the start cell is blocked — easily missed. Also reset blocked cells to 0 before adding the left-neighbor contribution.

---

## Pattern 2 — Minimum/Maximum Path Sum

### Minimum Path Sum (LeetCode 64)

**Problem:** Find path from top-left to bottom-right (right/down moves) with minimum sum of cell values.

**Recurrence:** `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`

```python
def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    # Modify grid in-place — O(1) extra space
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                grid[i][j] += grid[i][j-1]     # top row: only from left
            elif j == 0:
                grid[i][j] += grid[i-1][j]     # left col: only from above
            else:
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])
    return grid[m-1][n-1]
```

### Triangle — Minimum Path (LeetCode 120)

**Problem:** Triangle array; from top, move to adjacent element in next row. Find min path sum to bottom.

**Key insight:** Work **bottom-up** — avoid managing variable-width row indexing.

```python
def minimum_total(triangle: list[list[int]]) -> int:
    dp = triangle[-1][:]    # start from last row
    for i in range(len(triangle) - 2, -1, -1):
        for j in range(len(triangle[i])):
            dp[j] = triangle[i][j] + min(dp[j], dp[j+1])
    return dp[0]
```

### Dungeon Game (LeetCode 174)

**Problem:** Knight must survive (HP > 0 at all times) traveling from top-left to bottom-right. Find minimum initial HP. Cells can have negative values (demons) or positive (magic).

**Key insight:** Work **backwards** from bottom-right. `dp[i][j]` = minimum HP the knight needs when entering cell `(i,j)`.

```python
def calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    m, n = len(dungeon), len(dungeon[0])
    dp = [[0] * n for _ in range(m)]
    dp[m-1][n-1] = max(1 - dungeon[m-1][n-1], 1)

    # Fill last row (right to left)
    for j in range(n-2, -1, -1):
        dp[m-1][j] = max(dp[m-1][j+1] - dungeon[m-1][j], 1)
    # Fill last column (bottom to top)
    for i in range(m-2, -1, -1):
        dp[i][n-1] = max(dp[i+1][n-1] - dungeon[i][n-1], 1)
    # Fill rest
    for i in range(m-2, -1, -1):
        for j in range(n-2, -1, -1):
            need = min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]
            dp[i][j] = max(need, 1)

    return dp[0][0]
```

> [!CAUTION]
> **Forward DP fails for Dungeon Game.** You can't determine minimum entry HP from top-left forward because HP constraints propagate backwards. This is the canonical example where reversing the DP direction is mandatory.

---

## Pattern 3 — Maximal Square / Region DP

### Maximal Square (LeetCode 221)

**Problem:** Find the largest square containing only 1s in a binary matrix. Return its area.

**Recurrence:** `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1` when `matrix[i][j] == '1'`.

**Why min?** The side of the square is limited by the smallest square ending at each of the three neighbors. All three must agree.

```python
def maximal_square(matrix: list[list[str]]) -> int:
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    dp = [0] * (n + 1)
    max_side, prev = 0, 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            temp = dp[j]
            if matrix[i-1][j-1] == '1':
                dp[j] = min(dp[j], dp[j-1], prev) + 1
                max_side = max(max_side, dp[j])
            else:
                dp[j] = 0
            prev = temp

    return max_side * max_side
```

> [!TIP]
> `prev` holds the value of `dp[j]` from the **previous row before overwriting** — this is the diagonal `dp[i-1][j-1]` value in the 2D table. Essential for 1D space optimization of this recurrence.

### Maximal Rectangle (LeetCode 85)

**Problem:** Find the largest rectangle containing only 1s.

**Key insight:** For each row, treat it as the base of a histogram and run the "largest rectangle in histogram" algorithm (stack-based O(N)).

```python
def maximal_rectangle(matrix: list[list[str]]) -> int:
    if not matrix: return 0
    n = len(matrix[0])
    heights = [0] * n
    max_area = 0

    def largest_in_histogram(h: list[int]) -> int:
        stack, area = [], 0
        for i, height in enumerate(h + [0]):
            while stack and h[stack[-1]] > height:
                top = stack.pop()
                width = i if not stack else i - stack[-1] - 1
                area = max(area, h[top] * width)
            stack.append(i)
        return area

    for row in matrix:
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0
        max_area = max(max_area, largest_in_histogram(heights))

    return max_area
```

---

## Pattern 4 — Multi-Source / Multi-Trip Grid DP

### Cherry Pickup I (LeetCode 741)

**Problem:** N×N grid with cherries. Go from `(0,0)` to `(N-1,N-1)` and back; maximize cherries. A cell collected once is empty for the return trip.

**Key insight:** Simulate **two simultaneous forward trips** instead of forward + backward. Two people start at `(0,0)` and take `2N-2` steps.

**State:** `dp[t][r1][r2]` = max cherries when both are at step `t`, person1 in row `r1`, person2 in row `r2`. Derive `c1 = t - r1`, `c2 = t - r2`.

```python
def cherry_pickup(grid: list[list[int]]) -> int:
    n = len(grid)
    INF = float('-inf')
    # dp[r1][r2] for current step t
    dp = [[INF] * n for _ in range(n)]
    dp[0][0] = grid[0][0]

    for t in range(1, 2 * n - 1):
        ndp = [[INF] * n for _ in range(n)]
        for r1 in range(max(0, t - n + 1), min(n - 1, t) + 1):
            c1 = t - r1
            if not (0 <= c1 < n) or grid[r1][c1] == -1:
                continue
            for r2 in range(r1, min(n - 1, t) + 1):
                c2 = t - r2
                if not (0 <= c2 < n) or grid[r2][c2] == -1:
                    continue
                # Both people move from one of 4 previous positions
                best = max(
                    dp[r1][r2], dp[r1-1][r2] if r1 > 0 else INF,
                    dp[r1][r2-1] if r2 > 0 else INF,
                    dp[r1-1][r2-1] if r1 > 0 and r2 > 0 else INF
                )
                if best == INF:
                    continue
                cherries = grid[r1][c1]
                if r1 != r2:
                    cherries += grid[r2][c2]   # different cells: add both
                ndp[r1][r2] = best + cherries
        dp = ndp

    return max(dp[n-1][n-1], 0)
```

### Cherry Pickup II (LeetCode 1463)

**Problem:** Two robots start at `(0, 0)` and `(0, n-1)`. Both move down one row per step and left/right/stay. Maximize total cherries; same cell counts once.

**State:** `dp[c1][c2]` — both at the same row, columns `c1` and `c2`.

```python
def cherry_pickup_ii(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    INF = float('-inf')
    dp = [[INF] * n for _ in range(n)]
    dp[0][n-1] = grid[0][0] + (grid[0][n-1] if n > 1 else 0)

    for row in range(1, m):
        ndp = [[INF] * n for _ in range(n)]
        for c1 in range(n):
            for c2 in range(c1, n):   # c1 <= c2 by symmetry
                best = INF
                for dc1 in (-1, 0, 1):
                    for dc2 in (-1, 0, 1):
                        pc1, pc2 = c1 + dc1, c2 + dc2
                        if 0 <= pc1 < n and 0 <= pc2 < n and dp[pc1][pc2] != INF:
                            best = max(best, dp[pc1][pc2])
                if best == INF:
                    continue
                cherries = grid[row][c1] + (grid[row][c2] if c1 != c2 else 0)
                ndp[c1][c2] = best + cherries
        dp = ndp

    return max(max(row) for row in dp)
```

---

## Pattern 5 — DP with 4-Directional Movement

### Out of Boundary Paths (LeetCode 576)

**Problem:** Start at `(startRow, startCol)` in an M×N grid. Make exactly `maxMove` moves. Count paths that go out of bounds.

```python
def find_paths(m, n, maxMove, startRow, startCol) -> int:
    MOD = 10**9 + 7
    dp = [[0]*n for _ in range(m)]
    dp[startRow][startCol] = 1
    result = 0

    for _ in range(maxMove):
        ndp = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if dp[i][j] == 0: continue
                for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni, nj = i+di, j+dj
                    if 0 <= ni < m and 0 <= nj < n:
                        ndp[ni][nj] = (ndp[ni][nj] + dp[i][j]) % MOD
                    else:
                        result = (result + dp[i][j]) % MOD
        dp = ndp
    return result
```

---

## Interview Questions — Logic & Trickiness

| Problem | LC # | Pattern | Click Moment | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| **Unique Paths** | 62 | Count paths | `dp[i][j] = dp[i-1][j] + dp[i][j-1]` | Math formula `C(m+n-2, m-1)` is O(1) |
| **Unique Paths II** | 63 | Count paths with obstacles | Reset blocked cells to 0 | Blocked start → always 0 |
| **Minimum Path Sum** | 64 | Min cost path | `min(from_above, from_left)` | Can modify grid in-place for O(1) space |
| **Triangle** | 120 | Min path, variable width | Work bottom-up | Top-down forces complex index math |
| **Dungeon Game** | 174 | Min HP path | **Reverse DP** — backward from goal | Forward DP is impossible here |
| **Maximal Square** | 221 | Region DP | `min(3 neighbors) + 1` | `prev` scalar holds diagonal for 1D opt |
| **Maximal Rectangle** | 85 | Histogram + stack | Row → histogram → stack O(N) | Not pure 2D DP; stack-based inner loop |
| **Cherry Pickup I** | 741 | Two simultaneous paths | Two people, same step `t` | `r1 <= r2` symmetry halves state space |
| **Cherry Pickup II** | 1463 | Two robots from top | `dp[c1][c2]` per row | `c1 <= c2` symmetry; add cherry once if same col |
| **Out of Boundary Paths** | 576 | 4-direction DP | Simulate layer by layer | Modular arithmetic; result += out-of-bounds transitions |
| **Coin Change (Grid)** | — | 2D knapsack variant | Treat grid cells as items | Grid DP + knapsack hybrid |
| **Number of Islands DP** | — | Region expansion | DFS/BFS is better | DP rarely used for island counting |

---

## Space Optimization Rules for Grid DP

| DP Reads From | Optimize To | How |
| :--- | :--- | :--- |
| `dp[i-1][j]` only | 1D array overwrite | Process left→right; `dp[j]` becomes current row |
| `dp[i-1][j]` and `dp[i][j-1]` | 1D array | Same — `dp[j-1]` already updated for current row |
| `dp[i-1][j-1]` (diagonal) | 1D + `prev` scalar | Save `dp[j]` before overwriting; use as diagonal |
| `dp[i+1][j]`, `dp[i][j+1]` (reverse) | 1D reverse pass | Fill right→left, bottom→top |

---

## See also

- [README.md](README.md) — 4-step DP framework
- [dp-aditya-verma.md](dp-aditya-verma.md) — MCM / Interval DP
- [questions-bank.md](questions-bank.md) — Grid DP drill problems
