# DP patterns

Dp is nothing but modification on top of recursion&#x20;

How to solve DP questions&#x20;

* Create recursion solution \[ if choice at each instance then recursion]
* memoize it&#x20;
  * \[ if the problems overlapping then memoize it, or when we have max,min,longest, largest things to find]&#x20;
  * storing the recurive calls
  * Find out the recursive function and get values which are changing all the time and try to store them in an array or 2-d array
  * then in between the base condition and the choice digram we will check if that value is present in the array if not then we will store it in the array
  * ex— for 0-1 knap sack w and  h
* Top-Down

How to solve recursion problem&#x20;

* Choice digram&#x20;
* then find a base condition&#x20;
  * to write the base condition think of the smallest valid input&#x20;
* then make sure for each recursive call the input size is getting reduced&#x20;

Clear, Concise, pattern-wise summary of important Dynamic Programming (DP) patterns along with a short intro and similar problems you can practice under each category.

***

## 1. 0/1 Knapsack Pattern

Used when you must choose items under some constraint (usually weight, time, cost), and each item can be taken at most once.

The DP is usually of the form:

dp\[i]\[w] = best value using first i items and capacity w.

#### Similar Problems

* Subset Sum
* Partition Equal Subset Sum
* Count Subsets with Given Sum
* Minimum Subset Sum Difference
* Target Sum (Leetcode)
* Rod Cutting (bounded version)
* Assignments with constraints where you either take or skip an item

***

## 2. Unbounded Knapsack Pattern

Same as knapsack except you can take an item unlimited times.

Often solved with 1D DP where you iterate capacities first.

#### Similar Problems

* Coin Change (ways)
* Coin Change (min coins)
* Unbounded Rod Cutting
* Minimum Cost for Tickets (if unlimited passes allowed)
* Brick stacking / tiling with infinite tiles

***

## 3. Fibonacci / Simple Recurrence DP

Problems that follow a simple recurrence like:

dp\[n] = dp\[n-1] + dp\[n-2].

Mostly single-dimensional DP with overlapping subproblems.

#### Similar Problems

* Climbing Stairs
* Minimum/Maximum Jumps to Reach End
* Decode Ways (number of ways to decode string)
* House Robber
* Paint Fence
* Tiling Problems (2xn tiling)
* Tribonacci-like problems
* Counting paths with step constraints

***

## 4. LCS (Longest Common Subsequence) Pattern

DP on two strings where you compare characters at i and j.

Usually dp\[i]\[j] means: result for first i chars of A and first j chars of B.

#### Similar Problems

* Longest Common Substring
* Edit Distance
* Longest Palindromic Subsequence
* Shortest Common Supersequence
* Delete Operations for Two Strings
* Distinct Subsequences
* Wildcard Matching
* Regular Expression Matching

***

## 5. LIS (Longest Increasing Subsequence) Pattern

Sequential DP where for each index you look at previous indices.

Optimizable using binary search (O(n log n)).

#### Similar Problems

* Maximum Sum Increasing Subsequence
* Number of LIS
* Russian Doll Envelopes
* Longest Chain of Pairs
* Building Bridges
* Box Stacking
* Longest Bitonic Subsequence

***

## 6. Kadane’s Algorithm (Maximum Subarray)

A greedy + DP optimization to find maximum sum subarray in O(n).

DP relation:

dp\[i] = max(arr\[i], arr\[i] + dp\[i-1]).

#### Similar Problems

* Maximum Circular Subarray Sum
* Maximum Product Subarray
* Longest Subarray With Sum K (sliding window, but related)
* Maximum Absolute Subarray Sum
* Best Time to Buy and Sell Stock (variations use Kadane ideas)
* Maximum Sum Rectangle in 2D Matrix (Kadane inside)

***

## 7. Matrix Chain Multiplication (MCM

DP for partitioning problems where order matters.

Common pattern:

dp\[i]\[j] = min over k (dp\[i]\[k] + dp\[k+1]\[j] + cost).

#### Similar Problems

* Burst Balloons
* Boolean Parenthesization
* Palindrome Partitioning
* Minimum Score Triangulation
* Evaluate to True (expression parsing)
* Optimal BST
* Stick Cutting / Minimum Cost to Cut Stick

***

## 8. DP on Trees

DP where the structure is a tree, solved using DFS post-order traversal.

State is often:

dp\[node] depends on children.

#### Similar Problems

* Diameter of a Tree
* Maximum Path Sum in Binary Tree
* Count Paths / Sum Paths
* Tree DP with states (e.g., “Rob houses in a tree”)
* LCA-based DP problems
* DP on subtree sizes, number of ways, distances
* Binary Tree Cameras
* Distribute Coins in a Binary Tree

***

## 9. DP on Graphs

DP on DAGs or weighted graphs using longest/shortest path DP.

Requires topological ordering to ensure dependencies.

#### Similar Problems

* Longest Path in a DAG
* Shortest Path in DAG (DP-like)
* Number of Paths in a DAG
* DP on bitmasking over graph (e.g., Travelling Salesman Problem)
* Hamiltonian Path / Cycle variations
* Counting walks of length K
* DP with graph transitions (Markov-like)

***

## 10. Other Important DP Patterns

#### a) Bitmask DP

Used when state depends on subsets.

Similar Problems

* Traveling Salesman Problem (TSP)
* DP on subsets
* Maximum Compatibility of Students
* Assignments / matching problems

#### b) Digit DP

Counting numbers with constraints.

Similar Problems

* Count numbers with digit sum
* Count numbers without consecutive digits
* Numbers divisible by X

#### c) Interval DP

Same as MCM but without explicit matrix context.

Similar Problems

* Merge Stones
* Stone Game variations
* DP for choosing segments

#### d) DP on Grids

Classic 2D DP.

Problems

* Unique Paths
* Minimum Path Sum
* Cherry Pickup
* Gold Mine Problem

***

## How to solve DP problems

* Choice at each strep - Recursion
*





***

## 100+ Dynamic Programming Problems — Grouped by Patterns

***

## 1. Fibonacci / Simple Recurrence DP

#### Core idea: dp\[n] depends on dp\[n−1], dp\[n−2], …

1. Fibonacci Numbers
2. Climbing Stairs
3. Min Cost Climbing Stairs
4. House Robber
5. House Robber II
6. Decode Ways
7. Tribonacci Number
8. N-th Stair Problem (taking 1, 2, or 3 steps)
9. Number of Ways to Reach Destination (hop 1 or 2 or 3)
10. Tiling With Dominoes
11. Tiling With 2×1 and 2×2 tiles
12. Painting Fence
13. Count Balanced Parentheses (Catalan DP)
14. Unique BST (Catalan)
15. Number of Binary Trees with N nodes

