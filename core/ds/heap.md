# Heap / Priority Queue — SDE-3 Gold Standard

Complete binary tree with the heap property: parent ≤ children (min-heap) or parent ≥ children (max-heap). The canonical data structure for "always extract the current best" in O(log N).

---

## Theory & Mental Models

**What it is:** A complete binary tree stored as an array where every parent satisfies the heap property with its children. Min-heap: parent ≤ both children (root = global minimum). Max-heap: parent ≥ both children (root = global maximum). Core invariant: heap property maintained after every insert/delete via sift-up/sift-down.

**Why it exists:** Solves the problem of repeatedly extracting the current best (min or max) element from a dynamic set. Real-world analogy: a hospital triage queue — the most critical patient is always treated next, regardless of arrival order.

**Memory layout:** Stored as a flat array (0-indexed): parent of `i` is at `(i-1)//2`; children are at `2i+1` and `2i+2`. This avoids pointer overhead and gives good cache locality for the top levels.

**Key invariants:**
- Every parent satisfies the heap property with both children — not just one.
- The tree is always complete (filled level-by-level, left to right) — this enables array storage.
- After insert: append to end, sift up. After extract-root: move last element to root, sift down.
- Build-heap from an unsorted array is O(N) — not O(N log N). Start from last non-leaf and sift down.

**Complexity at a glance:**

| Operation | Time | Notes |
| :--- | :--- | :--- |
| Peek min/max | O(1) | Root of heap |
| Insert | O(log N) | Sift up |
| Extract min/max | O(log N) | Sift down |
| Build heap | O(N) | Heapify from last non-leaf |
| Arbitrary delete | O(log N) | Swap with last, sift down |
| Search | O(N) | No ordering across siblings |

**When to reach for it:**
- Top-K largest/smallest from a stream (heap of size K).
- Dynamic median maintenance (two heaps: max-heap lower half + min-heap upper half).
- Dijkstra's shortest path — always expand the lowest-cost unvisited node.
- K-way merge of sorted lists/arrays.
- Priority scheduling — always process the highest-priority available task.

**Common mistakes:**
- Python's `heapq` is min-heap only — negate values to simulate max-heap; negate again on pop.
- Not including a unique tie-breaker in tuples — comparing non-comparable objects (e.g., `ListNode`) raises `TypeError`.
- Calling `heapq.heapify()` on a non-list or forgetting to call it after bulk construction with `append`.
- Using lazy deletion incorrectly — must check if the popped element is still valid before processing.

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

#### Common Variants & Twists
1. **Find K Pairs with Smallest Sums**:
   - **What (The Problem & Goal):** Given two sorted arrays, find the `K` pairs `(u, v)` (one from each array) with the smallest sums.
   - **How (Intuition & Mental Model):** Seed the Min-Heap with `(nums1[i] + nums2[0], i, 0)` for all `i`. This avoids an O(N²) initial population. When popping the smallest pair `(i, j)`, immediately push the next pair in that row: `(nums1[i] + nums2[j+1], i, j+1)` if `j+1` is within bounds.
2. **Kth Smallest Element in a Sorted Matrix**:
   - **What (The Problem & Goal):** Find the $K^{th}$ smallest element in an $N \times N$ matrix where every row and every column is sorted.
   - **How (Intuition & Mental Model):** Exactly the same logic as K-Way Merge. Seed the heap with the first element of each row `(matrix[i][0], i, 0)`. Pop `K-1` times, advancing the column index each time `(matrix[i][j+1], i, j+1)`. The $K^{th}$ popped element is the answer.

### Custom Object Comparators

> [!IMPORTANT]
> **The Click Moment**: "I need to put **complex objects** (e.g., custom nodes) into a priority queue without using a messy tuple tie-breaker." — OR — "I need a **max-heap of objects**." Python's `heapq` relies entirely on the `<` operator (`__lt__`). By defining `__lt__` in a wrapper class, you control exactly how objects are prioritized.

