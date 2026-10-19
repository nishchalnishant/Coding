---
module: striver/09-basic-arrays
lesson: 3
topic: Check if the Array is Sorted
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-the-array-is-sorted-i?category=basic-arrays&source=strivers-a2z-dsa-sheet
tags: [striver, basic-arrays, arrays]
---
# 3. Check if the Array is Sorted

← [Count of Odd Numbers in Array](02-count-of-odd-numbers-in-array.md) · [Part 9 index](README.md) · Next → [Reverse an Array](04-reverse-an-array.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `nums` is sorted in non-decreasing order.
> **Key insight:** Sortedness is a local property. If every adjacent pair satisfies `a[i-1] ≤ a[i]`, the whole array is sorted, because `≤` is transitive.
> **Difficulty:** Easy · **Pattern:** Adjacent-pair scan
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-the-array-is-sorted-i?category=basic-arrays&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — compare with sorted copy](#3-brute--compare-with-sorted-copy) · [4. Better — all pairs](#4-better--all-pairs) · [5. Optimal — adjacent pairs](#5-optimal--adjacent-pairs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums`, return `true` if `nums[i-1] ≤ nums[i]` for every valid `i` (equal neighbours allowed).

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3, 4, 5]` | `true` |  |
| `nums = [1, 2, 1, 4, 5]` | `false` | 2 > 1 |
| `nums = [2, 2, 2]` | `true` | non-decreasing allows ties |
| `nums = [7]` | `true` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — compare with sorted copy | `nums == sorted(nums)` | O(n log n) | O(n) |
| Better — all pairs | check every i < j | O(n²) | O(1) |
| Optimal — adjacent pairs | first `a[i-1] > a[i]` → false | O(n) | O(1) |

---

## 3. Brute — compare with sorted copy

**Intuition.** Sort a copy and compare. It's correct, but it spends a sort to answer a yes/no question that one pass can settle.

```python
def is_sorted_brute(nums):
    return nums == sorted(nums)
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. Better — all pairs

**Intuition.** Check the definition literally: for every `i < j`, `a[i] ≤ a[j]`. Shown to motivate the transitivity argument that removes the inner loop.

```python
def is_sorted_pairs(nums):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] > nums[j]:
                return False
    return True
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 5. Optimal — adjacent pairs

**Intuition.** If `a[0] ≤ a[1]` and `a[1] ≤ a[2]`, then `a[0] ≤ a[2]`. Chaining the adjacent checks covers every pair. Return on the first violation.

**Algorithm**

1. For `i = 1 .. n-1`: if `nums[i-1] > nums[i]`, return false.
2. Return true.

**Dry run** — `[1, 2, 1, 4, 5]`: i = 1 → 1 ≤ 2 ✓; i = 2 → 2 > 1 ✗ → **false**.

**C++**
```cpp
bool isSorted(vector<int>& nums) {
    for (size_t i = 1; i < nums.size(); i++)
        if (nums[i - 1] > nums[i]) return false;
    return true;
}
```

**Java**
```java
static boolean isSorted(int[] nums) {
    for (int i = 1; i < nums.length; i++)
        if (nums[i - 1] > nums[i]) return false;
    return true;
}
```

**Python**
```python
def is_sorted(nums):
    for i in range(1, len(nums)):
        if nums[i - 1] > nums[i]:
            return False
    return True
```

**Complexity:** time **O(n)**, space **O(1)** — n − 1 comparisons at most.

---

## Edge cases

- Empty or single element → true.
- Duplicates → still sorted (`≥`, not `>`).
- Violation in the last pair only (`[1, 2, 3, 2]`).

---

## Common mistakes

1. Using `>=` in the check, which rejects ties.
2. Looping `i` to `n` and reading `nums[i+1]` out of bounds.
3. In C++, `nums.size() - 1` when size is 0 underflows to a huge unsigned value. Start at `i = 1` instead.

---

## Follow-ups

1. Is the array sorted and rotated? (LC 1752)
2. Check strictly increasing.

<details><summary>Answer sketches</summary>

**#1:** Count the drops `a[i] > a[(i+1) % n]` around the circle. It's sorted and rotated iff there's at most one drop.

**#2:** Change the test to `nums[i-1] >= nums[i]`.
</details>

---

## Flashcards

**Why are adjacent checks enough for sortedness?** #flashcard
≤ is transitive, so the adjacent inequalities chain into every pair.

**Sorted and rotated test?** #flashcard
At most one circular drop a[i] > a[(i+1) % n].

**Interview track →** [Arrays deep-dive](../../01-data-structures/01-array.md) · [Two pointers](../../02-algorithms/03-two-pointers.md) · [Concept: basic arrays](../07-concept-basics/02-basic-arrays.md)
