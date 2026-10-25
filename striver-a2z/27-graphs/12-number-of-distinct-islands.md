---
module: striver-a2z/27-graphs
lesson: 12
topic: Number of distinct islands
difficulty: Medium
source: https://takeuforward.org/learning/dsa/number-of-distinct-islands?category=traversal-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, grid, dfs, hashing]
---
# 12. Number of distinct islands

← [Surrounded Regions](11-surrounded-regions.md) · [Part 27 index](README.md) · Next → [Detect a cycle in an undirected graph](13-cycle-in-undirected-graph.md)

> [!abstract] Problem at a glance
> **Task:** Count islands with distinct shapes, where two islands are the same if one is a translation of the other (no rotation or reflection).
> **Key insight:** Translate each island so its **first-visited cell** sits at the origin. The scan reaches every island at its top-most, left-most cell, so this is a canonical anchor. Then two islands have the same shape exactly when they produce the same list of relative coordinates (in the same DFS order). Put each list, as a tuple, into a set.
> **Difficulty:** Medium · **Pattern:** Grid DFS + canonical shape hashing · **Also on:** LC 694 (premium)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-distinct-islands?category=traversal-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS path signature](#3-dfs-path-signature) · [4. Relative coordinates](#4-relative-coordinates) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `m × n` binary grid, an island is a 4-directionally connected group of `1`s. Two islands are identical if one can be translated (not rotated or reflected) to equal the other. Return the number of distinct islands.

| Input | Output | Why |
|---|---|---|
| `grid = [[1,1,0,0,0],[1,1,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]` | `1` | two identical 2×2 squares |
| `grid = [[1,1,0,1,1],[1,0,0,0,0],[0,0,0,0,1],[1,1,0,1,1]]` | `3` | the two L-shapes differ in orientation, so they count separately |

**Constraints:** `1 ≤ m, n ≤ 50`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS path signature | record direction letters + a back marker | O(m·n) | O(m·n) |
| Relative coordinates | store (r − r0, c − c0) of every cell in DFS order | O(m·n) | O(m·n) |

> [!tip] Interview angle
> The interviewer wants to hear why the encoding is canonical: same anchor (first cell in scan order) plus a deterministic DFS order means equal shapes produce equal sequences. A path signature must also record **backtracking**, or different shapes can collide.

---

## 3. DFS path signature

**Intuition.** Encode the DFS walk itself. Append the direction taken into each cell (`D U R L`) and a `b` when returning from it. The backtrack markers make the encoding unambiguous: without them, a straight line and an L-shape can produce the same letter sequence.

```python
import sys

def distinct_islands_path(grid):
    sys.setrecursionlimit(10 ** 6)
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    shapes = set()
    def dfs(r, c, d, path):
        if r < 0 or r >= R or c < 0 or c >= C or seen[r][c] or grid[r][c] != 1:
            return
        seen[r][c] = True
        path.append(d)
        dfs(r + 1, c, 'D', path); dfs(r - 1, c, 'U', path)
        dfs(r, c + 1, 'R', path); dfs(r, c - 1, 'L', path)
        path.append('b')
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1 and not seen[r][c]:
                path = []
                dfs(r, c, 'o', path)
                shapes.add(''.join(path))
    return len(shapes)
```

**Complexity:** time **O(m·n)**, space **O(m·n)**.

---

## 4. Relative coordinates

**Intuition.** For each island found by the scan at `(r0, c0)`, DFS in a fixed neighbour order and record `(r − r0, c − c0)` for each cell. Identical shapes start at the same relative cell and visit cells in the same order, so their lists match exactly. Insert the list into a set.

**Algorithm**

1. Scan cells; on an unvisited `1` at `(r0, c0)`, start a DFS with an empty list.
2. DFS (fixed order: down, up, right, left) appends `(r − r0, c − c0)` for every visited cell.
3. Insert the list into a set of shapes.
4. Return the set size.

**Dry run** — Example 1: first square anchored at (0,0) → [(0,0),(1,0),(1,1),(0,1)]. Second at (2,3) → the same offsets → set size 1.

**C++**
```cpp
int distinctIslands(vector<vector<int>>& grid) {
    int R = grid.size(), C = grid[0].size();
    vector<vector<bool>> seen(R, vector<bool>(C, false));
    set<vector<pair<int, int>>> shapes;
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    for (int r0 = 0; r0 < R; r0++)
        for (int c0 = 0; c0 < C; c0++) {
            if (grid[r0][c0] != 1 || seen[r0][c0]) continue;
            vector<pair<int, int>> shape, st = {{r0, c0}};
            seen[r0][c0] = true;
            while (!st.empty()) {
                auto [r, c] = st.back(); st.pop_back();
                shape.push_back({r - r0, c - c0});
                for (int d = 0; d < 4; d++) {
                    int a = r + dr[d], b = c + dc[d];
                    if (a >= 0 && a < R && b >= 0 && b < C && grid[a][b] == 1 && !seen[a][b]) {
                        seen[a][b] = true; st.push_back({a, b});
                    }
                }
            }
            shapes.insert(shape);
        }
    return shapes.size();
}
```

**Java**
```java
static int distinctIslands(int[][] grid) {
    int R = grid.length, C = grid[0].length;
    boolean[][] seen = new boolean[R][C];
    Set<String> shapes = new HashSet<>();
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    for (int r0 = 0; r0 < R; r0++)
        for (int c0 = 0; c0 < C; c0++) {
            if (grid[r0][c0] != 1 || seen[r0][c0]) continue;
            StringBuilder shape = new StringBuilder();
            ArrayDeque<int[]> st = new ArrayDeque<>();
            st.push(new int[]{r0, c0});
            seen[r0][c0] = true;
            while (!st.isEmpty()) {
                int[] p = st.pop();
                shape.append(p[0] - r0).append(',').append(p[1] - c0).append(';');
                for (int d = 0; d < 4; d++) {
                    int a = p[0] + dr[d], b = p[1] + dc[d];
                    if (a >= 0 && a < R && b >= 0 && b < C && grid[a][b] == 1 && !seen[a][b]) {
                        seen[a][b] = true; st.push(new int[]{a, b});
                    }
                }
            }
            shapes.add(shape.toString());
        }
    return shapes.size();
}
```

**Python**
```python
def distinct_islands(grid):
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    shapes = set()
    for r0 in range(R):
        for c0 in range(C):
            if grid[r0][c0] != 1 or seen[r0][c0]:
                continue
            shape, st = [], [(r0, c0)]
            seen[r0][c0] = True
            while st:
                r, c = st.pop()
                shape.append((r - r0, c - c0))
                for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= a < R and 0 <= b < C and grid[a][b] == 1 and not seen[a][b]:
                        seen[a][b] = True
                        st.append((a, b))
            shapes.add(tuple(shape))
    return len(shapes)
```

**Complexity:** time **O(m·n)**, space **O(m·n)** — each cell is visited once; the set stores O(m·n) coordinates in total.

---

## Edge cases

- No land: 0.
- All single cells: 1 distinct shape.
- Mirror images: distinct under translation-only equality.

---

## Common mistakes

1. Using absolute coordinates, so equal shapes never match.
2. Path signature without backtrack markers, so different shapes collide.
3. Using an unordered set of offsets per island in C++/Java but hashing a list (order-dependent): pick one canonical form and stick to it.

---

## Follow-ups

1. Rotations and reflections count as the same (LC 711)?
2. Why is the DFS order deterministic for equal shapes?

<details><summary>Answer sketches</summary>

**#1:** Generate all 8 transforms of the offsets, normalise each (sort, shift to its min), and use the lexicographically smallest as the key.

**#2:** Same anchor, same neighbour order, same relative layout → the traversal makes identical choices.
</details>

---

## Flashcards

**Canonical island shape?** #flashcard
Offsets from the first-scanned cell, recorded in a fixed DFS order.

**Why do path signatures need backtrack markers?** #flashcard
Without them, different shapes can yield the same move string.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
