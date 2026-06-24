---
module: 02-algorithms
topic: Advanced Graphs
subtopic: 
status: unread
tags: [algorithms, advanced-graphs]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)
## First-Principles Map

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop. Do not move on until these are reflexive.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Highly probable; know the core patterns cold. Edge cases matter less.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Know what it is conceptually; skip deep implementation practice.


```
WHY advanced graph algos → WHAT they are → HOW they work → WHEN to use → WHAT can go wrong
       │                         │                │               │               │
  [Basic BFS/DFS/Dijkstra       [MST: spanning    [Kruskal: sort  [MST: network   [Bellman-Ford
   can't handle: minimum         tree min weight;  edges, union-   design min cost; O(VE) TLE on
   spanning trees, strongly      SCC: maximal      find; O(E log E) SCC: dependency  dense graphs;
   connected components,         strongly connected Prim: grow MST  resolution,     Tarjan SCC
   max network flow —            subgraphs;        by min edge;    2-SAT; Max Flow: base case off;
   need specialized              Articulation:     Tarjan SCC:     traffic routing, Dijkstra fails
   algorithms]                   bridges/cutpoints] DFS with low[] assignment]      negative weights]
       │                         │                │
  [real-world:                   [SCC invariant:  [Max Flow: Ford-Fulkerson
   cable laying (MST);           every node in     BFS to find augmenting path;
   Twitter follow graph          SCC can reach      saturate; repeat; O(VE²) Edmonds-
   (SCC = mutual follower        every other;       Karp; min cut = max flow by
   group); internet routing      Kosaraju: 2 DFS    max-flow min-cut theorem;
   (flow algorithms)]            passes]           key for bipartite matching]
       ↓
[Decision: Which advanced algorithm]
  ├── Min cost spanning tree → Kruskal (sparse) or Prim (dense) O(E log V)
  ├── Strongly connected     → Tarjan (one DFS) or Kosaraju (two DFS)
  ├── Max flow / matching    → Edmonds-Karp O(VE²) or Dinic O(V²E)
  └── Shortest path DAG      → Topological relaxation O(V+E)
```

## First-Principles Breakdown
- **Root problem**: MST, SCCs, and max flow require exploiting global graph structure that local BFS/DFS misses — each needs a specialized invariant-preserving traversal.
- **Core insight**: Kruskal's correctness follows from the cut property (lightest edge crossing any cut is in some MST); Tarjan's SCC uses DFS finish times and a "low" array to detect back edges that define SCC boundaries.
- **Invariant**: Kruskal: edges added in weight order, no cycle (union-find enforces); Tarjan: low[v] = minimum DFS discovery time reachable from v's subtree via back edges.
- **Why it's fast**: Kruskal O(E log E) — just sort + union-find; Tarjan O(V+E) — single DFS with O(1) per node low-value update.
- **Where it breaks**: Bellman-Ford O(VE) is too slow for dense graphs; Dijkstra breaks on negative edges; Tarjan's low-link computation has subtle bugs when counting tree vs back edges.

# Advanced Graph Algorithms — SDE-3 Level

