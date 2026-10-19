---
module: striver/27-graphs
lesson: 42
topic: Making a large island
difficulty: Hard
source: https://takeuforward.org/learning/dsa/making-a-large-island?category=hard-problems-ii&source=strivers-a2z-dsa-sheet
tags: [striver, graph, union-find, matrix]
---
# 42. Making a large island

← [Number of islands II](41-number-of-islands-ii.md) · [Part 27 index](README.md) · Next → [Most stones removed with same row or column](43-most-stones-removed-with-same-row-or-column.md)

> [!abstract] Problem at a glance
> **Task:** In an `n × n` 0/1 grid you may flip at most one 0 to 1; return the largest possible island area.
> **Key insight:** Label every island once (DSU or DFS) and store its size. Flipping a 0 creates `1 + sum of sizes of the **distinct** islands among its 4 neighbours`. Use a set of roots so an island touching the cell on two sides isn't counted twice. If there is no 0, the answer is `n²`.
> **Difficulty:** Hard · **Pattern:** Component labelling + distinct-root sum · **Also on:** LC 827
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/making-a-large-island?category=hard-problems-ii&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Flip each 0 and recount](#3-flip-each-0-and-recount) · [4. DSU sizes + distinct neighbour roots](#4-dsu-sizes--distinct-neighbour-roots) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`grid` is `n × n` with 0 (water) and 1 (land). Change at most one 0 to 1. Return the size of the largest island (4-directional) after the change.

| Input | Output | Why |
|---|---|---|
| `[[1,0],[0,1]]` | `3` | flip either 0 |
| `[[1,1],[1,0]]` | `4` |  |
| `[[1,1],[1,1]]` | `4` | no 0 to flip |

**Constraints:** `1 ≤ n ≤ 500`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Flip each 0 and recount | for every 0, set to 1 and find max island by DFS | O(n⁴) | O(n²) |
| DSU sizes + distinct neighbour roots | union all land; each 0 scores 1 + Σ distinct neighbour sizes | O(n²·α) | O(n²) |

> [!tip] Interview angle
> Say the two-pass plan up front: pass 1 builds island sizes, pass 2 evaluates each 0 in O(1). The two must-mention details are the distinct-root set and the all-ones case. DFS labelling is equally fine; DSU is what Striver uses.

---

## 3. Flip each 0 and recount

**Intuition.** Each of up to n² zeros triggers an O(n²) flood fill: ~6·10¹⁰ at n = 500.

```python
def largest_island_bf(grid):
    n = len(grid)
    def max_area():
        seen = [[False] * n for _ in range(n)]
        best = 0
        for i in range(n):
            for j in range(n):
                if grid[i][j] and not seen[i][j]:
                    seen[i][j] = True
                    st, a = [(i, j)], 0
                    while st:
                        x, y = st.pop()
                        a += 1
                        for p, q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                            if 0 <= p < n and 0 <= q < n and grid[p][q] and not seen[p][q]:
                                seen[p][q] = True
                                st.append((p, q))
                    best = max(best, a)
        return best
    best = max_area()
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                grid[i][j] = 1
                best = max(best, max_area())
                grid[i][j] = 0
    return best
```

**Complexity:** time **O(n⁴)**, space **O(n²)**.

---

## 4. DSU sizes + distinct neighbour roots

**Intuition.** Pass 1: union every land cell with its land neighbours (right and down suffice); `sz[root]` is each island's area. Pass 2: for each 0, collect the roots of its land neighbours in a small set and score `1 + Σ sz[root]`. Answer = max over all scores and over existing island sizes.

**Algorithm**

1. DSU over `n²`, union adjacent 1s.
2. `best = max(sz[find(id)])` over land cells (covers the no-zero case).
3. For each 0: `roots = {find(nb)}` for land neighbours; `best = max(best, 1 + Σ sz[r])`.
4. Return `best`.

**Dry run** — [[1,1],[1,0]]: island {(0,0),(0,1),(1,0)} size 3. Cell (1,1): neighbours (0,1) and (1,0) share one root → 1 + 3 = 4.

**C++**
```cpp
int largestIsland(vector<vector<int>>& grid) {
    int n = grid.size();
    vector<int> parent(n * n), sz(n * n, 1);
    iota(parent.begin(), parent.end(), 0);
    function<int(int)> find = [&](int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); };
    auto unite = [&](int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return;
        if (sz[a] < sz[b]) swap(a, b);
        parent[b] = a; sz[a] += sz[b];
    };
    for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++) {
            if (!grid[r][c]) continue;
            if (r + 1 < n && grid[r + 1][c]) unite(r * n + c, (r + 1) * n + c);
            if (c + 1 < n && grid[r][c + 1]) unite(r * n + c, r * n + c + 1);
        }
    int best = 0, dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++) {
            if (grid[r][c]) { best = max(best, sz[find(r * n + c)]); continue; }
            set<int> roots;
            for (int d = 0; d < 4; d++) {
                int x = r + dr[d], y = c + dc[d];
                if (x >= 0 && y >= 0 && x < n && y < n && grid[x][y]) roots.insert(find(x * n + y));
            }
            int s = 1;
            for (int rt : roots) s += sz[rt];
            best = max(best, s);
        }
    return best;
}
```

**Java**
```java
static int[] parent, sz;
static int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
static void unite(int a, int b) {
    a = find(a); b = find(b);
    if (a == b) return;
    if (sz[a] < sz[b]) { int t = a; a = b; b = t; }
    parent[b] = a; sz[a] += sz[b];
}
static int largestIsland(int[][] grid) {
    int n = grid.length;
    parent = new int[n * n];
    sz = new int[n * n];
    for (int i = 0; i < n * n; i++) { parent[i] = i; sz[i] = 1; }
    for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++) {
            if (grid[r][c] == 0) continue;
            if (r + 1 < n && grid[r + 1][c] == 1) unite(r * n + c, (r + 1) * n + c);
            if (c + 1 < n && grid[r][c + 1] == 1) unite(r * n + c, r * n + c + 1);
        }
    int best = 0;
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++) {
            if (grid[r][c] == 1) { best = Math.max(best, sz[find(r * n + c)]); continue; }
            Set<Integer> roots = new HashSet<>();
            for (int d = 0; d < 4; d++) {
                int x = r + dr[d], y = c + dc[d];
                if (x >= 0 && y >= 0 && x < n && y < n && grid[x][y] == 1) roots.add(find(x * n + y));
            }
            int s = 1;
            for (int rt : roots) s += sz[rt];
            best = Math.max(best, s);
        }
    return best;
}
```

**Python**
```python
def largest_island(grid):
    n = len(grid)
    parent, sz = list(range(n * n)), [1] * (n * n)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def unite(a, b):
        a, b = find(a), find(b)
        if a == b:
            return
        if sz[a] < sz[b]:
            a, b = b, a
        parent[b] = a
        sz[a] += sz[b]
    for r in range(n):
        for c in range(n):
            if grid[r][c]:
                if r + 1 < n and grid[r + 1][c]: unite(r * n + c, (r + 1) * n + c)
                if c + 1 < n and grid[r][c + 1]: unite(r * n + c, r * n + c + 1)
    best = 0
    for r in range(n):
        for c in range(n):
            if grid[r][c]:
                best = max(best, sz[find(r * n + c)])
                continue
            roots = {find(x * n + y) for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
                     if 0 <= x < n and 0 <= y < n and grid[x][y]}
            best = max(best, 1 + sum(sz[rt] for rt in roots))
    return best
```

**Complexity:** time **O(n²·α)**, space **O(n²)** — two grid passes with ≤ 4 finds per cell.

---

## Edge cases

- All 1s: n² (no flip).
- All 0s: 1.
- A 0 surrounded by the same island on several sides: count that island once.

---

## Common mistakes

1. Summing neighbour sizes without deduping roots.
2. Initialising `best = 0` and only scoring zeros, which returns 0 for an all-ones grid.
3. Reading `sz[cell]` instead of `sz[find(cell)]`.

---

## Follow-ups

1. Flip up to k zeros?
2. Rectangular grid?

<details><summary>Answer sketches</summary>

**#1:** No longer local; becomes a search problem (k small: try combinations; in general NP-hard flavour). Discuss, don't code.

**#2:** Same with `r·m + c`.
</details>

---

## Flashcards

**LC 827 score of a zero cell?** #flashcard
1 + Σ size of distinct neighbouring island roots.

**LC 827 all-ones case?** #flashcard
Answer is n²; take max over island sizes too.

**Interview track →** [Union-find deep-dive](../../02-algorithms/14-union-find.md)
