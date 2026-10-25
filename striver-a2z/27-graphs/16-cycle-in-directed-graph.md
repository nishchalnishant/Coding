---
module: striver-a2z/27-graphs
lesson: 16
topic: Detect a cycle in a directed graph
difficulty: Medium
source: https://takeuforward.org/learning/dsa/detect-a-cycle-in-a-directed-graph?category=hard-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, topological-sort, dfs, cycle]
---
# 16. Detect a cycle in a directed graph

← [Topological sort or Kahn's algorithm](15-topological-sort-dfs-and-kahn.md) · [Part 27 index](README.md) · Next → [Find eventual safe states](17-find-eventual-safe-states.md)

> [!abstract] Problem at a glance
> **Task:** Return whether a directed graph contains a cycle.
> **Key insight:** Unlike the undirected case, reaching a visited node is not enough: in the diamond `0→1→3, 0→2→3`, node 3 is reached twice without a cycle. A cycle exists exactly when DFS meets a node that is **still on the current recursion path**, a back edge. Use three states: unvisited, on path, done. Alternatively, Kahn's algorithm fails to output every node exactly when there is a cycle.
> **Difficulty:** Medium · **Pattern:** DFS path-visited / Kahn
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/detect-a-cycle-in-a-directed-graph?category=hard-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS with path-visited](#3-dfs-with-path-visited) · [4. Kahn's algorithm](#4-kahns-algorithm) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A directed graph has `V` nodes and edge list `edges` (`[u, v]` = `u → v`, self-loops allowed). Return `true` if it contains a directed cycle.

| Input | Output | Why |
|---|---|---|
| `V = 4, edges = [[0,1],[1,2],[2,3],[3,3]]` | `true` | self-loop at 3 |
| `V = 4, edges = [[0,1],[0,2],[1,3],[2,3]]` | `false` | a diamond: 3 is shared but no cycle |

**Constraints:** `1 ≤ V ≤ 10⁵`, `0 ≤ E ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS with path-visited | state 1 = on path; meeting state 1 ⇒ cycle | O(V + E) | O(V) |
| Kahn's algorithm | cycle iff fewer than V nodes get processed | O(V + E) | O(V) |

> [!tip] Interview angle
> Draw the diamond to explain why the undirected parent trick fails here. Then offer both fixes: three colours (white/grey/black) or Kahn. Kahn is iterative and has no stack-depth risk.

---

## 3. DFS with path-visited

**Intuition.** Mark `state[u] = 1` on entry and `2` on exit. When exploring `u → v`: if `state[v] == 1`, `v` is an ancestor on the current path, so there is a back edge and a cycle. `state[v] == 2` is a finished node (cross or forward edge), so it is safe.

```python
import sys

def has_cycle_directed_dfs(V, edges):
    sys.setrecursionlimit(10 ** 6)
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
    state = [0] * V
    def go(u):
        state[u] = 1
        for v in adj[u]:
            if state[v] == 1 or (state[v] == 0 and go(v)):
                return True
        state[u] = 2
        return False
    return any(state[s] == 0 and go(s) for s in range(V))
```

**Complexity:** time **O(V + E)**, space **O(V)**.

---

## 4. Kahn's algorithm

**Intuition.** Nodes on a cycle (and everything downstream of one) never reach in-degree 0, because each waits on a predecessor in the cycle. Run Kahn and count the processed nodes; fewer than `V` means a cycle.

**Algorithm**

1. Compute in-degrees and queue the zeros.
2. Pop, count, decrement out-neighbours, enqueue new zeros.
3. Return `count < V`.

**Dry run** — Self-loop example: indeg = [0,1,1,2]. Pop 0 → indeg[1] 0. Pop 1 → indeg[2] 0. Pop 2 → indeg[3] 1 (the self-loop remains). count = 3 < 4 → true.

**C++**
```cpp
bool hasCycleDirected(int V, vector<vector<int>>& edges) {
    vector<vector<int>> adj(V);
    vector<int> indeg(V, 0);
    for (auto& e : edges) { adj[e[0]].push_back(e[1]); indeg[e[1]]++; }
    queue<int> q;
    for (int i = 0; i < V; i++) if (indeg[i] == 0) q.push(i);
    int count = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        count++;
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    return count < V;
}
```

**Java**
```java
static boolean hasCycleDirected(int V, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
    int[] indeg = new int[V];
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); indeg[e[1]]++; }
    ArrayDeque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < V; i++) if (indeg[i] == 0) q.add(i);
    int count = 0;
    while (!q.isEmpty()) {
        int u = q.poll();
        count++;
        for (int v : adj.get(u)) if (--indeg[v] == 0) q.add(v);
    }
    return count < V;
}
```

**Python**
```python
from collections import deque

def has_cycle_directed(V, edges):
    adj = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(V) if indeg[i] == 0)
    count = 0
    while q:
        u = q.popleft()
        count += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return count < V
```

**Complexity:** time **O(V + E)**, space **O(V)** — the standard Kahn traversal.

---

## Edge cases

- Self-loop: a cycle (Kahn never frees the node).
- Two-node cycle `0↔1`: a cycle (unlike in undirected graphs).
- Diamond shapes: no cycle.

---

## Common mistakes

1. Using a single `visited` flag, which reports diamonds as cycles.
2. Forgetting to reset the 'on path' mark when a DFS call returns.
3. Running the DFS only from node 0.

---

## Follow-ups

1. Return one cycle?
2. Which nodes are on some cycle?

<details><summary>Answer sketches</summary>

**#1:** Keep a parent array; when a back edge `u → v` is found, walk parents from `u` back to `v`.

**#2:** Nodes in strongly connected components of size > 1 (or with a self-loop): Kosaraju/Tarjan.
</details>

---

## Flashcards

**Directed cycle via DFS?** #flashcard
An edge to a node currently on the recursion path (grey).

**Directed cycle via Kahn?** #flashcard
Fewer than V nodes processed.

**Why does the undirected trick fail on directed graphs?** #flashcard
A visited node can be reached by two paths without a cycle (diamond).

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
