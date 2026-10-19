---
module: striver/28-dynamic-programming
lesson: 21
topic: Partition equal subset sum
difficulty: Medium
source: https://takeuforward.org/learning/dsa/partition-equal-subset-sum?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, subsequence, knapsack]
---
# 21. Partition equal subset sum

← [Subset sum equals to target](20-subset-sum-equals-to-target.md) · [Part 28 index](README.md) · Next → [Partition a set into two subsets with minimum absolute sum difference](22-partition-min-absolute-sum-difference.md)

> [!abstract] Problem at a glance
> **Task:** Can the array be split into two subsets with equal sums?
> **Key insight:** Equal halves means each sums to `total/2`. So: if `total` is odd, the answer is false; otherwise it is **subset sum to total/2**. Nothing new, which is exactly why it's here: recognise the reduction.
> **Difficulty:** Medium · **Pattern:** Reduce to subset sum · **Also on:** LC 416
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/partition-equal-subset-sum?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized subset sum to total/2](#3-memoized-subset-sum-to-total2) · [4. 1D boolean DP](#4-1d-boolean-dp) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given positive integers `nums`, return `true` if you can partition them into two subsets with equal sum.

| Input | Output | Why |
|---|---|---|
| `[1,5,11,5]` | `true` | {1,5,5} and {11} |
| `[1,2,3,5]` | `false` | total 11 is odd |

**Constraints:** `1 ≤ n ≤ 200`, `1 ≤ nums[i] ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized subset sum to total/2 | parity + f(i, t) | O(n·S) | O(n·S) |
| 1D boolean DP | dp[t] |= dp[t − x], t descending | O(n·S) | O(S) |

> [!tip] Interview angle
> Lead with the reduction and the parity check; that is the whole insight. Then reuse the 1D boolean subset-sum loop.

---

## 3. Memoized subset sum to total/2

**Intuition.** Odd total → false. Else run the memoized subset-sum on `target = total/2`.

```python
def part_memo(a):
    s = sum(a)
    if s % 2:
        return False
    k = s // 2
    from functools import lru_cache
    @lru_cache(None)
    def f(i, t):
        if t == 0:
            return True
        if i < 0 or t < 0:
            return False
        return f(i - 1, t) or f(i - 1, t - a[i])
    return f(len(a) - 1, k)
```

**Complexity:** time **O(n·S)**, space **O(n·S)**.

---

## 4. 1D boolean DP

**Intuition.** Same as subset sum with target `S/2`, with an early exit when `dp[target]` becomes true.

**Algorithm**

1. If `total` is odd → false.
2. `dp[0] = true`; for each `x`, for `t = target..x`: `dp[t] |= dp[t − x]`.
3. Return `dp[target]`.

**Dry run** — [1,5,11,5], target 11: reachable after 1,5,11 includes 11 → true.

**C++**
```cpp
bool canPartition(vector<int>& a) {
    int s = 0;
    for (int x : a) s += x;
    if (s % 2) return false;
    int k = s / 2;
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
static boolean canPartition(int[] a) {
    int s = 0;
    for (int x : a) s += x;
    if (s % 2 == 1) return false;
    int k = s / 2;
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
def can_partition(a):
    s = sum(a)
    if s % 2:
        return False
    k = s // 2
    dp = [True] + [False] * k
    for x in a:
        for t in range(k, x - 1, -1):
            dp[t] = dp[t] or dp[t - x]
    return dp[k]
```

**Complexity:** time **O(n·S)**, space **O(S)** — n × S/2 boolean updates.

---

## Edge cases

- Single element: false (the other half would be empty with sum 0 ≠ x).
- Odd total: false immediately.

---

## Common mistakes

1. Missing the odd-total check.
2. Upward `t` loop (reuses items).

---

## Follow-ups

1. Partition into k equal-sum subsets (LC 698)?
2. Minimise the difference instead?

<details><summary>Answer sketches</summary>

**#1:** Bitmask DP / backtracking, not this table.

**#2:** Next problem.
</details>

---

## Flashcards

**Equal partition reduction?** #flashcard
total even and subset sum to total/2.

**Early exit?** #flashcard
Stop once dp[target] is true.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
