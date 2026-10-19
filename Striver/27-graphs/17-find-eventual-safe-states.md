---
module: striver/27-graphs
lesson: 17
topic: Find eventual safe states
difficulty: Medium
source: https://takeuforward.org/learning/dsa/find-eventual-safe-states?category=hard-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, topological-sort, reverse-graph]
---
# 17. Find eventual safe states

← [Detect a cycle in a directed graph](16-cycle-in-directed-graph.md) · [Part 27 index](README.md) · Next → [Course Schedule I](18-course-schedule-i.md)

> [!abstract] Problem at a glance
> **Task:** Return, in ascending order, every node from which every path eventually reaches a terminal node (a node with no outgoing edges).
> **Key insight:** A node is unsafe exactly when some path from it can reach a cycle. **Reverse every edge**, then run Kahn's algorithm. Terminal nodes are the in-degree-0 starts in the reversed graph. A node gets peeled once all its original successors are proven safe. Nodes on or leading into cycles are never peeled.
> **Difficulty:** Medium · **Pattern:** Reverse graph + Kahn (or 3-colour DFS) · **Also on:** LC 802
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-eventual-safe-states?category=hard-problems&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. 3-colour DFS](#3-3-colour-dfs) · [4. Kahn on the reversed graph](#4-kahn-on-the-reversed-graph) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A directed graph has `V` nodes and an edge list. A node is **terminal** if it has no outgoing edges. A node is **safe** if every possible path starting from it leads to a terminal node. Return all safe nodes in ascending order.

| Input | Output | Why |
|---|---|---|
| `V = 7, edges = [[0,1],[0,2],[1,2],[1,3],[2,5],[3,0],[4,5]]` | `[2,4,5,6]` | 0, 1, 3 are on the cycle 0→1→3→0 |
| `V = 3, edges = [[0,1],[1,2],[2,0]]` | `[]` | all on one cycle |

**Constraints:** `1 ≤ V ≤ 10⁴`, `0 ≤ E ≤ 4·10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| 3-colour DFS | a node is safe iff its DFS finishes without hitting grey | O(V + E) | O(V) |
| Kahn on the reversed graph | reverse edges, peel out-degree-0 nodes | O(V + E) | O(V + E) |

> [!tip] Interview angle
> LC 802 gives `graph` as adjacency lists; Striver's version uses `V` + adjacency. Both reduce to 'not on and not leading to a cycle'. Explaining the reverse-graph Kahn idea earns more credit than the DFS, because it shows you understand what in-degree means.

---

## 3. 3-colour DFS

**Intuition.** Run the directed-cycle DFS. If exploring `u` hits a grey (on-path) node, or a node already known to be unsafe, `u` stays marked unsafe. If all its successors finish safely, mark it safe (black).

```python
import sys

def eventual_safe_dfs(V, edges):
    sys.setrecursionlimit(10 ** 6)
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
    state = [0] * V                 # 0 new, 1 visiting/unsafe, 2 safe
    def safe(u):
        if state[u]:
            return state[u] == 2
        state[u] = 1
        for v in adj[u]:
            if not safe(v):
                return False
        state[u] = 2
        return True
    return [u for u in range(V) if safe(u)]
```

**Complexity:** time **O(V + E)**, space **O(V)**.

---

## 4. Kahn on the reversed graph

**Intuition.** Build `radj[v]` (who points to `v`) and `outdeg[u]`. Queue every terminal node. When a node is proven safe, each predecessor loses one unresolved successor; when its count reaches 0, it is safe too. Sort the result.

**Algorithm**

1. `outdeg[u]` = out-degree; `radj[v].append(u)` for each `u → v`.
2. Queue all `u` with `outdeg[u] = 0`.
3. Pop `v`, mark safe; for each `u` in `radj[v]`: `outdeg[u]--`; enqueue if 0.
4. Return the safe nodes in ascending order.

**Dry run** — Example 1: terminal 5, 6. Pop 5 → preds 2, 4 hit 0 → safe. Pop 2 → preds 0 (3→2), 1 (2→1). Nothing else frees. Safe = {2,4,5,6}.

**C++**
```cpp
vector<int> eventualSafe(int V, vector<vector<int>>& edges) {
    vector<vector<int>> radj(V);
    vector<int> out(V, 0), res;
    for (auto& e : edges) { radj[e[1]].push_back(e[0]); out[e[0]]++; }
    queue<int> q;
    for (int i = 0; i < V; i++) if (out[i] == 0) q.push(i);
    vector<bool> safe(V, false);
    while (!q.empty()) {
        int v = q.front(); q.pop();
        safe[v] = true;
        for (int u : radj[v]) if (--out[u] == 0) q.push(u);
    }
    for (int i = 0; i < V; i++) if (safe[i]) res.push_back(i);
    return res;
}
```

**Java**
```java
static List<Integer> eventualSafe(int V, int[][] edges) {
    List<List<Integer>> radj = new ArrayList<>();
    for (int i = 0; i < V; i++) radj.add(new ArrayList<>());
    int[] out = new int[V];
    for (int[] e : edges) { radj.get(e[1]).add(e[0]); out[e[0]]++; }
    ArrayDeque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < V; i++) if (out[i] == 0) q.add(i);
    boolean[] safe = new boolean[V];
    while (!q.isEmpty()) {
        int v = q.poll();
        safe[v] = true;
        for (int u : radj.get(v)) if (--out[u] == 0) q.add(u);
    }
    List<Integer> res = new ArrayList<>();
    for (int i = 0; i < V; i++) if (safe[i]) res.add(i);
    return res;
}
```

**Python**
```python
from collections import deque

def eventual_safe(V, edges):
    radj = [[] for _ in range(V)]
    out = [0] * V
    for u, v in edges:
        radj[v].append(u)
        out[u] += 1
    q = deque(i for i in range(V) if out[i] == 0)
    safe = [False] * V
    while q:
        v = q.popleft()
        safe[v] = True
        for u in radj[v]:
            out[u] -= 1
            if out[u] == 0:
                q.append(u)
    return [i for i in range(V) if safe[i]]
```

**Complexity:** time **O(V + E)**, space **O(V + E)** — Kahn over the reversed graph; the final scan is O(V) and yields sorted output.

---

## Edge cases

- No edges: every node is terminal, so all are safe.
- A self-loop makes that node (and all its predecessors) unsafe.
- A node with one path to a terminal and another into a cycle: unsafe.

---

## Common mistakes

1. Treating 'some path reaches a terminal' as safe; the definition is **every** path.
2. Kahn on the original graph (in-degrees) instead of the reversed one.
3. Forgetting to sort when collecting from the queue order.

---

## Follow-ups

1. Why is the reversed graph needed?
2. Return the unsafe nodes instead?

<details><summary>Answer sketches</summary>

**#1:** Safety propagates backwards: a node is safe once all its successors are; that's out-degree peeling, i.e. in-degree peeling on reversed edges.

**#2:** The complement; they are exactly the nodes that can reach a cycle.
</details>

---

## Flashcards

**Eventual safe = ?** #flashcard
Cannot reach any cycle.

**Kahn trick for safe states?** #flashcard
Reverse edges; peel nodes whose out-degree drops to 0.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
