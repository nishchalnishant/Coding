---
module: striver-a2z/28-dynamic-programming
lesson: 24
topic: Count partitions with given difference
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-partitions-with-given-difference?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, subsequence, counting]
---
# 24. Count partitions with given difference

← [Count subsets with sum K](23-count-subsets-with-sum-k.md) · [Part 28 index](README.md) · Next → [0 and 1 Knapsack](25-0-1-knapsack.md)

> [!abstract] Problem at a glance
> **Task:** Count the ways to split the array into `S1, S2` with `sum(S1) − sum(S2) = d` (mod 10⁹+7).
> **Key insight:** `s1 − s2 = d` and `s1 + s2 = S` give `s1 = (S + d) / 2`. So the answer is **count subsets with sum (S + d)/2**, or 0 if `S + d` is odd or `d > S`.
> **Difficulty:** Medium · **Pattern:** Algebraic reduction to count subsets
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-partitions-with-given-difference?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized count to (S+d)/2](#3-memoized-count-to-sd2) · [4. 1D counting DP](#4-1d-counting-dp) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given non-negative integers `arr` and `d`, count the partitions into two subsets `S1`, `S2` (every element in exactly one) with `sum(S1) ≥ sum(S2)` and `sum(S1) − sum(S2) = d`. Return the count modulo 10⁹+7.

| Input | Output | Why |
|---|---|---|
| `arr = [5,2,6,4], d = 3` | `1` | {6,4} vs {5,2} |
| `arr = [1,1,1,1], d = 0` | `6` | C(4,2) |

**Constraints:** `1 ≤ n ≤ 50`, `0 ≤ arr[i] ≤ 50`, `0 ≤ d ≤ 2500`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized count to (S+d)/2 | validity check + count subsets | O(n·S) | O(n·S) |
| 1D counting DP | findWays(arr, (S+d)/2) | O(n·S) | O(S) |

> [!tip] Interview angle
> Write the two equations on the board and solve them. The interviewer is checking that you see the reduction, not that you invent a new DP.

---

## 3. Memoized count to (S+d)/2

**Intuition.** Reject when `S − d < 0` or `(S − d)` is odd, else count subsets summing to `(S + d)/2` with zero-safe base cases.

```python
def part_diff_memo(a, d):
    S = sum(a)
    if S - d < 0 or (S - d) % 2:
        return 0
    k = (S + d) // 2
    from functools import lru_cache
    @lru_cache(None)
    def f(i, t):
        if i < 0:
            return 1 if t == 0 else 0
        r = f(i - 1, t)
        if a[i] <= t:
            r += f(i - 1, t - a[i])
        return r % (10**9 + 7)
    return f(len(a) - 1, k)
```

**Complexity:** time **O(n·S)**, space **O(n·S)**.

---

## 4. 1D counting DP

**Intuition.** Reuse the counting loop from the previous problem.

**Algorithm**

1. `S = Σ arr`; if `S < d` or `(S + d)` odd → 0.
2. `k = (S + d)/2`; `dp[0] = 1`; for each `x`, `t = k..x`: `dp[t] += dp[t − x]`.
3. Return `dp[k]`.

**Dry run** — [5,2,6,4], d = 3: S = 17, k = 10 → subsets {6,4} only → 1.

**C++**
```cpp
int countPartitions(vector<int>& a, int d) {
    const int MOD = 1e9 + 7;
    int S = 0;
    for (int x : a) S += x;
    if (S < d || (S + d) % 2) return 0;
    int k = (S + d) / 2;
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
static int countPartitions(int[] a, int d) {
    final int MOD = 1_000_000_007;
    int S = 0;
    for (int x : a) S += x;
    if (S < d || (S + d) % 2 == 1) return 0;
    int k = (S + d) / 2;
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
def count_partitions(a, d):
    MOD = 10**9 + 7
    S = sum(a)
    if S < d or (S + d) % 2:
        return 0
    k = (S + d) // 2
    dp = [1] + [0] * k
    for x in a:
        for t in range(k, x - 1, -1):
            dp[t] = (dp[t] + dp[t - x]) % MOD
    return dp[k]
```

**Complexity:** time **O(n·S)**, space **O(S)** — one counting DP to a single target.

---

## Edge cases

- `d > S`: 0.
- `S + d` odd: 0.
- Zeros: each doubles the count.

---

## Common mistakes

1. Targeting `(S − d)/2` vs `(S + d)/2`: both give the same count (complements), but don't mix them.
2. Skipping the parity check.

---

## Follow-ups

1. Target sum with ± signs?
2. Difference at most d?

<details><summary>Answer sketches</summary>

**#1:** Identical maths: `+` group minus `−` group = target (LC 494).

**#2:** Sum counts over all valid s1.
</details>

---

## Flashcards

**Partition-difference reduction?** #flashcard
Count subsets with sum (S + d)/2.

**When is the answer 0 immediately?** #flashcard
d > S or S + d is odd.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
