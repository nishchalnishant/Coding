# Searching & Binary Search — SDE-3 Gold Standard

Find an element or the optimal value satisfying a predicate. SDE-3 focus: **binary search on answer** (predicate function), rotated arrays, lower/upper bound semantics, and knowing which template to use for each variant.

---

## Theory & Mental Models

**What it is.** Binary search is a divide-and-conquer strategy on a sorted (or monotonic) search space — eliminate half the candidates each iteration. Core invariant: the search space `[lo, hi]` always contains the answer, and every iteration strictly shrinks it. Terminates in O(log N) iterations.

**Why it exists.** Linear scan is O(N); binary search is O(log N). For N = 10^9 (feasibility check on a numeric range), binary search completes in ~30 iterations. The power insight: binary search applies to any monotonic predicate, not just sorted arrays — "binary search on the answer".

**The mental model.** Open a dictionary to the middle page. If your word comes before the middle word, close the right half and repeat on the left. The key is that the "answer" is always in the surviving half — never discard a range without being certain the answer isn't there.

**Complexity at a glance.**

| Variant | Time | Space |
| :--- | :--- | :--- |
| Exact match in sorted array | O(log N) | O(1) |
| Lower / upper bound | O(log N) | O(1) |
| Binary search on answer (predicate) | O(log(range) × predicate_cost) | O(1) |
| Rotated array search | O(log N) | O(1) |
| Median of two sorted arrays | O(log(min(m, n))) | O(1) |

**When to reach for it.**
- Sorted array lookup or first/last occurrence.
- Rotated sorted arrays — one half is always sorted.
- "Minimize the maximum" or "maximize the minimum" — convert to feasibility check.
- Feasibility check on a numeric range: "is speed k sufficient to finish in H hours?"
- Any monotone predicate over integers or floats.

**When NOT to use it.**
- Array is unsorted and sorting is too expensive — use a hash map or linear scan.
- Frequent insertions/deletions into a sorted structure — use a balanced BST or sorted list.
- The predicate is not monotone — binary search gives wrong results silently.

**Common mistakes.**
- Infinite loop from wrong mid rounding: always use `lo + (hi - lo) // 2`, and use `hi = mid` (not `hi = mid - 1`) with the `lo < hi` template.
- Mixing templates: `lo <= hi` with `hi = mid` loops forever; `lo < hi` with early return on exact match exits too soon.
- Off-by-one in `lo`/`hi` initialization — boundary problems fail on single-element arrays.
- Not verifying predicate monotonicity before applying — a non-monotone predicate breaks the algorithm.

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

#### Common Variants & Twists
1. **Find K-th Smallest Pair Distance**:
   - **What (The Problem & Goal):** Given an array, find the k-th smallest absolute difference between any two elements.
   - **How (Intuition & Mental Model):** The range of possible distances is `[0, max(nums) - min(nums)]`. Binary search on the distance `d`. For each `mid`, count how many pairs have distance `<= mid` using two pointers in O(N).
2. **K-th Smallest Element in a Sorted Matrix**:
   - **What (The Problem & Goal):** Find the k-th smallest element in an `n x n` matrix where each row and column is sorted in ascending order.
   - **How (Intuition & Mental Model):** The range of values is `[matrix[0][0], matrix[n-1][n-1]]`. Binary search on the value. For each `mid`, count how many elements are `<= mid` using a staircase traversal (starting from top-right) in O(N).
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

#### Common Variants & Twists
1. **Search Insert Position**:
   - **What (The Problem & Goal):** Find the index where a target would be inserted in a sorted array to maintain order.
   - **How (Intuition & Mental Model):** This is exactly the `lower_bound` problem. The first position where `arr[mid] >= target`.
2. **H-Index II**:
   - **What (The Problem & Goal):** Given a sorted array of citations, find the researcher's h-index.
   - **How (Intuition & Mental Model):** The h-index is the largest `h` such that `h` papers have at least `h` citations. Since citations are sorted, at index `i`, there are `n - i` papers with at least `citations[i]` citations. We need the first `i` where `citations[i] >= n - i`.
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

