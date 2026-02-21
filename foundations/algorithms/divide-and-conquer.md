# Divide and Conquer

An algorithmic paradigm that breaks a problem into smaller, independent subproblems of the same type, solves them recursively, and then combines their solutions.

## The Three Steps
1. **Divide**: Break the problem into smaller subproblems.
2. **Conquer**: Solve the subproblems recursively. If they are small enough, solve them directly (base case).
3. **Combine**: Merge the results of the subproblems to form the final solution.

## Key Algorithms
- **Merge Sort**: Divide array in half, sort each half, merge sorted halves. $O(N \log N)$ time, $O(N)$ space.
- **Quick Sort**: Pick a pivot, partition array into $\le$ pivot and $>$ pivot, then sort both parts. Average $O(N \log N)$ time, $O(\log N)$ space.
- **Binary Search**: Divide search space in half based on comparison. $O(\log N)$ time.
- **Strassen's Matrix Multiplication**: Optimized way to multiply matrices.

## Divide & Conquer vs Dynamic Programming
- **Divide & Conquer**: Subproblems are *independent* and do not overlap (e.g., sorting left half and right half of an array).
- **Dynamic Programming**: Subproblems *overlap*. DP stores the results to avoid re-computing them.

## Common SDE-3 Problems
- *Easy*: Merge Two Sorted Lists (building block), Majority Element (can be done with D&C).
- *Medium*: Sort List, Kth Largest Element in an Array (QuickSelect), Search a 2D Matrix II.
- *Hard*: Merge k Sorted Lists, Median of Two Sorted Arrays, Count of Smaller Numbers After Self, Reverse Pairs.
