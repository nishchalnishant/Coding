---
module: striver/13-sorting
lesson: 1
topic: Selection Sort
difficulty: Easy
source: https://takeuforward.org/learning/dsa/selection-sort?category=algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, algorithms, sorting, selection-sort]
---
# 1. Selection Sort

← [Part 13 index](README.md) · Next → [Bubble Sort](02-bubble-sort.md)

> [!abstract] Problem at a glance
> **Task:** Sort `nums` in place using selection sort.
> **Key insight:** For each position `i`, find the minimum of the unsorted suffix `[i, n)` and swap it into `i`. After pass `i` the prefix `[0, i]` is final, so there are n − 1 passes and at most n − 1 swaps.
> **Difficulty:** Easy · **Pattern:** Sorting: select the min
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/selection-sort?category=algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Selection sort](#3-selection-sort) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, sort it in non-decreasing order using selection sort.

| Input | Output | Why |
|---|---|---|
| `nums = [7, 4, 1, 5, 3]` | `[1, 3, 4, 5, 7]` |  |
| `nums = [5, 4, 4, 1, 1]` | `[1, 1, 4, 4, 5]` | duplicates |

**Constraints:** `1 ≤ n ≤ 10³`, `−10⁴ ≤ nums[i] ≤ 10⁴`. Sort in place, in non-decreasing order.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Selection sort | swap min of [i, n) into i | O(n²) in every case | O(1) |

> [!tip] Interview angle
> Selection sort is rarely the answer, but its *minimum number of swaps* property shows up: when writes are expensive (flash memory), or in the "minimum swaps to sort a permutation" puzzle (cycle decomposition).

---

## 3. Selection sort

**Intuition.** Invariant: after pass `i`, `nums[0..i]` holds the i + 1 smallest values in order. Each pass scans the suffix for the index of its minimum, then does one swap. The scan doesn't depend on the input order, so even sorted input costs n(n − 1)/2 comparisons.

**Algorithm**

1. For `i` in `0 .. n − 2`:
2.   `mn = i`; for `j` in `i + 1 .. n − 1`: if `nums[j] < nums[mn]`, `mn = j`.
3.   Swap `nums[i]` and `nums[mn]`.

**Dry run** — `[7 4 1 5 3]` → i = 0: min 1 → `[1 4 7 5 3]` → i = 1: min 3 → `[1 3 7 5 4]` → i = 2: min 4 → `[1 3 4 5 7]` → i = 3: min 5, no change.

**Not stable:** `[2a, 2b, 1]` → the first swap moves `2a` behind `2b`. A stable variant shifts instead of swapping, which makes it insertion-like and costs O(n²) writes.

**C++**
```cpp
void selectionSort(vector<int>& nums) {
    int n = nums.size();
    for (int i = 0; i < n - 1; i++) {
        int mn = i;
        for (int j = i + 1; j < n; j++)
            if (nums[j] < nums[mn]) mn = j;
        swap(nums[i], nums[mn]);
    }
}
```

**Java**
```java
static void selectionSort(int[] nums) {
    int n = nums.length;
    for (int i = 0; i < n - 1; i++) {
        int mn = i;
        for (int j = i + 1; j < n; j++)
            if (nums[j] < nums[mn]) mn = j;
        int t = nums[i]; nums[i] = nums[mn]; nums[mn] = t;
    }
}
```

**Python**
```python
def selection_sort(nums):
    n = len(nums)
    for i in range(n - 1):
        mn = i
        for j in range(i + 1, n):
            if nums[j] < nums[mn]:
                mn = j
        nums[i], nums[mn] = nums[mn], nums[i]
```

**Complexity:** time **O(n²) in every case**, space **O(1)** — comparisons are n(n − 1)/2 regardless of input; swaps ≤ n − 1.

---

## Edge cases

- n = 1, and n = 2 in either order.
- Already sorted, reverse sorted.
- All equal; duplicates; negatives.

---

## Common mistakes

1. Swapping every time a smaller `nums[j]` is found, instead of tracking the index: still correct, but O(n²) swaps.
2. Inner loop starting at `i` instead of `i + 1` (harmless, but a wasted comparison).
3. Calling it stable.

---

## Follow-ups

1. Minimum swaps to sort a permutation of 0..n−1.
2. Make it find both min and max per pass.

<details><summary>Answer sketches</summary>

**#1:** Count the cycles of `i → nums[i]`; the answer is n − (#cycles).

**#2:** Double-ended selection: place the min at `l` and the max at `r`, shrink both. Half the passes, same O(n²).
</details>

---

## Flashcards

**Selection sort swaps, at most?** #flashcard
n − 1.

**Is selection sort stable?** #flashcard
No: a long-distance swap can reorder equal keys.

**Selection sort best case?** #flashcard
O(n²): the scan ignores existing order.

**Interview track →** [Sorting deep-dive](../../02-algorithms/00-sorting.md) · [Sorting walkthroughs](../../coding/algorithms/00-sorting.md)
