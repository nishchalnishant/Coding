---
tags: [coding, algorithms, dynamic-programming]
topic: Dynamic Programming
difficulty: mixed
---

# Dynamic Programming — Amazon SDE-2

Use DP when the same subproblem reappears and the best overall answer is built from best sub-answers. Write the recurrence first, set base cases, fill the table in dependency order, then shrink space if you only need the last row or two.

**Memoization vs tabulation:** memoization = top-down recursion + cache (easier to write, handles sparse states); tabulation = bottom-up iterative (better constant, easier space optimization). Either is fine in interviews — state which you're using.

**Space optimization (rolling array):** when `dp[i]` only depends on `dp[i-1]` (or `dp[i-1][*]`), collapse to two variables or two rows.

---

## 1D DP

### Climbing Stairs

> [!example] Problem
> You can climb 1 or 2 steps at a time. How many distinct ways to reach step n?
>
> ```
> Input: n = 3 → Output: 3
> ```

> [!info] Approach
> `dp[i] = dp[i-1] + dp[i-2]` — Fibonacci. Space collapses to two variables.

> [!note]- Python Solution
> ```python
> def climb_stairs(n):
>     if n <= 2:
>         return n
>     two_back, one_back = 1, 2
>     for _ in range(3, n + 1):
>         two_back, one_back = one_back, two_back + one_back
>     return one_back
> ```

> [!success] Complexity
> O(n) time, O(1) space.

---

### House Robber

> [!example] Problem
> Rob houses without triggering adjacent alarms. Maximize money.
>
> ```
> Input: nums = [2,7,9,3,1] → Output: 12
> ```

> [!info] Approach
> `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`. Space: two variables.

> [!note]- Python Solution
> ```python
> def rob(nums):
>     two_back, one_back = 0, 0
>     for n in nums:
>         two_back, one_back = one_back, max(one_back, two_back + n)
>     return one_back
> ```

> [!success] Complexity
> O(n) time, O(1) space.

---

### House Robber II (Circular)

> [!example] Problem
> Houses in a circle — first and last are adjacent.
>
> ```
> Input: nums = [2,3,2] → Output: 3
> ```

> [!info] Approach
> Houses 0 and n-1 can't both be robbed. Run linear House Robber twice: `max(rob(0..n-2), rob(1..n-1))`.

> [!note]- Python Solution
> ```python
> def rob(nums):
>     def rob_linear(houses):
>         two_back, one_back = 0, 0
>         for h in houses:
>             two_back, one_back = one_back, max(one_back, two_back + h)
>         return one_back
>     if len(nums) == 1:
>         return nums[0]
>     return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
> ```

> [!success] Complexity
> O(n) time, O(1) space.

---

### Maximum Subarray (Kadane's)

> [!example] Problem
> Find the subarray with the largest sum.
>
> ```
> Input: nums = [-2,1,-3,4,-1,2,1,-5,4] → Output: 6
> ```

> [!info] Approach
> `dp[i] = max(nums[i], dp[i-1] + nums[i])` — either restart or extend. One variable.

