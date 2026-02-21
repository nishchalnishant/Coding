# Stack

## **Detailed Summary of Stacks (Data Structures)**

A **Stack** is a linear data structure that follows the **LIFO (Last In First Out)** principle, meaning the last element added to the stack is the first one to be removed. Think of a stack of plates: you add a plate to the top, and you also remove the plate from the top.

### **Key Concepts:**

1. **Basic Operations**:
   * **Push**: Adds an element to the top of the stack.
   * **Pop**: Removes the element from the top of the stack.
   * **Peek/Top**: Returns the element at the top of the stack without removing it.
   * **isEmpty**: Checks whether the stack is empty.
   * **isFull**: Checks if the stack is full (for fixed-size stacks).
2. **Stack Representation**:
   * **Array-based Stack**: Fixed-size implementation using an array. It has limited space and may cause stack overflow when full.
   * **Linked List-based Stack**: Dynamic-size implementation using a linked list. It grows and shrinks as needed, avoiding overflow.
3. **Applications of Stacks**:
   * **Expression Evaluation**: Stacks are used to evaluate expressions in postfix (Reverse Polish Notation) and convert infix expressions to postfix or prefix.
   * **Backtracking Algorithms**: Problems like maze solving or parsing recursion use stacks to store intermediate results.
   * **Undo Mechanisms**: Applications like text editors use stacks to implement undo functionality.
   * **Function Call Stack**: Manages function calls in recursive programs.
   * **Balanced Parentheses**: Check if a sequence of parentheses/brackets is balanced (common in compilers).
   * **Depth First Search (DFS)**: DFS traversal of graphs uses stacks to backtrack when exploring nodes.
4. **Real-World Examples**:
   * Browser history navigation (back and forward buttons).
   * Undo/Redo operations in software like MS Word or Photoshop.
   * Syntax parsing (checking matching parentheses, tags in HTML/XML).
5. **Stack Limitations**:
   * Limited **random access**: You can only access the top element; accessing any element other than the top requires popping elements.
   * For array-based stacks, overflow can occur when the stack reaches its size limit.

## **Advanced Concepts:**

1. **Monotonic Stacks**: These are specialized stacks used in problems involving finding the next greater/smaller element. A stack is maintained in increasing or decreasing order based on the problem requirements.
2. **Min/Max Stacks**: These are stacks where each element keeps track of the current minimum or maximum in the stack, allowing for constant-time min/max retrieval.

***

## **List of Important Questions for Stacks**:

**Easy:**

1. **Implement a stack using an array or linked list**.
2. **Design a stack that supports push, pop, and retrieving the minimum element in constant time** (Min Stack).
3. **Check for balanced parentheses in an expression**.
4. **Reverse a string using a stack**.
5. **Implement two stacks in an array**.

**Medium:**

1. **Evaluate a postfix expression** (Reverse Polish Notation).
2. **Infix to Postfix/Prefix conversion**.
3. **Sort a stack using recursion**.
4. **Next Greater Element**: Given an array, for each element, find the next greater element.
5. **Find the largest rectangular area in a histogram**.

**Hard:**

1. **Implement a stack with O(1) time complexity for push, pop, and getMax/getMin** (Max Stack or Min Stack).
2. **Design a stack with middle element access in O(1) time** (requires doubly linked list).
3. **Trap Rain Water Problem** (can be solved using a stack-based approach).
4. **Largest rectangle under the skyline** (use stacks to solve this in O(n) time).
5. **Validate the stack sequences**: Given pushed and popped sequences, validate whether they are valid stack operations.

***

These questions cover the full range of complexity for the stack data structure, giving you practice with both basic stack operations and advanced applications in algorithmic problem-solving. Let me know if you'd like more details or solutions to any specific problems!







When preparing for stack problems in software engineering interviews, here are some key tips and tricks to help you tackle them efficiently:

#### 1. **Understand LIFO (Last In, First Out)**

* A stack is a **Last In, First Out** data structure. This means the most recently added element is the first to be removed.
* Make sure you are familiar with the basic operations: `push`, `pop`, `peek/top`, and `isEmpty`.

#### 2. **Use Stacks for Reversals**

* Stacks are naturally suited for problems that involve reversing a process, such as reversing a string or list.
* They are great for backtracking problems where you need to reverse recent operations.

#### 3. **Balanced Parentheses Problems**

* Stacks are perfect for problems involving **balanced parentheses** (or other symbols like brackets and braces).
* Push opening parentheses onto the stack, and pop when you encounter a closing one. At the end, the stack should be empty if the parentheses are balanced.
* Handle edge cases like single unmatched parentheses or cases with other characters mixed in.

#### 4. **Use Stacks to Simulate Recursion**

* Stack-based solutions can often simulate recursive processes, making them helpful in problems that involve depth-first exploration (like traversing trees or graphs).

#### 5. **Monotonic Stack Technique**

* For problems involving arrays and **monotonic properties** (like finding the next greater or smaller element), use a stack to maintain elements in an increasing or decreasing order.
* This approach is used to optimize O(n²) brute-force solutions to O(n).
* Common examples:
  * Next Greater Element
  * Stock Span Problem
  * Largest Rectangle in Histogram

#### 6. **Stack with Auxiliary Structures**

* For problems that require keeping track of multiple values (e.g., the minimum value), use an auxiliary stack:
  * **Min Stack**: A stack that keeps track of the minimum value in constant time by maintaining a secondary stack for minimums.
  * Similar strategies can be used for **max stacks** or other conditions.

#### 7. **Infix, Prefix, Postfix Expression Evaluation**

* Stack problems often involve evaluating mathematical expressions in infix, prefix, or postfix notation.
* For **postfix (Reverse Polish Notation)**, use a stack to evaluate expressions. Push numbers onto the stack, and when encountering an operator, pop the required operands, apply the operator, and push the result back.
* Know how to handle multiple operators, parentheses, and operator precedence.

#### 8. **Undo Operations**

* Stacks are useful for implementing **undo** functionality (e.g., in text editors). Every operation can be pushed onto the stack, and the last operation can be popped when undoing.

#### 9. **Depth-First Search (DFS) Using Stacks**

* In many graph/tree traversal problems, you can use a stack to implement **DFS** iteratively instead of using recursion.
* Push the starting node onto the stack, and then iteratively process nodes by visiting and pushing neighbors.

#### 10. **Backtracking Problems**

* In backtracking problems (like solving a maze, or generating valid parenthesis combinations), stacks are often used to store the current path or state. Each step forward is pushed onto the stack, and when you need to backtrack, pop the stack.

#### 11. **Stack vs Recursion**

* Many recursive algorithms (like tree traversals) can be converted into iterative versions using a stack. Know when and how to switch between recursion and an explicit stack.

#### 12. **Common Edge Cases**

* Make sure to handle the following edge cases:
  * Empty stack operations (like popping from an empty stack).
  * Full stack scenarios (if implementing a stack with a fixed size).
  * Single-element stack situations in problems that require multiple pops or pushes.

#### 13. **Key Practice Problems**

* Valid Parentheses
* Min Stack
* Evaluate Reverse Polish Notation
* Daily Temperatures
* Largest Rectangle in Histogram
* Next Greater Element
* Design a Stack with `getMin()` or `getMax()` functions

By understanding these techniques and practicing stack-related problems regularly, you will be able to handle stack-based questions in interviews more effectively. Would you like a deep dive into any of these topics or specific problem examples?



