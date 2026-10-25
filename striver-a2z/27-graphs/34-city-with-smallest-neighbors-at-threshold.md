---
module: striver-a2z/27-graphs
lesson: 34
topic: Find the city with the smallest number of neighbors at a threshold distance
difficulty: Medium
source: https://takeuforward.org/learning/dsa/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, floyd-warshall, shortest-path]
---
# 34. Find the city with the smallest number of neighbors at a threshold distance

← [Floyd Warshall algorithm](33-floyd-warshall.md) · [Part 27 index](README.md) · Next → [Network delay time](35-network-delay-time.md)

> [!abstract] Problem at a glance
> **Task:** Return the city that can reach the fewest other cities within `distanceThreshold` (ties → the largest index).
> **Key insight:** It needs every city's distance to every other city, i.e. all-pairs shortest paths, and `n ≤ 100` makes Floyd-Warshall's O(n³) = 10⁶ trivially fast. Then count `d[i][j] ≤ threshold` per row, scanning `i` upward with `≤` so that ties go to the larger index.
> **Difficulty:** Medium · **Pattern:** All-pairs shortest paths + counting · **Also on:** LC 1334
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Dijkstra from every city](#3-dijkstra-from-every-city) · [4. Floyd-Warshall + count](#4-floyd-warshall--count) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`n` cities and bidirectional weighted `edges = [from, to, weight]`. Return the city with the smallest number of cities reachable through some path whose distance is at most `distanceThreshold`. If there are several, return the one with the greatest number.

| Input | Output | Why |
|---|---|---|
| `n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], threshold = 4` | `3` | cities 0 and 3 both reach 2 others; 3 is larger |
| `n = 5, edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]], threshold = 2` | `0` | 0 reaches only 1 |

**Constraints:** `2 ≤ n ≤ 100`, `1 ≤ weight, distanceThreshold ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Dijkstra from every city | n heap runs; count dist ≤ threshold | O(n·E log n) | O(n + E) |
| Floyd-Warshall + count | all-pairs matrix, then count per row | O(n³) | O(n²) |

> [!tip] Interview angle
> Mention the alternative, n Dijkstra runs (O(n · E log n)), which is better for sparse large graphs; here Floyd is simpler. The tie-break is the bug magnet: iterate ascending with `<=`, or descending with `<`.

---

## 3. Dijkstra from every city

**Intuition.** Run Dijkstra from each city and count the others within the threshold. Keep the city with the smallest count, preferring later indices.

```python
import heapq

def find_the_city_dijkstra(n, edges, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    best, ans = n + 1, -1
    for s in range(n):
        d = [float('inf')] * n
        d[s] = 0
        pq = [(0, s)]
        while pq:
            du, u = heapq.heappop(pq)
            if du > d[u]:
                continue
            for v, w in adj[u]:
                if du + w < d[v]:
                    d[v] = du + w
                    heapq.heappush(pq, (d[v], v))
        c = sum(1 for j in range(n) if j != s and d[j] <= t)
        if c <= best:
            best, ans = c, s
    return ans
```

**Complexity:** time **O(n·E log n)**, space **O(n + E)**.

---

## 4. Floyd-Warshall + count

**Intuition.** Fill an n×n matrix with ∞, 0 on the diagonal, and both directions of each edge. Run Floyd-Warshall. For each `i`, count `j ≠ i` with `d[i][j] ≤ t`; update the answer when the count is `≤` the best.

**Algorithm**

1. `d = ∞`, `d[i][i] = 0`, `d[u][v] = d[v][u] = w`.
2. Floyd-Warshall triple loop.
3. For `i` from 0 up: `c = #{j ≠ i : d[i][j] ≤ t}`; if `c ≤ best`, `best = c`, `ans = i`.
4. Return `ans`.

**Dry run** — Example 1: reach counts within 4 are 0→{1,2}, 1→{0,2,3}, 2→{0,1,3}, 3→{1,2}. Min 2 at cities 0 and 3 → 3.

**C++**
```cpp
int findTheCity(int n, vector<vector<int>>& edges, int t) {
    const int BIG = 1e9;
    vector<vector<int>> d(n, vector<int>(n, BIG));
    for (int i = 0; i < n; i++) d[i][i] = 0;
    for (auto& e : edges) { d[e[0]][e[1]] = min(d[e[0]][e[1]], e[2]); d[e[1]][e[0]] = d[e[0]][e[1]]; }
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (d[i][k] < BIG && d[k][j] < BIG) d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
    int best = n + 1, ans = -1;
    for (int i = 0; i < n; i++) {
        int c = 0;
        for (int j = 0; j < n; j++) if (j != i && d[i][j] <= t) c++;
        if (c <= best) { best = c; ans = i; }
    }
    return ans;
}
```

**Java**
```java
static int findTheCity(int n, int[][] edges, int t) {
    final int BIG = 1000000000;
    int[][] d = new int[n][n];
    for (int[] r : d) Arrays.fill(r, BIG);
    for (int i = 0; i < n; i++) d[i][i] = 0;
    for (int[] e : edges) { d[e[0]][e[1]] = Math.min(d[e[0]][e[1]], e[2]); d[e[1]][e[0]] = d[e[0]][e[1]]; }
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (d[i][k] < BIG && d[k][j] < BIG) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
    int best = n + 1, ans = -1;
    for (int i = 0; i < n; i++) {
        int c = 0;
        for (int j = 0; j < n; j++) if (j != i && d[i][j] <= t) c++;
        if (c <= best) { best = c; ans = i; }
    }
    return ans;
}
```

**Python**
```python
def find_the_city(n, edges, t):
    INF = float('inf')
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = d[v][u] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    best, ans = n + 1, -1
    for i in range(n):
        c = sum(1 for j in range(n) if j != i and d[i][j] <= t)
        if c <= best:
            best, ans = c, i
    return ans
```

**Complexity:** time **O(n³)**, space **O(n²)** — the Floyd-Warshall loop dominates; counting is O(n²).

---

## Edge cases

- No edges: every count is 0, so the answer is n − 1.
- Ties: the largest index wins.
- Parallel edges: keep the minimum weight.

---

## Common mistakes

1. Tie-break with `<` while scanning upward (returns the smallest index).
2. Counting the city itself.
3. Forgetting the reverse direction of each edge.

---

## Follow-ups

1. n = 10⁴, sparse?
2. Return the counts for all cities?

<details><summary>Answer sketches</summary>

**#1:** n Dijkstras, or prune each Dijkstra once distances exceed the threshold.

**#2:** The per-row counts are already computed.
</details>

---

## Flashcards

**LC 1334 tool of choice?** #flashcard
Floyd-Warshall (n ≤ 100), then count per row.

**LC 1334 tie-break?** #flashcard
Largest index: scan ascending with `<=`.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
