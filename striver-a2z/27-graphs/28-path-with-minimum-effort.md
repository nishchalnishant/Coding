---
module: striver-a2z/27-graphs
lesson: 28
topic: Path with minimum effort
difficulty: Medium
source: https://takeuforward.org/learning/dsa/path-with-minimum-effort?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, dijkstra, grid, minimax]
---
# 28. Path with minimum effort

← [Shortest distance in a binary maze](27-shortest-distance-binary-maze.md) · [Part 27 index](README.md) · Next → [Cheapest flights within K stops](29-cheapest-flights-within-k-stops.md)

> [!abstract] Problem at a glance
> **Task:** Return the minimum possible **maximum** absolute height difference between consecutive cells on a path from top-left to bottom-right.
> **Key insight:** Path cost here is a **bottleneck**, `max` of the edge weights, not a sum. Dijkstra still works, because `max` never decreases along a path (it is monotone), just like a sum of non-negative weights. Relax with `new = max(effort[u], |h[v] − h[u]|)`, and the first time the target is popped, its effort is optimal.
> **Difficulty:** Medium · **Pattern:** Dijkstra with a minimax cost · **Also on:** LC 1631
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/path-with-minimum-effort?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Binary search on effort + DFS](#3-binary-search-on-effort--dfs) · [4. Dijkstra on max-step](#4-dijkstra-on-max-step) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `n × m` grid `heights`, move up/down/left/right from `(0,0)` to `(n−1,m−1)`. A path's effort is the maximum absolute difference in heights between two consecutive cells. Return the minimum effort.

| Input | Output | Why |
|---|---|---|
| `heights = [[1,2,2],[3,8,2],[5,3,5]]` | `2` | path 1→3→5→3→5 has max step 2 |
| `heights = [[1,2,3],[3,8,4],[5,3,5]]` | `1` | 1→2→3→4→5 |

**Constraints:** `1 ≤ n, m ≤ 100`, `1 ≤ heights[i][j] ≤ 10⁶`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Binary search on effort + DFS | smallest k such that corners connect using steps ≤ k | O(nm log H) | O(nm) |
| Dijkstra on max-step | heap of (effort, r, c); relax with max | O(nm log nm) | O(nm) |

> [!tip] Interview angle
> Offer three solutions and rank them: binary search on the answer + BFS feasibility (O(nm log H)), Dijkstra with max (O(nm log nm)), and union-find adding edges in increasing weight until the corners connect (Kruskal-style). Say why Dijkstra applies: the cost function is monotone along a path.

---

## 3. Binary search on effort + DFS

**Intuition.** Feasibility is monotone in `k`: if a path exists with every step ≤ k, it exists for k + 1 too. Binary search `k` in `[0, 10⁶]` and check reachability with an iterative DFS that only takes steps ≤ k.

```python
def min_effort_bs(h):
    n, m = len(h), len(h[0])
    def ok(k):
        seen = [[False] * m for _ in range(n)]
        seen[0][0] = True
        st = [(0, 0)]
        while st:
            r, c = st.pop()
            if (r, c) == (n - 1, m - 1):
                return True
            for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= x < n and 0 <= y < m and not seen[x][y] and abs(h[x][y] - h[r][c]) <= k:
                    seen[x][y] = True
                    st.append((x, y))
        return False
    lo, hi = 0, 10 ** 6
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Complexity:** time **O(nm log H)**, space **O(nm)**.

---

## 4. Dijkstra on max-step

**Intuition.** `eff[r][c]` = the best known effort to reach the cell. Pop the smallest; moving to a neighbour costs `max(eff, |Δh|)`. Return when the bottom-right cell is popped.

**Algorithm**

1. `eff = ∞` grid, `eff[0][0] = 0`; heap `[(0, 0, 0)]`.
2. Pop `(e, r, c)`; if it is the target, return `e`; skip if stale.
3. For each neighbour: `ne = max(e, |h[x][y] − h[r][c]|)`; if `ne < eff[x][y]`, update and push.
4. (The target is always reachable, so the loop returns.)

**Dry run** — Example 2: the path along 1,2,3,4,5 never exceeds 1, so (1,(…)) entries reach (2,2) with effort 1 before any effort-2 entry is popped.

**C++**
```cpp
int minimumEffort(vector<vector<int>>& h) {
    int n = h.size(), m = h[0].size();
    vector<vector<int>> eff(n, vector<int>(m, INT_MAX));
    priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> pq;
    eff[0][0] = 0;
    pq.push({0, 0, 0});
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!pq.empty()) {
        auto [e, r, c] = pq.top(); pq.pop();
        if (r == n - 1 && c == m - 1) return e;
        if (e > eff[r][c]) continue;
        for (int k = 0; k < 4; k++) {
            int x = r + dr[k], y = c + dc[k];
            if (x < 0 || x >= n || y < 0 || y >= m) continue;
            int ne = max(e, abs(h[x][y] - h[r][c]));
            if (ne < eff[x][y]) { eff[x][y] = ne; pq.push({ne, x, y}); }
        }
    }
    return 0;
}
```

**Java**
```java
static int minimumEffort(int[][] h) {
    int n = h.length, m = h[0].length;
    int[][] eff = new int[n][m];
    for (int[] row : eff) Arrays.fill(row, Integer.MAX_VALUE);
    eff[0][0] = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
    pq.add(new int[]{0, 0, 0});
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    while (!pq.isEmpty()) {
        int[] t = pq.poll();
        int e = t[0], r = t[1], c = t[2];
        if (r == n - 1 && c == m - 1) return e;
        if (e > eff[r][c]) continue;
        for (int k = 0; k < 4; k++) {
            int x = r + dr[k], y = c + dc[k];
            if (x < 0 || x >= n || y < 0 || y >= m) continue;
            int ne = Math.max(e, Math.abs(h[x][y] - h[r][c]));
            if (ne < eff[x][y]) { eff[x][y] = ne; pq.add(new int[]{ne, x, y}); }
        }
    }
    return 0;
}
```

**Python**
```python
import heapq

