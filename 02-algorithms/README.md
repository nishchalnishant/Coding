# Algorithms — Index

All algorithm files live in `02-algorithms/`. This file is the navigation index.

---

## Topic Table

| Topic | When to Use | Must-Nail L4? | File |
|-------|------------|---------------|------|
| **Binary Search** | Sorted input, monotone predicate, "minimize max / maximize min" | YES | [`02-algorithms/binary-search.md`](./binary-search.md) |
| **Two Pointers** | Sorted array, pair/triplet sum, palindrome, partition | YES | [`02-algorithms/two-pointers.md`](./two-pointers.md) |
| **Sliding Window** | Contiguous subarray/substring, longest/shortest with constraint | YES | [`02-algorithms/sliding-window.md`](./sliding-window.md) |
| **Sorting** | Need ordered data; know when to use which sort | YES | [`sorting.md`](./sorting.md) |
| **Recursion & Backtracking** | Explore all possibilities, permutations, subsets, constraint satisfaction | YES | [`backtracking.md`](./backtracking.md), [`recursion/`](./recursion/) |
| **Dynamic Programming** | Overlapping subproblems + optimal substructure; memoization/tabulation | YES | [`dynamic-programming/`](./dynamic-programming/) |
| **Greedy** | Local optimum → global optimum; interval scheduling, activity selection | HIGH | [`greedy.md`](./greedy.md) |
| **Graph Algorithms** | BFS/DFS, shortest path, topological sort, cycle detection | YES | [`graph.md`](./graph.md), [`advanced-graphs.md`](./advanced-graphs.md) |
| **Searching** | Binary search variants, search in matrix | YES | [`searching.md`](./searching.md) |
| **Union-Find** | Dynamic connectivity, MST (Kruskal), cycle detection in undirected graphs | HIGH | [`union-find.md`](./union-find.md) |
| **Divide & Conquer** | Merge sort, quick select, closest pair | HIGH | [`divide-and-conquer.md`](./divide-and-conquer.md) |
| **String Algorithms** | Pattern matching (KMP, Rabin-Karp), palindromes, anagrams | HIGH | [`string.md`](./string.md) |
| **Bit Manipulation** | XOR tricks, power of 2, subset enumeration, single number | MEDIUM | [`bit-manipulation.md`](./bit-manipulation.md) |
| **Math** | GCD, primes, modular arithmetic, combinatorics | MEDIUM | [`maths.md`](./maths.md) |
| **System Design Algorithms** | Consistent hashing, HyperLogLog, Bloom filters | GOOD-TO-HAVE | [`system-design-algorithms.md`](./system-design-algorithms.md) |

---

## Must-Nail for L4 vs Good-to-Have

### Must-Nail (appear in almost every Google loop)
- **Binary Search** — including BS on answer (not just sorted array)
- **Two Pointers** — all three variants
- **Sliding Window** — both fixed and variable
- **DFS/BFS** — on trees AND graphs, iterative and recursive
- **Dynamic Programming** — 1D, 2D, interval, knapsack paradigms
- **Backtracking** — permutations, combinations, subsets, N-Queens pattern
- **Heap** — `heapq` API, top-K, two-heap median trick
- **Hash Map** — frequency counting, grouping, O(1) lookup patterns

### High Priority (appear in ~50% of loops)
- Topological Sort (Kahn's + DFS)
- Greedy (intervals, scheduling)
- Union-Find (connectivity)
- Divide & Conquer (merge sort, quick select)
- Monotonic Stack/Queue

### Good-to-Have (differentiator, not blocker)
- KMP / Rabin-Karp
- Bellman-Ford / Floyd-Warshall
- Segment Tree / Fenwick Tree
- Bit manipulation tricks
- Math (modular arithmetic, combinatorics)

---

## Algorithm Selection by Problem Signal

| Problem signal | Start with |
|---------------|-----------|
| "Subarray / substring with condition" | Sliding Window |
| "Sorted array, find pair/triplet" | Two Pointers |
| "Find in sorted / minimize-max" | Binary Search |
| "All combinations / permutations" | Backtracking |
| "Optimal substructure, overlapping" | DP |
| "Shortest path in unweighted graph" | BFS |
| "Shortest path in weighted graph" | Dijkstra |
| "Detect cycle / connected components" | Union-Find or DFS |
| "Top K / Kth largest" | Heap (min-heap of size K) |
| "Dependency ordering" | Topological Sort |
| "Prefix / range query" | Prefix Sum or Segment Tree |