***

## 2. 0/1 Knapsack Pattern

#### Core idea: pick or skip, finite items.

16. 0/1 Knapsack
17. Subset Sum
18. Partition Equal Subset Sum
19. Minimum Subset Sum Difference
20. Target Sum
21. Count Subsets With Given Sum
22. Rod Cutting (bounded)
23. Assign Tasks With Constraints
24. Students–Exam Assignment (take/not take)
25. Pick Movies/Songs With Time Limit

***

## 3. Unbounded Knapsack Pattern

#### &#x20;Core idea: pick item unlimited times.

26. Coin Change (Number of Ways)
27. Coin Change (Minimum Coins)
28. Unbounded Knapsack
29. Rod Cutting (unbounded)
30. Minimum Cost to Reach N
31. Perfect Squares (Min count)
32. Combination Sum
33. Tiling M×N Wall (infinite bricks)
34. Minimum Cost for Train Tickets
35. Word Break (unbounded dictionary)

***

## 4. Longest Increasing Sequence (LIS) Pattern

#### dp\[i] = best answer ending at i.

36. LIS
37. Number of LIS
38. Maximum Sum Increasing Subsequence
39. Longest Bitonic Subsequence
40. Russian Doll Envelopes
41. Box Stacking Problem
42. Building Bridges
43. Largest Divisible Subset
44. Minimum Deletions to Make Array Sorted
45. Minimum Number of Removals to Make Mountain Array

***

## 5. Longest Common Subsequence (LCS) Pattern

#### Compare characters of two sequences.

46. LCS
47. Longest Common Substring
48. Edit Distance
49. Shortest Common Supersequence
50. Distinct Subsequences
51. Min Insertions to Make String Palindrome
52. Longest Palindromic Subsequence
53. Delete Operation for Two Strings
54. Regular Expression Matching (DP)
55. Wildcard Matching
56. Interleaving Strings
57. Scramble String
58. Minimum Window Subsequence

***

## 6. Kadane’s Algorithm Style DP

#### &#x20;dp\[i] = max(arr\[i], arr\[i] + dp\[i-1]).

59. Maximum Subarray
60. Maximum Circular Subarray Sum
61. Maximum Product Subarray
62. Max Sum of Non-Adjacent Elements (Kadane variant)
63. Best Time to Buy and Sell Stock I
64. Best Time to Buy and Sell Stock II
65. Best Time to Buy and Sell Stock III
66. Best Time to Buy and Sell Stock IV
67. Maximum Subarray After One Deletion
68. Maximum Sum Rectangle in Matrix (Kadane inside)

***

## 7. Matrix Chain Multiplication (MCM) Pattern

#### &#x20;Interval DP — recursively break into left + right partitions.

69. Matrix Chain Multiplication
70. Palindrome Partitioning (min cuts)
71. Minimum Palindromic Partitioning II
72. Burst Balloons
73. Boolean Parenthesization
74. Evaluate Expression for True
75. Minimum Score Triangulation of Polygon
76. Stick Cutting / Minimum Cost to Cut a Stick
77. Optimal BST
78. Scrambled String Verification

***

## 8. DP on Trees

#### &#x20;Use DFS and compute dp from children.

79. Maximum Path Sum in Binary Tree
80. Diameter of Binary Tree
81. Sum of Root-to-Leaf Paths
82. House Robber on Trees
83. Count BSTs in a subtree
84. DP on Tree: Subtree Size
85. DP on Tree: Height, Depth, Parent
86. Distribute Coins in Binary Tree
87. Binary Tree Cameras
88. Maximum Independent Set in Tree
89. Minimum Vertex Cover (trees)

***

## 9. DP on Graphs (DAG DP + Paths)

#### Topological order DP.

90. Longest Path in a DAG
91. Shortest Path in a DAG
92. Number of Paths in Grid With Obstacles
93. Counting Paths in Directed Acyclic Graph
94. Hamiltonian Path with Bitmask DP
95. Traveling Salesman Problem (TSP)
96. DP for Weighted DAG path counting
97. Word Ladder II (DP on graph levels)
98. Frog Jump
99. Cherry Pickup (graph-like transitions)
100. Minimum Cost to Travel Between Cities (DAG DP variant)

***

## 10. Grid DP (2D DP)

100. Unique Paths
101. Unique Paths II
102. Minimum Path Sum
103. Dungeon Game
104. Gold Mine Problem
105. Cherry Pickup
106. Maximal Square
107. Largest Rectangle of 1s
108. Minimum Falling Path Sum
109. Increasing Paths in Grid

***

## 11. Bitmask DP

#### ✔ State represented by subsets.

110. Traveling Salesman Problem
111. Minimum Incompatibility
112. Assign Workers to Jobs
113. Maximum Compatibility of Students
114. Partition to K Equal Sum Subsets
115. Sudoku Solvers using bitmask DP
116. Count Ways to Visit All Nodes (state compression DP)

***

## 12. Digit DP

#### ✔ Count numbers with certain digit patterns.

117. Count numbers ≤ N with digit sum K
118. Count numbers with no consecutive digits
119. Count numbers divisible by X
120. Count numbers with limited set of digits
121. Count stepping numbers

***

## 13. Probability DP

#### ✔ DP on outcomes of events.

122. Dice Throw (ways to get sum)
123. Probability of Winning a Game
124. Knight Probability on Chessboard
125. New 21 Game
126. Number of Ways to Reach Target Score

***

## 14. Game Theory DP

#### ✔ Min-max DP.

127. Stone Game
128. Stone Game II
129. Stone Game III
130. Predict the Winner
131. Removing Stones (Nim-like DP)
132. Coins in a Line

***

## 15. Interval Scheduling / Segmented DP

#### ✔ DP on intervals sorted by start time.

133. Weighted Job Scheduling
134. Maximum Profit in Job Scheduling
135. Video Stitching
136. Taxi Earnings (Leetcode)
137. Interval DP for merging intervals

***

## 16. Advanced Patterns

#### (Rare but very powerful)

138. DP + Greedy hybrid (e.g., scheduling + DP)
139. DP + Prefix Sum optimisation
140. DP + Monotonic Queue Optimisation
141. DP + Binary Lifting (tree DP optimisation)
142. DP + Convex Hull Trick
143. DP + Divide and Conquer Optimisation

***

## Batch 1 — Full solutions (20 problems covering main DP patterns)

> Each solution includes: short statement, DP idea (state + recurrence), Python implementation, complexity, and a tiny test.

***

### 1) Fibonacci Numbers

Problem: Compute F(n) (0-indexed: F(0)=0, F(1)=1).

DP idea: simple recurrence F(n)=F(n-1)+F(n-2). Use iterative O(1) space.

