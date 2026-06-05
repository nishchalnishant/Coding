---
module: 03-patterns
topic: Patterns Master
subtopic: 
status: unread
tags: [patterns, patterns-master]
---
## First-Principles Map

```
WHY pattern recognition → WHAT it is → HOW it works → WHEN to use → WHAT can go wrong
       │                       │               │               │               │
  [Interviews don't test      [mapping         [scan problem   [identify in    [forcing a
   memorized solutions —       problem signals   statement for   first 2 mins:   pattern that
   they test the ability       to algorithm      trigger words   sorted? → BS;   doesn't fit;
   to map unfamiliar           families using    + constraints;  contiguous? →   using sliding
   problems to known           trigger signals   match to        sliding window; window when
   structures; without         and constraint    pattern family; graph? → BFS;   no window
   a pattern taxonomy,         analysis]         apply template; dynamic? → DP]  constraint;
   every problem feels new]                      adapt details]                  DP when greedy
                                                                                 suffices]
       │                       │               │
  [real-world:                [pattern         [Two-pointer: sorted array,
   doctor pattern              categories:      pair/triplet sum, palindrome;
   matching symptoms to        two-pointer,     Sliding window: max/min in
   diseases; chess master       sliding window,  subarray/substring; monotonic
   recognizing board            binary search,   stack: next greater element;
   positions]                  BFS/DFS, DP,     union-find: connected components;
                               greedy, union-   heap: top-K, median stream]
                               find, heap]
       ↓
[Decision: Which pattern for which signal]
  ├── "Sorted array, find pair"    → Two pointers
  ├── "Contiguous subarray max"    → Sliding window
  ├── "Shortest path"              → BFS (unweighted) / Dijkstra (weighted)
  ├── "Count/min/max ways"         → DP (optimal substructure)
  ├── "Connected groups"           → Union-Find or DFS
  └── "Top K / K smallest"         → Heap (priority queue)
```

## First-Principles Breakdown
- **Root problem**: Every problem in isolation looks unique; pattern taxonomy converts "novel problem" into "known template + small adaptation."
- **Core insight**: Problems share structural signatures (sorted input, contiguous subarray, graph edges, optimal substructure) — these signals map reliably to algorithm families.
- **Invariant**: A correctly identified pattern always reduces the problem to a known time complexity; misidentified patterns waste interview time backtracking.
- **Why it's fast**: Template code for each pattern is 10-30 lines; adapting it to a specific problem is faster than deriving from scratch.
- **Where it breaks**: Over-fitting to pattern — forcing DP on a greedy problem adds unnecessary O(n²) complexity; pattern recognition fails when the problem is a composition of two patterns simultaneously.

# Pattern Recognition Master Guide

> [!note] L3 Reference Document
> This file is a **reference / meta document** — read it once, then use it as a lookup.
> It is NOT a coding practice file. Do not deep-study it like a topic file.


