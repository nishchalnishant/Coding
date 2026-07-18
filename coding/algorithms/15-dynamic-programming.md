---
tags: [coding, algorithms, dynamic-programming]
topic: Dynamic Programming
difficulty: mixed
---

# Dynamic Programming — Problem Reference by Pattern

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.


> [!info] First Principles
> Use DP when the same subproblem shows up again and the best overall answer is built from best sub-answers. Write the recurrence first, set base cases, fill the table in an order where dependencies are ready, then shrink space if you only need the last row or two.




---

## Linear DP (1-D)

### Climbing Stairs `🎯 T2`

> [!example] Problem
> You are climbing a staircase. It takes n steps to reach the top.
> Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
> 
> **Example 1:**
> ```
> Input: n = 2
> Output: 2
> Explanation: There are two ways to climb to the top.
> 1. 1 step + 1 step
> 2. 2 steps
> ```
> 
> **Example 2:**
> ```
> Input: n = 3
> Output: 3
> Explanation: There are three ways to climb to the top.
> 1. 1 step + 1 step + 1 step
> 2. 1 step + 2 steps
> 3. 2 steps + 1 step
> ```
> 
> **Constraints:**
> - 1 <= n <= 45

> [!info] Approach
> reaching step `i` from step `i-1` or `i-2` creates overlapping recursive calls. `dp[i]` = number of ways to reach step `i`. `dp[i] = dp[i-1] + dp[i-2]`; base `dp[0]=1, dp[1]=1`. This is Fibonacci. Space collapses to two variables.

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
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down memoization; matrix exponentiation for O(log n).

---

### Min Cost Climbing Stairs `🎯 T2`

> [!example] Problem
> You are given an integer array cost where cost[i] is the cost of ith step on a staircase. Once you pay the cost, you can either climb one or two steps.
> You can either start from the step with index 0, or the step with index 1.
> Return the minimum cost to reach the top of the floor.
> 
> **Example 1:**
> ```
> Input: cost = [10,15,20]
> Output: 15
> Explanation: You will start at index 1.
> - Pay 15 and climb two steps to reach the top.
> The total cost is 15.
> ```
> 
> **Example 2:**
> ```
> Input: cost = [1,100,1,1,1,100,1,1,100,1]
> Output: 6
> Explanation: You will start at index 0.
> - Pay 1 and climb two steps to reach index 2.
> - Pay 1 and climb two steps to reach index 4.
> - Pay 1 and climb two steps to reach index 6.
> - Pay 1 and climb one step to reach index 7.
> - Pay 1 and climb two steps to reach index 9.
> - Pay 1 and climb one step to reach the top.
> The total cost is 6.
> ```
> 
> **Constraints:**
> - 2 <= cost.length <= 1000
> - 0 <= cost[i] <= 999

> [!info] Approach
> cost to reach step `i` depends on minimum of two prior steps. `dp[i]` = min cost to reach step `i`. `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`; answer = `min(dp[n-1], dp[n-2])`.

> [!note]- Python Solution
> ```python
> def min_cost_climbing_stairs(cost):
>     n = len(cost)
>     two_back, one_back = cost[0], cost[1]
>     for i in range(2, n):
>         two_back, one_back = one_back, cost[i] + min(one_back, two_back)
>     return min(one_back, two_back)
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down; extend `cost` with a zero at position `n` to unify the final min.

---

### House Robber `🎯 T2`

> [!example] Problem
> You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.
> Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3,1]
> Output: 4
> Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
> Total amount you can rob = 1 + 3 = 4.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,7,9,3,1]
> Output: 12
> Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
> Total amount you can rob = 2 + 9 + 1 = 12.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 100
> - 0 <= nums[i] <= 400

> [!info] Approach
> robbing house `i` forbids `i-1`; the optimal decision at each house depends on the optimal result two positions back. `dp[i]` = max money from houses `0..i`. `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`; base `dp[0]=nums[0]`, `dp[1]=max(nums[0],nums[1])`.

> [!note]- Python Solution
> ```python
> def rob(nums):
>     two_back, one_back = 0, 0
>     for n in nums:
>         two_back, one_back = one_back, max(one_back, two_back + n)
>     return one_back
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down memoization. Greedy fails — skipping a high house today can be globally optimal.

---

### House Robber II (Circular) `🎯 T2`

> [!example] Problem
> You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.
> Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
> 
> **Example 1:**
> ```
> Input: nums = [2,3,2]
> Output: 3
> Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2), because they are adjacent houses.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,1]
> Output: 4
> Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
> Total amount you can rob = 1 + 3 = 4.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,2,3]
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 100
> - 0 <= nums[i] <= 1000

> [!info] Approach
> Circular constraint means house 0 and house n-1 can't both be robbed. Reduce to two linear subproblems that are mutually exclusive. `max(rob(0..n-2), rob(1..n-1))` — run linear House Robber twice.

> [!note]- Python Solution
> ```python
> def rob(nums):
>     def rob_linear(houses):
>         two_back, one_back = 0, 0
>         for h in houses:
>             two_back, one_back = one_back, max(one_back, two_back + h)
>         return one_back
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

### Maximum Subarray (Kadane's — DP view) `🎯 T2`

