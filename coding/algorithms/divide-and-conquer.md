---
tags: [coding, algorithms, divide-and-conquer]
topic: Divide and Conquer
difficulty: mixed
---

# Divide and Conquer — Amazon SDE-2

---

## Conceptual Framework

D&C splits a problem into independent subproblems, solves each recursively, then combines results.

Three steps:
1. **Divide**: split into subproblems of the same type (often at midpoint)
2. **Conquer**: recurse until base case
3. **Combine**: merge results — this step is where most of the work happens

Master Theorem quick reference:
- T(n) = 2T(n/2) + O(n) → O(n log n) — merge sort
- T(n) = 2T(n/2) + O(1) → O(n) — binary search
- T(n) = T(n/k) + O(n) → O(n log_k n)

---

## Merge Sort — Canonical D&C

Stable sort. T(n) = 2T(n/2) + O(n) → O(n log n).

```python
def merge_sort(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Key insight for interviews**: merge sort is the canonical "combine step is expensive" example. When a problem requires counting inversions or pairs across halves, reach for merge sort.

---

### Count of Smaller Numbers After Self (Merge Sort)

> [!example] Problem
> Given integer array nums, return array counts where `counts[i]` = number of smaller elements to the right of `nums[i]`. LeetCode 315.

> [!info] Approach
> Each element that "jumps over" a right-side element during merge is a smaller-after-self pair. Track original indices through the merge. When taking from the right array, those elements are smaller than everything remaining in the left array.

> [!note]- Python Solution
> ```python
> def count_smaller(nums):
>     n = len(nums)
>     result = [0] * n
>     indexed = list(enumerate(nums))   # (original_idx, value)
>
>     def merge_sort(arr):
>         if len(arr) <= 1:
>             return arr
>         mid = len(arr) // 2
>         left = merge_sort(arr[:mid])
>         right = merge_sort(arr[mid:])
>         return merge(left, right)
>
>     def merge(left, right):
>         merged = []
>         i = j = right_count = 0
>         while i < len(left) and j < len(right):
>             if right[j][1] < left[i][1]:
>                 merged.append(right[j])
>                 j += 1
>                 right_count += 1
>             else:
>                 result[left[i][0]] += right_count
>                 merged.append(left[i])
>                 i += 1
>         while i < len(left):
>             result[left[i][0]] += right_count
>             merged.append(left[i])
>             i += 1
>         merged.extend(right[j:])
>         return merged
>
>     merge_sort(indexed)
>     return result
> ```

> [!success] Complexity
> Time O(n log n) | Space O(n).

---

## Binary Search as D&C

Binary search is D&C where one subproblem is always discarded. T(n) = T(n/2) + O(1) → O(log n).

The key invariant in every binary search variant: **what is the loop invariant?** The answer always lies within `[lo, hi]`.

---

### Median of Two Sorted Arrays

> [!example] Problem
> Given two sorted arrays nums1 and nums2, return the median in O(log(m+n)) time. LeetCode 4.

> [!info] Approach
> Binary search on the partition index of the smaller array. Partition both arrays such that left half total size = right half total size. Verify `max(left1, left2) <= min(right1, right2)`. If `left1 > right2`, move partition left; if `left2 > right1`, move partition right.

> [!note]- Python Solution
> ```python
> def find_median_sorted_arrays(nums1, nums2):
>     if len(nums1) > len(nums2):
>         nums1, nums2 = nums2, nums1
>     m, n = len(nums1), len(nums2)
>     lo, hi = 0, m
>     while lo <= hi:
>         i = (lo + hi) // 2
>         j = (m + n + 1) // 2 - i
>         max_left1 = float('-inf') if i == 0 else nums1[i - 1]
>         min_right1 = float('inf') if i == m else nums1[i]
>         max_left2 = float('-inf') if j == 0 else nums2[j - 1]
>         min_right2 = float('inf') if j == n else nums2[j]
>         if max_left1 <= min_right2 and max_left2 <= min_right1:
>             if (m + n) % 2 == 1:
>                 return float(max(max_left1, max_left2))
>             return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
>         elif max_left1 > min_right2:
>             hi = i - 1
>         else:
>             lo = i + 1
> ```

> [!success] Complexity
> Time O(log(min(m, n))) | Space O(1).

---

### Search in Rotated Sorted Array

> [!example] Problem
> Array sorted then rotated at unknown pivot. Find target index or -1. LeetCode 33.

> [!info] Approach
> At least one half is always sorted. Identify which half, check if target lies in it, recurse into it; otherwise recurse into the other half.

> [!note]- Python Solution
> ```python
> def search(nums, target):
>     lo, hi = 0, len(nums) - 1
>     while lo <= hi:
>         mid = (lo + hi) // 2
>         if nums[mid] == target:
>             return mid
>         if nums[lo] <= nums[mid]:          # left half sorted
>             if nums[lo] <= target < nums[mid]:
>                 hi = mid - 1
>             else:
>                 lo = mid + 1
>         else:                               # right half sorted
>             if nums[mid] < target <= nums[hi]:
>                 lo = mid + 1
>             else:
>                 hi = mid - 1
>     return -1
> ```

> [!success] Complexity
> Time O(log n) | Space O(1).

---

### Find Minimum in Rotated Sorted Array

> [!example] Problem
> Find the minimum in a sorted rotated array of unique elements. LeetCode 153.

> [!info] Approach
> Minimum is the rotation inflection point. If `nums[mid] > nums[hi]`, minimum is in right half; else it's in left half (including mid).

> [!note]- Python Solution
> ```python
> def find_min(nums):
>     lo, hi = 0, len(nums) - 1
>     while lo < hi:
>         mid = (lo + hi) // 2
>         if nums[mid] > nums[hi]:
>             lo = mid + 1
>         else:
>             hi = mid
>     return nums[lo]
> ```

> [!success] Complexity
> Time O(log n) | Space O(1).

> [!tip] Duplicates
> With duplicates (LC 154): when `nums[mid] == nums[hi]`, do `hi -= 1`. Degrades to O(n) worst case.

---

## QuickSelect — Kth Largest/Smallest

QuickSelect partitions around a pivot like quicksort but only recurses into one half. Average O(n), worst O(n²) — use random pivot to avoid worst case.

```python
import random

