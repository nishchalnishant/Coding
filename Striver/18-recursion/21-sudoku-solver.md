---
module: striver/18-recursion
lesson: 21
topic: Sudoku Solver
difficulty: Hard
source: https://takeuforward.org/learning/dsa/sudoku-solver?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking, matrix]
---
# 21. Sudoku Solver

← [M-Coloring Problem](20-m-coloring.md) · [Part 18 index](README.md) · Next → [Expression Add Operators](22-expression-add-operators.md)

> [!abstract] Problem at a glance
> **Task:** Fill a 9 × 9 Sudoku in place so every row, column and 3 × 3 box contains 1–9 exactly once.
> **Key insight:** Find the next empty cell, try digits 1–9 that are absent from its row, column and box, recurse, and undo on failure. Keep `row[r][d]`, `col[c][d]`, `box[b][d]` boolean tables (b = (r/3)·3 + c/3) so each check is O(1).
> **Difficulty:** Hard · **Pattern:** Constraint backtracking on a grid · **Also on:** [LC 37](https://leetcode.com/problems/sudoku-solver/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sudoku-solver?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Backtracking with row/column/box scans](#3-backtracking-with-rowcolumnbox-scans) · [4. Backtracking with constraint tables](#4-backtracking-with-constraint-tables) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Write a program to solve a Sudoku puzzle by filling the empty cells (`'.'`) in place. Each of the digits 1–9 must occur exactly once in each row, each column and each of the nine 3 × 3 sub-boxes. The input has exactly one solution.

| Input | Output | Why |
|---|---|---|
| `board = LC 37 example (first row "53..7....")` | `first row becomes "534678912"` |  |

**Constraints:** 9 × 9 board of digits and `'.'`; exactly one solution.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Backtracking with row/column/box scans | next empty cell; for d in 1–9 if valid by scanning 27 cells → place, recurse | O(9^E · 27) | O(E) recursion |
| Backtracking with constraint tables | row/col/box used-digit tables; recurse over the list of empty cells | O(9^E) | O(E + 243) |

> [!tip] Interview angle
> They expect the clean backtracking with a boolean return (`true` once solved, so the filled board is kept) and the box index formula. Strong answers add constraint tables instead of rescanning, and mention the MRV heuristic (pick the empty cell with the fewest candidates), which is what makes hard puzzles fast.

---

## 3. Backtracking with row/column/box scans

**Intuition.** `valid(r, c, d)` scans the row, the column and the box. Simple and acceptable; each check is 27 reads. E = number of empty cells.

```python
def solve_scan(board):
    def valid(r, c, d):
        br, bc = r // 3 * 3, c // 3 * 3
        for i in range(9):
            if board[r][i] == d or board[i][c] == d or board[br + i // 3][bc + i % 3] == d:
                return False
        return True
    def go():
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for d in "123456789":
                        if valid(r, c, d):
                            board[r][c] = d
                            if go():
                                return True
                            board[r][c] = "."
                    return False
        return True
    go()
```

**Complexity:** time **O(9^E · 27)**, space **O(E) recursion**.

---

## 4. Backtracking with constraint tables

**Intuition.** Precompute the empty cells and the three `used` tables. `go(k)` fills the k-th empty cell: try each digit unused in all three tables, mark, recurse, unmark. Returning `true` up the stack stops further changes, leaving the solved board.

**Algorithm**

1. Scan the board: mark given digits in row/col/box; collect empty cells.
2. `go(k)`: k == |empty| → true.
3. (r, c) = empty[k]; b = r/3·3 + c/3; for d in 1–9 unused in row[r], col[c], box[b] → place & mark; if go(k + 1) return true; unmark & reset.
4. Return false.

**Dry run** — Cell (0,2): row 0 has {5,3,7}, col 2 has {8}, box 0 has {5,3,6,9,8} → candidates {1,2,4}; try 1 → … eventually 4 fits the unique solution.

**C++**
```cpp
bool rowU[9][10], colU[9][10], boxU[9][10];
vector<pair<int,int>> emptyCells;
bool fill(vector<vector<char>>& b, int k) {
    if (k == (int)emptyCells.size()) return true;
    auto [r, c] = emptyCells[k];
    int bx = r / 3 * 3 + c / 3;
    for (int d = 1; d <= 9; d++) {
        if (rowU[r][d] || colU[c][d] || boxU[bx][d]) continue;
        rowU[r][d] = colU[c][d] = boxU[bx][d] = true;
        b[r][c] = '0' + d;
        if (fill(b, k + 1)) return true;
        rowU[r][d] = colU[c][d] = boxU[bx][d] = false;
        b[r][c] = '.';
    }
    return false;
}
void solveSudoku(vector<vector<char>>& board) {
    memset(rowU, 0, sizeof rowU); memset(colU, 0, sizeof colU); memset(boxU, 0, sizeof boxU);
    emptyCells.clear();
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            if (board[r][c] == '.') { emptyCells.push_back({r, c}); continue; }
            int d = board[r][c] - '0';
            rowU[r][d] = colU[c][d] = boxU[r / 3 * 3 + c / 3][d] = true;
        }
    fill(board, 0);
}
```

**Java**
```java
static boolean[][] rowU, colU, boxU;
static List<int[]> emptyCells;
static boolean fill(char[][] b, int k) {
    if (k == emptyCells.size()) return true;
    int r = emptyCells.get(k)[0], c = emptyCells.get(k)[1], bx = r / 3 * 3 + c / 3;
    for (int d = 1; d <= 9; d++) {
        if (rowU[r][d] || colU[c][d] || boxU[bx][d]) continue;
        rowU[r][d] = colU[c][d] = boxU[bx][d] = true;
        b[r][c] = (char) ('0' + d);
        if (fill(b, k + 1)) return true;
        rowU[r][d] = colU[c][d] = boxU[bx][d] = false;
        b[r][c] = '.';
    }
    return false;
}
static void solveSudoku(char[][] board) {
    rowU = new boolean[9][10]; colU = new boolean[9][10]; boxU = new boolean[9][10];
    emptyCells = new ArrayList<>();
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            if (board[r][c] == '.') { emptyCells.add(new int[]{r, c}); continue; }
            int d = board[r][c] - '0';
            rowU[r][d] = colU[c][d] = boxU[r / 3 * 3 + c / 3][d] = true;
        }
    fill(board, 0);
}
```

**Python**
```python
def solve_sudoku(board):
    row = [[False] * 10 for _ in range(9)]
    col = [[False] * 10 for _ in range(9)]
    box = [[False] * 10 for _ in range(9)]
    empty = []
    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                empty.append((r, c))
            else:
                d = int(board[r][c])
                row[r][d] = col[c][d] = box[r // 3 * 3 + c // 3][d] = True
    def fill(k):
        if k == len(empty):
            return True
        r, c = empty[k]
        b = r // 3 * 3 + c // 3
        for d in range(1, 10):
            if row[r][d] or col[c][d] or box[b][d]:
                continue
            row[r][d] = col[c][d] = box[b][d] = True
            board[r][c] = str(d)
            if fill(k + 1):
                return True
            row[r][d] = col[c][d] = box[b][d] = False
            board[r][c] = "."
        return False
    fill(0)
```

**Complexity:** time **O(9^E)**, space **O(E + 243)** — ≤ 9 choices per empty cell, O(1) checks; real puzzles prune heavily.

---

## Edge cases

- Already-solved board → no changes.
- A single empty cell.
- Hard puzzles — exponential without MRV.

---

## Common mistakes

1. Box index `r/3 + c/3` instead of `(r/3)·3 + c/3`.
2. Not returning `true` after solving — backtracking erases the solution.
3. Forgetting to reset the cell to `'.'` on failure.

---

## Follow-ups

1. Valid Sudoku (LC 36).
2. Speed up.

<details><summary>Answer sketches</summary>

**#1:** Single pass with the three tables; no solving.

**#2:** MRV: choose the empty cell with the fewest candidates (bitmask popcount); add naked-single propagation.
</details>

---

## Flashcards

**Sudoku box index?** #flashcard
(r / 3) · 3 + c / 3.

**Why must the Sudoku solver return bool?** #flashcard
So the first complete fill propagates up and stops the undo steps.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
