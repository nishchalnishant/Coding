---
module: striver/27-graphs
lesson: 9
topic: Rotten Oranges
difficulty: Medium
source: https://takeuforward.org/learning/dsa/rotten-oranges?category=traversal-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, grid, bfs, multi-source]
---
# 9. Rotten Oranges

← [Number of enclaves](08-number-of-enclaves.md) · [Part 27 index](README.md) · Next → [Distance of nearest cell having one](10-distance-of-nearest-cell-having-1.md)

> [!abstract] Problem at a glance
> **Task:** Each minute, rotten oranges (`2`) rot their 4-neighbour fresh oranges (`1`). Return the minutes until none are fresh, or `-1` if some never rot.
> **Key insight:** All rotten oranges spread **simultaneously**, which is exactly multi-source BFS: put every rotten orange in the queue at time 0. An orange's BFS level is the minute it rots, and the answer is the last level reached. Count fresh oranges up front; if any are left after the BFS, return −1.
> **Difficulty:** Medium · **Pattern:** Multi-source BFS (levels = time) · **Also on:** LC 994
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/rotten-oranges?category=traversal-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Minute-by-minute simulation](#3-minute-by-minute-simulation) · [4. Multi-source BFS](#4-multi-source-bfs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

In an `m × n` grid, `0` = empty, `1` = fresh orange, `2` = rotten orange. Every minute, any fresh orange 4-directionally adjacent to a rotten one becomes rotten. Return the minimum number of minutes until no fresh orange remains, or `-1` if that is impossible.

| Input | Output | Why |
|---|---|---|
| `grid = [[2,1,1],[1,1,0],[0,1,1]]` | `4` | the rot reaches (2,2) last, at minute 4 |
| `grid = [[2,1,1],[0,1,1],[1,0,1]]` | `-1` | (2,0) is isolated |
| `grid = [[0,2]]` | `0` | no fresh oranges at the start |

**Constraints:** `1 ≤ m, n ≤ 10`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Minute-by-minute simulation | scan the grid each minute, rot neighbours of rotten | O((m·n)²) | O(m·n) |
| Multi-source BFS | queue all rotten at t = 0; process level by level | O(m·n) | O(m·n) |

> [!tip] Interview angle
> Explain why one BFS from each rotten orange separately is wrong (or slow): the sources act at the same time. Seeding them all into one queue makes each fresh orange's BFS distance equal to its distance to the nearest source.

---

## 3. Minute-by-minute simulation

**Intuition.** Each minute, collect every fresh orange adjacent to a rotten one, rot them together, and count the minute. Stop when nothing changes. Up to m·n rounds, each scanning the grid.

```python
def oranges_rotting_sim(grid):
    R, C = len(grid), len(grid[0])
    t = 0
    while True:
        new = [(r, c) for r in range(R) for c in range(C) if grid[r][c] == 1 and any(
            0 <= a < R and 0 <= b < C and grid[a][b] == 2
            for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))]
        if not new:
            break
        for r, c in new:
            grid[r][c] = 2
        t += 1
    return -1 if any(1 in row for row in grid) else t
```

**Complexity:** time **O((m·n)²)**, space **O(m·n)**.

---

## 4. Multi-source BFS

**Intuition.** Seed the queue with every rotten cell and count the fresh ones. Process the queue one level at a time. Each fresh neighbour becomes rotten, the fresh count drops, and the cell is pushed. Each completed level that rotted something is one minute.

**Algorithm**

1. Push every `2`; count `fresh` = number of `1`s.
2. `minutes = 0`. While the queue is non-empty and `fresh > 0`: process exactly the current queue size.
3. For each popped cell, rot every fresh neighbour (`fresh--`, push it).
4. After the level, `minutes++`.
5. Return `minutes` if `fresh == 0`, else `-1`.

**Dry run** — [[2,1,1],[1,1,0],[0,1,1]], fresh = 6. Level 1: (0,1),(1,0). Level 2: (0,2),(1,1). Level 3: (2,1). Level 4: (2,2). fresh = 0 → 4.

**C++**
```cpp
int orangesRotting(vector<vector<int>>& grid) {
    int R = grid.size(), C = grid[0].size(), fresh = 0;
    queue<pair<int, int>> q;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (grid[r][c] == 2) q.push({r, c});
            else if (grid[r][c] == 1) fresh++;
        }
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1}, minutes = 0;
    while (!q.empty() && fresh > 0) {
        for (int k = q.size(); k > 0; k--) {
            auto [r, c] = q.front(); q.pop();
            for (int d = 0; d < 4; d++) {
                int a = r + dr[d], b = c + dc[d];
                if (a >= 0 && a < R && b >= 0 && b < C && grid[a][b] == 1) {
                    grid[a][b] = 2; fresh--; q.push({a, b});
                }
            }
        }
        minutes++;
    }
    return fresh == 0 ? minutes : -1;
}
```

**Java**
```java
static int orangesRotting(int[][] grid) {
    int R = grid.length, C = grid[0].length, fresh = 0;
    ArrayDeque<int[]> q = new ArrayDeque<>();
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (grid[r][c] == 2) q.add(new int[]{r, c});
            else if (grid[r][c] == 1) fresh++;
        }
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    int minutes = 0;
    while (!q.isEmpty() && fresh > 0) {
        for (int k = q.size(); k > 0; k--) {
            int[] p = q.poll();
            for (int d = 0; d < 4; d++) {
                int a = p[0] + dr[d], b = p[1] + dc[d];
                if (a >= 0 && a < R && b >= 0 && b < C && grid[a][b] == 1) {
                    grid[a][b] = 2; fresh--; q.add(new int[]{a, b});
                }
            }
        }
        minutes++;
    }
    return fresh == 0 ? minutes : -1;
}
```

**Python**
```python
from collections import deque

def oranges_rotting(grid):
    R, C = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):
            r, c = q.popleft()
            for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= a < R and 0 <= b < C and grid[a][b] == 1:
                    grid[a][b] = 2
                    fresh -= 1
                    q.append((a, b))
        minutes += 1
    return minutes if fresh == 0 else -1
```

**Complexity:** time **O(m·n)**, space **O(m·n)** — each cell enters the queue at most once.

---

## Edge cases

- No fresh oranges: 0 (even with no rotten ones).
- Fresh oranges but no rotten ones: −1.
- An isolated fresh orange: −1.

---

## Common mistakes

1. Looping `while q` without `fresh > 0`, which counts one extra minute for the final level that rots nothing.
2. Starting a BFS from each rotten orange separately.
3. Rotting during the level scan without the size snapshot, mixing minutes.

---

## Follow-ups

1. Return the time each orange rots?
2. Some cells are walls the rot cannot pass?

<details><summary>Answer sketches</summary>

**#1:** Keep `time[r][c]` set at push time instead of level counting.

**#2:** They are just `0`s: skipped by the neighbour check.
</details>

---

## Flashcards

**Simultaneous spread from many sources = ?** #flashcard
Multi-source BFS: seed every source at level 0.

**Why `while q and fresh`?** #flashcard
To avoid counting a final level that rots nothing.

**When to return −1?** #flashcard
Fresh oranges remain after the BFS.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
