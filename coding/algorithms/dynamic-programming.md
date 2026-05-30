---
tags: [coding, algorithms, dynamic-programming]
topic: Dynamic Programming
difficulty: mixed
---

# Dynamic Programming — Problem Reference by Pattern

> [!info] First Principles
> DP applies when a problem has *overlapping subproblems* (same sub-call arises from multiple paths) and *optimal substructure* (optimal whole = f(optimal parts)). The recipe: (1) name the state in one sentence, (2) write the recurrence, (3) identify base cases, (4) choose fill order so dependencies precede use, (5) optimize space if `dp[i]` only looks back a fixed window.

---

## Linear DP (1-D)

### Climbing Stairs

> [!example] Problem
> Count distinct ways to reach step `n` starting from 0; each move is +1 or +2 steps.

> [!info] Approach
> - **WHY:** reaching step `i` from step `i-1` or `i-2` creates overlapping recursive calls.
> - **WHAT:** `dp[i]` = number of ways to reach step `i`.
> - **HOW:** `dp[i] = dp[i-1] + dp[i-2]`; base `dp[0]=1, dp[1]=1`. This is Fibonacci. Space collapses to two variables.

> [!note]- Python Solution
> ```python
> def climbStairs(n: int) -> int:
>     if n <= 2:
>         return n
>     prev2, prev1 = 1, 2
>     for _ in range(3, n + 1):
>         prev2, prev1 = prev1, prev2 + prev1
>     return prev1
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down memoization; matrix exponentiation for O(log n).

---

### Min Cost Climbing Stairs

> [!example] Problem
> Each step has a cost. You can start from step 0 or 1. Pay cost to leave a step (+1 or +2). Minimize total cost to reach beyond the last step.

> [!info] Approach
> - **WHY:** cost to reach step `i` depends on minimum of two prior steps.
> - **WHAT:** `dp[i]` = min cost to reach step `i`.
> - **HOW:** `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`; answer = `min(dp[n-1], dp[n-2])`.

> [!note]- Python Solution
> ```python
> def minCostClimbingStairs(cost: list[int]) -> int:
>     n = len(cost)
>     prev2, prev1 = cost[0], cost[1]
>     for i in range(2, n):
>         prev2, prev1 = prev1, cost[i] + min(prev1, prev2)
>     return min(prev1, prev2)
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down; extend `cost` with a zero at position `n` to unify the final min.

---

### House Robber

> [!example] Problem
> Rob houses along a street; no two adjacent houses. Maximize money.

> [!info] Approach
> - **WHY:** robbing house `i` forbids `i-1`; the optimal decision at each house depends on the optimal result two positions back.
> - **WHAT:** `dp[i]` = max money from houses `0..i`.
> - **HOW:** `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`; base `dp[0]=nums[0]`, `dp[1]=max(nums[0],nums[1])`.

> [!note]- Python Solution
> ```python
> def rob(nums: list[int]) -> int:
>     prev2, prev1 = 0, 0
>     for n in nums:
>         prev2, prev1 = prev1, max(prev1, prev2 + n)
>     return prev1
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down memoization. Greedy fails — skipping a high house today can be globally optimal.

---

### House Robber II (Circular)

> [!example] Problem
> Houses in a circle — first and last are adjacent.

> [!info] Approach
> - **WHY:** Circular constraint means house 0 and house n-1 can't both be robbed.
> - **WHAT:** Reduce to two linear subproblems that are mutually exclusive.
> - **HOW:** `max(rob(0..n-2), rob(1..n-1))` — run linear House Robber twice.

> [!note]- Python Solution
> ```python
> def rob(nums: list[int]) -> int:
>     def rob_linear(houses: list[int]) -> int:
>         p2, p1 = 0, 0
>         for h in houses:
>             p2, p1 = p1, max(p1, p2 + h)
>         return p1
> 
>     if len(nums) == 1:
>         return nums[0]
>     return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Single pass tracking whether house 0 was taken — equivalent but more complex to implement.

---

### Maximum Subarray (Kadane's — DP view)

> [!example] Problem
> Find the contiguous subarray with the largest sum.

> [!info] Approach
> - **WHY:** max subarray ending at `i` depends on whether extending the previous subarray or restarting gives a larger value.
> - **WHAT:** `dp[i]` = max subarray sum ending at index `i`.
> - **HOW:** `dp[i] = max(nums[i], dp[i-1] + nums[i])`; answer = `max(dp)`. Collapses to one variable.

> [!note]- Python Solution
> ```python
> def maxSubArray(nums: list[int]) -> int:
>     best = curr = nums[0]
>     for x in nums[1:]:
>         curr = max(x, curr + x)
>         best = max(best, curr)
>     return best
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> D&C approach O(n log n) — cross-midpoint expansion, useful for explaining recurrence. Prefix sum with running minimum gives the same result.

---

### Word Break

> [!example] Problem
> Can string `s` be segmented into words from a dictionary?

> [!info] Approach
> - **WHY:** `s[0..i]` is breakable if any split `s[0..j]` is breakable and `s[j+1..i]` is in the dictionary. Subproblems overlap at shared prefixes.
> - **WHAT:** `dp[i]` = True if `s[0..i-1]` is breakable.
> - **HOW:** `dp[i] = any(dp[j] and s[j:i] in word_set)` for `j` in `[i-max_len, i)`. Base: `dp[0]=True`.

> [!note]- Python Solution
> ```python
> def wordBreak(s: str, wordDict: list[str]) -> bool:
>     word_set = set(wordDict)
>     max_len = max(len(w) for w in wordDict)
>     n = len(s)
>     dp = [False] * (n + 1)
>     dp[0] = True
>     for i in range(1, n + 1):
>         for j in range(max(0, i - max_len), i):
>             if dp[j] and s[j:i] in word_set:
>                 dp[i] = True
>                 break
>     return dp[n]
> ```

> [!success] Complexity
> Time O(n × max_word_len), Space O(n).

> [!tip] Alternatives
> BFS with memoization; Trie for faster dictionary lookup.

---

### Decode Ways

> [!example] Problem
> String of digits where A=1..Z=26. Count distinct decodings.

> [!info] Approach
> - **WHY:** each position can be decoded as 1 or 2 digits; choices overlap across prefixes.
> - **WHAT:** `dp[i]` = number of decodings of `s[0..i-1]`.
> - **HOW:** add `dp[i-1]` if `s[i-1] != '0'`; add `dp[i-2]` if `10 ≤ s[i-2:i] ≤ 26`. Base: `dp[0]=1`.

> [!note]- Python Solution
> ```python
> def numDecodings(s: str) -> int:
>     prev2, prev1 = 1, 0 if s[0] == '0' else 1
>     for i in range(2, len(s) + 1):
>         curr = 0
>         if s[i-1] != '0':
>             curr += prev1
>         if 10 <= int(s[i-2:i]) <= 26:
>             curr += prev2
>         prev2, prev1 = prev1, curr
>     return prev1
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down memoization. Wildcard variant (LC 639) adds branching at `'*'` but same structure.

---

## 0/1 Knapsack

### Subset Sum Problem

> [!example] Problem
> Given integers and target `T`, can any subset sum to `T`?

> [!info] Approach
> - **WHY:** each item has two choices (include/exclude); overlap arises because the same remaining capacity is reachable via multiple item sequences.
> - **WHAT:** `dp[j]` = True if sum `j` is achievable using a subset of items seen so far.
> - **HOW:** iterate items; for each item `x`, sweep `j` from `T` down to `x`: `dp[j] |= dp[j - x]`. Reverse sweep prevents reuse of same item (0/1 knapsack). Base: `dp[0]=True`.

> [!note]- Python Solution
> ```python
> def canPartition(nums: list[int], target: int) -> bool:
>     dp = [False] * (target + 1)
>     dp[0] = True
>     for x in nums:
>         for j in range(target, x - 1, -1):
>             dp[j] = dp[j] or dp[j - x]
>     return dp[target]
> ```

> [!success] Complexity
> Time O(n × T), Space O(T).

> [!tip] Alternatives
> Meet-in-the-middle O(2^(n/2)) for very large `n` with small target; bitset optimization.

---

### Partition Equal Subset Sum

> [!example] Problem
> Can `nums` be split into two subsets with equal sum?

> [!info] Approach
> - **WHY:** Equal partition iff one subset sums to `total/2`. Reduces to subset-sum with `T = total // 2`.
> - **WHAT:** Same as Subset Sum with `target = sum(nums) // 2`.
> - **HOW:** Odd total → return False immediately. Then run 0/1 knapsack DP.

> [!note]- Python Solution
> ```python
> def canPartition(nums: list[int]) -> bool:
>     total = sum(nums)
>     if total % 2:
>         return False
>     target = total // 2
>     dp = [False] * (target + 1)
>     dp[0] = True
>     for x in nums:
>         for j in range(target, x - 1, -1):
>             dp[j] = dp[j] or dp[j - x]
>     return dp[target]
> ```