> [!example] Problem
> Given an integer array nums, find the subarray with the largest sum, and return its sum.
> 
> **Example 1:**
> ```
> Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
> Output: 6
> Explanation: The subarray [4,-1,2,1] has the largest sum 6.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1]
> Output: 1
> Explanation: The subarray [1] has the largest sum 1.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [5,4,-1,7,8]
> Output: 23
> Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> max subarray ending at `i` depends on whether extending the previous subarray or restarting gives a larger value. `dp[i]` = max subarray sum ending at index `i`. `dp[i] = max(nums[i], dp[i-1] + nums[i])`; answer = `max(dp)`. Collapses to one variable.

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
> Time O(n), Space O(1).

> [!tip] Alternatives
> D&C approach O(n log n) — cross-midpoint expansion, useful for explaining recurrence. Prefix sum with running minimum gives the same result.

---

### Word Break `🎯 T2`

> [!example] Problem
> Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.
> Note that the same word in the dictionary may be reused multiple times in the segmentation.
> 
> **Example 1:**
> ```
> Input: s = "leetcode", wordDict = ["leet","code"]
> Output: true
> Explanation: Return true because "leetcode" can be segmented as "leet code".
> ```
> 
> **Example 2:**
> ```
> Input: s = "applepenapple", wordDict = ["apple","pen"]
> Output: true
> Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
> Note that you are allowed to reuse a dictionary word.
> ```
> 
> **Example 3:**
> ```
> Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 300
> - 1 <= wordDict.length <= 1000
> - 1 <= wordDict[i].length <= 20
> - s and wordDict[i] consist of only lowercase English letters.
> - All the strings of wordDict are unique.

> [!info] Approach
> `s[0..i]` is breakable if any split `s[0..j]` is breakable and `s[j+1..i]` is in the dictionary. Subproblems overlap at shared prefixes. `dp[i]` = True if `s[0..i-1]` is breakable. `dp[i] = any(dp[j] and s[j:i] in word_set)` for `j` in `[i-max_len, i)`. Base: `dp[0]=True`.

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
> Time O(n × max_word_len), Space O(n).

> [!tip] Alternatives
> BFS with memoization; Trie for faster dictionary lookup.

---

### Decode Ways `🎯 T2`

> [!example] Problem
> You have intercepted a secret message encoded as a string of numbers. The message is decoded via the following mapping:
> "1" -> 'A'
> "2" -> 'B'
> ...
> "25" -> 'Y'
> "26" -> 'Z'
> However, while decoding the message, you realize that there are many different ways you can decode the message because some codes are contained in other codes ("2" and "5" vs "25").
> For example, "11106" can be decoded into:
> Note: there may be strings that are impossible to decode.
> 
> Given a string s containing only digits, return the number of ways to decode it. If the entire string cannot be decoded in any valid way, return 0.
> The test cases are generated so that the answer fits in a 32-bit integer.
> 
> **Example 1:**
> ```
> Input: s = "12"
> Output: 2
> Explanation:
> "12" could be decoded as "AB" (1 2) or "L" (12).
> ```
> 
> **Example 2:**
> ```
> Input: s = "226"
> Output: 3
> Explanation:
> "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).
> ```
> 
> **Example 3:**
> ```
> Input: s = "06"
> Output: 0
> Explanation:
> "06" cannot be mapped to "F" because of the leading zero ("6" is different from "06"). In this case, the string is not a valid encoding, so return 0.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 100
> - s contains only digits and may contain leading zero(s).

> [!info] Approach
> each position can be decoded as 1 or 2 digits; choices overlap across prefixes. `dp[i]` = number of decodings of `s[0..i-1]`. add `dp[i-1]` if `s[i-1] != '0'`; add `dp[i-2]` if `10 ≤ s[i-2:i] ≤ 26`. Base: `dp[0]=1`.

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
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down memoization. Wildcard variant (LC 639) adds branching at `'*'` but same structure.

---

## 0/1 Knapsack

### Subset Sum Problem `🎯 T2`

> [!example] Problem
> Given integers and target `T`, can any subset sum to `T`?

> [!info] Approach
> each item has two choices (include/exclude); overlap arises because the same remaining capacity is reachable via multiple item sequences. `dp[j]` = True if sum `j` is achievable using a subset of items seen so far. iterate items; for each item `x`, sweep `j` from `T` down to `x`: `dp[j] |= dp[j - x]`. Reverse sweep prevents reuse of same item (0/1 knapsack). Base: `dp[0]=True`.

> [!note]- Python Solution
> ```python
> def can_partition(nums, target):
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

### Partition Equal Subset Sum `🎯 T2`

> [!example] Problem
> Given an integer array nums, return true if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or false otherwise.
> 
> **Example 1:**
> ```
> Input: nums = [1,5,11,5]
> Output: true
> Explanation: The array can be partitioned as [1, 5, 5] and [11].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,5]
> Output: false
> Explanation: The array cannot be partitioned into equal sum subsets.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 200
> - 1 <= nums[i] <= 100

> [!info] Approach
> Equal partition iff one subset sums to `total/2`. Reduces to subset-sum with `T = total // 2`. Same as Subset Sum with `target = sum(nums) // 2`. Odd total → return False immediately. Then run 0/1 knapsack DP.

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
> Time O(n × sum), Space O(sum).

> [!tip] Alternatives
> Early exit if any single element > target. Bitset trick for constant-factor speedup.

---

### Last Stone Weight II `⚡ T1`

> [!example] Problem
> You are given an array of integers stones where stones[i] is the weight of the ith stone.
> We are playing a game with the stones. On each turn, we choose any two stones and smash them together. Suppose the stones have weights x and y with x <= y. The result of this smash is:
> At the end of the game, there is at most one stone left.
> Return the smallest possible weight of the left stone. If there are no stones left, return 0.
> 
> **Example 1:**
> ```
> Input: stones = [2,7,4,1,8,1]
> Output: 1
> Explanation:
> We can combine 2 and 4 to get 2, so the array converts to [2,7,1,8,1] then,
> we can combine 7 and 8 to get 1, so the array converts to [2,1,1,1] then,
> we can combine 2 and 1 to get 1, so the array converts to [1,1,1] then,
> we can combine 1 and 1 to get 0, so the array converts to [1], then that's the optimal value.
> ```
> 
> **Example 2:**
> ```
> Input: stones = [31,26,33,21,40]
> Output: 5
> ```
> 
> **Constraints:**
> - 1 <= stones.length <= 30
> - 1 <= stones[i] <= 100

