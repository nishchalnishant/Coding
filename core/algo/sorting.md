# Sorting — SDE-3 Gold Standard

Arranging data to optimize subsequent operations. Senior interviews focus on **algorithm selection reasoning**, stability under constraints, external sorting for data > RAM, and parallel implementations.

---

## Theory & Mental Models

**What it is.** Arrange elements in a defined order — the foundation for a vast class of algorithmic optimizations. Core invariant: once data is sorted, binary search, two-pointer, and greedy interval algorithms become applicable — many O(N²) problems drop to O(N) or O(N log N).

**Why it exists.** "Sorting is the unlock." Sorted data enables binary search (O(log N) lookup), greedy interval algorithms (sort by end time → O(N) scan), two-pointer techniques (sorted array → O(N) two-sum), and merge-based counting (inversions, closest pair). Algorithm selection depends on: stability requirement, memory constraint, data size vs RAM, and whether data has special structure.

**The mental model.** Sorting doesn't just order data — it reveals structure. A sorted array is a prerequisite for a dozen other algorithms. Every time you sort, ask: "what does this unlock?" Comparison sorts are bounded by Ω(N log N); non-comparison sorts (counting, radix) break this with O(N) when K is small.

**Complexity at a glance.**

| Algorithm | Avg Time | Worst Time | Space | Stable? |
| :--- | :--- | :--- | :--- | :--- |
| Merge Sort | O(N log N) | O(N log N) | O(N) | Yes |
| Quick Sort (randomized) | O(N log N) | O(N²) | O(log N) | No |
| Heap Sort | O(N log N) | O(N log N) | O(1) | No |
| TimSort (Python default) | O(N log N) | O(N log N) | O(N) | Yes |
| Counting Sort | O(N + K) | O(N + K) | O(K) | Yes |
| Radix Sort | O(N × d) | O(N × d) | O(N + B) | Yes |

**When to reach for it.**
- Pre-process before binary search, two-pointer, or greedy interval pass.
- Count inversions — merge sort augmented.
- Kth order statistic without full sort — QuickSelect O(N) avg.
- External sort when data exceeds RAM — external merge sort with K-way heap merge.
- Top-K from a stream — min-heap of size K, O(N log K).

**When NOT to use it.**
- K is large for counting sort — memory blowup (O(K) space).
- Using naive pivot QuickSort on nearly-sorted input — degrades to O(N²); always randomize.
- Using unstable sort when equal-element relative order matters (e.g., stable sort by secondary key).

**Common mistakes.**
- Unstable sort when equal-element order matters — Python's `sorted()` / `.sort()` are TimSort (stable); Java's `Arrays.sort` on objects is also stable, but on primitives uses dual-pivot QuickSort (unstable).
- Naive last-element pivot in QuickSort on sorted input — O(N²) worst case; always randomize.
- Applying counting sort when K >> N — the O(K) space dominates and kills performance.
- Interval problems: sorting by start vs end — merging intervals uses start; maximum non-overlapping uses end.

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

#### Common Variants & Twists
1. **Count of Range Sum**:
   - **What (The Problem & Goal):** Given an array, find the number of subarrays whose sum lies in `[lower, upper]`.
   - **How (Intuition & Mental Model):** Calculate prefix sums. The problem becomes finding pairs `(i, j)` where `lower <= prefix[j] - prefix[i] <= upper`. Use merge sort on the prefix sums. Before merging the two sorted halves, for each element in the left half, use two pointers in the right half to find the window of elements that satisfy the range sum condition.
2. **Reverse Pairs**:
   - **What (The Problem & Goal):** Count pairs `(i, j)` where `i < j` and `nums[i] > 2 * nums[j]`.
   - **How (Intuition & Mental Model):** Also a merge sort twist. Before merging, use two pointers to count how many `nums[i]` in the left half are greater than `2 * nums[j]` in the right half. Count first, then merge.
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

#### Common Variants & Twists
1. **Pancake Sorting**:
   - **What (The Problem & Goal):** Sort an array using only the "flip" operation (reverses prefix of length `k`).
   - **How (Intuition & Mental Model):** This is selection sort with a twist. At each step, find the current largest element, flip it to the front, and then flip it to its correct sorted position at the end. Repeat for smaller and smaller prefixes.
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

#### Common Variants & Twists
1. **K Closest Points to Origin**:
   - **What (The Problem & Goal):** Given a list of points, find the `k` points closest to the origin.
   - **How (Intuition & Mental Model):** Calculate squared distances. Use QuickSelect on these distances to find the `k`-th smallest. All points to the left of the resulting pivot are the `k` closest.
2. **Top K Frequent Elements**:
   - **What (The Problem & Goal):** Find the `k` most frequent elements.
   - **How (Intuition & Mental Model):** Count frequencies. Use QuickSelect on the unique elements based on their frequencies to find the top `k` in O(N) average time.
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

