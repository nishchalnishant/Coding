---
module: striver-a2z/14-arrays
lesson: 1
topic: Linear Search
difficulty: Easy
source: https://takeuforward.org/learning/dsa/linear-search?category=fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, traversal]
---
# 1. Linear Search

← [Part 14 index](README.md) · Next → [Largest Element](02-largest-element.md)

> [!abstract] Problem at a glance
> **Task:** Return the first index of `target` in `nums`, or −1 if it's absent.
> **Key insight:** Scan left to right and return at the first match. This is the only option for unsorted data with no preprocessing, and the baseline that binary search and hashing improve on.
> **Difficulty:** Easy · **Pattern:** Array traversal · **Also on:** GfG Search an Element
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/linear-search?category=fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` and an integer `target`, return the smallest index `i` with `nums[i] == target`, or `-1` if there isn't one.

| Input | Output | Why |
|---|---|---|
| `nums = [2, 3, 4, 5, 3], target = 3` | `1` | first occurrence |
| `nums = [2, -4, 4, 0, 10], target = 6` | `-1` | absent |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁹ ≤ nums[i], target ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | return at the first match | O(n) | O(1) |

---

## 3. Linear scan

**Intuition.** Check every index in order. The first match is the answer, so return immediately. Falling off the end means the target is absent. Best case O(1) (match at index 0), worst case O(n).

**C++**
```cpp
int linearSearch(vector<int>& nums, int target) {
    for (int i = 0; i < (int)nums.size(); i++)
        if (nums[i] == target) return i;
    return -1;
}
```

**Java**
```java
static int linearSearch(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++)
        if (nums[i] == target) return i;
    return -1;
}
```

**Python**
```python
def linear_search(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- Target at index 0 or n − 1.
- Duplicates: return the first.
- Target absent.

---

## Common mistakes

1. Returning inside the loop's `else` branch (−1 after checking only index 0).
2. Returning the last match instead of the first.

---

## Follow-ups

1. Many queries on the same array?
2. Last occurrence?

<details><summary>Answer sketches</summary>

**#1:** Sort once + binary search (O(log n) per query), or build a value → first-index hash map (O(1) per query).

**#2:** Scan from the right, or keep overwriting the answer.
</details>

---

## Flashcards

**Linear search time, best/worst?** #flashcard
O(1) best, O(n) worst.

**When is linear search the right choice?** #flashcard
One query on unsorted data: preprocessing costs more than it saves.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
