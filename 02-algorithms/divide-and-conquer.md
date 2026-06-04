---
module: 02-algorithms
topic: Divide And Conquer
subtopic: 
status: unread
tags: [algorithms, divide-and-conquer]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)
## First-Principles Map

```
WHY Divide & Conquer exists
├── Problems with overlapping or independent sub-structure grow too slow naively
│   ├── Sorting n items: brute O(n²) → D&C gives O(n log n)
│   ├── Multiplying n-digit numbers: schoolbook O(n²) → Karatsuba O(n^1.585)
│   └── Closest pair of points: brute O(n²) → D&C O(n log n)
│
WHAT it is
├── Algorithmic paradigm: recursively split → solve independently → merge
│   ├── Split: divide input into k ≥ 2 subproblems of size n/b
│   ├── Conquer: recurse until base case (size 1 or threshold)
│   └── Merge: combine subproblem solutions into full solution
│       └── Merge cost drives total complexity via Master Theorem
│
HOW it works
├── Recurrence: T(n) = aT(n/b) + f(n)
│   ├── a = number of subproblems, b = split factor, f(n) = merge cost
│   ├── Master Theorem cases:
│   │   ├── Case 1: f(n) = O(n^(log_b a - ε)) → T(n) = Θ(n^log_b a)   [subproblems dominate]
│   │   ├── Case 2: f(n) = Θ(n^log_b a)       → T(n) = Θ(n^log_b a · log n) [balanced]
│   │   └── Case 3: f(n) = Ω(n^(log_b a + ε)) → T(n) = Θ(f(n))        [merge dominates]
│   ├── Merge Sort:   a=2, b=2, f=O(n)   → T=O(n log n)  [Case 2]
│   ├── Binary Search: a=1, b=2, f=O(1)  → T=O(log n)    [Case 1]
│   ├── Karatsuba:    a=3, b=2, f=O(n)   → T=O(n^1.585)  [Case 1]
│   └── Strassen:     a=7, b=2, f=O(n²)  → T=O(n^2.807)  [Case 1]
├── Canonical algorithms:
│   ├── Merge Sort — split mid, sort halves, merge in O(n); stable, O(n log n)
│   ├── Quicksort — partition around pivot, recurse; O(n log n) avg, O(n²) worst
│   ├── Closest Pair — sort by x, split, recurse each half, strip merge in O(n)
│   └── Counting Inversions — augmented merge sort; count cross-half inversions during merge
│
WHEN to use
├── Input can be split into independent (not overlapping) halves/thirds
│   ├── Sorting, searching on sorted input → always consider D&C
│   ├── "Count pairs / triples with property" → augmented merge sort
│   ├── Big-integer / polynomial multiplication → Karatsuba / FFT
│   └── Geometric problems on point sets → closest pair, convex hull
├── NOT when subproblems overlap with shared state → use DP instead
│   └── Fibonacci via D&C = O(2^n); DP = O(n)
│
WHAT can go wrong
├── Wrong split: unbalanced split → O(n²) worst case (quicksort on sorted input)
├── Merge cost dominates: if merge is O(n²), total is O(n² log n) — worse than brute
├── Stack overflow: recursion depth O(log n) normally safe; O(n) depth → overflow
├── Off-by-one in mid: mid = lo + (hi - lo) / 2 NOT (lo + hi) / 2 (overflow)
├── Forgetting base case: infinite recursion when subproblem size doesn't shrink
└── Confusing with DP: D&C subproblems are disjoint; DP subproblems overlap

Decision tree
├── Does the problem split into non-overlapping halves? YES → D&C candidate
│   ├── Can I sort or search? → Merge sort / Binary search / Quickselect
│   ├── Count pairs with a property? → Augmented merge sort (inversions)
│   ├── Big number arithmetic? → Karatsuba
│   ├── Matrix multiply? → Strassen
│   └── Geometric (point distances)? → Closest pair D&C
└── Do subproblems overlap / share results? NO→ D&C, YES → DP
```

## First-Principles Breakdown

