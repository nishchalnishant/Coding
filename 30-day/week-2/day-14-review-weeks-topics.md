# Day 14: Review Week’s Topics

Here are detailed notes for **Day 14: Review Week’s Topics**. This day is dedicated to revisiting challenging problems and summarizing key concepts learned throughout the week on advanced data structures and algorithms.

***

#### 1. **Review Topics**

During this review, focus on the following topics covered in Week 2:

* Binary Search Trees (BST)
* Heaps
* Graph Basics
* Graph Algorithms
* Dynamic Programming Introduction
* Intermediate Dynamic Programming

#### 2. **Key Concepts to Summarize**

**2.1 Binary Search Trees (BST)**

* **Definition**: A binary tree in which each node has at most two children, with the left child being less than the parent node and the right child being greater.
* **Common Operations**:
  * **Insertion**: Place a new value in the correct position.
  * **Deletion**: Remove a node and maintain the BST property.
  * **Searching**: Check if a value exists in the tree.
  * **Traversal**: In-order (sorted order), pre-order, and post-order.
* **Time Complexity**:
  * Average case for operations: O(log n)
  * Worst case (unbalanced tree): O(n)

***

**2.2 Heaps**

* **Definition**: A complete binary tree that satisfies the heap property (min-heap or max-heap).
  * **Min-Heap**: The value of each node is less than or equal to the values of its children.
  * **Max-Heap**: The value of each node is greater than or equal to the values of its children.
* **Common Operations**:
  * **Insert**: Add a new element while maintaining the heap property.
  * **Extract-Min/Extract-Max**: Remove the root element and restructure the heap.
  * **Peek**: Get the root element without removing it.
* **Time Complexity**:
  * Insert: O(log n)
  * Extract: O(log n)
  * Peek: O(1)

***

**2.3 Graph Basics**

* **Representations**:
  * **Adjacency Matrix**: A 2D array representation where the cell at row `i` and column `j` indicates the presence of an edge between vertices `i` and `j`.
  * **Adjacency List**: An array of lists where each index represents a vertex and the list at that index contains the adjacent vertices.
* **Basic Traversal Algorithms**:
  * **Depth-First Search (DFS)**: Explores as far down a branch before backtracking.
  * **Breadth-First Search (BFS)**: Explores all neighbors at the present depth before moving on to nodes at the next depth level.

***

**2.4 Graph Algorithms**

* **Dijkstra’s Algorithm**: Finds the shortest path from a starting node to all other nodes in a graph with non-negative weights.
  * Uses a priority queue (min-heap) for efficient retrieval of the next node with the smallest tentative distance.
* **Bellman-Ford Algorithm**: Computes shortest paths from a single source node to all other nodes in a graph, even with negative weights (but no negative cycles).
  * Relax edges repeatedly and check for negative-weight cycles.

***

**2.5 Dynamic Programming**

* **Key Concepts**:
  * **Overlapping Subproblems**: Problems can be broken down into smaller subproblems that are reused.
  * **Optimal Substructure**: The optimal solution can be constructed from optimal solutions of subproblems.
* **Common Problems**:
  * **Fibonacci Sequence**: Calculated via memoization or tabulation.
  * **[Coin Change](../../google-sde2/PROBLEM_DETAILS.md#coin-change)**: Finding the minimum number of coins for a specific amount.
  * **Longest Increasing Subsequence (LIS)**: Finding the longest subsequence of a sequence that is sorted in increasing order.
* **Time Complexity**:
  * Fibonacci: O(n) for both approaches.
  * Coin Change: O(n \* m) where (n) is the number of coins and (m) is the amount.
  * LIS: O(n²) for naive approach; O(n log n) for optimized approach.

***

#### 3. **Practice Problems**

Use this review day to solve a few practice problems to reinforce your understanding of the week’s topics:

1. **Binary Search Trees**:
   * Implement insertion and deletion in a BST.
   * Given a BST, write a function to find the kth smallest element.
2. **Heaps**:
   * Implement a min-heap and max-heap.
   * Solve problems related to merging k sorted lists using a heap.
3. **Graphs**:
   * Implement DFS and BFS on a graph.
   * Solve the shortest path problem using Dijkstra's algorithm.
4. **Dynamic Programming**:
   * Revisit the Coin Change problem and try to implement both approaches (minimum coins and number of ways).
   * Solve the Longest Increasing Subsequence problem using both O(n²) and O(n log n) methods.

***

#### 4. **Reflection and Self-Assessment**

* **Identify Weak Areas**: Reflect on which topics you found most challenging. Spend additional time understanding those concepts and solving related problems.
* **Summarize Key Learnings**: Write down key takeaways from each topic, focusing on definitions, key operations, and common algorithms.

***

#### 5. **Preparation for Next Week**

As you prepare for the next week, consider the following steps:

* Review key algorithms and their time complexities.
* Make a list of additional resources (books, online courses, practice websites) that you can use to deepen your understanding.
* Set specific goals for what you want to achieve in the next week, based on your reflections from this week’s review.

By thoroughly reviewing and reinforcing the concepts from this week, you’ll be well-prepared to tackle more complex problems and enhance your problem-solving skills in dynamic programming and other advanced data structures.
