# Recursion

#### Recursion: Detailed Summary

**Recursion** is a problem-solving technique where a function calls itself to solve smaller instances of the same problem. It breaks down a complex problem into simpler subproblems until the subproblems become trivial enough to be solved directly (base case). Recursion provides a clean and logical approach to solving problems that can be defined in terms of simpler versions of themselves.

***

#### Key Concepts in Recursion:

1. **Recursive Function**:
   * A function that calls itself directly or indirectly to solve a smaller instance of the same problem.
2. **Base Case**:
   * The simplest version of the problem, where no further recursive calls are needed. Without a base case, recursion would continue indefinitely, leading to an infinite loop.
3. **Recursive Case**:
   * The part of the function where the function calls itself to work on a smaller problem. Each recursive call reduces the problem size, eventually reaching the base case.
4. **Stack Memory**:
   * Each recursive call is added to the **call stack**, where the current function's state (parameters and local variables) is saved. When the base case is reached, the function starts returning from the call stack in reverse order of the calls.

***

#### Components of Recursive Functions:

1. **Base Condition**:
   * The stopping criterion that determines when the function will stop calling itself. It prevents the recursive process from going into an infinite loop.
2. **Recursive Call**:
   * The part of the function where the function calls itself with modified arguments, typically reduced to a simpler or smaller instance of the original problem.
3. **Return Statement**:
   * After hitting the base case, the return statement unwinds the recursive calls, building the final result as each call returns.

***

#### Example of Recursion: Factorial Function

A classic example of recursion is computing the factorial of a number (n), denoted (n!), which is the product of all integers from 1 to (n).

**Recursive Formula for Factorial:**

\[ n! = n \times (n-1)! ] \[ \text{Base Case}: 0! = 1 ]

**Recursive Code Example (Python):**

```python
def factorial(n):
    if n == 0:           # Base case
        return 1
    else:
        return n * factorial(n - 1)  # Recursive call
```

***

#### Types of Recursion:

1. **Direct Recursion**:
   * A function calls itself directly. This is the most common form of recursion.
   * Example: Factorial, Fibonacci series.
2. **Indirect Recursion**:
   * A function calls another function, and that function calls the first function again. This forms a loop of function calls.
   *   Example:

       ```python
       def functionA():
           functionB()

       def functionB():
           functionA()
       ```
3. **Tail Recursion**:
   * A special form of recursion where the recursive call is the last operation in the function. Tail recursion can be optimized by some compilers or interpreters to avoid using extra stack space.
   *   Example:

       ```python
       def tail_recursive_factorial(n, accumulator=1):
           if n == 0:
               return accumulator
           else:
               return tail_recursive_factorial(n-1, n * accumulator)
       ```
4.  **Head Recursion**:

    * Any recursion where the recursive call is not the last operation in the function, making it harder to optimize. Most recursive problems (like Fibonacci) fall into this category.
    * Example:

    ```python
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)   

    ```

**Head Recursion and Tall Recursion**

A Recursive function typically perform some task and call itself. If the call is\
made before the function performs its own task, then it is called HeadRecursion (Recursion is performed at the bead of thefunction body). If recursive call\
is made at the end, then it is Tail-Recursion.



A tail recursion is very easy to re-write in form of a loop. So there\
should ideally be no reason to write a tail recursion in code unless we are writing it to demonstrate recursion itself.\
Head and tail recursion are just given here as concepts. Most of the\
times (esp. in case of dynamic programming problems) recursion is more\
complex and may not be simple head or tail recursion. Consider one of the\
most rampant examples of recursion, in-order traversals of a Binary Tree.



How to Solve a Problem Using Recursion\
Our focus usually is to solve a problem, with recursion, we can actually\
code without solving a problem, if we can somehow define the large\
problem in terms of smaller problems of same type. Our focus is on solving the problem for top case and leave the rest for\
recursive calls to do. Consider the below example: bubble sort

Bubble Sort repeatedly steps through the array, compares each pair of\
adjacent items and swaps them if they are in the wrong order. After\
traversing for the first time, the largest element reaches last position in the\
array.\
In the second pass, the second largest element reaches second last\
position and so on. There are n-1 passes that takes n-1 elements to their\
right positions, the nth element will be automatically at the first position.



now to solve this using recursion ---

To make it a recursive function, we first need to define the larger\
problem in terms of smaller subproblems and task that each function will\
be performing. If the array is\
9, 6, 2, 12, 11, 9, 3, 7\
Then after the first pass, the largest element, 12, reach end of array:\
6, 2, 9, 11, 9, 3, 7, 12

