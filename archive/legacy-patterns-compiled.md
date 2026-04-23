# Legacy Patterns Compilation

This file contains a compilation of legacy pattern files for archival purposes.

---

## File: coding-patterns.md

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


---

## File: common-patterns-thita.ai.md

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


---

## File: common-patterns.md

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


---

## File: dp-advanced.md

# Advanced Dynamic Programming Patterns

Dynamic Programming (DP) is optimized recursion. 
- **Identify DP**: Is there a choice at each step? Are we maximizing/minimizing/counting ways? Are there overlapping subproblems?
- **Top-Down (Memoization)**: Recursion + Cache.
- **Bottom-Up (Tabulation)**: Iterative 1D/2D array filling.

## 16 Core DP Patterns

### 1. Fibonacci / Simple Recurrence DP
- **Core Idea**: $dp[n]$ depends on previous states like $dp[n-1]$ and $dp[n-2]$.
- **Click Moment**: "Climbing stairs," "ways to reach," or "no two adjacent" (House Robber). Simple linear dependency.
- **Examples**: Climbing Stairs, Min Cost Climbing Stairs, House Robber, Decode Ways, Domines Tiling.

### 2. 0/1 Knapsack Pattern
- **Core Idea**: You must either pick or skip an item (finite items).
- **Click Moment**: "Set of items," "limited capacity," "exact sum," and **each item used once**.
- **Examples**: Subset Sum, Target Sum, Partition Equal Subset Sum.

### 3. Unbounded Knapsack Pattern
- **Core Idea**: You can pick an item an unlimited number of times.
- **Click Moment**: "Unlimited supply," "minimum coins," or "ways to change" where items can be reused.
- **Examples**: Coin Change (Min coins / Ways), Perfect Squares, Infinite Bricks.

### 4. Longest Increasing Subsequence (LIS)
- **Core Idea**: $dp[i]$ stores the best answer ending at $i$. Optimizable to $O(N \log N)$ with Binary Search.
- **Click Moment**: "Increasing order," "longest chain," or "nested envelopes." Elements don't have to be contiguous.
- **Examples**: Number of LIS, Russian Doll Envelopes, Box Stacking.

### 5. Longest Common Subsequence (LCS)
- **Core Idea**: 2D DP comparing characters of two sequences string A and string B.
- **Click Moment**: "Two strings," "similarity," "edit distance," or "common characters" in order.
- **Examples**: Edit Distance, Shortest Common Supersequence, Wildcard Matching.

### 6. Kadane’s Algorithm Variants
- **Core Idea**: Maximum subarray ending at $i$. $dp[i] = \max(arr[i], arr[i] + dp[i-1])$.
- **Click Moment**: "Maximum sum subarray," "maximum product," or "circular array sum." Contiguous.
- **Examples**: Max Product Subarray, Maximum Circular Subarray Sum, Best Time to Buy and Sell Stock.

### 7. Matrix Chain Multiplication (MCM) / Interval DP
- **Core Idea**: Recursively break intervals into left and right partitions to minimize/maximize cost.
- **Click Moment**: "Burst balloons," "optimal merge," or "partitioning a polygon." Cost depends on the last element chosen in a range.
- **Examples**: Burst Balloons, Palindrome Partitioning, Minimum Score Triangulation.

### 8. DP on Trees
- **Core Idea**: Traverse tree using Post-Order DFS. A parent's state depends on its children's state.
- **Click Moment**: "Maximum path through any node," "node cameras," or "independent set on tree."
- **Examples**: Maximum Path Sum, Diameter of Binary Tree, House Robber III, Binary Tree Cameras.

### 9. DP on DAGs
- **Core Idea**: Find the longest/shortest paths in Directed Acyclic Graphs. Topological order matters.
- **Click Moment**: "Grid with obstacles," "longest path in matrix," or "task dependencies with weights."
- **Examples**: Longest Path in Matrix, Course Schedule with cost.

### 10. Grid 2D DP
- **Core Idea**: Pathfinding heavily restricted to moving Right/Down.
- **Click Moment**: "Minimum path sum," "unique paths," or "largest square/rectangle in matrix."
- **Examples**: Unique Paths, Min Path Sum, Dungeon Game, Maximal Square.