def minimum_effort(h):
    n, m = len(h), len(h[0])
    INF = float('inf')
    eff = [[INF] * m for _ in range(n)]
    eff[0][0] = 0
    pq = [(0, 0, 0)]
    while pq:
        e, r, c = heapq.heappop(pq)
        if (r, c) == (n - 1, m - 1):
            return e
        if e > eff[r][c]:
            continue
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < n and 0 <= y < m:
                ne = max(e, abs(h[x][y] - h[r][c]))
                if ne < eff[x][y]:
                    eff[x][y] = ne
                    heapq.heappush(pq, (ne, x, y))
    return 0
```

**Complexity:** time **O(nm log nm)**, space **O(nm)** — Dijkstra over nm cells with ≤ 4 edges each.

---

## Edge cases

- 1×1 grid: 0.
- A single row or column: the max adjacent difference along it.
- Equal heights everywhere: 0.

---

## Common mistakes

1. Summing differences instead of taking the max.
2. Returning `eff[target]` after a BFS in plain order: BFS ignores the costs.
3. Binary search with the wrong monotone direction.

---

## Follow-ups

1. Union-find solution?
2. Swim in Rising Water?

<details><summary>Answer sketches</summary>

**#1:** Sort all adjacent-cell edges by |Δh|; union them in order until (0,0) and (n−1,m−1) connect; the last weight added is the answer.

**#2:** The same minimax idea with cell weights instead of edge weights.
</details>

---

## Flashcards

**Minimum effort path cost function?** #flashcard
Max of step differences (bottleneck).

**Why does Dijkstra work for max-cost paths?** #flashcard
The path cost is monotone non-decreasing as the path extends.

**Three solutions to minimax paths?** #flashcard
Binary search + BFS, Dijkstra with max, Kruskal-style DSU.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