> [!info] Approach
> Each stone ultimately gets a sign `+1` or `-1`; minimize `|P - N| = |total - 2N|`. Maximize `N ≤ total/2`. Same as subset sum to target. `dp[j]` = True if subset sum `j` is reachable, for `j ≤ total // 2`. Standard 0/1 knapsack boolean DP; answer = `total - 2 × max_j_where_dp[j]`.

> [!note]- Python Solution
> ```python
> def last_stone_weight_ii(stones):
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

### Coin Change (Min Coins) `🎯 T2`

> [!example] Problem
> You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.
> Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.
> You may assume that you have an infinite number of each kind of coin.
> 
> **Example 1:**
> ```
> Input: coins = [1,2,5], amount = 11
> Output: 3
> Explanation: 11 = 5 + 5 + 1
> ```
> 
> **Example 2:**
> ```
> Input: coins = [2], amount = 3
> Output: -1
> ```
> 
> **Example 3:**
> ```
> Input: coins = [1], amount = 0
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= coins.length <= 12
> - 1 <= coins[i] <= 2^{31} - 1
> - 0 <= amount <= 10^4

> [!info] Approach
> Coins are reusable → unbounded knapsack. Overlapping subproblems: the optimal solution for amount `i` reuses optimal solutions for `i - coin`. `dp[i]` = min coins to make amount `i`. `dp[i] = min(dp[i-c] + 1)` for each coin `c ≤ i`; forward sweep (reuse allowed). Base: `dp[0]=0`, rest `inf`.

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
> Time O(amount × |coins|), Space O(amount).

> [!tip] Alternatives
> BFS level-by-level (level = coin count) — same complexity but queue overhead. Top-down memo.

---

### Coin Change II (Total Ways) `🎯 T2`

> [!example] Problem
> You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.
> Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.
> You may assume that you have an infinite number of each kind of coin.
> The answer is guaranteed to fit into a signed 32-bit integer.
> 
> **Example 1:**
> ```
> Input: amount = 5, coins = [1,2,5]
> Output: 4
> Explanation: there are four ways to make up the amount:
> 5=5
> 5=2+2+1
> 5=2+1+1+1
> 5=1+1+1+1+1
> ```
> 
> **Example 2:**
> ```
> Input: amount = 3, coins = [2]
> Output: 0
> Explanation: the amount of 3 cannot be made up just with coins of 2.
> ```
> 
> **Example 3:**
> ```
> Input: amount = 10, coins = [10]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= coins.length <= 300
> - 1 <= coins[i] <= 5000
> - All the values of coins are unique.
> - 0 <= amount <= 5000

> [!info] Approach
> Combinations require each denomination to be processed once, not per position. Loop coins outer, amounts inner. `dp[i]` = number of combination ways to make amount `i`. Outer loop over coins; inner forward sweep: `dp[i] += dp[i-c]`. This ensures [1,2] and [2,1] are the same combination.

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
> Time O(amount × |coins|), Space O(amount).

> [!tip] Alternatives
> Swapping loop order counts permutations (ordered sequences) — different problem. 2D DP clarifies the derivation.

---

### Perfect Squares `🎯 T2`

> [!example] Problem
> Given an integer n, return the least number of perfect square numbers that sum to n.
> A perfect square is an integer that is the square of an integer; in other words, it is the product of some integer with itself. For example, 1, 4, 9, and 16 are perfect squares while 3 and 11 are not.
> 
> **Example 1:**
> ```
> Input: n = 12
> Output: 3
> Explanation: 12 = 4 + 4 + 4.
> ```
> 
> **Example 2:**
> ```
> Input: n = 13
> Output: 2
> Explanation: 13 = 4 + 9.
> ```
> 
> **Constraints:**
> - 1 <= n <= 10^4

> [!info] Approach
> Perfect squares are unlimited "coins"; this is unbounded knapsack / coin change with coins = {1,4,9,16,...}. `dp[i]` = min squares summing to `i`. `dp[i] = min(dp[i - k²] + 1)` for all `k² ≤ i`. Base: `dp[0]=0`.

> [!note]- Python Solution
> ```python
> def num_squares(n):
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

### Longest Common Subsequence `🎯 T2`

> [!example] Problem
> Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.
> A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.
> A common subsequence of two strings is a subsequence that is common to both strings.
> 
> **Example 1:**
> ```
> Input: text1 = "abcde", text2 = "ace" 
> Output: 3  
> Explanation: The longest common subsequence is "ace" and its length is 3.
> ```
> 
> **Example 2:**
> ```
> Input: text1 = "abc", text2 = "abc"
> Output: 3
> Explanation: The longest common subsequence is "abc" and its length is 3.
> ```
> 
> **Example 3:**
> ```
> Input: text1 = "abc", text2 = "def"
> Output: 0
> Explanation: There is no such common subsequence, so the result is 0.
> ```
> 
> **Constraints:**
> - 1 <= text1.length, text2.length <= 1000
> - text1 and text2 consist of only lowercase English characters.

> [!info] Approach
> Matching characters at positions `i,j` yields a subproblem on the remaining suffixes; these sub-results are reused. `dp[i][j]` = LCS length of `s1[0..i-1]` and `s2[0..j-1]`. If `s1[i-1]==s2[j-1]`: `dp[i][j] = dp[i-1][j-1]+1`; else `max(dp[i-1][j], dp[i][j-1])`. Space: roll to one row.

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
> Time O(m×n), Space O(min(m,n)).

