---
module: striver/28-dynamic-programming
lesson: 5
topic: Maximum sum of non adjacent elements
difficulty: Medium
source: https://takeuforward.org/learning/dsa/maximum-sum-of-non-adjacent-elements?category=1d-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, 1d-dp, pick-not-pick]
---
# 5. Maximum sum of non adjacent elements

← [Frog jump with K distances](04-frog-jump-with-k-distances.md) · [Part 28 index](README.md) · Next → [House robber](06-house-robber.md)

> [!abstract] Problem at a glance
> **Task:** Pick a subset of the array with no two chosen elements adjacent, maximising their sum.
> **Key insight:** At index `i` you either **pick** it (then `i−1` is forbidden, so add `dp[i−2]`) or **skip** it (keep `dp[i−1]`): `dp[i] = max(a[i] + dp[i−2], dp[i−1])`. This pick/not-pick split is the core move of all subsequence DP.
> **Difficulty:** Medium · **Pattern:** 1D DP: pick / not pick · **Also on:** LC 198 (House Robber)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-sum-of-non-adjacent-elements?category=1d-dp&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Pick / not-pick recursion](#3-pick--not-pick-recursion) · [4. Memoization](#4-memoization) · [5. Space-optimised tabulation](#5-space-optimised-tabulation) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given non-negative integers `nums`, choose a subsequence in which no two elements are adjacent in the original array. Return the maximum possible sum.

| Input | Output | Why |
|---|---|---|
| `nums = [2,1,4,9]` | `11` | 2 + 9 |
| `nums = [1,2,4]` | `5` | 1 + 4 |
| `nums = [2,7,9,3,1]` | `12` | 2 + 9 + 1 |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Pick / not-pick recursion | f(i) = max(a[i] + f(i−2), f(i−1)) | O(2ⁿ) | O(n) |
| Memoization | cache f(i) | O(n) | O(n) |
| Space-optimised tabulation | prev = dp[i−1], prev2 = dp[i−2] | O(n) | O(1) |

> [!tip] Interview angle
> Write the pick/not-pick recursion first and let the interviewer watch it turn into a two-variable loop. This exact recurrence returns in House Robber II, in the knapsack family and in stock DP.

---

## 3. Pick / not-pick recursion

**Intuition.** `f(i)` = best sum using indices `0..i`. Base cases: `f(0) = a[0]` and `f(i < 0) = 0`.

```python
def nonadj_rec(a):
    def f(i):
        if i < 0:
            return 0
        if i == 0:
            return a[0]
        return max(a[i] + f(i - 2), f(i - 1))
    return f(len(a) - 1)
```

**Complexity:** time **O(2ⁿ)**, space **O(n)**.

---

## 4. Memoization

**Intuition.** There are only `n` distinct `i`, so caching makes it linear.

```python
def nonadj_memo(a):
    dp = [-1] * len(a)
    def f(i):
        if i < 0:
            return 0
        if i == 0:
            return a[0]
        if dp[i] == -1:
            dp[i] = max(a[i] + f(i - 2), f(i - 1))
        return dp[i]
    return f(len(a) - 1)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 5. Space-optimised tabulation

**Intuition.** Bottom-up, `dp[i]` reads only `dp[i−1]` and `dp[i−2]`. Treat `dp[−1] = 0`.

**Algorithm**

1. `prev = a[0]`, `prev2 = 0`.
2. For `i = 1..n−1`: `pick = a[i] + prev2`; `skip = prev`; `cur = max(pick, skip)`; shift.
3. Return `prev`.

**Dry run** — [2,7,9,3,1]: (prev2, prev) = (0,2) → (2,7) → (7,11) → (11,11) → (11,12). Answer 12.

**C++**
```cpp
int maximumNonAdjacentSum(vector<int>& a) {
    int prev = a[0], prev2 = 0;
    for (int i = 1; i < (int)a.size(); i++) {
        int cur = max(a[i] + prev2, prev);
        prev2 = prev;
        prev = cur;
    }
    return prev;
}
```

**Java**
```java
static int maximumNonAdjacentSum(int[] a) {
    int prev = a[0], prev2 = 0;
    for (int i = 1; i < a.length; i++) {
        int cur = Math.max(a[i] + prev2, prev);
        prev2 = prev;
        prev = cur;
    }
    return prev;
}
```

**Python**
```python
def max_non_adjacent(a):
    prev, prev2 = a[0], 0
    for i in range(1, len(a)):
        prev2, prev = prev, max(a[i] + prev2, prev)
    return prev
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, constant state.

---

## Edge cases

- Single element: return it.
- All zeros: 0.
- Two elements: the larger one.

---

## Common mistakes

1. Base case `f(−1)` returning `a[0]` instead of 0.
2. Assuming the answer alternates even/odd indices (fails on `[4,1,1,4]` → 8).

---

## Follow-ups

1. Negative numbers allowed and empty selection allowed?
2. Houses in a circle?
3. Return the chosen indices.

<details><summary>Answer sketches</summary>

**#1:** Same recurrence; `max` with 0 handles it. If the choice must be non-empty, start from `a[0]` and never clamp to 0.

**#2:** Next problem: run the linear version on `[0..n−2]` and on `[1..n−1]`.

**#3:** Store pick/skip decisions and backtrack from `n−1`.
</details>

---

## Flashcards

**Non-adjacent max-sum recurrence?** #flashcard
`dp[i] = max(a[i] + dp[i−2], dp[i−1])`.

**Name of this DP move?** #flashcard
Pick / not pick, the basis of subsequence DP.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
