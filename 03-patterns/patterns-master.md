---
module: 03-patterns
topic: Patterns Master
tags: [patterns, patterns-master]
---
# Pattern Recognition Master Guide

## What this covers

> [!abstract] In this file
> **Covers:** Pattern recognition end to end: constraint budgets, keyword triggers, DS/algorithm selection, every core pattern's template, pivot logic, pre-code checks and gotchas, brute → optimal paths, implicit graphs, follow-up chains, hybrids, and the exhaustive phrase → technique lookup.
> **You'll be able to:** Map signal words + constraints to a pattern and data structure, and know the pivot when the first idea fails.
> **Prereqs:** Most lecture files · **Pair with:** [How to think](HOW_TO_THINK.md) · [Interview judgment](INTERVIEW_JUDGMENT.md) · **Time:** 2 h
> **How to use:** reference — read once, then use as a lookup.
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../00-start-here/l3-google-roadmap.md#tier-legend))

**Sections:** [Quick Decision Trees](#quick-decision-trees) · [DS & Algorithm Selection](#ds--algorithm-selection) · [Core Patterns](#core-patterns) · [If-Not-X-Then-Y (Pivot Logic)](#if-not-x-then-y-pivot-logic) · [Mental Model Shifts](#mental-model-shifts) · [Pre-Code Checks & Gotchas](#pre-code-checks--gotchas) · [Progression Cheatsheet: Brute Force → Optimization → Optimal](#progression-cheatsheet-brute-force--optimization--optimal) · [Implicit Graph Pattern `⚡ T1`](#implicit-graph-pattern--t1) · [Follow-Up Chains — Interview Progression `⚡ T1`](#follow-up-chains--interview-progression--t1) · [Hybrid Patterns `🎯 T2`](#hybrid-patterns--t2) · [Phrase → Technique](#phrase--technique) · [When Stuck](#when-stuck) · [Flashcards](#flashcards) · [See Also](#see-also)

---

## Quick Decision Trees

### By Input Size (N)

A budget of about 10⁸ simple operations per second is a safe rule. Full detail is in [Part 5](../striver-a2z/05-time-complexity/01-theory-with-examples.md).

| n up to | Budget | Typical techniques |
|---|---|---|
| ≤ 10–12 | O(n!) or O(nⁿ) | Permutations, brute-force backtracking ([Part 18](../striver-a2z/18-recursion/README.md)) |
| ≤ 20 | O(2ⁿ · n) | Subsets, bitmask DP ([Part 32 §2](../striver-a2z/32-beyond-the-sheet/02-advanced-dp-theory.md)) |
| ≤ 40 | O(2^(n/2)) | Meet in the middle `💤 T3` ([Part 32 §4](../striver-a2z/32-beyond-the-sheet/04-techniques-toolbox-theory.md)) |
| ≤ 100–500 | O(n³) | Floyd–Warshall, interval DP / MCM ([Part 27](../striver-a2z/27-graphs/README.md), [Part 28](../striver-a2z/28-dynamic-programming/README.md)) |
| ≤ 10³–5·10³ | O(n²) | 2D DP (LCS, edit distance), all pairs |
| ≤ 10⁵–10⁶ | O(n log n) | Sort, binary search, heap, Dijkstra |
| ≤ 10⁷–10⁸ | O(n) | Two pointers, sliding window, prefix sums, hashing, monotonic stack, sieve |
| ≥ 10⁹ (a value, not a length) | O(log n) or O(√n) | Binary search on the answer, binary exponentiation, √n divisor loop, maths |
| 10¹⁸ | O(log n) or digit count | Closed form, binary exponentiation; digit DP / matrix power `💤 T3` |

| Other constraint signal | Implication |
|---|---|
| "Answer modulo 10⁹+7" | Counting DP or combinatorics ([Part 31 §5](../striver-a2z/31-maths/05-modular-arithmetic-and-combinatorics-theory.md)) |
| Values ≤ 10⁵ but n large | Counting array or bucket instead of a hashmap; sieve |
| Sum of n over tests ≤ 2·10⁵ | Per-test cost must be linear in that test's n |
| Grid m·n ≤ 10⁵ | BFS/DFS over cells, O(mn) |
| Q queries ≥ 10⁵ | Precompute (prefix sums) or O(log n) per query via sort + binary search ([Part 32 §1](../striver-a2z/32-beyond-the-sheet/01-range-queries-theory.md)) |

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
| "Overlapping intervals / events over time" | Sort + sweep, or heap of end times | Process endpoints in order, maintain the active set |
| "Prefix lookup / max XOR pair" | Trie | Shared prefixes walked once; greedy opposite bit |
| "Design a class with O(1) ops" | DS composition (hash map + DLL / heap / stack) | Each part covers the other's weak operation |

### 60-second problem → pattern tree

Identify the input shape and the repeated operation, pick a candidate, state its invariant, test it on a small example.

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

## DS & Algorithm Selection

### Data structure by required operation

| Need | Reach for |
|---|---|
| O(1) lookup / membership / counts | HashMap / HashSet |
| Ordered keys, floor / ceiling | TreeMap / balanced BST |
| Repeated O(1) min or max | Heap |
| Running median | Two heaps |
| Push/pop at both ends, window max | Deque |
| LIFO, undo, next greater/smaller | Stack (monotonic) |
| Prefix lookup / autocomplete | Trie |
| Static range sums | Prefix sum |
| Range queries with point updates | Segment tree / BIT `💤 T3` — out of scope; say it exists, don't code it |
| Dynamic connectivity | Union-Find |

| Upgrade | When |
|---|---|
| Stack → monotonic stack | Need nearest greater/smaller for every element |
| One heap → two heaps | Need the middle, not the extreme |
| HashSet → Trie | Queries are by prefix, or backtracking needs prefix pruning |
| Queue → deque | Must evict from the back too (sliding-window max) |

| Wrong choice | Why it fails |
|---|---|
| Array scan for key lookup | O(n) per query; hash it |
| HashMap when order is needed | No floor/ceil or sorted iteration |
| Single heap for median | Middle is not an extreme |
| Adjacency matrix for sparse graph | O(V²) space, O(V) neighbor scan |
| Brute string compare for many prefixes | O(n·L) per query; a trie shares prefixes |

### Algorithm family by core question

| Core question | Family |
|---|---|
| What order respects dependencies? | Topological sort |
| Optimize over overlapping subproblems? | DP |
| Enumerate ALL valid configurations? | Backtracking |
| Is a local choice provably safe? | Greedy (exchange argument) |
| Reachable / shortest path? | BFS (unweighted) · DFS · Dijkstra (weighted) |
| Are these connected, as edges arrive? | Union-Find |
| Sorted data or monotone predicate? | Binary search |
| Find a pattern in a string? | KMP / Z / rolling hash |
| Count modulo a prime? | Math / combinatorics |

| Upgrade | From → to |
|---|---|
| Nested loops over pairs | O(n²) → sort + two pointers O(n log n) |
| Rescanning each window | O(n²) → sliding window O(n) |
| Exponential recursion | O(2ⁿ) → memoized DP O(states × work) |
| Repeated connectivity BFS | O(n²) → Union-Find O(α(n)) |
| Naive substring search | O(n·L) → KMP / Z O(n + L) |

| Wrong choice | Symptom |
|---|---|
| DP when greedy suffices | Correct but slow / over-built |
| Backtracking when subproblems overlap | TLE — needs memo / DP |
| BFS on weighted edges | Wrong shortest path — use Dijkstra |
| Greedy without exchange proof | Fails a counterexample |
| Topo sort without cycle check | Silent wrong order on cyclic input |
| Memo key missing a state variable | Wrong cached answers |
| Wrong recurrence direction | Reads uncomputed table cells |

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
- **Converging:** Opposite ends (3Sum, Container With Most Water, Valid Palindrome)
- **Fast/Slow:** Cycle detection, middle finding (Floyd's algorithm)
- **Same direction (read/write):** Remove duplicates, move zeroes

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
    mid = low + (high - low) // 2
    if feasible(mid): high = mid
    else: low = mid + 1
```

---

### 3. Linked Lists

#### Fast/Slow Pointers
**Real-life:** Two runners on a circular track, one twice as fast as the other — if the track is a loop, the fast runner eventually laps the slow one; if it's a straight line, the fast one just finishes first (marking the middle).
**When:** Cycle detection, middle finding, kth from end
**Template:** `slow = fast = head; while fast and fast.next: slow, fast = slow.next, fast.next.next` → `slow` is the middle (second middle on even length); `slow is fast` mid-loop ⇒ cycle

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

#### Tree DP — return up, update global
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

#### Tree DP — include / exclude node
**Real-life:** Same org-chart rollup as §5, applied to an optimization: each manager decides whether to "use" themselves or skip to grandchildren, based on which children's answers score higher.
**When:** House Robber III, max independent set, camera placement
**Template:** Postorder; each node returns `(take, skip)`; `take = val + Σ skip(child)`, `skip = Σ max(child)`

#### Bitmask DP
**Real-life:** A delivery driver tracking which of ≤20 stops they've already visited as a single binary checklist (bit per stop) instead of a list, so "have I been to stop 7?" is a single bit check.
**When:** N ≤ 20, subsets, TSP `💤 T3` at L3 (🎯 T2 at L4)
**Template:** `dp[mask]` where mask represents visited/included elements

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
| Meeting rooms — can one person attend all? | Sort by start; any `start[i] < end[i-1]` ⇒ no |
| Meeting rooms — minimum rooms needed? | Sort by start + min-heap of end times |
| Word transformation | BFS (words = nodes, 1-char diff = edge) |
| Next greater temperature | Monotonic stack |
| Max gold in grid, any path, no revisits | Backtracking DFS from every cell (moves only right/down ⇒ 2D DP) |
| Assign tasks to k workers, minimise max load | Binary search on answer + greedy/backtracking check; bitmask DP if n ≤ 12 |
| Group words by same letters | Sorted string as hash key (anagram grouping) |
| Earliest time all nodes connected | Sort edges by time, Union-Find until components = 1 |
| "Minimum swaps to sort" | Graph of index → target index; answer = Σ (cycle length − 1) |
| Max area under bars / of 1s in matrix | Histogram per row + monotonic stack |

---

## Pre-Code Checks & Gotchas

Ask before coding (full edge-case table: [L3 cheatsheet §5](../00-start-here/L3_CHEATSHEET.md#5-universal-edge-cases)):
1. **Duplicates?** → Impacts hash map/set logic
2. **Sorted?** → Enables binary search/two pointers
3. **Empty/null input?** → Base case handling
4. **Memory constraints?** → O(1) space required?
5. **Negative values?** → Breaks simple sliding window, Dijkstra


| Gotcha | Rule |
|--------|------|
| Sliding window + negatives | Can't shrink window on negatives; use prefix sum + map instead |
| Duplicates in backtracking | `if i > start and nums[i] == nums[i-1]: continue` |
| Binary search mid overflow | `mid = lo + (hi - lo) // 2` in Java/C++ (Python ints don't overflow, but write it anyway) |
| BFS visited mark | Mark visited **when enqueuing**, not when dequeuing — prevents duplicates in queue |
| Topo sort cycle detection | If processed nodes < total nodes after Kahn's, there's a cycle |
| Tree DP return vs global | Return the single-arm gain upward; update global max with both arms at current node |
| Dijkstra with negative edges | Does not work — use Bellman-Ford |
| Dijkstra stale entries | `if d > dist[u]: continue` after pop, or you re-expand nodes |
| Mutable default / shared path list | Append `path[:]` (a copy) to results, never `path` |
| Grid DFS recursion depth | Python limit ~1000; 10⁵ cells ⇒ iterative stack or BFS |

---

## Progression Cheatsheet: Brute Force → Optimization → Optimal

| Pattern | Brute Force | Optimization | Optimal |
|---------|-------------|--------------|---------|
| **Subarray sum = K** | O(N²) nested loops | O(N) prefix sum + hash map | O(N) — same |
| **Two-sum** | O(N²) double loop | O(N log N) sort + two pointers | O(N) hash map (one pass) |
| **Sliding window max** | O(NK) recompute each window | O(N log K) heap | O(N) monotonic deque |
| **Top-K frequent** | O(N log N) full sort | O(N log K) min-heap of size K | O(N) bucket sort by frequency |
| **Longest increasing subsequence** | O(2^N) backtrack | O(N²) DP | O(N log N) patience sort |
| **Shortest path (weighted, ≥ 0)** | O(V·E) Bellman-Ford | — | O((V + E) log V) Dijkstra |
| **Count inversions** | O(N²) nested loops | — | O(N log N) merge sort augmented |
| **Kth largest element** | O(N log N) full sort | O(N log K) min-heap | O(N) avg quickselect |
| **Word prefix search** | O(W × L) per query | — | O(L) trie |
| **Next greater element** | O(N²) double scan | — | O(N) monotonic stack |
| **Overlapping intervals (non-overlapping max)** | O(N²) all pairs | — | O(N log N) sort by end + greedy |
| **Coin change** | O(N^(T/min)) backtrack | O(N × T) memo | O(N × T) tabulation, O(T) space |

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

**Bidirectional BFS** `🎯 T2` (when state space is huge): expand the smaller frontier each step, stop when frontiers meet. Cuts O(b^d) to O(b^(d/2)).

| Problem | State | Neighbor generation |
|---------|-------|---------------------|
| Word Ladder | word string | replace each char with a–z, keep if in dictionary (or wildcard buckets `h*t`) |
| Open the Lock | "0000" string | +1/-1 each of 4 wheels |
| Minimum Genetic Mutation | gene string | replace each char with A/C/G/T, keep if in bank |
| Sliding Puzzle | board tuple | swap 0 with adjacent cells |

---

## Follow-Up Chains — Interview Progression `⚡ T1`

> The five generic transformations behind every chain below: [HOW_TO_THINK § escalation grammar](HOW_TO_THINK.md#the-escalation-grammar-what-follow-ups-will-be).

Each chain is the order an interviewer escalates. Senior-only escalations (streaming, deletes, memory, scale): [INTERVIEW_JUDGMENT Part E](INTERVIEW_JUDGMENT.md#part-e--senior-follow-up-chains).

### Two Sum family
1. Two Sum (unsorted, hash map) → 2. Two Sum sorted (two pointers) → 3. 3Sum (fix one, two-pointer inner) → 4. 4Sum (fix two, two-pointer inner) → 5. Subarray Sum = K (prefix sum + hash map)

### Sliding Window family
1. Max sum of size-k subarray → 2. Longest substring with k distinct chars → 3. Minimum window substring → 4. Sliding window with frequency map and two pointers

### Binary Search family
1. Search in sorted array → 2. Search in rotated sorted array → 3. Find minimum in rotated array → 4. Search in 2D matrix → 5. Binary search on answer (capacity, split, minimize max)

### Tree DFS family
1. Max depth → 2. Path sum (root-to-leaf) → 3. Path sum III (any path, prefix sums) → 4. Lowest common ancestor → 5. Serialize/deserialize binary tree

### DP Linear family
1. Climb stairs → 2. House robber → 3. House robber II (circular: run twice) → 4. Decode ways → 5. Jump game II (greedy BFS over reach)

### Backtracking family
1. Subsets → 2. Combinations → 3. Permutations → 4. All three with duplicates (sort + skip) → 5. N-Queens / Sudoku (constraint + pruning)

### Graph BFS family
1. Number of islands (DFS/BFS) → 2. Walls and gates (multi-source BFS) → 3. Rotting oranges (multi-source BFS with time) → 4. Word ladder (implicit graph BFS) → 5. Alien dictionary (topological sort)

### Interval Scheduling family
1. Meeting rooms (any overlap?) → 2. Merge intervals → 3. Insert interval → 4. Non-overlapping intervals (min removals, sort by end) → 5. Meeting rooms II (min rooms, heap or sweep)

### Heap family
1. Kth largest element → 2. K closest points to origin → 3. Top K frequent elements → 4. Merge K sorted lists → 5. Find median from data stream (two heaps) → 6. Task scheduler (max-heap + cooldown queue, or formula)

---

## Hybrid Patterns `🎯 T2`

> How to *find* the seam between two patterns: [HOW_TO_THINK § two patterns with a seam](HOW_TO_THINK.md#hard-problems-are-two-patterns-with-a-seam).

When a problem combines two pattern families, name both upfront in the interview.

| Hybrid | When you see it | Example |
|--------|----------------|---------|
| **DP + Binary Search** | LIS-style: optimize over a sorted structure | Longest Increasing Subsequence O(N log N) |
| **Graph + DP** | Shortest path with state, DAG counting | Cheapest Flights Within K Stops, Longest Increasing Path in Matrix |
| **Backtracking + Memo** | Subproblems repeat in recursion tree | Word Break II, Palindrome Partitioning II |
| **Sort + Heap** | Sort by one key, dynamically pick best by another | Meeting Rooms II, IPO, Course Schedule III |
| **BFS + Binary Search** | "Minimum X such that Y is possible" in a grid/graph | Swim in Rising Water, Path With Minimum Effort |
| **Two Pointers + Hash Map** | Sliding window with constraint tracking | Minimum Window Substring, Fruit Into Baskets |
| **Trie + DFS** | Batch prefix queries, pruning on Trie branches | Word Search II |
| **Union-Find + Sort** | Process edges in weight order, merge components | Kruskal's MST, Redundant Connection |

**Naming hybrid patterns in interviews**: "This looks like a DP problem, but the recurrence needs to query a monotonic structure — so I'll use binary search on the DP array, which gives us O(N log N) instead of O(N²)."

---

## Phrase → Technique

### Arrays and strings

| Phrase / shape | Technique | Part |
|---|---|---|
| Sorted array, pair or triplet with target sum | Two pointers from both ends | [14](../striver-a2z/14-arrays/README.md), [22](../striver-a2z/22-sliding-window-and-2-pointer/README.md) |
| Longest / shortest **contiguous** subarray or substring with a condition | Variable sliding window (expand right, shrink left) | [22](../striver-a2z/22-sliding-window-and-2-pointer/01-sliding-window-theory.md) |
| **Count** subarrays with exactly K | `atMost(K) − atMost(K−1)` | [22](../striver-a2z/22-sliding-window-and-2-pointer/README.md) |
| Subarray sum = K with negatives | Prefix sum + hashmap of counts | [14](../striver-a2z/14-arrays/README.md), [15](../striver-a2z/15-hashing/README.md) |
| Maximum subarray sum | Kadane | [14](../striver-a2z/14-arrays/README.md) |
| Majority element (> n/2, > n/3) | Boyer–Moore voting | [14](../striver-a2z/14-arrays/README.md) |
| Values in 1..n, find missing / duplicate | Index marking, cyclic sort, XOR, or sum formulas | [14](../striver-a2z/14-arrays/README.md), [20](../striver-a2z/20-bit-manipulation/README.md) |
| Next permutation, rotate in place | Reversal tricks | [14](../striver-a2z/14-arrays/README.md) |
| Sort 0s/1s/2s | Dutch national flag (three pointers) | [14](../striver-a2z/14-arrays/README.md) |
| Merge / insert / overlap intervals | Sort by start, then sweep | [21](../striver-a2z/21-greedy-algorithms/README.md), [32 sweep](../striver-a2z/32-beyond-the-sheet/04-techniques-toolbox-theory.md) |
| Anagram, frequency, "same characters" | 26-count array | [11](../striver-a2z/11-basic-strings/README.md), [17](../striver-a2z/17-strings-basic-medium/00-string-basics-theory.md) |
| Longest palindromic substring | Expand around centre O(n²); Manacher O(n) `💤 T3` | [17](../striver-a2z/17-strings-basic-medium/README.md), [30 §12](../striver-a2z/30-strings-advanced/01-string-hashing-and-matching-theory.md) |
| Find a pattern in a text | KMP / Z-function / rolling hash | [30](../striver-a2z/30-strings-advanced/README.md) |
| Matrix spiral, rotate, set zeroes | Boundary pointers, transpose + reverse, first row/col as markers | [14](../striver-a2z/14-arrays/README.md) |

### Searching and ordering

| Phrase / shape | Technique | Part |
|---|---|---|
| Sorted or rotated-sorted array, find element / bound | Binary search, find the sorted half | [16](../striver-a2z/16-binary-search/01-binary-search-templates.md) |
| "Minimise the maximum" / "maximise the minimum" | Binary search on the answer + greedy feasibility check | [16](../striver-a2z/16-binary-search/README.md) (aggressive cows, book allocation, split array) |
| Smallest x such that f(x) holds, f monotone | Binary search on the answer | [16](../striver-a2z/16-binary-search/17-koko-eating-bananas.md) |
| Peak, bitonic | Binary search on the slope | [16](../striver-a2z/16-binary-search/24-find-peak-element.md) |
| Median / k-th of two sorted arrays | Binary search on the partition | [16](../striver-a2z/16-binary-search/25-median-of-two-sorted-arrays.md) |
| Row- and column-sorted matrix | Staircase from a corner, or flatten the index | [16](../striver-a2z/16-binary-search/README.md) |
| Count inversions / reverse pairs | Merge sort counting | [13](../striver-a2z/13-sorting/00-sorting-theory.md), [14](../striver-a2z/14-arrays/README.md) |
| K-th largest / smallest | Heap of size k or quickselect | [26](../striver-a2z/26-heaps/README.md) |
| Locally optimal choice is provably safe (exchange argument) | Greedy after sorting | [21](../striver-a2z/21-greedy-algorithms/01-greedy-fundamentals.md) |
| Max meetings / min platforms / activity selection | Sort by end time; sweep events | [21](../striver-a2z/21-greedy-algorithms/README.md) |

### Stacks, queues and heaps

| Phrase / shape | Technique | Part |
|---|---|---|
| Next / previous greater or smaller element | Monotonic stack | [23](../striver-a2z/23-stack-and-queues/15-next-greater-element.md) |
| Sum of subarray minimums or ranges, largest rectangle in a histogram | Monotonic stack, contribution technique (PSE/NSE) | [23](../striver-a2z/23-stack-and-queues/README.md) |
| Balanced brackets, undo, nested structure | Stack | [23](../striver-a2z/23-stack-and-queues/08-balanced-parenthesis.md) |
| Expression evaluation or conversion | Stack with precedence | [23](../striver-a2z/23-stack-and-queues/README.md) |
| Remove k digits, smallest lexicographic subsequence | Greedy monotonic stack | [23](../striver-a2z/23-stack-and-queues/20-remove-k-digits.md) |
| Sliding window max / min | Monotonic deque | [23](../striver-a2z/23-stack-and-queues/README.md) |
| Top k, k closest, k most frequent | Size-k heap | [26](../striver-a2z/26-heaps/01-heap-theory.md) |
| Merge k sorted lists or arrays | Min-heap of heads | [26](../striver-a2z/26-heaps/README.md) |
| Running median | Two heaps | [26](../striver-a2z/26-heaps/README.md) |
| Task scheduling with cooldown, reorganise string | Max-heap + greedy | [26](../striver-a2z/26-heaps/README.md) |

### Recursion and DP

| Phrase / shape | Technique | Part |
|---|---|---|
| "All" subsets, permutations, combinations, partitions | Backtracking (pick / not pick) | [18](../striver-a2z/18-recursion/01-subsequence-patterns.md) |
| Place items under constraints (N-Queens, Sudoku, colouring) | Backtracking with pruning | [18](../striver-a2z/18-recursion/README.md) |
| "Number of ways", "min/max cost", "is it possible", with overlapping choices | DP: recursion → memo → tabulation → space | [28](../striver-a2z/28-dynamic-programming/01-dp-theory.md) |
| Linear sequence, choose or skip each element | 1D DP (climbing stairs, house robber) | [28](../striver-a2z/28-dynamic-programming/README.md) |
| Grid paths with obstacles or costs | 2D grid DP | [28](../striver-a2z/28-dynamic-programming/README.md) |
| Target sum with items, capacity | Subset sum / 0-1 knapsack; unbounded if items repeat | [28](../striver-a2z/28-dynamic-programming/README.md) |
| Two strings: common, edit, match, wildcard | DP on strings `dp[i][j]` | [28](../striver-a2z/28-dynamic-programming/README.md) |
| Stock buy/sell with transactions or cooldown | State machine DP (day, holding, count) | [28](../striver-a2z/28-dynamic-programming/README.md) |
| Increasing subsequence, chains, envelopes | LIS; O(n log n) with binary search | [28](../striver-a2z/28-dynamic-programming/README.md) |
| Burst, merge, cut, partition a range | Interval / MCM DP by length | [28](../striver-a2z/28-dynamic-programming/README.md) |
| Largest square or rectangle of 1s | DP on squares; histogram per row | [28](../striver-a2z/28-dynamic-programming/README.md) |
| n ≤ 20, "visit all" | Bitmask DP `💤 T3` | [32 §2](../striver-a2z/32-beyond-the-sheet/02-advanced-dp-theory.md) |
| Count numbers in [L, R] with a digit property | Digit DP `💤 T3` | [32 §3](../striver-a2z/32-beyond-the-sheet/02-advanced-dp-theory.md) |
| Answer for every node as root | Rerooting `💤 T3` | [32 §5](../striver-a2z/32-beyond-the-sheet/02-advanced-dp-theory.md) |

### Trees

| Phrase / shape | Technique | Part |
|---|---|---|
| Height, diameter, balanced, max path sum | Post-order DFS returning a value, updating a global | [24](../striver-a2z/24-binary-trees/01-binary-tree-theory.md) |
| Level by level, zigzag, views, width | BFS with a level size; (column, level) maps for views | [24](../striver-a2z/24-binary-trees/README.md) |
| Root-to-node path, LCA | DFS returning found/not found | [24](../striver-a2z/24-binary-trees/README.md) |
| Build a tree from traversals | Inorder index map + preorder/postorder pointer | [24](../striver-a2z/24-binary-trees/README.md) |
| Serialise / deserialise | Preorder with null markers, or BFS | [24](../striver-a2z/24-binary-trees/README.md) |
| BST: search, floor/ceil, k-th smallest, validate | Use ordering; inorder is sorted; pass (min, max) bounds | [25](../striver-a2z/25-binary-search-trees/01-bst-theory.md) |
| Two-sum in a BST, BST iterator | Inorder iterator with a stack | [25](../striver-a2z/25-binary-search-trees/README.md) |
| Many LCA or k-th ancestor queries | Binary lifting `💤 T3` | [32 §1](../striver-a2z/32-beyond-the-sheet/03-advanced-trees-and-graphs-theory.md) |
| Prefix lookups, autocomplete, max XOR pair | Trie (binary trie for XOR) | [29](../striver-a2z/29-tries/01-trie-theory.md) |

### Graphs

| Phrase / shape | Technique | Part |
|---|---|---|
| Islands, regions, connected components, flood fill | DFS/BFS over a grid or adjacency list | [27](../striver-a2z/27-graphs/03-traversal-techniques-bfs-dfs.md) |
| Nearest distance from many sources, "minutes to rot" | Multi-source BFS | [27](../striver-a2z/27-graphs/09-rotten-oranges.md) |
| Shortest path, unit weights | BFS | [27](../striver-a2z/27-graphs/22-shortest-path-unit-weights.md) |
| Shortest path, non-negative weights | Dijkstra (heap) | [27](../striver-a2z/27-graphs/25-dijkstra.md) |
| Negative weights, detect a negative cycle, ≤ k edges | Bellman–Ford (k rounds for ≤ k stops) | [27](../striver-a2z/27-graphs/32-bellman-ford.md), [27](../striver-a2z/27-graphs/29-cheapest-flights-within-k-stops.md) |
| All-pairs shortest paths, n ≤ 400 | Floyd–Warshall `🎯 T2` | [27](../striver-a2z/27-graphs/33-floyd-warshall.md) |
| Minimise the max edge on a path | Dijkstra with max, or binary search + BFS, or DSU | [27](../striver-a2z/27-graphs/28-path-with-minimum-effort.md) |
| Weights only 0/1 | 0-1 BFS | [32 §5](../striver-a2z/32-beyond-the-sheet/03-advanced-trees-and-graphs-theory.md) |
| Prerequisites, ordering, dependencies | Topological sort (Kahn); cycle ⇔ not all nodes popped | [27](../striver-a2z/27-graphs/15-topological-sort-dfs-and-kahn.md) |
| Order of letters from a sorted dictionary | Topological sort on the derived edges | [27](../striver-a2z/27-graphs/20-alien-dictionary.md) |
| Two-colouring, "split into two groups" | Bipartite check (BFS colouring) | [27](../striver-a2z/27-graphs/14-bipartite-graph.md) |
| Dynamic connectivity, "are they connected after merges" | Disjoint set union | [27](../striver-a2z/27-graphs/37-disjoint-set.md) |
| Connect everything at minimum cost | MST (Kruskal + DSU, or Prim) | [27](../striver-a2z/27-graphs/02-mst-and-dsu-theory.md) |
| Critical connections, SCCs | Tarjan / Kosaraju — out of scope `💤 T3`; name it, move on | [27](../striver-a2z/27-graphs/45-bridges-in-graph.md) |
| Use every edge exactly once (itinerary) | Hierholzer `💤 T3` | [32 §4](../striver-a2z/32-beyond-the-sheet/03-advanced-trees-and-graphs-theory.md) |
| Word transformation | BFS on implicit graph (wildcard buckets) | [27](../striver-a2z/27-graphs/23-word-ladder-i.md) |

### Bits and maths

| Phrase / shape | Technique | Part |
|---|---|---|
| Every element twice except one | XOR all | [20](../striver-a2z/20-bit-manipulation/09-single-number-i.md) |
| Every element thrice except one | Count bits mod 3 | [20](../striver-a2z/20-bit-manipulation/10-single-number-ii.md) |
| Two unique numbers | XOR, split by the lowest set bit | [20](../striver-a2z/20-bit-manipulation/11-single-number-iii.md) |
| Power of two, count set bits, lowest bit | `n & (n−1)`, `n & −n` | [20](../striver-a2z/20-bit-manipulation/01-bits-and-tricks.md) |
| Enumerate subsets of ≤ 20 items | Mask from 0 to 2ⁿ − 1 | [20](../striver-a2z/20-bit-manipulation/13-power-set.md) |
| XOR of 1..n or a range | Period-4 formula | [20](../striver-a2z/20-bit-manipulation/14-xor-of-numbers-in-a-given-range.md) |
| Primes up to n, many factorisations | Sieve / smallest prime factor sieve | [31](../striver-a2z/31-maths/01-sieve-theory.md) |
| Divisors, primality of one number | √n loop | [8](../striver-a2z/08-basic-maths/README.md) |
| GCD, LCM, digit manipulation | Euclid, `% 10` peeling | [8](../striver-a2z/08-basic-maths/README.md) |
| xⁿ, huge exponent | Binary exponentiation | [18](../striver-a2z/18-recursion/02-pow-x-n.md), [31 §5](../striver-a2z/31-maths/05-modular-arithmetic-and-combinatorics-theory.md) |
| nCr, paths in a grid, Catalan structures | Factorials + inverses mod p | [31 §5](../striver-a2z/31-maths/05-modular-arithmetic-and-combinatorics-theory.md) |

### Linked lists, design and streams

| Phrase / shape | Technique | Part |
|---|---|---|
| LRU cache | Hashmap + doubly linked list | [23](../striver-a2z/23-stack-and-queues/README.md) |
| LFU cache | key → node, freq → DLL, `minFreq` | [32 §7](../striver-a2z/32-beyond-the-sheet/04-techniques-toolbox-theory.md) |
| Min stack | Pairs of (value, min) or an encoded difference | [23](../striver-a2z/23-stack-and-queues/README.md) |
| Linked list cycle, middle, k-th from end | Fast/slow pointers | [19](../striver-a2z/19-linked-list/README.md) |
| Reverse in groups, reorder, palindrome list | Reverse sub-lists, splice | [19](../striver-a2z/19-linked-list/README.md) |
| Uniform sample from a stream | Reservoir sampling | [32 §4](../striver-a2z/32-beyond-the-sheet/04-techniques-toolbox-theory.md) |
| Batch range adds, read once | Difference array | [32 §2](../striver-a2z/32-beyond-the-sheet/01-range-queries-theory.md) |

---

## When Stuck

Use the 60-second tree above to pick a candidate. If nothing fits: [HOW_TO_THINK §4 — the seven moves](HOW_TO_THINK.md#4-when-you-are-truly-stuck--the-seven-moves). If two candidates fit: [INTERVIEW_JUDGMENT B2](INTERVIEW_JUDGMENT.md#b2-choosing-between-two-plausible-approaches). DP state design: [Masterclass](RECURSION_AND_DP_MASTERCLASS.md).

---

## Flashcards

**What data structure should you reach for when you need to maintain a dynamic median from a stream of numbers?** #flashcard
**Two Heaps**: A Max-Heap for the lower half of the numbers, and a Min-Heap for the upper half. Keeping them balanced within size difference ≤ 1 allows retrieval of the median in O(1) time.

**What data structure should you use to find the "Next Greater Element" (NGE) for all indices of an array in O(N) total time?** #flashcard
**Monotonic Stack**: Keep a stack of indices/elements in strictly decreasing order. When you see a larger element, pop elements from the stack; this incoming element is their next greater element.

**When should you select a Trie instead of a HashSet for string lookups?** #flashcard
When you need **prefix matching** (e.g., autocomplete, finding all strings starting with prefix `P`), or when you need to prune a backtracking search space early by checking if a valid prefix path exists.

**What underlying data structures make up an LRU Cache with O(1) get and put performance?** #flashcard
A **HashMap** combined with a **Doubly Linked List (DLL)**. The DLL maintains the recency order (MRU at head, LRU at tail), and the HashMap maps keys directly to DLL Nodes for O(1) direct access and updates.

**When is an Adjacency List preferred over an Adjacency Matrix for graph representations?** #flashcard
For **sparse graphs** (where the number of edges E ≪ V²). An Adjacency List requires only O(V + E) space and allows O(degree) iteration over neighbors, whereas a matrix requires O(V²) space and O(V) neighbor iteration.

**Why does a variable sliding window fail on "subarray sum = K" with negative numbers, and what replaces it?** #flashcard
Shrinking the window no longer monotonically decreases the sum, so "invalid → shrink" has no proof. Use **prefix sum + hash map of counts**: count `prefix[running − K]` at each index, O(N).

**"Minimise the maximum" — what is the pattern and its two required pieces?** #flashcard
**Binary search on the answer.** (1) A monotone feasibility predicate `feasible(x)` (if x works, every larger x works). (2) A greedy O(N) check for it. Total O(N log range).

**When does BFS give shortest paths, and what do you use when it doesn't?** #flashcard
Only when every edge has the **same weight**. 0/1 weights → 0-1 BFS with a deque; non-negative weights → Dijkstra; negative weights or ≤ k edges → Bellman-Ford.

---

## See Also

- [HOW_TO_THINK.md](HOW_TO_THINK.md) — derive each pattern from first principles, then pressure-test on graded ladders
- [TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md](TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md) — canonical problems, traps, variants playbook
- [INTERVIEW_JUDGMENT.md](INTERVIEW_JUDGMENT.md) — live decisions, round cheatsheet, mocks, senior follow-up chains
- [mindmap.md](mindmap.md) — every practice problem by topic
