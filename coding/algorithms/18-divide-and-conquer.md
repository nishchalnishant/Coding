---
tags: [coding, algorithms, divide-and-conquer]
topic: Divide and Conquer
difficulty: mixed
---

# Divide and Conquer — Problem Reference by Pattern

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.


> [!info] First Principles
> D&C = split into *independent* subproblems of the same type, solve each recursively, combine results. Complexity is governed by the Master Theorem: T(n) = aT(n/b) + f(n). The key invariant: subproblems share *no* state — solving the left half never influences the right half. When subproblems overlap, use DP instead.




---

## Classic D&C

### Merge Sort (Implementation) `🎯 T2`

> [!example] Problem
> Sort an array in guaranteed O(n log n).

> [!info] Approach
> Split into two independent halves; sorting each independently produces sorted sub-arrays whose combination (merge) is O(n). T(n) = 2T(n/2) + O(n) → O(n log n) by Master Theorem Case 2. Recursively split at midpoint; merge two sorted halves with two-pointer technique. Base case len ≤ 1. Recurse left and right. Merge: advance the smaller of two pointers into result; append remainders. The combine step is the algorithm's core.

> [!note]- Python Solution
> ```python
> def merge_sort(nums):
>     if len(nums) <= 1:
>         return nums
>     mid = len(nums) // 2
>     left = merge_sort(nums[:mid])
>     right = merge_sort(nums[mid:])
>     return _merge(left, right)
> 
> def _merge(left, right):
>     result = []
>     i = j = 0
>     while i < len(left) and j < len(right):
>         if left[i] <= right[j]:
>             result.append(left[i])
>             i += 1
>         else:
>             result.append(right[j])
>             j += 1
>     result.extend(left[i:])
>     result.extend(right[j:])
>     return result
> ```

> [!success] Complexity
> Time O(n log n) — all cases. Space O(n) merge buffer + O(log n) call stack.

