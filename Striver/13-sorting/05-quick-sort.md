---
module: striver/13-sorting
lesson: 5
topic: Quick Sort
difficulty: Medium
source: https://takeuforward.org/learning/dsa/quick-sorting?category=algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, algorithms, sorting, quick-sort, divide-and-conquer, partition]
---
# 5. Quick Sort

← [Merge Sort](04-merge-sort.md) · [Part 13 index](README.md) · Next → [Recursive Bubble Sort](06-recursive-bubble-sort.md)

> [!abstract] Problem at a glance
> **Task:** Sort `nums` in place using quick sort.
> **Key insight:** Partition around a pivot so that everything ≤ pivot is on its left and everything greater is on its right; the pivot is then in its final position. Recurse on both sides. A good pivot gives O(n log n) and in-place sorting; a bad one on sorted input gives O(n²).
> **Difficulty:** Medium · **Pattern:** Divide and conquer: partition
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/quick-sorting?category=algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Lomuto partition (last element as pivot)](#3-lomuto-partition-last-element-as-pivot) · [4. Two-pointer partition, pivot at low (Striver's version) + middle/random pivot](#4-two-pointer-partition-pivot-at-low-strivers-version--middlerandom-pivot) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, sort it in non-decreasing order using quick sort.

| Input | Output | Why |
|---|---|---|
| `nums = [7, 4, 1, 5, 3]` | `[1, 3, 4, 5, 7]` |  |
| `nums = [5, 4, 4, 1, 1]` | `[1, 1, 4, 4, 5]` | duplicates |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁴ ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Lomuto partition (last element as pivot) | i tracks the end of the < pivot zone | O(n log n) avg, O(n²) worst | O(log n) avg stack, O(n) worst |
| Two-pointer partition, pivot at low (Striver's version) + middle/random pivot | i walks right over ≤ pivot, j walks left over > pivot, swap, place pivot at j | O(n log n) avg / best, O(n²) worst (rare with random pivot) | O(log n) avg stack |

> [!tip] Interview angle
> Say the worst case out loud (sorted input with a first/last pivot → O(n²), depth n) and fix it with a random pivot before the interviewer asks. `partition` on its own is the core of Quickselect (k-th largest in O(n) average) and Dutch National Flag (Sort Colors).

---

## 3. Lomuto partition (last element as pivot)

**Intuition.** Scan `j` from `l` to `r − 1`. Whenever `nums[j] < pivot`, swap it into position `i` and advance `i`. Finally swap the pivot into `i`. Simple to write, but it does more swaps than Hoare and degrades on many duplicates.

```python
def quick_lomuto(nums):
    def part(l, r):
        p, i = nums[r], l
        for j in range(l, r):
            if nums[j] < p:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[r] = nums[r], nums[i]
        return i

    def qs(l, r):
        if l < r:
            m = part(l, r)
            qs(l, m - 1)
            qs(m + 1, r)

    qs(0, len(nums) - 1)
```

**Complexity:** time **O(n log n) avg, O(n²) worst**, space **O(log n) avg stack, O(n) worst**.

---

## 4. Two-pointer partition, pivot at low (Striver's version) + middle/random pivot

**Intuition.** Move a well-chosen pivot to `low`. `i` advances while `nums[i] ≤ pivot`; `j` retreats while `nums[j] > pivot`; if `i < j`, swap them. When they cross, `j` is the last index ≤ pivot, so swap the pivot into `j`. Bounds checks (`i ≤ high − 1`, `j ≥ low + 1`) stop the scans from running off the range. Choosing the middle (or a random) element as the pivot avoids the sorted-input worst case.

**Algorithm**

1. `qs(low, high)`: if `low >= high` return.
2. Swap the middle element into `low`; `pivot = nums[low]`; `i = low`, `j = high`.
3. While `i < j`: advance `i` while `nums[i] <= pivot && i <= high − 1`; retreat `j` while `nums[j] > pivot && j >= low + 1`; if `i < j`, swap them.
4. Swap `nums[low]` and `nums[j]`; recurse on `[low, j − 1]` and `[j + 1, high]`.

**Dry run** — `[4 6 2 5 7 9 1 3]`, pivot 4 (low): i stops at 6, j stops at 3 → swap → `[4 3 2 5 7 9 1 6]`; i stops at 5, j at 1 → swap → `[4 3 2 1 7 9 5 6]`; i stops at 7 (idx 4), j at 1 (idx 3), crossed → swap pivot with idx 3 → `[1 3 2 4 7 9 5 6]`. 4 is final.

**Why O(n²) worst:** if the pivot is always the min or max, the partition sizes are n − 1 and 0, so T(n) = T(n − 1) + O(n). **Fixes:** random pivot (expected O(n log n)), median-of-three, introsort (switch to heap sort when depth > 2 log n). **Many duplicates:** a 3-way partition (`< = >`) makes all-equal input O(n).

**C++**
```cpp
int partitionAt(vector<int>& nums, int low, int high) {
    swap(nums[low], nums[low + (high - low) / 2]);
    int pivot = nums[low], i = low, j = high;
    while (i < j) {
        while (nums[i] <= pivot && i <= high - 1) i++;
        while (nums[j] > pivot && j >= low + 1) j--;
        if (i < j) swap(nums[i], nums[j]);
    }
    swap(nums[low], nums[j]);
    return j;
}
void qs(vector<int>& nums, int low, int high) {
    if (low >= high) return;
    int p = partitionAt(nums, low, high);
    qs(nums, low, p - 1);
    qs(nums, p + 1, high);
}
void quickSort(vector<int>& nums) { qs(nums, 0, (int)nums.size() - 1); }
```

**Java**
```java
static int partitionAt(int[] nums, int low, int high) {
    int mid = low + (high - low) / 2, t;
    t = nums[low]; nums[low] = nums[mid]; nums[mid] = t;
    int pivot = nums[low], i = low, j = high;
    while (i < j) {
        while (nums[i] <= pivot && i <= high - 1) i++;
        while (nums[j] > pivot && j >= low + 1) j--;
        if (i < j) { t = nums[i]; nums[i] = nums[j]; nums[j] = t; }
    }
    t = nums[low]; nums[low] = nums[j]; nums[j] = t;
    return j;
}
static void qs(int[] nums, int low, int high) {
    if (low >= high) return;
    int p = partitionAt(nums, low, high);
    qs(nums, low, p - 1);
    qs(nums, p + 1, high);
}
static void quickSort(int[] nums) { qs(nums, 0, nums.length - 1); }
```

**Python**
```python
def quick_sort(nums):
    def partition(low, high):
        mid = (low + high) // 2
        nums[low], nums[mid] = nums[mid], nums[low]
        pivot, i, j = nums[low], low, high
        while i < j:
            while nums[i] <= pivot and i <= high - 1:
                i += 1
            while nums[j] > pivot and j >= low + 1:
                j -= 1
            if i < j:
                nums[i], nums[j] = nums[j], nums[i]
        nums[low], nums[j] = nums[j], nums[low]
        return j

    def qs(low, high):
        if low >= high:
            return
        p = partition(low, high)
        qs(low, p - 1)
        qs(p + 1, high)

    qs(0, len(nums) - 1)
```

**Complexity:** time **O(n log n) avg / best, O(n²) worst (rare with random pivot)**, space **O(log n) avg stack** — balanced partitions → log n levels × O(n) partition work.

---

## Edge cases

- n = 1, and n = 2 in either order.
- Already sorted, reverse sorted.
- All equal; duplicates; negatives.
- All equal: this partition puts every element on the left of the pivot, so it degrades to O(n²); 3-way partitioning fixes it.

---

## Common mistakes

1. Missing bounds checks in the `i`/`j` scans → index out of range when the pivot is the max or min.
2. Swapping the pivot with `i` instead of `j` at the end.
3. Recursing on `[low, p]` instead of `[low, p − 1]` → infinite recursion.
4. Always using the first element as the pivot on sorted input → O(n²) time and depth n (stack overflow at 10⁵).

---

## Follow-ups

1. K-th largest element (LC 215).
2. Sort Colors (LC 75).
3. Guarantee O(log n) stack depth.

<details><summary>Answer sketches</summary>

**#1:** Quickselect: partition, then recurse into only the side containing index n − k. O(n) average.

**#2:** Dutch National Flag: 3-way partition with `low`, `mid`, `high`, in one pass.

**#3:** Recurse on the smaller side, loop on the larger one (tail-call elimination by hand).
</details>

---

## Flashcards

**Quick sort worst case and trigger?** #flashcard
O(n²): pivot is always the min/max (e.g. sorted input with first/last pivot).

**Fix for quick sort's worst case?** #flashcard
Random or median-of-three pivot; introsort fallback.

**Is quick sort stable?** #flashcard
No.

**After partition, where is the pivot?** #flashcard
At its final sorted index.

**Quickselect average time?** #flashcard
O(n).

**Interview track →** [Sorting deep-dive](../../02-algorithms/00-sorting.md) · [Sorting walkthroughs](../../coding/algorithms/00-sorting.md)
