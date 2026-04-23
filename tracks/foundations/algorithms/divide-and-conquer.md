# Divide and Conquer — SDE-3 Gold Standard

Break a problem into **independent subproblems**, solve recursively, and **combine** results. SDE-3 expects: Master Theorem application, recognizing D&C vs DP vs Greedy, and key augmentations (counting inversions, closest pair).

---

## 1. The Three Steps

> [!IMPORTANT]
> **The Click Moment**: "**Split** into equal halves, solve each independently, **merge**" — OR — "recurrence T(n) = aT(n/b) + O(n^k)" — OR — "the combine step reveals global information not visible in either half" (e.g., cross-midpoint subarray, cross-half inversions). D&C is the choice when subproblems are **independent** (no overlap) and the combine step is tractable.

1. **Divide**: Break the problem at a natural boundary (midpoint, pivot, median).
2. **Conquer**: Solve each part recursively. Base case = direct computation.
3. **Combine**: Merge results — this step often holds the insight (cross-half inversions, cross-midpoint subarray).

---

## 2. Core Algorithms & Click Moments

### Merge Sort — Guaranteed O(N log N)

> [!IMPORTANT]
> **The Click Moment**: "**Count inversions**" — OR — "**sort a linked list**" — OR — "stable sort with **guaranteed O(N log N)** worst case". The merge step is where cross-half inversions are counted for free.

```python
def merge_sort_count_inversions(nums: list[int]) -> tuple[list[int], int]:
    if len(nums) <= 1:
        return nums, 0
    mid = len(nums) // 2
    left, left_inv = merge_sort_count_inversions(nums[:mid])
    right, right_inv = merge_sort_count_inversions(nums[mid:])
    merged, split_inv = merge_count(left, right)
    return merged, left_inv + right_inv + split_inv

def merge_count(left: list[int], right: list[int]) -> tuple[list[int], int]:
    result = []
    inversions = 0
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
            inversions += len(left) - i  # all remaining left elements are > right[j]
    result.extend(left[i:])
    result.extend(right[j:])
    return result, inversions
```

---

### QuickSelect — O(N) Kth Element

> [!IMPORTANT]
> **The Click Moment**: "**Kth largest/smallest** element without full sort" — OR — "find the **median** in O(N) average". QuickSelect uses the partition step of QuickSort but only recurses into the half containing the target rank.

```python
import random

def quickselect(nums: list[int], k: int) -> int:
    target = len(nums) - k  # k-th largest = (n-k)-th smallest (0-indexed)
    return _qs(nums, 0, len(nums) - 1, target)

def _partition(nums: list[int], lo: int, hi: int) -> int:
    rand_idx = random.randint(lo, hi)
    nums[rand_idx], nums[hi] = nums[hi], nums[rand_idx]
    pivot, i = nums[hi], lo - 1
    for j in range(lo, hi):
        if nums[j] <= pivot:
            i += 1
            nums[i], nums[j] = nums[j], nums[i]
    nums[i+1], nums[hi] = nums[hi], nums[i+1]
    return i + 1

def _qs(nums: list[int], lo: int, hi: int, target: int) -> int:
    if lo == hi:
        return nums[lo]
    p = _partition(nums, lo, hi)
    if p == target:
        return nums[p]
    elif p < target:
        return _qs(nums, p + 1, hi, target)
    else:
        return _qs(nums, lo, p - 1, target)
```

---

### Fast Exponentiation — O(log N)

> [!IMPORTANT]
> **The Click Moment**: "Compute **x^n** efficiently" — OR — "matrix exponentiation for **Fibonacci in O(log N)**" — OR — any problem that reduces to repeated squaring. Halving the exponent at each step gives O(log N).

```python
def fast_pow(x: float, n: int) -> float:
    if n < 0:
        x, n = 1.0 / x, -n
    result = 1.0
    while n:
        if n % 2 == 1:
            result *= x
        x *= x
        n //= 2
    return result
```

> [!CAUTION]
> **INT_MIN overflow in other languages**: Negating `n` when `n = INT_MIN` overflows in Java/C++ (INT_MIN = -2^31; its negation exceeds INT_MAX). Cast to `long` before negation. In Python, integers are arbitrary precision — not an issue.

---

### Maximum Subarray — Cross-Midpoint Combine

> [!IMPORTANT]
> **The Click Moment**: "Explain how **Kadane's** relates to D&C" — OR — when an interviewer asks for the D&C approach to maximum subarray (O(N log N)). The insight: the maximum subarray either lies entirely in the left half, entirely in the right half, or **crosses the midpoint**. Compute the cross-midpoint case in O(N) by expanding outward from mid.

