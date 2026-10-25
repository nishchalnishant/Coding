---
module: striver-a2z/28-dynamic-programming
lesson: 29
topic: Unbounded knapsack
difficulty: Medium
source: https://takeuforward.org/learning/dsa/unbounded-knapsack?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, knapsack, unbounded]
---
# 29. Unbounded knapsack

← [Coin change II](28-coin-change-ii.md) · [Part 28 index](README.md) · Next → [Rod cutting problem](30-rod-cutting-problem.md)

> [!abstract] Problem at a glance
> **Task:** Knapsack where each item may be taken any number of times.
> **Key insight:** Identical to 0/1 knapsack except taking stays at `i`: `dp[i][w] = max(dp[i−1][w], v_i + dp[i][w − wt_i])`. In 1D, the only change is that the capacity loop runs **ascending**. Loop direction is the entire difference between 0/1 and unbounded.
> **Difficulty:** Medium · **Pattern:** Unbounded knapsack (max)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/unbounded-knapsack?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized (i, capacity)](#3-memoized-i-capacity) · [4. 1D tabulation, capacity ascending](#4-1d-tabulation-capacity-ascending) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `wt`, `val` for `n` item types and capacity `W`, maximise total value with total weight ≤ `W`, using any number of copies of each item.

| Input | Output | Why |
|---|---|---|
| `wt = [2,4,6], val = [5,11,13], W = 10` | `27` | 4+4+2 → 11+11+5 |
| `wt = [1,3,4,5], val = [10,40,50,70], W = 8` | `110` | 5+3 → 70+40 |

**Constraints:** `1 ≤ n, W ≤ 10³`, `1 ≤ wt[i], val[i] ≤ 10³`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized (i, capacity) | take → f(i, w − wt_i) | O(n·W) | O(n·W) |
| 1D tabulation, capacity ascending | dp[w] = max(dp[w], v + dp[w − wt]) | O(n·W) | O(W) |

> [!tip] Interview angle
> Put 0/1 and unbounded side by side and point at the one changed loop bound. That contrast is the takeaway of this group.

---

## 3. Memoized (i, capacity)

**Intuition.** `f(0, w) = (w / wt0) · val0`. Otherwise `max(f(i−1, w), val_i + f(i, w − wt_i))`.

```python
def unb_memo(wt, val, W):
    from functools import lru_cache
    @lru_cache(None)
    def f(i, w):
        if i == 0:
            return (w // wt[0]) * val[0]
        best = f(i - 1, w)
        if wt[i] <= w:
            best = max(best, val[i] + f(i, w - wt[i]))
        return best
    return f(len(wt) - 1, W)
```

**Complexity:** time **O(n·W)**, space **O(n·W)**.

---

## 4. 1D tabulation, capacity ascending

**Intuition.** Same as 0/1, but sweeping upward lets `dp[w − wt]` already contain this item.

**Algorithm**

1. `dp = [0]*(W+1)`.
2. For each item: for `w = wt..W`: `dp[w] = max(dp[w], val + dp[w − wt])`.
3. Return `dp[W]`.

**Dry run** — wt [2,4,6], val [5,11,13], W 10: after item 0 → dp[10] = 25; after item 1 → dp[8] = 22, dp[10] = 27.

**C++**
```cpp
int unboundedKnapsack(vector<int>& wt, vector<int>& val, int W) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < (int)wt.size(); i++)
        for (int w = wt[i]; w <= W; w++)
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]]);
    return dp[W];
}
```

**Java**
```java
static int unboundedKnapsack(int[] wt, int[] val, int W) {
    int[] dp = new int[W + 1];
    for (int i = 0; i < wt.length; i++)
        for (int w = wt[i]; w <= W; w++)
            dp[w] = Math.max(dp[w], val[i] + dp[w - wt[i]]);
    return dp[W];
}
```

**Python**
```python
def unbounded_knapsack(wt, val, W):
    dp = [0] * (W + 1)
    for wi, vi in zip(wt, val):
        for w in range(wi, W + 1):
            dp[w] = max(dp[w], vi + dp[w - wi])
    return dp[W]
```

**Complexity:** time **O(n·W)**, space **O(W)** — n × W, one row.

---

## Edge cases

- No item fits: 0.
- One item: `⌊W/wt⌋·val`.

---

## Common mistakes

1. Descending loop (that gives 0/1).
2. Base case at `i == 0` returning `val0` once instead of `⌊w/wt0⌋` copies.

---

## Follow-ups

1. Rod cutting?
2. Minimum weight to reach at least value V?

<details><summary>Answer sketches</summary>

**#1:** Next problem, the same DP with `wt = length`.

**#2:** Swap roles: dp over value.
</details>

---

## Flashcards

**0/1 vs unbounded in 1D?** #flashcard
Descending vs ascending capacity loop.

**Unbounded take transition (2D)?** #flashcard
Stay at i: `v_i + dp[i][w − w_i]`.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