```
[ADVANCED GRAPH ALGORITHMS — MINDMAP]
├── WHY IT EXISTS
│   ├── Standard BFS/DFS insufficient for: strongly connected components, bridges,
│   │   articulation points, max-flow, shortest path with negative weights
│   ├── Real systems (network routing, dependency resolution, scheduling) map to
│   │   these graph structures
│   └── SDE-3 signal: knowing which algorithm to invoke for which graph property
├── WHAT IT IS
│   ├── Kosaraju / Tarjan → Strongly Connected Components (SCCs)
│   ├── Tarjan / bridge-finding DFS → Bridges & Articulation Points
│   ├── Bellman-Ford → Shortest path with negative edges / negative cycle detection
│   ├── Floyd-Warshall → All-pairs shortest paths (dense graphs, small N)
│   └── Ford-Fulkerson / Edmonds-Karp → Max flow / min cut
├── HOW IT WORKS
│   ├── Kosaraju's SCC
│   │   ├── Step 1: DFS on original graph, push to stack in finish order
│   │   ├── Step 2: transpose graph (reverse all edges)
│   │   └── Step 3: DFS on transposed graph in reverse finish order → each DFS = 1 SCC
│   ├── Tarjan's SCC (single pass)
│   │   ├── Track disc[] (discovery time) and low[] (lowest reachable disc)
│   │   ├── Use explicit stack; node is SCC root when low[u] == disc[u]
│   │   └── Pop stack until root found → that set is one SCC
│   ├── Bridge / Articulation Point (Tarjan)
│   │   ├── Bridge: edge (u,v) is bridge if low[v] > disc[u]
│   │   └── Articulation: u is AP if low[v] >= disc[u] for any child v (root: ≥ 2 children)
│   ├── Bellman-Ford
│   │   ├── Relax all edges N-1 times
│   │   ├── If N-th relaxation still updates → negative cycle exists
│   │   └── O(VE) — slower than Dijkstra but handles negative weights
│   └── Edmonds-Karp (BFS-based max flow)
│       ├── Find augmenting path via BFS (shortest path in hops)
│       ├── Push flow along path, update residual graph
│       └── Repeat until no augmenting path → max flow found
├── COMPLEXITY
│   ├── Kosaraju:       O(V + E) time, O(V) space
│   ├── Tarjan SCC:     O(V + E) time, O(V) space
│   ├── Bridge finding: O(V + E) time
│   ├── Bellman-Ford:   O(VE) time, O(V) space
│   ├── Floyd-Warshall: O(V³) time, O(V²) space
│   └── Edmonds-Karp:   O(VE²) time
├── TRIGGER PATTERNS (when to use)
│   ├── "Find all SCCs / group mutually reachable nodes" → Kosaraju or Tarjan
│   ├── "Critical connections in network / bridges" → Tarjan bridge-finding
│   ├── "Single point of failure in network" → Articulation points
│   ├── "Shortest path with negative edges (no negative cycle)" → Bellman-Ford
│   ├── "Detect negative cycle" → Bellman-Ford N-th relaxation check
│   ├── "Max flow / bipartite matching / min cut" → Edmonds-Karp
│   └── "All-pairs shortest path, small graph N ≤ 500" → Floyd-Warshall
└── GOTCHAS
    ├── Kosaraju needs TWO DFS passes and explicit graph transposition
    ├── Tarjan: do NOT use visited[] — use disc[]/low[]; node on stack ≠ visited
    ├── Bellman-Ford: initialize dist[src]=0, all others=INF; use copy of dist each round
    ├── Floyd-Warshall: dp[i][j] = min(dp[i][j], dp[i][k]+dp[k][j]); k is outermost loop
    ├── Max flow: always update BOTH forward and backward residual edges
    └── Negative cycle in Bellman-Ford invalidates all shortest paths through it
```

SDE-3 interviews focus on complex topologies, strongly connected components, and network robustness.


For SDE 3 roles, problems often require knowledge of complex graph topologies, strongly connected components, or sophisticated shortest path algorithms.

## 1. Strongly Connected Components (Tarjan's)

### The Click Moment
> [!IMPORTANT]
> **The Click Moment**: "Find groups where everyone can reach everyone else in a **directed** graph" — OR — "condensation graph" — OR — "deadlock detection in complex dependency graphs".

Used to find all strongly connected components in a directed graph.


> [!TIP]
> **Tarjan's intuition `💤 T3`**: Think of DFS as exploring a cave system. Each cave (node) gets a discovery timestamp (`disc`). The `low` value tracks the earliest-discovered cave reachable from this subtree via back-edges. When `low[u] == disc[u]`, node `u` is the "root" of a strongly connected component — nothing in its subtree can reach back further than `u` itself. Pop everything on the stack down to `u`: that's one SCC.