```python
def fib(n: int) -> int:
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

# test
print(fib(10))  # 55
```

Time: O(n), Space: O(1).

***

### 2) Climbing Stairs

Problem: Number ways to reach n-th stair taking 1 or 2 steps.

DP idea: dp\[i] = dp\[i-1] + dp\[i-2].

```python
# Python program to count number of ways to reach
# nth stair using recursion

def countWays(n):

    # Base cases: If there are 0 or 1 stairs,
    # there is only one way to reach the top.
    if n == 0 or n == 1:
        return 1

    return countWays(n - 1) + countWays(n - 2)

n = 4
print(countWays(n))
```

Time: O(n), Space: O(1).

***

### 3) Min Cost Climbing Stairs

Problem: Given cost\[i], min cost to reach top (can start at 0 or 1).

DP idea: dp\[i] = cost\[i] + min(dp\[i-1], dp\[i-2]). Answer = min(dp\[n-1], dp\[n-2]) (or optimized).

```python
from typing import List

def min_cost_climbing_stairs(cost: List[int]) -> int:
    n = len(cost)
    if n <= 1: return 0
    dp0, dp1 = cost[0], cost[1]
    for i in range(2, n):
        dp0, dp1 = dp1, cost[i] + min(dp0, dp1)
    return min(dp0, dp1)

print(min_cost_climbing_stairs([10,15,20]))  # 15
```

Time: O(n), Space: O(1).

***

### 4) House Robber

Problem: Max sum of non-adjacent elements.

DP idea: dp\[i] = max(dp\[i-1], dp\[i-2] + nums\[i]).

```python
from typing import List

def house_robber(nums: List[int]) -> int:
    prev, cur = 0, 0
    for x in nums:
        prev, cur = cur, max(cur, prev + x)
    return cur

print(house_robber([2,7,9,3,1]))  # 12
```

Time: O(n), Space: O(1).

***

### 5) Decode Ways

Problem: Count ways to decode digits -> letters (1->A … 26->Z).

DP idea: dp\[i] = dp\[i-1] if single valid + dp\[i-2] if two-digit valid.

```python
def num_decodings(s: str) -> int:
    if not s or s[0] == '0': return 0
    n = len(s)
    dp0, dp1 = 1, 1  # dp[-1]=1, dp[0]=1
    for i in range(1, n):
        cur = 0
        if s[i] != '0':
            cur += dp1
        two = int(s[i-1:i+1])
        if 10 <= two <= 26:
            cur += dp0
        dp0, dp1 = dp1, cur
    return dp1

print(num_decodings("226"))  # 3
```

Time: O(n), Space: O(1).

***

### 6) 0/1 Knapsack (classic)

Problem: Given weights w\[i] and values v\[i], capacity W, maximize value picking each item at most once.

DP idea: dp\[w] = max(dp\[w], dp\[w-wi] + vi) iterating items then capacity (reverse capacity to avoid reuse).

```python
from typing import List

def knapsack_01(weights: List[int], values: List[int], W: int) -> int:
    dp = [0] * (W+1)
    n = len(weights)
    for i in range(n):
        wi, vi = weights[i], values[i]
        for cap in range(W, wi-1, -1):
            dp[cap] = max(dp[cap], dp[cap-wi] + vi)
    return dp[W]

print(knapsack_01([1,3,4], [15,20,30], 4))  # 35 (items 0 and 2)
```

Time: O(nW), Space: O(W).

***

### 7) Subset Sum (decision)

Problem: Given nums and target sum S, is subset sum S possible?

DP idea: 1D boolean dp: dp\[s] |= dp\[s - num].

```python
def subset_sum(nums, S):
    dp = [False] * (S+1)
    dp[0] = True
    for num in nums:
        for s in range(S, num-1, -1):
            dp[s] = dp[s] or dp[s-num]
    return dp[S]

print(subset_sum([3,34,4,12,5,2], 9))  # True
```

Time: O(nS), Space: O(S).

***

### 8) Coin Change — Minimum Coins (Unbounded Knapsack)

Problem: Given coins, min # coins to make amount.

DP idea: dp\[a] = min(dp\[a], dp\[a-coin] + 1).

```python
from math import inf

def coin_change_min(coins, amount):
    dp = [inf] * (amount+1)
    dp[0] = 0
    for a in range(1, amount+1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a-c] + 1)
    return dp[amount] if dp[amount] != inf else -1

print(coin_change_min([1,2,5], 11))  # 3 (5+5+1)
```

Time: O(amount \* len(coins)). Space: O(amount).

***

### 9) Coin Change — Number of Ways (combinations)

Problem: Count ways to make amount (order doesn’t matter).

DP idea: iterate coins outer, amount inner (unbounded).

```python
def coin_change_ways(coins, amount):
    dp = [0] * (amount+1)
    dp[0] = 1
    for c in coins:
        for a in range(c, amount+1):
            dp[a] += dp[a-c]
    return dp[amount]

print(coin_change_ways([1,2,5], 5))  # 4
```

Time/Space: O(amount \* len(coins)), O(amount).

***

### 10) Longest Increasing Subsequence (LIS) — O(n log n)

Problem: Length of LIS in array.

DP idea: patience sorting tails + binary search.

```python
import bisect
def lis_length(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)

print(lis_length([10,9,2,5,3,7,101,18]))  # 4 (2,3,7,101)
```

Time: O(n log n), Space: O(n).

***

### 11) Longest Common Subsequence (LCS)

Problem: LCS length of strings A,B.

DP idea: 2D dp dp\[i]\[j] = dp\[i-1]\[j-1]+1 if A\[i-1]==B\[j-1] else max(dp\[i-1]\[j], dp\[i]\[j-1]). Use rolling array for space.

```python
def lcs(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [0]*(n+1)
    for i in range(1, m+1):
        prev = 0
        for j in range(1, n+1):
            temp = dp[j]
            if a[i-1] == b[j-1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev = temp
    return dp[n]

print(lcs("abcde", "ace"))  # 3
```

Time: O(mn), Space: O(n).

***

### 12) Maximum Subarray (Kadane)

Problem: Max contiguous subarray sum.

DP idea: cur = max(a\[i], cur + a\[i]).

```python
def max_subarray(nums):
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

print(max_subarray([-2,1,-3,4,-1,2,1,-5,4]))  # 6 (4,-1,2,1)
```

Time: O(n), Space: O(1).

***

### 13) Matrix Chain Multiplication (MCM)

Problem: Min cost to compute product of matrices with dimensions p0 x p1, p1 x p2,....

DP idea: interval DP dp\[i]\[j] = min(dp\[i]\[k] + dp\[k+1]\[j] + p\[i-1]\*p\[k]\*p\[j]).

