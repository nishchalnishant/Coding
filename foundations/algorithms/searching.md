# Searching & Binary Search — SDE-3 Level

Techniques to find an element or the best value satisfying a condition. SDE-3 focus: binary search on index, binary search on answer (predicate), rotated arrays, and when to use which variant.

---

## 1. Concept Overview

**Problem space**: Sorted array lookup, lower/upper bound, rotated sorted array, search on answer (minimize max, maximize min), peak element, search in 2D matrix.

**When to use**: Sorted or monotonic → binary search on index. "Minimum possible maximum" / "maximum possible minimum" → binary search on answer with predicate.

---

## 2. Core Algorithms

### Standard Binary Search (Index)
- `lo`, `hi`; `mid = lo + (hi - lo) // 2`; compare with target; shrink to `[lo, mid-1]` or `[mid+1, hi]`. Loop `while lo <= hi`. Return mid or -1.
- **Lower bound**: First index i such that A[i] >= target. If A[mid] < target → lo = mid+1; else hi = mid (keep mid). Return lo.
- **Upper bound**: First index i such that A[i] > target. Return first index after last occurrence.

### Binary Search on Answer
- Identify range [low, high] of possible answers.
- Define predicate `valid(mid)` that is true for mid and (depending on problem) all larger or all smaller.
- Binary search so that we find min value where valid is true (or max where valid is false). Typical: minimize maximum → valid(mid) = "can we achieve max ≤ mid"; search for smallest mid where valid(mid).

### Rotated Sorted Array
- One half of [lo, hi] is always sorted. Compare target with A[mid] and with A[lo]/A[hi] to decide which half to search. Duplicates can force O(N) (e.g., A[lo]==A[mid]==A[hi]).

---

## 3. Advanced Variations

- **Peak element**: Binary search on index; compare A[mid] with A[mid+1]; if rising, peak in right half else left.
- **Search in 2D (row-sorted, first of row ≤ last of next)**: Flatten to 1D index: row = idx//n, col = idx%n; standard BS.
- **Median of two sorted arrays**: Binary search on partition in smaller array; balance left sizes and compare max_left ≤ min_right.
- **Aggressive cows / Split array largest sum**: Classic "minimize maximum" → binary search on answer; predicate: can we place with given limit.

### Edge Cases
- Empty array; single element; two elements; target smaller than min or larger than max; duplicates (lower/upper bound); rotated with duplicates (cannot do log N in worst case).

---

## 4. Common Interview Problems

**Easy**: Binary Search, First Bad Version, Guess Number.  
**Medium**: Search in Rotated Sorted Array, Find First and Last Position, Koko Eating Bananas (BS on answer).  
**Hard**: Median of Two Sorted Arrays, Split Array Largest Sum, Aggressive Cows.

---

## 5. Pattern Recognition (Binary Search Patterns)

- **Search on index**: Sorted array; lower/upper bound; first/last occurrence.
- **Search on answer**: "Minimize the maximum" / "maximize the minimum" → range [min_possible, max_possible], predicate, find boundary.
- **Rotated array**: One half always sorted; compare target with mid and ends to go left/right.
- **Peak / bitonic**: Compare mid with neighbors; move toward larger neighbor.
- **2D matrix**: Treat as 1D (row-major) if "sorted when flattened"; or binary search row then column.

---

## 6. Code Implementations

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

def binary_search_on_answer(candidates, predicate):
    lo, hi = min(candidates), max(candidates)
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

---

## 7. SDE-3 Level Thinking

- **Trade-offs**: Linear scan O(N) vs binary search O(log N) when data is sorted. BS on answer converts "optimization" to "feasibility" (predicate) — often simpler to reason.
- **Scalability**: Logarithmic passes; predicate should be O(N) or O(1) per call so total is O(N log range) or O(log N).

---

## 8. Interview Strategy

- **Identify**: "Sorted" / "monotonic" → BS on index. "Minimize max" / "maximize min" → BS on answer.
- **Approach**: State range, define predicate clearly, then implement loop (avoid off-by-one: use lo < hi vs lo <= hi and what to return).
- **Common mistakes**: Integer overflow in mid (use lo + (hi-lo)//2); forgetting to handle empty; rotated array with duplicates.

---

## 9. Quick Revision

- **Formulas**: mid = lo + (hi-lo)//2. Lower bound: first >= target; upper bound: first > target.
- **Tricks**: Predicate for "can we achieve X?"; smallest valid → hi = mid; largest valid → lo = mid (with appropriate loop).
- **Edge cases**: Empty; single element; target not in range; duplicates.
- **Pattern tip**: "Minimum maximum" → binary search on answer + greedy predicate.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness |
|----------|------------|------------|
| **Binary Search (sorted)** | `lo, hi`, `mid`, shrink half | `lo<=hi` vs `lo<hi`; return `lo` or `hi` |
| **First/Last Position** | Lower bound / upper bound templates | Duplicates: first `>=` vs last `<=` |
| **Rotated Sorted Array** | Find sorted half; check if target in range | Duplicates at ends → worst O(n) |
| **Koko / BS on answer** | `valid(mid)` greedy check; minimize `mid` | Ceil division `(p+k-1)//k` |
| **Median Two Sorted** | BS partition on smaller array; balance left/right | `i+j = m+n+1/2`; edge empty array |
| **Peak Element** | `mid` vs `mid+1` climb toward peak | Boundaries 0 and n-1 |

---

## See also

- [Array](../data-structures/array.md) — rotated array search patterns  
- [Sorting](sorting.md) — ordering prerequisite for binary search on index  
- [Graph](graph.md) — not directly related; BS on answer is cross-topic