```python
class Graph:
    def __init__(self, vertices):
        self.V = vertices 
        self.graph = collections.defaultdict(list) 
        self.Time = 0
  
    def addEdge(self, u, v):
        self.graph[u].append(v)
         
    def SCCUtil(self, u, low, disc, stackMember, st):
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        stackMember[u] = True
        st.append(u)
  
        for v in self.graph[u]:
            if disc[v] == -1:
                self.SCCUtil(v, low, disc, stackMember, st)
                low[u] = min(low[u], low[v])
            elif stackMember[v]: 
                low[u] = min(low[u], disc[v])
  
        w = -1 # To store stack extracted vertices
        if low[u] == disc[u]:
            component = []
            while w != u:
                w = st.pop()
                component.append(w)
                stackMember[w] = False
            print("SCC:", component)

    def SCC(self):
        disc = [-1] * self.V
        low = [-1] * self.V
        stackMember = [False] * self.V
        st = []
        for i in range(self.V):
            if disc[i] == -1:
                self.SCCUtil(i, low, disc, stackMember, st)
```

## 2. Critical Connections (Bridges & Articulation Points)

### The Click Moment
> [!IMPORTANT]
> **The Click Moment**: "Find edges whose removal disconnects the graph" (Bridges) — OR — "find nodes whose removal disconnects the graph" (Articulation Points) — OR — "network vulnerability analysis".

Very common in system design/LLD coding problems acting like "network robustess".

An Articulation Point is a vertex whose removal increases the number of connected components.
A Bridge is an edge whose removal increases the number of connected components.


```python
class BridgeGraph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = collections.defaultdict(list)
        self.Time = 0

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def bridgeUtil(self, u, visited, parent, low, disc, bridges):
        visited[u]= True
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1

        for v in self.graph[u]:
            if not visited[v]:
                parent[v] = u
                self.bridgeUtil(v, visited, parent, low, disc, bridges)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]: 
                    bridges.append((u, v))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])
                
    def findBridges(self):
        visited = [False] * (self.V)
        disc = [float("inf")] * (self.V)
        low = [float("inf")] * (self.V)
        parent = [-1] * (self.V)
        bridges = []
        for i in range(self.V):
            if not visited[i]:
                self.bridgeUtil(i, visited, parent, low, disc, bridges)
        return bridges
```

## 3. Eulerian Path & Circuit

> [!IMPORTANT]
> **The Click Moment**: "Traverse every **edge** exactly once" — OR — "reconstruct itinerary" — OR — "can you draw this figure without lifting your pen?" These are Eulerian path/circuit problems, not Hamiltonian (which is NP-hard).

**Rules (undirected graph):**
- Eulerian **circuit** exists iff: graph is connected AND every vertex has even degree.
- Eulerian **path `🎯 T2`** exists iff: graph is connected AND exactly 2 vertices have odd degree (they are start and end).

**Rules (directed graph):**
- Eulerian **circuit**: every vertex has in-degree == out-degree.
- Eulerian **path `🎯 T2`**: exactly one vertex has out-degree - in-degree = 1 (start), one has in-degree - out-degree = 1 (end).

**Hierholzer's Algorithm** (O(E)):
```python
from collections import defaultdict

def find_itinerary(tickets: list[list[str]]) -> list[str]:
    graph = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):
        graph[src].append(dst)
    result = []
    def dfs(node):
        while graph[node]:
            dfs(graph[node].pop())
        result.append(node)
    dfs("JFK")
    return result[::-1]
```

> [!TIP]
> The trick: sort edges in reverse so `.pop()` takes the lexicographically smallest destination. Add a node to `result` only AFTER all its outgoing edges are exhausted — this is post-order DFS, and reversing it gives the correct path.

## 4. Disjoint Set Union (Union-Find)

### The Click Moment
> [!IMPORTANT]
> **The Click Moment**: "Dynamic connectivity" — OR — "Kruskal's MST" — OR — "grouping elements with transitivity".