```python
from functools import lru_cache

def matrix_chain(p):
    n = len(p)-1
    dp = [[0]* (n+1) for _ in range(n+1)]
    for L in range(2, n+1):  # length
        for i in range(1, n-L+2):
            j = i + L - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
    return dp[1][n]

print(matrix_chain([40,20,30,10,30]))  # 26000
```

Time: O(n^3), Space: O(n^2).

***

### 14) Palindrome Partitioning II (min cuts)

Problem: Min cuts to partition string into palindromic substrings.

DP idea: Precompute is\_pal\[i]\[j]. cuts\[i] = min cuts for s\[:i+1].

```python
def min_cut_palindrome(s: str) -> int:
    n = len(s)
    is_pal = [[False]*n for _ in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(i, n):
            is_pal[i][j] = (s[i]==s[j]) and (j-i<2 or is_pal[i+1][j-1])
    cuts = [float('inf')] * n
    for i in range(n):
        if is_pal[0][i]:
            cuts[i] = 0
        else:
            for j in range(1, i+1):
                if is_pal[j][i]:
                    cuts[i] = min(cuts[i], cuts[j-1] + 1)
    return cuts[-1] if n else 0

print(min_cut_palindrome("aab"))  # 1 ("aa"|"b")
```

Time: O(n^2), Space: O(n^2).

***

### 15) House Robber on Tree

Problem: Max sum of nodes with no two adjacent (tree).

DP idea: DFS returns tuple (rob, not\_rob) for each node.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def rob_tree(root: TreeNode):
    def dfs(node):
        if not node:
            return (0, 0)  # rob, not_rob
        l = dfs(node.left)
        r = dfs(node.right)
        rob = node.val + l[1] + r[1]
        not_rob = max(l) + max(r)
        return (rob, not_rob)
    return max(dfs(root))

# example: tree [3,2,3,null,3,null,1]
root = TreeNode(3, TreeNode(2, None, TreeNode(3)), TreeNode(3, None, TreeNode(1)))
print(rob_tree(root))  # 7
```

Time: O(n), Space: O(h) recursion.

***

### 16) Longest Path in DAG

Problem: Longest path length in a DAG (weighted or unweighted).

DP idea: Topological sort then dp\[v] = max(dp\[u] + w(u->v)) over incoming edges.

```python
from collections import defaultdict, deque

def longest_path_dag(n, edges, start):
    # edges: list of (u,v,w)
    g = defaultdict(list)
    indeg = [0]*n
    for u,v,w in edges:
        g[u].append((v,w)); indeg[v]+=1
    topo = []
    dq = deque([i for i in range(n) if indeg[i]==0])
    while dq:
        u = dq.popleft()
        topo.append(u)
        for v,_ in g[u]:
            indeg[v]-=1
            if indeg[v]==0: dq.append(v)
    dist = [-10**18]*n
    dist[start] = 0
    for u in topo:
        if dist[u] > -10**17:
            for v,w in g[u]:
                dist[v] = max(dist[v], dist[u] + w)
    return dist

# sample DAG
print(longest_path_dag(5, [(0,1,3),(0,2,2),(1,3,4),(2,3,1),(3,4,2)], 0))
```

Time: O(V+E), Space: O(V).

***

### 17) Traveling Salesman Problem (TSP) — Bitmask DP

Problem: Shortest Hamiltonian cycle visiting all nodes (small n).

DP idea: dp\[mask]\[i] = min cost to reach i with visited mask. Transition: dp\[mask|1<\<j]\[j] = min(dp\[mask]\[i] + cost\[i]\[j]).

```python
from math import inf

def tsp(dist):
    n = len(dist)
    N = 1<<n
    dp = [[inf]*n for _ in range(N)]
    dp[1][0] = 0  # start at 0
    for mask in range(1, N):
        for u in range(n):
            if not (mask & (1<<u)): continue
            for v in range(n):
                if mask & (1<<v): continue
                dp[mask | (1<<v)][v] = min(dp[mask | (1<<v)][v], dp[mask][u] + dist[u][v])
    ans = inf
    for u in range(1, n):
        ans = min(ans, dp[N-1][u] + dist[u][0])
    return ans

# small example
dist = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
print(tsp(dist))  # 80
```

Time: O(n^2 \* 2^n), Space: O(n \* 2^n).

***

### 18) Unique Paths (Grid DP)

Problem: Number of ways from top-left to bottom-right moving only down/right.

DP idea: dp\[i]\[j] = dp\[i-1]\[j] + dp\[i]\[j-1].

```python
def unique_paths(m, n):
    dp = [1]*n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[-1]

print(unique_paths(3,7))  # 28
```

Time: O(mn), Space: O(n).

***

### 19) Weighted Job Scheduling (Interval DP)

Problem: Given jobs (start, end, profit), schedule non-overlapping jobs maximizing profit.

DP idea: Sort by end, dp\[i] = max(dp\[i-1], profit\[i] + dp\[p]) where p is last job ending before i (binary search).

```python
from bisect import bisect_right

def weighted_job_scheduling(jobs):
    # jobs: list of (start, end, profit)
    jobs.sort(key=lambda x: x[1])
    starts = [s for s, e, p in jobs]
    ends = [e for s, e, p in jobs]
    dp = [0]*len(jobs)
    for i, (s,e,p) in enumerate(jobs):
        incl = p
        # find rightmost job that ends <= s
        j = bisect_right(ends, s) - 1
        if j != -1:
            incl += dp[j]
        dp[i] = max(dp[i-1] if i>0 else 0, incl)
    return dp[-1]

print(weighted_job_scheduling([(1,3,50),(3,5,20),(6,19,100),(2,100,200)]))  # 250
```

Time: O(n log n), Space: O(n).

***

### 20) Digit DP — count numbers ≤ N with digit sum = S

Problem: Count non-negative integers ≤ N whose digits sum to S.

DP idea: classic digit DP: dp\[pos]\[tight]\[sum]. I’ll implement memoized DFS.

```python
from functools import lru_cache

def count_with_digit_sum(N: int, S: int) -> int:
    s = str(N)
    @lru_cache(None)
    def dfs(pos, tight, rem):
        if pos == len(s):
            return 1 if rem == 0 else 0
        if rem < 0:
            return 0
        limit = int(s[pos]) if tight else 9
        ans = 0
        for d in range(0, limit+1):
            ans += dfs(pos+1, tight and (d==limit), rem-d)
        return ans
    return dfs(0, True, S)

