# Array

A fixed-size sequential collection of elements of the same type stored in contiguous memory.

## Key Concepts
- **Memory**: Contiguous allocation allows $O(1)$ index access.
- **Operations**:
  - *Access/Update*: $O(1)$
  - *Search*: $O(N)$ linear, $O(\log N)$ binary (if sorted).
  - *Insertion/Deletion*: $O(N)$ (requires shifting elements).
- **Variations**: Dynamic Arrays (ArrayList), Sparse Arrays, 2D/3D Matrices.

## Core Techniques
- **Two-Pointer**: Efficiently search pairs or reverse subarrays in $O(N)$.
- **Sliding Window**: Track conditions (sum, max, unique elements) across contiguous subarrays.
- **Prefix Sum**: Pre-calculate cumulative sums to allow $O(1)$ range sum queries.
- **Kadane’s Alg**: Finding maximum contiguous subarray sum in $O(N)$.

## Common SDE-3 Array Problems
- *Easy*: Two Sum, Best Time to Buy/Sell Stock, Move Zeroes, Missing Number.
- *Medium*: 3Sum, Product of Array Except Self, Subarray Sum Equals K, Merge Intervals.
- *Hard*: Trapping Rain Water, Maximum Product Subarray, Median of Two Sorted Arrays, Minimum Number of Operations to Make Array Continuous.
