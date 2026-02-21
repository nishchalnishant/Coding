# Common patterns thita.ai

Common patterns used in DSA



## Two pointer patterns

*   **Two Pointers - Converging (Sorted Array Target Sum)**

    Use two pointers moving towards each other to solve target sum problems

    * **Container With Most Water**
      * The logic is essentially: "I've maximized the width, and the current height is capped by this short line. I can't do any better with this short line, so I'll move it inward and hope to find a taller one."

```python
class Solution:
    def maxArea(self, height: list[int]) -> int:
        i = 0
        j = len(height) - 1
        res = 0

        while i < j:
            res = max(res, (j - i) * min(height[i], height[j]))
            if height[i] < height[j]:
                i += 1
            else:
                j -= 1

        return res
```

* **3Sum**

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort()

        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            
            j = i + 1
            k = len(nums) - 1

            while j < k:
                total = nums[i] + nums[j] + nums[k]

                if total > 0:
                    k -= 1
                elif total < 0:
                    j += 1
                else:
                    res.append([nums[i], nums[j], nums[k]])
                    j += 1

                    while nums[j] == nums[j-1] and j < k:
                        j += 1
        
        return res
```



* **3Sum Closest**

```python
class Solution(object):
    def threeSumClosest(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        nums.sort()
        closest_sum = float('inf')
        min_diff = float('inf')

        for i in range(len(nums) - 2):
            left, right = i + 1, len(nums) - 1

            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]
                current_diff = abs(current_sum - target)

                if current_diff < min_diff:
                    min_diff = current_diff
                    closest_sum = current_sum

                if current_sum < target:
                    left += 1
                else:
                    right -= 1

        return closest_sum
```

* **4Sum**

```python
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        n = len(nums)
        seen = set()
        ans = set()
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    lastNumber = target - nums[i] - nums[j] - nums[k]
                    if lastNumber in seen:
                        arr = sorted([nums[i], nums[j], nums[k], lastNumber])
                        ans.add((arr[0], arr[1], arr[2], arr[3]))
            seen.add(nums[i])
        return ans
```

* <mark style="color:$success;">Two Sum II - Input Array Is Sorted</mark>
  * <mark style="color:$info;">simple two pointer approach</mark>



* **Intersection of Two Arrays**
  * normal dictionary approach to solve these two
* **Boats to Save People**
  * simple two pointer
* <mark style="color:$danger;">Squares of a Sorted Array</mark>

```python
def sortedSquares(self, nums: List[int]) -> List[int]:
        res = [0] * len(nums)
        left = 0
        right = len(nums) - 1

        for i in range(len(nums) - 1, -1, -1):
            if abs(nums[left]) > abs(nums[right]):
                res[i] = nums[left] ** 2
                left += 1
            else:
                res[i] = nums[right] ** 2
                right -= 1
        
        return res

