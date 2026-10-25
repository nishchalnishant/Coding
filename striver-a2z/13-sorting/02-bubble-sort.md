---
module: striver-a2z/13-sorting
lesson: 2
topic: Bubble Sort
difficulty: Easy
source: https://takeuforward.org/learning/dsa/bubble-sort?category=algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, algorithms, sorting, bubble-sort]
---
# 2. Bubble Sort

← [Selection Sort](01-selection-sort.md) · [Part 13 index](README.md) · Next → [Insertion Sort](03-insertion-sort.md)

> [!abstract] Problem at a glance
> **Task:** Sort `nums` in place using bubble sort.
> **Key insight:** Each pass swaps adjacent out-of-order pairs, which carries the largest unsorted element to the end. If a pass makes no swap, the array is sorted, so the `swapped` flag gives O(n) on sorted input.
> **Difficulty:** Easy · **Pattern:** Sorting: adjacent swaps
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/bubble-sort?category=algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Plain bubble sort](#3-plain-bubble-sort) · [4. Optimised — early exit with `swapped`](#4-optimised--early-exit-with-swapped) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, sort it in non-decreasing order using bubble sort.

| Input | Output | Why |
|---|---|---|
| `nums = [7, 4, 1, 5, 3]` | `[1, 3, 4, 5, 7]` |  |
| `nums = [5, 4, 4, 1, 1]` | `[1, 1, 4, 4, 5]` | duplicates |

**Constraints:** `1 ≤ n ≤ 10³`, `−10⁴ ≤ nums[i] ≤ 10⁴`. Sort in place, in non-decreasing order.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Plain bubble sort | n − 1 full passes | O(n²) always | O(1) |
| Optimised — early exit with `swapped` | stop after a pass with no swaps | O(n²) worst / avg, O(n) best | O(1) |

---

## 3. Plain bubble sort

**Intuition.** After pass `k`, the last `k` positions are final, so the inner loop can stop at `n − 1 − k`.

```python
def bubble_plain(nums):
    n = len(nums)
    for k in range(n - 1):
        for j in range(n - 1 - k):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
```

**Complexity:** time **O(n²) always**, space **O(1)**.

---

## 4. Optimised — early exit with `swapped`

**Intuition.** A pass with zero swaps means every adjacent pair is in order, so the whole array is sorted. Only strict `>` swaps, so equal elements never cross, which is why bubble sort is stable.

**Algorithm**

1. For `end` from `n − 1` down to 1:
2.   `swapped = false`.
3.   For `j` in `0 .. end − 1`: if `nums[j] > nums[j + 1]`, swap and set `swapped = true`.
4.   If not `swapped`, break.

**Dry run** — `[7 4 1 5 3]` → pass 1 `[4 1 5 3 7]` → pass 2 `[1 4 3 5 7]` → pass 3 `[1 3 4 5 7]` → pass 4: no swaps, stop.

Each swap removes exactly one inversion, so the total swaps = number of inversions (up to n(n − 1)/2).

**C++**
```cpp
void bubbleSort(vector<int>& nums) {
    int n = nums.size();
    for (int end = n - 1; end > 0; end--) {
        bool swapped = false;
        for (int j = 0; j < end; j++) {
            if (nums[j] > nums[j + 1]) {
                swap(nums[j], nums[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}
```

**Java**
```java
static void bubbleSort(int[] nums) {
    int n = nums.length;
    for (int end = n - 1; end > 0; end--) {
        boolean swapped = false;
        for (int j = 0; j < end; j++) {
            if (nums[j] > nums[j + 1]) {
                int t = nums[j]; nums[j] = nums[j + 1]; nums[j + 1] = t;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}
```

**Python**
```python
def bubble_sort(nums):
    n = len(nums)
    for end in range(n - 1, 0, -1):
        swapped = False
        for j in range(end):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:
            break
```

**Complexity:** time **O(n²) worst / avg, O(n) best**, space **O(1)**.

---

## Edge cases

- n = 1, and n = 2 in either order.
- Already sorted, reverse sorted.
- All equal; duplicates; negatives.

---

## Common mistakes

1. Inner loop to `n − 1` every pass, re-checking the finished tail.
2. `>=` in the comparison: equal elements swap, so it's no longer stable and does extra work.
3. Resetting `swapped` outside the outer loop.

---

## Follow-ups

1. Count the swaps bubble sort would make, for n = 10⁵.
2. Cocktail shaker sort.

<details><summary>Answer sketches</summary>

**#1:** That's the inversion count: merge-sort counting in O(n log n) ([Part 14](../14-arrays/README.md)).

**#2:** Alternate left-to-right and right-to-left passes; it helps when small elements sit at the end ("turtles").
</details>

---

## Flashcards

**Bubble sort best case and why?** #flashcard
O(n): one pass with no swaps triggers the early exit.

**Total swaps in bubble sort?** #flashcard
The number of inversions.

**Is bubble sort stable?** #flashcard
Yes, with a strict > comparison.

**Interview track →** [Sorting deep-dive](../../02-algorithms/00-sorting.md) · [Sorting walkthroughs](../../04-practice/algorithms/00-sorting.md)
