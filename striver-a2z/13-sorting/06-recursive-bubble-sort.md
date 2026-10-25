---
module: striver-a2z/13-sorting
lesson: 6
topic: Recursive Bubble Sort
difficulty: Easy
source: https://takeuforward.org/learning/dsa/recursive-bubble-sort?category=algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, algorithms, sorting, bubble-sort, recursion]
---
# 6. Recursive Bubble Sort

← [Quick Sort](05-quick-sort.md) · [Part 13 index](README.md) · Next → [Recursive Insertion Sort](07-recursive-insertion-sort.md)

> [!abstract] Problem at a glance
> **Task:** Sort `nums` in place with bubble sort, replacing the outer loop with recursion.
> **Key insight:** One pass over `[0, n)` puts the maximum at index `n − 1`; then sort the first `n − 1` recursively. Base: `n ≤ 1`. If a pass made no swaps, return early.
> **Difficulty:** Easy · **Pattern:** Loop → recursion
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/recursive-bubble-sort?category=algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive outer loop](#3-recursive-outer-loop) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, sort it in non-decreasing order using a recursive bubble sort.

| Input | Output | Why |
|---|---|---|
| `nums = [7, 4, 1, 5, 3]` | `[1, 3, 4, 5, 7]` |  |
| `nums = [5, 4, 4, 1, 1]` | `[1, 1, 4, 4, 5]` | duplicates |

**Constraints:** `1 ≤ n ≤ 10³`, `−10⁴ ≤ nums[i] ≤ 10⁴`. Sort in place, in non-decreasing order.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive outer loop | one pass, then f(n − 1) | O(n²) worst, O(n) best | O(n) stack |

---

## 3. Recursive outer loop

**Intuition.** The outer loop's variable `end` becomes the parameter `n`. Each call does one bubbling pass over `[0, n)`, which fixes `nums[n − 1]`, then recurses on the shorter prefix. The `swapped` flag carries over as the early return.

**Algorithm**

1. `f(n)`: if `n <= 1` return.
2. `swapped = false`; for `j` in `0 .. n − 2`: if `nums[j] > nums[j + 1]`, swap and set `swapped`.
3. If not `swapped`, return.
4. `f(n − 1)`.

**Dry run** — `[7 4 1 5 3]`: f(5) → `[4 1 5 3 7]`; f(4) → `[1 4 3 5 7]`; f(3) → `[1 3 4 5 7]`; f(2): no swaps, return.

Fully recursive (both loops): `pass(j, n)` does one comparison and calls `pass(j + 1, n)`. It's O(n²) calls in total, but the stack depth stays O(n).

**C++**
```cpp
void bubbleRec(vector<int>& nums, int n) {
    if (n <= 1) return;
    bool swapped = false;
    for (int j = 0; j < n - 1; j++) {
        if (nums[j] > nums[j + 1]) {
            swap(nums[j], nums[j + 1]);
            swapped = true;
        }
    }
    if (!swapped) return;
    bubbleRec(nums, n - 1);
}
void bubbleSort(vector<int>& nums) { bubbleRec(nums, nums.size()); }
```

**Java**
```java
static void bubbleRec(int[] nums, int n) {
    if (n <= 1) return;
    boolean swapped = false;
    for (int j = 0; j < n - 1; j++) {
        if (nums[j] > nums[j + 1]) {
            int t = nums[j]; nums[j] = nums[j + 1]; nums[j + 1] = t;
            swapped = true;
        }
    }
    if (!swapped) return;
    bubbleRec(nums, n - 1);
}
static void bubbleSort(int[] nums) { bubbleRec(nums, nums.length); }
```

**Python**
```python
def recursive_bubble_sort(nums, n=None):
    if n is None:
        n = len(nums)
    if n <= 1:
        return
    swapped = False
    for j in range(n - 1):
        if nums[j] > nums[j + 1]:
            nums[j], nums[j + 1] = nums[j + 1], nums[j]
            swapped = True
    if swapped:
        recursive_bubble_sort(nums, n - 1)
```

**Complexity:** time **O(n²) worst, O(n) best**, space **O(n) stack** — depth ≤ n, so this is a teaching exercise, not production code.

---

## Edge cases

- n = 1, and n = 2 in either order.
- Already sorted, reverse sorted.
- All equal; duplicates; negatives.

---

## Common mistakes

1. Recursing with `n` instead of `n − 1` → infinite recursion.
2. Inner loop to `n` → reads `nums[n]`.
3. Forgetting the early return, which loses the O(n) best case.

---

## Follow-ups

1. Make both loops recursive.
2. Stack depth for n = 10⁵ in Python?

<details><summary>Answer sketches</summary>

**#1:** `pass(j, n)`: if `j == n − 1` return; compare/swap `j, j + 1`; `pass(j + 1, n)`. Then `sort(n)`: `pass(0, n)`; `sort(n − 1)`.

**#2:** 10⁵ > 1000: RecursionError. Use the loop.
</details>

---

## Flashcards

**Recursive bubble sort: what does one call fix?** #flashcard
The max of [0, n) lands at n − 1.

**Recursive bubble sort base case?** #flashcard
n <= 1, or a pass with no swaps.

**Interview track →** [Sorting deep-dive](../../02-algorithms/00-sorting.md) · [Sorting walkthroughs](../../04-practice/algorithms/00-sorting.md)
