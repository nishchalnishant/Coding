# Master Decision Guide — DS + Algorithm Selection

> **How to use:** Read the problem. Find the matching keyword row. Pick the DS or algorithm. Done.
> This file merges `ds_tree.md` + `algorithm_tree.md` into one exhaustive lookup.

---

## PART 1 — The 5-Step Decision Protocol

Run this mental checklist for **every** problem before writing any code.

```
Step 1 ── What is the dominant operation?
          Lookup | Insert/Delete | Search | Range Query | Extremum | Count | Enumerate | Path

Step 2 ── What are the constraints?
          Static vs Dynamic data | Sorted vs Unsorted | Integer vs String keys
          n ≤ 20 | n ≤ 10³ | n ≤ 10⁵ | n ≤ 10⁶ | n ≤ 10⁷

Step 3 ── Map to the family (use Part 2 keyword table)

Step 4 ── Complexity check — does it fit?
          n ≤ 20    → O(2ⁿ) is fine   (backtracking / bitmask DP)
          n ≤ 10³   → O(n²) is fine   (DP, nested loops)
          n ≤ 10⁵   → O(n log n) max  (sort, heap, binary search, BFS/DFS)
          n ≤ 10⁶   → O(n) required   (two pointers, sliding window, prefix sum)
          n ≤ 10⁷⁺  → O(n) only       (linear scan / bitwise)

Step 5 ── Check for upgrade
          O(n) per query × n queries = O(n²) total → need O(log n) per query
          Static data? → Prefix sum (O(1) query)
          Dynamic data (updates)? → Segment Tree / BIT (O(log n) query + update)
```

---

## PART 2 — Keyword → DS / Algorithm (Master Table)

### 🔑 Keywords are the exact phrases you see in problem statements.

