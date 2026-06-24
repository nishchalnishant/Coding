---
tags: [algorithms, sde3, dsa, completeness, audit]
topic: SDE-3 DSA Completeness Addendum
difficulty: reference
---

# SDE-3 DSA Completeness Addendum — Algorithms

This note captures the algorithm-side gaps that often separate a solid L4 candidate from someone who is ready to handle harder Google-style follow-ups.

> [!important] SDE-3 bar for algorithms
> You should be able to:
> - map the problem to a known family quickly,
> - justify the recurrence or greedy choice,
> - prove correctness at a high level,
> - and know the standard optimization or follow-up variant.

---

## What this folder already covers well

- Search, recursion, divide-and-conquer, backtracking, greedy, DP, bit manipulation, union-find, graph algorithms, string algorithms, and advanced graph variants.
- Important communication patterns: constraint-first thinking, complexity derivation, and follow-up awareness.
- Several “deep dive” files already go past the minimum and are good SDE-3 prep material.

## What is often still missing at SDE-3 level

- **Advanced graph depth**: Tarjan bridges/articulation points, SCCs, Eulerian path, 0-1 BFS, bidirectional BFS, shortest path on DAGs, Floyd-Warshall.
- **DP depth**: state compression, bitmask DP, interval DP, tree DP returning tuples, and reconstruction variants.
- **Binary search depth**: binary search on answer, monotonic predicate design, lower/upper bound semantics.
- **Greedy depth**: exchange argument, stays-ahead proof, and knowing when to switch to DP.
- **String depth**: KMP, Z-function, Rabin-Karp, Aho-Corasick, suffix array, rolling hash caveats.
- **Bit depth**: submask enumeration, XOR basis, mask transitions, and `n <= 20` exponential-feasible thinking.

---

## Canonical follow-up questions

### Graphs

1. Can you detect bridges and articulation points?
2. Can you find SCCs and reason about the condensation graph?
3. Can you solve shortest path with 0/1 weights without a heap?
4. Can you do shortest path on DAGs in linear time?

### DP / recursion

1. Can you define the state cleanly before writing code?
2. Can you move from memoization to bottom-up tabulation?
3. Can you optimize a DP to O(n) or O(1) space?
4. Can you reconstruct the actual solution, not just the score?

### Greedy / search

1. Can you prove the greedy choice is safe?
2. Can you state the monotonic predicate for binary search on answer?
3. Can you tell greedy apart from interval DP?

### Strings / bits

1. Can you match many patterns in one pass?
2. Can you explain suffix-order problems?
3. Can you enumerate submasks without extra memory?

---

## Missing-content checklist

- Say why the obvious brute-force fails.
- Name the invariant or predicate.
- Derive the complexity of each sub-step, not just the headline.
- Know the edge cases: empty input, duplicates, negative values, disconnected graphs, and overflow.
- Be able to give a cleaner or faster follow-up if asked.

---

## Where to read next

- `graph.md`
- `advanced-graphs.md`
- `dynamic-programming.md`
- `recursion-to-dp.md`
- `backtracking.md`
- `greedy.md`
- `binary-search.md`
- `string.md`
- `bit-manipulation.md`

## Final bar

If you can identify the family, prove the transition/choice, and handle the follow-up variant under pressure, you are at the right algorithm level for an SDE-3 DSA interview.
