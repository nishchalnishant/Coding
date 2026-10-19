---
module: striver/32-beyond-the-sheet
topic: Beyond the sheet
tags: [striver, beyond-sheet, enrichment]
---
# Part 32: Beyond the Sheet

← [Striver course map](../README.md)

> [!abstract] What this part covers
> **Goal:** Close the gaps between the A2Z sheet and the hardest DSA rounds. Covers range-query structures, advanced DP families, LCA/Euler-tour/Eulerian-path graph tools, and the cross-cutting techniques (meet in the middle, sweep line, reservoir sampling, randomisation, data-structure design).
> **Prereqs:** Parts 14, 24, 27 and 28. **Time:** ~4 h.
> **Outcome:** Pick and write a Fenwick tree, sparse table or lazy segment tree on demand; spot bitmask, digit, tree and rerooting DP; answer LCA and subtree queries in O(log n); and recognise the trigger for each toolbox technique.
>
> **Not part of Striver's course.** This is original enrichment, so there are no source links. Treat it as the last layer after the sheet is done.

---

## Theory

| # | Lesson | What you get | Source |
|---|---|---|---|
| 1 | [Range Queries](01-range-queries-theory.md) | A chooser flowchart; prefix/difference/2D prefix; sparse table; Fenwick (inversions, range add, two BITs); segment tree templates with custom merges; lazy propagation; offline tricks (compression, Mo's, sqrt decomposition). | — |
| 2 | [Advanced DP](02-advanced-dp-theory.md) | Family recognition; bitmask DP (TSP, assignment, submask enumeration); the digit-DP template; tree DP states; rerooting (sum of distances); expected-value DP; optimisation tricks. | — |
| 3 | [Advanced Trees and Graphs](03-advanced-trees-and-graphs-theory.md) | Binary lifting (k-th ancestor, LCA); an LCA method comparison; Euler tour subtree ranges; Hierholzer Eulerian paths (Reconstruct Itinerary); 0-1, multi-source, state, bidirectional and A* BFS. | — |
| 4 | [Techniques Toolbox](04-techniques-toolbox-theory.md) | Meet in the middle, sweep line (rooms, skyline), coordinate compression, reservoir sampling, Fisher–Yates and other randomisation, streaming structures, O(1) design recipes (LRU, LFU, GetRandom). | — |

---

## Signature problems

| Problem | Lesson | Key insight |
|---|---|---|
| Range Sum Query – Mutable (LC 307) | 1 | Fenwick or segment tree with point updates |
| Count of Smaller Numbers After Self (LC 315) | 1 | Compress the values, scan right to left with a BIT |
| My Calendar III (LC 732) | 1 / 4 | Sweep with a sorted map, or a dynamic segment tree |
| Shortest Path Visiting All Nodes (LC 847) | 2 | BFS over (node, mask) |
| Numbers With Repeated Digits (LC 1012) | 2 | Digit DP with a used-digit mask, then take the complement |
| Sum of Distances in Tree (LC 834) | 2 | Rerooting: `ans[c] = ans[p] − sz[c] + n − sz[c]` |
| Kth Ancestor of a Tree Node (LC 1483) | 3 | Binary lifting |
| Reconstruct Itinerary (LC 332) | 3 | Hierholzer with a min-heap adjacency |
| Minimum Cost to Make at Least One Valid Path (LC 1368) | 3 | 0-1 BFS |
| Closest Subsequence Sum (LC 1755) | 4 | Meet in the middle |
| The Skyline Problem (LC 218) | 4 | Sweep plus a max-heap of active heights |
| Insert Delete GetRandom O(1) (LC 380) | 4 | Array plus an index map, swap-delete |

---

## Part 32 cheat sheet

| Trigger | Tool |
|---|---|
| Static range sum | Prefix sum |
| Static range min/max | Sparse table |
| Point update + range sum | Fenwick |
| Range update + range query | Lazy segment tree |
| n ≤ 20 with "which used" | Bitmask DP |
| Count in [L, R] up to 10¹⁸ by digits | Digit DP |
| Answer for every root | Rerooting |
| Many LCA / k-th ancestor queries | Binary lifting |
| Subtree queries | Euler tour + BIT |
| Use every edge once | Hierholzer |
| 0/1 edge weights | 0-1 BFS |
| n ≈ 40 subset search | Meet in the middle |
| Interval overlaps | Sweep line |
| Uniform sample from a stream | Reservoir |