> [!note]- Python Solution
> ```python
> def max_sub_array(nums):
>     best = curr = nums[0]
>     for x in nums[1:]:
>         curr = max(x, curr + x)
>         best = max(best, curr)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space.

---

### Coin Change (Min Coins)

> [!example] Problem
> Fewest coins to make amount. Coins are reusable (unbounded knapsack).
>
> ```
> Input: coins = [1,2,5], amount = 11 → Output: 3
> ```

> [!info] Approach
> `dp[i] = min(dp[i-c] + 1)` for each coin `c ≤ i`. Forward sweep allows reuse. Base: `dp[0]=0`, rest `inf`.

> [!note]- Python Solution
> ```python
> def coin_change(coins, amount):
>     dp = [float('inf')] * (amount + 1)
>     dp[0] = 0
>     for i in range(1, amount + 1):
>         for c in coins:
>             if c <= i:
>                 dp[i] = min(dp[i], dp[i - c] + 1)
>     return dp[amount] if dp[amount] != float('inf') else -1
> ```

> [!success] Complexity
> O(amount × |coins|) time, O(amount) space.

---

### Coin Change II (Total Ways)

> [!example] Problem
> Count combinations (not permutations) that make amount.
>
> ```
> Input: amount = 5, coins = [1,2,5] → Output: 4
> ```

> [!info] Approach
> Outer loop over coins, inner forward sweep. This ensures [1,2] and [2,1] count as the same combination.

> [!note]- Python Solution
> ```python
> def change(amount, coins):
>     dp = [0] * (amount + 1)
>     dp[0] = 1
>     for c in coins:
>         for i in range(c, amount + 1):
>             dp[i] += dp[i - c]
>     return dp[amount]
> ```

> [!success] Complexity
> O(amount × |coins|) time, O(amount) space.

> [!tip] Alternatives
> Swapping loop order counts permutations (ordered sequences) — different problem.

---

### Longest Increasing Subsequence (LIS)

> [!example] Problem
> Length of the longest strictly increasing subsequence.
>
> ```
> Input: nums = [10,9,2,5,3,7,101,18] → Output: 4
> ```

> [!info] Approach
> O(n²) DP: `dp[i] = max(dp[j]+1 for j<i if nums[j]<nums[i])`. O(n log n) patience sort: maintain `tails[]` where `tails[i]` = smallest tail of all increasing subsequences of length `i+1`. Binary search `tails` for each element.

> [!note]- Python Solution
> ```python
> import bisect
> def length_of_lis(nums):
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
> O(n log n) time, O(n) space.

---

### Word Break

> [!example] Problem
> Can s be segmented into dictionary words?
>
> ```
> Input: s = "leetcode", wordDict = ["leet","code"] → Output: true
> ```

> [!info] Approach
> `dp[i] = True if s[0..i-1]` is breakable. `dp[i] = any(dp[j] and s[j:i] in word_set)` for `j in [i-max_len, i)`. Base: `dp[0]=True`.

> [!note]- Python Solution
> ```python
> def word_break(s, wordDict):
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
> O(n × max_word_len) time, O(n) space.

---

### Decode Ways

> [!example] Problem
> Count decodings of a digit string where 1→A, 2→B, ..., 26→Z.
>
> ```
> Input: s = "226" → Output: 3
> ```

> [!info] Approach
> `dp[i]` = number of decodings of `s[0..i-1]`. Add `dp[i-1]` if `s[i-1] != '0'`; add `dp[i-2]` if `10 ≤ s[i-2:i] ≤ 26`.

> [!note]- Python Solution
> ```python
> def num_decodings(s):
>     two_back, one_back = 1, 0 if s[0] == '0' else 1
>     for i in range(2, len(s) + 1):
>         curr = 0
>         if s[i-1] != '0':
>             curr += one_back
>         if 10 <= int(s[i-2:i]) <= 26:
>             curr += two_back
>         two_back, one_back = one_back, curr
>     return one_back
> ```

> [!success] Complexity
> O(n) time, O(1) space.

---

## 0/1 Knapsack

### Partition Equal Subset Sum

> [!example] Problem
> Can nums be split into two subsets with equal sum?
>
> ```
> Input: nums = [1,5,11,5] → Output: true (subsets [1,5,5] and [11])
> ```

> [!info] Approach
> Equal partition iff one subset sums to `total/2`. 0/1 knapsack: `dp[j] |= dp[j-x]` iterating `j` from `target` down to `x` (reverse sweep prevents reuse).

> [!note]- Python Solution
> ```python
> def can_partition(nums):
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
> O(n × sum) time, O(sum) space.

> [!tip] Key pattern
> Reverse sweep (high→low) = 0/1 knapsack (each item used at most once). Forward sweep (low→high) = unbounded knapsack (items reusable).

---

### Target Sum

> [!example] Problem
> Assign + or - to each element. Count expressions that evaluate to target.
>
> ```
> Input: nums = [1,1,1,1,1], target = 3 → Output: 5
> ```

> [!info] Approach
> DP reduction: let P = sum of elements assigned +. P - N = target, P + N = total → P = (target + total) / 2. Count subsets summing to P using 0/1 knapsack.