> [!tip] Alternatives
> Bottom-up iterative merge sort — same complexity, O(log n) stack eliminated. TimSort (Python's built-in) — adaptive, O(n) on nearly-sorted data. Quicksort — O(n log n) average, O(n²) worst, O(1) extra space.

---

### Median of Two Sorted Arrays `⚡ T1`

> [!example] Problem
> Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
> The overall run time complexity should be O(log (m+n)).
> 
> **Example 1:**
> ```
> Input: nums1 = [1,3], nums2 = [2]
> Output: 2.00000
> Explanation: merged array = [1,2,3] and median is 2.
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [1,2], nums2 = [3,4]
> Output: 2.50000
> Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
> ```
> 
> **Constraints:**
> - nums1.length == m
> - nums2.length == n
> - 0 <= m <= 1000
> - 0 <= n <= 1000
> - 1 <= m + n <= 2000
> - -10^6 <= nums1[i], nums2[i] <= 10^6

> [!info] Approach
> A median partitions elements into equal halves. Binary search on the partition point of the smaller array: if partition `i` of `A` and `j = (m+n+1)//2 - i` of `B` satisfy `A[i-1] ≤ B[j]` and `B[j-1] ≤ A[i]`, we found the correct split. Binary search on shorter array's partition index; adjust based on cross-comparisons. Ensure `A` is shorter. Binary search `lo` to `hi` (size of `A`). At midpoint `i`, compute `j`. If `A[i-1] > B[j]`, go left; if `B[j-1] > A[i]`, go right; else compute median from boundary values.

> [!note]- Python Solution
> ```python
> def find_median_sorted_arrays(nums1, nums2):
>     A, B = nums1, nums2
>     if len(A) > len(B):
>         A, B = B, A
>     m, n = len(A), len(B)
>     half = (m + n + 1) // 2
>     lo, hi = 0, m
>     while lo <= hi:
>         i = (lo + hi) // 2
>         j = half - i
>         a_left  = A[i-1] if i > 0 else float('-inf')
>         a_right = A[i]   if i < m else float('inf')
>         b_left  = B[j-1] if j > 0 else float('-inf')
>         b_right = B[j]   if j < n else float('inf')
>         if a_left <= b_right and b_left <= a_right:
>             max_left = max(a_left, b_left)
>             if (m + n) % 2:
>                 return float(max_left)
>             return (max_left + min(a_right, b_right)) / 2.0
>         elif a_left > b_right:
>             hi = i - 1
>         else:
>             lo = i + 1
>     return 0.0
> ```

> [!success] Complexity
> Time O(log(min(m,n))). Space O(1).

> [!tip] Alternatives
> Merge both arrays — O(m+n) time and space. Binary search on the kth element — same asymptotic, different formulation.

---

### Majority Element (D&C Approach) `🎯 T2`

> [!example] Problem
> Given an array nums of size n, return the majority element.
> The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.
> 
> **Example 1:**
> ```
> Input: nums = [3,2,3]
> Output: 3
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,2,1,1,1,2,2]
> Output: 2
> ```
> 
> **Constraints:**
> - n == nums.length
> - 1 <= n <= 5 * 10^4
> - -10^9 <= nums[i] <= 10^9

> [!info] Approach
> If an element is majority in the full array, it must be the majority in at least one half. D&C: find majority of left and right; if they agree, that's the answer; if not, verify each candidate against the full range. Recurse to find candidate in each half; verify both in current range. Base: single element is its own majority. Count occurrences of left and right candidates in the full subarray; return whichever exceeds half.

> [!note]- Python Solution
> ```python
> def majority_element(nums):
>     def majority_range(lo, hi):
>         if lo == hi:
>             return nums[lo]
>         mid = (lo + hi) // 2
>         left = majority_range(lo, mid)
>         right = majority_range(mid + 1, hi)
>         if left == right:
>             return left
>         left_count = sum(1 for i in range(lo, hi + 1) if nums[i] == left)
>         right_count = sum(1 for i in range(lo, hi + 1) if nums[i] == right)
>         return left if left_count > right_count else right
> 
>     return majority_range(0, len(nums) - 1)
> ```

> [!success] Complexity
> Time O(n log n) — T(n) = 2T(n/2) + O(n) verification. Space O(log n) stack.

> [!tip] Alternatives
> Boyer-Moore voting algorithm — O(n) time, O(1) space. Counting with a dict — O(n) time, O(n) space. For interviews, Boyer-Moore is preferred.

---

### Majority Element II `🎯 T2`

> [!example] Problem
> Given an integer array of size n, find all elements that appear more than ⌊ n/3 ⌋ times.
> 
> **Example 1:**
> ```
> Input: nums = [3,2,3]
> Output: [3]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1]
> Output: [1]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,2]
> Output: [1,2]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 5 * 10^4
> - -10^9 <= nums[i] <= 10^9

> [!info] Approach
> At most 2 candidates can exceed n/3. Boyer-Moore extended to two candidates; then verify both in a second pass. Two-candidate Boyer-Moore voting; verify counts in second pass. Maintain two `(candidate, count)` pairs. On each element: if matches candidate, increment; else decrement both; if count reaches 0, replace. Final verification pass confirms actual frequency.

> [!note]- Python Solution
> ```python
> def majority_element(nums):
>     cand1 = cand2 = None
>     cnt1 = cnt2 = 0
>     for n in nums:
>         if n == cand1:
>             cnt1 += 1
>         elif n == cand2:
>             cnt2 += 1
>         elif cnt1 == 0:
>             cand1, cnt1 = n, 1
>         elif cnt2 == 0:
>             cand2, cnt2 = n, 1
>         else:
>             cnt1 -= 1
>             cnt2 -= 1
> 
>     threshold = len(nums) // 3
>     return [c for c in (cand1, cand2) if c is not None and nums.count(c) > threshold]
> ```

> [!success] Complexity
> Time O(n). Space O(1).

> [!tip] Alternatives
> Hash map frequency count — O(n) time and space. D&C generalization is complex and less efficient.

---

## Matrix / 2D D&C

### Maximum Gap (Conceptual)

> [!example] Problem
> Given an integer array nums, return the maximum difference between two successive elements in its sorted form. If the array contains less than two elements, return 0.
> You must write an algorithm that runs in linear time and uses linear extra space.
> 
> **Example 1:**
> ```
> Input: nums = [3,6,9,1]
> Output: 3
> Explanation: The sorted form of the array is [1,3,6,9], either (3,6) or (6,9) has the maximum difference 3.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [10]
> Output: 0
> Explanation: The array contains less than 2 elements, therefore return 0.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - 0 <= nums[i] <= 10^9

> [!info] Approach
> Sorting gives O(n log n). Bucket/radix approach: by pigeonhole, the maximum gap must span at least one empty bucket. Place elements into n-1 buckets of size `(max-min)/(n-1)`. Max gap = max over consecutive non-empty buckets. Bucket sort on the value range; track min/max within each bucket; scan gaps between consecutive non-empty buckets. Bucket size = `ceil((max_val - min_val) / (n - 1))`. For each element, assign to bucket index. Track `(bucket_min, bucket_max)`. Answer = `max(next_min - curr_max)` across adjacent filled buckets.

> [!note]- Python Solution
> ```python
> import math
> 
> def maximum_gap(nums):
>     if len(nums) < 2:
>         return 0
>     min_val, max_val = min(nums), max(nums)
>     if min_val == max_val:
>         return 0
>     n = len(nums)
>     bucket_size = max(1, math.ceil((max_val - min_val) / (n - 1)))
>     bucket_count = (max_val - min_val) // bucket_size + 1
>     buckets = [[float('inf'), float('-inf')] for _ in range(bucket_count)]
>     for num in nums:
>         idx = (num - min_val) // bucket_size
>         buckets[idx][0] = min(buckets[idx][0], num)
>         buckets[idx][1] = max(buckets[idx][1], num)
>     max_gap = 0
>     prev_max = min_val
>     for bmin, bmax in buckets:
>         if bmin == float('inf'):
>             continue
>         max_gap = max(max_gap, bmin - prev_max)
>         prev_max = bmax
>     return max_gap
> ```

> [!success] Complexity
> Time O(n). Space O(n) buckets.

> [!tip] Alternatives
> Radix sort — O(n) deterministic. Sorting — O(n log n).

---

### Super Pow (Modular Exponentiation) `💤 T3`

> [!example] Problem
> Your task is to calculate ab mod 1337 where a is a positive integer and b is an extremely large positive integer given in the form of an array.
> 
> **Example 1:**
> ```
> Input: a = 2, b = [3]
> Output: 8
> ```
> 
> **Example 2:**
> ```
> Input: a = 2, b = [1,0]
> Output: 1024
> ```
> 
> **Example 3:**
> ```
> Input: a = 1, b = [4,3,3,8,5,2]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= a <= 2^{31} - 1
> - 1 <= b.length <= 2000
> - 0 <= b[i] <= 9
> - b does not contain leading zeros.

> [!info] Approach
> `b` is too large to compute directly. Key identity: `a^[d1,d2,...,dk] = (a^[d1,...,dk-1])^10 * a^dk`. Process exponent digit by digit using D&C recursion. Recursive reduction: `pow(a, b) = pow(pow(a, b[:-1]), 10) * pow(a, b[-1])`. Base case: `b` is empty → return 1. At each step, multiply `pow(pow(a, b[:-1]), 10, mod) * pow(a, b[-1], mod)`.

> [!note]- Python Solution
> ```python
> def super_pow(a, b):
>     MOD = 1337
> 
>     def fast_pow(base, exp):
>         result = 1
>         base %= MOD
>         while exp:
>             if exp & 1:
>                 result = result * base % MOD
>             base = base * base % MOD
>             exp >>= 1
>         return result
> 
>     result = 1
>     for digit in b:
>         result = fast_pow(result, 10) * fast_pow(a, digit) % MOD
>     return result
> ```

> [!success] Complexity
> Time O(n log 1337) ≈ O(n) where n = len(b). Space O(1).

> [!tip] Alternatives
> Compute `b mod phi(1337)` using Euler's theorem — requires handling gcd(a, 1337) != 1 separately.

---

### Closest Pair of Points `💤 T3`

> [!example] Problem
> Find the minimum Euclidean distance between any two points in a 2D set. Achieve better than O(n²).

> [!info] Approach
> Brute force checks all n(n-1)/2 pairs O(n²). D&C: minimum distance in each half is found recursively. Only points within a vertical strip of width `2δ` (δ = min of two halves' answers) can improve the global minimum. By geometric packing, each strip point has at most 7 candidates in the strip — so strip scan is O(n). Sort by x. Split at midpoint x-coordinate. Recurse each half. Check strip candidates within `δ` of the dividing line. Sort strip points by y. For each strip point, check at most the next 7 points (geometric argument: in a δ×2δ rectangle, at most 8 points with pairwise distance ≥ δ).

> [!note]- Python Solution
> ```python
> import math
> 
> def closest_pair(points, float]]):
>     pts = sorted(points)  # sort by x
> 
>     def dist(one_back, two_back):
>         return math.hypot(one_back[0] - two_back[0], one_back[1] - two_back[1])
> 
>     def rec(arr):
>         n = len(arr)
>         if n <= 3:
>             return min(dist(arr[i], arr[j])
>                        for i in range(n) for j in range(i+1, n))
>         mid = n // 2
>         mid_x = arr[mid][0]
>         d = min(rec(arr[:mid]), rec(arr[mid:]))
>         # Strip: points within d of dividing line
>         strip = sorted([p for p in arr if abs(p[0] - mid_x) < d], key=lambda p: p[1])
>         for i in range(len(strip)):
>             for j in range(i + 1, min(i + 8, len(strip))):
>                 if strip[j][1] - strip[i][1] >= d:
>                     break
>                 d = min(d, dist(strip[i], strip[j]))
>         return d
> 
>     return rec(pts)
> ```

> [!success] Complexity
> Time O(n log² n) — T(n) = 2T(n/2) + O(n log n) (strip sort). If pre-sorted by y, O(n log n). Space O(n log n) for strip copies.

> [!tip] Alternatives
> KD-tree — O(n log n) build, O(log n) queries. Randomized incremental algorithm — O(n) expected. For interviews, the D&C O(n log² n) version is standard.
>
> **3D Closest Pair concept:** The 2D algorithm extends to 3D: divide by x-coordinate; the strip becomes a slab of width `2δ`; by sphere-packing argument, at most ~20 candidates per slab point instead of 7. Complexity remains O(n log² n).

---

## Binary Search D&C

### Search in Rotated Sorted Array `⚡ T1`

> [!example] Problem
> There is an integer array nums sorted in ascending order (with distinct values).
> Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become [4,5,6,7,0,1,2].
> Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.
> You must write an algorithm with O(log n) runtime complexity.
> 
> **Example 1:**
> ```
> Input: nums = [4,5,6,7,0,1,2], target = 0
> Output: 4
> ```
> 
> **Example 2:**
> ```
> Input: nums = [4,5,6,7,0,1,2], target = 3
> Output: -1
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1], target = 0
> Output: -1
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 5000
> - -10^4 <= nums[i] <= 10^4
> - All values of nums are unique.
> - nums is an ascending array that is possibly rotated.
> - -10^4 <= target <= 10^4

