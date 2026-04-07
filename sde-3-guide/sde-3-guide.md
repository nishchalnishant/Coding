# SDE 3 Comprehensive Coding Guide

Welcome to the SDE 3 / Senior Software Engineer Coding Preparation Guide. SDE 3 interviews focus on not just solving the problem, but solving it gracefully while handling edge cases, optimal data structures, and often introducing low-level system design or concurrency elements into the code.

**Deep dive — questions, logic, trickiness:** [TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md](../foundations/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md) (canonical problems by topic with solution logic and gotchas).

---

## 1. Advanced Data Structures & Algorithms (DSA)

Unlike SDE 1/2 interviews, SDE 3 problems often combine topics. You might need a Segment Tree for a sliding window problem or a Trie for a graph traversal problem.

- [Advanced DP Patterns](../patterns/dp-advanced.md)
  - Digit DP, Bitmask DP, Tree DP
- [Advanced Graphs](../advanced-dsa/advanced-graphs.md)
  - Strongly Connected Components (Tarjan), Articulation Points/Bridges.
- [Tries & Segment Trees](../advanced-dsa/trie-segment-trees.md)
  - String manipulation at scale, answering range queries.

---

## 2. Low-Level Design (LLD) Problem Integration

SDE 3 coding rounds often blur the line with Machine Coding / Object Oriented Design. You are expected to write code that is Extensible, Maintainable, and SOLID.

- Examples:
  - Design a Rate Limiter (Token Bucket / Leaky Bucket Implementation)
  - Design an In-Memory File System (Requires heavy use of Tries/Trees and HashMap OOP)
  - Design an LRU / LFU Cache (Combining HashMaps with Doubly Linked Lists)
- **Key Focus**: Use appropriate interfaces (`abstract classes` and `protocols`), encapsulate state, and use threading locks if required.

---

## 3. Concurrency and Multithreading

SDE 3 roles usually require backend or distributed systems expertise where concurrency knowledge is critical.

- [Concurrency Patterns](../concurrency/concurrency-patterns.md)
  - Readers-Writers Lock, Producer-Consumer architecture using wait/notify logic.
  - Avoiding deadlocks and starvation strategies.

---

## 4. Top 20 Curated SDE 3 Focus Problems

Practice these archetypes. For each: **core logic** (what to implement) and **trickiness** (what trips people up).