def aggressive_cows(stalls: list[int], cows: int) -> int:
    stalls.sort()
    
    def can_place(min_dist: int) -> bool:
        placed = 1
        last_pos = stalls[0]
        for i in range(1, len(stalls)):
            if stalls[i] - last_pos >= min_dist:
                placed += 1
                last_pos = stalls[i]
        return placed >= cows

    lo, hi = 1, stalls[-1] - stalls[0]
    while lo < hi:
        # Crucial: +1 prevents infinite loop when lo and hi are adjacent
        mid = lo + (hi - lo + 1) // 2  
        if can_place(mid):
            lo = mid      # mid is feasible, we want to MAXIMIZE it
        else:
            hi = mid - 1  # mid is NOT feasible, must be smaller
    return lo

#### Common Variants & Twists
1. **Minimum Speed to Arrive on Time**:
   - **What (The Problem & Goal):** Find the minimum integer speed `s` to reach destination in `hour` hours.
   - **How (Intuition & Mental Model):** The speed range is `[1, 10^7]`. The total time is `sum(ceil(dist[i]/s)) + dist[-1]/s`. Use binary search on speed.
2. **Minimize Maximum Distance to Gas Station (Float)**:
   - **What (The Problem & Goal):** Add `k` gas stations to minimize the maximum distance between adjacent stations.
   - **How (Intuition & Mental Model):** Binary search on the distance (a float). For a distance `d`, the number of stations needed between two existing stations at distance `D` is `floor(D/d)`. Sum these up and check if `<= k`. Use a fixed number of iterations (e.g., 100) or `while hi - lo > 1e-7`.
```

> [!CAUTION]
> **Maximize vs Minimize the Answer**: 
> - **Minimize** (`split_array_largest_sum`): If `valid(mid)` is true, try smaller. Use `hi = mid`, `lo = mid + 1`, and `mid = lo + (hi-lo)//2`.
> - **Maximize** (`aggressive_cows`): If `valid(mid)` is true, try larger. Use `lo = mid`, `hi = mid - 1`. **CRITICAL**: you must use `mid = lo + (hi - lo + 1) // 2`. Without the `+1`, if `lo=2, hi=3`, `mid` becomes `2`. If `valid(2)` is true, `lo=2`, creating an infinite loop.

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

#### Common Variants & Twists
1. **Search in Rotated Sorted Array II (with duplicates)**:
   - **What (The Problem & Goal):** Same as searching in rotated array, but duplicates are allowed.
   - **How (Intuition & Mental Model):** If `nums[lo] == nums[mid] == nums[hi]`, we cannot tell which side is sorted. Increment `lo` and decrement `hi` and continue. This makes the worst-case O(N).
2. **Find Minimum in Rotated Sorted Array II**:
   - **What (The Problem & Goal):** Find minimum in rotated array with duplicates.
   - **How (Intuition & Mental Model):** Similar logic. If `nums[mid] == nums[hi]`, just decrement `hi`.
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

#### Common Variants & Twists
1. **Find Peak Element in 2D Matrix**:
   - **What (The Problem & Goal):** Find a peak element in an `m x n` matrix (greater than its 4 neighbors).
   - **How (Intuition & Mental Model):** Binary search on columns. For the middle column, find the global maximum element at `(row, mid)`. Compare it with its neighbors at `(row, mid-1)` and `(row, mid+1)`. Move toward the higher neighbor.
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

