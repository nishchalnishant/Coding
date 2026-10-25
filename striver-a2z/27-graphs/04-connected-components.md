---
module: striver-a2z/27-graphs
lesson: 4
topic: Connected Components
difficulty: Easy
source: https://takeuforward.org/learning/dsa/connected-components?category=theory-and-traversals&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bfs, components]
---
# 4. Connected Components

← [Traversal Techniques](03-traversal-techniques-bfs-dfs.md) · [Part 27 index](README.md) · Next → [Number of provinces](05-number-of-provinces.md)

> [!abstract] Problem at a glance
> **Task:** Count the connected components of an undirected graph with `V` nodes and an edge list.
> **Key insight:** Every traversal started from an unvisited node visits exactly one whole component. So the number of times the outer loop finds an unvisited node and starts a traversal is the component count.
> **Difficulty:** Easy · **Pattern:** Traversal from every unvisited node · **Also on:** LC 323
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/connected-components?category=theory-and-traversals&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Adjacency matrix + DFS](#3-adjacency-matrix--dfs) · [4. Adjacency list + BFS](#4-adjacency-list--bfs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

An undirected graph has `V` nodes `0..V-1` and an edge list `edges` (`[u, v]` pairs; self-loops and duplicates may appear). Return the number of connected components.

| Input | Output | Why |
|---|---|---|
| `V = 5, edges = [[0,1],[1,2],[3,4]]` | `2` | {0,1,2} and {3,4} |
| `V = 4, edges = []` | `4` | every node is alone |

**Constraints:** `1 ≤ V ≤ 10⁵`, `0 ≤ E ≤ 2·10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Adjacency matrix + DFS | V×V matrix, scan a row per node | O(V²) | O(V²) |
| Adjacency list + BFS | build lists; BFS from each unvisited node | O(V + E) | O(V + E) |

> [!tip] Interview angle
> This outer loop ('for each node: if unvisited, traverse and count') is the skeleton for islands, provinces, cycle detection and bipartite checks on graphs that may be disconnected. Write it once and reuse it.

---

## 3. Adjacency matrix + DFS

**Intuition.** Fill a boolean matrix, then DFS where expanding `u` scans the whole row `u`. Simple but quadratic even when the graph has few edges.

```python
def count_components_matrix(V, edges):
    M = [[False] * V for _ in range(V)]
    for u, v in edges:
        M[u][v] = M[v][u] = True
    seen = [False] * V
    comps = 0
    for s in range(V):
        if seen[s]:
            continue
        comps += 1
        seen[s] = True
        st = [s]
        while st:
            u = st.pop()
            for v in range(V):
                if M[u][v] and not seen[v]:
                    seen[v] = True
                    st.append(v)
    return comps
```

**Complexity:** time **O(V²)**, space **O(V²)**.

---

## 4. Adjacency list + BFS

**Intuition.** Build adjacency lists, then loop over all nodes. Each unvisited node starts a BFS that marks its whole component; count how many BFS runs start.

**Algorithm**

1. Build `adj` from `edges` (both directions).
2. For each `s` in `0..V-1` that is unvisited: increment the count and BFS from `s`, marking every reached node.
3. Return the count.

**Dry run** — V = 5, edges [[0,1],[1,2],[3,4]]. s=0: BFS marks 0,1,2 → count 1. s=1,2 seen. s=3: marks 3,4 → count 2. Return 2.

**C++**
```cpp
int countComponents(int V, vector<vector<int>>& edges) {
    vector<vector<int>> adj(V);
    for (auto& e : edges) { adj[e[0]].push_back(e[1]); adj[e[1]].push_back(e[0]); }
    vector<bool> seen(V, false);
    int comps = 0;
    for (int s = 0; s < V; s++) {
        if (seen[s]) continue;
        comps++;
        seen[s] = true;
        queue<int> q; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) if (!seen[v]) { seen[v] = true; q.push(v); }
        }
    }
    return comps;
}
```

**Java**
```java
static int countComponents(int V, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    boolean[] seen = new boolean[V];
    int comps = 0;
    for (int s = 0; s < V; s++) {
        if (seen[s]) continue;
        comps++;
        seen[s] = true;
        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.add(s);
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int v : adj.get(u)) if (!seen[v]) { seen[v] = true; q.add(v); }
        }
    }
    return comps;
}
```

**Python**
```python
from collections import deque

def count_components(V, edges):
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * V
    comps = 0
    for s in range(V):
        if seen[s]:
            continue
        comps += 1
        seen[s] = True
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
    return comps
```

**Complexity:** time **O(V + E)**, space **O(V + E)** — every node is enqueued once and every edge is scanned twice.

---

## Edge cases

- No edges: the answer is `V`.
- Self-loop `[0,0]`: adds `0` to its own list; harmless.
- Duplicate edges: harmless with `visited`.

---

## Common mistakes

1. Only traversing from node 0, so other components are missed.
2. Adding each edge in one direction only for an undirected graph.
3. Counting `seen` nodes instead of traversal starts.

---

## Follow-ups

1. Edges arrive one at a time and you need the count after each?
2. Size of the largest component?
3. Directed graph, 'weakly connected' components?

<details><summary>Answer sketches</summary>

**#1:** Union-find: start with `V` components and decrement on every successful union.

**#2:** Count the nodes popped in each BFS and keep the maximum.

**#3:** Ignore direction (add both directions) and run the same code.
</details>

---

## Flashcards

**Number of components equals…?** #flashcard
The number of traversals started from unvisited nodes.

**Components via DSU?** #flashcard
Start at V, subtract 1 per union that merges two different roots.

**Matrix vs list traversal cost?** #flashcard
O(V²) vs O(V + E).

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