> [!tip] Alternatives
> Full 2D table for path reconstruction. Hunt-Szymanski for sparse matches.

---

### Edit Distance `🎯 T2`

> [!example] Problem
> Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.
> You have the following three operations permitted on a word
> 
> **Example 1:**
> ```
> Input: word1 = "horse", word2 = "ros"
> Output: 3
> Explanation: 
> horse -> rorse (replace 'h' with 'r')
> rorse -> rose (remove 'r')
> rose -> ros (remove 'e')
> ```
> 
> **Example 2:**
> ```
> Input: word1 = "intention", word2 = "execution"
> Output: 5
> Explanation: 
> intention -> inention (remove 't')
> inention -> enention (replace 'i' with 'e')
> enention -> exention (replace 'n' with 'x')
> exention -> exection (replace 'n' with 'c')
> exection -> execution (insert 'u')
> ```
> 
> **Constraints:**
> - 0 <= word1.length, word2.length <= 500
> - word1 and word2 consist of lowercase English letters.

> [!info] Approach
> Three operations at each mismatch create overlapping subproblems on shorter string pairs. `dp[i][j]` = edit distance between `word1[0..i-1]` and `word2[0..j-1]`. If chars match: `dp[i-1][j-1]`; else `1 + min(replace=dp[i-1][j-1], delete=dp[i-1][j], insert=dp[i][j-1])`. Base: `dp[i][0]=i`, `dp[0][j]=j`.

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
> Time O(m×n), Space O(min(m,n)).

> [!tip] Alternatives
> Full 2D for operation reconstruction. Ukkonen's O(k×min(m,n)) when distance `k` is small.

---

### Longest Palindromic Subsequence `🎯 T2`

> [!example] Problem
> Given a string s, find the longest palindromic subsequence's length in s.
> A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.
> 
> **Example 1:**
> ```
> Input: s = "bbbab"
> Output: 4
> Explanation: One possible longest palindromic subsequence is "bbbb".
> ```
> 
> **Example 2:**
> ```
> Input: s = "cbbd"
> Output: 2
> Explanation: One possible longest palindromic subsequence is "bb".
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 1000
> - s consists only of lowercase English letters.

> [!info] Approach
> A palindrome is its own reverse; LPS(s) = LCS(s, reverse(s)). Both overlapping subproblems. `dp[i][j]` = LPS length in `s[i..j]`. If `s[i]==s[j]`: `dp[i][j] = dp[i+1][j-1]+2`; else `max(dp[i+1][j], dp[i][j-1])`. Fill diagonals outward (length 1→2→…→n).

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
> Time O(n²), Space O(n²).

> [!tip] Alternatives
> LCS(s, s[::-1]) — simpler to implement, same complexity. Space-optimize with two 1D arrays.

---

### Minimum ASCII Delete Sum for Two Strings `🎯 T2`

> [!example] Problem
> Given two strings s1 and s2, return the lowest ASCII sum of deleted characters to make two strings equal.
> 
> **Example 1:**
> ```
> Input: s1 = "sea", s2 = "eat"
> Output: 231
> Explanation: Deleting "s" from "sea" adds the ASCII value of "s" (115) to the sum.
> Deleting "t" from "eat" adds 116 to the sum.
> At the end, both strings are equal, and 115 + 116 = 231 is the minimum sum possible to achieve this.
> ```
> 
> **Example 2:**
> ```
> Input: s1 = "delete", s2 = "leet"
> Output: 403
> Explanation: Deleting "dee" from "delete" to turn the string into "let",
> adds 100[d] + 101[e] + 101[e] to the sum.
> Deleting "e" from "leet" adds 101[e] to the sum.
> At the end, both strings are equal to "let", and the answer is 100+101+101+101 = 403.
> If instead we turned both strings into "lee" or "eet", we would get answers of 433 or 417, which are higher.
> ```
> 
> **Constraints:**
> - 1 <= s1.length, s2.length <= 1000
> - s1 and s2 consist of lowercase English letters.

> [!info] Approach
> Deleting characters to equalize is equivalent to keeping the maximum-weight common subsequence (measured in ASCII values). Overlapping on pairs of string prefixes. `dp[i][j]` = min ASCII delete cost to equalize `s1[0..i-1]` and `s2[0..j-1]`. If `s1[i-1]==s2[j-1]`: `dp[i][j]=dp[i-1][j-1]`; else `min(dp[i-1][j]+ord(s1[i-1]), dp[i][j-1]+ord(s2[j-1]))`. Base: prefix ASCII sums.

> [!note]- Python Solution
> ```python
> def minimum_delete_sum(s1, s2):
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

### Minimum Window Subsequence (LC 727) `🎯 T2`

> [!example] Problem
> Given strings `s1` and `s2`, return *the minimum contiguous substring part of *`s1`*, so that *`s2`* is a subsequence of the part*.
> 
> If there is no such window in `s1` that covers all characters in `s2`, return the empty string `""`. If there are multiple such minimum-length windows, return the one with the **left-most starting index**.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** s1 = "abcdebdde", s2 = "bde"
> **Output:** "bcde"
> **Explanation:** 
> "bcde" is the answer because it occurs before "bdde" which has the same length.
> "deb" is not a smaller window because the elements of s2 in the window must occur in order.
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** s1 = "jmeqksfrsdcmsiwvaovztaqenprpvnbstl", s2 = "u"
> **Output:** ""
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= s1.length <= 2 * 10^4`
> 	
> - `1 <= s2.length <= 100`
> 	
> - `s1` and `s2` consist of lowercase English letters.

> [!info] Approach
> Brute force tries all substrings O(n²*m). DP achieves O(n*m): track, for each position in s, the earliest start index in s such that t[0..j] has been matched as a subsequence ending at that position. 2D DP — dp[i][j] = starting index in s such that s[dp[i][j]..i] contains t[0..j] as a subsequence. dp[i][j] = dp[i-1][j-1] if s[i]==t[j] else dp[i-1][j]. Base: dp[i][0] = i when s[i]==t[0]. When dp[i][len(t)-1] is valid, compute window length = i - dp[i][len(t)-1] + 1 and track minimum.

> [!note]- Python Solution
> ```python
> def min_window(s, t):
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

