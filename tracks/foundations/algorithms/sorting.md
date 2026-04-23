# Sorting — SDE-3 Gold Standard

Arranging data to optimize subsequent operations. Senior interviews focus on **algorithm selection reasoning**, stability under constraints, external sorting for data > RAM, and parallel implementations.

---

## 1. Algorithm Overview

| Algorithm | Avg Time | Worst Time | Space | Stable? | Best For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Merge Sort** | O(N log N) | O(N log N) | O(N) | **Yes** | Linked lists; guaranteed O(N log N); counting inversions. |
| **Quick Sort** | O(N log N) | O(N²) | O(log N) | No | In-memory arrays — practically fastest due to cache locality. |
| **Heap Sort** | O(N log N) | O(N log N) | **O(1)** | No | Strict O(1) auxiliary space with O(N log N) guarantee. |
| **Tim Sort** | O(N log N) | O(N log N) | O(N) | **Yes** | Real-world data with existing runs (Python/Java default sort). |
| **Counting Sort** | O(N + K) | O(N + K) | O(K) | **Yes** | Small integer ranges; K must fit in memory. |
| **Radix Sort** | O(N × d) | O(N × d) | O(N + B) | **Yes** | Fixed-width integers/strings; d = digits, B = base. |
| **Bucket Sort** | O(N + K) avg | O(N²) | O(N + K) | **Yes** | Uniform distributions; floating-point in [0, 1). |

> [!TIP]
> Python uses **TimSort** (hybrid merge + insertion sort). Java uses dual-pivot QuickSort for primitives and TimSort for objects. Knowing *why* each language made its choice is an SDE-3 signal: TimSort exploits partially-sorted real-world data; dual-pivot QuickSort has better cache behavior for primitive arrays.

---

## 2. Core Algorithms & Click Moments

### Merge Sort — Divide & Conquer

> [!IMPORTANT]
> **The Click Moment**: "Sort a **linked list**" — OR — "need a **stable** sort" — OR — "**count inversions** in an array" — OR — "guarantee O(N log N) **regardless** of input distribution". Merge sort is the only comparison sort that achieves all four simultaneously.

- **Idea**: Split in half, recurse each half, merge two sorted halves with two pointers.
- **Complexity**: O(N log N) time, O(N) auxiliary space (O(log N) stack).

```python
def merge_sort(nums: list[int]) -> list[int]:
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return _merge(left, right)

def _merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

> [!TIP]
> **Counting inversions**: An inversion is a pair `(i, j)` where `i < j` but `nums[i] > nums[j]`. Count them inside `_merge`: every time you pick from `right` instead of `left`, there are `len(left) - i` inversions. No extra traversal needed — O(N log N) total.

---

### Quick Sort — Partitioning

> [!IMPORTANT]
> **The Click Moment**: "In-place sort" — OR — "large dataset fitting in RAM where average speed matters" — OR — "partition around a pivot for downstream processing". QuickSort's cache locality makes it 2–3× faster than Merge Sort in practice despite the same asymptotic complexity.

- **Idea**: Pick a pivot, partition so `left < pivot ≤ right`, recurse both sides.
- **Complexity**: O(N log N) average, O(N²) worst (already-sorted input with naive pivot).

```python
import random

def quick_sort(nums: list[int], lo: int, hi: int) -> None:
    if lo >= hi:
        return
    pivot_idx = _partition(nums, lo, hi)
    quick_sort(nums, lo, pivot_idx - 1)
    quick_sort(nums, pivot_idx + 1, hi)

def _partition(nums: list[int], lo: int, hi: int) -> int:
    # Randomize pivot to avoid O(N²) on sorted input
    rand_idx = random.randint(lo, hi)
    nums[rand_idx], nums[hi] = nums[hi], nums[rand_idx]
    pivot = nums[hi]
    i = lo - 1
    for j in range(lo, hi):
        if nums[j] <= pivot:
            i += 1
            nums[i], nums[j] = nums[j], nums[i]
    nums[i + 1], nums[hi] = nums[hi], nums[i + 1]
    return i + 1