#### Common Variants & Twists
1. **Sort Transformed Array**:
   - **What (The Problem & Goal):** Given a sorted array and a quadratic function `f(x) = ax^2 + bx + c`, return the sorted result of `f(x)` for each `x`.
   - **How (Intuition & Mental Model):** If `a > 0`, the function is a parabola opening upward; extreme values are at the ends of the array. Use two pointers starting at both ends and pick the larger value. If `a < 0`, start two pointers at both ends and pick the smaller value (filling the result array from middle or reverse).
2. **Move Zeroes**:
   - **What (The Problem & Goal):** Move all 0s to the end of the array while maintaining the relative order of non-zero elements.
   - **How (Intuition & Mental Model):** Use two pointers. `lo` tracks where the next non-zero should go. `mid` iterates. Every time `nums[mid] != 0`, swap `nums[lo]` and `nums[mid]` and increment `lo`. This is a 2-way Dutch National Flag variation.
```

---

### Counting Sort & Radix Sort — O(N) Linear Sorts

> [!IMPORTANT]
> **The Click Moment**: "Sort an array where elements are guaranteed to be in a small range `[0, K]`" — OR — "sort fixed-width integers/strings". When you must break the O(N log N) comparison barrier.

**Counting Sort** (O(N + K)): Count frequencies, prefix-sum the counts to find exact placement indices.
```python
def counting_sort(nums: list[int], max_val: int) -> list[int]:
    counts = [0] * (max_val + 1)
    for num in nums:
        counts[num] += 1
        
    # Prefix sum to determine ending positions
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
        
    result = [0] * len(nums)
    # Iterate backwards to maintain stability!
    for num in reversed(nums):
        counts[num] -= 1
        result[counts[num]] = num
        
    return result