> [!success] Complexity
> Time O(n × sum), Space O(sum).

> [!tip] Alternatives
> Early exit if any single element > target. Bitset trick for constant-factor speedup.

---

### Target Sum

> [!example] Problem
> Assign `+` or `-` to each number; count assignments achieving a target sum.

> [!info] Approach
> - **WHY:** Math insight: if `P` = sum of positives and `N` = sum of negatives, `P - N = target` and `P + N = total`. So `P = (target + total) / 2`. Count subsets summing to `P` — overlapping subproblems.
> - **WHAT:** `dp[j]` = number of subsets summing to `j`.
> - **HOW:** `dp[j] += dp[j - x]` in reverse order (0/1 knapsack). Base: `dp[0]=1`.

> [!note]- Python Solution
> ```python
> def findTargetSumWays(nums: list[int], target: int) -> int:
>     total = sum(nums)
>     if (total + target) % 2 or abs(target) > total:
>         return 0
>     S = (total + target) // 2
>     dp = [0] * (S + 1)
>     dp[0] = 1
>     for x in nums:
>         for j in range(S, x - 1, -1):
>             dp[j] += dp[j - x]
>     return dp[S]
> ```

> [!success] Complexity
> Time O(n × S), Space O(S).

> [!tip] Alternatives
> DFS + memoization on `(index, running_sum)`. 2D DP `dp[i][j]` counts ways using first `i` items with sum `j`.

---

### Last Stone Weight II

> [!example] Problem
> Smash pairs of stones (losing the difference); minimize the last remaining stone weight.

> [!info] Approach
> - **WHY:** Each stone ultimately gets a sign `+1` or `-1`; minimize `|P - N| = |total - 2N|`. Maximize `N ≤ total/2`. Same as subset sum to target.
> - **WHAT:** `dp[j]` = True if subset sum `j` is reachable, for `j ≤ total // 2`.
> - **HOW:** Standard 0/1 knapsack boolean DP; answer = `total - 2 × max_j_where_dp[j]`.

> [!note]- Python Solution
> ```python
> def lastStoneWeightII(stones: list[int]) -> int:
>     total = sum(stones)
>     target = total // 2
>     dp = [False] * (target + 1)
>     dp[0] = True
>     for s in stones:
>         for j in range(target, s - 1, -1):
>             dp[j] = dp[j] or dp[j - s]
>     best = next(j for j in range(target, -1, -1) if dp[j])
>     return total - 2 * best
> ```

> [!success] Complexity
> Time O(n × total), Space O(total).

> [!tip] Alternatives
> Integer DP counting ways; the boolean version suffices here.

---

## Unbounded Knapsack

### Coin Change (Min Coins)

> [!example] Problem
> Minimum coins from unlimited denominations to make amount `A`. Return -1 if impossible.

> [!info] Approach
> - **WHY:** Coins are reusable → unbounded knapsack. Overlapping subproblems: the optimal solution for amount `i` reuses optimal solutions for `i - coin`.
> - **WHAT:** `dp[i]` = min coins to make amount `i`.
> - **HOW:** `dp[i] = min(dp[i-c] + 1)` for each coin `c ≤ i`; forward sweep (reuse allowed). Base: `dp[0]=0`, rest `inf`.

> [!note]- Python Solution
> ```python
> def coinChange(coins: list[int], amount: int) -> int:
>     dp = [float('inf')] * (amount + 1)
>     dp[0] = 0
>     for i in range(1, amount + 1):
>         for c in coins:
>             if c <= i:
>                 dp[i] = min(dp[i], dp[i - c] + 1)
>     return dp[amount] if dp[amount] != float('inf') else -1
> ```

> [!success] Complexity
> Time O(amount × |coins|), Space O(amount).

> [!tip] Alternatives
> BFS level-by-level (level = coin count) — same complexity but queue overhead. Top-down memo.

---

### Coin Change II (Total Ways)

> [!example] Problem
> Count combinations (not permutations) of coins summing to `amount`.

> [!info] Approach
> - **WHY:** Combinations require each denomination to be processed once, not per position. Loop coins outer, amounts inner.
> - **WHAT:** `dp[i]` = number of combination ways to make amount `i`.
> - **HOW:** Outer loop over coins; inner forward sweep: `dp[i] += dp[i-c]`. This ensures [1,2] and [2,1] are the same combination.

> [!note]- Python Solution
> ```python
> def change(amount: int, coins: list[int]) -> int:
>     dp = [0] * (amount + 1)
>     dp[0] = 1
>     for c in coins:
>         for i in range(c, amount + 1):
>             dp[i] += dp[i - c]
>     return dp[amount]
> ```

> [!success] Complexity
> Time O(amount × |coins|), Space O(amount).

> [!tip] Alternatives
> Swapping loop order counts permutations (ordered sequences) — different problem. 2D DP clarifies the derivation.

---

### Perfect Squares

> [!example] Problem
> Minimum number of perfect squares summing to `n`.

> [!info] Approach
> - **WHY:** Perfect squares are unlimited "coins"; this is unbounded knapsack / coin change with coins = {1,4,9,16,...}.
> - **WHAT:** `dp[i]` = min squares summing to `i`.
> - **HOW:** `dp[i] = min(dp[i - k²] + 1)` for all `k² ≤ i`. Base: `dp[0]=0`.

> [!note]- Python Solution
> ```python
> def numSquares(n: int) -> int:
>     squares = [k*k for k in range(1, int(n**0.5) + 1)]
>     dp = [float('inf')] * (n + 1)
>     dp[0] = 0
>     for i in range(1, n + 1):
>         for sq in squares:
>             if sq > i:
>                 break
>             dp[i] = min(dp[i], dp[i - sq] + 1)
>     return dp[n]
> ```

> [!success] Complexity
> Time O(n√n), Space O(n).

> [!tip] Alternatives
> BFS (level = number of squares used). Lagrange's four-square theorem: answer ≤ 4; check 1, 2, 3, 4 mathematically in O(√n) — but DP is the expected interview answer.

---

## LCS Family

### Longest Common Subsequence

> [!example] Problem
> Length of longest common subsequence (non-contiguous) of two strings.

> [!info] Approach
> - **WHY:** Matching characters at positions `i,j` yields a subproblem on the remaining suffixes; these sub-results are reused.
> - **WHAT:** `dp[i][j]` = LCS length of `s1[0..i-1]` and `s2[0..j-1]`.
> - **HOW:** If `s1[i-1]==s2[j-1]`: `dp[i][j] = dp[i-1][j-1]+1`; else `max(dp[i-1][j], dp[i][j-1])`. Space: roll to one row.

> [!note]- Python Solution
> ```python
> def longestCommonSubsequence(text1: str, text2: str) -> int:
>     if len(text1) < len(text2):
>         text1, text2 = text2, text1
>     prev = [0] * (len(text2) + 1)
>     for ch1 in text1:
>         curr = [0] * (len(text2) + 1)
>         for j, ch2 in enumerate(text2, 1):
>             curr[j] = prev[j-1] + 1 if ch1 == ch2 else max(prev[j], curr[j-1])
>         prev = curr
>     return prev[len(text2)]
> ```

> [!success] Complexity
> Time O(m×n), Space O(min(m,n)).

> [!tip] Alternatives
> Full 2D table for path reconstruction. Hunt-Szymanski for sparse matches.

---

### Edit Distance

> [!example] Problem
> Minimum insert/delete/replace operations to convert `word1` to `word2`.

> [!info] Approach
> - **WHY:** Three operations at each mismatch create overlapping subproblems on shorter string pairs.
> - **WHAT:** `dp[i][j]` = edit distance between `word1[0..i-1]` and `word2[0..j-1]`.
> - **HOW:** If chars match: `dp[i-1][j-1]`; else `1 + min(replace=dp[i-1][j-1], delete=dp[i-1][j], insert=dp[i][j-1])`. Base: `dp[i][0]=i`, `dp[0][j]=j`.

> [!note]- Python Solution
> ```python
> def minDistance(word1: str, word2: str) -> int:
>     m, n = len(word1), len(word2)
>     prev = list(range(n + 1))
>     for i in range(1, m + 1):
>         curr = [i] + [0] * n
>         for j in range(1, n + 1):
>             if word1[i-1] == word2[j-1]:
>                 curr[j] = prev[j-1]
>             else:
>                 curr[j] = 1 + min(prev[j-1], prev[j], curr[j-1])
>         prev = curr
>     return prev[n]
> ```

> [!success] Complexity
> Time O(m×n), Space O(min(m,n)).

> [!tip] Alternatives
> Full 2D for operation reconstruction. Ukkonen's O(k×min(m,n)) when distance `k` is small.

---

### Longest Palindromic Subsequence

> [!example] Problem
> Length of longest palindromic subsequence in string `s`.

