# Heap

#### **Detailed Summary of Heaps (Data Structures)**



<figure><img src="../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

A **Heap** is a specialized tree-based data structure that satisfies the **heap property**. In a **max-heap**, for any given node, the value of the node is greater than or equal to the values of its children. In a **min-heap**, the value of a node is less than or equal to the values of its children. Heaps are binary trees but not necessarily binary search trees, and they are commonly used to implement priority queues.

**Key Concepts:**

1. **Heap Types**:
   * **Max-Heap**: The key at the root is the largest among all keys in the heap, and the same property applies recursively for all subtrees.
   * **Min-Heap**: The key at the root is the smallest among all keys in the heap, and the same property applies recursively for all subtrees.
2. **Heap Representation**:
   * **Array-based Representation**: Heaps are typically implemented using arrays. For a node at index `i`:
     * The left child is at index `2i + 1`.
     * The right child is at index `2i + 2`.
     * The parent is at index `(i - 1) / 2`.
3. **Heap Operations**:
   * **Insert (Push)**: Adds a new element to the heap while maintaining the heap property. This involves inserting the element at the end of the heap (array) and then “bubbling up” (swapping with parents) to maintain the heap order.
   * **Delete/Extract (Pop)**: Removes the root (maximum in max-heap or minimum in min-heap) and restructures the heap by moving the last element to the root and then "bubbling down" to maintain the heap property.
   * **Peek/Top**: Returns the root element (maximum in max-heap or minimum in min-heap) without removing it.
   * **Heapify**: Converts an unsorted array into a heap. This is done by applying the "heapify" process from the bottom of the tree upwards.
   * **Build-Heap**: Constructs a heap from an unordered array in O(n) time.
4. **Applications of Heaps**:
   * **Priority Queue**: A heap-based priority queue allows insertion of elements and extraction of the highest or lowest priority element in O(log n) time.
   * **Heap Sort**: A sorting algorithm that builds a heap and repeatedly extracts the maximum or minimum to sort elements in O(n log n) time.
   * **Graph Algorithms**: Algorithms like Dijkstra’s Shortest Path and Prim’s Minimum Spanning Tree use heaps for efficiently finding the next node to process.
   * **Median Finding**: Heaps can be used to maintain two halves of data, with the max-heap storing the smaller half and the min-heap storing the larger half, to find the median efficiently.
   * **Kth Largest or Smallest Element**: Heaps are used to efficiently find the k-th largest or smallest element in an unsorted array.
5. **Heap Properties**:
   * **Complete Binary Tree**: A heap is always a complete binary tree, meaning all levels are fully filled except possibly the last, which is filled from left to right.
   * **Balanced Structure**: The height of the heap is logarithmic in terms of the number of nodes, ensuring that insertion and deletion operations remain efficient (O(log n)).
6. **Advantages**:
   * **Efficient for Priority Operations**: Heaps provide fast access to the maximum or minimum element and support efficient insertion and deletion.
   * **Space Efficient**: Since heaps are implemented using arrays, they do not require extra space for pointers as in linked structures.
7. **Disadvantages**:
   * **No Ordered Traversal**: Unlike binary search trees, heaps do not allow efficient in-order traversal to retrieve elements in a sorted order.
   * **Fixed Root Access**: You can only access the root element efficiently; other elements are harder to access.

***

#### **List of Important Questions for Heaps**:

**Easy:**

1. **Implement a max-heap and a min-heap using arrays**.
2. **Find the k-th largest (or smallest) element in an array using a heap**.
3. **Merge k sorted arrays using a heap**.
4. **Implement a priority queue using a heap**.
5. **Find the median of a data stream using two heaps (max-heap and min-heap)**.

**Medium:**

1. **Heap Sort: Implement a heap-based sorting algorithm**.
2. **Find the k closest points to the origin in a 2D plane using a max-heap**.
3. **Design a system to find the top 'k' frequent elements in a stream**.
4. **Construct a min-heap from an unordered array**.
5. **Find the smallest range that includes at least one number from each of the k sorted lists using a heap**.

**Hard:**

1. **Design a data structure that supports the following operations: Insert, Delete, and GetMedian in O(log n) time** (Use a combination of two heaps).
2. **Dijkstra’s shortest path algorithm using a min-heap**.
3. **Find the maximum of all subarrays of size k using a heap**.
4. **Design and implement an efficient stock price tracking system using heaps**.
5. **Design a skyline problem solution using heaps to process events in sorted order**.

***

These questions cover the essential operations, concepts, and applications of heaps, giving you a solid foundation to tackle heap-related problems, especially in competitive programming and real-world system design. Let me know if you'd like a detailed explanation for any specific question!







