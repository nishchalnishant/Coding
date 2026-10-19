---
module: striver/14-arrays
lesson: 19
topic: Rotate Matrix by 90 Degrees
difficulty: Medium
source: https://takeuforward.org/learning/dsa/rotate-matrix-by-90-degrees?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, matrix, in-place, transpose]
---
# 19. Rotate Matrix by 90 Degrees

← [Pascal's Triangle III](18-pascals-triangle-iii.md) · [Part 14 index](README.md) · Next → [Set Matrix Zeroes](20-set-matrix-zeroes.md)

> [!abstract] Problem at a glance
> **Task:** Rotate an n × n matrix 90° clockwise, in place.
> **Key insight:** A clockwise rotation is a transpose (swap across the main diagonal) followed by reversing each row. Both steps are in place, and only the upper triangle is swapped during the transpose.
> **Difficulty:** Medium · **Pattern:** Matrix transforms · **Also on:** [LC 48](https://leetcode.com/problems/rotate-image/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/rotate-matrix-by-90-degrees?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. New matrix](#3-new-matrix) · [4. Transpose + reverse rows](#4-transpose--reverse-rows) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `n × n` integer matrix, rotate it by 90 degrees clockwise in place, without allocating another matrix.

| Input | Output | Why |
|---|---|---|
| `[[1,2,3],[4,5,6],[7,8,9]]` | `[[7,4,1],[8,5,2],[9,6,3]]` |  |
| `[[0,1],[2,3]]` | `[[2,0],[3,1]]` |  |

**Constraints:** `1 ≤ n ≤ 20`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| New matrix | ans[j][n − 1 − i] = mat[i][j] | O(n²) | O(n²) |
| Transpose + reverse rows | swap(m[i][j], m[j][i]) for j > i; reverse each row | O(n²) | O(1) |

---

## 3. New matrix

**Intuition.** Row `i` becomes column `n − 1 − i`. Fill a copy, then write it back. Simple, but it violates the in-place requirement.

```python
def rotate_copy(mat):
    n = len(mat)
    ans = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            ans[j][n - 1 - i] = mat[i][j]
    mat[:] = ans
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 4. Transpose + reverse rows

**Intuition.** After the transpose, `m[i][j]` holds the old `m[j][i]`. Reversing row `i` moves it to column `n − 1 − j`. Together: the old `m[j][i]` ends at `[i][n − 1 − j]`, which is exactly the clockwise mapping.

**Dry run** — `[[1 2 3][4 5 6][7 8 9]]` → transpose `[[1 4 7][2 5 8][3 6 9]]` → reverse rows `[[7 4 1][8 5 2][9 6 3]]`.

**Other rotations:** anticlockwise = transpose + reverse each **column** (or reverse rows first, then transpose). 180° = reverse rows + reverse each row. **Layer-by-layer 4-way swap** is the other O(1) method; it does each move in one step but is easier to get wrong.

**C++**
```cpp
void rotate(vector<vector<int>>& mat) {
    int n = mat.size();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) swap(mat[i][j], mat[j][i]);
    for (auto& row : mat) reverse(row.begin(), row.end());
}
```

**Java**
```java
static void rotate(int[][] mat) {
    int n = mat.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            int t = mat[i][j]; mat[i][j] = mat[j][i]; mat[j][i] = t;
        }
    for (int[] row : mat)
        for (int l = 0, r = n - 1; l < r; l++, r--) {
            int t = row[l]; row[l] = row[r]; row[r] = t;
        }
}
```

**Python**
```python
def rotate(mat):
    n = len(mat)
    for i in range(n):
        for j in range(i + 1, n):
            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]
    for row in mat:
        row.reverse()
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## Edge cases

- n = 1.
- Even and odd n.

---

## Common mistakes

1. Transposing the full matrix (`j` from 0) → swaps everything twice, so nothing changes.
2. Reversing columns instead of rows → anticlockwise.
3. Python: `mat = ans` rebinds the local; use `mat[:] = ans`.

---

## Follow-ups

1. Rotate anticlockwise.
2. Non-square m × n matrix.
3. Determine if one matrix is a rotation of another (LC 1886).

<details><summary>Answer sketches</summary>

**#1:** Transpose, then reverse each column; or reverse each row, then transpose.

**#2:** Can't be done in place in general; build an n × m result with `ans[j][m − 1 − i] = mat[i][j]`.

**#3:** Rotate up to 4 times and compare.
</details>

---

## Flashcards

**Rotate 90° clockwise in place?** #flashcard
Transpose, then reverse each row.

**Rotate 90° anticlockwise in place?** #flashcard
Transpose, then reverse each column.

**Clockwise index mapping?** #flashcard
(i, j) → (j, n − 1 − i).

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
