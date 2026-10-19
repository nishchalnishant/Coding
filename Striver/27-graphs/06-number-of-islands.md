---
module: striver/27-graphs
lesson: 6
topic: Number of islands
difficulty: Medium
source: https://takeuforward.org/learning/dsa/number-of-islands?category=traversal-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, grid, bfs, dfs]
---
# 6. Number of islands

← [Number of provinces](05-number-of-provinces.md) · [Part 27 index](README.md) · Next → [Flood fill algorithm](07-flood-fill.md)

> [!abstract] Problem at a glance
> **Task:** Count the islands (4-directionally connected groups of `'1'`) in a grid.
> **Key insight:** A grid is an implicit graph: cells are nodes and the 4 neighbours are edges. Scan every cell; each `'1'` not yet visited starts a flood that visits its whole island. Count the floods.
> **Difficulty:** Medium · **Pattern:** Grid flood fill / components · **Also on:** LC 200
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-islands?category=traversal-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive DFS (sink the island)](#3-recursive-dfs-sink-the-island) · [4. BFS flood](#4-bfs-flood) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `m × n` grid of `'1'` (land) and `'0'` (water), return the number of islands. An island is a maximal group of land cells connected horizontally or vertically. (The takeuforward/GFG version also connects diagonals; see follow-up #1.)

| Input | Output | Why |
|---|---|---|
| `grid = ["11110","11010","11000","00000"]` | `1` | all land is connected |
| `grid = ["11000","11000","00100","00011"]` | `3` | top-left block, the centre cell, the bottom-right pair |

**Constraints:** `1 ≤ m, n ≤ 300`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive DFS (sink the island) | dfs sets cells to '0' and recurses 4 ways | O(m·n) | O(m·n) recursion |
| BFS flood | queue per island, mark when pushed | O(m·n) | O(min(m, n)) queue |

> [!tip] Interview angle
> Ask whether you may mutate the grid. If yes, overwrite visited land with `'0'` ('sink' it) and skip the visited array. If no, use `visited`. Mention that recursive DFS can reach depth m·n = 9·10⁴, so BFS or an explicit stack is safer.

---

## 3. Recursive DFS (sink the island)

**Intuition.** For each land cell, count it and call `sink(r, c)`, which returns if out of bounds or water, otherwise sets the cell to `'0'` and recurses into its 4 neighbours. Overwriting replaces the visited array.

```python
import sys

def num_islands_dfs(grid):
    sys.setrecursionlimit(10 ** 6)
    R, C = len(grid), len(grid[0])
    def sink(r, c):
        if r < 0 or r >= R or c < 0 or c >= C or grid[r][c] != '1':
            return
        grid[r][c] = '0'
        sink(r + 1, c); sink(r - 1, c); sink(r, c + 1); sink(r, c - 1)
    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '1':
                count += 1
                sink(r, c)
    return count
```

**Complexity:** time **O(m·n)**, space **O(m·n) recursion**.

---

## 4. BFS flood

**Intuition.** Same scan, but each island is flooded with a queue. Marking a cell as water when it is **pushed** prevents duplicates. The BFS frontier is a diagonal band, at most O(min(m, n)) wide, and there is no recursion depth risk.

**Algorithm**

1. For every cell `(r, c)` with `'1'`: `count++`, set it to `'0'`, push it.
2. Pop `(r, c)`; for each of the 4 neighbours in bounds with `'1'`: set it to `'0'` and push it.
3. When the queue empties, the island is gone; continue scanning.
4. Return `count`.

**Dry run** — Second example: (0,0) floods the 2×2 block → 1. (2,2) floods itself → 2. (3,3) floods (3,3),(3,4) → 3.

**C++**
```cpp
int numIslands(vector<vector<char>>& grid) {
    int R = grid.size(), C = grid[0].size(), count = 0;
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (grid[r][c] != '1') continue;
            count++;
            grid[r][c] = '0';
            queue<pair<int, int>> q; q.push({r, c});
            while (!q.empty()) {
                auto [x, y] = q.front(); q.pop();
                for (int d = 0; d < 4; d++) {
                    int a = x + dr[d], b = y + dc[d];
                    if (a >= 0 && a < R && b >= 0 && b < C && grid[a][b] == '1') {
                        grid[a][b] = '0';
                        q.push({a, b});
                    }
                }
            }
        }
    return count;
}
```

**Java**
```java
static int numIslands(char[][] grid) {
    int R = grid.length, C = grid[0].length, count = 0;
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (grid[r][c] != '1') continue;
            count++;
            grid[r][c] = '0';
            ArrayDeque<int[]> q = new ArrayDeque<>();
            q.add(new int[]{r, c});
            while (!q.isEmpty()) {
                int[] p = q.poll();
                for (int d = 0; d < 4; d++) {
                    int a = p[0] + dr[d], b = p[1] + dc[d];
                    if (a >= 0 && a < R && b >= 0 && b < C && grid[a][b] == '1') {
                        grid[a][b] = '0';
                        q.add(new int[]{a, b});
                    }
                }
            }
        }
    return count;
}
```

**Python**
```python
from collections import deque

def num_islands(grid):
    R, C = len(grid), len(grid[0])
    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] != '1':
                continue
            count += 1
            grid[r][c] = '0'
            q = deque([(r, c)])
            while q:
                x, y = q.popleft()
                for nx_, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx_ < R and 0 <= ny < C and grid[nx_][ny] == '1':
                        grid[nx_][ny] = '0'
                        q.append((nx_, ny))
    return count
```

**Complexity:** time **O(m·n)**, space **O(min(m, n)) queue** — every cell is pushed at most once and checks 4 neighbours.

---

## Edge cases

- All water: 0. All land: 1.
- Checkerboard: diagonal cells are separate islands under 4-connectivity.
- Ring of land around water: one island.

---

## Common mistakes

1. Checking `grid[r][c]` before the bounds check (index error).
2. Marking visited on pop in BFS, so the same cell is queued from several neighbours.
3. Comparing with integer `1` when the grid holds characters `'1'`.

---

## Follow-ups

1. 8-directional connectivity (GFG/Striver version)?
2. Grid must not be modified?
3. Land is added cell by cell and you need the count after each addition?

<details><summary>Answer sketches</summary>

**#1:** Loop over all 8 `(dr, dc)` pairs with `dr, dc ∈ {−1, 0, 1}`, excluding `(0, 0)`. Nothing else changes.

**#2:** Use a separate `visited` matrix.

**#3:** That is Number of Islands II: union-find over cells.
</details>

---

## Flashcards

**Grid as a graph?** #flashcard
Cells are nodes, 4 (or 8) neighbours are edges.

**Why is BFS safer than recursive DFS on large grids?** #flashcard
Recursion depth can reach m·n and overflow the stack.

**Island count equals…?** #flashcard
The number of floods started from unvisited land cells.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