> [!info] Approach
> Full scan is O(n). Binary search still works because at least one half of any split is always sorted — identify which half is sorted, check if target lies inside it, recurse into that half; otherwise recurse into the other. At each binary search step, determine the sorted half using the midpoint vs boundary comparison. Narrow to the half that can contain the target. If `nums[lo] <= nums[mid]`, left half is sorted. If `nums[lo] <= target < nums[mid]`, go left; else go right. Mirror logic when right half is sorted.

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
> Time O(log n). Space O(1).

> [!tip] Alternatives
> Find pivot index first (separate binary search), then binary search in the correct segment — two passes but same O(log n). Works for duplicates with minor modification (LC 81).

---

### Find Minimum in Rotated Sorted Array `⚡ T1`

> [!example] Problem
> Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,2,4,5,6,7] might become:
> Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].
> Given the sorted rotated array nums of unique elements, return the minimum element of this array.
> You must write an algorithm that runs in O(log n) time.
> 
> **Example 1:**
> ```
> Input: nums = [3,4,5,1,2]
> Output: 1
> Explanation: The original array was [1,2,3,4,5] rotated 3 times.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [4,5,6,7,0,1,2]
> Output: 0
> Explanation: The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [11,13,15,17]
> Output: 11
> Explanation: The original array was [11,13,15,17] and it was rotated 4 times.
> ```
> 
> **Constraints:**
> - n == nums.length
> - 1 <= n <= 5000
> - -5000 <= nums[i] <= 5000
> - All the integers of nums are unique.
> - nums is sorted and rotated between 1 and n times.

