---
module: striver/16-binary-search
lesson: 10
topic: Find Minimum in Rotated Sorted Array
difficulty: Medium
source: https://takeuforward.org/learning/dsa/find-minimum-in-rotated-sorted-array?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, rotated-array]
---
# 10. Find Minimum in Rotated Sorted Array

← [Search in Rotated Sorted Array II](09-search-in-rotated-sorted-array-ii.md) · [Part 16 index](README.md) · Next → [Find Out How Many Times the Array Is Rotated](11-rotation-count.md)

> [!abstract] Problem at a glance
> **Task:** Return the minimum of a rotated sorted array of distinct values.
> **Key insight:** Compare `nums[mid]` with `nums[hi]`. If `nums[mid] > nums[hi]`, the drop (and the minimum) is strictly right of `mid`; otherwise `mid` is on the lower ramp, so the minimum is at `mid` or left of it.
> **Difficulty:** Medium · **Pattern:** Binary search on a rotated array · **Also on:** [LC 153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-minimum-in-rotated-sorted-array?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [4. Sorted-half minimum (Striver's version)](#4-sorted-half-minimum-strivers-version) · [5. Compare mid with hi](#5-compare-mid-with-hi) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a rotated ascending array of **distinct** integers, return its minimum element in O(log n).

| Input | Output | Why |
|---|---|---|
| `nums = [3, 4, 5, 1, 2]` | `1` |  |
| `nums = [4, 5, 6, 7, 0, 1, 2]` | `0` |  |
| `nums = [11, 13, 15, 17]` | `11` | not rotated |

**Constraints:** `1 ≤ n ≤ 5000`, `−5000 ≤ nums[i] ≤ 5000`, distinct.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | min(nums) | O(n) | O(1) |
| Sorted-half minimum (Striver's version) | take min of the sorted half's first element; discard it | O(log n) | O(1) |
| Compare mid with hi | nums[mid] > nums[hi] → lo = mid + 1, else hi = mid; answer nums[lo] | O(log n) | O(1) |

---

## 3. Linear scan

**Intuition.** Baseline.

```python
def find_min_linear(nums):
    return min(nums)
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Sorted-half minimum (Striver's version)

**Intuition.** If `[lo, hi]` is already sorted, `nums[lo]` is its min — done. Otherwise, the sorted half's smallest element is its first; record it and search the other half, which contains the drop.

```python
def find_min_halves(nums):
    lo, hi, ans = 0, len(nums) - 1, float('inf')
    while lo <= hi:
        if nums[lo] <= nums[hi]:          # whole range sorted
            ans = min(ans, nums[lo])
            break
        mid = (lo + hi) // 2
        if nums[lo] <= nums[mid]:         # left sorted
            ans = min(ans, nums[lo])
            lo = mid + 1
        else:                             # right sorted
            ans = min(ans, nums[mid])
            hi = mid - 1
    return ans
```

**Complexity:** time **O(log n)**, space **O(1)**.

---

## 5. Compare mid with hi

**Intuition.** The predicate `nums[i] ≤ nums[n − 1]` is false on the upper ramp and true on the lower ramp — monotone. The minimum is the first true. Using `hi = mid` (not `mid − 1`) keeps `mid` as a candidate; the loop runs while `lo < hi` and ends with both pointing at the minimum.

**Dry run** — `[4 5 6 7 0 1 2]`: lo 0 hi 6 mid 3 (7 > 2) → lo 4; mid 5 (1 ≤ 2) → hi 5; mid 4 (0 ≤ 1) → hi 4. Answer nums[4] = 0.

**Why compare with `hi`, not `lo`?** For an unrotated array, `nums[mid] > nums[lo]` holds but the min is on the left; the `lo` comparison needs a special case, the `hi` comparison doesn't.

**C++**
```cpp
int findMin(vector<int>& nums) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) lo = mid + 1;
        else hi = mid;
    }
    return nums[lo];
}
```

**Java**
```java
static int findMin(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) lo = mid + 1;
        else hi = mid;
    }
    return nums[lo];
}
```

**Python**
```python
def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
```

**Complexity:** time **O(log n)**, space **O(1)** — halving; `lo < hi` with `hi = mid` always shrinks since mid < hi.

---

## Edge cases

- Not rotated.
- Single element.
- Minimum at the last index.

---

## Common mistakes

1. `while lo <= hi` with `hi = mid` — infinite loop.
2. Comparing with `nums[lo]` without handling the unrotated case.

---

## Follow-ups

1. With duplicates (LC 154).
2. Index of the maximum.

<details><summary>Answer sketches</summary>

**#1:** If `nums[mid] == nums[hi]`, `hi −= 1`; worst case O(n).

**#2:** `(minIndex − 1 + n) % n`.
</details>

---

## Flashcards

**Min of rotated sorted array — comparison?** #flashcard
nums[mid] > nums[hi] → lo = mid + 1, else hi = mid.

**Loop condition for the hi = mid template?** #flashcard
while lo < hi; answer at lo.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