```python
import heapq

class Task:
    def __init__(self, name: str, priority: int, duration: int):
        self.name = name
        self.priority = priority
        self.duration = duration
        
    def __lt__(self, other: 'Task'):
        # Max-heap by priority, then Min-heap by duration as tie-breaker
        if self.priority != other.priority:
            return self.priority > other.priority  # > makes it a max-heap for this field
        return self.duration < other.duration      # < makes it a min-heap for this field

def schedule_tasks(tasks: list[Task]) -> list[str]:
    heapq.heapify(tasks)  # O(N) because __lt__ is defined
    order = []
    while tasks:
        order.append(heapq.heappop(tasks).name)
    return order
```

> [!TIP]
> Writing a wrapper class with `__lt__` is often cleaner in interviews than juggling `(-priority, duration, counter, item)` tuples, especially when the priority logic has multiple tie-breaker levels.

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

#### Common Variants & Twists
1. **Sliding Window Median**:
   - **What (The Problem & Goal):** Maintain the median as a fixed-size window slides across an array.
   - **How (Intuition & Mental Model):** Use two heaps, but removing elements from the middle of a heap is O(N). Instead, use **lazy deletion**. Track invalid elements (those that have slid out of the window) in a Hash Map counter. When you pop from a heap, if the popped element is in the "invalid" map, discard it and pop again. This avoids O(N) re-heapification per step.