```

**Radix Sort** (O(N × d)): Sort by least-significant digit to most-significant digit, using Counting Sort as the stable subroutine.
```python
def radix_sort(nums: list[int]) -> list[int]:
    if not nums: return []
    max_num = max(nums)
    exp = 1  # 1, 10, 100, 1000...
    
    while max_num // exp > 0:
        counts = [0] * 10
        for num in nums:
            counts[(num // exp) % 10] += 1
        for i in range(1, 10):
            counts[i] += counts[i - 1]
            
        result = [0] * len(nums)
        for num in reversed(nums):
            digit = (num // exp) % 10
            counts[digit] -= 1
            result[counts[digit]] = num
            
        for i in range(len(nums)):
            nums[i] = result[i]
        exp *= 10
    return nums
    
#### Common Variants & Twists
1. **Maximum Gap**:
   - **What (The Problem & Goal):** Find the maximum gap between successive elements in their sorted form in O(N) time.
   - **How (Intuition & Mental Model):** Use Bucket Sort logic. Divide the range `[min, max]` into `n-1` buckets. The maximum gap cannot occur within a bucket (by Pigeonhole Principle); it must occur between buckets. Track `min` and `max` for each bucket.
2. **Sort Characters By Frequency**:
   - **What (The Problem & Goal):** Sort a string by decreasing character frequency.
   - **How (Intuition & Mental Model):** Use bucket sort where the index is the frequency. Put characters with the same frequency in the same bucket. Traverse the buckets from largest frequency to smallest.
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

#### Common Variants & Twists
1. **Custom Sort String**:
   - **What (The Problem & Goal):** Given an order string `order` and a string `s`, sort the characters of `s` to follow the sequence of `order`.
   - **How (Intuition & Mental Model):** Create a mapping `char -> rank` based on `order`. Sort `s` using this rank as the key. Characters not in `order` can have any rank (e.g., infinity).
2. **Queue Reconstruction by Height**:
   - **What (The Problem & Goal):** Reconstruct a queue where each person is represented by `(h, k)` (height, number of people in front who are ≥ height).
   - **How (Intuition & Mental Model):** Sort people by height descending, and by `k` ascending for ties. Then, iterate and insert each person into the result list at index `k`. This works because all previously inserted people are taller, so their relative order isn't changed by inserting a shorter person at `k`.
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
- [Merge Intervals](problem-deep-dives.md#merge-intervals) — Sort by start time; sweep and merge.
- [Kth Largest Element](problem-deep-dives.md#kth-largest-element) — QuickSelect O(N) avg or min-heap O(N log K).
- **Sort Colors** — Dutch National Flag; single-pass three-pointer.
- **Largest Number** — Custom comparator: `a+b > b+a`.
- **Meeting Rooms II** — Sort starts and ends separately; two-pointer sweep for peak overlap.

### Hard
- **Count Inversions** — Merge sort modification; count right-picks during merge.
- **Maximum Gap** — Bucket sort / pigeonhole: O(N) time, the gap must span at least one empty bucket.
- **Russian Doll Envelopes** — Sort by width ascending, then height **descending**; LIS on heights (prevents same-width stacking).

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **[Merge Intervals](problem-deep-dives.md#merge-intervals)** | Sort + Greedy Merge | "Overlapping ranges" | Sort by start; `end = max(end, next.end)` | Update `end = max(end, next_end)`, not just `next_end`. |
| **Meeting Rooms II** | "Max concurrent meetings" | Sort starts + ends; two-pointer sweep | Use a **min-heap** of end times for generality. |
| **Largest Number** | "Lex concat order" | Custom comparator `a+b vs b+a` | Handle all-zeros: `[0,0]` → `"0"`, not `"00"`. |
| **H-Index** | "Count vs. value crossover" | Sort desc or bucket sort | Find `i` where `citations[i] >= i+1`; off-by-one is common. |
| **Kth Largest** | "Rank without full sort" | QuickSelect or min-heap-K | QuickSelect mutates array; min-heap is cleaner for streaming. |
| **Count Inversions** | "Out-of-order pairs" | Modified merge sort | Count `len(left) - i` inversions on each right-side pick. |
| **Russian Doll Envelopes** | "Nested 2D increasing" | Sort w asc, h **desc**; LIS on h | Height sort is **descending** to prevent same-width stacking. |
| **Maximum Gap** | "Largest gap in sorted form" | Bucket sort; gap spans empty bucket | Gap ≥ `(max - min) / (n-1)`; allocate `n-1` buckets. |
| **Sort Colors (Dutch National Flag)** [M] | "Sort array of 0s, 1s, 2s in one pass" | Three pointers: `lo`, `mid`, `hi`; swap 0s left, 2s right | `mid` advances on 0 (after swap) and 1 (no swap), but NOT on 2 — element from `hi` is unknown. |
| **Sort Characters by Frequency** [M] | "Descending frequency sort of string chars" | Count frequencies; sort by `-freq`; rebuild string | Bucket sort alternative: group by frequency index for O(N) vs O(N log N). |
| **Wiggle Sort II** [M] | "nums[0] < nums[1] > nums[2] < ..." | QuickSelect for median; 3-way partition; interleave via index mapping | Index mapping `(1 + 2*i) % (n | 1)` places larger half at odd indices without extra space. |
| **Find K-th Smallest Pair Distance** [H] | "Kth smallest absolute difference of any pair" | Binary search on answer; count pairs with distance ≤ mid via two pointers on sorted array | Binary search over difference value [0, max-min]; counting pairs is O(N) with two pointers. |
| **Minimum Number of Moves to Seat Everyone** [E] | "Match seats to students to minimize total moves" | Sort both arrays; pair sorted seats with sorted students; sum abs differences | Greedy: sorted pairing always minimizes total displacement (exchange argument). |
| **Largest Perimeter Triangle** [M] | "Largest triangle perimeter from array sides" | Sort desc; check first triplet where `a[i] < a[i-1] + a[i-2]` | Valid triangle: sum of two shorter sides > longest side. Only need to check adjacent triples after sorting. |
| **Minimum Time Difference** [M] | "Min difference between any two times in list" | Convert to minutes; sort; check adjacent and wrap-around (last - first vs 1440) | Circular: last gap = `1440 - (last - first)`. Sort enables O(N log N) instead of O(N²) pairs. |
| **Maximum Ice Cream Bars** [M] | "Buy max bars within budget; cheapest first" | Sort by cost; buy greedily from cheapest | Greedy works: maximizing count = minimize cost per item = take cheapest first. |
| **3Sum Closest** [M] | "Triplet sum closest to target" | Sort; fix `i`; two pointers; update closest on each candidate | Update closest only; move both pointers on exact match for efficiency. |
| **4Sum** [M] | "All unique quadruples summing to target" | Sort; fix two outer loops; two pointers for inner | Deduplicate at all four levels: outer loop `i`, second loop `j`, and both pointer positions. |

---

## Quick Revision Triggers

- "Problem becomes easy after sorting" → sort first; two pointers / greedy / binary search then apply.
- "Need stable sort preserving original order of equal elements" → merge sort or Python's TimSort (`sorted()`).
- "Sort and count inversions simultaneously" → merge sort; count cross-half pairs during merge step.
- "Interval problems: merge overlapping" → sort by start; greedy merge.
- "Interval problems: non-overlapping / scheduling" → sort by end; greedy pick earliest ending.
- "Values bounded by small range (0–K)" → counting sort O(N+K); or radix sort O(N·d) for integers.
- "Custom comparator in Python" → `functools.cmp_to_key`; never use `<` override alone (doesn't sort correctly).

---

## See also

- [Divide and Conquer](divide-and-conquer.md) — merge sort and quicksort derivation
- [Heap](../ds/heap.md) — heap sort and top-K streaming
- [Two Pointers](two-pointers.md) — Dutch National Flag, Meeting Rooms II
- [Patterns Master](../../../reference/patterns/patterns-master.md) — sorting-based pattern triggers