> [!note]- Python Solution
> ```python
> def find_target_sum_ways(nums, target):
>     total = sum(nums)
>     if (target + total) % 2 or abs(target) > total:
>         return 0
>     s = (target + total) // 2
>     dp = [0] * (s + 1)
>     dp[0] = 1
>     for x in nums:
>         for j in range(s, x - 1, -1):
>             dp[j] += dp[j - x]
>     return dp[s]
> ```

> [!success] Complexity
> O(n × S) time, O(S) space where S = (target + total) / 2.

---

## 2D DP

### Longest Common Subsequence (LCS)

> [!example] Problem
> Length of longest common subsequence of two strings.
>
> ```
> Input: text1 = "abcde", text2 = "ace" → Output: 3
> ```

> [!info] Approach
> `dp[i][j]` = LCS of `s1[0..i-1]` and `s2[0..j-1]`. If chars match: `dp[i-1][j-1]+1`; else `max(dp[i-1][j], dp[i][j-1])`. Roll to one row.

> [!note]- Python Solution
> ```python
> def longest_common_subsequence(text1, text2):
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
> O(m×n) time, O(min(m,n)) space.

---

### Edit Distance

> [!example] Problem
> Minimum operations (insert, delete, replace) to convert word1 to word2.
>
> ```
> Input: word1 = "horse", word2 = "ros" → Output: 3
> ```

> [!info] Approach
> `dp[i][j]` = edit distance for `word1[0..i-1]` and `word2[0..j-1]`. If match: `dp[i-1][j-1]`; else `1 + min(replace, delete, insert)`. Base: `dp[i][0]=i`, `dp[0][j]=j`.

> [!note]- Python Solution
> ```python
> def min_distance(word1, word2):
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
> O(m×n) time, O(min(m,n)) space.

---

### Unique Paths

> [!example] Problem
> Count paths from top-left to bottom-right of an m×n grid (only right or down moves).
>
> ```
> Input: m = 3, n = 7 → Output: 28
> ```

> [!info] Approach
> `dp[j] += dp[j-1]` per row (rolling 1D). Base: all 1s.

> [!note]- Python Solution
> ```python
> def unique_paths(m, n):
>     dp = [1] * n
>     for _ in range(1, m):
>         for j in range(1, n):
>             dp[j] += dp[j-1]
>     return dp[n-1]
> ```

> [!success] Complexity
> O(m×n) time, O(n) space. Combinatorics shortcut: `math.comb(m+n-2, m-1)`.

---

### Unique Paths II (With Obstacles)

> [!example] Problem
> Same as Unique Paths but obstacle cells block paths.
>
> ```
> Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]] → Output: 2
> ```

> [!info] Approach
> Same rolling DP; set `dp[j]=0` when `obstacleGrid[i][j]==1`.

> [!note]- Python Solution
> ```python
> def unique_paths_with_obstacles(obstacleGrid):
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
> O(m×n) time, O(n) space.

---

### Minimum Path Sum

> [!example] Problem
> Find path from top-left to bottom-right minimizing sum (right/down only).
>
> ```
> Input: grid = [[1,3,1],[1,5,1],[4,2,1]] → Output: 7
> ```

> [!info] Approach
> `dp[j] = grid[i][j] + min(dp[j], dp[j-1])`. Initialize first row as prefix sums.

> [!note]- Python Solution
> ```python
> def min_path_sum(grid):
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
> O(m×n) time, O(n) space.

---

### Maximal Square

> [!example] Problem
> Largest square containing only 1s in a binary matrix. Return its area.
>
> ```
> Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],...] → Output: 4
> ```

> [!info] Approach
> `dp[i][j]` = side of largest all-1s square with bottom-right at `(i,j)`. If `matrix[i][j]=='1'`: `min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1`.

