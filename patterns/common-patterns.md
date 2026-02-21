# common patterns

## <mark style="color:red;">Data structures --</mark>



* <mark style="color:yellow;">Arrays</mark>
  * <mark style="color:purple;">**Prefix Sum:**</mark> Used for efficiently querying the sum of elements in a subarray
  * <mark style="color:purple;">**Sliding Window:**</mark> Optimizes problems involving subarrays with constraints.
  * <mark style="color:purple;">**Two Pointers:**</mark> Useful for searching pairs, merging, or removing duplicates in sorted arrays.
  * <mark style="color:purple;">**Binary Search:**</mark> Efficiently finds elements or conditions in sorted arrays.
  * <mark style="color:purple;">**Kadane Algorithm:**</mark> Finds the maximum sum subarray in linear time.
  * <mark style="color:purple;">**Merge Intervals:**</mark> Helps in problems involving overlapping intervals.
* <mark style="color:yellow;">Linked list</mark>
  * <mark style="color:purple;">**Fast and Slow Pointers:**</mark> A variant of the two-pointer approach, useful for detecting cycles in linked lists.
  * <mark style="color:purple;">**Linked List In-Place Reversal:**</mark> Focuses on modifying linked lists without using extra space
  * <mark style="color:purple;">**Merge Two Sorted Lists:**</mark> Frequently used in sorting-related linked list problems.
  * <mark style="color:purple;">**Detect and Remove Loop:**</mark> Detects and removes cycles using Floyd’s Cycle Detection.
* <mark style="color:yellow;">Hashing</mark>
  * <mark style="color:purple;">**HashMap for Counting Frequency:**</mark> Efficiently counts occurrences of elements.
  * <mark style="color:purple;">**Two Sum using HashMap:**</mark> Finds pairs in an array that sum to a target.
  * <mark style="color:purple;">**Longest Subarray**</mark>**&#x20;with Given Sum:** Uses prefix sum and hashing.
  * <mark style="color:purple;">**Anagram Grouping:**</mark> Groups words with the same frequency of letters.
* <mark style="color:yellow;">Stack/Queues</mark>
  * <mark style="color:purple;">**Monotonic Stack:**</mark> Finds the next greater or smaller element in an array.
  * <mark style="color:purple;">**Stack for Balanced Parentheses:**</mark> Validates expressions containing parentheses.
  * <mark style="color:purple;">**Queue for Sliding Window Maximum:**</mark> Uses a deque to maintain maximum values efficiently.
  * <mark style="color:purple;">**Min/Max Stack:**</mark> Stack that supports retrieving min/max in O(1) time.
* <mark style="color:yellow;">Binary tree</mark>
  * <mark style="color:purple;">**DFS (Depth-First Search):**</mark> Visits all nodes by going deep first, commonly used in tree traversals.
  * <mark style="color:purple;">**BFS (Breadth-First Search):**</mark> Explores all nodes level by level, useful for shortest path problems.
  * <mark style="color:purple;">**Recursive Tree Traversals:**</mark> Preorder, Inorder, Postorder traversals.
  * <mark style="color:purple;">**Lowest Common Ancestor (LCA):**</mark> Finds the lowest common ancestor of two nodes.
* <mark style="color:yellow;">Binary seacrh tree</mark>
  * <mark style="color:purple;">**Inorder Traversal for Sorted Order:**</mark> Retrieves elements in sorted order.
  * <mark style="color:purple;">**Insert/Delete/Search in O(log n):**</mark> Uses the BST properties for efficient operations.
  * <mark style="color:purple;">**Kth Smallest/Largest Element:**</mark> Uses inorder traversal for ranking elements.
* <mark style="color:yellow;">Heap</mark>
  * <mark style="color:purple;">**Top K Elements:**</mark> Identifies the K largest, smallest, or most frequent elements.
  * <mark style="color:purple;">**Priority Queue for Scheduling:**</mark> Useful for scheduling tasks with priority.
  * <mark style="color:purple;">**Heap Sort:**</mark> Sorting using a heap.
  * <mark style="color:purple;">**Median of a Stream:**</mark> Uses two heaps to efficiently find the median.
