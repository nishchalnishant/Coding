## First-Principles Map

```text
WHY pattern recognition is the core interview skill
├── Novel problems are rare; novel disguises of known patterns are everywhere
│   ├── "Trapping Rain Water"  ≡ two-pointer scan with running max
│   ├── "Sliding Window Max"   ≡ monotonic deque pattern
│   └── "Word Ladder"          ≡ BFS on implicit graph of word states
├── Recognizing pattern in <60s → correct complexity from the start
├── Missing pattern → brute force → TLE → failed interview
└── Pattern fluency = the delta between L3 and L4 performance
│
WHAT the pattern taxonomy is
├── Two Pointers      — opposite ends or same-direction; sorted arrays, linked lists
├── Sliding Window    — fixed or variable window; max sum, longest substring
├── BFS / DFS         — level-order / exhaustive traversal; graphs, trees, matrices
├── DP                — memoized recursion or bottom-up table; count / optimize
├── Greedy            — sort + scan with local decision; intervals, scheduling
├── Backtracking      — DFS + undo; all valid combos, permutations, constraint sat
├── Heap              — maintain top-k or running extremum; two-heap for median
├── Binary Search     — on sorted array or on answer space (feasibility function)
├── Union-Find        — dynamic connectivity; components, Kruskal, redundancy
├── Monotonic Stack   — next greater/smaller element, histogram, temperatures
└── Prefix Sum / Hash — O(1) range sum; subarray sum = k, balance arrays
│
HOW to recognize the pattern in <60 seconds
├── Signal words → pattern
│   ├── "Subarray / substring"                → Sliding window or prefix sum
│   ├── "k-th largest / smallest"             → Heap or quickselect
│   ├── "All permutations / combinations"     → Backtracking
│   ├── "Shortest path"                       → BFS (unweighted) / Dijkstra (weighted)
│   ├── "Count ways / min cost"               → DP
│   ├── "Sorted + two values summing"         → Two pointers
│   ├── "Next greater element"                → Monotonic stack
│   ├── "Connected components / union"        → Union-Find or BFS/DFS
│   └── "Search in sorted / minimize max"     → Binary search on answer
├── Constraint signals → pattern
│   ├── n ≤ 20        → Backtracking / bitmask DP
│   ├── n ≤ 1000      → O(n²) DP or brute force with pruning
│   ├── n ≤ 10^5      → O(n log n) — sort, heap, segment tree, binary search
│   └── n ≤ 10^6      → O(n) — two pointers, sliding window, prefix sum
│
WHEN each pattern applies
├── Two Pointers   — pair/triplet sum, palindrome check, remove duplicates
├── Sliding Window — longest substring without repeat, max sum subarray of size k
├── BFS            — word ladder, 0-1 matrix, rotten oranges, min depth
├── DFS            — number of islands, path sum, clone graph
├── DP             — coin change, LCS, edit distance, house robber, knapsack
├── Greedy         — jump game, meeting rooms, task scheduler, gas station
├── Backtracking   — N-queens, subsets, letter combos, Sudoku solver
├── Heap           — merge k lists, top k frequent, median finder
├── Binary Search  — search rotated array, koko eating bananas, capacity to ship
├── Union-Find     — number of provinces, redundant connection, accounts merge
└── Monotonic Stack— daily temperatures, largest rectangle in histogram, stock span
│
WHAT CAN GO WRONG
├── Forcing sliding window on non-contiguous subproblem → wrong answer
├── Using DFS where BFS needed for shortest path         → wrong answer (not guaranteed shortest)
├── Greedy without verifying exchange argument           → fails on edge cases
├── Backtracking without pruning on large input          → TLE
├── DP with wrong state definition                       → wrong transitions, wrong answer
└── Missing key constraint (e.g. "sorted" → two pointers valid) → O(n²) instead of O(n)
│
DECISION — signal → pattern (60-second checklist)
├── Contiguous subarray/string    → Sliding window / prefix sum
├── Sorted + two targets          → Two pointers
├── Shortest unweighted path      → BFS
├── Count/optimize over choices   → DP
├── All valid arrangements        → Backtracking
├── Running min/max / top-k       → Heap
├── Search sorted / minimize max  → Binary search
├── Component / connectivity      → Union-Find / BFS/DFS
└── Next greater/smaller          → Monotonic stack
```

## First-Principles Breakdown

- **Root problem:** Interviews test pattern recognition, not creative problem-solving from scratch; every problem is a known template with a problem-specific twist applied on top.
- **Core insight:** Signal words and constraint sizes together uniquely narrow the pattern space — recognizing both reduces candidate patterns from ~15 to 1-2 in under 60 seconds.
- **Invariant:** The correct pattern is always determined by the problem's structural property (contiguity, ordering, connectivity, optimization) — not by the domain (trees, graphs, strings are surface).
- **Why it works:** Each pattern is a proven algorithmic shape that matches exactly one class of structural property; once matched, the template provides a correct starting frame and known complexity.
- **Where it breaks:** Forcing a mismatched pattern (DFS for shortest path, greedy without exchange property) produces either wrong answers or wrong complexity, neither fixable without restarting.

# Patterns — Index

> [!note] L3 Reference Document
> This file is a **reference / meta document** — read it once, then use it as a lookup.
> It is NOT a coding practice file. Do not deep-study it like a topic file.


