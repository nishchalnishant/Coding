---
module: 02-algorithms
topic: Algorithm Tree
subtopic: 
status: unread
tags: [algorithms, algorithm-tree]
---

← [Algorithms index](./README.md) · 🗺 [Master Decision Guide](../00-L3-EXECUTION-META/DECISION_GUIDE.md)
## First-Principles Map

```text
WHY systematic algorithm selection beats intuition
├── Under interview pressure, intuition produces the most recently seen algorithm
│   ├── Not necessarily the right one — leads to brute force or wrong complexity
│   └── Trial-and-error wastes 10-15 minutes on wrong family before pivoting
├── A systematic map gives deterministic O(1) family selection from problem signal
└── SDE-3 expectation: name the algorithm family and its complexity before coding starts
│
WHAT the strategic algorithm families are
├── Sort / Partition  — O(n log n); prerequisite for two-pointer, binary search, greedy
├── Search            — binary search O(log n); BFS O(V+E); Dijkstra O((V+E) log V)
├── Strings           — KMP / Z-function O(n); rolling hash O(n); trie O(L·n)
├── Union-Find        — O(α) per op; dynamic connectivity, Kruskal, redundancy
├── Dynamic Prog.     — O(n²) to O(n·k); memoize or tabulate; count / optimize
├── Backtracking      — O(k^n) worst case; prune aggressively; all valid states
├── Greedy            — O(n log n) with sort; exchange argument must hold
├── Math / Bits       — O(1) or O(log n); number theory, bit manipulation, modular
├── Concurrency       — lock/semaphore discipline; producer-consumer, readers-writers
└── Distributed       — Raft/Paxos consensus; consistent hashing; vector clocks
│
HOW to map a problem to a family in seconds
├── Core question → family
│   ├── "Has dependency ordering?"              → Topological sort (Kahn's / DFS)
│   ├── "Optimize with overlapping choices?"    → DP (define state, write recurrence)
│   ├── "Need ALL valid configurations?"        → Backtracking + pruning
│   ├── "Local choice provably global optimal?" → Greedy (prove exchange argument)
│   ├── "Connected / path / reachability?"      → Graph BFS/DFS/Dijkstra
│   ├── "Dynamic connectivity / merge sets?"    → Union-Find
│   ├── "Sorted input / search for target?"     → Binary search (value or answer space)
│   ├── "Pattern in string?"                    → KMP / Z-function / rolling hash
│   └── "Counting / modular arithmetic?"        → Math (combinatorics, Fermat's little theorem)
├── Complexity budget → family
│   ├── O(n) needed (n=10^6)     → Two pointers / sliding window / prefix sum
│   ├── O(n log n) (n=10^5)      → Sort + scan / heap / binary search / BFS
│   ├── O(n²) acceptable (n=10³) → DP / backtracking with strong pruning
│   └── O(2^n) only (n≤20)       → Full backtracking / bitmask DP
│
WHEN to upgrade from brute force
├── O(n²) nested loop → O(n log n) with sort + two pointers (pair sum, closest)
├── O(n²) repeated scan → O(n) with sliding window (max subarray, longest substring)
├── O(2^n) recursion → O(n²) with DP memoization (fibonacci, coin change)
├── O(n²) connectivity → O(n·α) with Union-Find (dynamic component queries)
└── O(n·L) string search → O(n+L) with KMP / Z-function (pattern matching)
│
WHAT CAN GO WRONG
├── DP when greedy suffices          → O(n²) for activity selection (should be O(n log n))
├── Backtracking when DP needed      → O(2^n) for edit distance (should be O(n·m))
├── BFS for weighted shortest path   → wrong answer (unweighted only); use Dijkstra
├── Greedy without exchange proof    → wrong on coin change with arbitrary denominations
├── Topo sort ignoring cycle check   → infinite loop or missed impossible case
├── Missing memoization key          → duplicate subproblem work → TLE
└── Wrong recurrence direction       → bottom-up built in wrong order → incorrect DP
│
DECISION — problem signal → algorithm family
├── Dependency order / DAG                → Topological sort
├── Overlapping subproblems + optimize    → DP (memoize or tabulate)
├── All valid states / exhaustive         → Backtracking (+ pruning)
├── Local greedy provably optimal         → Greedy (sort first, exchange arg)
├── Unweighted shortest path              → BFS
├── Weighted shortest path                → Dijkstra / Bellman-Ford
├── Dynamic merge / connectivity          → Union-Find
├── Sorted + search / minimize max        → Binary search (on value or answer space)
├── String pattern / substring            → KMP / Z / rolling hash / trie
└── Count modulo / combinatorics          → Math (nCr, Fermat, modular inverse)
```

