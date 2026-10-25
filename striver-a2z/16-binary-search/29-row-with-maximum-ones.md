---
module: striver-a2z/16-binary-search
lesson: 29
topic: Find Row with Maximum 1's
difficulty: Easy
source: https://takeuforward.org/learning/dsa/find-row-with-maximum-1's?category=2d-arrays&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, matrix]
---
# 29. Find Row with Maximum 1's

← [Split Array — Largest Sum](28-split-array-largest-sum.md) · [Part 16 index](README.md) · Next → [Search in a 2D Matrix](30-search-in-a-2d-matrix.md)

> [!abstract] Problem at a glance
> **Task:** In a binary matrix with each row sorted, return the index of the row with the most 1s (first on tie), or −1 if there are none.
> **Key insight:** In a sorted 0/1 row, ones = `m − lower_bound(row, 1)`. Do that per row: O(n log m). Or walk a staircase from the top-right: O(n + m).
> **Difficulty:** Easy · **Pattern:** Binary search per row / staircase
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-row-with-maximum-1's?category=2d-arrays&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Count every cell](#3-count-every-cell) · [4. Lower bound per row](#4-lower-bound-per-row) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `n × m` binary matrix whose rows are sorted in non-decreasing order, return the 0-based index of the row with the maximum number of 1s. If several rows tie, return the smallest index. Return `-1` if the matrix has no 1s.

| Input | Output | Why |
|---|---|---|
| `[[0,1,1,1],[0,0,1,1],[1,1,1,1],[0,0,0,0]]` | `2` |  |
| `[[0,0],[0,0]]` | `-1` |  |

**Constraints:** `1 ≤ n, m ≤ 10³`, entries are 0/1, rows sorted.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Count every cell | sum each row | O(n · m) | O(1) |
| Lower bound per row | ones = m − first index of 1 | O(n log m) | O(1) |

---

## 3. Count every cell

**Intuition.** Ignores sortedness.

```python
def row_max_ones_brute(mat):
    best, idx = 0, -1
    for i, row in enumerate(mat):
        c = sum(row)
        if c > best:
            best, idx = c, i
    return idx
```

**Complexity:** time **O(n · m)**, space **O(1)**.

---

## 4. Lower bound per row

**Intuition.** Binary search the first 1 in each row. Keep the strictly larger count so ties keep the earlier row.

**Staircase alternative, O(n + m):** start at the top-right; move left while you see 1 (recording this row), move down on 0. The column pointer never moves right, so total moves ≤ n + m. Mention it as the follow-up optimum.

**C++**
```cpp
int rowWithMax1s(vector<vector<int>>& mat) {
    int best = 0, idx = -1;
    for (int i = 0; i < (int)mat.size(); i++) {
        int m = mat[i].size(), lo = 0, hi = m - 1, first = m;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (mat[i][mid] == 1) { first = mid; hi = mid - 1; }
            else lo = mid + 1;
        }
        if (m - first > best) { best = m - first; idx = i; }
    }
    return idx;
}
```

**Java**
```java
static int rowWithMax1s(int[][] mat) {
    int best = 0, idx = -1;
    for (int i = 0; i < mat.length; i++) {
        int m = mat[i].length, lo = 0, hi = m - 1, first = m;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (mat[i][mid] == 1) { first = mid; hi = mid - 1; }
            else lo = mid + 1;
        }
        if (m - first > best) { best = m - first; idx = i; }
    }
    return idx;
}
```

**Python**
```python
def row_with_max_1s(mat):
    best, idx = 0, -1
    for i, row in enumerate(mat):
        lo, hi, first = 0, len(row) - 1, len(row)
        while lo <= hi:
            mid = (lo + hi) // 2
            if row[mid] == 1:
                first, hi = mid, mid - 1
            else:
                lo = mid + 1
        if len(row) - first > best:
            best, idx = len(row) - first, i
    return idx
```

**Complexity:** time **O(n log m)**, space **O(1)** — n rows × log m.

---

## Edge cases

- No ones → −1.
- Ties → smallest index (use `>`, not `≥`).

---

## Common mistakes

1. `≥` on tie → returns the last tied row.
2. Returning the count instead of the index.

---

## Follow-ups

1. Rows not sorted.
2. Column with max ones in a column-sorted matrix.

<details><summary>Answer sketches</summary>

**#1:** O(nm) — no shortcut.

**#2:** Same idea transposed.
</details>

---

## Flashcards

**Ones in a sorted 0/1 row?** #flashcard
m − lower_bound(row, 1).

**O(n + m) for row with max 1s?** #flashcard
Staircase from top-right: left on 1, down on 0.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
