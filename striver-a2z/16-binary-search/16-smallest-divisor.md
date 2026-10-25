---
module: striver-a2z/16-binary-search
lesson: 16
topic: Find the Smallest Divisor
difficulty: Medium
source: https://takeuforward.org/learning/dsa/find-the-smallest-divisor?category=on-answers&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer]
---
# 16. Find the Smallest Divisor

← [Find Nth Root of a Number](15-nth-root.md) · [Part 16 index](README.md) · Next → [Koko Eating Bananas](17-koko-eating-bananas.md)

> [!abstract] Problem at a glance
> **Task:** Find the smallest positive `d` such that `Σ ⌈nums[i] / d⌉ ≤ threshold`.
> **Key insight:** Larger `d` → every ceiling shrinks → sum is non-increasing. So feasibility is F…F T…T in `d ∈ [1, max(nums)]`; find the first true.
> **Difficulty:** Medium · **Pattern:** Binary search on answer — min feasible · **Also on:** [LC 1283](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-the-smallest-divisor?category=on-answers&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Try every divisor](#3-try-every-divisor) · [4. Binary search on d](#4-binary-search-on-d) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` and an integer `threshold`, choose a positive integer divisor `d`, divide every element by it rounding up, and sum the results. Return the smallest `d` such that the sum is `≤ threshold`. It's guaranteed that `threshold ≥ n`.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 5, 9], threshold = 6` | `5` | 1+1+1+2 = 5 ≤ 6; d = 4 gives 7 |
| `nums = [44, 22, 33, 11, 1], threshold = 5` | `44` |  |
| `nums = [2, 3, 5, 7, 11], threshold = 11` | `3` |  |

**Constraints:** `1 ≤ n ≤ 5·10⁴`, `1 ≤ nums[i] ≤ 10⁶`, `n ≤ threshold ≤ 10⁶`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Try every divisor | d = 1 … max(nums), first that passes | O(n · max) | O(1) |
| Binary search on d | check(d) = Σ ceil(x/d) ≤ threshold; first true in [1, max] | O(n log max) | O(1) |

> [!tip] Interview angle
> This is the template every "minimum X such that a greedy check passes" problem uses (Koko, bouquets, ship packages, split array). Name the three pieces: **range** `[1, max]`, **check(d)** in O(n), **direction** (min feasible → on true go left).

---

## 3. Try every divisor

**Intuition.** Monotone feasibility means the first passing `d` is the answer. Too slow for max = 10⁶ and n = 5·10⁴.

```python
def smallest_divisor_linear(nums, threshold):
    for d in range(1, max(nums) + 1):
        if sum((x + d - 1) // d for x in nums) <= threshold:
            return d
    return -1
```

**Complexity:** time **O(n · max)**, space **O(1)**.

---

## 4. Binary search on d

**Intuition.** `d = max(nums)` always works (sum = n ≤ threshold), so the answer exists in `[1, max]`. Binary search for the first `d` whose ceiling sum fits. Integer ceiling: `(x + d − 1) / d`.

**Dry run** — `[1 2 5 9]`, t 6: lo 1 hi 9 mid 5 (1+1+1+2 = 5 ✓) ans 5, hi 4; mid 2 (1+1+3+5 = 10 ✗) lo 3; mid 3 (1+1+2+3 = 7 ✗) lo 4; mid 4 (1+1+2+3 = 7 ✗) lo 5 → 5.

**C++**
```cpp
int smallestDivisor(vector<int>& nums, int threshold) {
    int lo = 1, hi = *max_element(nums.begin(), nums.end()), ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        long long s = 0;
        for (int x : nums) s += (x + mid - 1) / mid;
        if (s <= threshold) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Java**
```java
static int smallestDivisor(int[] nums, int threshold) {
    int hi = 0;
    for (int x : nums) hi = Math.max(hi, x);
    int lo = 1, ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        long s = 0;
        for (int x : nums) s += (x + mid - 1) / mid;
        if (s <= threshold) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Python**
```python
def smallest_divisor(nums, threshold):
    lo, hi = 1, max(nums)
    ans = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if sum((x + mid - 1) // mid for x in nums) <= threshold:
            ans, hi = mid, mid - 1
        else:
            lo = mid + 1
    return ans
```

**Complexity:** time **O(n log max)**, space **O(1)** — log(max) checks, each O(n).

---

## Edge cases

- threshold = n → answer is max(nums).
- Single element.

---

## Common mistakes

1. Using floor division instead of ceiling.
2. Starting `lo` at 0 — division by zero.
3. `int` overflow summing ceilings (fine here, but habitually use 64-bit).

---

## Follow-ups

1. Largest d instead (with sum ≥ threshold).
2. Why is the check monotone?

<details><summary>Answer sketches</summary>

**#1:** Flip direction: on true record and go right.

**#2:** Each ⌈x/d⌉ is non-increasing in d, so the sum is too.
</details>

---

## Flashcards

**BS on answer — three pieces?** #flashcard
Range of answers, O(n) feasibility check, direction (min feasible → go left on true).

**Integer ceil(a / b) for positive ints?** #flashcard
(a + b − 1) / b.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