print(count_with_digit_sum(100, 1))  # counts numbers <=100 with digit sum 1
```

Time: O(len(N) \* 10 \* S) roughly with memoization. Space: memo size.

***

## 21) Number of Longest Increasing Subsequences (count of LIS)

Problem: Count how many increasing subsequences achieve the LIS length.

DP idea: For each index i, track length\[i] = length of LIS ending at i and count\[i] = number of LIS ending at i. Update by scanning previous j < i.

```python
from typing import List

def count_LIS(nums: List[int]) -> int:
    n = len(nums)
    if n == 0: return 0
    length = [1]*n
    count = [1]*n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]
    max_len = max(length)
    return sum(c for l,c in zip(length,count) if l==max_len)

print(count_LIS([1,3,5,4,7]))  # 2
```

Time: O(n²), Space: O(n).

***

## 22) Maximum Sum Increasing Subsequence (MSIS)

Problem: Find max-sum increasing subsequence.

DP idea: dp\[i] = nums\[i] + max(dp\[j]) for j\<i and nums\[j] < nums\[i].

```python
def max_sum_increasing_subsequence(nums):
    n = len(nums)
    if n==0: return 0
    dp = nums[:]  # dp[i] best sum ending at i
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + nums[i])
    return max(dp)

print(max_sum_increasing_subsequence([1,101,2,3,100,4,5]))  # 106 (1+2+3+100)
```

Time: O(n²), Space: O(n).

***

## 23) Longest Bitonic Subsequence

Problem: Longest sequence which increases then decreases.

DP idea: Compute LIS ending at i and LIS from right (LDS) starting at i, combine.

```python
def longest_bitonic(nums):
    n = len(nums)
    if n==0: return 0
    lis = [1]*n
    lds = [1]*n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                lis[i] = max(lis[i], lis[j]+1)
    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            if nums[j] < nums[i]:
                lds[i] = max(lds[i], lds[j]+1)
    return max(lis[i] + lds[i] - 1 for i in range(n))

print(longest_bitonic([1,11,2,10,4,5,2,1]))  # 6
```

Time: O(n²), Space: O(n).

***

## 24) Russian Doll Envelopes (LIS on pairs)

Problem: Max number of envelopes you can nest (w,h) — both strictly increasing.

DP idea: Sort by width asc and height desc for equal widths, then LIS on heights.

```python
import bisect
from typing import List

def max_envelopes(env: List[List[int]]) -> int:
    env.sort(key=lambda x: (x[0], -x[1]))
    tails = []
    for _, h in env:
        i = bisect.bisect_left(tails, h)
        if i == len(tails):
            tails.append(h)
        else:
            tails[i] = h
    return len(tails)

