---
module: striver-a2z/26-heaps
lesson: 3
topic: Build heap from a given Array
difficulty: Medium
source: https://takeuforward.org/learning/dsa/build-heap-from-a-given-array?category=theory-and-implementation&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, array]
---
# 3. Build heap from a given Array

← [Heapify Algorithm](02-heapify-algorithm.md) · [Part 26 index](README.md) · Next → [Implement Min Heap](04-implement-min-heap.md)

> [!abstract] Problem at a glance
> **Task:** Rearrange an arbitrary array in place into a min-heap in **O(n)**.
> **Key insight:** Leaves (the last ⌈n/2⌉ indices) are already one-node heaps. Sift down every internal node from `n/2 − 1` down to `0`. When a node is processed both its subtrees are heaps, so one sift-down fixes it. Most nodes are near the bottom where sifts are short: Σ (nodes at height h)·h = O(n).
> **Difficulty:** Medium · **Pattern:** Bottom-up heapify (Floyd)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/build-heap-from-a-given-array?category=theory-and-implementation&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. n pushes (top-down)](#3-n-pushes-top-down) · [4. Bottom-up sift-down](#4-bottom-up-sift-down) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, convert it in place into a min-heap (for every `i`, `nums[i] ≤` both children) using the bottom-up build.

| Input | Output | Why |
|---|---|---|
| `nums = [4,10,3,5,1]` | `[1,4,3,5,10]` |  |
| `nums = [3,2,1]` | `[1,2,3]` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| n pushes (top-down) | sift each element up into a growing heap | O(n log n) | O(1) |
| Bottom-up sift-down | for i = n/2−1 … 0: siftDown(i) | O(n) | O(1) |

> [!tip] Interview angle
> The follow-up is always 'why is it O(n) and not O(n log n)?'. Answer with the height sum: n/4 nodes sift ≤ 1 level, n/8 sift ≤ 2, …; Σ h/2^(h+1) converges to 1, so the total is ≤ n swaps.

---

## 3. n pushes (top-down)

**Intuition.** Treat the prefix `nums[0..i-1]` as a heap and sift `nums[i]` up into it. Each insertion can climb the full height, and half the nodes sit at the bottom, so the worst case is Θ(n log n). The final layout differs from Floyd's, but it's still a valid heap.

```python
def build_by_push(nums):
    for i in range(1, len(nums)):
        j = i
        while j > 0 and nums[(j - 1) // 2] > nums[j]:
            p = (j - 1) // 2
            nums[j], nums[p] = nums[p], nums[j]
            j = p
```

**Complexity:** time **O(n log n)**, space **O(1)**.

---

## 4. Bottom-up sift-down

**Intuition.** Process internal nodes right-to-left, bottom-up. The invariant: when node `i` is processed, both its children are roots of valid heaps, which is exactly the precondition of sift down.

**Algorithm**

1. For `i` from `n/2 − 1` down to 0:
2.   sift down `i`: swap with the smaller child while that child is smaller.

**Dry run** — [4,10,3,5,1]: i=1 (10): children 5,1 → swap with 1 → [4,1,3,5,10]. i=0 (4): children 1,3 → swap with 1 → [1,4,3,5,10]; index 1 children 5,10 ≥ 4 → stop.

**C++**
```cpp
void siftDown(vector<int>& a, int i, int n) {
    while (true) {
        int s = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && a[l] < a[s]) s = l;
        if (r < n && a[r] < a[s]) s = r;
        if (s == i) return;
        swap(a[i], a[s]);
        i = s;
    }
}
void buildMinHeap(vector<int>& nums) {
    int n = nums.size();
    for (int i = n / 2 - 1; i >= 0; i--) siftDown(nums, i, n);
}
```

**Java**
```java
static void siftDown(int[] a, int i, int n) {
    while (true) {
        int s = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && a[l] < a[s]) s = l;
        if (r < n && a[r] < a[s]) s = r;
        if (s == i) return;
        int t = a[i]; a[i] = a[s]; a[s] = t;
        i = s;
    }
}
static void buildMinHeap(int[] nums) {
    for (int i = nums.length / 2 - 1; i >= 0; i--) siftDown(nums, i, nums.length);
}
```

**Python**
```python
def build_min_heap(nums):
    n = len(nums)
    def sift_down(i):
        while True:
            s, l, r = i, 2 * i + 1, 2 * i + 2
            if l < n and nums[l] < nums[s]: s = l
            if r < n and nums[r] < nums[s]: s = r
            if s == i:
                return
            nums[i], nums[s] = nums[s], nums[i]
            i = s
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i)
```

**Complexity:** time **O(n)**, space **O(1)** — a node at height h costs O(h); there are ≤ ⌈n/2^(h+1)⌉ such nodes; Σ h·n/2^(h+1) = O(n).

---

## Edge cases

- Empty or single element: the loop doesn't run.
- Already a heap: no swaps.
- Reverse-sorted input: the most swaps, still O(n).

---

## Common mistakes

1. Looping `i` upward from 0: children aren't heaps yet, so the result is wrong.
2. Starting at `n − 1`: harmless but wastes work on leaves; the last internal node is `n/2 − 1`.
3. Claiming O(n log n) for Floyd's build.

---

## Follow-ups

1. Python's `heapq.heapify`?
2. Why not build a sorted array instead (also a valid heap)?

<details><summary>Answer sketches</summary>

**#1:** Same bottom-up algorithm, O(n), in place.

**#2:** Sorting is Ω(n log n); a heap only needs the partial order.
</details>

---

## Flashcards

**Build-heap cost?** #flashcard
O(n) bottom-up; O(n log n) by n pushes.

**First index processed by bottom-up build?** #flashcard
`n/2 − 1`, the last internal node.

**Why bottom-up order?** #flashcard
Sift down requires both subtrees to already be heaps.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
