---
module: striver/27-graphs
lesson: 27
topic: Shortest distance in a binary maze
difficulty: Medium
source: https://takeuforward.org/learning/dsa/shortest-distance-in-a-binary-maze?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bfs, grid, shortest-path]
---
# 27. Shortest distance in a binary maze

← [Print shortest path](26-print-shortest-path-dijkstra.md) · [Part 27 index](README.md) · Next → [Path with minimum effort](28-path-with-minimum-effort.md)

> [!abstract] Problem at a glance
> **Task:** In a 0/1 grid, return the fewest 4-directional steps from `source` to `destination` moving only through 1-cells (`-1` if impossible).
> **Key insight:** Every move costs 1, so BFS from the source gives final distances at discovery. Dijkstra (what Striver teaches here) also works, but with unit weights its 'heap' is a FIFO queue anyway: entries are pushed in non-decreasing distance order.
> **Difficulty:** Medium · **Pattern:** Grid BFS
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/shortest-distance-in-a-binary-maze?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Dijkstra on the grid](#3-dijkstra-on-the-grid) · [4. BFS](#4-bfs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `n × m` grid of 0s and 1s, a `source` cell and a `destination` cell, return the minimum number of moves (up/down/left/right) from source to destination, visiting only cells with value 1. Return `-1` if it is impossible.

| Input | Output | Why |
|---|---|---|
| `grid = [[1,1,1,1],[1,1,0,1],[1,1,1,1],[1,1,0,0],[1,0,0,1]], src = (0,1), dst = (2,2)` | `3` | (0,1)→(1,1)→(2,1)→(2,2) |
| `grid = [[1,0,1]], src = (0,0), dst = (0,2)` | `-1` | the 0 blocks it |

**Constraints:** `1 ≤ n, m ≤ 500`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Dijkstra on the grid | heap of (dist, r, c) | O(nm log nm) | O(nm) |
| BFS | distance grid; first discovery is final | O(nm) | O(nm) |

> [!tip] Interview angle
> Ask: is the source itself guaranteed to be 1? Does `src == dst` return 0? Then say 'unit weights ⇒ BFS', and explain why Striver's Dijkstra framing collapses into a queue.

---

## 3. Dijkstra on the grid

**Intuition.** Treat each move as a weight-1 edge and run heap Dijkstra over cells. Correct, with a needless log factor.

```python
import heapq

def maze_dijkstra(grid, src, dst):
    n, m = len(grid), len(grid[0])
    if grid[src[0]][src[1]] == 0 or grid[dst[0]][dst[1]] == 0:
        return -1
    INF = float('inf')
    d = [[INF] * m for _ in range(n)]
    d[src[0]][src[1]] = 0
    pq = [(0, src[0], src[1])]
    while pq:
        k, r, c = heapq.heappop(pq)
        if [r, c] == list(dst):
            return k
        if k > d[r][c]:
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = r + dr, c + dc
            if 0 <= x < n and 0 <= y < m and grid[x][y] == 1 and k + 1 < d[x][y]:
                d[x][y] = k + 1
                heapq.heappush(pq, (k + 1, x, y))
    return -1
```

**Complexity:** time **O(nm log nm)**, space **O(nm)**.

---

## 4. BFS

**Intuition.** BFS from the source over 1-cells, storing distances in a grid initialised to −1. Return the destination's distance.

**Algorithm**

1. If source or destination is 0, return −1.
2. `dist[src] = 0`; enqueue `src`.
3. Pop `(r, c)`; for each in-bounds 1-neighbour with `dist = −1`: set `dist + 1`, enqueue.
4. Return `dist[dst]`.

**Dry run** — Example 1: (0,1)=0 → (1,1),(0,0),(0,2)=1 → (2,1)=2 → (2,2)=3.

**C++**
```cpp
int shortestMaze(vector<vector<int>>& grid, vector<int> src, vector<int> dst) {
    int n = grid.size(), m = grid[0].size();
    if (!grid[src[0]][src[1]] || !grid[dst[0]][dst[1]]) return -1;
    vector<vector<int>> dist(n, vector<int>(m, -1));
    dist[src[0]][src[1]] = 0;
    queue<pair<int, int>> q; q.push({src[0], src[1]});
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        for (int k = 0; k < 4; k++) {
            int x = r + dr[k], y = c + dc[k];
            if (x >= 0 && x < n && y >= 0 && y < m && grid[x][y] == 1 && dist[x][y] == -1) {
                dist[x][y] = dist[r][c] + 1;
                q.push({x, y});
            }
        }
    }
    return dist[dst[0]][dst[1]];
}
```

**Java**
```java
static int shortestMaze(int[][] grid, int[] src, int[] dst) {
    int n = grid.length, m = grid[0].length;
    if (grid[src[0]][src[1]] == 0 || grid[dst[0]][dst[1]] == 0) return -1;
    int[][] dist = new int[n][m];
    for (int[] row : dist) Arrays.fill(row, -1);
    dist[src[0]][src[1]] = 0;
    ArrayDeque<int[]> q = new ArrayDeque<>();
    q.add(new int[]{src[0], src[1]});
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    while (!q.isEmpty()) {
        int[] t = q.poll();
        for (int k = 0; k < 4; k++) {
            int x = t[0] + dr[k], y = t[1] + dc[k];
            if (x >= 0 && x < n && y >= 0 && y < m && grid[x][y] == 1 && dist[x][y] == -1) {
                dist[x][y] = dist[t[0]][t[1]] + 1;
                q.add(new int[]{x, y});
            }
        }
    }
    return dist[dst[0]][dst[1]];
}
```

**Python**
```python
from collections import deque

def shortest_maze(grid, src, dst):
    n, m = len(grid), len(grid[0])
    if grid[src[0]][src[1]] == 0 or grid[dst[0]][dst[1]] == 0:
        return -1
    dist = [[-1] * m for _ in range(n)]
    dist[src[0]][src[1]] = 0
    q = deque([(src[0], src[1])])
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = r + dr, c + dc
            if 0 <= x < n and 0 <= y < m and grid[x][y] == 1 and dist[x][y] == -1:
                dist[x][y] = dist[r][c] + 1
                q.append((x, y))
    return dist[dst[0]][dst[1]]
```

**Complexity:** time **O(nm)**, space **O(nm)** — each cell is enqueued at most once.

---

## Edge cases

- `src == dst`: 0.
- Source or destination is 0: −1.
- 1×1 grid.

---

## Common mistakes

1. Allowing diagonal moves (LC 1091 allows 8 directions; this problem doesn't).
2. Not checking the destination cell's value.
3. Marking visited on pop.

---

## Follow-ups

1. LC 1091 (8 directions, count cells not moves)?
2. Can remove up to k obstacles (LC 1293)?

<details><summary>Answer sketches</summary>

**#1:** Same BFS with 8 offsets; the answer is moves + 1.

**#2:** BFS over states `(r, c, k_left)`.
</details>

---

## Flashcards

**Unit-cost grid shortest path?** #flashcard
BFS (Dijkstra degenerates to it).

**Why does Dijkstra = BFS for unit weights?** #flashcard
Distances enter the heap in non-decreasing order, like a FIFO queue.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
