---
module: striver-a2z/12-basic-recursion
lesson: 10
topic: Check if the Array is Sorted
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-the-array-is-sorted-ii?category=basic-recursion&source=strivers-a2z-dsa-sheet
tags: [striver, basic-recursion, recursion, arrays]
---
# 10. Check if the Array is Sorted

← [Reverse an Array (Recursive)](09-reverse-an-array-recursive.md) · [Part 12 index](README.md) · Next → [Sum of Digits in a Given Number](11-sum-of-digits.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `nums` is sorted in non-decreasing order, using recursion.
> **Key insight:** Sorted means every adjacent pair is in order: `f(i) = nums[i] ≤ nums[i + 1] and f(i + 1)`, base `i ≥ n − 1 → true`.
> **Difficulty:** Easy · **Pattern:** Linear recursion over an index
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-the-array-is-sorted-ii?category=basic-recursion&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — compare with the sorted copy](#3-brute--compare-with-the-sorted-copy) · [4. Optimal — adjacent pairs recursively](#4-optimal--adjacent-pairs-recursively) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums`, return `true` if `nums[i] ≤ nums[i + 1]` for all valid `i`. Use recursion.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 2, 5]` | `true` | duplicates allowed |
| `nums = [3, 1, 2]` | `false` |  |
| `nums = [4]` | `true` |  |

**Constraints:** `1 ≤ n ≤ 10³`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — compare with the sorted copy | nums == sorted(nums) | O(n log n) | O(n) |
| Optimal — adjacent pairs recursively | nums[i] ≤ nums[i+1] and f(i + 1) | O(n) | O(n) stack |

---

## 3. Brute — compare with the sorted copy

**Intuition.** Simple, but it does far more work than needed.

```python
def sorted_brute(nums):
    return nums == sorted(nums)
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. Optimal — adjacent pairs recursively

**Intuition.** Non-decreasing order is transitive, so checking only the adjacent pairs is sufficient. The first violation returns false immediately.

**Algorithm**

1. `f(i)`: if `i >= n − 1` return true.
2. If `nums[i] > nums[i + 1]` return false.
3. Return `f(i + 1)`.

**Dry run** — `[3, 1, 2]`: f(0): 3 > 1 → **false**.

**C++**
```cpp
bool sortedFrom(vector<int>& nums, int i) {
    if (i >= (int)nums.size() - 1) return true;
    if (nums[i] > nums[i + 1]) return false;
    return sortedFrom(nums, i + 1);
}
bool isSorted(vector<int>& nums) { return sortedFrom(nums, 0); }
```

**Java**
```java
static boolean sortedFrom(int[] nums, int i) {
    if (i >= nums.length - 1) return true;
    if (nums[i] > nums[i + 1]) return false;
    return sortedFrom(nums, i + 1);
}
static boolean isSorted(int[] nums) { return sortedFrom(nums, 0); }
```

**Python**
```python
def is_sorted(nums, i=0):
    if i >= len(nums) - 1:
        return True
    if nums[i] > nums[i + 1]:
        return False
    return is_sorted(nums, i + 1)
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## Edge cases

- n = 1 → true.
- Equal neighbours are allowed (non-decreasing).

---

## Common mistakes

1. `>=` instead of `>` in the violation check, which rejects duplicates.
2. Accessing `nums[i + 1]` without the `i ≥ n − 1` guard.

---

## Follow-ups

1. Check whether the array is sorted and rotated (LC 1752).
2. Check strictly increasing.

<details><summary>Answer sketches</summary>

**#1:** Count the drops `nums[i] > nums[(i+1) % n]`; valid iff there's at most one.

**#2:** Use `>=` as the violation.
</details>

---

## Flashcards

**Sorted-check recursion base case?** #flashcard
i >= n − 1 → true.

**Why are adjacent pairs enough to check?** #flashcard
≤ is transitive.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
