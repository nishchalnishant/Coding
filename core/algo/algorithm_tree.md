# Algorithm Tree — SDE-3 Master Index

A hierarchical map of core algorithms, their underlying patterns, and high-yield interview variants. This tree serves as a rapid revision guide for senior-level algorithmic mastery.

---

## 1. Sorting & Partitioning
- **Merge Sort (Divide & Conquer)** — Recursive halving and merging; the standard for stable sorting and inversion counting.
    - *Variants:* Count of Range Sum, Reverse Pairs, Global Inversions.
- **Quick Sort (Partitioning)** — Pivot-based partitioning; optimized for in-place sorting and cache efficiency.
    - *Variants:* Pancake Sorting, In-place partitioning.
- **QuickSelect (Kth Order Statistic)** — Partitioning-based selection; finds the k-th smallest element in O(N) average time.
    - *Variants:* K Closest Points to Origin, Top K Frequent Elements.
- **Dutch National Flag (3-Way Partition)** — 3-way partitioning to group three distinct values or handle duplicate pivots.
    - *Variants:* Sort Colors, Move Zeroes, Sort Transformed Array.
- **Non-Comparison Sorts (Bucket/Radix/Counting)** — Distribution-based sorting for specific data ranges; achieves O(N) in optimal conditions.
    - *Variants:* Maximum Gap (Bucket Sort), Sort Characters By Frequency.
- **Custom Comparators** — User-defined sorting logic for complex objects or string-based number ordering.
    - *Variants:* Largest Number, Custom Sort String, Queue Reconstruction by Height.

## 2. Searching & Binary Search
- **Binary Search (Template Variants)** — Logarithmic search in sorted spaces using low/high pointers and mid-point logic.
    - *Patterns:* Left-most vs Right-most insertion point.
- **Binary Search on Answer (Optimization)** — Searching the range of possible solutions when the "is possible" function is monotonic.
    - *Variants:* Kth Smallest in Sorted Matrix, Capacity to Ship Packages, Split Array Largest Sum.
- **Searching in Rotated Arrays** — Modified binary search that identifies which half is sorted to find targets or pivots.
    - *Variants:* Search in Rotated Sorted Array I & II, Find Minimum in Rotated Sorted Array.
- **Median Finding** — Advanced partitioning or binary search on value range to find the middle element of combined sets.
    - *Variants:* Median of Two Sorted Arrays (O(log(min(N,M)))).
- **2D Grid Search** — Efficient matrix traversal leveraging row/column sorting or binary search.
    - *Variants:* Search a 2D Matrix I (Sorted list) & II (Step-wise elimination).

## 3. Strings & Pattern Matching
- **KMP (LPS Table)** — Pattern matching using a failure function to skip unnecessary comparisons in O(N+M).
    - *Variants:* strStr(), Shortest Palindrome (LPS of `s + # + rev(s)`), Repeated Substring Pattern.
- **Rabin-Karp (Rolling Hash)** — Hash-based matching; constant time window updates enable efficient multi-pattern search.
    - *Variants:* Longest Duplicate Substring (Binary Search + Hash), Distinct Echo Substrings.
- **Palindrome Expand Center** — Generating palindromes by expanding from 2N-1 centers; avoids the O(N³) brute force.
    - *Variants:* Longest Palindromic Substring, Palindrome Partitioning II, Count Palindromic Substrings.
- **Sliding Window** — Dynamic window boundary management to find contiguous segments meeting character/sum constraints.
    - *Variants:* Minimum Window Substring, Longest Substring with At Most K Distinct, Permutation in String.
- **Z-Algorithm** — Linear time matching based on prefix-matching lengths at each position.
    - *Variants:* Longest Happy Prefix, Pattern Matching.
- **Trie (Prefix Tree)** — Hierarchical retrieval of strings; optimizes prefix-based lookups and dictionary search.
    - *Variants:* Word Search II, Map Sum Pairs, Stream of Characters (Reverse Trie).

## 4. Union-Find (Disjoint Set Union)
- **Standard DSU (Path Compression + Rank)** — Near-constant time connectivity tracking and set merging.
    - *Variants:* Number of Provinces, Longest Consecutive Sequence.
- **Kruskal's MST** — Greedy edge selection for minimum spanning trees; uses sorting and DSU for cycle detection.
    - *Variants:* Min Cost to Connect All Points, Critical and Pseudo-Critical Edges in MST.
