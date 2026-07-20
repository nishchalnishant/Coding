---
module: root
topic: Flowcharts
tags: [root, flowcharts, l3]
---

← [L3 Roadmap](coding/l3-google-roadmap.md) · [Mindmap (problems + hints)](MINDMAP.md) · [DS index](01-data-structures/README.md) · [Algorithms index](02-algorithms/README.md)

# Flowcharts — ASCII only (Google L3)
_Each block = one topic file · pattern triggers · canonical problems · complexity_

---

## Master — Problem → Pattern (60-second)

```
Read constraints + examples (n, m, sorted?, negative?, tree/graph?)
│
├── Contiguous subarray / substring + sum / distinct / repeat constraint?
│   └── Sliding Window (variable or fixed) → 04-sliding-window.md · 01-array.md `⚡ T1`
│
├── Sorted input OR "minimize the maximum / maximize the minimum"?
│   ├── Exact value in sorted array → Binary Search → 11-binary-search.md `⚡ T1`
│   └── Feasibility on answer space → Binary Search on Answer → 11-binary-search.md `⚡ T1`
│
├── Tree or graph structure?
│   ├── Shortest path (unweighted) → BFS → 13-graphs.md `⚡ T1`
│   ├── Connected components / flood fill → DFS → 13-graphs.md `⚡ T1`
│   ├── Prerequisites / ordering → Topological Sort → 13-graphs.md `⚡ T1`
│   ├── Dynamic connectivity / grouping → Union-Find → 14-union-find.md `⚡ T1`
│   └── Weighted shortest path (non-negative) → Dijkstra + heap → 13-graphs.md `⚡ T1`
│
├── Top-K / merge K streams / running median?
│   └── Heap → 10-heap.md · 16-greedy.md `⚡ T1`
│
├── Prefix / complement / frequency count?
│   └── Hash map → 02-hashing.md · 03-string.md `⚡ T1`
│
├── Monotonic property while scanning (next greater, histogram)?
│   └── Monotonic Stack → 05-stack.md `⚡ T1`
│
├── Overlapping intervals / scheduling?
│   └── Sort + Greedy → 16-greedy.md · 00-sorting.md `🎯 T2`
│
├── Count / generate all valid configurations?
│   └── Backtracking → 12-backtracking.md · 09-recursion.md `🎯 T2`
│
└── Optimal substructure + overlapping subproblems?
    └── DP (1D / knapsack / grid / LCS) → 15-dynamic-programming.md `🎯 T2`
```

---

## 00 — Start Here (L3)

```
README.md
└── Entry point — topic-first, not linear
    ├── Day 1 → coding/l3-google-roadmap.md (4-week plan) `⚡ T1`
    ├── Always → 00-L3-EXECUTION-META/L3_CHEATSHEET.md (pacing + constraints)
    └── Interview day → 03-patterns/GOOGLE_INTERVIEW_REVISION.md Part A (10 min max)

Have 4 weeks?
    Week 1 → Arrays, hashing, two pointers, sliding window, binary search
    Week 2 → Graphs, BFS/DFS, topo, union-find, heaps
    Week 3 → DP core patterns, backtracking, recursion bridge
    Week 4 → Greedy, intervals, timed mocks + 03-patterns/GOOGLE_INTERVIEW_REVISION.md

Have 2 weeks?
    T1 only from 01-data-structures/README.md + 02-algorithms/README.md must-solve lists
    + 4 timed mocks (log misses in your own tracker)
```

---

## 01 — Data Structures (study path)

```
01-data-structures/README.md

01-data-structures/01-array.md
    ├── Two Pointers → 3Sum · container with most water · trapping rain water `⚡ T1`
    ├── Sliding Window → max consecutive ones III · subarrays with K distinct `⚡ T1`
    ├── Prefix / Kadane → subarray sum equals K · maximum subarray `⚡ T1`/`🎯 T2`
    └── Partition → sort colors (Dutch flag) `⚡ T1`

01-data-structures/02-hashing.md
    └── Hash Maps [O(1) avg]
        ├── Complement → two sum (unsorted) `⚡ T1`
        └── Grouping → group anagrams `⚡ T1`

01-data-structures/03-string.md
    ├── Frequency Map → valid anagram · group anagrams `⚡ T1`
    ├── Sliding Window → longest substring without repeat · min window substring `⚡ T1`
    └── Stack / parsing → valid parentheses · decode string `🎯 T2`

01-data-structures/07-linked-list.md
    ├── Reverse In-Place → reverse linked list `🎯 T2`
    ├── Fast/Slow → linked list cycle · middle node `⚡ T1`
    └── Merge → merge two sorted lists `⚡ T1`

01-data-structures/05-stack.md
    └── Monotonic Stack
        ├── Next greater → daily temperatures `🎯 T2`
        └── Histogram → largest rectangle in histogram `🎯 T2`

01-data-structures/06-queue.md
    ├── BFS queue → rotting oranges · word ladder `⚡ T1`
    └── Deque window max → sliding window maximum `⚡ T1`

01-data-structures/08-tree.md
    ├── DFS In-order → kth smallest in BST `🎯 T2`
    ├── DFS Post-order → diameter · max path sum `🎯 T2`
    ├── BFS level → right side view · level order `⚡ T1`
    └── LCA / validate → lowest common ancestor · validate BST `🎯 T2`

01-data-structures/13-graphs.md
    ├── BFS → shortest path unweighted · walls and gates `⚡ T1`
    ├── DFS → number of islands · pacific atlantic `⚡ T1`
    ├── Topo (Kahn) → course schedule I/II `⚡ T1`
    └── Dijkstra → network delay time `⚡ T1`

01-data-structures/10-heap.md
    ├── Top-K → kth largest · top K frequent `⚡ T1`
    └── Merge K → merge k sorted lists `⚡ T1`

01-data-structures/09-trie.md
    └── Prefix tree → implement trie · word search II `⚡ T1`
```

