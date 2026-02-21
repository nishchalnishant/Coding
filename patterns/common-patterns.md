# Common Data Structures & Algorithms

A quick-reference guide to standard DSA concepts.

## Data Structures

### 1. Arrays
- **Prefix Sum:** $O(1)$ range sum queries.
- **Sliding Window:** Subarray optimization constraints.
- **Two Pointers:** Pair searching, merging, in-place deduplication.
- **Binary Search:** $O(\log n)$ search on sorted arrays.
- **Kadane's Algorithm:** Max sum subarray.

### 2. Linked Lists
- **Fast and Slow Pointers:** Cycle detection (Floyd's).
- **In-Place Reversal:** Reverse segments with $O(1)$ space.
- **Merge Lists:** Combining sorted structures.

### 3. Hashing
- **Frequency Maps:** Count occurrences.
- **Two Sum:** $O(N)$ lookup for target pairs.
- **Anagram Grouping:** Character frequency arrays as keys.

### 4. Stacks & Queues
- **Monotonic Stack:** Next Greater/Smaller Element.
- **Balanced Parentheses:** Stateful string parsing.
- **Sliding Window Max:** Deque tracking monotonic sequences.

### 5. Trees (Binary, BST, Tries)
- **DFS / BFS:** Depth vs Level-order exploration.
- **BST Properties:** Inorder yields sorted order. $O(\log n)$ search.
- **Trie:** Prefix matching, word search dictionaries.

### 6. Heaps / Priority Queues
- **Top K Elements:** Min/Max heaps for frequency or value.
- **Median of Stream:** Two-heap balancing approach.

### 7. Graphs
- **DFS/BFS:** Connected components, shortest unweighted path.
- **Dijkstra's:** Shortest path (weighted).
- **Topological Sort:** Task dependencies (Kahn's algorithm).
- **Union-Find:** Dynamic connectivity, cycle detection (undirected).

---

## Algorithms

### 1. Sorting
- **Merge Sort:** $O(N \log N)$ divide-and-conquer (stable).
- **Quick Sort:** $O(N \log N)$ average, in-place partitioning.
- **Bucket / Counting Sort:** $O(N)$ for restricted domains.

### 2. Binary Search
- Core templates for bounds checking: `mid = left + (right - left) // 2`.
- Binary Search on Answer Space (e.g. Min max capacity).

### 3. Recursion & Backtracking
- **Backtracking:** State -> Explore -> Un-State.
- Examples: Subsets, Permutations, N-Queens, Sudoku.

### 4. Greedy
- **Activity Selection:** Max non-overlapping intervals (sort by end time).
- **Huffman Coding:** Optimal compression.
- **Jump Game:** Max reachability tracking.

### 5. Dynamic Programming (DP)
- **Memoization / Tabulation:** Overlapping subproblems.
- **Classic DP:** Knapsack (0/1 or Unbounded), LCS, LIS, Matrix Chain Multiplication.