2. **IPO (Maximize Capital)**:
   - **What (The Problem & Goal):** Pick at most `K` projects to maximize capital. You can only start a project if your current capital `>=` its required capital.
   - **How (Intuition & Mental Model):** A twist on two ordered structures. Sort projects by required capital. Iterate through the sorted projects and push the profit of all *currently affordable* projects into a Max-Heap. Pop the top of the Max-Heap (most profitable), add it to your capital, and repeat `K` times.

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

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **[Merge K Sorted Lists](../algo/problem-deep-dives.md#merge-k-sorted-lists)** | K-Way Merge (Min-Heap) | "Smallest among K heads" | Min-heap `(val, list_id, node)` | Tie-break: include `list_id` as second element to avoid comparing nodes. |
| **[Kth Largest Element](../algo/problem-deep-dives.md#kth-largest-element)** | "Rank without full sort" | QuickSelect O(N) avg or min-heap-K | QuickSelect mutates array; heap is cleaner for streams. Confirm if K can equal N. |
| **[Top K Frequent](../algo/problem-deep-dives.md#top-k-frequent-elements)** | "K by frequency" | Count + min-heap-K, or bucket sort | Bucket sort is O(N) — prefer when K not given or K = N. |
| **[Find Median from Stream](../algo/problem-deep-dives.md#find-median-from-data-stream)** | "Median as data arrives" | Two heaps: max-lo + min-hi | Even count → average of tops; ensure `lo` stays ≥ `hi` in size. |
| **K Closest Points** | "Nearest K in Euclidean" | Max-heap-K on `x²+y²` | Use squared distance — avoids `sqrt` and float precision. |
| **IPO** | "Max capital after K projects" | Sort by capital; max-heap of profits | Projects unlock incrementally as capital grows — pointer into sorted list. |
| **Reorganize String** | "No two adjacent same char" | Max-heap by freq; place, then swap back | Impossible if `max_freq > (n+1)//2`. Handle tie when two chars have equal freq. |
| **[Task Scheduler](../algo/problem-deep-dives.md#task-scheduler)** | "Min time with cooldown n" | `(max_f-1)*(n+1) + count_max_f`, cap at len | The cap: `max(formula, len(tasks))` — when variety fills the idle slots. |
| **Sliding Window Median** | "Median in moving window of size k" | Two heaps + lazy deletion dict | Lazy delete: only remove from top when it surfaces, not immediately. |
| **Smallest Range (K Lists)** | "Smallest range containing one from each list" | K-way merge + track global max | Advance the list with the current minimum; stop when any list exhausted. |
| **Last Stone Weight** [E] | "Repeatedly smash two heaviest stones" | Max-heap; pop two, push difference if nonzero | Python has min-heap only — negate values to simulate max-heap. |
| **Kth Largest in Stream** [E] | "Maintain Kth largest as elements arrive" | Min-heap of size K; root = Kth largest | Pop when size > K to keep only top K; root of min-heap is Kth largest. |
| **Find Median from Stream** [M] | "Maintain median for dynamic insertions" | Max-heap (lower half) + min-heap (upper half); rebalance so sizes differ by ≤ 1 | Always push to max-heap first, then move max of max-heap to min-heap — ensures balance invariant. |
| **Furthest Building You Can Reach** [M] | "Use bricks/ladders optimally to climb" | Min-heap of ladder-used jumps; swap smallest ladder for bricks when bricks run out | Greedily save ladders for largest jumps; min-heap tracks the smallest ladder jump currently used. |
| **Single-Threaded CPU** [M] | "Process tasks: pick smallest duration at available time" | Sort by enqueue time; min-heap of `(duration, index)`; advance time if idle | If CPU idle, jump time to next task's enqueue time — don't simulate every second. |
| **Maximum Performance of a Team** [M] | "Choose K engineers, maximize sum_speed × min_efficiency" | Sort by efficiency desc; sliding window with min-heap of size K on speed | When adding engineer i (efficiency = new min), pop smallest speed from heap to maintain size K. |
| **K Closest Points to Origin** [M] | "Efficiently find K closest" | Max-heap of size K; pop if heap size > K | Alternatively: QuickSelect O(N) average — no sorting needed. Max-heap gives O(N log K). |
| **Meeting Rooms II** [M] | "Minimum conference rooms needed" | Sort by start; min-heap of end times; pop if `end <= new_start` | Heap size = rooms in use at any point = answer at peak. |
| **Ugly Number II** [M] | "Nth ugly number (factors only 2, 3, 5)" | Min-heap; push `n*2`, `n*3`, `n*5` on each pop; deduplicate | Use a visited set or three-pointer DP approach to avoid duplicates in heap. |
| **Find K Pairs with Smallest Sums** [M] | "K smallest pairs (one from each sorted array)" | Min-heap seeded with `(nums1[i]+nums2[0], i, 0)`; expand column per row | Only seed first column; on pop `(i, j)`, push `(i, j+1)` — avoids O(N²) initial population. |
| **Trapping Rain Water II** [H] | "3D trapped water in matrix" | Min-heap BFS from borders; propagate water level inward | Level at each cell = `max(border_height, parent_level)`; process border cells first. |

---

## Quick Revision Triggers

- If the problem says "top K largest/smallest" → think Min-Heap of size K; pop when size exceeds K; root = K-th largest.
- If the problem says "median of a stream" → think Two Heaps; max-heap for lower half (negated in Python), min-heap for upper half; rebalance on every insert.
- If the problem says "merge K sorted lists/arrays" → think K-Way Merge Heap; push `(value, list_idx, element_idx)` tuples with tie-breaking index.
- If the problem says "shortest path in weighted graph" → think Dijkstra with min-heap; `(cost, node)` tuple; skip already-settled nodes.
- If the problem says "scheduling with deadlines or priorities" → think Max-Heap of available tasks; unlock tasks as capacity grows.
- If you need a max-heap in Python → negate values before pushing and negate again after popping; use `(-priority, counter, item)` for stability.
- If the problem says "build heap from array" → use `heapq.heapify()` which is O(N) — not O(N log N).

## See also

- [Sorting](../algo/sorting.md) — QuickSelect vs heap for top-K; external merge sort using K-way merge
- [Queue](queue.md) — priority queue vs FIFO; blocking queue for concurrency
- [Graph](../algo/graph.md) — Dijkstra's algorithm uses a min-heap
- [Patterns Master](../../reference/patterns/patterns-master.md) — top-K and merge-K pattern triggers
