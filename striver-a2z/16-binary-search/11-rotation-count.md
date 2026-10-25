---
module: striver-a2z/16-binary-search
lesson: 11
topic: Find Out How Many Times the Array Is Rotated
difficulty: Easy
source: https://takeuforward.org/learning/dsa/find-out-how-many-times-the-array-is-rotated?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, rotated-array]
---
# 11. Find Out How Many Times the Array Is Rotated

← [Find Minimum in Rotated Sorted Array](10-minimum-in-rotated-sorted-array.md) · [Part 16 index](README.md) · Next → [Single Element in a Sorted Array](12-single-element-in-sorted-array.md)

> [!abstract] Problem at a glance
> **Task:** Return how many right-rotations turned a sorted array (distinct values) into `nums`.
> **Key insight:** The rotation count is the **index of the minimum**. Same binary search as the previous problem, return `lo` instead of `nums[lo]`.
> **Difficulty:** Easy · **Pattern:** Binary search on a rotated array
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-out-how-many-times-the-array-is-rotated?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan for the drop](#3-linear-scan-for-the-drop) · [4. Index of minimum](#4-index-of-minimum) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A sorted array of distinct integers was right-rotated `k` times. Given the result, return `k` (`0 ≤ k < n`).

| Input | Output | Why |
|---|---|---|
| `nums = [4, 5, 6, 7, 0, 1, 2, 3]` | `4` | min 0 at index 4 |
| `nums = [3, 4, 5, 1, 2]` | `3` |  |
| `nums = [1, 2, 3]` | `0` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, distinct values.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan for the drop | first i with nums[i] < nums[i − 1] | O(n) | O(1) |
| Index of minimum | nums[mid] > nums[hi] → lo = mid + 1, else hi = mid; return lo | O(log n) | O(1) |

---

## 3. Linear scan for the drop

**Intuition.** The minimum is right after the only descent; no descent → 0.

```python
def rotations_linear(nums):
    for i in range(1, len(nums)):
        if nums[i] < nums[i - 1]:
            return i
    return 0
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Index of minimum

**Intuition.** After `k` right rotations, original index 0 (the minimum) sits at index `k`. Find it with the mid-vs-hi search.

**C++**
```cpp
int findKRotation(vector<int>& nums) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

**Java**
```java
static int findKRotation(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

**Python**
```python
def find_k_rotation(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

**Complexity:** time **O(log n)**, space **O(1)** — same search as the minimum.

---

## Edge cases

- Unrotated → 0.
- Rotated by n − 1.

---

## Common mistakes

1. Returning the minimum's value instead of its index.
2. Counting left rotations — clarify direction (left count = `(n − k) % n`).

---

## Follow-ups

1. Left rotations instead of right.
2. With duplicates.

<details><summary>Answer sketches</summary>

**#1:** `(n − idx) % n`.

**#2:** `hi −= 1` on `nums[mid] == nums[hi]`, but then return the *first* index of the minimum carefully.
</details>

---

## Flashcards

**Rotation count of a rotated sorted array?** #flashcard
Index of its minimum.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
