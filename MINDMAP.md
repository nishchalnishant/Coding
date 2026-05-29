---
module: root
topic: Mindmap
subtopic: 
status: unread
tags: [root, mindmap]
---
# Google SDE-2 Prep — Mind Map
_Last updated: 2026-05-17 (gap audit pass)_

---

## Repo Architecture

```
Coding/
├── 00-start-here/          [navigation hub, 4-week plan, 48-hr sprint, interview-day guide]
├── 01-data-structures/     [12 DS deep-dives: arrays → segment trees]
├── 02-algorithms/          [flat algo files + dp/ and recursion/ subdirs]
├── 03-patterns/            [pattern triggers, cheatsheets, revision guides]
├── 04-behavioral/          [Google 4 attributes + STAR stories]
├── 05-revision/            [complexity tables, Python gotchas, coding rubric]
└── books/                  [algorithm design references, CP3, DP book]
```

---

## 01 — Data Structures

```
01-data-structures/
├── Arrays          [Two Pointers · Sliding Window · Prefix Sum · Kadane's]              ✅ L4 Very High
├── Hash Maps       [Frequency Count · Two Sum · Grouping · Rolling Hash]                ✅ L4 Very High
├── Strings         [Immutability · Freq Array · Anagram · Palindrome · Sliding Window]  ✅ L4 Very High
│                   [→ 02-algorithms/string.md for KMP · Rabin-Karp · Z-algo · Manacher]
├── Trees / BST     [DFS pre/in/post · BFS · LCA · Path Sum · Morris Traversal]    ✅ L4 Very High
├── Graphs          [BFS · DFS · Topological Sort · Union-Find · Dijkstra]          ✅ L4 Very High
├── Stacks          [Monotonic Stack · Bracket Match · Next Greater Element]        ✅ L4 High
├── Heaps           [Top-K · Merge K Sorted · Two-Heap Median · Dijkstra]          ✅ L4 High
├── Linked Lists    [Fast/Slow Pointers · Dummy Node · Reverse In-Place]            ✅ L4 High
├── Queues          [BFS backbone · Sliding Window Max (Monotonic Deque)]           ⚠️ L4 Medium
├── Tries           [Prefix Search · Word Break · Autocomplete · XOR Max]           ⚠️ L4 Medium
├── Segment Trees   [Range Query · Range Update · Lazy Propagation]                ⚠️ L4 Lower
└── Advanced        [Bloom Filter · Skip List · Fenwick Tree · Disjoint Set]       ⚠️ Know use-case only
```

---

## 02 — Algorithms

```
02-algorithms/
├── Techniques (flat files)
│   ├── two-pointers.md       [Converging · Fast/Slow · Same-direction]
│   ├── sliding-window.md     [Fixed · Variable · Frequency map · Monotonic deque]
│   ├── binary-search.md      [Standard · Lower/Upper bound · BS-on-answer · 2D matrix]
│   ├── searching.md          [BFS/DFS patterns · exhaustive search]
│   ├── sorting.md            [Merge · Quick · Heap · Counting · Radix · TimSort]
│   ├── greedy.md             [Activity select · Interval scheduling · Huffman]
│   ├── divide-and-conquer.md [Merge sort · Quick select · Closest pair]
│   ├── backtracking.md       [Subsets · Permutations · N-Queens · Sudoku]
│   ├── union-find.md         [Path compression · Union by rank · Kruskal's]
│   ├── bit-manipulation.md   [XOR tricks · Bit masking · Power of 2]
│   ├── maths.md              [GCD · Sieve · Modular arithmetic · Combinatorics]
│   ├── string.md             [KMP · Rabin-Karp · Z-algorithm · Manacher's]
│   ├── graph.md              [BFS · DFS · Topo sort · Dijkstra · Bellman-Ford]
│   ├── advanced-graphs.md    [Floyd-Warshall · A* · Bridges · Articulation points]
│   ├── concurrency.md        [Mutex · Semaphore · Producer-Consumer · Dining Philosophers]
│   ├── system-design-algorithms.md  [Bloom Filter · Consistent Hashing · HyperLogLog · Rate Limiting]
│   ├── miscellaneous.md      [Fenwick Tree · Sweep Line · LRU/LFU implementation · Sparse Table]
│   ├── problem-deep-dives.md [100+ canonical problems: description + pseudocode]
│   └── algorithm_tree.md     [Decision tree: problem type → algorithm → template]
│
├── dynamic-programming/
│   ├── README.md                        [DP framework · state design · recurrence]
│   ├── dp-aditya-verma.md               [Pattern-based DP: 0-1 knapsack → LCS]
│   ├── grid-dp.md                       [2D grids · paths · obstacles]
│   ├── string-palindrome-dp.md          [LCS · LIS · Edit distance · Palindrome]
│   ├── stock-trading-dp.md              [State machine: hold/sell/cooldown]
│   ├── digit-dp.md                      [Count numbers with constraints]
│   ├── probability-combinatorics-dp.md  [Expected value · Ways to count]
│   ├── advanced-dp-optimizations.md     [Divide & Conquer opt · Knuth · Convex hull]
│   ├── tips-and-gotchas.md              [Common errors · memoization pitfalls]
│   └── questions-bank.md               [Canonical DP problems with key insights]
│
└── recursion/
    ├── README.md                [recursion model · call stack · base case design]
    ├── aditya-verma.md          [IBH method · hypothesis → induction → base]
    ├── tree-recursion.md        [subtree returns · path tracking]
    ├── graph-recursion.md       [DFS with state · backtrack undo]
    ├── string-recursion.md      [generate all · subsequences]
    ├── combination-problems.md  [choose k · power set]
    ├── recursion-to-dp.md       [memoize → tabulate pipeline]
    ├── tips-and-gotchas.md      [stack overflow · shared state bugs]
    └── questions-bank.md        [canonical recursion problems]
```

