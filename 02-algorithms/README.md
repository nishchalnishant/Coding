## First-Principles Map

```text
WHY algorithm families matter
├── Problems recur across domains in disguised forms
│   ├── "Find shortest path in graph" ≡ "Minimum cost to convert word" ≡ BFS/Dijkstra
│   ├── "Count valid arrangements"    ≡ "Number of ways to tile"        ≡ DP / backtracking
│   └── "Merge k sorted streams"      ≡ "K-th smallest in matrix"       ≡ Heap / binary search
├── Recognizing the family → skip brute-force → apply known template
└── Wrong family → exponential where polynomial exists (backtracking vs DP)
│
WHAT the major algorithm families are
├── Search         — binary search (sorted input), BFS (shortest unweighted), Dijkstra (weighted)
├── Sort           — comparisons O(n log n); counting/radix O(n+k); sort-then-scan pattern
├── Two Pointers   — O(n) scan replacing O(n²) nested loops; sorted array or linked list
├── Sliding Window — O(n) variable/fixed window; substring, subarray problems
├── Dynamic Prog.  — overlapping subproblems + optimal substructure; memoize or tabulate
├── Greedy         — locally optimal choice → globally optimal; must prove exchange argument
├── Backtracking   — all possibilities with pruning; permutations, combinations, Sudoku
├── Graph          — BFS/DFS/Topo/SCC/MST/Shortest path; any connectivity / dependency problem
├── Divide&Conquer — split → solve → merge; merge sort, closest pair, matrix multiply
└── Union-Find     — O(α) connectivity queries; dynamic graph, Kruskal, redundant connections
│
HOW to map problem signals to families
├── "Sorted array / search for value"         → Binary search
├── "Optimize over choices, overlapping"      → DP (top-down or bottom-up)
├── "Find all valid combos / arrangements"    → Backtracking (+ pruning)
├── "Minimum spanning / shortest path"        → Greedy (Kruskal/Prim) / Dijkstra
├── "Connected components / cycle detection"  → BFS/DFS / Union-Find
├── "Ordering with dependencies"              → Topological sort (Kahn's / DFS)
├── "Contiguous subarray / substring"         → Sliding window / prefix sum
├── "Two elements summing to target"          → Two pointers (sorted) / hash map
└── "Max/min across window"                   → Monotonic deque / segment tree
│
WHEN each family applies
├── Binary search  — sorted structure, answer-space search (bisect on feasibility)
├── DP             — counting ways, min cost, longest sequence, boolean reachability
├── Greedy         — interval scheduling, Huffman, activity selection, gas station
├── Backtracking   — N-queens, word search, generate parentheses, subsets
├── Graph BFS      — shortest unweighted path, multi-source spread, 0-1 BFS
├── Topo sort      — course schedule, build order, alien dictionary
├── Union-Find     — dynamic connectivity, Kruskal's MST, account merge
└── Divide&Conquer — merge sort, inversion count, Karatsuba, closest pair
│
WHAT CAN GO WRONG
├── DP when greedy suffices          → O(n²) where O(n log n) works (e.g. activity selection)
├── Backtracking when DP needed      → exponential where polynomial exists (e.g. edit distance)
├── BFS for weighted shortest path   → wrong answer; use Dijkstra
├── Greedy without exchange proof    → fails on counterexample (e.g. coin change with odd coins)
├── Missing memoization in recursion → O(2^n) instead of O(n²) or O(n)
└── Wrong family = wrong complexity class; algorithm tricks can't save a fundamentally wrong approach
│
DECISION — problem signal → algorithm family
├── Sorted input + find value          → Binary search
├── Optimize, overlapping subproblems  → DP
├── All possibilities needed           → Backtracking
├── Local choice → global optimum      → Greedy (verify exchange argument)
├── Connectivity / path / cycle        → Graph (BFS/DFS/Dijkstra/Topo)
├── Dynamic connectivity               → Union-Find
├── Contiguous subarray / substring    → Sliding window / two pointers
└── Divide large into halves           → Divide & Conquer
```

## First-Principles Breakdown

- **Root problem:** Problems across domains share hidden structural similarities; recognizing the family eliminates the need to solve from scratch under pressure.
- **Core insight:** Each algorithm family exploits one structural property — monotonicity (binary search), optimal substructure (DP), greedy exchange (greedy), adjacency (graph) — and is useless without it.
- **Invariant:** The dominant constraint in the problem (sorted, overlapping, connected, all-possibilities) uniquely identifies the algorithm family before any code is written.
- **Why it works:** Templates encode decades of proven solutions; applying the right template guarantees correctness and known complexity, while adaptation handles the problem-specific twist.
- **Where it breaks:** Forcing the wrong family (backtracking on a DP problem, greedy on a non-exchange problem) produces exponential or incorrect solutions that no micro-optimization can fix.

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
| **SQL** | Window functions, JOINs, CTEs, aggregation patterns | HIGH | [`sql.md`](./sql.md) |

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
- SQL (window functions, JOINs, CTEs — common in data/analytics rounds)
- System Design Algorithms (Bloom filter, Consistent Hashing, Raft — SDE-3 signal)

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
| "Top N per group / running total / MoM growth" | SQL window function |
| "Add/remove servers without data reshuffle" | Consistent Hashing |
| "Unique count at scale" | HyperLogLog |
| "Membership check, avoid DB hit" | Bloom Filter |
