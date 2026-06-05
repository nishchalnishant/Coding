---
module: root
topic: Flowcharts
subtopic: 
status: unread
tags: [root, flowcharts]
---

← [Start here](00-start-here/README.md) · [Mindmap (problems + hints)](MINDMAP.md) · [DS index](01-data-structures/README.md) · [Algorithms index](02-algorithms/README.md)

# Flowcharts — ASCII only
_Each block = one topic file · pattern triggers · canonical problems · complexity_


## Master — Problem → Pattern (60-second)

```
Read constraints + examples
├── Contiguous subarray / substring + constraint?
├── Sorted input OR "minimize max / maximize min"?
└── Tree or graph structure?
│   └── Shortest path (unweighted)      → BFS (01-data-structures/13-graphs.md) `⚡ T1`
```


## 00 — Start Here

```
00-start-here/README.md
└── Entry point (topic-first; don't read linearly)
    └── Have 14 days?   → DP `⚡ T1` · Binary Search `🎯 T2`
    │                     + 02-algorithms/20-problem-deep-dives.md#l4-must-nail-problems
    │                     + 03-patterns/GOOGLE_INTERVIEW_REVISION.md (Part D)
    │                     Hour 8–16: 05-revision/README.md + Quick Revision Triggers per weak topic
    │                     Hour 16–24: 2 timed mocks + problem-deep-dives L4 list redo
```


## 01 — Data Structures

```
01-data-structures/README.md

01-data-structures/array.md
    ├── Two Pointers → container with most water `⚡ T1`
    ├── Sliding Window → longest substring without repeat `⚡ T1`
    └── Sorting-based → merge intervals `🎯 T2` · meeting rooms `🎯 T2` · 3Sum `⚡ T1`

01-data-structures/hashing.md
└── Hash Maps [O(1) avg insert/search/delete]
    ├── Grouping → group anagrams `⚡ T1`

01-data-structures/string.md
    ├── Frequency Map → group anagrams `⚡ T1`
    ├── Sliding Window (variable) → at-most-K distinct `⚡ T1`
    ├── Sliding Window (fixed) → permutation in string `⚡ T1`

01-data-structures/linked-list.md
    ├── Reverse In-Place → reverse linked list `🎯 T2`

01-data-structures/stack.md
└── Stacks [O(1) push/pop]
    ├── Monotonic Stack (decreasing) → Daily Temperatures `🎯 T2` · Largest Rectangle in Histogram `🎯 T2`
    ├── Monotonic Stack (increasing) → Trapping Rain Water `⚡ T1`

01-data-structures/queue.md
└── Queues / Deques [O(1) enqueue/dequeue]
    ├── BFS → rotting oranges `⚡ T1` · word ladder `⚡ T1`
    └── Priority Queue (heap) → top-K `⚡ T1`

01-data-structures/tree.md
└── Trees / BST [O(log n) avg BST ops]
    ├── DFS In-order   → kth smallest `🎯 T2`
    ├── DFS Post-order → diameter `🎯 T2`
    ├── BFS (level)    → right side view `🎯 T2`
    ├── Path Sum       → max path sum `🎯 T2`

01-data-structures/graphs.md
    ├── BFS → walls and gates `⚡ T1`
    ├── DFS → number of islands `⚡ T1`
    ├── Topological Sort (Kahn's) → course schedule `⚡ T1`
    ├── Union-Find → redundant connection `⚡ T1`
    ├── Dijkstra (min-heap) → network delay `⚡ T1` · cheapest flights `⚡ T1`

01-data-structures/heap.md
    ├── Merge K sorted lists → min-heap of (val, list_idx, elem_idx) `⚡ T1`

01-data-structures/trie.md
└── Tries [O(m) insert/search — m = word length]
    ├── Prefix search → implement Trie `⚡ T1`
    ├── Word Break → DP + Trie to find valid splits `🎯 T2`
    ├── Word Search II → Trie + DFS backtrack on grid `⚡ T1`

01-data-structures/segment-tree.md
    ├── Range Sum Query → range query `🎯 T2`

01-data-structures/advanced-structures.md
└── Advanced [Know use-case; unlikely to implement from scratch at L4]

01-data-structures/ds_tree.md
```


## 02 — Algorithms (Flat Files)

