---
module: striver-a2z/26-heaps
lesson: 10
topic: Kth largest element in a stream of running integers
difficulty: Easy
source: https://takeuforward.org/learning/dsa/kth-largest-element-in-a-stream-of-running-integers?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, design, top-k]
---
# 10. Kth largest element in a stream of running integers

← [K-th Largest element in an array](09-k-th-largest-element-in-an-array.md) · [Part 26 index](README.md) · Next → [Sort K sorted array](11-sort-k-sorted-array.md)

> [!abstract] Problem at a glance
> **Task:** Design `KthLargest(k, nums)` whose `add(val)` inserts `val` and returns the current k-th largest.
> **Key insight:** A **min-heap holding exactly the k largest** values so far. Its root is the k-th largest. A new value smaller than the root can never matter again, so it's dropped; otherwise it replaces the root. Each `add` is O(log k) and memory stays O(k) no matter how long the stream is.
> **Difficulty:** Easy · **Pattern:** Bounded min-heap (top-k) · **Also on:** [LC 703](https://leetcode.com/problems/kth-largest-element-in-a-stream/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/kth-largest-element-in-a-stream-of-running-integers?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 12 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Keep everything sorted](#3-keep-everything-sorted) · [4. Min-heap of size k](#4-min-heap-of-size-k) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement `KthLargest(int k, int[] nums)` and `int add(int val)`: append `val` to the stream and return the k-th largest element so far. When `add` is called, at least k elements exist.

| Input | Output | Why |
|---|---|---|
| `KthLargest(3, [4,5,8,2]); add 3, 5, 10, 9, 4` | `4, 5, 5, 8, 8` |  |

**Constraints:** `1 ≤ k ≤ 10⁴`, `0 ≤ nums.length ≤ 10⁴`, up to `10⁴` calls to `add`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Keep everything sorted | insort each value; answer = a[-k] | add O(n) | O(n) |
| Min-heap of size k | push; pop while size > k; return root | add O(log k) | O(k) |

> [!tip] Interview angle
> The interviewer is checking that you pick a **min**-heap (not max) and cap it at k. Say why: you need to evict the smallest of the top k, which is exactly the min-heap root. Mention that the constructor can heapify then pop down to k in O(n + (n−k) log n).

---

## 3. Keep everything sorted

**Intuition.** A sorted list answers in O(1) by index, but every insert shifts O(n) elements and memory grows with the stream.

```python
import bisect
class KthLargestSorted:
    def __init__(self, k, nums):
        self.k, self.a = k, sorted(nums)
    def add(self, val):
        bisect.insort(self.a, val)
        return self.a[-self.k]
```

**Complexity:** time **add O(n)**, space **O(n)**.

---

## 4. Min-heap of size k

**Intuition.** Invariant: the heap holds the k largest values seen. Push the new value; if the size exceeds k, pop the minimum. The root is the k-th largest.

**Algorithm**

1. Constructor: push every `nums[i]`, popping whenever size > k.
2. `add(val)`: push `val`; if size > k pop; return the root.

**Dry run** — k=3, [4,5,8,2] → heap {4,5,8}. add 3 → {3,4,5,8} → pop 3 → root 4. add 5 → {4,5,5,8} → pop 4 → 5. add 10 → pop 5 → {5,8,10} → 5. add 9 → pop 5 → {8,9,10} → 8.

**C++**
```cpp
class KthLargest {
    priority_queue<int, vector<int>, greater<int>> pq;
    int k;
public:
    KthLargest(int k, vector<int> nums) : k(k) {
        for (int x : nums) add(x);
    }
    int add(int val) {
        pq.push(val);
        if ((int)pq.size() > k) pq.pop();
        return pq.top();
    }
};
```

**Java**
```java
static class KthLargest {
    private final PriorityQueue<Integer> pq = new PriorityQueue<>();
    private final int k;
    KthLargest(int k, int[] nums) {
        this.k = k;
        for (int x : nums) add(x);
    }
    int add(int val) {
        pq.offer(val);
        if (pq.size() > k) pq.poll();
        return pq.peek();
    }
}
```

**Python**
```python
import heapq
class KthLargest:
    def __init__(self, k, nums):
        self.k, self.h = k, []
        for x in nums:
            self.add(x)
    def add(self, val):
        heapq.heappush(self.h, val)
        if len(self.h) > self.k:
            heapq.heappop(self.h)
        return self.h[0]
```

**Complexity:** time **add O(log k)**, space **O(k)** — the heap never holds more than k + 1 items.

---

## Edge cases

- `nums` shorter than k at construction: the root is invalid until k values exist (guaranteed by the problem).
- Duplicates count separately.
- Negative values.

---

## Common mistakes

1. Using a max-heap of everything and popping k times per query: O(k log n) per add.
2. Returning the root before trimming the heap to size k.
3. Forgetting that `add` in the constructor can return garbage while size < k (ignore the return value there).

---

## Follow-ups

1. Also support `remove(val)`?
2. k changes per query?

<details><summary>Answer sketches</summary>

**#1:** Use two balanced multisets (top-k and rest) or a heap with lazy deletion plus a counter.

**#2:** Order-statistic tree / Fenwick tree over compressed values: O(log n) k-th queries.
</details>

---

## Flashcards

**Kth largest of a stream: structure?** #flashcard
Min-heap capped at k; root = answer.

**Why min-heap for k largest?** #flashcard
You need to evict the smallest of the top k quickly.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