| Keywords / Patterns You See | → Use | Complexity |
| :--- | :--- | :--- |
| **"find two numbers that sum to target"** | HashMap complement | O(N) |
| **"find pair with sum", "complement exists"** | HashMap / HashSet | O(N) |
| **"count frequency", "most common", "top K"** | Counter + HashMap | O(N) |
| **"group by anagram", "same characters"** | HashMap, sorted-char key | O(N·L) |
| **"subarray sum equals K"** | Prefix sum + HashMap | O(N) |
| **"range sum query" (static array)** | Prefix sum array | O(1) query |
| **"range sum/min/max WITH point updates"** | Fenwick Tree / Segment Tree | O(log N) |
| **"range update AND range query"** | Segment Tree + Lazy Propagation | O(log N) |
| **"longest substring / subarray"** | Sliding window (variable) | O(N) |
| **"minimum window", "smallest window containing all chars"** | Sliding window + freq map | O(N) |
| **"subarray / substring of fixed size K"** | Sliding window (fixed) | O(N) |
| **"sorted array, find target"** | Binary search `lo ≤ hi` | O(log N) |
| **"rotated sorted array"** | Binary search — identify sorted half | O(log N) |
| **"find minimum K such that condition holds"** | Binary search on answer + `feasible(mid)` | O(N log N) |
| **"minimize the maximum", "maximize the minimum"** | Binary search on answer | O(N log N) |
| **"two numbers in sorted array"** | Two pointers (converging) | O(N) |
| **"3Sum", "triplets summing to"** | Sort + two pointers | O(N²) |
| **"remove duplicates", "move zeros to end"** | Two pointers (same direction) | O(N) |
| **"Dutch National Flag", "sort 0/1/2"** | Three-pointer partition | O(N) |
| **"maximum subarray sum"** | Kadane's algorithm | O(N) |
| **"maximum product subarray"** | Kadane's variant (track min too) | O(N) |
| **"all K largest / K smallest"** | Min-heap size K | O(N log K) |
| **"K closest points"** | Max-heap size K or QuickSelect | O(N log K) |
| **"dynamic median", "median from stream"** | Two heaps (max lower + min upper) | O(log N) per add |
| **"merge K sorted lists/arrays"** | K-way merge min-heap | O(N log K) |
| **"always extract current min or max"** | Heap (min-heap default; negate for max) | O(log N) |
| **"sliding window min/max"** | Monotonic deque (store indices) | O(N) |
| **"next greater element", "daily temperatures"** | Monotonic stack (decreasing) | O(N) |
| **"largest rectangle in histogram"** | Monotonic stack (increasing) | O(N) |
| **"valid parentheses", "matching brackets"** | Stack — push opens, match closes | O(N) |
| **"LIFO", "undo/redo", "DFS iterative"** | Stack | O(N) |
| **"FIFO", "BFS", "level-order"** | Queue (deque in Python) | O(N) |
| **"all strings starting with prefix", "autocomplete"** | Trie | O(L) per op |
| **"word search in a grid"** + dictionary | Trie + grid DFS + backtrack | O(W·L + R·C·4^L) |
| **"shortest path" (unweighted graph / grid)** | BFS | O(V+E) |
| **"shortest path" (non-negative weights)** | Dijkstra + min-heap | O((V+E) log V) |
| **"shortest path" (negative weights or K stops)** | Bellman-Ford | O(V·E) |
| **"all-pairs shortest path"** | Floyd-Warshall | O(V³) |
| **"0/1 weight edges"** | 0-1 BFS (deque) | O(V+E) |
| **"all cells spread simultaneously"** | Multi-source BFS | O(V+E) |
| **"connected components", "number of islands", "flood fill"** | DFS / BFS from unvisited nodes | O(V+E) |
| **"dependency ordering", "prerequisites"** | Kahn's topo sort (BFS in-degree) | O(V+E) |
| **"detect cycle in directed graph"** | DFS 3-color OR Kahn's (cycle ↔ len < n) | O(V+E) |
| **"connected / disconnected?", "union two groups"** | Union-Find (DSU) | O(α) |
| **"minimum spanning tree"** | Kruskal (sort edges + DSU) / Prim (heap) | O(E log E) |
| **"cycle in undirected graph"** | Union-Find — first edge where find(u)==find(v) | O(E·α) |
| **"count ways", "how many paths", "number of arrangements"** | DP (define state, write recurrence) | varies |
| **"minimum cost / steps to reach"** | DP bottom-up or Dijkstra | varies |
| **"overlapping subproblems"** | DP with memoization (top-down) | varies |
| **"subsequence" (not contiguous)** | LCS DP 2D table | O(N·M) |
| **"substring" (contiguous)** | Sliding window or DP | O(N) or O(N²) |
| **"pick items once with weight limit"** | 0/1 Knapsack — iterate W **backward** | O(N·W) |
| **"pick items unlimited with weight limit"** | Unbounded Knapsack — iterate W **forward** | O(N·W) |
| **"partition array into two equal parts"** | 0/1 Knapsack to target = total/2 | O(N·total) |
| **"all valid combinations", "generate all"** | Backtracking (choose→recurse→undo) | O(k^n) |
| **"all permutations"** | Backtracking with `used[]` | O(N!) |
| **"all subsets / power set"** | Backtracking with `start` index | O(2^N) |
| **"N-Queens", "constraint satisfaction"** | Backtracking with constraint sets | O(N!) |
| **"local optimal = global optimal"** | Greedy + exchange argument | O(N log N) |
| **"interval scheduling", "non-overlapping"** | Greedy — sort by end time | O(N log N) |
| **"merge overlapping intervals"** | Sort by start + sweep | O(N log N) |
| **"minimum rooms / resources needed"** | Heap of end-times (or sweep line) | O(N log N) |
| **"jump game", "can reach end"** | Greedy — track farthest reachable | O(N) |
| **"cycle detection in linked list"** | Floyd's fast/slow pointers | O(N) O(1) |
| **"k-th from end", "remove n-th from end"** | Two-pointer with k-offset | O(N) |
| **"LRU Cache"** | HashMap + Doubly Linked List | O(1) all ops |
| **"level order traversal", "BFS on tree"** | Queue + level-size snapshot | O(N) |
| **"lowest common ancestor"** | Postorder DFS / BST property walk | O(H) |
| **"validate BST"** | DFS with (lo, hi) bounds propagated down | O(N) |
| **"tree path sum" (any start/end)** | Tree DP — postorder, global closure | O(N) |
| **"serialize / deserialize tree"** | Preorder + null markers | O(N) |
| **"pattern matching in string"** | KMP (single pattern O(N+M)) or Rabin-Karp | O(N+M) |
| **"count inversions"** | Merge sort during merge step | O(N log N) |
| **"XOR of pairs", "single number"** | Bit manipulation (a^a=0; a^0=a) | O(N) |
| **"all paths in a DAG"** | DFS backtracking (no visited set — DAG has no cycles) | O(V+E) |
| **"state machine (hold/sell/cooldown)"** | DP — track all states at each step | O(N) |
| **"bipartite check", "2-coloring graph"** | BFS/DFS coloring | O(V+E) |
| **"reconstruct from traversal"** | Preorder + inorder → HashMap + recursion | O(N) |
| **"reverse linked list"** | Three-pointer: prev, curr, nxt | O(N) O(1) |
| **"matrix shortest path (0s/1s)"** | BFS (8-directional if allowed) | O(R·C) |
| **"reverse words", "palindrome check"** | Two pointers / string manipulation | O(N) |