```



* **3Sum Smaller**
*
*   **Two Pointers - Fast & Slow (Cycle Detection)**

    Floyd's cycle detection algorithm using fast and slow pointers

    * Linked List Cycle
    * Linked List Cycle
    * Find the Duplicate Number
    * **Is Subsequence**


*   **Two Pointers - Fixed Separation (Nth Node from End)**

    Maintain fixed distance between pointers to find nth element from end

    * **Remove Nth Node From End of List**
    * **Middle of the Linked List**
    * **Delete the Middle Node of a Linked List**<br>
*   **Two Pointers - In-place Array Modification**

    Modify arrays in-place using two pointers technique

    * **Remove Duplicates from Sorted Array**
    * **Remove Element**
    * **Sort Colors**
    * **Remove Duplicates from Sorted Array II**
    * **Move Zeroes**
    * **String Compression**
    * **Sort Array By Parity**
    * **Move Pieces to Obtain a String**
    * **Separate Black and White Balls**<br>
*   **Two Pointers - String Comparison with Backspaces**

    Handle string modifications with backspace operations

    * **Backspace String Compare**
    * **Crawler Log Folder**<br>
*   **Two Pointers - Expanding From Center (Palindromes)**

    Find palindromes by expanding from center outwards

    * **Longest Palindromic Substring**
    * **Palindromic Substrings**


*   **Two Pointers - String Reversal**

    Reverse strings or parts of strings using two pointers&#x20;

    * **Reverse Words in a String**
    * **Reverse String**
    * **Reverse Vowels of a String**
    * **Reverse String II**

## Sliding window patterns

*   **Sliding Window - Fixed Size (Subarray Calculation)**

    Fixed-size sliding window for calculating metrics over subarrays

    * **Moving Average from Data Stream**
    * **Maximum Average Subarray I**
    * **Calculate Compressed Mean**
    * **Find the Power of K-Size Subarrays I**
    * **Find X-Sum of All K-Long Subarrays I**


*   **Sliding Window - Variable Size (Condition-Based)**

    Variable-size sliding window that expands/contracts based on conditions

    * **Longest Substring Without Repeating Characters**
    * **Minimum Window Substring**
    * **Minimum Size Subarray Sum**
    * **Contains Duplicate II**
    * **Longest Repeating Character Replacement**
    * **Subarray Product Less Than K**
    * **Fruit Into Baskets**
    * **Max Consecutive Ones III**
    * **Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit**
    * **Longest Subarray of 1's After Deleting One Element**
    * **Minimum Operations to Reduce X to Zero**
    * **Frequency of the Most Frequent Element**
    * **Maximum Sum of Distinct Subarrays With Length K**
    * **Take K of Each Character From Left and Right**
    * **Continuous Subarrays**
    * **Maximum Beauty of an Array After Applying Operation**
    * **Find Longest Special Substring That Occurs Thrice I**
    * **Maximum Good Subarray Sum**
    * **Maximum Frequency of an Element After Performing Operations I**
    *   **Maximum Frequency of an Element After Performing Operations II**


*   **Sliding Window - Monotonic Queue for Max/Min**

    Use monotonic deque to efficiently track max/min in sliding window

    * **Sliding Window Maximum**
    * <mark style="color:$danger;">Shortest Subarray with Sum at Least K</mark>
    * **Jump Game VI**<br>
*   **Sliding Window - Character Frequency Matching**

    Match character frequencies within sliding windows

    * **Find All Anagrams in a String**
    * **Permutation in String**

## Tree Traversal patterns (BFS/DFS)

*   **Tree BFS - Level Order Traversal**

    Breadth-first traversal to process trees level by level

    * **Binary Tree Level Order Traversal**
    * **Binary Tree Zigzag Level Order Traversal**
    * **Binary Tree Right Side View**
      * We perform a level-order traversal using a queue. For every level, we record the **last node** processed. This gives us the rightmost node at that depth.
    * **Find Largest Value in Each Tree Row**
    * **Maximum Level Sum of a Binary Tree**
    *



```python
def levelOrder(root):
    if root is None:
        return []
    
    result = []
    queue = deque([root])  # Use a queue to store nodes
    
    while queue:
        level_size = len(queue)
        level_nodes = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level_nodes.append(node.data)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level_nodes)
    
    return result


```

```python
# Recursive Level Order Traversal
def levelOrderRecursive(root):
    h = height(root)
    result = []
    for i in range(1, h + 1):
        level_nodes = []
        printCurrentLevel(root, i, level_nodes)
        result.append(level_nodes)
    return result
```

*   **Tree DFS - Recursive Preorder Traversal**

    Process root before children in depth-first traversal

    * **Same Tree**
    * **Symmetric Tree**
    * **Construct Binary Tree from Preorder and Inorder Traversal**
    * **Flatten Binary Tree to Linked List**
    * **Invert Binary Tree**
    * **Binary Tree Paths**
    * **Smallest String Starting From Leaf**

```python
# Recursive Preorder Traversal
def preorderTraversal(root):
    if root is None:
        return []
    
    result = []
    
    # Visit root
    result.append(root.data)
    
    # Recur on left subtree
    result += preorderTraversal(root.left)
    
    # Recur on right subtree
    result += preorderTraversal(root.right)
    
    return result

