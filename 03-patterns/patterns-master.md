---
module: 03-patterns
topic: Patterns Master
tags: [patterns, patterns-master]
---
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



**Use this when:** You read a problem and need to identify the solution approach within 60 seconds.

---

## Quick Decision Trees

### By Input Size (N)

Constraint size → target complexity → algorithm family:
[`L3_CHEATSHEET.md` § 2 Constraint Analysis](../00-L3-EXECUTION-META/L3_CHEATSHEET.md#2-constraint-analysis-n105--on-or-on-log-n).

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
| "Kth smallest/largest" (incl. sorted matrix) | Heap, quickselect, binary search on answer | Heap: O(N log K); Quickselect: O(N) average; matrix: BS on value range, count ≤ mid |
| "Subarray sum = K" | Prefix sum + hash map | `prefix_count[running_sum - K]` gives count of valid subarrays |
| "Next greater/smaller" | Monotonic stack | Store indices; pop while current element breaks monotonicity |
| "Connectivity / cycles" | Union-Find | Union two nodes; find detects if already connected (cycle) |
| "Stream / running median" | Two heaps | Max-heap (lower half) + min-heap (upper half); rebalance to size diff ≤ 1 |

---

## Core Patterns

### 1. Arrays & Strings

#### Prefix Sum
**Real-life:** A car's trip odometer — instead of re-adding every mile driven, you subtract two odometer readings to get distance for any leg of the trip.
**When:** Range sum queries, subarray sum = K
**Template:** `P[i] = P[i-1] + arr[i]`; range sum = `P[j] - P[i-1]`
**Variants:**
- With hash map: Count subarrays with sum = K → `{prefix_sum: frequency}`
- 2D prefix sum: Matrix range queries

#### Two Pointers
**Real-life:** Two people searching a sorted phone book for a pair of names that combine to a target — one starts from A, one from Z, and they walk toward each other.
**When:** Sorted array, pair/triplet search, in-place operations
**Variants:**
- **Converging:** Opposite ends (3Sum, Container With Most Water)
- **Fast/Slow:** Cycle detection, middle finding (Floyd's algorithm)
- **Same direction:** Valid palindrome, remove duplicates

#### Sliding Window
**Real-life:** Cruise control adjusting your following distance — you only look at the car directly ahead and behind, expanding or shrinking the gap, never rescanning the whole highway.
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
**Real-life:** Tracking a stock's best buy-low-sell-high run — you keep riding the current winning streak, but the instant it turns net-negative you cut losses and restart from today.
**When:** Maximum subarray sum
**Template:** `curr = max(num, curr + num)`; `global_max = max(global_max, curr)`

---

### 2. Binary Search

#### Standard Binary Search
**Real-life:** Looking up a word in a paper dictionary — you open to the middle, decide "earlier" or "later," and repeat, never scanning page by page.
**When:** Sorted array, search/insert/find bounds
**Template:** `mid = left + (right - left) // 2`

#### Rotated Sorted Array
**Real-life:** A deck of cards cut once and restacked — still two sorted runs, so you first figure out which half you're looking at, then binary-search within it.
**When:** Sorted but rotated
**Logic:** Compare mid with left to find sorted half, then decide which side to search

#### Binary Search on Answer
**Real-life:** Tuning a shower to the right temperature by feel — you don't compute the exact setting, you guess, check "too hot/too cold," and bisect toward the answer.
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
**Real-life:** Two runners on a circular track, one twice as fast as the other — if the track is a loop, the fast runner eventually laps the slow one; if it's a straight line, the fast one just finishes first (marking the middle).
**When:** Cycle detection, middle finding, kth from end
**Template:** `slow = head, fast = head.next`

#### In-Place Reversal
**Real-life:** Flipping a chain of paperclips one link at a time — each clip gets pointed backward to the one before it as you walk down the chain, no extra chain needed.
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
**Real-life:** A placeholder "0th" ticket at the front of a queue so you never have to special-case "what if the person at the very front leaves."
**When:** Merge lists, remove nodes, edge cases with head
**Template:** `dummy = ListNode(0); dummy.next = head`

---

### 4. Stack & Queue

#### Monotonic Stack
**Real-life:** A stack of people waiting to see the next taller person behind them in line — each time a taller person joins the back, everyone shorter ahead of them finally gets their answer and steps out.
**When:** Next greater/smaller element, histogram rectangle
**Template:** Store indices; pop while current violates monotonicity
**Examples:** Daily Temperatures, Largest Rectangle in Histogram

#### Monotonic Deque
**Real-life:** Keeping a leaderboard of the tallest person currently visible through a moving window — you discard anyone shorter than the newest entrant since they can never win again.
**When:** Sliding window maximum/minimum
**Template:** Maintain decreasing (for max) or increasing (for min) deque

#### BFS (Queue)
**Real-life:** Ripples spreading from a stone dropped in a pond — everyone at distance 1 is reached before anyone at distance 2, so the first ripple to reach a point is the shortest path.
**When:** Level-order traversal, shortest path (unweighted)
**Template:** Queue + visited set

---

### 5. Trees

**Real-life:** A company org chart — PreOrder announces the manager before their reports (top-down memo), PostOrder tallies each team's headcount before reporting up to the manager (bottom-up rollup), LevelOrder is announcing everyone rank by rank at an all-hands.

#### Traversals
- **PreOrder:** Root → Left → Right (serialize, clone)
- **InOrder:** Left → Root → Right (BST sorted order)
- **PostOrder:** Left → Right → Root (tree DP, delete)
- **LevelOrder:** BFS with queue

#### LCA (Lowest Common Ancestor)
**Real-life:** The most recent shared ancestor of two cousins in a family tree — the closest node from which both people's lineage branches apart.
**BST:** If both p,q < root → left; else if both > root → right; else return root
**Binary Tree:** Recursive; if left and right non-null → current is LCA

#### Tree DP
**Real-life:** Each manager reports their team's best result up the chain, and the CEO takes the max across all divisions — every node combines its children's answers before passing a single number upward.
**When:** Max path through node, subtree calculations
**Template:** Postorder; return value up, update global at node

---

### 6. Heaps

#### Top K Elements
**Real-life:** A hospital ER keeping only the 5 most critical patients visible on the board — anyone less urgent than the least-critical of those 5 doesn't make the cut.
**When:** K largest/smallest, frequent elements
**Template:** Min-heap of size K (for K largest); pop when size > K

#### Two Heaps
**Real-life:** Splitting a line of people by height into a "shorter half" and "taller half," each sorted internally, so the median is always visible right at the boundary.
**When:** Median of data stream
**Template:** Max-heap (small half), Min-heap (large half); rebalance to keep size diff ≤ 1

#### Merge K Sorted
**Real-life:** Merging K sorted stacks of graded exams into one ranked pile — you always pull the current top-most paper across all stacks and refill from whichever stack it came from.
**When:** Merge k sorted lists/arrays
**Template:** Min-heap of (value, list_id, node); push next from same list

---

### 7. Graphs

#### BFS
**Real-life:** Same ripple-in-a-pond idea as tree BFS, but now the pond has irregular connections — the ripple still reaches everyone at distance 1 before distance 2.
**When:** Shortest path (unweighted), level-order, connected components
**Complexity:** O(V + E) time, O(V) space

#### DFS
**Real-life:** Exploring a maze by always taking the first unexplored turn and backtracking only when you hit a dead end — you commit deep before you go wide.
**When:** Connected components, cycle detection, backtracking
**Complexity:** O(V + E) time, O(V) space (recursion stack)

#### Topological Sort
**Real-life:** Deciding what order to take college courses in when some are prerequisites for others — you can't take "Algorithms II" before "Algorithms I."
**When:** Dependencies, DAG ordering
**Variants:**
- **Kahn's:** In-degree array, queue of zero-degree nodes
- **DFS:** Postorder + reverse

#### Dijkstra
**Real-life:** GPS route-finding with tolls and traffic — you always expand from the currently cheapest-known reachable city next, never assume the map is unweighted.
**When:** Shortest path (weighted, non-negative)
**Template:** Min-heap of (distance, node); update if shorter path found
**Complexity:** O((V + E) log V)

#### Union-Find (DSU)
**Real-life:** Tracking which friend groups have merged at a party — every time two people who know each other are introduced, their whole friend circles fuse into one group, and you can instantly check if two people are in the same circle.
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
**Real-life:** Climbing a staircase where you remember how many ways you reached the last two steps instead of recounting from the ground every time.
**When:** Climbing stairs, house robber, max subarray
**Template:** `dp[i] = f(dp[i-1], dp[i-2], ...)`

#### 0/1 Knapsack
**Real-life:** Packing a suitcase with a strict weight limit — each item goes in whole or stays home, so you weigh every combination's value against the limit.
**When:** Pick or skip, weight constraint
**Template:** `dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w-wt[i]])`

#### Unbounded Knapsack
**Real-life:** Making change from an ATM with unlimited bills of each denomination — you can reuse the same bill value as many times as needed.
**When:** Infinite supply (coin change)
**Template:** `dp[w] = min(dp[w], 1 + dp[w - coin])`

#### LIS (Longest Increasing Subsequence)
**Real-life:** Picking the longest run of ever-improving quarterly scores from your report card, skipping the bad quarters without needing them to be consecutive.
**When:** Increasing subsequence (not necessarily contiguous)
**O(N²):** `dp[i] = max(dp[j] + 1)` for all j < i where arr[j] < arr[i]
**O(N log N):** Patience sorting with tails array

#### LCS (Longest Common Subsequence)
**Real-life:** Diffing two edited drafts of a document to find the longest shared skeleton of sentences that appear in the same order in both.
**When:** Two strings, common order
**Template:** `dp[i][j] = 1 + dp[i-1][j-1]` if match; else `max(dp[i-1][j], dp[i][j-1])`

#### Interval DP
**Real-life:** Deciding the cheapest order to demolish a row of connected buildings when the cost of each demolition depends on which neighbors are still standing — you try every possible "last building removed" split.
**When:** Burst balloons, matrix chain multiplication
**Template:** Try all split points k in range (i, j)

#### Tree DP
**Real-life:** Same org-chart rollup as §5, applied to an optimization: each manager decides whether to "use" themselves or skip to grandchildren, based on which children's answers score higher.
**When:** Max path sum through node, house robber III
**Template:** Postorder; compute at node using children results

#### Bitmask DP
**Real-life:** A delivery driver tracking which of ≤20 stops they've already visited as a single binary checklist (bit per stop) instead of a list, so "have I been to stop 7?" is a single bit check.
**When:** N ≤ 20, subsets, TSP
**Template:** `dp[mask]` where mask represents visited/included elements

#### Binary Search on Answer (DP variant)
**When:** Minimize maximum, feasibility check
**Examples:** Split array into m subarrays, allocate books

---

### 9. Greedy

#### Interval Scheduling
**Real-life:** Booking a single conference room for as many meetings as possible — you always accept the meeting that finishes soonest first, since it frees the room fastest for the next one.
**When:** Non-overlapping intervals, minimum removals
**Template:** Sort by end time; pick earliest finishing

#### Jump Game
**Real-life:** Hopping across stepping stones in a river where each stone shows how far you can leap from it — you just track the furthest stone reachable so far.
**When:** Can reach end, minimum jumps
**Template:** Track furthest reachable; increment jumps at boundary

#### Gas Station
**Real-life:** Planning a road trip around a circular route where each stop gives you some gas and costs some to reach the next — if your tank ever goes negative starting from a stop, that stop (and everything before it since the last reset) can't be the starting point.
**When:** Circular route, can complete circuit
**Template:** Reset start when tank < 0; if total gas ≥ cost, solution exists

---

### 10. Backtracking

**Real-life:** Solving a maze by trying a path, and the instant you hit a dead end, retracing your last step and trying the next unexplored branch — you never bulldoze forward once a choice is proven wrong.

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
| Meeting rooms — can all fit? | Merge intervals |
| Meeting rooms — minimum rooms needed? | Sort by start + min-heap of end times |
| Word transformation | BFS (words = nodes, 1-char diff = edge) |
| Next greater temperature | Monotonic stack |
| Collecting gold in grid | 2D DP pathfinding |
| Assigning tasks to workers | Bin packing (backtracking) or flow (advanced) |
| Group words by same letters | Sorted string as hash key (anagram grouping) |
| Earliest time all nodes connected | Union-Find + sort edges by weight (Kruskal) |

---

## 60-Second Pre-Code Checklist

Ask interviewer:
1. **Duplicates?** → Impacts hash map/set logic
2. **Sorted?** → Enables binary search/two pointers
3. **Empty/null input?** → Base case handling
4. **Memory constraints?** → O(1) space required?
5. **Negative values?** → Breaks simple sliding window, Dijkstra

---

## Critical Gotchas (Last-Minute Check)

| Gotcha | Rule |
|--------|------|
| Sliding window + negatives | Can't shrink window on negatives; use prefix sum + map instead |
| Duplicates in backtracking | `if i > start and nums[i] == nums[i-1]: continue` |
| Binary search mid overflow | `mid = lo + (hi - lo) // 2`, not `(lo + hi) // 2` |
| BFS visited mark | Mark visited **when enqueuing**, not when dequeuing — prevents duplicates in queue |
| Topo sort cycle detection | If processed nodes < total nodes after Kahn's, there's a cycle |
| Tree DP return vs global | Return the single-arm gain upward; update global max with both arms at current node |
| Dijkstra with negative edges | Does not work — use Bellman-Ford |

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

## Implicit Graph Pattern `⚡ T1`

An **implicit graph** is one where nodes and edges are never explicitly listed — they emerge from problem state. You recognize it when the problem never says "graph" but BFS/DFS is the right tool.

**Trigger signals**:
- "Minimum number of operations/steps to reach state X from state Y"
- State transitions described by rules (flip bit, rotate, swap, replace character)
- Lock combinations, word ladders, sliding puzzles

**Template**:
```python
from collections import deque

def bfs_implicit(start, target):
    if start == target:
        return 0
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        state, steps = queue.popleft()
        for next_state in get_neighbors(state):   # domain-specific
            if next_state == target:
                return steps + 1
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, steps + 1))
    return -1
```

**Key insight**: Encode state as a string/tuple so it's hashable for `visited`. Generate neighbors by applying every valid operation to the current state. BFS gives shortest path in unweighted state space.

**Bidirectional BFS** (when state space is huge): expand from both ends, meet in the middle. Cuts from O(b^d) to O(b^(d/2)).

| Problem | State | Neighbor generation |
|---------|-------|---------------------|
| Word Ladder | word string | swap each char with a–z |
| Open the Lock | "0000" string | +1/-1 each of 4 wheels |
| Minimum Genetic Mutation | gene string | swap each char from bank |
| Sliding Puzzle | board tuple | swap 0 with adjacent cells |

---

## Follow-Up Chains — Interview Progression `⚡ T1`

Google interviewers stack follow-ups to probe depth. Know the upgrade path for each pattern family.

### Two Sum family
1. Two Sum (unsorted, hash map) → 2. Two Sum sorted (two pointers) → 3. 3Sum (fix one, two-pointer inner) → 4. 4Sum (fix two, two-pointer inner) → 5. Subarray Sum = K (prefix sum + hash map)

### Sliding Window family
1. Max sum of size-k subarray → 2. Longest substring with k distinct chars → 3. Minimum window substring → 4. Sliding window with frequency map and two pointers

### Binary Search family
1. Search in sorted array → 2. Search in rotated sorted array → 3. Find minimum in rotated array → 4. Search in 2D matrix → 5. Binary search on answer (capacity, split, minimize max)

### Tree DFS family
1. Max depth → 2. Path sum (root-to-leaf) → 3. Path sum III (any path, prefix sums) → 4. Lowest common ancestor → 5. Serialize/deserialize binary tree

### DP Linear family
1. Climb stairs → 2. House robber → 3. House robber II (circular) → 4. Decode ways → 5. Jump game II (BFS/greedy DP)

### Backtracking family
1. Subsets → 2. Combinations → 3. Permutations → 4. All three with duplicates (sort + skip) → 5. N-Queens / Sudoku (constraint + pruning)

### Graph BFS family
1. Number of islands (DFS/BFS) → 2. Walls and gates (multi-source BFS) → 3. Rotting oranges (multi-source BFS with time) → 4. Word ladder (implicit graph BFS) → 5. Alien dictionary (topological sort)

### Interval Scheduling family
1. Merge intervals → 2. Meeting rooms (any overlap?) → 3. Meeting rooms II (min rooms, heap) → 4. Non-overlapping intervals (max removals) → 5. Task scheduler (formula)

### Heap family
1. Kth largest element → 2. K closest points to origin → 3. Top K frequent elements → 4. Merge K sorted lists → 5. Find median from data stream (two heaps)

---

## Hybrid Patterns `🎯 T2`

When a problem combines two pattern families, name both upfront in the interview.

| Hybrid | When you see it | Example |
|--------|----------------|---------|
| **DP + Binary Search** | LIS-style: optimize over a sorted structure | Longest Increasing Subsequence O(N log N) |
| **Graph + DP** | Shortest path with state, DAG counting | Unique paths in grid, cheapest flights within K stops |
| **Backtracking + Memo** | Subproblems repeat in recursion tree | Word Break II, Palindrome Partitioning II |
| **Greedy + Heap** | Sort by one key, dynamically pick best by another | Meeting Rooms II, Task Scheduler, Dijkstra |
| **BFS + Binary Search** | "Minimum X such that Y is possible" in a grid/graph | Swim in Rising Water, Path With Minimum Effort |
| **Two Pointers + Hash Map** | Sliding window with constraint tracking | Minimum Window Substring, Fruit Into Baskets |
| **Trie + DFS** | Batch prefix queries, pruning on Trie branches | Word Search II |
| **Union-Find + Sort** | Process edges in weight order, merge components | Kruskal's MST, Redundant Connection |

**Naming hybrid patterns in interviews**: "This looks like a DP problem, but the recurrence needs to query a monotonic structure — so I'll use binary search on the DP array, which gives us O(N log N) instead of O(N²)."

---

## See Also

- Problem bank with logic & trickiness: `03-patterns/TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md`
- Derive the pattern from first principles: `03-patterns/HOW_TO_THINK.md`
- Problem deep-dives with full walkthroughs: `02-algorithms/problem-deep-dives.md`
