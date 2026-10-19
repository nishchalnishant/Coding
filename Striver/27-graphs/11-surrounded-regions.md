---
module: striver/27-graphs
lesson: 11
topic: Surrounded Regions
difficulty: Medium
source: https://takeuforward.org/learning/dsa/surrounded-regions?category=traversal-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, grid, dfs, boundary]
---
# 11. Surrounded Regions

← [Distance of nearest cell having one](10-distance-of-nearest-cell-having-1.md) · [Part 27 index](README.md) · Next → [Number of distinct islands](12-number-of-distinct-islands.md)

> [!abstract] Problem at a glance
> **Task:** Flip every region of `'O'` that is fully surrounded by `'X'` (not connected to the border) to `'X'`, in place.
> **Key insight:** A region survives exactly when it touches the border. So mark the survivors instead of hunting for the doomed regions. Flood from every border `'O'` and mark it safe (temporarily `'#'`). Then every remaining `'O'` becomes `'X'` and every `'#'` turns back into `'O'`.
> **Difficulty:** Medium · **Pattern:** Boundary flood + relabel · **Also on:** LC 130
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/surrounded-regions?category=traversal-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Check each region](#3-check-each-region) · [4. Mark from the border](#4-mark-from-the-border) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `m × n` board of `'X'` and `'O'`, capture every region of `'O'`s (4-directionally connected) that is not connected to any `'O'` on the board's border, by flipping all its cells to `'X'`. Modify the board in place.

| Input | Output | Why |
|---|---|---|
| `board = ["XXXX","XOOX","XXOX","XOXX"]` | `["XXXX","XXXX","XXXX","XOXX"]` | the bottom O touches the border and survives |
| `board = ["OOO","OXO","OOO"]` | `unchanged` | every O is on the border |

**Constraints:** `1 ≤ m, n ≤ 200`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Check each region | BFS each O-region; flip if it never hits the border | O(m·n) | O(m·n) |
| Mark from the border | border O → '#', flood; then O→X, #→O | O(m·n) | O(m·n) stack |

> [!tip] Interview angle
> This is the same move as Number of Enclaves: turn 'is this region enclosed?' into 'what can be reached from the edge?'. Using a third symbol (`'#'`) avoids allocating a visited matrix.

---

## 3. Check each region

**Intuition.** Scan for an unvisited `'O'`; BFS its region, recording its cells and whether any is on the border. If none is, flip the whole region. Still linear, but more bookkeeping (a visited matrix and a cell list per region).

```python
from collections import deque

def solve_regions(board):
    R, C = len(board), len(board[0])
    seen = [[False] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            if board[r][c] != 'O' or seen[r][c]:
                continue
            seen[r][c] = True
            q, cells, border = deque([(r, c)]), [], False
            while q:
                x, y = q.popleft()
                cells.append((x, y))
                border |= x in (0, R - 1) or y in (0, C - 1)
                for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= a < R and 0 <= b < C and board[a][b] == 'O' and not seen[a][b]:
                        seen[a][b] = True
                        q.append((a, b))
            if not border:
                for x, y in cells:
                    board[x][y] = 'X'
```

**Complexity:** time **O(m·n)**, space **O(m·n)**.

---

## 4. Mark from the border

**Intuition.** Iterative DFS from every border `'O'`, relabelling reached cells `'#'`. Then one sweep flips `'O'` → `'X'` (captured) and `'#'` → `'O'` (safe).

**Algorithm**

1. Push every border cell holding `'O'`.
2. Pop `(r, c)`; if it is in bounds and `'O'`, set it to `'#'` and push its 4 neighbours.
3. Sweep the board: `'O'` → `'X'`, `'#'` → `'O'`.

**Dry run** — Example 1: the only border O is (3,1) → '#'. Its neighbours are X. The sweep flips (1,1),(1,2),(2,2) to X and restores (3,1).

**C++**
```cpp
void solve(vector<vector<char>>& board) {
    int R = board.size(), C = board[0].size();
    vector<pair<int, int>> st;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if ((r == 0 || r == R - 1 || c == 0 || c == C - 1) && board[r][c] == 'O') st.push_back({r, c});
    while (!st.empty()) {
        auto [r, c] = st.back(); st.pop_back();
        if (r < 0 || r >= R || c < 0 || c >= C || board[r][c] != 'O') continue;
        board[r][c] = '#';
        st.push_back({r + 1, c}); st.push_back({r - 1, c});
        st.push_back({r, c + 1}); st.push_back({r, c - 1});
    }
    for (auto& row : board)
        for (char& ch : row) ch = ch == '#' ? 'O' : 'X';
}
```

**Java**
```java
static void solve(char[][] board) {
    int R = board.length, C = board[0].length;
    ArrayDeque<int[]> st = new ArrayDeque<>();
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if ((r == 0 || r == R - 1 || c == 0 || c == C - 1) && board[r][c] == 'O') st.push(new int[]{r, c});
    while (!st.isEmpty()) {
        int[] p = st.pop();
        int r = p[0], c = p[1];
        if (r < 0 || r >= R || c < 0 || c >= C || board[r][c] != 'O') continue;
        board[r][c] = '#';
        st.push(new int[]{r + 1, c}); st.push(new int[]{r - 1, c});
        st.push(new int[]{r, c + 1}); st.push(new int[]{r, c - 1});
    }
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) board[r][c] = board[r][c] == '#' ? 'O' : 'X';
}
```

**Python**
```python
def solve(board):
    R, C = len(board), len(board[0])
    st = [(r, c) for r in range(R) for c in range(C)
          if (r in (0, R - 1) or c in (0, C - 1)) and board[r][c] == 'O']
    while st:
        r, c = st.pop()
        if 0 <= r < R and 0 <= c < C and board[r][c] == 'O':
            board[r][c] = '#'
            st += [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    for r in range(R):
        for c in range(C):
            board[r][c] = 'O' if board[r][c] == '#' else 'X'
```

**Complexity:** time **O(m·n)**, space **O(m·n) stack** — each cell is relabelled at most once; each relabel pushes 4 entries.

---

## Edge cases

- Boards with ≤ 2 rows or columns: every cell is on the border, nothing flips.
- All `'O'`: nothing flips.
- A region touching the border only diagonally: captured (diagonals don't connect).

---

## Common mistakes

1. Flipping regions during the first scan, which can flip a region before discovering it reaches the border.
2. Forgetting to restore `'#'` to `'O'`.
3. Recursive DFS on 200×200 all-O boards in Python (depth 4·10⁴).

---

## Follow-ups

1. Return the number of captured regions?
2. Union-find version?

<details><summary>Answer sketches</summary>

**#1:** Count O-regions that remain unmarked after the border flood.

**#2:** Union border O's with a virtual node `R·C`; at the end flip O's not connected to it.
</details>

---

## Flashcards

**Surrounded regions trick?** #flashcard
Flood from border O's, mark '#', then O→X and #→O.

**Why not flip regions directly during a scan?** #flashcard
You only know a region is enclosed after exploring all of it.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
