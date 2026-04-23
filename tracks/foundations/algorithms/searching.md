# Searching & Binary Search — SDE-3 Gold Standard

Find an element or the optimal value satisfying a predicate. SDE-3 focus: **binary search on answer** (predicate function), rotated arrays, lower/upper bound semantics, and knowing which template to use for each variant.

---

## 1. Binary Search Template Reference

> [!IMPORTANT]
> **The Click Moment**: "**Sorted** or **monotonic** data" — OR — "**minimize the maximum**" — OR — "**maximize the minimum**" — OR — "**feasibility**: can we achieve value X?". When you can define a monotone predicate `valid(mid)` → binary search on the answer.

Two correct templates — pick one and never mix them:

```python
# Template 1: lo <= hi — finds exact element
def binary_search_exact(arr: list[int], target: int) -> int:
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2  # avoids overflow in other languages
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# Template 2: lo < hi — finds boundary (first True in a monotone predicate)
def binary_search_boundary(lo: int, hi: int, predicate) -> int:
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if predicate(mid):
            hi = mid      # mid might be the answer; don't exclude it
        else:
            lo = mid + 1  # mid is definitely not the answer
    return lo  # lo == hi at convergence
```

> [!CAUTION]
> The two templates have different loop conditions and termination. **Never mix them**: `lo <= hi` with `hi = mid` creates an infinite loop; `lo < hi` with `return mid` on match exits too early. Choose one template per problem and commit to it.

---

## 2. Core Algorithms & Click Moments

### Lower Bound / Upper Bound

> [!IMPORTANT]
> **The Click Moment**: "First **position** where element **≥ target**" (lower bound) — OR — "last position where element **≤ target**" (upper bound) — OR — "**first/last occurrence**" of a value. These are the building blocks of all binary-search-on-index problems.

```python
def lower_bound(arr: list[int], target: int) -> int:
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid  # mid >= target; might be answer
    return lo  # first index where arr[lo] >= target; == len(arr) if all < target

def upper_bound(arr: list[int], target: int) -> int:
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo  # first index where arr[lo] > target

def search_range(arr: list[int], target: int) -> list[int]:
    left = lower_bound(arr, target)
    if left == len(arr) or arr[left] != target:
        return [-1, -1]
    right = upper_bound(arr, target) - 1
    return [left, right]
```

> [!TIP]
> Python's `bisect` module implements these directly: `bisect_left` = lower bound, `bisect_right` = upper bound. In interviews, use them and explain what they do — or implement from scratch if asked.

---

### Binary Search on Answer — Predicate Pattern

