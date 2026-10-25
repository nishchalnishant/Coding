---
module: striver-a2z/16-binary-search
lesson: 31
topic: Search in 2D Matrix II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/search-in-2d-matrix-ii?category=2d-arrays&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, matrix, two-pointers]
---
# 31. Search in 2D Matrix II

← [Search in a 2D Matrix](30-search-in-a-2d-matrix.md) · [Part 16 index](README.md) · Next → [Find Peak Element II](32-find-peak-element-ii.md)

> [!abstract] Problem at a glance
> **Task:** Rows sorted left→right, columns sorted top→bottom. Return whether `target` exists.
> **Key insight:** Start at the top-right. It's the largest in its row and smallest in its column, so one comparison eliminates a whole row (too small → down) or column (too big → left). O(n + m).
> **Difficulty:** Medium · **Pattern:** Staircase search · **Also on:** [LC 240](https://leetcode.com/problems/search-a-2d-matrix-ii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/search-in-2d-matrix-ii?category=2d-arrays&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Binary search each row](#3-binary-search-each-row) · [4. Staircase from top-right](#4-staircase-from-top-right) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `n × m` matrix where each row is sorted ascending and each column is sorted ascending, return `true` if `target` is present.

| Input | Output | Why |
|---|---|---|
| `5×5 sample matrix, target = 5` | `true` |  |
| `same matrix, target = 20` | `false` |  |

**Constraints:** `1 ≤ n, m ≤ 300`, `|values| ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Binary search each row | n binary searches | O(n log m) | O(1) |
| Staircase from top-right | v > target → col − 1; v < target → row + 1 | O(n + m) | O(1) |

> [!tip] Interview angle
> Interviewers often expect you to first try "binary search each row" (O(n log m)) and then find the staircase. Explain why top-left or bottom-right corners don't work: from there both moves go the same direction in value.

---

## 3. Binary search each row

**Intuition.** Uses row sortedness only.

```python
def search_matrix_rows(mat, target):
    for row in mat:
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

**Complexity:** time **O(n log m)**, space **O(1)**.

---

## 4. Staircase from top-right

**Intuition.** Each step discards one row or one column, so at most `n + m` steps. Bottom-left works symmetrically.

**Dry run** — target 5 in the sample: (0,4) 15 → left; 11 → left; 7 → left; 4 → down; (1,1) 5 ✓.

**C++**
```cpp
bool searchMatrixII(vector<vector<int>>& mat, int target) {
    int r = 0, c = mat[0].size() - 1;
    while (r < (int)mat.size() && c >= 0) {
        if (mat[r][c] == target) return true;
        if (mat[r][c] > target) c--;
        else r++;
    }
    return false;
}
```

**Java**
```java
static boolean searchMatrixII(int[][] mat, int target) {
    int r = 0, c = mat[0].length - 1;
    while (r < mat.length && c >= 0) {
        if (mat[r][c] == target) return true;
        if (mat[r][c] > target) c--;
        else r++;
    }
    return false;
}
```

**Python**
```python
def search_matrix_ii(mat, target):
    r, c = 0, len(mat[0]) - 1
    while r < len(mat) and c >= 0:
        if mat[r][c] == target:
            return True
        if mat[r][c] > target:
            c -= 1
        else:
            r += 1
    return False
```

**Complexity:** time **O(n + m)**, space **O(1)** — row index only increases, column only decreases.

---

## Edge cases

- Single row / column.
- Target at a corner.

---

## Common mistakes

1. Starting at top-left — both moves increase value.
2. Using the LC 74 flattened search here (rows don't chain).

---

## Follow-ups

1. Count elements ≤ x.
2. Divide and conquer.

<details><summary>Answer sketches</summary>

**#1:** Same staircase, accumulate counts per row: O(n + m) — used in k-th smallest in sorted matrix.

**#2:** Quad-split on the centre value — O(n^1.58), worse than staircase.
</details>

---

## Flashcards

**Row+column sorted search — start where?** #flashcard
Top-right (or bottom-left).

**Staircase complexity?** #flashcard
O(n + m).

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