### 11. Bitmask DP
- **Core Idea**: Represent state (visited nodes/assigned jobs) as an integer's bits. Useful for $N \le 20$.
- **Click Moment**: "Assign N tasks to N people," "Traveling Salesman," or "partition into K subsets." Small N.
- **Examples**: Travelling Salesman Problem (TSP), Assign Workers to Jobs, Partition to K Equal Sum Subsets.

### 12. Digit DP
- **Core Idea**: Counting numbers in a range $[L, R]$ satisfying digit criteria.
- **Click Moment**: "Count numbers between X and Y," "sum of digits equals K," or "no repeating digits."
- **Examples**: Numbers $\le N$ with tight bounds, Count numbers with digit sum K.

### 13. Probability / Expected Value DP
- **Core Idea**: Expected value based on multiple random choices.
- **Click Moment**: "Expected number of turns," "probability of staying on board," or "soup servings."
- **Examples**: Knight Probability on Chessboard, Soup Servings.

### 14. Game Theory DP
- **Core Idea**: Min-Max DP where players play optimally.
- **Click Moment**: "Two players," "optimal play," "take stones," or "predict the winner."
- **Examples**: Stone Game I-IV, Predict the Winner.

### 15. Interval Scheduling / Linear DP
- **Core Idea**: Sorted intervals. DP jumps efficiently.
- **Click Moment**: "Weighted job scheduling," "no overlapping jobs," or "maximum profit with cooldown."
- **Examples**: Weighted Job Scheduling, Maximum Profit in Job Scheduling.

### 16. State Machine DP
- **Core Idea**: Transitions between different active states.
- **Click Moment**: "Buy/sell stock with fee," "cooldown period," or "alternating choices."
- **Examples**: Best Time to Buy and Sell Stock with Cooldown/Transaction Fee.


---

## File: leetcode-patterns.md

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
- **[Edit Distance](../google-sde2/PROBLEM_DETAILS.md#edit-distance)**: Minimum insertions/deletions/replacements to convert strings.
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


---

## File: two-pointers-sliding-window.md

# Two Pointers & Sliding Window — Pattern Summary

Quick reference for when to use each pattern. Full content: [Arrays](../foundations/data-structures/array.md), [Strings](../foundations/algorithms/string.md).

---

## Two Pointers

### Opposite ends (sorted array)
- **When**: Pairs, triplets (fix one + two pointers), validity from both ends.
- **Examples**: Two Sum (if sorted), 3Sum, Container With Most Water, Valid Palindrome.
- **Template**: `left=0`, `right=n-1`; move left or right based on comparison; O(N) or O(N²) with fix.

### Same direction (fast & slow)
- **When**: Partition (move zeros), remove duplicates in-place, or "fast/slow" on linked list (see [Linked List](../foundations/data-structures/linked-list.md)).
- **Examples**: Move Zeroes, Remove Duplicates from Sorted Array, Linked List cycle/middle.

---

## Sliding Window

### Variable size
- **When**: "Longest/shortest contiguous subarray/substring" with constraint (sum, at most K distinct, etc.).
- **Template**: Expand `j`, then shrink `i` until valid; update answer. O(N).
- **Examples**: Longest Substring Without Repeating Characters, Minimum Window Substring, Longest Substring with At Most K Distinct Characters.

### Fixed size K
- **When**: "Max/min in every window of size K" or "all subarrays of size K".
- **Examples**: Max in sliding window → monotonic deque; or simple scan per window O(N*K) → O(N) with deque.
- **See**: [Queue](../foundations/data-structures/queue.md) for monotonic deque implementation.

---

## Pattern Recognition

| Clue | Pattern |
|------|--------|
| Sorted array + pair/triplet | Two pointers (opposite ends) |
| Contiguous + "longest/shortest" + condition | Sliding window (variable) |
| "Max/min in each window of size K" | Monotonic deque (or two pointers) |
| In-place partition / move | Two pointers (same direction) |
| "At most K" distinct/sum | Sliding window + map/count |

---

## Quick Revision

- **Two pointers opposite**: left/right; move based on value vs target; never miss in sorted array.
- **Sliding window**: [i,j); add j, then while invalid remove i; candidate = j-i+1.
- **Edge cases**: Empty; K=0; all same; negative numbers (window sum).


---

