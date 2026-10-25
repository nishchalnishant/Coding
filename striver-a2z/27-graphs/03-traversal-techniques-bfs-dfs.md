---
module: striver-a2z/27-graphs
lesson: 3
topic: Traversal Techniques
difficulty: Easy
source: https://takeuforward.org/learning/dsa/traversal-techniques?category=theory-and-traversals&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bfs, dfs]
---
# 3. Traversal Techniques

← [Minimum Spanning Trees and Disjoint Set Union](02-mst-and-dsu-theory.md) · [Part 27 index](README.md) · Next → [Connected Components](04-connected-components.md)

> [!abstract] Problem at a glance
> **Task:** Given a connected undirected graph as an adjacency list, return its BFS order and its DFS order, both from node 0 and visiting neighbours in list order.
> **Key insight:** Both traversals are 'pop a node, expand its unvisited neighbours'. The only difference is the container. A **queue** pops the oldest node, so BFS explores layer by layer. A **stack** (or recursion) pops the newest, so DFS goes as deep as it can before backtracking. A `visited` array ensures each node is expanded once, giving O(V + E).
> **Difficulty:** Easy · **Pattern:** Graph traversal (queue vs stack)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/traversal-techniques?category=theory-and-traversals&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. BFS + recursive DFS](#3-bfs--recursive-dfs) · [4. BFS + iterative DFS](#4-bfs--iterative-dfs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

You are given `adj`, the adjacency list of a connected undirected graph with `V` nodes labelled `0..V-1`. Return `[bfs, dfs]`: the breadth-first order and the depth-first (preorder) order, both starting at node `0` and visiting neighbours in the order they appear in `adj[u]`.

| Input | Output | Why |
|---|---|---|
| `adj = [[1,2],[0,3],[0,4],[1],[2]]` | `[[0,1,2,3,4],[0,1,3,2,4]]` | BFS: layer {0}, {1,2}, {3,4}. DFS: 0→1→3, back, →2→4 |
| `adj = [[1],[0,2],[1,3],[2]]` | `[[0,1,2,3],[0,1,2,3]]` | on a path both orders agree |

**Constraints:** `1 ≤ V ≤ 10⁴`, `0 ≤ E ≤ 10⁵`, the graph is connected.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| BFS + recursive DFS | queue for BFS; recursion for DFS | O(V + E) | O(V) |
| BFS + iterative DFS | explicit stack, push neighbours reversed, mark on pop | O(V + E) | O(V + E) |

> [!tip] Interview angle
> Say the invariant out loud. BFS: when a node is popped, every node closer to the source has already been popped, which is why BFS gives shortest paths on unweighted graphs. DFS: when `go(u)` returns, everything reachable from `u` through unvisited nodes has been visited.

---

## 3. BFS + recursive DFS

**Intuition.** BFS: push 0, mark it, then repeatedly pop the front, record it, and push its unvisited neighbours (marking them **when pushed** so no node enters the queue twice). DFS: `go(u)` marks `u`, records it, and recurses into each unvisited neighbour in order. The recursion depth can reach V, which overflows the default stack on a long path.

```python
from collections import deque

def traversals_rec(adj):
    n = len(adj)
    seen = [False] * n
    bfs, q = [], deque([0])
    seen[0] = True
    while q:
        u = q.popleft()
        bfs.append(u)
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                q.append(v)
    seen = [False] * n
    dfs = []
    def go(u):
        seen[u] = True
        dfs.append(u)
        for v in adj[u]:
            if not seen[v]:
                go(v)
    go(0)
    return [bfs, dfs]
```

**Complexity:** time **O(V + E)**, space **O(V)**.

---

## 4. BFS + iterative DFS

**Intuition.** Replace recursion with a stack. To reproduce the recursive preorder exactly, push neighbours in **reverse** so the first neighbour is popped first, and mark a node visited when it is **popped** (a node may sit on the stack several times; stale copies are skipped). The stack can hold up to E entries.

**Algorithm**

1. BFS: queue `[0]`, `seen[0] = true`; pop, record, push unseen neighbours and mark them.
2. Reset `seen`. DFS: stack `[0]`.
3. Pop `u`; if already seen, skip. Otherwise mark it, record it, and push its unseen neighbours from last to first.
4. Return both orders.

**Dry run** — adj = [[1,2],[0,3],[0,4],[1],[2]]. BFS: 0 → push 1,2 → pop 1 → push 3 → pop 2 → push 4 → pop 3, 4 = [0,1,2,3,4]. DFS stack: [0] → pop 0, push 2,1 → pop 1, push 3 → pop 3 → pop 2, push 4 → pop 4 = [0,1,3,2,4].

**C++**
```cpp
vector<vector<int>> traversals(vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> bfs, dfs;
    vector<bool> seen(n, false);
    queue<int> q; q.push(0); seen[0] = true;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        bfs.push_back(u);
        for (int v : adj[u]) if (!seen[v]) { seen[v] = true; q.push(v); }
    }
    seen.assign(n, false);
    stack<int> st; st.push(0);
    while (!st.empty()) {
        int u = st.top(); st.pop();
        if (seen[u]) continue;
        seen[u] = true;
        dfs.push_back(u);
        for (int k = (int)adj[u].size() - 1; k >= 0; k--)
            if (!seen[adj[u][k]]) st.push(adj[u][k]);
    }
    return {bfs, dfs};
}
```

**Java**
```java
static List<List<Integer>> traversals(int[][] adj) {
    int n = adj.length;
    List<Integer> bfs = new ArrayList<>(), dfs = new ArrayList<>();
    boolean[] seen = new boolean[n];
    ArrayDeque<Integer> q = new ArrayDeque<>();
    q.add(0); seen[0] = true;
    while (!q.isEmpty()) {
        int u = q.poll();
        bfs.add(u);
        for (int v : adj[u]) if (!seen[v]) { seen[v] = true; q.add(v); }
    }
    seen = new boolean[n];
    ArrayDeque<Integer> st = new ArrayDeque<>();
    st.push(0);
    while (!st.isEmpty()) {
        int u = st.pop();
        if (seen[u]) continue;
        seen[u] = true;
        dfs.add(u);
        for (int k = adj[u].length - 1; k >= 0; k--) if (!seen[adj[u][k]]) st.push(adj[u][k]);
    }
    return Arrays.asList(bfs, dfs);
}
```

**Python**
```python
from collections import deque

def traversals(adj):
    n = len(adj)
    seen = [False] * n
    bfs, q = [], deque([0])
    seen[0] = True
    while q:
        u = q.popleft()
        bfs.append(u)
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                q.append(v)
    seen = [False] * n
    dfs, st = [], [0]
    while st:
        u = st.pop()
        if seen[u]:
            continue
        seen[u] = True
        dfs.append(u)
        for v in reversed(adj[u]):
            if not seen[v]:
                st.append(v)
    return [bfs, dfs]
```

**Complexity:** time **O(V + E)**, space **O(V + E)** — each node is expanded once and each adjacency entry is scanned once; the DFS stack may hold one entry per edge.

---

## Edge cases

- Single node: both orders are `[0]`.
- Disconnected graph: run the traversal from every unvisited node (that is the components problem next).
- Self-loops / parallel edges: `visited` makes them harmless.
- Directed graph: the same code works, using out-neighbours only.

---

## Common mistakes

1. BFS: marking visited on **pop** instead of push, so a node can be queued many times (still correct, but O(E) queue entries and wrong 'distance' if you track levels carelessly).
2. Iterative DFS: marking on push. That gives a valid DFS-like order, but not the recursive preorder.
3. Recursive DFS on 10⁵ nodes in Python/Java without raising the stack limit.
4. Using an adjacency matrix for sparse graphs: O(V²) memory and time.

---

## Follow-ups

1. BFS shortest distances from 0?
2. Print BFS level by level?
3. DFS pre-order vs post-order uses?

<details><summary>Answer sketches</summary>

**#1:** Store `dist[v] = dist[u] + 1` when `v` is pushed. The first time a node is reached is via a shortest path.

**#2:** Process the queue in batches: read `size = len(q)` and pop exactly that many before starting the next level.

**#3:** Pre-order: copying or serialising. Post-order (record after the children finish): topological sort, subtree sizes, Kosaraju's first pass.
</details>

---

## Flashcards

**BFS container vs DFS container?** #flashcard
Queue (FIFO) vs stack/recursion (LIFO).

**When should BFS mark visited?** #flashcard
When a node is pushed, so it is enqueued at most once.

**Time of BFS/DFS on adjacency lists?** #flashcard
O(V + E).

**How do you make iterative DFS match recursive order?** #flashcard
Push neighbours in reverse and mark on pop.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
