# Dynamic Programming

An optimization technique used to solve problems by breaking them down into simpler, overlapping subproblems, and storing their solutions (memoization or tabulation) to avoid redundant computation.

## Key Properties
- **Optimal Substructure**: The optimal solution to the main problem can be constructed from optimal solutions to its subproblems.
- **Overlapping Subproblems**: The recursive algorithm solves the same subproblem multiple times.

## Two Approaches

| Feature | Top-Down (Memoization) | Bottom-Up (Tabulation) |
| --- | --- | --- |
| **Logic** | Recursive. Start at the end, compute base cases as needed | Iterative. Start from base cases, build up to the end |
| **Storage** | Hash Map or Array | Array / 2D Matrix (often space-optimized) |
| **Pros** | Intuitive, only computes needed subproblems | Faster (no call stack overhead), easy space optimization |
| **Cons** | Call stack overhead / recursion depth limits | Might compute unnecessary subproblems |

## Classic Problem Categories
1. **1D DP**: Fibonacci, Climbing Stairs, House Robber, Coin Change, Longest Increasing Subsequence (LIS), Maximum Subarray (Kadane's), Decode Ways.
2. **2D DP**: Unique Paths, Minimum Path Sum, Longest Common Subsequence (LCS), Edit Distance, Subset Sum.
3. **0/1 Knapsack**: Target Sum, Partition Equal Subset Sum.
4. **Unbounded Knapsack**: Coin Change, Rod Cutting.
5. **Interval DP**: Palindromic Substrings, Burst Balloons, Matrix Chain Multiplication.

## Interview Tip
1. First, articulate the naive recursive approach. Write the recurrence relation.
2. Build the top-down memoized solution (store states in a cache like a dictionary).
3. (Optional but great): Convert the relation into a bottom-up tabulation approach, noting the $O(N)$ space table.
4. (Best): Notice if the $i$-th element only depends on $(i-1)$ and $(i-2)$, then reduce space complexity to $O(1)$.