> [!info] Approach
> - **WHY:** A palindrome is its own reverse; LPS(s) = LCS(s, reverse(s)). Both overlapping subproblems.
> - **WHAT:** `dp[i][j]` = LPS length in `s[i..j]`.
> - **HOW:** If `s[i]==s[j]`: `dp[i][j] = dp[i+1][j-1]+2`; else `max(dp[i+1][j], dp[i][j-1])`. Fill diagonals outward (length 1→2→…→n).

> [!note]- Python Solution
> ```python
> def longestPalindromeSubseq(s: str) -> int:
>     n = len(s)
>     dp = [[0] * n for _ in range(n)]
>     for i in range(n):
>         dp[i][i] = 1
>     for length in range(2, n + 1):
>         for i in range(n - length + 1):
>             j = i + length - 1
>             if s[i] == s[j]:
>                 dp[i][j] = (dp[i+1][j-1] if length > 2 else 0) + 2
>             else:
>                 dp[i][j] = max(dp[i+1][j], dp[i][j-1])
>     return dp[0][n-1]
> ```

> [!success] Complexity
> Time O(n²), Space O(n²).

> [!tip] Alternatives
> LCS(s, s[::-1]) — simpler to implement, same complexity. Space-optimize with two 1D arrays.

---

### Minimum ASCII Delete Sum for Two Strings

> [!example] Problem
> Find minimum sum of ASCII values of deleted characters to make two strings equal.

> [!info] Approach
> - **WHY:** Deleting characters to equalize is equivalent to keeping the maximum-weight common subsequence (measured in ASCII values). Overlapping on pairs of string prefixes.
> - **WHAT:** `dp[i][j]` = min ASCII delete cost to equalize `s1[0..i-1]` and `s2[0..j-1]`.
> - **HOW:** If `s1[i-1]==s2[j-1]`: `dp[i][j]=dp[i-1][j-1]`; else `min(dp[i-1][j]+ord(s1[i-1]), dp[i][j-1]+ord(s2[j-1]))`. Base: prefix ASCII sums.

> [!note]- Python Solution
> ```python
> def minimumDeleteSum(s1: str, s2: str) -> int:
>     m, n = len(s1), len(s2)
>     prev = [sum(ord(c) for c in s2[:j]) for j in range(n + 1)]
>     for i in range(1, m + 1):
>         curr = [prev[0] + ord(s1[i-1])] + [0] * n
>         for j in range(1, n + 1):
>             if s1[i-1] == s2[j-1]:
>                 curr[j] = prev[j-1]
>             else:
>                 curr[j] = min(prev[j] + ord(s1[i-1]), curr[j-1] + ord(s2[j-1]))
>         prev = curr
>     return prev[n]
> ```

> [!success] Complexity
> Time O(m×n), Space O(min(m,n)).

> [!tip] Alternatives
> Compute LCS weighted by ASCII; answer = `total_ascii(s1) + total_ascii(s2) - 2 × weighted_LCS`.

---

### Minimum Window Subsequence (LC 727)

> [!example] Problem
> Given strings s and t, find the minimum length substring of s such that t is a subsequence of that substring. Return "" if none exists.

> [!info] Approach
> - WHY: Brute force tries all substrings O(n²*m). DP achieves O(n*m): track, for each position in s, the earliest start index in s such that t[0..j] has been matched as a subsequence ending at that position.
> - WHAT: 2D DP — dp[i][j] = starting index in s such that s[dp[i][j]..i] contains t[0..j] as a subsequence.
> - HOW: dp[i][j] = dp[i-1][j-1] if s[i]==t[j] else dp[i-1][j]. Base: dp[i][0] = i when s[i]==t[0]. When dp[i][len(t)-1] is valid, compute window length = i - dp[i][len(t)-1] + 1 and track minimum.

> [!note]- Python Solution
> ```python
> def minWindow(s: str, t: str) -> str:
>     m, n = len(s), len(t)
>     # dp[j] = start index in s for matching t[0..j] ending at current s position
>     INF = float('inf')
>     dp = [INF] * n
>     best_start, best_len = 0, INF
> 
>     for i in range(m):
>         # iterate j in reverse to avoid using s[i] twice in same row
>         new_dp = [INF] * n
>         for j in range(n):
>             if s[i] == t[j]:
>                 if j == 0:
>                     new_dp[j] = i  # fresh match starting at i
>                 elif dp[j-1] != INF:
>                     new_dp[j] = dp[j-1]  # extend previous match
>             else:
>                 new_dp[j] = dp[j]  # carry forward
>         dp = new_dp
>         if dp[n-1] != INF:
>             window_len = i - dp[n-1] + 1
>             if window_len < best_len:
>                 best_len = window_len
>                 best_start = dp[n-1]
> 
>     return s[best_start:best_start + best_len] if best_len != INF else ""
> ```

> [!success] Complexity
> O(n*m) time, O(m) space (rolling 1D dp array, optimized from O(n*m)).

> [!tip] Alternatives
> Two-pointer O(n*m): forward pass to find end of window (extend right until t matched), backward pass to minimize start (contract left). Simpler to implement — for each valid end, walk backwards through s matching t in reverse to find tightest start.

---

## Grid DP

### Unique Paths

> [!example] Problem
> Count distinct paths from top-left to bottom-right of m×n grid moving only right or down.

> [!info] Approach
> - **WHY:** Each cell is reachable from exactly above or left; paths to any cell = sum of paths to two neighbors — overlapping.
> - **WHAT:** `dp[j]` = paths to column `j` of current row (rolling 1D array).
> - **HOW:** `dp[j] += dp[j-1]` for each row. Base: all 1s initially (single path along edges).

> [!note]- Python Solution
> ```python
> def uniquePaths(m: int, n: int) -> int:
>     dp = [1] * n
>     for _ in range(1, m):
>         for j in range(1, n):
>             dp[j] += dp[j-1]
>     return dp[n-1]
> ```

> [!success] Complexity
> Time O(m×n), Space O(n).

> [!tip] Alternatives
> Combinatorics: `math.comb(m+n-2, m-1)` — O(min(m,n)) time, O(1) space.

---

### Unique Paths II (With Obstacles)

> [!example] Problem
> Unique paths but some cells are blocked (obstacle=1).

> [!info] Approach
> - **WHY:** Same grid DP but obstacle cells have zero paths and block propagation downstream.
> - **WHAT:** `dp[j]` = paths to `(i,j)` treating blocked cells as 0.
> - **HOW:** Same recurrence; set `dp[j]=0` when `obstacleGrid[i][j]==1`. Careful with first row/col initialization.

> [!note]- Python Solution
> ```python
> def uniquePathsWithObstacles(obstacleGrid: list[list[int]]) -> int:
>     m, n = len(obstacleGrid), len(obstacleGrid[0])
>     dp = [0] * n
>     dp[0] = 1 if obstacleGrid[0][0] == 0 else 0
>     for i in range(m):
>         for j in range(n):
>             if obstacleGrid[i][j] == 1:
>                 dp[j] = 0
>             elif j > 0:
>                 dp[j] += dp[j-1]
>     return dp[n-1]
> ```

> [!success] Complexity
> Time O(m×n), Space O(n).

> [!tip] Alternatives
> Full 2D table is simpler to reason about. No combinatorial shortcut with obstacles.

---

### Minimum Path Sum

> [!example] Problem
> Top-left to bottom-right, moving right/down only. Minimize sum of values on path.

> [!info] Approach
> - **WHY:** Min-cost path to `(i,j)` = grid value + min of cost from above or left — overlapping.
> - **WHAT:** `dp[j]` = min cost to reach column `j` of current row.
> - **HOW:** `dp[j] = grid[i][j] + min(dp[j], dp[j-1])`. Initialize first row as prefix sums.

> [!note]- Python Solution
> ```python
> def minPathSum(grid: list[list[int]]) -> int:
>     m, n = len(grid), len(grid[0])
>     dp = grid[0][:]
>     for j in range(1, n):
>         dp[j] += dp[j-1]
>     for i in range(1, m):
>         dp[0] += grid[i][0]
>         for j in range(1, n):
>             dp[j] = grid[i][j] + min(dp[j], dp[j-1])
>     return dp[n-1]
> ```

> [!success] Complexity
> Time O(m×n), Space O(n).

> [!tip] Alternatives
> Dijkstra if negative weights possible. In-place modification gives O(1) extra space.

---

### Maximal Square

> [!example] Problem
> Largest square of 1s in a binary matrix; return its area.

> [!info] Approach
> - **WHY:** A square of side `k` at `(i,j)` requires squares of side `k-1` at three adjacent neighbors — optimal substructure with overlapping sub-rectangles.
> - **WHAT:** `dp[i][j]` = side of largest all-1s square with bottom-right at `(i,j)`.
> - **HOW:** If `matrix[i][j]=='1'`: `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1`. Roll to two rows or 1D.

