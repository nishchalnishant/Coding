---
module: striver-a2z/14-arrays
lesson: 3
topic: Second Largest Element
difficulty: Easy
source: https://takeuforward.org/learning/dsa/second-largest-element?category=fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, traversal]
---
# 3. Second Largest Element

← [Largest Element](02-largest-element.md) · [Part 14 index](README.md) · Next → [Maximum Consecutive Ones](04-maximum-consecutive-ones.md)

> [!abstract] Problem at a glance
> **Task:** Return the second largest *distinct* value in `nums`, or −1 if it doesn't exist.
> **Key insight:** Keep `first` and `second` in one pass. A bigger value demotes `first` into `second`; a value strictly between them replaces `second`. Equal-to-`first` values must be skipped, or duplicates of the max get reported.
> **Difficulty:** Easy · **Pattern:** Array traversal: top-2 · **Also on:** GfG Second Largest
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/second-largest-element?category=fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort + scan from the end](#3-sort--scan-from-the-end) · [4. Two passes](#4-two-passes) · [5. One pass, top-2 tracking](#5-one-pass-top-2-tracking) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, return the second largest distinct element. If no such element exists (all equal, or n = 1), return `-1`.

| Input | Output | Why |
|---|---|---|
| `nums = [8, 8, 7, 6, 5]` | `7` | 8 repeats; distinct second is 7 |
| `nums = [10, 10, 10]` | `-1` | no second distinct value |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ nums[i] ≤ 10⁹` (so −1 is a safe sentinel).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort + scan from the end | first value below the max | O(n log n) | O(1) |
| Two passes | find max; then max of values < max | O(n) | O(1) |
| One pass, top-2 tracking | demote first → second on a new max | O(n) | O(1) |

---

## 3. Sort + scan from the end

**Intuition.** Sort ascending; walk left from `n − 2` until a value differs from the max.

```python
def second_sort(nums):
    a = sorted(nums)
    for i in range(len(a) - 2, -1, -1):
        if a[i] != a[-1]:
            return a[i]
    return -1
```

**Complexity:** time **O(n log n)**, space **O(1)**.

---

## 4. Two passes

**Intuition.** Pass 1 finds `mx`. Pass 2 takes the maximum of all elements strictly less than `mx`.

```python
def second_two_pass(nums):
    mx = max(nums)
    sec = -1
    for x in nums:
        if x != mx and x > sec:
            sec = x
    return sec
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 5. One pass, top-2 tracking

**Intuition.** Invariant: `first` is the max so far, `second` the largest value strictly below it (or −1). For each `x`: if `x > first`, then `second = first`, `first = x`; else if `first > x > second`, `second = x`. Equal to `first` is ignored.

**Dry run** — `[8 8 7 6 5]`: 8 → (8, −1); 8 → equal, skip; 7 → (8, 7); 6, 5 → no change. Answer 7.

Generalises to the k-th largest with a min-heap of size k: O(n log k). See [Part 26](../26-heaps/README.md).

**C++**
```cpp
int secondLargestElement(vector<int>& nums) {
    int first = -1, second = -1;
    for (int x : nums) {
        if (x > first) {
            second = first;
            first = x;
        } else if (x < first && x > second) {
            second = x;
        }
    }
    return second;
}
```

**Java**
```java
static int secondLargestElement(int[] nums) {
    int first = -1, second = -1;
    for (int x : nums) {
        if (x > first) {
            second = first;
            first = x;
        } else if (x < first && x > second) {
            second = x;
        }
    }
    return second;
}
```

**Python**
```python
def second_largest(nums):
    first = second = -1
    for x in nums:
        if x > first:
            first, second = x, first
        elif first > x > second:
            second = x
    return second
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- n = 1 → −1.
- All equal → −1.
- Max repeated many times.
- Second largest is 0 (valid answer, not "missing").

---

## Common mistakes

1. `elif x > second` without `x < first` → duplicates of the max become the second.
2. Forgetting to demote `first` into `second` on a new max.
3. Seeding with −1 when negatives are allowed. Use `INT_MIN` / `None` then.

---

## Follow-ups

1. Second smallest too, in the same pass?
2. K-th largest distinct?

<details><summary>Answer sketches</summary>

**#1:** Mirror logic with `small`, `secondSmall` seeded at +∞.

**#2:** Min-heap of size k over a set of values, or sort the distinct values.
</details>

---

## Flashcards

**Second largest: update when x > first?** #flashcard
second = first, first = x.

**Second largest: when does x update second?** #flashcard
When first > x > second (strictly).

**Second largest when all equal?** #flashcard
Doesn't exist → −1.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