```
[PATTERN RECOGNITION — MINDMAP]
├── WHY IT EXISTS
│   ├── Problem it solves: map an unfamiliar problem to a known algorithmic template within 60 seconds
│   ├── Most interview problems are compositions of ~15 core patterns — recognition beats re-invention
│   └── Analogy: patterns are chess openings — you don't compute from scratch, you pattern-match and adapt
├── WHAT IT IS (First Principles)
│   ├── Core definition: a pattern = (trigger signals) → (algorithm family) + (canonical data structure)
│   ├── Signal types: problem constraints, input shape, optimization target, query type
│   └── Hierarchy: input type → constraint → pattern → algorithm → implementation variant
├── HOW TO RECOGNIZE PATTERNS
│   ├── Array / Subarray Patterns
│   │   ├── "Contiguous subarray, max/min sum" → Kadane's algorithm O(N)
│   │   ├── "Subarray sum equals K" → prefix sum + hash map O(N)
│   │   ├── "Two elements / pair / complement" → two pointers or hash map O(N)
│   │   └── "Longest subarray with constraint" → sliding window O(N)
│   ├── Search / Optimization Patterns
│   │   ├── "Sorted array, find element / boundary" → binary search O(log N)
│   │   ├── "Minimize max / maximize min over a range" → binary search on answer
│   │   └── "K-th smallest/largest" → heap (min/max) or quickselect O(N) avg
│   ├── Tree / Graph Patterns
│   │   ├── "Explore all paths, level order" → BFS (queue)
│   │   ├── "DFS: path, cycle, topological order" → DFS + visited/color array
│   │   ├── "Shortest path, unweighted" → BFS | weighted positive → Dijkstra | negative → Bellman-Ford
│   │   └── "Connected components, union queries" → Union-Find
│   ├── Dynamic Programming Patterns
│   │   ├── "Count/optimize over subsets or subsequences" → DP
│   │   ├── "Overlapping subproblems" → memoization / bottom-up table
│   │   ├── "Decision at each step: take or skip" → 0/1 knapsack pattern
│   │   └── "Interval DP" → dp[i][j] = optimal for s[i..j]; diagonal fill
│   ├── String Patterns
│   │   ├── "Pattern match in text" → KMP O(N+M)
│   │   ├── "Anagram / permutation in string" → sliding window + freq array O(N)
│   │   └── "Longest palindromic substring" → expand-around-center or Manacher
│   ├── Greedy Patterns
│   │   ├── "Interval scheduling / merging" → sort by end time, greedy pick
│   │   ├── "Minimum cost to connect all" → Kruskal / Prim MST
│   │   └── "Local optimum = global optimum" → greedy; else → DP
│   └── Backtracking Patterns
│       ├── "Generate all subsets / permutations / combinations" → backtrack with undo
│       └── "Constraint satisfaction (N-Queens, Sudoku)" → backtrack + pruning
├── COMPLEXITY SUMMARY (Pattern → Typical Complexity)
│   ├── Sliding window: O(N)
│   ├── Binary search: O(log N) or O(N log N) with pre-sort
│   ├── BFS/DFS on graph: O(V + E)
│   ├── DP (2D): O(N·M) time and space (optimize to O(M) space with rolling array)
│   └── Backtracking: O(2^N) or O(N!) worst — prune aggressively
├── WHEN TO USE WHICH PATTERN
│   ├── Signal: "find all / enumerate" → backtracking
│   ├── Signal: "optimal / min / max with choices" → DP or greedy
│   ├── Signal: "sorted + search" → binary search
│   ├── Signal: "shortest path" → BFS (unweighted) / Dijkstra (weighted)
│   ├── Signal: "sliding / contiguous window" → sliding window or two pointers
│   └── Signal: "group / component / connectivity" → Union-Find or BFS/DFS
└── COMMON MISTAKES / GOTCHAS
    ├── Using DFS for shortest path: BFS guarantees shortest in unweighted graphs — DFS does not
    ├── Greedy on problems requiring global optimum: always verify greedy choice property before committing
    ├── DP without memoization: exponential time — always cache or build bottom-up
    ├── Two pointers requiring sort: forgetting to sort first invalidates the approach
    ├── Sliding window with negative numbers: two-pointer shrinking doesn't work — use deque or prefix sum
    └── Pattern misfire: "find any" vs "find all" vs "find optimal" require different approaches
```

**Use this when:** You read a problem and need to identify the solution approach within 60 seconds.

---

## Quick Decision Trees

### By Input Size (N)

| Constraint | Expected Complexity | Likely Patterns |
|------------|---------------------|-----------------|
| N ≤ 10 | O(N!) | Permutations, TSP, exhaustive search |
| N ≤ 20 | O(2^N) | Backtracking, subsets, bitmask DP |
| N ≤ 500 | O(N³) | Floyd-Warshall, 3D DP, interval DP |
| N ≤ 2000 | O(N²) | 2D DP, nested loops, matrix paths |
| N ≤ 10⁵ | O(N log N) or O(N) | Sorting, binary search, heaps, two pointers, sliding window |
| N ≤ 10⁶ | O(N) or O(log N) | Single pass, greedy, math, binary search |