With 12 at the nth position, we need to sort first n-1 elements. "Sort\
first n elements" and "Sort first n-1 elements" are same problems with different\
parameters. We have found our recursion, each function performs one pass\
and rest is left to recursion:



* optimal substructure\
  \
  while building the solution for a\
  problem of size n, define it in terms of similar problems of smaller size, say,\
  k (k < n). We find optimal solutions of less elements and combine the\
  solutions to get final result.
  * ex — finding shortest bath from a to b , we can divide the whole problem into a small problem of 3 or 4 cities and solve those&#x20;
  * In a nutshell, it means, we can write recursive formula for solution to the problem of finding shortest path.
  * Standard algorithms like Floyd-Warshall and Bellman-Ford to find allpair shortest paths are typical examples of Dynamic Programming.
  * use of optimal  substructure in dp&#x20;
    * Fundamentally, DP is an important tool for optimizing recursive solutions\
      in a way that is more efficient, both in terms of memory and time than\
      regular recursion.
    * The logic of dynamic programming usually comes from recursion.\
      Solution of a problem is derived from solution of subproblems, solution of\
      subproblem is derived from solution of sub-subproblems and so on.\
      In questions of dynamic programming, it is a good idea, to first solve\
      the problem using recursive formula and then use the same formula with\
      bottom-up approach of dynamic programming.
    * **BTTM — bottom up \[ tabulation, storing values in array and using it next] tabulation storing value in stack and using it**





***



Advantages of Recursion:

1. **Simplifies Problem-Solving**:
   * Problems that can be naturally divided into subproblems, like tree traversals or divide and conquer algorithms, are simpler to implement recursively.
2. **Cleaner and More Intuitive Code**:
   * Recursion often results in shorter and more readable code, especially for problems like tree-based structures (e.g., binary trees).
3. **Effective for Divide and Conquer**:
   * Recursion is a natural fit for divide-and-conquer algorithms, where a problem is divided into smaller subproblems (e.g., merge sort, quicksort).

***

#### Disadvantages of Recursion:

