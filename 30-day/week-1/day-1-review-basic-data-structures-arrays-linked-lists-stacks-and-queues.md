# Day 1: Review Basic Data Structures (Arrays, Linked Lists, Stacks, and Queues):



## 1. **Arrays**

* **Definition**: An array is a collection of elements stored at contiguous memory locations.
* **Key Properties**:
  * **Indexing**: Elements can be accessed by their index, starting from 0.
  * **Size**: Fixed size in most programming languages, meaning it cannot be resized once allocated.
  * **Time Complexity**:
    * Access by index: O(1)
    * Search: O(n)
    * Insertion/Deletion: O(n) (as shifting elements might be required)
* **Common Operations**:
  * **Access**: `array[index]`
  * **Insertion**: At the end of the array (O(1)), at a specific position (O(n))
  * **Deletion**: Removing an element requires shifting, making it O(n).
* **Practical Example**: The `Two Sum` problem, where the task is to find two numbers that add up to a target.

## 2. **Linked Lists**

* **Definition**: A linked list is a linear data structure where elements (nodes) are linked using pointers.
* **Types**:
  * **Singly Linked List**: Each node points to the next node.
  * **Doubly Linked List**: Each node points to both the previous and the next node.
  * **Circular Linked List**: The last node points to the first node.
* **Key Properties**:
  * **Dynamic Size**: Unlike arrays, linked lists can grow/shrink dynamically.
  * **No random access**: You can’t access an element by index directly (O(n) time to search).
* **Time Complexity**:
  * Search: O(n)
  * Insertion/Deletion at head: O(1)
  * Insertion/Deletion at any other position: O(n)
* **Common Operations**:
  * **Traversal**: Go through each node until you reach the end (null in singly linked lists).
  * **Insertion**: Efficient at the head (O(1)), but inefficient at other positions.
  * **Deletion**: Efficient at the head (O(1)), but inefficient at other positions (O(n)).
* **Practical Example**: Problems like reversing a linked list or detecting cycles.

## 3. **Stacks**

* **Definition**: A stack is a linear data structure that follows the **LIFO (Last In First Out)** principle.
* **Common Operations**:
  * **Push**: Add an element to the top of the stack (O(1)).
  * **Pop**: Remove the top element from the stack (O(1)).
  * **Peek/Top**: Access the top element without removing it (O(1)).
  * **IsEmpty**: Check if the stack is empty (O(1)).
* **Time Complexity**:
  * Push, Pop, Peek: O(1)
* **Use Cases**:
  * **Function calls** (call stack).
  * **Backtracking problems** (e.g., maze solvers).
  * **Balanced parentheses**: Stacks are often used to check if a sequence of parentheses is balanced.
* **Practical Example**: Implementing a browser’s back button or evaluating postfix expressions.

## 4. **Queues**

* **Definition**: A queue is a linear data structure that follows the **FIFO (First In First Out)** principle.
* **Types**:
  * **Simple Queue**: Elements are enqueued at the back and dequeued from the front.
  * **Circular Queue**: The last position is connected to the first, making the queue circular.
  * **Priority Queue**: Elements are dequeued based on their priority, not the order they were enqueued.
* **Common Operations**:
  * **Enqueue**: Add an element to the end of the queue (O(1)).
  * **Dequeue**: Remove an element from the front (O(1)).
  * **Peek/Front**: Access the front element without removing it (O(1)).
  * **IsEmpty**: Check if the queue is empty (O(1)).
* **Time Complexity**:
  * Enqueue, Dequeue, Peek: O(1)
* **Use Cases**:
  * **Task scheduling**: Queues are used in task scheduling and order processing.
  * **Breadth-First Search (BFS)** in graphs/trees.
* **Practical Example**: Printing jobs in a print queue or managing processes in an operating system.

***

## Summary of Key Differences:

* **Arrays** offer constant-time access via indices but resizing them is expensive.
* **Linked Lists** allow efficient insertion and deletion but require linear time for access.
* **Stacks** are ideal for situations where you need to access the most recent item added first (LIFO).
* **Queues** follow a FIFO pattern, making them useful for processing items in the order they are received.

These notes provide an overview of each data structure's functionality, time complexities, and practical applications, preparing you for deeper problem-solving on Day 2.
