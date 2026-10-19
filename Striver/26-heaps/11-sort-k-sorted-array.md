---
module: striver/26-heaps
lesson: 11
topic: Sort K sorted array
difficulty: Medium
source: https://takeuforward.org/learning/dsa/sort-k-sorted-array?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, sorting]
---
# 11. Sort K sorted array

← [Kth largest element in a stream of running integers](10-kth-largest-in-a-stream.md) · [Part 26 index](README.md) · Next → [Merge K sorted Lists](12-merge-k-sorted-lists.md)

> [!abstract] Problem at a glance
> **Task:** Sort an array where every element is at most `k` positions away from its sorted position.
> **Key insight:** The element that belongs at index `i` must be among `nums[i … i+k]`. So a **min-heap of size k+1** sliding over the array always contains the next output. That's O(n log k), better than O(n log n) when k ≪ n.
> **Difficulty:** Medium · **Pattern:** Sliding min-heap of size k+1
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sort-k-sorted-array?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 12 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Plain sort](#3-plain-sort) · [4. Insertion sort](#4-insertion-sort) · [5. Min-heap of size k+1](#5-min-heap-of-size-k1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums` where each element is at most `k` indices from where it would be in sorted order, return the sorted array.

| Input | Output | Why |
|---|---|---|
| `nums = [6,5,3,2,8,10,9], k = 3` | `[2,3,5,6,8,9,10]` |  |
| `nums = [10,9,8,7,4,70,60,50], k = 4` | `[4,7,8,9,10,50,60,70]` |  |

**Constraints:** `0 ≤ k < n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Plain sort | ignore k | O(n log n) | O(n) |
| Insertion sort | each element moves left ≤ k steps | O(nk) | O(1) |
| Min-heap of size k+1 | seed k+1; pop min to output, push next | O(n log k) | O(k) |

> [!tip] Interview angle
> Prove the window size: the smallest remaining element is at most k positions to the right of the next output slot, so k+1 candidates suffice. Note that insertion sort is also O(nk) on this input, which is fine for tiny k.

---

## 3. Plain sort

**Intuition.** Correct, but doesn't use the structure. (Timsort happens to be fast on nearly sorted input, but the guarantee is still O(n log n).)

```python
def sort_k_plain(nums, k):
    return sorted(nums)
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. Insertion sort

**Intuition.** Insertion sort's cost is the number of inversions; each element has at most k of them to its left.

```python
def sort_k_insertion(nums, k):
    a = list(nums)
    for i in range(1, len(a)):
        x, j = a[i], i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]; j -= 1
        a[j + 1] = x
    return a
```

**Complexity:** time **O(nk)**, space **O(1)**.

---

## 5. Min-heap of size k+1

**Intuition.** Seed the heap with the first k+1 elements. Repeatedly pop the min into the next output slot and push the next unread element. When input runs out, drain the heap.

**Algorithm**

1. Push `nums[0 … k]` into a min-heap.
2. For `i = k+1 … n−1`: output `pop()`, push `nums[i]`.
3. Drain the heap into the output.

**Dry run** — [6,5,3,2,8,10,9], k=3: heap {6,5,3,2} → out 2, push 8 → out 3, push 10 → out 5, push 9 → out 6 → drain 8, 9, 10.

**C++**
```cpp
vector<int> sortKSorted(vector<int> nums, int k) {
    priority_queue<int, vector<int>, greater<int>> pq;
    vector<int> out;
    for (int x : nums) {
        pq.push(x);
        if ((int)pq.size() > k) { out.push_back(pq.top()); pq.pop(); }
    }
    while (!pq.empty()) { out.push_back(pq.top()); pq.pop(); }
    return out;
}
```

**Java**
```java
static int[] sortKSorted(int[] nums, int k) {
    PriorityQueue<Integer> pq = new PriorityQueue<>();
    int[] out = new int[nums.length];
    int w = 0;
    for (int x : nums) {
        pq.offer(x);
        if (pq.size() > k) out[w++] = pq.poll();
    }
    while (!pq.isEmpty()) out[w++] = pq.poll();
    return out;
}
```

**Python**
```python
import heapq
def sort_k_sorted(nums, k):
    h, out = [], []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:                 # heap holds k+1 → its min is final
            out.append(heapq.heappop(h))
    while h:
        out.append(heapq.heappop(h))
    return out
```

**Complexity:** time **O(n log k)**, space **O(k)** — n pushes and n pops on a heap of size ≤ k+1.

---

## Edge cases

- k = 0: already sorted; the heap has size 1.
- k ≥ n − 1: degenerates to heap sort.
- Duplicates.

---

## Common mistakes

1. Heap of size k instead of k+1 (misses the element exactly k away).
2. Pushing everything first and then popping: correct but O(n log n) and O(n) memory.

---

## Follow-ups

1. Lower bound?
2. Stream with bounded lateness (event-time reordering)?

<details><summary>Answer sketches</summary>

**#1:** Ω(n log k) comparisons: you can encode n/k independent sorts of k elements.

**#2:** Same heap: emit the min once the heap exceeds k (a watermark).
</details>

---

## Flashcards

**k-sorted array: heap size?** #flashcard
k + 1.

**k-sorted sort complexity?** #flashcard
O(n log k) with a heap; O(nk) with insertion sort.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