> [!info] Approach
> The minimum is the only point where `nums[i] > nums[i+1]` — the rotation inflection. Binary search exploits: if `nums[mid] > nums[hi]`, the minimum must be in the right half; otherwise it's in the left half (including mid). Binary search maintaining the invariant that the minimum is within `[lo, hi]`. Compare `nums[mid]` with `nums[hi]`. If `nums[mid] > nums[hi]`, `lo = mid + 1`. Else `hi = mid`. Converges when `lo == hi`.

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
> Time O(log n). Space O(1).

> [!tip] Alternatives
> With duplicates (LC 154): when `nums[mid] == nums[hi]`, shrink `hi -= 1` — degrades to O(n) worst case. Linear scan is O(n) but simpler.

---

## Tree Construction D&C

### Construct Binary Tree from Preorder and Inorder `🎯 T2`

> [!example] Problem
> Given preorder and inorder traversal arrays, reconstruct the binary tree.

> [!info] Approach
> The first element of preorder is always the root. Finding root in inorder splits it into left and right subtrees — the lengths of those segments tell us how many elements belong to each side in preorder. Classic D&C: each call solves an independent subproblem with no overlap. Root = `preorder[0]`. Locate root in inorder at index `k`. Left subtree uses `preorder[1:k+1]` and `inorder[:k]`; right uses the rest. Precompute an index map of `{value: inorder_index}` for O(1) lookup. Track preorder start offset instead of slicing to stay O(n) total.