> [!note]- Python Solution
> ```python
> def maximalSquare(matrix: list[list[str]]) -> int:
>     m, n = len(matrix), len(matrix[0])
>     dp = [[0] * (n + 1) for _ in range(m + 1)]
>     side = 0
>     for i in range(1, m + 1):
>         for j in range(1, n + 1):
>             if matrix[i-1][j-1] == '1':
>                 dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
>                 side = max(side, dp[i][j])
>     return side * side
> ```

> [!success] Complexity
> Time O(m×n), Space O(m×n) → reducible to O(n).

> [!tip] Alternatives
> Histogram approach (largest rectangle in histogram per row) — O(m×n) but harder to implement.

---

## Interval DP

### Burst Balloons

> [!example] Problem
> `n` balloons with values. Bursting balloon `i` scores `nums[i-1]*nums[i]*nums[i+1]`. Maximize total coins.

> [!info] Approach
> - **WHY:** Choosing which balloon to burst first/last creates overlapping sub-intervals. Thinking "last balloon burst" in an interval gives clean independence.
> - **WHAT:** `dp[i][j]` = max coins from bursting all balloons strictly between `i` and `j` (pad array with 1s at both ends).
> - **HOW:** For each `k` in `(i,j)`: `dp[i][j] = max(dp[i][k] + nums[i]*nums[k]*nums[j] + dp[k][j])`. Fill by increasing interval length.

> [!note]- Python Solution
> ```python
> def maxCoins(nums: list[int]) -> int:
>     nums = [1] + nums + [1]
>     n = len(nums)
>     dp = [[0] * n for _ in range(n)]
>     for length in range(2, n):
>         for left in range(n - length):
>             right = left + length
>             for k in range(left + 1, right):
>                 dp[left][right] = max(
>                     dp[left][right],
>                     dp[left][k] + nums[left] * nums[k] * nums[right] + dp[k][right]
>                 )
>     return dp[0][n-1]
> ```

> [!success] Complexity
> Time O(n³), Space O(n²).

> [!tip] Alternatives
> Top-down memoization with same state. No known improvement below O(n³).

---

### Matrix Chain Multiplication (Concept)

> [!example] Problem
> Given dimensions of matrices to multiply in sequence, find the optimal parenthesization minimizing scalar multiplications.

> [!info] Approach
> - **WHY:** Splitting the chain at any point `k` yields independent subproblems for left and right chains; optimal split depends on results of all sub-chains — overlapping.
> - **WHAT:** `dp[i][j]` = min cost to multiply matrices `i` through `j`.
> - **HOW:** `dp[i][j] = min(dp[i][k] + dp[k+1][j] + dims[i-1]*dims[k]*dims[j])` for `k` in `[i,j)`. Base: `dp[i][i]=0`.

> [!note]- Python Solution
> ```python
> def matrixChainOrder(dims: list[int]) -> int:
>     n = len(dims) - 1  # n matrices
>     dp = [[0] * n for _ in range(n)]
>     for length in range(2, n + 1):
>         for i in range(n - length + 1):
>             j = i + length - 1
>             dp[i][j] = float('inf')
>             for k in range(i, j):
>                 cost = dp[i][k] + dp[k+1][j] + dims[i] * dims[k+1] * dims[j+1]
>                 dp[i][j] = min(dp[i][j], cost)
>     return dp[0][n-1]
> ```

> [!success] Complexity
> Time O(n³), Space O(n²).

> [!tip] Alternatives
> Hu-Shing algorithm achieves O(n log n) but is rarely asked in interviews.

---

### Palindrome Partitioning II (Minimum Cuts)

> [!example] Problem
> Minimum cuts to partition `s` into palindromic substrings.

> [!info] Approach
> - **WHY:** Min cuts for `s[0..i]` depends on min cuts for all valid palindromic suffixes — overlapping.
> - **WHAT:** `dp[i]` = min cuts for `s[0..i]`. Precompute `is_pal[i][j]` in O(n²).
> - **HOW:** `dp[i] = min(dp[j-1]+1)` for all `j ≤ i` where `s[j..i]` is palindrome; `dp[j-1]=-1` when `j=0`.

> [!note]- Python Solution
> ```python
> def minCut(s: str) -> int:
>     n = len(s)
>     is_pal = [[False] * n for _ in range(n)]
>     for i in range(n - 1, -1, -1):
>         for j in range(i, n):
>             is_pal[i][j] = s[i] == s[j] and (j - i < 2 or is_pal[i+1][j-1])
>     dp = list(range(-1, n))  # dp[i+1] = min cuts for s[0..i]
>     for i in range(n):
>         for j in range(i + 1):
>             if is_pal[j][i]:
>                 dp[i+1] = min(dp[i+1], dp[j] + 1)
>     return dp[n]
> ```

> [!success] Complexity
> Time O(n²), Space O(n²).

> [!tip] Alternatives
> Manacher's for O(n) palindrome precomputation; the cuts DP itself stays O(n²).

---

### Strange Printer

> [!example] Problem
> A printer can only print a sequence of the same character. Minimum turns to print string `s`.

> [!info] Approach
> - **WHY:** Printing `s[i..j]` can leverage if `s[i]==s[k]` for some `k` in `(i,j)` — we can extend the first turn to cover `s[k]`. Interval DP captures this.
> - **WHAT:** `dp[i][j]` = min turns to print `s[i..j]`.
> - **HOW:** Base: `dp[i][i]=1`. For `i<j`: start with `dp[i][j] = dp[i+1][j] + 1` (print `s[i]` alone, then recurse). If `s[i]==s[k]` for some `k` in `(i,j]`: `dp[i][j] = min(dp[i][j], dp[i+1][k] + dp[k+1][j])` — merge `s[i]` with `s[k]`'s turn.

> [!note]- Python Solution
> ```python
> def strangePrinter(s: str) -> int:
>     n = len(s)
>     dp = [[0] * n for _ in range(n)]
>     for i in range(n - 1, -1, -1):
>         dp[i][i] = 1
>         for j in range(i + 1, n):
>             dp[i][j] = dp[i+1][j] + 1
>             for k in range(i + 1, j + 1):
>                 if s[k] == s[i]:
>                     dp[i][j] = min(dp[i][j],
>                                    (dp[i+1][k-1] if k > i+1 else 0) + dp[k][j])
>     return dp[0][n-1]
> ```

> [!success] Complexity
> Time O(n³), Space O(n²).

> [!tip] Alternatives
> Top-down memoization with same state.

---

## Tree DP

### Diameter of Binary Tree

> [!example] Problem
> Length of longest path between any two nodes (may not pass through root).

> [!info] Approach
> - **WHY:** The diameter through a node = depth of left subtree + depth of right subtree. Post-order DFS — each node's result depends on its children's results.
> - **WHAT:** For each node, compute depth (max path to leaf) and update global diameter.
> - **HOW:** DFS returns depth; at each node `diameter = max(diameter, left_depth + right_depth)`. Return `max(left, right) + 1`.

> [!note]- Python Solution
> ```python
> def diameterOfBinaryTree(root) -> int:
>     ans = 0
>     def depth(node) -> int:
>         nonlocal ans
>         if not node:
>             return 0
>         L, R = depth(node.left), depth(node.right)
>         ans = max(ans, L + R)
>         return max(L, R) + 1
>     depth(root)
>     return ans
> ```

> [!success] Complexity
> Time O(n), Space O(h) call stack.

> [!tip] Alternatives
> BFS-based approaches work but DFS post-order is canonical.

---

### Binary Tree Maximum Path Sum

> [!example] Problem
> Maximum sum of any path in a binary tree (path can start and end at any nodes).

