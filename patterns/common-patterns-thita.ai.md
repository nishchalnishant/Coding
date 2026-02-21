# Common DSA Patterns

A streamlined checklist of common coding patterns used to categorize and solve DSA problems.

## 1. Two Pointers
Used to process elements from both ends or distinct positions.
- **Converging (Sorted Target Sum)**: E.g., Container With Most Water, 3Sum, Boats to Save People.
- **Fast & Slow (Cycle Detection)**: Floyd's Algorithm. E.g., Linked List Cycle, Find the Duplicate Number.
- **Fixed Separation (Nth from End)**: E.g., Remove Nth Node From End of List.
- **In-place Modification**: E.g., Remove Duplicates, Sort Colors, Move Zeroes.
- **Expanding from Center**: Palindrome substrings.
- **String Reversal**: Reverse strings or vowels in-place.

## 2. Sliding Window
Used for subarray or substring calculations.
- **Fixed Size**: Metrics over $k$-length windows (Moving Average, Max Subarray of Size K).
- **Variable Size**: Expands/contracts based on constraints (Longest Substring Without Repeating Characters, Min Window Substring).
- **Monotonic Queue for Max/Min**: Track extrema in a window (Sliding Window Maximum).
- **Character Frequency Matching**: E.g., Find All Anagrams in a string.

## 3. Tree Traversal (BFS/DFS)
- **BFS (Level Order)**: Process level by level using a Queue (Right Side View, Zigzag Traversal).
- **DFS (Preorder)**: Root -> Left -> Right (Serialize tree, flatten tree).
- **DFS (Inorder)**: Left -> Root -> Right (BST validation, Kth smallest).
- **DFS (Postorder)**: Left -> Right -> Root (Tree height, deleting nodes).
- **Lowest Common Ancestor (LCA)**: Recursively find common descendants.

## 4. Graph Traversal
- **DFS**: Connected components, Path finding, Cycle detection (directed).
- **BFS**: Shortest path in unweighted graphs, Topological sort (Kahn's).
- **Shortest Path**: Dijkstra's (weighted, no negative cycles), Bellman-Ford (negative weights).
- **Advanced**: Minimum Spanning Tree (Kruskal/Prim), Strongly Connected Components (Tarjan's).
- **Union-Find (DSU)**: Efficient component connectivity checking.

## 5. Dynamic Programming (DP)
- **1D Array**: Min cost stairs, House Robber, LIS.
- **2D Array**: LCS, Edit Distance, Unique Paths.
- **Knapsack**: 0/1 (Subset Sum) and Unbounded (Coin Change).

## 6. Greedy
Make locally optimal choices.
- **Interval Merging/Scheduling**: Task scheduling, Merge Intervals.
- **Reachability**: Jump Game.
- **Minimization/Maximization**: Buy/Sell Stock, Gas Station.

## 7. Backtracking
Explore all permutations/combinations.
- **Subsets / Permutations / Combinations**: Generate all possibilities.
- **Grid Search**: Word Search, N-Queens.
- **Parentheses**: Generate Valid Parentheses.

## 8. Stack, Heap & Binary Search
- **Stack**: Valid parentheses, Monotonic Stack (Next greater element), Expression evaluation.
- **Heap (Priority Queue)**: Top K elements, 2 Heaps (Median finding), K-way Merge.
- **Binary Search**: Sorted array search, Min/Max in Rotated Array, Binary search on Answer space.
