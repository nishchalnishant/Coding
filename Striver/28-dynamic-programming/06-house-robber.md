---
module: striver/28-dynamic-programming
lesson: 6
topic: House robber
difficulty: Medium
source: https://takeuforward.org/learning/dsa/house-robber?category=1d-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, 1d-dp, circular]
---
# 6. House robber

← [Maximum sum of non adjacent elements](05-maximum-sum-of-non-adjacent-elements.md) · [Part 28 index](README.md) · Next → [Ninja's training](07-ninjas-training.md)

> [!abstract] Problem at a glance
> **Task:** Houses stand in a **circle**; robbing two adjacent houses triggers the alarm. Maximise the loot.
> **Key insight:** The circle only adds one constraint: the first and last house are adjacent. So at most one of them is used, and the answer is `max(linear(a[0..n−2]), linear(a[1..n−1]))`, reusing the non-adjacent-sum DP.
> **Difficulty:** Medium · **Pattern:** Reduce circular to two linear runs · **Also on:** LC 213 (House Robber II)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/house-robber?category=1d-dp&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Two linear passes on slices](#3-two-linear-passes-on-slices) · [4. Two passes by index range](#4-two-passes-by-index-range) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`nums[i]` is the money in house `i`, and the houses form a circle (house `n−1` neighbours house 0). Return the maximum sum you can rob with no two adjacent houses robbed.

| Input | Output | Why |
|---|---|---|
| `nums = [2,3,2]` | `3` | 2 and 2 are adjacent across the wrap |
| `nums = [1,2,3,1]` | `4` | 1 + 3 |
| `nums = [1,2,3]` | `3` | only one of the ends |

**Constraints:** `1 ≤ n ≤ 100`, `0 ≤ nums[i] ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Two linear passes on slices | max(rob(a[:-1]), rob(a[1:])) | O(n) | O(n) |
| Two passes by index range | same, without copying | O(n) | O(1) |

> [!tip] Interview angle
> Say the reduction in one sentence before coding: "Either the first house is excluded or the last one is." Handle `n = 1` explicitly, because both slices would otherwise be empty.

---

## 3. Two linear passes on slices

**Intuition.** Build the two sub-arrays and run the linear pick/not-pick DP on each.

```python
def rob_slices(a):
    if len(a) == 1:
        return a[0]
    def lin(b):
        prev, prev2 = 0, 0
        for x in b:
            prev2, prev = prev, max(x + prev2, prev)
        return prev
    return max(lin(a[:-1]), lin(a[1:]))
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Two passes by index range

**Intuition.** Pass index bounds instead of slicing. Range `[0, n−2]` drops the last house and `[1, n−1]` drops the first.

**Algorithm**

1. If `n == 1`, return `a[0]`.
2. `lin(lo, hi)`: rolling `prev, prev2 = 0, 0`; for `i` in `lo..hi`: `cur = max(a[i] + prev2, prev)`.
3. Return `max(lin(0, n−2), lin(1, n−1))`.

**Dry run** — [1,2,3,1]: lin(0..2) on [1,2,3] = 4; lin(1..3) on [2,3,1] = 3 → 4.

**C++**
```cpp
int linRob(vector<int>& a, int lo, int hi) {
    int prev = 0, prev2 = 0;
    for (int i = lo; i <= hi; i++) {
        int cur = max(a[i] + prev2, prev);
        prev2 = prev;
        prev = cur;
    }
    return prev;
}
int rob(vector<int>& a) {
    int n = a.size();
    if (n == 1) return a[0];
    return max(linRob(a, 0, n - 2), linRob(a, 1, n - 1));
}
```

**Java**
```java
static int linRob(int[] a, int lo, int hi) {
    int prev = 0, prev2 = 0;
    for (int i = lo; i <= hi; i++) {
        int cur = Math.max(a[i] + prev2, prev);
        prev2 = prev;
        prev = cur;
    }
    return prev;
}
static int rob(int[] a) {
    int n = a.length;
    if (n == 1) return a[0];
    return Math.max(linRob(a, 0, n - 2), linRob(a, 1, n - 1));
}
```

**Python**
```python
def rob(a):
    n = len(a)
    if n == 1:
        return a[0]
    def lin(lo, hi):
        prev = prev2 = 0
        for i in range(lo, hi + 1):
            prev2, prev = prev, max(a[i] + prev2, prev)
        return prev
    return max(lin(0, n - 2), lin(1, n - 1))
```

**Complexity:** time **O(n)**, space **O(1)** — two linear passes with constant state.

---

## Edge cases

- `n = 1`: rob it; both slices would be empty.
- `n = 2`: the larger of the two.
- Large value at both ends: you can take only one.

---

## Common mistakes

1. Forgetting `n = 1`, which returns 0.
2. Running the linear DP once on the whole array, which ignores the wrap.
3. Excluding both ends in a single pass, which misses answers that use one end.

---

## Follow-ups

1. Houses on a binary tree (LC 337)?
2. Robber must skip at least k houses between robberies?

<details><summary>Answer sketches</summary>

**#1:** Tree DP: each node returns `(rob_me, skip_me)`; `rob_me = val + skip_l + skip_r`, `skip_me = max(l) + max(r)`.

**#2:** `dp[i] = max(dp[i−1], a[i] + dp[i−k−1])`.
</details>

---

## Flashcards

**Circular house robber reduction?** #flashcard
`max(linear(a[0..n−2]), linear(a[1..n−1]))`; special-case n = 1.

**House Robber III (tree)?** #flashcard
Post-order returning (rob, skip) pairs.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
