# Heap / Priority Queue — SDE-2+ Level

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

More SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/arrays.py`, `../../google-sde2/snippets/python/two_pointers_window.py`, `../../google-sde2/snippets/python/stack_queue.py`.

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

## 7. Trade-offs & Scaling (optional)

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

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#merge-k-sorted-lists)** | Min-heap stores `(value, list_id, node)`; repeatedly pop min, append to result, push `node.next` if any. Alternative: **divide & conquer** pairwise merge. | **Empty** input lists; **Python heap** tie-break needs tuple with unique `list_id`. **Complexity:** O(N log k) vs O(N log N) sort-all. |
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#kth-largest-element)** | **Quickselect** average O(n); or **min-heap of size k** streaming largest. Max-heap of n−k+1 for “kth largest” less common. | **Duplicates:** partition on `<=` vs `<` matters. **Worst-case** quickselect O(n²) unless randomized/median-of-medians. |
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#top-k-frequent-elements)** | Count with map; **min-heap** of size k on `(freq, key)` **or** bucket sort by frequency O(n). | Bucket: freq 1..n buckets of lists; scan from high freq. **Tie** on frequency. |
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#find-median-from-data-stream)** | **Two heaps:** `small` max-heap (lower half), `large` min-heap (upper half); invariant `len(small) == len(large)` or +1. Rebalance after insert. | **Even** count: median average of both tops. **Duplicate** values fine. **Follow-up:** sliding window median (harder). |
| **K Closest Points to Origin** | **Max-heap** of size k on squared distance (avoid sqrt); or **quickselect** on distances. | **Squared distance** avoids float; **overflow** on `x*x+y*y`. **All same distance**—any k. |
| **IPO / Max Capital** | Sort projects by capital; min-heap of profits for affordable set; pick max profit, add capital, repeat k times. | **Greedy + heap**; projects become affordable as capital grows. |
| **Reorganize String** | Count chars; max-heap by freq; repeatedly place most frequent not equal to last placed. | **Impossible** if `max_freq > (n+1)/2`. **Tie** handling when popping. |
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#task-scheduler)** | **Math:** `(max_count-1)*(n+1) + num_with_max_freq`, capped at `tasks.length`. **Sim:** heap of task counts + idle slots. | **Cap** explains “cooling fits inside task count”. **Multiple** max frequencies add slots. |
| **Smallest Range Covering Elements from K Lists** | Min-heap over current head of each list; track global min/max; advance list that had min. | Like **merge k sorted** tracking range; **O(N log k)**. |
| **Furthest Building** (bricks/ladders) | Greedy: use **min-heap** of climbs for largest jumps to cover with ladders; rest bricks. | Clarify **ladders** replace one climb entirely. |

---

## See also

- [Sorting](../algorithms/sorting.md) — QuickSelect vs heap for top-K  
- [Queue](queue.md) — priority queue vs FIFO  
- [Graph](../algorithms/graph.md) — Dijkstra uses min-heap