def quick_select(nums, k):
    """Return the kth largest element (1-indexed)."""
    target = len(nums) - k   # kth largest = (n-k)th smallest in 0-indexed

    def partition(lo, hi):
        pivot_idx = random.randint(lo, hi)
        nums[pivot_idx], nums[hi] = nums[hi], nums[pivot_idx]
        pivot = nums[hi]
        store = lo
        for i in range(lo, hi):
            if nums[i] <= pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1
        nums[store], nums[hi] = nums[hi], nums[store]
        return store

    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        p = partition(lo, hi)
        if p == target:
            return nums[p]
        elif p < target:
            lo = p + 1
        else:
            hi = p - 1
```

**Complexity**: Average O(n), worst O(n²) with random pivot (degenerate O(n²) negligible). Space O(1).

---

### Kth Largest Element in an Array

> [!example] Problem
> Return the kth largest element in the array (not kth distinct). LeetCode 215.

> [!note]- Python Solution
> ```python
> import heapq
>
> def find_kth_largest(nums, k):
>     # Min-heap of size k — simpler, O(n log k)
>     return heapq.nlargest(k, nums)[-1]
>     # OR: QuickSelect — O(n) average
> ```

> [!success] Complexity
> Heap: O(n log k) | QuickSelect: O(n) average.

> [!tip] Which to use
> For small k relative to n: heap is simpler and safe. If interviewer asks for O(n), use QuickSelect.

---

## Tree Construction D&C

### Construct Binary Tree from Preorder and Inorder

> [!example] Problem
> Reconstruct binary tree from preorder and inorder traversal arrays. LeetCode 105.

> [!info] Approach
> First element of preorder is root. Locate root in inorder: elements to its left are the left subtree, elements to its right are the right subtree. Recurse with corresponding slices. Precompute `{value: inorder_index}` map for O(1) lookup.

> [!note]- Python Solution
> ```python
> def build_tree(preorder, inorder):
>     idx_map = {v: i for i, v in enumerate(inorder)}
>     pre_iter = iter(preorder)
>
>     def build(in_lo, in_hi):
>         if in_lo > in_hi:
>             return None
>         root_val = next(pre_iter)
>         root = TreeNode(root_val)
>         k = idx_map[root_val]
>         root.left = build(in_lo, k - 1)
>         root.right = build(k + 1, in_hi)
>         return root
>
>     return build(0, len(inorder) - 1)
> ```

> [!success] Complexity
> Time O(n) | Space O(n) for index map + O(h) call stack.

---

## Maximum Subarray D&C

### Maximum Subarray (Divide and Conquer)

> [!example] Problem
> Find the contiguous subarray with the maximum sum. LeetCode 53.

> [!info] Approach
> Max-sum subarray lies entirely in left half, entirely in right half, or crosses the midpoint. The cross-subarray max = max suffix of left + max prefix of right. Combine: `max(left_best, right_best, cross_best)`.

> [!note]- Python Solution
> ```python
> def max_sub_array(nums):
>     def max_cross(lo, mid, hi):
>         left_sum, s = float('-inf'), 0
>         for i in range(mid, lo - 1, -1):
>             s += nums[i]
>             left_sum = max(left_sum, s)
>         right_sum, s = float('-inf'), 0
>         for i in range(mid + 1, hi + 1):
>             s += nums[i]
>             right_sum = max(right_sum, s)
>         return left_sum + right_sum
>
>     def dc(lo, hi):
>         if lo == hi:
>             return nums[lo]
>         mid = (lo + hi) // 2
>         return max(dc(lo, mid), dc(mid + 1, hi), max_cross(lo, mid, hi))
>
>     return dc(0, len(nums) - 1)
> ```

> [!success] Complexity
> Time O(n log n) — T(n) = 2T(n/2) + O(n) | Space O(log n) call stack.

> [!tip] Alternatives
> Kadane's: O(n) time, O(1) space — always preferred in practice. D&C version is the CLRS canonical and demonstrates the crossing-subarray technique.

---

## Expression D&C

### Different Ways to Add Parentheses

> [!example] Problem
> Given an expression string with +, -, * operators and numbers, return all possible results from all groupings. LeetCode 241.

> [!info] Approach
> Each operator can be the "last" operation (root of expression tree). Split at each operator, recurse left and right sub-expressions, combine every pair from left × right using the operator.

> [!note]- Python Solution
> ```python
> def diff_ways_to_compute(expression):
>     memo = {}
>
>     def solve(s):
>         if s in memo:
>             return memo[s]
>         results = []
>         for i, ch in enumerate(s):
>             if ch in '+-*':
>                 for l in solve(s[:i]):
>                     for r in solve(s[i+1:]):
>                         if ch == '+': results.append(l + r)
>                         elif ch == '-': results.append(l - r)
>                         else: results.append(l * r)
>         if not results:
>             results.append(int(s))
>         memo[s] = results
>         return results
>
>     return solve(expression)
> ```

> [!success] Complexity
> Time O(n · Cₙ) where Cₙ = nth Catalan number (exponential in operator count) | Space O(Cₙ).

---

## See Also

[[sorting]] | [[binary-search]] | [[recursion]] | [[heap]]