> [!note]- Python Solution
> ```python
> from typing import Optional
> 
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val
>         self.left = left
>         self.right = right
> 
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
> Time O(n) — each node created once, O(1) lookup. Space O(n) for index map + O(h) call stack (h = tree height).

> [!tip] Alternatives
> Construct from postorder+inorder: root = `postorder[-1]`, same idea reversed. Construct from preorder+postorder only works for full binary trees.

---

## Maximum Subarray D&C

### Maximum Subarray (Divide and Conquer) `🎯 T2`

> [!example] Problem
> Given an integer array nums, find the subarray with the largest sum, and return its sum.
> 
> **Example 1:**
> ```
> Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
> Output: 6
> Explanation: The subarray [4,-1,2,1] has the largest sum 6.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1]
> Output: 1
> Explanation: The subarray [1] has the largest sum 1.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [5,4,-1,7,8]
> Output: 23
> Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> The max-sum subarray either lies entirely in the left half, entirely in the right half, or crosses the midpoint. Cross-subarray max = max suffix of left + max prefix of right, computable in O(n). T(n) = 2T(n/2) + O(n) → O(n log n). At each level: compute best-in-left, best-in-right, and best-crossing; return the maximum of the three. Cross sum: scan left from `mid` accumulating suffix max; scan right from `mid+1` accumulating prefix max; sum them.

> [!note]- Python Solution
> ```python
> def max_sub_array(nums):
>     def max_cross(lo, mid, hi):
>         left_sum = float('-inf')
>         s = 0
>         for i in range(mid, lo - 1, -1):
>             s += nums[i]
>             left_sum = max(left_sum, s)
>         right_sum = float('-inf')
>         s = 0
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
> Time O(n log n) — T(n) = 2T(n/2) + O(n). Space O(log n) call stack.

> [!tip] Alternatives
> Kadane's algorithm — O(n) time, O(1) space; preferred in practice. D&C version is the textbook CLRS approach and demonstrates the crossing-subarray technique used in many harder problems.

---

## Expression D&C

### Different Ways to Add Parentheses

> [!example] Problem
> Given a string expression of numbers and operators, return all possible results from computing all the different possible ways to group numbers and operators. You may return the answer in any order.
> The test cases are generated such that the output values fit in a 32-bit integer and the number of different results does not exceed 104.
> 
> **Example 1:**
> ```
> Input: expression = "2-1-1"
> Output: [0,2]
> Explanation:
> ((2-1)-1) = 0 
> (2-(1-1)) = 2
> ```
> 
> **Example 2:**
> ```
> Input: expression = "2*3-4*5"
> Output: [-34,-14,-10,-10,10]
> Explanation:
> (2*(3-(4*5))) = -34 
> ((2*3)-(4*5)) = -14 
> ((2*(3-4))*5) = -10 
> (2*((3-4)*5)) = -10 
> (((2*3)-4)*5) = 10
> ```
> 
> **Constraints:**
> - 1 <= expression.length <= 20
> - expression consists of digits and the operator '+', '-', and '*'.
> - All the integer values in the input expression are in the range [0, 99].
> - The integer values in the input expression do not have a leading '-' or '+' denoting the sign.

> [!info] Approach
> Each operator can be the "last operation" (the root of an expression tree). Dividing on operator `i` creates independent left and right sub-expressions — classic D&C. The number of distinct expression trees is the Catalan number, exponential in the number of operators. For each operator in the string, split into left and right sub-expressions. Recurse each side to get all possible values. Combine every pair from left × right using the current operator. Base case: string is a number → return `[int(string)]`. Memoize on `(lo, hi)` or the sub-string to avoid recomputing overlapping sub-expressions.

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
>                 left = solve(s[:i])
>                 right = solve(s[i+1:])
>                 for l in left:
>                     for r in right:
>                         if ch == '+':
>                             results.append(l + r)
>                         elif ch == '-':
>                             results.append(l - r)
>                         else:
>                             results.append(l * r)
>         if not results:          # pure number, no operators
>             results.append(int(s))
>         memo[s] = results
>         return results
>
>     return solve(expression)
> ```

