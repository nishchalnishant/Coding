# LeetCode Patterns

A condensed guide to standard problem-solving patterns.

## 1. Array & String Manipulation
- **Prefix Sum**: Precompute cumulative sums to answer subarray sum queries in $O(1)$. `P[j] - P[i-1]`.
- **Sliding Window**: Maintain a window of elements to optimize contiguous subarray/substring problems.
- **Two Pointers**: Iterate with two pointers (usually sorted arrays).
  - *Fast & Slow*: Cycle detection (Floyd's algorithm).
- **Overlapping Intervals**: Sort by start time. Merge if `prev_end >= curr_start`.

## 2. Searching & Sorting
- **Modified Binary Search**: Adapt binary search for rotated arrays, or binary search on an answer space.
- **Top K Elements**: Use a Min-Heap of size `K` or QuickSelect.
- **Monotonic Stack**: Keep stack elements sorted to find the "Next Greater/Smaller Element" in $O(N)$.

## 3. Linked Lists
- **In-place Reversal**: Reverse nodes by re-wiring `next` pointers without extra memory.

## 4. Trees & Graphs
- **BFS (Breadth-First Search)**: Level-by-level traversal. Use a Queue. Excellent for shortest path in unweighted graphs.
- **DFS (Depth-First Search)**: Deep exploration. Use Recursion/Stack. Excellent for connected components, backtracking.
- **Tree Traversals**:
  - *PreOrder*: Root -> Left -> Right
  - *InOrder*: Left -> Root -> Right (Yields sorted order in BSTs)
  - *PostOrder*: Left -> Right -> Root

## 5. Dynamic Programming (DP)
- **Fibonacci Sequence**: $O(N)$ 1D DP where $dp[i]$ depends on $dp[i-1], dp[i-2]$.
- **Kadane's Algorithm**: Max contiguous subarray sum. `curr = max(num, curr + num)`.
- **0/1 Knapsack**: Pick or don't pick an item. Maximize value under weight constraints.
- **Unbounded Knapsack**: Items can be picked multiple times (e.g., Coin Change).
- **LCS (Longest Common Subsequence)**: 2D DP comparing strings.
- **LIS (Longest Increasing Subsequence)**: $O(N \log N)$ using binary search + tails array.
- **Palindromic Subsequence**: DP focusing on expanding from center or shrinking from ends.
- **Edit Distance**: Minimum insertions/deletions/replacements to convert strings.
- **Subset Sum**: Determine if a subset sums to target $K$.
- **Matrix Chain Multiplication**: Interval DP. Grouping optimally.
- **Catalan Numbers**: Combinatorial DP (e.g., Unique BSTs, Valid Parentheses).
- **DP on Grids**: Pathfinding with constraints (Unique Paths, Min Path Sum).
- **Tree DP**: Post-order traversal where parent state depends on children (House Robber III).
- **Graph DP**: Often combined with Topological Sort (Cheapest Flights).
- **Digit DP**: State includes `(index, is_tight_bound, sum/condition)`. Used for counting numbers in a range.
- **Bitmask DP**: `mask` represents visited/included states. Used for small $N \le 20$ (TSP, Combinations).
- **Probability DP**: Expected values or chances of outcomes (Soup Servings).
- **State Machine DP**: Multiple states transitioning (Stock Buy/Sell with cooldown/fee).

## 6. Backtracking
- Generate permutations, combinations, or subsets recursively, abandoning branches that fail constraints (Grid paths, N-Queens).
