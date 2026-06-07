---
module: 01-data-structures
topic: Ds Tree
subtopic: 
status: unread
tags: [data-structures, ds-tree]
---

← [Data structures index](./README.md) · 🗺 [Master Decision Guide](../00-L3-EXECUTION-META/DECISION_GUIDE.md)
## First-Principles Map

```text
WHY tactical DS selection matters
├── Wrong DS = correct algorithm at wrong complexity
│   ├── Linear scan where O(1) lookup exists      → HashMap not Array
│   ├── Sorting repeatedly where heap suffices    → Heap not Sort
│   └── Prefix sum when segment tree overkill     → don't over-engineer
|   |-- Segment Tree — Use when updates happen at runtime alongside queries (Updates + range sum/min/max queries)
├── DS choice is the first decision — made before writing a single line
└── At SDE-3 level, interviewer expects O(1) time to name the right DS given constraints
│
WHAT the decision criteria are
├── Access pattern   — lookup by key? sequential? both ends? range?
├── Mutability       — static data (prefix sum) vs dynamic updates (segment tree / BIT)
├── Ordering needed  — arbitrary (hash) vs sorted (BST/TreeMap) vs partial (heap)
├── Key type         — integer (array/BIT) vs string (trie/hash) vs generic (TreeMap)
└── Frequency of ops — which operation dominates? optimize for that one
│
HOW to navigate the decision tree
├── Step 1: What is the dominant operation? (lookup / insert / delete / range / extremum)
├── Step 2: What are the key constraints? (sorted? dynamic? integer keys? prefix?)
├── Step 3: Map to DS family
│   ├── Lookup O(1)           → HashMap / HashSet
│   ├── Sorted + dynamic      → TreeMap / BST
│   ├── Min/Max always ready  → Heap (PriorityQueue)
│   ├── Prefix match          → Trie
│   ├── Range query + update  → Segment Tree / BIT
│   ├── Both ends             → Deque
│   ├── LIFO / NGE / parens   → Stack
│   └── Connectivity          → Graph + Union-Find
├── Step 4: Check for upgrade — does naive choice hit TLE?
│   ├── O(n) per query on n queries → O(n²) total → need O(log n) per query
│   └── Static range → prefix sum; dynamic range → segment tree
└── Step 5: Confirm complexity fits the constraint (n ≤ 10^5 → need O(n log n) or better)
│
WHEN advanced structures beat basics
├── Monotonic stack over simple stack  — next greater element (NGE), largest histogram
├── Two-heap over single heap          — running median (max-heap + min-heap)
├── Segment tree over prefix sum       — range queries WITH point updates
├── BIT (Fenwick) over segment tree    — simpler code when only prefix sums needed
├── Trie over set<string>              — O(L) per query vs O(L·log N) with set
└── Deque over queue                   — sliding window max needs O(1) front removal
│
WHAT CAN GO WRONG
├── Segment tree when prefix sum works     → over-engineered, coding time wasted
├── Array for key-value lookup             → O(n) search vs O(1) hash
├── HashMap when sorted order needed       → can't do floor/ceil; need TreeMap
├── Single heap for median                 → can't balance halves; need two heaps
├── Adjacency matrix for sparse graph      → O(V²) space, O(V) neighbor iteration
└── Brute force string matching over trie  → O(N·L) vs O(L) per query with trie
│
DECISION — access pattern → DS (tactical lookup table)
├── O(1) lookup by key (unordered)     → HashMap / HashSet
├── O(log n) ordered ops (floor/ceil)  → TreeMap / BST
├── O(1) min or max peek               → Heap (min or max)
├── Running median                     → Two heaps (max + min)
├── O(1) both-end access/removal       → Deque
├── LIFO / undo / NGE                  → Stack
├── Prefix word / autocomplete         → Trie
├── Static range sum/min/max           → Prefix sum array
├── Dynamic range sum/min/max          → Segment Tree / BIT
└── Dynamic connectivity               → Union-Find
```

