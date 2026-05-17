# The Data Structure Tree: Your Tactical Toolkit

Think of this as your "Map of the Hardware." When you're in an interview and the problem feels overwhelming, I want you to come back here. The secret to SDE-3 mastery isn't knowing every data structure; it's knowing **which tool to grab for which constraint.** 

If you need the "next greater" element, you reach for the **Monotonic Stack**. If you're maintaining a dynamic median, you reach for **Two Heaps**. This tree is your rapid-revision guide to making those structural decisions in seconds.

---

## 1. Arrays & Hashing
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
- **Traversal & Basic Ops** — Standard pointer manipulation for list modification and structural analysis.
    - *Patterns:* Reverse a Linked List, Middle of the Linked List.
- **Two Pointers (Fast & Slow)** — Using two pointers at different speeds (Tortoise and Hare) for cycle and midpoint detection.
    - *Patterns:* Linked List Cycle I & II, Find the Kth node from the end.
- **List Reversal Variants** — Segmented or conditional list reversal requiring careful pointer rewiring.
    - *Patterns:* Reverse Nodes in k-Group, Reverse Linked List II (Segmented reversal).
- **Merging & Sorting** — Combining sorted lists or applying Divide & Conquer to unsorted linear structures.
    - *Patterns:* Merge Two Sorted Lists, Merge k Sorted Lists (Priority Queue), Sort List (Merge Sort).

## 3. Stacks & Queues
- **Monotonic Stack** — Maintaining a stack in sorted order to solve "Next Greater/Smaller" problems in O(N).
    - *Patterns:* Next Greater Element, Daily Temperatures, Largest Rectangle in Histogram, Trapping Rain Water.
- **Monotonic Queue** — Maintaining a queue of elements to efficiently track the max/min in a moving window.
    - *Patterns:* Sliding Window Maximum, Constrained Subsequence Sum.
- **System Design** — Implementing standard data structures with specific performance constraints or hybrid architectures.
    - *Patterns:* Min Stack, Implement Queue using Stacks, LRU Cache (DLL + Hash Map).

## 4. Trees (Binary, BST, N-ary)
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
- **Top K Elements** — Using a min/max-heap to track the largest/smallest elements in O(N log K).
    - *Patterns:* Kth Largest Element in an Array, Top K Frequent Elements, K Closest Points to Origin.
- **Merging K-Sorted Data** — Combining multiple sorted streams using a priority queue to maintain global order.
    - *Patterns:* Merge k Sorted Lists, Smallest Range Covering Elements from K Lists.
- **Two Heaps Pattern** — Using a min-heap and a max-heap together to maintain a dynamic median or balanced partitions.
    - *Patterns:* Find Median from Data Stream, IPO (Maximize Capital).

## 6. Graphs
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
    - *Deep Dive:* [Segment Trees](segment-tree.md).

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
