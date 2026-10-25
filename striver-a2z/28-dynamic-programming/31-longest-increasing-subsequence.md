---
module: striver-a2z/28-dynamic-programming
lesson: 31
topic: Longest increasing subsequence
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-increasing-subsequence?category=lis-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, lis, binary-search]
---
# 31. Longest increasing subsequence

← [Rod cutting problem](30-rod-cutting-problem.md) · [Part 28 index](README.md) · Next → [Print longest increasing subsequence](32-print-longest-increasing-subsequence.md)

> [!abstract] Problem at a glance
> **Task:** Length of the longest strictly increasing subsequence.
> **Key insight:** O(n²): `dp[i]` = LIS ending at `i` = `1 + max dp[j]` over `j < i, a[j] < a[i]`. O(n log n): keep `tails[k]` = the smallest possible tail of an increasing subsequence of length `k+1`. For each `x`, `lower_bound(tails, x)` and overwrite (or append). `tails` is not an actual LIS, but its length is the answer.
> **Difficulty:** Medium · **Pattern:** LIS (dp-ending-at / patience tails) · **Also on:** LC 300
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-increasing-subsequence?category=lis-dp&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Pick / not-pick memo (i, prev)](#3-pick--not-pick-memo-i-prev) · [4. dp[i] = LIS ending at i](#4-dpi--lis-ending-at-i) · [5. Tails + binary search](#5-tails--binary-search) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums`, return the length of the longest strictly increasing subsequence.

| Input | Output | Why |
|---|---|---|
| `[10,9,2,5,3,7,101,18]` | `4` | 2,3,7,101 |
| `[0,1,0,3,2,3]` | `4` | 0,1,2,3 |
| `[7,7,7,7]` | `1` | strict |

**Constraints:** `1 ≤ n ≤ 2500`, `−10⁴ ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Pick / not-pick memo (i, prev) | Striver's (index, prevIndex) recursion | O(n²) | O(n²) |
| dp[i] = LIS ending at i | 1 + max over smaller predecessors | O(n²) | O(n) |
| Tails + binary search | lower_bound replace or append | O(n log n) | O(n) |

> [!tip] Interview angle
> Give the O(n²) DP with its state sentence, then offer the O(n log n) version. Explain why overwriting is safe: a smaller tail for the same length can only help future elements. Use `lower_bound` for strict and `upper_bound` for non-decreasing.

---

## 3. Pick / not-pick memo (i, prev)

**Intuition.** `f(i, prev)`: skip `a[i]`, or take it if `prev == −1` or `a[i] > a[prev]`. The state stores `prev + 1` to avoid index −1.

```python
def lis_memo(a):
    n = len(a)
    from functools import lru_cache
    @lru_cache(None)
    def f(i, prev):
        if i == n:
            return 0
        best = f(i + 1, prev)
        if prev == -1 or a[i] > a[prev]:
            best = max(best, 1 + f(i + 1, i))
        return best
    return f(0, -1)
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 4. dp[i] = LIS ending at i

**Intuition.** Every LIS ends somewhere. Extend the best chain ending at any smaller earlier element.

```python
def lis_n2(a):
    dp = [1] * len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j] < a[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 5. Tails + binary search

**Intuition.** `tails` is strictly increasing. For each `x`, find the first tail ≥ `x`. If none exists, append (the LIS grew); otherwise replace it with `x` (same length, smaller tail).

**Algorithm**

1. `tails = []`.
2. For each `x`: `k = lower_bound(tails, x)`; if `k == len` append, else `tails[k] = x`.
3. Return `len(tails)`.

**Dry run** — [10,9,2,5,3,7,101,18]: [10] → [9] → [2] → [2,5] → [2,3] → [2,3,7] → [2,3,7,101] → [2,3,7,18] → 4.

**C++**
```cpp
int lengthOfLIS(vector<int>& a) {
    vector<int> tails;
    for (int x : a) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    return (int)tails.size();
}
```

**Java**
```java
static int lengthOfLIS(int[] a) {
    int[] tails = new int[a.length];
    int len = 0;
    for (int x : a) {
        int lo = 0, hi = len;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (tails[mid] < x) lo = mid + 1; else hi = mid;
        }
        tails[lo] = x;
        if (lo == len) len++;
    }
    return len;
}
```

**Python**
```python
from bisect import bisect_left
def length_of_lis(a):
    tails = []
    for x in a:
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
    return len(tails)
```

**Complexity:** time **O(n log n)**, space **O(n)** — n binary searches over a list of length ≤ n.

---

## Edge cases

- All equal: 1 (strict).
- Decreasing: 1.
- Single element: 1.

---

## Common mistakes

1. `upper_bound` for a strict LIS (lets equal values chain).
2. Returning `tails` as the LIS itself.
3. `dp` answer = `dp[n−1]` instead of `max(dp)`.

---

## Follow-ups

1. Non-decreasing subsequence?
2. Russian doll envelopes (LC 354)?
3. Minimum deletions to make the array sorted?

<details><summary>Answer sketches</summary>

**#1:** `upper_bound` in the tails method.

**#2:** Sort by width ascending, height **descending**, then LIS on heights.

**#3:** `n − LIS` (non-decreasing).
</details>

---

## Flashcards

**LIS O(n log n) invariant?** #flashcard
`tails[k]` = smallest tail of an increasing subsequence of length k+1.

**Strict vs non-strict LIS?** #flashcard
lower_bound vs upper_bound.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