```python
def max_subarray_dc(nums: list[int], lo: int, hi: int) -> int:
    if lo == hi:
        return nums[lo]
    mid = (lo + hi) // 2
    left_max = max_subarray_dc(nums, lo, mid)
    right_max = max_subarray_dc(nums, mid + 1, hi)
    # Cross-midpoint: expand left from mid, right from mid+1
    cross_left = cross_right = float('-inf')
    running = 0
    for i in range(mid, lo - 1, -1):
        running += nums[i]
        cross_left = max(cross_left, running)
    running = 0
    for i in range(mid + 1, hi + 1):
        running += nums[i]
        cross_right = max(cross_right, running)
    return max(left_max, right_max, cross_left + cross_right)
```

> [!TIP]
> Kadane's (O(N)) is almost always preferred over D&C (O(N log N)) for maximum subarray in practice. Mention D&C when the interviewer asks "how would you verify your O(N) solution's correctness?" — the D&C formulation makes the recurrence clear.

---

### Closest Pair of Points — O(N log N)

> [!IMPORTANT]
> **The Click Moment**: "Minimum distance between any **two points** in a 2D plane" in less than O(N²). The D&C trick: after finding the minimum distance δ in each half, only check points within distance δ of the dividing line — and at most 7 other points per candidate (geometric packing argument).

```python
def closest_pair(points: list[tuple[float,float]]) -> float:
    import math
    pts = sorted(points)  # sort by x coordinate

    def dist(p1, p2):
        return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

    def rec(pts_x):
        n = len(pts_x)
        if n <= 3:
            return min(dist(pts_x[i], pts_x[j]) for i in range(n) for j in range(i+1, n))
        mid = n // 2
        mid_x = pts_x[mid][0]
        d = min(rec(pts_x[:mid]), rec(pts_x[mid:]))
        strip = [p for p in pts_x if abs(p[0] - mid_x) < d]
        strip.sort(key=lambda p: p[1])  # sort by y
        for i in range(len(strip)):
            for j in range(i+1, min(i+8, len(strip))):  # at most 7 candidates
                if strip[j][1] - strip[i][1] >= d:
                    break
                d = min(d, dist(strip[i], strip[j]))
        return d

    return rec(pts)
```

---

## 3. Master Theorem

> [!TIP]
> For recurrences T(n) = aT(n/b) + f(n) where a ≥ 1, b > 1:

| Case | Condition | Result |
| :--- | :--- | :--- |
| **Case 1** | f(n) = O(n^(log_b(a) - ε)) | T(n) = Θ(n^(log_b(a))) |
| **Case 2** | f(n) = Θ(n^(log_b(a))) | T(n) = Θ(n^(log_b(a)) log n) |
| **Case 3** | f(n) = Ω(n^(log_b(a) + ε)) and regularity | T(n) = Θ(f(n)) |

**Common recurrences**:

| Algorithm | Recurrence | Result |
| :--- | :--- | :--- |
| Merge Sort | T(n) = 2T(n/2) + Θ(n) | Θ(n log n) — Case 2 |
| Binary Search | T(n) = T(n/2) + Θ(1) | Θ(log n) — Case 2 |
| Strassen's Matrix Mult | T(n) = 7T(n/2) + Θ(n²) | Θ(n^log₂7) ≈ Θ(n^2.81) — Case 1 |
| Fast Pow (iterative) | T(n) = T(n/2) + Θ(1) | Θ(log n) — Case 2 |