- **Root problem:** Naive algorithms scan all combinations; D&C exploits problem structure to prune redundant work by ensuring each element is processed O(log n) times instead of O(n) times.
- **Core insight:** If a problem of size n can be split into a subproblems of size n/b with O(f(n)) merge cost, the recursion tree has log_b n levels and total work telescopes to the Master Theorem bound.
- **Invariant:** At every recursive call, the subproblem is strictly smaller than the parent; merge produces a fully correct solution for the parent given correct child solutions — no global state is mutated between calls.
- **Why it's fast:** The split halves the problem size each level, so the recursion tree has only O(log n) depth; merge sort's O(n) merge across O(log n) levels yields O(n log n) total — each element participates in exactly one merge per level.
- **Where it breaks:** Unbalanced splits (pivot = min/max in quicksort) degrade depth to O(n), making total work O(n²); also fails when subproblems are not independent — if merging requires re-solving shared subproblems, DP is required instead.


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

# Divide and Conquer — SDE-3 Gold Standard

Break a problem into **independent subproblems**, solve recursively, and **combine** results. SDE-3 expects: Master Theorem application, recognizing D&C vs DP vs Greedy, and key augmentations (counting inversions, closest pair).

---

## Theory & Mental Models

**What it is.** Break a problem into smaller, independent subproblems of the same type, solve each recursively, then combine the results. Core invariant: subproblems are **independent** — solving the left half never depends on or changes the right half.

**Why it exists.** Many problems have a recursive self-similar structure that naturally halves the search space each level, giving O(log N) depth. The combine step often reveals global information invisible in either half alone (cross-midpoint maximum subarray, cross-half inversions).

**The mental model.** Military divide-and-conquer: split the enemy force, defeat each half independently, then unify. The reunion (combine) step may require coordination but each battle is self-contained.

**Complexity at a glance.**

| Algorithm | Recurrence | Result |
| :--- | :--- | :--- |
| Merge Sort | T(n) = 2T(n/2) + O(n) | O(N log N) — Master Theorem Case 2 |
| Binary Search | T(n) = T(n/2) + O(1) | O(log N) — Master Theorem Case 2 |
| QuickSelect (avg) | T(n) = T(n/2) + O(n) | O(N) average |
| Closest Pair of Points | T(n) = 2T(n/2) + O(n log n) | O(N log² N) |
| Fast Exponentiation | T(n) = T(n/2) + O(1) | O(log N) |

**When to reach for it.**
- Sorting (merge sort, quicksort) or Kth order statistic (quickselect).
- Counting inversions or pairs satisfying a cross-half condition.
- Binary search and its generalizations (rotated arrays, search on answer).
- Matrix exponentiation (Fibonacci in O(log N)).
- Closest pair of points, polynomial multiplication (FFT).

**When NOT to use it.**
- Subproblems overlap — use DP (memoization avoids recomputation).
- The combine step costs O(N²) — the recurrence degrades to O(N² log N).
- Subproblems are unequal and unbalanced — analyze with the recursion tree, not the Master Theorem.

**Common mistakes.**
- Forgetting the combine step's cost in the recurrence (must include merge cost to get O(N log N), not O(N)).
- Incorrect base case — must handle n = 0 and n = 1 separately.
- Off-by-one in midpoint: always use `mid = lo + (hi - lo) // 2` (avoids overflow in C/Java, correct in Python).
- Mutating shared state across the two recursive calls — each call must operate on its own slice.

---

## 1. The Three Steps

> [!IMPORTANT]
> **The Click Moment**: "**Split** into equal halves, solve each independently, **merge `🔥 Google`**" — OR — "recurrence T(n) = aT(n/b) + O(n^k)" — OR — "the combine step reveals global information not visible in either half" (e.g., cross-midpoint subarray, cross-half inversions). D&C is the choice when subproblems are **independent** (no overlap) and the combine step is tractable.

1. **Divide `⭐ Google`**: Break the problem at a natural boundary (midpoint, pivot, median).
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

#### Common Variants & Twists
1. **Count Smaller Numbers After Self**:
   - **What (The Problem & Goal):** For each element in an array, count how many numbers to its right are smaller than it.
   - **How (Intuition & Mental Model):** Use merge sort on an array of `(value, original_index)`. During the merge step, when you pull an element from the `right` half into the result, it means all remaining elements in the `left` half have "jumped over" this smaller right element. For each element in the `left` half, increment its "smaller after" count by the number of elements already taken from the `right` half.
2. **Reverse Pairs `⭐ Google`**:
   - **What (The Problem & Goal):** Count pairs `(i, j)` where `i < j` and `nums[i] > 2 * nums[j]`.
   - **How (Intuition & Mental Model):** Similar to counting inversions, but the condition is different. Before merging the two sorted halves, use two pointers to count the pairs: for each `i` in the left half, move the right pointer `j` as far as `nums[i] > 2 * nums[j]` holds. Add the count to the total, then proceed with the standard merge.
