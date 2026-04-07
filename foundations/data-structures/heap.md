# Heap / Priority Queue — SDE-3 Level

Complete binary tree with heap property: parent ≥ children (max-heap) or parent ≤ children (min-heap). Used for priority queue, top-K, K-way merge, median maintenance.

---

## 1. Concept Overview

**Problem space**: Top K elements (min-heap of size K for largest; max-heap for smallest), K-way merge (min-heap of heads), median from stream (max-heap left half, min-heap right half), scheduling (earliest deadline / highest priority).

**When to use**: Need repeated "extract min/max" or "maintain K best"; merge K sorted; dynamic median; Dijkstra.

---

## 2. Core Algorithms

### Array Representation (0-indexed)
- Parent: `(i-1)//2`; Left: `2*i+1`; Right: `2*i+2`.
- **Insert**: Append, then bubble up (compare with parent, swap if violates).
- **Extract**: Swap root with last, pop last, bubble down (swap with smaller/larger child until heap property holds).
- **Heapify**: From last non-leaf down to 0, bubble down. O(N) total.

### Top K Largest
- Min-heap of size K. For each x: if len(heap)<K, push x; else if x > heap[0], pop then push x. Result = heap (or pop all). O(N log K).

### K-Way Merge
- Min-heap stores (value, list_id, index). Push first element of each list. Pop min, push next from same list. O(N log K).

### Two Heaps (Median)
- Max-heap (left) holds lower half; min-heap (right) upper half. Keep balance (|left| - |right| ≤ 1). Median = top of larger or average of tops.

---

## 3. Advanced Variations

- **Lazy deletion**: For "remove element" in heap (e.g., sliding window median), mark deleted and ignore when it surfaces at top. Count valid vs invalid at top.
- **Custom comparator**: Objects by key; (priority, timestamp) for stable ordering.
- **Kth largest in stream**: Same as top-K with min-heap of size K.

### Edge Cases
- Empty input; K=0 or K > n; duplicates; negative numbers; median with even count (average of two mids).

---

## 4. Common Interview Problems

**Easy**: Kth Largest in Stream.  
**Medium**: K Closest Points, Top K Frequent Elements, Reorganize String, Task Scheduler.  
**Hard**: Find Median from Data Stream, Merge K Sorted Lists, Sliding Window Median, IPO.

---

## 5. Pattern Recognition

- **Top K**: Min-heap size K (for largest) or max-heap (for smallest); if stream, maintain size K.
- **K-way merge**: Heap of heads; pop min, push next from same source.
- **Median / percentiles**: Two heaps (max for lower, min for upper); rebalance on insert.
- **Scheduling**: Priority by deadline or profit; heap for "next available" or "highest profit".

---

## 6. Code Implementations

```python
import heapq

def top_k_largest(nums, k):
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap

class MedianFinder:
    def __init__(self):
        self.lo = []   # max-heap: negate for min-heap behavior
        self.hi = []   # min-heap

    def addNum(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
```

---

## 7. SDE-3 Level Thinking

- **Trade-offs**: Heap vs sort — heap O(N log K) for top-K without fully sorting. Two heaps for median: O(log N) add, O(1) median; alternative is sorted structure (e.g., balanced BST).
- **Memory**: Top-K heap uses O(K). Median two heaps O(N). For distributed top-K, merge local top-K from each shard.
- **Concurrency**: Thread-safe priority queue (locking or lock-free); multiple consumers with priority.

---

## 8. Interview Strategy

- **Identify**: "K largest/smallest" → heap of size K. "Merge K sorted" → K-way merge. "Median" → two heaps.
- **Common mistakes**: Wrong heap type (max vs min for "K largest"); forgetting to rebalance in two heaps; off-by-one in median (even vs odd).

---

## 9. Quick Revision

- **Formulas**: Parent `(i-1)//2`, children `2*i+1`, `2*i+2`. Heapify O(N); insert/extract O(log N).
- **Tricks**: K largest → min-heap K; K smallest → max-heap K (negate in Python). Median → lo (max) + hi (min), keep lo size ≥ hi.
- **Edge cases**: K=0, K>n; empty stream; duplicate values.
- **Pattern tip**: "K" + "largest/smallest" or "merge K" → heap.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness |
|----------|------------|------------|
| **Merge K Sorted Lists** | Min-heap of `(val, list_id, node)` | Empty lists; same value tie-break |
| **Top K Frequent** | Count → min-heap of size K **or** bucket by freq | Bucket O(n) vs heap O(n log k) |
| **Find Median Data Stream** | Max-heap lower half + min-heap upper; rebalance | Even length: average two tops; after each insert rebalance |
| **K Closest to Origin** | Max-heap size K of distance (or squared) | Avoid sqrt until compare; integer overflow |
| **Task Scheduler** | Idle slot formula or greedy with heap | `(max-1)*(n+1)+num_max` capped at `len` |

---

## See also

- [Sorting](../algorithms/sorting.md) — QuickSelect vs heap for top-K  
- [Queue](queue.md) — priority queue vs FIFO  
- [Graph](../algorithms/graph.md) — Dijkstra uses min-heap
