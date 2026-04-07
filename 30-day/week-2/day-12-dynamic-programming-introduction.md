# Day 12: Dynamic Programming Introduction

Here are detailed notes for **Day 12: Dynamic Programming Introduction**. This day focuses on understanding the concept of dynamic programming (DP) and solving simple DP problems like the Fibonacci sequence.

***

#### 1. **What is Dynamic Programming?**

Dynamic Programming is a powerful algorithmic technique used to solve problems by breaking them down into simpler subproblems. It is particularly useful for optimization problems where the same subproblems are solved multiple times.

**Key Characteristics**:

* **Overlapping Subproblems**: The problem can be broken down into subproblems that are reused several times.
* **Optimal Substructure**: The optimal solution to the problem can be constructed from optimal solutions of its subproblems.

***

#### 2. **Approaches to Dynamic Programming**

There are two primary approaches to implement dynamic programming:

**2.1 Top-Down Approach (Memoization)**

* This approach uses recursion and stores the results of subproblems in a data structure (usually an array or dictionary) to avoid redundant calculations.
* If a subproblem has already been solved, the stored result is returned instead of recalculating.

**Example**: Fibonacci Sequence using Memoization

```python
def fibonacci_memo(n, memo={}):
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]

# Example Usage
print(fibonacci_memo(10))  # Output: 55
```

**2.2 Bottom-Up Approach (Tabulation)**

* This approach builds up a table in a bottom-up manner, solving smaller subproblems first and using their results to solve larger subproblems.
* It eliminates the overhead of recursive calls.

**Example**: Fibonacci Sequence using Tabulation

```python
def fibonacci_tab(n):
    if n <= 1:
        return n
    fib = [0] * (n + 1)
    fib[1] = 1
    
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    
    return fib[n]

# Example Usage
print(fibonacci_tab(10))  # Output: 55
```

***

#### 3. **Time Complexity of Fibonacci Sequence**

* **Top-Down Approach (Memoization)**: O(n), where (n) is the input number. Each subproblem is solved once.
* **Bottom-Up Approach (Tabulation)**: O(n), as it iterates through the array once.

***

#### 4. **Common Dynamic Programming Problems**

1. **Fibonacci Sequence**: Calculate the nth Fibonacci number.
2. **Climbing Stairs**: Given `n` stairs, calculate how many ways one can reach the top if you can climb 1 or 2 stairs at a time.
3. **Coin Change Problem**: Given an amount and denominations of coins, find the minimum number of coins needed to make that amount.
4. **[Longest Common Subsequence](../../google-sde2/PROBLEM_DETAILS.md#longest-common-subsequence)**: Find the longest subsequence common to two sequences.
5. **0/1 Knapsack Problem**: Given weights and values of items, determine the maximum value that can be carried in a knapsack of fixed capacity.

***

#### 5. **Example Problems**

**5.1 Climbing Stairs**

* **Problem Statement**: Given `n` stairs, calculate how many distinct ways one can climb to the top, taking either 1 step or 2 steps at a time.

**Solution Using DP (Tabulation)**:

```python
def climb_stairs(n):
    if n <= 1:
        return 1
    ways = [0] * (n + 1)
    ways[0] = 1
    ways[1] = 1
    
    for i in range(2, n + 1):
        ways[i] = ways[i - 1] + ways[i - 2]
    
    return ways[n]

# Example Usage
print(climb_stairs(5))  # Output: 8 (ways to climb 5 stairs)
```

**5.2 Coin Change Problem**

* **Problem Statement**: Given coins of different denominations and an amount, find the minimum number of coins that make up that amount.

**Solution Using DP (Tabulation)**:

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

# Example Usage
coins = [1, 2, 5]
amount = 11
print(coin_change(coins, amount))  # Output: 3 (11 = 5 + 5 + 1)
```

***

#### 6. **Recommended Practice Problems**

1. **LeetCode**:
   * Climbing Stairs
   * [Coin Change](../../google-sde2/PROBLEM_DETAILS.md#coin-change)
   * Unique Paths
   * [Longest Increasing Subsequence](../../google-sde2/PROBLEM_DETAILS.md#longest-increasing-subsequence)
2. **HackerRank**:
   * Coin Change Problem
   * Maximum Sum Problem

***

#### 7. **Key Concepts to Remember**

* Understand the concepts of overlapping subproblems and optimal substructure as the foundations of dynamic programming.
* Be familiar with both top-down (memoization) and bottom-up (tabulation) approaches to solving dynamic programming problems.
* Practice implementing simple DP problems to build confidence and familiarity with the technique.

By mastering the basics of dynamic programming, you’ll be well-equipped to tackle a variety of problems in coding interviews that require optimization and efficiency.
