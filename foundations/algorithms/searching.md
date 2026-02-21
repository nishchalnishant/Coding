# Searching

#### **Detailed Summary of Searching (Algorithms)**

**Searching** algorithms are used to retrieve or locate a specific item from a collection of items. These items could be stored in an array, list, or database. The efficiency of a searching algorithm depends on how the data is organized and the characteristics of the algorithm. Searching can generally be classified into **two main categories**: **Linear Searching** and **Binary Searching**.

**1. Linear Search:**

* **Definition**: In a linear search, each element in the data set is checked sequentially to find the target. The search starts at the first element and moves through the list until the target is found or the list is exhausted.
* **Time Complexity**: O(n) in the worst case, where `n` is the number of elements.
* **Advantages**: Simple to implement; works well with small datasets and unsorted data.
* **Disadvantages**: Inefficient for large datasets due to its linear time complexity.

**2. Binary Search:**

* **Definition**: Binary search is a more efficient search algorithm that works on sorted data. The algorithm repeatedly divides the search space in half, comparing the target value to the middle element, and discarding half of the elements each time.
* **Precondition**: The data must be sorted before applying binary search.
* **Time Complexity**: O(log n) in the worst case.
* **Advantages**: Much more efficient than linear search for large datasets.
* **Disadvantages**: Only applicable to sorted data.

**Variants of Binary Search:**

* **Lower Bound Search**: Finds the first occurrence of the target element.
* **Upper Bound Search**: Finds the last occurrence of the target element.
* **Binary Search on Answer**: A variation used in optimization problems where the solution space is binary searched to find the optimal answer (e.g., minimizing or maximizing a parameter).

**3. Interpolation Search:**

* **Definition**: Similar to binary search but instead of always checking the middle element, it estimates the position of the target using the values of the first and last elements.
* **Time Complexity**: O(log log n) in the best case (for uniformly distributed data); O(n) in the worst case.
* **Precondition**: Data must be sorted and uniformly distributed for good performance.
* **Advantages**: Faster than binary search for uniformly distributed data.
* **Disadvantages**: Less efficient if the data is not uniformly distributed.

**4. Jump Search:**

* **Definition**: Jump search divides the data set into blocks of fixed size `m` and skips `m` elements at a time. When the target seems to be found in a block, linear search is applied within that block.
* **Time Complexity**: O(√n) in the worst case.
* **Advantages**: Faster than linear search for larger datasets.
* **Disadvantages**: Requires sorted data; not as fast as binary search.

**5. Exponential Search:**

* **Definition**: Used to find the range where the target might be, and then binary search is applied within that range. It starts by searching elements at exponentially increasing indices (1, 2, 4, 8, etc.) until the range containing the target is found.
* **Time Complexity**: O(log n) in the worst case.
* **Advantages**: Efficient when the target is near the beginning of the list.
* **Disadvantages**: Only works on sorted arrays.

**6. Ternary Search:**

* **Definition**: A variation of binary search that divides the array into three parts instead of two and recursively searches in the appropriate section.
* **Time Complexity**: O(log₃ n) in the worst case.
* **Advantages**: Slightly faster than binary search in theory but requires more comparisons in practice.
* **Disadvantages**: More complex than binary search and not widely used in practice.

**7. Search Algorithms in Trees:**

* **Binary Search Tree (BST) Search**: Searches for a value in a Binary Search Tree, where left children are smaller and right children are larger than the parent node. Time complexity: O(log n) in a balanced tree and O(n) in a skewed tree.
* **Depth-First Search (DFS)** and **Breadth-First Search (BFS)**: Though these are primarily traversal algorithms, they can also be used for searching in graphs and trees.

**Applications of Searching:**

* **Database indexing** for fast retrieval of data.
* **Search engines** for looking up documents based on keywords.
* **Spell checkers** to find the correct word from a dictionary.
* **Network routing** algorithms that search for the shortest path.

***

#### **List of Important Questions for Searching**:

**Easy:**

1. **Implement linear search** in an unsorted array.
2. **Implement binary search** in a sorted array.
3. **Find the first and last occurrence of an element** in a sorted array using binary search.
4. **Check if an element exists in an infinite sorted array** (can be simulated by applying binary search with exponentially increasing range).
5. **Find the square root of a number using binary search**.

**Medium:**

1. **Search in a rotated sorted array** using binary search.
2. **Find the peak element in an array** (element that is greater than its neighbors) using binary search.
3. **Find the element that appears once in a sorted array** where all other elements appear twice.
4. **Implement a ternary search**.
5. **Find the position of an element in a sparse array** (contains empty strings) using binary search.

**Hard:**

1. **Median of two sorted arrays** of the same or different sizes using a binary search approach.
2. **Search in a 2D matrix** using binary search (matrix is sorted both row-wise and column-wise).
3. **Find the smallest missing number** in a sorted array using binary search.
4. **Search in a bitonic array** (an array that increases then decreases) using binary search.
5. **Aggressive cows problem**: Place cows in stalls such that the minimum distance between any two cows is as large as possible (can be solved using binary search on the answer).

***

These questions focus on both fundamental and advanced searching techniques, helping you develop a solid understanding of various searching algorithms and their applications. Let me know if you'd like explanations or solutions for any of the problems listed!







Here are some helpful tips and tricks for solving searching algorithm problems in software engineering interviews:

#### 1. **Linear Search**

* **When to use**: Linear search is used when the list is **unsorted** or **small**.
* **Time complexity**: O(n), where `n` is the number of elements in the array.
* **Edge cases**: Ensure to handle cases like searching for the first or last element, or when the element is absent.

#### 2. **Binary Search**