Pattern recognition is the skill that separates L4 from L3. The goal: hear a problem, identify the pattern in under 60 seconds, and begin with the right structure.

---

## Core Resources

| Resource | What's in it |
|----------|-------------|
| [`patterns-master.md`](./patterns-master.md) | **Primary guide.** 60-second recognition triggers for all major patterns. Read this first. |
| [`02-algorithms/two-pointers.md`](../02-algorithms/03-two-pointers.md) | All three two-pointer variants with templates + 8 canonical problems |
| [`02-algorithms/sliding-window.md`](../02-algorithms/04-sliding-window.md) | Fixed + variable window, monotonic deque, 8 canonical problems |
| [`02-algorithms/binary-search.md`](../02-algorithms/11-binary-search.md) | Standard, rotated, BS-on-answer, 2D matrix, 10 canonical problems |
| [`dynamic-programming/`](../02-algorithms/dynamic-programming/) | DP paradigms: 1D, 2D, interval, knapsack |
| [`12-backtracking.md`](../02-algorithms/12-backtracking.md) | Backtracking template + pruning strategies |
| [`13-graph.md`](../02-algorithms/13-graph.md) | BFS, DFS, topological sort, shortest path |
| [`20-problem-deep-dives.md`](../02-algorithms/20-problem-deep-dives.md) | 100+ problems with pattern tags and key insights |

---

## Pattern → Topic Cross-Reference

| Pattern | When triggered | Primary file |
|---------|---------------|-------------|
| **Two Pointers (Converging)** | Sorted array, pair/triplet sum, palindrome, water container | `02-algorithms/two-pointers.md` |
| **Two Pointers (Fast/Slow)** | Cycle detection, linked list middle, duplicate in array | `02-algorithms/two-pointers.md` |
| **Sliding Window (Fixed)** | Max/min/avg of every K-window, anagram check | `02-algorithms/sliding-window.md` |
| **Sliding Window (Variable)** | Longest/shortest subarray with constraint | `02-algorithms/sliding-window.md` |
| **Binary Search (Exact)** | "Find in sorted", "is X in the array" | `02-algorithms/binary-search.md` |
| **Binary Search (Bounds)** | First/last occurrence, insertion point | `02-algorithms/binary-search.md` |
| **Binary Search on Answer** | Minimize max, maximize min, "can we do X in Y" | `02-algorithms/binary-search.md` |
| **BFS** | Shortest path (unweighted), level-order, connected components, multi-source flood | `02-algorithms/graph.md` |
| **DFS** | Path existence, all paths, islands, cycle detection, backtracking | `02-algorithms/graph.md` |
| **Topological Sort** | Dependencies, build order, alien dictionary | `02-algorithms/graph.md` |
| **Dynamic Programming (1D)** | Linear recurrence — house robber, climb stairs, coin change | `02-algorithms/dynamic-programming/` |
| **Dynamic Programming (2D)** | Grid paths, edit distance, LCS, matrix chain | `02-algorithms/dynamic-programming/` |
| **Knapsack** | "Pick items with weight/value constraints" | `02-algorithms/dynamic-programming/` |
| **Interval DP** | Burst balloons, stone merge, optimal BST | `02-algorithms/dynamic-programming/` |
| **Greedy** | Interval scheduling, jump game, task scheduler | `02-algorithms/greedy.md` |
| **Backtracking** | Permutations, combinations, subsets, N-Queens, Sudoku | `02-algorithms/backtracking.md` |
| **Monotonic Stack** | Next greater/smaller element, histogram, trapped water | `01-data-structures/stack.md` |
| **Monotonic Deque** | Sliding window max/min | `02-algorithms/sliding-window.md` |
| **Union-Find** | Connected components, cycle in undirected, MST (Kruskal) | `02-algorithms/union-find.md` |
| **Heap / Priority Queue** | Top-K, merge K sorted, Dijkstra, two-heap median | `01-data-structures/heap.md` |
| **Trie** | Prefix matching, word search, autocomplete, XOR max | `01-data-structures/trie.md` |
| **Prefix Sum** | Subarray sum queries, range sum, 2D prefix sum | `01-data-structures/array.md` |
| **Divide & Conquer** | Merge sort, quick select, closest pair | `02-algorithms/divide-and-conquer.md` |
| **Bit Manipulation** | XOR tricks, power of 2, single number, subset enumeration | `02-algorithms/bit-manipulation.md` |

---

## 60-Second Pattern Recognition Checklist

When you hear a problem, ask these in order:

1. **Input sorted?** → Binary search candidate
2. **Subarray / substring, find longest/shortest/sum?** → Sliding window
3. **Pair/triplet sum, palindrome, sorted partitioning?** → Two pointers
4. **Graph / grid / connectivity?** → BFS (shortest) or DFS (paths/islands)
5. **Ordering with dependencies?** → Topological sort
6. **Best way to do X across all possibilities?** → DP (check: overlapping subproblems?)
7. **All valid combinations / permutations?** → Backtracking
8. **Top K, Kth largest/smallest, median stream?** → Heap
9. **Prefix/range query?** → Prefix sum or Segment tree
10. **Dynamic connectivity?** → Union-Find