> [!IMPORTANT]
> **The Click Moment**: "**Minimize the maximum**" — OR — "**maximize the minimum**" — OR — "what is the **minimum X** such that we can [achieve Y]?" — OR — "**how many** X can we fit given constraint Y?". Convert optimization to feasibility: `valid(mid)` = "can we achieve result ≤ mid?" Then binary search for the minimum `mid` where `valid` is true.

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    import math
    def can_finish(speed: int) -> bool:
        return sum(math.ceil(p / speed) for p in piles) <= h

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_finish(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def split_array_largest_sum(nums: list[int], k: int) -> int:
    def can_split(max_sum: int) -> bool:
        parts, cur = 1, 0
        for x in nums:
            if x > max_sum:
                return False
            if cur + x > max_sum:
                parts += 1
                cur = x
            else:
                cur += x
        return parts <= k

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_split(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

> [!TIP]
> **Range for binary search on answer**: `lo = minimum possible answer` (often `max(nums)` or `1`), `hi = maximum possible answer` (often `sum(nums)` or `max(nums)`). The predicate must be monotone: if `valid(mid)` is true, then `valid(mid+1)` must also be true (for minimization). Always verify monotonicity before applying.

---

### Rotated Sorted Array

> [!IMPORTANT]
> **The Click Moment**: "Search in a **rotated** sorted array" — OR — "find the **minimum** in a rotated array". One half of `[lo, hi]` is always sorted — use this to determine which side to search. Compare `nums[mid]` with `nums[lo]` and `nums[hi]` to identify the sorted half.

```python
def search_rotated(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

def find_min_rotated(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1  # minimum is in right half
        else:
            hi = mid       # mid might be the minimum
    return nums[lo]
```

> [!CAUTION]
> **Duplicates break the O(log N) guarantee**: If `nums[lo] == nums[mid] == nums[hi]`, you can't determine which half is sorted. The only safe move is `lo += 1; hi -= 1` (shrink both ends), which degrades to O(N) worst case. Always ask the interviewer if duplicates are possible in rotated array problems.

---

### Peak Element

> [!IMPORTANT]
> **The Click Moment**: "Find any **peak** element" — OR — "element greater than its neighbors" with no particular value target. Move toward the higher neighbor — a peak must exist in that direction (treat array boundaries as `-∞`).

```python
def find_peak_element(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[mid + 1]:
            hi = mid   # peak is at mid or to the left
        else:
            lo = mid + 1  # peak is strictly to the right
    return lo
```

---

### Median of Two Sorted Arrays

> [!IMPORTANT]
> **The Click Moment**: "Median of **two sorted arrays** in O(log(min(m,n)))" — this is one of the hardest binary search problems. Partition both arrays such that `len(left_half) == len(right_half) ± 1` and `max(left_half) <= min(right_half)`.

```python
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    A, B = nums1, nums2
    if len(A) > len(B):
        A, B = B, A  # binary search on smaller array
    m, n = len(A), len(B)
    lo, hi = 0, m
    while lo <= hi:
        i = lo + (hi - lo) // 2  # partition index in A
        j = (m + n + 1) // 2 - i  # partition index in B
        max_left_A = A[i-1] if i > 0 else float('-inf')
        min_right_A = A[i] if i < m else float('inf')
        max_left_B = B[j-1] if j > 0 else float('-inf')
        min_right_B = B[j] if j < n else float('inf')
        if max_left_A <= min_right_B and max_left_B <= min_right_A:
            if (m + n) % 2 == 1:
                return float(max(max_left_A, max_left_B))
            return (max(max_left_A, max_left_B) + min(min_right_A, min_right_B)) / 2.0
        elif max_left_A > min_right_B:
            hi = i - 1
        else:
            lo = i + 1
    raise ValueError("Input arrays are not sorted")
```

---

## 3. SDE-3 Deep Dives

### Scalability: Parallel Binary Search

> [!TIP]
> When you have Q offline queries, each requiring binary search over the same sorted answer space, **parallel binary search** reduces the total number of predicate evaluations from `O(Q log N)` to `O(N log Q)` (or similar, depending on the predicate).
>
> Technique: maintain a `[lo, hi]` interval per query. In each round, compute the `mid` for all queries; run the predicate for all `mid` values in one pass; update `[lo, hi]` for each query. `O(log N)` rounds, each processing all Q queries together.
>
> Used in competitive programming for counting inversions, offline range queries, and monotone predicate problems at scale.

### Scalability: External Binary Search

> [!TIP]
> Binary search over **sorted files on disk**: each comparison reads one page (O(1) I/O). For a file of N records with B records per page: `O(log(N/B))` I/O operations total — the basis of B-tree search. A B-tree of height h with branching factor b = page size / key size achieves O(h) = O(log_b(N)) I/O reads.

### Concurrency: Lock-Free Binary Search

> [!TIP]
> Binary search on a **static sorted array** is trivially parallelizable — reads are lock-free with no coordination needed (each thread searches independently). For concurrent inserts into a sorted structure, use a concurrent skip list or B-tree with fine-grained locking. Java's `ConcurrentSkipListMap` achieves lock-free O(log N) reads and writes.

### Trade-offs: Binary Search Variants

| Variant | Template | Loop Condition | Returns |
| :--- | :--- | :--- | :--- |
| Exact match | `lo <= hi` | `lo <= hi` | `mid` or -1 |
| Lower bound (first ≥ target) | `lo < hi` | `lo < hi` | `lo` |
| Upper bound (first > target) | `lo < hi` | `lo < hi` | `lo` |
| Binary search on answer (minimize) | `lo < hi` | `lo < hi` | `lo` |
| Binary search on answer (maximize) | `lo < hi` | `lo < hi` | `lo` (after adjusting predicate) |

---

## 4. Common Interview Problems

### Easy
- **Binary Search** — Classic exact match; `lo <= hi` template.
- **First Bad Version** — Binary search on answer; first True in `[False...True]`.
- **Guess Number Higher or Lower** — Same as exact match.

### Medium
- **Find First and Last Position** — Lower bound + upper bound.
- [Search in Rotated Sorted Array](../../google-sde2/PROBLEM_DETAILS.md#search-in-rotated-sorted-array) — Identify sorted half; recurse.
- [Find Minimum in Rotated Array](../../google-sde2/PROBLEM_DETAILS.md#find-minimum-in-rotated-sorted-array) — Compare `mid` to `hi`.
- **Koko Eating Bananas** — BS on answer `[1, max(piles)]`; predicate = can finish in H hours.
- **Capacity to Ship Packages** — BS on answer; predicate = can fit in D days.
- **Find Peak Element** — Compare with right neighbor; move toward higher side.
- **Search a 2D Matrix** — Treat as flattened 1D array; `row = mid // n, col = mid % n`.
- **Random Pick with Weight** — Prefix sums + binary search on random float.

### Hard
- [Split Array Largest Sum](../../google-sde2/PROBLEM_DETAILS.md#split-array-largest-sum) — BS on answer; predicate = can split into ≤ k parts with max ≤ mid.
- [Median of Two Sorted Arrays](../../google-sde2/PROBLEM_DETAILS.md#median-of-two-sorted-arrays) — Binary search on partition; O(log(min(m,n))).
- **Minimize Max Distance to Gas Station** — BS on answer (floating point); predicate = can place stations.
- **Aggressive Cows (or Magnetism)** — Maximize minimum distance; predicate = can place k cows.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **Classic Binary Search** | "Find element in sorted array" | `lo <= hi`; shrink left or right | `mid = lo + (hi-lo)//2` avoids overflow in C++/Java; Python int is arbitrary size. |
| **First / Last Position** | "Range of target in sorted array" | Lower bound + upper bound | Lower bound returns first ≥; subtract 1 for last occurrence. Handle "not found" case. |
| **[Search Rotated Array](../../google-sde2/PROBLEM_DETAILS.md#search-in-rotated-sorted-array)** | "Binary search in rotated sorted" | Identify sorted half via `nums[lo] <= nums[mid]` | Duplicates → `nums[lo]==nums[mid]==nums[hi]` forces O(N) — clarify with interviewer. |
| **[Find Min Rotated](../../google-sde2/PROBLEM_DETAILS.md#find-minimum-in-rotated-sorted-array)** | "Minimum in rotated sorted array" | `nums[mid] > nums[hi]` → min in right half | No duplicates simplifies; with duplicates: `hi -= 1` when equal. |
| **Koko Eating Bananas** | "Minimum speed to finish in H hours" | BS on `[1, max(piles)]`; `ceil(p/k)` hours per pile | `math.ceil(p/k)` or `(p + k - 1) // k`; integer overflow on sum in other languages. |
| **[Split Array Largest Sum](../../google-sde2/PROBLEM_DETAILS.md#split-array-largest-sum)** | "Minimize maximum subarray sum" | BS on `[max(A), sum(A)]`; greedy feasibility check | Single element > `max_sum` → infeasible; handle in predicate. |
| **[Median of Two Arrays](../../google-sde2/PROBLEM_DETAILS.md#median-of-two-sorted-arrays)** | "Median without merging, O(log N)" | Partition both arrays; `max(left) <= min(right)` | Sentinel `-inf`/`+inf` for empty partitions; even vs odd total length changes formula. |
| **Find Peak Element** | "Any peak (greater than neighbors)" | Move toward larger neighbor | Multiple peaks: any valid answer; boundaries are treated as `-inf`. |
| **Random Pick by Weight** | "Weighted random selection" | Prefix sums + `bisect_left` on random float | Inclusive vs exclusive random range; prefix sum must be exclusive (start from 0). |
| **Aggressive Cows** | "Maximize minimum distance between k cows" | BS on answer; predicate = can place k with min distance ≥ mid | Classic "maximize minimum" — predicate is greedy: greedily place cows starting from leftmost. |

---

## See also

- [Array](../data-structures/array.md) — sorted array prerequisites; binary search on rotated arrays
- [Sorting](sorting.md) — ordering required for binary search on index
- [Dynamic Programming](dynamic-programming/README.md) — some BS-on-answer problems reduce to DP feasibility checks
- [Patterns Master](../../../reference/patterns/patterns-master.md) — binary search pattern triggers
