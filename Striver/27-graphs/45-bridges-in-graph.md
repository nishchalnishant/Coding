---
module: striver/27-graphs
lesson: 45
topic: Bridges in graph
difficulty: Hard
source: https://takeuforward.org/learning/dsa/bridges-in-graph?category=additional-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bridges, tarjan, dfs]
---
# 45. Bridges in graph

← [Kosaraju's algorithm](44-kosarajus-algorithm.md) · [Part 27 index](README.md) · Next → [Articulation point in graph](46-articulation-point-in-graph.md)

> [!abstract] Problem at a glance
> **Task:** Return every edge whose removal disconnects the undirected graph (critical connections).
> **Key insight:** DFS with discovery time `tin[u]` and `low[u]` = earliest `tin` reachable from u's subtree using **one back edge**. Tree edge `u–v` is a bridge iff `low[v] > tin[u]`: nothing under v can climb back to u or above without that edge.
> **Difficulty:** Hard · **Pattern:** Tarjan low-link DFS · **Also on:** LC 1192
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/bridges-in-graph?category=additional-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Remove each edge and test connectivity](#3-remove-each-edge-and-test-connectivity) · [4. Tarjan tin / low](#4-tarjan-tin--low) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`n` servers `0..n−1`, `connections[i] = [a, b]` undirected. A critical connection is one whose removal makes some server unable to reach another. Return all critical connections in any order (each as `[min, max]` here).

| Input | Output | Why |
|---|---|---|
| `n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]` | `[[1,3]]` | the triangle has no bridges |
| `n = 2, connections = [[0,1]]` | `[[0,1]]` |  |

**Constraints:** `2 ≤ n ≤ 10⁵`, `n − 1 ≤ E ≤ 10⁵`, no repeated connections.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Remove each edge and test connectivity | for every edge, BFS without it | O(E·(V + E)) | O(V + E) |
| Tarjan tin / low | DFS; low[u] = min(tin[u], low[child], tin[back-edge target]); bridge if low[v] > tin[u] | O(V + E) | O(V + E) |

> [!tip] Interview angle
> Define `tin` and `low` precisely and state the bridge condition before coding. Bridges / articulation points / SCC are rare at L3/L4 (the repo marks Tarjan/SCC out of scope); know the idea, the invariant and the complexity, and code it only if asked. The parent-skip must skip the parent **edge**, not the parent vertex, if parallel edges are allowed.

---

## 3. Remove each edge and test connectivity

**Intuition.** An edge is a bridge iff the graph without it has more components (equivalently, its endpoints become disconnected).

```python
from collections import deque

def critical_connections_bf(n, connections):
    out = []
    for k, (a, b) in enumerate(connections):
        adj = [[] for _ in range(n)]
        for i, (u, v) in enumerate(connections):
            if i != k:
                adj[u].append(v)
                adj[v].append(u)
        seen = [False] * n
        seen[a] = True
        q = deque([a])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
        if not seen[b]:
            out.append([min(a, b), max(a, b)])
    return out
```

**Complexity:** time **O(E·(V + E))**, space **O(V + E)**.

---

## 4. Tarjan tin / low

**Intuition.** Assign `tin[u] = low[u] = timer++` on entry. For each neighbour `v` other than the parent: if visited, it's a back edge, so `low[u] = min(low[u], tin[v])`; else recurse, then `low[u] = min(low[u], low[v])` and report `u–v` if `low[v] > tin[u]`.

**Algorithm**

1. `tin`, `low` = −1; `timer = 0`.
2. `dfs(u, parent)`: set `tin[u] = low[u] = timer++`.
3. For `v` in `adj[u]`, skip `v == parent`.
4. Visited `v`: `low[u] = min(low[u], tin[v])`.
5. Unvisited: `dfs(v, u)`; `low[u] = min(low[u], low[v])`; if `low[v] > tin[u]` record the bridge.
6. Run from every unvisited vertex.

**Dry run** — Example 1: dfs 0 (t0) → 1 (t1) → 2 (t2); 2 sees 0 visited → low2 = 0. Back at 1: low1 = 0; low2 = 0 > tin1? No. 1 → 3 (t3): low3 = 3 > tin1 = 1 → bridge [1,3]. Back at 0: low1 = 0 > 0? No.

**C++**
```cpp
int timer_;
vector<int> tin_, low_;
vector<vector<int>> adj_, res_;
void dfs(int u, int p) {
    tin_[u] = low_[u] = timer_++;
    for (int v : adj_[u]) {
        if (v == p) continue;
        if (tin_[v] != -1) { low_[u] = min(low_[u], tin_[v]); continue; }
        dfs(v, u);
        low_[u] = min(low_[u], low_[v]);
        if (low_[v] > tin_[u]) res_.push_back({min(u, v), max(u, v)});
    }
}
vector<vector<int>> criticalConnections(int n, vector<vector<int>>& connections) {
    adj_.assign(n, {});
    for (auto& c : connections) { adj_[c[0]].push_back(c[1]); adj_[c[1]].push_back(c[0]); }
    tin_.assign(n, -1);
    low_.assign(n, -1);
    res_.clear();
    timer_ = 0;
    for (int i = 0; i < n; i++) if (tin_[i] == -1) dfs(i, -1);
    return res_;
}
```

**Java**
```java
static int timer;
static int[] tin, low;
static List<List<Integer>> adj;
static List<int[]> res;
static void dfs(int u, int p) {
    tin[u] = low[u] = timer++;
    for (int v : adj.get(u)) {
        if (v == p) continue;
        if (tin[v] != -1) { low[u] = Math.min(low[u], tin[v]); continue; }
        dfs(v, u);
        low[u] = Math.min(low[u], low[v]);
        if (low[v] > tin[u]) res.add(new int[]{Math.min(u, v), Math.max(u, v)});
    }
}
static List<int[]> criticalConnections(int n, int[][] connections) {
    adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] c : connections) { adj.get(c[0]).add(c[1]); adj.get(c[1]).add(c[0]); }
    tin = new int[n]; low = new int[n];
    Arrays.fill(tin, -1);
    res = new ArrayList<>();
    timer = 0;
    for (int i = 0; i < n; i++) if (tin[i] == -1) dfs(i, -1);
    return res;
}
```

**Python**
```python
import sys

def critical_connections(n, connections):
    sys.setrecursionlimit(10000)
    adj = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
    tin, low = [-1] * n, [-1] * n
    timer, out = 0, []
    def dfs(u, p):
        nonlocal timer
        tin[u] = low[u] = timer
        timer += 1
        for v in adj[u]:
            if v == p:
                continue
            if tin[v] != -1:                       # back edge
                low[u] = min(low[u], tin[v])
                continue
            dfs(v, u)
            low[u] = min(low[u], low[v])
            if low[v] > tin[u]:
                out.append([min(u, v), max(u, v)])
    for i in range(n):
        if tin[i] == -1:
            dfs(i, -1)
    return out
```

**Complexity:** time **O(V + E)**, space **O(V + E)** — one DFS; each edge is examined twice.

---

## Edge cases

- A tree: every edge is a bridge.
- A single cycle: no bridges.
- Recursion depth ~10⁵ on a path: iterative DFS or a raised stack limit in Python/Java.

---

## Common mistakes

1. Using `>=` (that's the articulation-point condition).
2. Updating `low[u]` with `low[v]` for a back edge instead of `tin[v]`.
3. Not skipping the parent, so every tree edge looks like a back edge.

---

## Follow-ups

1. Parallel edges allowed?
2. 2-edge-connected components?

<details><summary>Answer sketches</summary>

**#1:** Skip the parent **edge id**, not the parent vertex; a duplicate edge is a legitimate back edge.

**#2:** Delete bridges; remaining components are the 2-edge-connected components.
</details>

---

## Flashcards

**Bridge condition?** #flashcard
Tree edge u–v with low[v] > tin[u].

**low[u] definition?** #flashcard
Min tin reachable from u's DFS subtree using at most one back edge.

**Back edge updates low with?** #flashcard
tin[v] (not low[v]).

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
