---
module: striver-a2z/27-graphs
lesson: 14
topic: Bipartite graph
difficulty: Medium
source: https://takeuforward.org/learning/dsa/bipartite-graph?category=cycles&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bfs, bipartite]
---
# 14. Bipartite graph

← [Detect a cycle in an undirected graph](13-cycle-in-undirected-graph.md) · [Part 27 index](README.md) · Next → [Topological sort or Kahn's algorithm](15-topological-sort-dfs-and-kahn.md)

> [!abstract] Problem at a glance
> **Task:** Decide whether the nodes can be 2-coloured so that every edge joins different colours.
> **Key insight:** Colour greedily. The first node of a component gets colour 0, and every neighbour is forced to the opposite colour. The choice for the first node never matters, because swapping colours gives a mirror solution. So the graph is bipartite iff this forced colouring never meets an edge with both ends the same colour. Equivalently, there is **no odd cycle**.
> **Difficulty:** Medium · **Pattern:** BFS 2-colouring · **Also on:** LC 785
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/bipartite-graph?category=cycles&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS colouring](#3-dfs-colouring) · [4. BFS colouring](#4-bfs-colouring) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

An undirected graph has `V` nodes and an edge list. Return `true` if its nodes can be split into two sets such that every edge connects a node in one set to a node in the other.

| Input | Output | Why |
|---|---|---|
| `V = 4, edges = [[0,1],[1,2],[2,3],[3,0]]` | `true` | even cycle: {0,2} and {1,3} |
| `V = 3, edges = [[0,1],[1,2],[2,0]]` | `false` | odd cycle (triangle) |

**Constraints:** `1 ≤ V ≤ 10⁵`, `0 ≤ E ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS colouring | recursive colour, neighbour gets 1 − c | O(V + E) | O(V) |
| BFS colouring | queue; neighbour gets the opposite colour | O(V + E) | O(V) |

> [!tip] Interview angle
> State the theorem: bipartite ⇔ no odd-length cycle. A conflict found by BFS is direct evidence: the two same-coloured endpoints lie at equal depth, and their paths back to the common ancestor form an odd cycle.

---

## 3. DFS colouring

**Intuition.** `dfs(u, c)` assigns `c`. An uncoloured neighbour recurses with `1 − c`. A neighbour already coloured `c` is a conflict. Run it from every uncoloured node.

```python
import sys

def is_bipartite_dfs(V, edges):
    sys.setrecursionlimit(10 ** 6)
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    col = [-1] * V
    def dfs(u, c):
        col[u] = c
        for v in adj[u]:
            if col[v] == -1:
                if not dfs(v, 1 - c):
                    return False
            elif col[v] == c:
                return False
        return True
    return all(col[s] != -1 or dfs(s, 0) for s in range(V))
```

**Complexity:** time **O(V + E)**, space **O(V)**.

---

## 4. BFS colouring

**Intuition.** For every uncoloured node, colour it 0 and BFS. Each uncoloured neighbour gets the opposite colour and is enqueued. A neighbour with the same colour fails immediately.

**Algorithm**

1. `col = [−1]·V`.
2. For each uncoloured `s`: `col[s] = 0`, enqueue it.
3. Pop `u`; for each `v`: if uncoloured, `col[v] = 1 − col[u]` and enqueue; else if `col[v] == col[u]`, return `false`.
4. Return `true`.

**Dry run** — Triangle: 0→0. Neighbours 1,2 → 1. Pop 1: neighbour 2 has colour 1 = col[1] → false.

**C++**
```cpp
bool isBipartite(int V, vector<vector<int>>& edges) {
    vector<vector<int>> adj(V);
    for (auto& e : edges) { adj[e[0]].push_back(e[1]); adj[e[1]].push_back(e[0]); }
    vector<int> col(V, -1);
    for (int s = 0; s < V; s++) {
        if (col[s] != -1) continue;
        col[s] = 0;
        queue<int> q; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (col[v] == -1) { col[v] = 1 - col[u]; q.push(v); }
                else if (col[v] == col[u]) return false;
            }
        }
    }
    return true;
}
```

**Java**
```java
static boolean isBipartite(int V, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    int[] col = new int[V];
    Arrays.fill(col, -1);
    for (int s = 0; s < V; s++) {
        if (col[s] != -1) continue;
        col[s] = 0;
        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.add(s);
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int v : adj.get(u)) {
                if (col[v] == -1) { col[v] = 1 - col[u]; q.add(v); }
                else if (col[v] == col[u]) return false;
            }
        }
    }
    return true;
}
```

**Python**
```python
from collections import deque

def is_bipartite(V, edges):
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    col = [-1] * V
    for s in range(V):
        if col[s] != -1:
            continue
        col[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if col[v] == -1:
                    col[v] = 1 - col[u]
                    q.append(v)
                elif col[v] == col[u]:
                    return False
    return True
```

**Complexity:** time **O(V + E)**, space **O(V)** — a standard BFS over every component.

---

## Edge cases

- No edges: bipartite.
- Trees and even cycles: bipartite.
- An odd cycle in any component: not bipartite.

---

## Common mistakes

1. Colouring only the component of node 0.
2. Using `visited` alone (no colours), which cannot detect conflicts.
3. LC 785 passes `graph` as adjacency lists: don't rebuild from edges.

---

## Follow-ups

1. Possible Bipartition (LC 886, people who dislike each other)?
2. Return the two groups?
3. DSU version?

<details><summary>Answer sketches</summary>

**#1:** Same check on the dislike graph.

**#2:** Group nodes by `col`.

**#3:** For each `u`, union all of its neighbours together; if `u` ever shares a root with a neighbour, fail.
</details>

---

## Flashcards

**Bipartite ⇔ ?** #flashcard
No odd-length cycle.

**BFS bipartite conflict?** #flashcard
An edge whose two ends have the same colour.

**Is a tree bipartite?** #flashcard
Always (colour by depth parity).

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
