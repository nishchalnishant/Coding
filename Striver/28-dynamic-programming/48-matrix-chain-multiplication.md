---
module: striver/28-dynamic-programming
lesson: 48
topic: Matrix chain multiplication
difficulty: Hard
source: https://takeuforward.org/learning/dsa/matrix-chain-multiplication?category=mcm-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, partition-dp, interval]
---
# 48. Matrix chain multiplication

← [Count palindromic subsequences](47-count-palindromic-subsequences.md) · [Part 28 index](README.md) · Next → [Minimum cost to cut the stick](49-minimum-cost-to-cut-the-stick.md)

> [!abstract] Problem at a glance
> **Task:** Minimum scalar multiplications to compute the product of a chain of matrices.
> **Key insight:** Matrix `i` is `arr[i−1] × arr[i]`. `f(i, j)` = cheapest way to multiply matrices `i..j`. The **last** multiplication splits the chain at some `k`: `(i..k)(k+1..j)` costs `arr[i−1]·arr[k]·arr[j]` plus both halves. Try every `k`. This is the template for every partition DP: **interval state, loop over the split point**.
> **Difficulty:** Hard · **Pattern:** Partition DP (MCM template)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/matrix-chain-multiplication?category=mcm-dp&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized f(i, j)](#3-memoized-fi-j) · [4. Bottom-up interval table](#4-bottom-up-interval-table) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `arr` of length `n` where matrix `i` (1-indexed, `1 ≤ i < n`) has dimensions `arr[i−1] × arr[i]`, return the minimum number of scalar multiplications needed to multiply all `n − 1` matrices.

| Input | Output | Why |
|---|---|---|
| `[10,20,30,40,50]` | `38000` | ((AB)C)D |
| `[4,2,3]` | `24` | a single product |
| `[10,15,20,25]` | `8000` |  |

**Constraints:** `2 ≤ n ≤ 100`, `1 ≤ arr[i] ≤ 500`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized f(i, j) | min over split k | O(n³) | O(n²) |
| Bottom-up interval table | i from n−1 down, j from i+1 up | O(n³) | O(n²) |

> [!tip] Interview angle
> Say the four partition-DP steps: (1) state `f(i, j)` over a contiguous block, (2) base case for a single item, (3) loop `k` over every split, (4) combine as cost(split) + f(left) + f(right). Tabulate with `i` descending and `j` ascending, or by increasing interval length.

---

## 3. Memoized f(i, j)

**Intuition.** `f(i, i) = 0`. Otherwise `min over k in [i, j)` of `arr[i−1]·arr[k]·arr[j] + f(i, k) + f(k+1, j)`.

```python
def mcm_memo(arr):
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if i == j:
            return 0
        return min(arr[i - 1] * arr[k] * arr[j] + f(i, k) + f(k + 1, j) for k in range(i, j))
    return f(1, len(arr) - 1)
```

**Complexity:** time **O(n³)**, space **O(n²)**.

---

## 4. Bottom-up interval table

**Intuition.** `dp[i][j]` depends on `dp[i][k]` (same row, smaller `j`) and `dp[k+1][j]` (later row), so fill `i` descending and `j` ascending.

**Algorithm**

1. `dp[i][i] = 0`.
2. For `i = n−1..1`, `j = i+1..n−1`: `dp[i][j] = min over k` of `arr[i−1]·arr[k]·arr[j] + dp[i][k] + dp[k+1][j]`.
3. Return `dp[1][n−1]`.

**Dry run** — [10,20,30,40,50]: dp[1][2] = 6000, dp[1][3] = 18000, dp[1][4] = 38000.

**C++**
```cpp
int matrixMultiplication(vector<int>& arr) {
    int n = arr.size();
    vector<vector<int>> dp(n, vector<int>(n, 0));
    for (int i = n - 1; i >= 1; i--)
        for (int j = i + 1; j < n; j++) {
            int best = INT_MAX;
            for (int k = i; k < j; k++)
                best = min(best, arr[i - 1] * arr[k] * arr[j] + dp[i][k] + dp[k + 1][j]);
            dp[i][j] = best;
        }
    return dp[1][n - 1];
}
```

**Java**
```java
static int matrixMultiplication(int[] arr) {
    int n = arr.length;
    int[][] dp = new int[n][n];
    for (int i = n - 1; i >= 1; i--)
        for (int j = i + 1; j < n; j++) {
            int best = Integer.MAX_VALUE;
            for (int k = i; k < j; k++)
                best = Math.min(best, arr[i - 1] * arr[k] * arr[j] + dp[i][k] + dp[k + 1][j]);
            dp[i][j] = best;
        }
    return dp[1][n - 1];
}
```

**Python**
```python
def matrix_multiplication(arr):
    n = len(arr)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, 0, -1):
        for j in range(i + 1, n):
            dp[i][j] = min(arr[i - 1] * arr[k] * arr[j] + dp[i][k] + dp[k + 1][j] for k in range(i, j))
    return dp[1][n - 1]
```

**Complexity:** time **O(n³)**, space **O(n²)** — O(n²) intervals × O(n) splits.

---

## Edge cases

- `n = 2` (one matrix): 0.
- Watch overflow for large dimensions (use 64-bit if `arr[i]` can be ~10³).

---

## Common mistakes

1. Indexing matrices from 0 and getting `arr[i−1]` wrong.
2. Filling `i` ascending (reads `dp[k+1][j]` before it exists).

---

## Follow-ups

1. Print the parenthesisation.
2. Faster?

<details><summary>Answer sketches</summary>

**#1:** Store `split[i][j] = argmin k` and recurse: `(` + print(i, k) + print(k+1, j) + `)`.

**#2:** Hu–Shing is O(n log n), but it is not interview material. Knuth's optimisation does not apply directly.
</details>

---

## Flashcards

**Partition DP template?** #flashcard
f(i, j) = best over k in [i, j) of cost(i, k, j) + f(i, k) + f(k+1, j).

**MCM split cost?** #flashcard
arr[i−1] · arr[k] · arr[j].

**MCM fill order?** #flashcard
i descending, j ascending (or by interval length).

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
