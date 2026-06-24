---
tags: [coding, amazon-sde2, dsa, completeness, checklist]
topic: Amazon SDE-2 DSA Completeness Checklist
difficulty: reference
---

# Amazon SDE-2 DSA Completeness Checklist

Use this to audit your readiness before an Amazon SDE-2 loop. Check off topics you can solve cold (no reference) in under 25 minutes with clean, bug-free code.

---

## Arrays & Strings

- [ ] Two-pointer (opposite ends): two sum sorted, 3Sum, container with most water
- [ ] Sliding window (variable): longest substring without repeat, minimum window substring
- [ ] Sliding window (fixed): max sum subarray of size k
- [ ] Prefix sums: subarray sum equals k, range sum query
- [ ] Kadane's algorithm: maximum subarray
- [ ] In-place array tricks: rotate array, move zeroes, remove duplicates
- [ ] String: anagram check, group anagrams, valid palindrome
- [ ] Sorting tricks: sort colors (Dutch flag), merge intervals, meeting rooms

---

## Linked Lists

- [ ] Fast/slow pointers: cycle detection (Floyd's), find cycle start
- [ ] Reversal: reverse linked list (iterative + recursive), reverse k-group
- [ ] Merge: merge two sorted lists, merge k sorted lists
- [ ] Runner technique: find middle, reorder list
- [ ] LRU Cache: doubly linked list + hash map, O(1) get/put

---

## Stacks & Queues

- [ ] Monotonic stack: next greater element, largest rectangle in histogram, daily temperatures
- [ ] Valid parentheses and variants
- [ ] Min stack (O(1) getMin)
- [ ] Monotonic deque: sliding window maximum
- [ ] BFS queue patterns (separate from graph section below)

---

## Hash Maps / Hash Sets

- [ ] Frequency map: top K frequent elements, first unique character
- [ ] Complement lookup: two sum, four sum
- [ ] Grouping: group anagrams, isomorphic strings
- [ ] Sliding window with hash map: longest substring with k distinct characters

---

## Trees

- [ ] All four traversals: preorder, inorder, postorder (iterative + recursive), level-order BFS
- [ ] Path problems: max path sum, path sum II (root to leaf), diameter of binary tree
- [ ] LCA: lowest common ancestor of binary tree and BST
- [ ] BST: validate BST, kth smallest in BST, BST insert/delete
- [ ] Construction: build tree from preorder+inorder, serialize/deserialize
- [ ] Tree DP: house robber III, maximum goods (rob tree)

---

## Heaps / Priority Queues

- [ ] Top-K elements (min-heap of size k)
- [ ] K-way merge: merge k sorted lists, smallest range covering k lists
- [ ] Kth largest/smallest: kth largest in array, kth smallest in sorted matrix
- [ ] Median of data stream (two heaps: max-heap + min-heap)
- [ ] Task scheduler (greedy + heap)

---

## Tries

- [ ] Insert and search words
- [ ] Starts-with (prefix) check
- [ ] Word search II (trie + backtracking)
- [ ] Replace words (trie for dictionary lookups)

---

## Graphs

- [ ] Representations: adjacency list, adjacency matrix
- [ ] BFS: shortest path unweighted, word ladder, 01 matrix (multi-source BFS)
- [ ] DFS: number of islands, flood fill, connected components
- [ ] Topological sort (Kahn's BFS and DFS): course schedule, alien dictionary
- [ ] Dijkstra's: network delay time, cheapest flights within k stops
- [ ] Union-Find: number of connected components, redundant connection, accounts merge
- [ ] Cycle detection: directed (DFS with states) and undirected (Union-Find or DFS)

---

## Dynamic Programming

- [ ] 1D DP: climbing stairs, house robber, coin change, decode ways
- [ ] 2D DP: unique paths, edit distance, longest common subsequence
- [ ] Knapsack: 0/1 knapsack, coin change II (unbounded)
- [ ] LIS: longest increasing subsequence (O(n²) DP + O(n log n) with binary search)
- [ ] String DP: palindromic substrings, longest palindromic subsequence
- [ ] Interval DP: burst balloons (awareness — rare at SDE-2)
- [ ] DP with states: jump game II, best time to buy and sell stock with cooldown

---

## Backtracking

- [ ] Subsets (with and without duplicates)
- [ ] Permutations (with and without duplicates)
- [ ] Combinations (combination sum I and II)
- [ ] N-Queens (conceptual understanding)
- [ ] Word search (grid backtracking)
- [ ] Palindrome partitioning

---

## Binary Search

- [ ] Standard: binary search, search in rotated sorted array, find minimum in rotated array
- [ ] Binary search on answer: koko eating bananas, capacity to ship packages, split array largest sum
- [ ] 2D binary search: search a 2D matrix

---

## Greedy

- [ ] Interval greedy: merge intervals, non-overlapping intervals, meeting rooms II
- [ ] Jump game (I and II)
- [ ] Gas station
- [ ] Task scheduler

---

## Bit Manipulation (Awareness-level)

- [ ] XOR tricks: find single number, missing number
- [ ] Bit masking: count bits, power of two, hamming distance
- [ ] Subsets via bitmask (n ≤ 20)

---

## System Design (SDE-2 Scope)

- [ ] URL shortener: Base62 encoding, Redis cache, KV store
- [ ] Rate limiter: token bucket, sliding window counter, Redis atomic ops
- [ ] Simple feed: fan-out on write vs read, Redis sorted set for timeline
- [ ] Distributed cache: Redis cluster, eviction policies (LRU/LFU/TTL), cache stampede
- [ ] Framework: requirements → capacity → high-level → deep dive → scale → tradeoffs

---

## Readiness Bar

You are ready for an Amazon SDE-2 coding loop when you can:
- Solve any Tier 1 topic above cold in ≤ 20 minutes with correct edge case handling
- State time and space complexity before writing code
- Handle empty input, single element, duplicates, overflow (mention INT_MIN/MAX where relevant)
- Optimize from brute force to optimal when asked without prompting

---

## See Also

- `amazon-sde2/` — full Amazon interview track
- `coding/patterns-quick-reference.md` — code templates
- `coding/complexity-cheatsheet.md` — complexity reference
- `coding/behavioral-interview.md` — Amazon Leadership Principles guide
