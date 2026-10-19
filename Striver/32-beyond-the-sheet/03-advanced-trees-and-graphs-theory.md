---
module: striver/32-beyond-the-sheet
lesson: 3
topic: Advanced trees and graphs — binary lifting and LCA, Euler tour and subtree ranges, Hierholzer's Eulerian path, 0-1 BFS, multi-source BFS, A*, bipartite matching overview, strongly connected components overview
source: beyond the A2Z sheet (enrichment)
tags: [striver, beyond-sheet, theory, lca, binary-lifting, euler-tour, hierholzer, 0-1-bfs]
---
# 3. Advanced Trees and Graphs

← [Advanced DP](02-advanced-dp-theory.md) · [Part 32 index](README.md) · Next → [Techniques toolbox](04-techniques-toolbox-theory.md)

> [!abstract] What this covers
> **Core idea:** Three ideas turn hard tree and graph questions into ones you already know.
> - **Binary lifting** stores ancestors at power-of-two distances, so a k-th ancestor or LCA query costs O(log n).
> - An **Euler tour** flattens a tree, so every subtree becomes a contiguous array range and range structures apply.
> - **Edge-centric traversals** (Hierholzer, 0-1 BFS) adapt DFS and BFS when edges, not nodes, are what matters.
>
> **You'll be able to:** answer LCA and k-th-ancestor queries; turn subtree queries into range queries; build an Eulerian path (Reconstruct Itinerary); and use 0-1 BFS instead of Dijkstra for 0/1 weights.
> **Source:** not in the A2Z sheet. It extends [Part 24 trees](../24-binary-trees/README.md) and [Part 27 graphs](../27-graphs/README.md). Tarjan/SCC and matching are listed for completeness only. · **Time:** 60 min

