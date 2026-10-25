---
module: striver-a2z/27-graphs
lesson: 31
topic: Number of ways to arrive at destination
difficulty: Medium
source: https://takeuforward.org/learning/dsa/number-of-ways-to-arrive-at-destination?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, dijkstra, counting, shortest-path]
---
# 31. Number of ways to arrive at destination

← [Minimum multiplications to reach end](30-minimum-multiplications-to-reach-end.md) · [Part 27 index](README.md) · Next → [Bellman-Ford algorithm](32-bellman-ford.md)

> [!abstract] Problem at a glance
> **Task:** Count the shortest paths from node `0` to node `n − 1` in a weighted undirected graph, modulo 10⁹+7.
> **Key insight:** Run Dijkstra and carry `ways[v]` with it. A **strict** improvement via `u` means the old paths are no longer shortest, so `ways[v] = ways[u]`. A **tie** means another equally short route arrived, so `ways[v] += ways[u]`. This is correct because Dijkstra pops `u` only once `dist[u]` and `ways[u]` are final, and every shortest path's second-to-last node is popped before `v`.
> **Difficulty:** Medium · **Pattern:** Dijkstra + path counting · **Also on:** LC 1976
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-ways-to-arrive-at-destination?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Dijkstra, then DP in distance order](#3-dijkstra-then-dp-in-distance-order) · [4. Dijkstra with ways array](#4-dijkstra-with-ways-array) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`n` intersections and `roads[i] = [u, v, time]` (undirected, `1 ≤ time ≤ 10⁹`). Return the number of ways to travel from `0` to `n − 1` in the shortest possible time, modulo `10⁹ + 7`.

| Input | Output | Why |
|---|---|---|
| `n = 7, roads = [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],[3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]` | `4` | four routes of time 7 |
| `n = 2, roads = [[1,0,10]]` | `1` | one road |

**Constraints:** `1 ≤ n ≤ 200`, `n − 1 ≤ roads.length ≤ n(n−1)/2`, `1 ≤ time ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Dijkstra, then DP in distance order | dist first; then sum ways over shortest-path edges sorted by dist | O(E log V) | O(V + E) |
| Dijkstra with ways array | improve → ways[v] = ways[u]; tie → ways[v] += ways[u] | O(E log V) | O(V + E) |

> [!tip] Interview angle
> Two traps to flag: distances overflow 32-bit (sums up to 2·10¹¹), so use `long`; and ties must **add** while improvements **reset**. Comparing floats or applying the mod to distances are both instant failures.

---

## 3. Dijkstra, then DP in distance order

**Intuition.** Two phases. Compute `dist`, then process nodes in increasing `dist`: for every edge `u–v` with `dist[u] + w == dist[v]`, add `ways[u]` to `ways[v]`. These edges form a DAG, so the sorted order is topological.

```python
import heapq

def count_paths_two_phase(n, roads):
    MOD = 10 ** 9 + 7
    adj = [[] for _ in range(n)]
    for u, v, w in roads:
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float('inf')
    d = [INF] * n
    d[0] = 0
    pq = [(0, 0)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(pq, (d[v], v))
    ways = [0] * n
    ways[0] = 1
    for u in sorted(range(n), key=lambda x: d[x]):
        for v, w in adj[u]:
            if d[u] + w == d[v]:
                ways[v] = (ways[v] + ways[u]) % MOD
    return ways[n - 1]
```

**Complexity:** time **O(E log V)**, space **O(V + E)**.

---

## 4. Dijkstra with ways array

**Intuition.** One pass. Distances are 64-bit; `ways` is kept modulo 10⁹+7. The stale-entry check guarantees each node propagates its final count exactly once.

**Algorithm**

1. `dist[0] = 0`, `ways[0] = 1`; heap `[(0, 0)]`.
2. Pop `(d, u)`; skip if `d > dist[u]`.
3. For each `(v, w)`: if `d + w < dist[v]`: `dist[v] = d + w`, `ways[v] = ways[u]`, push. Elif equal: `ways[v] += ways[u]` (mod).
4. Return `ways[n−1]`.

**Dry run** — Square 0-1-3, 0-2-3 (all weights 1): pop 0 → d1 = d2 = 1, ways 1, 1. Pop 1 → d3 = 2, ways 1. Pop 2 → tie at 3 → ways 2.

**C++**
```cpp
int countPaths(int n, vector<vector<int>>& roads) {
    const int MOD = 1e9 + 7;
    vector<vector<pair<int, int>>> adj(n);
    for (auto& r : roads) { adj[r[0]].push_back({r[1], r[2]}); adj[r[1]].push_back({r[0], r[2]}); }
    vector<long long> dist(n, LLONG_MAX);
    vector<int> ways(n, 0);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
    dist[0] = 0; ways[0] = 1;
    pq.push({0, 0});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (d + w < dist[v]) { dist[v] = d + w; ways[v] = ways[u]; pq.push({dist[v], v}); }
            else if (d + w == dist[v]) ways[v] = (ways[v] + ways[u]) % MOD;
        }
    }
    return ways[n - 1];
}
```

**Java**
```java
static int countPaths(int n, int[][] roads) {
    final int MOD = 1_000_000_007;
    List<List<int[]>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] r : roads) { adj.get(r[0]).add(new int[]{r[1], r[2]}); adj.get(r[1]).add(new int[]{r[0], r[2]}); }
    long[] dist = new long[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    int[] ways = new int[n];
    dist[0] = 0; ways[0] = 1;
    PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    pq.add(new long[]{0, 0});
    while (!pq.isEmpty()) {
        long[] t = pq.poll();
        long d = t[0];
        int u = (int) t[1];
        if (d > dist[u]) continue;
        for (int[] e : adj.get(u)) {
            int v = e[0];
            if (d + e[1] < dist[v]) { dist[v] = d + e[1]; ways[v] = ways[u]; pq.add(new long[]{dist[v], v}); }
            else if (d + e[1] == dist[v]) ways[v] = (ways[v] + ways[u]) % MOD;
        }
    }
    return ways[n - 1];
}
```

**Python**
```python
import heapq

def count_paths(n, roads):
    MOD = 10 ** 9 + 7
    adj = [[] for _ in range(n)]
    for u, v, w in roads:
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float('inf')
    dist = [INF] * n
    ways = [0] * n
    dist[0], ways[0] = 0, 1
    pq = [(0, 0)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                ways[v] = ways[u]
                heapq.heappush(pq, (dist[v], v))
            elif d + w == dist[v]:
                ways[v] = (ways[v] + ways[u]) % MOD
    return ways[n - 1]
```

**Complexity:** time **O(E log V)**, space **O(V + E)** — standard heap Dijkstra; the ways updates are O(1) per relaxation.

---

## Edge cases

- `n = 1`: one way (stay put).
- Road times up to 10⁹: distances need 64-bit.
- Many ties: counts grow exponentially, hence the modulus.

---

## Common mistakes

1. `int` distances (overflow).
2. On a strict improvement, adding instead of resetting `ways[v]`.
3. Processing stale heap entries, which propagates a node's count twice.

---

## Follow-ups

1. Why is propagating from popped nodes safe?
2. Count shortest paths in an unweighted graph?

<details><summary>Answer sketches</summary>

**#1:** Weights are positive, so every predecessor on a shortest path to v has strictly smaller distance and is finalised (popped) before v propagates.

**#2:** The same idea with BFS levels.
</details>

---

## Flashcards

**Counting shortest paths with Dijkstra?** #flashcard
Improve → copy ways; tie → add ways.

**LC 1976 overflow trap?** #flashcard
Distances up to ~2·10¹¹: use 64-bit.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
