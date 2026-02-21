# Coding patterns

## <mark style="color:purple;">Prefix sum</mark>&#x20;

Use this pattern when you need to perform multiple sum queries on a subarray or need to calculate cumulative sums.

* <mark style="color:$success;">Products of array except self</mark>
* <mark style="color:$danger;">Longest subarray with sum K</mark>
  * [**Hash Map Approach (Works for Positives & Negatives)**](https://www.google.com/search?q=Hash+Map+Approach+%28Works+for+Positives+%26+Negatives%29\&rlz=1C5OZZY_enIN1131IN1132\&oq=longest+subarray+with+sum+k\&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCDUxMDZqMGo3qAIAsAIA\&sourceid=chrome\&ie=UTF-8\&ved=2ahUKEwjhmqHlh7GSAxXuTGwGHTwCA_MQgK4QegYIAQgAEAw):
    * Iterate through the array while keeping a running prefix sum (![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)sums u m𝑠𝑢𝑚).
    * If![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)sum=ks u m equals k𝑠𝑢𝑚=𝑘, update the maximum length to the current index + 1.
    * If![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)(sum−k)open paren s u m minus k close paren(𝑠𝑢𝑚−𝑘)exists in the map, the subarray between the stored index and the current index has a sum of![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)kk𝑘. Calculate its length and update the maximum length if it's larger.
    * If![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)sums u m𝑠𝑢𝑚is not in the map, store it with its index.
    * **Complexity**:![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)O(n)cap O open paren n close paren𝑂(𝑛)Time,![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)O(n)cap O open paren n close paren𝑂(𝑛)Space.
* <mark style="color:$danger;">minimum removals for target sum</mark>
  *   This approach uses a hash map to store the first occurrence of each prefix sum, allowing for O(1) lookups to find the length of potential subarrays. This results in an overall time complexity of O(n).&#x20;

      1. **Calculate Total Sum:** First, compute the sum of all elements in the array (`total_sum`).
      2. **Determine Remaining Target:** The target sum for the _remaining_ subarray is `remaining_target = total_sum - k`. If `remaining_target` is negative, it's impossible to achieve the sum, so return -1.
      3. **Initialize Data Structures:**
         * A hash map (`map`) to store the prefix sum and its corresponding index (e.g., `{current_sum: index}`). Initialize it with `{0: -1}` to handle cases where the subarray starts from the beginning of the array.
         * `current_sum = 0`
         * `max_length = 0` (to store the length of the longest valid remaining subarray)
      4. **Iterate and Update:** Traverse the array from left to right:
         * Update `current_sum` by adding the current element.
         * Calculate the `target_subarray_sum = current_sum - remaining_target`.
         * If `target_subarray_sum` is found in the `map`:
           * Calculate the length of the current valid subarray: `current_length = current_index - map.get(target_subarray_sum)`.
           * Update `max_length = max(max_length, current_length)`.
         * If `current_sum` is not already in the `map`, add it: `map.put(current_sum, current_index)`.
      5. **Calculate Removals:** The minimum number of removals is `arr.length - max_length`. If `max_length` remains 0 (and no valid subarray was found), return -1.&#x20;

      Optimized Solution using Sli
* <mark style="color:$danger;">Largest submatrix with sum 0</mark>
  * Approach: Prefix Sum with Row Boundaries&#x20;
    1. **Iterate through all possible pairs of rows** (![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)r1r 1𝑟1and![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)r2r 2𝑟2), where![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)0≤r1≤r2\<rows0 is less than or equal to r 1 is less than or equal to r 2 is less than rows0≤𝑟1≤𝑟2\<rows.
       1. For each pair, calculate a temporary 1D array (`temp[]`) of size equal to columns, where `temp[i]` stores the sum of elements from row![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)r1r 1𝑟1to![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)r2r 2𝑟2in column![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)ii𝑖.
       2. **Find the largest subarray with sum 0 in `temp[]`** using a hash map (Prefix Sum + Hash Map technique).
          * Maintain a prefix sum of `temp[]`.
          * If a prefix sum repeats, the subarray between the two occurrences has a sum of 0.
          * Store the indices to calculate the maximum width (column range![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)c1c 1𝑐1to![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)c2c 2𝑐2).
       3. **Calculate Area**:![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)Area=(r2−r1+1)×(c2−c1+1)Area equals open paren r 2 minus r 1 plus 1 close paren cross open paren c 2 minus c 1 plus 1 close parenArea=(𝑟2−𝑟1+1)×(𝑐2−𝑐1+1).
       4. Update `maxArea` if the current area is larger.&#x20;



## <mark style="color:purple;">Two pointer patterns</mark>

### Converging (Sorted Array Target Sum)

* <mark style="color:$success;">Container With Most Water</mark>
* <mark style="color:$success;">3Sum</mark>
* <mark style="color:$success;">3Sum Closest,</mark>
* <mark style="color:$success;">4Sum</mark>
* <mark style="color:$success;">Two Sum II - Input Array Is Sorted</mark>
* <mark style="color:$success;">Intersection of Two Array</mark>
* <mark style="color:$success;">Boats to Save People</mark>
*   <mark style="color:orange;">Squares of a Sorted Array</mark>

    &#x20;       n = len(nums)

    &#x20;       res = \[0] \* n

    &#x20;       left, right = 0, n - 1

    &#x20;       pos = n - 1

    &#x20;       while left <= right:

    &#x20;           if abs(nums\[left]) > abs(nums\[right]):

    &#x20;               res\[pos] = nums\[left] \* nums\[left]

    &#x20;               left += 1

    &#x20;           else:

    &#x20;               res\[pos] = nums\[right] \* nums\[right]

    &#x20;               right -= 1

    &#x20;           pos -= 1

    &#x20;       return res
* <mark style="color:$success;">Sum Smaller</mark>

### Fast & Slow (Cycle Detection)

* <mark style="color:$success;">Linked List Cycle</mark>
*   <mark style="color:$danger;">Happy Number</mark>



    ```python
    class Solution:
        def isHappy(self, n: int) -> bool:
            # Helper function to calculate sum of squares of digits
            def get_next(num):
                total_sum = 0
                while num > 0:
                    num, digit = divmod(num, 10)
                    total_sum += digit ** 2
                return total_sum

            # Initialize fast and slow pointers
            slow = n
            fast = get_next(n)
            
            # Move slow by 1 step and fast by 2 steps
            while fast != 1 and slow != fast:
                slow = get_next(slow)
                fast = get_next(get_next(fast))
            
            # If fast reached 1, it's a happy number
            return fast == 1

    ```
* <mark style="color:$success;">Find the Duplicate Number</mark>

### Fixed Separation (Nth Node from End)

* <mark style="color:$success;">Remove Nth Node From End of List</mark>
* <mark style="color:$success;">Middle of the Linked List</mark>
* <mark style="color:$success;">Delete the Middle Node of a Linked List</mark>

### In-place Array Modification

* <mark style="color:$success;">Remove Duplicates from Sorted Array</mark>
* Remove Element
* Sort Colors
* Remove Duplicates from Sorted Array II
* Move Zeroes
* String Compression
* Sort Array By Parity
* Move Pieces to Obtain a String
* Separate Black and White Balls

### String Comparison with Backspaces

* Backspace String Compare
* Crawler Log Folder
* Removing Stars From a String

### Expanding From Center (Palindromes)

* Longest Palindromic Substring
* Palindromic Substrings

### String Reversal

* Reverse Words in a String
* Reverse String
* Reverse Vowels of a String
* Reverse String II

## Sliding window patterns

### Fixed Size (Subarray Calculation)

* Moving Average from Data Stream
* Maximum Average Subarray I
* Calculate Compressed Mean
* Find the Power of K-Size Subarrays I
* Find X-Sum of All K-Long Subarrays I

### Variable Size (Condition-Based)

* Longest Substring Without Repeating Characters
* Minimum Window Substring,&#x20;
* Minimum Size Subarray Sum
* Contains Duplicate II
* Longest Repeating Character Replacement
* Subarray Product Less Than K
* Fruit Into Baskets
* Max Consecutive Ones III
* Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit
* Longest Subarray of 1's After Deleting One Element
* Minimum Operations to Reduce X to Zero
* Frequency of the Most Frequent Element
* Maximum Sum of Distinct Subarrays With Length K
* Take K of Each Character From Left and Right
* Continuous Subarrays
* Maximum Beauty of an Array After Applying Operation
* Find Longest Special Substring That Occurs Thrice I
* Maximum Good Subarray Sum
* Maximum Frequency of an Element After Performing Operations I
* Maximum Frequency of an Element After Performing Operations II 2

### Monotonic Queue for Max/Min

* Sliding Window Maximum
* Shortest Subarray with Sum at Least K&#x20;
* Jump Game VI

### Character Frequency Matching

* TwoSum
* Find All Anagrams in a String
* Permutation in String



## Linked list in place reversal

<mark style="color:$danger;">reverses parts of linked list without using extra space</mark>

## Monotonic stack

uses a stack to maintain a sequence of elements in a specific order (increasing or decreasing)

* next greated element
* Daily temperatures
* Largest rectance in a histogram

## Overlapping intervals&#x20;

used to merge of handle overlapping intervals in an array

* merge intervals
* insert intervals
* non-overlapping intervals&#x20;

## Modified binary search

Modified Binary Search pattern adapts binary search to solve a wider range of problems, such as finding elements in rotated sorted arrays.

* search in rotated and sorted array
* find minimum in rotated sorteed array
* search in 2D matrix

## Matrix traversal&#x20;

involves elements in a matrix using different techniques (DFS, BFS)

* Flood fill
* Number of islands
* surrounded regions

## Tree traversal pattern (BFS/DFS)

Level Order Traversal

* Binary Tree Level Order Traversal
* Binary Tree Zigzag Level Order Traversal
* Binary Tree Right Side View
* Find Largest Value in Each Tree Row
* Maximum Level Sum of a Binary Tree

Recursive Preorder Traversal

* Same Tree
* Symmetric Tree
* Construct Binary Tree from Preorder and Inorder Traversal
* Flatten Binary Tree to Linked List
* Invert Binary Tree
* Binary Tree Paths
* Smallest String Starting From Leaf

Recursive Inorder Traversal

* Binary Tree Inorder Traversal
* Validate Binary Search Tree
* Binary Search Tree Iterator
* Kth Smallest Element in a BST
* Find Mode in Binary Search Tree
* Minimum Absolute Difference in BST

Recursive Postorder Traversal

* Maximum Depth of Binary Tree
* Balanced Binary Tree
* Binary Tree Maximum Path Sum
* Binary Tree Postorder Traversal
* House Robber III
* Find Leaves of Binary Tree
* Diameter of Binary Tree
* All Nodes Distance K in Binary Tree
* Delete Nodes And Return Forest
* Height of Binary Tree After Subtree Removal Queries

Lowest Common Ancestor (LCA) Finding

* Lowest Common Ancestor of a Binary Search Tree,
* Lowest Common Ancestor of a Binary Tree

&#x20;Serialization and Deserialization

* Serialize and Deserialize Binary Tree
* Subtree of Another Tree
* Find Duplicate Subtrees

## Graph Traversal Patterns (DFS & BFS)

Graph DFS - Connected Components / Island Counting

* Surrounded Regions
* Number of Islands
* Pacific Atlantic Water Flow
* Number of Provinces
* Max Area of Island
* Flood Fill
* Keys and Rooms
* Number of Enclaves
* Number of Closed Islands
* Count Sub Islands
* Detonate the Maximum Bombs

Connected Components / Island Countin

* 01 Matrix
* Rotting Oranges
* Shortest Path in Binary Matrix



Cycle Detection (Directed Graph)

* Course Schedule
* Course Schedule II
* Find Eventual Safe States
* All Paths from Source Lead to Destination

Topological Sort (Kahn's Algorithm)

* Course Schedule II
* Alien Dictionary
* Minimum Height Trees
* Sequence Reconstruction
* &#x20;Parallel Courses
* Largest Color Value in a Directed Graph
* Parallel Courses III
* Find All Possible Recipes from Given Supplies
* Build a Matrix With Conditions

Deep Copy / Cloning

* Clone Graph
* Find the City With the Smallest Number of Neighbors at a Threshold Distance
* Copy List with Random Pointer
* Clone N-ary Tree

Shortest Path (Dijkstra's Algorithm)

* Network Delay Time
* Swim in Rising Water
* Path with Maximum Probability
* Path With Minimum Effort
* Number of Ways to Arrive at Destination
* Second Minimum Time to Reach Destination
* Minimum Weighted Subgraph With the Required Paths
* &#x20;Minimum Obstacle Removal to Reach Corner
* Minimum Time to Visit a Cell In a Grid
* Find the Safest Path in a Grid

Shortest Path (Bellman-Ford / BFS+K)

* Cheapest Flights Within K Stops
* Shortest Path with Alternating Colors

Union-Find (Disjoint Set Union - DSU)

* Number of Islands, 261. Graph Valid Tree,&#x20;
* Number of Islands II
* Number of Connected Components in an Undirected Graph,
* Number of Provinces
* Redundant Connection
* Accounts Merge
* Sentence Similarity II
* Most Stones Removed with Same Row or Column
* Largest Component Size by Common Factor
* &#x20;Regions Cut By Slashes
* The Earliest Moment When Everyone Become Friends

Strongly Connected Components (Kosaraju / Tarjan)

* Course Schedule II, 547. Number of Provinces
* Critical Connections in a Network
* &#x20;Maximum Employees to Be Invited to a Meeting

Bridges & Articulation Points (Tarjan low-link

* Critical Connections in a Network
* Longest Cycle in a Graph

Minimum Spanning Tree (Kruskal / Prim / DSU + heap)

* Connecting Cities With Minimum Cost
* Min Cost to Connect All Points
* Optimize Water Distribution in a Village
* Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree

&#x20;Bidirectional BFS (BFS optimisation for known source & target

* Word Ladder
* Word Ladder II
* Bus Routes

## Dynamic Programming (DP) Patterns

* 1D Array (Fibonacci Style)
* 1D Array (Kadane's Algorithm for Max/Min Subarray)
* 1D Array (Coin Change / Unbounded Knapsack Style)
* 1D Array (0/1 Knapsack Subset Sum Style)
* 1D Array (Word Break Style)
* 1D Array (Longest Common Subsequence - LCS)
* 2D Array (Edit Distance / Levenshtein Distance)
* 2D Array (Unique Paths on Grid)
* interval DP
* Catalan Numbers
* Longest Increasing Subsequence (LIS)
* Stock problems

## Heap (Priority Queue) Patterns

Top K Elements (Selection/Frequency)

Two Heaps for Median Finding

K-way Merge

Scheduling / Minimum Cost (Greedy with Priority Queue)

## Backtracking Patterns

Subsets (Include/Exclude)

Permutations

Combination Sum

Parentheses Generation

Word Search / Path Finding in Grid

N-Queens / Constraint Satisfaction

Palindrome Partitioning

## Greedy Patterns

Interval Merging/Scheduling

Jump Game Reachability/Minimization

Buy/Sell Stock

Gas Station Circuit

Task Scheduling (Frequency Based)

Sorting Based

## Binary Search Patterns

On Sorted Array/List

* Find Min/Max in Rotated Sorted Array
* On Answer / Condition Function
* Find First/Last Occurrence
* Median / Kth across Two Sorted Arrays

## Stack Patterns

Valid Parentheses Matching

* Valid Parentheses
* Longest Valid Parentheses
* Minimum Add to Make Parentheses Valid
* Minimum Remove to Make Valid Parentheses
* Minimum Number of Swaps to Make the String Balanced

Monotonic Stack

* Remove K Digits
* Next Greater Element I
* Next Greater Element II
* Daily Temperatures
* Online Stock Span
* Sum of Subarray Minimums
* Maximum Width Ramp
* Final Prices With a Special Discount in a Shop
* Find the Most Competitive Subsequence

Expression Evaluation (RPN/Infix)

* Evaluate Reverse Polish Notation
* Basic Calculator
* Basic Calculator II
* Basic Calculator III

Simulation / Backtracking Helper

* Simplify Path
* Decode String
* Asteroid Collision

Min Stack Design

* Min Stack
* Maximum Frequency Stack
* &#x20;Online Stock Span

Largest Rectangle in Histogram

* Largest Rectangle in Histogram
* Maximal Rectangle

## Bit Manipulation Patterns

* Bitwise XOR - Finding Single/Missing Number
* Single Number
* Single Number II
* Missing Number,
* Find the Difference
* Bitwise AND - Counting Set Bits (Hamming Weight
* Number of 1 Bits,
* Power of Two
* Total Hamming Distance
* Bitwise DP - Counting Bits Optimization
* Counting Bits
* Parallel Courses II
* Count Triplets That Can Form Two Arrays of Equal XOR
* Bitwise Operations - Power of Two/Four Check
* Power of Two
* Power of Four

## Linked List Manipulation Patterns

In-place Reversal

* Remove Duplicates from Sorted List
* Reverse Linked List II
* Reverse Linked List
* Reverse Nodes in k-Group
* Palindrome Linked List
* Remove Duplicates from Sorted List II

Merging Two Sorted Lists

* Merge Two Sorted Lists
* Merge k Sorted Lists

Addition of Numbers

* Add Two Numbers
* Plus One Linked List

Intersection Detection

* Intersection of Two Linked Lists
* Minimum Index Sum of Two Lists

Reordering / Partitioning

* Swap Nodes in Pairs
* Rotate List&#x20;
* Partition List
* Reorder List
* Odd Even Linked List

## Array/Matrix Manipulation Patterns

In-place Rotation

* Rotate Image
* Rotate Array,
* Transpose Matrix

Spiral Traversal

* Spiral Matrix
* Spiral Matrix II
* Spiral Matrix III
* Spiral Matrix IV

Set Matrix Zeroes (In-place Marking)

* Set Matrix Zeroes
* Game of Life
* Diagonal Traverse

Product Except Self (Prefix/Suffix Products)

* Product of Array Except Self
* Longest Mountain in Array
  * Minimum Penalty for a Shop

Plus One (Handling Carry)

* Plus One
* Multiply Strings
* Add to Array-Form of Integer
* Add Binary

Merge Sorted Array (In-place from End)

* Merge Sorted Array
* Squares of a Sorted Array

Cyclic Sort

* First Missing Positive
* Missing Number
* Find the Duplicate Number&#x20;
* Find All Duplicates in an Array
* Find All Numbers Disappeared in an Array

## String Manipulation Patterns

### Palindrome Check (Two Pointers / Reverse)

* Palindrome Number
* Valid Palindrome,
* Valid Palindrome II

### Anagram Check (Frequency Count/Sort)

* Group Anagrams
* Valid Anagram

### Roman to Integer Conversion

* Roman to Integer
* Integer to Roman

### String to Integer (atoi)

* String to Integer (atoi),
* Valid Number

Multiply Strings (Manual Simulation)

* Multiply Strings
* Add Strings
* Add Binary

String Matching - Naive / KMP / Rabin-Karp

* Find the Index of the First Occurrence in a String
* Shortest Palindrome
* Repeated String Match
* Rotate String
* Find Beautiful Indices in the Given Array II

Repeated Substring Pattern Detection

* Repeated Substring Pattern
* Find the Index of the First Occurrence in a String
* Repeated String Match

## Design Patterns

* Design (General/Specific)
* Tries
