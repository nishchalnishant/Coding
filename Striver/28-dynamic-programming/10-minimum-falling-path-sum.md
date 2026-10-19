---
module: striver/28-dynamic-programming
lesson: 10
topic: Minimum Falling Path Sum
difficulty: Medium
source: https://takeuforward.org/learning/dsa/minimum-falling-path-sum?category=dp-on-grids&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, grid]
---
# 10. Minimum Falling Path Sum

← [Unique paths II](09-unique-paths-ii.md) · [Part 28 index](README.md) · Next → [Triangle](11-triangle.md)

> [!abstract] Problem at a glance
> **Task:** Choose one cell per row of an `n × n` matrix, moving to column `j−1`, `j` or `j+1` each step, minimising the sum.
> **Key insight:** This is a grid DP with a **variable start and end**: `dp[i][j] = a[i][j] + min(dp[i−1][j−1], dp[i−1][j], dp[i−1][j+1])`. Initialise row 0 with itself and take the min of the last row. One previous row is enough.
> **Difficulty:** Medium · **Pattern:** Grid DP: three predecessors, any start/end · **Also on:** LC 931
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-falling-path-sum?category=dp-on-grids&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized recursion from the bottom](#3-memoized-recursion-from-the-bottom) · [4. Row-by-row tabulation](#4-row-by-row-tabulation) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `n × n` integer matrix, a falling path starts at any cell of row 0, and from `(i, j)` moves to `(i+1, j−1)`, `(i+1, j)` or `(i+1, j+1)`. Return the minimum sum over all falling paths.

| Input | Output | Why |
|---|---|---|
| `[[2,1,3],[6,5,4],[7,8,9]]` | `13` | 1 → 4 → 8 or 1 → 5 → 7 |
| `[[-19,57],[-40,-5]]` | `-59` | -19 + (-40) |

**Constraints:** `1 ≤ n ≤ 100`, `−100 ≤ a[i][j] ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized recursion from the bottom | f(i,j) = a[i][j] + min(f(i−1, j±1, j)) | O(n²) | O(n²) |
| Row-by-row tabulation | prev row → cur row | O(n²) | O(n) |

> [!tip] Interview angle
> Values can be negative, so don't use 0 as an "unset" sentinel. Out-of-range neighbours must be ∞, not 0. The maximum-falling-path version only flips `min` to `max` and ∞ to −∞.

---

## 3. Memoized recursion from the bottom

**Intuition.** `f(i, j)` = cheapest path from row 0 ending at `(i, j)`. The answer is `min_j f(n−1, j)`.

```python
def fall_memo(a):
    n = len(a)
    INF = float("inf")
    dp = [[None] * n for _ in range(n)]
    def f(i, j):
        if j < 0 or j >= n:
            return INF
        if i == 0:
            return a[0][j]
        if dp[i][j] is None:
            dp[i][j] = a[i][j] + min(f(i - 1, j - 1), f(i - 1, j), f(i - 1, j + 1))
        return dp[i][j]
    return min(f(n - 1, j) for j in range(n))
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 4. Row-by-row tabulation

**Intuition.** `prev` = best sums ending in each column of the previous row. Build `cur` from the three neighbours, treating out-of-range as ∞.

**Algorithm**

1. `prev = a[0]`.
2. For `i = 1..n−1`: `cur[j] = a[i][j] + min(prev[j], prev[j−1] if j>0, prev[j+1] if j<n−1)`.
3. `prev = cur`; return `min(prev)`.

**Dry run** — [[2,1,3],[6,5,4],[7,8,9]]: prev = [2,1,3] → [7,6,5] → [7+6, 8+5, 9+5] = [13,13,14] → 13.

**C++**
```cpp
int minFallingPathSum(vector<vector<int>>& a) {
    int n = a.size();
    vector<int> prev = a[0];
    for (int i = 1; i < n; i++) {
        vector<int> cur(n);
        for (int j = 0; j < n; j++) {
            int best = prev[j];
            if (j > 0) best = min(best, prev[j - 1]);
            if (j < n - 1) best = min(best, prev[j + 1]);
            cur[j] = a[i][j] + best;
        }
        prev = cur;
    }
    return *min_element(prev.begin(), prev.end());
}
```

**Java**
```java
static int minFallingPathSum(int[][] a) {
    int n = a.length;
    int[] prev = a[0].clone();
    for (int i = 1; i < n; i++) {
        int[] cur = new int[n];
        for (int j = 0; j < n; j++) {
            int best = prev[j];
            if (j > 0) best = Math.min(best, prev[j - 1]);
            if (j < n - 1) best = Math.min(best, prev[j + 1]);
            cur[j] = a[i][j] + best;
        }
        prev = cur;
    }
    int ans = Integer.MAX_VALUE;
    for (int x : prev) ans = Math.min(ans, x);
    return ans;
}
```

**Python**
```python
def min_falling_path_sum(a):
    n = len(a)
    prev = list(a[0])
    for i in range(1, n):
        prev = [a[i][j] + min(prev[max(j - 1, 0):j + 2]) for j in range(n)]
    return min(prev)
```

**Complexity:** time **O(n²)**, space **O(n)** — n rows × n columns × 3 neighbours.

---

## Edge cases

- `n = 1`: the single value.
- Negative values: use ∞ sentinels, not 0 or −1.
- Edge columns have only two predecessors.

---

## Common mistakes

1. Starting only from column 0 (the path may start anywhere).
2. Using `0` for out-of-range neighbours, which wrongly makes them attractive.

---

## Follow-ups

1. Falling path with non-zero shifts (LC 1289: next row must use a **different** column)?
2. Maximum falling path?

<details><summary>Answer sketches</summary>

**#1:** Keep the min and second-min of `prev`; `cur[j] = a[i][j] + (min1 if argmin ≠ j else min2)`, O(n²).

**#2:** Flip min → max and ∞ → −∞.
</details>

---

## Flashcards

**Falling path recurrence?** #flashcard
`dp[i][j] = a[i][j] + min(dp[i−1][j−1..j+1])`.

**Variable start/end in grid DP?** #flashcard
Initialise the whole first row; answer = best of the last row.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
