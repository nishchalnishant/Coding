---
module: striver/14-arrays
lesson: 2
topic: Largest Element
difficulty: Easy
source: https://takeuforward.org/learning/dsa/largest-element?category=fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, traversal]
---
# 2. Largest Element

← [Linear Search](01-linear-search.md) · [Part 14 index](README.md) · Next → [Second Largest Element](03-second-largest-element.md)

> [!abstract] Problem at a glance
> **Task:** Return the maximum value in `nums`.
> **Key insight:** Seed `best` with `nums[0]` (not 0 and not `INT_MIN` by habit) and update it in a single pass. Sorting also works, but it's O(n log n) for an O(n) question.
> **Difficulty:** Easy · **Pattern:** Array traversal
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/largest-element?category=fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort](#3-sort) · [4. Single pass](#4-single-pass) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-empty integer array `nums`, return its largest element.

| Input | Output | Why |
|---|---|---|
| `nums = [3, 3, 6, 1]` | `6` |  |
| `nums = [-3, -1, -7]` | `-1` | all negative: seeding with 0 would be wrong |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁹ ≤ nums[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort | sort, take the last | O(n log n) | O(1)–O(n) |
| Single pass | track the running max | O(n) | O(1) |

---

## 3. Sort

**Intuition.** After sorting, the max is at the end. Correct, but it does more work than needed and mutates the input.

```python
def largest_sort(nums):
    return sorted(nums)[-1]
```

**Complexity:** time **O(n log n)**, space **O(1)–O(n)**.

---

## 4. Single pass

**Intuition.** Invariant: after index `i`, `best = max(nums[0..i])`. Seeding with `nums[0]` makes it correct for all-negative arrays.

**C++**
```cpp
int largestElement(vector<int>& nums) {
    int best = nums[0];
    for (int x : nums) best = max(best, x);
    return best;
}
```

**Java**
```java
static int largestElement(int[] nums) {
    int best = nums[0];
    for (int x : nums) best = Math.max(best, x);
    return best;
}
```

**Python**
```python
def largest_element(nums):
    best = nums[0]
    for x in nums:
        if x > best:
            best = x
    return best
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- n = 1.
- All negative.
- Max repeated.

---

## Common mistakes

1. `best = 0` → wrong for all-negative input.
2. Empty-array access: confirm `n ≥ 1` with the interviewer.

---

## Follow-ups

1. Max and min in fewest comparisons?
2. Index of the max?

<details><summary>Answer sketches</summary>

**#1:** Compare in pairs: the larger goes against max, the smaller against min → 3n/2 comparisons instead of 2n.

**#2:** Track `bi` alongside `best`; use `>` for the first occurrence, `>=` for the last.
</details>

---

## Flashcards

**Seed for a running max?** #flashcard
nums[0] (or −∞), never 0.

**Comparisons to find both min and max?** #flashcard
About 3n/2 using pairwise comparison.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
