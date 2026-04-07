# Divide and Conquer

An algorithmic paradigm that breaks a problem into smaller, independent subproblems of the same type, solves them recursively, and then combines their solutions.

## The Three Steps
1. **Divide**: Break the problem into smaller subproblems.
2. **Conquer**: Solve the subproblems recursively. If they are small enough, solve them directly (base case).
3. **Combine**: Merge the results of the subproblems to form the final solution.

## Key Algorithms

SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/sorting.py` (quickselect) and `../../google-sde2/snippets/python/maths.py` (fast pow).

- **Merge Sort**: Divide array in half, sort each half, merge sorted halves. $O(N \log N)$ time, $O(N)$ space.
- **Quick Sort**: Pick a pivot, partition array into $\le$ pivot and $>$ pivot, then sort both parts. Average $O(N \log N)$ time, $O(\log N)$ space.
- **Binary Search**: Divide search space in half based on comparison. $O(\log N)$ time.
- **Strassen's Matrix Multiplication**: Optimized way to multiply matrices.

## Divide & Conquer vs Dynamic Programming
- **Divide & Conquer**: Subproblems are *independent* and do not overlap (e.g., sorting left half and right half of an array).
- **Dynamic Programming**: Subproblems *overlap*. DP stores the results to avoid re-computing them.

## Common SDE-3 Problems
- *Easy*: Merge Two Sorted Lists (building block), Majority Element (can be done with D&C).
- *Medium*: Sort List, Kth Largest Element in an Array (QuickSelect), Search a 2D Matrix II.
- *Hard*: Merge k Sorted Lists, Median of Two Sorted Arrays, Count of Smaller Numbers After Self, Reverse Pairs.

---

## Pattern Recognition

- **Split in half** → Merge sort, binary search, "divide and combine" (e.g. max subarray crossing mid).
- **Master Theorem**: T(n) = aT(n/b) + f(n). Case 1: f(n) = O(n^(log_b a - ε)) → T(n) = Θ(n^(log_b a)). Case 2: f(n) = Θ(n^(log_b a)) → T(n) = Θ(n^(log_b a) log n). Case 3: f(n) = Ω(n^(log_b a + ε)) and regularity → T(n) = Θ(f(n)).
- **D&C vs DP**: Subproblems independent (no overlap) → D&C. Overlapping → DP with memo/table.

## Interview Strategy

- **Identify**: "Independent subproblems", "split and combine" → D&C. If same subproblem repeated → mention DP.
- **Approach**: Define base case, split (e.g. left/right half), conquer (recurse), combine (merge or aggregate). State recurrence and solve with Master Theorem if applicable.
- **Common mistakes**: Wrong base case; combine step O(N) forgotten in recurrence; applying Master Theorem when a or b is not constant.

## Quick Revision

- **Merge sort**: T(n) = 2T(n/2) + Θ(n) → Θ(n log n). **Quick sort**: T(n) = T(k) + T(n-k-1) + Θ(n); average k ≈ n/2 → Θ(n log n).
- **Binary search**: T(n) = T(n/2) + Θ(1) → Θ(log n). **Majority**: Split; majority of array = majority of left or right half (then verify in O(n)).

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **Merge Sort** | Divide at `mid`, recursively sort, **merge** two sorted runs with two pointers O(n). | **O(n)** extra array; **stable**; **linked list** can merge in O(1) space for list nodes. **Bottom-up** iterative merges. |
| **Quick Sort** | **Partition** around pivot (Lomuto/Hoare); recurse on left/right. **QuickSelect** recurses only side containing k. | **Pivot** random/median-of-three avoids O(n²) on sorted input; **3-way partition** (Dutch flag) for many duplicates. |
| **Majority Element** | **Boyer–Moore:** candidate + count; cancel pairs; second pass **verify** count > n/2. | Works only if **strict majority** > ⌊n/2⌋; **D&C:** majority of whole is majority of a half or doesn’t exist—then verify. |
| **Count Inversions** | **Merge sort** augmentation: when taking from **right** before left, add `len(left_remaining)` to inversion count. | Use **64-bit** count; **merge** step is where cross inversions counted. |
| **Maximum Subarray (divide & conquer)** | Max in left, right, or **crossing** through mid—combine O(n) per level. | **Kadane** O(n) usually preferred; D&C shows recurrence thinking. |
| **Closest Pair of Points** | Sort by x; divide; min distance in strips by y-sorted **strip** scan O(n) per level. | **Strip** only points within δ of midline; **6-point** packing argument. |
| **Median of Two Sorted Arrays** | See binary search partition in [searching](searching.md)—often classified as D&C + BS. | **O(log(min(m,n)))** goal. |
| **Pow(x, n)** | Divide: `x^n = (x^(n/2))²` for even n; odd `x * x^(n-1)`. | **Negative** n; **MIN_INT** overflow when negate. |

---

## See also

- [Sorting](sorting.md) — merge and quick sort  
- [Searching](searching.md) — binary search  
- [Dynamic Programming](dynamic-programming/README.md) — overlapping vs independent subproblems
