---
module: striver-a2z/27-graphs
lesson: 46
topic: Articulation point in graph
difficulty: Hard
source: https://takeuforward.org/learning/dsa/articulation-point-in-graph?category=additional-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, articulation-points, tarjan, dfs]
---
# 46. Articulation point in graph

← [Bridges in graph](45-bridges-in-graph.md) · [Part 27 index](README.md) · Next → [Part 28: Dynamic Programming](../28-dynamic-programming/README.md)

> [!abstract] Problem at a glance
> **Task:** Return every vertex whose removal increases the number of connected components (sorted), or `[-1]` if none.
> **Key insight:** Same `tin`/`low` DFS as bridges, two changes. A **non-root** u is a cut vertex if some child v has `low[v] ≥ tin[u]` (v's subtree can't get above u). The **root** is a cut vertex iff it has **≥ 2 DFS children**. Use a boolean mark, since u can qualify through several children.
> **Difficulty:** Hard · **Pattern:** Tarjan low-link DFS (vertex version)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/articulation-point-in-graph?category=additional-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Remove each vertex and count components](#3-remove-each-vertex-and-count-components) · [4. Tarjan tin / low](#4-tarjan-tin--low) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Undirected graph with `V` vertices and `edges[i] = [u, v]`. Return all articulation points in ascending order, or `[-1]` if there are none.

| Input | Output | Why |
|---|---|---|
| `V = 5, edges = [[0,1],[1,4],[4,2],[2,3],[3,4]]` | `[1,4]` | removing 1 isolates 0; removing 4 splits {0,1} from {2,3} |
| `V = 4, a 4-cycle` | `[-1]` |  |

**Constraints:** `1 ≤ V ≤ 10⁴`, `0 ≤ E ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Remove each vertex and count components | for each v, count components of G − v | O(V·(V + E)) | O(V + E) |
| Tarjan tin / low | non-root: low[child] ≥ tin[u]; root: ≥ 2 children | O(V + E) | O(V + E) |

> [!tip] Interview angle
> Contrast with bridges explicitly: `≥` instead of `>`, and the root special case. Bridges / articulation points / SCC are rare at L3/L4 (the repo marks Tarjan/SCC out of scope); know the idea, the invariant and the complexity, and code it only if asked.

---

## 3. Remove each vertex and count components

**Intuition.** v is an articulation point iff `components(G − v) > components(G)`.

```python
def articulation_points_bf(V, edges):
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    def comps(skip):
        seen = [False] * V
        if skip >= 0:
            seen[skip] = True
        c = 0
        for s in range(V):
            if seen[s]:
                continue
            c += 1
            seen[s] = True
            st = [s]
            while st:
                u = st.pop()
                for w in adj[u]:
                    if not seen[w]:
                        seen[w] = True
                        st.append(w)
        return c
    base = comps(-1)
    out = [v for v in range(V) if comps(v) > base]
    return out or [-1]
```

**Complexity:** time **O(V·(V + E))**, space **O(V + E)**.

---

## 4. Tarjan tin / low

**Intuition.** DFS assigning `tin`/`low`. For each unvisited child `v` of `u`: recurse, fold `low[v]` into `low[u]`, and if `low[v] ≥ tin[u]` and `u` is not the root, mark `u`; count children. Back edges fold `tin[v]`. After the loop, a root with ≥ 2 children is marked.

**Algorithm**

1. `tin = low = −1`, `mark = False`.
2. `dfs(u, p)`: `tin[u] = low[u] = timer++`, `children = 0`.
3. For `v ≠ p`: visited → `low[u] = min(low[u], tin[v])`.
4. Unvisited → `dfs(v, u)`, `low[u] = min(low[u], low[v])`, if `low[v] ≥ tin[u]` and `p ≠ −1` mark u; `children += 1`.
5. If `p == −1` and `children > 1` mark u.
6. Collect marked vertices in order; `[-1]` if none.

**Dry run** — Example 1: 0 (t0) → 1 (t1) → 4 (t2) → 2 (t3) → 3 (t4); 3 sees 4 → low3 = 2. Back at 2: low2 = 2 ≥ tin2? 2 ≥ 3 no. At 4: low2 = 2 ≥ tin4 = 2 → mark 4. At 1: low4 = 2 ≥ 1 → mark 1. Root 0 has one child → not marked. [1,4].

**C++**
```cpp
int timer_;
vector<int> tin_, low_;
vector<bool> mark_;
vector<vector<int>> adj_;
void dfs(int u, int p) {
    tin_[u] = low_[u] = timer_++;
    int children = 0;
    for (int v : adj_[u]) {
        if (v == p) continue;
        if (tin_[v] != -1) { low_[u] = min(low_[u], tin_[v]); continue; }
        dfs(v, u);
        low_[u] = min(low_[u], low_[v]);
        if (low_[v] >= tin_[u] && p != -1) mark_[u] = true;
        children++;
    }
    if (p == -1 && children > 1) mark_[u] = true;
}
vector<int> articulationPoints(int V, vector<vector<int>>& edges) {
    adj_.assign(V, {});
    for (auto& e : edges) { adj_[e[0]].push_back(e[1]); adj_[e[1]].push_back(e[0]); }
    tin_.assign(V, -1);
    low_.assign(V, -1);
    mark_.assign(V, false);
    timer_ = 0;
    for (int i = 0; i < V; i++) if (tin_[i] == -1) dfs(i, -1);
    vector<int> out;
    for (int i = 0; i < V; i++) if (mark_[i]) out.push_back(i);
    if (out.empty()) out.push_back(-1);
    return out;
}
```

**Java**
```java
static int timer;
static int[] tin, low;
static boolean[] mark;
static List<List<Integer>> adj;
static void dfs(int u, int p) {
    tin[u] = low[u] = timer++;
    int children = 0;
    for (int v : adj.get(u)) {
        if (v == p) continue;
        if (tin[v] != -1) { low[u] = Math.min(low[u], tin[v]); continue; }
        dfs(v, u);
        low[u] = Math.min(low[u], low[v]);
        if (low[v] >= tin[u] && p != -1) mark[u] = true;
        children++;
    }
    if (p == -1 && children > 1) mark[u] = true;
}
static List<Integer> articulationPoints(int V, int[][] edges) {
    adj = new ArrayList<>();
    for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    tin = new int[V]; low = new int[V]; mark = new boolean[V];
    Arrays.fill(tin, -1);
    timer = 0;
    for (int i = 0; i < V; i++) if (tin[i] == -1) dfs(i, -1);
    List<Integer> out = new ArrayList<>();
    for (int i = 0; i < V; i++) if (mark[i]) out.add(i);
    if (out.isEmpty()) out.add(-1);
    return out;
}
```

**Python**
```python
import sys

def articulation_points(V, edges):
    sys.setrecursionlimit(20000)
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    tin, low, mark = [-1] * V, [-1] * V, [False] * V
    timer = 0
    def dfs(u, p):
        nonlocal timer
        tin[u] = low[u] = timer
        timer += 1
        children = 0
        for v in adj[u]:
            if v == p:
                continue
            if tin[v] != -1:
                low[u] = min(low[u], tin[v])
                continue
            dfs(v, u)
            low[u] = min(low[u], low[v])
            if low[v] >= tin[u] and p != -1:
                mark[u] = True
            children += 1
        if p == -1 and children > 1:
            mark[u] = True
    for i in range(V):
        if tin[i] == -1:
            dfs(i, -1)
    out = [i for i in range(V) if mark[i]]
    return out or [-1]
```

**Complexity:** time **O(V + E)**, space **O(V + E)** — one DFS over all vertices and edges.

---

## Edge cases

- Root with one child: never a cut vertex, even though `low[child] ≥ tin[root]` always holds.
- Isolated vertices: not cut vertices.
- Vertex qualifying through several children: mark once (boolean, not a list append).

---

## Common mistakes

1. Using `>` (bridge condition), which misses vertices on cycles joined at a point.
2. Applying the child rule to the root.
3. Appending u to the answer per qualifying child, producing duplicates.

---

## Follow-ups

1. Biconnected components?
2. Every bridge endpoint an articulation point?

<details><summary>Answer sketches</summary>

**#1:** Keep an edge stack; when `low[v] ≥ tin[u]`, pop edges down to u–v as one block.

**#2:** Not always: an endpoint of degree 1 is not. Otherwise yes.
</details>

---

## Flashcards

**Articulation point condition (non-root)?** #flashcard
Some DFS child v with low[v] ≥ tin[u].

**Articulation point root rule?** #flashcard
Root is a cut vertex iff it has ≥ 2 DFS children.

**Bridge vs articulation comparison?** #flashcard
Bridge: low[v] > tin[u]. Vertex: low[v] ≥ tin[u].

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
