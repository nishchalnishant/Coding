---
module: striver-a2z/28-dynamic-programming
lesson: 49
topic: Minimum cost to cut the stick
difficulty: Hard
source: https://takeuforward.org/learning/dsa/minimum-cost-to-cut-the-stick?category=mcm-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, partition-dp, interval]
---
# 49. Minimum cost to cut the stick

← [Matrix chain multiplication](48-matrix-chain-multiplication.md) · [Part 28 index](README.md) · Next → [Burst balloons](50-burst-balloons.md)

> [!abstract] Problem at a glance
> **Task:** Order the given cuts on a stick of length `n` so the total cost (each cut costs its piece's length) is minimal.
> **Key insight:** Sort the cuts and add the endpoints `0` and `n`. Then `f(i, j)` = min cost to make all cuts strictly between `c[i]` and `c[j]`. The **first** cut `k` in that piece costs `c[j] − c[i]` and splits it into two independent pieces: `f(i, j) = (c[j] − c[i]) + min_k f(i, k) + f(k, j)`.
> **Difficulty:** Hard · **Pattern:** Partition DP · **Also on:** LC 1547
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-cost-to-cut-the-stick?category=mcm-dp&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized f(i, j) over sorted cuts](#3-memoized-fi-j-over-sorted-cuts) · [4. Bottom-up interval table](#4-bottom-up-interval-table) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A stick of length `n` has positions `0..n`. Given `cuts`, perform all cuts in any order; each costs the length of the stick being cut. Return the minimum total cost.

| Input | Output | Why |
|---|---|---|
| `n = 7, cuts = [1,3,4,5]` | `16` | order 3, 5, 1, 4 |
| `n = 9, cuts = [5,6,1,4,2]` | `22` |  |

**Constraints:** `2 ≤ n ≤ 10⁶`, `1 ≤ |cuts| ≤ min(n − 1, 100)`, distinct.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized f(i, j) over sorted cuts | first cut k inside (c[i], c[j]) | O(m³) | O(m²) |
| Bottom-up interval table | by increasing gap j − i | O(m³) | O(m²) |

> [!tip] Interview angle
> Explain why sorting is needed: after sorting, the cuts inside a piece form a contiguous index range, so the state is two indices. Without sorting, the subproblems are not independent intervals.

---

## 3. Memoized f(i, j) over sorted cuts

**Intuition.** Pad with 0 and n; `f(i, j) = 0` when `j = i + 1`.

```python
def cut_memo(n, cuts):
    c = [0] + sorted(cuts) + [n]
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if j - i < 2:
            return 0
        return c[j] - c[i] + min(f(i, k) + f(k, j) for k in range(i + 1, j))
    return f(0, len(c) - 1)
```

**Complexity:** time **O(m³)**, space **O(m²)**.

---

## 4. Bottom-up interval table

**Intuition.** Same recurrence. Fill `i` descending and `j` from `i + 2` upward.

**Algorithm**

1. `c = [0] + sorted(cuts) + [n]`.
2. For `i = m−1..0`, `j = i+2..m+1`: `dp[i][j] = c[j] − c[i] + min over k in (i, j)` of `dp[i][k] + dp[k][j]`.
3. Return `dp[0][m+1]`.

**Dry run** — n = 7, c = [0,1,3,4,5,7]: dp[0][5] = 7 + min(...) = 7 + 9 = 16.

**C++**
```cpp
int minCost(int n, vector<int>& cuts) {
    vector<int> c = cuts;
    c.push_back(0);
    c.push_back(n);
    sort(c.begin(), c.end());
    int m = c.size();
    vector<vector<int>> dp(m, vector<int>(m, 0));
    for (int i = m - 1; i >= 0; i--)
        for (int j = i + 2; j < m; j++) {
            int best = INT_MAX;
            for (int k = i + 1; k < j; k++) best = min(best, dp[i][k] + dp[k][j]);
            dp[i][j] = best + c[j] - c[i];
        }
    return dp[0][m - 1];
}
```

**Java**
```java
static int minCost(int n, int[] cuts) {
    int m = cuts.length + 2;
    int[] c = new int[m];
    for (int i = 0; i < cuts.length; i++) c[i + 1] = cuts[i];
    c[m - 1] = n;
    Arrays.sort(c);
    int[][] dp = new int[m][m];
    for (int i = m - 1; i >= 0; i--)
        for (int j = i + 2; j < m; j++) {
            int best = Integer.MAX_VALUE;
            for (int k = i + 1; k < j; k++) best = Math.min(best, dp[i][k] + dp[k][j]);
            dp[i][j] = best + c[j] - c[i];
        }
    return dp[0][m - 1];
}
```

**Python**
```python
def min_cost(n, cuts):
    c = [0] + sorted(cuts) + [n]
    m = len(c)
    dp = [[0] * m for _ in range(m)]
    for i in range(m - 1, -1, -1):
        for j in range(i + 2, m):
            dp[i][j] = c[j] - c[i] + min(dp[i][k] + dp[k][j] for k in range(i + 1, j))
    return dp[0][m - 1]
```

**Complexity:** time **O(m³)**, space **O(m²)** — m = |cuts| + 2 points, O(m²) intervals × O(m) splits, independent of n.

---

## Edge cases

- One cut: n.
- Unsorted input: sort first.

---

## Common mistakes

1. DP over positions `0..n` (n up to 10⁶): use cut indices.
2. Forgetting the 0 and n sentinels.

---

## Follow-ups

1. Why "first cut" and not "last"?
2. Merge stones (LC 1000)?

<details><summary>Answer sketches</summary>

**#1:** The first cut's cost is the current piece length, which the interval knows.

**#2:** Same interval idea in reverse (merging), with a K-way constraint.
</details>

---

## Flashcards

**Cut the stick state?** #flashcard
f(i, j) over sorted cuts padded with 0 and n.

**Cut cost added?** #flashcard
c[j] − c[i], the current piece length.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