## First-Principles Breakdown

- **Root problem:** Under pressure, the human brain defaults to recently seen solutions — a systematic strategic map replaces pattern-matching with deterministic family selection from problem signals.
- **Core insight:** Each algorithm family exploits exactly one structural property (optimal substructure → DP; exchange argument → greedy; adjacency → graph; monotonicity → binary search); the family is invalid without that property.
- **Invariant:** Problem signal (dependency, optimization, exhaustive, connectivity, sorted) maps 1-to-1 to an algorithm family; constraint size (n ≤ 20 vs 10^5) narrows to the specific variant within the family.
- **Why it works:** Templates encode proven solutions with known correctness guarantees and complexity bounds — the only work is identifying the match and applying the problem-specific twist.
- **Where it breaks:** Applying backtracking on DP problems produces exponential solutions; applying greedy without a valid exchange argument produces wrong answers — both are unrecoverable within the interview window.

# The Algorithm Tree: Your Strategic Map

> [!note] L3 Reference Document
> This file is a **reference / meta document** — read it once, use it as a lookup.
> Not a coding practice file. Do not deep-study it like a topic file.


If the Data Structure Tree was your "Toolkit," this is your **"Battle Plan."** Most candidates panic because they try to solve every problem from scratch. We don't do that. We recognize the **Pattern**, apply the **Template**, and then handle the **Twist.**

When you're reading a problem, I want you to ask: "Is this a **Dependency** problem? (Topo Sort)" or "Is this an **Optimization** problem with overlapping parts? (DP)". This tree is your index for mapping a vague interview question to a concrete logical trigger.

---

## 1. Sorting & Partitioning

→ [sorting.md](./00-sorting.md) · [divide-and-conquer.md](./18-divide-and-conquer.md)
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

→ [binary-search.md](./11-binary-search.md)
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

→ [string.md](./02-string.md) · [sliding-window.md](./04-sliding-window.md) · [trie.md](../01-data-structures/09-trie.md)
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

→ [union-find.md](./14-union-find.md)

- **Standard DSU (Path Compression + Rank)** — Near-constant time `O(α(N))` per operation for connectivity tracking and set merging. Essential for dynamic connectivity and detecting cycles in undirected graphs.
    - *Variants:* Number of Provinces, Longest Consecutive Sequence, Redundant Connection, Accounts Merge.
- **Kruskal's MST** — Greedy edge selection for minimum spanning trees. Sorts edges by weight and uses DSU to safely connect nodes without forming cycles. Time complexity `O(E log E + E α(V))`.
    - *Variants:* Min Cost to Connect All Points, Critical and Pseudo-Critical Edges in MST.
- **Weighted DSU (Ratio/Parity Tracking)** — A specialized DSU that maintains relationship values (e.g., ratios, distance, parity) between a node and its root. Used for equations and consistency checks.
    - *Variants:* Evaluate Division, Is Graph Bipartite? (Using DSU), Satisfiability of Equality Equations.
- **DSU with Rollback** — DSU variant for undoing operations. Used in offline queries or backtracking. Drops path compression (uses only Union by Rank/Size) to maintain a strict tree structure for `O(log N)` rollback.
    - *Variants:* Number of Islands II (Dynamic additions grid), Offline Dynamic Connectivity.

## 4b. Graph Traversal & Shortest Path

→ [graph.md](./13-graph.md) · [graphs.md](../01-data-structures/13-graphs.md) · [recursion/graph-recursion.md](./recursion/graph-recursion.md)