```

> [!CAUTION]
> Always **randomize the pivot** before partitioning. Naive last-element pivot degrades to O(N²) on already-sorted or reverse-sorted input — a frequent interview trap and a real production disaster for user-supplied data.

---

### QuickSelect — Kth Order Statistic

> [!IMPORTANT]
> **The Click Moment**: "Find the **Kth largest / Kth smallest**" — OR — "**median** of an unsorted array" — OR — "O(N) average time is acceptable". QuickSelect is QuickSort that skips the irrelevant half. When the interviewer says "can you do better than O(N log N)?", this is almost always the answer.

- **Idea**: Partition around a pivot. If pivot lands at k, done. Otherwise recurse only into the side containing k.
- **Complexity**: O(N) average, O(N²) worst (avoidable with random pivot). O(N) guaranteed with Median-of-Medians pivot (not expected in interviews).

```python
def find_kth_largest(nums: list[int], k: int) -> int:
    target = len(nums) - k  # kth largest = (n-k)th smallest (0-indexed)
    return _quickselect(nums, 0, len(nums) - 1, target)

def _quickselect(nums: list[int], lo: int, hi: int, target: int) -> int:
    if lo == hi:
        return nums[lo]
    pivot_idx = _partition(nums, lo, hi)  # reuse from above
    if pivot_idx == target:
        return nums[pivot_idx]
    elif pivot_idx < target:
        return _quickselect(nums, pivot_idx + 1, hi, target)
    else:
        return _quickselect(nums, lo, pivot_idx - 1, target)
```

> [!CAUTION]
> QuickSelect **mutates** the input array. If the caller needs the original order preserved, make a copy first. This side-effect surprises interviewers who assume "find" operations are read-only.

---

### Dutch National Flag — 3-Way Partition

> [!IMPORTANT]
> **The Click Moment**: "Sort array of **0s, 1s, and 2s**" — OR — "group elements into three categories in one pass" — OR — "move all zeros/negatives to the front". Three-pointer invariant, single O(N) pass, O(1) space.

```python
def sort_colors(nums: list[int]) -> None:
    lo, mid, hi = 0, 0, len(nums) - 1
    while mid <= hi:
        if nums[mid] == 0:
            nums[lo], nums[mid] = nums[mid], nums[lo]
            lo += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[hi] = nums[hi], nums[mid]
            hi -= 1
    # Loop invariant: nums[:lo]=0s, nums[lo:mid]=1s, nums[mid:]=2s
```

---

### Custom Comparators — Sorting Objects & Intervals

> [!TIP]
> When sorting **Intervals**: sort by `start` for overlap-merging problems; sort by `end` for greedy "maximum non-overlapping" problems. Getting this backwards is the #1 interval bug.

```python
from functools import cmp_to_key

# Largest Number: concatenation order comparison
def largest_number(nums: list[int]) -> str:
    if not nums or max(nums) == 0:
        return "0"
    def compare(a: str, b: str) -> int:
        return (1 if a + b < b + a else -1)
    strs = sorted(map(str, nums), key=cmp_to_key(compare))
    return "".join(strs)
```

> [!CAUTION]
> For **Largest Number**, after sorting, check if the result starts with `'0'` — this handles the all-zeros edge case (e.g., `[0, 0]` should return `"0"`, not `"00"`).

---

## 3. SDE-3 Deep Dives

### Scalability: External Merge Sort (Data > RAM)

> [!TIP]
> When the dataset doesn't fit in RAM (think: sorting 100 GB of logs on a machine with 4 GB RAM):
> 1. **Split**: Read chunks that fit in RAM, sort each chunk, write sorted runs to disk.
> 2. **K-way merge**: Use a **min-heap** of size K (one entry per run file) to merge all runs in O(N log K) time with O(K) RAM.
>
> This is the architecture behind `sort` in Unix, Google's MapReduce shuffle phase, and database `ORDER BY` with limited buffer pool.

```python
import heapq

def k_way_merge(sorted_runs: list[list[int]]) -> list[int]:
    heap = []
    iterators = [iter(run) for run in sorted_runs]
    for i, it in enumerate(iterators):
        val = next(it, None)
        if val is not None:
            heapq.heappush(heap, (val, i))

    result = []
    while heap:
        val, i = heapq.heappop(heap)
        result.append(val)
        next_val = next(iterators[i], None)
        if next_val is not None:
            heapq.heappush(heap, (next_val, i))
    return result