> [!info] Approach
> - **WHY:** At each node, the max path through it = node.val + max(0, left_gain) + max(0, right_gain). But the recursive return must only pass one arm upward (can't fork up).
> - **WHAT:** DFS returns max single-arm gain from node upward; updates global answer with both arms.
> - **HOW:** `left_gain = max(0, dfs(left))`, `right_gain = max(0, dfs(right))`. `ans = max(ans, node.val + left_gain + right_gain)`. Return `node.val + max(left_gain, right_gain)`.

> [!note]- Python Solution
> ```python
> def maxPathSum(root) -> int:
>     ans = float('-inf')
>     def dfs(node) -> int:
>         nonlocal ans
>         if not node:
>             return 0
>         left = max(0, dfs(node.left))
>         right = max(0, dfs(node.right))
>         ans = max(ans, node.val + left + right)
>         return node.val + max(left, right)
>     dfs(root)
>     return ans
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> Iterative post-order with explicit stack — same complexity, more verbose.

---

### House Robber III

> [!example] Problem
> Rob houses in a binary tree; no two directly connected nodes. Maximize sum.

> [!info] Approach
> - **WHY:** At each node, two choices: rob it (can't rob children) or don't (can rob children). Post-order DP — decision at node depends on subtree results.
> - **WHAT:** For each node, return `(rob, skip)` = max profit with and without robbing this node.
> - **HOW:** `rob = node.val + left_skip + right_skip`; `skip = max(left_rob, left_skip) + max(right_rob, right_skip)`.

> [!note]- Python Solution
> ```python
> def rob(root) -> int:
>     def dfs(node):
>         if not node:
>             return 0, 0  # (rob, skip)
>         lr, ls = dfs(node.left)
>         rr, rs = dfs(node.right)
>         rob_node = node.val + ls + rs
>         skip_node = max(lr, ls) + max(rr, rs)
>         return rob_node, skip_node
>     return max(dfs(root))
> ```

> [!success] Complexity
> Time O(n), Space O(h).

> [!tip] Alternatives
> Memoization with a dict on node identity — same complexity, less elegant.

---

## State Machine DP

### Best Time to Buy and Sell Stock (All Variants)

> [!example] Problem I — One transaction
> Max profit with at most 1 buy-sell.

> [!note]- Python Solution
> ```python
> def maxProfit(prices: list[int]) -> int:
>     min_price, max_profit = float('inf'), 0
>     for p in prices:
>         min_price = min(min_price, p)
>         max_profit = max(max_profit, p - min_price)
>     return max_profit
> ```

> [!example] Problem II — Unlimited transactions

> [!note]- Python Solution
> ```python
> def maxProfit(prices: list[int]) -> int:
>     return sum(max(0, prices[i] - prices[i-1]) for i in range(1, len(prices)))
> ```

> [!example] Problem III — At most 2 transactions

> [!note]- Python Solution
> ```python
> def maxProfit(prices: list[int]) -> int:
>     b1 = b2 = float('-inf')
>     s1 = s2 = 0
>     for p in prices:
>         b1 = max(b1, -p)
>         s1 = max(s1, b1 + p)
>         b2 = max(b2, s1 - p)
>         s2 = max(s2, b2 + p)
>     return s2
> ```

> [!example] Problem IV — At most k transactions

> [!note]- Python Solution
> ```python
> def maxProfit(k: int, prices: list[int]) -> int:
>     n = len(prices)
>     if not prices or k == 0:
>         return 0
>     if k >= n // 2:
>         return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))
>     dp = [0] * n
>     for _ in range(k):
>         new_dp, best = [0] * n, -prices[0]
>         for i in range(1, n):
>             new_dp[i] = max(new_dp[i-1], prices[i] + best)
>             best = max(best, dp[i] - prices[i])
>         dp = new_dp
>     return dp[-1]
> ```

> [!success] Complexity
> Time O(n) for I/II/III; O(kn) for IV. Space O(1) for I/II/III; O(n) for IV.

---

### Stock with Cooldown

> [!example] Problem
> Unlimited transactions; must rest 1 day after selling.

> [!info] Approach
> - **WHY:** Three states model the constraint: holding, just sold (cooldown), resting. Transitions connect states across days.
> - **WHAT:** `held` = best profit when holding; `sold` = best on day of sell; `rest` = best when not holding and not in cooldown.
> - **HOW:** `held = max(held, rest - price)`, `sold = held + price`, `rest = max(rest, sold)`.

> [!note]- Python Solution
> ```python
> def maxProfit(prices: list[int]) -> int:
>     held, sold, rest = float('-inf'), 0, 0
>     for p in prices:
>         held, sold, rest = max(held, rest - p), held + p, max(rest, sold)
>     return max(sold, rest)
> ```

> [!success] Complexity
> Time O(n), Space O(1).

---

### Stock with Transaction Fee

> [!example] Problem
> Unlimited transactions; fixed `fee` per sell.

> [!info] Approach
> - **WHAT:** Two states: `hold` (best profit holding), `cash` (best profit not holding).
> - **HOW:** `hold = max(hold, cash - price)`, `cash = max(cash, hold + price - fee)`.

> [!note]- Python Solution
> ```python
> def maxProfit(prices: list[int], fee: int) -> int:
>     hold, cash = float('-inf'), 0
>     for p in prices:
>         hold, cash = max(hold, cash - p), max(cash, hold + p - fee)
>     return cash
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Apply fee on buy side: `cash - p - fee` when buying. Equivalent result.

---

## Bitmask / Digit DP

### Shortest Path Visiting All Nodes

> [!example] Problem
> In an undirected connected graph, find the shortest path that visits every node at least once.

