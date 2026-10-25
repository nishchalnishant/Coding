---
module: striver-a2z/27-graphs
lesson: 44
topic: Kosaraju's algorithm
difficulty: Hard
source: https://takeuforward.org/learning/dsa/kosaraju's-algorithm?category=additional-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, scc, kosaraju, dfs]
---
# 44. Kosaraju's algorithm

← [Most stones removed with same row or column](43-most-stones-removed-with-same-row-or-column.md) · [Part 27 index](README.md) · Next → [Bridges in graph](45-bridges-in-graph.md)

> [!abstract] Problem at a glance
> **Task:** Count the strongly connected components of a directed graph.
> **Key insight:** Two DFS passes. Pass 1 records vertices by **finish time**. The vertex that finishes last lies in a *source* SCC of the condensation. In the **reversed** graph that SCC becomes a sink, so a DFS from it stays inside exactly that SCC. Repeat in decreasing finish order; each new DFS start is one SCC.
> **Difficulty:** Hard · **Pattern:** Finish-order DFS + reversed graph
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/kosaraju's-algorithm?category=additional-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Pairwise reachability](#3-pairwise-reachability) · [4. Kosaraju (two DFS passes)](#4-kosaraju-two-dfs-passes) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Directed graph with `V` vertices and `edges[i] = [u, v]` (u → v). Return the number of strongly connected components: maximal sets where every vertex reaches every other.

| Input | Output | Why |
|---|---|---|
| `V = 5, edges = [[1,0],[0,2],[2,1],[0,3],[3,4]]` | `3` | {0,1,2}, {3}, {4} |
| `V = 3, edges = [[0,1],[1,2],[2,0]]` | `1` | one cycle |

**Constraints:** `1 ≤ V ≤ 5000`, `0 ≤ E ≤ V(V−1)`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Pairwise reachability | BFS from every vertex; u, v together iff each reaches the other | O(V·(V + E)) | O(V²) |
| Kosaraju (two DFS passes) | DFS for finish order; DFS on reversed graph in reverse finish order | O(V + E) | O(V + E) |

> [!tip] Interview angle
> Explain why the finish order matters before writing it: the condensation is a DAG, finish order is a topological order of it, and reversing edges flips sources into sinks so DFS can't leak. Bridges / articulation points / SCC are rare at L3/L4 (the repo marks Tarjan/SCC out of scope); know the idea, the invariant and the complexity, and code it only if asked. Tarjan (one pass with low-links) is the alternative.

---

## 3. Pairwise reachability

**Intuition.** Compute `reach[u]` by BFS from each u. Group vertices by mutual reachability. Simple to justify, quadratic.

```python
from collections import deque

def kosaraju_bf(V, edges):
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
    reach = []
    for s in range(V):
        seen = [False] * V
        seen[s] = True
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
        reach.append(seen)
    comp, cnt = [-1] * V, 0
    for u in range(V):
        if comp[u] != -1:
            continue
        for v in range(V):
            if reach[u][v] and reach[v][u]:
                comp[v] = cnt
        cnt += 1
    return cnt
```

**Complexity:** time **O(V·(V + E))**, space **O(V²)**.

---

## 4. Kosaraju (two DFS passes)

**Intuition.** Pass 1: DFS the original graph, pushing each vertex on a stack when it finishes. Build the transpose. Pass 2: pop vertices; each unvisited popped vertex starts a DFS in the transpose that marks exactly one SCC.

**Algorithm**

1. DFS every unvisited vertex; push `u` to `order` after all its neighbours finish.
2. Build `radj` with every edge reversed.
3. Reset `visited`; for `u` in `reversed(order)`: if unvisited, `count += 1` and DFS `u` in `radj`.
4. Return `count`.

**Dry run** — Example 1 from 0: 0 → 2 → 1 (1 finishes, then 2), 0 → 3 → 4 (4, 3 finish), 0 finishes. order = [1,2,4,3,0]. Reverse: start 0 in transpose → reaches 1, 2 (via 1→0, 2→1 reversed). SCC 1 = {0,1,2}. Next 3 → {3}. Next 4 → {4}. Count 3.

