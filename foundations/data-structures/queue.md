# Queue — SDE-3 Level

FIFO (First In, First Out). SDE-3 focus: BFS, deque for sliding-window max (monotonic queue), circular buffer, and priority queue (heap) usage.

---

## 1. Concept Overview

**Problem space**: BFS (level-order, shortest path in unweighted graph), sliding window maximum, task scheduling, LRU (with DLL), design circular queue.

**When to use**: Level-by-level processing; "first come first served"; sliding window max (deque maintaining monotonic decreasing).

---

## 2. Core Algorithms

### BFS (Shortest Path in Unweighted Graph)
- Queue of (node, distance); enqueue neighbors with distance+1; first time reaching target = shortest. O(V+E).

### Monotonic Deque (Sliding Window Maximum)
- Deque stores indices in decreasing order of value. For window [i, i+k): front = max. When sliding: remove indices outside window from front; from back, pop while value at back < current; push current. Front is always max for current window.
- **Complexity**: O(N).

### Circular Queue
- `front`, `rear`, `capacity`; `(rear+1) % capacity == front` ⇒ full; `front == rear` ⇒ empty (with one slot wasted) or use size counter.

---

## 3. Advanced Variations

- **Priority Queue**: Extract min/max in O(log N); used for Dijkstra, merge K lists, top K. Not FIFO but priority-ordered.
- **Deque**: Double-ended; sliding window max uses deque; 0-1 BFS uses deque (0-weight front, 1-weight back).
- **LRU**: HashMap + doubly linked list; queue-like "recent at head, evict from tail".

### Edge Cases
- Empty queue; single element; k=1 or k=n in sliding window; circular queue full/empty distinction.

---

## 4. Common Interview Problems

**Easy**: Implement Queue using Stacks, Moving Average from Data Stream.  
**Medium**: Design Circular Queue, LRU Cache, Rotten Oranges (BFS).  
**Hard**: Sliding Window Maximum (monotonic deque), Maximum of Minimums of Every Window Size.

---

## 5. Pattern Recognition

- **BFS**: Shortest path (unweighted), level order, multi-source (e.g., rotten oranges — all rotten at time 0).
- **Monotonic deque**: Sliding window max/min — keep indices of "candidates" in order.
- **Two stacks as queue**: Push stack + pop stack; when pop stack empty, pour push into pop. Amortized O(1).

---

## 6. Code Implementations

```python
def sliding_window_maximum(nums, k):
    from collections import deque
    dq = deque()
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] < x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            while dq[0] <= i - k:
                dq.popleft()
            out.append(nums[dq[0]])
    return out
```

---

## 7. SDE-3 Level Thinking

- **Trade-offs**: Array queue wastes space (front moves); circular reuses. Deque for sliding window max avoids O(K) scan per window (O(N) total).
- **Concurrency**: Blocking queue for producer-consumer; lock-free queues in high-throughput systems.

---

## 8. Interview Strategy

- **Identify**: "Shortest path" unweighted → BFS. "Max in window" → monotonic deque. "Recent/evict" → LRU (DLL+HashMap).
- **Common mistakes**: Forgetting to remove expired indices from deque front; circular queue full/empty logic.

---

## 9. Quick Revision

- **Tricks**: Monotonic deque: store indices; remove from back if smaller than current; remove from front if out of window.
- **Edge cases**: k=0, k>n; empty graph; disconnected (BFS from each unvisited).