## First-Principles Breakdown

- **Root problem:** Every problem has a dominant operation, and choosing a DS that makes that operation slow (O(n) instead of O(1) or O(log n)) produces a solution that is correct but fails at scale.
- **Core insight:** DS selection is a constraint-matching problem — map (access pattern, ordering requirement, key type, mutability) to the unique DS that satisfies all constraints at minimum complexity cost.
- **Invariant:** The dominant operation determines the DS; secondary operations determine variants (e.g., max-heap vs min-heap, segment tree vs BIT, deque vs queue).
- **Why it works:** Each DS encodes a structural invariant (heap property, BST ordering, trie prefix path, LIFO stack discipline) that makes its target operation cheap by definition — no runtime trick can replicate this.
- **Where it breaks:** Over-engineering (segment tree when prefix sum suffices) wastes interview time and signals poor judgment; under-engineering (array where hash needed) produces TLE — both are failure modes.

# The Data Structure Tree: Your Tactical Toolkit

> [!note] L3 Reference Document
> This file is a **reference / meta document** — read it once, use it as a lookup.
> Not a coding practice file. Do not deep-study it like a topic file.


Think of this as your "Map of the Hardware." When you're in an interview and the problem feels overwhelming, I want you to come back here. The secret to SDE-3 mastery isn't knowing every data structure; it's knowing **which tool to grab for which constraint.** 

If you need the "next greater" element, you reach for the **Monotonic Stack**. If you're maintaining a dynamic median, you reach for **Two Heaps**. This tree is your rapid-revision guide to making those structural decisions in seconds.

---

## 1. Arrays & Hashing

→ [array.md](./01-array.md) · [hashing.md](./02-hashing.md)
- **Two Pointers** — Using two indices to scan a sorted or linear structure from different directions or at different speeds.
    - *Patterns:* Opposite direction (Two Sum II), Same direction (Remove Duplicates), Sliding Window (Subarray Sum).
- **Sliding Window** — Maintaining a sub-segment of an array/string to satisfy specific frequency, sum, or character constraints.
    - *Fixed Window:* Find All Anagrams, Maximum Sum Subarray of size K.
    - *Variable Window:* Longest Substring Without Repeating Characters, Minimum Window Substring.
- **Prefix Sums / Precomputation** — Precomputing cumulative sums to answer range sum queries in O(1) or find specific subarray totals.
    - *Patterns:* Range Sum Query (1D & 2D), Subarray Sum Equals K (Prefix Sum + Hash Map).
- **Hashing Patterns** — Leveraging HashMaps/Sets for O(1) lookups, frequency tracking, and grouping.
    - *Variants:* Group Anagrams (Sorted key), Longest Consecutive Sequence (Hash Set), Subarray Sums Divisible by K.

## 2. Linked Lists

→ [linked-list.md](./07-linked-list.md)
- **Traversal & Basic Ops** — Standard pointer manipulation for list modification and structural analysis.
    - *Patterns:* Reverse a Linked List, Middle of the Linked List.
- **Two Pointers (Fast & Slow)** — Using two pointers at different speeds (Tortoise and Hare) for cycle and midpoint detection.
    - *Patterns:* Linked List Cycle I & II, Find the Kth node from the end.
- **List Reversal Variants** — Segmented or conditional list reversal requiring careful pointer rewiring.
    - *Patterns:* Reverse Nodes in k-Group, Reverse Linked List II (Segmented reversal).
- **Merging & Sorting** — Combining sorted lists or applying Divide & Conquer to unsorted linear structures.
    - *Patterns:* Merge Two Sorted Lists, Merge k Sorted Lists (Priority Queue), Sort List (Merge Sort).

## 3. Stacks & Queues

→ [stack.md](./05-stack.md) · [queue.md](./06-queue.md)
- **Monotonic Stack** — Maintaining a stack in sorted order to solve "Next Greater/Smaller" problems in O(N).
    - *Patterns:* Next Greater Element, Daily Temperatures, Largest Rectangle in Histogram, Trapping Rain Water.
