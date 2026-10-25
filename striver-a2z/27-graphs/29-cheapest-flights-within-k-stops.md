---
module: striver-a2z/27-graphs
lesson: 29
topic: Cheapest flights within K stops
difficulty: Medium
source: https://takeuforward.org/learning/dsa/cheapest-flights-within-k-stops?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bellman-ford, bfs, shortest-path]
---
# 29. Cheapest flights within K stops

← [Path with minimum effort](28-path-with-minimum-effort.md) · [Part 27 index](README.md) · Next → [Minimum multiplications to reach end](30-minimum-multiplications-to-reach-end.md)

> [!abstract] Problem at a glance
> **Task:** Return the cheapest price from `src` to `dst` using at most `k` intermediate stops (`-1` if impossible).
> **Key insight:** The stop limit breaks plain Dijkstra. A route that is more expensive but uses fewer stops may be the only one that can still be extended, so 'cheapest so far' is not final. Make the number of edges the primary dimension. **Bellman-Ford run exactly `k + 1` rounds**, each round relaxing from the *previous* round's snapshot, computes the cheapest cost using at most `k + 1` flights.
> **Difficulty:** Medium · **Pattern:** Bounded-edges shortest path (Bellman-Ford rounds / BFS by stops) · **Also on:** LC 787
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/cheapest-flights-within-k-stops?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. BFS by stops (Striver)](#3-bfs-by-stops-striver) · [4. Bellman-Ford with k + 1 rounds](#4-bellman-ford-with-k--1-rounds) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

There are `n` cities and `flights[i] = [from, to, price]` (directed). Given `src`, `dst` and `k`, return the cheapest price from `src` to `dst` with at most `k` stops in between, or `-1`.

| Input | Output | Why |
|---|---|---|
| `n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1` | `700` | 0→1→3; 0→1→2→3 = 400 needs 2 stops |
| `n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0` | `500` | direct flight only |

**Constraints:** `1 ≤ n ≤ 100`, `0 ≤ flights.length ≤ n·(n−1)/2`, `1 ≤ price ≤ 10⁴`, `0 ≤ k < n`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| BFS by stops (Striver) | queue (stops, node, cost); expand while stops ≤ k | O(k·E) | O(n + E) |
| Bellman-Ford with k + 1 rounds | relax every edge from the previous round's snapshot | O(k·E) | O(n) |

> [!tip] Interview angle
> Striver's solution is a BFS queue of `(stops, node, cost)` with a `dist` array, processed level by level, so stops increase monotonically. Bellman-Ford with a snapshot is the cleanest to prove. Both run in O(k·E). Explain why the snapshot (`prev` copy) is needed: without it a single round can chain several flights.

---

## 3. BFS by stops (Striver)

**Intuition.** The queue holds `(stops, node, cost)`. Since every hop adds one stop, FIFO order processes stops in increasing order. Relax `v` when `cost + w < dist[v]` and `stops ≤ k`. Because stops only increase, a cheaper arrival later always uses at least as many stops, so it is worth recording only if cheaper.

```python
from collections import deque

def cheapest_bfs(n, flights, src, dst, k):
    adj = [[] for _ in range(n)]
    for u, v, w in flights:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    q = deque([(0, src, 0)])
    while q:
        stops, u, cost = q.popleft()
        if stops > k:
            continue
        for v, w in adj[u]:
            if cost + w < dist[v]:
                dist[v] = cost + w
                q.append((stops + 1, v, cost + w))
    return dist[dst] if dist[dst] < INF else -1
```

**Complexity:** time **O(k·E)**, space **O(n + E)**.

---

## 4. Bellman-Ford with k + 1 rounds

**Intuition.** After round `i`, `best[v]` is the cheapest cost using at most `i` flights. Round `i + 1` relaxes every edge **from a copy of the previous round**, so each round adds at most one flight. `k` stops = `k + 1` flights.

**Algorithm**

1. `best = [∞]·n`, `best[src] = 0`.
2. Repeat `k + 1` times: `nb = best[:]`; for each `(u, v, w)` with `best[u] < ∞`: `nb[v] = min(nb[v], best[u] + w)`; `best = nb`.
3. Return `best[dst]` or −1.

**Dry run** — Example 1, k = 1: round 1 → b1 = 100. Round 2 → b2 = 200, b3 = 700 (from b1 = 100 + 600). The 400 route needs round 3. Answer 700.

**C++**
```cpp
int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
    const int INF = INT_MAX;
    vector<int> best(n, INF);
    best[src] = 0;
    for (int r = 0; r <= k; r++) {
        vector<int> nb = best;
        for (auto& f : flights)
            if (best[f[0]] != INF && best[f[0]] + f[2] < nb[f[1]]) nb[f[1]] = best[f[0]] + f[2];
        best = nb;
    }
    return best[dst] == INF ? -1 : best[dst];
}
```

**Java**
```java
static int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
    final int INF = Integer.MAX_VALUE;
    int[] best = new int[n];
    Arrays.fill(best, INF);
    best[src] = 0;
    for (int r = 0; r <= k; r++) {
        int[] nb = best.clone();
        for (int[] f : flights)
            if (best[f[0]] != INF && best[f[0]] + f[2] < nb[f[1]]) nb[f[1]] = best[f[0]] + f[2];
        best = nb;
    }
    return best[dst] == INF ? -1 : best[dst];
}
```

**Python**
```python
def find_cheapest_price(n, flights, src, dst, k):
    INF = float('inf')
    best = [INF] * n
    best[src] = 0
    for _ in range(k + 1):
        nb = best[:]
        for u, v, w in flights:
            if best[u] + w < nb[v]:
                nb[v] = best[u] + w
        best = nb
    return best[dst] if best[dst] < INF else -1
```

**Complexity:** time **O(k·E)**, space **O(n)** — k + 1 rounds over all E flights.

---

## Edge cases

- `k = 0`: only direct flights.
- No route at all: −1.
- Cheaper route exists but exceeds k stops: it must be ignored.

---

## Common mistakes

1. Relaxing in place within a round, which lets one round use several flights.
2. Plain Dijkstra by cost with a `dist` array: it discards the more expensive but shorter-hop routes.
3. Off-by-one: k stops = k + 1 edges.

---

## Follow-ups

1. Dijkstra variant?
2. Exactly k stops?

<details><summary>Answer sketches</summary>

**#1:** Heap ordered by cost over states `(node, stops)`; keep `best_stops[node]` and only expand a pop if it uses fewer stops than any earlier pop of that node.

**#2:** DP over exact edge counts: `dp[i][v]` without carrying over the previous round's values.
</details>

---

## Flashcards

**Why does plain Dijkstra fail with a stop limit?** #flashcard
A pricier route with fewer stops may be the only one that can be extended.

**Bellman-Ford rounds for k stops?** #flashcard
k + 1, each from the previous round's snapshot.

**Why the snapshot copy?** #flashcard
So each round adds at most one edge.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