print(max_envelopes([[5,4],[6,4],[6,7],[2,3]]))  # 3
```

Time: O(n log n), Space: O(n).

***

## 25) Longest Common Substring

Problem: Longest contiguous substring appearing in both strings.

DP idea: dp\[i]\[j] = dp\[i-1]\[j-1]+1 if chars equal, else 0. Use rolling arrays.

```python
def longest_common_substring(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [0]*(n+1)
    best = 0
    for i in range(1, m+1):
        prev = 0
        for j in range(1, n+1):
            temp = dp[j]
            if a[i-1] == b[j-1]:
                dp[j] = prev + 1
                best = max(best, dp[j])
            else:
                dp[j] = 0
            prev = temp
    return best

print(longest_common_substring("abcdxyz","xyzabcd"))  # 4 ("abcd")
```

Time: O(mn), Space: O(n).

***

## 26) Edit Distance (Levenshtein)

Problem: Minimum operations (insert/delete/replace) to convert a -> b.

DP idea: dp\[i]\[j] = min(dp\[i-1]\[j]+1, dp\[i]\[j-1]+1, dp\[i-1]\[j-1] + cost).

```python
def edit_distance(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = list(range(n+1))
    for i in range(1, m+1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n+1):
            temp = dp[j]
            if a[i-1] == b[j-1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j-1])  # replace, delete, insert
            prev = temp
    return dp[n]

print(edit_distance("intention","execution"))  # 5
```

Time: O(mn), Space: O(n).

***

## 27) Shortest Common Supersequence (SCS) length

Problem: Shortest string that has both a and b as subsequences.

DP idea: len(SCS) = m + n - LCS(a,b).

```python
def scs_length(a: str, b: str) -> int:
    # use LCS
    m, n = len(a), len(b)
    dp = [0]*(n+1)
    for i in range(1,m+1):
        prev = 0
        for j in range(1,n+1):
            temp = dp[j]
            if a[i-1] == b[j-1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev = temp
    lcs = dp[n]
    return m + n - lcs

print(scs_length("aggtab","gxtxayb"))  # 9
```

Time: O(mn), Space: O(n).

***

## 28) Distinct Subsequences

Problem: Count ways s can form t as subsequence.

DP idea: dp\[i]\[j] ways using s\[:i] to form t\[:j]. Optimize to 1D backwards.

```python
def num_distinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    dp = [0]*(n+1)
    dp[0] = 1
    for i in range(1, m+1):
        for j in range(n, 0, -1):
            if s[i-1] == t[j-1]:
                dp[j] += dp[j-1]
    return dp[n]

print(num_distinct("rabbbit","rabbit"))  # 3
```

Time: O(mn), Space: O(n).

***

## 29) Maximum Product Subarray

Problem: Max product of contiguous subarray (negatives flip sign).

DP idea: Track both max\_ending\_here and min\_ending\_here.

```python
def max_product(nums):
    max_here = min_here = ans = nums[0]
    for x in nums[1:]:
        candidates = (x, max_here * x, min_here * x)
        max_here = max(candidates)
        min_here = min(candidates)
        ans = max(ans, max_here)
    return ans

print(max_product([2,3,-2,4]))  # 6
```

Time: O(n), Space: O(1).

***

## 30) Maximum Sum Rectangle in 2D Matrix

Problem: Max sum submatrix in 2D array.

DP idea: Fix top and bottom rows, collapse to 1D by summing columns, run Kadane.

```python
def max_sum_rectangle(mat):
    if not mat or not mat[0]: return 0
    n, m = len(mat), len(mat[0])
    max_sum = float('-inf')
    for top in range(n):
        col_sum = [0]*m
        for bottom in range(top, n):
            for c in range(m):
                col_sum[c] += mat[bottom][c]
            # Kadane on col_sum
            cur = col_sum[0]
            best = col_sum[0]
            for x in col_sum[1:]:
                cur = max(x, cur + x)
                best = max(best, cur)
            max_sum = max(max_sum, best)
    return max_sum

print(max_sum_rectangle([[1,2,-1],[-3,4,5],[2,-1,3]]))  # 12 (submatrix)
```

Time: O(n² \* m), Space: O(m).

***

## 31) Burst Balloons (MCM-like)

Problem: Max coins by bursting balloons; bursting order matters.

DP idea: Interval DP with dp\[i]\[j] max coins bursting between i and j.

```python
def max_coins(nums):
    A = [1] + nums + [1]
    n = len(A)
    dp = [[0]*n for _ in range(n)]
    for length in range(2, n):
        for i in range(0, n-length):
            j = i + length
            for k in range(i+1, j):
                dp[i][j] = max(dp[i][j], dp[i][k] + A[i]*A[k]*A[j] + dp[k][j])
    return dp[0][n-1]

print(max_coins([3,1,5,8]))  # 167
```

Time: O(n³), Space: O(n²).

***

## 32) Boolean Parenthesization (count ways to get True)

Problem: Count ways to parenthesize boolean expression to true.

DP idea: Interval DP tracking counts of true/false for each substring.

```python
def count_bool_parenthesization(s: str, ops: str) -> int:
    # s: operands string like "TFT", ops: operators "^|&"
    n = len(s)
    T = [[0]*n for _ in range(n)]
    F = [[0]*n for _ in range(n)]
    for i in range(n):
        T[i][i] = 1 if s[i]=='T' else 0
        F[i][i] = 1 if s[i]=='F' else 0
    for L in range(2, n+1):
        for i in range(n-L+1):
            j = i+L-1
            for k in range(i, j):
                op = ops[k]
                lt, lf = T[i][k], F[i][k]
                rt, rf = T[k+1][j], F[k+1][j]
                if op == '&':
                    T[i][j] += lt * rt
                    F[i][j] += lt*rf + lf*rt + lf*rf
                elif op == '|':
                    T[i][j] += lt*rt + lt*rf + lf*rt
                    F[i][j] += lf*rf
                else:  # ^
                    T[i][j] += lt*rf + lf*rt
                    F[i][j] += lt*rt + lf*rf
    return T[0][n-1]

# example: (T|F)&T -> operands "TFT", ops "|&"
print(count_bool_parenthesization("TFT","|&"))  # 2
```

Time: O(n³), Space: O(n²).

***

## 33) Scramble String (interval DP with memo)

Problem: Check if s2 is scramble of s1 (recursive partitioning).

DP idea: Try splits and both swapped/unswapped partitions; memoize.

```python
from functools import lru_cache

def is_scramble(s1: str, s2: str) -> bool:
    @lru_cache(None)
    def dfs(a,b):
        if a == b: return True
        if sorted(a) != sorted(b): return False
        n = len(a)
        for i in range(1, n):
            if dfs(a[:i], b[:i]) and dfs(a[i:], b[i:]):
                return True
            if dfs(a[:i], b[-i:]) and dfs(a[i:], b[:-i]):
                return True
        return False
    return dfs(s1, s2)

print(is_scramble("great","rgeat"))  # True
```

Time: Exponential worst-case but memoized; pruning by char-check reduces branching.

***

## 34) Minimum Falling Path Sum (grid)

Problem: From top row to bottom choose a path (down-left/down/down-right) minimize sum.

DP idea: row-by-row DP.

```python
def min_falling_path_sum(mat):
    n = len(mat)
    dp = mat[0][:]
    for i in range(1, n):
        ndp = [10**18]*n
        for j in range(n):
            for nj in (j-1, j, j+1):
                if 0 <= nj < n:
                    ndp[nj] = min(ndp[nj], dp[j] + mat[i][nj])
        dp = ndp
    return min(dp)

print(min_falling_path_sum([[2,1,3],[6,5,4],[7,8,9]]))  # 13
```

Time: O(n²), Space: O(n).

***

## 35) Cherry Pickup (two-person DP on grid)

Problem: Two people start at (0,0) and move to bottom-right and back, collecting cherries (can’t double collect).

DP idea: Transform to two people moving from start to end simultaneously; state by total steps t and positions r1,r2 (or columns), memoize.

```python
from functools import lru_cache

def cherry_pickup(grid):
    n = len(grid)
    @lru_cache(None)
    def dp(t, x1, x2):
        y1 = t - x1
        y2 = t - x2
        if x1>=n or y1>=n or x2>=n or y2>=n: return -10**9
        val = grid[x1][y1]
        if x1 != x2:
            val += grid[x2][y2]
        if t == 2*(n-1):
            return val
        best = -10**9
        for nx1 in (x1, x1+1):
            for nx2 in (x2, x2+1):
                best = max(best, dp(t+1, nx1, nx2))
        return val + best
    res = dp(0,0,0)
    return max(0, res)

print(cherry_pickup([[0,1,-1],[1,0,-1],[1,1,1]]))  # 5
```

Time: O(n³), Space: O(n³) memo.

***

## 36) Count Paths in DAG

Problem: Count number of paths from s to t in a DAG (mod large).

DP idea: Topological order and dp\[v] = sum dp\[u] over predecessors.

```python
from collections import defaultdict, deque

def count_paths_dag(n, edges, s, t):
    g = defaultdict(list)
    indeg = [0]*n
    for u,v in edges:
        g[u].append(v); indeg[v]+=1
    topo = []
    dq = deque([i for i in range(n) if indeg[i]==0])
    while dq:
        u = dq.popleft()
        topo.append(u)
        for v in g[u]:
            indeg[v]-=1
            if indeg[v]==0: dq.append(v)
    dp = [0]*n
    dp[s]=1
    for u in topo:
        for v in g[u]:
            dp[v]+=dp[u]
    return dp[t]

print(count_paths_dag(4, [(0,1),(0,2),(1,2),(1,3),(2,3)], 0, 3))  # 3
```

Time: O(V+E), Space: O(V).

***

## 37) Partition Equal Subset Sum

Problem: Can array be partitioned into two equal-sum subsets?

DP idea: Subset sum to total//2 using 1D boolean dp.

```python
def can_partition(nums):
    total = sum(nums)
    if total % 2: return False
    target = total//2
    dp = [False]*(target+1)
    dp[0] = True
    for num in nums:
        for s in range(target, num-1, -1):
            dp[s] |= dp[s-num]
    return dp[target]

print(can_partition([1,5,11,5]))  # True
```

Time: O(n \* target), Space: O(target).

***

## 38) Partition to K Equal Sum Subsets (bitmask DP)

Problem: Partition nums into k subsets each with equal sum.

DP idea: Bitmask DP tracking current remainder sum; dp\[mask] true if mask can form some number of full groups.

```python
from functools import lru_cache

def can_partition_k_subsets(nums, k):
    total = sum(nums)
    if total % k: return False
    target = total // k
    n = len(nums)
    @lru_cache(None)
    def dfs(mask, cur):
        if mask == (1<<n)-1:
            return cur==0
        for i in range(n):
            if not (mask >> i) & 1 and cur + nums[i] <= target:
                if dfs(mask | (1<<i), (cur+nums[i])%target):
                    return True
        return False
    return dfs(0,0)

print(can_partition_k_subsets([4,3,2,3,5,2,1], 4))  # True
```

Time: O(n \* 2^n) worst, Space: O(2^n).

***

## 39) New 21 Game (Probability DP)

Problem: Alice draws numbers 1..W until sum >= K. Probability sum <= N.

DP idea: dp\[x] probability of reaching x; sliding window sum optimization.

```python
def new21game(N, K, W):
    if K == 0: return 1.0
    dp = [0.0] * (K+W)
    dp[0] = 1.0
    window = 1.0
    res = 0.0
    for i in range(1, K+W):
        dp[i] = window / W
        if i < K:
            window += dp[i]
        else:
            res += dp[i]
        if i - W >= 0:
            window -= dp[i-W]
    return res if N >= K else sum(dp[K:min(N+1, K+W)])

print(new21game(21,17,10))  # sample probability
```

Time: O(K+W), Space: O(K+W).

***

## 40) Stone Game (simple game-theory DP)

Problem: Two players pick from ends of array; both play optimally. Decide winner or best score difference.

DP idea: dp\[i]\[j] = max(nums\[i]-dp\[i+1]\[j], nums\[j]-dp\[i]\[j-1]) (score difference).

```python
def stone_game(nums):
    n = len(nums)
    dp = [[0]*n for _ in range(n)]
    for i in range(n):
        dp[i][i] = nums[i]
    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i+length-1
            dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])
    return dp[0][n-1] > 0  # True if player1 wins