| # | Problem | Core logic | Trickiness |
|---|---------|------------|------------|
| 1 | **Word Search II** | Trie of words + backtrack on grid; prune if prefix not in trie | Building trie; **time limit** — trie cuts branches; **reuse** same cell in one path only. |
| 2 | **[Alien Dictionary](../google-sde2/PROBLEM_DETAILS.md#alien-dictionary)** | Compare adjacent words → edges between chars; **topological sort** | **Invalid** if cycle; **prefix** pairs give no edge; **all letters** as nodes. |
| 3 | **[Serialize and Deserialize Binary Tree](../google-sde2/PROBLEM_DETAILS.md#serialize-and-deserialize-binary-tree)** | Preorder with `null` markers + queue rebuild (or level-order) | **One canonical** string; **delimiter** for multi-digit values; **empty** tree. |
| 4 | **[LFU Cache](../google-sde2/PROBLEM_DETAILS.md#lfu-cache)** | freq → list of keys; **min_freq** on get/put; LRU within same freq | **O(1)** needs careful struct; **tie** on LRU; increment freq on get. |
| 5 | **[Merge K Sorted Lists](../google-sde2/PROBLEM_DETAILS.md#merge-k-sorted-lists)** | Min-heap of (val, list_id, node); pop min, push next | **O(N log k)** vs **compare all k** each step; **empty** lists. |
| 6 | **[Median of Two Sorted Arrays](../google-sde2/PROBLEM_DETAILS.md#median-of-two-sorted-arrays)** | Binary search **partition** on smaller array; balance left/right sizes | **Indices** vs lengths; **even/odd** total; **binary search** on `i`, derive `j`. |
| 7 | **[Sliding Window Maximum](../google-sde2/PROBLEM_DETAILS.md#sliding-window-maximum)** | Monotonic **deque** of indices (decreasing values) | Pop **front** when out of window; **indices** on deque, not raw values. |
| 8 | **[Trapping Rain Water](../google-sde2/PROBLEM_DETAILS.md#trapping-rain-water)** | Two pointers: `left_max`, `right_max`; or stack | Move **shorter** side; **why** — shorter side caps water. |
| 9 | **Critical Connections** | Tarjan: `disc`, `low`; bridge if `low[v] > disc[u]` | **Undirected** graph; **back edge** vs tree edge; **articulation** vs **bridge** different. |
| 10 | **[Regular Expression Matching](../google-sde2/PROBLEM_DETAILS.md#regular-expression-matching)** | 2D DP: `match[i][j]` for `s[0:i]` vs `p[0:j]`; `*` repeats zero or more | **`*`** = zero of previous **or** match + stay; **empty** string vs `pattern`. |
| 11 | **[Burst Balloons](../google-sde2/PROBLEM_DETAILS.md#burst-balloons)** | Interval DP: open interval `(i,j)`; last balloon `k` in between | **Multiply** `nums[i]*nums[k]*nums[j]` — **sentinel** 1s at ends. |
| 12 | **[The Skyline Problem](../google-sde2/PROBLEM_DETAILS.md#the-skyline-problem)** | Sweep + heap / segment tree / divide by critical x | **Start/end** events; **height** changes; **merge** overlapping buildings. |
| 13 | **[Find Median from Data Stream](../google-sde2/PROBLEM_DETAILS.md#find-median-from-data-stream)** | Two heaps: max (lower) + min (upper); rebalance | **Median** = top of larger or avg of two tops; **balance** sizes after insert. |
| 14 | **Design Search Autocomplete** | Trie + **sort** children by count or heap at node for top-K | **Concurrency**; **prefix**; **update** frequency on search. |
| 15 | **Design Tic-Tac-Toe** | `rows`, `cols`, `diag`, `anti` counts per player; **O(1)** per move | **n×n** generalization; **win** when count hits `n`. |
| 16 | **[Longest Valid Parentheses](../google-sde2/PROBLEM_DETAILS.md#longest-valid-parentheses)** | Stack with **index** base or DP `dp[i]` | Stack stores **indices**; **base** for invalid segment length. |
| 17 | **[Maximum XOR of Two Numbers](../google-sde2/PROBLEM_DETAILS.md#maximum-xor-of-two-numbers)** | Binary trie; **greedy** opposite bit per level | **31 bits** for non-negative; **leading** zeros in trie. |
| 18 | **[Print FooBar Alternately](../google-sde2/PROBLEM_DETAILS.md#print-foobar-alternately)** | Two semaphores (or `Condition`) | **Deadlock** if wrong order; **first** printer must acquire first. |
| 19 | **Dining Philosophers** | Pick **lowest chopstick id first** or **waiter** semaphore | **Circular wait** = deadlock; **asymmetric** ordering breaks cycle. |
| 20 | **[Reconstruct Itinerary](../google-sde2/PROBLEM_DETAILS.md#reconstruct-itinerary)** | Hierholzer: **Eulerian path** — sort edges lexicographically; **post-order** DFS | **JFK** start; **lexicographic** smallest; **multi-edge** tickets; **reverse** order at end. |

---

## Related

- [Foundations](../foundations/README.md) — full topic notes  
- [SDE3_DSA_ROADMAP.md](../SDE3_DSA_ROADMAP.md) — practice order  
- [GOOGLE_INTERVIEW_REVISION.md](../foundations/GOOGLE_INTERVIEW_REVISION.md) — focused revision  
