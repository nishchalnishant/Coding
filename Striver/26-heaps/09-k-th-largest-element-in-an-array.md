---
module: striver/26-heaps
lesson: 9
topic: K-th Largest element in an array
difficulty: Medium
source: https://takeuforward.org/learning/dsa/k-th-largest-element-in-an-array?category=theory-and-implementation&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, quickselect, top-k]
---
# 9. K-th Largest element in an array

← [Heap Sort](08-heap-sort.md) · [Part 26 index](README.md) · Next → [Kth largest element in a stream of running integers](10-kth-largest-in-a-stream.md)

> [!abstract] Problem at a glance
> **Task:** Return the k-th largest element (by sorted position, duplicates counted) of an unsorted array.
> **Key insight:** Keep a **min-heap of size k**: it holds the k largest seen so far, and its root is the k-th largest. O(n log k). Quickselect partitions like quicksort but recurses into one side only: expected O(n).
> **Difficulty:** Medium · **Pattern:** Top-k with a bounded heap / quickselect · **Also on:** [LC 215](https://leetcode.com/problems/kth-largest-element-in-an-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/k-th-largest-element-in-an-array?category=theory-and-implementation&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort](#3-sort) · [4. Min-heap of size k](#4-min-heap-of-size-k) · [5. Quickselect (3-way partition)](#5-quickselect-3-way-partition) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums` and `k`, return the k-th largest element in sorted order (not the k-th distinct). Try to beat O(n log n).

| Input | Output | Why |
|---|---|---|
| `nums = [3,2,1,5,6,4], k = 2` | `5` |  |
| `nums = [3,2,3,1,2,4,5,5,6], k = 4` | `4` | 6,5,5,4 |

**Constraints:** `1 ≤ k ≤ n ≤ 10⁵`, `−10⁴ ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort | sort, return nums[n−k] | O(n log n) | O(1)–O(n) |
| Min-heap of size k | push; pop when size > k; answer = root | O(n log k) | O(k) |
| Quickselect (3-way partition) | partition around pivot; recurse into the side holding index n−k | O(n) expected | O(1) |

> [!tip] Interview angle
> Give all three and their trade-offs: sort O(n log n); heap O(n log k), streaming-friendly, deterministic; quickselect O(n) expected and O(n²) worst case (random pivot, 3-way partition for duplicates). The bounded heap is the one that generalises to streams.

---

## 3. Sort

**Intuition.** Sort ascending; the k-th largest sits at index `n − k`.

```python
def kth_sort(nums, k):
    return sorted(nums)[len(nums) - k]
```

**Complexity:** time **O(n log n)**, space **O(1)–O(n)**.

---

## 4. Min-heap of size k

**Intuition.** Invariant: the heap holds the k largest elements seen so far. A new element bigger than the root evicts the root (the smallest of the top k).

```python
import heapq
def kth_heap(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]
```

**Complexity:** time **O(n log k)**, space **O(k)**.

---

## 5. Quickselect (3-way partition)

**Intuition.** Target index `t = n − k` in ascending order. Partition `[lo, hi]` around a pivot into `< p`, `= p`, `> p` (Dutch flag). If `t` falls in the `=` band, the answer is the pivot; otherwise continue on one side. Expected sizes shrink geometrically, giving n + n/2 + … = O(n). The 3-way split keeps all-duplicate inputs linear.

**Algorithm**

1. `t = n − k`, `lo = 0`, `hi = n − 1`.
2. Pick pivot `p` (middle or random).
3. Dutch-flag partition `[lo, hi]` into `[lo, lt)` < p, `[lt, gt]` = p, `(gt, hi]` > p.
4. If `t < lt` → `hi = lt − 1`; if `t > gt` → `lo = gt + 1`; else return `p`.

**Dry run** — [3,2,1,5,6,4], k=2 → t=4. Pivot nums[2]=1 → [1 | 2,3,5,6,4]… band [0,0]; t > 0 → lo=1. Pivot nums[3]=5 → < : 2,3,4; = : 5; > : 6 → band at index 4 = t → 5.

**C++**
```cpp
int findKthLargest(vector<int>& nums, int k) {
    int t = nums.size() - k, lo = 0, hi = nums.size() - 1;
    while (true) {
        int p = nums[lo + (hi - lo) / 2];
        int lt = lo, i = lo, gt = hi;
        while (i <= gt) {
            if (nums[i] < p) swap(nums[lt++], nums[i++]);
            else if (nums[i] > p) swap(nums[i], nums[gt--]);
            else i++;
        }
        if (t < lt) hi = lt - 1;
        else if (t > gt) lo = gt + 1;
        else return p;
    }
}
```

**Java**
```java
static int findKthLargest(int[] nums, int k) {
    int t = nums.length - k, lo = 0, hi = nums.length - 1;
    while (true) {
        int p = nums[lo + (hi - lo) / 2];
        int lt = lo, i = lo, gt = hi;
        while (i <= gt) {
            if (nums[i] < p) { int x = nums[lt]; nums[lt++] = nums[i]; nums[i++] = x; }
            else if (nums[i] > p) { int x = nums[i]; nums[i] = nums[gt]; nums[gt--] = x; }
            else i++;
        }
        if (t < lt) hi = lt - 1;
        else if (t > gt) lo = gt + 1;
        else return p;
    }
}
```

**Python**
```python
def find_kth_largest(nums, k):
    t, lo, hi = len(nums) - k, 0, len(nums) - 1
    while True:
        p = nums[lo + (hi - lo) // 2]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if nums[i] < p:
                nums[lt], nums[i] = nums[i], nums[lt]; lt += 1; i += 1
            elif nums[i] > p:
                nums[i], nums[gt] = nums[gt], nums[i]; gt -= 1
            else:
                i += 1
        if t < lt:
            hi = lt - 1
        elif t > gt:
            lo = gt + 1
        else:
            return p
```

**Complexity:** time **O(n) expected**, space **O(1)** — each round discards one side; with a good pivot the work is n + n/2 + n/4 + … ≤ 2n. A random pivot makes O(n²) vanishingly unlikely.

---

## Edge cases

- k = 1 → max; k = n → min.
- All duplicates: the 3-way partition finishes in one round.
- Negative values.

---

## Common mistakes

1. Using a **max**-heap of all n and popping k times: O(n + k log n), fine, but not the bounded-memory answer they want.
2. Off-by-one: the k-th largest is at ascending index `n − k`, not `k`.
3. 2-way Lomuto partition on many duplicates degrades to O(n²).

---

## Follow-ups

1. Stream of numbers, query k-th largest any time.
2. Guaranteed O(n) worst case?

<details><summary>Answer sketches</summary>

**#1:** Keep the size-k min-heap persistent: see Kth largest in a stream.

**#2:** Median-of-medians pivot selection, rarely coded in interviews but worth naming.
</details>

---

## Flashcards

**k-th largest with a heap: which heap, what size?** #flashcard
Min-heap of size k; the root is the answer.

**Quickselect complexity?** #flashcard
O(n) expected, O(n²) worst; median of medians gives O(n) worst.

**k-th largest = which ascending index?** #flashcard
`n − k`.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