Here are some helpful tips and tricks for solving heap problems in software engineering interviews:

#### 1. **Understand the Binary Heap Structure**

* A **binary heap** is a complete binary tree that satisfies the heap property:
  * In a **max-heap**, the parent is always greater than or equal to its children.
  * In a **min-heap**, the parent is always smaller than or equal to its children.
* The heap is usually implemented using an array where:
  * For a node at index `i`, the left child is at `2*i + 1` and the right child is at `2*i + 2`. The parent is at `(i - 1) // 2`.

#### 2. **Heapify Operations**

* **Heapify** (also called **sift-down** or **bubble-down**) is the process of maintaining the heap property. It's essential for:
  * Inserting elements.
  * Deleting the root.
  * Building a heap from an array (done in O(n) time using bottom-up heapify).
* Master the heapify-up and heapify-down processes for both max-heaps and min-heaps.

#### 3. **Priority Queue Implementation**

* A **priority queue** is commonly implemented using heaps:
  * For **min-heaps**, elements with the smallest priority are dequeued first.
  * For **max-heaps**, elements with the highest priority are dequeued first.
* Practice priority queue operations like `insert`, `peek`, and `extract` for both min- and max-priorities.

#### 4. **Top K Elements Problems**

* Heaps are ideal for problems involving the **k-th largest or smallest elements**.
  * Use a **min-heap** to keep track of the largest k elements (where the root will be the smallest of the k largest elements).
  * Use a **max-heap** to track the smallest k elements.
* In **Top K Frequent Elements** problems, you can pair heaps with hashmaps to count element frequencies and store them in the heap for efficient extraction.

#### 5. **Merging Sorted Arrays or Lists**

* In problems where you need to **merge k sorted arrays or linked lists**, use a **min-heap** to always extract the smallest current element from the lists.
* This reduces the time complexity to O(n log k), where `n` is the total number of elements and `k` is the number of lists.

#### 6. **Heap Sort**

* **Heap sort** uses a heap to sort an array in O(n log n) time:
  * First, build a max-heap (or min-heap) from the input array.
  * Then repeatedly extract the maximum (or minimum) element and rebuild the heap.
* Heap sort is particularly useful when in-place sorting is required and you want guaranteed O(n log n) time.

#### 7. **Median of a Data Stream**

* To efficiently find the **median of a stream of numbers**, maintain two heaps:
  * A **max-heap** for the smaller half of the numbers.
  * A **min-heap** for the larger half.
  * The median is either the top of the max-heap (for odd-sized streams) or the average of the tops of both heaps (for even-sized streams).
* Practice balancing the heaps as new elements are added.

#### 8. **Dijkstra’s Algorithm**

* In shortest path algorithms like **Dijkstra’s**, heaps (or priority queues) are used to always process the next node with the smallest distance in O(log n) time.
* Practice using heaps with graphs for pathfinding problems.

#### 9. **Handling Dynamic Data**

* Heaps are useful in scenarios where the data is dynamic and you need efficient access to the largest or smallest elements.
  * For example, maintaining a running **minimum/maximum** or calculating the **median** of data that is constantly changing.

#### 10. **Heap Variants**

* Be familiar with different heap variants, including:
  * **Fibonacci heaps**: Useful for algorithms like Dijkstra’s with better amortized time for some operations.
  * **Binomial heaps**: Useful for merging heaps efficiently.
  * **Pairing heaps**: A simpler alternative to Fibonacci heaps, often used in practice.

#### 11. **Common Edge Cases**

* **Empty heap**: Always handle operations like extracting from an empty heap gracefully.
* **Heap size limits**: Be aware of the heap’s size in cases where space complexity is a concern.
* **Duplicates**: Understand how the heap will handle duplicate values and whether this affects the problem you’re solving.

#### 12. **Key Practice Problems**

* **K-th Largest Element** in a stream or array.
* **Merge k Sorted Lists/Arrays**.
* **Top K Frequent Elements**.
* **Find Median from Data Stream**.
* **Building a Min/Max Heap** from an array.
* **Smallest Range Covering Elements from k Lists**.
* **Dijkstra’s Algorithm** for shortest paths.

#### 13. **Communicate Clearly in Interviews**

* When discussing heap-based solutions, clearly explain:
  * Why the heap is appropriate for the problem.
  * The time complexity for each operation (e.g., insert and extract both take O(log n) time).
  * How heap operations fit into the overall solution (especially in graph-based problems or dynamic data streams).

By mastering these tips and tricks and practicing a variety of heap-related problems, you'll be well-prepared to tackle heap problems in technical interviews. Would you like to dive deeper into any specific heap problems or algorithms?