```

*   **Tree DFS - Recursive Inorder Traversal**

    Process nodes in sorted order for BST

    * **Binary Tree Inorder Traversal**
    * **Validate Binary Search Tree**
    * **Binary Search Tree Iterator**
    * **Kth Smallest Element in a BST**
    * **Find Mode in Binary Search Tree**
    * **Minimum Absolute Difference in BST**

```python
def inorderTraversal(root):
    if root is None:
        return []
    
    result = []
    
    # Traverse left subtree
    result += inorderTraversal(root.left)
    
    # Visit root
    result.append(root.data)
    
    # Traverse right subtree
    result += inorderTraversal(root.right)
    
    return result
```



*   **Tree DFS - Recursive Postorder Traversal**

    Process children before root in depth-first traversal

    * **Maximum Depth of Binary Tree**
    * **Balanced Binary Tree**
    * **Binary Tree Maximum Path Sum**
    * **Binary Tree Postorder Traversal**
    * **House Robber III**
    * **Find Leaves of Binary Tree**
    * **Diameter of Binary Tree**
    * **All Nodes Distance K in Binary Tree**
    * **Delete Nodes And Return Forest**
    * **Height of Binary Tree After Subtree Removal Queries**

```python
# Recursive Postorder Traversal
def postorderTraversal(root):
    if root is None:
        return []
    
    result = []
    
    # Traverse left subtree
    result += postorderTraversal(root.left)
    
    # Traverse right subtree
    result += postorderTraversal(root.right)
    
    # Visit root
    result.append(root.data)
    
    return result
```



*   **Tree - Lowest Common Ancestor (LCA) Finding**

    Find the lowest common ancestor of two nodes

    * **Lowest Common Ancestor of a Binary Search Tree**
    * **Lowest Common Ancestor of a Binary Tree**

```python
def findLCA(root, n1, n2):
    # Base Case
    if root is None:
        return None

    # If either n1 or n2 matches the root, report the root
    if root.data == n1 or root.data == n2:
        return root

    # Look for keys in left and right subtrees
    left_lca = findLCA(root.left, n1, n2)
    right_lca = findLCA(root.right, n1, n2)

    # If both sides return non-null, this node is the LCA
    if left_lca and right_lca:
        return root

    # Otherwise return the non-null value
    return left_lca if left_lca else right_lca

