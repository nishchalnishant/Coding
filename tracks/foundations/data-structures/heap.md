# Heap / Priority Queue — SDE-3 Gold Standard

Complete binary tree with the heap property: parent ≤ children (min-heap) or parent ≥ children (max-heap). The canonical data structure for "always extract the current best" in O(log N).

---

## 1. Concept Overview

### Array Representation (0-indexed)

| Relationship | Formula |
| :--- | :--- |
| Parent of i | `(i - 1) // 2` |
| Left child of i | `2 * i + 1` |
| Right child of i | `2 * i + 2` |

- **Insert**: Append, then bubble up — swap with parent while heap property violated. O(log N).
- **Extract-min/max**: Swap root with last element, pop last, bubble down — swap with the better child. O(log N).
- **Heapify (build from array)**: Start from last non-leaf, bubble each down. O(N) — not O(N log N).

> [!TIP]
> Python's `heapq` is a **min-heap only**. To simulate a max-heap, negate all values before pushing and negate again when popping. For objects, use `(-priority, item)` tuples so the tuple comparison sorts by priority first.

---

## 2. Core Algorithms & Click Moments

### Top-K Largest / Smallest

> [!IMPORTANT]
> **The Click Moment**: "Find the **K largest**" — OR — "find the **K most frequent**" — OR — "**K closest** points to origin" — OR — "**Kth** largest in a stream". If the constraint is K << N and you don't need a fully sorted result, a heap of size K beats full sort.

- **K largest** → **min-heap of size K**: maintain only the K largest seen so far. When the heap exceeds K, pop the current minimum (smallest of the K). O(N log K).
- **K smallest** → **max-heap of size K** (negate in Python): same logic inverted.

```python
import heapq

def top_k_largest(nums: list[int], k: int) -> list[int]:
    if k <= 0 or not nums:
        return []
    heap: list[int] = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)  # remove the smallest of the k+1
    return heap  # contains k largest, smallest is heap[0]

def kth_largest(nums: list[int], k: int) -> int:
    return heapq.nlargest(k, nums)[-1]  # O(N log k); or use above and return heap[0]
```

> [!CAUTION]
> **K > N edge case**: If `k > len(nums)`, return all elements sorted or raise an error — don't silently return fewer. Always validate `k` at the function boundary.

---

### K-Way Merge

> [!IMPORTANT]
> **The Click Moment**: "Merge **K sorted** lists/arrays into one sorted output" — OR — "sorted output from K sources". A min-heap of size K stores one element per source; each pop gives the globally smallest remaining element.

```python
from typing import Iterator

def k_way_merge(sorted_lists: list[list[int]]) -> list[int]:
    heap: list[tuple[int, int, int]] = []  # (value, list_idx, element_idx)
    for i, lst in enumerate(sorted_lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result = []
    while heap:
        val, i, j = heapq.heappop(heap)
        result.append(val)
        if j + 1 < len(sorted_lists[i]):
            heapq.heappush(heap, (sorted_lists[i][j + 1], i, j + 1))
    return result
```

> [!CAUTION]
> **Python heap tie-breaking**: If two tuples have equal first elements, Python compares the second. If `list_idx` values are ints, comparison is fine. But if the second element is a non-comparable type (e.g., a `ListNode` object), Python will raise `TypeError`. Always include a unique tie-breaker (like a counter) as the second element.

---

### Two Heaps — Dynamic Median

> [!IMPORTANT]
> **The Click Moment**: "Median of a **data stream**" — OR — "maintain the **median** as elements arrive" — OR — "find the **median** of a sliding window". Two heaps partition the data at the median: max-heap for the lower half, min-heap for the upper half.

- **Invariant**: `|len(lo) - len(hi)| <= 1` and `max(lo) <= min(hi)`.
- **Add**: Push to `lo` (max-heap), then rebalance by moving `lo`'s max to `hi` if it's larger. Rebalance sizes.
- **Median**: If sizes equal → average of tops; else → top of the larger heap.

