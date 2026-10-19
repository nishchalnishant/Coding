---
module: striver/28-dynamic-programming
lesson: 54
topic: Minimum path sum in a grid
difficulty: Medium
source: https://takeuforward.org/learning/dsa/minimum-path-sum-in-a-grid?category=2d-3d-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, grid]
---
# 54. Minimum path sum in a grid

← [Partition array for maximum sum](53-partition-array-for-maximum-sum.md) · [Part 28 index](README.md) · Next → [Part 29: Tries](../29-tries/README.md)

> [!abstract] Problem at a glance
> **Task:** Moving only right or down from top-left to bottom-right, minimise the sum of the cells visited.
> **Key insight:** `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`, with the first row and first column filled as prefix sums. This is unique-paths with `min` in place of `+` and a cost per cell. Space drops to one row because row `i` only reads row `i − 1` and the cell to its left.
> **Difficulty:** Medium · **Pattern:** 2D DP on grids · **Also on:** [LC 64](https://leetcode.com/problems/minimum-path-sum/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-path-sum-in-a-grid?category=2d-3d-dp&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoised recursion](#3-memoised-recursion) · [4. 1D rolling DP](#4-1d-rolling-dp) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `m × n` grid of non-negative integers, find a path from the top-left to the bottom-right cell that minimises the sum of all numbers on it. You can only move down or right.

| Input | Output | Why |
|---|---|---|
| `[[1,3,1],[1,5,1],[4,2,1]]` | `7` | 1→3→1→1→1 |
| `[[1,2,3],[4,5,6]]` | `12` | 1→2→3→6 |
| `[[5]]` | `5` |  |

**Constraints:** `1 ≤ m, n ≤ 200`, `0 ≤ grid[i][j] ≤ 200`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoised recursion | f(i,j) = g + min(f(i-1,j), f(i,j-1)) | O(mn) | O(mn) + O(m+n) stack |
| 1D rolling DP | row[j] = g[i][j] + min(row[j], row[j-1]) | O(mn) | O(n) |

> [!tip] Interview angle
> Follow the DP ladder:
1. The recursion `f(i, j) = g[i][j] + min(f(i−1, j), f(i, j−1))`, which is exponential.
2. Memoise it, O(mn).
3. Tabulate it.
4. Reduce to a 1D row, O(n) space.

Handle the borders explicitly: out-of-grid cells cost +∞, and they must not count as 0.

---

## 3. Memoised recursion

**Intuition.** Recurse from the bottom-right. The base case is (0, 0). Out-of-bounds returns +∞.

```python
def mps_memo(grid):
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if i < 0 or j < 0:
            return float('inf')
        if i == 0 and j == 0:
            return grid[0][0]
        return grid[i][j] + min(f(i - 1, j), f(i, j - 1))
    return f(len(grid) - 1, len(grid[0]) - 1)
```

**Complexity:** time **O(mn)**, space **O(mn) + O(m+n) stack**.

---

## 4. 1D rolling DP

**Intuition.** `row[j]` holds the best value for the cell above until it is overwritten. `row[j-1]` already holds the best value for the cell to the left in the current row.

**Algorithm**

1. `row[0] = g[0][0]`; for `j ≥ 1`: `row[j] = row[j-1] + g[0][j]`.
2. For each later row `i`: `row[0] += g[i][0]`; for `j ≥ 1`: `row[j] = g[i][j] + min(row[j], row[j-1])`.
3. Return `row[n-1]`.

**Dry run** — [[1,3,1],[1,5,1],[4,2,1]]: row = [1,4,5]. i=1: [2, 5+min(4,2)=7, 1+min(5,7)=6]. i=2: [6, 2+min(7,6)=8, 1+min(6,8)=7]. Answer 7.

**C++**
```cpp
int minPathSum(vector<vector<int>>& g) {
    int m = g.size(), n = g[0].size();
    vector<int> row(n);
    row[0] = g[0][0];
    for (int j = 1; j < n; j++) row[j] = row[j - 1] + g[0][j];
    for (int i = 1; i < m; i++) {
        row[0] += g[i][0];
        for (int j = 1; j < n; j++) row[j] = g[i][j] + min(row[j], row[j - 1]);
    }
    return row[n - 1];
}
```

**Java**
```java
static int minPathSum(int[][] g) {
    int m = g.length, n = g[0].length;
    int[] row = new int[n];
    row[0] = g[0][0];
    for (int j = 1; j < n; j++) row[j] = row[j - 1] + g[0][j];
    for (int i = 1; i < m; i++) {
        row[0] += g[i][0];
        for (int j = 1; j < n; j++) row[j] = g[i][j] + Math.min(row[j], row[j - 1]);
    }
    return row[n - 1];
}
```

**Python**
```python
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    row = [0] * n
    row[0] = grid[0][0]
    for j in range(1, n):
        row[j] = row[j - 1] + grid[0][j]
    for i in range(1, m):
        row[0] += grid[i][0]
        for j in range(1, n):
            row[j] = grid[i][j] + min(row[j], row[j - 1])
    return row[-1]
```

**Complexity:** time **O(mn)**, space **O(n)** — Every path to (i, j) enters from (i−1, j) or (i, j−1). Optimal substructure holds because the costs are additive and do not depend on the path taken earlier.

---

## Edge cases

- 1×1 grid.
- Single row or column (prefix sum).
- Zeros everywhere.

---

## Common mistakes

1. Treating out-of-grid neighbours as 0 instead of +∞ in the recursion.
2. Forgetting to accumulate down the first column (`row[0] += g[i][0]`).
3. Using `INT_MAX + cell`, which overflows.

---

## Follow-ups

1. Print the path?
2. Also allowed to move diagonally?
3. Max path sum / negative cells?

<details><summary>Answer sketches</summary>

**#1:** Keep the full dp table and walk back from (m−1, n−1) choosing the smaller predecessor.

**#2:** Add dp[i−1][j−1] to the min.

**#3:** Same recurrence with max; negatives are fine for a DAG DP.
</details>

---

## Flashcards

**Min path sum recurrence?** #flashcard
dp[i][j] = g[i][j] + min(dp[i-1][j], dp[i][j-1]).

**Space optimisation?** #flashcard
One row: row[j] = g + min(row[j], row[j-1]).

**Interview track →** 