> [!success] Complexity
> Time O(n · Cₙ) where Cₙ is the nth Catalan number (exponential in operator count). Space O(Cₙ) for memoization and result lists.

> [!tip] Alternatives
> Without memoization: same asymptotic but with redundant recomputation. DP bottom-up on interval `[i, j]` — same values, avoids recursion stack. This problem is the same structure as Matrix Chain Multiplication.

---

### Kth Largest in a Stream (Running QuickSelect Concept)

> [!example] Problem
> Design a class that finds the kth largest element in a stream as new elements are added.

> [!info] Approach
> Maintaining a sorted structure is O(log n) per insertion. A min-heap of size k keeps the k largest elements seen so far; its root is always the kth largest. No QuickSelect needed — heap gives O(1) answer, O(log k) insert. Maintain a min-heap of exactly k elements. When a new element arrives: push it; if heap size exceeds k, pop the minimum. Root = kth largest. Initialize heap with first elements; prune to size k. Each `add`: `heappush` then `heappop` if len > k. Return `heap[0]`.

> [!note]- Python Solution
> ```python
> import heapq
> 
> class KthLargest:
>     def __init__(self, k, nums):
>         self.k = k
>         self.heap: list[int] = []
>         for n in nums:
>             self.add(n)
> 
>     def add(self, val):
>         heapq.heappush(self.heap, val)
>         if len(self.heap) > self.k:
>             heapq.heappop(self.heap)
>         return self.heap[0]
> ```

> [!success] Complexity
> Time O(log k) per `add`. Space O(k).

> [!tip] Alternatives
> QuickSelect on the full array each time — O(n) per query, acceptable for offline batch. Sorted list with `bisect` — O(n) insert due to shifting. Order-statistics tree — O(log n) insert + query but no built-in in Python.

---

## See Also

[[sorting]] | [[recursion]] | [[binary-search]] | [[heap]]
### Construct Quad Tree `💤 T3`

> [!example] Problem
> Given a n * n matrix grid of 0's and 1's only. We want to represent grid with a Quad-Tree.
> Return the root of the Quad-Tree representing grid.
> A Quad-Tree is a tree data structure in which each internal node has exactly four children. Besides, each node has two attributes:
> We can construct a Quad-Tree from a two-dimensional area using the following steps:
> If you want to know more about the Quad-Tree, you can refer to the wiki.
> Quad-Tree format:
> You don't need to read this section for solving the problem. This is only if you want to understand the output format here. The output represents the serialized format of a Quad-Tree using level order traversal, where null signifies a path terminator where no node exists below.
> It is very similar to the serialization of the binary tree. The only difference is that the node is represented as a list [isLeaf, val].
> If the value of isLeaf or val is True we represent it as 1 in the list [isLeaf, val] and if the value of isLeaf or val is False we represent it as 0.
> 
> **Example 1:**
> ```
> class Node {
>     public boolean val;
>     public boolean isLeaf;
>     public Node topLeft;
>     public Node topRight;
>     public Node bottomLeft;
>     public Node bottomRight;
> }
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[0,1],[1,0]]
> Output: [[0,1],[1,0],[1,1],[1,1],[1,0]]
> Explanation: The explanation of this example is shown below:
> Notice that 0 represents False and 1 represents True in the photo representing the Quad-Tree.
> ```
> 
> **Example 3:**
> ```
> Input: grid = [[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0]]
> Output: [[0,1],[1,1],[0,1],[1,1],[1,0],null,null,null,null,[1,0],[1,0],[1,1],[1,1]]
> Explanation: All values in the grid are not the same. We divide the grid into four sub-grids.
> The topLeft, bottomLeft and bottomRight each has the same value.
> The topRight have different values so we divide it into 4 sub-grids where each has the same value.
> Explanation is shown in the photo below:
> ```
> 
> **Constraints:**
> - n == grid.length == grid[i].length
> - n == 2x where 0 <= x <= 6

