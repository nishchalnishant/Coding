---
tags: [l3-google, reference, required]
topic: Complexity Cheatsheet
---

# Complexity Cheatsheet — L3

State time and space complexity at the end of every round.

| Pattern | Time | Space |
| :--- | :--- | :--- |
| BFS / DFS on graph | O(V + E) | O(V) |
| Dijkstra (min-heap) | O((V + E) log V) | O(V) |
| Binary search | O(log N) | O(1) |
| Sliding window / two pointers | O(N) | O(1)–O(K) |
| Sort | O(N log N) | O(1)–O(N) |
| Hash map ops (avg) | O(1) | O(N) |
| Heap push/pop | O(log N) | O(N) |
| 0/1 Knapsack DP | O(N × W) | O(W) |
| LCS / Edit Distance | O(M × N) | O(N) with 1 row |

Full constraint heuristics (if N = 10⁵ → need O(N) or O(N log N)): [`00-L3-EXECUTION-META/02-constraint-analysis-heuristic.md`](../00-L3-EXECUTION-META/02-constraint-analysis-heuristic.md)