---

## 02 — Algorithms (study path)

```
02-algorithms/README.md

02-algorithms/03-two-pointers.md
    └── Converging vs same-direction
        ├── Opposite ends → two sum sorted · 3Sum · container water `⚡ T1`
        └── Same direction → remove duplicates · partition `⚡ T1`

02-algorithms/04-sliding-window.md
    └── Variable vs fixed window
        ├── At-most-K distinct → longest substring K distinct `⚡ T1`
        └── Exactly-K trick → subarrays with K different integers `⚡ T1`

02-algorithms/11-binary-search.md
    ├── Standard → search insert position · rotated sorted array `⚡ T1`
    └── Search on answer → koko eating bananas · capacity to ship `⚡ T1`

02-algorithms/00-sorting.md
    └── Reference only [O(n log n) comparison sorts]
        ├── Merge sort → inversion count side-effect `🎯 T2`
        └── Intervals → merge intervals · meeting rooms (with greedy) `🎯 T2`

02-algorithms/14-union-find.md
    └── DSU template [α(n) amortized]
        ├── Cycle → redundant connection · graph valid tree `⚡ T1`
        └── Grouping → accounts merge · number of provinces `⚡ T1`

02-algorithms/16-greedy.md
    └── Local choice + proof sketch
        ├── Intervals → merge · non-overlapping · meeting rooms II `🎯 T2`
        └── Scheduling → jump game · task scheduler `🎯 T2`

02-algorithms/12-backtracking.md
    └── Choose → explore → unchoose
        Subsets · permutations · combination sum · generate parentheses · word search `🎯 T2`

01-data-structures/03-string.md
    └── KMP / rolling hash (know when window fails) `🎯 T2`

02-algorithms/09-recursion.md + 10-recursion-to-dp.md
    └── Recursion → memo → tabulation bridge `🎯 T2`
```

---

## 02 — Dynamic Programming (L3 core)

```
02-algorithms/15-dynamic-programming.md
    │
    ├── UNIVERSAL RECIPE
    │   ├── 1. Recursive brute force (correct base cases)
    │   ├── 2. Memoization (top-down)
    │   ├── 3. Tabulation (bottom-up)
    │   └── 4. Space optimize (rolling row / two vars)
    │
    ├── CHOOSE PATTERN IN 30s
    │   ├── 1D Linear/Fibonacci → house robber · decode ways · climb stairs `🎯 T2`
    │   ├── 0/1 Knapsack       → target sum · partition equal subset `🎯 T2`
    │   ├── Grid DP            → unique paths · min path sum · maximal square `🎯 T2`
    │   ├── LCS family         → edit distance · longest common subsequence `🎯 T2`
    │   ├── String DP          → word break · palindrome partitioning `🎯 T2`
    │   └── Stock state machine → buy/sell with cooldown / fee `🎯 T2`
    │
    └── L3 MUST-SOLVE (from README checklist)
        house robber · coin change · unique paths · edit distance · word break `🎯 T2`
```

---

## 02 — Recursion (L3 core)

```
02-algorithms/09-recursion.md
    │
    ├── BASE CASE CHECKLIST
    │   ├── Empty input (n==0, node==None, i==len(s))
    │   ├── Single element / leaf
    │   └── Constraint met (remaining==0, target found)
    │
    ├── RETURN VALUE DESIGN
    │   ├── Include/Exclude     → subset sum · combination sum `🎯 T2`
    │   ├── Permutations        → permutations · letter case permute `🎯 T2`
    │   ├── Tree/graph DFS      → number of islands · path sum `⚡ T1`
    │   └── Constraint satisfy  → sudoku · N-queens · word search `🎯 T2`
    │
    └── TOP BUGS
        ├── Graph → mark visited BEFORE recurse `⚡ T1`
        └── Always undo mutations after backtrack `🎯 T2`
```

---

## 03 — Patterns & Revision

```
03-patterns/patterns-master.md
    └── Pattern Recognition Master [read before drilling]
        Trigger: sorted + pair sum → Two Pointers `⚡ T1`
        Trigger: contiguous + constraint → Sliding Window `⚡ T1`
        Trigger: dependencies → Topological Sort `⚡ T1`

03-patterns/GOOGLE_INTERVIEW_REVISION.md
    └── Week 4 deep revision (Google lens); Part A = interview-day quick sheet

00-L3-EXECUTION-META/L3_CHEATSHEET.md
    └── Big-O quick reference + gotchas (§6–7)
```

---

## 04 — Behavioral (required at L3)

```
04-behavioral/BEHAVIORAL_GOOGLINESS.md
    ├── STAR story bank (8 stories, coverage-checked)
    └── Four Google attributes — deep dive
        Signal: clarify before coding · own ambiguous work · learn fast · collaborate
```

---

## Practice loop (L3)

```
Weekly cycle
    Mon–Thu → 1 topic file + 2–3 T1 problems timed (35 min)
    Fri       → 1 full mock (45 min) + log misses
    Sat       → redo misses without looking at solutions
    Sun       → 03-patterns/patterns-master.md weak triggers only

Readiness signal (L3)
    ├── Can name pattern in ~60s for README must-solve lists
    ├── Medium problems cold in ~25–35 min with communication
    ├── 4+ mocks logged; failure modes shrinking (not just problem count)
    └── Behavioral stories ready for Googliness round
```

---

_Out of L3 scope (intentionally omitted): segment trees, bit manipulation, advanced graphs, divide & conquer deep-dives, maths, concurrency, SQL, system design, LLD._
