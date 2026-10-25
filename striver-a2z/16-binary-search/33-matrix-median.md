---
module: striver-a2z/16-binary-search
lesson: 33
topic: Matrix Median
difficulty: Hard
source: https://takeuforward.org/learning/dsa/matrix-median?category=2d-arrays&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, matrix]
---
# 33. Matrix Median

← [Find Peak Element II](32-find-peak-element-ii.md) · [Part 16 index](README.md) · Next → [Part 17: Strings (Basic and Medium)](../17-strings-basic-medium/README.md)

> [!abstract] Problem at a glance
> **Task:** Each row of an `n × m` matrix (n·m odd) is sorted. Return the median of all elements.
> **Key insight:** Binary search on the **value** `x ∈ [min, max]`. `count(≤ x)` = Σ `upper_bound(row, x)`, monotone in `x`. The median is the smallest `x` with count > nm/2.
> **Difficulty:** Hard · **Pattern:** Binary search on value + counting
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/matrix-median?category=2d-arrays&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Flatten and sort](#3-flatten-and-sort) · [4. Binary search on value](#4-binary-search-on-value) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `n × m` matrix with each row sorted ascending and `n · m` odd, return the median of all its elements without flattening and sorting.

| Input | Output | Why |
|---|---|---|
| `[[1,3,5],[2,6,9],[3,6,9]]` | `5` | 1 2 3 3 5 6 6 9 9 |
| `[[1,3,8],[2,3,4],[1,2,5]]` | `3` |  |

**Constraints:** `1 ≤ n, m ≤ 500`, `1 ≤ values ≤ 10⁹`, n·m odd.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Flatten and sort | collect, sort, middle | O(nm log nm) | O(nm) |
| Binary search on value | first x with Σ upper_bound(row, x) > nm/2 | O(n log m · log(max − min)) | O(1) |

> [!tip] Interview angle
> "Binary search on value + count" is the trick behind k-th smallest in a sorted matrix (LC 378), k-th smallest pair distance (LC 719) and median of k arrays. The median is the `(nm/2 + 1)`-th smallest.

---

## 3. Flatten and sort

**Intuition.** Ignores row ordering.

```python
def matrix_median_brute(mat):
    a = sorted(x for row in mat for x in row)
    return a[len(a) // 2]
```

**Complexity:** time **O(nm log nm)**, space **O(nm)**.

---

## 4. Binary search on value

**Intuition.** The min is among first columns, the max among last columns. For each candidate `x`, count elements ≤ x with one `upper_bound` per row. Search the first `x` whose count exceeds `nm / 2`; that `x` always exists in the matrix (the count only jumps at real values).

**Dry run** — `[[1 3 5] [2 6 9] [3 6 9]]`, need > 4: lo 1 hi 9 mid 5 → 3 + 1 + 1 = 5 ✓ hi 4; mid 2 → 1 + 1 + 0 = 2 ✗ lo 3; mid 3 → 2 + 1 + 1 = 4 ✗ lo 4; mid 4 → 4 ✗ lo 5 → 5.

**C++**
```cpp
int findMedian(vector<vector<int>>& mat) {
    int n = mat.size(), m = mat[0].size(), lo = INT_MAX, hi = INT_MIN;
    for (auto& row : mat) { lo = min(lo, row[0]); hi = max(hi, row[m - 1]); }
    int need = n * m / 2;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, cnt = 0;
        for (auto& row : mat) cnt += upper_bound(row.begin(), row.end(), mid) - row.begin();
        if (cnt <= need) lo = mid + 1;
        else hi = mid - 1;
    }
    return lo;
}
```

**Java**
```java
static int upperBound(int[] row, int x) {
    int lo = 0, hi = row.length;
    while (lo < hi) {
        int mid = (lo + hi) >>> 1;
        if (row[mid] <= x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
static int findMedian(int[][] mat) {
    int n = mat.length, m = mat[0].length, lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;
    for (int[] row : mat) { lo = Math.min(lo, row[0]); hi = Math.max(hi, row[m - 1]); }
    int need = n * m / 2;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, cnt = 0;
        for (int[] row : mat) cnt += upperBound(row, mid);
        if (cnt <= need) lo = mid + 1;
        else hi = mid - 1;
    }
    return lo;
}
```

**Python**
```python
from bisect import bisect_right

def matrix_median(mat):
    lo = min(row[0] for row in mat)
    hi = max(row[-1] for row in mat)
    need = len(mat) * len(mat[0]) // 2
    while lo <= hi:
        mid = (lo + hi) // 2
        cnt = sum(bisect_right(row, mid) for row in mat)
        if cnt <= need:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo
```

**Complexity:** time **O(n log m · log(max − min))**, space **O(1)** — log(range) values × n rows × log m per upper_bound.

---

## Edge cases

- Single cell.
- All equal values.
- Single row / column.

---

## Common mistakes

1. `lower_bound` instead of `upper_bound` (counts < x, not ≤ x).
2. Condition `cnt < need` — off by one; median needs count > nm/2.
3. Assuming columns are sorted.

---

## Follow-ups

1. k-th smallest in row+column sorted matrix (LC 378).
2. Even n·m.

<details><summary>Answer sketches</summary>

**#1:** Same value search; count with the O(n + m) staircase.

**#2:** Average the (nm/2)-th and (nm/2 + 1)-th — two searches.
</details>

---

## Flashcards

**Matrix median — search over?** #flashcard
Values [min, max]; count ≤ x via upper_bound per row.

**Matrix median — stop condition?** #flashcard
Smallest x with count(≤ x) > nm/2.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
