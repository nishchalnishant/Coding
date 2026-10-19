---
module: striver/28-dynamic-programming
lesson: 9
topic: Unique paths II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/unique-paths-ii?category=dp-on-grids&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, grid]
---
# 9. Unique paths II

← [Grid unique paths](08-grid-unique-paths.md) · [Part 28 index](README.md) · Next → [Minimum Falling Path Sum](10-minimum-falling-path-sum.md)

> [!abstract] Problem at a glance
> **Task:** Count right/down paths from the top-left to the bottom-right when some cells are blocked (`1`).
> **Key insight:** Same recurrence as Unique Paths, but an obstacle cell has 0 paths. That single override also handles blocked starts, blocked ends and blocked first rows or columns, which the all-ones shortcut gets wrong.
> **Difficulty:** Medium · **Pattern:** Grid DP with blocked cells · **Also on:** LC 63
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/unique-paths-ii?category=dp-on-grids&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized recursion](#3-memoized-recursion) · [4. 1D rolling row](#4-1d-rolling-row) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`grid[i][j] = 1` marks an obstacle. Moving only right or down, return the number of paths from `(0,0)` to `(m−1,n−1)` that avoid obstacles.

| Input | Output | Why |
|---|---|---|
| `grid = [[0,0,0],[0,1,0],[0,0,0]]` | `2` | around the centre either way |
| `grid = [[0,1],[0,0]]` | `1` | down then right |

**Constraints:** `1 ≤ m, n ≤ 100`; the answer is < 2·10⁹.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized recursion | 0 on obstacle, else up + left | O(m·n) | O(m·n) |
| 1D rolling row | row[j] = 0 if blocked else row[j] + row[j−1] | O(m·n) | O(n) |

> [!tip] Interview angle
> Don't pre-fill the first row and column with 1s. A single obstacle in row 0 blocks everything to its right. Let the general recurrence handle the borders.

---

## 3. Memoized recursion

**Intuition.** `f(i,j) = 0` if out of grid or blocked; `f(0,0) = 1` if open.

```python
def obst_memo(g):
    m, n = len(g), len(g[0])
    dp = [[-1] * n for _ in range(m)]
    def f(i, j):
        if i < 0 or j < 0 or g[i][j] == 1:
            return 0
        if i == 0 and j == 0:
            return 1
        if dp[i][j] == -1:
            dp[i][j] = f(i - 1, j) + f(i, j - 1)
        return dp[i][j]
    return f(m - 1, n - 1)
```

**Complexity:** time **O(m·n)**, space **O(m·n)**.

---

## 4. 1D rolling row

**Intuition.** One row of state. Start with `row[0] = 1` (before any obstacle check) and sweep every row including the first. A blocked cell resets its entry to 0.

**Algorithm**

1. `row = [0]*n`; `row[0] = 1`.
2. For each row `i`, for `j = 0..n−1`: if `g[i][j] == 1`, `row[j] = 0`; else if `j > 0`, `row[j] += row[j−1]`.
3. Return `row[n−1]`.

**Dry run** — [[0,0,0],[0,1,0],[0,0,0]]: row 0 → [1,1,1]; row 1 → [1,0,1]; row 2 → [1,1,2] → 2.

**C++**
```cpp
int uniquePathsWithObstacles(vector<vector<int>>& g) {
    int m = g.size(), n = g[0].size();
    vector<long long> row(n, 0);
    row[0] = 1;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            if (g[i][j] == 1) row[j] = 0;
            else if (j > 0) row[j] += row[j - 1];
        }
    return (int)row[n - 1];
}
```

**Java**
```java
static int uniquePathsWithObstacles(int[][] g) {
    int m = g.length, n = g[0].length;
    long[] row = new long[n];
    row[0] = 1;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            if (g[i][j] == 1) row[j] = 0;
            else if (j > 0) row[j] += row[j - 1];
        }
    return (int) row[n - 1];
}
```

**Python**
```python
def unique_paths_obstacles(g):
    n = len(g[0])
    row = [0] * n
    row[0] = 1
    for r in g:
        for j in range(n):
            if r[j] == 1:
                row[j] = 0
            elif j > 0:
                row[j] += row[j - 1]
    return row[-1]
```

**Complexity:** time **O(m·n)**, space **O(n)** — each cell once; `long` guards intermediate rows that exceed int.

---

## Edge cases

- Start or end blocked: 0.
- `1 × 1` open grid: 1.
- An obstacle in the first row blocks every cell to its right in that row.

---

## Common mistakes

1. Pre-filling row 0 and column 0 with 1.
2. Returning 1 for a blocked `1 × 1` grid.

---

## Follow-ups

1. Minimum path sum on the same grid?
2. Count modulo 10⁹+7 on a 10³ × 10³ grid?

<details><summary>Answer sketches</summary>

**#1:** Replace `+` with `min` of the predecessors plus the cell cost (LC 64).

**#2:** The same DP with `% MOD`.
</details>

---

## Flashcards

**Obstacle grid DP rule?** #flashcard
Blocked cell → 0; otherwise above + left.

**Why not pre-fill borders with 1?** #flashcard
An obstacle on the border blocks everything after it.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
