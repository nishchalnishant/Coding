# Searching

Techniques to retrieve an item or check for a condition in a collection.

## Core Algorithms
- **Linear Search**: $O(N)$ time. Used when data is unsorted.
- **Binary Search**: $O(\log N)$ time. Requires sorted (or monotonic) data.
  - *Standard Binary Search*: `mid = left + (right - left) // 2`
  - *Lower Bound*: Find first index $i$ such that $arr[i] \ge target$.
  - *Upper Bound*: Find first index $i$ such that $arr[i] > target$.

## Binary Search on Answer
A very common pattern for "Minimizing the maximum" or "Maximizing the minimum". 
1. Determine the range of possible answers `[low, high]`.
2. Write an `is_valid(mid)` boolean function that checks if a value `mid` satisfies the required condition in $O(N)$ time.
3. Binary search the range using `is_valid()`.

## Common SDE-3 Searching Problems
- *Easy*: Binary Search, First Bad Version, Guess Number Higher or Lower.
- *Medium*: Search in Rotated Sorted Array, Find First and Last Position of Element, Koko Eating Bananas (Binary Search on Answer).
- *Hard*: Median of Two Sorted Arrays, Split Array Largest Sum, Aggressive Cows.
