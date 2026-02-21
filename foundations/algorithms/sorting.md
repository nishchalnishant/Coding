# Sorting

Arranging data in a specific order to optimize subsequent operations (like searching or merging).

## Big-O Overview
| Algorithm      | Average Time | Worst Time | Space | Stable? | Best Used For |
| -------------- | ------------ | ---------- | ----- | ------- | ------------- |
| **Bubble** | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | Educational only |
| **Insertion** | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | Nearly sorted or tiny arrays |
| **Merge Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes | Linked Lists, guaranteed $N \log N$ |
| **Quick Sort** | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$| No | Large arrays in-memory (fastest practically) |
| **Heap Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(1)$ | No | $O(1)$ space requirement with $O(N \log N)$ guarantee |
| **Counting** | $O(N + K)$| $O(N + K)$ | $O(K)$ | Yes | Small integer ranges |
| **Radix** | $O(d(N+b))$| $O(d(N+b))$| $O(N+b)$| Yes | Fixed-width keys or digit processing |

## Core Techniques
- **Merge Process**: Two-pointer iteration to combine two sorted structures in $O(N)$ time.
- **Partitioning (QuickSort)**: Choosing a pivot and placing all smaller elements to the left, larger to the right. Use the Dutch National Flag algorithm for 3-way partitioning.
- **Top K Elements (QuickSelect)**: A variation of QuickSort that only recurses into the partition containing the target rank $K$. Average time $O(N)$.
- **Custom Comparators**: Implement custom sorting logic when dealing with complex objects or intervals (e.g., sort intervals by start time).

## Common SDE-3 Sorting Problems
- *Easy*: Merge Sorted Array, Squares of a Sorted Array, Valid Anagram (by sorting).
- *Medium*: Sort Colors (Dutch National Flag), Merge Intervals, Sort List, Top K Frequent Elements (Bucket sort).
- *Hard*: Count Inversions, Maximum Gap (Pigeonhole principle), Optimal Account Balancing.