Essential for Kruskal's MST and solving connected components efficiently.


```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            # Union by rank
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
            return True # Connected successfully
        return False # Already connected
```

## 5. Other Advanced Graph Concepts

- **A* Search**: Heuristic search for shortest paths (good for maze/grid problems in interviews where Euclidean distance matters).
- **Bellman-Ford `💤 T3`**:
  > [!IMPORTANT]
  > **The Click Moment**: "Shortest path with **negative edge weights**" — OR — "detect **negative cycles**".
- **Floyd-Warshall `💤 T3`**:
  > [!IMPORTANT]
  > **The Click Moment**: "**All-pairs** shortest paths" — OR — "transitive closure of a graph".
- **Hierholzer's Algorithm**:
  > [!IMPORTANT]
  > **The Click Moment**: "Visit every **edge** exactly once" — OR — "reconstruct itinerary".




---

## 6. Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Critical Connections [H]** | Tarjan's Bridges | "Remove one edge, network splits" | DFS with `disc[]` and `low[]`; bridge when `low[v] > disc[u]` | Undirected graph — must not back-track through parent; multi-edges require tracking parent edge index, not node |
| **Reconstruct Itinerary [H]** | Hierholzer's (Eulerian Path) | "Use every ticket exactly once" | Sort adjacency lists; post-order DFS — add node to result only when no edges remain | Sort in reverse + `.pop()` for lexicographic order; result needs reversal at end |
| **[Alien Dictionary](problem-deep-dives.md#alien-dictionary) [H] `⚡ T1`** | Topological Sort (implicit graph) | "Derive character ordering from sorted word list" | Compare adjacent words char-by-char; first diff → directed edge; run Kahn's BFS | If word A is a prefix of word B and A comes after B in input → invalid (return `""`) |
| **Cheapest Flights Within K Stops [M]** | Bellman-Ford (bounded) | "Shortest path with at most K hops" | Run K+1 relaxation rounds; use snapshot of previous round to prevent cascading updates | Dijkstra fails here — greedily expanding cheapest node doesn't respect hop limit |
| **Network Delay Time [M]** | Dijkstra | "Min time for signal to reach all nodes" | Standard Dijkstra from source; answer is `max(dist.values())`; return -1 if any node unreachable | Unreachable nodes — check `len(dist) == n`, not just final max |
| **Path With Minimum Effort [M]** | Binary Search + BFS/DFS OR Dijkstra | "Minimize the maximum single-step difference" | Dijkstra where `dist[node]` = min effort to reach it; weight = `abs(h1 - h2)` | Binary search on answer + BFS also works; Dijkstra is cleaner and O((V+E) log V) |
| **Swim in Rising Water [H]** | Dijkstra OR Binary Search + BFS | "Minimize the maximum elevation traversed" | Dijkstra with `dist[i][j]` = max elevation seen on path to `(i,j)` | Looks like water-fill BFS but requires minimizing a max — standard BFS gives wrong answer |
| **Find the City With Smallest Reachable Count [M]** | Floyd-Warshall | "All-pairs shortest paths + count reachable under threshold" | Floyd-Warshall → for each city count neighbors with `dist ≤ threshold` | O(V³) acceptable for small N (≤ 100); prefer Floyd-Warshall for all-pairs over V×Dijkstra |
| **Minimum Cost to Reach Destination (Floyd-Warshall) [M]** | Floyd-Warshall | "All-pairs shortest path in dense small graph" | `dp[i][j] = min over k of dp[i][k] + dp[k][j]`; initialize diagonal to 0 | Initialization: `dp[i][j] = inf` unless direct edge exists; loop order must be `k` outermost |
| **Course Schedule II [M] `⚡ T1`** | Topological Sort (Kahn's) | "Find valid task ordering with dependencies" | In-degree array + BFS queue of zero-in-degree nodes | If result length < N → cycle exists; return empty array |
| **Minimum Spanning Tree — Kruskal's [M] `⚡ T1`** | Union-Find + sort edges | "Minimum cost to connect all nodes" | Sort edges by weight; union each edge if endpoints not yet connected | Greedy correctness relies on cycle property — adding next cheapest edge never violates optimality if no cycle formed |
| **Minimum Spanning Tree — Prim's [M] `⚡ T1`** | Min-Heap (greedy) | "MST from a source node outward" | Min-heap of `(weight, node)`; greedily add cheapest edge to a non-visited node | Better than Kruskal on dense graphs (O(E log V) vs O(E log E)); need visited set to avoid re-adding nodes |
| **Evaluate Division [M]** | Weighted graph + BFS/DFS | "Chain of ratio queries — can you go A→B?" | Build directed graph with edge weight = ratio; query = DFS/BFS product along path | If query nodes not in graph → return -1; same-node query (A/A) should return 1.0 unless A unknown |
| **Strongly Connected Components — Kosaraju's [H] `💤 T3`** | Two-pass DFS | "Find all groups where every node reaches every other" | Pass 1: DFS on original graph, push to stack by finish time; Pass 2: DFS on reversed graph in stack order | Two full DFS passes; Tarjan's SCC is single-pass but harder to implement — know both |
| **Word Ladder II [H] `⚡ T1`** | BFS (layered) + backtracking | "All shortest transformation sequences" | BFS to build `parent` map (layer by layer); backtrack from target to source to reconstruct paths | BFS must process entire layer before removing words from `wordSet` — removing mid-layer causes missed paths |
| **Detect Negative Cycle (Bellman-Ford) [M]** | Bellman-Ford | "Does a path get cheaper indefinitely?" | Run N-1 relaxation rounds; if Nth round still relaxes → negative cycle exists | Check `dist[v] > dist[u] + w` on the Nth iteration; Dijkstra cannot detect negative cycles at all |

---

## 7. DAG Shortest Path — Topological Relaxation

> [!IMPORTANT]
> **The Click Moment**: "Shortest path in a **directed acyclic graph**" — OR — "dependencies with weights, find min cost ordering" — OR — "longest path in DAG (negate weights)". Dijkstra is O((V+E) log V); DAG topological relaxation is **O(V+E)** with no heap.

**Why it works**: In a DAG, a topological ordering guarantees that when we process node `u`, all predecessors of `u` have already been finalized. Relaxing outgoing edges in topological order is therefore always safe — no predecessor can be updated later.

```python
from collections import defaultdict, deque

def dag_shortest_path(n: int, edges: list[tuple[int, int, int]], src: int) -> list[float]:
    graph = defaultdict(list)
    in_degree = [0] * n
    for u, v, w in edges:
        graph[u].append((v, w))
        in_degree[v] += 1

    # Kahn's BFS for topological order
    queue = deque(i for i in range(n) if in_degree[i] == 0)
    topo = []
    while queue:
        u = queue.popleft()
        topo.append(u)
        for v, _ in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    dist = [float('inf')] * n
    dist[src] = 0
    for u in topo:
        if dist[u] == float('inf'):
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist  # dist[i] = min cost from src to i; inf = unreachable
```

> [!TIP]
> **Longest path**: negate all weights before running. The "critical path" in project scheduling is longest-path on a DAG — identical algorithm.

**Complexity**: O(V + E) — topological sort is O(V + E); relaxation visits each edge once.

**Gotchas**:
- Only works on DAGs — use Dijkstra or Bellman-Ford for graphs with cycles.
- If multiple nodes have in-degree 0 at the start, the src node still initializes `dist[src] = 0`; other zero-in-degree nodes will have `dist = inf` and be skipped.
- Longest path in a general graph is NP-hard; on a DAG it's O(V + E).

---

## See also

- [Graph Fundamentals](../01-data-structures/graphs.md) — BFS, DFS, and Dijkstra  
- [SDE-3 Roadmap](roadmap.md) — advanced study plan  
- [Patterns Master](../../03-patterns/patterns-master.md)