> [!info] Approach
> - **WHY:** State must encode which nodes have been visited; bitmask encodes visited set in O(1) space per state. BFS on state `(mask, last_node)` finds minimum steps.
> - **WHAT:** BFS with state `(visited_mask, current_node)`. Start from all nodes simultaneously (distance 0).
> - **HOW:** Enqueue `(1 << i, i)` for each node `i`. BFS level = distance. Terminate when `mask == (1<<n)-1`.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def shortestPathLength(graph: list[list[int]]) -> int:
>     n = len(graph)
>     full = (1 << n) - 1
>     queue = deque()
>     visited = set()
>     for i in range(n):
>         state = (1 << i, i)
>         queue.append((state, 0))
>         visited.add(state)
>     while queue:
>         (mask, node), dist = queue.popleft()
>         if mask == full:
>             return dist
>         for nb in graph[node]:
>             new_mask = mask | (1 << nb)
>             if (new_mask, nb) not in visited:
>                 visited.add((new_mask, nb))
>                 queue.append(((new_mask, nb), dist + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(2^n × n²), Space O(2^n × n).

> [!tip] Alternatives
> DP with bitmask `dp[mask][node]` gives same complexity — BFS is cleaner here since it finds minimum directly.

---

### Numbers At Most N Given Digit Set

> [!example] Problem
> Count positive integers ≤ `n` whose digits come from a given sorted set `digits`.

> [!info] Approach
> - **WHY:** Digit-by-digit construction with a "tight" constraint — once a digit below the bound is placed, all subsequent digits can be anything in the set.
> - **WHAT:** Count numbers with fewer digits than `n` + count numbers with same digit count respecting the tight constraint.
> - **HOW:** For `k < len(n_str)` digits: `|digits|^k` choices. For `k == len(n_str)`: iterate digit by digit, count choices where current digit < bound digit, then check tight equality.

> [!note]- Python Solution
> ```python
> def atMostNGivenDigitSet(digits: list[str], n: int) -> int:
>     s = str(n)
>     k = len(s)
>     count = 0
>     # Numbers with fewer digits
>     for length in range(1, k):
>         count += len(digits) ** length
>     # Numbers with same number of digits
>     for i, ch in enumerate(s):
>         smaller = sum(1 for d in digits if d < ch)
>         count += smaller * (len(digits) ** (k - 1 - i))
>         if ch not in digits:
>             break
>         if i == k - 1:
>             count += 1  # n itself is valid
>     return count
> ```

> [!success] Complexity
> Time O(k × |digits|), Space O(1).

> [!tip] Alternatives
> Full digit DP with memoization on `(position, tight)` state — generalizes to more complex constraints.

---

### Super Egg Drop

> [!example] Problem
> With `k` eggs and `n` floors, find the minimum number of trials to determine the critical floor in the worst case.

> [!info] Approach
> - **WHY:** Naive DP `dp[k][n] = min over t(1 + max(dp[k-1][t-1], dp[k][n-t]))` is O(kn²). Inverted DP is O(kn log n).
> - **WHAT (inverted):** `dp[m][k]` = max floors testable in `m` moves with `k` eggs.
> - **HOW:** `dp[m][k] = dp[m-1][k-1] + dp[m-1][k] + 1`. Find minimum `m` where `dp[m][k] >= n`.

> [!note]- Python Solution
> ```python
> def superEggDrop(k: int, n: int) -> int:
>     m = 0
>     dp = [0] * (k + 1)
>     while dp[k] < n:
>         m += 1
>         new_dp = [0] * (k + 1)
>         for j in range(1, k + 1):
>             new_dp[j] = dp[j-1] + dp[j] + 1
>         dp = new_dp
>     return m
> ```

> [!success] Complexity
> Time O(k log n) — at most O(n) iterations but bounded by log n for large k. Space O(k).

> [!tip] Alternatives
> Binary search on `dp[m][k]` as a function of `m` gives O(kn log n). Direct DP with binary search on `t` gives O(kn log n).

---

## Longest Increasing Subsequence (LIS) Family

### Longest Increasing Subsequence

> [!example] Problem
> Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

> [!info] Approach
> - **WHY:** Naïve O(n²) DP checks all prior elements; patience sort uses a maintained tails array to binary-search the right position, achieving O(n log n).
> - **WHAT:** `tails[i]` = smallest tail element of all increasing subsequences of length `i+1` seen so far.
> - **HOW:** For each `x` in `nums`, binary search `tails` for the first element `>= x`. If found, replace it with `x`; otherwise append `x`. Answer = `len(tails)`.

> [!note]- Python Solution
> ```python
> import bisect
> def lengthOfLIS(nums: list[int]) -> int:
>     tails = []
>     for x in nums:
>         pos = bisect.bisect_left(tails, x)
>         if pos == len(tails):
>             tails.append(x)
>         else:
>             tails[pos] = x
>     return len(tails)
> ```

> [!success] Complexity
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> O(n²) DP: `dp[i] = max(dp[j]+1 for j<i if nums[j]<nums[i])`. To reconstruct the actual subsequence, maintain a `parent` array alongside the patience sort.

---

### Number of LIS

> [!example] Problem
> Given `nums`, return the number of longest increasing subsequences (LC 673).

> [!info] Approach
> - **WHY:** Length alone isn't enough; need to count paths. Two parallel arrays track both.
> - **WHAT:** `length[i]` = LIS length ending at index `i`. `count[i]` = number of such subsequences.
> - **HOW:** For each `i`, scan `j < i`. If `nums[j] < nums[i]`: if `length[j]+1 > length[i]`, update both; if equal, add `count[j]` to `count[i]`. Answer = sum of `count[i]` where `length[i] == max_length`.

> [!note]- Python Solution
> ```python
> def findNumberOfLIS(nums: list[int]) -> int:
>     n = len(nums)
>     length = [1] * n
>     count = [1] * n
>     for i in range(n):
>         for j in range(i):
>             if nums[j] < nums[i]:
>                 if length[j] + 1 > length[i]:
>                     length[i] = length[j] + 1
>                     count[i] = count[j]
>                 elif length[j] + 1 == length[i]:
>                     count[i] += count[j]
>     max_len = max(length)
>     return sum(c for l, c in zip(length, count) if l == max_len)
> ```

> [!success] Complexity
> Time O(n²), Space O(n).

> [!tip] Alternatives
> O(n log n) with a BIT/segment tree storing (max_length, count) pairs per compressed value.

---

### Longest Bitonic Subsequence

> [!example] Problem
> A bitonic subsequence first increases then decreases (either part may be empty). Find its maximum length.

> [!info] Approach
> - **WHY:** Decompose into LIS from the left and LIS from the right (longest decreasing = LIS reversed). The peak at index `i` contributes `lis[i] + lds[i] - 1`.
> - **WHAT:** `lis[i]` = LIS length ending at `i`; `lds[i]` = longest decreasing subsequence starting at `i`.
> - **HOW:** Compute `lis` left-to-right O(n²), `lds` right-to-left O(n²). Answer = `max(lis[i] + lds[i] - 1)`.

> [!note]- Python Solution
> ```python
> def longestBitonicSubsequence(nums: list[int]) -> int:
>     n = len(nums)
>     lis = [1] * n
>     lds = [1] * n
>     for i in range(1, n):
>         for j in range(i):
>             if nums[j] < nums[i]:
>                 lis[i] = max(lis[i], lis[j] + 1)
>     for i in range(n - 2, -1, -1):
>         for j in range(i + 1, n):
>             if nums[j] < nums[i]:
>                 lds[i] = max(lds[i], lds[j] + 1)
>     return max(lis[i] + lds[i] - 1 for i in range(n))
> ```

> [!success] Complexity
> Time O(n²), Space O(n).

> [!tip] Alternatives
> Combine with O(n log n) patience sort for each direction to reduce to O(n log n) overall.

---

## String DP

### Distinct Subsequences

> [!example] Problem
> Given strings `s` and `t`, count the number of distinct subsequences of `s` that equal `t` (LC 115).

> [!info] Approach
> - **WHY:** At each position we either use `s[i]` to match `t[j]` or we skip it; both branches must be counted.
> - **WHAT:** `dp[i][j]` = number of ways to form `t[:j]` from `s[:i]`.
> - **HOW:** If `s[i-1] == t[j-1]`: `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]` (use or skip). Else: `dp[i][j] = dp[i-1][j]`. Base: `dp[i][0] = 1` for all `i`.

> [!note]- Python Solution
> ```python
> def numDistinct(s: str, t: str) -> int:
>     m, n = len(s), len(t)
>     dp = [0] * (n + 1)
>     dp[0] = 1
>     for ch in s:
>         for j in range(n, 0, -1):
>             if ch == t[j - 1]:
>                 dp[j] += dp[j - 1]
>     return dp[n]
> ```

> [!success] Complexity
> Time O(mn), Space O(n) with 1-D rolling array.

> [!tip] Alternatives
> Full 2-D table is clearer for derivation; rolling array suffices for space optimization.

---

### Interleaving String

> [!example] Problem
> Given `s1`, `s2`, `s3`, return true if `s3` is formed by an interleaving of `s1` and `s2` (LC 97).

> [!info] Approach
> - **WHY:** At each position in `s3` we choose whether the next character comes from `s1` or `s2`; overlapping subproblems arise.
> - **WHAT:** `dp[i][j]` = true if `s3[:i+j]` can be formed from `s1[:i]` and `s2[:j]`.
> - **HOW:** `dp[i][j] = (dp[i-1][j] and s1[i-1]==s3[i+j-1]) or (dp[i][j-1] and s2[j-1]==s3[i+j-1])`. Base: `dp[0][0] = True`.

> [!note]- Python Solution
> ```python
> def isInterleave(s1: str, s2: str, s3: str) -> bool:
>     m, n = len(s1), len(s2)
>     if m + n != len(s3):
>         return False
>     dp = [False] * (n + 1)
>     dp[0] = True
>     for j in range(1, n + 1):
>         dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
>     for i in range(1, m + 1):
>         dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
>         for j in range(1, n + 1):
>             dp[j] = (dp[j] and s1[i-1] == s3[i+j-1]) or \
>                     (dp[j-1] and s2[j-1] == s3[i+j-1])
>     return dp[n]
> ```

> [!success] Complexity
> Time O(mn), Space O(n).

> [!tip] Alternatives
> BFS/DFS with memoization on `(i, j)` state is equivalent and sometimes clearer.

---

### Regular Expression Matching

> [!example] Problem
> Implement regex matching with `.` (any single char) and `*` (zero or more of preceding element) (LC 10).

> [!info] Approach
> - **WHY:** `*` introduces branching — match zero occurrences (skip pattern pair) or one-or-more — creating overlapping sub-problems.
> - **WHAT:** `dp[i][j]` = true if `s[:i]` matches `p[:j]`.
> - **HOW:** If `p[j-1] == '*'`: `dp[i][j] = dp[i][j-2]` (zero uses) or `(dp[i-1][j] and (p[j-2]=='.' or p[j-2]==s[i-1]))` (one+ uses). Else: `dp[i][j] = dp[i-1][j-1] and (p[j-1]=='.' or p[j-1]==s[i-1])`.

> [!note]- Python Solution
> ```python
> def isMatch(s: str, p: str) -> bool:
>     m, n = len(s), len(p)
>     dp = [[False] * (n + 1) for _ in range(m + 1)]
>     dp[0][0] = True
>     for j in range(2, n + 1):
>         if p[j - 1] == '*':
>             dp[0][j] = dp[0][j - 2]
>     for i in range(1, m + 1):
>         for j in range(1, n + 1):
>             if p[j - 1] == '*':
>                 dp[i][j] = dp[i][j - 2] or \
>                     (dp[i - 1][j] and p[j - 2] in {'.', s[i - 1]})
>             else:
>                 dp[i][j] = dp[i - 1][j - 1] and p[j - 1] in {'.', s[i - 1]}
>     return dp[m][n]
> ```

> [!success] Complexity
> Time O(mn), Space O(mn); reducible to O(n) with two rows.

> [!tip] Alternatives
> LC 44 (Wildcard Matching) replaces `*` semantics — similar structure but `*` matches any sequence directly.

---

## Probability / Expected Value DP

### Knight Probability in Chessboard

> [!example] Problem
> A knight starts at `(r, c)` on an `n×n` board. After `k` moves, return the probability it stays on the board (LC 688).

> [!info] Approach
> - **WHY:** After each move, probability distributes over up to 8 neighbours; cells off-board contribute 0. Iterating forward avoids recomputing overlapping sums.
> - **WHAT:** `dp[i][j]` = probability of being at `(i, j)` after the current step.
> - **HOW:** Start with probability 1 at `(r, c)`. Each step: new `dp[ni][nj] += dp[i][j] / 8` for each valid knight move. Repeat `k` times; answer = `sum(dp)`.

> [!note]- Python Solution
> ```python
> def knightProbability(n: int, k: int, row: int, column: int) -> float:
>     moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
>     dp = [[0.0] * n for _ in range(n)]
>     dp[row][column] = 1.0
>     for _ in range(k):
>         ndp = [[0.0] * n for _ in range(n)]
>         for i in range(n):
>             for j in range(n):
>                 if dp[i][j]:
>                     for di, dj in moves:
>                         ni, nj = i + di, j + dj
>                         if 0 <= ni < n and 0 <= nj < n:
>                             ndp[ni][nj] += dp[i][j] / 8
>         dp = ndp
>     return sum(dp[i][j] for i in range(n) for j in range(n))
> ```

> [!success] Complexity
> Time O(k · n²), Space O(n²).

> [!tip] Alternatives
> Memoized recursion `prob(step, i, j)` is equivalent; forward DP avoids redundant division.

---

### New 21 Game

> [!example] Problem
> Start at 0 points. Each turn draw a number in `[1, maxPts]` uniformly at random and add it. Stop once reaching `>= k`. Return probability the final score is `<= n` (LC 837).

> [!info] Approach
> - **WHY:** `dp[x]` = probability of reaching exactly `x` before stopping. Each `dp[x]` is the average of `dp[x-1], ..., dp[x-maxPts]` (for `x < k`). A sliding window sum avoids O(n·maxPts) recomputation.
> - **WHAT:** `dp[x]` = probability of landing on score `x`.
> - **HOW:** Base `dp[0] = 1`. Maintain `window_sum`. For `x` in `1..n`: `dp[x] = window_sum / maxPts`. If `x < k`, add `dp[x]` to window; if `x >= maxPts`, subtract `dp[x - maxPts]`. Answer = `sum(dp[k..n])`.

> [!note]- Python Solution
> ```python
> def new21Game(n: int, k: int, maxPts: int) -> float:
>     if k == 0 or n >= k + maxPts:
>         return 1.0
>     dp = [0.0] * (n + 1)
>     dp[0] = 1.0
>     window_sum = 1.0
>     for x in range(1, n + 1):
>         dp[x] = window_sum / maxPts
>         if x < k:
>             window_sum += dp[x]
>         if x >= maxPts:
>             window_sum -= dp[x - maxPts]
>     return sum(dp[k:])
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> Brute-force convolution is O(n · maxPts); the prefix-sum trick reduces it to O(n).

---

## Bitmask DP

### Shortest Path Visiting All Nodes (TSP Bitmask DP)

> [!example] Problem
> Find the shortest path that visits every node in an undirected graph (LC 847). Generalises to the Travelling Salesman bitmask DP template.

> [!info] Approach
> - **WHY:** With up to 12 nodes, 2^12 states × 12 nodes is feasible. BFS on `(node, visited_mask)` gives shortest path; DP on the same state gives minimum cost for weighted TSP.
> - **WHAT:** `dist[mask][v]` = min steps to have visited exactly the nodes in `mask` and currently be at `v`.
> - **HOW:** BFS (unweighted): enqueue all `(node, 1<<node)` with distance 0. Expand neighbours; stop when `mask == (1<<n)-1`. For weighted TSP: `dp[mask | (1<<u)][u] = min(dp[mask][v] + w(v,u))` over all `v` in `mask`.

> [!note]- Python Solution
> ```python
> from collections import deque
> def shortestPathLength(graph: list[list[int]]) -> int:
>     n = len(graph)
>     full = (1 << n) - 1
>     dist = [[float('inf')] * n for _ in range(1 << n)]
>     q = deque()
>     for i in range(n):
>         dist[1 << i][i] = 0
>         q.append((1 << i, i))
>     while q:
>         mask, v = q.popleft()
>         if mask == full:
>             return dist[mask][v]
>         for u in graph[v]:
>             nmask = mask | (1 << u)
>             if dist[nmask][u] == float('inf'):
>                 dist[nmask][u] = dist[mask][v] + 1
>                 q.append((nmask, u))
>     return 0
> ```

> [!success] Complexity
> Time O(2^n · n), Space O(2^n · n).

> [!tip] Alternatives
> For weighted complete graphs (classic TSP): same DP, O(2^n · n²). Prim's/Kruskal's gives MST (not TSP) — use bitmask DP when visiting-all-nodes with revisits is the goal.

---

### Partition to K Equal Subset Sums

> [!example] Problem
> Given `nums` and integer `k`, return true if the array can be partitioned into `k` subsets each with equal sum (LC 698).

> [!info] Approach
> - **WHY:** Subset assignment is NP-hard in general but `n ≤ 16` makes 2^n bitmask DP feasible.
> - **WHAT:** `dp[mask]` = true if the elements indicated by `mask` can be perfectly distributed into some number of full buckets.
> - **HOW:** `target = total / k`. Iterate all masks in order. For each set mask, compute `current_sum = sum of selected elements % target`. Try adding each unselected element; if it fits, `dp[mask | (1<<i)] = True`. Answer = `dp[(1<<n)-1]`.

> [!note]- Python Solution
> ```python
> def canPartitionKSubsets(nums: list[int], k: int) -> bool:
>     total = sum(nums)
>     if total % k:
>         return False
>     target = total // k
>     nums.sort(reverse=True)
>     if nums[0] > target:
>         return False
>     n = len(nums)
>     dp = [False] * (1 << n)
>     dp[0] = True
>     current_sum = [0] * (1 << n)
>     for mask in range(1 << n):
>         if not dp[mask]:
>             continue
>         for i in range(n):
>             if mask & (1 << i):
>                 continue
>             next_mask = mask | (1 << i)
>             if current_sum[mask] + nums[i] <= target:
>                 current_sum[next_mask] = (current_sum[mask] + nums[i]) % target
>                 dp[next_mask] = True
>     return dp[(1 << n) - 1]
> ```

> [!success] Complexity
> Time O(2^n · n), Space O(2^n).

> [!tip] Alternatives
> Backtracking with pruning often faster in practice. Bitmask DP guarantees polynomial in 2^n so preferred when n ≤ 20.

---

## Digit DP

### Count Numbers with Unique Digits

> [!example] Problem
> Given `n`, count numbers in `[0, 10^n)` with all unique digits (LC 357).

> [!info] Approach
> - **WHY:** At each digit position, choices depend only on how many distinct digits have been used — classic digit DP structure.
> - **WHAT:** `dp[i]` = count of valid `i`-digit numbers (no leading zeros counted separately).
> - **HOW:** `dp[0] = 1`. For length `i`: first digit has 9 choices (1–9); each subsequent digit has `10 - (i-1)` choices (avoid used). `dp[i] = 9 * 9 * 8 * ... * (10-i+1)`. Accumulate sum.

> [!note]- Python Solution
> ```python
> def countNumbersWithUniqueDigits(n: int) -> int:
>     if n == 0:
>         return 1
>     res, unique = 10, 9
>     available = 9
>     for _ in range(n - 1):
>         unique *= available
>         res += unique
>         available -= 1
>     return res
> ```

> [!success] Complexity
> Time O(n), Space O(1). (n ≤ 10 by constraint so effectively O(1).)

> [!tip] Alternatives
> General digit DP template below handles arbitrary digit constraints for larger ranges.

---

### Digit DP Template

> [!example] Problem
> Count integers in `[1, n]` satisfying an arbitrary digit constraint (e.g., digit sum divisible by `k`, no two adjacent equal digits). General template with tight/free flag.

> [!info] Approach
> - **WHY:** Digit-by-digit construction with a `tight` flag tracks whether we are still bounded by `n`'s prefix, enabling safe enumeration without brute force.
> - **WHAT:** State = `(position, constraint_state, tight, started)`. `tight=True` means all digits chosen so far match `n`'s prefix exactly.
> - **HOW:** At each position, iterate digit 0–9 (or 0–`n[pos]` if tight). Recurse; memoize on `(pos, state, tight, started)`. Base case: `pos == len(digits)` — check if constraint satisfied.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
>
> def digitDP(n: int, k: int) -> int:
>     """Count integers in [1, n] whose digit sum % k == 0."""
>     digits = list(map(int, str(n)))
>     L = len(digits)
>
>     @lru_cache(maxsize=None)
>     def dp(pos: int, remainder: int, tight: bool, started: bool) -> int:
>         if pos == L:
>             return int(started and remainder == 0)
>         limit = digits[pos] if tight else 9
>         result = 0
>         for d in range(0, limit + 1):
>             new_started = started or d > 0
>             new_rem = (remainder + d) % k if new_started else 0
>             result += dp(pos + 1, new_rem, tight and d == limit, new_started)
>         return result
>
>     return dp(0, 0, True, False)
> ```

> [!success] Complexity
> Time O(L · S · 2 · 2 · 10) where S = number of constraint states, L = digits in n. Effectively O(L · S).

> [!tip] Alternatives
> Iterative digit DP with explicit tables avoids recursion overhead. For constraints on digit counts/patterns, expand the state accordingly.

---

## Game Theory DP

### Stone Game

> [!example] Problem
> Alice and Bob alternately take stones from either end of a row of piles. Both play optimally; Alice goes first. Return true if Alice wins (LC 877).

> [!info] Approach
> - **WHY:** Each player maximises their own score minus the opponent's; the decision at each subarray depends on what the opponent will optimally do.
> - **WHAT:** `dp[i][j]` = maximum score difference (current player − other player) achievable on subarray `piles[i..j]`.
> - **HOW:** `dp[i][j] = max(piles[i] - dp[i+1][j], piles[j] - dp[i][j-1])`. Base: `dp[i][i] = piles[i]`. Alice wins iff `dp[0][n-1] > 0`.

> [!note]- Python Solution
> ```python
> def stoneGame(piles: list[int]) -> bool:
>     n = len(piles)
>     dp = piles[:]
>     for length in range(2, n + 1):
>         for i in range(n - length + 1):
>             j = i + length - 1
>             dp[i] = max(piles[i] - dp[i + 1], piles[j] - dp[i])
>             # reusing 1-D; careful index mapping needed for full 2-D
>     # Full 2-D version is clearer:
>     dp2 = [[0] * n for _ in range(n)]
>     for i in range(n):
>         dp2[i][i] = piles[i]
>     for length in range(2, n + 1):
>         for i in range(n - length + 1):
>             j = i + length - 1
>             dp2[i][j] = max(piles[i] - dp2[i+1][j], piles[j] - dp2[i][j-1])
>     return dp2[0][n - 1] > 0
> ```

> [!success] Complexity
> Time O(n²), Space O(n²); reducible to O(n) with rolling array.

> [!tip] Alternatives
> LC 877 Alice always wins (mathematical proof: take all even or all odd piles). The DP generalises to arbitrary pile values and variants like Stone Game II.

---

### Stone Game II

> [!example] Problem
> Players can take `1..2M` piles from the front; `M` updates to `max(M, X)` after taking `X`. Maximise stones for Alice (LC 1140).

> [!info] Approach
> - **WHY:** The value of `M` changes each turn, so state must encode both position and current `M`.
> - **WHAT:** `dp[i][m]` = max stones the current player can get from `piles[i:]` with current multiplier `m`.
> - **HOW:** Precompute suffix sums. `dp[i][m] = suffix[i] - min(dp[i+x][max(m,x)] for x in 1..2m)` — the current player takes whatever minimises the opponent's haul. Fill right-to-left.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
> def stoneGameII(piles: list[int]) -> int:
>     n = len(piles)
>     suffix = [0] * (n + 1)
>     for i in range(n - 1, -1, -1):
>         suffix[i] = suffix[i + 1] + piles[i]
>
>     @lru_cache(maxsize=None)
>     def dp(i: int, m: int) -> int:
>         if i + 2 * m >= n:
>             return suffix[i]
>         return suffix[i] - min(dp(i + x, max(m, x)) for x in range(1, 2 * m + 1))
>
>     return dp(0, 1)
> ```

> [!success] Complexity
> Time O(n² log n) amortised, Space O(n²) for memo.

> [!tip] Alternatives
> Bottom-up DP iterating `i` from right and `m` from large to small avoids recursion.

---

### Predict the Winner

> [!example] Problem
> Two players pick from either end of `nums`. Return true if Player 1 can win or tie (LC 486).

> [!info] Approach
> - **WHY:** Identical structure to Stone Game. `dp[i][j]` = score advantage of the current player over the opponent on subarray `nums[i..j]`.
> - **WHAT:** `dp[i][j]` = max(nums[i] − dp[i+1][j], nums[j] − dp[i][j−1]).
> - **HOW:** Fill by increasing subarray length. Player 1 wins iff `dp[0][n-1] >= 0`.

> [!note]- Python Solution
> ```python
> def predictTheWinner(nums: list[int]) -> bool:
>     n = len(nums)
>     dp = [[0] * n for _ in range(n)]
>     for i in range(n):
>         dp[i][i] = nums[i]
>     for length in range(2, n + 1):
>         for i in range(n - length + 1):
>             j = i + length - 1
>             dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])
>     return dp[0][n - 1] >= 0
> ```

> [!success] Complexity
> Time O(n²), Space O(n²); 1-D rolling possible.

> [!tip] Alternatives
> Minimax with memoization is equivalent. Note: Player 1 always wins when `n` is odd (same parity argument as Stone Game).

---

## DP on Sequences

### Jump Game II

> [!example] Problem
> Given `nums` where `nums[i]` is max jump length from index `i`, return the minimum number of jumps to reach the last index (LC 45).

> [!info] Approach
> - **WHY:** Greedy DP: at each jump, greedily extend to the farthest reachable index. Counting jumps only when forced to jump.
> - **WHAT:** Track `current_end` (end of current jump range) and `farthest` (max reachable from within range).
> - **HOW:** Iterate; update `farthest = max(farthest, i + nums[i])`. When `i == current_end` and not at last index: increment jumps, set `current_end = farthest`.

> [!note]- Python Solution
> ```python
> def jump(nums: list[int]) -> int:
>     jumps = current_end = farthest = 0
>     for i in range(len(nums) - 1):
>         farthest = max(farthest, i + nums[i])
>         if i == current_end:
>             jumps += 1
>             current_end = farthest
>     return jumps
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> O(n) DP: `dp[i] = min jumps to reach i`; update via `dp[j] = min(dp[j], dp[i]+1)` for `j` in `[i+1, i+nums[i]]`. Greedy is simpler and equivalent.