### By Keyword/Constraint

| You hear/see | Think | Why |
|--------------|-------|-----|
| "Contiguous subarray/substring" | Sliding window, prefix sum | Window covers range; prefix calculates any range in O(1) |
| "Subsequence" | DP (take/skip), LIS | Elements not contiguous; decide for each element |
| "Sorted array" | Binary search, two pointers | Sorting enables O(log N) or O(N) convergence |
| "Top K / Most frequent" | Heap (size K), hash map | Heap maintains top order; map counts frequency |
| "Dependencies / order" | Topological sort (DAG) | Node A must happen before B |
| "Shortest path" (unweighted) | BFS | BFS explores layers; first hit = shortest |
| "Shortest path" (weighted) | Dijkstra | Min-heap expands cheapest known node |
| "Maximize minimum / Minimize maximum" | Binary search on answer | Guess value, check feasibility (monotonicity) |
| "All possible ways" | Backtracking (list them), DP (count them) | Backtrack to enumerate; DP for count only |
| "Kth smallest/largest" | Heap, quickselect, binary search on answer | Heap: O(N log K); Quickselect: O(N) average |

---

## Core Patterns

### 1. Arrays & Strings

#### Prefix Sum
**When:** Range sum queries, subarray sum = K
**Template:** `P[i] = P[i-1] + arr[i]`; range sum = `P[j] - P[i-1]`
**Variants:**
- With hash map: Count subarrays with sum = K → `{prefix_sum: frequency}`
- 2D prefix sum: Matrix range queries

