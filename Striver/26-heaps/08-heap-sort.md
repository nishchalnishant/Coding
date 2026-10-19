---
module: striver/26-heaps
lesson: 8
topic: Heap Sort
difficulty: Medium
source: https://takeuforward.org/learning/dsa/heap-sort?category=theory-and-implementation&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, sorting]
---
# 8. Heap Sort

← [Convert Min Heap to Max Heap](07-convert-min-heap-to-max-heap.md) · [Part 26 index](README.md) · Next → [K-th Largest element in an array](09-k-th-largest-element-in-an-array.md)

> [!abstract] Problem at a glance
> **Task:** Sort an array ascending in place in O(n log n) worst case with O(1) extra space.
> **Key insight:** Build a **max**-heap in place (O(n)). Then n − 1 times swap the root (the current max) with the last element of the heap region, shrink the region by one, and sift the new root down. The sorted suffix grows from the right.
> **Difficulty:** Medium · **Pattern:** Heap as selection engine · **Also on:** [LC 912](https://leetcode.com/problems/sort-an-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/heap-sort?category=theory-and-implementation&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Selection sort](#3-selection-sort) · [4. In-place heap sort](#4-in-place-heap-sort) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Sort `nums` in non-decreasing order in place using heap sort.

| Input | Output | Why |
|---|---|---|
| `nums = [5,2,9,1,5,6]` | `[1,2,5,5,6,9]` |  |
| `nums = [3,2,1]` | `[1,2,3]` |  |

**Constraints:** `0 ≤ n ≤ 5·10⁴`, `−5·10⁴ ≤ nums[i] ≤ 5·10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Selection sort | repeatedly find the max of the unsorted prefix | O(n²) | O(1) |
| In-place heap sort | max-heapify; swap root to end; shrink; sift down | O(n log n) | O(1) |

> [!tip] Interview angle
> Contrast it with the others: heap sort gets O(n log n) **worst case** and O(1) space (merge sort needs O(n) space, quicksort is O(n²) worst case), but it's **not stable** and has poor cache locality, so introsort falls back to it only when quicksort recursion gets too deep.

---

## 3. Selection sort

**Intuition.** Heap sort *is* selection sort. Selection sort finds the max by a linear scan; heap sort keeps the unsorted prefix as a heap so finding and removing the max costs O(log n).

```python
def selection_sort(nums):
    for end in range(len(nums) - 1, 0, -1):
        m = max(range(end + 1), key=nums.__getitem__)
        nums[m], nums[end] = nums[end], nums[m]
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. In-place heap sort

**Intuition.** The max-heap occupies `nums[0..end]` and the sorted tail is `nums[end+1..]`. Each round moves the heap max to position `end`, which is its final place.

**Algorithm**

1. Build a max-heap bottom-up on the whole array.
2. For `end = n − 1 … 1`: swap `nums[0]` and `nums[end]`; sift down 0 within size `end`.

**Dry run** — [3,2,1] is already a max-heap. Swap 3↔1 → [1,2 | 3]; sift 1 → [2,1 | 3]. Swap 2↔1 → [1 | 2,3]. Done.

**C++**
```cpp
void siftDownMax(vector<int>& a, int i, int n) {
    while (true) {
        int b = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && a[l] > a[b]) b = l;
        if (r < n && a[r] > a[b]) b = r;
        if (b == i) return;
        swap(a[i], a[b]); i = b;
    }
}
void heapSort(vector<int>& nums) {
    int n = nums.size();
    for (int i = n / 2 - 1; i >= 0; i--) siftDownMax(nums, i, n);
    for (int end = n - 1; end > 0; end--) {
        swap(nums[0], nums[end]);
        siftDownMax(nums, 0, end);
    }
}
```

**Java**
```java
static void siftDownMax(int[] a, int i, int n) {
    while (true) {
        int b = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && a[l] > a[b]) b = l;
        if (r < n && a[r] > a[b]) b = r;
        if (b == i) return;
        int t = a[i]; a[i] = a[b]; a[b] = t; i = b;
    }
}
static void heapSort(int[] nums) {
    int n = nums.length;
    for (int i = n / 2 - 1; i >= 0; i--) siftDownMax(nums, i, n);
    for (int end = n - 1; end > 0; end--) {
        int t = nums[0]; nums[0] = nums[end]; nums[end] = t;
        siftDownMax(nums, 0, end);
    }
}
```

**Python**
```python
def heap_sort(nums):
    def sift(i, n):
        while True:
            b, l, r = i, 2 * i + 1, 2 * i + 2
            if l < n and nums[l] > nums[b]: b = l
            if r < n and nums[r] > nums[b]: b = r
            if b == i:
                return
            nums[i], nums[b] = nums[b], nums[i]
            i = b
    n = len(nums)
    for i in range(n // 2 - 1, -1, -1):
        sift(i, n)
    for end in range(n - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        sift(0, end)
```

**Complexity:** time **O(n log n)**, space **O(1)** — O(n) build + (n − 1) sifts of O(log n).

---

## Edge cases

- Empty / single element.
- Duplicates (the order of equal keys may change: unstable).
- Already sorted input: still Θ(n log n).

---

## Common mistakes

1. Using a **min**-heap for ascending in-place sort (the min lands at the end).
2. Sifting within size `n` instead of the shrinking `end`, which pulls sorted elements back in.
3. Calling it stable.

---

## Follow-ups

1. Descending order?
2. Only the k smallest, sorted?

<details><summary>Answer sketches</summary>

**#1:** Use a min-heap, or reverse after.

**#2:** Partial heap sort: build a heap and pop k times, O(n + k log n).
</details>

---

## Flashcards

**Heap sort: which heap for ascending order?** #flashcard
Max-heap: the max is swapped to the end each round.

**Heap sort stability / space / worst case?** #flashcard
Unstable, O(1), O(n log n).

**Heap sort is an optimised version of which simple sort?** #flashcard
Selection sort.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
