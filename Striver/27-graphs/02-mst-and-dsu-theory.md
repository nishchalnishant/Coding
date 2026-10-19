---
module: striver/27-graphs
lesson: 2
topic: Minimum spanning trees (cut/cycle properties, Prim, Kruskal) and Disjoint Set Union (path compression, union by rank/size, patterns)
source: https://takeuforward.org/learning/dsa/mst-theory?category=minimum-spanning-tree&source=strivers-a2z-dsa-sheet
tags: [striver, graph, mst, prim, kruskal, dsu, union-find, theory]
---
# 2. Minimum Spanning Trees and Disjoint Set Union

← [Graphs: Representations, BFS/DFS, Cycles, Topological Order and Shortest Paths](01-graph-theory.md) · [Part 27 index](README.md) · Next → [Traversal Techniques](03-traversal-techniques-bfs-dfs.md)

> [!abstract] What this covers
> **Core idea:** A minimum spanning tree (MST) connects every vertex at the lowest total edge weight.
> - Two greedy rules are always safe:
>   - **cut property:** the lightest edge crossing any cut belongs to some MST;
>   - **cycle property:** the heaviest edge on a cycle can be dropped.
> - Prim grows one tree from a vertex. Kruskal merges forests in edge-weight order.
> - Kruskal's "does this edge make a cycle?" check is a **Disjoint Set Union** (DSU) query. With path compression plus union by rank/size, a DSU query costs amortised α(n) ≈ O(1).
>
> **You'll be able to:** state and use the cut and cycle properties; implement Prim (lazy heap) and Kruskal (sort + DSU) and give their complexities; write a DSU with both optimisations from memory; and recognise the DSU patterns: dynamic connectivity, counting components, grid unions, mapping strings or coordinates to ids, and "extra edges".
> **Source:** [Striver: MST theory](https://takeuforward.org/learning/dsa/mst-theory?category=minimum-spanning-tree&source=strivers-a2z-dsa-sheet) · **Time:** 60 min

**Sections:** [1. Spanning trees](#1-spanning-trees) · [2. Cut and cycle properties](#2-cut-and-cycle-properties) · [3. Prim's algorithm](#3-prims-algorithm) · [4. Kruskal's algorithm](#4-kruskals-algorithm) · [5. Prim vs Kruskal](#5-prim-vs-kruskal) · [6. Disjoint Set Union](#6-disjoint-set-union) · [7. Why α(n)](#7-why-αn) · [8. DSU patterns](#8-dsu-patterns) · [9. DSU vs BFS/DFS](#9-dsu-vs-bfsdfs) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Key terms](#key-terms) · [Flashcards](#flashcards)

---

## 1. Spanning trees

A **spanning tree** of a connected undirected graph is a subgraph that:
- includes every vertex;
- is a tree, so it is connected, acyclic and has exactly `V − 1` edges.

An **MST** is a spanning tree with the minimum total weight.

| Fact | Consequence |
|---|---|
| A disconnected graph has no spanning tree, only a spanning **forest** | Kruskal naturally returns a minimum spanning forest. Check `edgesUsed == V − 1` to know whether the graph was connected |
| If all weights are distinct, the MST is **unique** | With ties, several MSTs can exist, but they all have the **same total weight** |
| A complete graph `K_n` has `n^(n−2)` spanning trees (Cayley's formula) | Brute force is hopeless, so greedy algorithms are required |
| The MST also minimises the **largest** edge used (it is a minimum bottleneck spanning tree) | It answers "minimise the maximum edge needed to connect everything" questions |

MSTs apply to **undirected** graphs only. The directed analogue, the minimum arborescence (Edmonds' algorithm), is out of scope.

---

## 2. Cut and cycle properties

**Cut property.** Split V into two non-empty sets S and V∖S. The lightest edge crossing that cut belongs to **some** MST, and to every MST if it is strictly lightest.

*Proof sketch, by exchange.* Take an MST T that lacks the light edge `e = (u, v)`.
1. Adding `e` to T creates a cycle.
2. That cycle must cross the cut again through some other edge `f`, and `w(f) ≥ w(e)`.
3. `T + e − f` is still a spanning tree, and it weighs no more than T.

**Cycle property.** The strictly heaviest edge on any cycle belongs to **no** MST.

How the algorithms use these:
- **Prim** applies the cut property with S = the vertices already in the tree.
- **Kruskal** applies it to the cut that separates `u`'s component from everything else. Kruskal skips an edge exactly when it is the heaviest edge on a cycle so far, which is the cycle property.

---

## 3. Prim's algorithm

Grow a single tree outward from any start vertex. At each step, add the cheapest edge that leaves the tree.

```python
import heapq
def prim(V, adj):                      # adj[u] = [(v, w), ...]
    in_mst = [False] * V
    pq = [(0, 0)]                      # (weight, vertex)
    total = 0
    while pq:
        w, u = heapq.heappop(pq)
        if in_mst[u]:
            continue                   # stale entry (lazy deletion)
        in_mst[u] = True
        total += w
        for v, wt in adj[u]:
            if not in_mst[v]:
                heapq.heappush(pq, (wt, v))
    return total
```

**To output the edges as well**, push `(w, v, parent)` and record `(parent, v)` when you accept a vertex.

| Variant | Time | When |
|---|---|---|
| Lazy, binary heap (above) | O(E log E) = O(E log V) | the default in interviews |
| Eager, indexed heap / decrease-key | O(E log V) | the same order, with a smaller heap |
| Array, no heap | O(V²) | **dense** graphs or a complete graph given as points, e.g. LC 1584 *Min Cost to Connect All Points* |

The code looks almost identical to Dijkstra's, but the two do different things:
- **Dijkstra** sorts the heap by the distance **from the source**, `dist[u] + w`.
- **Prim** sorts it by the **edge weight** `w` alone.

Mixing these up is the classic Prim bug.

---

## 4. Kruskal's algorithm

Sort every edge by weight. Then take each edge in that order, keeping it only if it joins two different components.

```python
def kruskal(V, edges):                 # edges = [(w, u, v), ...]
    edges.sort()
    dsu = DSU(V)
    total = used = 0
    for w, u, v in edges:
        if dsu.union(u, v):            # False means it would form a cycle
            total += w
            used += 1
            if used == V - 1:
                break
    return total if used == V - 1 else -1   # -1 means disconnected
```

**Cost:** the sort dominates at O(E log E). The DSU work adds only O(E·α(V)).

**Stop early** once you have `V − 1` edges. On dense inputs this skips most of the remaining edges.

---

## 5. Prim vs Kruskal

| | Prim | Kruskal |
|---|---|---|
| Grows | one tree | a forest that merges |
| Data structure | min-heap + `in_mst[]` | sorted edges + DSU |
| Input it prefers | an adjacency list | an edge list |
| Dense graph | O(V²) array version wins | sorting V² edges is costly |
| Disconnected graph | covers one component only (restart it for a forest) | produces a spanning forest for free |
| Edges arrive pre-sorted or online | awkward | natural |
| Also gives | — | connectivity queries via the DSU |

**Rule of thumb:** if you are given an edge list, or you also need DSU-style connectivity, use Kruskal. If the graph is dense or given implicitly (points), use the O(V²) Prim.

---

## 6. Disjoint Set Union

The DSU maintains a partition of `{0 … n−1}` under two operations:
- `find(x)` returns the representative (root) of x's set;
- `union(a, b)` merges the two sets.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.comps = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra                               # attach smaller under larger
        self.size[ra] += self.size[rb]
        self.comps -= 1
        return True
```
```cpp
struct DSU {
    vector<int> p, sz;
    DSU(int n) : p(n), sz(n, 1) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }      // full compression
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a; sz[a] += sz[b];
        return true;
    }
};
```

The two optimisations:

| Optimisation | What it does | Alone |
|---|---|---|
| **Union by rank** (rank ≈ an upper bound on tree height) **or by size** | attaches the shallower or smaller tree under the other | height ≤ log n, so O(log n) per operation |
| **Path compression** (full, or halving/splitting) | points nodes on the find path directly (or closer) to the root | O(log n) amortised |
| **Both** | | **O(α(n)) amortised**, effectively constant |

**Rank or size?** They have the same asymptotics. Size is more useful in practice because it answers "how big is this component?", for example in *Making a Large Island*.

**Rank rule:** increment the rank only when two **equal**-rank roots merge. Path compression never updates rank, which is why rank is an upper bound on height rather than the exact height.

---

## 7. Why α(n)

α is the inverse Ackermann function. α(n) ≤ 4 for every n below 2^(2^(2^65536)), which is far more than the number of atoms in the universe.

The Tarjan / Hopcroft–Ullman analysis shows that `m` operations on `n` elements cost O(m·α(n)) in total.

**What to say in an interview:** "amortised near-constant, inverse Ackermann." You do not need to derive it.

One caveat: the bound is **amortised**. A single `find` can still walk O(log n) nodes before compression flattens the path.

---

## 8. DSU patterns

| Pattern | Trick | Part 27 problems |
|---|---|---|
| **Count components / connectivity** | start `comps = n`, decrement on each union that succeeds | Number of provinces (DSU version) |
| **Extra / redundant edges** | a union of two nodes already in one set means a spare edge. Need ≥ `comps − 1` spares | LC 1319 *Number of Operations to Make Network Connected* |
| **Map non-integers to ids** | give strings an id through a hashmap, union them, then group by root | LC 721 *Accounts Merge* |
| **Grid unions** | cell id = `r·m + c`; union with each land neighbour | LC 305 *Number of Islands II* (online additions) |
| **Union then query sizes** | union every 1-cell, then try each 0-cell: `1 + Σ size` of its **distinct** neighbouring roots | LC 827 *Making a Large Island* |
| **Union rows with columns** | a stone `(r, c)` unions `r` with `c + offset`; answer = stones − components | LC 947 *Most Stones Removed* |
| **Offline queries sorted by threshold** | sort the edges and the queries, then add edges as the threshold grows | LC 1697 (the same idea as Kruskal) |
| **Cycle in an undirected edge stream** | a union that fails means a cycle | LC 684 *Redundant Connection* |

**Limit:** a DSU cannot **delete** edges or split sets. If a problem needs deletions, reverse time: process the operations backwards so that deletions become additions.

---

## 9. DSU vs BFS/DFS

| Need | Prefer |
|---|---|
| A one-off component count on a static graph | either works; BFS/DFS is simpler |
| Edges arriving one by one, with connectivity queries in between | **DSU** |
| Component **sizes** maintained under merges | **DSU** |
| Shortest path or distance | **BFS** (the DSU knows nothing about paths) |
| Directed reachability or SCCs | DFS (Kosaraju/Tarjan); DSU is undirected only |

---

## Common mistakes

- **Writing `parent[a] = b` instead of `parent[find(a)] = find(b)`.** Union must link **roots**.
- **Comparing `parent[a] == parent[b]` to test connectivity.** Compare `find(a) == find(b)`.
- **Recursive `find` in Python on long chains.** Without rank or size it can hit the recursion limit, so use the iterative halving version.
- **Running Prim with `dist[u] + w`.** That is Dijkstra.
- **Kruskal on a disconnected graph that reports the forest weight as an MST.** Check `used == V − 1`.
- **Making a Large Island: summing the same root twice** when two neighbours share one component. Dedupe the roots with a set.
- **Most Stones Removed:** forgetting to offset column ids, which makes row 3 and column 3 collide.

---

## Practice

<details><summary>1. Edges: (0,1,4) (0,2,3) (1,2,1) (1,3,2) (2,3,4) (3,4,2). Run Kruskal: which edges does it take, and what is the weight?</summary>

Sorted: (1,2,1), (1,3,2), (3,4,2), (0,2,3), (0,1,4), (2,3,4).

It takes 1–2, 1–3, 3–4 and 0–2, for a total weight of 8. It skips 0–1 and 2–3 because each would close a cycle.
</details>

<details><summary>2. Run Prim from vertex 0 on the same graph. In what order does it add vertices?</summary>

0, then 2 (w = 3), then 1 (w = 1), then 3 (w = 2), then 4 (w = 2). Total 8, the same as Kruskal.
</details>

<details><summary>3. Every edge weight is distinct. How many MSTs are there?</summary>

Exactly one.
</details>

<details><summary>4. A graph has 10 vertices, 12 edges and 3 components. How many redundant edges are there, and how many cables must move to connect everything?</summary>

A spanning forest uses 10 − 3 = 7 edges, so 12 − 7 = 5 are spare. You need 3 − 1 = 2 moves, which is possible because 5 ≥ 2.
</details>

<details><summary>5. Why does union by size alone give O(log n) height?</summary>

A node's depth grows only when its tree is attached under one at least as large. Each such step at least doubles the size of the set containing it, and that can happen at most log₂ n times.
</details>

<details><summary>6. Points on a plane, n = 1000, with all pairwise Manhattan edges. Prim or Kruskal?</summary>

O(n²) array Prim: about 10⁶ operations. Kruskal would first have to sort about 5·10⁵ edges.
</details>

<details><summary>7. The stones are (0,0) (0,1) (1,0) (1,2) (2,2). How many can be removed?</summary>

All five stones form one component: (0,0) connects to (0,1) and (1,0), and (1,0) connects through row 1 to (1,2), which connects through column 2 to (2,2). Answer: 5 − 1 = 4.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Spanning tree | an acyclic subgraph with all V vertices and V − 1 edges |
| MST | the spanning tree of minimum total weight |
| Cut | a partition of the vertices into two non-empty sets |
| Light edge | the minimum-weight edge crossing a cut |
| DSU / union-find | a structure for disjoint sets with `find` and `union` |
| Path compression | re-pointing nodes on a find path toward the root |
| Union by rank / size | attaching the shallower or smaller tree under the other root |
| α(n) | the inverse Ackermann function, ≤ 4 for any practical n |
| Spanning forest | the union of spanning trees of each component |

---

## Flashcards

**Cut property?** #flashcard
The lightest edge crossing any cut is in some MST.

**Cycle property?** #flashcard
The strictly heaviest edge on a cycle is in no MST.

**Prim's complexity (heap) and its dense-graph variant?** #flashcard
O(E log V) with a heap; O(V²) with an array for dense graphs.

**Kruskal's complexity?** #flashcard
O(E log E) for the sort, plus O(E·α(V)) for the DSU.

**Prim heap key vs Dijkstra heap key?** #flashcard
Prim uses the edge weight `w`; Dijkstra uses `dist[u] + w`.

**When does Kruskal know the graph is disconnected?** #flashcard
It accepts fewer than V − 1 edges.

**DSU with both optimisations: cost?** #flashcard
Amortised O(α(n)), effectively constant.

**When does the rank increase?** #flashcard
Only when two roots of equal rank merge.

**Count components with DSU?** #flashcard
Start at `n` and decrement on every union that succeeds.

**Can a DSU delete an edge?** #flashcard
No. Process the operations in reverse so deletions become additions.

**Most Stones Removed: what is the answer?** #flashcard
Stones − components, after unioning each row with its column (offset the column ids).

**Making a Large Island: the key trick?** #flashcard
For each 0-cell, take 1 + the sum of the sizes of its distinct neighbouring roots.

**Interview track →** [Union-find deep-dive](../../02-algorithms/14-union-find.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md) · [Greedy](../../02-algorithms/16-greedy.md)
