---
module: striver/16-binary-search
lesson: 6
topic: Floor and Ceil in Sorted Array
difficulty: Easy
source: https://takeuforward.org/learning/dsa/floor-and-ceil-in-sorted-array?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search]
---
# 6. Floor and Ceil in Sorted Array

← [Search Insert Position](05-search-insert-position.md) · [Part 16 index](README.md) · Next → [First and Last Occurrence](07-first-and-last-occurrence.md)

> [!abstract] Problem at a glance
> **Task:** Return `[floor, ceil]` of `x`: the largest element ≤ x and the smallest element ≥ x (−1 if missing).
> **Key insight:** Ceil is the value at lower bound. Floor is a mirror search: when `nums[mid] ≤ x`, record it and go right (last true of a T…T F…F predicate).
> **Difficulty:** Easy · **Pattern:** First-true / last-true binary search
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/floor-and-ceil-in-sorted-array?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 12 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [4. Two binary searches](#4-two-binary-searches) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a sorted array `nums` and an integer `x`, find the **floor** (largest element `≤ x`) and **ceil** (smallest element `≥ x`). Return `[floor, ceil]`, using `-1` for one that doesn't exist.

| Input | Output | Why |
|---|---|---|
| `nums = [3, 4, 4, 7, 8, 10], x = 5` | `[4, 7]` |  |
| `nums = [3, 4, 4, 7, 8, 10], x = 8` | `[8, 8]` | exact match |
| `nums = [3, 4, 4, 7, 8, 10], x = 2` | `[-1, 3]` | no floor |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ nums[i], x ≤ 10⁹`, sorted.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | track last ≤ x and first ≥ x | O(n) | O(1) |
| Two binary searches | floor: last nums[i] ≤ x · ceil: first nums[i] ≥ x | O(log n) | O(1) |

---

## 3. Linear scan

**Intuition.** One pass: update floor while values are ≤ x; the first value ≥ x is the ceil.

```python
def floor_ceil_linear(nums, x):
    fl, ce = -1, -1
    for v in nums:
        if v <= x:
            fl = v
        if v >= x and ce == -1:
            ce = v
    return [fl, ce]
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Two binary searches

**Intuition.** `nums[i] ≤ x` is true then false along the array, so the floor is the **last true**: on true, record and move `lo = mid + 1`. `nums[i] ≥ x` is false then true, so the ceil is the **first true**: record and move `hi = mid − 1`.

**Dry run** — `[3 4 4 7 8 10]`, x = 5 — floor: mid 2 (4 ≤ 5) fl 4, lo 3; mid 4 (8) hi 3; mid 3 (7) hi 2 → 4. Ceil: mid 2 (4) lo 3; mid 4 (8 ≥ 5) ce 8, hi 3; mid 3 (7) ce 7, hi 2 → 7.

**C++**
```cpp
vector<int> getFloorAndCeil(vector<int>& nums, int x) {
    int n = nums.size(), fl = -1, ce = -1;
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] <= x) { fl = nums[mid]; lo = mid + 1; }
        else hi = mid - 1;
    }
    lo = 0; hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] >= x) { ce = nums[mid]; hi = mid - 1; }
        else lo = mid + 1;
    }
    return {fl, ce};
}
```

**Java**
```java
static int[] getFloorAndCeil(int[] nums, int x) {
    int n = nums.length, fl = -1, ce = -1;
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] <= x) { fl = nums[mid]; lo = mid + 1; }
        else hi = mid - 1;
    }
    lo = 0; hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] >= x) { ce = nums[mid]; hi = mid - 1; }
        else lo = mid + 1;
    }
    return new int[]{fl, ce};
}
```

**Python**
```python
def get_floor_and_ceil(nums, x):
    fl = ce = -1
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] <= x:
            fl, lo = nums[mid], mid + 1
        else:
            hi = mid - 1
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] >= x:
            ce, hi = nums[mid], mid - 1
        else:
            lo = mid + 1
    return [fl, ce]
```

**Complexity:** time **O(log n)**, space **O(1)** — two independent O(log n) searches.

---

## Edge cases

- `x` below the minimum → no floor.
- `x` above the maximum → no ceil.
- `x` present → floor = ceil = x.

---

## Common mistakes

1. Returning indices when values were asked (or vice versa) — clarify.
2. Mixing up which direction to move after recording.

---

## Follow-ups

1. Floor/ceil in a BST.
2. Many queries on a dynamic set.

<details><summary>Answer sketches</summary>

**#1:** Same logic walking down the tree — Part 25.

**#2:** Balanced BST: C++ `set::lower_bound`, Java `TreeSet.floor/ceiling`.
</details>

---

## Flashcards

**Floor of x in sorted array?** #flashcard
Last i with nums[i] ≤ x: on true record, lo = mid + 1.

**Ceil of x in sorted array?** #flashcard
nums[lower_bound(x)] if in range.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
