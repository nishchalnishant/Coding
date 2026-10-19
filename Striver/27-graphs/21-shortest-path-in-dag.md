---
module: striver/27-graphs
lesson: 21
topic: Shortest path in DAG
difficulty: Medium
source: https://takeuforward.org/learning/dsa/shortest-path-in-dag?category=hard-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, topological-sort, shortest-path]
---
# 21. Shortest path in DAG

← [Alien dictionary](20-alien-dictionary.md) · [Part 27 index](README.md) · Next → [Shortest path in undirected graph with unit weights](22-shortest-path-unit-weights.md)

> [!abstract] Problem at a glance
> **Task:** In a weighted DAG, return the shortest distance from node 0 to every node (`-1` if unreachable).
> **Key insight:** In topological order, every edge into `v` comes from a node processed earlier. So relaxing the edges of each node, in topological order, finalises `dist[v]` before `v`'s own edges are relaxed. One pass, O(V + E), and **negative weights are fine** (there are no cycles to exploit).
> **Difficulty:** Medium · **Pattern:** Topological order + relaxation
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/shortest-path-in-dag?category=hard-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Bellman-Ford style passes](#3-bellman-ford-style-passes) · [4. Topological order + relaxation](#4-topological-order--relaxation) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A directed acyclic graph has `V` nodes and edges `[u, v, w]` (`u → v` with weight `w`). Return `dist`, where `dist[i]` is the shortest-path distance from node `0` to `i`, or `-1` if `i` is unreachable.

| Input | Output | Why |
|---|---|---|
| `V = 6, edges = [[0,1,2],[0,4,1],[4,5,4],[4,2,2],[1,2,3],[2,3,6],[5,3,1]]` | `[0,2,3,6,1,5]` | 0→4→2 = 3; 0→4→5→3 = 6 |
| `V = 3, edges = [[1,2,4]]` | `[0,-1,-1]` | nothing leaves 0 |

**Constraints:** `1 ≤ V ≤ 100`, `0 ≤ E ≤ 100`, `|w| ≤ 100`, the graph is acyclic.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Bellman-Ford style passes | relax all edges V−1 times | O(V·E) | O(V) |
| Topological order + relaxation | Kahn order; relax out-edges once | O(V + E) | O(V + E) |

> [!tip] Interview angle
> Contrast this with Dijkstra: no heap, linear time, and it handles negative edges because the processing order is fixed by the topology, not by distances. With all signs flipped, the same code finds the **longest** path in a DAG, which is NP-hard on general graphs.

---

## 3. Bellman-Ford style passes

**Intuition.** Ignore the DAG structure: V − 1 rounds of relaxing every edge is enough for any graph without negative cycles.

```python
def shortest_dag_bf(V, edges):
    INF = float('inf')
    d = [INF] * V
    d[0] = 0
    for _ in range(V - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return [x if x < INF else -1 for x in d]
```

**Complexity:** time **O(V·E)**, space **O(V)**.

---

## 4. Topological order + relaxation

**Intuition.** Get a topological order with Kahn's algorithm. Set `dist[0] = 0` and everything else to ∞. Walk the order and relax each reachable node's out-edges. Map ∞ to −1.

**Algorithm**

1. Build `adj` with weights and in-degrees; run Kahn to get `order`.
2. `dist = [∞]·V`, `dist[0] = 0`.
3. For `u` in `order`: if `dist[u] < ∞`, relax every `u → v (w)`: `dist[v] = min(dist[v], dist[u] + w)`.
4. Replace ∞ by −1.

**Dry run** — Example 1 topo order 0,1,4,2,5,3. From 0: d1 = 2, d4 = 1. From 1: d2 = 5. From 4: d5 = 5, d2 = 3. From 2: d3 = 9. From 5: d3 = 6.

**C++**
```cpp
vector<int> shortestDag(int V, vector<vector<int>>& edges) {
    vector<vector<pair<int, int>>> adj(V);
    vector<int> indeg(V, 0), order;
    for (auto& e : edges) { adj[e[0]].push_back({e[1], e[2]}); indeg[e[1]]++; }
    queue<int> q;
    for (int i = 0; i < V; i++) if (indeg[i] == 0) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (auto [v, w] : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    const int INF = INT_MAX;
    vector<int> d(V, INF);
    d[0] = 0;
    for (int u : order) {
        if (d[u] == INF) continue;
        for (auto [v, w] : adj[u]) d[v] = min(d[v], d[u] + w);
    }
    for (int& x : d) if (x == INF) x = -1;
    return d;
}
```

**Java**
```java
static int[] shortestDag(int V, int[][] edges) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
    int[] indeg = new int[V];
    for (int[] e : edges) { adj.get(e[0]).add(new int[]{e[1], e[2]}); indeg[e[1]]++; }
    ArrayDeque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < V; i++) if (indeg[i] == 0) q.add(i);
    int[] order = new int[V];
    int k = 0;
    while (!q.isEmpty()) {
        int u = q.poll();
        order[k++] = u;
        for (int[] e : adj.get(u)) if (--indeg[e[0]] == 0) q.add(e[0]);
    }
    final int INF = Integer.MAX_VALUE;
    int[] d = new int[V];
    Arrays.fill(d, INF);
    d[0] = 0;
    for (int i = 0; i < k; i++) {
        int u = order[i];
        if (d[u] == INF) continue;
        for (int[] e : adj.get(u)) d[e[0]] = Math.min(d[e[0]], d[u] + e[1]);
    }
    for (int i = 0; i < V; i++) if (d[i] == INF) d[i] = -1;
    return d;
}
```

**Python**
```python
from collections import deque

def shortest_dag(V, edges):
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    q = deque(i for i in range(V) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    INF = float('inf')
    d = [INF] * V
    d[0] = 0
    for u in order:
        if d[u] == INF:
            continue
        for v, w in adj[u]:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return [x if x < INF else -1 for x in d]
```

**Complexity:** time **O(V + E)**, space **O(V + E)** — one Kahn pass plus one relaxation per edge.

---

## Edge cases

- Nodes before 0 in topological order: unreachable unless 0 reaches them (it can't), so −1.
- Negative weights: correct (no cycles).
- Skip relaxing from `∞` nodes, or `∞ + w` overflows in C++/Java.

---

## Common mistakes

1. Relaxing from unreachable nodes with `INT_MAX + w` (overflow).
2. Using BFS order instead of topological order.
3. Returning ∞ instead of −1.

---

## Follow-ups

1. Longest path in a DAG?
2. Count shortest paths?

<details><summary>Answer sketches</summary>

**#1:** Negate the weights (or use max), same pass. Used for critical-path scheduling.

**#2:** Keep `ways[v]`: on a strict improvement copy `ways[u]`, on a tie add it.
</details>

---

## Flashcards

**Shortest path in a DAG: time and trick?** #flashcard
O(V + E): relax edges in topological order.

**Does DAG shortest path handle negative weights?** #flashcard
Yes, there are no cycles.

**Longest path in a DAG?** #flashcard
Same pass with max (or negated weights).

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