#### Common Variants & Twists
1. **K-th Smallest Element of Two Sorted Arrays**:
   - **What (The Problem & Goal):** Find the k-th smallest element in the union of two sorted arrays.
   - **How (Intuition & Mental Model):** A generalization of the median problem. Partition `A` and `B` such that `i + j = k`. Use binary search to find the correct `i` such that `A[i-1] <= B[j]` and `B[j-1] <= A[i]`.
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
- [Search in Rotated Sorted Array](problem-deep-dives.md#search-in-rotated-sorted-array) — Identify sorted half; recurse.
- [Find Minimum in Rotated Array](problem-deep-dives.md#find-minimum-in-rotated-sorted-array) — Compare `mid` to `hi`.
- **Koko Eating Bananas** — BS on answer `[1, max(piles)]`; predicate = can finish in H hours.
- **Capacity to Ship Packages** — BS on answer; predicate = can fit in D days.
- **Find Peak Element** — Compare with right neighbor; move toward higher side.
- **Search a 2D Matrix** — Treat as flattened 1D array; `row = mid // n, col = mid % n`.
- **Random Pick with Weight** — Prefix sums + binary search on random float.

### Hard
- [Split Array Largest Sum](problem-deep-dives.md#split-array-largest-sum) — BS on answer; predicate = can split into ≤ k parts with max ≤ mid.
- [Median of Two Sorted Arrays](problem-deep-dives.md#median-of-two-sorted-arrays) — Binary search on partition; O(log(min(m,n))).
- **Minimize Max Distance to Gas Station** — BS on answer (floating point); predicate = can place stations.
- **Aggressive Cows (or Magnetism)** — Maximize minimum distance; predicate = can place k cows.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Classic Binary Search** | Binary Search (Exact Match) | "Find element in sorted array" | `lo <= hi`; shrink left or right | `mid = lo + (hi-lo)//2` avoids overflow in C++/Java; Python int is arbitrary size. |
| **First / Last Position** | "Range of target in sorted array" | Lower bound + upper bound | Lower bound returns first ≥; subtract 1 for last occurrence. Handle "not found" case. |
| **[Search Rotated Array](problem-deep-dives.md#search-in-rotated-sorted-array)** | "Binary search in rotated sorted" | Identify sorted half via `nums[lo] <= nums[mid]` | Duplicates → `nums[lo]==nums[mid]==nums[hi]` forces O(N) — clarify with interviewer. |
| **[Find Min Rotated](problem-deep-dives.md#find-minimum-in-rotated-sorted-array)** | "Minimum in rotated sorted array" | `nums[mid] > nums[hi]` → min in right half | No duplicates simplifies; with duplicates: `hi -= 1` when equal. |
| **Koko Eating Bananas** | "Minimum speed to finish in H hours" | BS on `[1, max(piles)]`; `ceil(p/k)` hours per pile | `math.ceil(p/k)` or `(p + k - 1) // k`; integer overflow on sum in other languages. |
| **[Split Array Largest Sum](problem-deep-dives.md#split-array-largest-sum)** | "Minimize maximum subarray sum" | BS on `[max(A), sum(A)]`; greedy feasibility check | Single element > `max_sum` → infeasible; handle in predicate. |
| **[Median of Two Arrays](problem-deep-dives.md#median-of-two-sorted-arrays)** | "Median without merging, O(log N)" | Partition both arrays; `max(left) <= min(right)` | Sentinel `-inf`/`+inf` for empty partitions; even vs odd total length changes formula. |
| **Find Peak Element** | "Any peak (greater than neighbors)" | Move toward larger neighbor | Multiple peaks: any valid answer; boundaries are treated as `-inf`. |
| **Random Pick by Weight** | "Weighted random selection" | Prefix sums + `bisect_left` on random float | Inclusive vs exclusive random range; prefix sum must be exclusive (start from 0). |
| **Aggressive Cows** | "Maximize minimum distance between k cows" | BS on answer; predicate = can place k with min distance ≥ mid | Classic "maximize minimum" — predicate is greedy: greedily place cows starting from leftmost. |
| **Guess Number Higher or Lower** [E] | "Binary search on number range" | `lo=1, hi=n`; call `guess(mid)`; adjust bounds on result | Template: `lo <= hi`; return `mid` on exact match. Canonical BS exercise. |
| **Sqrt(x)** [E] | "Integer square root without built-ins" | BS on `[0, x]`; find largest `mid` where `mid*mid <= x` | Use `lo < hi` template; `hi = mid` when `mid*mid > x`. Avoid overflow: `mid <= x // mid` instead of `mid*mid`. |
| **Count of Negative Numbers in Sorted Matrix** [E] | "Count negatives in row-wise and col-wise sorted matrix" | Start from top-right; move left on negative (count col+1), move down on non-negative | O(R+C) staircase traversal — faster than binary search per row when matrix is small. |
| **First Bad Version** [E] | "Find first True in monotone bool sequence" | `lo < hi` boundary template; `hi = mid` when `isBadVersion(mid)` | Don't call `isBadVersion(mid+1)` inside the loop — minimize API calls. |
| **Search in Rotated Sorted Array II** [M] | "Rotated array with duplicates; find target" | Duplicates degrade worst case to O(N): when `lo == mid == hi`, shrink bounds by 1 | Adds `lo += 1; hi -= 1` on ambiguous duplicate — key difference from no-duplicate version. |
| **Find Minimum in Rotated Sorted Array II** [M] | "With duplicates; find minimum" | When `nums[mid] == nums[hi]`, `hi -= 1`; otherwise standard rotation logic | Deduplication step prevents false confidence about which half is sorted. |
| **Time Based Key-Value Store** [M] | "Get largest timestamp ≤ query" | Map `key → sorted (timestamp, value)` list; `bisect_right` on timestamps | `bisect_right(times, t) - 1` gives the insertion point's predecessor — the largest ≤ t. |
| **Find Kth Missing Positive Number** [M] | "Binary search on missing count" | `missing count at index i = arr[i] - (i+1)`; BS for first index where missing ≥ k | After loop, `lo + k` is the answer — elements before `lo` are all present. |
| **Minimize Max Distance to Gas Station** [H] | "Add K stations to minimize max gap" | BS on answer (max gap); feasibility = `ceil((gap / D) - 1)` additional stations per interval | Float BS: `eps = 1e-6`; count `int(gaps[i] / D)` stations needed per segment. |
| **Count of Smaller Numbers After Self** [H] | "For each element, count elements to its right that are smaller" | Binary search into sorted suffix (built left-to-right via bisect); or BIT/merge sort | Merge sort approach gives O(N log N); bisect + insert gives O(N²) — know which to use. |
| **Koko Eating Bananas** [M] | "Min eating speed to finish all piles in H hours" | BS on speed `[1, max(piles)]`; feasibility = `sum(ceil(p/k)) <= H` | `ceil(p/k)` in integer arithmetic: `(p + k - 1) // k`. |

---

## Quick Revision Triggers

- "Find exact value in sorted array" → `lo≤hi` template; `mid = (lo+hi)//2`; shrink both sides on match.
- "Find leftmost / rightmost position satisfying a condition" → `lo<hi` boundary template; never return inside loop.
- "Answer is a value in a range and feasibility is monotone" → binary search on the answer space, not the array.
- "Sorted array rotated at unknown pivot" → binary search; determine which half is sorted before choosing direction.
- "Array is sorted but has duplicates; find boundary" → `lo<hi` template; use `mid+1` carefully to avoid infinite loop.
- "Peak element: find any element greater than its neighbors" → binary search; move toward the higher neighbor.
- "Two templates exist; never mix them" → `lo≤hi` returns inside loop (exact search); `lo<hi` returns `lo` after loop (boundary search).

---

## See also

- [Array](../ds/array.md) — sorted array prerequisites; binary search on rotated arrays
- [Sorting](sorting.md) — ordering required for binary search on index
- [Dynamic Programming](dynamic-programming/README.md) — some BS-on-answer problems reduce to DP feasibility checks
- [Patterns Master](../../../reference/patterns/patterns-master.md) — binary search pattern triggers