#### Two Pointers
**When:** Sorted array, pair/triplet search, in-place operations
**Variants:**
- **Converging:** Opposite ends (3Sum, Container With Most Water)
- **Fast/Slow:** Cycle detection, middle finding (Floyd's algorithm)
- **Same direction:** Valid palindrome, remove duplicates

#### Sliding Window
**When:** Longest/shortest contiguous subarray/substring with constraint
**Template:**
```
Expand right pointer
While invalid: shrink left pointer
Update answer
```
**Variants:**
- **Fixed size:** K-length calculations
- **Variable size:** Expand/shrink based on condition
- **With hash map:** Character frequency (longest substring without repeats)
- **Monotonic deque:** Sliding window maximum

#### Kadane's Algorithm
**When:** Maximum subarray sum
**Template:** `curr = max(num, curr + num)`; `global_max = max(global_max, curr)`

---

### 2. Binary Search

#### Standard Binary Search
**When:** Sorted array, search/insert/find bounds
**Template:** `mid = left + (right - left) // 2`

#### Rotated Sorted Array
**When:** Sorted but rotated
**Logic:** Compare mid with left to find sorted half, then decide which side to search

#### Binary Search on Answer
**When:** "Minimize maximum", "Maximize minimum", feasibility check exists
**Examples:** Koko Eating Bananas, Split Array Largest Sum
**Template:**
```
low = min_possible, high = max_possible
while low < high:
    mid = (low + high) // 2
    if feasible(mid): high = mid
    else: low = mid + 1
```

---

### 3. Linked Lists

#### Fast/Slow Pointers
**When:** Cycle detection, middle finding, kth from end
**Template:** `slow = head, fast = head.next`

#### In-Place Reversal
**When:** Reverse linked list, reverse in k-group
**Template:**
```
prev = None
while curr:
    next_temp = curr.next
    curr.next = prev
    prev = curr
    curr = next_temp
```

#### Dummy Node
**When:** Merge lists, remove nodes, edge cases with head
**Template:** `dummy = ListNode(0); dummy.next = head`

---

### 4. Stack & Queue

#### Monotonic Stack
**When:** Next greater/smaller element, histogram rectangle
**Template:** Store indices; pop while current violates monotonicity
**Examples:** Daily Temperatures, Largest Rectangle in Histogram

#### Monotonic Deque
**When:** Sliding window maximum/minimum
**Template:** Maintain decreasing (for max) or increasing (for min) deque

#### BFS (Queue)
**When:** Level-order traversal, shortest path (unweighted)
**Template:** Queue + visited set

---

### 5. Trees

#### Traversals
- **PreOrder:** Root → Left → Right (serialize, clone)
- **InOrder:** Left → Root → Right (BST sorted order)
- **PostOrder:** Left → Right → Root (tree DP, delete)
- **LevelOrder:** BFS with queue

#### LCA (Lowest Common Ancestor)
**BST:** If both p,q < root → left; else if both > root → right; else return root
**Binary Tree:** Recursive; if left and right non-null → current is LCA

#### Tree DP
**When:** Max path through node, subtree calculations
**Template:** Postorder; return value up, update global at node

---

### 6. Heaps

#### Top K Elements
**When:** K largest/smallest, frequent elements
**Template:** Min-heap of size K (for K largest); pop when size > K

#### Two Heaps
**When:** Median of data stream
**Template:** Max-heap (small half), Min-heap (large half); rebalance to keep size diff ≤ 1

#### Merge K Sorted
**When:** Merge k sorted lists/arrays
**Template:** Min-heap of (value, list_id, node); push next from same list

---

### 7. Graphs

#### BFS
**When:** Shortest path (unweighted), level-order, connected components
**Complexity:** O(V + E) time, O(V) space

#### DFS
**When:** Connected components, cycle detection, backtracking
**Complexity:** O(V + E) time, O(V) space (recursion stack)

#### Topological Sort
**When:** Dependencies, DAG ordering
**Variants:**
- **Kahn's:** In-degree array, queue of zero-degree nodes
- **DFS:** Postorder + reverse

#### Dijkstra
**When:** Shortest path (weighted, non-negative)
**Template:** Min-heap of (distance, node); update if shorter path found
**Complexity:** O((V + E) log V)

#### Union-Find (DSU)
**When:** Connectivity, cycle detection, Kruskal's MST
**Complexity:** ~O(1) amortized
**Template (Python — path compression + union by rank):**
```python
parent = list(range(n))
rank = [0] * n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # path halving
        x = parent[x]
    return x

def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False  # already connected; returning False signals a cycle
    if rank[ra] < rank[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    if rank[ra] == rank[rb]:
        rank[ra] += 1
    return True
```
Note: all pseudocode in this file is illustrative.

---

### 8. Dynamic Programming

#### 1D DP (Fibonacci pattern)
**When:** Climbing stairs, house robber, max subarray
**Template:** `dp[i] = f(dp[i-1], dp[i-2], ...)`

#### 0/1 Knapsack
**When:** Pick or skip, weight constraint
**Template:** `dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w-wt[i]])`

#### Unbounded Knapsack
**When:** Infinite supply (coin change)
**Template:** `dp[w] = min(dp[w], 1 + dp[w - coin])`

#### LIS (Longest Increasing Subsequence)
**When:** Increasing subsequence (not necessarily contiguous)
**O(N²):** `dp[i] = max(dp[j] + 1)` for all j < i where arr[j] < arr[i]
**O(N log N):** Patience sorting with tails array

#### LCS (Longest Common Subsequence)
**When:** Two strings, common order
**Template:** `dp[i][j] = 1 + dp[i-1][j-1]` if match; else `max(dp[i-1][j], dp[i][j-1])`

#### Interval DP
**When:** Burst balloons, matrix chain multiplication
**Template:** Try all split points k in range (i, j)

#### Tree DP
**When:** Max path sum through node, house robber III
**Template:** Postorder; compute at node using children results

#### Bitmask DP
**When:** N ≤ 20, subsets, TSP
**Template:** `dp[mask]` where mask represents visited/included elements

#### Binary Search on Answer (DP variant)
**When:** Minimize maximum, feasibility check
**Examples:** Split array into m subarrays, allocate books

---

### 9. Greedy

#### Interval Scheduling
**When:** Non-overlapping intervals, minimum removals
**Template:** Sort by end time; pick earliest finishing

#### Jump Game
**When:** Can reach end, minimum jumps
**Template:** Track furthest reachable; increment jumps at boundary

#### Gas Station
**When:** Circular route, can complete circuit
**Template:** Reset start when tank < 0; if total gas ≥ cost, solution exists

---

### 10. Backtracking

#### Template
```
def backtrack(start, path):
    if base_case:
        add to result
        return
    for i in range(start, n):
        if valid(i):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
```

#### Variants
- **Permutations:** All orderings, use `used` array
- **Combinations:** Choose k, use `start` index
- **Subsets:** All subsets, skip duplicates at same level
- **Word Search:** Grid DFS, mark visited, backtrack

---

## If-Not-X-Then-Y (Pivot Logic)

| If stuck with... | Try instead |
|------------------|-------------|
| Array O(N²) too slow | Hash map (space for time), sort + two pointers, sliding window, prefix sums |
| Tree recursion stuck | Postorder (children → parent), preorder with state passed down |
| Graph with 0/1 weights | 0-1 BFS (deque) instead of Dijkstra |
| DP state too large | Reduce 2D → 1D, bitmask for small N |
| Can't find DP recurrence | Try greedy, or binary search on answer |

---

## Mental Model Shifts

| Problem type | Reframe as |
|--------------|------------|
| Meeting rooms | Merge intervals |
| Word transformation | BFS (words = nodes, 1-char diff = edge) |
| Next greater temperature | Monotonic stack |
| Collecting gold in grid | 2D DP pathfinding |
| Assigning tasks to workers | Bin packing (backtracking) or flow (advanced) |

---

## 60-Second Pre-Code Checklist

Ask interviewer:
1. **Duplicates?** → Impacts hash map/set logic
2. **Sorted?** → Enables binary search/two pointers
3. **Empty/null input?** → Base case handling
4. **Memory constraints?** → O(1) space required?
5. **Negative values?** → Breaks simple sliding window, Dijkstra

---

---

## Progression Cheatsheet: Brute Force → Optimization → Optimal

Use this when you have a brute-force solution and need to optimize under time pressure.

| Pattern | Brute Force | Optimization | Optimal |
|---------|-------------|--------------|---------|
| **Subarray sum = K** | O(N²) nested loops | O(N) prefix sum + hash map | O(N) — same |
| **Two-sum** | O(N²) double loop | O(N) hash set (one pass) | O(N) — same |
| **Sliding window max** | O(NK) recompute each window | O(N log K) heap | O(N) monotonic deque |
| **Top-K frequent** | O(N log N) full sort | O(N log K) min-heap of size K | O(N) bucket sort (if K = N) |
| **Longest increasing subsequence** | O(2^N) backtrack | O(N²) DP | O(N log N) patience sort |
| **Shortest path (unweighted)** | O(V × E) repeated BFS | — | O(V + E) BFS (already optimal) |
| **Shortest path (weighted)** | O(V²) Bellman-Ford | O(E log V) Dijkstra | O(E log V) — same |
| **Count inversions** | O(N²) nested loops | — | O(N log N) merge sort augmented |
| **Kth largest element** | O(N log N) full sort | O(N log K) min-heap | O(N) avg quickselect |
| **Word prefix search** | O(W × L) per query | — | O(L) trie |
| **Next greater element** | O(N²) double scan | — | O(N) monotonic stack |
| **Overlapping intervals (non-overlapping max)** | O(N²) all pairs | — | O(N log N) sort by end + greedy |
| **Coin change** | O(K^(T/min)) backtrack | O(N × T) DP | O(N × T) — same |

> [!TIP]
> The most common upgrade paths: **O(N²) → O(N)** via hash map or two pointers; **O(N²) → O(N log N)** via sort + greedy; **exponential → polynomial** via DP or memoization. When stuck on optimization, ask: "Am I recomputing something? Can I cache it?" (hash/DP) or "Is the data sortable? Does sorting unlock a linear pass?" (sort + greedy/two-pointer).

---

## See Also

- Problem bank with logic & trickiness: `03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md`
- Canonical questions index: `03-patterns/canonical-questions.md`
- Problem deep-dives with full walkthroughs: `02-algorithms/problem-deep-dives.md`
