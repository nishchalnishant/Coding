---
module: striver/18-recursion
lesson: 20
topic: M-Coloring Problem
difficulty: Medium
source: https://takeuforward.org/learning/dsa/m-coloring-problem?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking, graph]
---
# 20. M-Coloring Problem

← [Rat in a Maze](19-rat-in-a-maze.md) · [Part 18 index](README.md) · Next → [Sudoku Solver](21-sudoku-solver.md)

> [!abstract] Problem at a glance
> **Task:** Decide whether an undirected graph's vertices can be coloured with at most `m` colours so no edge joins two same-coloured vertices.
> **Key insight:** Colour vertices 0, 1, 2, … in order; for vertex v try each colour not used by an already-coloured neighbour, recurse, and undo on failure. Return true at v == n. NP-complete in general, so backtracking is the expected answer.
> **Difficulty:** Medium · **Pattern:** Constraint backtracking (assign → check → recurse → undo) · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/m-coloring-problem-1587115620/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/m-coloring-problem?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Try every colouring](#3-try-every-colouring) · [4. Backtracking vertex by vertex](#4-backtracking-vertex-by-vertex) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an undirected graph with `n` vertices (0-indexed) and an edge list `edges`, and an integer `m`, return `true` if the vertices can be coloured using at most `m` colours such that no two adjacent vertices share a colour.

| Input | Output | Why |
|---|---|---|
| `n = 4, edges = [[0,1],[1,2],[2,3],[3,0],[0,2]], m = 3` | `true` |  |
| `n = 3, edges = [[0,1],[1,2],[0,2]], m = 2` | `false` | a triangle needs 3 |

**Constraints:** `1 ≤ n ≤ 20`, `1 ≤ m ≤ n`, `0 ≤ |edges| ≤ n(n−1)/2`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Try every colouring | enumerate mⁿ assignments, check every edge | O(mⁿ · E) | O(n) |
| Backtracking vertex by vertex | for colour c in 1..m: if safe(v, c) → assign, recurse, undo | O(mⁿ) worst | O(n + E) |

> [!tip] Interview angle
> Template backtracking: state = colours of vertices < v, choice = colour of v, constraint = neighbours. Mention: m ≥ max degree + 1 is always enough (greedy), m = 2 is just bipartite checking (BFS, polynomial), and the worst case is O(mⁿ). Build an adjacency list first.

---

## 3. Try every colouring

**Intuition.** Generate all colour vectors and test each one. The baseline that ignores pruning.

```python
from itertools import product as _p
def color_brute(n, edges, m):
    return any(all(col[u] != col[v] for u, v in edges) for col in _p(range(m), repeat=n))
```

**Complexity:** time **O(mⁿ · E)**, space **O(n)**.

---

## 4. Backtracking vertex by vertex

**Intuition.** Check only neighbours of v when assigning — invalid partial colourings are cut immediately instead of at the leaves.

**Algorithm**

1. Build adjacency list; `color[v] = 0` (uncoloured).
2. `go(v)`: if v == n → true.
3. For c = 1 … m: if no neighbour has colour c → color[v] = c; if go(v + 1) → true; color[v] = 0.
4. Return false.

**Dry run** — Triangle, m = 2: v0 = 1, v1 = 2, v2: neighbours have {1, 2} → no colour → backtrack v1 (no other colour) → v0 = 2 symmetric → false.

**C++**
```cpp
bool go(int v, int n, int m, vector<vector<int>>& adj, vector<int>& color) {
    if (v == n) return true;
    for (int c = 1; c <= m; c++) {
        bool ok = true;
        for (int u : adj[v]) if (color[u] == c) { ok = false; break; }
        if (!ok) continue;
        color[v] = c;
        if (go(v + 1, n, m, adj, color)) return true;
        color[v] = 0;
    }
    return false;
}
bool graphColoring(int n, vector<vector<int>>& edges, int m) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) { adj[e[0]].push_back(e[1]); adj[e[1]].push_back(e[0]); }
    vector<int> color(n, 0);
    return go(0, n, m, adj, color);
}
```

**Java**
```java
static boolean go(int v, int n, int m, List<List<Integer>> adj, int[] color) {
    if (v == n) return true;
    for (int c = 1; c <= m; c++) {
        boolean ok = true;
        for (int u : adj.get(v)) if (color[u] == c) { ok = false; break; }
        if (!ok) continue;
        color[v] = c;
        if (go(v + 1, n, m, adj, color)) return true;
        color[v] = 0;
    }
    return false;
}
static boolean graphColoring(int n, int[][] edges, int m) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    return go(0, n, m, adj, new int[n]);
}
```

**Python**
```python
def graph_coloring(n, edges, m):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    color = [0] * n
    def go(v):
        if v == n:
            return True
        for c in range(1, m + 1):
            if all(color[u] != c for u in adj[v]):
                color[v] = c
                if go(v + 1):
                    return True
                color[v] = 0
        return False
    return go(0)
```

**Complexity:** time **O(mⁿ) worst**, space **O(n + E)** — mⁿ assignments in the worst case; each safety check O(deg v).

---

## Edge cases

- No edges → any m ≥ 1 works.
- Complete graph Kₙ needs exactly n colours.
- Odd cycle needs 3.

---

## Common mistakes

1. Checking all vertices for conflicts instead of only neighbours.
2. Not resetting `color[v]` on failure (harmless here, but breaks variants that scan all colours).
3. Assuming the graph is connected — the vertex-order recursion handles any graph.

---

## Follow-ups

1. m = 2.
2. Minimum colours (chromatic number).

<details><summary>Answer sketches</summary>

**#1:** Bipartite check by BFS/DFS 2-colouring — O(V + E).

**#2:** Try m = 1, 2, … with this backtracking; NP-hard in general.
</details>

---

## Flashcards

**M-colouring recursion skeleton?** #flashcard
go(v): for c in 1..m: if no neighbour has c → assign, if go(v+1) return true, undo.

**When is m-colouring polynomial?** #flashcard
m = 2 (bipartite check); also always true if m > max degree.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
