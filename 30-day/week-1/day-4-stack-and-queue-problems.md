# Day 4: Stack and Queue Problems

Here are the detailed notes for  The focus today is understanding how to implement stacks and queues, common operations, and solving key problems like using one to implement the other (stack using queues and vice versa), as well as solving problems like valid parentheses.

#### 1. **Stacks Overview**

* **Definition**: A **stack** is a linear data structure that follows the **Last In First Out (LIFO)** principle. The last element added is the first one to be removed.
* **Common Operations**:
  * **Push(x)**: Add an element `x` to the top of the stack.
  * **Pop()**: Remove and return the element from the top of the stack.
  * **Peek()/Top()**: View the element at the top of the stack without removing it.
  * **isEmpty()**: Check if the stack is empty.
* **Applications**:
  * **Function calls**: The call stack in programming languages is an example of stack usage.
  * **Undo operations**: Stacks are often used to store states for undo functionality.
  * **Expression evaluation**: Parsing expressions in postfix, infix, or prefix notation.

***

#### 2. **Queues Overview**

* **Definition**: A **queue** is a linear data structure that follows the **First In First Out (FIFO)** principle. The first element added is the first one to be removed.
* **Common Operations**:
  * **Enqueue(x)**: Add an element `x` to the end of the queue.
  * **Dequeue()**: Remove and return the element from the front of the queue.
  * **Peek()/Front()**: View the element at the front of the queue without removing it.
  * **isEmpty()**: Check if the queue is empty.
* **Applications**:
  * **Task scheduling**: Queues are used to manage tasks in systems like CPU scheduling.
  * **Breadth-First Search (BFS)** in graphs and trees.

***

#### 3. **Key Problems and Solutions**

**1. Implement a Stack using Queues**

* **Problem Statement**: Implement a stack using two queues.
* **Approach**:
  * Use two queues (`q1` and `q2`), where:
    * Push the element into the non-empty queue (`q1` or `q2`).
    * For popping the top element, transfer all elements except the last one to the other queue.
* **Time Complexity**:
  * **Push operation**: O(1).
  * **Pop operation**: O(n), as all elements (except the last one) are transferred between the two queues.

```python
from collections import deque

class MyStack:
    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()

    def push(self, x: int):
        self.q1.append(x)

    def pop(self) -> int:
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        popped_element = self.q1.popleft()
        self.q1, self.q2 = self.q2, self.q1  # Swap queues
        return popped_element

    def top(self) -> int:
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        top_element = self.q1[0]
        self.q2.append(self.q1.popleft())
        self.q1, self.q2 = self.q2, self.q1  # Swap queues
        return top_element

    def empty(self) -> bool:
        return not self.q1 and not self.q2
```

**2. Implement a Queue using Stacks**

* **Problem Statement**: Implement a queue using two stacks.
* **Approach**:
  * Use two stacks (`stack_in` and `stack_out`), where:
    * **Enqueue**: Push the element onto `stack_in`.
    * **Dequeue**: If `stack_out` is empty, transfer all elements from `stack_in` to `stack_out`, then pop from `stack_out`.
* **Time Complexity**:
  * **Enqueue operation**: O(1).
  * **Dequeue operation**: Amortized O(1), because elements are only moved between stacks once.

```python
class MyQueue:
    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def push(self, x: int):
        self.stack_in.append(x)

    def pop(self) -> int:
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        return self.stack_out.pop()

    def peek(self) -> int:
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        return self.stack_out[-1]

    def empty(self) -> bool:
        return not self.stack_in and not self.stack_out
```

***

#### 4. **Common Stack and Queue Problems**

**1. Valid Parentheses**

* **Problem Statement**: Given a string containing just the characters `'(', ')', '{', '}', '[' and ']'`, determine if the input string is valid.
* **Approach**:
  * Use a stack to store the opening brackets.
  * For every closing bracket, check if it matches the top of the stack.
  * If the stack is empty at the end, the parentheses are balanced.
* **Time Complexity**: O(n), where `n` is the length of the string.
* **Space Complexity**: O(n), in the worst case where all elements are stored in the stack.

```python
def isValid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
    
    return not stack
```

**2. Min Stack**

* **Problem Statement**: Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
* **Approach**:
  * Use two stacks: one for the stack itself and one to track the minimum elements.
* **Time Complexity**: O(1) for all operations.
* **Space Complexity**: O(n), where `n` is the number of elements pushed.

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self):
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

**3. Evaluate Reverse Polish Notation (Postfix Expression)**

* **Problem Statement**: Evaluate the value of an arithmetic expression in Reverse Polish Notation (RPN). Valid operators are `+`, `-`, `*`, and `/`. Each operand may be an integer or another expression.
* **Approach**:
  * Use a stack to evaluate the expression. Push numbers onto the stack, and when encountering an operator, pop the top two numbers, apply the operation, and push the result back.
* **Time Complexity**: O(n), where `n` is the length of the tokens.
* **Space Complexity**: O(n), to store intermediate results.

```python
def evalRPN(tokens: List[str]) -> int:
    stack = []
    for token in tokens:
        if token in "+-*/":
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:
                stack.append(int(a / b))  # Handle division to truncate towards zero
        else:
            stack.append(int(token))
    return stack[0]
```

**4. Next Greater Element**

* **Problem Statement**: Given an array, find the **next greater element** for every element. The next greater element of an element `x` is the first greater element to the right of `x` in the array.
* **Approach**:
  * Use a stack to keep track of elements for which we haven’t yet found a greater element.
  * Traverse the array from right to left, maintaining the current "next greater" element on the stack.
* **Time Complexity**: O(n), where `n` is the length of the array.
* **Space Complexity**: O(n), to store the stack.

```python
def nextGreaterElements(nums: List[int]) -> List[int]:
    n = len(nums)
    result = [-1] * n
    stack = []
    
    for i in range(2 * n - 1, -1, -1):
        while stack and stack[-1] <= nums[i % n]:
            stack.pop()
        if stack:
            result[i % n] = stack[-1]
        stack.append(nums[i

% n])
    
    return result
```

***

#### 5. **Key Techniques for Stacks and Queues**

1. **Using Two Data Structures**:
   * **Stack with a Supporting Stack**: For problems like the min stack, use a secondary stack to track the minimum values.
   * **Queue with Two Stacks**: By reversing the order of elements with two stacks, you can implement a queue using stacks.
2. **Backtracking with Stacks**:
   * Stacks are frequently used for backtracking problems (e.g., valid parentheses, depth-first search, etc.).
3. **Sliding Windows with Deques**:
   * Deques (double-ended queues) are used for optimizing sliding window problems where you need quick access to both ends of the queue.

***

#### Recommended Practice Problems

1. **LeetCode**:
   * [Valid Parentheses](../../google-sde2/PROBLEM_DETAILS.md#valid-parentheses)
   * Min Stack
   * Implement Queue using Stacks
   * Next Greater Element I
2. **HackerRank**:
   * Balanced Brackets
   * Queue using Two Stacks
   * Maximum Element

By mastering stack and queue problems, and learning to implement one using the other, you will gain key insights into how data structures can be adapted to fit specific problem constraints.