print(stone_game([5,3,4,5]))  # True
```

Time: O(n²), Space: O(n²).

***

***

## 38) Partition to K Equal Sum Subsets (bitmask DP)

Problem: Can we split nums into k subsets, each summing to the same value?

DP idea:

* Total sum must be divisible by k.
* Sort descending (pruning).
*   Use bitmask DP + memo:

    dfs(mask, curr\_sum) tells if remaining elements in mask can complete valid buckets.
* When curr\_sum == target, restart a new bucket with curr\_sum = 0.

<br>

#### Solution

```python
from functools import lru_cache

def can_partition_k_subsets(nums, k):
    total = sum(nums)
    if total % k != 0:
        return False
    target = total // k

    nums.sort(reverse=True)
    n = len(nums)

    @lru_cache(None)
    def dfs(mask, curr_sum):
        if mask == 0:
            return True          # all used successfully

        if curr_sum == target:
            return dfs(mask, 0)  # start a new bucket

        for i in range(n):
            if (mask >> i) & 1 and curr_sum + nums[i] <= target:
                if dfs(mask ^ (1 << i), curr_sum + nums[i]):
                    return True
        return False

    return dfs((1 << n) - 1, 0)

print(can_partition_k_subsets([4,3,2,3,5,2,1], 4))  # True
```

Time: \~O(n \* 2ⁿ)

Space: O(2ⁿ)

***

## 39) Word Break (can segment string)

DP idea:

dp\[i] = True if s\[:i] can be segmented.

Check dictionary words.

```python
def word_break(s, wordDict):
    n = len(s)
    wordSet = set(wordDict)
    dp = [False]*(n+1)
    dp[0] = True
    for i in range(1, n+1):
        for j in range(i):
            if dp[j] and s[j:i] in wordSet:
                dp[i] = True
                break
    return dp[n]

print(word_break("leetcode", ["leet","code"]))  # True
```

***

## 40) Word Break II (print all segmentations)

DP idea: DFS + memo: build sentences from end.

```python
from functools import lru_cache

def word_break_ii(s, wordDict):
    wordSet = set(wordDict)
    n = len(s)

    @lru_cache(None)
    def dfs(i):
        if i == n:
            return [""]  # one valid way
        ans = []
        for j in range(i+1, n+1):
            w = s[i:j]
            if w in wordSet:
                for rest in dfs(j):
                    ans.append(w + (" " + rest if rest else ""))
        return ans

    return dfs(0)

print(word_break_ii("catsanddog", ["cat","cats","and","sand","dog"]))
```

***

## 41) Decode Ways (ways to decode digit string)

DP idea:

dp\[i] = dp\[i-1] (single digit if valid) + dp\[i-2] (two digits if valid).

```python
def num_decodings(s):
    if not s or s[0] == '0': return 0
    n = len(s)
    dp1, dp2 = 1, 1  # dp[i-1], dp[i-2]

    for i in range(1, n):
        cur = 0
        if s[i] != '0':
            cur += dp1
        if 10 <= int(s[i-1:i+1]) <= 26:
            cur += dp2
        dp1, dp2 = cur, dp1

    return dp1

print(num_decodings("226"))  # 3
```

***

## 42) Decode Ways II (with ‘\*’)

\* can mean 1–9. Hard DP but standard.

```python
def num_decodings_ii(s):
    MOD = 10**9+7
    n = len(s)
    dp1, dp2 = 1, 1  # i-1, i-2

    def ways_single(c):
        if c == '*': return 9
        if c == '0': return 0
        return 1

    def ways_double(a, b):
        if a == '*' and b == '*':
            return 15  # 11-19 (9 ways) + 21-26 (6 ways)
        if a == '*':
            if '0' <= b <= '6': return 2  # 10-16, 20-26
            else: return 1
        if b == '*':
            if a == '1': return 9
            if a == '2': return 6
            return 0
        # both digits
        v = int(a+b)
        return 1 if 10 <= v <= 26 else 0

    for i in range(1, n):
        c1, c2 = s[i], s[i-1]
        cur = (ways_single(c1)*dp1 + ways_double(c2,c1)*dp2) % MOD
        dp1, dp2 = cur, dp1

    return dp1 % MOD

print(num_decodings_ii("*"))  # 9
```

***

## 43) Domino and Tromino Tiling

<br>

DP idea:

dp\[n] = dp\[n-1] + dp\[n-2] + 2\*sum(dp\[0..n-3])

Use optimized recurrence:

dp\[n] = 2\*dp\[n-1] + dp\[n-3].

```python
def num_tilings(n):
    if n <= 2: return [1,1,2][n]
    dp = [0]*(n+1)
    dp[0], dp[1], dp[2] = 1,1,2
    for i in range(3, n+1):
        dp[i] = 2*dp[i-1] + dp[i-3]
    return dp[n]

print(num_tilings(5))  # 24
```

***

## 44) Paint Fence

DP idea:

Two states: same-color and diff-color.

Final: dp\[n] = (k-1)\*(dp\[n-1] + dp\[n-2]).

```python
def num_ways_paint_fence(n, k):
    if n == 1: return k
    same = k
    diff = k*(k-1)
    for _ in range(3, n+1):
        new_same = diff
        new_diff = (same + diff)*(k-1)
        same, diff = new_same, new_diff
    return same + diff