---

### Maximum Product Subarray

> [!example] Problem
> Find the contiguous subarray with the largest product (LC 152).

> [!info] Approach
> - **WHY:** A negative number flips max↔min, so both must be tracked at each position.
> - **WHAT:** `max_prod` and `min_prod` ending at index `i`.
> - **HOW:** At each element `x`: `max_prod, min_prod = max(x, max_prod*x, min_prod*x), min(x, max_prod*x, min_prod*x)`. Update global answer with `max_prod`.

> [!note]- Python Solution
> ```python
> def maxProduct(nums: list[int]) -> int:
>     max_p = min_p = res = nums[0]
>     for x in nums[1:]:
>         candidates = (x, max_p * x, min_p * x)
>         max_p, min_p = max(candidates), min(candidates)
>         res = max(res, max_p)
>     return res
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Prefix product with reset at zeros; or observe the answer is always a prefix or suffix product between zeros.

---

### Arithmetic Slices II — Subsequence

> [!example] Problem
> Count the number of arithmetic subsequences (length ≥ 3) in `nums` (LC 446).

> [!info] Approach
> - **WHY:** Unlike subarrays, subsequences can skip elements; tracking every possible common difference per ending index is necessary.
> - **WHAT:** `dp[i]` is a dict mapping common difference `d` → count of **weak** arithmetic subsequences (length ≥ 2) ending at index `i` with difference `d`.
> - **HOW:** For each pair `(j, i)` with `j < i`, `d = nums[i] - nums[j]`: `dp[i][d] += dp[j].get(d, 0) + 1`. The `+1` starts a new weak subsequence `(j,i)`. Each existing weak subseq extended to length ≥ 3 contributes `dp[j][d]` to the answer.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> def numberOfArithmeticSlices(nums: list[int]) -> int:
>     n = len(nums)
>     dp = [defaultdict(int) for _ in range(n)]
>     ans = 0
>     for i in range(n):
>         for j in range(i):
>             d = nums[i] - nums[j]
>             cnt = dp[j][d]
>             ans += cnt
>             dp[i][d] += cnt + 1
>     return ans
> ```

