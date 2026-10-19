---
module: striver/13-sorting
lesson: 3
topic: Insertion Sort
difficulty: Easy
source: https://takeuforward.org/learning/dsa/insertion-sorting?category=algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, algorithms, sorting, insertion-sort]
---
# 3. Insertion Sort

← [Bubble Sort](02-bubble-sort.md) · [Part 13 index](README.md) · Next → [Merge Sort](04-merge-sort.md)

> [!abstract] Problem at a glance
> **Task:** Sort `nums` in place using insertion sort.
> **Key insight:** Grow a sorted prefix: take `key = nums[i]`, shift every larger element of `[0, i)` one step right, and drop `key` into the gap. The cost is O(n + inversions), so it's O(n) on nearly sorted data.
> **Difficulty:** Easy · **Pattern:** Sorting: insert into sorted prefix
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insertion-sorting?category=algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Swap-based](#3-swap-based) · [4. Shift-based (standard)](#4-shift-based-standard) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, sort it in non-decreasing order using insertion sort.

| Input | Output | Why |
|---|---|---|
| `nums = [7, 4, 1, 5, 3]` | `[1, 3, 4, 5, 7]` |  |
| `nums = [5, 4, 4, 1, 1]` | `[1, 1, 4, 4, 5]` | duplicates |

**Constraints:** `1 ≤ n ≤ 10³`, `−10⁴ ≤ nums[i] ≤ 10⁴`. Sort in place, in non-decreasing order.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Swap-based | swap key left while smaller | O(n²) worst, O(n) best | O(1) |
| Shift-based (standard) | hold key, shift larger right, place once | O(n²) worst / avg, O(n) best | O(1) |

> [!tip] Interview angle
> Insertion sort is the right answer for tiny or nearly-sorted inputs. TimSort and introsort switch to it below ~16–32 elements. Mention that when you're asked why library sorts are fast.

---

## 3. Swap-based

**Intuition.** Correct, but each step is a 3-write swap.

```python
def insertion_swap(nums):
    for i in range(1, len(nums)):
        j = i
        while j > 0 and nums[j - 1] > nums[j]:
            nums[j - 1], nums[j] = nums[j], nums[j - 1]
            j -= 1
```

**Complexity:** time **O(n²) worst, O(n) best**, space **O(1)**.

---

## 4. Shift-based (standard)

**Intuition.** Invariant: before step `i`, `nums[0..i−1]` is sorted. Hold `key`, move each larger element one slot right, and write `key` once into the hole. Using strict `>` stops at equal keys, so it's stable.

**Algorithm**

1. For `i` in `1 .. n − 1`:
2.   `key = nums[i]`, `j = i − 1`.
3.   While `j >= 0` and `nums[j] > key`: `nums[j + 1] = nums[j]`, `j−−`.
4.   `nums[j + 1] = key`.

**Dry run** — `[7 4 1 5 3]`: i = 1 → `[4 7 1 5 3]`; i = 2 → `[1 4 7 5 3]`; i = 3 → `[1 4 5 7 3]`; i = 4 → `[1 3 4 5 7]`.

**Binary insertion sort** finds the slot with binary search (O(log n) comparisons) but still shifts O(n), so it stays O(n²) overall.

**C++**
```cpp
void insertionSort(vector<int>& nums) {
    int n = nums.size();
    for (int i = 1; i < n; i++) {
        int key = nums[i], j = i - 1;
        while (j >= 0 && nums[j] > key) {
            nums[j + 1] = nums[j];
            j--;
        }
        nums[j + 1] = key;
    }
}
```

**Java**
```java
static void insertionSort(int[] nums) {
    int n = nums.length;
    for (int i = 1; i < n; i++) {
        int key = nums[i], j = i - 1;
        while (j >= 0 && nums[j] > key) {
            nums[j + 1] = nums[j];
            j--;
        }
        nums[j + 1] = key;
    }
}
```

**Python**
```python
def insertion_sort(nums):
    for i in range(1, len(nums)):
        key, j = nums[i], i - 1
        while j >= 0 and nums[j] > key:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key
```

**Complexity:** time **O(n²) worst / avg, O(n) best**, space **O(1)** — each shift fixes one inversion, so the work is n + (#inversions).

---

## Edge cases

- n = 1, and n = 2 in either order.
- Already sorted, reverse sorted.
- All equal; duplicates; negatives.

---

## Common mistakes

1. Checking `nums[j] > key` before `j >= 0`, which reads `nums[−1]` (wraps silently in Python).
2. Writing `nums[j] = key` instead of `nums[j + 1]`.
3. Comparing with `nums[i]` inside the loop after it's been overwritten. Save `key` first.

---

## Follow-ups

1. Insertion Sort List (LC 147).
2. Each element is at most k away from its sorted position.

<details><summary>Answer sketches</summary>

**#1:** Dummy head; for each node, walk from the dummy to find the slot, and splice it in.

**#2:** Insertion sort runs in O(nk); a min-heap of size k + 1 gives O(n log k) ([Part 26](../26-heaps/README.md)).
</details>

---

## Flashcards

**Insertion sort cost in terms of inversions?** #flashcard
O(n + inversions).

**Why do library sorts use insertion sort for small runs?** #flashcard
Low overhead, cache-friendly, O(n) on nearly sorted data.

**Insertion sort loop condition order?** #flashcard
j >= 0 first, then nums[j] > key.

**Interview track →** [Sorting deep-dive](../../02-algorithms/00-sorting.md) · [Sorting walkthroughs](../../coding/algorithms/00-sorting.md)
