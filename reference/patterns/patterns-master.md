# Pattern Recognition Master Guide

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
**Template:** Path compression + union by rank
**Complexity:** ~O(1) amortized

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

## See Also

- Problem bank with logic & trickiness: `reference/problem-bank/`
- Quick revision sheets: `reference/quick-sheets/`
- Track-specific problem sets: `tracks/google-sde2/`, `tracks/sde3-dsa/`