print(num_ways_paint_fence(3,2))  # 6
```

***

## 45) Remove Boxes (hard DP)

DP idea:

3D DP: dp\[l]\[r]\[k]: max points in boxes\[l..r] with k equal boxes appended at right.

```python
from functools import lru_cache

def remove_boxes(boxes):
    @lru_cache(None)
    def dp(l, r, k):
        if l > r: return 0
        # merge equal boxes at right
        while l < r and boxes[r] == boxes[r-1]:
            r -= 1
            k += 1
        res = dp(l, r-1, 0) + (k+1)*(k+1)
        for i in range(l, r):
            if boxes[i] == boxes[r]:
                res = max(res, dp(i+1, r-1, 0) + dp(l, i, k+1))
        return res
    return dp(0, len(boxes)-1, 0)

print(remove_boxes([1,3,2,2,2,3,4,3,1]))  # 23
```

***

## 46) Palindrome Partitioning II (minimum cuts)

DP idea:

* Precompute palindromes.
* dp\[i] = min cuts for prefix ending at i.

```python
def min_cut(s):
    n = len(s)
    pal = [[False]*n for _ in range(n)]
    for i in reversed(range(n)):
        for j in range(i, n):
            if s[i] == s[j] and (j-i < 2 or pal[i+1][j-1]):
                pal[i][j] = True

    dp = [0]*n
    for i in range(n):
        if pal[0][i]:
            dp[i] = 0
        else:
            dp[i] = min(dp[j] + 1 for j in range(i) if pal[j+1][i])
    return dp[-1]

print(min_cut("aab"))  # 1 ("aa"|"b")
```

***

## 47) Count Palindromic Subsequences (DP)

DP idea:

If s\[i] == s\[j], include inner + two ends; else subtract overlap.

```python
def count_pal_subseq(s):
    n = len(s)
    MOD = 10**9+7
    dp = [[0]*n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for L in range(2, n+1):
        for i in range(n-L+1):
            j = i+L-1
            if s[i] == s[j]:
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] + 1) % MOD
            else:
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1]) % MOD
    return dp[0][n-1]

print(count_pal_subseq("aaa"))  # 6
```

***

## 48) Minimum ASCII Delete Sum for Two Strings

DP idea:

dp\[i]\[j]: min delete sum to equalize s1\[:i] and s2\[:j].

```python
def minimum_delete_sum(s1, s2):
    m, n = len(s1), len(s2)
    dp = [0]*(n+1)
    for j in range(1, n+1):
        dp[j] = dp[j-1] + ord(s2[j-1])
    for i in range(1, m+1):
        prev = dp[0]
        dp[0] += ord(s1[i-1])
        for j in range(1, n+1):
            temp = dp[j]
            if s1[i-1] == s2[j-1]:
                dp[j] = prev
            else:
                dp[j] = min(dp[j] + ord(s1[i-1]),
                            dp[j-1] + ord(s2[j-1]))
            prev = temp
    return dp[n]

print(minimum_delete_sum("sea","eat"))  # 231
```

***

## 49) Maximum Sum of Non-Adjacent Elements (House Robber I)

DP idea:

Classic: dp\[i] = max(dp\[i-1], dp\[i-2] + nums\[i]).

```python
def rob(nums):
    prev, curr = 0, 0
    for x in nums:
        prev, curr = curr, max(curr, prev + x)
    return curr

print(rob([1,2,3,1]))  # 4
```

***

## 50) House Robber II (circular)

DP idea: rob either \[0..n-2] or \[1..n-1].

```python
def rob2(nums):
    if len(nums) <= 1:
        return nums[0] if nums else 0

    def rob_linear(arr):
        prev, curr = 0, 0
        for x in arr:
            prev, curr = curr, max(curr, prev + x)
        return curr

    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))

print(rob2([2,3,2]))  # 3
```

***


## 17. Digit DP
Counting numbers with certain constraints on digits between `[L, R]`.

### Core Idea:
State is `dp(idx, tightly_bound, ...other_constraints)`.
`tightly_bound` is a boolean indicating if the digit we pick is restricted by the upper bound `R` at `idx`.

```python
# Example: Count numbers <= R whose digits sum to S
def solve(R, S):
    digit_str = str(R)
    n = len(digit_str)
    memo = {}

    def dp(idx, tight, curr_sum):
        if curr_sum > S:
            return 0
        if idx == n:
            return 1 if curr_sum == S else 0
        if (idx, tight, curr_sum) in memo:
            return memo[(idx, tight, curr_sum)]
            
        limit = int(digit_str[idx]) if tight else 9
        res = 0
        for d in range(limit + 1):
            res += dp(idx + 1, tight and (d == limit), curr_sum + d)
            
        memo[(idx, tight, curr_sum)] = res
        return res

    return dp(0, True, 0)
```

## 18. DP with Bitmask
Useful when the state can be represented as a subset of elements (usually `N <= 20`).

### Core Idea:
Use an integer to represent a set of items. `bitmask & (1 << i)` checks if item `i` is in the set.

```python
# Example: Traveling Salesman Problem (TSP) using Bitmask DP
def tsp(graph):
    n = len(graph)
    VISITED_ALL = (1 << n) - 1
    memo = {}
    
    def dp(mask, pos):
        if mask == VISITED_ALL:
            return graph[pos][0] # Return to start
            
        if (mask, pos) in memo:
            return memo[(mask, pos)]
            
        ans = float('inf')
        for city in range(n):
            if (mask & (1 << city)) == 0: # If not visited
                ans = min(ans, graph[pos][city] + dp(mask | (1 << city), city))
                
        memo[(mask, pos)] = ans
        return ans
        
    return dp(1, 0) # Start at city 0
```

## 19. DP on Trees
Often requires a post-order traversal (children evaluated before parent).

### Core Idea:
`dp[node]` depends on `dp[leftChild]` and `dp[rightChild]`.

```python
# Example: Maximum Path Sum in a Binary Tree
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float('-inf')

        def max_gain(node):
            if not node:
                return 0
            
            # Max sum on the left and right sub-trees of node
            left_gain = max(max_gain(node.left), 0)
            right_gain = max(max_gain(node.right), 0)
            
            # Current max path with node as the highest point
            price_newpath = node.val + left_gain + right_gain
            self.max_sum = max(self.max_sum, price_newpath)
            
            # For recursion, return the max gain if we continue the path
            return node.val + max(left_gain, right_gain)

        max_gain(root)
        return self.max_sum
```
