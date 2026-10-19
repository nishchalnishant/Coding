---
module: striver/16-binary-search
lesson: 5
topic: Search Insert Position
difficulty: Easy
source: https://takeuforward.org/learning/dsa/search-insert-position?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, lower-bound]
---
# 5. Search Insert Position

← [Upper Bound](04-upper-bound.md) · [Part 16 index](README.md) · Next → [Floor and Ceil in Sorted Array](06-floor-and-ceil.md)

> [!abstract] Problem at a glance
> **Task:** Return the index of `target` if present, else the index where it would be inserted to keep the array sorted.
> **Key insight:** Both answers are the same number: the first index with `nums[i] ≥ target`. It's lower bound, unchanged.
> **Difficulty:** Easy · **Pattern:** Lower bound · **Also on:** [LC 35](https://leetcode.com/problems/search-insert-position/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/search-insert-position?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 8 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [4. Lower bound](#4-lower-bound) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a sorted array of distinct integers `nums` and a `target`, return the index of `target` if found; otherwise return the index where it would be inserted in order. Must be O(log n).

| Input | Output | Why |
|---|---|---|
| `nums = [1, 3, 5, 6], target = 5` | `2` | found |
| `nums = [1, 3, 5, 6], target = 2` | `1` | between 1 and 3 |
| `nums = [1, 3, 5, 6], target = 7` | `4` | end |

**Constraints:** `1 ≤ n ≤ 10⁴`, `−10⁴ ≤ nums[i], target ≤ 10⁴`, distinct, sorted.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | first i with nums[i] ≥ target | O(n) | O(1) |
| Lower bound | answer-variable binary search with ≥ | O(log n) | O(1) |

---

## 3. Linear scan

**Intuition.** The insertion point is the first element not smaller than the target.

```python
def search_insert_linear(nums, target):
    for i, v in enumerate(nums):
        if v >= target:
            return i
    return len(nums)
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Lower bound

**Intuition.** If `target` exists, the first `≥` element *is* the target. If not, every element left of the first `≥` is smaller, so inserting there keeps order. Default `ans = n` covers "insert at end".

**C++**
```cpp
int searchInsert(vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size() - 1, ans = nums.size();
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] >= target) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Java**
```java
static int searchInsert(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1, ans = nums.length;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] >= target) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Python**
```python
def search_insert(nums, target):
    lo, hi, ans = 0, len(nums) - 1, len(nums)
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] >= target:
            ans, hi = mid, mid - 1
        else:
            lo = mid + 1
    return ans
```

**Complexity:** time **O(log n)**, space **O(1)** — plain lower bound.

---

## Edge cases

- Insert before everything → 0.
- Insert after everything → n.

---

## Common mistakes

1. Returning −1 when not found.
2. Special-casing "found" separately — unnecessary.

---

## Follow-ups

1. With duplicates, insert after all equal elements.
2. Classic `while lo <= hi` without ans variable — what's the answer?

<details><summary>Answer sketches</summary>

**#1:** Use upper bound instead.

**#2:** `lo` at loop exit is the insertion point.
</details>

---

## Flashcards

**Search insert position = ?** #flashcard
Lower bound of target.

**After a failed `lo ≤ hi` binary search, where does lo point?** #flashcard
To the insertion position (first element > target).

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
