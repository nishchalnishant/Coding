---
module: striver-a2z/27-graphs
lesson: 25
topic: Dijkstra's algorithm
difficulty: Medium
source: https://takeuforward.org/learning/dsa/dijkstras-algorithm?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, dijkstra, heap, shortest-path]
---
# 25. Dijkstra's algorithm

← [Word ladder II](24-word-ladder-ii.md) · [Part 27 index](README.md) · Next → [Print shortest path](26-print-shortest-path-dijkstra.md)

> [!abstract] Problem at a glance
> **Task:** Return the shortest distance from `src` to every node of an undirected graph with non-negative weights (`-1` if unreachable).
> **Key insight:** Dijkstra is greedy. The unfinished node with the smallest tentative distance cannot be improved later, because every other route to it would pass through a node that is already at least as far, and weights are ≥ 0. So finalise it and relax its edges. A min-heap finds that node in O(log V). Stale heap entries (pushed before a later improvement) are skipped on pop.
> **Difficulty:** Medium · **Pattern:** Dijkstra (min-heap)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/dijkstras-algorithm?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Array scan (O(V²))](#3-array-scan-ov²) · [4. Min-heap with lazy deletion](#4-min-heap-with-lazy-deletion) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

An undirected graph has `V` nodes and weighted edges `[u, v, w]` with `w ≥ 0`. Return `dist`, the shortest-path distance from `src` to every node, with `-1` for unreachable nodes.

| Input | Output | Why |
|---|---|---|
| `V = 3, edges = [[0,1,1],[1,2,3],[0,2,6]], src = 2` | `[4,3,0]` | 2→1→0 = 4 beats the direct 6 |
| `V = 4, edges = [[0,1,5]], src = 1` | `[5,0,-1,-1]` | 2 and 3 are isolated |

**Constraints:** `1 ≤ V ≤ 10⁴`, `0 ≤ E ≤ 10⁵`, `0 ≤ w ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Array scan (O(V²)) | pick the smallest unfinished dist by linear scan | O(V² + E) | O(V) |
| Min-heap with lazy deletion | pop smallest (d, u); skip stale; relax | O((V + E) log V) | O(V + E) |

> [!tip] Interview angle
> Name the variants and their costs: binary heap with lazy deletion O((V + E) log V), which is what everyone codes; the array scan O(V²), which is better for dense graphs (E ≈ V²); and `std::set` with erase-on-update, which keeps one entry per node. State the precondition out loud: **no negative edges**. A negative edge can make a 'finalised' node improvable later.

---

## 3. Array scan (O(V²))

**Intuition.** Keep `done[]`. V times: scan for the unfinished node with the smallest finite distance, finalise it, and relax its edges. No heap needed; optimal for dense graphs.

```python
def dijkstra_scan(V, edges, src):
    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float('inf')
    d, done = [INF] * V, [False] * V
    d[src] = 0
    for _ in range(V):
        u = min((i for i in range(V) if not done[i]), key=lambda i: d[i])
        if d[u] == INF:
            break
        done[u] = True
        for v, w in adj[u]:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return [x if x < INF else -1 for x in d]
```

**Complexity:** time **O(V² + E)**, space **O(V)**.

---

## 4. Min-heap with lazy deletion

**Intuition.** Push `(0, src)`. Pop `(du, u)`; if `du > dist[u]` the entry is stale, so skip it. Otherwise relax every edge, pushing `(dist[v], v)` whenever it improves.

**Algorithm**

1. `dist = [∞]·V`, `dist[src] = 0`, heap = `[(0, src)]`.
2. Pop `(du, u)`; if `du > dist[u]`, continue.
3. For each `(v, w)`: if `du + w < dist[v]`, set it and push `(dist[v], v)`.
4. Map ∞ → −1.

**Dry run** — src 2: pop (0,2) → d1 = 3, d0 = 6. Pop (3,1) → d0 = 4. Pop (4,0). Pop (6,0) stale. [4,3,0].

**C++**
```cpp
vector<int> dijkstra(int V, vector<vector<int>>& edges, int src) {
    vector<vector<pair<int, int>>> adj(V);
    for (auto& e : edges) { adj[e[0]].push_back({e[1], e[2]}); adj[e[1]].push_back({e[0], e[2]}); }
    vector<int> dist(V, INT_MAX);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [du, u] = pq.top(); pq.pop();
        if (du > dist[u]) continue;
        for (auto [v, w] : adj[u])
            if (du + w < dist[v]) { dist[v] = du + w; pq.push({dist[v], v}); }
    }
    for (int& x : dist) if (x == INT_MAX) x = -1;
    return dist;
}
```

**Java**
```java
static int[] dijkstra(int V, int[][] edges, int src) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(new int[]{e[1], e[2]}); adj.get(e[1]).add(new int[]{e[0], e[2]}); }
    int[] dist = new int[V];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[src] = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
    pq.add(new int[]{0, src});
    while (!pq.isEmpty()) {
        int[] t = pq.poll();
        int du = t[0], u = t[1];
        if (du > dist[u]) continue;
        for (int[] e : adj.get(u))
            if (du + e[1] < dist[e[0]]) { dist[e[0]] = du + e[1]; pq.add(new int[]{dist[e[0]], e[0]}); }
    }
    for (int i = 0; i < V; i++) if (dist[i] == Integer.MAX_VALUE) dist[i] = -1;
    return dist;
}
```

**Python**
```python
import heapq

def dijkstra(V, edges, src):
    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float('inf')
    dist = [INF] * V
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > dist[u]:
            continue
        for v, w in adj[u]:
            if du + w < dist[v]:
                dist[v] = du + w
                heapq.heappush(pq, (dist[v], v))
    return [x if x < INF else -1 for x in dist]
```

**Complexity:** time **O((V + E) log V)**, space **O(V + E)** — each edge can push one entry, so the heap holds O(E) items and each operation costs O(log E) = O(log V).

---

## Edge cases

- Isolated nodes: −1.
- Zero-weight edges: fine.
- Parallel edges: both are relaxed; the smaller wins.

---

## Common mistakes

1. Skipping the stale-entry check: still correct, but it re-relaxes edges and can degrade badly.
2. Using a max-heap by accident (Java/C++ default ordering).
3. Using Dijkstra with negative edge weights.

---

## Follow-ups

1. Why does a negative edge break Dijkstra?
2. Why not a visited set marked on push?

<details><summary>Answer sketches</summary>

**#1:** A node finalised at distance d could later be reached via a negative edge for less; greedy finalisation is no longer safe.

**#2:** A node's distance can still improve after it is first pushed; only the pop is final.
</details>

---

## Flashcards

**Dijkstra precondition?** #flashcard
Non-negative edge weights.

**Heap Dijkstra time?** #flashcard
O((V + E) log V).

**Stale heap entry check?** #flashcard
`if d > dist[u]: continue`.

**Dense-graph Dijkstra?** #flashcard
O(V²) array scan, no heap.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
