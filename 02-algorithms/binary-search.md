## First-Principles Map

```text
WHY Binary Search exists
├── Linear scan is O(n) — unacceptable on sorted data at scale
│   ├── Each comparison on sorted data eliminates half the space
│   └── Reduces O(n) search to O(log n) by exploiting monotonicity
WHAT it is
├── Iterative halving of a sorted search space
│   ├── Maintains invariant: answer always in [lo, hi]
│   └── Terminates when lo > hi or exact match found
HOW it works
├── mid = lo + (hi - lo) // 2  (avoids overflow)
│   ├── If target == arr[mid] → found
│   ├── If target < arr[mid]  → hi = mid - 1
│   └── If target > arr[mid]  → lo = mid + 1
WHEN to use
├── "find X in sorted array" → classic binary search O(log n)
├── "minimum X satisfying condition" → binary search on answer space
└── "rotated sorted array / bitonic" → modified binary search
WHAT can go wrong
├── Off-by-one: lo = mid vs lo = mid+1 → infinite loop
├── Integer overflow: (lo + hi) / 2 on large indices
└── Applying to unsorted data → incorrect results silently
DECISION
└── Data is sorted OR answer space is monotone → binary search; unsorted small array → linear scan
```

## First-Principles Breakdown

- **Root problem**: Locate a value (or boundary) in a large ordered space without scanning every element.
- **Core insight**: A monotone predicate on a sorted space lets every comparison eliminate half the remaining candidates.
- **Invariant**: The answer always lies within [lo, hi]; the loop shrinks this interval by at least 1 each iteration.
- **Why it works**: Each step halves the interval → at most ⌈log₂ n⌉ steps → O(log n) time, O(1) space.
- **Where it breaks**: Non-monotone predicates or unsorted data — the halving step may discard the answer.

---

# Binary Search

```
[BINARY SEARCH — MINDMAP]
├── WHY IT EXISTS
│   ├── Problem class it solves: finding a target or boundary in sorted / monotonic search spaces
│   └── Intuition / real-world analogy: dictionary lookup — open to middle, discard irrelevant half, repeat
├── WHAT IT IS (First Principles)
│   ├── Core invariant: after every iteration, the answer lies within [lo, hi]; the invariant is never violated
│   └── Mathematical basis: halving the interval each step → T(n) = T(n/2) + O(1) → O(log n) by Master Theorem
├── HOW IT WORKS
│   ├── Step 1: define lo = 0, hi = n-1 (or problem-specific bounds)
│   ├── Step 2: compute mid = lo + (hi - lo) // 2  (avoids integer overflow)
│   ├── Step 3: evaluate predicate f(mid) → if satisfied, record answer and move boundary; else move other boundary
│   ├── Step 4: repeat until lo > hi (or lo == hi for boundary search)
│   └── Key condition/guard: choose lo=mid or hi=mid carefully based on whether you seek lower/upper bound
├── COMPLEXITY
│   ├── Time: O(log n)  Why: search space halves each iteration → log₂(n) iterations max
│   └── Space: O(1) iterative | O(log n) recursive call stack
├── WHEN TO USE (trigger patterns)
│   ├── Trigger 1: "sorted array + find target/index" → classic binary search
│   ├── Trigger 2: "minimize/maximize X subject to a monotonic constraint" → binary search on answer
│   ├── Trigger 3: "first/last occurrence", "leftmost/rightmost position" → lower/upper bound variant
│   ├── Trigger 4: "rotated sorted array" → find pivot then binary search in correct half
│   └── Trigger 5: "feasibility check is O(n), need overall O(n log n)" → binary search on answer space
└── COMMON MISTAKES
    ├── Mistake 1: mid = (lo + hi) / 2 → integer overflow for large values; use lo + (hi-lo)//2
    ├── Mistake 2: off-by-one on loop termination (< vs <=) causing infinite loop or missed element
    ├── Mistake 3: not anchoring the invariant — being unclear about what [lo,hi] represents at each step
    └── Mistake 4: applying binary search to non-monotonic predicate → incorrect results
```

