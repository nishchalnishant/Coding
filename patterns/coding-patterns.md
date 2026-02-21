# Coding Patterns Index

Essential algorithmic techniques to recognize during SDE 3 interviews.

## 1. Prefix Sum
Use for $O(1)$ sum queries on subarrays.
- *Examples*: Product of Array Except Self, Longest Subarray with sum K, Min removals for target sum.
- *Tip*: Combine a Prefix Sum with a Hash Map (`{sum: index}`) to find target sums in $O(N)$ time.

## 2. Two Pointers
- *Converging*: Sorted Array Target Sum (3Sum, Container With Most Water).
- *Cycle Detection*: Fast/Slow pointers (Linked List Cycle, Find Duplicate Number).
- *In-Place Mod*: Remove Duplicates, Move Zeroes.

## 3. Sliding Window
- *Fixed Size*: Calculations on contiguous $k$-length elements.
- *Variable Size*: Expand right pointer, conditionally shrink left pointer (Longest Substring Without Repeating Characters).
- *Monotonic Queue*: Track sliding max/min in $O(N)$ (Sliding Window Maximum).

## 4. Stack & Queues
- *Monotonic Stack*: Find the 'Next Greater Element'. Stack maintains elements in increasing/decreasing order.
- *Min Stack*: Stack that tracks the minimum element at each push in $O(1)$.

## 5. Binary Search Variations
- *Rotated Sorted Arrays*: Find the sorted half, then decide to search left or right.
- *Binary Search on Answer*: Guess a value `mid` and check if it satisfies constraints (e.g. Koko Eating Bananas).

## 6. Matrix & Array Manipulation
- *In-place Rotation*: Transpose then reverse rows.
- *Spiral Traversal*: Manage 4 boundary pointers (top, bottom, left, right).
- *Set Matrix Zeroes*: Use first row/col as markers to save $O(M \times N)$ space.

## 7. Graph Traversal Options
- *DFS*: Recursion-heavy. Good for Connected Components, Cycle Detection.
- *BFS*: Queue-heavy. Good for Shortest Path.
- *Topological Sort*: Kahn's algorithm (In-Degree Array) for dependency resolution.
- *Advanced Paths*: Dijkstra's (Shortest Path without negative weights), Bellman-Ford (negative weights okay).
- *Union-Find*: Best for "Dynamic connectivity" tasks (e.g., Kruskal's MST, validating trees).

## 8. Dynamic Programming
- *1D Recurrence*: Fibonacci, Climbing Stairs, House Robber.
- *2D Grid*: Unique Paths, Min Path Sum, LCS, Edit Distance.
- *Knapsack*: 0/1 (Subset Sum) and Unbounded (Coin Change).

## 9. Backtracking
- Template: `Make choice -> Backtrack(State) -> Undo Choice`.
- *Examples*: Permutations, Combinations, Word Search, N-Queens.

## 10. Bit Manipulation
- `x ^ x = 0`, `x ^ 0 = x`.
- Find missing elements, check powers of 2 ( `n & (n-1) == 0` ).

## 11. Custom Data Structures
- *Trie (Prefix Tree)*: Fast string/prefix lookups.
- *LRU Cache*: HashMap + Doubly Linked List.
