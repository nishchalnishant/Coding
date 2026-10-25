---
module: striver-a2z/14-arrays
lesson: 20
topic: Set Matrix Zeroes
difficulty: Medium
source: https://takeuforward.org/learning/dsa/set-matrix-zeroes?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, matrix, in-place, markers]
---
# 20. Set Matrix Zeroes

← [Rotate Matrix by 90 Degrees](19-rotate-matrix.md) · [Part 14 index](README.md) · Next → [Two Sum](21-two-sum.md)

> [!abstract] Problem at a glance
> **Task:** If any cell is 0, set its entire row and column to 0, in place.
> **Key insight:** Use the first row and first column as the marker arrays. Column 0's own marker needs a separate flag (`col0`), because `mat[0][0]` can only hold one of row 0 and column 0. Fill the inner cells first, then row 0, then column 0.
> **Difficulty:** Medium · **Pattern:** Matrix: in-place markers · **Also on:** [LC 73](https://leetcode.com/problems/set-matrix-zeroes/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/set-matrix-zeroes?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Row and column marker arrays](#3-row-and-column-marker-arrays) · [4. First row/column as markers](#4-first-rowcolumn-as-markers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `m × n` integer matrix, if an element is `0`, set its entire row and column to `0`. Do it in place.

| Input | Output | Why |
|---|---|---|
| `[[1,1,1],[1,0,1],[1,1,1]]` | `[[1,0,1],[0,0,0],[1,0,1]]` |  |
| `[[0,1,2,0],[3,4,5,2],[1,3,1,5]]` | `[[0,0,0,0],[0,4,5,0],[0,3,1,0]]` |  |

**Constraints:** `1 ≤ m, n ≤ 200`, `−2³¹ ≤ mat[i][j] ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Row and column marker arrays | row[i], col[j] flags; second pass zeroes | O(m · n) | O(m + n) |
| First row/column as markers | mat[i][0], mat[0][j] are the flags; col0 for column 0 | O(m · n) | O(1) |

> [!tip] Interview angle
> State the three tiers (O(mn) copy → O(m + n) markers → O(1)) and their trade-off before coding the O(1) one. The order of the final fill is the part to say out loud.

---

## 3. Row and column marker arrays

**Intuition.** Pass 1 records which rows and columns contain a zero. Pass 2 zeroes `mat[i][j]` if `row[i] or col[j]`. Recording first and writing later prevents new zeros from spreading.

```python
def set_zeroes_flags(mat):
    m, n = len(mat), len(mat[0])
    row, col = [False] * m, [False] * n
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                row[i] = col[j] = True
    for i in range(m):
        for j in range(n):
            if row[i] or col[j]:
                mat[i][j] = 0
```

**Complexity:** time **O(m · n)**, space **O(m + n)**.

---

## 4. First row/column as markers

**Intuition.** Store `row[i]` in `mat[i][0]` and `col[j]` in `mat[0][j]`. The cell `mat[0][0]` would be both `row[0]` and `col[0]`, so let it mean `row[0]` and keep `col0` as a separate variable.

**Algorithm**

1. Mark: for every zero at `(i, j)`: `mat[i][0] = 0`; if `j > 0`, `mat[0][j] = 0`, else `col0 = 0`.
2. Fill inner cells `i ≥ 1, j ≥ 1`: zero if `mat[i][0] == 0 or mat[0][j] == 0`.
3. If `mat[0][0] == 0`, zero row 0 (for `j ≥ 1`).
4. If `col0 == 0`, zero column 0.

**C++**
```cpp
void setZeroes(vector<vector<int>>& mat) {
    int m = mat.size(), n = mat[0].size(), col0 = 1;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (mat[i][j] == 0) {
                mat[i][0] = 0;
                if (j > 0) mat[0][j] = 0; else col0 = 0;
            }
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            if (mat[i][0] == 0 || mat[0][j] == 0) mat[i][j] = 0;
    if (mat[0][0] == 0)
        for (int j = 0; j < n; j++) mat[0][j] = 0;
    if (col0 == 0)
        for (int i = 0; i < m; i++) mat[i][0] = 0;
}
```

**Java**
```java
static void setZeroes(int[][] mat) {
    int m = mat.length, n = mat[0].length, col0 = 1;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (mat[i][j] == 0) {
                mat[i][0] = 0;
                if (j > 0) mat[0][j] = 0; else col0 = 0;
            }
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            if (mat[i][0] == 0 || mat[0][j] == 0) mat[i][j] = 0;
    if (mat[0][0] == 0)
        for (int j = 0; j < n; j++) mat[0][j] = 0;
    if (col0 == 0)
        for (int i = 0; i < m; i++) mat[i][0] = 0;
}
```

**Python**
```python
def set_zeroes(mat):
    m, n, col0 = len(mat), len(mat[0]), 1
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                mat[i][0] = 0
                if j > 0:
                    mat[0][j] = 0
                else:
                    col0 = 0
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][0] == 0 or mat[0][j] == 0:
                mat[i][j] = 0
    if mat[0][0] == 0:
        for j in range(n):
            mat[0][j] = 0
    if col0 == 0:
        for i in range(m):
            mat[i][0] = 0
```

**Complexity:** time **O(m · n)**, space **O(1)** — the markers live in row 0 and column 0, so those are overwritten last. Otherwise they'd be cleared before they're read.

---

## Edge cases

- Zero in row 0 or column 0 only.
- Zero at (0, 0).
- 1 × n, m × 1.
- No zeros.

---

## Common mistakes

1. Zeroing while scanning → zeros cascade over the whole matrix.
2. Using `mat[0][0]` for both row 0 and column 0.
3. Filling row 0 / column 0 before the inner cells, which erases the markers.
4. Marking with a sentinel like −1: invalid when −1 is a legal value.

---

## Follow-ups

1. Game of Life (LC 289): update in place from neighbour states.
2. Sparse huge matrix, list of zero coordinates given.

<details><summary>Answer sketches</summary>

**#1:** Encode the old and new state in the same cell (e.g. bit 0 = old, bit 1 = new).

**#2:** Collect the row and column sets, then zero only those rows and columns.
</details>

---

## Flashcards

**Set matrix zeroes O(1): where are the markers?** #flashcard
Row 0 and column 0; plus a col0 flag.

**Set matrix zeroes: fill order?** #flashcard
Inner cells, then row 0 (if mat[0][0] == 0), then column 0 (if col0 == 0).

**Why not zero during the scan?** #flashcard
New zeros would trigger more zeroing.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