- **Weighted DSU (Ratio Tracking)** — DSU variant that maintains relationships or weights (e.g., ratios) relative to the root.
    - *Variants:* Evaluate Division, Path with Maximum Probability.
- **DSU with Rollback** — DSU optimized for undoing operations, typically used in offline dynamic connectivity.
    - *Variants:* Number of Islands II (Dynamic additions), Offline Dynamic Connectivity.

## 5. Dynamic Programming
- **Linear DP (1D)** — Optimization over a sequence where the current state depends on a fixed number of previous states.
    - *Variants:* Fibonacci, House Robber, Decode Ways, Min Cost For Tickets.
- **Knapsack Family** — Optimization problems involving item selection under capacity or budget constraints.
    - *0/1 Knapsack:* Target Sum, Partition Equal Subset Sum.
    - *Unbounded Knapsack:* Coin Change I & II.
    - *Partitioning:* Partition to K Equal Sum Subsets (Bitmask).
- **Longest Common Subsequence (LCS)** — Pairwise sequence alignment to find shared non-contiguous structure.
    - *Variants:* Edit Distance, Shortest Common Supersequence, Min ASCII Delete Sum.
- **Interval DP** — Optimization over sub-ranges `[i, j]`, often involving merging or splitting segments.
    - *Variants:* Burst Balloons, Matrix Chain Multiplication, Triangulation of Polygon.
- **Bitmask DP (N ≤ 20)** — Subset-state tracking using integers as bitsets to solve NP-Hard problems for small N.
    - *Variants:* Traveling Salesperson (TSP), Can I Win.
- **Digit DP** — Counting numbers in a range `[L, R]` that satisfy specific digit-level properties.
    - *Variants:* Numbers At Most N Given Digit Set, Non-negative Integers without Consecutive Ones.
- **Tree DP** — Propagation of state from leaves to root (postorder) to optimize selections on tree structures.
    - *Variants:* Binary Tree Maximum Path Sum, House Robber III.
- **State Machine DP** — DP where transitions occur between distinct operational modes (e.g., CoolDown).
    - *Variants:* Best Time to Buy/Sell Stock (Unlimited, Cooldown, Fee).

## 6. Recursion & Backtracking
- **Structural Recursion** — Processing data structures by delegating work to their self-similar sub-parts (trees, lists).
    - *Variants:* Lowest Common Ancestor (LCA), Flatten Binary Tree to Linked List.
- **Memoized Recursion (Top-Down)** — Recursion with a cache to solve overlapping subproblems efficiently.
    - *Variants:* Unique Paths II, Word Break.
- **Iterative Recursion (Explicit Stack)** — Mimicking the call stack with a list to avoid recursion limits and improve control.
    - *Variants:* Level Order Traversal, Clone Graph.
- **Graph DFS** — Deep exploration of paths; the foundation for reachability, cycles, and topological sorting.
    - *Variants:* Flood Fill, Pacific Atlantic Water Flow, Topological Sort.
- **Constrained Generation (Backtracking)** — Systematic search with "choose, recurse, undo" to find valid states or combinations.
    - *Variants:* Generate Parentheses, Word Search, N-Queens, Combination Sum I & II.

## 7. Greedy Algorithms
- **Interval Scheduling** — Greedy selection of non-overlapping intervals, usually optimized by end-time sorting.
    - *Variants:* Merge Intervals, Non-overlapping Intervals, Minimum Number of Arrows to Burst Balloons.
- **Jump Game** — Reaching a target by tracking the maximum reachable range at each step.
    - *Variants:* Jump Game I (Can reach?) & II (Min jumps?).
- **Resource Management** — Optimizing distribution or consumption of finite resources.
    - *Variants:* Gas Station, Task Scheduler, Candy.

## 8. Mathematics & Bit Manipulation
- **Number Theory**
    - *Variants:* Sieve of Eratosthenes, Prime Factorization, GCD (Euclidean), Fast Exponentiation.
- **Bit Manipulation**
    - *Variants:* Counting Bits, Single Number I & II, Maximum XOR of Two Numbers.

---

## How to use this tree
1. **Identify the Core**: When given a problem, map it to a top-level branch (e.g., "This is a grid problem with path counting → Dynamic Programming").
2. **Find the Pattern**: Drill down to the pattern (e.g., "I move right/down → Grid DP").
3. **Apply the Twist**: Match the variant (e.g., "There are obstacles → Unique Paths II").
4. **Recall the Click Moment**: Use the specific "Click Moment" logic from the individual module files to jump straight to the optimal recurrence or data structure.
