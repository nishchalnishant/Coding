---
tags: [l3-google, meta, complexity]
topic: Complexity Cheatsheet
---

# Complexity Cheatsheet — Google L3

Quick Big-O reference for whiteboard interviews. Pair with [`00-L3-EXECUTION-META/02-constraint-analysis-heuristic.md`](../00-L3-EXECUTION-META/02-constraint-analysis-heuristic.md). Theory (amortized analysis, recurrences, Master theorem): [`00-L3-EXECUTION-META/05-complexity-analysis.md`](../00-L3-EXECUTION-META/05-complexity-analysis.md).

## Constraint → expected complexity

| n (or input size) | Target complexity |
| :--- | :--- |
| n ≤ 20 | O(2^n) backtracking OK |
| n ≤ 200 | O(n³) sometimes OK |
| n ≤ 3,000 | O(n²) |
| n ≤ 10⁵ | O(n log n) |
| n ≤ 10⁶ | O(n) or O(n log n) |

## Data structures

| Structure | Insert | Search | Delete | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Array | O(1) tail | O(n) | O(n) | Random access O(1) |
| Hash map | O(1)* | O(1)* | O(1)* | *amortized average |
| Stack / Queue | O(1) | — | O(1) | |
| Linked list | O(1) head | O(n) | O(n) | |
| Binary heap | O(log n) | O(1) peek | O(log n) | |
| BST (balanced) | O(log n) | O(log n) | O(log n) | |
| Trie | O(L) | O(L) | O(L) | L = key length |

## Algorithms

| Pattern | Time | Space | When |
| :--- | :--- | :--- | :--- |
| Two pointers | O(n) | O(1) | Sorted array, opposite ends |
| Sliding window | O(n) | O(1)–O(k) | Contiguous subarray/substring |
| Binary search | O(log n) | O(1) | Sorted or monotonic feasibility |
| Sort + scan | O(n log n) | O(1)–O(n) | Intervals, greedy prep |
| BFS / DFS | O(V+E) | O(V) | Graphs, grids |
| Dijkstra | O((V+E) log V) | O(V) | Non-negative weights |
| Topological sort | O(V+E) | O(V) | DAG dependencies |
| Union-Find | O(α(n)) per op | O(n) | Dynamic connectivity |
| 1D DP | O(n) | O(n) → O(1) | Linear recurrence |
| 2D DP | O(n·m) | O(n·m) → O(m) | Grid, LCS, edit distance |
| Backtracking | O(k^n) worst | O(n) stack | Generate all valid configs |

## Common interview mistakes

- Nested loop on n=10⁵ → O(n²) TLE
- BFS on weighted graph → wrong; use Dijkstra
- Greedy on coin change (arbitrary denominations) → wrong; use DP
- Forgetting `seen[0]=1` in prefix-sum counting
- Marking graph nodes visited **after** enqueue (BFS duplicates)

## Python gotchas (whiteboard)

```python
# Shallow copy
copy = arr[:]          # new list
alias = arr            # same reference

# Default dict
from collections import defaultdict, deque

# Heap: min-heap by default
import heapq
heapq.heappush(h, val)
heapq.heappop(h)

# Sort with key
sorted(items, key=lambda x: x[1])
```

More syntax: [`00-L3-EXECUTION-META/03-python-whiteboarding-cheatsheet.md`](../00-L3-EXECUTION-META/03-python-whiteboarding-cheatsheet.md)