- **Monotonic Queue** — Maintaining a queue of elements to efficiently track the max/min in a moving window.
    - *Patterns:* Sliding Window Maximum, Constrained Subsequence Sum.
- **System Design** — Implementing standard data structures with specific performance constraints or hybrid architectures.
    - *Patterns:* Min Stack, Implement Queue using Stacks, LRU Cache (DLL + Hash Map).

## 4. Trees (Binary, BST, N-ary)

→ [tree.md](./08-tree.md)
- **DFS Traversals** — Deep exploration of branches using recursion or an explicit stack.
    - *Patterns:* Inorder, Preorder, Postorder (Recursive vs Iterative with Stack).
- **BFS (Level Order)** — Layer-by-layer traversal; used for level-based analysis and shortest paths in unweighted trees.
    - *Patterns:* Binary Tree Level Order Traversal, Zigzag Level Order, Right Side View.
- **Tree Properties & Logic** — Recursive analysis of structural invariants and node relationships.
    - *Patterns:* Maximum Depth, Balanced Binary Tree, Same Tree, Invert Binary Tree.
- **Binary Search Tree (BST)** — Leveraging the `left < root < right` invariant for efficient search and validation.
    - *Patterns:* Validate BST, Kth Smallest Element in a BST, Lowest Common Ancestor (LCA) in BST.
- **Path & Subtree Problems** — Complex recursive logic involving path accumulation or tree serialization.
    - *Patterns:* Path Sum I, II, & III, Binary Tree Maximum Path Sum, Serialize and Deserialize Binary Tree.

## 5. Heaps (Priority Queues)

→ [heap.md](./10-heap.md)
- **Top K Elements** — Using a min/max-heap to track the largest/smallest elements in O(N log K).
    - *Patterns:* Kth Largest Element in an Array, Top K Frequent Elements, K Closest Points to Origin.
- **Merging K-Sorted Data** — Combining multiple sorted streams using a priority queue to maintain global order.
    - *Patterns:* Merge k Sorted Lists, Smallest Range Covering Elements from K Lists.
- **Two Heaps Pattern** — Using a min-heap and a max-heap together to maintain a dynamic median or balanced partitions.
    - *Patterns:* Find Median from Data Stream, IPO (Maximize Capital).

## 6. Graphs

→ [graphs.md](./13-graphs.md) · weighted algos: [graph.md](../02-algorithms/13-graph.md)
- **Representations** — Choosing between Adjacency Lists (Space-efficient) and Adjacency Matrices (Lookup-efficient).
    - *Patterns:* Adjacency List (Standard), Adjacency Matrix (Dense/Grid).
- **Basic Traversal** — Foundation for exploring connectivity and node relationships.
    - *BFS:* Shortest path in unweighted graph, Level-order expansion.
    - *DFS:* Reachability, Connected Components, Flood Fill.
