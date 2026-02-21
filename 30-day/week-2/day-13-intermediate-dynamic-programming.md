# Day 13: Intermediate Dynamic Programming

Here are detailed notes for **Day 13: Intermediate Dynamic Programming**. This day focuses on solving more complex dynamic programming problems, specifically the Coin Change problem and the Longest Increasing Subsequence (LIS) problem.

***

#### 1. **Coin Change Problem**

The Coin Change problem is a classic dynamic programming problem where the goal is to determine the minimum number of coins required to make a specific amount using given denominations.

**1.1 Problem Statement**

Given an array of coin denominations and an amount, find the minimum number of coins that make up that amount. If that amount cannot be formed, return -1.

**1.2 Example**

* **Input**: `coins = [1, 2, 5]`, `amount = 11`
* **Output**: `3` (11 = 5 + 5 + 1)

**1.3 Dynamic Programming Approach**

1. **Initialization**: Create a DP array `dp` where `dp[i]` will hold the minimum number of coins needed to make the amount `i`. Initialize `dp[0]` to `0` (0 coins to make amount 0) and all other entries to infinity (indicating initially unreachable amounts).
2. **State Transition**: For each coin, iterate through all amounts from the coin value to the target amount. Update the DP array: \[ dp\[x] = \min(dp\[x], dp\[x - \text{coin}] + 1) ] This checks if using the current coin improves the minimum coin count for amount `x`.
3. **Result**: If `dp[amount]` remains infinity, it means that amount cannot be formed with the given coins.

**1.4 Implementation**

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # No coins needed to make 0

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

# Example Usage
coins = [1, 2, 5]
amount = 11
print(coin_change(coins, amount))  # Output: 3
```

**1.5 Time Complexity**

* **Time Complexity**: O(n \* m), where (n) is the number of coins and (m) is the amount.
* **Space Complexity**: O(m) for the DP array.

***

#### 2. **Longest Increasing Subsequence (LIS)**

The Longest Increasing Subsequence problem seeks to find the longest subsequence in a given sequence of numbers such that all elements of the subsequence are sorted in increasing order.

**2.1 Problem Statement**

Given an array of integers, return the length of the longest increasing subsequence.

**2.2 Example**

* **Input**: `nums = [10, 9, 2, 5, 3, 7, 101, 18]`
* **Output**: `4` (The LIS is `[2, 3, 7, 101]`)

**2.3 Dynamic Programming Approach**

1. **Initialization**: Create a DP array `dp` where `dp[i]` represents the length of the longest increasing subsequence that ends with the element at index `i`. Initialize all entries to `1` because each element can be a subsequence of length `1`.
2. **State Transition**: For each pair of indices (i) and (j) (where (j < i)), check if `nums[j] < nums[i]`. If true, update `dp[i]`: \[ dp\[i] = \max(dp\[i], dp\[j] + 1) ]
3. **Result**: The result will be the maximum value in the DP array.

**2.4 Implementation**

```python
def length_of_lis(nums):
    if not nums:
        return 0

    dp = [1] * len(nums)  # Each element is an increasing subsequence of length 1
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

# Example Usage
nums = [10, 9, 2, 5, 3, 7, 101, 18]
print(length_of_lis(nums))  # Output: 4
```

**2.5 Time Complexity**

* **Time Complexity**: O(n^2), where (n) is the length of the input array.
* **Space Complexity**: O(n) for the DP array.

***

#### 3. **Optimized Approach for LIS**

While the O(n²) solution is straightforward, a more efficient O(n log n) approach can be achieved using a combination of binary search and a dynamic list to maintain the smallest tail elements of increasing subsequences.

**3.1 Optimized Approach**

1. Maintain a list `tails` where `tails[i]` holds the smallest possible tail value for all increasing subsequences of length (i + 1).
2. For each number, use binary search to find its position in `tails`. If it is larger than all elements, append it. Otherwise, replace the first element that is greater or equal to it.

**3.2 Implementation**

```python
from bisect import bisect_left

def length_of_lis_optimized(nums):
    tails = []
    for num in nums:
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)

# Example Usage
nums = [10, 9, 2, 5, 3, 7, 101, 18]
print(length_of_lis_optimized(nums))  # Output: 4
```

**3.3 Time Complexity**

* **Time Complexity**: O(n log n), due to the binary search.
* **Space Complexity**: O(n) for the `tails` array.

***

#### 4. **Recommended Practice Problems**

1. **LeetCode**:
   * Coin Change II (finding the number of ways to make change).
   * Longest Increasing Subsequence.
   * Maximum Product Subarray (a related dynamic programming problem).
2. **HackerRank**:
   * Coin Change Problem.
   * The Maximum Subarray.

***

#### 5. **Key Concepts to Remember**

* Understand how to formulate problems in terms of overlapping subproblems and optimal substructure to apply dynamic programming effectively.
* Practice both memoization and tabulation techniques to build familiarity with dynamic programming concepts.
* Recognize patterns in problems that can be solved using dynamic programming, and identify potential optimizations for performance.

By mastering these intermediate dynamic programming concepts and problems, you'll be well-prepared for more complex challenges in coding interviews and real-world scenarios.
