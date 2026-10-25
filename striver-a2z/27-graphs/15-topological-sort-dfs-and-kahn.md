---
module: striver-a2z/27-graphs
lesson: 15
topic: Topological sort or Kahn's algorithm
difficulty: Medium
source: https://takeuforward.org/learning/dsa/topological-sort-or-kahns-algorithm?category=hard-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, topological-sort, bfs, dfs]
---
# 15. Topological sort or Kahn's algorithm

← [Bipartite graph](14-bipartite-graph.md) · [Part 27 index](README.md) · Next → [Detect a cycle in a directed graph](16-cycle-in-directed-graph.md)

> [!abstract] Problem at a glance
> **Task:** Return any ordering of the nodes of a DAG such that for every edge `u → v`, `u` comes before `v`.
> **Key insight:** Two equivalent views. **DFS:** a node finishes only after everything reachable from it has finished, so reversed finish order is a topological order. **Kahn (BFS):** a node with in-degree 0 has no remaining prerequisites, so it can go next. Removing it may free its neighbours.
> **Difficulty:** Medium · **Pattern:** Topological sort
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/topological-sort-or-kahns-algorithm?category=hard-problems&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS post-order, reversed](#3-dfs-post-order-reversed) · [4. Kahn's algorithm (BFS on in-degrees)](#4-kahns-algorithm-bfs-on-in-degrees) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a directed acyclic graph with `V` nodes `0..V-1` and edge list `edges` (`[u, v]` means `u → v`), return any topological ordering.

| Input | Output | Why |
|---|---|---|
| `V = 6, edges = [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]` | `[5,4,2,3,1,0] (one of several)` | every edge points forward |
| `V = 3, edges = []` | `[0,1,2] (any permutation)` | no constraints |

**Constraints:** `1 ≤ V ≤ 10⁴`, `0 ≤ E ≤ 10⁵`, the graph is acyclic.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS post-order, reversed | push u after all children finish; reverse | O(V + E) | O(V) |
| Kahn's algorithm (BFS on in-degrees) | queue of in-degree-0 nodes; decrement neighbours | O(V + E) | O(V) |

> [!tip] Interview angle
> Kahn's version detects cycles for free: if fewer than V nodes are output, the leftovers lie on or behind a cycle. It is also iterative and easy to adapt for 'lexicographically smallest order' (use a min-heap instead of a queue). The checker accepts any valid order.

---

## 3. DFS post-order, reversed

**Intuition.** DFS from every unvisited node. Append `u` to a list **after** recursing into all its out-neighbours. Every edge `u → v` has `v` finishing before `u`, so the reversed list is valid.

```python
import sys

def topo_dfs(V, edges):
    sys.setrecursionlimit(10 ** 6)
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
    seen = [False] * V
    out = []
    def go(u):
        seen[u] = True
        for v in adj[u]:
            if not seen[v]:
                go(v)
        out.append(u)
    for s in range(V):
        if not seen[s]:
            go(s)
    return out[::-1]
```

**Complexity:** time **O(V + E)**, space **O(V)**.

---

## 4. Kahn's algorithm (BFS on in-degrees)

**Intuition.** Compute in-degrees. Enqueue every node with in-degree 0. Pop a node, output it, and decrement each out-neighbour's in-degree, enqueuing any that reach 0.

**Algorithm**

1. `indeg[v]` = number of edges into `v`.
2. Queue every node with `indeg = 0`.
3. Pop `u`, append it to the order; for each `u → v`: `indeg[v]--`, enqueue `v` if it hits 0.
4. Return the order (it has `V` nodes when the graph is a DAG).

**Dry run** — Example 1: in-degree 0 = {4,5}. Pop 4 → out 0? indeg[0] 2→1; indeg[1] 2→1. Pop 5 → indeg[2] → 0 (push), indeg[0] → 0 (push). Pop 2 → 3. Pop 0. Pop 3 → 1. Order [4,5,2,0,3,1].

**C++**
```cpp
vector<int> topoSort(int V, vector<vector<int>>& edges) {
    vector<vector<int>> adj(V);
    vector<int> indeg(V, 0), order;
    for (auto& e : edges) { adj[e[0]].push_back(e[1]); indeg[e[1]]++; }
    queue<int> q;
    for (int i = 0; i < V; i++) if (indeg[i] == 0) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    return order;
}
```

**Java**
```java
static int[] topoSort(int V, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
    int[] indeg = new int[V];
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); indeg[e[1]]++; }
    ArrayDeque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < V; i++) if (indeg[i] == 0) q.add(i);
    int[] order = new int[V];
    int k = 0;
    while (!q.isEmpty()) {
        int u = q.poll();
        order[k++] = u;
        for (int v : adj.get(u)) if (--indeg[v] == 0) q.add(v);
    }
    return k == V ? order : new int[0];
}
```

**Python**
```python
from collections import deque

def topo_sort(V, edges):
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(V) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order
```

**Complexity:** time **O(V + E)**, space **O(V)** — each node is enqueued once and each edge decremented once.

---

## Edge cases

- No edges: any permutation is valid.
- Several sources: all start in the queue together.
- A cycle (invalid input here): Kahn outputs fewer than V nodes.

---

## Common mistakes

1. DFS: appending `u` **before** the children (pre-order) instead of after.
2. Forgetting to reverse the DFS finish list.
3. Kahn: computing in-degree from the wrong endpoint (`u` instead of `v`).

---

## Follow-ups

1. Lexicographically smallest topological order?
2. Count the number of topological orders?
3. Parallel scheduling: minimum semesters?

<details><summary>Answer sketches</summary>

**#1:** Kahn with a min-heap instead of a queue: O((V + E) log V).

**#2:** Exponential in general: backtracking (or bitmask DP for V ≤ 20).

**#3:** Kahn level by level; the number of levels is the answer (LC 1136).
</details>

---

## Flashcards

**DFS topological order?** #flashcard
Reverse post-order (finish order reversed).

**Kahn's starting set?** #flashcard
All nodes with in-degree 0.

**How does Kahn detect a cycle?** #flashcard
It outputs fewer than V nodes.

**Smallest-lexicographic topo order?** #flashcard
Kahn with a min-heap.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