> [!note]- Python Solution
> ```python
> def maximal_square(matrix):
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
> O(m×n) time, O(m×n) space → reducible to O(n).

---

## Stock Problems

### Best Time to Buy and Sell Stock (I–IV + Cooldown + Fee)

> One transaction (I): track running min price; `max_profit = max(price - min_price)`. O(n), O(1).
>
> Unlimited transactions (II): sum all positive daily differences. O(n), O(1).
>
> At most 2 transactions (III): four variables `b1, s1, b2, s2`; update in one pass. O(n), O(1).
>
> At most k transactions (IV): O(kn) DP; if `k >= n//2` reduce to unlimited. O(kn), O(n).
>
> With cooldown: three states — `held`, `sold`, `rest`. O(n), O(1).
>
> With fee: two states — `hold`, `cash`. O(n), O(1).

> [!note]- Python Solutions
> ```python
> # I: one transaction
> def max_profit_i(prices):
>     min_price, best = float('inf'), 0
>     for p in prices:
>         min_price = min(min_price, p)
>         best = max(best, p - min_price)
>     return best
>
> # II: unlimited
> def max_profit_ii(prices):
>     return sum(max(0, prices[i] - prices[i-1]) for i in range(1, len(prices)))
>
> # III: at most 2
> def max_profit_iii(prices):
>     b1 = b2 = float('-inf')
>     s1 = s2 = 0
>     for p in prices:
>         b1 = max(b1, -p); s1 = max(s1, b1 + p)
>         b2 = max(b2, s1 - p); s2 = max(s2, b2 + p)
>     return s2
>
> # Cooldown
> def max_profit_cooldown(prices):
>     held, sold, rest = float('-inf'), 0, 0
>     for p in prices:
>         held, sold, rest = max(held, rest - p), held + p, max(rest, sold)
>     return max(sold, rest)
>
> # With fee
> def max_profit_fee(prices, fee):
>     hold, cash = float('-inf'), 0
>     for p in prices:
>         hold, cash = max(hold, cash - p), max(cash, hold + p - fee)
>     return cash
> ```

---

## LCS Family

### Longest Palindromic Subsequence

> [!example] Problem
> Length of longest palindromic subsequence in s.
>
> ```
> Input: s = "bbbab" → Output: 4
> ```

> [!info] Approach
> `LPS(s) = LCS(s, s[::-1])`. Or interval DP: if `s[i]==s[j]`: `dp[i][j] = dp[i+1][j-1]+2`; else `max(dp[i+1][j], dp[i][j-1])`.

> [!note]- Python Solution
> ```python
> def longest_palindrome_subseq(s):
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
> O(n²) time, O(n²) space.

---

### Distinct Subsequences

> [!example] Problem
> Count distinct subsequences of s that equal t.
>
> ```
> Input: s = "rabbbit", t = "rabbit" → Output: 3
> ```

> [!info] Approach
> `dp[j]` = ways to form `t[:j]` from s seen so far. If `ch == t[j-1]`: `dp[j] += dp[j-1]`. Reverse sweep (0/1 — each s char used once).

> [!note]- Python Solution
> ```python
> def num_distinct(s, t):
>     dp = [0] * (len(t) + 1)
>     dp[0] = 1
>     for ch in s:
>         for j in range(len(t), 0, -1):
>             if ch == t[j - 1]:
>                 dp[j] += dp[j - 1]
>     return dp[len(t)]
> ```

> [!success] Complexity
> O(mn) time, O(n) space.

---

### Interleaving String

> [!example] Problem
> Is s3 formed by interleaving s1 and s2?
>
> ```
> Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac" → Output: true
> ```

> [!info] Approach
> `dp[j]` = whether `s3[:i+j]` can be formed from `s1[:i]` and `s2[:j]`. Update rolling row.

> [!note]- Python Solution
> ```python
> def is_interleave(s1, s2, s3):
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
> O(mn) time, O(n) space.

---

## Grid DP

### Minimum Path Sum (covered above)

### Burst Balloons (interval DP — awareness)

> O(n³) interval DP. `dp[left][right]` = max coins from bursting all balloons strictly between `left` and `right`. Trick: think "last balloon to burst" in the interval — it sees its boundary neighbors `nums[left]` and `nums[right]` intact. Pad with 1s at both ends. Not commonly asked at SDE-2 but appears occasionally.

---

## See Also

[[backtracking]] | [[graph-algorithms]] | [[greedy]]