- **Directed Graph Specifics** — Handling directed dependencies, cycles, and ordering.
    - *Patterns:* Cycle Detection (3-color DFS), Topological Sort (Kahn's BFS or DFS-based).
- **Shortest Paths** — Optimizing routes between nodes based on various edge weight constraints.
    - *Patterns:* Dijkstra (Non-negative weights), Bellman-Ford (Handles negative weights), Floyd-Warshall (All-pairs).
- **Spanning Trees** — Finding a subset of edges that connects all vertices with minimum total weight.
    - *Patterns:* Kruskal's MST (DSU), Prim's MST.

## 7. Matrices & Grids

→ [array.md](./01-array.md) (spiral / in-place) · [graphs.md](./13-graphs.md) (islands, flood fill)
- **Matrix Traversal** — Systematic exploration of 2D grids using specific spatial patterns.
    - *Patterns:* Spiral Matrix, Diagonal Traverse, Transpose Matrix.
- **In-place Manipulation** — Modifying matrix structure without allocating significant extra space.
    - *Patterns:* Rotate Image (Transpose + Reverse), Set Matrix Zeroes.
- **Grid Patterns** — Applying graph algorithms (DFS/BFS) to coordinate-based grid systems.
    - *Patterns:* Number of Islands (DFS/BFS), Word Search (Backtracking).

## 8. Advanced Structures

- **Trie (Prefix Tree)** — Optimized string storage and prefix retrieval; essential for dictionary-based apps.
    - *Patterns:* Implement Trie, Word Search II (Trie + DFS).
- **Disjoint Set Union (DSU)** — Tracking connected components and dynamic merging with near-O(1) performance.
    - *Patterns:* Redundant Connection, Accounts Merge (Group elements).
- **Segment Trees / Fenwick Trees** — Advanced structures for efficient range updates and range queries in O(log N).
    - *Patterns:* Range Sum Query - Mutable, Count of Smaller Numbers After Self.

## 9. Concurrency Primitives
- **Semaphores & Mutexes** — Atomic locks and signals for multi-threaded resource management.
- **Bounded Blocking Queues** — Thread-safe buffers for data exchange between producers and consumers.
- **Atomic Variables** — Lock-free primitives for thread-safe value updates (CAS).

## 10. Distributed & System Design Structures
- **LRU / LFU Cache** — Hybrid structures (DLL + Map) for efficient item eviction and retrieval.
- **Consistent Hashing Ring** — Circular partitioning of keys across dynamic node sets.
- **Bloom Filters & Count-Min Sketch** — Probabilistic structures for high-cardinality data streams.
- **Quadtrees & Geohash** — Spatial data structures for proximity-based search and 2D partitioning.

---

## How to use this tree
1. **Analyze the Data Type**: Is the input a list, a grid, a tree, or a set of nodes?
2. **Select the Tool**: Choose the appropriate structure (e.g., "I need to find the nearest larger element → Monotonic Stack").
3. **Identify the Pattern**: Match the problem to a structural pattern (e.g., "I need level-by-level info → BFS / Level Order").
4. **Optimize**: Check if a more advanced structure (like DSU or a Heap) can reduce the time complexity from O(N²) to O(N log N) or O(α(N)).

## Flashcards

**What data structure should you reach for when you need to maintain a dynamic median from a stream of numbers?** #flashcard
**Two Heaps**: A Max-Heap for the lower half of the numbers, and a Min-Heap for the upper half. Keeping them balanced within size difference $\le 1$ allows retrieval of the median in $O(1)$ time.

**What data structure should you use to find the "Next Greater Element" (NGE) for all indices of an array in O(N) total time?** #flashcard
**Monotonic Stack**: Keep a stack of indices/elements in strictly decreasing order. When you see a larger element, pop elements from the stack; this incoming element is their next greater element.

**When should you select a Trie instead of a HashSet for string lookups?** #flashcard
When you need **prefix matching** (e.g., autocomplete, finding all strings starting with prefix `P`), or when you need to prune a backtracking search space early by checking if a valid prefix path exists.

**What underlying data structures make up an LRU Cache with O(1) get and put performance?** #flashcard
A **HashMap** combined with a **Doubly Linked List (DLL)**. The DLL maintains the recency order (MRU at head, LRU at tail), and the HashMap maps keys directly to DLL Nodes for $O(1)$ direct access and updates.

**When is an Adjacency List preferred over an Adjacency Matrix for graph representations?** #flashcard
For **sparse graphs** (where the number of edges $E \ll V^2$). An Adjacency List requires only $O(V + E)$ space and allows $O(\text{degree})$ iteration over neighbors, whereas a matrix requires $O(V^2)$ space and $O(V)$ neighbor iteration.

**What structure is required for range queries (Sum/Min/Max) with dynamic point updates, both in O(log N) time?** #flashcard
A **Segment Tree** (or **Fenwick Tree / BIT** if only prefix sums are needed). They balance static prefix arrays (which have $O(1)$ query but $O(N)$ update) and raw arrays (which have $O(N)$ query but $O(1)$ update).

