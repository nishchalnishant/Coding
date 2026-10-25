---
module: striver-a2z/28-dynamic-programming
lesson: 13
topic: Count Square Submatrices with All Ones
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-square-submatrices-with-all-one?category=dp-on-grids&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, grid, matrix]
---
# 13. Count Square Submatrices with All Ones

← [Cherry pickup II](12-cherry-pickup-ii.md) · [Part 28 index](README.md) · Next → [Best time to buy and sell stock](14-best-time-to-buy-and-sell-stock.md)

> [!abstract] Problem at a glance
> **Task:** Count every square submatrix (of any size) consisting only of 1s.
> **Key insight:** Let `dp[i][j]` = side of the largest all-ones square with **bottom-right corner** `(i, j)`. Then `dp[i][j] = 1 + min(top, left, top-left)` when the cell is 1. A square of side `s` ending at `(i, j)` contains squares of sides `1..s` ending there, so the answer is `Σ dp`.
> **Difficulty:** Medium · **Pattern:** Grid DP: min of three neighbours · **Also on:** LC 1277
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-square-submatrices-with-all-one?category=dp-on-grids&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: grow each square](#3-brute-force-grow-each-square) · [4. DP on the bottom-right corner](#4-dp-on-the-bottom-right-corner) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `m × n` binary matrix, return the number of square submatrices whose cells are all 1.

| Input | Output | Why |
|---|---|---|
| `[[0,1,1,1],[1,1,1,1],[0,1,1,1]]` | `15` | 10 of side 1, 4 of side 2, 1 of side 3 |
| `[[1,0,1],[1,1,0],[1,1,0]]` | `7` | 6 of side 1, 1 of side 2 |

**Constraints:** `1 ≤ m, n ≤ 300`, `matrix[i][j] ∈ {0, 1}`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: grow each square | for each top-left, extend while all ones | O(m·n·min(m,n)²) | O(1) |
| DP on the bottom-right corner | dp = 1 + min(up, left, diag); sum dp | O(m·n) | O(m·n) |

> [!tip] Interview angle
> Prove the recurrence. A side-`s` square at `(i, j)` needs side-`(s−1)` squares ending at the top, left and top-left neighbours, and the smallest of those three limits `s`. The same DP gives the Maximal Square (LC 221) answer as `max(dp)²`.

---

## 3. Brute force: grow each square

**Intuition.** For every top-left cell, try sides 1, 2, … and stop at the first failure. Checking only the new row and column keeps each extension O(side).

```python
def squares_brute(m):
    R, C, cnt = len(m), len(m[0]), 0
    for i in range(R):
        for j in range(C):
            k = 0
            while i + k < R and j + k < C and all(m[i + k][j + t] for t in range(k + 1)) and all(m[i + t][j + k] for t in range(k + 1)):
                k += 1
                cnt += 1
    return cnt
```

**Complexity:** time **O(m·n·min(m,n)²)**, space **O(1)**.

---

## 4. DP on the bottom-right corner

**Intuition.** Fill `dp` row by row. First row and column cells are `matrix[i][j]` itself, and every other 1-cell takes `1 + min` of its three neighbours. Summing as you go gives the count.

**Algorithm**

1. `dp[i][j] = matrix[i][j]` if `i == 0` or `j == 0`.
2. Else if `matrix[i][j] == 1`: `dp[i][j] = 1 + min(dp[i−1][j], dp[i][j−1], dp[i−1][j−1])`; else 0.
3. Return `Σ dp[i][j]`.

**Dry run** — [[1,0,1],[1,1,0],[1,1,0]]: dp = [[1,0,1],[1,1,0],[1,2,0]] → sum 7.

**C++**
```cpp
int countSquares(vector<vector<int>>& m) {
    int R = m.size(), C = m[0].size(), total = 0;
    vector<vector<int>> dp(R, vector<int>(C, 0));
    for (int i = 0; i < R; i++)
        for (int j = 0; j < C; j++) {
            if (m[i][j] == 0) continue;
            if (i == 0 || j == 0) dp[i][j] = 1;
            else dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
            total += dp[i][j];
        }
    return total;
}
```

**Java**
```java
static int countSquares(int[][] m) {
    int R = m.length, C = m[0].length, total = 0;
    int[][] dp = new int[R][C];
    for (int i = 0; i < R; i++)
        for (int j = 0; j < C; j++) {
            if (m[i][j] == 0) continue;
            if (i == 0 || j == 0) dp[i][j] = 1;
            else dp[i][j] = 1 + Math.min(dp[i - 1][j], Math.min(dp[i][j - 1], dp[i - 1][j - 1]));
            total += dp[i][j];
        }
    return total;
}
```

**Python**
```python
def count_squares(m):
    R, C = len(m), len(m[0])
    dp = [[0] * C for _ in range(R)]
    total = 0
    for i in range(R):
        for j in range(C):
            if m[i][j]:
                dp[i][j] = 1 if i == 0 or j == 0 else 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                total += dp[i][j]
    return total
```

**Complexity:** time **O(m·n)**, space **O(m·n)** — each cell once; can be reduced to O(n) with a rolling row plus a saved diagonal.

---

## Edge cases

- All zeros: 0.
- Single row or column: the count of 1s.
- Full `n × n` of ones: `Σ k²` for k = 1..n.

---

## Common mistakes

1. Using `max` instead of `min` of the three neighbours.
2. Counting only the largest square per cell instead of summing `dp`.

---

## Follow-ups

1. Largest all-ones square (LC 221)?
2. Largest all-ones rectangle (LC 85)?

<details><summary>Answer sketches</summary>

**#1:** `(max dp)²`.

**#2:** A different technique: histogram per row with a monotonic stack.
</details>

---

## Flashcards

**Count-squares recurrence?** #flashcard
`dp[i][j] = 1 + min(up, left, diag)` if the cell is 1.

**Why does Σ dp count all squares?** #flashcard
A max side s at a corner means squares of sides 1..s end there.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