> [!success] Complexity
> Time O(n²), Space O(n²) in the worst case (all distinct differences).

> [!tip] Alternatives
> No known sub-quadratic solution for the general case. For subarrays (contiguous), O(n) is achievable.

---

## See Also

[[recursion]] | [[greedy]] | [[graph-algorithms]] | [[tree]] | [[string-algorithms]]
### Longest Common Substring

> [!example] Problem
> Find the length of the longest common contiguous substring shared by two strings.

> [!info] Approach
> - **WHY:** Unlike LCS, contiguity matters. A mismatch breaks the chain, so the DP state must reset to zero on mismatch.
> - **WHAT:** `dp[i][j]` is the length of the longest common substring ending at `s1[i-1]` and `s2[j-1]`.
> - **HOW:** If characters match, extend the diagonal: `dp[i][j] = dp[i-1][j-1] + 1`; else `dp[i][j] = 0`. Track the global maximum.

> [!note]- Python Solution
> ```python
> def longest_common_substring(s1: str, s2: str) -> int:
>     m, n = len(s1), len(s2)
>     prev = [0] * (n + 1)
>     best = 0
>     for i in range(1, m + 1):
>         cur = [0] * (n + 1)
>         for j in range(1, n + 1):
>             if s1[i - 1] == s2[j - 1]:
>                 cur[j] = prev[j - 1] + 1
>                 best = max(best, cur[j])
>         prev = cur
>     return best
> ```

> [!success] Complexity
> O(mn) time, O(n) space with row compression.

> [!tip] Alternatives
> Suffix automaton or suffix array can solve richer substring problems faster, but DP is the clean interview answer.
