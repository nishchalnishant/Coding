---
module: striver/16-binary-search
lesson: 24
topic: Find Peak Element
difficulty: Medium
source: https://takeuforward.org/learning/dsa/find-peak-element?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search]
---
# 24. Find Peak Element

← [Book Allocation Problem](23-book-allocation-problem.md) · [Part 16 index](README.md) · Next → [Median of 2 Sorted Arrays](25-median-of-two-sorted-arrays.md)

> [!abstract] Problem at a glance
> **Task:** Return the index of any element strictly greater than its neighbours (`nums[−1] = nums[n] = −∞`).
> **Key insight:** Compare `nums[mid]` with `nums[mid + 1]`. If it's rising, a peak exists to the right (the slope must come down by `nums[n] = −∞`). Otherwise `mid` or something left of it is a peak. Binary search on the slope, not on values.
> **Difficulty:** Medium · **Pattern:** Binary search on unsorted data via slope · **Also on:** [LC 162](https://leetcode.com/problems/find-peak-element/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-peak-element?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [4. Binary search on slope](#4-binary-search-on-slope) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` where `nums[i] ≠ nums[i + 1]`, return the index of any peak element. Treat out-of-range neighbours as −∞. Must run in O(log n).

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3, 1]` | `2` |  |
| `nums = [1, 2, 1, 3, 5, 6, 4]` | `1 or 5` | either peak is accepted |

**Constraints:** `1 ≤ n ≤ 1000`, adjacent elements differ.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | first i with nums[i] > nums[i + 1] | O(n) | O(1) |
| Binary search on slope | nums[mid] < nums[mid+1] → lo = mid + 1 else hi = mid | O(log n) | O(1) |

> [!tip] Interview angle
> This is the go-to example that **binary search doesn't need sorted input** — it needs a predicate that tells you which half is guaranteed to contain an answer. Say that sentence.

---

## 3. Linear scan

**Intuition.** The array starts rising from −∞; the first time it falls, you're on a peak. If it never falls, the last element is a peak.

```python
def find_peak_linear(nums):
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            return i
    return len(nums) - 1
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Binary search on slope

**Intuition.** Half-open style `while lo < hi`: `mid + 1` is always in range because `mid < hi`. Rising at `mid` → some peak in `(mid, hi]`. Falling → some peak in `[lo, mid]`. Loop ends with `lo == hi` on a peak.

**Dry run** — `[1 2 1 3 5 6 4]`: lo 0 hi 6 mid 3 (3 < 5) lo 4; mid 5 (6 > 4) hi 5; mid 4 (5 < 6) lo 5 → 5.

**Why it's valid:** invariant — the range `[lo, hi]` always contains a peak, because `nums[lo − 1] < nums[lo]` (or lo = 0) and `nums[hi] > nums[hi + 1]` (or hi = n − 1).

**C++**
```cpp
int findPeakElement(vector<int>& nums) {
    int lo = 0, hi = nums.size() - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < nums[mid + 1]) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

**Java**
```java
static int findPeakElement(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < nums[mid + 1]) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

**Python**
```python
def find_peak_element(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

**Complexity:** time **O(log n)**, space **O(1)** — range halves each step.

---

## Edge cases

- n = 1.
- Strictly increasing → last index.
- Strictly decreasing → 0.

---

## Common mistakes

1. Using `while lo <= hi` with `hi = mid` — infinite loop.
2. Checking both neighbours with manual bounds — messy and error-prone.

---

## Follow-ups

1. Equal neighbours allowed.
2. 2D peak.

<details><summary>Answer sketches</summary>

**#1:** Worst case becomes O(n) — a plateau hides the slope.

**#2:** Next problem in this part: binary search columns, take the column max.
</details>

---

## Flashcards

**Peak element — compare mid with?** #flashcard
nums[mid + 1]: rising → go right, else hi = mid.

**Binary search requirement, really?** #flashcard
A predicate that tells you which half surely contains an answer — not sortedness.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