* **When to use**: Binary search works when the array is **sorted**.
* **Time complexity**: O(log n), where `n` is the number of elements in the array.
* **Algorithm**:
  * Compare the target with the middle element of the array.
  * If they are equal, return the index.
  * If the target is smaller, search the left half. If larger, search the right half.
  * Repeat the process until the range becomes invalid (start > end).
* **Edge cases**:
  * Handle cases when the element is at the boundary (first or last index).
  * If the array is empty or contains duplicates, handle those carefully.
* **Tip**: When searching for the **first occurrence** or **last occurrence** of a target in a sorted array, modify the binary search to continue searching in the respective half after finding the target.

#### 3. **Binary Search Variants**

* **Lower Bound**: Find the first element that is greater than or equal to the target.
* **Upper Bound**: Find the first element that is greater than the target.
* **Search in Rotated Sorted Array**: Binary search can be applied to a **rotated sorted array** by identifying which half is sorted and adjusting the search range accordingly.
* **Binary Search on the Answer**: In problems where you need to minimize or maximize a value, you can use binary search to "search for the answer" (e.g., finding the smallest feasible value in optimization problems).

#### 4. **Ternary Search**

* **When to use**: Use ternary search to find the **minimum** or **maximum** in unimodal functions (functions that have only one peak or trough).
* **Algorithm**:
  * Divide the search range into three equal parts and evaluate the values at these points.
  * Depending on whether you're finding a maximum or minimum, eliminate one of the three regions.
  * Repeat the process until you narrow down to the desired point.
* **Time complexity**: O(log n), but it's generally less efficient than binary search in most practical cases.

#### 5. **Exponential Search**

* **When to use**: Use exponential search when you're not sure about the size of the array (for example, in unbounded or infinite arrays).
* **Algorithm**:
  * Start with an initial range and **double** the range each time until the element is larger than the target or the range exceeds the size of the array.
  * After finding the range, perform binary search within that range.
* **Time complexity**: O(log n) for finding the range, O(log n) for binary search within the range.

#### 6. **Jump Search**

* **When to use**: Jump search works well when the array is **sorted** but you want to skip some elements.
* **Algorithm**:
  * Jump ahead by a fixed step size (e.g., √n) and compare the target with the current element.
  * If the current element is larger than the target, perform a linear search in the previous jump’s range.
* **Time complexity**: O(√n), where `n` is the number of elements.

#### 7. **Interpolation Search**

* **When to use**: Use interpolation search when the values in the array are uniformly distributed.
* **Algorithm**:
  * Estimate the position of the target using the formula: \[ pos = low + \frac\{{(target - arr\[low]) \times (high - low)\}}\{{arr\[high] - arr\[low]\}} ]
  * Compare the value at the estimated position with the target and adjust the range accordingly.
* **Time complexity**: O(log log n) in the best case but can degrade to O(n) if the values are not uniformly distributed.

#### 8. **Depth-First Search (DFS) and Breadth-First Search (BFS)**

* Although DFS and BFS are primarily **graph traversal algorithms**, they are also used for searching in tree or graph-like structures.
* **DFS**: Goes as deep as possible into the structure before backtracking. Use it for pathfinding, backtracking, and exploring all possible solutions.
* **BFS**: Explores level by level, making it ideal for finding the **shortest path** in unweighted graphs or for solving problems like connected components.

#### 9. **Search in a Matrix**

* **Sorted 2D Matrix**: If the matrix is sorted row-wise and column-wise:
  * You can start from the top-right corner and move left or down based on the comparison between the current element and the target.
  * This approach runs in O(m + n) time, where `m` is the number of rows and `n` is the number of columns.
* **Binary Search on 2D Matrix**: Treat the 2D matrix as a 1D array (flatten it), then apply binary search. Time complexity is O(log(m \* n)).

#### 10. **Advanced Search Problems**

* **K-th Smallest/Largest Element**: You can use binary search combined with a counting function or a min-heap/max-heap to find the k-th smallest or largest element efficiently.
* **Median of Two Sorted Arrays**: This is a common interview problem where binary search is used to partition two sorted arrays and find the median in O(log(min(m, n))) time.

#### 11. **Searching in Tries**

* **Tries** (prefix trees) are often used to search for words in a **dictionary-like structure**. They provide efficient O(k) search time, where `k` is the length of the word.
* Use tries for problems like prefix matching, auto-complete, or word search puzzles.

#### 12. **Time and Space Complexity**

* Always be mindful of the time and space complexity of your searching algorithm. For instance:
  * **Linear search**: O(n) time complexity, O(1) space complexity.
  * **Binary search**: O(log n) time complexity, O(1) space complexity.
  * **DFS/BFS**: O(V + E) time complexity, where `V` is the number of vertices and `E` is the number of edges.

#### 13. **Key Practice Problems**

* **Binary Search Variations**: Find the first or last occurrence of an element.
* **Search in Rotated Sorted Array**: Find a target in a rotated version of a sorted array.
* **Median of Two Sorted Arrays**: Use binary search to find the median of two sorted arrays.
* **K-th Smallest Element**: Use binary search, heaps, or partitioning to solve this problem.
* **Matrix Search**: Search for an element in a sorted 2D matrix.

#### 14. **Edge Cases**

* Consider the following when dealing with searching problems:
  * Empty arrays or matrices.
  * Arrays or structures with duplicate elements.
  * Elements that are not present in the array or matrix.
  * Edge positions (first and last elements).

By mastering these searching algorithms and their variations, you’ll be well-prepared for DSA interview questions that involve searching. Would you like to dive deeper into a specific algorithm or problem type?