```

---

### QuickSelect — O(N) Kth Element

> [!IMPORTANT]
> **The Click Moment**: "**Kth largest/smallest `🔥 Google`** element without full sort" — OR — "find the **median** in O(N) average". QuickSelect uses the partition step of QuickSort but only recurses into the half containing the target rank.

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

#### Common Variants & Twists
1. **Top K Frequent Elements `🔥 Google`**:
   - **What (The Problem & Goal):** Find the `k` most frequent elements in an array.
   - **How (Intuition & Mental Model):** First, count frequencies using a hash map. Then, run QuickSelect on the unique elements based on their frequencies. Once the `(n-k)`-th smallest frequency position is found, all elements to its right are the top `k` most frequent.
2. **K Closest Points to Origin `🔥 Google`**:
   - **What (The Problem & Goal):** Given a list of points, find the `k` points closest to `(0,0)`.
   - **How (Intuition & Mental Model):** Calculate the squared Euclidean distance for each point. Use QuickSelect on the distances to find the `k`-th smallest distance. All points partitioned to the left of this pivot are your answer.
```

---

### Fast Exponentiation — O(log N)

> [!IMPORTANT]
> **The Click Moment**: "Compute **x^n** efficiently" — OR — "matrix exponentiation for **Fibonacci in O(log N) `🔥 Google`**" — OR — any problem that reduces to repeated squaring. Halving the exponent at each step gives O(log N).

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

#### Common Variants & Twists
1. **Matrix Exponentiation `⭐ Google`**:
   - **What (The Problem & Goal):** Compute the `n`-th term of a linear recurrence (like Fibonacci) in O(log N) time.
   - **How (Intuition & Mental Model):** Represent the recurrence as a matrix multiplication: `[F(n), F(n-1)] = [1, 1; 1, 0] * [F(n-1), F(n-2)]`. To find the `n`-th term, compute `M^n` using the fast power algorithm, then multiply by the base case vector.
2. **Super Pow**:
   - **What (The Problem & Goal):** Compute `a^b % 1337` where `b` is a very large positive integer represented as an array.
   - **How (Intuition & Mental Model):** Use the property `a^[1,2,3] = (a^[1,2])^10 * a^3`. Recurse through the array from right to left: `solve(a, b_array) = pow(solve(a, b_array[:-1]), 10) * pow(a, b_array[-1])`.
