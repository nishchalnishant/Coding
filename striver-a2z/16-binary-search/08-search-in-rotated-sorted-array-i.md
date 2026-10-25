---
module: striver-a2z/16-binary-search
lesson: 8
topic: Search in Rotated Sorted Array I
difficulty: Medium
source: https://takeuforward.org/learning/dsa/search-in-rotated-sorted-array-i?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, rotated-array]
---
# 8. Search in Rotated Sorted Array I

← [First and Last Occurrence](07-first-and-last-occurrence.md) · [Part 16 index](README.md) · Next → [Search in Rotated Sorted Array II](09-search-in-rotated-sorted-array-ii.md)

> [!abstract] Problem at a glance
> **Task:** Find `target` in a sorted array of distinct values that has been rotated at an unknown pivot.
> **Key insight:** Any `mid` splits the array into two halves and **at least one of them is sorted** (`nums[lo] ≤ nums[mid]` → left is sorted). Check whether the target lies inside the sorted half's range; if yes go there, else go to the other half.
> **Difficulty:** Medium · **Pattern:** Binary search — identify the sorted half · **Also on:** [LC 33](https://leetcode.com/problems/search-in-rotated-sorted-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/search-in-rotated-sorted-array-i?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [4. Find pivot, then binary search one ramp](#4-find-pivot-then-binary-search-one-ramp) · [5. One pass: pick the sorted half](#5-one-pass-pick-the-sorted-half) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

An ascending array of **distinct** integers was rotated at some unknown index `k`, giving `[nums[k], …, nums[n−1], nums[0], …, nums[k−1]]`. Given the rotated array and `target`, return its index or `-1`, in O(log n).

| Input | Output | Why |
|---|---|---|
| `nums = [4, 5, 6, 7, 0, 1, 2], target = 0` | `4` |  |
| `nums = [4, 5, 6, 7, 0, 1, 2], target = 3` | `-1` |  |
| `nums = [1], target = 0` | `-1` |  |

**Constraints:** `1 ≤ n ≤ 5000`, `−10⁴ ≤ nums[i], target ≤ 10⁴`, distinct values.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | check every index | O(n) | O(1) |
| Find pivot, then binary search one ramp | min index k; search [0, k−1] or [k, n−1] | O(log n) | O(1) |
| One pass: pick the sorted half | nums[lo] ≤ nums[mid] → left sorted; test range, else go right | O(log n) | O(1) |

> [!tip] Interview angle
> Draw the rotated array as two ascending ramps. Say: "one side of mid is always a single ramp — I can test membership there with two comparisons." Mention the alternative (find the pivot, then binary search the correct ramp) as equally valid.

---

## 3. Linear scan

**Intuition.** Ignores structure.

```python
def search_rot_linear(nums, target):
    for i, v in enumerate(nums):
        if v == target:
            return i
    return -1
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Find pivot, then binary search one ramp

**Intuition.** First binary-search the index of the minimum (the rotation point — see problem 9). Both ramps are then sorted; pick the one whose range contains the target and run plain binary search. Two passes, but each piece is simple.

```python
from bisect import bisect_left
def search_rot_pivot(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:                       # index of minimum
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    k = lo
    if k > 0 and nums[0] <= target <= nums[k - 1]:
        l, r = 0, k
    else:
        l, r = k, len(nums)
    i = bisect_left(nums, target, l, r)
    return i if i < r and nums[i] == target else -1
```

**Complexity:** time **O(log n)**, space **O(1)**.

---

## 5. One pass: pick the sorted half

**Intuition.** If `nums[lo] ≤ nums[mid]`, the segment `[lo, mid]` has no rotation point, so it's sorted. Target is in it iff `nums[lo] ≤ target < nums[mid]` — go left, otherwise right. Symmetric when the right half `[mid, hi]` is sorted: in it iff `nums[mid] < target ≤ nums[hi]`.

**Algorithm**

1. Check `nums[mid] == target`.
2. If `nums[lo] ≤ nums[mid]` (left sorted): `nums[lo] ≤ target < nums[mid]` ? `hi = mid − 1` : `lo = mid + 1`.
3. Else (right sorted): `nums[mid] < target ≤ nums[hi]` ? `lo = mid + 1` : `hi = mid − 1`.

**Dry run** — `[4 5 6 7 0 1 2]`, t = 0: lo 0 hi 6 mid 3 (7). Left `[4..7]` sorted; 0 ∉ [4, 7) → lo 4. mid 5 (1). `nums[4]=0 ≤ 1` left sorted; 0 ∈ [0, 1) → hi 4. mid 4 (0) → return 4.

**Why `≤` in `nums[lo] ≤ nums[mid]`:** when `lo == mid` (two-element range) the left half is a single element and *is* sorted; `<` would misclassify it.

**C++**
```cpp
int search(vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}
```

**Java**
```java
static int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}
```

**Python**
```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

**Complexity:** time **O(log n)**, space **O(1)** — one side is always sorted, so each step discards half.

---

## Edge cases

- Not rotated at all (k = 0).
- Two elements `[3, 1]`.
- Target at the pivot or the last index.

---

## Common mistakes

1. `nums[lo] < nums[mid]` (strict) — fails when `lo == mid`.
2. Half-open/closed mismatch in the range test (`<` vs `≤` at the `mid` end).
3. Applying it with duplicates — see the next problem.

---

## Follow-ups

1. With duplicates.
2. Return the rotation count.

<details><summary>Answer sketches</summary>

**#1:** Next problem: shrink both ends when `nums[lo] == nums[mid] == nums[hi]`.

**#2:** Index of the minimum — problem 10.
</details>

---

## Flashcards

**Rotated sorted search — key observation?** #flashcard
At any mid, at least one half is sorted; test the target against that half's range.

**Left half sorted test?** #flashcard
nums[lo] ≤ nums[mid] (≤ handles lo == mid).

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