### Unique Paths `🎯 T2`

> [!example] Problem
> There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.
> Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.
> The test cases are generated so that the answer will be less than or equal to 2 * 109.
> 
> **Example 1:**
> ```
> Input: m = 3, n = 7
> Output: 28
> ```
> 
> **Example 2:**
> ```
> Input: m = 3, n = 2
> Output: 3
> Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
> 1. Right -> Down -> Down
> 2. Down -> Down -> Right
> 3. Down -> Right -> Down
> ```
> 
> **Constraints:**
> - 1 <= m, n <= 100

> [!info] Approach
> Each cell is reachable from exactly above or left; paths to any cell = sum of paths to two neighbors — overlapping. `dp[j]` = paths to column `j` of current row (rolling 1D array). `dp[j] += dp[j-1]` for each row. Base: all 1s initially (single path along edges).

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
> Time O(m×n), Space O(n).

> [!tip] Alternatives
> Combinatorics: `math.comb(m+n-2, m-1)` — O(min(m,n)) time, O(1) space.

---

### Unique Paths II (With Obstacles) `🎯 T2`

> [!example] Problem
> You are given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.
> An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.
> Return the number of possible unique paths that the robot can take to reach the bottom-right corner.
> The testcases are generated so that the answer will be less than or equal to 2 * 109.
> 
> **Example 1:**
> ```
> Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
> Output: 2
> Explanation: There is one obstacle in the middle of the 3x3 grid above.
> There are two ways to reach the bottom-right corner:
> 1. Right -> Right -> Down -> Down
> 2. Down -> Down -> Right -> Right
> ```
> 
> **Example 2:**
> ```
> Input: obstacleGrid = [[0,1],[0,0]]
> Output: 1
> ```
> 
> **Constraints:**
> - m == obstacleGrid.length
> - n == obstacleGrid[i].length
> - 1 <= m, n <= 100
> - obstacleGrid[i][j] is 0 or 1.

> [!info] Approach
> Same grid DP but obstacle cells have zero paths and block propagation downstream. `dp[j]` = paths to `(i,j)` treating blocked cells as 0. Same recurrence; set `dp[j]=0` when `obstacleGrid[i][j]==1`. Careful with first row/col initialization.

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
> Time O(m×n), Space O(n).

> [!tip] Alternatives
> Full 2D table is simpler to reason about. No combinatorial shortcut with obstacles.

---

### Minimum Path Sum `🎯 T2`

> [!example] Problem
> Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path.
> Note: You can only move either down or right at any point in time.
> 
> **Example 1:**
> ```
> Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
> Output: 7
> Explanation: Because the path 1 → 3 → 1 → 1 → 1 minimizes the sum.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[1,2,3],[4,5,6]]
> Output: 12
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 200
> - 0 <= grid[i][j] <= 200

> [!info] Approach
> Min-cost path to `(i,j)` = grid value + min of cost from above or left — overlapping. `dp[j]` = min cost to reach column `j` of current row. `dp[j] = grid[i][j] + min(dp[j], dp[j-1])`. Initialize first row as prefix sums.

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
> Time O(m×n), Space O(n).

> [!tip] Alternatives
> Dijkstra if negative weights possible. In-place modification gives O(1) extra space.

---

### Maximal Square `🎯 T2`

> [!example] Problem
> Given an m x n binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its area.
> 
> **Example 1:**
> ```
> Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
> Output: 4
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [["0","1"],["1","0"]]
> Output: 1
> ```
> 
> **Example 3:**
> ```
> Input: matrix = [["0"]]
> Output: 0
> ```
> 
> **Constraints:**
> - m == matrix.length
> - n == matrix[i].length
> - 1 <= m, n <= 300
> - matrix[i][j] is '0' or '1'.

> [!info] Approach
> A square of side `k` at `(i,j)` requires squares of side `k-1` at three adjacent neighbors — optimal substructure with overlapping sub-rectangles. `dp[i][j]` = side of largest all-1s square with bottom-right at `(i,j)`. If `matrix[i][j]=='1'`: `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1`. Roll to two rows or 1D.

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
> Time O(m×n), Space O(m×n) → reducible to O(n).

> [!tip] Alternatives
> Histogram approach (largest rectangle in histogram per row) — O(m×n) but harder to implement.

---

## State Machine DP (Stock Problems)

### Best Time to Buy and Sell Stock (All Variants) `🎯 T2`

> [!example] Problem
> You are given an array prices where prices[i] is the price of a given stock on the ith day.
> You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
> Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
> 
> **Example 1:**
> ```
> Input: prices = [7,1,5,3,6,4]
> Output: 5
> Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
> Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
> ```
> 
> **Example 2:**
> ```
> Input: prices = [7,6,4,3,1]
> Output: 0
> Explanation: In this case, no transactions are done and the max profit = 0.
> ```
> 
> **Constraints:**
> - 1 <= prices.length <= 10^5
> - 0 <= prices[i] <= 10^4

> [!note]- Python Solution
> ```python
> def max_profit(prices):
>     min_price, max_profit = float('inf'), 0
>     for p in prices:
>         min_price = min(min_price, p)
>         max_profit = max(max_profit, p - min_price)
>     return max_profit
> ```

> [!example] Problem II — Unlimited transactions

> [!note]- Python Solution
> ```python
> def max_profit(prices):
>     return sum(max(0, prices[i] - prices[i-1]) for i in range(1, len(prices)))
> ```

> [!example] Problem III — At most 2 transactions

> [!note]- Python Solution
> ```python
> def max_profit(prices):
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
> def max_profit(k, prices):
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
> Three states model the constraint: holding, just sold (cooldown), resting. Transitions connect states across days. `held` = best profit when holding; `sold` = best on day of sell; `rest` = best when not holding and not in cooldown. `held = max(held, rest - price)`, `sold = held + price`, `rest = max(rest, sold)`.

