---
module: striver/28-dynamic-programming
lesson: 20
topic: Subset sum equals to target
difficulty: Medium
source: https://takeuforward.org/learning/dsa/subset-sum-equals-to-target?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, subsequence, knapsack]
---
# 20. Subset sum equals to target

← [Best time to buy and sell stock with cooldown](19-best-time-to-buy-and-sell-stock-with-cooldown.md) · [Part 28 index](README.md) · Next → [Partition equal subset sum](21-partition-equal-subset-sum.md)

> [!abstract] Problem at a glance
> **Task:** Decide whether some subset of the array sums exactly to `k`.
> **Key insight:** `f(i, t)` = can `a[0..i]` make `t`? Either skip `a[i]` (`f(i−1, t)`) or take it if `a[i] ≤ t` (`f(i−1, t − a[i])`). Base cases: `t == 0` → true, and `i == 0` → `a[0] == t`. The table is `n × (k+1)` booleans, and a single row is enough if you iterate `t` **downward**.
> **Difficulty:** Medium · **Pattern:** 0/1 subset DP (index, target)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/subset-sum-equals-to-target?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized (i, target)](#3-memoized-i-target) · [4. 1D tabulation, t descending](#4-1d-tabulation-t-descending) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given positive integers `arr` and a target `k`, return `true` if there is a subset whose sum is `k`.

| Input | Output | Why |
|---|---|---|
| `arr = [1,2,3,4], k = 4` | `true` | {4} or {1,3} |
| `arr = [4,3,2,1], k = 5` | `true` | {4,1} |
| `arr = [2,5,1,6,7], k = 4` | `false` |  |

**Constraints:** `1 ≤ n ≤ 10³`, `1 ≤ arr[i], k ≤ 10³`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized (i, target) | take or skip a[i] | O(n·k) | O(n·k) |
| 1D tabulation, t descending | dp[t] |= dp[t − x] | O(n·k) | O(k) |

> [!tip] Interview angle
> This is the parent of every knapsack-style problem in this section. Say "state = (index, remaining target), pick/not-pick" and draw the table. The 1D trick (iterate `t` from high to low) is what interviewers look for.

---

## 3. Memoized (i, target)

**Intuition.** `f(i, t)`: `t == 0` → true; `i == 0` → `a[0] == t`; else `f(i−1, t) or (a[i] ≤ t and f(i−1, t−a[i]))`.

```python
def ss_memo(a, k):
    n = len(a)
    dp = [[None] * (k + 1) for _ in range(n)]
    def f(i, t):
        if t == 0:
            return True
        if i == 0:
            return a[0] == t
        if dp[i][t] is None:
            dp[i][t] = f(i - 1, t) or (a[i] <= t and f(i - 1, t - a[i]))
        return dp[i][t]
    return f(n - 1, k)
```

**Complexity:** time **O(n·k)**, space **O(n·k)**.

---

## 4. 1D tabulation, t descending

**Intuition.** `dp[t]` = reachable with the items seen so far. For each item, sweep `t` from `k` down to `x` so that `dp[t − x]` still refers to the previous item set, i.e. each item is used at most once.

**Algorithm**

1. `dp = [False]*(k+1)`; `dp[0] = True`.
2. For each `x`: for `t = k..x`: `dp[t] = dp[t] or dp[t − x]`.
3. Return `dp[k]`.

**Dry run** — [2,5,1,6,7], k = 4: after 2 → {0,2}; after 5 → {0,2}; after 1 → {0,1,2,3}; 6, 7 too big → dp[4] false.

**C++**
```cpp
bool subsetSumToK(vector<int>& a, int k) {
    vector<bool> dp(k + 1, false);
    dp[0] = true;
    for (int x : a)
        for (int t = k; t >= x; t--)
            if (dp[t - x]) dp[t] = true;
    return dp[k];
}
```

**Java**
```java
static boolean subsetSumToK(int[] a, int k) {
    boolean[] dp = new boolean[k + 1];
    dp[0] = true;
    for (int x : a)
        for (int t = k; t >= x; t--)
            if (dp[t - x]) dp[t] = true;
    return dp[k];
}
```

**Python**
```python
def subset_sum_to_k(a, k):
    dp = [False] * (k + 1)
    dp[0] = True
    for x in a:
        for t in range(k, x - 1, -1):
            if dp[t - x]:
                dp[t] = True
    return dp[k]
```

**Complexity:** time **O(n·k)**, space **O(k)** — n items × k targets, one boolean row (a bitset gives /64).

---

## Edge cases

- `k` larger than the total: false.
- A single element equal to `k`: true.

---

## Common mistakes

1. Iterating `t` upward in 1D, which reuses an item (that gives unbounded subset sum).
2. Base case `i == 0` returning true whenever `a[0] ≤ t`.

---

## Follow-ups

1. Bitset speed-up?
2. Return the subset.

<details><summary>Answer sketches</summary>

**#1:** `bits |= bits << x` for each item; answer bit k. That is O(n·k/64).

**#2:** Keep the 2D table and walk back: if `dp[i−1][t]` holds, skip; else take `a[i]`.
</details>

---

## Flashcards

**Subset-sum recurrence?** #flashcard
`f(i,t) = f(i−1,t) ∨ f(i−1,t−a_i)`.

**1D 0/1 loop direction?** #flashcard
Target descending, so each item is used once.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
