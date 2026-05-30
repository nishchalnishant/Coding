# Algorithms — Start Here

Technique deep-dives for **Google SDE-2 / SDE-3** coding interviews. Pair with data-structure notes in [01-data-structures](../01-data-structures/README.md); use this folder for **how to solve** (patterns, recurrences, graph algos, string matching).

**Repo hub:** [00-start-here/README.md](../00-start-here/README.md) · **Patterns (triggers):** [03-patterns/patterns-master.md](../03-patterns/patterns-master.md) · **Walkthroughs:** [problem-deep-dives.md](./problem-deep-dives.md) · **Google revision:** [GOOGLE_INTERVIEW_REVISION.md](../03-patterns/GOOGLE_INTERVIEW_REVISION.md)

---

## Pick your path

| If you… | Do this |
|---------|---------|
| **Have ~2 weeks before Google L4** | Must-nail topics below → **Quick Revision Triggers** per file → 2 timed problems/day → [GOOGLE_INTERVIEW_REVISION.md](../03-patterns/GOOGLE_INTERVIEW_REVISION.md) |
| **Learning a technique fresh** | Topic file → **Core Algorithms / Click Moments** → 2 problems from **Interview Questions** table |
| **Are revising before a mock** | **Quick Revision Triggers** + **Interview Questions** only; use [problem-deep-dives.md](./problem-deep-dives.md#l4-must-nail-problems) for one full walkthrough |
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
| **Dynamic programming** | Overlapping subproblems, optimal substructure | [dynamic-programming/README.md](./dynamic-programming/README.md) |
| **Recursion** | Tree DFS, memo, recursion → DP | [recursion/README.md](./recursion/README.md) |

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

## Subfolders

### [dynamic-programming/](./dynamic-programming/)

| File | Focus |
|------|--------|
| [README.md](./dynamic-programming/README.md) | **Start here** — 4-step framework, core patterns |
| [dp-aditya-verma.md](./dynamic-programming/dp-aditya-verma.md) | Pattern catalog (knapsack, LCS, …) |
| [grid-dp.md](./dynamic-programming/grid-dp.md) | Unique paths, min path sum, maximal square |
| [stock-trading-dp.md](./dynamic-programming/stock-trading-dp.md) | Buy/sell state machine |
| [string-palindrome-dp.md](./dynamic-programming/string-palindrome-dp.md) | LPS, palindrome partitioning |
| [digit-dp.md](./dynamic-programming/digit-dp.md) | Count numbers with digit constraints |
| [probability-combinatorics-dp.md](./dynamic-programming/probability-combinatorics-dp.md) | Expected value, game theory |
| [advanced-dp-optimizations.md](./dynamic-programming/advanced-dp-optimizations.md) | CHT, SOS DP, Knuth (stretch) |
| [tips-and-gotchas.md](./dynamic-programming/tips-and-gotchas.md) | **Revision** — bugs, iteration direction |
| [questions-bank.md](./dynamic-programming/questions-bank.md) | Leveled drill list |

### [recursion/](./recursion/)

| File | Focus |
|------|--------|
| [README.md](./recursion/README.md) | **Start here** — types, templates |
| [aditya-verma.md](./recursion/aditya-verma.md) | Include/exclude, IP/OP patterns |
| [combination-problems.md](./recursion/combination-problems.md) | Combinations, subset sum |
| [recursion-to-dp.md](./recursion/recursion-to-dp.md) | Top-down → tabulation |
| [tree-recursion.md](./recursion/tree-recursion.md) | Path sum, BST, tree DP |
| [graph-recursion.md](./recursion/graph-recursion.md) | DFS, topo, flood fill |
| [string-recursion.md](./recursion/string-recursion.md) | Parsing, generation |
| [tips-and-gotchas.md](./recursion/tips-and-gotchas.md) | **Revision** — common bugs |
| [questions-bank.md](./recursion/questions-bank.md) | Leveled drill list |

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

**Shorter technique files** ([two-pointers.md](./two-pointers.md), [sliding-window.md](./sliding-window.md)) use: When to Use → Variants → Canonical Problems → Interview table → Quick Revision.

---

## Study progression (L4-first)

**Week 1 — Search & arrays techniques**  
[binary-search.md](./binary-search.md) → [two-pointers.md](./two-pointers.md) → [sliding-window.md](./sliding-window.md) → [sorting.md](./sorting.md)  
DS side: [array.md](../01-data-structures/array.md), [hashing.md](../01-data-structures/hashing.md)

**Week 2 — Graphs & trees**  
[graph.md](./graph.md) + [graphs.md](../01-data-structures/graphs.md) → [tree.md](../01-data-structures/tree.md) → [recursion/tree-recursion.md](./recursion/tree-recursion.md)

**Week 3 — DP & backtracking**  
[dynamic-programming/README.md](./dynamic-programming/README.md) → [backtracking.md](./backtracking.md) → [greedy.md](./greedy.md)

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
| Optimal substructure + overlapping | [dynamic-programming/README.md](./dynamic-programming/README.md) |
| Shortest path (unweighted) | BFS — [graph.md](./graph.md), [graphs.md](../01-data-structures/graphs.md) |
| Shortest path (weighted, non-negative) | Dijkstra — [graph.md](./graph.md) |
| Dependency ordering | Topological sort — [graph.md](./graph.md) |
| Dynamic connectivity | [union-find.md](./union-find.md) |
| Top K / Kth largest | Heap — [heap.md](../01-data-structures/heap.md) |
| Pattern in text | [string.md](./string.md) |

---

## Must-nail vs good-to-have (L4)

**Must-nail:** binary search (incl. on answer), two pointers, sliding window, BFS/DFS, core DP (1D/2D/knapsack), backtracking template, heap top-K, hash patterns (in [01-data-structures](../01-data-structures/README.md))

**High:** greedy intervals, union-find, topo sort, divide & conquer (quickselect)

**Good-to-have:** KMP/Rabin-Karp, Tarjan/bridges, segment tree, bit tricks, system-design algos, SQL, concurrency