```python
class MedianFinder:
    def __init__(self):
        self._lo: list[int] = []  # max-heap (negated)
        self._hi: list[int] = []  # min-heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self._lo, -num)
        # Ensure every element in lo <= every element in hi
        heapq.heappush(self._hi, -heapq.heappop(self._lo))
        # Rebalance so lo has >= elements as hi
        if len(self._lo) < len(self._hi):
            heapq.heappush(self._lo, -heapq.heappop(self._hi))

    def find_median(self) -> float:
        if len(self._lo) > len(self._hi):
            return float(-self._lo[0])
        return (-self._lo[0] + self._hi[0]) / 2.0
```

> [!TIP]
> **Sliding Window Median (hard follow-up)**: Use two heaps + **lazy deletion**. Track invalid elements (those that have slid out of the window) in a counter. When they surface at the top of a heap during a pop, discard them instead. This avoids O(N) re-heapification per step.

---

### Scheduling — Priority by Custom Key

> [!IMPORTANT]
> **The Click Moment**: "Tasks with **deadlines**" — OR — "assign work based on **priority**" — OR — "**Task Scheduler** with cooldown". Sort by deadline/profit, then use a heap to dynamically pick the best available option.

```python
def ipo_maximize_capital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
    # IPO: pick up to k projects to maximize capital; can only start if current capital >= required
    projects = sorted(zip(capital, profits))  # sort by required capital
    available: list[int] = []  # max-heap of profits (negated)
    i = 0
    for _ in range(k):
        # Unlock all projects we can now afford
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(available, -projects[i][1])
            i += 1
        if not available:
            break
        w += -heapq.heappop(available)  # take most profitable available project
    return w
```

---

## 3. SDE-3 Deep Dives

### Scalability: Distributed Top-K

> [!TIP]
> **Top-K at scale** (e.g., top 10 trending videos across 1000 shards):
> 1. Each shard independently maintains a local top-K min-heap.
> 2. The coordinator collects K results from each of N shards (total K×N elements).
> 3. Run K-way merge on the K×N elements with a heap of size N.
> 4. Total: O(K×N log N) at coordinator — independent of total dataset size.
>
> This is the architecture behind Google Trends, Twitter trending, and leaderboards.

### Scalability: Streaming Percentiles

For P99 latency from a live request stream:
- **Exact**: Two-heap median approach gives P50. For arbitrary percentile, maintain heap sizes at `p : (1-p)` ratio.
- **Approximate**: Use a **t-digest** or **DDSketch** — merge-friendly probabilistic structures that approximate any percentile with bounded error and O(1) per insert. Used in Prometheus, Datadog.

### Concurrency: Thread-Safe Priority Queues

