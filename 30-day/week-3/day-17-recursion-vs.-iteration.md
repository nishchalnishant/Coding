# Day 17: Recursion vs. Iteration

Here are detailed notes for **Day 17: Recursion vs. Iteration**. This day focuses on understanding the differences between recursion and iteration, along with practicing converting recursive solutions to iterative ones.

***

#### 1. **Recursion Overview**

Recursion is a method where a function calls itself to solve smaller subproblems. It often leads to simpler and cleaner code for problems that can be divided into similar subproblems.

**1.1 Key Characteristics of Recursion**

* **Base Case**: The condition under which the recursive calls stop.
* **Recursive Case**: The part of the function that includes the recursive call.
* **Stack Memory**: Each recursive call uses stack space, which can lead to stack overflow if the recursion depth is too large.

#### 2. **Iteration Overview**

Iteration involves using loops to repeat a block of code until a certain condition is met. It usually uses less memory than recursion and can be more efficient for certain problems.

**2.1 Key Characteristics of Iteration**

* **Control Flow**: Uses loops (e.g., for, while) to repeat actions.
* **No Stack Memory**: Iteration does not involve function calls, thus avoiding stack overflow.
* **State Maintenance**: State is maintained using variables outside the loop.

#### 3. **Comparing Recursion and Iteration**

| Feature        | Recursion                                       | Iteration                           |
| -------------- | ----------------------------------------------- | ----------------------------------- |
| Structure      | Simplifies code for complex problems            | Often leads to more complex code    |
| Memory Usage   | Uses stack memory for each call                 | Generally uses constant space       |
| Performance    | Can be slower due to overhead of function calls | Generally faster and more efficient |
| Stack Overflow | Possible if depth is too high                   | Not a concern                       |

#### 4. **Converting Recursion to Iteration**

To convert a recursive algorithm into an iterative one, you typically need to:

* Use a loop instead of recursive calls.
* Maintain an explicit stack or use variables to manage the state.

**4.1 Example: Factorial Calculation**

**Recursive Approach**

```python
def factorial_recursive(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)

# Example Usage
print(factorial_recursive(5))  # Output: 120
```

**Iterative Approach**

```python
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Example Usage
print(factorial_iterative(5))  # Output: 120
```

#### 5. **Example: Fibonacci Series**

**Recursive Approach**

```python
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# Example Usage
print(fibonacci_recursive(5))  # Output: 5
```

**Iterative Approach**

```python
def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Example Usage
print(fibonacci_iterative(5))  # Output: 5
```

#### 6. **Practice Problems**

1. **Binary Search**: Implement both recursive and iterative versions of binary search.
2. **Tower of Hanoi**: Solve the Tower of Hanoi problem recursively and convert it to an iterative approach.
3. **Depth-First Search (DFS)**: Implement both recursive and iterative DFS for a binary tree or graph.
4. **Power Function**: Implement the power function (x^n) recursively and iteratively.

#### 7. **Tips for Transitioning from Recursion to Iteration**

* **Use an Explicit Stack**: If the recursive function relies heavily on the call stack, replicate this with an explicit stack data structure.
* **Maintain State with Variables**: Keep track of necessary variables to simulate the recursion depth and manage state.
* **Test for Base Cases**: Ensure to replicate the base case condition within the iteration.

#### 8. **When to Use Each Approach**

* **Recursion**: Use when the problem can naturally be divided into similar subproblems (e.g., tree traversal, divide and conquer algorithms).
* **Iteration**: Prefer for problems that involve simple repetition or where performance and memory efficiency are critical (e.g., traversing arrays).

By understanding the differences between recursion and iteration and practicing conversions between the two, you'll become a more versatile programmer capable of choosing the best approach for various problems.
