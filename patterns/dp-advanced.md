# Advanced Dynamic Programming Patterns

Dynamic Programming (DP) is optimized recursion. 
- **Identify DP**: Is there a choice at each step? Are we maximizing/minimizing/counting ways? Are there overlapping subproblems?
- **Top-Down (Memoization)**: Recursion + Cache.
- **Bottom-Up (Tabulation)**: Iterative 1D/2D array filling.

## 16 Core DP Patterns

### 1. Fibonacci / Simple Recurrence DP
- **Core Idea**: $dp[n]$ depends on previous states like $dp[n-1]$ and $dp[n-2]$.
- **Examples**: Climbing Stairs, Min Cost Climbing Stairs, House Robber, Decode Ways, Domines Tiling.

### 2. 0/1 Knapsack Pattern
- **Core Idea**: You must either pick or skip an item (finite items).
- **Examples**: Subset Sum, Target Sum, Partition Equal Subset Sum.

### 3. Unbounded Knapsack Pattern
- **Core Idea**: You can pick an item an unlimited number of times.
- **Examples**: Coin Change (Min coins / Ways), Perfect Squares, Infinite Bricks.

### 4. Longest Increasing Subsequence (LIS)
- **Core Idea**: $dp[i]$ stores the best answer ending at $i$. Optimizable to $O(N \log N)$ with Binary Search.
- **Examples**: Number of LIS, Russian Doll Envelopes, Box Stacking.

### 5. Longest Common Subsequence (LCS)
- **Core Idea**: 2D DP comparing characters of two sequences string A and string B.
- **Examples**: Edit Distance, Shortest Common Supersequence, Wildcard Matching.

### 6. Kadane’s Algorithm Variants
- **Core Idea**: Maximum subarray ending at $i$. $dp[i] = \max(arr[i], arr[i] + dp[i-1])$.
- **Examples**: Max Product Subarray, Maximum Circular Subarray Sum, Best Time to Buy and Sell Stock.

### 7. Matrix Chain Multiplication (MCM) / Interval DP
- **Core Idea**: Recursively break intervals into left and right partitions to minimize/maximize cost.
- **Examples**: Burst Balloons, Palindrome Partitioning, Minimum Score Triangulation.

### 8. DP on Trees
- **Core Idea**: Traverse tree using Post-Order DFS. A parent's state depends on its children's state.
- **Examples**: Maximum Path Sum, Diameter of Binary Tree, House Robber III, Binary Tree Cameras.

### 9. DP on DAGs
- **Core Idea**: Find the longest/shortest paths in Directed Acyclic Graphs. Topological order matters.
- **Examples**: Longest Path in Matrix, Course Schedule with cost.

### 10. Grid 2D DP
- **Core Idea**: Pathfinding heavily restricted to moving Right/Down.
- **Examples**: Unique Paths, Min Path Sum, Dungeon Game, Maximal Square.

### 11. Bitmask DP
- **Core Idea**: Represent state (visited nodes/assigned jobs) as an integer's bits. Useful for $N \le 20$.
- **Examples**: Travelling Salesman Problem (TSP), Assign Workers to Jobs, Partition to K Equal Sum Subsets.

### 12. Digit DP
- **Core Idea**: Counting numbers in a range $[L, R]$ satisfying digit criteria.
- **Examples**: Numbers $\le N$ with tight bounds, Count numbers with digit sum K.

### 13. Probability / Expected Value DP
- **Core Idea**: Expected value based on multiple random choices.
- **Examples**: Knight Probability on Chessboard, Soup Servings.

### 14. Game Theory DP
- **Core Idea**: Min-Max DP where players play optimally.
- **Examples**: Stone Game I-IV, Predict the Winner.

### 15. Interval Scheduling / Linear DP
- **Core Idea**: Sorted intervals. DP jumps efficiently.
- **Examples**: Weighted Job Scheduling, Maximum Profit in Job Scheduling.

### 16. State Machine DP
- **Core Idea**: Transitions between different active states.
- **Examples**: Best Time to Buy and Sell Stock with Cooldown/Transaction Fee.
