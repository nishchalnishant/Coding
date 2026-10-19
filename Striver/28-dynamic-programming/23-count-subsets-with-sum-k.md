---
module: striver/28-dynamic-programming
lesson: 23
topic: Count subsets with sum K
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-subsets-with-sum-k?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, subsequence, counting]
---
# 23. Count subsets with sum K

← [Partition a set into two subsets with minimum absolute sum difference](22-partition-min-absolute-sum-difference.md) · [Part 28 index](README.md) · Next → [Count partitions with given difference](24-count-partitions-with-given-difference.md)

> [!abstract] Problem at a glance
> **Task:** Count the subsets summing to `k` (mod 10⁹+7). Elements may be 0.
> **Key insight:** Turn the boolean OR into a sum: `dp[i][t] = dp[i−1][t] + dp[i−1][t − a[i]]`. **Zeros** are the trap: a 0 can be taken or skipped, doubling the count. So the base case must not stop early at `t == 0`. Start from `dp[0] = 1` (the empty set) and process every element, including zeros.
> **Difficulty:** Medium · **Pattern:** Count subsets (index, target)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-subsets-with-sum-k?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized count](#3-memoized-count) · [4. 1D counting DP](#4-1d-counting-dp) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given non-negative integers `arr` and `k`, return the number of subsets (by index) whose sum equals `k`, modulo 10⁹+7.

| Input | Output | Why |
|---|---|---|
| `arr = [1,2,2,3], k = 3` | `3` | {1,2}, {1,2'}, {3} |
| `arr = [0,0,1], k = 1` | `4` | zeros double the count twice |

**Constraints:** `1 ≤ n ≤ 100`, `0 ≤ arr[i] ≤ 10³`, `1 ≤ k ≤ 10³`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized count | f(i, t) = skip + take, base at i < 0 | O(n·k) | O(n·k) |
| 1D counting DP | dp[t] += dp[t − x], t descending | O(n·k) | O(k) |

> [!tip] Interview angle
> Say up front how zeros are handled. The classic bug is `if t == 0: return 1` before checking the remaining elements, which undercounts subsets that include zeros.

---

## 3. Memoized count

**Intuition.** Recurse to `i = −1` and return `1 if t == 0 else 0` there. Since nothing short-circuits at `t == 0`, zeros are counted correctly.

```python
def cnt_memo(a, k):
    from functools import lru_cache
    MOD = 10**9 + 7
    @lru_cache(None)
    def f(i, t):
        if i < 0:
            return 1 if t == 0 else 0
        res = f(i - 1, t)
        if a[i] <= t:
            res += f(i - 1, t - a[i])
        return res % MOD
    return f(len(a) - 1, k)
```

**Complexity:** time **O(n·k)**, space **O(n·k)**.

---

## 4. 1D counting DP

**Intuition.** `dp[0] = 1` (the empty subset). For each `x` (including 0), sweep `t` downward: `dp[t] += dp[t − x]`. For `x = 0` this doubles every entry, as it should.

**Algorithm**

1. `dp = [1, 0, …, 0]`.
2. For each `x`: for `t = k..x`: `dp[t] = (dp[t] + dp[t−x]) % MOD`.
3. Return `dp[k]`.

**Dry run** — [0,0,1], k = 1: after 0 → [2,0]; after 0 → [4,0]; after 1 → [4,4] → 4.

**C++**
```cpp
int findWays(vector<int>& a, int k) {
    const int MOD = 1e9 + 7;
    vector<int> dp(k + 1, 0);
    dp[0] = 1;
    for (int x : a)
        for (int t = k; t >= x; t--)
            dp[t] = (dp[t] + dp[t - x]) % MOD;
    return dp[k];
}
```

**Java**
```java
static int findWays(int[] a, int k) {
    final int MOD = 1_000_000_007;
    int[] dp = new int[k + 1];
    dp[0] = 1;
    for (int x : a)
        for (int t = k; t >= x; t--)
            dp[t] = (dp[t] + dp[t - x]) % MOD;
    return dp[k];
}
```

**Python**
```python
def find_ways(a, k):
    MOD = 10**9 + 7
    dp = [1] + [0] * k
    for x in a:
        for t in range(k, x - 1, -1):
            dp[t] = (dp[t] + dp[t - x]) % MOD
    return dp[k]
```

**Complexity:** time **O(n·k)**, space **O(k)** — n × k additions; the `t ≥ x` loop with x = 0 covers t = k..0 in place, which is safe because dp[t − 0] is dp[t] itself (doubling).

---

## Edge cases

- Zeros in the array: each one doubles the count.
- No subset possible: 0.

---

## Common mistakes

1. Returning 1 as soon as `t == 0`, which ignores zeros left to process.
2. Forgetting the modulus on intermediate sums.

---

## Follow-ups

1. Count partitions with a given difference?
2. Count with each element usable unlimited times?

<details><summary>Answer sketches</summary>

**#1:** Next problem: reduce to counting subsets with sum `(S + d)/2`.

**#2:** Ascending `t` loop (coin change II).
</details>

---

## Flashcards

**Count-subsets base case?** #flashcard
At `i < 0`: `t == 0 ? 1 : 0`, so zeros are counted.

**Effect of a zero element?** #flashcard
It doubles every count.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
