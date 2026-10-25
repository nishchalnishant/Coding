---
module: striver-a2z/27-graphs
lesson: 32
topic: Bellman-Ford algorithm
difficulty: Medium
source: https://takeuforward.org/learning/dsa/bellman-ford-algorithm?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bellman-ford, negative-weights, shortest-path]
---
# 32. Bellman-Ford algorithm

← [Number of ways to arrive at destination](31-number-of-ways-to-arrive-at-destination.md) · [Part 27 index](README.md) · Next → [Floyd Warshall algorithm](33-floyd-warshall.md)

> [!abstract] Problem at a glance
> **Task:** Return single-source shortest distances in a directed graph that may have negative edges (`10⁸` for unreachable), or `[-1]` if a negative cycle is reachable from the source.
> **Key insight:** A shortest path without cycles has at most `V − 1` edges. Relaxing **every** edge once extends every correct prefix by at least one edge, so `V − 1` full rounds finalise every distance. If a `V`-th round can still improve something, some 'shortest path' needs more than `V − 1` edges, which is only possible if there is a negative cycle.
> **Difficulty:** Medium · **Pattern:** Bellman-Ford
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/bellman-ford-algorithm?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. SPFA (queue-based Bellman-Ford)](#3-spfa-queue-based-bellman-ford) · [4. Bellman-Ford (V − 1 rounds + check)](#4-bellman-ford-v--1-rounds--check) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A directed graph has `V` nodes and weighted edges `[u, v, w]` (weights may be negative). Return the shortest distance from `src` to each node, using `10⁸` for unreachable nodes. If a negative-weight cycle is reachable from `src`, return `[-1]`.

| Input | Output | Why |
|---|---|---|
| `V = 3, edges = [[0,1,5],[1,0,3],[1,2,-1],[2,0,1]], src = 2` | `[1,6,0]` | 2→0 = 1, 2→0→1 = 6 |
| `V = 3, edges = [[0,1,1],[1,2,-2],[2,0,-1]], src = 0` | `[-1]` | the cycle 0→1→2→0 weighs −2 |

**Constraints:** `1 ≤ V ≤ 500`, `1 ≤ E ≤ V·(V−1)`, `−1000 ≤ w ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| SPFA (queue-based Bellman-Ford) | only re-relax from nodes whose distance changed | O(V·E) worst, often ~O(E) | O(V + E) |
| Bellman-Ford (V − 1 rounds + check) | relax all edges V−1 times; one more improving pass ⇒ negative cycle | O(V·E) | O(V) |

> [!tip] Interview angle
> Say all three facts: V − 1 rounds suffice; a V-th improving round proves a negative cycle; and it works for directed graphs. An undirected negative edge is itself a 2-cycle. Mention the early-exit optimisation (stop when a round changes nothing) and that SPFA is the queue-based variant, which is often faster in practice but has the same worst case.

---

## 3. SPFA (queue-based Bellman-Ford)

**Intuition.** Keep a queue of nodes whose distance just dropped; only their out-edges can produce new improvements. Count how many times each node is enqueued; reaching `V` means a negative cycle.

```python
from collections import deque

def bellman_ford_spfa(V, edges, src):
    BIG = 10 ** 8
    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
    d = [BIG] * V
    d[src] = 0
    inq, cnt = [False] * V, [0] * V
    q = deque([src])
    inq[src], cnt[src] = True, 1
    while q:
        u = q.popleft()
        inq[u] = False
        for v, w in adj[u]:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                if not inq[v]:
                    cnt[v] += 1
                    if cnt[v] >= V + 1:
                        return [-1]
                    inq[v] = True
                    q.append(v)
    return d
```

**Complexity:** time **O(V·E) worst, often ~O(E)**, space **O(V + E)**.

---

## 4. Bellman-Ford (V − 1 rounds + check)

**Intuition.** Initialise distances to `10⁸` except `src = 0`. Repeat `V − 1` times: relax every edge whose tail is reachable. Then scan once more; any improvement means a reachable negative cycle.

**Algorithm**

1. `dist = [10⁸]·V`, `dist[src] = 0`.
2. Repeat V − 1 times: for every `(u, v, w)` with `dist[u] ≠ 10⁸`: `dist[v] = min(dist[v], dist[u] + w)`.
3. One more pass: if any edge still relaxes, return `[-1]`.
4. Return `dist`.

**Dry run** — Example 1, src 2: round 1 → d0 = 1, d1 = 6 (via 0→1 = 1 + 5). Round 2 → no change. Check passes. [1,6,0].

**C++**
```cpp
vector<int> bellmanFord(int V, vector<vector<int>>& edges, int src) {
    const int BIG = 1e8;
    vector<int> d(V, BIG);
    d[src] = 0;
    for (int r = 0; r < V - 1; r++) {
        bool changed = false;
        for (auto& e : edges)
            if (d[e[0]] != BIG && d[e[0]] + e[2] < d[e[1]]) { d[e[1]] = d[e[0]] + e[2]; changed = true; }
        if (!changed) break;
    }
    for (auto& e : edges)
        if (d[e[0]] != BIG && d[e[0]] + e[2] < d[e[1]]) return {-1};
    return d;
}
```

**Java**
```java
static int[] bellmanFord(int V, int[][] edges, int src) {
    final int BIG = 100000000;
    int[] d = new int[V];
    Arrays.fill(d, BIG);
    d[src] = 0;
    for (int r = 0; r < V - 1; r++) {
        boolean changed = false;
        for (int[] e : edges)
            if (d[e[0]] != BIG && d[e[0]] + e[2] < d[e[1]]) { d[e[1]] = d[e[0]] + e[2]; changed = true; }
        if (!changed) break;
    }
    for (int[] e : edges)
        if (d[e[0]] != BIG && d[e[0]] + e[2] < d[e[1]]) return new int[]{-1};
    return d;
}
```

**Python**
```python
def bellman_ford(V, edges, src):
    BIG = 10 ** 8
    d = [BIG] * V
    d[src] = 0
    for _ in range(V - 1):
        changed = False
        for u, v, w in edges:
            if d[u] != BIG and d[u] + w < d[v]:
                d[v] = d[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if d[u] != BIG and d[u] + w < d[v]:
            return [-1]
    return d
```

**Complexity:** time **O(V·E)**, space **O(V)** — V − 1 passes over E edges, plus one check pass.

---

## Edge cases

- A negative cycle **not** reachable from `src`: ignored (the reachability guard).
- Unreachable nodes stay `10⁸`.
- V = 1: one node, no rounds.

---

## Common mistakes

1. Relaxing from unreachable nodes (`10⁸ + (−5) < 10⁸` looks like an improvement).
2. Running only V − 2 rounds or skipping the final check.
3. Using it on an undirected graph with a negative edge: that edge alone is a negative cycle.

---

## Follow-ups

1. Which nodes are affected by a negative cycle?
2. Why exactly V − 1 rounds?

<details><summary>Answer sketches</summary>

**#1:** Every node reachable from a node that still relaxes in round V: mark them −∞ with a BFS.

**#2:** A simple path has at most V − 1 edges; round i finalises every node whose shortest path has i edges.
</details>

---

## Flashcards

**Bellman-Ford rounds?** #flashcard
V − 1 relaxations of every edge.

**Negative cycle detection?** #flashcard
A V-th pass that still relaxes an edge.

**Bellman-Ford time?** #flashcard
O(V·E).

**Guard needed when relaxing?** #flashcard
Skip edges whose tail is still 'infinity'.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
