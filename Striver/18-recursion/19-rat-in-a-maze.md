---
module: striver/18-recursion
lesson: 19
topic: Rat in a Maze
difficulty: Medium
source: https://takeuforward.org/learning/dsa/rat-in-a-maze?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking, matrix]
---
# 19. Rat in a Maze

← [N-Queens](18-n-queens.md) · [Part 18 index](README.md) · Next → [M-Coloring Problem](20-m-coloring.md)

> [!abstract] Problem at a glance
> **Task:** List all paths (as D/L/R/U strings) from the top-left to the bottom-right of a 0/1 grid, visiting each cell at most once.
> **Key insight:** Grid DFS with a visited mark and backtracking. Exploring moves in alphabetical order D, L, R, U produces the paths already sorted, so no final sort is needed.
> **Difficulty:** Medium · **Pattern:** Grid DFS backtracking (enumerate paths) · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/rat-in-a-maze-problem/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/rat-in-a-maze?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS, collect, then sort](#3-dfs-collect-then-sort) · [4. DFS in D, L, R, U order](#4-dfs-in-d-l-r-u-order) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A rat starts at `(0, 0)` of an `n × n` matrix `mat` and must reach `(n−1, n−1)`. It can move `U`, `D`, `L`, `R`; `1` cells are open, `0` cells are blocked. A cell can't be visited twice in one path. Return all paths in lexicographically increasing order; return `[]` if none (including when the start or end is blocked).

| Input | Output | Why |
|---|---|---|
| `mat = [[1,0,0,0],[1,1,0,1],[1,1,0,0],[0,1,1,1]]` | `["DDRDRR", "DRDDRR"]` |  |
| `mat = [[1,0],[1,0]]` | `[]` | destination blocked |

**Constraints:** `2 ≤ n ≤ 5`, `mat[i][j] ∈ {0, 1}`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS, collect, then sort | any direction order, sort the paths at the end | O(3^(n²) · n²) | O(n²) |
| DFS in D, L, R, U order | direction arrays in alphabetical order → sorted output | O(3^(n²) · n²) | O(n²) |

> [!tip] Interview angle
> Same skeleton as Word Search but collecting every path instead of stopping at the first. Points to mention: check the start cell, use direction arrays `dr/dc/ch` in DLRU order to get sorted output, and bound the complexity by O(4^(n²)) (really ≤ 3^(n²) after the first move).

---

## 3. DFS, collect, then sort

**Intuition.** Explore in any order and sort the final list. Correct; the sort is avoidable.

```python
def maze_sort(mat):
    n = len(mat)
    if not mat[0][0] or not mat[n - 1][n - 1]:
        return []
    out, seen = [], [[False] * n for _ in range(n)]
    def go(r, c, path):
        if (r, c) == (n - 1, n - 1):
            out.append(path)
            return
        seen[r][c] = True
        for dr, dc, ch in ((-1, 0, "U"), (0, 1, "R"), (1, 0, "D"), (0, -1, "L")):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and mat[nr][nc] and not seen[nr][nc]:
                go(nr, nc, path + ch)
        seen[r][c] = False
    go(0, 0, "")
    return sorted(out)
```

**Complexity:** time **O(3^(n²) · n²)**, space **O(n²)**.

---

## 4. DFS in D, L, R, U order

**Intuition.** Two paths first differ at some move; the one taking the alphabetically smaller move there is explored first. So DFS in D < L < R < U order emits paths in sorted order.

**Algorithm**

1. If start or end blocked → `[]`.
2. `go(r, c)`: at target → record path.
3. Mark (r, c); for (dr, dc, ch) in D, L, R, U: if in bounds, open, unvisited → push ch, recurse, pop. Unmark.

**Dry run** — Example: (0,0) D (1,0) D (2,0) R (2,1) D (3,1) R R ✓ DDRDRR; back to (1,0) R (1,1) D (2,1) D (3,1) R R ✓ DRDDRR.

**C++**
```cpp
void go(int r, int c, vector<vector<int>>& m, vector<vector<bool>>& seen, string& path, vector<string>& out) {
    int n = m.size();
    if (r == n - 1 && c == n - 1) { out.push_back(path); return; }
    static const int dr[] = {1, 0, 0, -1}, dc[] = {0, -1, 1, 0};
    static const char ch[] = {'D', 'L', 'R', 'U'};
    seen[r][c] = true;
    for (int k = 0; k < 4; k++) {
        int nr = r + dr[k], nc = c + dc[k];
        if (nr < 0 || nc < 0 || nr >= n || nc >= n || !m[nr][nc] || seen[nr][nc]) continue;
        path.push_back(ch[k]);
        go(nr, nc, m, seen, path, out);
        path.pop_back();
    }
    seen[r][c] = false;
}
vector<string> findPath(vector<vector<int>>& mat) {
    int n = mat.size();
    vector<string> out;
    if (!mat[0][0] || !mat[n - 1][n - 1]) return out;
    vector<vector<bool>> seen(n, vector<bool>(n, false));
    string path;
    go(0, 0, mat, seen, path, out);
    return out;
}
```

**Java**
```java
static final int[] DR = {1, 0, 0, -1}, DC = {0, -1, 1, 0};
static final char[] CH = {'D', 'L', 'R', 'U'};
static void go(int r, int c, int[][] m, boolean[][] seen, StringBuilder path, List<String> out) {
    int n = m.length;
    if (r == n - 1 && c == n - 1) { out.add(path.toString()); return; }
    seen[r][c] = true;
    for (int k = 0; k < 4; k++) {
        int nr = r + DR[k], nc = c + DC[k];
        if (nr < 0 || nc < 0 || nr >= n || nc >= n || m[nr][nc] == 0 || seen[nr][nc]) continue;
        path.append(CH[k]);
        go(nr, nc, m, seen, path, out);
        path.deleteCharAt(path.length() - 1);
    }
    seen[r][c] = false;
}
static List<String> findPath(int[][] mat) {
    int n = mat.length;
    List<String> out = new ArrayList<>();
    if (mat[0][0] == 0 || mat[n - 1][n - 1] == 0) return out;
    go(0, 0, mat, new boolean[n][n], new StringBuilder(), out);
    return out;
}
```

**Python**
```python
def find_path(mat):
    n = len(mat)
    if not mat[0][0] or not mat[n - 1][n - 1]:
        return []
    out, path = [], []
    seen = [[False] * n for _ in range(n)]
    moves = ((1, 0, "D"), (0, -1, "L"), (0, 1, "R"), (-1, 0, "U"))
    def go(r, c):
        if r == n - 1 and c == n - 1:
            out.append("".join(path))
            return
        seen[r][c] = True
        for dr, dc, ch in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and mat[nr][nc] and not seen[nr][nc]:
                path.append(ch)
                go(nr, nc)
                path.pop()
        seen[r][c] = False
    go(0, 0)
    return out
```

**Complexity:** time **O(3^(n²) · n²)**, space **O(n²)** — each cell entered at most once per path; ≤ 3 onward choices.

---

## Edge cases

- Start or end blocked → `[]`.
- Fully open grid — exponential number of paths.

---

## Common mistakes

1. Not checking the start cell.
2. Marking visited but never unmarking — loses paths sharing cells.
3. Wrong direction order → unsorted output.

---

## Follow-ups

1. Shortest path only.
2. Only moves right/down; count paths.

<details><summary>Answer sketches</summary>

**#1:** BFS — O(n²).

**#2:** DP `ways[r][c] = ways[r−1][c] + ways[r][c−1]` on open cells (LC 63).
</details>

---

## Flashcards

**Rat in a Maze sorted-output trick?** #flashcard
Explore D, L, R, U in that (alphabetical) order.

**Rat in a Maze vs Word Search?** #flashcard
Same visited/backtrack DFS; collect all paths vs stop at first success.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
