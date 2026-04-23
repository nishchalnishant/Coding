# Queue — SDE-3 Gold Standard

FIFO ordered processing. SDE-3 focus: BFS shortest path, monotonic deque for sliding-window max, two-stack queue, circular ring buffer, and lock-free queue design for production systems.

---

## 1. Representation Choice

> [!IMPORTANT]
> **The Click Moment**: "**Level-by-level** processing" — OR — "**shortest path** in unweighted graph" — OR — "**sliding window max/min** in O(N)" — OR — "**multi-source spread**" (rotten oranges, walls and gates). A plain `deque` is for BFS; a monotonic deque is for sliding-window; `heapq` (priority queue) is for Dijkstra — these are different tools with different guarantees.

| Variant | Key Operation | Best For |
| :--- | :--- | :--- |
| `collections.deque` | O(1) append / popleft | BFS, sliding window max |
| `heapq` (min-heap) | O(log N) push / pop | Dijkstra, top-K, task scheduling |
| Circular array queue | O(1) enqueue / dequeue | Fixed-capacity ring buffer, design questions |
| Two-stack queue | Amortized O(1) | "Implement queue using stacks" |

```python
from collections import deque

def bfs_level_order(adj: dict, start: int) -> list[list[int]]:
    visited = {start}
    queue = deque([start])
    levels = []
    while queue:
        level_size = len(queue)  # snapshot current level width
        level = []
        for _ in range(level_size):
            u = queue.popleft()
            level.append(u)
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        levels.append(level)
    return levels
```

---

## 2. Core Patterns & Click Moments

### Monotonic Deque — Sliding Window Maximum

> [!IMPORTANT]
> **The Click Moment**: "Maximum (or minimum) in every window of size k" — OR — "**constraint on window**" where you need O(N) not O(NK). Deque stores **indices** in monotonically decreasing order of value. Front = index of max for current window. Each index enters and exits the deque at most once → O(N) total.

```python
def sliding_window_maximum(nums: list[int], k: int) -> list[int]:
    if not nums or k == 0:
        return []
    dq: deque = deque()  # stores indices; values are monotonically decreasing
    result = []
    for i, x in enumerate(nums):
        # Remove indices outside the current window from front
        while dq and dq[0] <= i - k:
            dq.popleft()
        # Remove indices with smaller values from back — they can never be future maxima
        while dq and nums[dq[-1]] < x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

> [!CAUTION]
> **Store indices, not values.** The deque holds indices so you can check window expiry (`dq[0] <= i - k`) without a separate pointer. A common bug is storing values and losing the ability to evict expired entries — this gives wrong answers silently on inputs like `[1, 3, -1, -3, 5, 3, 6, 7], k=3`.

> [!TIP]
> **Sliding window minimum**: flip the comparison — maintain an **increasing** deque: `while dq and nums[dq[-1]] > x: dq.pop()`. The front is always the minimum of the current window. Same O(N) complexity.

---

### BFS Multi-Source — Simultaneous Spread

> [!IMPORTANT]
> **The Click Moment**: "All X cells spread **simultaneously**" — OR — "distance to **nearest** Y" — OR — "minimum time for all cells to reach state Z". Add all sources to the queue at distance 0 before starting BFS. The queue naturally interleaves all fronts, so each cell is first reached via the shortest path from any source.

```python
def multi_source_bfs(grid: list[list[int]], sources: list[tuple[int, int]]) -> list[list[int]]:
    rows, cols = len(grid), len(grid[0])
    DIRS = [(1,0), (-1,0), (0,1), (0,-1)]
    dist = [[-1] * cols for _ in range(rows)]
    queue: deque = deque()
    for r, c in sources:
        dist[r][c] = 0
        queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist
