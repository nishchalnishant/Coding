---
module: 01-data-structures
topic: Matrix / Grid
tags: [data-structures, matrix, grid, bfs, dfs]
---
# Matrix / Grid

← [DS index](./README.md) · [DS decision tree](./ds_tree.md)

## What this covers

> [!abstract] In this file
> **Covers:** Grids as implicit graphs: direction arrays, bounds checks, BFS/DFS flood fill, in-place transforms (rotate, spiral, set zeroes), grid DP.
> **You'll be able to:** Write a bug-free grid BFS/DFS template from memory; recognise when a grid problem is really shortest path, connected components or DP.
> **Prereqs:** Queue, recursion · **Pair with:** [Matrix problems](../coding/data-structures/04-matrix.md) · [Graphs](13-graphs.md) · **Time:** 1.5 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../coding/l3-google-roadmap.md#tier-legend))

**Sections:** [Core Idea](#core-idea) · [The Templates](#the-templates) · [Bounds checking](#bounds-checking) · [Decision Guide](#decision-guide) · [Interview Questions — Logic & Trickiness](#interview-questions--logic--trickiness) · [Flashcards](#flashcards)

---

## Core Idea

- **Root problem**: Answer reachability, distance, or optimisation questions over a 2D layout without materialising an explicit graph.
- **Core insight**: Adjacency in a grid is computable from coordinates, so the graph is *implicit* — you get O(V+E) algorithms with zero graph-construction cost. The direction array `[(0,1),(1,0),(0,-1),(-1,0)]` **is** your adjacency list.
- **Invariant (BFS)**: Cells are dequeued in non-decreasing distance from the source set, so the first time you reach a cell you have reached it optimally — which is exactly why BFS gives shortest paths and DFS does not.
- **Why it works**: Every cell is visited at most once when marked correctly, so traversal is O(m·n) regardless of grid shape.
- **Where it breaks**: Weighted moves (cost varies per cell) break plain BFS — that needs Dijkstra or 0-1 BFS with a deque. Constraints that depend on path history (e.g. "at most k obstacles removed") require adding that state to the visited key, turning the node into `(r, c, k)`.

---

### One-Page Map

```
[MATRIX — MINDMAP]
├── WHY IT EXISTS
│   └── Grid = implicit graph; adjacency is arithmetic
├── AS A GRAPH
│   ├── Flood fill (DFS/BFS)      → Number of Islands
│   ├── Multi-source BFS          → Rotting Oranges, Walls and Gates, 01 Matrix
│   ├── Shortest path BFS         → Shortest Path in Binary Matrix
│   └── Union-Find                → dynamic connectivity variants
├── AS A DP TABLE
│   ├── Path counting             → Unique Paths
│   ├── Path optimisation         → Minimum Path Sum
│   ├── Rectangle/square DP       → Maximal Square
│   └── Memo on cells             → Longest Increasing Path
├── AS PURE INDEXING
│   ├── Spiral Matrix             → shrinking boundaries
│   ├── Rotate Image              → transpose + reverse rows
│   └── Set Matrix Zeroes         → first row/col as marker storage
└── PREFIX STRUCTURES
    └── 2D prefix sum             → O(1) submatrix queries
```

> [!warning] Common mistakes
> - Marking visited on **dequeue** instead of enqueue — cells get pushed many times and BFS blows up.
> - Swapping `m`/`n` in bounds checks on non-square grids — `0 <= r < len(grid)`, `0 <= c < len(grid[0])`.
> - DFS for "shortest / fewest steps" — DFS returns *a* path, not the shortest; use BFS.
> - Running single-source BFS once per source — seed every source in one queue (multi-source BFS).
> - Mutating the input grid as a visited marker without saying so — ask first, or restore it.
> - Path-dependent constraints (obstacles removed, keys held) need the state in the visited key: `(r, c, k)`.

## The Templates

### 4-directional BFS — the workhorse

```python
from collections import deque

DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

def bfs(grid, sources):
    m, n = len(grid), len(grid[0])
    q = deque(sources)
    seen = set(sources)
    steps = 0
    while q:
        for _ in range(len(q)):            # level-by-level → steps is the distance
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen and grid[nr][nc] != BLOCKED:
                    seen.add((nr, nc))     # mark on ENQUEUE — this is the critical line
                    q.append((nr, nc))
        steps += 1
    return steps
```

**Multi-source is free.** Seed `q` with every source before the loop starts and every cell gets its distance to the *nearest* source in one pass. That single change turns this template into Rotting Oranges, Walls and Gates, and 01 Matrix.

### Flood fill — count the regions

```python
def num_islands(grid):
    m, n = len(grid), len(grid[0])
    def sink(r, c):
        if not (0 <= r < m and 0 <= c < n) or grid[r][c] != '1':
            return
        grid[r][c] = '0'                   # mark in place — no visited set needed
        for dr, dc in DIRS:
            sink(r + dr, c + dc)
    return sum(sink(r, c) or 1
               for r in range(m) for c in range(n) if grid[r][c] == '1')
```

Say out loud that you're mutating the input, and offer a `seen` set if the caller needs the grid preserved. Interviewers notice.

### Grid DP

```python
# dp[r][c] depends only on the row above and the cell to the left
for r in range(m):
    for c in range(n):
        dp[c] = grid[r][c] + min(dp[c],            # from above
                                 dp[c-1] if c else INF)   # from left
```

Rolling a single row gives O(n) space. Mention it even if you write the O(m·n) version.

---

## Bounds checking

Two idioms; pick one and use it consistently.

```python
if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == target:   # guard before access
```

```python
grid = [[SENTINEL] * (n + 2)] + [[SENTINEL] + row + [SENTINEL] for row in grid] + ...
```

The sentinel border removes bounds checks entirely, but costs O(m+n) extra memory and confuses the index arithmetic. **At L3, use the explicit guard** — it is what interviewers expect and it never produces an off-by-one on the padding.

---

## Decision Guide

| Prompt | Technique | Complexity |
|---|---|---|
| "How many islands / regions?" | DFS or BFS flood fill | O(mn) |
| "Fewest steps to reach X" | BFS | O(mn) |
| "Time until everything is infected" | Multi-source BFS | O(mn) |
| "Distance to nearest 0 for every cell" | Multi-source BFS from all 0s | O(mn) |
| "How many paths corner to corner" | DP | O(mn) |
| "Minimum path sum" | DP | O(mn) |
| "Largest square of 1s" | DP on min of three neighbours | O(mn) |
| "Longest increasing path" | DFS + memo (DAG, no visited set) | O(mn) |
| "Sum of any submatrix, many queries" | 2D prefix sum | O(mn) build, O(1) query |
| "Rotate / spiral / transpose" | Index algebra | O(mn) |
| "Islands, but edges appear over time" | Union-Find | O(mn·α) |

> [!tip] BFS vs DFS — the only rule you need
> **Shortest path → BFS. Always.** DFS finds *a* path and will happily return a wandering one. If the question says "minimum", "fewest", or "shortest", and moves are unweighted, it is BFS. If moves have different costs, it is Dijkstra.

---

Practice → [`coding/data-structures/04-matrix.md`](../coding/data-structures/04-matrix.md) (12 problems with full walkthroughs)

---

## Interview Questions — Logic & Trickiness

| Question | Variant | Click moment | Core logic | Gotchas |
|---|---|---|---|---|
| ⚡ T1 · Medium — Number of Islands (LC 200) | Flood fill | "count connected regions" | DFS/BFS from each unvisited `'1'`, count launches | Grid holds strings `'1'`, not ints |
| ⚡ T1 · Medium — Rotting Oranges (LC 994) | Multi-source BFS | "minutes until all…" | Seed all rotten, BFS by levels | Return `-1` if fresh remain; `0` if none at start |
| ⚡ T1 · Medium — Spiral Matrix (LC 54) | Index algebra | "print in spiral order" | Four shrinking bounds `top/bot/left/right` | Re-check `top <= bot` / `left <= right` before the reverse passes |
| ⚡ T1 · Medium — Rotate Image (LC 48) | Index algebra | "in place, 90°" | Transpose, then reverse rows | Transpose only `c > r`, or you swap back |
| ⚡ T1 · Medium — Set Matrix Zeroes (LC 73) | Marker storage | "O(1) extra space" | Use row 0 / col 0 as flags | Separate flag for whether col 0 itself had a zero |
| 🎯 T2 · Medium — 01 Matrix (LC 542) | Multi-source BFS | "distance to nearest 0 for every cell" | Seed all 0s, BFS outward | Running BFS from every 1 is O((mn)²) |
| 🎯 T2 · Medium — Pacific Atlantic Water Flow (LC 417) | Reverse BFS | "can reach both borders" | BFS uphill from each ocean, intersect | Searching downhill from every cell is O((mn)²) |
| 🎯 T2 · Medium — Maximal Square (LC 221) | Grid DP | "largest square of 1s" | `dp = 1 + min(up, left, diag)` | Returns side; answer is area `side²` |
| 🎯 T2 · Hard — Longest Increasing Path (LC 329) | DFS + memo | Strictly increasing ⇒ DAG | Memoize `dfs(r,c)`; no visited set needed | A visited set is unnecessary *because* of the strict order |
| 💤 T3 · Hard — Shortest Path with Obstacle Elimination (LC 1293) | State BFS | "remove at most k" | BFS on `(r, c, k_left)` | Visited must include `k` |

---

## Flashcards

**Grid shortest path vs. reachability — which traversal, and why?** #flashcard
BFS for shortest/fewest-steps (dequeue order is non-decreasing distance, so first arrival is optimal); DFS or union-find for "count regions" where any path suffices. DFS finds *a* path, not the shortest.

**Why must a BFS mark cells visited on enqueue rather than dequeue?** #flashcard
Marking on dequeue lets the same cell be pushed once per neighbour before it is ever processed, so the queue blows up and the traversal degrades from O(mn) toward exponential. Marking on enqueue guarantees each cell enters the queue exactly once.

**What single change turns a plain grid BFS into Rotting Oranges / Walls and Gates / 01 Matrix?** #flashcard
Seed the queue with *every* source before the loop starts. Multi-source BFS then computes each cell's distance to the *nearest* source in one pass — no per-source reruns.

**Grid DP is O(m·n) space by default — when can you compress to O(n), and when does that break?** #flashcard
Compress to a single rolling row whenever `dp[r][c]` depends only on `dp[r-1][*]` and `dp[r][c-1]`. It breaks when the recurrence reads a row you have already overwritten — e.g. Dungeon Game, which fills bottom-up right-to-left.

**A grid problem adds "you may remove at most k obstacles." What changes?** #flashcard
The node is no longer a cell but a state: `(r, c, k_remaining)`. Bound the visited set on that triple. Plain BFS over cells is wrong because the same cell is worth revisiting with more budget left.

**Rotate an m×n matrix 90° clockwise in place — what is the two-step trick?** #flashcard
Transpose (swap `M[r][c]` with `M[c][r]`), then reverse each row. Reversing columns instead gives 90° counter-clockwise.

---

## See Also

[[graph]] | [[array]] | [[dynamic-programming]] | [[union-find]] | [[queue]]