> [!note]- Python Solution
> ```python
> def max_profit(prices):
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
> Two states: `hold` (best profit holding), `cash` (best profit not holding). `hold = max(hold, cash - price)`, `cash = max(cash, hold + price - fee)`.

> [!note]- Python Solution
> ```python
> def max_profit(prices, fee):
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

## Longest Increasing Subsequence (LIS) Family

### Longest Increasing Subsequence `⚡ T1`

> [!example] Problem
> Given an integer array nums, return the length of the longest strictly increasing subsequence.
> 
> **Example 1:**
> ```
> Input: nums = [10,9,2,5,3,7,101,18]
> Output: 4
> Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,0,3,2,3]
> Output: 4
> ```
> 
> **Example 3:**
> ```
> Input: nums = [7,7,7,7,7,7,7]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2500
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> Naïve O(n²) DP checks all prior elements; patience sort uses a maintained tails array to binary-search the right position, achieving O(n log n). `tails[i]` = smallest tail element of all increasing subsequences of length `i+1` seen so far. For each `x` in `nums`, binary search `tails` for the first element `>= x`. If found, replace it with `x`; otherwise append `x`. Answer = `len(tails)`.

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
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> O(n²) DP: `dp[i] = max(dp[j]+1 for j<i if nums[j]<nums[i])`. To reconstruct the actual subsequence, maintain a `parent` array alongside the patience sort.

---

### Number of LIS

> [!example] Problem
> Given `nums`, return the number of longest increasing subsequences (LC 673).

> [!info] Approach
> Length alone isn't enough; need to count paths. Two parallel arrays track both. `length[i]` = LIS length ending at index `i`. `count[i]` = number of such subsequences. For each `i`, scan `j < i`. If `nums[j] < nums[i]`: if `length[j]+1 > length[i]`, update both; if equal, add `count[j]` to `count[i]`. Answer = sum of `count[i]` where `length[i] == max_length`.

> [!note]- Python Solution
> ```python
> def find_number_of_lis(nums):
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

## String DP

### Distinct Subsequences `🎯 T2`

> [!example] Problem
> Given two strings s and t, return the number of distinct subsequences of s which equals t.
> The test cases are generated so that the answer fits on a 32-bit signed integer.
> 
> **Example 1:**
> ```
> Input: s = "rabbbit", t = "rabbit"
> Output: 3
> Explanation:
> As shown below, there are 3 ways you can generate "rabbit" from s.
> rabbbit
> rabbbit
> rabbbit
> ```
> 
> **Example 2:**
> ```
> Input: s = "babgbag", t = "bag"
> Output: 5
> Explanation:
> As shown below, there are 5 ways you can generate "bag" from s.
> babgbag
> babgbag
> babgbag
> babgbag
> babgbag
> ```
> 
> **Constraints:**
> - 1 <= s.length, t.length <= 1000
> - s and t consist of English letters.

> [!info] Approach
> At each position we either use `s[i]` to match `t[j]` or we skip it; both branches must be counted. `dp[i][j]` = number of ways to form `t[:j]` from `s[:i]`. If `s[i-1] == t[j-1]`: `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]` (use or skip). Else: `dp[i][j] = dp[i-1][j]`. Base: `dp[i][0] = 1` for all `i`.

> [!note]- Python Solution
> ```python
> def num_distinct(s, t):
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

### Interleaving String `🎯 T2`

> [!example] Problem
> Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of s1 and s2.
> An interleaving of two strings s and t is a configuration where s and t are divided into n and m substrings respectively, such that:
> Note: a + b is the concatenation of strings a and b.
> 
> **Example 1:**
> ```
> Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
> Output: true
> Explanation: One way to obtain s3 is:
> Split s1 into s1 = "aa" + "bc" + "c", and s2 into s2 = "dbbc" + "a".
> Interleaving the two splits, we get "aa" + "dbbc" + "bc" + "a" + "c" = "aadbbcbcac".
> Since s3 can be obtained by interleaving s1 and s2, we return true.
> ```
> 
> **Example 2:**
> ```
> Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
> Output: false
> Explanation: Notice how it is impossible to interleave s2 with any other string to obtain s3.
> ```
> 
> **Example 3:**
> ```
> Input: s1 = "", s2 = "", s3 = ""
> Output: true
> ```
> 
> **Constraints:**
> - 0 <= s1.length, s2.length <= 100
> - 0 <= s3.length <= 200
> - s1, s2, and s3 consist of lowercase English letters.

> [!info] Approach
> At each position in `s3` we choose whether the next character comes from `s1` or `s2`; overlapping subproblems arise. `dp[i][j]` = true if `s3[:i+j]` can be formed from `s1[:i]` and `s2[:j]`. `dp[i][j] = (dp[i-1][j] and s1[i-1]==s3[i+j-1]) or (dp[i][j-1] and s2[j-1]==s3[i+j-1])`. Base: `dp[0][0] = True`.

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
> Time O(mn), Space O(n).

> [!tip] Alternatives
> BFS/DFS with memoization on `(i, j)` state is equivalent and sometimes clearer.

---

### Regular Expression Matching

> [!example] Problem
> Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:
> The matching should cover the entire input string (not partial).
> 
> **Example 1:**
> ```
> Input: s = "aa", p = "a"
> Output: false
> Explanation: "a" does not match the entire string "aa".
> ```
> 
> **Example 2:**
> ```
> Input: s = "aa", p = "a*"
> Output: true
> Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".
> ```
> 
> **Example 3:**
> ```
> Input: s = "ab", p = ".*"
> Output: true
> Explanation: ".*" means "zero or more (*) of any character (.)".
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 20
> - 1 <= p.length <= 20
> - s contains only lowercase English letters.
> - p contains only lowercase English letters, '.', and '*'.
> - It is guaranteed for each appearance of the character '*', there will be a previous valid character to match.

