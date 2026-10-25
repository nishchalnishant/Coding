---
module: striver-a2z/16-binary-search
lesson: 7
topic: First and Last Occurrence
difficulty: Easy
source: https://takeuforward.org/learning/dsa/first-and-last-occurrence?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search]
---
# 7. First and Last Occurrence

← [Floor and Ceil in Sorted Array](06-floor-and-ceil.md) · [Part 16 index](README.md) · Next → [Search in Rotated Sorted Array I](08-search-in-rotated-sorted-array-i.md)

> [!abstract] Problem at a glance
> **Task:** Return `[first, last]` indices of `target` in a sorted array, or `[−1, −1]`.
> **Key insight:** First = lower bound (if it holds target). Last = upper bound − 1. Or write one search with a flag: on a match, record and keep going left (first) or right (last).
> **Difficulty:** Easy · **Pattern:** Lower / upper bound · **Also on:** [LC 34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/first-and-last-occurrence?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 12 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [4. Lower bound and upper bound](#4-lower-bound-and-upper-bound) · [5. One search, two directions](#5-one-search-two-directions) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a sorted array `nums` (duplicates allowed) and `target`, return the first and last index of `target`. If absent, return `[-1, -1]`. Must be O(log n).

| Input | Output | Why |
|---|---|---|
| `nums = [5, 7, 7, 8, 8, 10], target = 8` | `[3, 4]` |  |
| `nums = [5, 7, 7, 8, 8, 10], target = 6` | `[-1, -1]` | absent |
| `nums = [], target = 0` | `[-1, -1]` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`, `−10⁹ ≤ nums[i], target ≤ 10⁹`, sorted non-decreasing.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | first and last match in one pass | O(n) | O(1) |
| Lower bound and upper bound | first = lb; last = ub − 1; check presence | O(log n) | O(1) |
| One search, two directions | on match record and continue left (first) or right (last) | O(log n) | O(1) |

> [!tip] Interview angle
> The trap: finding one occurrence then expanding left/right linearly is O(n) on `[8, 8, 8, …, 8]`. Interviewers ask for this exact input.

---

## 3. Linear scan

**Intuition.** Record the first index on the first match; keep overwriting `last`.

```python
def search_range_linear(nums, target):
    first = last = -1
    for i, v in enumerate(nums):
        if v == target:
            if first == -1:
                first = i
            last = i
    return [first, last]
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Lower bound and upper bound

**Intuition.** `lb = lower_bound(target)`. If `lb == n` or `nums[lb] != target`, it's absent. Otherwise last is `upper_bound(target) − 1`.

```python
from bisect import bisect_left, bisect_right
def search_range_bounds(nums, target):
    lb = bisect_left(nums, target)
    if lb == len(nums) or nums[lb] != target:
        return [-1, -1]
    return [lb, bisect_right(nums, target) - 1]
```

**Complexity:** time **O(log n)**, space **O(1)**.

---

## 5. One search, two directions

**Intuition.** A single helper with a flag. On `nums[mid] == target`, store `mid`; for the first occurrence continue in the left half, for the last in the right half. Less/greater cases are normal binary search. This is the form most interviewers expect because it shows you understand *why* lower bound works.

**Dry run** — `[5 7 7 8 8 10]`, t = 8, first: mid 2 (7) lo 3; mid 4 (8) ans 4, hi 3; mid 3 (8) ans 3, hi 2 → 3. Last: mid 2 lo 3; mid 4 ans 4, lo 5; mid 5 (10) hi 4 → 4.

**C++**
```cpp
int occ(vector<int>& a, int t, bool first) {
    int lo = 0, hi = (int)a.size() - 1, ans = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == t) { ans = mid; if (first) hi = mid - 1; else lo = mid + 1; }
        else if (a[mid] < t) lo = mid + 1;
        else hi = mid - 1;
    }
    return ans;
}
vector<int> searchRange(vector<int>& nums, int target) {
    return {occ(nums, target, true), occ(nums, target, false)};
}
```

**Java**
```java
static int occ(int[] a, int t, boolean first) {
    int lo = 0, hi = a.length - 1, ans = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == t) { ans = mid; if (first) hi = mid - 1; else lo = mid + 1; }
        else if (a[mid] < t) lo = mid + 1;
        else hi = mid - 1;
    }
    return ans;
}
static int[] searchRange(int[] nums, int target) {
    return new int[]{occ(nums, target, true), occ(nums, target, false)};
}
```

**Python**
```python
def search_range(nums, target):
    def occ(first):
        lo, hi, ans = 0, len(nums) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                ans = mid
                if first:
                    hi = mid - 1
                else:
                    lo = mid + 1
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
    return [occ(True), occ(False)]
```

**Complexity:** time **O(log n)**, space **O(1)** — two O(log n) searches.

---

## Edge cases

- Empty array.
- Every element equals target.
- Single occurrence → first = last.

---

## Common mistakes

1. Finding one match and expanding linearly — O(n) worst case.
2. Forgetting the presence check after lower bound (`lb == n`).
3. Returning `ub` instead of `ub − 1` for the last index.

---

## Follow-ups

1. Count occurrences.
2. Range of values in [a, b].

<details><summary>Answer sketches</summary>

**#1:** `last − first + 1` — next-but-two problem.

**#2:** `[lower_bound(a), upper_bound(b) − 1]`.
</details>

---

## Flashcards

**First occurrence via binary search?** #flashcard
On match: record, hi = mid − 1.

**Last occurrence?** #flashcard
On match: record, lo = mid + 1 (or upper_bound − 1).

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
