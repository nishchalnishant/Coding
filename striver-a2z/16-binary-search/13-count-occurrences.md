---
module: striver-a2z/16-binary-search
lesson: 13
topic: Count Occurrences in a Sorted Array
difficulty: Easy
source: https://takeuforward.org/learning/dsa/count-occurrences-in-a-sorted-array?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search]
---
# 13. Count Occurrences in a Sorted Array

← [Single Element in a Sorted Array](12-single-element-in-sorted-array.md) · [Part 16 index](README.md) · Next → [Find Square Root of a Number](14-square-root.md)

> [!abstract] Problem at a glance
> **Task:** Return how many times `target` appears in a sorted array.
> **Key insight:** `upper_bound(target) − lower_bound(target)`. Two O(log n) searches, no presence check needed (absent → both bounds equal → 0).
> **Difficulty:** Easy · **Pattern:** Lower / upper bound
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-occurrences-in-a-sorted-array?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 8 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear count](#3-linear-count) · [4. Upper bound − lower bound](#4-upper-bound--lower-bound) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a sorted array `nums` and an integer `target`, return the number of occurrences of `target` in O(log n).

| Input | Output | Why |
|---|---|---|
| `nums = [0, 0, 1, 1, 1, 2, 3], target = 1` | `3` |  |
| `nums = [5, 5, 5, 5, 5, 5], target = 5` | `6` |  |
| `nums = [1, 2, 3], target = 4` | `0` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, sorted.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear count | nums.count(target) | O(n) | O(1) |
| Upper bound − lower bound | two binary searches | O(log n) | O(1) |

---

## 3. Linear count

**Intuition.** Baseline.

```python
def count_occ_linear(nums, target):
    return sum(1 for x in nums if x == target)
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Upper bound − lower bound

**Intuition.** Everything in `[lower_bound, upper_bound)` equals `target`, so the length of that half-open range is the count. Written as one helper parameterised by strictness.

**C++**
```cpp
int bound(vector<int>& a, int t, bool strict) {
    int lo = 0, hi = (int)a.size() - 1, ans = a.size();
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (strict ? a[mid] > t : a[mid] >= t) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
int countOccurrences(vector<int>& nums, int target) {
    return bound(nums, target, true) - bound(nums, target, false);
}
```

**Java**
```java
static int bound(int[] a, int t, boolean strict) {
    int lo = 0, hi = a.length - 1, ans = a.length;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (strict ? a[mid] > t : a[mid] >= t) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
static int countOccurrences(int[] nums, int target) {
    return bound(nums, target, true) - bound(nums, target, false);
}
```

**Python**
```python
def count_occurrences(nums, target):
    def bound(strict):
        lo, hi, ans = 0, len(nums) - 1, len(nums)
        while lo <= hi:
            mid = (lo + hi) // 2
            if (nums[mid] > target) if strict else (nums[mid] >= target):
                ans, hi = mid, mid - 1
            else:
                lo = mid + 1
        return ans
    return bound(True) - bound(False)
```

**Complexity:** time **O(log n)**, space **O(1)** — two halving searches.

---

## Edge cases

- Absent → 0 automatically.
- Whole array equals target.

---

## Common mistakes

1. Finding one occurrence then counting outward — O(n).
2. Off-by-one with `last − first` (needs `+ 1`) if using first/last indices.

---

## Follow-ups

1. Count values in [a, b].
2. Most frequent element in a sorted array in O(k log n) for k distinct values.

<details><summary>Answer sketches</summary>

**#1:** `upper_bound(b) − lower_bound(a)`.

**#2:** Jump with upper bound from each new value.
</details>

---

## Flashcards

**Count of x in sorted array?** #flashcard
upper_bound(x) − lower_bound(x).

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