> [!info] Approach
> `*` introduces branching — match zero occurrences (skip pattern pair) or one-or-more — creating overlapping sub-problems. `dp[i][j]` = true if `s[:i]` matches `p[:j]`. If `p[j-1] == '*'`: `dp[i][j] = dp[i][j-2]` (zero uses) or `(dp[i-1][j] and (p[j-2]=='.' or p[j-2]==s[i-1]))` (one+ uses). Else: `dp[i][j] = dp[i-1][j-1] and (p[j-1]=='.' or p[j-1]==s[i-1])`.

> [!note]- Python Solution
> ```python
> def is_match(s, p):
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

## Bitmask DP

### Partition to K Equal Subset Sums `🎯 T2`

> [!example] Problem
> Given `nums` and integer `k`, return true if the array can be partitioned into `k` subsets each with equal sum (LC 698).

> [!info] Approach
> Subset assignment is NP-hard in general but `n ≤ 16` makes 2^n bitmask DP feasible. `dp[mask]` = true if the elements indicated by `mask` can be perfectly distributed into some number of full buckets. `target = total / k`. Iterate all masks in order. For each set mask, compute `current_sum = sum of selected elements % target`. Try adding each unselected element; if it fits, `dp[mask | (1<<i)] = True`. Answer = `dp[(1<<n)-1]`.

> [!note]- Python Solution
> ```python
> def can_partition_k_subsets(nums, k):
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

## DP on Sequences

### Jump Game II `🎯 T2`

> [!example] Problem
> You are given a 0-indexed array of integers nums of length n. You are initially positioned at nums[0].
> Each element nums[i] represents the maximum length of a forward jump from index i. In other words, if you are at nums[i], you can jump to any nums[i + j] where:
> Return the minimum number of jumps to reach nums[n - 1]. The test cases are generated such that you can reach nums[n - 1].
> 
> **Example 1:**
> ```
> Input: nums = [2,3,1,1,4]
> Output: 2
> Explanation: The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, then 3 steps to the last index.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,3,0,1,4]
> Output: 2
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - 0 <= nums[i] <= 1000
> - It's guaranteed that you can reach nums[n - 1].

> [!info] Approach
> Greedy DP: at each jump, greedily extend to the farthest reachable index. Counting jumps only when forced to jump. Track `current_end` (end of current jump range) and `farthest` (max reachable from within range). Iterate; update `farthest = max(farthest, i + nums[i])`. When `i == current_end` and not at last index: increment jumps, set `current_end = farthest`.

> [!note]- Python Solution
> ```python
> def jump(nums):
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

### Maximum Product Subarray `🎯 T2`

> [!example] Problem
> Given an integer array nums, find a subarray that has the largest product, and return the product.
> The test cases are generated so that the answer will fit in a 32-bit integer.
> 
> **Example 1:**
> ```
> Input: nums = [2,3,-2,4]
> Output: 6
> Explanation: [2,3] has the largest product 6.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [-2,0,-1]
> Output: 0
> Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - -10 <= nums[i] <= 10
> - The product of any subarray of nums is guaranteed to fit in a 32-bit integer.

> [!info] Approach
> A negative number flips max↔min, so both must be tracked at each position. `max_prod` and `min_prod` ending at index `i`. At each element `x`: `max_prod, min_prod = max(x, max_prod*x, min_prod*x), min(x, max_prod*x, min_prod*x)`. Update global answer with `max_prod`.

> [!note]- Python Solution
> ```python
> def max_product(nums):
>     max_p = min_p = result = nums[0]
>     for x in nums[1:]:
>         candidates = (x, max_p * x, min_p * x)
>         max_p, min_p = max(candidates), min(candidates)
>         result = max(result, max_p)
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Prefix product with reset at zeros; or observe the answer is always a prefix or suffix product between zeros.

---

### Longest Common Substring

> [!example] Problem
> Find the length of the longest common contiguous substring shared by two strings.

> [!info] Approach
> Unlike LCS, contiguity matters. A mismatch breaks the chain, so the DP state must reset to zero on mismatch. `dp[i][j]` is the length of the longest common substring ending at `s1[i-1]` and `s2[j-1]`. If characters match, extend the diagonal: `dp[i][j] = dp[i-1][j-1] + 1`; else `dp[i][j] = 0`. Track the global maximum.

> [!note]- Python Solution
> ```python
> def longest_common_substring(s1, s2):
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

---


### Russian Doll Envelopes (LC 354)

> [!example] Problem
> You are given a 2D array of integers envelopes where envelopes[i] = [wi, hi] represents the width and the height of an envelope.
> One envelope can fit into another if and only if both the width and height of one envelope are greater than the other envelope's width and height.
> Return the maximum number of envelopes you can Russian doll (i.e., put one inside the other).
> Note: You cannot rotate an envelope.
> 
> **Example 1:**
> ```
> Input: envelopes = [[5,4],[6,4],[6,7],[2,3]]
> Output: 3
> Explanation: The maximum number of envelopes you can Russian doll is 3 ([2,3] => [5,4] => [6,7]).
> ```
> 
> **Example 2:**
> ```
> Input: envelopes = [[1,1],[1,1],[1,1]]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= envelopes.length <= 10^5
> - envelopes[i].length == 2
> - 1 <= wi, hi <= 10^5

