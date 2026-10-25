---
module: striver-a2z/27-graphs
lesson: 35
topic: Network delay time
difficulty: Medium
source: https://takeuforward.org/learning/dsa/network-delay-time?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, dijkstra, shortest-path]
---
# 35. Network delay time

← [Find the city with the smallest number of neighbors at a threshold distance](34-city-with-smallest-neighbors-at-threshold.md) · [Part 27 index](README.md) · Next → [Swim in rising water](36-swim-in-rising-water.md)

> [!abstract] Problem at a glance
> **Task:** A signal starts at node `k`; return the time until every node has received it (`-1` if some node never does).
> **Key insight:** Each node receives the signal at its shortest-path distance from `k`. Everyone has it once the **farthest** node does, so the answer is `max(dist)` from one Dijkstra run, or −1 if any distance is infinite.
> **Difficulty:** Medium · **Pattern:** Dijkstra + max · **Also on:** LC 743
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/network-delay-time?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Bellman-Ford](#3-bellman-ford) · [4. Dijkstra](#4-dijkstra) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`times[i] = [u, v, w]` is a directed edge from `u` to `v` taking `w` time, with nodes `1..n`. A signal is sent from `k`. Return the minimum time for all `n` nodes to receive it, or `-1` if that is impossible.

| Input | Output | Why |
|---|---|---|
| `times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2` | `2` | node 4 at time 2 |
| `times = [[1,2,1]], n = 2, k = 2` | `-1` | node 1 is unreachable from 2 |

**Constraints:** `1 ≤ n ≤ 100`, `1 ≤ times.length ≤ 6000`, `0 ≤ w ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Bellman-Ford | n − 1 rounds of relaxing all times | O(n·E) | O(n) |
| Dijkstra | heap from k; answer = max dist | O(E log n) | O(n + E) |

> [!tip] Interview angle
> A 10-minute warm-up: say 'single-source shortest paths, take the max', code heap Dijkstra, and handle the 1-indexing. With n ≤ 100, mention that Bellman-Ford or Floyd also pass.

---

## 3. Bellman-Ford

**Intuition.** Relax every edge `n − 1` times from `k`, then take the max. Simple, and fast enough for n ≤ 100.

```python
def network_delay_bf(times, n, k):
    INF = float('inf')
    d = [INF] * (n + 1)
    d[k] = 0
    for _ in range(n - 1):
        for u, v, w in times:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    ans = max(d[1:])
    return ans if ans < INF else -1
```

**Complexity:** time **O(n·E)**, space **O(n)**.

---

## 4. Dijkstra

**Intuition.** Heap Dijkstra from `k` over 1-indexed nodes; return `max(dist[1..n])`, or −1 if it is ∞.

**Algorithm**

1. Build adjacency for nodes 1..n.
2. Dijkstra from `k`.
3. `ans = max(dist[1..n])`; return −1 if ∞.

**Dry run** — Example 1: d2 = 0 → d1 = 1, d3 = 1 → d4 = 2. max = 2.

**C++**
```cpp
int networkDelayTime(vector<vector<int>>& times, int n, int k) {
    vector<vector<pair<int, int>>> adj(n + 1);
    for (auto& t : times) adj[t[0]].push_back({t[1], t[2]});
    vector<int> d(n + 1, INT_MAX);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    d[k] = 0;
    pq.push({0, k});
    while (!pq.empty()) {
        auto [du, u] = pq.top(); pq.pop();
        if (du > d[u]) continue;
        for (auto [v, w] : adj[u]) if (du + w < d[v]) { d[v] = du + w; pq.push({d[v], v}); }
    }
    int ans = *max_element(d.begin() + 1, d.end());
    return ans == INT_MAX ? -1 : ans;
}
```

**Java**
```java
static int networkDelayTime(int[][] times, int n, int k) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());
    for (int[] t : times) adj.get(t[0]).add(new int[]{t[1], t[2]});
    int[] d = new int[n + 1];
    Arrays.fill(d, Integer.MAX_VALUE);
    d[k] = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
    pq.add(new int[]{0, k});
    while (!pq.isEmpty()) {
        int[] t = pq.poll();
        if (t[0] > d[t[1]]) continue;
        for (int[] e : adj.get(t[1]))
            if (t[0] + e[1] < d[e[0]]) { d[e[0]] = t[0] + e[1]; pq.add(new int[]{d[e[0]], e[0]}); }
    }
    int ans = 0;
    for (int i = 1; i <= n; i++) ans = Math.max(ans, d[i]);
    return ans == Integer.MAX_VALUE ? -1 : ans;
}
```

**Python**
```python
import heapq

def network_delay_time(times, n, k):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in times:
        adj[u].append((v, w))
    INF = float('inf')
    d = [INF] * (n + 1)
    d[k] = 0
    pq = [(0, k)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(pq, (d[v], v))
    ans = max(d[1:])
    return ans if ans < INF else -1
```

**Complexity:** time **O(E log n)**, space **O(n + E)** — one heap Dijkstra.

---

## Edge cases

- n = 1: 0.
- Unreachable node: −1.
- Zero-weight edges: fine.

---

## Common mistakes

1. Including index 0 in the max (it stays ∞ in a 1-indexed array).
2. Summing distances instead of taking the max.
3. Treating edges as undirected.

---

## Follow-ups

1. Time until a specific node?
2. Signal from several sources?

<details><summary>Answer sketches</summary>

**#1:** Its distance; stop Dijkstra when it is popped.

**#2:** Multi-source Dijkstra: push every source with distance 0.
</details>

---

## Flashcards

**Network delay = ?** #flashcard
Max over shortest distances from k.

**Network delay unreachable?** #flashcard
Any distance still ∞ → −1.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
