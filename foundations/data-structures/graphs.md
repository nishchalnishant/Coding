# Graphs — Interview Notes (Google SDE-2)

Graphs show up at Google primarily as:
- **Grid problems** (implicit graphs): islands, flood fill, rotten oranges
- **Dependencies**: course schedule (topological sort)
- **Shortest paths**: BFS (unweighted) and basic Dijkstra (non-negative weights)

This file focuses on the **SDE-2 essentials**: pick the right representation, choose BFS/DFS/topo, and implement correctly with clean state/visited handling.

If you want the algorithm-heavy deep dive (Dijkstra/Bellman-Ford/MST), also see: `../algorithms/graph.md`.

---

## 1) SDE-2 Must Know Checklist

You’re “ready enough” for an SDE-2 graph round if you can do these quickly:

- Model input as a graph (adjacency list or implicit grid neighbors).
- Implement **BFS** and **DFS** without visited bugs.
- Recognize **multi-source BFS** (enqueue all sources at distance 0).
- Recognize **topological sort** (dependencies) and detect cycles.
- State correct complexity: **O(V+E)** for traversals; space **O(V)**.

---

## 2) Representation

### Adjacency list (default)
- Space: `O(V+E)`
- Best for sparse graphs and interview problems.

Example (undirected):

```python
from collections import defaultdict

adj = defaultdict(list)
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)
```

### Grid as implicit graph
Neighbors from `(r,c)` are typically 4-dir:

```python
DIRS = [(1,0), (-1,0), (0,1), (0,-1)]
```

---

## 3) BFS / DFS templates

SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/graphs.py`.

### BFS (shortest path in unweighted graph)

```python
from collections import deque

def bfs(start):
    q = deque([start])
    dist = {start: 0}
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

### DFS (components, reachability)

```python
def dfs(u):
    stack = [u]
    seen = {u}
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen
```

---

## 4) Core patterns (what to reach for)

### A) Connected components (graph or grid)
- “How many groups/islands/components…”
- Use DFS/BFS, mark visited.

### B) Shortest path in unweighted graph
- “Minimum steps”, “minimum moves”, “shortest transformation”
- Use BFS. First time you pop/visit the target is optimal.

### C) Multi-source BFS
- “Spread”, “rot”, “distance to nearest X”, “fill”
- Put **all sources** in queue at distance 0.

### D) Topological sort (dependencies)
- “Must take A before B”, “order tasks”
- Use Kahn (in-degree queue) or DFS coloring; cycle ⇒ impossible.

### E) Dijkstra (only if weights and non-negative)
- If edges have costs/time and you need minimum sum cost.
- If weights are 0/1, consider **0–1 BFS** (deque) as a follow-up.

---

## 5) Topological sort (Kahn’s algorithm)

```python
from collections import deque, defaultdict

def topo_kahn(n, edges):
    adj = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:          # u -> v
        adj[u].append(v)
        indeg[v] += 1

    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    return order if len(order) == n else []   # empty => cycle
```

Key interview points:
- Time `O(V+E)`.
- If you can’t process all nodes, there’s a **cycle**.

---

## 6) Common SDE-2 problems

### Easy/Medium (high frequency)
- Number of Islands (grid DFS/BFS)
- Flood Fill
- Rotting Oranges (multi-source BFS)
- Course Schedule / Course Schedule II (topo + cycle)
- Clone Graph (graph traversal + map)
- Surrounded Regions (border flood fill)

### Hard/Stretch (still common at Google)
- Word Ladder (BFS; bidirectional BFS follow-up)
- Alien Dictionary (topo; prefix invalid case)
- Evaluate Division (graph with weights; DFS/BFS)

---

## 7) Interview Strategy (Google-style)

- Start by asking: directed/undirected? weighted? size limits? grid neighbors 4 or 8?
- Say the pattern name: “This is a multi-source BFS” / “This is topo sort”.
- Define the invariant: “Once a node is visited, we never need to revisit it in BFS for unweighted shortest path.”
- Test two cases: a normal case + a “disconnected / unreachable” case.

---

## 8) Quick Revision

- Traversal complexity: **O(V+E)**.
- Grid BFS/DFS: each cell visited once ⇒ **O(R·C)**.
- Multi-source BFS: enqueue all sources, then standard BFS levels.
- Topo: cycle if processed nodes < total nodes.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **Number of Islands** | DFS/BFS flood-fill from each unvisited `1`; count components. | **4 vs 8** neighbors; recursion depth on large grid—use stack/queue. |
| **Flood Fill** | BFS/DFS recolor connected component starting at `(sr,sc)` with original color. | Don’t loop if `newColor == oldColor`. |
| **Rotting Oranges** | Multi-source BFS from all rotten; minutes = BFS levels; track fresh count. | If fresh remain unreachable → `-1`. |
| **Course Schedule** | Build directed edges “prereq → course”; topo; cycle means impossible. | Edge direction is the #1 bug: `a,b` means **b before a**. |
| **Clone Graph** | DFS/BFS with map `old → clone`; connect neighbors using the map. | Cycles require you to create clone before traversing neighbors. |
| **Surrounded Regions** | Flood from border `O` to mark safe; flip remaining `O` to `X`. | Don’t BFS from every interior `O`—too slow. |
| **Word Ladder** | BFS; neighbors are one-letter edits in set; first reach end is shortest. | Bidirectional BFS follow-up; remove visited words early. |
| **Alien Dictionary** | Build edges from first mismatch in adjacent words; topo all letters. | Prefix invalid: `"abc"` before `"ab"` is impossible. |

---

## See also

- Graph algorithms deep dive: `../algorithms/graph.md`
- Union-Find (connectivity / Kruskal): `../algorithms/union-find.md`
- Patterns: `../../patterns/leetcode-patterns.md`