> [!info] Approach
> If we sort by width, this becomes LIS on heights. But with equal widths, we can't include two envelopes (a wider envelope can't fit inside one of the same width). Fix: sort by `(width asc, height desc)` — the descending height ensures equal-width envelopes can never form an increasing subsequence. Sort by `(w asc, h desc)`. Extract heights. Run patience sort (O(n log n) LIS) on heights. `bisect_left` on the `tails` array — same as LC 300 LIS.

> [!note]- Python Solution
> ```python
> import bisect
> >
> def max_envelopes(envelopes):
>     envelopes.sort(key=lambda x: (x[0], -x[1]))
>     tails = []
>     for _, h in envelopes:
>         pos = bisect.bisect_left(tails, h)
>         if pos == len(tails):
>             tails.append(h)
>         else:
>             tails[pos] = h
>     return len(tails)
> ```

> [!success] Complexity
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> - O(n²) DP: for each envelope, check all previous ones and extend. Too slow for large inputs (n up to 10^5).
> - Key trick: the `(w asc, h desc)` sort is the entire insight — without it, equal-width envelopes would incorrectly contribute to the LIS.

---

---

## Interval DP

### Matrix Chain Multiplication

> [!example] Problem
> Given a sequence of matrices with dimensions `dims[i-1] × dims[i]`, find the minimum number of scalar multiplications to compute their product.

> [!info] Approach
> The order of multiplication matters. Interval DP: `dp[i][j]` = minimum cost to multiply matrices `i` through `j`. Split at every `k` from `i` to `j-1`. `dp[i][j] = min over k in [i, j-1] of dp[i][k] + dp[k+1][j] + dims[i-1] * dims[k] * dims[j]`. Fill by increasing interval length (length 1 has cost 0). Outer loop: `length` from 2 to n. Inner loops: `i`, then `k`.

> [!note]- Python Solution
> ```python
> def matrix_chain_order(dims):
>     n = len(dims) - 1
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
> - Top-down with a memo dict on `(i, j)` — same asymptotic, easy to explain in an interview.
> - Pattern: this is the canonical "interval DP" template. Also appears in: burst balloons, remove boxes, strange printer.

---

### Burst Balloons (LC 312) `🎯 T2`

> [!example] Problem
> Given `n` balloons with values `nums[i]`, bursting balloon `i` earns `nums[left] * nums[i] * nums[right]` coins (adjacent *remaining* balloons). Maximize total coins after bursting all balloons. [H]

> [!info] Approach
> Thinking forward ("which balloon do I burst first?") fails because bursting changes adjacency unpredictably. Think **backward**: fix which balloon `k` is burst **last** in the open interval `(i, j)`. When `k` is last, its neighbors are the fixed boundaries `i` and `j`, so it earns `nums[i] * nums[k] * nums[j]`. Pad the array with 1s on both ends. `dp[i][j]` = max coins from bursting everything strictly between `i` and `j`: `dp[i][j] = max over k in (i, j) of dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j]`. Fill by increasing interval length.

> [!note]- Python Solution
> ```python
> def max_coins(nums):
>     nums = [1] + nums + [1]
>     n = len(nums)
>     dp = [[0] * n for _ in range(n)]
>     for length in range(2, n):          # gap between i and j
>         for i in range(n - length):
>             j = i + length
>             for k in range(i + 1, j):   # k burst last in (i, j)
>                 dp[i][j] = max(dp[i][j],
>                                dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])
>     return dp[0][n-1]
> ```

> [!success] Complexity
> Time O(n³), Space O(n²).

> [!tip] Alternatives
> - Key insight to state in interview: "last burst" makes subproblems independent — "first burst" does not.
> - Same last-action-in-interval trick: Remove Boxes (LC 546), Strange Printer (LC 664), Minimum Cost to Merge Stones — all `💤 T3` at L3.

---

## DP + Binary Search — L4 addition

### Maximum Profit in Job Scheduling `🎯 T2`

> [!example] Problem
> Given jobs as `(startTime, endTime, profit)`, pick non-overlapping jobs maximizing total profit. Jobs ending at t and starting at t don't overlap.

> [!info] Approach
> Weighted interval scheduling — greedy fails because profits are arbitrary, so it's DP. Sort jobs by **end time**; let `dp[i]` = best profit using the first i jobs. For job i: skip it (`dp[i-1]`) or take it (`profit + dp[j]` where j = count of jobs ending `≤ start_i`, found with `bisect_right` on the sorted ends). The DP + binary-search composition is exactly the "combine two T1 patterns" move Google L4 rounds test.

> [!note]- Python Solution
> ```python
> import bisect
> >
> def jobScheduling(startTime, endTime, profit):
>     jobs = sorted(zip(endTime, startTime, profit))
>     ends = [e for e, _, _ in jobs]
>     dp = [0] * (len(jobs) + 1)
>     for i, (e, s, p) in enumerate(jobs):
>         j = bisect.bisect_right(ends, s, 0, i)
>         dp[i + 1] = max(dp[i], dp[j] + p)
>     return dp[-1]
> ```

> [!success] Complexity
> Time O(n log n); Space O(n).

> [!warning] Gotcha
> `bisect_right` (not `bisect_left`) because a job ending exactly at `s` is compatible. Limit the search to `[0, i)` — searching the whole array can "find" the current job. State the greedy counter-example (one long high-profit job vs many short ones) before writing the DP.

---


## See Also

[[recursion]] | [[sorting]] | [[binary-search]] | [[graph-algorithms]]
