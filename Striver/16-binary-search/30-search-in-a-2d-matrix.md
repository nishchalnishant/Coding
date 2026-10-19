---
module: striver/16-binary-search
lesson: 30
topic: Search in a 2D Matrix
difficulty: Medium
source: https://takeuforward.org/learning/dsa/search-in-a-2d-matrix?category=2d-arrays&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, matrix]
---
# 30. Search in a 2D Matrix

← [Find Row with Maximum 1's](29-row-with-maximum-ones.md) · [Part 16 index](README.md) · Next → [Search in 2D Matrix II](31-search-in-2d-matrix-ii.md)

> [!abstract] Problem at a glance
> **Task:** Each row sorted, and each row's first element > previous row's last. Return whether `target` exists.
> **Key insight:** The matrix is one sorted array of length `n·m` laid out row by row. Binary search index `i ∈ [0, nm − 1]` and read `mat[i / m][i % m]`.
> **Difficulty:** Medium · **Pattern:** Binary search on flattened index · **Also on:** [LC 74](https://leetcode.com/problems/search-a-2d-matrix/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/search-in-a-2d-matrix?category=2d-arrays&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Pick the row, then search it](#3-pick-the-row-then-search-it) · [4. Flattened binary search](#4-flattened-binary-search) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `n × m` integer matrix where every row is sorted ascending and the first integer of each row is greater than the last integer of the previous row, return `true` if `target` is in the matrix. Must be O(log(n·m)).

| Input | Output | Why |
|---|---|---|
| `[[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3` | `true` |  |
| `same matrix, target = 13` | `false` |  |

**Constraints:** `1 ≤ n, m ≤ 100`, `|values| ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Pick the row, then search it | binary search last row with first ≤ target, then search that row | O(log n + log m) | O(1) |
| Flattened binary search | idx → (idx / m, idx % m) | O(log(n · m)) | O(1) |

---

## 3. Pick the row, then search it

**Intuition.** Two binary searches. Same complexity as the flattened version; slightly more code.

```python
def search_matrix_two(mat, target):
    lo, hi, r = 0, len(mat) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if mat[mid][0] <= target:
            r, lo = mid, mid + 1
        else:
            hi = mid - 1
    if r == -1:
        return False
    row = mat[r]
    lo, hi = 0, len(row) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if row[mid] == target:
            return True
        if row[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

**Complexity:** time **O(log n + log m)**, space **O(1)**.

---

## 4. Flattened binary search

**Intuition.** Treat it as a virtual 1D array. No copying.

**Dry run** — target 3, n 3 m 4: lo 0 hi 11 mid 5 → (1,1) = 11 > 3 hi 4; mid 2 → (0,2) = 5 > 3 hi 1; mid 0 → 1 < 3 lo 1; mid 1 → 3 ✓.

**C++**
```cpp
bool searchMatrix(vector<vector<int>>& mat, int target) {
    int n = mat.size(), m = mat[0].size(), lo = 0, hi = n * m - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, v = mat[mid / m][mid % m];
        if (v == target) return true;
        if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}
```

**Java**
```java
static boolean searchMatrix(int[][] mat, int target) {
    int n = mat.length, m = mat[0].length, lo = 0, hi = n * m - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, v = mat[mid / m][mid % m];
        if (v == target) return true;
        if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}
```

**Python**
```python
def search_matrix(mat, target):
    n, m = len(mat), len(mat[0])
    lo, hi = 0, n * m - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = mat[mid // m][mid % m]
        if v == target:
            return True
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

**Complexity:** time **O(log(n · m))**, space **O(1)** — log of the total cell count.

---

## Edge cases

- Single row or column.
- Target smaller than everything / larger than everything.

---

## Common mistakes

1. `mid / n` instead of `mid / m` (divide by column count).
2. Applying this to LC 240 matrices — their rows don't chain.

---

## Follow-ups

1. Only rows and columns sorted (LC 240).
2. n · m overflows int.

<details><summary>Answer sketches</summary>

**#1:** Next problem — staircase search.

**#2:** Use 64-bit indices.
</details>

---

## Flashcards

**Flattened index → cell?** #flashcard
(i / m, i % m), m = columns.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
