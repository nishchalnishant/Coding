# Recursion

A problem-solving technique where a function calls itself to solve smaller instances of the same problem.

## Key Concepts
- **Base Case**: The simplest version of the problem where the function stops calling itself. Essential to prevent infinite loops / Stack Overflow.
- **Recursive Step**: The part of the function where it calls itself with a smaller/simpler input, moving towards the base case.
- **Call Stack**: Every recursive call pushes the current state onto the memory stack. Limits maximum depth (usually ~1000 in Python, varies by language).

## Types of Recursion
- **Head/Pre Recursion**: Operations are performed *before* the recursive call.
- **Tail/Post Recursion**: The recursive call is the very last operation. Many compilers can optimize this to use $O(1)$ stack space (Tail Call Optimization).
- **Tree Recursion**: The function makes multiple recursive calls (e.g., Fibonacci, Tree DFS). Time complexity is typically exponential unless memoized.

## Optimizations & Variations
- **Memoization**: Cache results of expensive recursive calls to avoid redundant work (Top-Down Dynamic Programming).
- **Backtracking**: A form of recursion that builds a solution incrementally and abandons a path ("backtracks") as soon as it determines the path cannot lead to a valid solution.

## Common SDE-3 Recursion Problems
- *Easy*: Fibonacci Number, Factorial, Reverse Linked List, Same Tree.
- *Medium*: Subsets, Permutations, Combinations, Validate Binary Search Tree.
- *Hard*: Serialize and Deserialize Binary Tree, Word Search II, Regular Expression Matching.
