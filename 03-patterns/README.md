# Patterns — Index

Pattern recognition is the skill that separates L4 from L3. The goal: hear a problem, identify the pattern in under 60 seconds, and begin with the right structure.

---

## Core Resources

| Resource | What's in it |
|----------|-------------|
| [`patterns-master.md`](./patterns-master.md) | **Primary guide.** 60-second recognition triggers for all major patterns. Read this first. |
| [`02-algorithms/two-pointers.md`](../02-algorithms/two-pointers.md) | All three two-pointer variants with templates + 8 canonical problems |
| [`02-algorithms/sliding-window.md`](../02-algorithms/sliding-window.md) | Fixed + variable window, monotonic deque, 8 canonical problems |
| [`02-algorithms/binary-search.md`](../02-algorithms/binary-search.md) | Standard, rotated, BS-on-answer, 2D matrix, 10 canonical problems |
| [`dynamic-programming/`](../02-algorithms/dynamic-programming/) | DP paradigms: 1D, 2D, interval, knapsack |
| [`backtracking.md`](../02-algorithms/backtracking.md) | Backtracking template + pruning strategies |
| [`graph.md`](../02-algorithms/graph.md) | BFS, DFS, topological sort, shortest path |
| [`problem-deep-dives.md`](../02-algorithms/problem-deep-dives.md) | 100+ problems with pattern tags and key insights |

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