```

> [!CAUTION]
> **INT_MIN overflow in other languages**: Negating `n` when `n = INT_MIN` overflows in Java/C++ (INT_MIN = -2^31; its negation exceeds INT_MAX). Cast to `long` before negation. In Python, integers are arbitrary precision — not an issue.

---

### Maximum Subarray — Cross-Midpoint Combine

> [!IMPORTANT]
> **The Click Moment**: "Explain how **Kadane's `🔥 Google`** relates to D&C" — OR — when an interviewer asks for the D&C approach to maximum subarray (O(N log N)). The insight: the maximum subarray either lies entirely in the left half, entirely in the right half, or **crosses the midpoint**. Compute the cross-midpoint case in O(N) by expanding outward from mid.

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

#### Common Variants & Twists
1. **Max Subarray Sum in 2D (Matrix)**:
   - **What (The Problem & Goal):** Find the rectangular submatrix with the maximum sum.
   - **How (Intuition & Mental Model):** Reduce this to 1D by fixing the top and bottom row boundaries. Sum the columns between these rows into a 1D array. Run Kadane's (or D&C Max Subarray) on this 1D array. Repeat for all O(N^2) row pairs.
2. **Maximum Product Subarray `🔥 Google`**:
   - **What (The Problem & Goal):** Find the contiguous subarray with the maximum product.
   - **How (Intuition & Mental Model):** While usually DP (tracking `min` and `max` due to negatives), the D&C approach involves tracking four values from each half: `max_prod`, `min_prod`, and the products starting/ending at the boundaries. The cross-midpoint combine step is significantly more complex than the sum case.
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

#### Common Variants & Twists
1. **Closest Pair of Points in 3D**:
   - **What (The Problem & Goal):** Extend the 2D algorithm to 3D space.
   - **How (Intuition & Mental Model):** The D&C structure remains the same (divide by x, solve halves, check strip). However, the strip in 3D is a "slab" of width `2δ`, and the "check constant" increases from 7 to roughly 15-20 points based on 3D sphere packing.
2. **All Nearest Neighbors**:
   - **What (The Problem & Goal):** For every point in a set, find its nearest neighbor.
   - **How (Intuition & Mental Model):** While it can be solved with a KD-Tree, a D&C approach can solve this in O(N log N) by passing more information up the merge step.
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

**Concrete Example: Fibonacci vs Merge Sort**
- `fib(n) = fib(n-1) + fib(n-2)`: The call to `fib(n-1)` completely subsumes the work of `fib(n-2)`. The tree has massive overlap. Without DP memoization, this is O(2^N).
- `merge_sort(lo, hi)`: The left half `[lo, mid]` shares exactly **zero** elements with the right half `[mid+1, hi]`. There is no overlapping work to memoize. This is pure D&C and strictly O(N log N).

**Quick Test**: Draw the recursion tree. Do nodes across different branches receive the exact same arguments? If yes → DP. If no → D&C.

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
- **Merge Two Sorted Lists `🔥 Google`** — Building block for merge sort combine step.
- **Majority Element `⭐ Google`** — Boyer-Moore O(N) or D&C: majority of whole = majority of a half (then verify).
- **Pow(x, n) `🔥 Google`** — Fast exponentiation; handle `n < 0`.

### Medium
- **Sort List `⭐ Google`** — Merge sort on linked list; O(N log N) time, O(log N) stack.
- **Kth Largest Element `🔥 Google`** — QuickSelect; O(N) average.
- **Majority Element II `⭐ Google`** (n/3) — Boyer-Moore extended; two candidates.
- **Count of Range Sum `⭐ Google`** — Merge sort augmented; count cross-half pairs in range [lower, upper].

### Hard
- **[Merge K Sorted Lists](problem-deep-dives.md#merge-k-sorted-lists) `🔥 Google`** — D&C pairwise merge: O(N log K) time.
- **[Median of Two Sorted Arrays](problem-deep-dives.md#median-of-two-sorted-arrays) `🔥 Google`** — Binary search on partition; O(log(min(m,n))).
- **Count of Smaller Numbers After Self `⭐ Google`** — Merge sort augmented; count right-picks during merge.
- **Reverse Pairs `⭐ Google`** — Merge sort; count pairs `nums[i] > 2 × nums[j]` across halves.
- **Closest Pair of Points** — O(N log N) D&C; strip scanning.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Merge Sort** | Divide → Merge | "Stable sort, guaranteed O(N log N)" | Divide at mid; merge sorted halves | Combine step is O(N) — include in recurrence T(n)=2T(n/2)+O(n). |
| **Count Inversions** | "Pairs where i<j but nums[i]>nums[j]" | Merge sort; count right-picks during merge (`len(left)-i`) | Requires a copy of left array; in-place merge loses position info. |
| **QuickSelect** | "Kth largest in O(N) average" | Partition; recurse only into side with target | Mutates array; randomize pivot to avoid O(N²). Median-of-medians gives O(N) worst. |
| **Pow(x,n)** | "Fast exponentiation" | `x^n = (x^(n/2))²`; odd: multiply by x once | Negative n: `x = 1/x, n = -n`; INT_MIN overflow in Java/C++. |
| **Maximum Subarray (D&C) `🔥 Google`** | "Explain subarray beyond Kadane's" | Cross-midpoint expansion + max of three cases | O(N log N) — always mention Kadane is O(N) and preferred; D&C demonstrates recurrence thinking. |
| **[Majority Element](problem-deep-dives.md#majority-element) `⭐ Google`** | "Element appearing >n/2 times" | Boyer-Moore O(N)/O(1) or D&C — majority of whole must be majority of some half | D&C: majority of neither half → no majority. Must verify in O(N) second pass. |
| **Merge K Sorted Lists `🔥 Google`** | "Merge K into one sorted list" | D&C pairwise merge: merge pairs in O(N log K) | K-way heap is also O(N log K) — D&C has better cache locality. |
| **Reverse Pairs `⭐ Google`** | "Pairs where nums[i] > 2×nums[j], i<j" | Modified merge sort; count cross-half pairs | Different from standard inversions — inequality is strict and scaled. Use two pointers in combine. |
| **Closest Pair of Points** | "Min distance in 2D plane, O(N log N)" | D&C with strip of width 2δ; sort strip by y; check 7 candidates | 6-point packing argument ensures at most 7 comparisons per strip point. |
| **Majority Element [E] `⭐ Google`** | "Element appearing > n/2 times guaranteed to exist" | Boyer-Moore: candidate + count; or D&C — majority of whole must be majority of some half | D&C: if both halves agree → that's majority. If they differ → count each in full array. One scan for Boyer-Moore; two scans for D&C. |
| **Sort List [M] `⭐ Google`** | "Sort a linked list in O(N log N) time and O(log N) space" | Merge sort: slow/fast pointers to find mid; split; merge | Splitting at mid requires setting `slow.next = None`. Bottom-up merge sort avoids O(log N) recursion stack entirely. |
| **Beautiful Array [M]** | "Construct array where no A[k]*2 == A[i]+A[j] for i<k<j" | D&C: split into odd and even halves recursively; beautiful property is preserved | `1` is trivially beautiful. Odd positions preserve the property after transformation `2x-1`; even after `2x`. |
| **Different Ways to Add Parentheses [M]** | "All possible results from parenthesizing expression" | D&C on each operator: split left/right, combine all pairs of results | Memoize on `(lo, hi)` substring to avoid recomputing subexpressions. Return `[num]` for pure numeric substrings. |
| **Count of Range Sum [H] `⭐ Google`** | "Count subarrays with sum in [lower, upper]" | Prefix sums + modified merge sort; count pairs `(i,j)` where `lower <= prefix[j]-prefix[i] <= upper` | During merge: for each left element, slide two pointers on right to count valid window. Do NOT forget to merge after counting. |
| **Reverse Pairs [H] `⭐ Google`** | "Count pairs where nums[i] > 2*nums[j] for i < j" | Modified merge sort; count cross-half pairs before merging | Counting step and merge step are separate — count with two pointers first, then do the actual merge. Inequality `>2*` differs from standard inversions. |

---

## Quick Revision Triggers

- "Split the input in half, solve each half independently, merge results" → divide and conquer.
- "Count inversions / cross-half pairs while sorting" → merge sort variant with counting during merge.
- "Find median of two sorted arrays in O(log N)" → binary search on partition point (D&C on index).
- "Recurrence fits `T(n) = aT(n/b) + f(n)`" → apply Master Theorem to read off complexity immediately.
- "Closest pair of points in 2D" → D&C; strip merge in O(N); overall O(N log N).
- "Fast exponentiation: `a^n` in O(log n)" → `pow(a, n//2, mod)` squared, times `a` if n is odd.
- "Subproblems overlap (same arguments repeated)" → D&C becomes DP; add memoization.

---

## See also

- [Sorting](sorting.md) — merge sort and quicksort derivation; TimSort
- [Searching](searching.md) — binary search as D&C; median of two sorted arrays
- [Dynamic Programming](dynamic-programming/README.md) — overlapping vs independent subproblems
- [Patterns Master](../../03-patterns/patterns-master.md) — D&C pattern recognition triggers

## Flashcards

**"Split the input in half, solve each half independently, merge results" → divide and conquer.?** #flashcard
"Split the input in half, solve each half independently, merge results" → divide and conquer.

**"Count inversions / cross-half pairs while sorting" → merge sort variant with counting during merge.?** #flashcard
"Count inversions / cross-half pairs while sorting" → merge sort variant with counting during merge.

**"Find median of two sorted arrays in O(log N)" → binary search on partition point (D&C on index).?** #flashcard
"Find median of two sorted arrays in O(log N)" → binary search on partition point (D&C on index).

**"Recurrence fits `T(n) = aT(n/b) + f(n)`" → apply Master Theorem to read off complexity immediately.?** #flashcard
"Recurrence fits `T(n) = aT(n/b) + f(n)`" → apply Master Theorem to read off complexity immediately.

**"Closest pair of points in 2D" → D&C; strip merge in O(N); overall O(N log N).?** #flashcard
"Closest pair of points in 2D" → D&C; strip merge in O(N); overall O(N log N).

**"Fast exponentiation?** #flashcard
`a^n` in O(log n)" → `pow(a, n//2, mod)` squared, times `a` if n is odd.

**"Subproblems overlap (same arguments repeated)" → D&C becomes DP; add memoization.?** #flashcard
"Subproblems overlap (same arguments repeated)" → D&C becomes DP; add memoization.