> [!CAUTION]
> Master Theorem requires a and b to be **constants** — not functions of n. Also, the "regularity condition" in Case 3 must be verified (af(n/b) ≤ cf(n) for some c < 1). For non-uniform splits (QuickSort's average case), use the recursion tree or the Akra-Bazzi theorem instead.

---

## 4. SDE-3 Deep Dives

### D&C vs DP: The Key Distinction

> [!IMPORTANT]
> **D&C**: Subproblems are **independent** — solving the left half never depends on or influences the right half. No caching needed. O(recursion depth × combine cost).
>
> **DP**: Subproblems **overlap** — the same subproblem arises from multiple distinct calls. Memoization or tabulation avoids recomputation.
>
> Quick test: Draw the recursion tree. If nodes at the same level have different arguments → D&C (independent). If they share arguments → DP (overlapping).

### Scalability: Parallel D&C

> [!TIP]
> D&C is **embarrassingly parallelizable**: the left and right subproblems are independent and can run on separate cores/machines. Java's `ForkJoinPool` implements parallel merge sort with a configurable threshold — below the threshold, use sequential sort (avoids thread overhead for small arrays). Python: use `multiprocessing.Pool` for CPU-bound D&C; `ThreadPoolExecutor` is limited by the GIL for Python code.
>
> **MapReduce as D&C**: The map phase = divide (parallel); reduce phase = combine (also parallel per key). Merge sort on 1 TB of data: workers sort local shards (map), then a tree of reducers merges pairs (combine) — O(N/P log N/P + log P × N/P) total time.

### Concurrency: Thread-Safe Combine

> [!CAUTION]
> The combine step often requires **coordination**: all sub-results must be available before combining. Use `Future.get()` (Java) or `Pool.map()` (Python) to block until all recursive calls complete. Avoid shared mutable state in the combine step — each level should produce a new result rather than mutating a shared array.

---

## 5. Common Interview Problems

### Easy
- **Merge Two Sorted Lists** — Building block for merge sort combine step.
- **Majority Element** — Boyer-Moore O(N) or D&C: majority of whole = majority of a half (then verify).
- **Pow(x, n)** — Fast exponentiation; handle `n < 0`.

### Medium
- **Sort List** — Merge sort on linked list; O(N log N) time, O(log N) stack.
- **Kth Largest Element** — QuickSelect; O(N) average.
- **Majority Element II** (n/3) — Boyer-Moore extended; two candidates.
- **Count of Range Sum** — Merge sort augmented; count cross-half pairs in range [lower, upper].

### Hard
- **[Merge K Sorted Lists](../../google-sde2/PROBLEM_DETAILS.md#merge-k-sorted-lists)** — D&C pairwise merge: O(N log K) time.
- **[Median of Two Sorted Arrays](../../google-sde2/PROBLEM_DETAILS.md#median-of-two-sorted-arrays)** — Binary search on partition; O(log(min(m,n))).
- **Count of Smaller Numbers After Self** — Merge sort augmented; count right-picks during merge.
- **Reverse Pairs** — Merge sort; count pairs `nums[i] > 2 × nums[j]` across halves.
- **Closest Pair of Points** — O(N log N) D&C; strip scanning.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **Merge Sort** | "Stable sort, guaranteed O(N log N)" | Divide at mid; merge sorted halves | Combine step is O(N) — include in recurrence T(n)=2T(n/2)+O(n). |
| **Count Inversions** | "Pairs where i<j but nums[i]>nums[j]" | Merge sort; count right-picks during merge (`len(left)-i`) | Requires a copy of left array; in-place merge loses position info. |
| **QuickSelect** | "Kth largest in O(N) average" | Partition; recurse only into side with target | Mutates array; randomize pivot to avoid O(N²). Median-of-medians gives O(N) worst. |
| **Pow(x,n)** | "Fast exponentiation" | `x^n = (x^(n/2))²`; odd: multiply by x once | Negative n: `x = 1/x, n = -n`; INT_MIN overflow in Java/C++. |
| **Maximum Subarray (D&C)** | "Explain subarray beyond Kadane's" | Cross-midpoint expansion + max of three cases | O(N log N) — always mention Kadane is O(N) and preferred; D&C demonstrates recurrence thinking. |
| **[Majority Element](../../google-sde2/PROBLEM_DETAILS.md#majority-element)** | "Element appearing >n/2 times" | Boyer-Moore O(N)/O(1) or D&C — majority of whole must be majority of some half | D&C: majority of neither half → no majority. Must verify in O(N) second pass. |
| **Merge K Sorted Lists** | "Merge K into one sorted list" | D&C pairwise merge: merge pairs in O(N log K) | K-way heap is also O(N log K) — D&C has better cache locality. |
| **Reverse Pairs** | "Pairs where nums[i] > 2×nums[j], i<j" | Modified merge sort; count cross-half pairs | Different from standard inversions — inequality is strict and scaled. Use two pointers in combine. |
| **Closest Pair of Points** | "Min distance in 2D plane, O(N log N)" | D&C with strip of width 2δ; sort strip by y; check 7 candidates | 6-point packing argument ensures at most 7 comparisons per strip point. |

---

## See also

- [Sorting](sorting.md) — merge sort and quicksort derivation; TimSort
- [Searching](searching.md) — binary search as D&C; median of two sorted arrays
- [Dynamic Programming](dynamic-programming/README.md) — overlapping vs independent subproblems
- [Patterns Master](../../../reference/patterns/patterns-master.md) — D&C pattern recognition triggers
