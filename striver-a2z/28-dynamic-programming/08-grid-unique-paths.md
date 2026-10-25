---
module: striver-a2z/28-dynamic-programming
lesson: 8
topic: Grid unique paths
difficulty: Medium
source: https://takeuforward.org/learning/dsa/grid-unique-paths?category=dp-on-grids&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, grid, combinatorics]
---
# 8. Grid unique paths

← [Ninja's training](07-ninjas-training.md) · [Part 28 index](README.md) · Next → [Unique paths II](09-unique-paths-ii.md)

> [!abstract] Problem at a glance
> **Task:** Count the monotone (right/down) paths from the top-left to the bottom-right of an `m × n` grid.
> **Key insight:** A cell is entered from above or from the left: `dp[i][j] = dp[i−1][j] + dp[i][j−1]`, with the first row and column all 1. Combinatorially it is `C(m+n−2, m−1)`: choose which of the `m+n−2` moves go down.
> **Difficulty:** Medium · **Pattern:** Grid DP: sum of two predecessors · **Also on:** LC 62
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/grid-unique-paths?category=dp-on-grids&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized recursion](#3-memoized-recursion) · [4. Combinatorics](#4-combinatorics) · [5. 1D rolling row](#5-1d-rolling-row) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A robot starts at `(0,0)` of an `m × n` grid and moves only right or down. Return the number of distinct paths to `(m−1, n−1)`.

| Input | Output | Why |
|---|---|---|
| `m = 3, n = 7` | `28` | C(8, 2) |
| `m = 3, n = 2` | `3` | RDD, DRD, DDR |

**Constraints:** `1 ≤ m, n ≤ 100`; the answer is ≤ 2·10⁹.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized recursion | f(i,j) = f(i−1,j) + f(i,j−1) | O(m·n) | O(m·n) |
| Combinatorics | C(m+n−2, m−1) | O(min(m,n)) | O(1) |
| 1D rolling row | row[j] += row[j−1] | O(m·n) | O(n) |

> [!tip] Interview angle
> Write the DP, then mention the O(min(m, n)) combinatorial answer. Compute it multiplicatively (`res = res·(N−k+i)/i`) so every intermediate value stays an integer.

---

## 3. Memoized recursion

**Intuition.** `f(i, j)` = paths from `(0,0)` to `(i,j)`. Base: `f(0,0) = 1`, out of grid = 0.

```python
def paths_memo(m, n):
    dp = [[-1] * n for _ in range(m)]
    def f(i, j):
        if i < 0 or j < 0:
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

## 4. Combinatorics

**Intuition.** Every path is a word of `m−1` D's and `n−1` R's. Count the arrangements.

```python
def paths_comb(m, n):
    N, k = m + n - 2, min(m, n) - 1
    res = 1
    for i in range(1, k + 1):
        res = res * (N - k + i) // i
    return res
```

**Complexity:** time **O(min(m,n))**, space **O(1)**.

---

## 5. 1D rolling row

**Intuition.** Tabulate row by row. `row[j]` currently holds the value from the row above, and `row[j−1]` is already today's left neighbour, so `row[j] += row[j−1]` updates in place.

**Algorithm**

1. `row = [1] * n` (first row).
2. Repeat `m − 1` times: for `j = 1..n−1`, `row[j] += row[j−1]`.
3. Return `row[n−1]`.

**Dry run** — m = 3, n = 3: [1,1,1] → [1,2,3] → [1,3,6] → 6.

**C++**
```cpp
int uniquePaths(int m, int n) {
    vector<int> row(n, 1);
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            row[j] += row[j - 1];
    return row[n - 1];
}
```

**Java**
```java
static int uniquePaths(int m, int n) {
    int[] row = new int[n];
    Arrays.fill(row, 1);
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            row[j] += row[j - 1];
    return row[n - 1];
}
```

**Python**
```python
def unique_paths(m, n):
    row = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]
    return row[-1]
```

**Complexity:** time **O(m·n)**, space **O(n)** — m·n cell updates, one row of storage.

---

## Edge cases

- `m = 1` or `n = 1`: exactly one path.
- Large grid: the combinatorial form needs 64-bit intermediates in C++/Java.

---

## Common mistakes

1. Computing `(m+n−2)! / …` directly, which overflows.
2. Starting the 1D loop at `j = 0`, which reads `row[−1]`.

---

## Follow-ups

1. Obstacles?
2. Paths that must pass through cell `(a, b)`?

<details><summary>Answer sketches</summary>

**#1:** Next problem: zero out obstacle cells.

**#2:** `paths((0,0)→(a,b)) × paths((a,b)→end)`.
</details>

---

## Flashcards

**Unique paths closed form?** #flashcard
C(m+n−2, m−1).

**Grid DP 1D update?** #flashcard
`row[j] += row[j−1]` (above + left).

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