```

02-algorithms/two-pointers.md
└── Two Pointers [Converging vs same-direction vs multi-sequence scan]
    ├── Converging (opposite ends) → container with most water `⚡ T1`

02-algorithms/sliding-window.md
└── Sliding Window [running aggregates over contiguous sub-ranges]

02-algorithms/binary-search.md
└── Binary Search `🎯 T2`
    ├── Standard → sorted array `⚡ T1` · search insert position `⚡ T1`

02-algorithms/sorting.md
└── Sorting [Ordering invariants & selection tradeoffs]
    ├── Merge Sort → count inversions `🎯 T2`
    ├── External Merge Sort → split runs + K-way merge for data > RAM `🎯 T2`

02-algorithms/greedy.md
└── Greedy [Irrevocable local choices for global optimum]
    ├── Jump Game → O(n) `🎯 T2`
    └── Huffman & Task Scheduler → frequency-based merge/slots counting `⚡ T1`

02-algorithms/divide-and-conquer.md
└── Divide & Conquer
    ├── Merge Sort → inversion count as side-effect `🎯 T2`

02-algorithms/backtracking.md
└── Backtracking [O(2^n) subsets · O(n!) permutations] `🎯 T2`
    ├── Subsets → power set `🎯 T2`
    ├── Permutations → swap in-place or used[] array `🎯 T2`
    ├── Combinations → k-of-n `🎯 T2`
    ├── N-Queens → col+diag sets for O(1) conflict check `🎯 T2`
    └── Sudoku Solver → undo on failure `🎯 T2`

02-algorithms/dynamic-programming.md

02-algorithms/recursion.md

02-algorithms/recursion-to-dp.md

02-algorithms/union-find.md

02-algorithms/bit-manipulation.md
└── Bit Manipulation [Direct integer register operations]

02-algorithms/graph.md
└── Graph Algorithms
    └── Minimum Spanning Tree (MST)

02-algorithms/advanced-graphs.md
└── Advanced Graphs
    └── A* → f = g + h `⚡ T1`

02-algorithms/string.md
└── String Algorithms

02-algorithms/maths.md
└── Math [Number theory & algebraic invariants]

02-algorithms/searching.md
└── Searching [O(log n) binary search vs O(n) linear scan]
    ├── Rotated Sorted Array → identify sorted half first → search target or find min `⚡ T1`
    ├── Peak Element → compare mid with mid+1 → climb gradient to local maximum `⚡ T1`
    └── Median of Two Sorted Arrays → partition both arrays → O(log(min(M, N))) `⚡ T1`

02-algorithms/concurrency.md
└── Concurrency [SDE-3 depth; SDE-2: know the patterns]

02-algorithms/system-design-algorithms.md
└── System Design Algorithms [distributed systems building blocks]


02-algorithms/miscellaneous.md
└── Miscellaneous Advanced Structures [SDE-3 level; SDE-2: know use-cases]
    ├── LRU Cache → move to head on access `🎯 T2`


02-algorithms/algorithm_tree.md
    └── Design patterns → Sliding Window `⚡ T1`
```


## 02 — Dynamic Programming

```
02-algorithms/dynamic-programming.md
    │
    ├── UNIVERSAL RECIPE (always in this order)
    │   ├── 1. Recursive brute force (correct base cases)
    │   ├── 2. Memoization (top-down)
    │   ├── 3. Tabulation (bottom-up)
    │   └── 4. Space optimize (rolling row / two vars)
    │
    ├── CHOOSE PATTERN IN 30s
    │
    │   ├── 1  Linear/Fibonacci    → house robber `🎯 T2` · decode ways `🎯 T2` · word break `🎯 T2`
    │   ├── 2  0/1 Knapsack        → target sum `🎯 T2` · partition equal subset `🎯 T2`
    │   ├── 4  LCS family          → edit distance `🎯 T2` · interleaving `🎯 T2` · distinct subseq `🎯 T2`
    │   ├── 8  Grid DP             → unique paths `🎯 T2` · maximal square `🎯 T2`
    │   ├── 9  Tree DP             → house robber III `🎯 T2` · diameter `🎯 T2`
    │   ├── 12 String/palindrome   → palindrome partitioning `🎯 T2`
    │
    ├── L4 MUST-NAIL
    │   └── house robber `🎯 T2`· coin change `🎯 T2`· word break `🎯 T2`· LIS `⚡ T1`· LCS · edit distance `🎯 T2`
    │
    ├── TOP BUGS (memorize these)
    │
```


## 02 — Recursion

