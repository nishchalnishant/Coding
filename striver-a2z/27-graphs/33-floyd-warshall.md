---
module: striver-a2z/27-graphs
lesson: 33
topic: Floyd Warshall algorithm
difficulty: Medium
source: https://takeuforward.org/learning/dsa/floyd-warshall-algorithm?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, floyd-warshall, dp, shortest-path]
---
# 33. Floyd Warshall algorithm

← [Bellman-Ford algorithm](32-bellman-ford.md) · [Part 27 index](README.md) · Next → [Find the city with the smallest number of neighbors at a threshold distance](34-city-with-smallest-neighbors-at-threshold.md)

> [!abstract] Problem at a glance
> **Task:** Given an adjacency matrix (`-1` = no edge), replace it in place by all-pairs shortest distances (`-1` if unreachable).
> **Key insight:** DP over allowed intermediate nodes. After phase `k`, `d[i][j]` is the shortest `i → j` path whose intermediate nodes all lie in `{0..k}`. Allowing node `k` either doesn't help, or splits the path into `i → k` and `k → j`, both using only `{0..k−1}`: `d[i][j] = min(d[i][j], d[i][k] + d[k][j])`. **`k` must be the outermost loop.**
> **Difficulty:** Medium · **Pattern:** All-pairs DP (Floyd-Warshall)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/floyd-warshall-algorithm?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Dijkstra from every node](#3-dijkstra-from-every-node) · [4. Floyd-Warshall triple loop](#4-floyd-warshall-triple-loop) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`matrix` is an `n × n` adjacency matrix of a directed weighted graph: `matrix[i][j]` is the weight of edge `i → j`, or `-1` if there is none (`matrix[i][i] = 0`). Modify it in place so `matrix[i][j]` is the shortest distance from `i` to `j`, or `-1` if `j` is unreachable from `i`.

| Input | Output | Why |
|---|---|---|
| `[[0,1,43],[1,0,6],[-1,-1,0]]` | `[[0,1,7],[1,0,6],[-1,-1,0]]` | 0→1→2 = 7 beats 43 |
| `[[0,25],[-1,0]]` | `[[0,25],[-1,0]]` | nothing to improve |

**Constraints:** `1 ≤ n ≤ 100`, `0 ≤ w ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Dijkstra from every node | n heap Dijkstras (non-negative weights only) | O(n·E log n) | O(n²) |
| Floyd-Warshall triple loop | for k: for i: for j: d[i][j] = min(d[i][j], d[i][k] + d[k][j]) | O(n³) | O(1) extra |

> [!tip] Interview angle
> It handles negative edges, and detects negative cycles: some `d[i][i] < 0` afterwards. Use it when n ≤ ~400 or when you need all pairs on a dense graph. Otherwise run Dijkstra from every node: O(V·E log V). Convert `-1` to a large sentinel before the triple loop and back afterwards.

---

## 3. Dijkstra from every node

**Intuition.** All-pairs = n single-source runs. Better on sparse graphs, but it requires non-negative weights.

```python
import heapq

def floyd_by_dijkstra(m):
    n = len(m)
    INF = float('inf')
    adj = [[(j, m[i][j]) for j in range(n) if m[i][j] != -1 and i != j] for i in range(n)]
    for s in range(n):
        d = [INF] * n
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
        m[s] = [x if x < INF else -1 for x in d]
```

**Complexity:** time **O(n·E log n)**, space **O(n²)**.

---

## 4. Floyd-Warshall triple loop

**Intuition.** Replace `-1` with a sentinel larger than any path, run the k-i-j loop in place, then restore `-1`. Updating in place is safe: in phase `k`, `d[i][k]` and `d[k][j]` don't change (`d[k][k] = 0`).

**Algorithm**

1. Map every `-1` to `BIG` (e.g. 10⁹).
2. For `k` in 0..n−1, `i` in 0..n−1, `j` in 0..n−1: if `d[i][k] + d[k][j] < d[i][j]`, update.
3. Map every value ≥ `BIG` back to −1.

**Dry run** — Example 1: k = 0 → d[1][2] stays 6. k = 1 → d[0][2] = min(43, 1 + 6) = 7. k = 2 → no change.

**C++**
```cpp
void shortestDistance(vector<vector<int>>& m) {
    int n = m.size();
    const int BIG = 1e9;
    for (auto& r : m) for (int& x : r) if (x == -1) x = BIG;
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (m[i][k] < BIG && m[k][j] < BIG && m[i][k] + m[k][j] < m[i][j]) m[i][j] = m[i][k] + m[k][j];
    for (auto& r : m) for (int& x : r) if (x >= BIG) x = -1;
}
```

**Java**
```java
static void shortestDistance(int[][] m) {
    int n = m.length;
    final int BIG = 1000000000;
    for (int[] r : m) for (int j = 0; j < n; j++) if (r[j] == -1) r[j] = BIG;
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (m[i][k] < BIG && m[k][j] < BIG && m[i][k] + m[k][j] < m[i][j]) m[i][j] = m[i][k] + m[k][j];
    for (int[] r : m) for (int j = 0; j < n; j++) if (r[j] >= BIG) r[j] = -1;
}
```

**Python**
```python
def shortest_distance(m):
    n = len(m)
    BIG = 10 ** 9
    for i in range(n):
        for j in range(n):
            if m[i][j] == -1:
                m[i][j] = BIG
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if m[i][k] + m[k][j] < m[i][j]:
                    m[i][j] = m[i][k] + m[k][j]
    for i in range(n):
        for j in range(n):
            if m[i][j] >= BIG:
                m[i][j] = -1
```

**Complexity:** time **O(n³)**, space **O(1) extra** — three nested loops of n.

---

## Edge cases

- n = 1.
- No edges at all: only the diagonal is 0.
- Sentinel + sentinel overflows `int` in C++/Java: guard or use 10⁹ with the `< BIG` checks.

---

## Common mistakes

1. Putting `k` in an inner loop, which gives wrong answers.
2. Running the loop with `-1` still in the matrix (treated as a negative edge).
3. `INT_MAX` as the sentinel, which overflows when two are added.

---

## Follow-ups

1. Detect a negative cycle?
2. Transitive closure (reachability only)?
3. Reconstruct paths?

<details><summary>Answer sketches</summary>

**#1:** After the loop, any `d[i][i] < 0`.

**#2:** The same loop with `reach[i][j] |= reach[i][k] && reach[k][j]` (Warshall).

**#3:** Keep `next[i][j]`; on an update via k set `next[i][j] = next[i][k]`.
</details>

---

## Flashcards

**Floyd-Warshall recurrence?** #flashcard
d[i][j] = min(d[i][j], d[i][k] + d[k][j]).

**Which loop is outermost?** #flashcard
k (the intermediate node).

**Floyd-Warshall negative-cycle test?** #flashcard
Some d[i][i] < 0 at the end.

**Floyd-Warshall time/space?** #flashcard
O(n³) / O(n²).

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
