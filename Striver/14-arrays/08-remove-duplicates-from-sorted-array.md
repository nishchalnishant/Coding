---
module: striver/14-arrays
lesson: 8
topic: Remove Duplicates from Sorted Array
difficulty: Easy
source: https://takeuforward.org/learning/dsa/remove-duplicates-from-sorted-array?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, two-pointers, in-place]
---
# 8. Remove Duplicates from Sorted Array

← [Move Zeros to End](07-move-zeros-to-end.md) · [Part 14 index](README.md) · Next → [Find Missing Number](09-find-missing-number.md)

> [!abstract] Problem at a glance
> **Task:** Remove duplicates in place from a sorted array; return the count `k` of unique elements, which must occupy `nums[0..k)`.
> **Key insight:** Sorted means duplicates are adjacent. Keep a write index `i` at the last unique value; when `nums[j] != nums[i]`, write it to `++i`. Answer `i + 1`.
> **Difficulty:** Easy · **Pattern:** Two pointers: read/write · **Also on:** [LC 26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/remove-duplicates-from-sorted-array?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Set](#3-set) · [4. Two pointers](#4-two-pointers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` sorted in non-decreasing order, remove the duplicates in place so that each unique element appears once, in order, in the first `k` slots. Return `k`. What's beyond index `k − 1` doesn't matter.

| Input | Output | Why |
|---|---|---|
| `nums = [0, 0, 3, 3, 5, 6]` | `k = 4, nums[0..4) = [0, 3, 5, 6]` |  |
| `nums = [-2, 2, 4, 4, 4, 4, 5, 5]` | `k = 4, [-2, 2, 4, 5]` |  |

**Constraints:** `1 ≤ n ≤ 10⁴`, sorted, `−10⁴ ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Set | collect distinct values, write back | O(n log n) ordered set / O(n) hash + sort | O(n) |
| Two pointers | i = last unique, j scans | O(n) | O(1) |

> [!tip] Interview angle
> The grader checks both `k` and the prefix. Say so, and state that the tail is garbage, so the interviewer knows you understand the contract.

---

## 3. Set

**Intuition.** Insert into an ordered set (C++ `set`, Java `TreeSet`), then copy the values to the front. Ignores the fact that the input is already sorted.

```python
def remove_dups_set(nums):
    uniq = sorted(set(nums))
    nums[:len(uniq)] = uniq
    return len(uniq)
```

**Complexity:** time **O(n log n) ordered set / O(n) hash + sort**, space **O(n)**.

---

## 4. Two pointers

**Intuition.** Invariant: `nums[0..i]` is the de-duplicated prefix of `nums[0..j)`. Because the input is sorted, `nums[j]` is new exactly when it differs from `nums[i]`.

**Dry run** — `[0 0 3 3 5 6]`: i=0; j=2 (3≠0) → nums[1]=3, i=1; j=4 (5≠3) → nums[2]=5, i=2; j=5 → nums[3]=6, i=3. k = 4.

**At most two copies (LC 80):** compare `nums[j]` with `nums[w − 2]` instead of `nums[w − 1]`; generalises to at most `t` copies.

**C++**
```cpp
int removeDuplicates(vector<int>& nums) {
    int i = 0;
    for (int j = 1; j < (int)nums.size(); j++)
        if (nums[j] != nums[i]) nums[++i] = nums[j];
    return i + 1;
}
```

**Java**
```java
static int removeDuplicates(int[] nums) {
    int i = 0;
    for (int j = 1; j < nums.length; j++)
        if (nums[j] != nums[i]) nums[++i] = nums[j];
    return i + 1;
}
```

**Python**
```python
def remove_duplicates(nums):
    i = 0
    for j in range(1, len(nums)):
        if nums[j] != nums[i]:
            i += 1
            nums[i] = nums[j]
    return i + 1
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- n = 1 → 1.
- All equal → 1.
- Already unique → n.

---

## Common mistakes

1. Returning `i` instead of `i + 1`.
2. Comparing `nums[j]` with `nums[j − 1]` *after* overwriting: works here, but comparing with the write position is the reusable form.
3. Using this on an unsorted array: it only removes *adjacent* duplicates.

---

## Follow-ups

1. Allow at most two of each (LC 80).
2. Unsorted input?

<details><summary>Answer sketches</summary>

**#1:** Write `nums[j]` when `w < 2` or `nums[j] != nums[w − 2]`.

**#2:** Hash set of seen values with a write index: O(n) time, O(n) space, preserves first-occurrence order.
</details>

---

## Flashcards

**Remove duplicates (sorted): return value?** #flashcard
i + 1, the length of the unique prefix.

**Generalise to at most t copies?** #flashcard
Write when nums[j] != nums[w − t].

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