---

## PART 3 — Complexity Budget Decision

Pick the right family based purely on n.

```
n ≤ 20         → Full Backtracking or Bitmask DP   (O(2ⁿ) or O(2ⁿ · N))
n ≤ 10²        → Any O(N³) or O(N²·log N) is OK
n ≤ 10³        → O(N²) acceptable                 (DP, nested loops)
n ≤ 10⁴        → O(N² ) is borderline — try O(N log N) first
n ≤ 10⁵        → Must be O(N log N) or better     (heap, sort, BFS, binary search)
n ≤ 10⁶        → Must be O(N) or O(N log N) tight (sliding window, prefix sum, two pointers)
n ≤ 10⁷⁺       → Must be O(N) strictly            (linear scan only)
```

---

## PART 4 — DS Selection Matrix

When you know the data type but not the algorithm — use this.

| Data Type | Key Constraint | → Choose |
| :--- | :--- | :--- |
| Integers | Arbitrary O(1) lookup | HashMap / HashSet |
| Integers | Sorted, range, floor/ceil | TreeMap / SortedList |
| Integers | Always need min or max | Heap (min default; negate for max) |
| Integers | Need both min AND max simultaneously | Two Heaps |
| Integers | Static, range sum queries | Prefix Sum Array |
| Integers | Dynamic (updates), range queries | Segment Tree / BIT |
| Integers | Range updates + range queries | Segment Tree + Lazy Propagation |
| Strings | Exact match lookup | HashMap |
| Strings | Prefix queries, autocomplete | Trie |
| Strings | Single pattern search in text | KMP (O(N+M)) |
| Strings | Sliding window of chars | Sliding Window + Counter |
| Nodes | Hierarchical, parent-child | Tree (Binary / N-ary) |
| Nodes | Any relationships, cycles possible | Graph + DFS/BFS |
| Nodes | Dynamic group membership | Union-Find (DSU) |
| Nodes | Dependency chains | Topological Sort |
| Nodes | Unweighted shortest path | BFS |
| Nodes | Weighted shortest path | Dijkstra |
| Sequence | LIFO access | Stack |
| Sequence | FIFO access | Queue / Deque |
| Sequence | Both-end access | Deque |
| Sequence | In-order dynamic max/min | Monotonic Stack / Monotonic Deque |

---

## PART 5 — Algorithm Family Selector

When you know the problem TYPE — use this.