> [!info] Approach
> If a region is uniform, the tree can stop early; otherwise divide the region into four equal quadrants and recurse. Recursively inspect subgrids. A uniform subgrid becomes a leaf node; a mixed one becomes an internal node with four children. For each region, check whether all values are the same. If yes, return a leaf. If no, split by midpoint and build children in the order top-left, top-right, bottom-left, bottom-right.

> [!note]- Python Solution
> ```python
> class Node:
>     def __init__(self, val, isLeaf, topLeft=None, topRight=None, bottomLeft=None, bottomRight=None):
>         self.val = val
>         self.isLeaf = isLeaf
>         self.topLeft = topLeft
>         self.topRight = topRight
>         self.bottomLeft = bottomLeft
>         self.bottomRight = bottomRight
> 
> def construct(grid):
>     def build(r1, c1, size):
>         first = grid[r1][c1]
>         same = True
>         for r in range(r1, r1 + size):
>             for c in range(c1, c1 + size):
>                 if grid[r][c] != first:
>                     same = False
>                     break
>             if not same:
>                 break
>         if same:
>             return Node(bool(first), True)
>         half = size // 2
>         return Node(
>             True,
>             False,
>             build(r1, c1, half),
>             build(r1, c1 + half, half),
>             build(r1 + half, c1, half),
>             build(r1 + half, c1 + half, half),
>         )
> 
>     return build(0, 0, len(grid))
> ```

> [!success] Complexity
> O(n^2 log n) in the straightforward uniformity check; O(n^2) with prefix sums or early pruning.

> [!tip] Alternatives
> Prefix sums can answer “all zeros/all ones?” in O(1) per region and avoid repeated scans.

---

## Divide and Conquer — More Problems

### Different Ways to Add Parentheses (LC 241)

> [!example] Problem
> Given a string expression of numbers and operators, return all possible results from computing all the different possible ways to group numbers and operators. You may return the answer in any order.
> The test cases are generated such that the output values fit in a 32-bit integer and the number of different results does not exceed 104.
> 
> **Example 1:**
> ```
> Input: expression = "2-1-1"
> Output: [0,2]
> Explanation:
> ((2-1)-1) = 0 
> (2-(1-1)) = 2
> ```
> 
> **Example 2:**
> ```
> Input: expression = "2*3-4*5"
> Output: [-34,-14,-10,-10,10]
> Explanation:
> (2*(3-(4*5))) = -34 
> ((2*3)-(4*5)) = -14 
> ((2*(3-4))*5) = -10 
> (2*((3-4)*5)) = -10 
> (((2*3)-4)*5) = 10
> ```
> 
> **Constraints:**
> - 1 <= expression.length <= 20
> - expression consists of digits and the operator '+', '-', and '*'.
> - All the integer values in the input expression are in the range [0, 99].
> - The integer values in the input expression do not have a leading '-' or '+' denoting the sign.

> [!info] Approach
> Each operator can be the “last operation applied” — split the expression at that operator, recursively compute all values for the left and right sub-expressions, and combine them. This is divide and conquer where each operator is the split point. For each operator in the expression, recurse on the left and right substrings. Collect all results by combining every pair from left and right with the operator. Base case: no operator found → the string is a single number. Memoize with a dict keyed on the expression string to avoid recomputing the same subexpression.

> [!note]- Python Solution
> ```python
> def diff_ways_to_compute(expression):
>     memo = {}
>
>     def solve(expr):
>         if expr in memo:
>             return memo[expr]
>         results = []
>         for i, ch in enumerate(expr):
>             if ch in '+-*':
>                 left = solve(expr[:i])
>                 right = solve(expr[i+1:])
>                 for l in left:
>                     for r in right:
>                         if ch == '+':
>                             results.append(l + r)
>                         elif ch == '-':
>                             results.append(l - r)
>                         else:
>                             results.append(l * r)
>         if not results:
>             results.append(int(expr))
>         memo[expr] = results
>         return results
>
>     return solve(expression)
> ```

> [!success] Complexity
> Time O(C(n) * n) where C(n) is the Catalan number — roughly O(4^n / n^1.5). Space O(same) for memoization.

> [!tip] Alternatives
> - Bottom-up DP with interval DP: `dp[i][j]` = list of values for substring `i..j`. Fill by increasing interval length. Equivalent asymptotically.
> - Key insight: this is exactly matrix chain multiplication shape — every operator is a potential last operation.

---

