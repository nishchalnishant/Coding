---
module: striver/27-graphs
lesson: 8
topic: Number of enclaves
difficulty: Medium
source: https://takeuforward.org/learning/dsa/number-of-enclaves?category=traversal-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, grid, bfs, multi-source]
---
# 8. Number of enclaves

← [Flood fill algorithm](07-flood-fill.md) · [Part 27 index](README.md) · Next → [Rotten Oranges](09-rotten-oranges.md)

> [!abstract] Problem at a glance
> **Task:** Count land cells (`1`) from which you cannot walk off the grid's boundary (4-directional moves over land).
> **Key insight:** Turn the question around. Instead of asking which cells can escape, start from every land cell **on the border** and flood inwards. Everything reached can escape. The land that is never reached is the answer.
> **Difficulty:** Medium · **Pattern:** Boundary flood (reverse the question) · **Also on:** LC 1020
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-enclaves?category=traversal-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. BFS from every land cell](#3-bfs-from-every-land-cell) · [4. Multi-source BFS from the border](#4-multi-source-bfs-from-the-border) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`grid` is `m × n` with `0` = sea and `1` = land. A move goes to an adjacent land cell (4 directions) or off the grid from a border cell. Return the number of land cells from which you **cannot** reach the boundary in any number of moves.

| Input | Output | Why |
|---|---|---|
| `grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]` | `3` | (1,0) is on the border; (1,2),(2,1),(2,2) are trapped |
| `grid = [[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]` | `0` | the whole island touches the top border |

**Constraints:** `1 ≤ m, n ≤ 500`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| BFS from every land cell | for each land cell, does it reach the border? | O((m·n)²) | O(m·n) |
| Multi-source BFS from the border | flood from border land; count the rest | O(m·n) | O(m·n) |

> [!tip] Interview angle
> The same 'start from the boundary' move solves Surrounded Regions and Pacific Atlantic Water Flow. Name the pattern when you use it.

---

## 3. BFS from every land cell

**Intuition.** For each land cell, BFS its island and check whether any reached cell is on the border. Every cell of an island repeats the same BFS, so this is quadratic.

```python
from collections import deque

def num_enclaves_brute(grid):
    R, C = len(grid), len(grid[0])
    trapped = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] != 1:
                continue
            seen = {(r, c)}
            q = deque([(r, c)])
            esc = False
            while q:
                x, y = q.popleft()
                if x in (0, R - 1) or y in (0, C - 1):
                    esc = True
                    break
                for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if grid[a][b] == 1 and (a, b) not in seen:
                        seen.add((a, b))
                        q.append((a, b))
            trapped += not esc
    return trapped
```

**Complexity:** time **O((m·n)²)**, space **O(m·n)**.

---

## 4. Multi-source BFS from the border

**Intuition.** Push every border land cell into one queue and mark it. BFS through land. Every marked cell can escape. Finally count the land cells that were never marked.

**Algorithm**

1. Push every land cell in the first/last row or column, and mark it.
2. BFS: pop a cell; push and mark each unmarked land neighbour.
3. Return the number of land cells that are not marked.

**Dry run** — Example 1: border land = (1,0) only. BFS from it reaches nothing new ((1,1) is sea). Unmarked land: (1,2),(2,1),(2,2) = 3.

**C++**
```cpp
int numEnclaves(vector<vector<int>>& grid) {
    int R = grid.size(), C = grid[0].size();
    vector<vector<bool>> seen(R, vector<bool>(C, false));
    queue<pair<int, int>> q;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if (grid[r][c] == 1 && (r == 0 || r == R - 1 || c == 0 || c == C - 1)) {
                seen[r][c] = true; q.push({r, c});
            }
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        for (int d = 0; d < 4; d++) {
            int a = r + dr[d], b = c + dc[d];
            if (a >= 0 && a < R && b >= 0 && b < C && grid[a][b] == 1 && !seen[a][b]) {
                seen[a][b] = true; q.push({a, b});
            }
        }
    }
    int cnt = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) cnt += grid[r][c] == 1 && !seen[r][c];
    return cnt;
}
```

**Java**
```java
static int numEnclaves(int[][] grid) {
    int R = grid.length, C = grid[0].length;
    boolean[][] seen = new boolean[R][C];
    ArrayDeque<int[]> q = new ArrayDeque<>();
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if (grid[r][c] == 1 && (r == 0 || r == R - 1 || c == 0 || c == C - 1)) {
                seen[r][c] = true; q.add(new int[]{r, c});
            }
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    while (!q.isEmpty()) {
        int[] p = q.poll();
        for (int d = 0; d < 4; d++) {
            int a = p[0] + dr[d], b = p[1] + dc[d];
            if (a >= 0 && a < R && b >= 0 && b < C && grid[a][b] == 1 && !seen[a][b]) {
                seen[a][b] = true; q.add(new int[]{a, b});
            }
        }
    }
    int cnt = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) if (grid[r][c] == 1 && !seen[r][c]) cnt++;
    return cnt;
}
```

**Python**
```python
from collections import deque

def num_enclaves(grid):
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    q = deque()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1 and (r in (0, R - 1) or c in (0, C - 1)):
                seen[r][c] = True
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= a < R and 0 <= b < C and grid[a][b] == 1 and not seen[a][b]:
                seen[a][b] = True
                q.append((a, b))
    return sum(grid[r][c] == 1 and not seen[r][c] for r in range(R) for c in range(C))
```

**Complexity:** time **O(m·n)**, space **O(m·n)** — each cell is enqueued at most once.

---

## Edge cases

- Grid with 1 or 2 rows/columns: every cell is on the border → 0.
- No land: 0.
- Interior island next to (but not touching) a border island: still trapped.

---

## Common mistakes

1. Seeding only the first and last row, forgetting the first and last column.
2. Counting islands instead of cells.
3. Starting a separate BFS per border cell without a shared `seen` (repeated work).

---

## Follow-ups

1. Count closed islands instead of cells (LC 1254)?
2. Pacific Atlantic (LC 417)?

<details><summary>Answer sketches</summary>

**#1:** Flood from the border first, then count the remaining islands (water and land roles swap in that problem: 0 is land).

**#2:** Two boundary BFS runs going uphill, one from each ocean; answer = cells reached by both.
</details>

---

## Flashcards

**Enclaves trick?** #flashcard
BFS from border land; unreached land is the answer.

**Multi-source BFS seeding?** #flashcard
Push all sources into one queue before the loop.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
