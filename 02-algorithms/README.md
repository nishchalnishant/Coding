# Algorithms — Start Here

Technique deep-dives for **Amazon SDE-2** coding interviews. Pair with data-structure notes in [01-data-structures](../01-data-structures/README.md); use this folder for **how to solve** (patterns, recurrences, graph algos, string matching).

**Repo hub:** [00-start-here/README.md](../00-start-here/README.md) · **Patterns (triggers):** [03-patterns/patterns-master.md](../03-patterns/patterns-master.md) · **Walkthroughs:** [problem-deep-dives.md](./problem-deep-dives.md) · **Amazon SDE-2 track:** [amazon-sde2/README.md](../amazon-sde2/README.md)

---

## Pick your path

| If you… | Do this |
|---------|---------|
| **Have ~2 weeks before Amazon SDE-2** | Must-nail topics below → **Quick Revision Triggers** per file → 2 timed problems/day → [amazon-sde2/02-coding-questions.md](../amazon-sde2/02-coding-questions.md) |
| **Learning a technique fresh** | Topic file → **Core Algorithms / Click Moments** → 2 problems from **Interview Questions** table |
| **Are revising before a mock** | **Quick Revision Triggers** + **Interview Questions** only; use [problem-deep-dives.md](./problem-deep-dives.md) for one full walkthrough |
| **Stuck on “which algorithm?”** | [algorithm_tree.md](./algorithm_tree.md) — signal → family → file |

---

## Topic index

### Core coding (must-nail L4)

| Topic | When to use | File |
|-------|-------------|------|
| **Binary search** | Sorted input, BS on answer | [binary-search.md](./binary-search.md) |
| **Searching** | BS variants, search in matrix | [searching.md](./searching.md) |
| **Two pointers** | Sorted pairs, fast/slow, partition | [two-pointers.md](./two-pointers.md) |
| **Sliding window** | Contiguous subarray/substring | [sliding-window.md](./sliding-window.md) |
| **Sorting** | Which sort, quickselect, dutch flag | [sorting.md](./sorting.md) |
| **Graph algorithms** | BFS, Dijkstra, topo, shortest path | [graph.md](./graph.md) |
| **Backtracking** | Permutations, subsets, constraint search | [backtracking.md](./backtracking.md) |
| **Greedy** | Intervals, scheduling, exchange argument | [greedy.md](./greedy.md) |
| **Union-Find** | Connectivity, Kruskal, dynamic components | [union-find.md](./union-find.md) |
| **Divide & conquer** | Merge sort, inversion count, closest pair | [divide-and-conquer.md](./divide-and-conquer.md) |
| **String algorithms** | KMP, Rabin-Karp, Z-function | [string.md](./string.md) |
| **Dynamic programming** | Overlapping subproblems, optimal substructure | [dynamic-programming.md](./dynamic-programming.md) |
| **Recursion** | Tree DFS, memo, recursion → DP | [recursion.md](./recursion.md) · [recursion-to-dp.md](./recursion-to-dp.md) |

### Stretch & specialized

