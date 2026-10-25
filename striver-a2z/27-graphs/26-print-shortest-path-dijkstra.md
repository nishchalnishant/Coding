---
module: striver-a2z/27-graphs
lesson: 26
topic: Print shortest path
difficulty: Medium
source: https://takeuforward.org/learning/dsa/print-shortest-path?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, dijkstra, shortest-path]
---
# 26. Print shortest path

← [Dijkstra's algorithm](25-dijkstra.md) · [Part 27 index](README.md) · Next → [Shortest distance in a binary maze](27-shortest-distance-binary-maze.md)

> [!abstract] Problem at a glance
> **Task:** In a weighted undirected graph with nodes `1..n`, return the nodes of a shortest path from `1` to `n` (`[-1]` if none).
> **Key insight:** Run Dijkstra and, every time `dist[v]` improves via `u`, set `parent[v] = u`. When the run ends, the parent pointers form a shortest-path tree. Walk back from `n` to `1` and reverse.
> **Difficulty:** Medium · **Pattern:** Dijkstra + parent array
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/print-shortest-path?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Dijkstra, then rebuild by checking edges](#3-dijkstra-then-rebuild-by-checking-edges) · [4. Dijkstra with parent pointers](#4-dijkstra-with-parent-pointers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

An undirected graph has nodes `1..n` and edges `[u, v, w]` (`w > 0`). Return the list of nodes on a shortest path from `1` to `n`, starting with `1`, or `[-1]` if `n` is unreachable. (Tests have a unique shortest path.)

| Input | Output | Why |
|---|---|---|
| `n = 5, edges = [[1,2,2],[2,5,5],[2,3,4],[1,4,1],[4,3,3],[3,5,1]]` | `[1,4,3,5]` | cost 1 + 3 + 1 = 5 |
| `n = 3, edges = [[1,2,1]]` | `[-1]` | 3 is isolated |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ m ≤ 10⁵`, `1 ≤ w ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Dijkstra, then rebuild by checking edges | from n, step to any neighbour u with dist[u] + w = dist[v] | O((n + m) log n) | O(n + m) |
| Dijkstra with parent pointers | parent[v] = u on every improvement; walk back from n | O((n + m) log n) | O(n + m) |

> [!tip] Interview angle
> GfG's version prepends the path weight to the list. Mention it, but the reconstruction is the point. Parent pointers are always set on the **improving** relaxation, never on pop.

---

## 3. Dijkstra, then rebuild by checking edges

**Intuition.** Run plain Dijkstra. Then walk backwards from `n`: any neighbour `u` with `dist[u] + w == dist[v]` lies on a shortest path, so step there until reaching 1. This needs no parent array but rescans adjacency lists.

```python
import heapq

def shortest_path_rebuild(n, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float('inf')
    d = [INF] * (n + 1)
    d[1] = 0
    pq = [(0, 1)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(pq, (d[v], v))
    if d[n] == INF:
        return [-1]
    path, v = [n], n
    while v != 1:
        v = next(u for u, w in adj[v] if d[u] + w == d[v])
        path.append(v)
    return path[::-1]
```

**Complexity:** time **O((n + m) log n)**, space **O(n + m)**.

---

## 4. Dijkstra with parent pointers

**Intuition.** Same Dijkstra; record `parent[v] = u` whenever `dist[v]` improves. Initially `parent[i] = i`. Follow parents from `n` until reaching the node that is its own parent (node 1), then reverse.

**Algorithm**

1. Build adjacency for nodes 1..n.
2. Dijkstra from 1, setting `par[v] = u` on each improvement.
3. If `dist[n] = ∞`, return `[-1]`.
4. Walk `v = n` → `par[v]` until `v == 1`; reverse.

**Dry run** — Example 1: d4 = 1 (par 1), d2 = 2 (par 1), d3 = 4 via 4 (par 4), d5 = 5 via 3 (par 3). Walk 5 → 3 → 4 → 1 → reversed [1,4,3,5].

**C++**
```cpp
vector<int> shortestPath(int n, vector<vector<int>>& edges) {
    vector<vector<pair<int, int>>> adj(n + 1);
    for (auto& e : edges) { adj[e[0]].push_back({e[1], e[2]}); adj[e[1]].push_back({e[0], e[2]}); }
    vector<long long> dist(n + 1, LLONG_MAX);
    vector<int> par(n + 1);
    iota(par.begin(), par.end(), 0);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
    dist[1] = 0;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [du, u] = pq.top(); pq.pop();
        if (du > dist[u]) continue;
        for (auto [v, w] : adj[u])
            if (du + w < dist[v]) { dist[v] = du + w; par[v] = u; pq.push({dist[v], v}); }
    }
    if (dist[n] == LLONG_MAX) return {-1};
    vector<int> path = {n};
    while (path.back() != 1) path.push_back(par[path.back()]);
    reverse(path.begin(), path.end());
    return path;
}
```

**Java**
```java
static List<Integer> shortestPath(int n, int[][] edges) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(new int[]{e[1], e[2]}); adj.get(e[1]).add(new int[]{e[0], e[2]}); }
    long[] dist = new long[n + 1];
    Arrays.fill(dist, Long.MAX_VALUE);
    int[] par = new int[n + 1];
    for (int i = 0; i <= n; i++) par[i] = i;
    PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    dist[1] = 0;
    pq.add(new long[]{0, 1});
    while (!pq.isEmpty()) {
        long[] t = pq.poll();
        int u = (int) t[1];
        if (t[0] > dist[u]) continue;
        for (int[] e : adj.get(u))
            if (t[0] + e[1] < dist[e[0]]) { dist[e[0]] = t[0] + e[1]; par[e[0]] = u; pq.add(new long[]{dist[e[0]], e[0]}); }
    }
    List<Integer> path = new ArrayList<>();
    if (dist[n] == Long.MAX_VALUE) { path.add(-1); return path; }
    for (int v = n; ; v = par[v]) { path.add(v); if (v == 1) break; }
    Collections.reverse(path);
    return path;
}
```

**Python**
```python
import heapq

def shortest_path(n, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float('inf')
    dist = [INF] * (n + 1)
    par = list(range(n + 1))
    dist[1] = 0
    pq = [(0, 1)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > dist[u]:
            continue
        for v, w in adj[u]:
            if du + w < dist[v]:
                dist[v] = du + w
                par[v] = u
                heapq.heappush(pq, (dist[v], v))
    if dist[n] == INF:
        return [-1]
    path = [n]
    while path[-1] != 1:
        path.append(par[path[-1]])
    return path[::-1]
```

**Complexity:** time **O((n + m) log n)**, space **O(n + m)** — Dijkstra plus an O(n) walk.

---

## Edge cases

- `n = 1`: path `[1]`.
- Unreachable `n`: `[-1]`.
- Path sums up to 10¹⁰: use 64-bit distances.

---

## Common mistakes

1. Setting `parent` when popping instead of when improving.
2. Forgetting to reverse the walked path.
3. An infinite loop when `par` is initialised to −1 or 0 instead of `i`.

---

## Follow-ups

1. All shortest paths?
2. Path for every target?

<details><summary>Answer sketches</summary>

**#1:** Keep a list of parents per node (every tie on `du + w == dist[v]`), then backtrack, as in Word Ladder II.

**#2:** The parent array already encodes the whole shortest-path tree.
</details>

---

## Flashcards

**Reconstruct a Dijkstra path?** #flashcard
`parent[v] = u` on each improving relaxation; walk back from the target.

**Parent initialisation for the walk-back?** #flashcard
`par[i] = i` so the source stops the loop.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
