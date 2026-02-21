# Day 25: Review Common Patterns in Problems.

Here are detailed notes for **Day 25: Review Common Patterns in Problems**. This day focuses on identifying and revisiting key problem-solving patterns that frequently appear in coding interviews, which will help you recognize and apply them during actual interview scenarios.

***

#### 1. **Importance of Recognizing Patterns**

Recognizing common patterns in coding problems can simplify the problem-solving process and lead to more efficient solutions. Understanding these patterns allows you to:

* Quickly identify the best approach to a problem.
* Reduce the time spent on new problems by applying known techniques.
* Improve your confidence and performance in interviews.

#### 2. **Common Patterns in Coding Problems**

Here are several common patterns with brief explanations and examples:

**2.1 Sliding Window**

* **Concept**: This pattern involves creating a window that can either expand or contract to solve problems related to arrays or strings.
* **Typical Problems**:
  * Longest substring with at most `k` distinct characters.
  * Minimum size subarray sum.
*   **Example**:

    ```python
    def min_sub_array_len(target, nums):
        left, total, min_length = 0, 0, float('inf')
        for right in range(len(nums)):
            total += nums[right]
            while total >= target:
                min_length = min(min_length, right - left + 1)
                total -= nums[left]
                left += 1
        return min_length if min_length != float('inf') else 0
    ```

**2.2 Two Pointers**

* **Concept**: Use two pointers to solve problems involving arrays or linked lists, typically to find pairs or subarrays.
* **Typical Problems**:
  * Valid palindrome.
  * 3Sum problem.
*   **Example**:

    ```python
    def three_sum(nums):
        nums.sort()
        result = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            left, right = i + 1, len(nums) - 1
            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]
                if current_sum < 0:
                    left += 1
                elif current_sum > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
        return result
    ```

**2.3 Fast and Slow Pointers**

* **Concept**: This technique uses two pointers moving at different speeds to detect cycles or find middle points in linked lists.
* **Typical Problems**:
  * Detecting a cycle in a linked list (Floyd’s Tortoise and Hare).
  * Finding the middle of a linked list.
*   **Example**:

    ```python
    def has_cycle(head):
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False
    ```

**2.4 Backtracking**

* **Concept**: This is a depth-first search technique used for solving problems that require exploring all potential solutions.
* **Typical Problems**:
  * N-Queens problem.
  * Permutations and combinations.
*   **Example**:

    ```python
    def permute(nums):
        result = []
        def backtrack(first=0):
            if first == len(nums):
                result.append(nums[:])
            for i in range(first, len(nums)):
                nums[first], nums[i] = nums[i], nums[first]  # swap
                backtrack(first + 1)
                nums[first], nums[i] = nums[i], nums[first]  # backtrack
        backtrack()
        return result
    ```

**2.5 Dynamic Programming**

* **Concept**: This approach involves breaking down problems into simpler subproblems and storing the results to avoid redundant computations.
* **Typical Problems**:
  * Fibonacci sequence.
  * Coin change problem.
*   **Example**:

    ```python
    def fib(n):
        if n <= 1:
            return n
        dp = [0] * (n + 1)
        dp[1] = 1
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]
    ```

**2.6 Binary Search**

* **Concept**: This technique is used for searching in a sorted array or finding optimal solutions.
* **Typical Problems**:
  * Search in rotated sorted array.
  * Find the square root of a number.
*   **Example**:

    ```python
    def binary_search(arr, target):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    ```

#### 3. **Practice Exercises**

* Review and practice problems that fit these patterns. Here are some recommended exercises:
  * **Sliding Window**: Maximum sum of a subarray of size `k`.
  * **Two Pointers**: Container with most water.
  * **Backtracking**: Subset sum problem.
  * **Dynamic Programming**: Longest common subsequence.
  * **Binary Search**: Find peak element.

#### 4. **Reflection on Patterns**

* After practicing, reflect on how identifying these patterns helped you solve problems more efficiently.
* Document key takeaways and any variations in how the patterns were applied.

#### 5. **Conclusion**

Understanding and practicing common problem-solving patterns is crucial for success in coding interviews, especially at Google. Recognizing these patterns during an interview can help you devise a solution more quickly and efficiently. Continue practicing problems across these patterns to build confidence and proficiency, which will ultimately lead to better performance in interviews.
