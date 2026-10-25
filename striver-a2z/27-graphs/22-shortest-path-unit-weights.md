---
module: striver-a2z/27-graphs
lesson: 22
topic: Shortest path in undirected graph with unit weights
difficulty: Medium
source: https://takeuforward.org/learning/dsa/shortest-path-in-undirected-graph-with-unit-weights?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bfs, shortest-path]
---
# 22. Shortest path in undirected graph with unit weights

← [Shortest path in DAG](21-shortest-path-in-dag.md) · [Part 27 index](README.md) · Next → [Word ladder I](23-word-ladder-i.md)

> [!abstract] Problem at a glance
> **Task:** Return the shortest distance (number of edges) from `src` to every node of an undirected graph, `-1` if unreachable.
> **Key insight:** With every edge weighing 1, BFS **is** Dijkstra. The queue pops nodes in non-decreasing distance, so the first time a node is discovered, it is via a shortest path. `dist[v] = dist[u] + 1` at discovery is final.
> **Difficulty:** Medium · **Pattern:** BFS shortest path
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/shortest-path-in-undirected-graph-with-unit-weights?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Bellman-Ford with unit weights](#3-bellman-ford-with-unit-weights) · [4. BFS](#4-bfs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

An undirected graph has `V` nodes and unit-weight edges. Given `src`, return `dist` where `dist[i]` is the minimum number of edges from `src` to `i`, or `-1` if unreachable.

| Input | Output | Why |
|---|---|---|
| `V = 9, edges = [[0,1],[0,3],[3,4],[4,5],[5,6],[1,2],[2,6],[6,7],[7,8],[6,8]], src = 0` | `[0,1,2,1,2,3,3,4,4]` | 6 via 0-1-2-6 |
| `V = 4, edges = [[0,1],[1,2]], src = 2` | `[2,1,0,-1]` | 3 is isolated |

**Constraints:** `1 ≤ V ≤ 10⁴`, `0 ≤ E ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Bellman-Ford with unit weights | relax every edge V−1 times | O(V·E) | O(V) |
| BFS | dist set at discovery is final | O(V + E) | O(V + E) |

> [!tip] Interview angle
> Say why BFS is correct (the queue holds at most two consecutive distance values, in order) and when it stops being correct: weighted edges need Dijkstra, and 0/1 weights need a deque (0-1 BFS).

---

## 3. Bellman-Ford with unit weights

**Intuition.** Treat it as a general weighted problem: V − 1 rounds, relaxing both directions of every edge.

```python
def unit_sp_bf(V, edges, src):
    INF = float('inf')
    d = [INF] * V
    d[src] = 0
    for _ in range(V - 1):
        for u, v in edges:
            if d[u] + 1 < d[v]: d[v] = d[u] + 1
            if d[v] + 1 < d[u]: d[u] = d[v] + 1
    return [x if x < INF else -1 for x in d]
```

**Complexity:** time **O(V·E)**, space **O(V)**.

---

## 4. BFS

**Intuition.** `dist = −1` everywhere, `dist[src] = 0`. BFS: an undiscovered neighbour gets `dist[u] + 1` and is enqueued. −1 doubles as 'unvisited'.

**Algorithm**

1. Build adjacency lists.
2. `dist[src] = 0`, enqueue `src`.
3. Pop `u`; for each `v` with `dist[v] = −1`: `dist[v] = dist[u] + 1`, enqueue.
4. Return `dist`.

**Dry run** — Example 1: level 0 {0}, level 1 {1,3}, level 2 {2,4}, level 3 {6,5}, level 4 {7,8}.

**C++**
```cpp
vector<int> unitSp(int V, vector<vector<int>>& edges, int src) {
    vector<vector<int>> adj(V);
    for (auto& e : edges) { adj[e[0]].push_back(e[1]); adj[e[1]].push_back(e[0]); }
    vector<int> dist(V, -1);
    dist[src] = 0;
    queue<int> q; q.push(src);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
    }
    return dist;
}
```

**Java**
```java
static int[] unitSp(int V, int[][] edges, int src) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    int[] dist = new int[V];
    Arrays.fill(dist, -1);
    dist[src] = 0;
    ArrayDeque<Integer> q = new ArrayDeque<>();
    q.add(src);
    while (!q.isEmpty()) {
        int u = q.poll();
        for (int v : adj.get(u)) if (dist[v] == -1) { dist[v] = dist[u] + 1; q.add(v); }
    }
    return dist;
}
```

**Python**
```python
from collections import deque

def unit_sp(V, edges, src):
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    dist = [-1] * V
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

**Complexity:** time **O(V + E)**, space **O(V + E)** — a single BFS.

---

## Edge cases

- Source isolated: everything else −1.
- Cycles: harmless; each node is discovered once.
- Directed version: the same code with one-way edges.

---

## Common mistakes

1. Updating `dist` on pop instead of discovery, so nodes are queued several times.
2. Using DFS, which does not give shortest paths.
3. Using Dijkstra: correct but adds a needless log factor.

---

## Follow-ups

1. Edge weights 0 or 1?
2. Reconstruct the path to a target?

<details><summary>Answer sketches</summary>

**#1:** 0-1 BFS: deque, push-front on weight 0, push-back on weight 1.

**#2:** Store `parent[v] = u` at discovery and walk back.
</details>

---

## Flashcards

**Unit-weight shortest path?** #flashcard
BFS, O(V + E).

**When is a BFS distance final?** #flashcard
At discovery (first push).

**0/1 weights?** #flashcard
0-1 BFS with a deque.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