| Problem Type | Signal | → Algorithm |
| :--- | :--- | :--- |
| **Optimization** | "minimize", "maximize", overlapping subproblems | DP |
| **Counting** | "how many ways", "count paths" | DP |
| **Exhaustive** | "all combinations", "generate all" | Backtracking |
| **Greedy** | "interval", "scheduling", local optimal = global | Greedy + sort |
| **Connectivity** | "connected", "component", "path exists" | BFS / DFS |
| **Dependency** | "prerequisite", "ordering", DAG | Topological Sort |
| **Shortest Path** | "minimum steps", "fewest hops" | BFS (unweighted) / Dijkstra (weighted) |
| **Dynamic groups** | "union", "merge groups", "connected pairs" | Union-Find |
| **Sorted search** | "find in sorted", "monotone feasibility" | Binary Search |
| **String pattern** | "does pattern exist", "find occurrences" | KMP / Rabin-Karp |

---

## PART 6 — Common Upgrade Rules (Brute → Optimal)

| Brute Force | Why It Fails | Upgrade To |
| :--- | :--- | :--- |
| O(N²) nested loop for pair sum | TLE at N=10⁵ | Sort + two pointers → O(N log N) |
| O(N²) scan per window | TLE | Sliding window → O(N) |
| O(2^N) recursion with repeats | TLE | Memoization (top-down DP) → O(N²) |
| O(N) range query × N queries | O(N²) total | Prefix sum (static) or Segment Tree (dynamic) → O(N log N) |
| O(N·L) string search | TLE | KMP → O(N+L) |
| O(N·L) set<string> prefix | TLE | Trie → O(L) per query |
| O(N²) connectivity queries | TLE | Union-Find → O(N·α) |
| O(V²) BFS per source | TLE | Multi-source BFS → O(V+E) |
| O(N log N) sort + search per query | TLE | Binary search on monotone answer → O(N log N) total |
| Simple stack for NGE | O(N²) | Monotonic stack → O(N) |
| Single sort for median | O(N log N) per insert | Two heaps → O(log N) per insert |

---

## PART 7 — What Can Go Wrong (Anti-patterns)

| Mistake | Symptom | Correct Fix |
| :--- | :--- | :--- |
| Array for O(1) key lookup | TLE (O(N) per lookup) | HashMap |
| HashMap when floor/ceil needed | Wrong answer | TreeMap / SortedList |
| Prefix sum when updates exist | Wrong answer after update | Segment Tree / BIT |
| Segment Tree when no updates | Over-engineered, wasted time | Prefix Sum |
| Single heap for median | Can't split halves | Two Heaps |
| BFS for weighted shortest path | Wrong answer | Dijkstra |
| Greedy without exchange proof | Wrong answer (coin change etc.) | DP |
| Backtracking for DP problems | TLE (exponential) | DP with memoization |
| DFS for shortest path in grid | Wrong answer (not guaranteed shortest) | BFS |
| Marking visited AFTER dequeue | Duplicate processing, wrong distances | Mark BEFORE enqueue |
| Adjacency matrix for sparse graph | O(V²) space, TLE | Adjacency list |
| Not popping before pushing in DP | Wrong recurrence direction | Trace through one example |
| `list.pop(0)` in Python | O(N) → TLE | `collections.deque.popleft()` |
| `heapq` for max-heap | Wrong order | Negate values or use `(-val, item)` |

---

## PART 8 — Last-Minute Keyword Drill

> Read this the morning of your interview. One pattern per line.

