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
| [`HOW_TO_THINK.md`](./HOW_TO_THINK.md) | First-principles derivation of every pattern — build intuition instead of memorizing |
| [`RECURSION_AND_DP_MASTERCLASS.md`](./RECURSION_AND_DP_MASTERCLASS.md) | Teacher-voice course: recursion → memoization → bottom-up DP |
| [`INTERVIEW_JUDGMENT.md`](./INTERVIEW_JUDGMENT.md) | Live-interview decisions: correctness arguments, pivoting, using hints, recovery |
| [`PATTERN_LADDERS.md`](./PATTERN_LADDERS.md) | Problem ladders per pattern — learn by deriving each rung from the last |
| [`TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md`](./TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md) | Question bank: per-topic canonical problems with core logic + trickiness |
| [`GOOGLE_INTERVIEW_REVISION.md`](./GOOGLE_INTERVIEW_REVISION.md) | Final revision: complexity sound bites, topic capsules, day-before schedule |
| [`MOCK_INTERVIEW_SET.md`](./MOCK_INTERVIEW_SET.md) | 25 timed mock problems with rubric |
| [`leetcode-variants.md`](./leetcode-variants.md) | Narrative walkthroughs of follow-up/variant questions |
| [`02-algorithms/03-two-pointers.md`](../02-algorithms/03-two-pointers.md) | All three two-pointer variants with templates + 8 canonical problems |
| [`02-algorithms/04-sliding-window.md`](../02-algorithms/04-sliding-window.md) | Fixed + variable window, monotonic deque, 8 canonical problems |
| [`02-algorithms/11-binary-search.md`](../02-algorithms/11-binary-search.md) | Standard, rotated, BS-on-answer, 2D matrix, 10 canonical problems |
| [`15-dynamic-programming.md`](../02-algorithms/15-dynamic-programming.md) | DP paradigms: 1D, 2D, grid, knapsack, LCS |
| [`12-backtracking.md`](../02-algorithms/12-backtracking.md) | Backtracking template + pruning strategies |
| [`13-graph.md`](../01-data-structures/13-graphs.md) | BFS, DFS, topological sort, shortest path |
| [`MINDMAP.md`](../MINDMAP.md) | T1/T2 problem index with one-line hints (`coding/`) |

---

## Pattern → Topic Cross-Reference

| Pattern | When triggered | Primary file |
|---------|---------------|-------------|
| **Two Pointers (Converging)** | Sorted array, pair/triplet sum, palindrome, water container | `02-algorithms/03-two-pointers.md` |
| **Two Pointers (Fast/Slow)** | Cycle detection, linked list middle, duplicate in array | `02-algorithms/03-two-pointers.md` |
| **Sliding Window (Fixed)** | Max/min/avg of every K-window, anagram check | `02-algorithms/04-sliding-window.md` |
| **Sliding Window (Variable)** | Longest/shortest subarray with constraint | `02-algorithms/04-sliding-window.md` |
| **Binary Search (Exact)** | "Find in sorted", "is X in the array" | `02-algorithms/11-binary-search.md` |
| **Binary Search (Bounds)** | First/last occurrence, insertion point | `02-algorithms/11-binary-search.md` |
| **Binary Search on Answer** | Minimize max, maximize min, "can we do X in Y" | `02-algorithms/11-binary-search.md` |
| **BFS** | Shortest path (unweighted), level-order, connected components, multi-source flood | `01-data-structures/13-graphs.md` |
| **DFS** | Path existence, all paths, islands, cycle detection, backtracking | `01-data-structures/13-graphs.md` |
| **Topological Sort** | Dependencies, build order, alien dictionary | `01-data-structures/13-graphs.md` |
| **Dynamic Programming (1D)** | Linear recurrence — house robber, climb stairs, coin change | `02-algorithms/15-dynamic-programming.md` |
| **Dynamic Programming (2D)** | Grid paths, edit distance, LCS, matrix chain | `02-algorithms/15-dynamic-programming.md` |
| **Knapsack** | "Pick items with weight/value constraints" | `02-algorithms/15-dynamic-programming.md` |
| **Greedy** | Interval scheduling, jump game, task scheduler | `02-algorithms/16-greedy.md` |
| **Backtracking** | Permutations, combinations, subsets, N-Queens, Sudoku | `02-algorithms/12-backtracking.md` |
| **Monotonic Stack** | Next greater/smaller element, histogram, trapped water | `01-data-structures/05-stack.md` |
| **Monotonic Deque** | Sliding window max/min | `02-algorithms/04-sliding-window.md` |
| **Union-Find** | Connected components, cycle in undirected, MST (Kruskal) | `02-algorithms/14-union-find.md` |
| **Heap / Priority Queue** | Top-K, merge K sorted, Dijkstra, two-heap median | `01-data-structures/10-heap.md` |
| **Trie** | Prefix matching, word search, autocomplete, XOR max | `01-data-structures/09-trie.md` |
| **Prefix Sum** | Subarray sum queries, range sum, 2D prefix sum | `01-data-structures/01-array.md` |
| **Divide & Conquer (reference)** | Merge sort, quick select — in sorting file | `02-algorithms/00-sorting.md` |

---

## 60-Second Pattern Recognition

The ordered trigger questions, the keyword → pattern table, and the pre-code
clarifying questions all live in one place:
[`patterns-master.md` § Quick Decision Trees](./patterns-master.md#quick-decision-trees).
