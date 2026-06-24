---
module: 02-algorithms
topic: Advanced Graphs
subtopic: 
status: awareness-only
tags: [algorithms, advanced-graphs]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)

> [!warning] **Amazon SDE-2 scope: awareness only for SCC/bridges/Eulerian; DSU is SDE-2 core.**
> Tarjan SCC, Kosaraju, bridge-finding, and Eulerian path are SDE-3 / Google L5 topics. Know they exist and roughly how they work — do NOT drill implementations for Amazon SDE-2. DSU (union-find) and Dijkstra/Bellman-Ford/Floyd-Warshall are covered in [graph.md](./graph.md) and [union-find.md](./union-find.md).

## Awareness Map

| Algorithm | Problem it solves | One-sentence idea | Needed for SDE-2? |
|-----------|-------------------|-------------------|-------------------|
| Tarjan SCC | Find all strongly connected components in directed graph | DFS with `disc[]` and `low[]`; SCC root when `low[u]==disc[u]` | No — awareness only |
| Kosaraju SCC | Same as Tarjan | Two DFS passes: original graph + reversed graph | No — awareness only |
| Tarjan bridges | Find edges whose removal disconnects graph | Bridge when `low[v] > disc[u]` | No — awareness only |
| Articulation points | Find nodes whose removal disconnects graph | AP when `low[v] >= disc[u]` for child v | No — awareness only |
| Hierholzer's (Eulerian path) | Traverse every edge exactly once | Post-order DFS; append node only when all edges exhausted | SDE-2: Reconstruct Itinerary (LC 332) |
| DAG shortest path | Shortest path in directed acyclic graph, O(V+E) | Topological sort then relax in order — no heap needed | No — Dijkstra is sufficient for SDE-2 |

## Eulerian Path — One SDE-2 Problem That Appears

**Reconstruct Itinerary (LC 332)** — only interview-relevant Eulerian path problem at SDE-2 level.

Trigger: "Use every ticket/edge exactly once, return lexicographically smallest path."

```python
from collections import defaultdict

def find_itinerary(tickets):
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

Key insight: sort in reverse + `.pop()` gives lexicographic order. Post-order append + reverse gives correct path.

## DSU (Union-Find) — SDE-2 Core

DSU is fully covered in [union-find.md](./union-find.md). It IS in scope for Amazon SDE-2.

## SCC / Bridges — What to Say in an Interview

If asked: "Strongly connected components are found with Tarjan's (one DFS) or Kosaraju's (two DFS). Tarjan tracks discovery time and lowest reachable time. I know how these work conceptually but would implement BFS/DFS-based component detection for most interview problems."

## See Also

- [Graph Algorithms](./graph.md) — BFS, DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, topological sort
- [Union-Find](./union-find.md) — DSU with path compression and union by rank