**C++**
```cpp
void dfs1(int u, vector<vector<int>>& adj, vector<bool>& vis, vector<int>& order) {
    vis[u] = true;
    for (int v : adj[u]) if (!vis[v]) dfs1(v, adj, vis, order);
    order.push_back(u);
}
void dfs2(int u, vector<vector<int>>& radj, vector<bool>& vis) {
    vis[u] = true;
    for (int v : radj[u]) if (!vis[v]) dfs2(v, radj, vis);
}
int kosaraju(int V, vector<vector<int>>& edges) {
    vector<vector<int>> adj(V), radj(V);
    for (auto& e : edges) { adj[e[0]].push_back(e[1]); radj[e[1]].push_back(e[0]); }
    vector<bool> vis(V, false);
    vector<int> order;
    for (int i = 0; i < V; i++) if (!vis[i]) dfs1(i, adj, vis, order);
    fill(vis.begin(), vis.end(), false);
    int count = 0;
    for (int i = V - 1; i >= 0; i--) {
        int u = order[i];
        if (!vis[u]) { count++; dfs2(u, radj, vis); }
    }
    return count;
}
```

**Java**
```java
static List<List<Integer>> adj, radj;
static boolean[] vis;
static Deque<Integer> order;
static void dfs1(int u) {
    vis[u] = true;
    for (int v : adj.get(u)) if (!vis[v]) dfs1(v);
    order.push(u);
}
static void dfs2(int u) {
    vis[u] = true;
    for (int v : radj.get(u)) if (!vis[v]) dfs2(v);
}
static int kosaraju(int V, int[][] edges) {
    adj = new ArrayList<>(); radj = new ArrayList<>();
    for (int i = 0; i < V; i++) { adj.add(new ArrayList<>()); radj.add(new ArrayList<>()); }
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); radj.get(e[1]).add(e[0]); }
    vis = new boolean[V];
    order = new ArrayDeque<>();
    for (int i = 0; i < V; i++) if (!vis[i]) dfs1(i);
    vis = new boolean[V];
    int count = 0;
    while (!order.isEmpty()) {
        int u = order.pop();
        if (!vis[u]) { count++; dfs2(u); }
    }
    return count;
}
```

**Python**
```python
import sys

def kosaraju(V, edges):
    sys.setrecursionlimit(10000)
    adj = [[] for _ in range(V)]
    radj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        radj[v].append(u)
    vis, order = [False] * V, []
    def dfs1(u):
        vis[u] = True
        for v in adj[u]:
            if not vis[v]:
                dfs1(v)
        order.append(u)                      # push on finish
    for i in range(V):
        if not vis[i]:
            dfs1(i)
    vis = [False] * V
    def dfs2(u):
        vis[u] = True
        for v in radj[u]:
            if not vis[v]:
                dfs2(v)
    count = 0
    for u in reversed(order):
        if not vis[u]:
            count += 1
            dfs2(u)
    return count
```

**Complexity:** time **O(V + E)**, space **O(V + E)** — two DFS traversals plus building the transpose, each O(V + E).

---

## Edge cases

- No edges: V components.
- Self-loops: no effect on the count.
- Disconnected graph: pass 1 must start from every unvisited vertex.

---

## Common mistakes

1. Pass 2 on the **original** graph (leaks into downstream SCCs).
2. Pass 2 in increasing finish order.
3. Recording vertices on entry (pre-order) instead of on finish.

---

## Follow-ups

1. Return the components?
2. 2-SAT?
3. Tarjan vs Kosaraju?

<details><summary>Answer sketches</summary>

**#1:** Collect the vertices visited by each pass-2 DFS.

**#2:** Build the implication graph; unsatisfiable iff x and ¬x share an SCC.

**#3:** Tarjan: one DFS, low-link + stack, no transpose. Same O(V + E).
</details>

---

## Flashcards

**Kosaraju pass 1 records?** #flashcard
Vertices in order of DFS finish time.

**Kosaraju pass 2 graph and order?** #flashcard
Transposed graph, decreasing finish time; each new start = one SCC.

**Why reverse the graph?** #flashcard
Source SCCs of the condensation become sinks, so DFS can't escape them.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
