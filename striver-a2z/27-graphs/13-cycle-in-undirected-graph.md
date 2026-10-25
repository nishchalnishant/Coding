---
module: striver-a2z/27-graphs
lesson: 13
topic: Detect a cycle in an undirected graph
difficulty: Medium
source: https://takeuforward.org/learning/dsa/detect-a-cycle-in-an-undirected-graph?category=cycles&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bfs, dfs, cycle]
---
# 13. Detect a cycle in an undirected graph

← [Number of distinct islands](12-number-of-distinct-islands.md) · [Part 27 index](README.md) · Next → [Bipartite graph](14-bipartite-graph.md)

> [!abstract] Problem at a glance
> **Task:** Return whether an undirected graph (possibly disconnected) contains a cycle.
> **Key insight:** During a traversal, every edge either reaches a new node (a tree edge) or points to an already-visited node. In an undirected graph, the one visited neighbour that is **not** a cycle is the parent you just came from. Any other visited neighbour closes a cycle. Track `(node, parent)` and check every component.
> **Difficulty:** Medium · **Pattern:** Traversal with parent tracking
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/detect-a-cycle-in-an-undirected-graph?category=cycles&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. BFS with parent](#3-bfs-with-parent) · [4. DFS with parent](#4-dfs-with-parent) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

An undirected graph has `V` nodes `0..V-1` and a list of edges (no self-loops or parallel edges). Return `true` if the graph contains a cycle, `false` otherwise.

| Input | Output | Why |
|---|---|---|
| `V = 5, edges = [[0,1],[1,2],[2,3],[3,4]]` | `false` | a path |
| `V = 5, edges = [[0,1],[1,2],[2,0],[3,4]]` | `true` | triangle 0-1-2 |

**Constraints:** `1 ≤ V ≤ 10⁵`, `0 ≤ E ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| BFS with parent | queue of (node, parent); visited non-parent ⇒ cycle | O(V + E) | O(V) |
| DFS with parent | dfs(u, p): visited neighbour ≠ p ⇒ cycle | O(V + E) | O(V) |

> [!tip] Interview angle
> Mention the one-line alternative: a forest with `V` nodes and `c` components has exactly `V − c` edges, so a cycle exists iff `E > V − c`. Union-find gives the same answer: a cycle exists iff some edge joins two nodes already in the same set. The parent trick assumes no parallel edges; with parallel edges, track the parent **edge id** instead.

---

## 3. BFS with parent

**Intuition.** BFS from every unvisited node, storing each node's parent. When scanning `u`'s neighbours, an unvisited `v` gets parent `u`. A visited `v` that is not `parent[u]` means two different paths reach `v`, so there is a cycle.

```python
from collections import deque

def has_cycle_bfs(V, edges):
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    par = [-2] * V                      # -2 = unvisited
    for s in range(V):
        if par[s] != -2:
            continue
        par[s] = -1
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if par[v] == -2:
                    par[v] = u
                    q.append(v)
                elif v != par[u]:
                    return True
    return False
```

**Complexity:** time **O(V + E)**, space **O(V)**.

---

## 4. DFS with parent

**Intuition.** Iterative DFS pushing `(node, parent)` pairs. Mark on push so each node is pushed once. While expanding `u` (with parent `p`), an already-visited neighbour other than `p` closes a cycle.

**Algorithm**

1. Build adjacency lists.
2. For every unvisited `s`: mark it and push `(s, −1)`.
3. Pop `(u, p)`; for each neighbour `v`: if unvisited, mark and push `(v, u)`; else if `v ≠ p`, return `true`.
4. Return `false` after all components.

**Dry run** — Triangle 0-1-2: push (0,−1). Pop 0: push (1,0), (2,0). Pop (2,0): neighbour 0 is the parent, neighbour 1 is visited and ≠ 0 → true.

**C++**
```cpp
bool hasCycle(int V, vector<vector<int>>& edges) {
    vector<vector<int>> adj(V);
    for (auto& e : edges) { adj[e[0]].push_back(e[1]); adj[e[1]].push_back(e[0]); }
    vector<bool> seen(V, false);
    for (int s = 0; s < V; s++) {
        if (seen[s]) continue;
        seen[s] = true;
        vector<pair<int, int>> st = {{s, -1}};
        while (!st.empty()) {
            auto [u, p] = st.back(); st.pop_back();
            for (int v : adj[u]) {
                if (!seen[v]) { seen[v] = true; st.push_back({v, u}); }
                else if (v != p) return true;
            }
        }
    }
    return false;
}
```

**Java**
```java
static boolean hasCycle(int V, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    boolean[] seen = new boolean[V];
    for (int s = 0; s < V; s++) {
        if (seen[s]) continue;
        seen[s] = true;
        ArrayDeque<int[]> st = new ArrayDeque<>();
        st.push(new int[]{s, -1});
        while (!st.isEmpty()) {
            int[] t = st.pop();
            for (int v : adj.get(t[0])) {
                if (!seen[v]) { seen[v] = true; st.push(new int[]{v, t[0]}); }
                else if (v != t[1]) return true;
            }
        }
    }
    return false;
}
```

**Python**
```python
def has_cycle(V, edges):
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * V
    for s in range(V):
        if seen[s]:
            continue
        seen[s] = True
        st = [(s, -1)]
        while st:
            u, p = st.pop()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    st.append((v, u))
                elif v != p:
                    return True
    return False
```

**Complexity:** time **O(V + E)**, space **O(V)** — each node is pushed once and each edge is examined twice.

---

## Edge cases

- No edges: no cycle.
- Disconnected graph whose cycle is in a later component: the outer loop must reach it.
- Single edge `0-1`: when expanding 1, neighbour 0 is its parent, so no cycle.

---

## Common mistakes

1. Checking only from node 0.
2. Comparing against the parent of the wrong node (e.g. the BFS source).
3. Applying the parent trick to a **directed** graph: there, a visited node is not necessarily on the current path.

---

## Follow-ups

1. Parallel edges allowed (`[0,1]` twice is a cycle)?
2. Return the cycle itself?
3. Using union-find?

<details><summary>Answer sketches</summary>

**#1:** Track the edge index used to enter a node and skip only that one edge.

**#2:** When the back edge `u–v` is found, walk parent pointers from `u` and from `v` until they meet.

**#3:** For each edge, if `find(u) == find(v)` a cycle exists; otherwise union them.
</details>

---

## Flashcards

**Undirected cycle test in a traversal?** #flashcard
A visited neighbour other than the parent.

**Edge-count test for undirected cycles?** #flashcard
Cycle iff E > V − (number of components).

**DSU cycle test?** #flashcard
An edge whose endpoints already share a root.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
