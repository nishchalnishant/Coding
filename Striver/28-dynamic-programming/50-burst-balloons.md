---
module: striver/28-dynamic-programming
lesson: 50
topic: Burst balloons
difficulty: Hard
source: https://takeuforward.org/learning/dsa/burst-balloons?category=mcm-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, partition-dp, interval]
---
# 50. Burst balloons

← [Minimum cost to cut the stick](49-minimum-cost-to-cut-the-stick.md) · [Part 28 index](README.md) · Next → [Evaluate boolean expression to true](51-evaluate-boolean-expression-to-true.md)

> [!abstract] Problem at a glance
> **Task:** Burst all balloons in the best order; bursting `i` earns `left · nums[i] · right` with its current neighbours.
> **Key insight:** Choosing the **first** balloon to burst breaks independence, because neighbours change. Choose the **last** balloon `k` to burst in `(i, j)` instead. When it pops, its neighbours are the fixed boundaries `a[i−1]` and `a[j+1]`, and the two sides were cleared independently: `f(i, j) = max_k a[i−1]·a[k]·a[j+1] + f(i, k−1) + f(k+1, j)`.
> **Difficulty:** Hard · **Pattern:** Partition DP (last-to-burst) · **Also on:** LC 312
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/burst-balloons?category=mcm-dp&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized f(i, j), last balloon k](#3-memoized-fi-j-last-balloon-k) · [4. Bottom-up interval table](#4-bottom-up-interval-table) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums`, burst every balloon. Bursting balloon `i` gains `nums[i−1] · nums[i] · nums[i+1]`, where out-of-range neighbours count as 1. Return the maximum total.

| Input | Output | Why |
|---|---|---|
| `[3,1,5,8]` | `167` | burst 1, 5, 3, 8: 15 + 120 + 24 + 8 |
| `[1,5]` | `10` |  |

**Constraints:** `1 ≤ n ≤ 300`, `0 ≤ nums[i] ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized f(i, j), last balloon k | pad with 1s; max over k | O(n³) | O(n²) |
| Bottom-up interval table | i descending, j ascending | O(n³) | O(n²) |

> [!tip] Interview angle
> The decisive line is: "I pick the last balloon in the range, because then its neighbours are known." Pad with 1 on both ends. This is the classic reversal trick for partition DP.

---

## 3. Memoized f(i, j), last balloon k

**Intuition.** `f(i, j) = 0` if `i > j`.

```python
def burst_memo(nums):
    a = [1] + nums + [1]
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if i > j:
            return 0
        return max(a[i - 1] * a[k] * a[j + 1] + f(i, k - 1) + f(k + 1, j) for k in range(i, j + 1))
    return f(1, len(nums))
```

**Complexity:** time **O(n³)**, space **O(n²)**.

---

## 4. Bottom-up interval table

**Intuition.** `dp[i][j]` over 1-indexed padded positions. `dp[i][k−1]` and `dp[k+1][j]` are ready under this order.

**Algorithm**

1. `a = [1] + nums + [1]`, `dp` of size `(n+2)²`.
2. For `i = n..1`, `j = i..n`: `dp[i][j] = max over k` of `a[i−1]·a[k]·a[j+1] + dp[i][k−1] + dp[k+1][j]`.
3. Return `dp[1][n]`.

**Dry run** — [3,1,5,8]: dp[1][4] picks 8 last: 1·8·1 + dp[1][3] (159) = 167.

**C++**
```cpp
int maxCoins(vector<int>& nums) {
    int n = nums.size();
    vector<int> a(n + 2, 1);
    for (int i = 0; i < n; i++) a[i + 1] = nums[i];
    vector<vector<int>> dp(n + 2, vector<int>(n + 2, 0));
    for (int i = n; i >= 1; i--)
        for (int j = i; j <= n; j++)
            for (int k = i; k <= j; k++)
                dp[i][j] = max(dp[i][j], a[i - 1] * a[k] * a[j + 1] + dp[i][k - 1] + dp[k + 1][j]);
    return dp[1][n];
}
```

**Java**
```java
static int maxCoins(int[] nums) {
    int n = nums.length;
    int[] a = new int[n + 2];
    a[0] = a[n + 1] = 1;
    for (int i = 0; i < n; i++) a[i + 1] = nums[i];
    int[][] dp = new int[n + 2][n + 2];
    for (int i = n; i >= 1; i--)
        for (int j = i; j <= n; j++)
            for (int k = i; k <= j; k++)
                dp[i][j] = Math.max(dp[i][j], a[i - 1] * a[k] * a[j + 1] + dp[i][k - 1] + dp[k + 1][j]);
    return dp[1][n];
}
```

**Python**
```python
def max_coins(nums):
    n = len(nums)
    a = [1] + nums + [1]
    dp = [[0] * (n + 2) for _ in range(n + 2)]
    for i in range(n, 0, -1):
        for j in range(i, n + 1):
            dp[i][j] = max(a[i - 1] * a[k] * a[j + 1] + dp[i][k - 1] + dp[k + 1][j] for k in range(i, j + 1))
    return dp[1][n]
```

**Complexity:** time **O(n³)**, space **O(n²)** — O(n²) intervals × O(n) choices of the last balloon.

---

## Edge cases

- Single balloon: `nums[0]`.
- Zeros are allowed: they still have to be burst.

---

## Common mistakes

1. Choosing the first balloon to burst (the subproblems aren't independent).
2. Using `a[k−1]·a[k]·a[k+1]` instead of the interval boundaries.

---

## Follow-ups

1. Why do the boundaries survive?
2. Print the order.

<details><summary>Answer sketches</summary>

**#1:** `k` is last in `(i, j)`, so everything between was popped and only `a[i−1]` and `a[j+1]` remain beside it.

**#2:** Store argmax k; output a post-order (left part, right part, then k).
</details>

---

## Flashcards

**Burst balloons trick?** #flashcard
Choose the LAST balloon in the interval; its neighbours are the fixed boundaries.

**Burst balloons gain for last k in (i, j)?** #flashcard
a[i−1] · a[k] · a[j+1].

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