| Topic | When to use | File |
|-------|-------------|------|
| **Advanced graphs** | Tarjan SCC, bridges, Euler | [advanced-graphs.md](./advanced-graphs.md) |
| **Bit manipulation** | XOR, subsets, power of 2 | [bit-manipulation.md](./bit-manipulation.md) |
| **Maths** | GCD, primes, mod arithmetic | [maths.md](./maths.md) |
| **System design algorithms** | Bloom, consistent hash, rate limit | [system-design-algorithms.md](./system-design-algorithms.md) |
| **Concurrency** | Producer-consumer, locks (LLD-style) | [concurrency.md](./concurrency.md) |
| **SQL** | Window functions, JOINs, CTEs | [sql.md](./sql.md) |
| **Miscellaneous** | Cross-cutting tricks | [miscellaneous.md](./miscellaneous.md) |
| **Problem bank (all topics)** | Full pseudocode walkthroughs + **[TOC at top](problem-deep-dives.md#jump-to-section)** | [problem-deep-dives.md](./problem-deep-dives.md) |

---

## DP & recursion (companion files)

| File | Focus |
|------|--------|
| [dynamic-programming.md](./dynamic-programming.md) | **Complete DP guide** — patterns, templates, interview bank |
| [recursion.md](./recursion.md) | **Complete recursion reference** — types, templates, tree/graph |
| [recursion-to-dp.md](./recursion-to-dp.md) | **Recursion → memo → bottom-up** — conversion bridge with worked examples |

**Problem lists with hints:** [coding/algorithms/](../coding/algorithms/) · ASCII overview: [MINDMAP.md](../MINDMAP.md) · Pattern triggers: [FLOWCHARTS.md](../FLOWCHARTS.md)

---

## How every topic file is organized

| Section | When to read |
|---------|----------------|
| **First-Principles Map** | First visit — why this technique exists |
| **Core Algorithms / Click Moments** | Learn templates and invariants |
| **Trade-offs** | Algorithm selection and when NOT to use a technique |
| **Interview Questions — Logic & Trickiness** | **High yield** before mocks |
| **Quick Revision Triggers** | **Day-before** — phrase → technique |
| **See also** | Links to DS files + patterns |
| **Flashcards** | Obsidian `#flashcard` tags (where present) |

**Shorter technique files** ([two-pointers.md](./two-pointers.md), [sliding-window.md](./sliding-window.md)) use: When to Use → Variants → Canonical Problems → Interview table → Quick Revision.

---

## Study progression (L4-first)

**Week 1 — Search & arrays techniques**  
[binary-search.md](./binary-search.md) → [two-pointers.md](./two-pointers.md) → [sliding-window.md](./sliding-window.md) → [sorting.md](./sorting.md)  
DS side: [array.md](../01-data-structures/array.md), [hashing.md](../01-data-structures/hashing.md)

**Week 2 — Graphs & trees**  
[graph.md](./graph.md) + [graphs.md](../01-data-structures/graphs.md) → [tree.md](../01-data-structures/tree.md) → [recursion.md](./recursion.md)

**Week 3 — DP & backtracking**  
[dynamic-programming.md](./dynamic-programming.md) → [recursion-to-dp.md](./recursion-to-dp.md) → [backtracking.md](./backtracking.md) → [greedy.md](./greedy.md)

**Week 4 — Polish**  
[union-find.md](./union-find.md) → [string.md](./string.md) → weak areas from [problem-deep-dives.md](./problem-deep-dives.md)

---

## Algorithm selection cheat sheet

Full tree: [algorithm_tree.md](./algorithm_tree.md).

| Problem signal | Start with |
|----------------|------------|
| Subarray / substring with constraint | [sliding-window.md](./sliding-window.md) |
| Sorted array, pair / triplet / minimize max | [binary-search.md](./binary-search.md) or [two-pointers.md](./two-pointers.md) |
| All combinations / permutations | [backtracking.md](./backtracking.md) |
| Optimal substructure + overlapping | [dynamic-programming.md](./dynamic-programming.md) · [recursion-to-dp.md](./recursion-to-dp.md) |
| Shortest path (unweighted) | BFS — [graph.md](./graph.md), [graphs.md](../01-data-structures/graphs.md) |
| Shortest path (weighted, non-negative) | Dijkstra — [graph.md](./graph.md) |
| Dependency ordering | Topological sort — [graph.md](./graph.md) |
| Dynamic connectivity | [union-find.md](./union-find.md) |
| Top K / Kth largest | Heap — [heap.md](../01-data-structures/heap.md) |
| Pattern in text | [string.md](./string.md) |

---

## Must-nail vs good-to-have (Amazon SDE-2)

**Must-nail:** binary search (incl. on answer), two pointers, sliding window, BFS/DFS, core DP (1D/2D/knapsack), backtracking (subsets/permutations/N-Queens), heap top-K, hash patterns (in [01-data-structures](../01-data-structures/README.md))

**High:** greedy intervals (meeting rooms, non-overlapping), union-find, topo sort, Dijkstra, divide & conquer (merge sort/quickselect)

**Good-to-have:** KMP awareness, bit manipulation (XOR tricks, power of 2), string patterns (anagram, palindrome), DSU Kruskal

**Awareness only (not tested in depth):** Tarjan/bridges, suffix arrays, Aho-Corasick, system-design algos, SQL, concurrency LLD
