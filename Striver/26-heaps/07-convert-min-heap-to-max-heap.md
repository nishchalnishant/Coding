---
module: striver/26-heaps
lesson: 7
topic: Convert Min Heap to Max Heap
difficulty: Medium
source: https://takeuforward.org/learning/dsa/convert-min-heap-to-max-heap?category=theory-and-implementation&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, array]
---
# 7. Convert Min Heap to Max Heap

← [Check if an array represents a min heap](06-check-if-an-array-represents-a-min-heap.md) · [Part 26 index](README.md) · Next → [Heap Sort](08-heap-sort.md)

> [!abstract] Problem at a glance
> **Task:** Rearrange a min-heap array in place into a max-heap.
> **Key insight:** The min-heap ordering is no help: a max-heap needs the opposite partial order. Treat the input as an arbitrary array and run the O(n) bottom-up build with max comparisons.
> **Difficulty:** Medium · **Pattern:** Bottom-up heapify (max)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/convert-min-heap-to-max-heap?category=theory-and-implementation&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort descending](#3-sort-descending) · [4. Bottom-up max-heapify](#4-bottom-up-max-heapify) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums`, a min-heap in array form, convert it in place into a max-heap (every node ≥ its children) using the bottom-up build.

| Input | Output | Why |
|---|---|---|
| `nums = [3,5,9,6,8,20,10,12,18,9]` | `[20,18,10,12,9,9,3,5,6,8]` |  |
| `nums = [1,2,3,4,5]` | `[5,4,3,1,2]` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort descending | a descending array is a max-heap | O(n log n) | O(1) |
| Bottom-up max-heapify | for i = n/2−1 … 0: siftDown toward the larger child | O(n) | O(1) |

> [!tip] Interview angle
> The trap is trying to 'reverse' the heap or swap levels. A reversed min-heap isn't a max-heap in general. State the O(n) build, and point out that the min-heap input helps nothing (and costs nothing).

---

## 3. Sort descending

**Intuition.** A non-increasing array satisfies parent ≥ child everywhere because the parent index is smaller. Correct, but it does more work than needed and gives a different layout than the bottom-up build.

```python
def to_max_by_sort(nums):
    nums.sort(reverse=True)
```

**Complexity:** time **O(n log n)**, space **O(1)**.

---

## 4. Bottom-up max-heapify

**Intuition.** Same as building a min-heap, with 'larger child' and 'child > node' comparisons.

**Algorithm**

1. For `i` from `n/2 − 1` down to 0: sift down `i` toward the larger child while that child is bigger.

**Dry run** — [1,2,3,4,5]: i=1 (2): children 4,5 → swap 5 → [1,5,3,4,2]. i=0 (1): children 5,3 → swap 5 → [5,1,3,4,2]; index 1 children 4,2 → swap 4 → [5,4,3,1,2].

**C++**
```cpp
void convertMinToMaxHeap(vector<int>& nums) {
    int n = nums.size();
    for (int s = n / 2 - 1; s >= 0; s--) {
        int i = s;
        while (true) {
            int b = i, l = 2 * i + 1, r = 2 * i + 2;
            if (l < n && nums[l] > nums[b]) b = l;
            if (r < n && nums[r] > nums[b]) b = r;
            if (b == i) break;
            swap(nums[i], nums[b]); i = b;
        }
    }
}
```

**Java**
```java
static void convertMinToMaxHeap(int[] nums) {
    int n = nums.length;
    for (int s = n / 2 - 1; s >= 0; s--) {
        int i = s;
        while (true) {
            int b = i, l = 2 * i + 1, r = 2 * i + 2;
            if (l < n && nums[l] > nums[b]) b = l;
            if (r < n && nums[r] > nums[b]) b = r;
            if (b == i) break;
            int t = nums[i]; nums[i] = nums[b]; nums[b] = t; i = b;
        }
    }
}
```

**Python**
```python
def convert_min_to_max_heap(nums):
    n = len(nums)
    for s in range(n // 2 - 1, -1, -1):
        i = s
        while True:
            b, l, r = i, 2 * i + 1, 2 * i + 2
            if l < n and nums[l] > nums[b]: b = l
            if r < n and nums[r] > nums[b]: b = r
            if b == i:
                break
            nums[i], nums[b] = nums[b], nums[i]
            i = b
```

**Complexity:** time **O(n)**, space **O(1)** — Floyd's build is O(n) regardless of the input's order.

---

## Edge cases

- Empty / single element.
- All equal: no swaps.
- Input is already also a max-heap (all equal).

---

## Common mistakes

1. Reversing the array: `[1,2,3,4,5]` reversed is `[5,4,3,2,1]` (OK by luck), but `[1,3,2]` reversed is `[2,3,1]`, which is not a max-heap.
2. Using the min-heap sift by copy-paste without flipping both comparisons.
3. Iterating from 0 upward.

---

## Follow-ups

1. Convert a max-heap to a min-heap.
2. Get the max of a min-heap without converting.

<details><summary>Answer sketches</summary>

**#1:** Same algorithm with min comparisons.

**#2:** It's among the leaves (`n/2 … n−1`): O(n) scan of the second half.
</details>

---

## Flashcards

**Min-heap → max-heap cost?** #flashcard
O(n): rebuild bottom-up with max comparisons.

**Where's the max in a min-heap?** #flashcard
In a leaf, among indices ≥ n/2.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