```
02-algorithms/recursion.md
    │
    ├── ADITYA VERMA 4-STEP
    │   ├── 1. Draw choice diagram (branches per level)
    │   ├── 3. Explore all paths (include/exclude or choose-next)
    │   └── 4. Unchoose / restore state (undo mutations)
    │
    ├── BASE CASE CHECKLIST
    │   ├── Empty input (n==0, node==None, i==len(s))
    │   ├── Single element / leaf
    │   └── Constraint met (remaining==0, target found)
    │
    ├── RETURN VALUE DESIGN (pick one)
    │
    │   ├── 1 Include/Exclude     → target sum `🎯 T2`
    │   ├── 2 Permutations        → letter case perm `🎯 T2`
    │   ├── 3 IP/OP + guard       → restore IP `🎯 T2`
    │   ├── 4 Divide & combine    → merge"      → merge sort `🎯 T2`
    │   ├── 6 Tree/graph DFS      → islands `⚡ T1`
    │   ├── 7 Constraint satisfy  → Sudoku `🎯 T2` · word search II (trie prune) `⚡ T1`
    │
    ├── COMBINATION FAMILY (same file)
    │
    ├── L4 MUST-NAIL
    │   └── subsets `🎯 T2`· permutations `🎯 T2`· combination sum `🎯 T2`· generate parentheses `🎯 T2`· word search `🎯 T2`
    │
    ├── TOP BUGS
    │   ├── Graph → mark visited BEFORE recurse `⚡ T1`
    │   └── @lru_cache → args must be hashable (tuple not list) `🎯 T2`
    │
```


## 03 — Patterns

```
03-patterns/README.md
└── Patterns folder index

03-patterns/patterns-master.md
└── Pattern Recognition Master [READ FIRST — before drilling problems]
    ├── Trigger: sorted + target sum → Two Pointers `🎯 T2`

03-patterns/interview-cheatsheet.md
└── One-page interview cheatsheet [Read on interview day — 10 min max]
    └── All patterns + complexity + Python snippet

03-patterns/GOOGLE_QUICK_SHEET.md
└── Google-specific [What they reward / red flags]

03-patterns/GOOGLE_INTERVIEW_REVISION.md
└── Deep revision guide [topic-by-topic Google lens]
    └── Use in Week 4 and 48-hr sprint

03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md
└── 100+ canonical problems [logic + trickiness per problem]
    └── Use to identify why a problem is tricky, not just what the solution is

03-patterns/canonical-questions.md
└── Canonical Questions — Key Insight Index [one-line insight per problem]
    ├── Graphs: Word Ladder → BFS on graph where edge = 1-char difference `⚡ T1`
    ├── DP: Coin Change → Burst Balloons → last balloon in interval = dp[i][j] `🎯 T2`
    └── Use: check if you know the key insight cold before opening solution

03-patterns/leetcode-variants.md
└── LC variants by pattern [grouped for drilling]
    └── Use after reading patterns-master — drill 2-3 variants per pattern

03-patterns/lld.md

03-patterns/system-design.md
    └── Pair with 02-algorithms/system-design-algorithms.md for building blocks
```


## 04 — Behavioral

```
04-behavioral/README.md
└── Google 4 Attributes

04-behavioral/behavioral.md
└── STAR Story Index

04-behavioral/BEHAVIORAL_GOOGLINESS.md
└── Four Google Attributes — Deep Dive
    │   └── Signal: "Before I start coding, let me think about edge cases..."
    │   └── Signal: "No one was owning X, so I set up a sync and drove it to completion..."
    │   └── Signal: "We chose eventual consistency because strong consistency added 3x latency..."
    │   └── Signal: "I didn't know X, so I read the source code and ran an experiment..."

04-behavioral/googliness-round.md
└── Googliness Round [Proving team effectiveness & structured behavior]
```


## 05 — Revision

```
05-revision/README.md
└── Complexity Quick-Reference
    ├── DS          → Heap O(log n) push `⚡ T1`
    ├── Graphs      → n) `⚡ T1`
    
└── Python Gotchas
    ├── arr[:] → shallow copy (arr = arr2 is a reference, not copy) `⚡ T1`

05-revision/mock-log.md

05-revision/coding-rubric.md
└── Google Coding Rubric
```


## Practice loop (what to do with this file)

```
Weekly cycle

Readiness signal (DSA)
├── Can name pattern in ~60s for L4 must-nail list
├── Medium problems cold in ~25–35 min with communication
└── 4+ mocks logged with improving failure modes
```