```
"two numbers sum to target"         → HashMap complement (one pass)
"subarray sum equals K"             → Prefix sum + hash map
"maximum subarray"                  → Kadane's (reset when negative)
"all words with prefix"             → Trie
"shortest path" (unweighted)        → BFS (mark visited BEFORE enqueue)
"shortest path" (weighted)          → Dijkstra (skip stale: if d > dist[u]: continue)
"dependency order / prerequisites"  → Kahn's topo sort (cycle ↔ len < n)
"all cells spread simultaneously"   → Multi-source BFS
"max/min in sliding window of K"    → Monotonic deque (store indices not values)
"always extract current min/max"    → Heap (min-heap; negate for max)
"K-th largest"                      → Min-heap size K / QuickSelect O(N) avg
"merge K sorted"                    → K-way merge heap (val, idx, elem)
"dynamic median"                    → Two heaps (max lower + min upper)
"cycle in linked list"              → Floyd's fast/slow (slow is fast identity)
"reverse linked list"               → Three-pointer prev/curr/nxt (save nxt FIRST)
"max path through tree"             → Tree DP postorder (global closure for cross-arm)
"level order / level count"         → BFS snapshot len(queue) each level
"count components / flood fill"     → DFS/BFS outer loop over all unvisited
"sort tasks with prerequisites"     → Topological sort Kahn's
"0/1 pick items hit weight"         → 0/1 Knapsack iterate W backward
"count subsets / permutations"      → Backtracking (always undo after recurse)
"minimize max / maximize min"       → Binary search on answer + feasible(mid)
"interval scheduling / merge"       → Sort by start/end; greedy sweep
"XOR of pairs / single number"      → XOR bit trick (a^a=0; a^0=a)
"pattern match in string"           → KMP O(N+M); Rabin-Karp for multiple
"state machine hold/sell/cooldown"  → DP track all states simultaneously
"local optimal = global optimal"    → Greedy (prove exchange argument first)
"all paths in DAG"                  → DFS backtrack (no visited set needed in DAG)
```

---

## PART 9 — Data Structure Properties Cheat Sheet

| DS | Insert | Delete | Lookup | Min/Max | Range | Ordered | Notes |
| :-- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| Array | O(N) | O(N) | O(1) | O(N) | O(N) | ✗ | O(1) random access by index |
| HashMap | O(1) avg | O(1) avg | O(1) avg | O(N) | ✗ | ✗ | Worst case O(N) on collision |
| HashSet | O(1) avg | O(1) avg | O(1) avg | O(N) | ✗ | ✗ | Same as HashMap without values |
| Sorted Array | O(N) | O(N) | O(log N) | O(1) | O(log N) | ✓ | Binary search; poor insert |
| BST (balanced) | O(log N) | O(log N) | O(log N) | O(log N) | O(log N) | ✓ | TreeMap in Java / SortedList in Python |
| Min-Heap | O(log N) | O(log N) | O(N) | O(1) peek | ✗ | partial | Python `heapq` default |
| Max-Heap | O(log N) | O(log N) | O(N) | O(1) peek | ✗ | partial | Negate in Python |
| Stack | O(1) | O(1) | O(N) | ✗ | ✗ | ✗ | LIFO |
| Queue (deque) | O(1) | O(1) | O(N) | ✗ | ✗ | ✗ | FIFO; `deque.popleft()` O(1) |
| Trie | O(L) | O(L) | O(L) | ✗ | ✗ | prefix | L = key length |
| Prefix Sum | — | — | O(1) | — | O(1) | — | Static only; O(N) build |
| Segment Tree | O(log N) | O(log N) | O(log N) | O(log N) | O(log N) | — | Dynamic + range |
| Fenwick / BIT | O(log N) | O(log N) | O(log N) | — | O(log N) | — | Prefix sums only; simpler code |
| Union-Find | O(α) | — | O(α) | — | — | — | Dynamic connectivity |
| Monotonic Stack | O(N) total | — | — | — | — | ✗ | NGE, histogram problems |
| Monotonic Deque | O(N) total | — | O(1) front | O(1) front | — | ✗ | Sliding window max/min |

---

*This file synthesises `01-data-structures/ds_tree.md` and `02-algorithms/algorithm_tree.md`.*
*For deep-dives, go to the individual topic files under `01-data-structures/` and `02-algorithms/`.*