- **Breadth-First Search (BFS)** — Shortest path on unweighted graphs. Explore level-by-level. Mark nodes visited *before* enqueueing to prevent exponential blow-up.
    - *Variants:* Word Ladder, Shortest Path in Binary Matrix, Rotting Oranges (Multi-source BFS).
- **Depth-First Search (DFS)** — Recursively explore to the deepest nodes. Used for connected components, Topological Sorting, and cycle detection (3-Color states).
    - *Variants:* Clone Graph, Course Schedule (Cycle Detection), Pacific Atlantic Water Flow.
- **Dijkstra's Algorithm** — Shortest path on weighted graphs with non-negative edges. Uses a Min-Heap `(distance, node)` and relaxes edges greedily. Time `O((V+E) log V)`.
    - *Variants:* Network Delay Time, Path With Minimum Effort.
- **Bellman-Ford Algorithm** — Shortest path allowing negative edges or enforcing a maximum number of steps `K`. Requires snapshotting distances across `K+1` rounds.
    - *Variants:* Cheapest Flights Within K Stops.

## 5. Dynamic Programming

→ [dynamic-programming.md](./15-dynamic-programming.md) · [recursion-to-dp.md](./15-recursion-to-dp.md)
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
    - *Variants:* Numbers At Most N Given Digit Set, Non-negative Integers without Consecutive Ones.
- **Tree DP** — Propagation of state from leaves to root (postorder) to optimize selections on tree structures.
    - *Variants:* Binary Tree Maximum Path Sum, House Robber III.
- **State Machine DP** — DP where transitions occur between distinct operational modes (e.g., CoolDown).
    - *Variants:* Best Time to Buy/Sell Stock (Unlimited, Cooldown, Fee).

## 6. Recursion & Backtracking

→ [recursion.md](./15-recursion.md) · [backtracking.md](./12-backtracking.md)
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

→ [greedy.md](./16-greedy.md)
- **Interval Scheduling** — Greedy selection of non-overlapping intervals, usually optimized by end-time sorting.
    - *Variants:* Merge Intervals, Non-overlapping Intervals, Minimum Number of Arrows to Burst Balloons.
- **Jump Game** — Reaching a target by tracking the maximum reachable range at each step.
    - *Variants:* Jump Game I (Can reach?) & II (Min jumps?).
- **Resource Management** — Optimizing distribution or consumption of finite resources.
    - *Variants:* Gas Station, Task Scheduler, Candy.

## 8. Mathematics & Bit Manipulation

→ [maths.md](./17-maths.md) · [bit-manipulation.md](./17-bit-manipulation.md)
- **Number Theory**
    - *Variants:* Sieve of Eratosthenes, Prime Factorization, GCD (Euclidean), Fast Exponentiation.
- **Bit Manipulation**
    - *Variants:* Counting Bits, Single Number I & II, Maximum XOR of Two Numbers.

## 9. Concurrency & Parallelism

- **Producer-Consumer** — Synchronization between data sources and sinks using bounded buffers and semaphores.
- **Read-Write Locking** — Optimizing for high-read throughput while ensuring exclusive write access.
- **Barrier/Phaser Synchronization** — Multi-threaded coordination where threads must wait at specific checkpoints.

## 10. System Design Algorithms (Distributed Scale)

- **Consistent Hashing** — Distributed data partitioning that minimizes reshuffling during node churn.
- **Rate Limiting (Token/Leaky Bucket)** — Algorithms for flow control and protecting systems from traffic bursts.
- **Consensus (Raft/Paxos)** — Reaching agreement across unreliable distributed nodes for leader election and state replication.
- **Sketching (Count-Min Sketch)** — Frequency estimation in high-volume data streams (e.g., trending hashtags).

---

## How to use this tree
1. **Identify the Core**: When given a problem, map it to a top-level branch (e.g., "This is a grid problem with path counting → Dynamic Programming").
2. **Find the Pattern**: Drill down to the pattern (e.g., "I move right/down → Grid DP").
3. **Apply the Twist**: Match the variant (e.g., "There are obstacles → Unique Paths II").
4. **Recall the Click Moment**: Use the specific "Click Moment" logic from the individual module files to jump straight to the optimal recurrence or data structure.
