---
module: striver-a2z/18-recursion
lesson: 18
topic: N-Queens
difficulty: Hard
source: https://takeuforward.org/learning/dsa/n-queens?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking]
---
# 18. N-Queens

← [Word Search](17-word-search.md) · [Part 18 index](README.md) · Next → [Rat in a Maze](19-rat-in-a-maze.md)

> [!abstract] Problem at a glance
> **Task:** Place `n` queens on an `n × n` board so none attack each other; return every board.
> **Key insight:** One queen per row, so recurse on the row and choose a column. A placement is safe iff its column, `r − c` diagonal and `r + c` anti-diagonal are all unused — three boolean arrays give O(1) checks.
> **Difficulty:** Hard · **Pattern:** Row-by-row backtracking with O(1) conflict sets · **Also on:** [LC 51](https://leetcode.com/problems/n-queens/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/n-queens?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Row recursion, scan the board for conflicts](#3-row-recursion-scan-the-board-for-conflicts) · [4. Row recursion with column/diagonal sets](#4-row-recursion-with-columndiagonal-sets) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Return all distinct solutions to the n-queens puzzle. Each solution is a board of `n` strings where `'Q'` marks a queen and `'.'` an empty square. Any order.

| Input | Output | Why |
|---|---|---|
| `n = 4` | `[[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]` |  |
| `n = 1` | `[["Q"]]` |  |

**Constraints:** `1 ≤ n ≤ 9`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Row recursion, scan the board for conflicts | for each column, scan up the column and both diagonals | O(n! · n) | O(n²) |
| Row recursion with column/diagonal sets | cols[c], diag[r − c + n − 1], anti[r + c] | O(n!) | O(n) |

> [!tip] Interview angle
> The canonical backtracking showcase. Start from "one queen per row" (which collapses n² choose n to n! orderings), then the O(1) diagonal sets via `r − c + n − 1` and `r + c` indices. Solution counts for n = 1…8: 1, 0, 0, 2, 10, 4, 40, 92. N-Queens II (count only) uses the same search; bitmasks make it fastest.

---

## 3. Row recursion, scan the board for conflicts

**Intuition.** Place row by row; to test `(r, c)` walk upward through the column and both diagonals looking for a `Q`. Correct, but every test is O(n).

```python
def queens_scan(n):
    board = [["."] * n for _ in range(n)]
    out = []
    def safe(r, c):
        for i in range(r):
            d = r - i
            if board[i][c] == "Q" or (c - d >= 0 and board[i][c - d] == "Q") or (c + d < n and board[i][c + d] == "Q"):
                return False
        return True
    def go(r):
        if r == n:
            out.append(["".join(row) for row in board])
            return
        for c in range(n):
            if safe(r, c):
                board[r][c] = "Q"
                go(r + 1)
                board[r][c] = "."
    go(0)
    return out
```

**Complexity:** time **O(n! · n)**, space **O(n²)**.

---

## 4. Row recursion with column/diagonal sets

**Intuition.** All squares on a `\` diagonal share `r − c`; on a `/` diagonal they share `r + c`. Keep three boolean arrays (sizes n, 2n − 1, 2n − 1); placing and removing a queen flips three entries.

**Algorithm**

1. `go(r)`: if r == n → record board.
2. For c in 0 … n−1: if cols[c] or diag[r−c+n−1] or anti[r+c] → skip.
3. Mark all three, set board[r][c] = 'Q', `go(r + 1)`, unmark and reset.

**Dry run** — n = 4: row0 c1 → row1 c3 → row2 c0 → row3 c2 ✓ → [".Q..", "...Q", "Q...", "..Q."].

**C++**
```cpp
void go(int r, int n, vector<string>& b, vector<bool>& col, vector<bool>& d1, vector<bool>& d2, vector<vector<string>>& out) {
    if (r == n) { out.push_back(b); return; }
    for (int c = 0; c < n; c++) {
        if (col[c] || d1[r - c + n - 1] || d2[r + c]) continue;
        col[c] = d1[r - c + n - 1] = d2[r + c] = true;
        b[r][c] = 'Q';
        go(r + 1, n, b, col, d1, d2, out);
        b[r][c] = '.';
        col[c] = d1[r - c + n - 1] = d2[r + c] = false;
    }
}
vector<vector<string>> solveNQueens(int n) {
    vector<string> b(n, string(n, '.'));
    vector<bool> col(n), d1(2 * n - 1), d2(2 * n - 1);
    vector<vector<string>> out;
    go(0, n, b, col, d1, d2, out);
    return out;
}
```

**Java**
```java
static void go(int r, int n, char[][] b, boolean[] col, boolean[] d1, boolean[] d2, List<List<String>> out) {
    if (r == n) {
        List<String> sol = new ArrayList<>();
        for (char[] row : b) sol.add(new String(row));
        out.add(sol);
        return;
    }
    for (int c = 0; c < n; c++) {
        if (col[c] || d1[r - c + n - 1] || d2[r + c]) continue;
        col[c] = d1[r - c + n - 1] = d2[r + c] = true;
        b[r][c] = 'Q';
        go(r + 1, n, b, col, d1, d2, out);
        b[r][c] = '.';
        col[c] = d1[r - c + n - 1] = d2[r + c] = false;
    }
}
static List<List<String>> solveNQueens(int n) {
    char[][] b = new char[n][n];
    for (char[] row : b) Arrays.fill(row, '.');
    List<List<String>> out = new ArrayList<>();
    go(0, n, b, new boolean[n], new boolean[2 * n - 1], new boolean[2 * n - 1], out);
    return out;
}
```

**Python**
```python
def solve_n_queens(n):
    board = [["."] * n for _ in range(n)]
    col, d1, d2 = [False] * n, [False] * (2 * n - 1), [False] * (2 * n - 1)
    out = []
    def go(r):
        if r == n:
            out.append(["".join(row) for row in board])
            return
        for c in range(n):
            if col[c] or d1[r - c + n - 1] or d2[r + c]:
                continue
            col[c] = d1[r - c + n - 1] = d2[r + c] = True
            board[r][c] = "Q"
            go(r + 1)
            board[r][c] = "."
            col[c] = d1[r - c + n - 1] = d2[r + c] = False
    go(0)
    return out
```

**Complexity:** time **O(n!)**, space **O(n)** — ≤ n choices in row 0, ≤ n − 1 in row 1, … → O(n!), each check O(1).

---

## Edge cases

- n = 2, 3 → no solutions.
- n = 1 → `[["Q"]]`.

---

## Common mistakes

1. Negative index for `r − c` — offset by n − 1.
2. Forgetting to clear all three markers on backtrack.
3. Placing more than one queen per row (iterating cells, not rows).

---

## Follow-ups

1. Count only (LC 52).
2. Any one solution fast for large n.

<details><summary>Answer sketches</summary>

**#1:** Bitmask: `avail = ~(cols | d1 | d2) & full`; pick lowest bit; shift d1 left, d2 right per row.

**#2:** Constructive pattern exists for n ≥ 4; or min-conflicts local search.
</details>

---

## Flashcards

**N-Queens diagonal indices?** #flashcard
\ diagonal: r − c + n − 1; / diagonal: r + c; each array size 2n − 1.

**Solutions for n = 4, 5, 6, 8?** #flashcard
2, 10, 4, 92.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../04-practice/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../04-practice/algorithms/12-backtracking.md)