## The Mental Model

Binary search eliminates half the search space each step by asking: **"Is the answer in the left half or right half?"**

**Key decision:** What are `lo` and `hi` representing?
- **Invariant:** The answer always lies in `[lo, hi]` (inclusive).
- **Termination:** When `lo > hi`, the space is exhausted.
- **Off-by-one source:** Whether you use `lo <= hi` or `lo < hi`, and whether you set `lo = mid+1` or `lo = mid`.

---

## Variant 1: Standard Binary Search (Exact Value + Bounds)

### Find exact value
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:          # loop while search space is non-empty
        mid = lo + (hi - lo) // 2   # avoid overflow (relevant in Java/C++)
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1                # not found
```

### Find leftmost (first occurrence / lower bound)
```python
def lower_bound(arr, target):
    """First index where arr[i] >= target."""
    lo, hi = 0, len(arr)   # hi = len(arr) — answer can be one past end
    while lo < hi:          # lo < hi (not <=) — hi is exclusive sentinel
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid        # keep mid as candidate
    return lo               # lo == hi == answer
```

### Find rightmost (last occurrence / upper bound)
```python
def upper_bound(arr, target):
    """First index where arr[i] > target."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo  # subtract 1 for last occurrence of target
```

**When to use `lo <= hi` vs `lo < hi`:**
- `lo <= hi` with `hi = len-1`: for exact-match search, returns -1 if not found.
- `lo < hi` with `hi = len`: for finding insertion point / boundary. Terminates with `lo == hi` pointing to answer.

---

## Variant 2: Rotated Sorted Array

**Key insight:** One half is always sorted. Determine which half, check if target is in it, recurse on that half.

```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid

        # Left half is sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1    # target in sorted left half
            else:
                lo = mid + 1    # target in right half
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1    # target in sorted right half
            else:
                hi = mid - 1    # target in left half

    return -1
```

**With duplicates (LC 81):** When `nums[lo] == nums[mid] == nums[hi]`, can't determine sorted half — do `lo += 1; hi -= 1`. Worst case degrades to O(n).

**Find minimum in rotated array:**
```python
def find_min_rotated(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1    # min is in right half
        else:
            hi = mid        # mid could be the min
    return nums[lo]
```

---

## Variant 3: Binary Search on Answer

**Use when:** Asked to minimize the maximum, maximize the minimum, or "can we achieve X with Y resources?" → binary search on the answer value, validate with a greedy check.

**Template:**
```python
def binary_search_on_answer(lo, hi, feasible_fn):
    """
    Minimize the answer: find smallest x in [lo, hi] where feasible(x) is True.
    Assumption: feasible is monotone — once True, stays True for all larger x.
    """
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible_fn(mid):
            hi = mid        # mid could be answer; search left
        else:
            lo = mid + 1   # mid too small
    return lo

def binary_search_maximize(lo, hi, feasible_fn):
    """
    Maximize the answer: find largest x where feasible(x) is True.
    """
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2  # upper-mid to avoid infinite loop
        if feasible_fn(mid):
            lo = mid        # mid is feasible; search right
        else:
            hi = mid - 1
    return lo
```

**Koko Eating Bananas (minimize max speed):**
```python
def min_eating_speed(piles, h):
    def feasible(speed):
        return sum(-(-p // speed) for p in piles) <= h  # ceiling division

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Split Array Largest Sum (minimize the maximum sum):**
```python
def split_array(nums, k):
    def feasible(max_sum):
        count, curr = 1, 0
        for n in nums:
            if curr + n > max_sum:
                count += 1
                curr = 0
            curr += n
        return count <= k

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

---

## 2D Binary Search (Sorted Matrix)

**LC 74 — each row sorted, first element of next row > last of prev row:**
```python
def search_matrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        val = matrix[mid // n][mid % n]   # convert 1D index to 2D
        if val == target: return True
        elif val < target: lo = mid + 1
        else: hi = mid - 1
    return False
```

**LC 240 — each row and column sorted (not flattened):**
```python
def search_matrix_ii(matrix, target):
    row, col = 0, len(matrix[0]) - 1   # start top-right
    while row < len(matrix) and col >= 0:
        if matrix[row][col] == target: return True
        elif matrix[row][col] > target: col -= 1  # too big, go left
        else: row += 1                             # too small, go down
    return False
```

---

## Off-By-One Mental Model

| Goal | `lo` init | `hi` init | Loop condition | On `arr[mid] < target` | On `arr[mid] >= target` | Answer |
|------|-----------|-----------|----------------|----------------------|------------------------|--------|
| Exact match | 0 | n-1 | `lo <= hi` | `lo = mid+1` | `hi = mid-1` | `mid` or `-1` |
| Lower bound | 0 | n | `lo < hi` | `lo = mid+1` | `hi = mid` | `lo` |
| Upper bound | 0 | n | `lo < hi` | `lo = mid+1` (≤) | `hi = mid` | `lo` |
| Minimize answer | feasible lo | feasible hi | `lo < hi` | `lo = mid+1` | `hi = mid` | `lo` |
| Maximize answer | feasible lo | feasible hi | `lo < hi` | `lo = mid` (upper mid) | `hi = mid-1` | `lo` |

**Upper-mid trick:** When you do `lo = mid`, use `mid = lo + (hi - lo + 1) // 2` to avoid infinite loop when `hi = lo + 1`.

---

## Canonical Problems

| Problem | Variant | Boundary Setup | Pitfall |
|---------|---------|---------------|---------|
| Binary Search (LC 704) | Standard exact | `lo=0, hi=n-1` | `lo <= hi`, return -1 at end |
| First Bad Version | Lower bound | `lo=1, hi=n` | Use `lo < hi`; set `hi=mid` not `hi=mid-1` |
| Search in Rotated Array (LC 33) | Rotated | Check which half is sorted | The `nums[lo] <= nums[mid]` check (= handles lo==mid) |
| Find Min in Rotated Array (LC 153) | Rotated | `lo=0, hi=n-1`; compare `nums[mid]` with `nums[hi]` | Don't compare with `nums[lo]` — wrong invariant |
| Koko Eating Bananas (LC 875) | BS on answer | `lo=1, hi=max(piles)` | Ceiling division: `math.ceil(p/s)` or `-((-p)//s)` |
| Split Array Largest Sum (LC 410) | BS on answer | `lo=max(nums), hi=sum(nums)` | feasible check: count splits, compare to k |
| Search 2D Matrix (LC 74) | 2D flattened | Treat as 1D array of size m*n | Row/col conversion: `mid//n`, `mid%n` |
| Search 2D Matrix II (LC 240) | Staircase | Start top-right corner | Not binary search — it's O(m+n) staircase |
| Find Peak Element (LC 162) | Bound search | `lo=0, hi=n-1`; if `nums[mid]<nums[mid+1]` go right | Always guaranteed a peak exists — invariant holds |
| Median of Two Sorted Arrays (LC 4) | Partition | Binary search on smaller array's partition | Boundary: left max ≤ right min on both sides |

---

## Edge Cases

- **Empty array:** Check `if not arr: return -1` before entering loop.
- **Single element:** Works correctly with both `lo <= hi` templates.
- **All same values:** Exact match finds one instance. Lower/upper bound still work correctly.
- **Overflow:** In Python, integers don't overflow. In Java/C++: `mid = lo + (hi - lo) / 2`.
- **Target not in array:** Standard template returns -1. Lower bound returns insertion point.
- **Rotated with duplicates:** Worst case O(n) when can't determine sorted half.
- **BS on answer — set boundaries tightly:** Wrong `lo`/`hi` init causes TLE or wrong answer. Think: what is the minimum possible answer? What is the maximum?