**Sections:** [1. Binary lifting](#1-binary-lifting) · [2. LCA methods](#2-lca-methods) · [3. Euler tour](#3-euler-tour) · [4. Hierholzer](#4-hierholzer) · [5. BFS variants](#5-bfs-variants) · [6. Reference only](#6-reference-only)

---

## 1. Binary lifting

`up[k][v]` is the 2ᵏ-th ancestor of v. Set `up[0][v] = parent[v]`, and `up[k][v] = up[k−1][ up[k−1][v] ]`.

```cpp
int kth(int v, int k) {
    for (int j = 0; j < LOG && v != -1; j++)
        if (k >> j & 1) v = up[j][v];
    return v;
}
int lca(int a, int b) {
    if (depth[a] < depth[b]) swap(a, b);
    a = kth(a, depth[a] - depth[b]);
    if (a == b) return a;
    for (int j = LOG - 1; j >= 0; j--)
        if (up[j][a] != up[j][b]) a = up[j][a], b = up[j][b];
    return up[0][a];
}
```

- **Cost:** O(n log n) build and O(log n) per query.
- **Distance between two nodes:** `depth[a] + depth[b] − 2·depth[lca]`.
- **k-th ancestor of a tree node:** LC 1483. This is the canonical interview version.

---

## 2. LCA methods

| Method | Pre | Query | When |
|---|---|---|---|
| Recursive (Part 24) | — | O(n) | Single query, binary tree |
| BST walk | — | O(h) | BST (Part 25) |
| Parent pointers + set | — | O(h) | Nodes have parent links |
| Binary lifting | O(n log n) | O(log n) | Many queries, also k-th ancestor |
| Euler tour + sparse table | O(n log n) | O(1) | Many queries, static tree |
| Tarjan offline | O(n α) | O(1) amortised | All queries known up front (DSU) |

---

## 3. Euler tour

Record `tin[v]` on entering v and `tout[v]` on leaving it. Then **u is in the subtree of v iff `tin[v] ≤ tin[u] ≤ tout[v]`**.

| Query | Reduction |
|---|---|
| Subtree sum, point update | BIT over the tin order: `sum(tin[v], tout[v])` |
| Add to a subtree | Range update over `[tin, tout]` |
| Is u an ancestor of v? | Check the tin/tout containment, O(1) |
| LCA in O(1) | Full Euler sequence (2n − 1) + RMQ on depth |
| Path queries | Heavy-light decomposition (out of scope) |

---

## 4. Hierholzer

An **Eulerian path** uses every edge exactly once.

| Graph | Eulerian circuit exists iff | Eulerian path exists iff |
|---|---|---|
| Undirected | All degrees even (and edges connected) | 0 or 2 odd-degree vertices |
| Directed | in = out everywhere | One vertex with out − in = 1 (the start) and one with in − out = 1 |

```text
dfs(u): while adj[u] not empty: v = pop(adj[u]); dfs(v)
        path.append(u)
answer = reverse(path)
```

- **Cost:** O(E).
- **Reconstruct Itinerary (LC 332):** keep the adjacency in a min-heap or sorted order to get the lexicographically smallest itinerary.
- **Cracking the Safe (LC 753):** a De Bruijn sequence is an Eulerian circuit over the (n−1)-length prefixes.
- **Valid Arrangement of Pairs (LC 2097):** a directed Eulerian path.

---

## 5. BFS variants

| Variant | When | How |
|---|---|---|
| Multi-source BFS | Distance to the nearest of many sources | Seed the queue with all sources at distance 0 (rotting oranges, 01-matrix, Part 27) |
| 0-1 BFS | Weights are only 0 and 1 | Deque: a 0-edge goes to the front, a 1-edge to the back. O(V + E). Example: minimum cost to make a valid grid path (LC 1368) |
| BFS on state | Extra state such as keys or a mask | Node = (cell, mask); shortest path to get all keys (LC 864) |
| Bidirectional BFS | Huge implicit graph, known target | Expand the smaller frontier; Word Ladder (Part 27) |
| Dial's / bucket | Small integer weights ≤ C | Buckets by distance |
| A* | Admissible heuristic available | Dijkstra keyed on `g + h`; sliding puzzle with the Manhattan heuristic |

---

## 6. Reference only

These are out of scope for the repo (see `CLAUDE.md`). Know the names and what they solve:
- **Tarjan / Kosaraju SCC** (Striver covers Kosaraju in Part 27): finds strongly connected components in O(V + E).
- **Bridges / articulation points** (Tarjan low-link, Part 27): critical connections.
- **Bipartite matching** (Hopcroft–Karp), **max flow** (Edmonds–Karp/Dinic): assignment problems. These rarely come up in SWE interviews.
- **Heavy-light decomposition / centroid decomposition:** path queries on trees. These are competitive-programming level.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| `LOG` too small | `LOG = ceil(log2(n)) + 1` (17 for 10⁵, 20 for 10⁶) |
| The root's ancestor is undefined | Set `up[k][root] = root` or −1, and guard for it |
| Hierholzer that appends on entry | Append **after** exhausting the edges, then reverse |
| Dijkstra on 0/1 weights | 0-1 BFS is simpler and O(V + E) |
| Multi-source BFS run once per source | Seed all sources together |

---

## Practice

<details><summary>1. Distance between nodes 4 and 6 if depth[4] = 3, depth[6] = 2, depth[lca] = 1?</summary>

3 + 2 − 2 = 3.
</details>

<details><summary>2. Tickets [JFK→SFO, JFK→ATL, SFO→ATL, ATL→JFK, ATL→SFO]: itinerary?</summary>

JFK → ATL → JFK → SFO → ATL → SFO.
</details>

<details><summary>3. Subtree-sum queries with point updates on a tree of 10⁵ nodes?</summary>

An Euler tour, then a BIT over the tin positions. Each query or update is O(log n).
</details>

<details><summary>4. Grid with free moves along arrows and cost 1 to change direction: algorithm?</summary>

0-1 BFS.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Binary lifting | Ancestor tables at distances 2ᵏ |
| tin / tout | DFS entry and exit times |
| Eulerian path | Uses every edge exactly once |
| 0-1 BFS | Deque BFS for 0/1 weights |

---

## Flashcards

**Binary lifting recurrence?** #flashcard
up[k][v] = up[k−1][up[k−1][v]].

**Subtree as a range?** #flashcard
[tin[v], tout[v]] in Euler tour order.

**Hierholzer key step?** #flashcard
Post-order append after all edges are used, then reverse.

**0-1 BFS rule?** #flashcard
A 0-weight edge goes to the front of the deque, a 1-weight edge to the back.

**Directed Eulerian path condition?** #flashcard
in = out everywhere, except start (out − in = 1) and end (in − out = 1).

---

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md) · [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph walkthroughs](../../coding/algorithms/13-graph-algorithms.md)
