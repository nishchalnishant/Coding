# Patterns — Index

## What this covers

> [!abstract] In this file
> **Covers:** Which pattern guide answers which question, and a pattern → lecture-file cross-reference.
> **You'll be able to:** Know which pattern guide to open and when.
> **Prereqs:** None · **Pair with:** [Patterns master](patterns-master.md) · **Time:** 10 min
> **How to use:** reference — read once, then use as a lookup.

**Sections:** [Core Resources](#core-resources) · [Pattern → Topic Cross-Reference](#pattern--topic-cross-reference) · [60-Second Pattern Recognition](#60-second-pattern-recognition)

---

## Core Resources

Each guide answers one question. Open the one that matches what you need right now.

| Your question | File | Mode |
|---|---|---|
| "Which pattern is this?" — triggers, decision trees, pivots | [`patterns-master.md`](./patterns-master.md) | Lookup |
| "Why does this pattern work / how do I re-derive it?" | [`HOW_TO_THINK.md`](./HOW_TO_THINK.md) | Read once, in order |
| "I can't design recursion or DP states" | [`RECURSION_AND_DP_MASTERCLASS.md`](./RECURSION_AND_DP_MASTERCLASS.md) | Lesson, in order |
| "Give me graded practice for one pattern" | [`PATTERN_LADDERS.md`](./PATTERN_LADDERS.md) | Practice (weeks) |
| "The interviewer changed the problem — now what?" | [`leetcode-variants.md`](./leetcode-variants.md) | Read once |
| "What's the trap in canonical problem X?" | [`TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md`](./TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md) | Lookup |
| "Commit or pivot? How do I use a hint?" | [`INTERVIEW_JUDGMENT.md`](./INTERVIEW_JUDGMENT.md) | Read once, reread before mocks |
| "Am I ready?" — timed problems + rubric | [`MOCK_INTERVIEW_SET.md`](./MOCK_INTERVIEW_SET.md) | Practice |
| "Interview is in 7 days / 48 h / tomorrow" | [`GOOGLE_INTERVIEW_REVISION.md`](./GOOGLE_INTERVIEW_REVISION.md) | Plan |
| "What follow-ups will a senior interviewer ask?" | [`SENIOR_FOLLOWUPS.md`](./SENIOR_FOLLOWUPS.md) | L4+/senior only |

Outside this folder: [L3 cheatsheet](../00-L3-EXECUTION-META/L3_CHEATSHEET.md) (round clock, Big-O, edge cases) · [MINDMAP](../MINDMAP.md) (problem-name → hint recall) · [questions.md](../questions.md) (find a walkthrough) · [FLOWCHARTS](../FLOWCHARTS.md) (visual study paths).

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
