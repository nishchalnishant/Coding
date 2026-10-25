---
module: striver-a2z/28-dynamic-programming
lesson: 25
topic: 0 and 1 Knapsack
difficulty: Medium
source: https://takeuforward.org/learning/dsa/0-and-1-knapsack?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, knapsack]
---
# 25. 0 and 1 Knapsack

← [Count partitions with given difference](24-count-partitions-with-given-difference.md) · [Part 28 index](README.md) · Next → [Minimum coins](26-minimum-coins.md)

> [!abstract] Problem at a glance
> **Task:** Pick items (each at most once) with total weight ≤ `W` to maximise total value.
> **Key insight:** `dp[i][w] = max(dp[i−1][w], val[i] + dp[i−1][w − wt[i]])`. It is subset sum with values: the boolean OR becomes a max. One row suffices with `w` **descending**. Greedy by value/weight ratio is wrong for 0/1 items (it is right only for the fractional version).
> **Difficulty:** Medium · **Pattern:** 0/1 knapsack
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/0-and-1-knapsack?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized (i, capacity)](#3-memoized-i-capacity) · [4. 1D tabulation, w descending](#4-1d-tabulation-w-descending) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `wt[i]`, `val[i]` for `n` items and capacity `W`, choose a subset with total weight ≤ `W` maximising total value. Each item is used at most once.

| Input | Output | Why |
|---|---|---|
| `wt = [1,2,4,5], val = [5,4,8,6], W = 5` | `13` | items 0 and 2 |
| `wt = [10,20,30], val = [60,100,120], W = 50` | `220` | items 1 and 2 (greedy by ratio gives 160) |

**Constraints:** `1 ≤ n ≤ 10³`, `1 ≤ W ≤ 10³`, `1 ≤ wt[i], val[i] ≤ 10³`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized (i, capacity) | max(skip, take) | O(n·W) | O(n·W) |
| 1D tabulation, w descending | dp[w] = max(dp[w], v + dp[w − wt]) | O(n·W) | O(W) |

> [!tip] Interview angle
> Show the ratio-greedy counter-example, then write the 2D recurrence and collapse it. Explain the descending loop: "`dp[w − wt]` must still be the value **without** this item."

---

## 3. Memoized (i, capacity)

**Intuition.** `f(i, w)`: `i < 0` → 0. Skip: `f(i−1, w)`; take if `wt[i] ≤ w`: `val[i] + f(i−1, w − wt[i])`.

```python
def knap_memo(wt, val, W):
    n = len(wt)
    dp = [[-1] * (W + 1) for _ in range(n)]
    def f(i, w):
        if i < 0:
            return 0
        if dp[i][w] == -1:
            best = f(i - 1, w)
            if wt[i] <= w:
                best = max(best, val[i] + f(i - 1, w - wt[i]))
            dp[i][w] = best
        return dp[i][w]
    return f(n - 1, W)
```

**Complexity:** time **O(n·W)**, space **O(n·W)**.

---

## 4. 1D tabulation, w descending

**Intuition.** `dp[w]` = best value with capacity `w` using items so far. A descending sweep keeps each item single-use.

**Algorithm**

1. `dp = [0]*(W+1)`.
2. For each item `(wi, vi)`: for `w = W..wi`: `dp[w] = max(dp[w], vi + dp[w − wi])`.
3. Return `dp[W]`.

**Dry run** — wt [1,2,4,5], val [5,4,8,6], W 5: after item 0 → all 5; after item 1 → dp[3..5] = 9; after item 2 → dp[5] = 13.

**C++**
```cpp
int knapsack(vector<int>& wt, vector<int>& val, int W) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < (int)wt.size(); i++)
        for (int w = W; w >= wt[i]; w--)
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]]);
    return dp[W];
}
```

**Java**
```java
static int knapsack(int[] wt, int[] val, int W) {
    int[] dp = new int[W + 1];
    for (int i = 0; i < wt.length; i++)
        for (int w = W; w >= wt[i]; w--)
            dp[w] = Math.max(dp[w], val[i] + dp[w - wt[i]]);
    return dp[W];
}
```

**Python**
```python
def knapsack(wt, val, W):
    dp = [0] * (W + 1)
    for wi, vi in zip(wt, val):
        for w in range(W, wi - 1, -1):
            dp[w] = max(dp[w], vi + dp[w - wi])
    return dp[W]
```

**Complexity:** time **O(n·W)**, space **O(W)** — n × W updates, one row.

---

## Edge cases

- No item fits: 0.
- `W` large enough for everything: the sum of values.

---

## Common mistakes

1. Ascending `w` (turns into unbounded knapsack).
2. Greedy by ratio.

---

## Follow-ups

1. W up to 10⁹ but values small?
2. Reconstruct the chosen items.

<details><summary>Answer sketches</summary>

**#1:** Swap roles: `dp[value] = min weight`, answer = max value with weight ≤ W.

**#2:** Keep the 2D table; item i was taken if `dp[i][w] ≠ dp[i−1][w]`.
</details>

---

## Flashcards

**0/1 knapsack recurrence?** #flashcard
`dp[i][w] = max(dp[i−1][w], v_i + dp[i−1][w−w_i])`.

**Large W, small values?** #flashcard
DP over value: min weight to reach each value.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
