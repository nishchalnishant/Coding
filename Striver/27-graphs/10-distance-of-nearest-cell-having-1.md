---
module: striver/27-graphs
lesson: 10
topic: Distance of nearest cell having one
difficulty: Medium
source: https://takeuforward.org/learning/dsa/distance-of-nearest-cell-having-one?category=traversal-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, grid, bfs, multi-source]
---
# 10. Distance of nearest cell having one

← [Rotten Oranges](09-rotten-oranges.md) · [Part 27 index](README.md) · Next → [Surrounded Regions](11-surrounded-regions.md)

> [!abstract] Problem at a glance
> **Task:** For every cell of a binary grid, return the 4-directional distance to the nearest cell containing `1`.
> **Key insight:** Run one BFS backwards from the targets instead of a BFS forwards from every cell. Seed **every 1** at distance 0; BFS then labels each cell with its distance to the nearest seed, because BFS reaches each cell first by a shortest path from the whole source set.
> **Difficulty:** Medium · **Pattern:** Multi-source BFS (distance field) · **Also on:** LC 542 (mirror: nearest 0)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/distance-of-nearest-cell-having-one?category=traversal-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Min Manhattan distance to every 1](#3-min-manhattan-distance-to-every-1) · [4. Multi-source BFS](#4-multi-source-bfs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `m × n` grid of `0`s and `1`s with at least one `1`, return a matrix `dist` where `dist[r][c]` is the minimum number of 4-directional steps from `(r, c)` to any cell containing `1`.

| Input | Output | Why |
|---|---|---|
| `grid = [[0,1,1,0],[1,1,0,0],[0,0,1,1]]` | `[[1,0,0,1],[0,0,1,1],[1,1,0,0]]` | every 0 is 1 step from a 1 |
| `grid = [[0,0,0],[0,1,0],[0,0,0]]` | `[[2,1,2],[1,0,1],[2,1,2]]` | distance from the centre |

**Constraints:** `1 ≤ m, n ≤ 500`, at least one `1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Min Manhattan distance to every 1 | for each cell, scan all 1s | O((m·n)²) | O(m·n) |
| Multi-source BFS | seed all 1s with distance 0 | O(m·n) | O(m·n) |

> [!tip] Interview angle
> Without obstacles the distance is just the minimum Manhattan distance to a 1, which gives an O((mn)²) brute force. BFS still wins, and it keeps working when obstacles appear in a follow-up. The DP alternative is two passes (top-left, then bottom-right), each taking the min of neighbours + 1.

---

## 3. Min Manhattan distance to every 1

**Intuition.** With free movement, the shortest path to a given 1 has length `|r−a| + |c−b|`. Take the minimum over all 1s for every cell.

```python
def nearest_brute(grid):
    R, C = len(grid), len(grid[0])
    ones = [(r, c) for r in range(R) for c in range(C) if grid[r][c] == 1]
    return [[min(abs(r - a) + abs(c - b) for a, b in ones) for c in range(C)] for r in range(R)]
```

**Complexity:** time **O((m·n)²)**, space **O(m·n)**.

---

## 4. Multi-source BFS

**Intuition.** Initialise `dist` to −1 (unvisited), set every 1 to 0 and enqueue it. BFS: a neighbour with −1 gets `dist[u] + 1` and is enqueued. The first assignment is final.

**Algorithm**

1. `dist[r][c] = 0` and enqueue for each `1`; `−1` elsewhere.
2. Pop `(r, c)`; for each in-bounds neighbour with `dist = −1`: set `dist[r][c] + 1`, enqueue.
3. Return `dist`.

**Dry run** — Centre-1 example: seed (1,1). Level 1: (0,1),(2,1),(1,0),(1,2) = 1. Level 2: the corners = 2.

**C++**
```cpp
vector<vector<int>> nearest(vector<vector<int>>& grid) {
    int R = grid.size(), C = grid[0].size();
    vector<vector<int>> dist(R, vector<int>(C, -1));
    queue<pair<int, int>> q;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if (grid[r][c] == 1) { dist[r][c] = 0; q.push({r, c}); }
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        for (int d = 0; d < 4; d++) {
            int a = r + dr[d], b = c + dc[d];
            if (a >= 0 && a < R && b >= 0 && b < C && dist[a][b] == -1) {
                dist[a][b] = dist[r][c] + 1; q.push({a, b});
            }
        }
    }
    return dist;
}
```

**Java**
```java
static int[][] nearest(int[][] grid) {
    int R = grid.length, C = grid[0].length;
    int[][] dist = new int[R][C];
    ArrayDeque<int[]> q = new ArrayDeque<>();
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            dist[r][c] = -1;
            if (grid[r][c] == 1) { dist[r][c] = 0; q.add(new int[]{r, c}); }
        }
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    while (!q.isEmpty()) {
        int[] p = q.poll();
        for (int d = 0; d < 4; d++) {
            int a = p[0] + dr[d], b = p[1] + dc[d];
            if (a >= 0 && a < R && b >= 0 && b < C && dist[a][b] == -1) {
                dist[a][b] = dist[p[0]][p[1]] + 1; q.add(new int[]{a, b});
            }
        }
    }
    return dist;
}
```

**Python**
```python
from collections import deque

def nearest(grid):
    R, C = len(grid), len(grid[0])
    dist = [[-1] * C for _ in range(R)]
    q = deque()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1:
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= a < R and 0 <= b < C and dist[a][b] == -1:
                dist[a][b] = dist[r][c] + 1
                q.append((a, b))
    return dist
```

**Complexity:** time **O(m·n)**, space **O(m·n)** — every cell is assigned and enqueued exactly once.

---

## Edge cases

- All ones: all zeros.
- Single 1 in a corner: the distance is the Manhattan distance to that corner.
- One row: a 1D distance field.

---

## Common mistakes

1. BFS from each 0 separately: O((mn)²).
2. Initialising `dist` to 0 and using it as the visited check, which confuses unvisited cells with the sources.
3. Forgetting `dist` is relative to the **nearest** 1: one BFS from a single 1 is wrong.

---

## Follow-ups

1. LC 542 asks for the distance to the nearest 0?
2. Some cells are walls?
3. O(1) extra space?

<details><summary>Answer sketches</summary>

**#1:** Seed the 0s instead; identical code.

**#2:** Skip wall neighbours; the Manhattan shortcut no longer works, BFS still does.

**#3:** Two-pass DP in place: forward pass uses top/left, backward pass uses bottom/right.
</details>

---

## Flashcards

**Distance-to-nearest-X field?** #flashcard
Multi-source BFS from all X cells.

**Two-pass DP alternative?** #flashcard
Top-left pass then bottom-right pass, min of neighbour + 1.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
