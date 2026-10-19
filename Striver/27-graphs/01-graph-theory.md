---
module: striver/27-graphs
lesson: 1
topic: Graphs — vocabulary, representations, BFS/DFS invariants, components, cycle detection, bipartiteness, topological sort, shortest-path decision table
source: https://takeuforward.org/learning/dsa/introduction-to-graph?category=theory-and-traversals&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bfs, dfs, topological-sort, shortest-path, theory]
---
# 1. Graphs: Representations, BFS/DFS, Cycles, Topological Order and Shortest Paths

← [Part 27 index](README.md) · Next → [Minimum Spanning Trees and Disjoint Set Union](02-mst-and-dsu-theory.md)

> [!abstract] What this covers
> **Core idea:** A graph is a set of vertices and the edges between them. Almost every graph problem is one of three things:
> 1. A **traversal** (BFS or DFS) that visits each vertex once and does some bookkeeping along the way.
> 2. An **ordering** (topological sort) of a DAG.
> 3. A **shortest-path** relaxation whose algorithm depends only on the edge weights.
>
> Pick the representation, pick the traversal, and decide what to record: `visited`, `dist`, `parent`, `color`, `indegree` or finish order.
>
> **You'll be able to:** choose between an adjacency list, a matrix and an edge list; turn grids and word lists into implicit graphs; write BFS and DFS with the correct visited timing; count components; detect cycles in undirected graphs (parent check) and directed graphs (recursion stack / Kahn); test bipartiteness; produce a topological order two ways; and pick the right shortest-path algorithm from the weights alone.
> **Source:** [Striver: Introduction to graphs](https://takeuforward.org/learning/dsa/introduction-to-graph?category=theory-and-traversals&source=strivers-a2z-dsa-sheet) · **Time:** 75 min

**Sections:** [1. Vocabulary](#1-vocabulary) · [2. Representations](#2-representations) · [3. Implicit graphs](#3-implicit-graphs) · [4. BFS](#4-bfs) · [5. DFS](#5-dfs) · [6. Connected components](#6-connected-components) · [7. Cycle detection](#7-cycle-detection) · [8. Bipartite graphs](#8-bipartite-graphs) · [9. Topological sort](#9-topological-sort) · [10. Shortest paths: the decision table](#10-shortest-paths-the-decision-table) · [11. Multi-source BFS and 0-1 BFS](#11-multi-source-bfs-and-0-1-bfs) · [12. Complexity summary](#12-complexity-summary) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Key terms](#key-terms) · [Flashcards](#flashcards)

---

## 1. Vocabulary

| Term | Meaning |
|---|---|
| **Undirected / directed** | an edge `u–v` works both ways, while an edge `u → v` works one way only |
| **Weighted** | each edge carries a cost `w` |
| **Degree** | the number of incident edges. Directed graphs split it into **indegree** and **outdegree** |
| **Path / cycle** | a sequence of distinct vertices joined by edges, or a path that returns to its start |
| **Connected** | every vertex can reach every other (undirected) |
| **Strongly connected** | every vertex can reach every other along directed edges |
| **Tree** | connected and acyclic, so it has exactly `V − 1` edges |
| **Forest** | an acyclic graph made of `c` trees, so it has `V − c` edges |
| **DAG** | a directed acyclic graph: it has a topological order |
| **Sparse / dense** | `E ≈ V` versus `E ≈ V²` |

**Handshake lemma:** `Σ degree = 2E` in an undirected graph. Two consequences:
- The number of odd-degree vertices is even.
- An adjacency list stores `2E` entries (`E` if directed).

Edge-count limits: a simple undirected graph has at most `V(V−1)/2` edges, and a simple directed graph at most `V(V−1)`. If a problem says `E ≤ 2·10⁵` and `V ≤ 10⁵`, the graph is sparse, so use an adjacency list.

---

## 2. Representations

| | Adjacency matrix | Adjacency list | Edge list |
|---|---|---|---|
| Space | O(V²) | O(V + E) | O(E) |
| "Is `u–v` an edge?" | O(1) | O(deg u) | O(E) |
| Iterate neighbours of u | O(V) | O(deg u) | O(E) |
| Best for | dense graphs, Floyd-Warshall, V ≤ ~2000 | almost everything else | Kruskal, Bellman-Ford |

```cpp
vector<vector<int>> adj(V);                      // unweighted
for (auto& e : edges) { adj[e[0]].push_back(e[1]); adj[e[1]].push_back(e[0]); }
vector<vector<pair<int,int>>> wadj(V);           // weighted: (neighbour, weight)
```
```java
List<List<Integer>> adj = new ArrayList<>();
for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
```
```python
adj = [[] for _ in range(V)]
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)          # omit for directed
```

**1-indexed input:** allocate `V + 1` lists rather than shifting every index. Off-by-one errors on vertex labels are the most common graph bug in interviews.

---

## 3. Implicit graphs

Many problems never mention a graph, but they describe one:

| Disguise | Vertices | Edges |
|---|---|---|
| Grid (islands, oranges, mazes) | cells `(r, c)` | 4 or 8 neighbours that pass a filter |
| Word ladder | words | words that differ in one letter |
| Lock / puzzle states | states such as `"0000"` | single moves |
| Course prerequisites | courses | `prereq → course` |
| Alien dictionary | letters | first differing letter of adjacent words |
| Equations `a / b = k` | variables | weighted `a → b` (k) and `b → a` (1/k) |

The grid idiom:

```python
for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    r2, c2 = r + dr, c + dc
    if 0 <= r2 < n and 0 <= c2 < m and grid[r2][c2] == 1 and not seen[r2][c2]:
        ...
```

Encode a cell as `r·m + c` when you need a single integer, for example as a DSU id or as a key into `dist`.

---

## 4. BFS

BFS uses a queue, so it expands vertices in **non-decreasing distance** from the source. The first time it reaches a vertex is along a shortest path, provided every edge has the same weight.

```python
from collections import deque
def bfs(adj, s):
    dist = [-1] * len(adj)
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:          # doubles as `visited`
                dist[v] = dist[u] + 1  # mark on PUSH
                q.append(v)
    return dist
```

- **Mark visited when you push, not when you pop.** If you mark on pop, a vertex can sit in the queue many times.
- **Processing level by level:** take `for _ in range(len(q))` at the top of the loop. Rotten oranges and word ladder count levels this way.
- **Cost:** O(V + E) time and O(V) space.

---

## 5. DFS

DFS goes as deep as possible before it backtracks. You can write it with recursion or with an explicit stack. Its strength is the **timing** it exposes: a vertex is *entered* (pre-order), and later it *finishes* (post-order) once its whole subtree is done.

```python
def dfs(u):
    seen[u] = True
    # pre-order work
    for v in adj[u]:
        if not seen[v]:
            dfs(v)
    # post-order work (topological order, low-link, subtree sizes)
```

DFS classifies the edges of a **directed** graph into four kinds:

| Edge `u → v` | When | Meaning |
|---|---|---|
| Tree | `v` unvisited | becomes a DFS child |
| Back | `v` is on the current recursion stack | **cycle** |
| Forward | `v` is a finished descendant of `u` | harmless |
| Cross | `v` is finished, in another branch | harmless |

In an undirected DFS, every non-tree edge is a back edge. That is why the parent check (§7) is enough there.

**Recursion depth:** a path graph with V = 10⁵ makes recursive DFS 10⁵ calls deep. Python's default limit is 1000, so raise it with `sys.setrecursionlimit` or use an iterative stack. Java's default stack overflows at around 10⁴–10⁵ frames.

---

## 6. Connected components

Each traversal started from an unvisited vertex covers exactly one component:

```python
comps = 0
for s in range(V):
    if not seen[s]:
        comps += 1
        dfs(s)
```

**Equivalent with DSU:** start with `comps = V` and decrement on every union that succeeds ([Lesson 2](02-mst-and-dsu-theory.md)). Use DSU when edges arrive online or when you also need component sizes.

---

## 7. Cycle detection

| Graph | Method | Cycle iff |
|---|---|---|
| Undirected | BFS/DFS storing each vertex's parent | you meet a visited neighbour that is **not your parent** |
| Undirected | DSU | an edge joins two vertices already in the same set |
| Undirected | counting | `E > V − components` |
| Directed | DFS with `path[]` (recursion stack) / 3 colours | you meet a vertex that is still **on the stack** (grey) |
| Directed | Kahn's algorithm | the topological order has fewer than `V` vertices |

Why "visited" alone fails for directed graphs: take `0 → 1`, `0 → 2`, `2 → 1`. DFS reaches 1 twice, yet there is no cycle. Only an edge back to a vertex still on the current path closes a cycle.

```python
WHITE, GREY, BLACK = 0, 1, 2
def has_cycle(u):
    color[u] = GREY
    for v in adj[u]:
        if color[v] == GREY: return True
        if color[v] == WHITE and has_cycle(v): return True
    color[u] = BLACK
    return False
```

**Eventual safe states** reuses this colouring. The safe vertices are the ones that finish BLACK and can never reach a GREY vertex. Equivalently, run Kahn's algorithm on the reversed graph.

---

## 8. Bipartite graphs

A graph is bipartite when its vertices can be 2-coloured so that every edge joins different colours. This holds **iff the graph has no odd-length cycle.**

To test it, run BFS or DFS and give each neighbour the opposite colour. If an edge ever joins two vertices of the same colour, the graph is not bipartite. Run the test from every uncoloured vertex, because the graph may be disconnected.

A tree is always bipartite. An even cycle is bipartite. A triangle is not.

---

## 9. Topological sort

A topological order is a linear order of the vertices in which every edge `u → v` puts `u` before `v`. It **exists iff the graph is a DAG.**

| | DFS finish order | Kahn's algorithm (BFS) |
|---|---|---|
| Idea | when `u` finishes, everything reachable from it has already been emitted | repeatedly remove a vertex with indegree 0 |
| Output | reverse the finish order | the order in which vertices are dequeued |
| Detects a cycle? | only with grey/black colouring | yes: the output has fewer than V vertices |
| Lexicographically smallest order | no | yes, if you use a min-heap instead of a queue |

```python
from collections import deque
def kahn(V, adj):
    indeg = [0] * V
    for u in range(V):
        for v in adj[u]:
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
    return order if len(order) == V else []      # [] means a cycle
```

**Where it shows up:** course schedule I/II, alien dictionary, build orders, shortest/longest path in a DAG (relax in topological order) and eventual safe states.

---

## 10. Shortest paths: the decision table

Choose the algorithm from the **edge weights** and from **how many sources** you need:

| Weights | Sources | Algorithm | Time |
|---|---|---|---|
| all equal (unit) | one / many | **BFS** (multi-source: put every source in the queue) | O(V + E) |
| only 0 and 1 | one | **0-1 BFS** with a deque | O(V + E) |
| any weights, graph is a DAG | one | **relax edges in topological order** | O(V + E) |
| non-negative | one | **Dijkstra** with a min-heap | O(E log V) |
| negative edges allowed, need to detect negative cycles | one | **Bellman-Ford**: V − 1 rounds, then one check round | O(V·E) |
| at most k edges | one | **Bellman-Ford limited to k + 1 rounds** (copy `dist` each round), or BFS over (node, stops) | O(k·E) |
| any (no negative cycles) | all pairs | **Floyd-Warshall** | O(V³) |
| non-negative | all pairs, sparse | Dijkstra from every vertex | O(V·E log V) |

**Relaxation**, which all of them share:

```text
if dist[u] + w < dist[v]:
    dist[v] = dist[u] + w
    parent[v] = u
```

The algorithms differ only in the **order** in which they relax edges.

**Why Dijkstra needs non-negative weights.** When Dijkstra pops `u` with distance `d`, it assumes no later path can reach `u` more cheaply. A negative edge breaks that assumption.

**The lazy-deletion idiom.** Push duplicate heap entries, then skip any popped entry whose `d > dist[u]`.

**Path reconstruction.** Record `parent[v]` during relaxation, then walk back from the target and reverse the list.

**Dijkstra variants seen in Part 27:**
- **Path with minimum effort:** the cost is the max edge on the path, not the sum.
- **Swim in rising water:** the max cell value along the path.
- **Number of ways to arrive:** keep a count array and add to it on ties (`==`).
- **Cheapest flights:** the state is (node, stops), so plain distance ordering is wrong.

---

## 11. Multi-source BFS and 0-1 BFS

**Multi-source BFS.** Start with **every** source in the queue at distance 0. One BFS then computes each vertex's distance to its nearest source.
- Examples: rotten oranges, distance to the nearest 1, walls and gates.
- Cost: O(V + E), not O(k·(V + E)).
- **Reverse the question** when that helps. "Which cells can reach the border?" becomes "BFS inward from the border" (surrounded regions, number of enclaves, Pacific–Atlantic).

**0-1 BFS.** When weights are only 0 and 1, use a deque:
- push a **front** neighbour for a 0-edge;
- push a **back** neighbour for a 1-edge.

The deque stays sorted by distance, so you get Dijkstra's correctness in O(V + E).

---

## 12. Complexity summary

| Task | Time | Space |
|---|---|---|
| BFS / DFS / components / bipartite / undirected cycle | O(V + E) | O(V) |
| Directed cycle / topological sort | O(V + E) | O(V) |
| DAG shortest path | O(V + E) | O(V) |
| Dijkstra (binary heap) | O(E log V) | O(V + E) |
| Bellman-Ford | O(V·E) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Grid BFS on `n × m` | O(n·m) | O(n·m) |

---

## Common mistakes

- **Marking visited on pop in BFS.** This queues duplicates and, if you track levels carelessly, gives wrong distances.
- **Using a plain `visited` array for directed cycles.** You need the on-stack/grey state.
- **Undirected parent check with parallel edges.** Skip the parent's **edge id**, not the parent vertex.
- **Traversing only from vertex 0.** Disconnected graphs need an outer loop over every vertex.
- **Running Dijkstra with negative edges, or treating a grid with 0/1 costs as plain BFS.**
- **Forgetting the `d > dist[u]` stale check in lazy Dijkstra.** The result is still correct but can be much slower, and counting problems (number of ways) give wrong totals.
- **Building a 1-indexed graph in a 0-indexed array.**
- **Python recursion depth** on deep DFS.

---

## Practice

<details><summary>1. V = 10⁵, E = 2·10⁵. Matrix or list? How much memory does each need?</summary>

A list: about 4·10⁵ ints for the undirected entries, roughly 1.6 MB. A matrix needs 10¹⁰ cells, which is impossible.
</details>

<details><summary>2. BFS from 0 on edges 0–1, 0–2, 1–3, 2–3, 3–4. Give the distances and one BFS order.</summary>

dist = [0, 1, 1, 2, 3]. One BFS order is 0, 1, 2, 3, 4. Vertex 3 is discovered from 1, so it is not pushed again from 2.
</details>

<details><summary>3. Does the directed graph 0→1, 1→2, 0→2 contain a cycle? What would a plain visited-check DFS report?</summary>

There is no cycle. A plain visited check reaches 2 a second time (via 0→2) and wrongly reports one. Grey/black colouring is correct, because 2 is already black at that point.
</details>

<details><summary>4. Give a Kahn order for 5→0, 5→2, 4→0, 4→1, 2→3, 3→1.</summary>

The indegree-0 vertices are 4 and 5. One valid order is 4, 5, 0, 2, 3, 1. Other orders are also valid.
</details>

<details><summary>5. Is a 5-cycle bipartite? Is a 6-cycle?</summary>

A 5-cycle is not (odd cycle). A 6-cycle is (alternate the colours).
</details>

<details><summary>6. Weights are in {0, 1}, V = 10⁶. Which algorithm, and why not Dijkstra?</summary>

Use 0-1 BFS, which runs in O(V + E). Dijkstra also works but adds a log factor and heap overhead.
</details>

<details><summary>7. Some edges are negative, there are no cycles, and the graph is a DAG. Fastest single-source algorithm?</summary>

Relax the edges in topological order. That is O(V + E), and negative weights are fine in a DAG.
</details>

<details><summary>8. Cheapest flight with at most k stops: why can plain Dijkstra on (cost) fail?</summary>

A cheaper path may use too many stops and block a slightly costlier path that is within k. The state must include the stop count. Bellman-Ford limited to k + 1 rounds, or BFS level by level on stops, handles this.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Adjacency list | `adj[u]` = the list of `u`'s neighbours, O(V + E) space |
| Implicit graph | vertices and edges generated on the fly (grid cells, words, states) |
| Multi-source BFS | BFS started with all sources at distance 0 |
| Back edge | an edge to a vertex still on the DFS recursion stack |
| Indegree | the number of edges entering a vertex |
| Topological order | a linear order consistent with every directed edge |
| Relaxation | `dist[v] = min(dist[v], dist[u] + w)` |
| Lazy deletion | skip stale heap entries instead of decreasing keys |
| Bipartite | 2-colourable, equivalently it has no odd cycle |

---

## Flashcards

**Matrix vs list: when to use the matrix?** #flashcard
Dense graphs, O(1) edge lookup, or Floyd-Warshall with V ≤ ~2000.

**BFS: mark visited when?** #flashcard
When you push, so each vertex is queued at most once.

**Undirected cycle test (DFS/BFS)?** #flashcard
You meet a visited neighbour that is not the parent.

**Directed cycle test?** #flashcard
An edge to a grey (on-stack) vertex, or Kahn outputs fewer than V vertices.

**Bipartite iff?** #flashcard
There is no odd-length cycle; 2-colour by BFS/DFS.

**Two ways to topologically sort?** #flashcard
Reverse DFS finish order, or Kahn's algorithm (repeatedly remove indegree-0 vertices).

**Shortest path with unit weights?** #flashcard
BFS, O(V + E).

**Shortest path with 0/1 weights?** #flashcard
0-1 BFS with a deque: 0-edges go to the front, 1-edges to the back.

**Shortest path in a DAG with negative weights?** #flashcard
Relax the edges in topological order, O(V + E).

**Dijkstra precondition and cost?** #flashcard
Non-negative weights; O(E log V) with a binary heap.

**Bellman-Ford rounds and negative-cycle check?** #flashcard
Relax all edges V − 1 times; if a V-th round still improves something, there is a negative cycle.

**Floyd-Warshall loop order?** #flashcard
The intermediate vertex `k` is the outermost loop.

**Multi-source BFS cost?** #flashcard
O(V + E): one BFS seeded with every source.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
