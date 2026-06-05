# Algorithms — Start Here

> [!note] L3 Reference Document
> This file is a **reference / meta document** — read it once, use it as a lookup.
> Not a coding practice file. Do not deep-study it like a topic file.


Technique deep-dives for **Google SDE-2 / SDE-3** coding interviews. Pair with data-structure notes in [01-data-structures](../01-data-structures/README.md); use this folder for **how to solve** (patterns, recurrences, graph algos, string matching).

**Repo hub:** [00-start-here/README.md](../00-start-here/README.md) · **Patterns (triggers):** [03-patterns/patterns-master.md](../03-patterns/patterns-master.md) · **Walkthroughs:** [problem-deep-dives.md](./20-problem-deep-dives.md) · **Google revision:** [GOOGLE_INTERVIEW_REVISION.md](../03-patterns/GOOGLE_INTERVIEW_REVISION.md)

---

## Pick your path

| If you… | Do this |
|---------|---------|
| **Have ~2 weeks before Google L4** | Must-nail topics below → **Quick Revision Triggers** per file → 2 timed problems/day → [GOOGLE_INTERVIEW_REVISION.md](../03-patterns/GOOGLE_INTERVIEW_REVISION.md) |
| **Learning a technique fresh** | Topic file → **Core Algorithms / Click Moments** → 2 problems from **Interview Questions** table |
| **Are revising before a mock** | **Quick Revision Triggers** + **Interview Questions** only; use [problem-deep-dives.md](./20-problem-deep-dives.md#l4-must-nail-problems) for one full walkthrough |
| **Stuck on “which algorithm?”** | [algorithm_tree.md](./algorithm_tree.md) — signal → family → file |

---

## Topic index

### Core coding (must-nail L4)

| Topic | When to use | File |
|-------|-------------|------|
| **Binary search** | Sorted input, BS on answer | [binary-search.md](./11-binary-search.md) |
| **Searching** | BS variants, search in matrix | [searching.md](./11-searching.md) |
| **Two pointers** | Sorted pairs, fast/slow, partition | [two-pointers.md](./03-two-pointers.md) |
| **Sliding window** | Contiguous subarray/substring | [sliding-window.md](./04-sliding-window.md) |
| **Sorting** | Which sort, quickselect, dutch flag | [sorting.md](./00-sorting.md) |
| **Graph algorithms** | BFS, Dijkstra, topo, shortest path | [graph.md](./13-graph.md) |
| **Backtracking** | Permutations, subsets, constraint search | [backtracking.md](./12-backtracking.md) |
| **Greedy** | Intervals, scheduling, exchange argument | [greedy.md](./16-greedy.md) |
| **Union-Find** | Connectivity, Kruskal, dynamic components | [union-find.md](./14-union-find.md) |
| **Divide & conquer** | Merge sort, inversion count, closest pair | [divide-and-conquer.md](./18-divide-and-conquer.md) |
| **String algorithms** | KMP, Rabin-Karp, Z-function | [string.md](./02-string.md) |
| **Dynamic programming** | Overlapping subproblems, optimal substructure | [dynamic-programming.md](./15-dynamic-programming.md) |
| **Recursion** | Tree DFS, memo, recursion → DP | [recursion.md](./15-recursion.md) · [recursion-to-dp.md](./15-recursion-to-dp.md) |

### Stretch & specialized

| Topic | When to use | File |
|-------|-------------|------|
| **Advanced graphs** | Tarjan SCC, bridges, Euler | [advanced-graphs.md](./14-advanced-graphs.md) |
| **Bit manipulation** | XOR, subsets, power of 2 | [bit-manipulation.md](./17-bit-manipulation.md) |
| **Maths** | GCD, primes, mod arithmetic | [maths.md](./17-maths.md) |
| **Miscellaneous** | Cross-cutting tricks | [miscellaneous.md](./19-miscellaneous.md) |
| **Problem bank (all topics)** | Full pseudocode walkthroughs + **[TOC at top](20-problem-deep-dives.md#jump-to-section)** | [problem-deep-dives.md](./20-problem-deep-dives.md) |

---

## DP & recursion (companion files)

| File | Focus |
|------|--------|
| [dynamic-programming.md](./15-dynamic-programming.md) | **Complete DP guide** — patterns, templates, interview bank |
| [recursion.md](./15-recursion.md) | **Complete recursion reference** — types, templates, tree/graph |
| [recursion-to-dp.md](./15-recursion-to-dp.md) | **Recursion → memo → bottom-up** — conversion bridge with worked examples |

**Problem lists with hints:** [coding/algorithms/](../coding/algorithms/) · ASCII overview: [MINDMAP.md](../MINDMAP.md) · Pattern triggers: [FLOWCHARTS.md](../FLOWCHARTS.md)

---

## How every topic file is organized

| Section | When to read |
|---------|----------------|
| **First-Principles Map** | First visit — why this technique exists |
| **Core Algorithms / Click Moments** | Learn templates and invariants |
| **SDE-3 Deep Dives** | Stretch; skip until L4 core is solid |
| **Interview Questions — Logic & Trickiness** | **High yield** before mocks |
| **Quick Revision Triggers** | **Day-before** — phrase → technique |
| **See also** | Links to DS files + patterns |
| **Flashcards** | Obsidian `#flashcard` tags (where present) |

**Shorter technique files** ([two-pointers.md](./03-two-pointers.md), [sliding-window.md](./04-sliding-window.md)) use: When to Use → Variants → Canonical Problems → Interview table → Quick Revision.

---

## Study progression (L4-first)

**Week 1 — Search & arrays techniques**  
[binary-search.md](./11-binary-search.md) → [two-pointers.md](./03-two-pointers.md) → [sliding-window.md](./04-sliding-window.md) → [sorting.md](./00-sorting.md)  
DS side: [array.md](../01-data-structures/01-array.md), [hashing.md](../01-data-structures/02-hashing.md)

**Week 2 — Graphs & trees**  
[graph.md](./13-graph.md) + [graphs.md](../01-data-structures/13-graphs.md) → [tree.md](../01-data-structures/08-tree.md) → [recursion.md](./15-recursion.md)

**Week 3 — DP & backtracking**  
[dynamic-programming.md](./15-dynamic-programming.md) → [recursion-to-dp.md](./15-recursion-to-dp.md) → [backtracking.md](./12-backtracking.md) → [greedy.md](./16-greedy.md)

**Week 4 — Polish**  
[union-find.md](./14-union-find.md) → [string.md](./02-string.md) → weak areas from [problem-deep-dives.md](./20-problem-deep-dives.md)

---

## Algorithm selection cheat sheet

Full tree: [algorithm_tree.md](./algorithm_tree.md).

| Problem signal | Start with |
|----------------|------------|
| Subarray / substring with constraint | [sliding-window.md](./04-sliding-window.md) |
| Sorted array, pair / triplet / minimize max | [binary-search.md](./11-binary-search.md) or [two-pointers.md](./03-two-pointers.md) |
| All combinations / permutations | [backtracking.md](./12-backtracking.md) |
| Optimal substructure + overlapping | [dynamic-programming.md](./15-dynamic-programming.md) · [recursion-to-dp.md](./15-recursion-to-dp.md) |
| Shortest path (unweighted) | BFS — [graph.md](./13-graph.md), [graphs.md](../01-data-structures/13-graphs.md) |
| Shortest path (weighted, non-negative) | Dijkstra — [graph.md](./13-graph.md) |
| Dependency ordering | Topological sort — [graph.md](./13-graph.md) |
| Dynamic connectivity | [union-find.md](./14-union-find.md) |
| Top K / Kth largest | Heap — [heap.md](../01-data-structures/10-heap.md) |
| Pattern in text | [string.md](./02-string.md) |

---

## Must-nail vs good-to-have (L4)

**Must-nail:** binary search (incl. on answer), two pointers, sliding window, BFS/DFS, core DP (1D/2D/knapsack), backtracking template, heap top-K, hash patterns (in [01-data-structures](../01-data-structures/README.md))

**High:** greedy intervals, union-find, topo sort, divide & conquer (quickselect)

**Good-to-have:** KMP/Rabin-Karp, Tarjan/bridges, segment tree, bit tricks, system-design algos, SQL, concurrency
