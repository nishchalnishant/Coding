---
module: striver-a2z/13-sorting
lesson: 7
topic: Recursive Insertion Sort
difficulty: Easy
source: https://takeuforward.org/learning/dsa/recursive-insertion-sort?category=algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, algorithms, sorting, insertion-sort, recursion]
---
# 7. Recursive Insertion Sort

← [Recursive Bubble Sort](06-recursive-bubble-sort.md) · [Part 13 index](README.md) · Next → [Part 14: Arrays](../14-arrays/README.md)

> [!abstract] Problem at a glance
> **Task:** Sort `nums` in place with insertion sort written recursively.
> **Key insight:** To sort `[0, n)`: sort `[0, n − 1)` recursively, then insert `nums[n − 1]` into that sorted prefix. Equivalently, go forward: insert `nums[i]`, then call `f(i + 1)`.
> **Difficulty:** Easy · **Pattern:** Loop → recursion
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/recursive-insertion-sort?category=algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Forward recursion on i](#3-forward-recursion-on-i) · [4. Head recursion on n (classic)](#4-head-recursion-on-n-classic) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, sort it in non-decreasing order using a recursive insertion sort.

| Input | Output | Why |
|---|---|---|
| `nums = [7, 4, 1, 5, 3]` | `[1, 3, 4, 5, 7]` |  |
| `nums = [5, 4, 4, 1, 1]` | `[1, 1, 4, 4, 5]` | duplicates |

**Constraints:** `1 ≤ n ≤ 10³`, `−10⁴ ≤ nums[i] ≤ 10⁴`. Sort in place, in non-decreasing order.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Forward recursion on i | insert nums[i], then f(i + 1) | O(n²) worst, O(n) best | O(n) stack |
| Head recursion on n (classic) | f(n − 1), then insert nums[n − 1] | O(n²) worst, O(n) best | O(n) stack |

---

## 3. Forward recursion on i

**Intuition.** The outer loop index becomes the parameter: process `i`, then hand `i + 1` to the next call.

```python
def insertion_forward(nums, i=1):
    if i >= len(nums):
        return
    key, j = nums[i], i - 1
    while j >= 0 and nums[j] > key:
        nums[j + 1] = nums[j]
        j -= 1
    nums[j + 1] = key
    insertion_forward(nums, i + 1)
```

**Complexity:** time **O(n²) worst, O(n) best**, space **O(n) stack**.

---

## 4. Head recursion on n (classic)

**Intuition.** Leap of faith: assume `f(n − 1)` leaves `nums[0..n−2]` sorted. Then a single insertion of `nums[n − 1]` makes `[0, n)` sorted. Base: `n <= 1` is already sorted. The real work happens as the stack unwinds, so prefixes of length 2, 3, …, n get sorted in that order, just like the loop.

**Algorithm**

1. `f(n)`: if `n <= 1` return.
2. `f(n − 1)`.
3. `key = nums[n − 1]`, `j = n − 2`; shift while `j >= 0 && nums[j] > key`; place `key` at `j + 1`.

**Dry run** — `[7 4 1 5 3]`: f(5) → f(4) → f(3) → f(2) → f(1) returns. f(2) inserts 4 → `[4 7 …]`; f(3) inserts 1 → `[1 4 7 …]`; f(4) inserts 5 → `[1 4 5 7 3]`; f(5) inserts 3 → `[1 3 4 5 7]`.

**C++**
```cpp
void insertionRec(vector<int>& nums, int n) {
    if (n <= 1) return;
    insertionRec(nums, n - 1);
    int key = nums[n - 1], j = n - 2;
    while (j >= 0 && nums[j] > key) {
        nums[j + 1] = nums[j];
        j--;
    }
    nums[j + 1] = key;
}
void insertionSort(vector<int>& nums) { insertionRec(nums, nums.size()); }
```

**Java**
```java
static void insertionRec(int[] nums, int n) {
    if (n <= 1) return;
    insertionRec(nums, n - 1);
    int key = nums[n - 1], j = n - 2;
    while (j >= 0 && nums[j] > key) {
        nums[j + 1] = nums[j];
        j--;
    }
    nums[j + 1] = key;
}
static void insertionSort(int[] nums) { insertionRec(nums, nums.length); }
```

**Python**
```python
def recursive_insertion_sort(nums, n=None):
    if n is None:
        n = len(nums)
    if n <= 1:
        return
    recursive_insertion_sort(nums, n - 1)
    key, j = nums[n - 1], n - 2
    while j >= 0 and nums[j] > key:
        nums[j + 1] = nums[j]
        j -= 1
    nums[j + 1] = key
```

**Complexity:** time **O(n²) worst, O(n) best**, space **O(n) stack**.

---

## Edge cases

- n = 1, and n = 2 in either order.
- Already sorted, reverse sorted.
- All equal; duplicates; negatives.

---

## Common mistakes

1. Inserting before recursing in the head-recursive version: that inserts into an unsorted prefix.
2. Using `n` as an index (`nums[n]`) instead of `n − 1`.

---

## Follow-ups

1. Sort a stack using recursion only (classic).
2. Why prefer the loop?

<details><summary>Answer sketches</summary>

**#1:** Pop the top, sort the rest recursively, then insert the top into the sorted stack recursively: this is exactly insertion sort ([Part 18](../18-recursion/README.md)).

**#2:** Same O(n²) time, but O(1) space instead of an O(n) stack.
</details>

---

## Flashcards

**Recursive insertion sort order of operations?** #flashcard
Sort first n − 1 (recurse), then insert nums[n − 1].

**Which classic stack problem is recursive insertion sort?** #flashcard
Sort a stack using recursion.

**Interview track →** [Sorting deep-dive](../../02-algorithms/00-sorting.md) · [Sorting walkthroughs](../../04-practice/algorithms/00-sorting.md)
