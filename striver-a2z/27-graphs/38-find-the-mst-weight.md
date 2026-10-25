---
module: striver-a2z/27-graphs
lesson: 38
topic: Find the MST weight
difficulty: Medium
source: https://takeuforward.org/learning/dsa/find-the-mst-weight?category=minimum-spanning-tree&source=strivers-a2z-dsa-sheet
tags: [striver, graph, mst, kruskal, prim, union-find]
---
# 38. Find the MST weight

← [Disjoint Set (Union-Find)](37-disjoint-set.md) · [Part 27 index](README.md) · Next → [Number of operations to make network connected](39-number-of-operations-to-make-network-connected.md)

> [!abstract] Problem at a glance
> **Task:** Given a connected weighted undirected graph, return the total weight of a minimum spanning tree.
> **Key insight:** **Cut property:** for any split of the vertices into two sides, the lightest edge crossing the split belongs to some MST. Prim grows one tree and repeatedly takes the lightest edge leaving it (heap). Kruskal sorts all edges and takes each one that joins two different components (DSU).
> **Difficulty:** Medium · **Pattern:** Greedy MST: Prim (heap) / Kruskal (sort + DSU)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-the-mst-weight?category=minimum-spanning-tree&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Prim's algorithm](#3-prims-algorithm) · [4. Kruskal's algorithm](#4-kruskals-algorithm) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`V` vertices `0..V−1` and `edges[i] = [u, v, w]` (undirected). The graph is connected. Return the sum of edge weights of a minimum spanning tree.

| Input | Output | Why |
|---|---|---|
| `V = 3, edges = [[0,1,5],[1,2,3],[0,2,1]]` | `4` | take 0–2 (1) and 1–2 (3) |
| `V = 2, edges = [[0,1,5]]` | `5` | the only edge |

**Constraints:** `2 ≤ V ≤ 1000`, `V − 1 ≤ E ≤ V(V−1)/2`, `1 ≤ w ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Prim's algorithm | heap of (w, node); pop, skip if in tree, add w, push neighbours | O(E log E) | O(V + E) |
| Kruskal's algorithm | sort edges by weight; accept an edge if DSU says its ends differ | O(E log E) | O(V) |

> [!tip] Interview angle
> Know both and say when each wins: Kruskal is shortest to code with a DSU and natural for an edge list (O(E log E)); Prim with a heap fits an adjacency list and dense graphs. If asked for the edges, not just the weight, collect them as you accept them.

---

## 3. Prim's algorithm

**Intuition.** Start from vertex 0. A min-heap holds candidate edges `(w, v)` leaving the tree. Pop the lightest; if `v` is already in the tree, skip it (stale); otherwise add `w`, mark `v` and push all its edges to vertices not yet in the tree. This is the cut property applied to the cut (tree, rest).

```python
import heapq

def spanning_tree_prim(V, edges):
    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    in_tree = [False] * V
    pq = [(0, 0)]
    total = 0
    while pq:
        w, u = heapq.heappop(pq)
        if in_tree[u]:
            continue
        in_tree[u] = True
        total += w
        for v, wt in adj[u]:
            if not in_tree[v]:
                heapq.heappush(pq, (wt, v))
    return total
```

**Complexity:** time **O(E log E)**, space **O(V + E)**.

---

## 4. Kruskal's algorithm

**Intuition.** Process edges lightest first. An edge whose ends are already connected would close a cycle, so skip it; otherwise it is the lightest edge across the cut between its two components, so accept it and union them. Stop after `V − 1` accepted edges.

**Algorithm**

1. Sort `edges` by `w`.
2. DSU on V vertices.
3. For each `(u, v, w)`: if `find(u) != find(v)`, union and add `w`.
4. Return the sum (optionally break after V − 1 edges).

**Dry run** — Example 1 sorted: (0,2,1), (1,2,3), (0,1,5). Take 0–2 → 1. Take 1–2 → 4. 0–1: same set, skip. Answer 4.

**C++**
```cpp
int spanningTree(int V, vector<vector<int>>& edges) {
    vector<int> parent(V), sz(V, 1);
    iota(parent.begin(), parent.end(), 0);
    function<int(int)> find = [&](int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); };
    vector<vector<int>> es = edges;
    sort(es.begin(), es.end(), [](const vector<int>& a, const vector<int>& b) { return a[2] < b[2]; });
    int total = 0;
    for (auto& e : es) {
        int a = find(e[0]), b = find(e[1]);
        if (a == b) continue;
        if (sz[a] < sz[b]) swap(a, b);
        parent[b] = a;
        sz[a] += sz[b];
        total += e[2];
    }
    return total;
}
```

**Java**
```java
static int[] parent, sz;
static int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
static int spanningTree(int V, int[][] edges) {
    parent = new int[V];
    sz = new int[V];
    for (int i = 0; i < V; i++) { parent[i] = i; sz[i] = 1; }
    int[][] es = edges.clone();
    Arrays.sort(es, (a, b) -> Integer.compare(a[2], b[2]));
    int total = 0;
    for (int[] e : es) {
        int a = find(e[0]), b = find(e[1]);
        if (a == b) continue;
        if (sz[a] < sz[b]) { int t = a; a = b; b = t; }
        parent[b] = a;
        sz[a] += sz[b];
        total += e[2];
    }
    return total;
}
```

**Python**
```python
def spanning_tree(V, edges):
    parent, sz = list(range(V)), [1] * V
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    total = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = find(u), find(v)
        if a == b:
            continue
        if sz[a] < sz[b]:
            a, b = b, a
        parent[b] = a
        sz[a] += sz[b]
        total += w
    return total
```

**Complexity:** time **O(E log E)**, space **O(V)** — the sort dominates; the DSU part is O(E·α(V)).

---

## Edge cases

- V = 1: weight 0.
- Equal weights: several MSTs share the same total.
- Disconnected input (not here): Kruskal returns a minimum spanning **forest**; Prim only spans vertex 0's component.

---

## Common mistakes

1. Prim: marking a vertex visited when **pushed** instead of when popped (that is Dijkstra-style relaxation and gives wrong totals without a key array).
2. Prim: pushing `dist + w` (Dijkstra) instead of just `w`.
3. Kruskal: forgetting to sort, or sorting by endpoint.

---

## Follow-ups

1. Second-best MST?
2. Maximum spanning tree?
3. Dense graph, V = 5000, adjacency matrix?

<details><summary>Answer sketches</summary>

**#1:** For each MST edge, forbid it and rerun Kruskal (O(V·E α)); or add each non-tree edge and drop the heaviest edge on the tree path it closes.

**#2:** Sort descending (or negate weights).

**#3:** Array-based Prim without a heap: O(V²), beats O(E log E) when E ≈ V².
</details>

---

## Flashcards

**Cut property?** #flashcard
The lightest edge crossing any cut is in some MST.

**Prim vs Dijkstra heap key?** #flashcard
Prim: edge weight w. Dijkstra: dist[u] + w.

**Kruskal cost?** #flashcard
O(E log E) for the sort + O(E α(V)) for DSU.

**Interview track →** [Union-find deep-dive](../../02-algorithms/14-union-find.md)
