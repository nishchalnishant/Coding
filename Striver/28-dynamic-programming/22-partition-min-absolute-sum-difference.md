---
module: striver/28-dynamic-programming
lesson: 22
topic: Partition a set into two subsets with minimum absolute sum difference
difficulty: Hard
source: https://takeuforward.org/learning/dsa/partition-a-set-into-two-subsets-with-minimum-absolute-sum-difference?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, subsequence, knapsack]
---
# 22. Partition a set into two subsets with minimum absolute sum difference

← [Partition equal subset sum](21-partition-equal-subset-sum.md) · [Part 28 index](README.md) · Next → [Count subsets with sum K](23-count-subsets-with-sum-k.md)

> [!abstract] Problem at a glance
> **Task:** Split non-negative numbers into two groups minimising `|sum1 − sum2|`.
> **Key insight:** If one group sums to `s1`, the other is `S − s1`, and the difference is `|S − 2·s1|`. Build the subset-sum reachability row for all `t ∈ [0, S]` and pick the reachable `s1 ≤ S/2` closest to `S/2`. **The last row of the subset-sum table answers every target at once.**
> **Difficulty:** Hard · **Pattern:** Subset-sum table, scan the last row
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/partition-a-set-into-two-subsets-with-minimum-absolute-sum-difference?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Enumerate subset sums](#3-enumerate-subset-sums) · [4. Boolean row + scan](#4-boolean-row--scan) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given non-negative integers `arr`, partition them into two subsets (each element in exactly one) to minimise the absolute difference of their sums. Return that minimum.

| Input | Output | Why |
|---|---|---|
| `[1,6,11,5]` | `1` | {1,5,6} = 12 vs {11} |
| `[3,1,4,2,2,1]` | `1` | total 13, best half 6 |
| `[1,2,3,4]` | `0` |  |

**Constraints:** `1 ≤ n ≤ 10³`, `0 ≤ arr[i]`, `Σ arr ≤ 10⁴`. (LC 2035 allows negatives and needs meet-in-the-middle instead.)

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Enumerate subset sums | set of all reachable sums | O(n·S) | O(S) |
| Boolean row + scan | dp[t] for t ≤ S/2, take the largest true | O(n·S) | O(S) |

> [!tip] Interview angle
> Point out the restriction: the DP needs non-negative values with a small total. For LC 2035 (negatives, n ≤ 30) say "meet in the middle" and don't try to force this table.

---

## 3. Enumerate subset sums

**Intuition.** Grow a set of reachable sums item by item, then minimise `|S − 2s|`.

```python
def mindiff_set(a):
    reach = {0}
    for x in a:
        reach |= {s + x for s in reach}
    tot = sum(a)
    return min(abs(tot - 2 * s) for s in reach)
```

**Complexity:** time **O(n·S)**, space **O(S)**.

---

## 4. Boolean row + scan

**Intuition.** Only `s1 ≤ S/2` matters (the complement covers the rest), so build `dp[0..S/2]` and scan down from `S/2` for the first reachable sum.

**Algorithm**

1. `half = S/2`; `dp[0] = true`.
2. For each `x`: for `t = half..x`: `dp[t] |= dp[t − x]`.
3. Find the largest `t ≤ half` with `dp[t]`; return `S − 2t`.

**Dry run** — [1,6,11,5]: S = 23, half = 11; reachable includes 11 → 23 − 22 = 1.

**C++**
```cpp
int minSubsetSumDifference(vector<int>& a) {
    int S = 0;
    for (int x : a) S += x;
    int half = S / 2;
    vector<bool> dp(half + 1, false);
    dp[0] = true;
    for (int x : a)
        for (int t = half; t >= x; t--)
            if (dp[t - x]) dp[t] = true;
    for (int t = half; t >= 0; t--)
        if (dp[t]) return S - 2 * t;
    return S;
}
```

**Java**
```java
static int minSubsetSumDifference(int[] a) {
    int S = 0;
    for (int x : a) S += x;
    int half = S / 2;
    boolean[] dp = new boolean[half + 1];
    dp[0] = true;
    for (int x : a)
        for (int t = half; t >= x; t--)
            if (dp[t - x]) dp[t] = true;
    for (int t = half; t >= 0; t--)
        if (dp[t]) return S - 2 * t;
    return S;
}
```

**Python**
```python
def min_subset_sum_difference(a):
    S = sum(a)
    half = S // 2
    dp = [True] + [False] * half
    for x in a:
        for t in range(half, x - 1, -1):
            if dp[t - x]:
                dp[t] = True
    t = max(t for t in range(half + 1) if dp[t])
    return S - 2 * t
```

**Complexity:** time **O(n·S)**, space **O(S)** — n × S/2 updates plus one scan.

---

## Edge cases

- One element: the difference is the element itself.
- Zeros: they don't change sums but are harmless.

---

## Common mistakes

1. Scanning all `t` up to S without the `≤ S/2` restriction (fine, but return `|S − 2t|`).
2. Using this DP with negative numbers.

---

## Follow-ups

1. Negative numbers, n ≤ 30 (LC 2035)?
2. Last stone weight II (LC 1049)?

<details><summary>Answer sketches</summary>

**#1:** Meet in the middle: subset sums per half grouped by size, sort, binary search.

**#2:** This exact problem.
</details>

---

## Flashcards

**Min-difference partition answer?** #flashcard
`S − 2·max{t ≤ S/2 : reachable}`.

**Key reuse?** #flashcard
The last row of subset-sum answers every target.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