* <mark style="color:yellow;">Graph</mark>
  * <mark style="color:purple;">**DFS (Depth-First Search):**</mark> Explores paths deeply before backtracking.
  * <mark style="color:purple;">**BFS (Breadth-First Search):**</mark> Explores neighbors first, used for shortest path problems.
  * <mark style="color:purple;">**Dijkstra’s Algorithm:**</mark> Finds the shortest path in weighted graphs.
  * <mark style="color:purple;">**Topological Sorting:**</mark> Used for ordering tasks based on dependencies.
  * <mark style="color:purple;">**Union-Find (Disjoint Set Union - DSU):**</mark> Detects cycles and connected components.
* <mark style="color:yellow;">Tries</mark>
  * <mark style="color:purple;">**Auto-Complete System:**</mark> Efficiently suggests words based on prefixes.
  * <mark style="color:purple;">**Word Search & Dictionary Problems:**</mark> Stores words efficiently for searching.
  * <mark style="color:purple;">**Longest Common Prefix:**</mark> Finds the common prefix of a set of words.
  * <mark style="color:purple;">**Counting Prefixes**</mark>**:** Counts how many words start with a given prefix.

## <mark style="color:red;">Algorithms --</mark>



* <mark style="color:yellow;">**Sorting —**</mark>&#x20;
  * <mark style="color:purple;">**Merge Sort:**</mark> Efficient divide-and-conquer sorting algorithm with O(n log n) complexity.
  * <mark style="color:purple;">**Quick Sort:**</mark> Uses partitioning to sort an array efficiently.
  * <mark style="color:purple;">**Counting Sort:**</mark> Works well for sorting integers with a known range.
  * <mark style="color:purple;">**Bucket Sort:**</mark> Useful when the input is uniformly distributed over a range.
  * <mark style="color:purple;">**Radix Sort:**</mark> Sorts numbers digit by digit for efficiency.
  * <mark style="color:purple;">**Sort by Custom Comparator:**</mark> Sorting based on custom rules, useful in problems with sorting constraints.



* <mark style="color:yellow;">**Binary search --**</mark>
  *   use (this stops the stack overflow)

      ```python
      mid = left + (right - left) // 2
      ```
  * happend only in sorted arrays
  * Common pattern
    * ```python
      left, right = 0, len(nums)
              
              while left < right:
                  mid = left + (right - left) // 2
                  if nums[mid] < target:
                      left = mid + 1
                  else:
                      right = mid
              
              return left
      ```
    * based on the greater than equal condition change the if condition and point the left and right value to different value
    * **Overlapping Intervals:** Useful for problems involving intervals or ranges that may overlap, such as merging intervals
  * <mark style="color:purple;">**Search in a Sorted Array:**</mark> Classic application of binary search.
  * <mark style="color:purple;">**Finding Lower/Upper Bound:**</mark> First occurrence (lower bound) or next larger element (upper bound).
  * <mark style="color:purple;">**Search in Rotated Sorted Array:**</mark> Modified binary search for rotated arrays.
  * <mark style="color:purple;">**Binary Search on Answer:**</mark> Used in optimization problems, e.g., minimum maximum value.
  * <mark style="color:purple;">**Search in 2D Matrix:**</mark> Applying binary search in a row-wise and column-wise sorted matrix.



* <mark style="color:yellow;">**Recursion**</mark>&#x20;
  * **Divide and Conquer:** Solving problems by recursively dividing into subproblems (e.g., Merge Sort, Quick Sort).
  * **Recursive Tree Traversals:** Inorder, Preorder, Postorder traversals.
  * **Subset Generation:** Generating all subsets using recursion.
  * **Tower of Hanoi:** Classic recursion problem.
  * **Fibonacci Series:** Simple example of recursion with memoization for optimization.



