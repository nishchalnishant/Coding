---
module: striver-a2z/16-binary-search
lesson: 32
topic: Find Peak Element II
difficulty: Hard
source: https://takeuforward.org/learning/dsa/find-peak-element-ii?category=2d-arrays&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, matrix]
---
# 32. Find Peak Element II

← [Search in 2D Matrix II](31-search-in-2d-matrix-ii.md) · [Part 16 index](README.md) · Next → [Matrix Median](33-matrix-median.md)

> [!abstract] Problem at a glance
> **Task:** Return `[r, c]` of any cell strictly greater than its 4 neighbours (border treated as −1).
> **Key insight:** Binary search **columns**. In column `mid`, take the row `r` of its maximum. That cell beats its up/down neighbours. If the left neighbour is bigger, a peak exists in the left half; if the right is bigger, in the right half; else it's a peak. O(n log m).
> **Difficulty:** Hard · **Pattern:** Binary search on columns + column max · **Also on:** [LC 1901](https://leetcode.com/problems/find-a-peak-element-ii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-peak-element-ii?category=2d-arrays&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Global maximum](#3-global-maximum) · [4. Binary search on columns](#4-binary-search-on-columns) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `n × m` matrix with no two adjacent cells equal, find any peak — a cell strictly greater than all its adjacent (up, down, left, right) neighbours, with the outside treated as −1. Return `[row, col]`. Target O(n log m) or O(m log n).

| Input | Output | Why |
|---|---|---|
| `[[1,4],[3,2]]` | `[0,1] or [1,0]` |  |
| `[[1,2,3],[4,5,6],[7,8,9]]` | `[2,2]` |  |

**Constraints:** `1 ≤ n, m ≤ 500`, `1 ≤ values ≤ 10⁵`, adjacent cells differ.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Global maximum | the largest cell is always a peak | O(n · m) | O(1) |
| Binary search on columns | r = argmax column mid; compare with left/right | O(n log m) | O(1) |

> [!tip] Interview angle
> Build on 1D peak: "if I collapse each column to its maximum, I get a 1D array; the 1D slope argument then applies, and the column max already beats its vertical neighbours."

---

## 3. Global maximum

**Intuition.** Simple and correct: nothing around the global max can be larger.

```python
def peak_grid_brute(mat):
    best = [0, 0]
    for i, row in enumerate(mat):
        for j, v in enumerate(row):
            if v > mat[best[0]][best[1]]:
                best = [i, j]
    return best
```

**Complexity:** time **O(n · m)**, space **O(1)**.

---

## 4. Binary search on columns

**Intuition.** Same invariant as 1D: the range `[lo, hi]` of columns always contains a peak. Moving toward the larger horizontal neighbour keeps that true, because the column-max chain only increases in that direction.

**Dry run** — `[[1 2 3] [4 5 6] [7 8 9]]`: lo 0 hi 2 mid 1 → col max 8 at row 2, right 9 bigger → lo 2; mid 2 → 9 at row 2, left 8 → peak [2, 2].

**C++**
```cpp
vector<int> findPeakGrid(vector<vector<int>>& mat) {
    int n = mat.size(), m = mat[0].size(), lo = 0, hi = m - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, r = 0;
        for (int i = 1; i < n; i++) if (mat[i][mid] > mat[r][mid]) r = i;
        int left = mid > 0 ? mat[r][mid - 1] : -1;
        int right = mid + 1 < m ? mat[r][mid + 1] : -1;
        if (mat[r][mid] > left && mat[r][mid] > right) return {r, mid};
        if (left > mat[r][mid]) hi = mid - 1;
        else lo = mid + 1;
    }
    return {-1, -1};
}
```

**Java**
```java
static int[] findPeakGrid(int[][] mat) {
    int n = mat.length, m = mat[0].length, lo = 0, hi = m - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, r = 0;
        for (int i = 1; i < n; i++) if (mat[i][mid] > mat[r][mid]) r = i;
        int left = mid > 0 ? mat[r][mid - 1] : -1;
        int right = mid + 1 < m ? mat[r][mid + 1] : -1;
        if (mat[r][mid] > left && mat[r][mid] > right) return new int[]{r, mid};
        if (left > mat[r][mid]) hi = mid - 1;
        else lo = mid + 1;
    }
    return new int[]{-1, -1};
}
```

**Python**
```python
def find_peak_grid(mat):
    n, m = len(mat), len(mat[0])
    lo, hi = 0, m - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        r = max(range(n), key=lambda i: mat[i][mid])
        left = mat[r][mid - 1] if mid > 0 else -1
        right = mat[r][mid + 1] if mid + 1 < m else -1
        if mat[r][mid] > left and mat[r][mid] > right:
            return [r, mid]
        if left > mat[r][mid]:
            hi = mid - 1
        else:
            lo = mid + 1
    return [-1, -1]
```

**Complexity:** time **O(n log m)**, space **O(1)** — log m columns probed, O(n) each.

---

## Edge cases

- Single row → 1D peak.
- Single column → column max.

---

## Common mistakes

1. Picking any cell in column mid instead of the column max — vertical neighbours may be larger.
2. Searching rows *and* columns at once.

---

## Follow-ups

1. O(n + m) algorithm.
2. Search rows instead.

<details><summary>Answer sketches</summary>

**#1:** Exists (window-splitting), rarely expected.

**#2:** Symmetric: O(m log n). Pick the smaller dimension to scan.
</details>

---

## Flashcards

**2D peak — what do you binary search?** #flashcard
Columns; in column mid take the max row.

**2D peak complexity?** #flashcard
O(n log m).

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