1. **Memory Usage**:
   * Recursion uses the call stack to store the state of each recursive call, which can lead to a **stack overflow** for deep recursion (e.g., when recursion depth exceeds the system's stack limit).
2. **Performance Overhead**:
   * Recursive solutions can be less efficient than iterative ones due to the overhead of function calls and the use of stack memory.
3. **Risk of Infinite Recursion**:
   * If the base case is not properly defined or the recursive step doesn't reduce the problem size, recursion can lead to infinite loops, crashing the program with a stack overflow.

***

#### Common Recursion Patterns:

1. **Linear Recursion**:
   * The recursive function makes a single recursive call. The problem size is reduced by one in each step.
   * Example: Factorial, Fibonacci sequence.
2. **Multiple Recursion**:
   * The recursive function makes multiple recursive calls. The problem branches into multiple subproblems at each step.
   * Example: Tree traversals, Fibonacci (which calls itself twice).
3. **Nested Recursion**:
   * A form of recursion where a recursive call occurs inside another recursive call.
   * Example: Ackermann function.

***

#### Recursion vs. Iteration:

1. **Recursion**:
   * Uses function calls and the call stack to break a problem down into smaller subproblems. Recursion is often more elegant and easier to understand for problems with a recursive structure (e.g., trees).
2. **Iteration**:
   * Uses loops to repeatedly execute a set of instructions. Iterative solutions are typically more memory-efficient since they don’t rely on the call stack.

#### Recursion Use Cases:

1. **Divide and Conquer Algorithms**:
   * Many divide and conquer algorithms like merge sort, quicksort, and binary search use recursion to break down the problem into smaller subproblems.
2. **Tree and Graph Traversals**:
   * Recursion is a natural fit for tree traversals (in-order, pre-order, post-order) and for depth-first search (DFS) in graphs.
3. **Mathematical Problems**:
   * Problems like factorial, Fibonacci numbers, and the Tower of Hanoi are naturally solved using recursion.
4. **Dynamic Programming**:
   * Dynamic programming problems often use recursion with memoization to avoid redundant calculations.

***

#### Common Recursion Problems and Questions:

1. **Factorial of a Number**:
   * Write a recursive function to compute the factorial of a given number (n).
   * Example: (5! = 5 \times 4 \times 3 \times 2 \times 1 = 120).

```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Example
print(factorial(5))  # Output: 120
```

1. **Fibonacci Sequence**:
   * Write a recursive function to compute the (n^{th}) Fibonacci number. The Fibonacci sequence is defined as: \[ F(n) = F(n-1) + F(n-2), \quad F(0) = 0, F(1) = 1 ]

```python
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

# Example
print(fibonacci(5))  # Output: 5
```

1. **Tower of Hanoi**:
   * Solve the Tower of Hanoi problem for (n) disks, where the goal is to move all disks from one peg to another using an auxiliary peg.
   * **Recursive relation**: Move (n-1) disks from source to auxiliary, move the largest disk to the target, and then move (n-1) disks from auxiliary to target.

```python
def tower_of_hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    tower_of_hanoi(n - 1, source, auxiliary, target)
    print(f"Move disk {n} from {source} to {target}")
    tower_of_hanoi(n - 1, auxiliary, target, source)

# Example
tower_of_hanoi(3, 'A', 'C', 'B')
```

1. **Binary Search**:
   * Implement binary search recursively. Given a sorted array and a target value, use recursion to find the index of the target value.
   * **Time complexity**: (O(\log n)).

```python
def binary_search(arr, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search(arr, target, left, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, right)

# Example
arr = [1, 2, 3, 4, 5, 6, 7]
print(binary_search(arr, 5, 0, len(arr) - 1))  # Output: 4
```

1. **Permutations of a String**:
   * Generate all permutations of a string using recursion. For example, the permutations of the string "ABC" are "ABC", "ACB", "BAC", "BCA", "CAB", and "CBA".

```python
def permutations(s, path=""):
    if len(s) == 0:
        print(path)
        return
    for i in range(len(s)):
        permutations(s[:i] + s[i+1:], path + s[i])

# Example
permutations("ABC")
```

1. **Subsets (Power Set)**:
   * Write a recursive function to generate all subsets of a given set (also known as the power set).

```python
def subsets(s, index=0, current=""):
    if index == len(s):
        print(current)
        return
    subsets(s, index + 1, current + s[index])  # Include
    subsets(s, index + 1, current)            # Exclude

# Example
subsets("ABC")
```

1. **Palindrome Check**:
   * Write a recursive function to check if a string is a palindrome. A string is a palindrome if it reads the same forward and backward.

```python
def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])

# Example
print(is_palindrome("racecar"))  # Output: True
```

1. **Maximum Depth of a Binary Tree**:
   * Given a binary tree, write a recursive function to find its maximum depth. The maximum depth is the number of nodes along the longest path from the root to a leaf.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Example
root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
print(max_depth(root))  # Output: 3
```

1. **Merge Sort**:
   * Implement the merge sort algorithm using recursion. Merge sort divides the array into two halves, recursively sorts each half, and merges the two sorted halves.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Example
print(merge_sort([3, 5, 1, 4, 2]))  # Output: [1, 2, 3, 4, 5]
```

1. **Quicksort**:
   * Implement the quicksort algorithm using recursion. Quicksort picks a pivot element, partitions the array, and recursively sorts the partitions.

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quicksort(left) + [pivot] + quicksort(right)

# Example
print(quicksort([3, 5, 1, 4, 2]))  # Output: [1, 2, 3, 4, 5]
```

1. **N-Queens Problem**:
   * Solve the N-Queens problem using recursion. Place (N) queens on an (N \times N) chessboard so that no two queens threaten each other.

```python
def solve_n_queens(n):
    board = [-1] * n
    def is_safe(row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == row - i:
                return False
        return True

    def place_queens(row):
        if row == n:
            print(board)
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                place_queens(row + 1)

    place_queens(0)

# Example
solve_n_queens(4)
```

1. **Combination Sum Problem**:
   * Given a set of candidate numbers and a target sum, write a recursive function to find all unique combinations that sum up to the target.

```python
def combination_sum(candidates, target, path=[], index=0):
    if target == 0:
        print(path)
        return
    if target < 0:
        return
    for i in range(index, len(candidates)):
        combination_sum(candidates, target - candidates[i], path + [candidates[i]], i)

# Example
combination_sum([2, 3, 6, 7], 7)
```

1. **Reverse a Linked List**:
   * Reverse a singly linked list using recursion.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    if not head or not head.next:
        return head
    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

1. **Sudoku Solver**:
   * Implement a recursive solution to solve a Sudoku puzzle by filling the grid in a valid way.

```python
def solve_sudoku(board):
    def is_valid(r, c, n):
        for i in range(9):
            if board[r][i] == n or board[i][c] == n or board[3*(r//3)+i//3][3*(c//3)+i%3] == n:
                return False
        return True

    def backtrack():
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for n in "123456789":
                        if is_valid(r, c, n):
                            board[r][c] = n
                            if backtrack():
                                return True
                            board[r][c] = "."
                    return False
        return True

    backtrack()
```



15. **Flatten a Nested List**:
    * Write a recursive function to flatten a nested list (i.e., a list containing sublists).

```python
def flatten_list(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result

# Example
print(flatten_list([1, [2, [3, 4]], 5]))  # Output: [1, 2, 3, 4, 5]
```

***

#### Summary:

Recursion is a fundamental technique in computer science, especially useful for solving problems that have a natural recursive structure like divide and conquer algorithms, tree traversals, and combinatorial problems. While recursion can simplify code, it also comes with challenges like increased memory usage and the potential for stack overflow.









Here are some tips and tricks for mastering recursion algorithms in software engineering interviews:

#### 1. **Understand Recursion**

* Recursion is a method where a function calls itself to solve smaller instances of the same problem.
* It often simplifies the problem-solving process by breaking down complex problems into simpler subproblems.

#### 2. **Identify Recursive Problems**

* Look for problems that can be defined in terms of smaller subproblems. Common indicators include:
  * Problems with a recursive structure, such as calculating factorials or Fibonacci numbers.
  * Problems involving tree traversals, backtracking, and combinatorial algorithms.

#### 3. **Base Cases**

* Clearly define base cases that indicate when the recursion should stop. This prevents infinite recursion.
* Base cases typically handle the simplest instances of the problem (e.g., the factorial of 0 or 1 is 1).

#### 4. **Recursive Cases**

* Define how to break the problem down into smaller subproblems. Each recursive call should move closer to a base case.
* Make sure to include the necessary logic for combining results from the subproblems if applicable.

#### 5. **Draw the Recursive Tree**

* For complex recursive functions, drawing a recursive call tree can help visualize the structure and flow of the algorithm.
* This can clarify how many times functions are called and how results are combined.

#### 6. **Memoization**

* Use memoization (caching results of expensive function calls) to optimize recursive solutions for problems with overlapping subproblems, like Fibonacci numbers or dynamic programming scenarios.
* This can dramatically reduce the time complexity by avoiding repeated calculations.

#### 7. **Tail Recursion**

* If applicable, consider using tail recursion, where the recursive call is the last operation in the function. This can optimize space usage in some programming languages.
* However, not all languages optimize tail recursion, so be aware of the specifics of the language you're using.

#### 8. **Iterative vs. Recursive Solutions**

* Some problems can be solved both recursively and iteratively. Be prepared to discuss the pros and cons of each approach.
* Recursive solutions may be more intuitive, while iterative solutions can be more efficient in terms of space.

#### 9. **Stack Overflow Considerations**

* Be mindful of the maximum recursion depth, especially for problems with large input sizes. Deep recursion can lead to stack overflow errors.
* For very deep recursive problems, consider converting the solution to an iterative approach.

#### 10. **Practice Common Recursive Problems**

* Familiarize yourself with classic recursive problems, such as:
  * **Factorial Calculation**: Compute the factorial of a number.
  * **Fibonacci Sequence**: Find the n-th Fibonacci number using recursion.
  * **Binary Tree Traversals**: Implement pre-order, in-order, and post-order traversals recursively.
  * **Permutations and Combinations**: Generate all permutations or combinations of a given set.

#### 11. **Debugging Techniques**

* If your recursive solution isn’t working, use print statements to trace the values of variables and the depth of recursion.
* Validate your approach with small inputs to ensure it produces the expected results.

#### 12. **Edge Cases and Constraints**

* Always consider edge cases and constraints, such as negative inputs, empty inputs, or maximum input sizes.

#### 13. **Communicate Your Thought Process**

* During interviews, clearly articulate your thought process, especially your reasoning for the base cases and recursive cases.
* Explain how you would handle edge cases and what you expect the function to return for them.

#### 14. **Refine Your Solution**

* After finding a solution, review it for possible optimizations or clearer implementations.
* Discuss how you could improve the efficiency or clarity of your recursive solution.

#### 15. **Key Takeaways for Interviews**

* Be prepared to explain why you chose recursion for a specific problem and how it simplifies the solution.
* If you encounter difficulties, talk through your thought process to give the interviewer insight into your problem-solving approach.

By mastering these principles and practicing various recursive problems, you'll be well-prepared for relevant questions in your software engineering interviews. If you want to explore specific recursive problems or concepts, feel free to ask!

***

## Common problems for me&#x20;

Given an array, arr, of integers, write arecursive function that add sum of all the previous numbers to each index of the array.&#x20;

```python
def cumulative_sum(arr, index=1):
    # Base case: stop when we reach the end of the array
    if index == len(arr):
        return
    
    # Update the current index by adding the previous one
    arr[index] += arr[index - 1]
    
    # Recursive call for the next index
    cumulative_sum(arr, index + 1)

# Example usage:
arr = [1, 2, 3, 4]
cumulative_sum(arr)
print(arr)  # Output: [1, 3, 6, 10]
```