* <mark style="color:yellow;">**Backtracking:**</mark>&#x20;
  * Explores all potential solution paths, backtracking when a path doesn't lead to a valid solution
  * **Subset Sum:** Finding subsets that sum up to a target.
  * **N-Queens Problem:** Placing N queens on an N×N chessboard without attacking each other.
  * **Sudoku Solver:** Filling a Sudoku board using backtracking.
  * **Word Search in Grid:** Searching for a word in a matrix using DFS.
  * **Permutations and Combinations:** Generating permutations and combinations of elements.



*   <mark style="color:yellow;">**Topological Sort:**</mark>&#x20;

    * Arranges elements based on dependencies \[[04:32](https://www.youtube.com/watch?v=xo7XrRVxH8Y\&ab_channel=Sahil%26Sarra\&t=272)], helpful for prerequisite chains&#x20;
    * **Task Scheduling:** Ordering tasks based on dependencies.
    * **Course Schedule:** Determining if courses can be completed based on prerequisites.
    * **Alien Dictionary:** Finding the order of letters in an alien language.
    * **Dependency Resolution:** Used in build systems to determine the order of compilation.


*   <mark style="color:yellow;">**Bit-manipulation**</mark>

    * **Checking if a Number is Power of Two:** Using bitwise AND.
    * **Counting Set Bits:** Counting the number of 1s in a binary representation.
    * **XOR Tricks:** Finding the unique element in a list where others appear twice.
    * **Bit Masking for Subsets:** Generating all subsets using bitwise operations.
    * **Swapping Numbers Without a Temporary Variable:** Using XOR.


*   <mark style="color:yellow;">**Greedy algorithm**</mark>

    * **Activity Selection Problem:** Selecting the maximum number of non-overlapping intervals.
    * **Huffman Coding:** Building an optimal prefix-free encoding.
    * **Minimum Coins to Make Change:** Finding the minimum number of coins for a target sum.
    * **Fractional Knapsack:** Choosing items to maximize profit with fractional choices.
    * **Job Scheduling with Deadlines:** Scheduling tasks with the highest profit.


*   <mark style="color:yellow;">**Sliding window**</mark>

    * **Maximum Sum Subarray of Fixed Size:** Finding the max sum of any k-length subarray.
    * **Variable Size Sliding Window:** Used in problems like longest substring with k distinct characters.
    * **Minimum Window Substring:** Finding the smallest substring containing all characters of another string.
    * **Longest Substring Without Repeating Characters:** Maintaining a window with unique characters.
    * **Maximum of Every K-Size Subarray:** Using a deque for efficiency.


*   <mark style="color:yellow;">**DP**</mark>

    * **Knapsack Problem:** 0/1 Knapsack and Fractional Knapsack.
    * **Longest Common Subsequence (LCS):** Finding the longest common sequence between two strings.
    * **Longest Increasing Subsequence (LIS):** Finding the longest increasing subsequence in an array.
    * **Matrix Chain Multiplication:** Parenthesizing a matrix multiplication sequence for minimal cost.
    * **Coin Change Problem:** Finding the minimum number of coins to make a target sum.
    * **Fibonacci with Memoization:** Optimized recursion using memoization.
    * **DP on Trees:** Solving tree-based DP problems.
    * **Subset Sum Problem:** Checking if a subset with a given sum exists.


* <mark style="color:yellow;">**Two-Pointer:**</mark>&#x20;
  * Iterates through a sorted array using two pointers effective for problems like finding pairs that sum to a target
  * **Pair Sum in Sorted Array:** Finding a pair that sums to a target in a sorted array.
  * **Three Sum Problem:** Finding triplets with a given sum.
  * **Container with Most Water:** Maximizing area between two heights in an array.
  * **Sort Colors (Dutch National Flag Algorithm):** Sorting an array with three distinct values.
  * **Trapping Rain Water:** Calculating trapped rainwater between heights efficiently.