```

### Scalability: Streaming Sort (Approximate / Top-K)

When you need only the **top K** elements from a stream of N items (N >> K):
- Use a **min-heap of size K**. Push each element; if heap exceeds K, pop the minimum.
- Result: O(N log K) time, O(K) space — no need to sort the full stream.

### Concurrency: Parallel Merge Sort

> [!TIP]
> Merge sort is **embarrassingly parallelizable**: each half is independent. Java's `ForkJoinPool` / `Arrays.parallelSort()` splits at a configurable threshold (default: 8192 elements) and merges on the calling thread. In Python, use `concurrent.futures.ThreadPoolExecutor` for the recursive split, but note the GIL limits CPU parallelism — use `ProcessPoolExecutor` for CPU-bound sorts.

For distributed sort (MapReduce model):
- **Map**: Each worker sorts its local shard.
- **Shuffle**: Range-partition keys across workers (requires knowing the key distribution or sampling).
- **Reduce**: Each worker receives a contiguous key range, already locally sorted — final merge is trivial.

> [!CAUTION]
> **Load balancing** is the hard problem in distributed sort. Naive range partitioning skews badly on non-uniform data (e.g., log data with timestamps — most logs cluster in a short window). Use **reservoir sampling** to estimate quantiles before partitioning.

### Trade-offs: Choosing the Right Sort

| Scenario | Best Choice | Why |
| :--- | :--- | :--- |
| General in-memory sort | QuickSort (randomized) | Cache-friendly, O(N log N) avg, O(log N) space |
| Must be stable | Merge Sort or TimSort | Stable by design; use when order of equal elements matters |
| Linked list | Merge Sort | No random access — QuickSort's swap step is O(N) on linked lists |
| Data > RAM | External Merge Sort | K-way merge with disk runs |
| Top-K from stream | Min-Heap of size K | O(N log K) time, O(K) space — never materialize the full sort |
| Small integer range | Counting / Radix Sort | O(N + K) beats O(N log N) when K is small |
| Nearly sorted data | TimSort / Insertion Sort | Exploits existing runs; O(N) best case |
| O(1) auxiliary space required | Heap Sort | Only comparison sort with both O(N log N) worst and O(1) space |

---

## 4. Common Interview Problems

### Medium
- [Merge Intervals](../../google-sde2/PROBLEM_DETAILS.md#merge-intervals) — Sort by start time; sweep and merge.
- [Kth Largest Element](../../google-sde2/PROBLEM_DETAILS.md#kth-largest-element) — QuickSelect O(N) avg or min-heap O(N log K).
- **Sort Colors** — Dutch National Flag; single-pass three-pointer.
- **Largest Number** — Custom comparator: `a+b > b+a`.
- **Meeting Rooms II** — Sort starts and ends separately; two-pointer sweep for peak overlap.

### Hard
- **Count Inversions** — Merge sort modification; count right-picks during merge.
- **Maximum Gap** — Bucket sort / pigeonhole: O(N) time, the gap must span at least one empty bucket.
- **Russian Doll Envelopes** — Sort by width ascending, then height **descending**; LIS on heights (prevents same-width stacking).

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Merge Intervals](../../google-sde2/PROBLEM_DETAILS.md#merge-intervals)** | "Overlapping ranges" | Sort by start; `end = max(end, next.end)` | Update `end = max(end, next_end)`, not just `next_end`. |
| **Meeting Rooms II** | "Max concurrent meetings" | Sort starts + ends; two-pointer sweep | Use a **min-heap** of end times for generality. |
| **Largest Number** | "Lex concat order" | Custom comparator `a+b vs b+a` | Handle all-zeros: `[0,0]` → `"0"`, not `"00"`. |
| **H-Index** | "Count vs. value crossover" | Sort desc or bucket sort | Find `i` where `citations[i] >= i+1`; off-by-one is common. |
| **Kth Largest** | "Rank without full sort" | QuickSelect or min-heap-K | QuickSelect mutates array; min-heap is cleaner for streaming. |
| **Count Inversions** | "Out-of-order pairs" | Modified merge sort | Count `len(left) - i` inversions on each right-side pick. |
| **Russian Doll Envelopes** | "Nested 2D increasing" | Sort w asc, h **desc**; LIS on h | Height sort is **descending** to prevent same-width stacking. |
| **Maximum Gap** | "Largest gap in sorted form" | Bucket sort; gap spans empty bucket | Gap ≥ `(max - min) / (n-1)`; allocate `n-1` buckets. |

---

## See also

- [Divide and Conquer](divide-and-conquer.md) — merge sort and quicksort derivation
- [Heap](../data-structures/heap.md) — heap sort and top-K streaming
- [Two Pointers](two-pointers.md) — Dutch National Flag, Meeting Rooms II
- [Patterns Master](../../../reference/patterns/patterns-master.md) — sorting-based pattern triggers
