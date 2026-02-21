# Day 2: Practice Array Problems

Here are the detailed notes for **Day 2: Practice Array Problems**. The goal is to focus on some key array problems, which are frequently asked in coding interviews. We will cover problem types like searching, subarrays, and manipulation.

## Key Concepts in Array Problems

1. **Two-pointer Technique**:
   * **Definition**: Use two pointers to iterate through an array, one starting at the beginning and the other at the end or somewhere else depending on the problem.
   * **Use Case**: Useful when solving problems where the array needs to be traversed from both directions or when the elements need to be compared.
   * **Common Problems**:
     * Finding pairs that sum up to a target value.
     * Merging two sorted arrays.
     * Reversing an array or subarray.
2. **Sliding Window Technique**:
   * **Definition**: Involves maintaining a window (subarray) that slides across the array.
   * **Use Case**: Effective for problems involving subarrays or substrings, especially when you're looking for the maximum/minimum/target value in a continuous range.
   * **Common Problems**:
     * Maximum sum subarray of size `k`.
     * Longest substring without repeating characters.
     * Find all anagrams of a string within another string.
3. **Prefix Sum**:
   * **Definition**: Store cumulative sums of array elements to allow for quick calculations of subarray sums.
   * **Use Case**: Helpful for problems where repeated sum calculations of subarrays are required.
   * **Common Problems**:
     * Subarray sum equal to a target value.
     * Finding the equilibrium index of an array.

***

## Example Problems and Solutions

**1. Two Sum Problem**

* **Problem Statement**: Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.
* **Approach**:
  * **Brute force**: Check all pairs to find the solution (O(n²)).
  * **Optimal solution**: Use a hash map to store the difference (`target - nums[i]`) as the key and index as the value. For each element, check if it exists in the hash map.
* **Time Complexity**: O(n)
* **Space Complexity**: O(n)

```python
def twoSum(nums, target):
    hashmap = {}
    for i, num in enumerate(nums):
        difference = target - num
        if difference in hashmap:
            return [hashmap[difference], i]
        hashmap[num] = i
```

**2. Maximum Subarray (Kadane’s Algorithm)**

* **Problem Statement**: Find the contiguous subarray (containing at least one number) which has the largest sum.
* **Approach**:
  * Use Kadane’s Algorithm. Iterate through the array, and at each element, determine whether to include it in the current subarray or start a new one.
* **Time Complexity**: O(n)
* **Space Complexity**: O(1)

```python
def maxSubArray(nums):
    max_sum = curr_sum = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum
```

**3. Move Zeros to the End**

* **Problem Statement**: Given an array, move all zeros to the end while maintaining the relative order of the non-zero elements.
* **Approach**:
  * Use the two-pointer technique: one pointer to track the position for non-zero elements and another to iterate through the array.
* **Time Complexity**: O(n)
* **Space Complexity**: O(1)

```python
def moveZeroes(nums):
    pos = 0  # Position to place the next non-zero element
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[pos], nums[i] = nums[i], nums[pos]
            pos += 1
```

**4. Best Time to Buy and Sell Stock**

* **Problem Statement**: You are given an array where each element represents the stock price on a particular day. Find the maximum profit you can achieve by buying and selling on different days.
* **Approach**:
  * Use a single-pass solution to track the minimum price and calculate the maximum profit.
* **Time Complexity**: O(n)
* **Space Complexity**: O(1)

```python
def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit
```

**5. Contains Duplicate**

* **Problem Statement**: Given an array, determine if it contains any duplicates.
* **Approach**:
  * Use a set to track elements we’ve seen so far. If an element is already in the set, return `True`; otherwise, return `False`.
* **Time Complexity**: O(n)
* **Space Complexity**: O(n)

```python
def containsDuplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

***

## Advanced Topics

1. **Subarray Problems**:
   * **Maximum Subarray of Size `K`**: Use a sliding window to keep track of the sum of subarrays of size `K`.
   * **Subarrays with a Given Sum**: Use a prefix sum approach to calculate the sum of subarrays efficiently.
2.  **Matrix Manipulation**:

    * Arrays can be extended into matrices (2D arrays) where row/column traversal, matrix rotations, and searching are common operations.
    * **Example Problem**: Search for a number in a 2D matrix sorted row-wise and column-wise.

    ```python
    def searchMatrix(matrix, target):
        if not matrix:
            return False
        row, col = 0, len(matrix[0]) - 1
        while row < len(matrix) and col >= 0:
            if matrix[row][col] == target:
                return True
            elif matrix[row][col] > target:
                col -= 1
            else:
                row += 1
        return False
    ```

***

#### Summary of Key Array Problem-Solving Techniques:

1. **Two-pointer**: Efficient for pair problems, like finding a pair with a specific sum.
2. **Sliding Window**: Optimal for problems involving subarrays.
3. **Prefix Sum**: Useful for problems involving subarray sums and for avoiding repeated summation.

#### Recommended Practice Problems:

1. **LeetCode**:
   * Two Sum
   * Best Time to Buy and Sell Stock
   * Maximum Subarray
   * Move Zeros
   * Contains Duplicate
2. **HackerRank**: Arrays – DS, Array Manipulation.

Practicing these key problems will help you build a strong foundation in arrays, one of the most common data structures you'll encounter in coding interviews.
