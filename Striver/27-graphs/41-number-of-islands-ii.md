---
module: striver/27-graphs
lesson: 41
topic: Number of islands II
difficulty: Hard
source: https://takeuforward.org/learning/dsa/number-of-islands-ii?category=hard-problems-ii&source=strivers-a2z-dsa-sheet
tags: [striver, graph, union-find, matrix, online]
---
# 41. Number of islands II

← [Accounts merge](40-accounts-merge.md) · [Part 27 index](README.md) · Next → [Making a large island](42-making-a-large-island.md)

> [!abstract] Problem at a glance
> **Task:** Cells of an all-water `n × m` grid turn into land one at a time; after each operation report the number of islands.
> **Key insight:** Adding land is a union-only process, so the count can be maintained online: a new cell adds one island, and each union with a **different** neighbouring island subtracts one. Encode cell `(r, c)` as `r·m + c`. Re-adding an existing land cell changes nothing.
> **Difficulty:** Hard · **Pattern:** Online DSU on a grid · **Also on:** LC 305
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-islands-ii?category=hard-problems-ii&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recount after every operation](#3-recount-after-every-operation) · [4. Online DSU](#4-online-dsu) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

An `n × m` grid starts as water. `operators[i] = [r, c]` turns cell `(r, c)` into land. Return a list where element `i` is the number of islands (4-directionally connected land) after operation `i`.

| Input | Output | Why |
|---|---|---|
| `n = 4, m = 5, ops = [[1,1],[0,1],[3,3],[3,4]]` | `[1,1,2,2]` | (0,1) joins (1,1); (3,4) joins (3,3) |
| `n = 3, m = 3, ops = [[0,0],[0,1],[1,2],[2,1]]` | `[1,1,2,3]` |  |

**Constraints:** `1 ≤ n, m ≤ 1000`, `1 ≤ k ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recount after every operation | add the cell, BFS-count islands | O(k·n·m) | O(n·m) |
| Online DSU | new cell +1; each union with a distinct neighbour −1 | O(n·m + k·α) | O(n·m) |

> [!tip] Interview angle
> Lead with the brute force (BFS after each op, O(k·nm)) to show you see why it's too slow, then the incremental argument. The most common bug is the repeated cell: say out loud that you skip it.

---

## 3. Recount after every operation

**Intuition.** Correct but re-scans the grid each time: up to 10⁴ · 10⁶ operations.

```python
def num_of_islands_bfs(n, m, operators):
    grid = [[0] * m for _ in range(n)]
    out = []
    for r, c in operators:
        grid[r][c] = 1
        seen = [[False] * m for _ in range(n)]
        cnt = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] and not seen[i][j]:
                    cnt += 1
                    seen[i][j] = True
                    st = [(i, j)]
                    while st:
                        x, y = st.pop()
                        for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                            if 0 <= a < n and 0 <= b < m and grid[a][b] and not seen[a][b]:
                                seen[a][b] = True
                                st.append((a, b))
        out.append(cnt)
    return out
```

**Complexity:** time **O(k·n·m)**, space **O(n·m)**.

---

## 4. Online DSU

**Intuition.** Keep a `land` grid and a DSU over `n·m` ids. On a new land cell, `count += 1`, then for each land neighbour whose root differs from the cell's root, union and `count −= 1`. Append `count`.

**Algorithm**

1. DSU over `n·m`; `land` all false; `count = 0`.
2. For `(r, c)`: if already land, append `count` and continue.
3. Mark land, `count += 1`, `id = r·m + c`.
4. For each of 4 neighbours on land: if `find(id) != find(nid)`, union, `count −= 1`.
5. Append `count`.

**Dry run** — Example 1: (1,1) → 1. (0,1): +1 → 2, neighbour (1,1) differs → union → 1. (3,3) → 2. (3,4): +1 → 3, union with (3,3) → 2. Output [1,1,2,2].

**C++**
```cpp
vector<int> numOfIslands(int n, int m, vector<vector<int>>& operators) {
    vector<int> parent(n * m);
    iota(parent.begin(), parent.end(), 0);
    function<int(int)> find = [&](int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); };
    vector<vector<bool>> land(n, vector<bool>(m, false));
    int count = 0, dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    vector<int> out;
    for (auto& op : operators) {
        int r = op[0], c = op[1];
        if (land[r][c]) { out.push_back(count); continue; }
        land[r][c] = true;
        count++;
        int id = r * m + c;
        for (int d = 0; d < 4; d++) {
            int x = r + dr[d], y = c + dc[d];
            if (x < 0 || y < 0 || x >= n || y >= m || !land[x][y]) continue;
            int a = find(id), b = find(x * m + y);
            if (a != b) { parent[a] = b; count--; }
        }
        out.push_back(count);
    }
    return out;
}
```

**Java**
```java
static int[] parent;
static int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
static List<Integer> numOfIslands(int n, int m, int[][] operators) {
    parent = new int[n * m];
    for (int i = 0; i < n * m; i++) parent[i] = i;
    boolean[][] land = new boolean[n][m];
    int count = 0;
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    List<Integer> out = new ArrayList<>();
    for (int[] op : operators) {
        int r = op[0], c = op[1];
        if (land[r][c]) { out.add(count); continue; }
        land[r][c] = true;
        count++;
        int id = r * m + c;
        for (int d = 0; d < 4; d++) {
            int x = r + dr[d], y = c + dc[d];
            if (x < 0 || y < 0 || x >= n || y >= m || !land[x][y]) continue;
            int a = find(id), b = find(x * m + y);
            if (a != b) { parent[a] = b; count--; }
        }
        out.add(count);
    }
    return out;
}
```

**Python**
```python
def num_of_islands(n, m, operators):
    parent = list(range(n * m))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    land = [[False] * m for _ in range(n)]
    count, out = 0, []
    for r, c in operators:
        if land[r][c]:
            out.append(count)
            continue
        land[r][c] = True
        count += 1
        cid = r * m + c
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < n and 0 <= y < m and land[x][y]:
                a, b = find(cid), find(x * m + y)
                if a != b:
                    parent[a] = b
                    count -= 1
        out.append(count)
    return out
```

**Complexity:** time **O(n·m + k·α)**, space **O(n·m)** — O(n·m) to initialise the DSU, then 4 near-constant unions per operation.

---

## Edge cases

- Repeated cell: answer unchanged.
- 1 × 1 grid.
- A new cell bridging 3–4 existing islands: each distinct root subtracts one (re-`find` after every union).

---

## Common mistakes

1. Not skipping repeated cells (count goes up by one wrongly).
2. Comparing the neighbour's root against a stale root of the new cell computed before earlier unions.
3. Encoding `r·n + c` instead of `r·m + c` on non-square grids.

---

## Follow-ups

1. Cells can also turn back into water?
2. Grid is 10⁹ × 10⁹, k = 10⁴?

<details><summary>Answer sketches</summary>

**#1:** DSU can't delete; process offline in reverse (removals become additions) or use a dynamic connectivity structure.

**#2:** Allocate DSU nodes lazily with a hash map keyed by the cell.
</details>

---

## Flashcards

**Islands II per-op update?** #flashcard
+1 for the new cell, −1 per successful union with a land neighbour.

**Islands II repeated cell?** #flashcard
Skip: count unchanged.

**Interview track →** [Union-find deep-dive](../../02-algorithms/14-union-find.md)