> [!TIP]
> **Java**: `PriorityBlockingQueue` provides a thread-safe min-heap with blocking `take()` (blocks until an element is available). Used for producer-consumer systems where producers add tasks and multiple consumers extract the highest-priority one.
>
> **Lock-free**: CAS-based skip lists (e.g., Java's `ConcurrentSkipListMap`) provide O(log N) lock-free priority queue operations — lower contention under high concurrency than mutex-based heaps.
>
> **Python**: `heapq` is not thread-safe. Use `queue.PriorityQueue` (internally uses `heapq` with a `threading.Lock`) for multi-threaded use.

> [!CAUTION]
> **Heap instability**: Python's `heapq` is not stable — equal-priority elements don't preserve insertion order. For stable priority queues, use `(priority, counter, item)` tuples where `counter` is a monotonically increasing sequence number.

### Trade-offs

| Use Case | Best Structure | Why |
| :--- | :--- | :--- |
| Top-K from static array | QuickSelect | O(N) avg; no extra space |
| Top-K from stream | Min-heap of size K | O(N log K); handles infinite stream |
| All elements sorted | Full sort | O(N log N); simpler than heap |
| Dynamic median | Two heaps | O(log N) insert, O(1) median |
| Sliding window median | Two heaps + lazy delete | Amortized O(log N); avoids re-heapification |
| Priority scheduling | Min-heap | O(log N) insert/extract |
| Merge K sorted streams | K-way merge heap | O(N log K); never materializes full data |

---

## 4. Common Interview Problems

### Easy
- **Kth Largest in Stream** — Min-heap of size K; push and pop if overflows.
- **Last Stone Weight** — Max-heap; pop two, push difference if non-zero.

### Medium
- **K Closest Points to Origin** — Max-heap of size K on squared distance (avoid sqrt).
- **Top K Frequent Elements** — Count with map; min-heap on `(freq, key)` of size K, or bucket sort.
- **Reorganize String** — Max-heap by frequency; place most frequent not equal to previous.
- **Task Scheduler** — Math: `(max_freq - 1) * (n + 1) + count_of_max_freq`, capped at `len(tasks)`.
- **Find Median from Data Stream** — Two heaps with rebalancing.

### Hard
- **Merge K Sorted Lists** — K-way merge; handle empty lists; tie-break with list index.
- **Sliding Window Median** — Two heaps + lazy deletion counter.
- **IPO (Maximize Capital)** — Sort by capital; max-heap of unlocked profits.
- **Smallest Range Covering K Lists** — K-way merge tracking `[min, max]` of current window.
- **Furthest Building** — Greedy: min-heap of climbs assigned ladders; fall back to bricks.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Merge K Sorted Lists](../../google-sde2/PROBLEM_DETAILS.md#merge-k-sorted-lists)** | "Smallest among K heads" | Min-heap `(val, list_id, node)` | Tie-break: include `list_id` as second element to avoid comparing nodes. |
| **[Kth Largest Element](../../google-sde2/PROBLEM_DETAILS.md#kth-largest-element)** | "Rank without full sort" | QuickSelect O(N) avg or min-heap-K | QuickSelect mutates array; heap is cleaner for streams. Confirm if K can equal N. |
| **[Top K Frequent](../../google-sde2/PROBLEM_DETAILS.md#top-k-frequent-elements)** | "K by frequency" | Count + min-heap-K, or bucket sort | Bucket sort is O(N) — prefer when K not given or K = N. |
| **[Find Median from Stream](../../google-sde2/PROBLEM_DETAILS.md#find-median-from-data-stream)** | "Median as data arrives" | Two heaps: max-lo + min-hi | Even count → average of tops; ensure `lo` stays ≥ `hi` in size. |
| **K Closest Points** | "Nearest K in Euclidean" | Max-heap-K on `x²+y²` | Use squared distance — avoids `sqrt` and float precision. |
| **IPO** | "Max capital after K projects" | Sort by capital; max-heap of profits | Projects unlock incrementally as capital grows — pointer into sorted list. |
| **Reorganize String** | "No two adjacent same char" | Max-heap by freq; place, then swap back | Impossible if `max_freq > (n+1)//2`. Handle tie when two chars have equal freq. |
| **[Task Scheduler](../../google-sde2/PROBLEM_DETAILS.md#task-scheduler)** | "Min time with cooldown n" | `(max_f-1)*(n+1) + count_max_f`, cap at len | The cap: `max(formula, len(tasks))` — when variety fills the idle slots. |
| **Sliding Window Median** | "Median in moving window of size k" | Two heaps + lazy deletion dict | Lazy delete: only remove from top when it surfaces, not immediately. |
| **Smallest Range (K Lists)** | "Smallest range containing one from each list" | K-way merge + track global max | Advance the list with the current minimum; stop when any list exhausted. |

---

## See also

- [Sorting](../algorithms/sorting.md) — QuickSelect vs heap for top-K; external merge sort using K-way merge
- [Queue](queue.md) — priority queue vs FIFO; blocking queue for concurrency
- [Graph](../algorithms/graph.md) — Dijkstra's algorithm uses a min-heap
- [Patterns Master](../../../reference/patterns/patterns-master.md) — top-K and merge-K pattern triggers
