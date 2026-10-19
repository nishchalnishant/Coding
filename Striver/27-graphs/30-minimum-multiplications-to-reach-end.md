---
module: striver/27-graphs
lesson: 30
topic: Minimum multiplications to reach end
difficulty: Medium
source: https://takeuforward.org/learning/dsa/minimum-multiplications-to-reach-end?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bfs, implicit-graph]
---
# 30. Minimum multiplications to reach end

← [Cheapest flights within K stops](29-cheapest-flights-within-k-stops.md) · [Part 27 index](README.md) · Next → [Number of ways to arrive at destination](31-number-of-ways-to-arrive-at-destination.md)

> [!abstract] Problem at a glance
> **Task:** Starting from `start`, each step multiplies by any `arr[i]` and takes the result mod 100000; return the fewest steps to reach `end` (`-1` if impossible).
> **Key insight:** It is a graph in disguise. There are 100000 nodes (the residues), and each node `x` has edges to `x · a mod 100000` for every `a`. Every step costs 1, so BFS from `start` finds the answer, and the state space is bounded by the modulus no matter how large the numbers get.
> **Difficulty:** Medium · **Pattern:** BFS over a state space
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-multiplications-to-reach-end?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Dijkstra over residues (Striver)](#3-dijkstra-over-residues-striver) · [4. BFS over residues](#4-bfs-over-residues) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `arr`, `start` and `end` (both < 100000), one step replaces the current number `x` by `(x · arr[i]) % 100000` for some `i`. Return the minimum number of steps to turn `start` into `end`, or `-1`.

| Input | Output | Why |
|---|---|---|
| `arr = [2,5,7], start = 3, end = 30` | `2` | 3·2 = 6, 6·5 = 30 |
| `arr = [3,4,65], start = 7, end = 66175` | `4` | 7·3·3·5·65… four steps mod 10⁵ |

**Constraints:** `1 ≤ |arr| ≤ 10⁴`, `1 ≤ arr[i] ≤ 10⁴`, `1 ≤ start, end < 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Dijkstra over residues (Striver) | heap of (steps, value); dist array of size 10⁵ | O(10⁵·|arr|·log) | O(10⁵) |
| BFS over residues | dist array, −1 = unseen; return at discovery of end | O(10⁵·|arr|) | O(10⁵) |

> [!tip] Interview angle
> The key move is recognising the implicit graph and bounding it: 10⁵ states × |arr| edges. Striver codes it with Dijkstra, but every edge weighs 1, so a plain BFS is enough. Ask whether `start == end` should return 0.

---

## 3. Dijkstra over residues (Striver)

**Intuition.** Treat it as weighted shortest path with weight 1 and run heap Dijkstra over residues.

```python
import heapq

def min_mult_dijkstra(arr, start, end):
    MOD = 100000
    dist = [float('inf')] * MOD
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, x = heapq.heappop(pq)
        if x == end:
            return d
        if d > dist[x]:
            continue
        for a in arr:
            y = x * a % MOD
            if d + 1 < dist[y]:
                dist[y] = d + 1
                heapq.heappush(pq, (d + 1, y))
    return -1
```

**Complexity:** time **O(10⁵·|arr|·log)**, space **O(10⁵)**.

---

## 4. BFS over residues

**Intuition.** BFS from `start` with a `dist` array of size 100000. Return as soon as `end` is discovered.

**Algorithm**

1. If `start == end`, return 0.
2. `dist[start] = 0`; enqueue `start`.
3. Pop `x`; for each `a`: `y = x·a mod 10⁵`; if unseen, set `dist[y] = dist[x] + 1`; return it if `y == end`; enqueue.
4. Return −1.

**Dry run** — [2,5,7], 3 → 30: level 1 {6,15,21}; from 6: 12, 30 → found at 2.

**C++**
```cpp
int minimumMultiplications(vector<int>& arr, int start, int end) {
    const int MOD = 100000;
    if (start == end) return 0;
    vector<int> dist(MOD, -1);
    dist[start] = 0;
    queue<int> q; q.push(start);
    while (!q.empty()) {
        int x = q.front(); q.pop();
        for (int a : arr) {
            int y = (int)((long long)x * a % MOD);
            if (dist[y] == -1) {
                dist[y] = dist[x] + 1;
                if (y == end) return dist[y];
                q.push(y);
            }
        }
    }
    return -1;
}
```

**Java**
```java
static int minimumMultiplications(int[] arr, int start, int end) {
    final int MOD = 100000;
    if (start == end) return 0;
    int[] dist = new int[MOD];
    Arrays.fill(dist, -1);
    dist[start] = 0;
    ArrayDeque<Integer> q = new ArrayDeque<>();
    q.add(start);
    while (!q.isEmpty()) {
        int x = q.poll();
        for (int a : arr) {
            int y = (int) ((long) x * a % MOD);
            if (dist[y] == -1) {
                dist[y] = dist[x] + 1;
                if (y == end) return dist[y];
                q.add(y);
            }
        }
    }
    return -1;
}
```

**Python**
```python
from collections import deque

def minimum_multiplications(arr, start, end):
    MOD = 100000
    if start == end:
        return 0
    dist = [-1] * MOD
    dist[start] = 0
    q = deque([start])
    while q:
        x = q.popleft()
        for a in arr:
            y = x * a % MOD
            if dist[y] == -1:
                dist[y] = dist[x] + 1
                if y == end:
                    return dist[y]
                q.append(y)
    return -1
```

**Complexity:** time **O(10⁵·|arr|)**, space **O(10⁵)** — each of the 10⁵ residues is expanded at most once, with |arr| edges.

---

## Edge cases

- `start == end`: 0.
- Multipliers that only cycle (e.g. all 1s): −1 unless already equal.
- `x · a` can reach 10⁹: fits in 32-bit, but cast to 64-bit to be safe.

---

## Common mistakes

1. Forgetting the mod when indexing `dist`.
2. Unbounded BFS without a visited array.
3. Returning `dist[end]` without handling `start == end`.

---

## Follow-ups

1. Additions instead of multiplications?
2. Return the multipliers used?

<details><summary>Answer sketches</summary>

**#1:** Same BFS with `(x + a) % MOD`.

**#2:** Store the parent residue and the multiplier at discovery.
</details>

---

## Flashcards

**Minimum multiplications: graph?** #flashcard
Nodes are residues mod 10⁵; edges x → x·a mod 10⁵.

**Why is BFS enough?** #flashcard
Every step costs 1.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