```

---

### Two-Stack Queue — Amortized O(1)

> [!IMPORTANT]
> **The Click Moment**: "Implement **queue using two stacks**" (classic design question). Push-stack receives all enqueues. Pop-stack is filled lazily from push-stack when empty. Each element moves push → pop exactly once → amortized O(1) per dequeue.

```python
class MyQueue:
    def __init__(self) -> None:
        self._push: list = []
        self._pop: list = []

    def push(self, x: int) -> None:
        self._push.append(x)

    def pop(self) -> int:
        self._refill()
        return self._pop.pop()

    def peek(self) -> int:
        self._refill()
        return self._pop[-1]

    def empty(self) -> bool:
        return not self._push and not self._pop

    def _refill(self) -> None:
        if not self._pop:
            while self._push:
                self._pop.append(self._push.pop())
```

---

### Circular Queue — Fixed-Capacity Ring Buffer

> [!IMPORTANT]
> **The Click Moment**: "Design a **fixed-size** queue" — OR — "circular buffer for **streaming** data with bounded memory" — OR — "producer-consumer with bounded capacity". Track `front`, `size`, and `capacity`; compute `rear = (front + size) % capacity`. Using a `size` counter avoids the wasted-slot hack and the full/empty ambiguity.

```python
class CircularQueue:
    def __init__(self, k: int) -> None:
        self._data = [0] * k
        self._front = 0
        self._size = 0
        self._cap = k

    def enqueue(self, val: int) -> bool:
        if self._size == self._cap:
            return False
        rear = (self._front + self._size) % self._cap
        self._data[rear] = val
        self._size += 1
        return True

    def dequeue(self) -> bool:
        if self._size == 0:
            return False
        self._front = (self._front + 1) % self._cap
        self._size -= 1
        return True

    def front(self) -> int:
        return -1 if self._size == 0 else self._data[self._front]

    def rear(self) -> int:
        if self._size == 0:
            return -1
        return self._data[(self._front + self._size - 1) % self._cap]

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self._cap
```

> [!CAUTION]
> **Full vs empty ambiguity**: The classic "wasted slot" approach (`rear+1 == front` means full) works but wastes one slot and is error-prone. The `size` counter approach above is cleaner: full when `size == cap`, empty when `size == 0`. Always prefer the counter approach in interviews.

---

## 3. SDE-3 Deep Dives

### Scalability: LMAX Disruptor — Lock-Free Ring Buffer

> [!TIP]
> Java's **LMAX Disruptor** is a lock-free bounded circular queue used in high-frequency trading (millions of events/second). Key insight: a single 64-bit `AtomicLong` sequence counter replaces both head and tail. Producers claim a slot via CAS on the sequence; consumers read when the slot's sequence matches expectations. Cache-line padding (`@sun.misc.Contended`) prevents false sharing between producer and consumer counters. This is 10-100× faster than `ArrayBlockingQueue` under contention.

### Scalability: Persistent Queue

> [!TIP]
> A **persistent (immutable) functional queue** (Okasaki's real-time queue) supports O(1) amortized push/pop while preserving all historical versions. After each operation, both the old and new queue versions exist. Implemented with a lazy front list + a reversed rear list balanced via lazy evaluation. Used in functional languages (Haskell, Clojure) and undo-redo systems.

### Concurrency: Blocking Queue for Producer-Consumer

> [!TIP]
> Python's `queue.Queue` is thread-safe via an internal `threading.Condition`. `put()` blocks when full; `get()` blocks when empty. In Java, `LinkedBlockingQueue` uses two separate locks — a **head lock** for consumers and a **tail lock** for producers. This doubles throughput vs a single lock because producers and consumers don't contend when the queue is neither full nor empty. For Python, use `asyncio.Queue` in async contexts and `multiprocessing.Queue` for multiprocessing.

### Trade-offs: BFS Queue vs DFS Stack

| Property | BFS (Queue) | DFS (Stack) |
| :--- | :--- | :--- |
| Shortest path (unweighted) | **Yes** — first reach = shortest | No |
| Memory | O(max level width) | O(max depth) |
| Level order output | Natural | Requires post-processing |
| Grid problems | Better (steps = levels) | Works; Python recursion limit risk |
| Topological sort | Kahn's algorithm | DFS postorder |
| Multi-source spread | Natural (add all to queue at t=0) | Awkward |

---

## 4. Common Interview Problems

### Easy / Medium
- **Rotten Oranges** — Multi-source BFS from all rotten cells at t=0; count fresh oranges; return level count if fresh = 0, else -1.
- **[Word Ladder](../../google-sde2/PROBLEM_DETAILS.md#word-ladder)** — BFS; neighbors = one-letter edits in word set; remove visited words from set immediately.
- **[Sliding Window Maximum](../../google-sde2/PROBLEM_DETAILS.md#sliding-window-maximum)** — Monotonic deque of indices; decreasing values; front = max.
- **Design Circular Queue** — Fixed array + `front`/`size`/`cap`; mod arithmetic.
- **Moving Average from Data Stream** — Fixed-size deque + running sum; evict front when over capacity.
- **01 Matrix** — Multi-source BFS from all `0` cells; distances expand outward.

### Hard
- **Sliding Window Minimum** — Same deque pattern; maintain increasing order (flip comparison).
- **Maximum of Minimums of Every Window Size** — Monotonic stack for prev/next smaller element; fill answer array.
- **[Cheapest Flights Within K Stops](../../google-sde2/PROBLEM_DETAILS.md#cheapest-flights-within-k-stops)** — BFS with state `(node, stops_used)`; or Bellman-Ford with K+1 relaxations.
- **Shortest Path in Binary Matrix** — BFS on 8-neighbor open (0) cells; return step count.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **Rotten Oranges** | "Simultaneous spread; minimum time" | Multi-source BFS from all rotten cells at t=0; count fresh | If `fresh > 0` after BFS → return -1 (blocked fresh cells). All-rotten or no-fresh are instant-return edge cases. |
| **[Word Ladder](../../google-sde2/PROBLEM_DETAILS.md#word-ladder)** | "Minimum transformation steps" | BFS; each word's neighbors = one-letter edits in word set | Remove word from set when visited — prevents revisit and cycles. Bidirectional BFS halves explored nodes for follow-up. |
| **[Sliding Window Maximum](../../google-sde2/PROBLEM_DETAILS.md#sliding-window-maximum)** | "Max in every k-window in O(N)" | Deque of indices; pop back while `nums[back] < nums[i]`; pop front if expired | Each index enqueued/dequeued once → O(N). Store indices, not values, for window expiry check. |
| **Shortest Path in Binary Matrix** | "Min path in 0-grid, 8 directions" | BFS on open (0) cells; 8-directional neighbors; return steps | Return -1 if `grid[0][0]` or `grid[n-1][n-1]` is 1. Mark visited before enqueue (not after dequeue) to avoid TLE. |
| **01 Matrix** | "Distance to nearest 0 for every cell" | Multi-source BFS from all 0s; single pass O(RC) | BFS from targets (0s), not from each 1 individually — avoids O(R²C²). Initialize 1-cells to inf, 0-cells to 0. |
| **Design Circular Queue** | "Bounded FIFO with O(1) all ops" | Array + `front`/`size`/`cap`; `rear = (front+size)%cap` | Use `size` counter over wasted-slot trick — cleaner. Thread-safety follow-up: add a mutex around enqueue/dequeue. |
| **Moving Average from Data Stream** | "Average of last k values in O(1)" | Deque + running sum; evict front when `len > k` | Float division. Python `deque(maxlen=k)` auto-evicts but you still need the running sum — don't recompute. |
| **[Cheapest Flights K Stops](../../google-sde2/PROBLEM_DETAILS.md#cheapest-flights-within-k-stops)** | "Shortest path with at most K intermediate nodes" | BFS level = stops; or Bellman-Ford K+1 rounds | Standard Dijkstra doesn't bound stops. Need state `(cost, node, stops)` and prune when `stops > K`. |

---

## See also

- [Stack](stack.md) — stack vs queue; monotonic stack for next greater element
- [Graph Algorithms](../algorithms/graph.md) — BFS shortest path; Dijkstra with priority queue
- [Array](array.md) — sliding window (pointer-based); deque for window max variant
- [Patterns Master](../../../reference/patterns/patterns-master.md) — BFS and queue pattern recognition triggers
