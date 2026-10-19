---
module: striver/27-graphs
lesson: 36
topic: Swim in rising water
difficulty: Hard
source: https://takeuforward.org/learning/dsa/swim-in-rising-water?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, dijkstra, grid, minimax]
---
# 36. Swim in rising water

← [Network delay time](35-network-delay-time.md) · [Part 27 index](README.md) · Next → [Disjoint Set (Union-Find)](37-disjoint-set.md)

> [!abstract] Problem at a glance
> **Task:** On an `n × n` grid of distinct elevations, return the earliest time `t` at which you can swim from top-left to bottom-right through cells with elevation ≤ `t`.
> **Key insight:** A path is usable at time `t` iff its highest cell is ≤ `t`. So the answer is the minimum over paths of the **maximum cell** on the path, a minimax path, exactly like Minimum Effort but with node weights. Dijkstra with `new = max(cur, grid[x][y])`, starting from `grid[0][0]`, pops the target at the optimal time.
> **Difficulty:** Hard · **Pattern:** Dijkstra with a minimax cost · **Also on:** LC 778
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/swim-in-rising-water?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Binary search on time + DFS](#3-binary-search-on-time--dfs) · [4. Min-heap flood (Dijkstra)](#4-min-heap-flood-dijkstra) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`grid` is an `n × n` permutation of `0..n²−1`. At time `t` the water level is `t`, and you can move 4-directionally between cells whose elevations are both ≤ `t` (moving is instant). Starting at `(0,0)`, return the least time at which you can reach `(n−1, n−1)`.

| Input | Output | Why |
|---|---|---|
| `[[0,2],[1,3]]` | `3` | the target itself has elevation 3 |
| `5×5 spiral` | `16` | the cheapest route must cross 16 |

**Constraints:** `1 ≤ n ≤ 50`, the values are a permutation of `0..n²−1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Binary search on time + DFS | smallest t whose ≤t cells connect the corners | O(n² log n²) | O(n²) |
| Min-heap flood (Dijkstra) | always expand the lowest reachable cell; track the max so far | O(n² log n) | O(n²) |

> [!tip] Interview angle
> Recognise it as the twin of Path With Minimum Effort. Three solutions again: binary search on `t` + DFS (O(n² log n²)), Dijkstra/min-heap 'flood' (O(n² log n)), and union-find, adding cells in elevation order until the corners connect. Don't forget that the start cell's own elevation counts.

---

## 3. Binary search on time + DFS

**Intuition.** Reachability is monotone in `t`. Binary search `t ∈ [grid[0][0], n² − 1]`, checking with an iterative DFS over cells ≤ `t`.

```python
def swim_bs(grid):
    n = len(grid)
    def ok(t):
        if grid[0][0] > t:
            return False
        seen = [[False] * n for _ in range(n)]
        seen[0][0] = True
        st = [(0, 0)]
        while st:
            r, c = st.pop()
            if (r, c) == (n - 1, n - 1):
                return True
            for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= x < n and 0 <= y < n and not seen[x][y] and grid[x][y] <= t:
                    seen[x][y] = True
                    st.append((x, y))
        return False
    lo, hi = grid[0][0], n * n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Complexity:** time **O(n² log n²)**, space **O(n²)**.

---

## 4. Min-heap flood (Dijkstra)

**Intuition.** Push `(grid[0][0], 0, 0)`. Pop the lowest frontier cell, raise `t` to its elevation if needed, and stop at the target. Each cell is visited once, because the first pop is optimal.

**Algorithm**

1. `seen[0][0] = True`; heap `[(grid[0][0], 0, 0)]`.
2. Pop `(t, r, c)`; if it is the target, return `t`.
3. For each unseen neighbour: mark it, push `(max(t, grid[x][y]), x, y)`.
4. (The target is always reachable.)

**Dry run** — [[0,2],[1,3]]: pop (0) → push (2,(0,1)), (1,(1,0)). Pop 1 → push (3,(1,1)). Pop 2 → (1,1) already seen. Pop 3 = target → 3.

**C++**
```cpp
int swimInWater(vector<vector<int>>& grid) {
    int n = grid.size();
    vector<vector<bool>> seen(n, vector<bool>(n, false));
    priority_queue<array<int, 3>, vector<array<int, 3>>, greater<>> pq;
    seen[0][0] = true;
    pq.push({grid[0][0], 0, 0});
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!pq.empty()) {
        auto [t, r, c] = pq.top(); pq.pop();
        if (r == n - 1 && c == n - 1) return t;
        for (int k = 0; k < 4; k++) {
            int x = r + dr[k], y = c + dc[k];
            if (x < 0 || x >= n || y < 0 || y >= n || seen[x][y]) continue;
            seen[x][y] = true;
            pq.push({max(t, grid[x][y]), x, y});
        }
    }
    return -1;
}
```

**Java**
```java
static int swimInWater(int[][] grid) {
    int n = grid.length;
    boolean[][] seen = new boolean[n][n];
    seen[0][0] = true;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
    pq.add(new int[]{grid[0][0], 0, 0});
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    while (!pq.isEmpty()) {
        int[] p = pq.poll();
        int t = p[0], r = p[1], c = p[2];
        if (r == n - 1 && c == n - 1) return t;
        for (int k = 0; k < 4; k++) {
            int x = r + dr[k], y = c + dc[k];
            if (x < 0 || x >= n || y < 0 || y >= n || seen[x][y]) continue;
            seen[x][y] = true;
            pq.add(new int[]{Math.max(t, grid[x][y]), x, y});
        }
    }
    return -1;
}
```

**Python**
```python
import heapq

def swim_in_water(grid):
    n = len(grid)
    seen = [[False] * n for _ in range(n)]
    seen[0][0] = True
    pq = [(grid[0][0], 0, 0)]
    while pq:
        t, r, c = heapq.heappop(pq)
        if (r, c) == (n - 1, n - 1):
            return t
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < n and 0 <= y < n and not seen[x][y]:
                seen[x][y] = True
                heapq.heappush(pq, (max(t, grid[x][y]), x, y))
    return -1
```

**Complexity:** time **O(n² log n)**, space **O(n²)** — each of the n² cells is pushed once.

---

## Edge cases

- n = 1: `grid[0][0]`.
- The start cell is the highest on every path: the answer is at least `grid[0][0]`.
- The target cell's elevation is a lower bound too.

---

## Common mistakes

1. Starting the heap at time 0 instead of `grid[0][0]`.
2. Summing elevations.
3. Marking cells seen on pop and re-pushing them many times (correct but slower).

---

## Follow-ups

1. Why is mark-on-push safe here but not in general Dijkstra?
2. Union-find solution?

<details><summary>Answer sketches</summary>

**#1:** Node weights: a cell's cost is max(path max, its own height), and any later route reaches it through a frontier cell with value ≥ the current pop, so the first push already has the optimal value.

**#2:** Process cells in increasing elevation, union with already-active neighbours, and stop when (0,0) and (n−1,n−1) share a root; the current elevation is the answer.
</details>

---

## Flashcards

**Swim in rising water = ?** #flashcard
Minimax path over cell elevations.

**Swim in rising water heap start?** #flashcard
(grid[0][0], 0, 0).

**Twin problem of LC 778?** #flashcard
Path with minimum effort (LC 1631).

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