---

## 03 — Patterns

```
03-patterns/
├── patterns-master.md           [60-second trigger → pattern → template — READ FIRST]
├── interview-cheatsheet.md      [one-page: all patterns + complexity — interview-day read]
├── GOOGLE_QUICK_SHEET.md        [Google-specific: what they love, red flags]
├── GOOGLE_INTERVIEW_REVISION.md [deep revision guide: topic-by-topic]
├── TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md  [logic + trickiness for 100+ problems]
├── canonical-questions.md       [one-line key insight per canonical problem — quick check]
├── leetcode-variants.md         [LC problem variants grouped by pattern]
└── system-design.md             [system design stubs for SDE-2 scope]
```

---

## 04 — Behavioral

```
04-behavioral/
├── README.md                   [Google's 4 attributes overview + quick prep checklist]
├── behavioral.md               [STAR story index — 10+ stories with measurable outcomes]
└── BEHAVIORAL_GOOGLINESS.md    [Deep: GCA · Leadership · RRK · Googliness signal phrases + anti-patterns]
```

---

## 05 — Revision

```
05-revision/
├── README.md        [Complexity tables · Python gotchas · day-before checklist]
└── coding-rubric.md [Google coding rubric: what interviewers score]
```

---

## 4-Week Study Sequence

| Week | Focus | Key Files |
|------|-------|-----------|
| **1** | Arrays · Strings · Hashing · Linked Lists | `01-ds/array.md` · `01-ds/hashing.md` · `02-algo/two-pointers.md` · `02-algo/sliding-window.md` |
| **2** | Trees · Graphs · BFS/DFS · Topological Sort | `01-ds/tree.md` · `01-ds/graphs.md` · `02-algo/graph.md` · `02-algo/advanced-graphs.md` |
| **3** | DP · Backtracking · Greedy · Recursion | `02-algo/dynamic-programming/` · `02-algo/backtracking.md` · `02-algo/greedy.md` · `02-algo/recursion/` |
| **4** | Binary Search · Heaps · Tries · Behavioral | `02-algo/binary-search.md` · `01-ds/heap.md` · `01-ds/trie.md` · `04-behavioral/` |

> Week 5 (if 6 weeks): Segment Trees · Union-Find · Bit Manipulation · Math  
> Week 6: Full mock interviews + revision blitz

---

## Pattern → DS/Algo Cross-Reference

| Pattern | Primary DS | Key Algorithm File |
|---------|-----------|-------------------|
| Two Pointers | Array · Linked List | `02-algorithms/two-pointers.md` |
| Sliding Window | Array · String | `02-algorithms/sliding-window.md` |
| Binary Search | Array · Answer-space | `02-algorithms/binary-search.md` |
| BFS | Graph · Tree · Matrix | `02-algorithms/graph.md` |
| DFS / Backtracking | Graph · Tree | `02-algorithms/backtracking.md` |
| Monotonic Stack | Array · String | `01-data-structures/stack.md` |
| Monotonic Deque | Array | `01-data-structures/queue.md` |
| Top-K / Median | Heap | `01-data-structures/heap.md` |
| DP (1D/2D) | Array · String | `02-algorithms/dynamic-programming/README.md` |
| Trie Prefix | String | `01-data-structures/trie.md` |
| Union-Find | Graph | `02-algorithms/union-find.md` |
| Topological Sort | Graph (DAG) | `02-algorithms/graph.md` |

---

## L4 Priority Map

| Priority | Topics |
|----------|--------|
| ✅ Must nail | Arrays · Hash Maps · Trees · Graphs · Strings |
| ✅ High | Stacks · Heaps · Linked Lists |
| ⚠️ Medium | Tries · Union-Find · Queues |
| ⚠️ Know use-case | Segment Trees · Bloom Filter · Skip List |

---

## Books

| Book | Focus |
|------|-------|
| `the-algorithm-design-manual.md` | Algorithm design intuition, war stories |
| `dynamic-programming-for-coding-interviews.md` | DP pattern drilling |
| `elements-of-programming-interviews-in-python.md` | EPI — problem + solution walkthroughs |
| `data-structures-and-algorithms-using-python.md` | Python-specific DS implementations |
| `cp3.md` | Competitive programming — advanced techniques |
