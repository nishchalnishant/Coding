---
module: 01-data-structures
topic: Matrix / Grid
tags: [data-structures, matrix, grid, bfs, dfs]
---

← [DS index](./README.md) · [DS decision tree](./ds_tree.md)
## First-Principles Map

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Highly probable; know the core patterns cold.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Know it conceptually.

> [!important] The single most useful reframe
> **A grid is a graph.** Each cell is a node; its 4 (or 8) in-bounds neighbours are its edges. Once you see that, "number of islands" is connected components, "rotting oranges" is multi-source BFS, and "shortest path in binary matrix" is plain BFS. You are not learning a new data structure — you are learning that graph algorithms already cover this, with the adjacency list computed on the fly instead of stored.

```text
WHY Matrix problems exist
├── 2D grids are the most natural implicit graph — adjacency is arithmetic, not storage
│   ├── Neighbours of (r,c) are (r±1,c) and (r,c±1) — no edge list needed
│   └── V = m·n, E ≈ 2mn → any O(V+E) graph algorithm is O(m·n) here
WHAT it is
├── An m×n array where position encodes adjacency
│   ├── As a graph      → BFS / DFS / union-find over cells
│   ├── As a DP table   → dp[r][c] built from dp[r-1][c], dp[r][c-1]
│   └── As pure indexing→ spiral, rotate, transpose — no traversal, just coordinate algebra
HOW it works
├── Traversal: queue/stack of (r,c); mark visited on ENQUEUE not dequeue
│   ├── Multi-source BFS: seed the queue with ALL sources → distances computed in one pass
│   └── In-place marking: overwrite the cell to avoid an O(mn) visited set
├── DP on grid: dp[r][c] = f(dp[r-1][c], dp[r][c-1]) → row-rolling gives O(n) space
└── Coordinate tricks: transpose + reverse rows = rotate 90°; layer-by-layer = spiral
WHEN to use
├── "count regions / islands / connected areas"    → DFS/BFS flood fill or union-find
├── "shortest path / minimum steps on a grid"      → BFS (unweighted) — never DFS
├── "spread simultaneously from several starts"    → multi-source BFS
├── "paths from corner to corner / min path sum"   → grid DP
└── "rotate / spiral / transpose"                  → index manipulation, no search
WHAT can go wrong
├── Bounds check written after the array access → IndexError; check before dereferencing
├── Marking visited on dequeue → the same cell is enqueued many times → TLE / blowup
├── Using DFS for shortest path → finds *a* path, not the shortest
├── Mutating the input grid when the caller needs it intact → ask before doing this
└── Forgetting 8-directional when the problem says diagonal moves count
DECISION
├── Shortest / fewest steps        → BFS
├── Reachability / count regions   → DFS or union-find (either is fine)
├── Count paths / optimise a path  → DP
└── Rearrange in place             → index algebra
```

## First-Principles Breakdown

- **Root problem**: Answer reachability, distance, or optimisation questions over a 2D layout without materialising an explicit graph.
- **Core insight**: Adjacency in a grid is computable from coordinates, so the graph is *implicit* — you get O(V+E) algorithms with zero graph-construction cost. The direction array `[(0,1),(1,0),(0,-1),(-1,0)]` **is** your adjacency list.
- **Invariant (BFS)**: Cells are dequeued in non-decreasing distance from the source set, so the first time you reach a cell you have reached it optimally — which is exactly why BFS gives shortest paths and DFS does not.
- **Why it works**: Every cell is visited at most once when marked correctly, so traversal is O(m·n) regardless of grid shape.
- **Where it breaks**: Weighted moves (cost varies per cell) break plain BFS — that needs Dijkstra or 0-1 BFS with a deque. Constraints that depend on path history (e.g. "at most k obstacles removed") require adding that state to the visited key, turning the node into `(r, c, k)`.

---

# Matrix / Grid

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