```



*   **Tree - Serialization and Deserialization**

    Convert trees to/from string representation

    * **Serialize and Deserialize Binary Tree**
    * **Subtree of Another Tree**
    * **Find Duplicate Subtrees**

## Graph traversal patterns (DFS/BFS)

*   **Graph DFS - Connected Components / Island Counting**

    Use DFS to find connected components in graphs
*   **Graph BFS - Connected Components / Island Counting**

    Use BFS to find connected components and shortest paths
*   **Graph DFS - Cycle Detection (Directed Graph)**

    Detect cycles in directed graphs using DFS
*   **Graph BFS - Topological Sort (Kahn's Algorithm)**

    Topological ordering using BFS and in-degree tracking
*   **Graph - Deep Copy / Cloning**

    Create deep copies of graph structures
*   **Graph - Shortest Path (Dijkstra's Algorithm)**

    Find shortest paths in weighted graphs
*   **Graph - Shortest Path (Bellman-Ford / BFS+K)**

    Shortest paths with constraints or negative edges
*   **Graph - Union-Find (Disjoint Set Union - DSU)**

    Efficiently track connected components with Union-Find
*   **Graph - Strongly Connected Components (Kosaraju / Tarjan)**

    Find strongly connected components in directed graphs
*   **Graph - Bridges & Articulation Points (Tarjan low-link)**

    Find critical edges and vertices in graphs
*   **Graph - Minimum Spanning Tree (Kruskal / Prim / DSU + heap)**

    Find minimum cost to connect all vertices
*   **Graph - Bidirectional BFS (BFS optimization for known source & target)**

    Optimize BFS by searching from both ends

    <br>

## Dynamic programming (DP) Patterns

*   **DP - 1D Array (Fibonacci Style)**

    Simple 1D DP with recurrence relations
*   **DP - 1D Array (Kadane's Algorithm for Max/Min Subarray)**

    Find maximum/minimum subarray using Kadane's algorithm
*   **DP - 1D Array (Coin Change / Unbounded Knapsack Style)**

    Unbounded knapsack problems with unlimited item usage
*   **DP - 1D Array (0/1 Knapsack Subset Sum Style)**

    0/1 knapsack where each item can be used once
*   **DP - 1D Array (Word Break Style)**

    String partitioning and word segmentation problems
*   **DP - 2D Array (Longest Common Subsequence - LCS)**

    2D DP for comparing two sequences
*   **DP - 2D Array (Edit Distance / Levenshtein Distance)**

    Calculate minimum operations to transform one string to another
*   **DP - 2D Array (Unique Paths on Grid)**

    Grid-based DP for counting paths and finding optimal paths
*   **DP - Interval DP**

    DP on intervals and ranges
*   **DP - Catalan Numbers**

    Problems involving Catalan number sequences
*   **DP - Longest Increasing Subsequence (LIS)**

    Find longest increasing subsequences with optimizations
*   **DP - Stock problems**

    Stock trading problems with various constraints

## Heap (priority queue) patterns

*   **Heap - Top K Elements (Selection/Frequency)**

    Find top K elements efficiently using heaps
*   **Heap - Two Heaps for Median Finding**

    Use two heaps to efficiently track median
*   **Heap - K-way Merge**

    Merge multiple sorted data structures efficiently
*   **Heap - Scheduling / Minimum Cost (Greedy with Priority Queue)**

    Scheduling and optimization problems using priority queues

## Backtracking patterns&#x20;

*   **Backtracking - Subsets (Include/Exclude)**

    Generate all possible subsets using include/exclude decisions
*   **Backtracking - Permutations**

    Generate permutations and handle permutation logic
*   **Backtracking - Combination Sum**

    Find combinations that sum to target values
*   **Backtracking - Parentheses Generation**

    Generate valid parentheses combinations
*   **Backtracking - Word Search / Path Finding in Grid**

    Search for words or paths in 2D grids
*   **Backtracking - N-Queens / Constraint Satisfaction**

    Solve constraint satisfaction problems with backtracking
*   **Backtracking - Palindrome Partitioning**

    Partition strings into palindromic subsequences

## Greedy patterns

*   **Greedy - Interval Merging/Scheduling**

    Optimal scheduling and interval manipulation
*   **Greedy - Jump Game Reachability/Minimization**

    Determine reachability and minimum jumps in arrays
*   **Greedy - Buy/Sell Stock**

    Maximize profit in stock trading scenarios
*   **Greedy - Gas Station Circuit**

    Find starting points for circular traversal problems
*   **Greedy - Task Scheduling (Frequency Based)**

    Schedule tasks to avoid conflicts based on frequencies
*   **Greedy - Sorting Based**

    Sorting-based greedy solutions for optimization

## Binary search patterns

*   **Binary Search - On Sorted Array/List**

    Standard binary search on sorted arrays
*   **Binary Search - Find Min/Max in Rotated Sorted Array**

    Binary search in rotated or mountain arrays
*   **Binary Search - On Answer / Condition Function**

    Binary search on answer space with condition checking
*   **Binary Search - Find First/Last Occurrence**

    Find boundaries and ranges in sorted arrays
*   **Binary Search - Median and Kth of Two Sorted Arrays**

    Advanced binary search for median and kth element problems

## Stack patterns

*   **Stack - Valid Parentheses Matching**

    Validate and manipulate parentheses using stack
*   **Stack - Monotonic Stack**

    Maintain monotonic property in stack for next greater/smaller elements
*   **Stack - Expression Evaluation (RPN/Infix)**

    Evaluate mathematical expressions using stack
*   **Stack - Simulation / Backtracking Helper**

    Use stack to simulate processes and track state
*   **Stack - Min Stack Design**

    Design stacks with additional functionality
*   **Stack - Largest Rectangle in Histogram**

    Find largest rectangular areas using stack

## Bit manipulation patterns

*   **Bitwise XOR - Finding Single/Missing Number**

    Use XOR properties to find unique or missing elements
*   **Bitwise AND - Counting Set Bits (Hamming Weight)**

    Count set bits and analyze bit patterns
*   **Bitwise DP - Counting Bits Optimization**

    Dynamic programming with bitwise operations
*   **Bitwise Operations - Power of Two/Four Check**

    Check for powers of 2 and 4 using bit manipulation

## Linked list manipulation patterns

*   **Linked List - In-place Reversal**

    Reverse linked lists in-place without extra space
*   **Linked List - Merging Two Sorted Lists**

    Merge sorted linked lists efficiently
*   **Linked List - Addition of Numbers**

    Perform arithmetic operations on linked list numbers
*   **Linked List - Intersection Detection**

    Find intersections and common elements in linked lists
*   **Linked List - Reordering / Partitioning**

    Reorder and partition linked lists based on criteria

## Array matrix  manipulation patterns

*   **Array/Matrix - In-place Rotation**

    Rotate arrays and matrices in-place
*   **Array/Matrix - Spiral Traversal**

    Traverse matrices in spiral patterns
*   **Array/Matrix - Set Matrix Zeroes (In-place Marking)**

    Modify matrices in-place using marking techniques
*   **Array - Product Except Self (Prefix/Suffix Products)**

    Calculate products excluding current element using prefix/suffix
*   **Array - Plus One (Handling Carry)**

    Handle carry propagation in array arithmetic
*   **Array - Merge Sorted Array (In-place from End)**

    Merge sorted arrays efficiently from the end
*   **Array - Cyclic Sort**

    Sort arrays by placing elements at their correct indices

## String manipulation patterns

*   **String - Palindrome Check (Two Pointers / Reverse)**

    Check for palindromes using two pointers or reversal
*   **String - Anagram Check (Frequency Count/Sort)**

    Check for anagrams using character frequency or sorting
*   **String - Roman to Integer Conversion/ String to Integer (atoi)**

    Convert between string and integer representations
*   **String - Multiply Strings/Add Strings (Manual Simulation)**

    Simulate arithmetic operations on string numbers
*   **String Matching - Naive / KMP / Rabin-Karp**

    Efficient string matching algorithms
*   **String - Repeated Substring Pattern Detection**

    Detect repeating patterns within strings

## Design patterns

*   **Design (General/Specific)**

    Design and implement custom data structures and systems
*   **Tries**

    Implement and use trie data structures for string operations





Common patterns used in DSA



## Two pointer patterns

*   **Two Pointers - Converging (Sorted Array Target Sum)**

    Use two pointers moving towards each other to solve target sum problems

    * **Container With Most Water**
    * **3Sum**
    * **3Sum Closest**
    * **4Sum**
    * Two Sum II - Input Array Is Sorted
    * **Intersection of Two Arrays**
    * **Boats to Save People**
    * **Squares of a Sorted Array**
    * **3Sum Smaller**
*   **Two Pointers - Fast & Slow (Cycle Detection)**

    Floyd's cycle detection algorithm using fast and slow pointers

    * Linked List Cycle
    * **Happy Number**
    * **Find the Duplicate Number**
    * **Is Subsequence**
*   **Two Pointers - Fixed Separation (Nth Node from End)**

    Maintain fixed distance between pointers to find nth element from end

    *   **Remove Nth Node From End of List**

        <br>
*   **Two Pointers - In-place Array Modification**

    Modify arrays in-place using two pointers technique
*   **Two Pointers - String Comparison with Backspaces**

    Handle string modifications with backspace operations
*   **Two Pointers - Expanding From Center (Palindromes)**

    Find palindromes by expanding from center outwards
*   **Two Pointers - String Reversal**

    Reverse strings or parts of strings using two pointers&#x20;

## Sliding window patterns

*   **Sliding Window - Fixed Size (Subarray Calculation)**

    Fixed-size sliding window for calculating metrics over subarrays
*   **Sliding Window - Variable Size (Condition-Based)**

    Variable-size sliding window that expands/contracts based on conditions
*   **Sliding Window - Monotonic Queue for Max/Min**

    Use monotonic deque to efficiently track max/min in sliding window
*   **Sliding Window - Character Frequency Matching**

    Match character frequencies within sliding windows

## Tree Traversal patterns (BFS/DFS)

*   **Tree BFS - Level Order Traversal**

    Breadth-first traversal to process trees level by level
*   **Tree DFS - Recursive Preorder Traversal**

    Process root before children in depth-first traversal
*   **Tree DFS - Recursive Inorder Traversal**

    Process nodes in sorted order for BST
*   **Tree DFS - Recursive Postorder Traversal**

    Process children before root in depth-first traversal
*   **Tree - Lowest Common Ancestor (LCA) Finding**

    Find the lowest common ancestor of two nodes
*   **Tree - Serialization and Deserialization**

    Convert trees to/from string representation

## Graph traversal patterns (DFS/BFS)

*   **Graph DFS - Connected Components / Island Counting**

    Use DFS to find connected components in graphs
*   **Graph BFS - Connected Components / Island Counting**

    Use BFS to find connected components and shortest paths
*   **Graph DFS - Cycle Detection (Directed Graph)**

    Detect cycles in directed graphs using DFS
*   **Graph BFS - Topological Sort (Kahn's Algorithm)**

    Topological ordering using BFS and in-degree tracking
*   **Graph - Deep Copy / Cloning**

    Create deep copies of graph structures
*   **Graph - Shortest Path (Dijkstra's Algorithm)**

    Find shortest paths in weighted graphs
*   **Graph - Shortest Path (Bellman-Ford / BFS+K)**

    Shortest paths with constraints or negative edges
*   **Graph - Union-Find (Disjoint Set Union - DSU)**

    Efficiently track connected components with Union-Find
*   **Graph - Strongly Connected Components (Kosaraju / Tarjan)**

    Find strongly connected components in directed graphs
*   **Graph - Bridges & Articulation Points (Tarjan low-link)**

    Find critical edges and vertices in graphs
*   **Graph - Minimum Spanning Tree (Kruskal / Prim / DSU + heap)**

    Find minimum cost to connect all vertices
*   **Graph - Bidirectional BFS (BFS optimization for known source & target)**

    Optimize BFS by searching from both ends

    <br>

## Dynamic programming (DP) Patterns

*   **DP - 1D Array (Fibonacci Style)**

    Simple 1D DP with recurrence relations
*   **DP - 1D Array (Kadane's Algorithm for Max/Min Subarray)**

    Find maximum/minimum subarray using Kadane's algorithm
*   **DP - 1D Array (Coin Change / Unbounded Knapsack Style)**

    Unbounded knapsack problems with unlimited item usage
*   **DP - 1D Array (0/1 Knapsack Subset Sum Style)**

    0/1 knapsack where each item can be used once
*   **DP - 1D Array (Word Break Style)**

    String partitioning and word segmentation problems
*   **DP - 2D Array (Longest Common Subsequence - LCS)**

    2D DP for comparing two sequences
*   **DP - 2D Array (Edit Distance / Levenshtein Distance)**

    Calculate minimum operations to transform one string to another
*   **DP - 2D Array (Unique Paths on Grid)**

    Grid-based DP for counting paths and finding optimal paths
*   **DP - Interval DP**

    DP on intervals and ranges
*   **DP - Catalan Numbers**

    Problems involving Catalan number sequences
*   **DP - Longest Increasing Subsequence (LIS)**

    Find longest increasing subsequences with optimizations
*   **DP - Stock problems**

    Stock trading problems with various constraints

## Heap (priority queue) patterns

*   **Heap - Top K Elements (Selection/Frequency)**

    Find top K elements efficiently using heaps
*   **Heap - Two Heaps for Median Finding**

    Use two heaps to efficiently track median
*   **Heap - K-way Merge**

    Merge multiple sorted data structures efficiently
*   **Heap - Scheduling / Minimum Cost (Greedy with Priority Queue)**

    Scheduling and optimization problems using priority queues

## Backtracking patterns&#x20;

*   **Backtracking - Subsets (Include/Exclude)**

    Generate all possible subsets using include/exclude decisions
*   **Backtracking - Permutations**

    Generate permutations and handle permutation logic
*   **Backtracking - Combination Sum**

    Find combinations that sum to target values
*   **Backtracking - Parentheses Generation**

    Generate valid parentheses combinations
*   **Backtracking - Word Search / Path Finding in Grid**

    Search for words or paths in 2D grids
*   **Backtracking - N-Queens / Constraint Satisfaction**

    Solve constraint satisfaction problems with backtracking
*   **Backtracking - Palindrome Partitioning**

    Partition strings into palindromic subsequences

## Greedy patterns

*   **Greedy - Interval Merging/Scheduling**

    Optimal scheduling and interval manipulation
*   **Greedy - Jump Game Reachability/Minimization**

    Determine reachability and minimum jumps in arrays
*   **Greedy - Buy/Sell Stock**

    Maximize profit in stock trading scenarios
*   **Greedy - Gas Station Circuit**

    Find starting points for circular traversal problems
*   **Greedy - Task Scheduling (Frequency Based)**

    Schedule tasks to avoid conflicts based on frequencies
*   **Greedy - Sorting Based**

    Sorting-based greedy solutions for optimization

## Binary search patterns

*   **Binary Search - On Sorted Array/List**

    Standard binary search on sorted arrays
*   **Binary Search - Find Min/Max in Rotated Sorted Array**

    Binary search in rotated or mountain arrays
*   **Binary Search - On Answer / Condition Function**

    Binary search on answer space with condition checking
*   **Binary Search - Find First/Last Occurrence**

    Find boundaries and ranges in sorted arrays
*   **Binary Search - Median and Kth of Two Sorted Arrays**

    Advanced binary search for median and kth element problems

## Stack patterns

*   **Stack - Valid Parentheses Matching**

    Validate and manipulate parentheses using stack
*   **Stack - Monotonic Stack**

    Maintain monotonic property in stack for next greater/smaller elements
*   **Stack - Expression Evaluation (RPN/Infix)**

    Evaluate mathematical expressions using stack
*   **Stack - Simulation / Backtracking Helper**

    Use stack to simulate processes and track state
*   **Stack - Min Stack Design**

    Design stacks with additional functionality
*   **Stack - Largest Rectangle in Histogram**

    Find largest rectangular areas using stack

## Bit manipulation patterns

*   **Bitwise XOR - Finding Single/Missing Number**

    Use XOR properties to find unique or missing elements
*   **Bitwise AND - Counting Set Bits (Hamming Weight)**

    Count set bits and analyze bit patterns
*   **Bitwise DP - Counting Bits Optimization**

    Dynamic programming with bitwise operations
*   **Bitwise Operations - Power of Two/Four Check**

    Check for powers of 2 and 4 using bit manipulation

## Linked list manipulation patterns

*   **Linked List - In-place Reversal**

    Reverse linked lists in-place without extra space
*   **Linked List - Merging Two Sorted Lists**

    Merge sorted linked lists efficiently
*   **Linked List - Addition of Numbers**

    Perform arithmetic operations on linked list numbers
*   **Linked List - Intersection Detection**

    Find intersections and common elements in linked lists
*   **Linked List - Reordering / Partitioning**

    Reorder and partition linked lists based on criteria

## Array matrix  manipulation patterns

*   **Array/Matrix - In-place Rotation**

    Rotate arrays and matrices in-place
*   **Array/Matrix - Spiral Traversal**

    Traverse matrices in spiral patterns
*   **Array/Matrix - Set Matrix Zeroes (In-place Marking)**

    Modify matrices in-place using marking techniques
*   **Array - Product Except Self (Prefix/Suffix Products)**

    Calculate products excluding current element using prefix/suffix
*   **Array - Plus One (Handling Carry)**

    Handle carry propagation in array arithmetic
*   **Array - Merge Sorted Array (In-place from End)**

    Merge sorted arrays efficiently from the end
*   **Array - Cyclic Sort**

    Sort arrays by placing elements at their correct indices

## String manipulation patterns

*   **String - Palindrome Check (Two Pointers / Reverse)**

    Check for palindromes using two pointers or reversal
*   **String - Anagram Check (Frequency Count/Sort)**

    Check for anagrams using character frequency or sorting
*   **String - Roman to Integer Conversion/ String to Integer (atoi)**

    Convert between string and integer representations
*   **String - Multiply Strings/Add Strings (Manual Simulation)**

    Simulate arithmetic operations on string numbers
*   **String Matching - Naive / KMP / Rabin-Karp**

    Efficient string matching algorithms
*   **String - Repeated Substring Pattern Detection**

    Detect repeating patterns within strings

## Design patterns

*   **Design (General/Specific)**

    Design and implement custom data structures and systems
*   **Tries**

    Implement and use trie data structures for string operations
