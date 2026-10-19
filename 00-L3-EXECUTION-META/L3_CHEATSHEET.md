# Google L3 Execution & Meta Cheatsheet

## What this covers

> [!abstract] In this file
> **Covers:** Round execution: the 45-minute plan, constraint → Big-O table, decision keywords, Python essentials, universal edge cases, Big-O reference, what to skip at L3.
> **You'll be able to:** Run every round on the same clock and pick the target complexity from N.
> **Prereqs:** None · **Pair with:** [Interview judgment](../03-patterns/INTERVIEW_JUDGMENT.md) · [L3 roadmap](../coding/l3-google-roadmap.md) · **Time:** 20 min (reread before every mock)

**Sections:** [1. 45-Minute Execution Plan](#1-45-minute-execution-plan) · [2. Constraint Analysis (N=10^5 → O(N) or O(N log N))](#2-constraint-analysis-n105--on-or-on-log-n) · [3. Decision Guide & Keywords](#3-decision-guide--keywords) · [4. Python Whiteboarding Essentials](#4-python-whiteboarding-essentials) · [5. Universal Edge Cases](#5-universal-edge-cases) · [6. Big-O Reference](#6-big-o-reference) · [7. Complexity Gotchas](#7-complexity-gotchas) · [8. What to Skip at L3](#8-what-to-skip-at-l3)

---

## 1. 45-Minute Execution Plan
- **Min 0-5 (Clarify & De-risk):** Listen, repeat, clarify edge cases (empty, negative, cycles, memory), write a custom tricky example.
- **Min 5-15 (Design):** State brute force, reverse-engineer constraints, pitch optimal solution (draw it out). Get green light before coding.
- **Min 15-35 (Code):** Write clean, modular, bug-free code. Stop talking to focus. Use helper functions.
- **Min 35-45 (Dry Run & Big-O):** Trace code line-by-line with custom example. State Time/Space complexity. Fix bugs gracefully.

## 2. Constraint Analysis (N=10^5 → O(N) or O(N log N))
| N limit | Target Big-O | Algorithm Family |
|---|---|---|
| ≤ 10 | O(N!) | Permutations, exhaustive search |
| ≤ 20 | O(2^N) | Backtracking, subsets, bitmask DP |
| ≤ 500 | O(N^3) | 3D DP, interval DP, Floyd-Warshall |
| ≤ 2,000 | O(N^2) | 2D DP, nested loops, matrix paths |
| 10^5 | O(N log N) | Sorting, Binary Search, Heaps |
| 10^5 - 10^6 | O(N) | Sliding Window, Two Pointers, Hash Maps |
| 10^9+ | O(log N) or O(1) | Binary Search on Answer, Math |

## 3. Decision Guide & Keywords
- **Array/String:**
  - Pair/target sum → HashMap
  - Subarray sum = K → Prefix Sum + HashMap
  - Longest/shortest substring → Sliding Window
  - Max in window K → Monotonic Deque
  - Next greater element → Monotonic Stack
  - Sorted array target → Binary Search
- **Grid/Graph:**
  - Shortest path (unweighted) → BFS
  - Shortest path (weighted) → Dijkstra
  - Connected components / Islands → BFS/DFS or Union-Find
  - Prerequisites / dependencies → Topological Sort (Kahn's)
- **Trees/Lists:**
  - Level-by-level → BFS
  - Cycle detection → Fast/Slow pointers
  - K sorted lists → Min-Heap
- **DP/Optimization:**
  - Min/Max target (overlapping) → DP
  - All combinations → Backtracking
  - Interval scheduling → Greedy (sort by end)
  - Top K / dynamic extremum → Heap

## 4. Python Whiteboarding Essentials
- **Heaps:** `import heapq` (min-heap default). Multiply by -1 for max-heap. `heapify(arr)`, `heappush(arr, x)`, `heappop(arr)`.
- **Queues:** `from collections import deque`. `q.append()`, `q.appendleft()`, `q.popleft()`, `q.pop()`. (Never `list.pop(0)`!)
- **Maps/Sets:** `from collections import defaultdict, Counter`.
- **Sorting:** `arr.sort(key=lambda x: (x[1], x[0]))`.
- **Binary Search:** `import bisect`. `bisect_left(arr, x)`, `bisect_right(arr, x)`.

## 5. Universal Edge Cases
- **General:** Empty input, single element, all identical, negative values, integer max bounds.
- **Array:** Already sorted, reverse sorted, duplicates.
- **String:** Case sensitivity, whitespace, special chars.
- **Linked List:** `None` head, single node, cycles, even/odd lengths.
- **Trees:** Skewed tree (O(n) height), `None` root, disconnected graphs, graph with cycles.
- **Binary Search:** Off-by-one bounds (`lo <= hi`), infinite loops (`mid = (lo+hi)//2`).

## 6. Big-O Reference

### Data structures

| Structure | Insert | Search | Delete | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Array | O(1) tail | O(n) | O(n) | Random access O(1) |
| Hash map | O(1)* | O(1)* | O(1)* | *amortized average |
| Stack / Queue | O(1) | — | O(1) | |
| Linked list | O(1) head | O(n) | O(n) | |
| Binary heap | O(log n) | O(1) peek | O(log n) | |
| BST (balanced) | O(log n) | O(log n) | O(log n) | |
| Trie | O(L) | O(L) | O(L) | L = key length |

### Algorithm patterns

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

### Common complexity mistakes

- Nested loop on n=10⁵ → O(n²) TLE
- BFS on weighted graph → wrong; use Dijkstra
- Greedy on coin change (arbitrary denominations) → wrong; use DP
- Forgetting `seen[0]=1` in prefix-sum counting
- Marking graph nodes visited **after** enqueue (BFS duplicates)

## 7. Complexity Gotchas
- **Amortized O(1):** Hash map insertions, Python `list.append()`.
- **Space:** Recursion depth uses stack space! DFS on skewed tree is O(N) space.
- **String Concat:** `s += c` in a loop is O(N^2). Use `"".join(list)` for O(N).
- **Master Theorem:** Recognize when halving vs subtracting changes complexity.

## 8. What to Skip at L3
- **Do NOT study:** Segment Trees, Fenwick Trees (BIT), Tarjan/Kosaraju SCC, Floyd-Warshall, Bitmask/Digit DP, System Design. (Focus heavily on BFS/DFS, Heaps, Two Pointers, Binary Search instead).
