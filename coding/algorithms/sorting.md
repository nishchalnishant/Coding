---
tags: [coding, algorithms, sorting]
topic: Sorting
difficulty: mixed
---

# Sorting — Problem Compendium

> [!info] Approach
> Identify what property sorting exposes (adjacency, rank, monotone structure), then apply the right sort variant. Non-comparison sorts (counting/radix/bucket) bypass O(n log n) when keys are bounded integers. QuickSelect gets rank-k in O(n) avg. Merge sort naturally counts cross-half inversions.

---

## Merge Sort Variants

### Merge Intervals

> [!example] Problem
> Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.
> 
> **Example 1:**
> ```
> Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
> Output: [[1,6],[8,10],[15,18]]
> Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
> ```
> 
> **Example 2:**
> ```
> Input: intervals = [[1,4],[4,5]]
> Output: [[1,5]]
> Explanation: Intervals [1,4] and [4,5] are considered overlapping.
> ```
> 
> **Constraints:**
> - 1 <= intervals.length <= 10^4
> - intervals[i].length == 2
> - 0 <= starti <= endi <= 10^4

> [!info] Approach
> Overlapping intervals can't be detected in arbitrary order. Sorting by start makes all potential overlaps adjacent — reduces O(n²) pair checks to one linear scan. Sort by start; greedily extend the last merged interval if `current.start ≤ last.end`. For each interval after sort, either extend `merged[-1][1] = max(merged[-1][1], end)` or append a new interval.


> [!note]- Python Solution
> ```python
> def merge(intervals):
>     intervals.sort(key=lambda x: x[0])
>     merged = []
>     for start, end in intervals:
>         if merged and start <= merged[-1][1]:
>             merged[-1][1] = max(merged[-1][1], end)
>         else:
>             merged.append([start, end])
>     return merged
> ```

> [!success] Complexity
> O(n log n) time, O(n) space (output).

> [!tip] Alternatives
> Sweep line with +1/-1 events at start/end — O(n log n), harder to reconstruct intervals. Segment tree for dynamic insertions.

---

### Sort List

> [!example] Problem
> Given the head of a linked list, return the list after sorting it in ascending order.
> 
> **Example 1:**
> ```
> Input: head = [4,2,1,3]
> Output: [1,2,3,4]
> ```
> 
> **Example 2:**
> ```
> Input: head = [-1,5,3,4,0]
> Output: [-1,0,3,4,5]
> ```
> 
> **Example 3:**
> ```
> Input: head = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [0, 5 * 10^4].
> - -10^5 <= Node.val <= 10^5

> [!info] Approach
> Array sorts require O(1) random access; linked lists have O(1) split/merge — merge sort is a natural fit. Top-down recursion uses O(log n) stack; bottom-up avoids even that. Find midpoint via slow/fast pointers; recursively sort halves; merge in O(n). `get_mid` severs the list at the middle. Merge uses dummy head and two pointers.


> [!note]- Python Solution
> ```python
> from typing import Optional
> 
> class ListNode:
>     def __init__(self, val=0, next=None):
>         self.val = val; self.next = next
> 
> def sort_list(head):
>     if not head or not head.next:
>         return head
> 
>     def get_mid(node):
>         slow, fast = node, node.next
>         while fast and fast.next:
>             slow = slow.next; fast = fast.next.next
>         mid = slow.next
>         slow.next = None  # sever
>         return mid
> 
>     def merge(l1, l2):
>         dummy = ListNode()
>         cur = dummy
>         while l1 and l2:
>             if l1.val <= l2.val:
>                 cur.next, l1 = l1, l1.next
>             else:
>                 cur.next, l2 = l2, l2.next
>             cur = cur.next
>         cur.next = l1 or l2
>         return dummy.next
> 
>     mid = get_mid(head)
>     left = sortList(head)
>     right = sortList(mid)
>     return merge(left, right)
> ```

> [!success] Complexity
> O(n log n) time, O(log n) stack; bottom-up variant achieves O(1) space.

> [!tip] Alternatives
> Convert to array → sort → rebuild: O(n) extra space. In-place heapsort on linked list: complex pointer arithmetic, not recommended.

---

### Count of Smaller Numbers After Self

> [!example] Problem
> Given an integer array nums, return an integer array counts where counts[i] is the number of smaller elements to the right of nums[i].
> 
> **Example 1:**
> ```
> Input: nums = [5,2,6,1]
> Output: [2,1,1,0]
> Explanation:
> To the right of 5 there are 2 smaller elements (2 and 1).
> To the right of 2 there is only 1 smaller element (1).
> To the right of 6 there is 1 smaller element (1).
> To the right of 1 there is 0 smaller element.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [-1]
> Output: [0]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [-1,-1]
> Output: [0,0]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> Brute force O(n²). During merge sort, every time a right-half element is placed before remaining left-half elements, those left elements each have a right-smaller count increment of exactly 1. The merge step naturally counts cross-half inversions. Tag each element with its original index. In the merge step, when right-half element at position `r` is selected, all remaining left-half elements get `+r` to their count. Sort `(original_index, value)` pairs; accumulate into `result[original_index]` during merge.


> [!note]- Python Solution
> ```python
> def count_smaller(nums):
>     n = len(nums)
>     result = [0] * n
>     indexed = list(enumerate(nums))  # (orig_idx, value)
> 
>     def merge_sort(arr, int]]):
>         if len(arr) <= 1:
>             return arr
>         mid = len(arr) // 2
>         left = merge_sort(arr[:mid])
>         right = merge_sort(arr[mid:])
>         merged = []
>         l = r = 0
>         while l < len(left) and r < len(right):
>             if left[l][1] <= right[r][1]:
>                 # right[r] is NOT smaller; r elements already placed from right = smaller count
>                 result[left[l][0]] += r
>                 merged.append(left[l]); l += 1
>             else:
>                 merged.append(right[r]); r += 1
>         while l < len(left):
>             result[left[l][0]] += r  # all r right elements are smaller
>             merged.append(left[l]); l += 1
>         merged.extend(right[r:])
>         return merged
> 
>     merge_sort(indexed)
>     return result
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> Fenwick Tree (BIT) on coordinate-compressed values — O(n log n), simpler to implement. Segment tree. Both require coordinate compression.

---

### Count of Range Sum

> [!example] Problem
> Given an integer array nums and two integers lower and upper, return the number of range sums that lie in [lower, upper] inclusive.
> Range sum S(i, j) is defined as the sum of the elements in nums between indices i and j inclusive, where i <= j.
> 
> **Example 1:**
> ```
> Input: nums = [-2,5,-1], lower = -2, upper = 2
> Output: 3
> Explanation: The three ranges are: [0,0], [2,2], and [0,2] and their respective sums are: -2, -1, 2.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0], lower = 0, upper = 0
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -2^{31} <= nums[i] <= 2^{31} - 1
> - -10^5 <= lower <= upper <= 10^5
> - The answer is guaranteed to fit in a 32-bit integer.

> [!info] Approach
> `sum(nums[i..j]) = prefix[j+1] - prefix[i]`. Need to count pairs in prefix array. Merge sort on prefix array lets us count valid pairs across halves in O(n) per level using two monotone pointers. Build prefix sum array (size n+1). Merge sort it counting valid (right - left) pairs. For each right-half prefix `r`, maintain two pointers `lo, hi` on sorted left half: `lo` = first index where `r - left[lo] ≤ upper`, `hi` = first where `r - left[hi] < lower`. Count = `hi - lo`.


> [!note]- Python Solution
> ```python
> def count_range_sum(nums, lower, upper):
>     from itertools import accumulate
>     prefix = [0] + list(accumulate(nums))
>     count = 0
> 
>     def merge_sort(arr):
>         nonlocal count
>         if len(arr) <= 1:
>             return arr
>         mid = len(arr) // 2
>         left = merge_sort(arr[:mid])
>         right = merge_sort(arr[mid:])
>         lo = hi = 0
>         for r in right:
>             while lo < len(left) and r - left[lo] > upper:
>                 lo += 1
>             while hi < len(left) and r - left[hi] >= lower:
>                 hi += 1
>             count += hi - lo
>         # standard merge
>         merged, i, j = [], 0, 0
>         while i < len(left) and j < len(right):
>             if left[i] <= right[j]:
>                 merged.append(left[i]); i += 1
>             else:
>                 merged.append(right[j]); j += 1
>         merged.extend(left[i:]); merged.extend(right[j:])
>         return merged
> 
>     merge_sort(prefix)
>     return count
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> Fenwick Tree with coordinate compression on prefix sums — O(n log n). Segment tree.

---

### Reverse Pairs

> [!example] Problem
> Given an integer array nums, return the number of reverse pairs in the array.
> A reverse pair is a pair (i, j) where
> 
> **Example 1:**
> ```
> Input: nums = [1,3,2,3,1]
> Output: 2
> Explanation: The reverse pairs are:
> (1, 4) --> nums[1] = 3, nums[4] = 1, 3 > 2 * 1
> (3, 4) --> nums[3] = 3, nums[4] = 1, 3 > 2 * 1
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,4,3,5,1]
> Output: 3
> Explanation: The reverse pairs are:
> (1, 4) --> nums[1] = 4, nums[4] = 1, 4 > 2 * 1
> (2, 4) --> nums[2] = 3, nums[4] = 1, 3 > 2 * 1
> (3, 4) --> nums[3] = 5, nums[4] = 1, 5 > 2 * 1
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 5 * 10^4
> - -2^{31} <= nums[i] <= 2^{31} - 1

> [!info] Approach
> Same merge-sort inversion insight. During merge, left is sorted ascending. For a fixed right element `r`, all left elements `l` with `l > 2*r` form a contiguous suffix (since left is sorted). Advance pointer j monotonically per right element → O(n) counting pass per merge level. Separate counting pass before standard merge; two-pointer on sorted left for each right element. Inner loop: for each `left[i]`, advance `j` while `left[i] > 2 * right[j]`. Count += j per left element.


> [!note]- Python Solution
> ```python
> def reverse_pairs(nums):
>     count = 0
> 
>     def merge_sort(arr):
>         nonlocal count
>         if len(arr) <= 1:
>             return arr
>         mid = len(arr) // 2
>         left = merge_sort(arr[:mid])
>         right = merge_sort(arr[mid:])
>         # counting pass
>         j = 0
>         for i in range(len(left)):
>             while j < len(right) and left[i] > 2 * right[j]:
>                 j += 1
>             count += j
>         # standard merge
>         merged, l, r = [], 0, 0
>         while l < len(left) and r < len(right):
>             if left[l] <= right[r]:
>                 merged.append(left[l]); l += 1
>             else:
>                 merged.append(right[r]); r += 1
>         merged.extend(left[l:]); merged.extend(right[r:])
>         return merged
> 
>     merge_sort(nums)
>     return count
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> Fenwick Tree with 2× coordinate compression (map all values and 2× values together).

---

### Count Inversions (Merge Sort)

> [!example] Problem
> Given array, count pairs (i,j) where i < j but arr[i] > arr[j].

> [!info] Approach
> Brute force O(n²). Merge sort naturally counts inversions — when a right half element is placed before left half elements, each remaining left half element contributes one inversion. Modified merge sort. During merge, when right[j] < left[i], add (mid - left_ptr) to count. Recursive merge sort returning (sorted_array, inversion_count). Standard merge with count accumulation.


> [!note]- Python Solution
> ```python
> def count_inversions(arr):
>     def merge_sort(a):
>         if len(a) <= 1:
>             return a, 0
>         mid = len(a) // 2
>         left, lc = merge_sort(a[:mid])
>         right, rc = merge_sort(a[mid:])
>         merged = []
>         count = lc + rc
>         i = j = 0
>         while i < len(left) and j < len(right):
>             if left[i] <= right[j]:
>                 merged.append(left[i]); i += 1
>             else:
>                 # all remaining left elements > right[j]
>                 count += len(left) - i
>                 merged.append(right[j]); j += 1
>         merged.extend(left[i:]); merged.extend(right[j:])
>         return merged, count
> 
>     _, total = merge_sort(arr)
>     return total
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> Fenwick Tree (BIT) on coordinate-compressed values — O(n log n), different approach: process elements left to right, query prefix sum for elements already seen that are larger.

---

## QuickSort / QuickSelect

### Kth Largest Element in an Array

> [!example] Problem
> Given an integer array nums and an integer k, return the kth largest element in the array.
> Note that it is the kth largest element in the sorted order, not the kth distinct element.
> Can you solve it without sorting?
> 
> **Example 1:**
> ```
> Input: nums = [3,2,1,5,6,4], k = 2
> Output: 5
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
> Output: 4
> ```
> 
> **Constraints:**
> - 1 <= k <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> Full sort O(n log n) computes all ranks; we need only one. QuickSelect partitions around a pivot and recurses into exactly one half — average O(n) total work. Randomized partition into [≥pivot | pivot | <pivot]. After partitioning, pivot is at its final rank. Recurse left or right based on pivot rank vs target. Target rank = k-1 (0-indexed from largest). Stop when pivot index == target.


> [!note]- Python Solution
> ```python
> import random
> 
> def find_kth_largest(nums, k):
>     def partition(lo, hi):
>         pivot_idx = random.randint(lo, hi)
>         nums[pivot_idx], nums[hi] = nums[hi], nums[pivot_idx]
>         pivot = nums[hi]
>         store = lo
>         for i in range(lo, hi):
>             if nums[i] >= pivot:  # largest-first ordering
>                 nums[store], nums[i] = nums[i], nums[store]
>                 store += 1
>         nums[store], nums[hi] = nums[hi], nums[store]
>         return store
> 
>     lo, hi, target = 0, len(nums) - 1, k - 1
>     while lo <= hi:
>         p = partition(lo, hi)
>         if p == target:
>             return nums[p]
>         elif p < target:
>             lo = p + 1
>         else:
>             hi = p - 1
>     return -1
> ```

> [!success] Complexity
> O(n) average, O(n²) worst (mitigated by randomization); O(1) extra space.

> [!tip] Alternatives
> Min-heap of size k: O(n log k), always O(n log k) — better when k ≪ n. Full sort O(n log n). Introselect for guaranteed O(n) worst case.

---

### K Closest Points to Origin

> [!example] Problem
> Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).
> The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).
> You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).
> 
> **Example 1:**
> ```
> Input: points = [[1,3],[-2,2]], k = 1
> Output: [[-2,2]]
> Explanation:
> The distance between (1, 3) and the origin is sqrt(10).
> The distance between (-2, 2) and the origin is sqrt(8).
> Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
> We only want the closest k = 1 points from the origin, so the answer is just [[-2,2]].
> ```
> 
> **Example 2:**
> ```
> Input: points = [[3,3],[5,-1],[-2,4]], k = 2
> Output: [[3,3],[-2,4]]
> Explanation: The answer [[-2,4],[3,3]] would also be accepted.
> ```
> 
> **Constraints:**
> - 1 <= k <= points.length <= 10^4
> - -10^4 <= xi, yi <= 10^4

> [!info] Approach
> Need top-k by distance. QuickSelect finds the exact boundary at rank k in O(n) average without sorting all n points. Squared distance avoids sqrt and preserves order. QuickSelect partitioning by dist²; once pivot lands at index k, indices 0..k-1 are the k closest. Partition by dist² ascending; recurse until pivot == k.


> [!note]- Python Solution
> ```python
> def k_closest(points, k):
>     def dist(p):
>         return p[0] * p[0] + p[1] * p[1]
> 
>     def partition(lo, hi):
>         pivot_d = dist(points[hi])
>         store = lo
>         for i in range(lo, hi):
>             if dist(points[i]) <= pivot_d:
>                 points[store], points[i] = points[i], points[store]
>                 store += 1
>         points[store], points[hi] = points[hi], points[store]
>         return store
> 
>     lo, hi = 0, len(points) - 1
>     while lo <= hi:
>         p = partition(lo, hi)
>         if p == k:
>             break
>         elif p < k:
>             lo = p + 1
>         else:
>             hi = p - 1
>     return points[:k]
> ```

> [!success] Complexity
> O(n) average, O(n²) worst; O(1) extra space.

> [!tip] Alternatives
> Max-heap of size k: O(n log k), simpler to implement. Full sort O(n log n).

---

### Top K Frequent Elements

> [!example] Problem
> Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,1,2,2,3], k = 2
> Output: [1,2]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1], k = 1
> Output: [1]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4
> - k is in the range [1, the number of unique elements in the array].
> - It is guaranteed that the answer is unique.

> [!info] Approach
> Count frequencies O(n), then need top-k by frequency. Frequencies are bounded by n — bucket sort on frequency is O(n) total, beating any comparison-based approach. Count with hashmap; bucket[freq].append(num) where index = frequency; scan from high to low collecting k elements. len(nums)+1 buckets (freq ranges 1..n); linear scan backward.


> [!note]- Python Solution
> ```python
> def top_k_frequent(nums, k):
>     from collections import Counter
>     freq = Counter(nums)
>     buckets = [[] for _ in range(len(nums) + 1)]
>     for num, f in freq.items():
>         buckets[f].append(num)
>     result = []
>     for f in range(len(buckets) - 1, 0, -1):
>         for num in buckets[f]:
>             result.append(num)
>             if len(result) == k:
>                 return result
>     return result
> ```

> [!success] Complexity
> O(n) time and space.

> [!tip] Alternatives
> Min-heap of size k: O(n log k). QuickSelect on (num, freq) pairs: O(n) average. Sort by frequency: O(n log n).

---

## Counting / Radix Sort

### Sort Colors

> [!example] Problem
> Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.
> We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.
> You must solve this problem without using the library's sort function.
> 
> **Example 1:**
> ```
> Input: nums = [2,0,2,1,1,0]
> Output: [0,0,1,1,2,2]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,0,1]
> Output: [0,1,2]
> ```
> 
> **Constraints:**
> - n == nums.length
> - 1 <= n <= 300
> - nums[i] is either 0, 1, or 2.

> [!info] Approach
> Only 3 distinct values — counting sort requires two passes. DNF achieves one pass, O(n), O(1) space by maintaining three invariant regions simultaneously. Three pointers `lo, mid, hi` partitioning array into [0s | 1s | unexplored | 2s]. Advance mid, swapping 0s left and 2s right. nums[mid]==0: swap(lo,mid), lo++, mid++. nums[mid]==1: mid++. nums[mid]==2: swap(mid,hi), hi-- (don't advance mid — swapped value is unexplored).


> [!note]- Python Solution
> ```python
> def sort_colors(nums):
>     lo, mid, hi = 0, 0, len(nums) - 1
>     while mid <= hi:
>         if nums[mid] == 0:
>             nums[lo], nums[mid] = nums[mid], nums[lo]
>             lo += 1; mid += 1
>         elif nums[mid] == 1:
>             mid += 1
>         else:
>             nums[mid], nums[hi] = nums[hi], nums[mid]
>             hi -= 1
> ```

> [!success] Complexity
> O(n) time, O(1) space, single pass.

> [!tip] Alternatives
> Counting sort: two passes, O(1) space. Generalized to k colors: QuickSort 3-way partition.

---

### Maximum Gap (Bucket Sort)

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
> Comparison sort O(n log n) is too slow. Key insight (Pigeonhole): n elements span [min, max]; the n-1 gaps average `(max-min)/(n-1)`. The maximum gap must be ≥ this average, meaning it must straddle at least one bucket boundary. So intra-bucket gaps are irrelevant — only inter-bucket gaps matter. Create n-1 buckets of width `ceil((max-min)/(n-1))`. Track only min/max per bucket. Max gap = max over consecutive non-empty bucket pairs of `next_bucket.min - prev_bucket.max`. bucket_idx = `(num - min_v) // bucket_width`; scan pairs of consecutive non-empty buckets.


> [!note]- Python Solution
> ```python
> def maximum_gap(nums):
>     if len(nums) < 2:
>         return 0
>     min_v, max_v = min(nums), max(nums)
>     if min_v == max_v:
>         return 0
>     n = len(nums)
>     bucket_width = max(1, (max_v - min_v) // (n - 1))
>     num_buckets = (max_v - min_v) // bucket_width + 1
>     # Each bucket stores [min, max] or None
>     buckets = [None] * num_buckets
>     for num in nums:
>         idx = (num - min_v) // bucket_width
>         if buckets[idx] is None:
>             buckets[idx] = [num, num]
>         else:
>             buckets[idx][0] = min(buckets[idx][0], num)
>             buckets[idx][1] = max(buckets[idx][1], num)
>     max_gap = 0
>     prev_max = min_v
>     for bucket in buckets:
>         if bucket is None:
>             continue
>         max_gap = max(max_gap, bucket[0] - prev_max)
>         prev_max = bucket[1]
>     return max_gap
> ```

> [!success] Complexity
> O(n) time and space.

> [!tip] Alternatives
> Radix sort — O(n·d) where d = digits; same asymptotic. Both bypass O(n log n) lower bound.

---

## Bucket Sort

### Sort Characters by Frequency

> [!example] Problem
> Given a string s, sort it in decreasing order based on the frequency of the characters. The frequency of a character is the number of times it appears in the string.
> Return the sorted string. If there are multiple answers, return any of them.
> 
> **Example 1:**
> ```
> Input: s = "tree"
> Output: "eert"
> Explanation: 'e' appears twice while 'r' and 't' both appear once.
> So 'e' must appear before both 'r' and 't'. Therefore "eetr" is also a valid answer.
> ```
> 
> **Example 2:**
> ```
> Input: s = "cccaaa"
> Output: "aaaccc"
> Explanation: Both 'c' and 'a' appear three times, so both "cccaaa" and "aaaccc" are valid answers.
> Note that "cacaca" is incorrect, as the same characters must be together.
> ```
> 
> **Example 3:**
> ```
> Input: s = "Aabb"
> Output: "bbAa"
> Explanation: "bbaA" is also a valid answer, but "Aabb" is incorrect.
> Note that 'A' and 'a' are treated as two different characters.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 5 * 10^5
> - s consists of uppercase and lowercase English letters and digits.

> [!info] Approach
> Comparison sort O(n log n). Frequencies are bounded by n — bucket sort achieves O(n). Count frequencies; bucket[freq].append(char); build result concatenating `char * freq` from high freq down. At most n distinct frequencies; linear scan of buckets from top.


> [!note]- Python Solution
> ```python
> def frequency_sort(s):
>     from collections import Counter
>     freq = Counter(s)
>     buckets = [[] for _ in range(len(s) + 1)]
>     for char, f in freq.items():
>         buckets[f].append(char)
>     result = []
>     for f in range(len(buckets) - 1, 0, -1):
>         for char in buckets[f]:
>             result.append(char * f)
>     return "".join(result)
> ```

> [!success] Complexity
> O(n) time and space.

> [!tip] Alternatives
> Sort by frequency descending: O(n log n). Max-heap over (freq, char): O(n log k) where k = unique chars.

---

## Custom Comparators

### Pancake Sorting

> [!example] Problem
> Given an array of integers arr, sort the array by performing a series of pancake flips.
> In one pancake flip we do the following steps:
> For example, if arr = [3,2,1,4] and we performed a pancake flip choosing k = 3, we reverse the sub-array [3,2,1], so arr = [1,2,3,4] after the pancake flip at k = 3.
> Return an array of the k-values corresponding to a sequence of pancake flips that sort arr. Any valid answer that sorts the array within 10 * arr.length flips will be judged as correct.
> 
> **Example 1:**
> ```
> Input: arr = [3,2,4,1]
> Output: [4,2,4,3]
> Explanation: 
> We perform 4 pancake flips, with k values 4, 2, 4, and 3.
> Starting state: arr = [3, 2, 4, 1]
> After 1st flip (k = 4): arr = [1, 4, 2, 3]
> After 2nd flip (k = 2): arr = [4, 1, 2, 3]
> After 3rd flip (k = 4): arr = [3, 2, 1, 4]
> After 4th flip (k = 3): arr = [1, 2, 3, 4], which is sorted.
> ```
> 
> **Example 2:**
> ```
> Input: arr = [1,2,3]
> Output: []
> Explanation: The input is already sorted, so there is no need to flip anything.
> Note that other answers, such as [3, 3], would also be accepted.
> ```
> 
> **Constraints:**
> - 1 <= arr.length <= 100
> - 1 <= arr[i] <= arr.length
> - All integers in arr are unique (i.e. arr is a permutation of the integers from 1 to arr.length).

> [!info] Approach
> Standard swaps aren't available; only prefix reversals. Think selection sort analog: place the largest unsorted element at the correct position using at most 2 flips — bring it to front (flip 1), then flip to final position (flip 2). For each size from n down to 2: find max in arr[0..size-1], flip it to front if not there, then flip to position size-1. At most 2(n-1) flips total.


> [!note]- Python Solution
> ```python
> def pancake_sort(arr):
>     result = []
>     n = len(arr)
>     for size in range(n, 1, -1):
>         max_idx = arr.index(max(arr[:size]))
>         if max_idx == size - 1:
>             continue
>         if max_idx != 0:
>             result.append(max_idx + 1)
>             arr[:max_idx + 1] = arr[:max_idx + 1][::-1]
>         result.append(size)
>         arr[:size] = arr[:size][::-1]
>     return result
> ```

> [!success] Complexity
> O(n²) time, O(n) space for result.

> [!tip] Alternatives
> No asymptotically better algorithm known for pancake sort. Gate Sorting uses 2n-3 flips (optimal).

---

### Queue Reconstruction by Height

> [!example] Problem
> You are given an array of people, people, which are the attributes of some people in a queue (not necessarily in order). Each people[i] = [hi, ki] represents the ith person of height hi with exactly ki other people in front who have a height greater than or equal to hi.
> Reconstruct and return the queue that is represented by the input array people. The returned queue should be formatted as an array queue, where queue[j] = [hj, kj] is the attributes of the jth person in the queue (queue[0] is the person at the front of the queue).
> 
> **Example 1:**
> ```
> Input: people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
> Output: [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
> Explanation:
> Person 0 has height 5 with no other people taller or the same height in front.
> Person 1 has height 7 with no other people taller or the same height in front.
> Person 2 has height 5 with two persons taller or the same height in front, which is person 0 and 1.
> Person 3 has height 6 with one person taller or the same height in front, which is person 1.
> Person 4 has height 4 with four people taller or the same height in front, which are people 0, 1, 2, and 3.
> Person 5 has height 7 with one person taller or the same height in front, which is person 1.
> Hence [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]] is the reconstructed queue.
> ```
> 
> **Example 2:**
> ```
> Input: people = [[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]
> Output: [[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]
> ```
> 
> **Constraints:**
> - 1 <= people.length <= 2000
> - 0 <= hi <= 10^6
> - 0 <= ki < people.length
> - It is guaranteed that the queue can be reconstructed.

> [!info] Approach
> Taller people are unaffected by shorter people's positions. If we insert tallest first, each person's k-value is exact at insertion time (all people in the result list so far are ≥ their height). Sort descending by height (ties: ascending by k). Insert each person at index `person[1]`. Python list.insert(k, person) shifts subsequent elements right — their k values remain valid since all have height ≤ current.


> [!note]- Python Solution
> ```python
> def reconstruct_queue(people):
>     people.sort(key=lambda x: (-x[0], x[1]))
>     result = []
>     for person in people:
>         result.insert(person[1], person)
>     return result
> ```

> [!success] Complexity
> O(n²) time (list insert is O(n)), O(n) space.

> [!tip] Alternatives
> Fenwick Tree (BIT) tracking empty slot positions — O(n log n). Binary search on sorted result list — O(n log n) with a BIT/order-statistic tree.

---

### Custom Sort String

> [!example] Problem
> You are given two strings order and s. All the characters of order are unique and were sorted in some custom order previously.
> Permute the characters of s so that they match the order that order was sorted. More specifically, if a character x occurs before a character y in order, then x should occur before y in the permuted string.
> Return any permutation of s that satisfies this property.
> 
> **Example 1:**
> ```
> Input: order = "cba", s = "abcd"
> Output: "cbad"
> Explanation: "a" , "b" , "c" appear in order, so the order of "a" , "b" , "c" should be "c" , "b" , and "a" .
> Since "d" does not appear in order , it can be at any position in the returned string. "dcba" , "cdba" , "cbda" are also valid outputs.
> ```
> 
> **Example 2:**
> ```
> Input: order = "bcafg", s = "abcd"
> Output: "bcad"
> Explanation: The characters "b" , "c" , and "a" from order dictate the order for the characters in s . The character "d" in s does not appear in order , so its position is flexible.
> Following the order of appearance in order , "b" , "c" , and "a" from s should be arranged as "b" , "c" , "a" . "d" can be placed at any position since it's not in order. The output "bcad" correctly follows this rule. Other arrangements like "dbca" or "bcda" would also be valid, as long as "b" , "c" , "a" maintain their order.
> ```
> 
> **Constraints:**
> - 1 <= order.length <= 26
> - 1 <= s.length <= 200
> - order and s consist of lowercase English letters.
> - All the characters of order are unique.

> [!info] Approach
> Standard sort knows nothing about the custom ordering. Assign integer ranks from `order`; sort `s` by those ranks. `rank = {c: i for i, c in enumerate(order)}`; sort `s` with `key=lambda c: rank.get(c, len(order))`. O(n log n) sort; unranked characters get a default rank beyond the end.


> [!note]- Python Solution
> ```python
> def custom_sort_string(order, s):
>     rank = {c: i for i, c in enumerate(order)}
>     return "".join(sorted(s, key=lambda c: rank.get(c, len(order))))
> ```

> [!success] Complexity
> O(n log n) time where n = len(s), O(1) extra space (rank dict ≤ 26 entries).

> [!tip] Alternatives
> Count-based O(n): count chars in s, place by order, append remainder — avoids sort entirely.

---

### Largest Number (custom comparator)

> [!example] Problem
> Given a list of non-negative integers nums, arrange them such that they form the largest number and return it.
> Since the result may be very large, so you need to return a string instead of an integer.
> 
> **Example 1:**
> ```
> Input: nums = [10,2]
> Output: "210"
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,30,34,5,9]
> Output: "9534330"
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 100
> - 0 <= nums[i] <= 10^9

> [!info] Approach
> Numeric sort fails (e.g., 9 vs 91: "991" > "919" so 9 should precede 91). The correct ordering is: a before b if str(a)+str(b) > str(b)+str(a). This comparison is transitive and defines a total order. Convert to strings; sort with `functools.cmp_to_key` using concatenation comparison. Edge case: all zeros → return "0".


> [!note]- Python Solution
> ```python
> from functools import cmp_to_key
> 
> def largest_number(nums):
>     strs = list(map(str, nums))
> 
>     def compare(a, b):
>         if a + b > b + a:
>             return -1
>         elif a + b < b + a:
>             return 1
>         return 0
> 
>     strs.sort(key=cmp_to_key(compare))
>     result = "".join(strs)
>     return "0" if result[0] == "0" else result
> ```

> [!success] Complexity
> O(n log n · L) where L = avg digit length; O(n) space.

> [!tip] Alternatives
> No standard numeric sort works. The concatenation comparator is the only correct approach.

---

### Russian Doll Envelopes (LC 354)

> [!example] Problem
> You are given a 2D array of integers envelopes where envelopes[i] = [wi, hi] represents the width and the height of an envelope.
> One envelope can fit into another if and only if both the width and height of one envelope are greater than the other envelope's width and height.
> Return the maximum number of envelopes you can Russian doll (i.e., put one inside the other).
> Note: You cannot rotate an envelope.
> 
> **Example 1:**
> ```
> Input: envelopes = [[5,4],[6,4],[6,7],[2,3]]
> Output: 3
> Explanation: The maximum number of envelopes you can Russian doll is 3 ([2,3] => [5,4] => [6,7]).
> ```
> 
> **Example 2:**
> ```
> Input: envelopes = [[1,1],[1,1],[1,1]]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= envelopes.length <= 10^5
> - envelopes[i].length == 2
> - 1 <= wi, hi <= 10^5

> [!info] Approach
> Sort by width ascending. For equal widths, sort height DESCENDING — this prevents using two same-width envelopes in the LIS. Then the problem reduces to LIS on heights. Sort + LIS with binary search (patience sorting). Sort envelopes by (w asc, h desc). Extract heights. Find LIS length using binary search on tails array.


> [!note]- Python Solution
> ```python
> import bisect
> 
> def max_envelopes(envelopes):
>     envelopes.sort(key=lambda x: (x[0], -x[1]))
>     heights = [e[1] for e in envelopes]
>     tails = []
>     for h in heights:
>         pos = bisect.bisect_left(tails, h)
>         if pos == len(tails):
>             tails.append(h)
>         else:
>             tails[pos] = h
>     return len(tails)
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> DP O(n²) LIS — TLE for large n. The descending-height trick for equal widths is the key insight; without it same-width envelopes would incorrectly extend the sequence.

---

### Wiggle Sort II (LC 324)

> [!example] Problem
> Given an integer array nums, reorder it such that nums[0]  nums[2] < nums[3]....
> You may assume the input array always has a valid answer.
> 
> **Example 1:**
> ```
> Input: nums = [1,5,1,1,6,4]
> Output: [1,6,1,5,1,4]
> Explanation: [1,4,1,5,1,6] is also accepted.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,3,2,2,3,1]
> Output: [2,3,1,3,1,2]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 5 * 10^4
> - 0 <= nums[i] <= 5000
> - It is guaranteed that there will be an answer for the given input nums.

> [!info] Approach
> Find median, then place larger-than-median elements at odd indices and smaller-than-median elements at even indices, both in reverse order to avoid equal adjacent elements. QuickSelect for median + index mapping. Find median (QuickSelect O(n)). Use 3-way partition (Dutch flag). Place using index map i → (1+2*i)%(n|1) to interleave.


> [!note]- Python Solution
> ```python
> def wiggle_sort(nums):
>     n = len(nums)
>     # index mapping: virtual index i -> actual index (1+2*i)%(n|1)
>     def idx(i):
>         return (1 + 2 * i) % (n | 1)
> 
>     # find median via nth_element (simplified: sort for clarity)
>     median = sorted(nums)[n // 2]
> 
>     # 3-way Dutch flag partition using mapped indices
>     lo, mid, hi = 0, 0, n - 1
>     while mid <= hi:
>         if nums[idx(mid)] > median:
>             nums[idx(lo)], nums[idx(mid)] = nums[idx(mid)], nums[idx(lo)]
>             lo += 1; mid += 1
>         elif nums[idx(mid)] < median:
>             nums[idx(mid)], nums[idx(hi)] = nums[idx(hi)], nums[idx(mid)]
>             hi -= 1
>         else:
>             mid += 1
> ```

> [!success] Complexity
> O(n) with QuickSelect for median + O(n) 3-way partition, O(1) extra space.

> [!tip] Alternatives
> Sort + interleave O(n log n) — simpler: sort, split into two halves, interleave in reverse to avoid equal adjacency. The O(n) approach requires QuickSelect and the index mapping trick.

---

## Interview Classics

### H-Index (LC 274)

> [!example] Problem
> Given an array of integers citations where citations[i] is the number of citations a researcher received for their ith paper, return the researcher's h-index.
> According to the definition of h-index on Wikipedia: The h-index is defined as the maximum value of h such that the given researcher has published at least h papers that have each been cited at least h times.
> 
> **Example 1:**
> ```
> Input: citations = [3,0,6,1,5]
> Output: 3
> Explanation: [3,0,6,1,5] means the researcher has 5 papers in total and each of them had received 3, 0, 6, 1, 5 citations respectively.
> Since the researcher has 3 papers with at least 3 citations each and the remaining two with no more than 3 citations each, their h-index is 3.
> ```
> 
> **Example 2:**
> ```
> Input: citations = [1,3,1]
> Output: 1
> ```
> 
> **Constraints:**
> - n == citations.length
> - 1 <= n <= 5000
> - 0 <= citations[i] <= 1000

> [!info] Approach
> After sorting descending, at position i (0-indexed), if citations[i] >= i+1 then at least i+1 papers have >= i+1 citations. Track the largest such i+1. Sort descending; scan linearly to find max h. For each i, if citations[i] >= i+1, update h = i+1. Return max h found.


> [!note]- Python Solution
> ```python
> def h_index(citations):
>     citations.sort(reverse=True)
>     h = 0
>     for i, c in enumerate(citations):
>         if c >= i + 1:
>             h = i + 1
>         else:
>             break
>     return h
> ```

> [!success] Complexity
> O(n log n) time, O(1) space.

> [!tip] Alternatives
> Counting sort O(n): bucket[min(c, n)] += 1; scan from n down accumulating count — stop when cumulative count >= bucket index. Binary search on sorted array O(n log n) same asymptotic.

---

### Meeting Rooms II (LC 253)

> [!example] Problem
> Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return *the minimum number of conference rooms required*.
> 
>  
> 
> Example 1:
> 
> ```
> **Input:** intervals = [[0,30],[5,10],[15,20]]
> **Output:** 2
> 
> ```
> 
> Example 2:
> 
> ```
> **Input:** intervals = [[7,10],[2,4]]
> **Output:** 1
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= intervals.length <= 10^4`
> 	
> - `0 <= start_i < end_i <= 10^6`

> [!info] Approach
> Sort by start time. Use a min-heap of end times. For each new meeting, if the earliest-ending room frees up before this meeting starts, reuse it (pop). Push this meeting's end time. Heap size = rooms needed. Sort by start + min-heap of end times. Sort intervals by start. For each interval: if heap and heap[0] <= start, heappop (reuse). heappush(end). Return heap size.


> [!note]- Python Solution
> ```python
> import heapq
> 
> def min_meeting_rooms(intervals):
>     if not intervals:
>         return 0
>     intervals.sort(key=lambda x: x[0])
>     heap = []  # end times
>     for start, end in intervals:
>         if heap and heap[0] <= start:
>             heapq.heapreplace(heap, end)
>         else:
>             heapq.heappush(heap, end)
>     return len(heap)
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> Sweep line with sorted start/end events O(n log n): create +1 events at starts and -1 at ends; scan sorted events tracking running room count and max. Same complexity, different mental model — useful when asked for chronological ordering of room assignments.

---

## Classic Merge Variants

### Merge Two Sorted Lists

> [!example] Problem
> You are given the heads of two sorted linked lists list1 and list2.
> Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.
> Return the head of the merged linked list.
> 
> **Example 1:**
> ```
> Input: list1 = [1,2,4], list2 = [1,3,4]
> Output: [1,1,2,3,4,4]
> ```
> 
> **Example 2:**
> ```
> Input: list1 = [], list2 = []
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: list1 = [], list2 = [0]
> Output: [0]
> ```
> 
> **Constraints:**
> - The number of nodes in both lists is in the range [0, 50].
> - -100 <= Node.val <= 100
> - Both list1 and list2 are sorted in non-decreasing order.

> [!info] Approach
> Both lists are sorted — no need to re-sort. Compare heads; greedily take the smaller head, advancing that pointer. One pass O(m+n). Dummy head + two pointers. Attach smaller node at each step; attach remainder when one list exhausts. Dummy head avoids null-checking the result head. After loop, `cur.next = l1 or l2`.


> [!note]- Python Solution
> ```python
> def merge_two_lists(
>     list1: Optional[ListNode], list2: Optional[ListNode]
> ) -> Optional[ListNode]:
>     dummy = ListNode()
>     cur = dummy
>     while list1 and list2:
>         if list1.val <= list2.val:
>             cur.next, list1 = list1, list1.next
>         else:
>             cur.next, list2 = list2, list2.next
>         cur = cur.next
>     cur.next = list1 or list2
>     return dummy.next
> ```

> [!success] Complexity
> O(m+n) time, O(1) space.

> [!tip] Alternatives
> Recursive — O(m+n) stack depth. Convert to arrays, merge, reconstruct — O(m+n) extra space.

---

### Merge K Sorted Lists

> [!example] Problem
> You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
> Merge all the linked-lists into one sorted linked-list and return it.
> 
> **Example 1:**
> ```
> Input: lists = [[1,4,5],[1,3,4],[2,6]]
> Output: [1,1,2,3,4,4,5,6]
> Explanation: The linked-lists are:
> [
>   1->4->5,
>   1->3->4,
>   2->6
> ]
> merging them into one sorted linked list:
> 1->1->2->3->4->4->5->6
> ```
> 
> **Example 2:**
> ```
> Input: lists = []
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: lists = [[]]
> Output: []
> ```
> 
> **Constraints:**
> - k == lists.length
> - 0 <= k <= 10^4
> - 0 <= lists[i].length <= 500
> - -10^4 <= lists[i][j] <= 10^4
> - lists[i] is sorted in ascending order.
> - The sum of lists[i].length will not exceed 10^4.

> [!info] Approach
> Sequential merge of k lists: O(nk). Min-heap always extracts the globally smallest current head in O(log k); total O(n log k) where n = total nodes. Push all list heads into min-heap. Repeatedly pop min node, append to result, push its successor. Heap entries are `(val, tie_break_id, node)` — tie-break prevents comparing ListNode objects on equal values.


> [!note]- Python Solution
> ```python
> import heapq
> 
> def merge_k_lists(lists):
>     heap = []
>     for i, node in enumerate(lists):
>         if node:
>             heapq.heappush(heap, (node.val, i, node))
>     dummy = ListNode()
>     cur = dummy
>     while heap:
>         val, i, node = heapq.heappop(heap)
>         cur.next = node; cur = cur.next
>         if node.next:
>             heapq.heappush(heap, (node.next.val, i, node.next))
>     return dummy.next
> ```

> [!success] Complexity
> O(n log k) time, O(k) heap space.

> [!tip] Alternatives
> Divide and conquer pairwise merge — O(n log k), same asymptotic. Sequential merge — O(nk).

---

### Median of Two Sorted Arrays

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
> Merging is O(m+n); need O(log). The median partitions the combined array at position `(m+n)//2`. Binary search on the partition point in the smaller array determines where to cut both arrays such that all left elements ≤ all right elements. Binary search on `i` (cut in A); j = `(m+n+1)//2 - i` (cut in B). Valid partition when `A[i-1] ≤ B[j]` and `B[j-1] ≤ A[i]`. Always binary search on the shorter array. Handle edge cases with ±inf.


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
>     return 0.0
> ```

> [!success] Complexity
> O(log(min(m,n))) time, O(1) space.

> [!tip] Alternatives
> Merge and index to middle: O(m+n). Binary search on value range: O((m+n) log V).

---

## Majority / Frequency

### Majority Element (Boyer-Moore)

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
> The majority element has count > n/2, so it outnumbers all others combined. Boyer-Moore voting: each non-majority element can "cancel" one majority element, but majority still survives. Maintain `(candidate, count)`. Increment count if current matches candidate; decrement otherwise; reset candidate when count hits 0. The surviving candidate after one pass is the majority. (If majority not guaranteed, do a second pass to verify.).


> [!note]- Python Solution
> ```python
> def majority_element(nums):
>     candidate, count = nums[0], 0
>     for num in nums:
>         if count == 0:
>             candidate = num
>         count += 1 if num == candidate else -1
>     return candidate
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Sort, return `nums[n//2]` — O(n log n). Hash map count — O(n) time and space. Randomized: pick random element, verify in O(n); expected O(1) iterations.

---

### Majority Element II

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
> At most 2 elements can satisfy `count > n/3` (since 3 × (⌊n/3⌋+1) > n). Extend Boyer-Moore to track 2 candidates simultaneously. Two `(candidate, count)` pairs. Each number either reinforces a candidate, claims a vacant slot (count=0), or decrements both when it matches neither. After the voting pass, verify both candidates have true count > n/3 (the vote may admit false positives for the second candidate).


> [!note]- Python Solution
> ```python
> def majority_element2(nums):
>     cand1, cand2, cnt1, cnt2 = 0, 1, 0, 0  # cand1 ≠ cand2 initially
>     for num in nums:
>         if num == cand1:
>             cnt1 += 1
>         elif num == cand2:
>             cnt2 += 1
>         elif cnt1 == 0:
>             cand1, cnt1 = num, 1
>         elif cnt2 == 0:
>             cand2, cnt2 = num, 1
>         else:
>             cnt1 -= 1; cnt2 -= 1
>     return [c for c in (cand1, cand2) if nums.count(c) > len(nums) // 3]
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Hash map count — O(n) space. Sort and scan runs — O(n log n). Generalize to ⌊n/k⌋: maintain k-1 candidates.

---

## Radix / Counting Sort

### Sort an Array (Counting Sort Variant)

> [!example] Problem
> Given an array of integers nums, sort the array in ascending order and return it.
> You must solve the problem without using any built-in functions in O(nlog(n)) time complexity and with the smallest space complexity possible.
> 
> **Example 1:**
> ```
> Input: nums = [5,2,3,1]
> Output: [1,2,3,5]
> Explanation: After sorting the array, the positions of some numbers are not changed (for example, 2 and 3), while the positions of other numbers are changed (for example, 1 and 5).
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5,1,1,2,0,0]
> Output: [0,0,1,1,2,5]
> Explanation: Note that the values of nums are not necessarily unique.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 5 * 10^4
> - -5 * 10^4 <= nums[i] <= 5 * 10^4

> [!info] Approach
> Comparison-based sorts bottom out at O(n log n); counting sort exploits a bounded integer domain to achieve O(n + k). Build a frequency array of size `max - min + 1`, accumulate prefix counts, then scatter elements into output in stable order. Shift values by `min` so indices stay non-negative. Reconstruct the sorted array by iterating the count array.


> [!note]- Python Solution
> ```python
> def sort_array(nums):
>     lo, hi = min(nums), max(nums)
>     count = [0] * (hi - lo + 1)
>     for x in nums:
>         count[x - lo] += 1
>     idx = 0
>     for v, c in enumerate(count):
>         for _ in range(c):
>             nums[idx] = v + lo
>             idx += 1
>     return nums
> ```

> [!success] Complexity
> Time O(n + k), Space O(k), where k = max − min + 1.

> [!tip] Alternatives
> Radix sort for large k; merge sort / heap sort for unbounded integers.

---

### Radix Sort Implementation

> [!example] Problem
> Sort a list of non-negative integers using radix sort — process digits from LSD (least significant) to MSD using a stable counting sort per digit pass.

> [!info] Approach
> Achieves O(d · (n + b)) where d = number of digits, b = base (10). Beats comparison sort when d is small. For each digit position (units, tens, hundreds, …), perform a stable counting sort keyed on that digit only. Extract digit with `(x // exp) % base`. Counting sort must be stable so relative order from previous passes is preserved.


> [!note]- Python Solution
> ```python
> def radix_sort(nums):
>     if not nums:
>         return nums
>     base = 10
>     exp = 1
>     max_val = max(nums)
>     while max_val // exp > 0:
>         count = [0] * base
>         for x in nums:
>             count[(x // exp) % base] += 1
>         for i in range(1, base):
>             count[i] += count[i - 1]
>         output = [0] * len(nums)
>         for x in reversed(nums):          # reversed for stability
>             d = (x // exp) % base
>             count[d] -= 1
>             output[count[d]] = x
>         nums = output
>         exp *= base
>     return nums
> ```

> [!success] Complexity
> Time O(d · n), Space O(n + b). d = ⌈log_b(max_val)⌉.

> [!tip] Alternatives
> For signed integers, sort by absolute value then handle negatives separately. For strings, same LSD approach on characters.

---

### Maximum Number After Digit Swaps (LC 2231)

> [!example] Problem
> You are given a positive integer num. You may swap any two digits of num that have the same parity (i.e. both odd digits or both even digits).
> Return the largest possible value of num after any number of swaps.
> 
> **Example 1:**
> ```
> Input: num = 1234
> Output: 3412
> Explanation: Swap the digit 3 with the digit 1, this results in the number 3214.
> Swap the digit 2 with the digit 4, this results in the number 3412.
> Note that there may be other sequences of swaps but it can be shown that 3412 is the largest possible number.
> Also note that we may not swap the digit 4 with the digit 1 since they are of different parities.
> ```
> 
> **Example 2:**
> ```
> Input: num = 65875
> Output: 87655
> Explanation: Swap the digit 8 with the digit 6, this results in the number 85675.
> Swap the first digit 5 with the digit 7, this results in the number 87655.
> Note that there may be other sequences of swaps but it can be shown that 87655 is the largest possible number.
> ```
> 
> **Constraints:**
> - 1 <= num <= 10^9

> [!info] Approach
> Digits at even positions can only be rearranged among themselves; same for odd positions. Maximize each group independently. Use counting sort (digit frequency array) to greedily fill even positions with the largest available even-position digits, then do the same for odd positions. Collect digits at even indices into a sorted (descending) pool, refill positions left-to-right from the pool; repeat for odd indices.


> [!note]- Python Solution
> ```python
> def maximum_swap(num):
>     digits = list(str(num))
>     for parity in (0, 1):
>         pool = sorted(
>             [digits[i] for i in range(parity, len(digits), 2)],
>             reverse=True
>         )
>         j = 0
>         for i in range(parity, len(digits), 2):
>             digits[i] = pool[j]; j += 1
>     return int("".join(digits))
> ```

> [!success] Complexity
> Time O(n log n) for the sort (n ≤ 9 digits → effectively O(1)), Space O(n).

> [!tip] Alternatives
> Counting sort bucket per parity group is O(n + 10) = O(n). Note: LC 2231 specifically restricts swaps to same-parity indices.

---

## Interval / Sweep Line

### Insert Interval (LC 57)

> [!example] Problem
> You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi] represent the start and the end of the ith interval and intervals is sorted in ascending order by starti. You are also given an interval newInterval = [start, end] that represents the start and end of another interval.
> Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).
> Return intervals after the insertion.
> Note that you don't need to modify intervals in-place. You can make a new array and return it.
> 
> **Example 1:**
> ```
> Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
> Output: [[1,5],[6,9]]
> ```
> 
> **Example 2:**
> ```
> Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
> Output: [[1,2],[3,10],[12,16]]
> Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].
> ```
> 
> **Constraints:**
> - 0 <= intervals.length <= 10^4
> - intervals[i].length == 2
> - 0 <= starti <= endi <= 10^5
> - intervals is sorted by starti in ascending order.
> - newInterval.length == 2
> - 0 <= start <= end <= 10^5

> [!info] Approach
> The list is already sorted — no re-sort needed. A single linear pass suffices to find overlap and merge. Three phases: (1) copy all intervals that end before the new interval starts, (2) merge all overlapping intervals into the new interval, (3) copy remaining intervals. Overlap condition: `existing.end >= new.start` AND `existing.start <= new.end`.


> [!note]- Python Solution
> ```python
> def insert(intervals, newInterval):
>     result = []
>     i, n = 0, len(intervals)
>     while i < n and intervals[i][1] < newInterval[0]:
>         result.append(intervals[i]); i += 1
>     while i < n and intervals[i][0] <= newInterval[1]:
>         newInterval[0] = min(newInterval[0], intervals[i][0])
>         newInterval[1] = max(newInterval[1], intervals[i][1])
>         i += 1
>     result.append(newInterval)
>     result.extend(intervals[i:])
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> Binary search to find insertion point — still O(n) for the merge phase but reduces comparisons in phase 1.

---

### Non-overlapping Intervals (LC 435)

> [!example] Problem
> Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.
> Note that intervals which only touch at a point are non-overlapping. For example, [1, 2] and [2, 3] are non-overlapping.
> 
> **Example 1:**
> ```
> Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
> Output: 1
> Explanation: [1,3] can be removed and the rest of the intervals are non-overlapping.
> ```
> 
> **Example 2:**
> ```
> Input: intervals = [[1,2],[1,2],[1,2]]
> Output: 2
> Explanation: You need to remove two [1,2] to make the rest of the intervals non-overlapping.
> ```
> 
> **Example 3:**
> ```
> Input: intervals = [[1,2],[2,3]]
> Output: 0
> Explanation: You don't need to remove any of the intervals since they're already non-overlapping.
> ```
> 
> **Constraints:**
> - 1 <= intervals.length <= 10^5
> - intervals[i].length == 2
> - -5 * 10^4 <= starti < endi <= 5 * 10^4

> [!info] Approach
> Greedy by earliest end time maximizes the number of non-overlapping intervals kept (classic activity selection). Sort by end time. Keep a running `last_end`. For each interval: if it starts ≥ `last_end`, keep it (update `last_end`); otherwise, discard it (increment removal count). Removals = total − number kept. Ties in end time: keep the one with the earlier end (already handled by sort).


> [!note]- Python Solution
> ```python
> def erase_overlap_intervals(intervals):
>     intervals.sort(key=lambda x: x[1])
>     last_end = float('-inf')
>     kept = 0
>     for start, end in intervals:
>         if start >= last_end:
>             last_end = end
>             kept += 1
>     return len(intervals) - kept
> ```

> [!success] Complexity
> Time O(n log n), Space O(1).

> [!tip] Alternatives
> Sort by start time and greedily remove the interval with the later end — same result, slightly different framing.

---

### Minimum Number of Arrows to Burst Balloons (LC 452)

> [!example] Problem
> There are some spherical balloons taped onto a flat wall that represents the XY-plane. The balloons are represented as a 2D integer array points where points[i] = [xstart, xend] denotes a balloon whose horizontal diameter stretches between xstart and xend. You do not know the exact y-coordinates of the balloons.
> Arrows can be shot up directly vertically (in the positive y-direction) from different points along the x-axis. A balloon with xstart and xend is burst by an arrow shot at x if xstart <= x <= xend. There is no limit to the number of arrows that can be shot. A shot arrow keeps traveling up infinitely, bursting any balloons in its path.
> Given the array points, return the minimum number of arrows that must be shot to burst all balloons.
> 
> **Example 1:**
> ```
> Input: points = [[10,16],[2,8],[1,6],[7,12]]
> Output: 2
> Explanation: The balloons can be burst by 2 arrows:
> - Shoot an arrow at x = 6, bursting the balloons [2,8] and [1,6].
> - Shoot an arrow at x = 11, bursting the balloons [10,16] and [7,12].
> ```
> 
> **Example 2:**
> ```
> Input: points = [[1,2],[3,4],[5,6],[7,8]]
> Output: 4
> Explanation: One arrow needs to be shot for each balloon for a total of 4 arrows.
> ```
> 
> **Example 3:**
> ```
> Input: points = [[1,2],[2,3],[3,4],[4,5]]
> Output: 2
> Explanation: The balloons can be burst by 2 arrows:
> - Shoot an arrow at x = 2, bursting the balloons [1,2] and [2,3].
> - Shoot an arrow at x = 4, bursting the balloons [3,4] and [4,5].
> ```
> 
> **Constraints:**
> - 1 <= points.length <= 10^5
> - points[i].length == 2
> - -2^{31} <= xstart < xend <= 2^{31} - 1

> [!info] Approach
> Same greedy activity-selection structure as LC 435. Sort by end point; one arrow at the earliest end bursts as many overlapping balloons as possible. Sort intervals by end. Fire an arrow at the first interval's end. Skip all balloons burst by this arrow. Fire again at the next unbursted balloon's end. A balloon `[start, end]` is burst by arrow at position `pos` iff `start <= pos <= end`.


> [!note]- Python Solution
> ```python
> def find_min_arrow_shots(points):
>     points.sort(key=lambda x: x[1])
>     arrows = 1
>     arrow_pos = points[0][1]
>     for start, end in points[1:]:
>         if start > arrow_pos:
>             arrows += 1
>             arrow_pos = end
>     return arrows if points else 0
> ```

> [!success] Complexity
> Time O(n log n), Space O(1).

> [!tip] Alternatives
> Sort by start time with a priority queue (overkill here). Note the strict inequality vs LC 435 — touching endpoints count as burst.

---

## Offline Sorting Tricks

### Sort Array by Parity (LC 905)

> [!example] Problem
> Given an integer array nums, move all the even integers at the beginning of the array followed by all the odd integers.
> Return any array that satisfies this condition.
> 
> **Example 1:**
> ```
> Input: nums = [3,1,2,4]
> Output: [2,4,3,1]
> Explanation: The outputs [4,2,3,1], [2,4,1,3], and [4,2,1,3] would also be accepted.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0]
> Output: [0]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 5000
> - 0 <= nums[i] <= 5000

> [!info] Approach
> Classic two-pointer Dutch-flag-style partition. O(n) time, O(1) extra space. Left pointer seeks odd from the left; right pointer seeks even from the right. Swap when both are found. Invariant: everything left of `lo` is even; everything right of `hi` is odd.


> [!note]- Python Solution
> ```python
> def sort_array_by_parity(nums):
>     lo, hi = 0, len(nums) - 1
>     while lo < hi:
>         while lo < hi and nums[lo] % 2 == 0:
>             lo += 1
>         while lo < hi and nums[hi] % 2 == 1:
>             hi -= 1
>         nums[lo], nums[hi] = nums[hi], nums[lo]
>         lo += 1; hi -= 1
>     return nums
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> `sorted(nums, key=lambda x: x % 2)` — O(n log n), stable but extra space. For stable in-place: insertion sort by parity — O(n²).

---

### Relative Sort Array (LC 1122)

> [!example] Problem
> Given two arrays arr1 and arr2, the elements of arr2 are distinct, and all elements in arr2 are also in arr1.
> Sort the elements of arr1 such that the relative ordering of items in arr1 are the same as in arr2. Elements that do not appear in arr2 should be placed at the end of arr1 in ascending order.
> 
> **Example 1:**
> ```
> Input: arr1 = [2,3,1,3,2,4,6,7,9,2,19], arr2 = [2,1,4,3,9,6]
> Output: [2,2,2,1,4,3,3,9,6,7,19]
> ```
> 
> **Example 2:**
> ```
> Input: arr1 = [28,6,22,8,44,17], arr2 = [22,28,8,6]
> Output: [22,28,8,6,17,44]
> ```
> 
> **Constraints:**
> - 1 <= arr1.length, arr2.length <= 1000
> - 0 <= arr1[i], arr2[i] <= 1000
> - All the elements of arr2 are distinct.
> - Each arr2[i] is in arr1.

> [!info] Approach
> Custom rank sort: elements in `arr2` get rank equal to their index in `arr2`; elements not in `arr2` get rank `len(arr2) + value` to sort them ascending after the defined group. Build a rank map from `arr2`. Sort `arr1` with a key function using this rank map. Key = `rank[x]` if `x in rank` else `len(arr2) + x`.


> [!note]- Python Solution
> ```python
> def relative_sort_array(arr1, arr2):
>     rank = {v: i for i, v in enumerate(arr2)}
>     return sorted(arr1, key=lambda x: rank[x] if x in rank else len(arr2) + x)
> ```

> [!success] Complexity
> Time O(n log n + m), Space O(m), where m = len(arr2).

> [!tip] Alternatives
> Counting sort: collect elements by their `arr2` position bucket, then append remaining sorted. O(n + m + max_val).

---

### Advantages Shuffle (LC 870)

> [!example] Problem
> You are given two integer arrays nums1 and nums2 both of the same length. The advantage of nums1 with respect to nums2 is the number of indices i for which nums1[i] > nums2[i].
> Return any permutation of nums1 that maximizes its advantage with respect to nums2.
> 
> **Example 1:**
> ```
> Input: nums1 = [2,7,11,15], nums2 = [1,10,4,11]
> Output: [2,11,7,15]
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [12,24,8,32], nums2 = [13,25,32,11]
> Output: [24,32,8,12]
> ```
> 
> **Constraints:**
> - 1 <= nums1.length <= 10^5
> - nums2.length == nums1.length
> - 0 <= nums1[i], nums2[i] <= 10^9

> [!info] Approach
> Greedy: for each element of `nums2` (sorted descending), try to "beat" it with the smallest element of `nums1` that is still larger. If none can beat it, assign the globally smallest remaining element (sacrifice it). Sort `nums1`. Use a deque sorted ascending. Process `nums2` sorted by value descending. For each `nums2[i]`, if `nums1`'s max > `nums2[i]`, assign that max; otherwise assign the min (sacrifice). Track original indices of `nums2` to place answers correctly.


> [!note]- Python Solution
> ```python
> from collections import deque
> def advantage_count(nums1, nums2):
>     nums1.sort()
>     order = sorted(range(len(nums2)), key=lambda i: -nums2[i])
>     lo, hi = 0, len(nums1) - 1
>     result = [0] * len(nums1)
>     dq = deque(sorted(nums1))
>     for i in order:
>         if dq[-1] > nums2[i]:
>             result[i] = dq.pop()
>         else:
>             result[i] = dq.popleft()
>     return result
> ```

> [!success] Complexity
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> Two-pointer on sorted `nums1` and sorted `(value, original_index)` pairs from `nums2` — same complexity, slightly cleaner.

---

## Topological Sort

### Course Schedule II (LC 210)

> [!example] Problem
> There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.
> Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.
> 
> **Example 1:**
> ```
> Input: numCourses = 2, prerequisites = [[1,0]]
> Output: [0,1]
> Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1].
> ```
> 
> **Example 2:**
> ```
> Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
> Output: [0,2,1,3]
> Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
> So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].
> ```
> 
> **Example 3:**
> ```
> Input: numCourses = 1, prerequisites = []
> Output: [0]
> ```
> 
> **Constraints:**
> - 1 <= numCourses <= 2000
> - 0 <= prerequisites.length <= numCourses * (numCourses - 1)
> - prerequisites[i].length == 2
> - 0 <= ai, bi < numCourses
> - ai != bi
> - All the pairs [ai, bi] are distinct.

> [!info] Approach
> Topological sort detects cycles and produces a valid linear ordering of a DAG. Kahn's BFS is iterative and cycle-detection falls out naturally (unprocessed nodes remain). Build adjacency list + in-degree array. Enqueue all nodes with in-degree 0. BFS: pop node → add to order → decrement neighbors' in-degrees → enqueue any that reach 0. If `len(order) < n`, a cycle exists → return `[]`.


> [!note]- Python Solution
> ```python
> from collections import deque
> def find_order(numCourses, prerequisites):
>     graph = [[] for _ in range(numCourses)]
>     indegree = [0] * numCourses
>     for a, b in prerequisites:
>         graph[b].append(a)
>         indegree[a] += 1
>     queue = deque(i for i in range(numCourses) if indegree[i] == 0)
>     order = []
>     while queue:
>         node = queue.popleft()
>         order.append(node)
>         for nei in graph[node]:
>             indegree[nei] -= 1
>             if indegree[nei] == 0:
>                 queue.append(nei)
>     return order if len(order) == numCourses else []
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> DFS-based topological sort with `visited` / `in-stack` coloring. Post-order DFS reversal gives topo order; back edge → cycle.

---

### Alien Dictionary (LC 269)

> [!example] Problem
> There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you.
> 
> You are given a list of strings `words` from the alien language's dictionary. Now it is claimed that the strings in `words` are **sorted lexicographically** by the rules of this new language.
> 
> If this claim is incorrect, and the given arrangement of string in `words` cannot correspond to any order of letters, return `"".`
> 
> Otherwise, return *a string of the unique letters in the new alien language sorted in **lexicographically increasing order** by the new language's rules**. *If there are multiple solutions, return* **any of them***.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** words = ["wrt","wrf","er","ett","rftt"]
> **Output:** "wertf"
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** words = ["z","x"]
> **Output:** "zx"
> 
> ```
> 
> Example 3:
> 
> ```
> 
> **Input:** words = ["z","x","z"]
> **Output:** ""
> **Explanation:** The order is invalid, so return `""`.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= words.length <= 100`
> 	
> - `1 <= words[i].length <= 100`
> 	
> - `words[i]` consists of only lowercase English letters.

> [!info] Approach
> Adjacent words in the sorted list reveal relative character ordering. Build a directed graph from these relations, then topological sort gives the alphabet. Compare each consecutive pair of words character-by-character; the first mismatch gives an edge `u → v` (u comes before v). Detect invalid input: if word A is a prefix of shorter word B, that's impossible. Kahn's BFS topological sort on the character graph. Cycle → return `""`. Unconnected characters can appear anywhere.


> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> def alien_order(words):
>     graph = defaultdict(set)
>     indegree = {c: 0 for w in words for c in w}
>     for i in range(len(words) - 1):
>         w1, w2 = words[i], words[i + 1]
>         min_len = min(len(w1), len(w2))
>         if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
>             return ""
>         for c1, c2 in zip(w1, w2):
>             if c1 != c2:
>                 if c2 not in graph[c1]:
>                     graph[c1].add(c2)
>                     indegree[c2] += 1
>                 break
>     queue = deque(c for c in indegree if indegree[c] == 0)
>     order = []
>     while queue:
>         c = queue.popleft()
>         order.append(c)
>         for nei in graph[c]:
>             indegree[nei] -= 1
>             if indegree[nei] == 0:
>                 queue.append(nei)
>     return "".join(order) if len(order) == len(indegree) else ""
> ```

> [!success] Complexity
> Time O(C) where C = total characters across all words, Space O(U + E), U = unique chars.

> [!tip] Alternatives
> DFS with cycle detection (white/gray/black coloring). Output is reverse post-order.

---

## External Sort / K-way Merge

### Find K Pairs with Smallest Sums (LC 373)

> [!example] Problem
> You are given two integer arrays nums1 and nums2 sorted in non-decreasing order and an integer k.
> Define a pair (u, v) which consists of one element from the first array and one element from the second array.
> Return the k pairs (u1, v1), (u2, v2), ..., (uk, vk) with the smallest sums.
> 
> **Example 1:**
> ```
> Input: nums1 = [1,7,11], nums2 = [2,4,6], k = 3
> Output: [[1,2],[1,4],[1,6]]
> Explanation: The first 3 pairs are returned from the sequence: [1,2],[1,4],[1,6],[7,2],[7,4],[11,2],[7,6],[11,4],[11,6]
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [1,1,2], nums2 = [1,2,3], k = 2
> Output: [[1,1],[1,1]]
> Explanation: The first 2 pairs are returned from the sequence: [1,1],[1,1],[1,2],[2,1],[1,2],[2,2],[1,3],[1,3],[2,3]
> ```
> 
> **Constraints:**
> - 1 <= nums1.length, nums2.length <= 10^5
> - -10^9 <= nums1[i], nums2[i] <= 10^9
> - nums1 and nums2 both are sorted in non-decreasing order.
> - 1 <= k <= 10^4
> - k <= nums1.length * nums2.length

> [!info] Approach
> K-way merge pattern: each row `i` of the implicit (nums1 × nums2) matrix is sorted. A min-heap efficiently extracts the global minimum at each step. Seed the heap with `(nums1[i] + nums2[0], i, 0)` for all i < min(k, len(nums1)). Each pop yields the next best pair; push the next pair in the same row (increment j). At most k pops → O(k log k) after O(min(k, m) log min(k, m)) initial heapify.


> [!note]- Python Solution
> ```python
> import heapq
> def k_smallest_pairs(nums1, nums2, k):
>     if not nums1 or not nums2:
>         return []
>     heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
>     heapq.heapify(heap)
>     result = []
>     while heap and len(result) < k:
>         _, i, j = heapq.heappop(heap)
>         result.append([nums1[i], nums2[j]])
>         if j + 1 < len(nums2):
>             heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
>     return result
> ```

> [!success] Complexity
> Time O(k log k), Space O(k).

> [!tip] Alternatives
> Binary search on sum value + counting — complex but useful when k is very large. Brute force: generate all pairs and heap-select top-k — O(mn log k).

---

### Kth Smallest Element in a Sorted Matrix (LC 378)

> [!example] Problem
> Given an n x n matrix where each of the rows and columns is sorted in ascending order, return the kth smallest element in the matrix.
> Note that it is the kth smallest element in the sorted order, not the kth distinct element.
> You must find a solution with a memory complexity better than O(n2).
> 
> **Example 1:**
> ```
> Input: matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
> Output: 13
> Explanation: The elements in the matrix are [1,5,9,10,11,12,13,13,15], and the 8th smallest number is 13
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [[-5]], k = 1
> Output: -5
> ```
> 
> **Constraints:**
> - n == matrix.length == matrix[i].length
> - 1 <= n <= 300
> - -10^9 <= matrix[i][j] <= 10^9
> - All the rows and columns of matrix are guaranteed to be sorted in non-decreasing order.
> - 1 <= k <= n2

> [!info] Approach
> Two canonical approaches — heap-based k-way merge and binary search on value range. Binary search is O(n log(max − min)) and avoids heap overhead.

> Binary search the answer between `matrix[0][0]` and `matrix[n-1][n-1]`. To count values ≤ `mid`, start top-right: if `matrix[r][c] <= mid`, add `r+1` to the count and move right; else move up. O(n) per count.

> [!note]- Python Solution
> ```python
> def kth_smallest(matrix, k):
>     n = len(matrix)
>     def count_le(mid):
>         r, c = 0, n - 1
>         cnt = 0
>         while r < n and c >= 0:
>             if matrix[r][c] <= mid:
>                 cnt += r + 1
>                 c -= 1
>             else:
>                 r += 1
>         return cnt
>     lo, hi = matrix[0][0], matrix[n - 1][n - 1]
>     while lo < hi:
>         mid = (lo + hi) // 2
>         if count_le(mid) < k:
>             lo = mid + 1
>         else:
>             hi = mid
>     return lo
> ```

> [!success] Complexity
> Time O(n log(max − min)), Space O(1). Heap approach: O(k log n), Space O(n).

> [!tip] Alternatives
> Min-heap k-way merge: push first column, pop k times each time pushing the next in the same row — O(k log n).

---

## Partial Sort / Order Statistics

### Kth Largest Element in a Stream (LC 703)

> [!example] Problem
> You are part of a university admissions office and need to keep track of the kth highest test score from applicants in real-time. This helps to determine cut-off marks for interviews and admissions dynamically as new applicants submit their scores.
> You are tasked to implement a class which, for a given integer k, maintains a stream of test scores and continuously returns the kth highest test score after a new score has been submitted. More specifically, we are looking for the kth highest score in the sorted list of all scores.
> Implement the KthLargest class
> 
> **Example 1:**
> ```
> Input: ["KthLargest", "add", "add", "add", "add", "add"] [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]
> Output: [null, 4, 5, 5, 8, 8]
> Explanation:
> KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]); kthLargest.add(3); // return 4 kthLargest.add(5); // return 5 kthLargest.add(10); // return 5 kthLargest.add(9); // return 8 kthLargest.add(4); // return 8
> ```
> 
> **Example 2:**
> ```
> Input: ["KthLargest", "add", "add", "add", "add"] [[4, [7, 7, 7, 7, 8, 3]], [2], [10], [9], [9]]
> Output: [null, 7, 7, 7, 8]
> Explanation:
> ```
> 
> **Constraints:**
> - 0 <= nums.length <= 10^4
> - 1 <= k <= nums.length + 1
> - -10^4 <= nums[i] <= 10^4
> - -10^4 <= val <= 10^4
> - At most 10^4 calls will be made to add.

> [!info] Approach
> A min-heap of size k maintains exactly the k largest elements seen so far. The heap root is always the kth largest. On initialization, add all elements and trim to size k. On `add`: push new value, pop if size > k, return heap[0]. Heap size invariant: always ≤ k. After each add, heap[0] = k-th largest among all seen elements.


> [!note]- Python Solution
> ```python
> import heapq
> class KthLargest:
>     def __init__(self, k, nums):
>         self.k = k
>         self.heap = nums[:]
>         heapq.heapify(self.heap)
>         while len(self.heap) > k:
>             heapq.heappop(self.heap)
>     def add(self, val):
>         heapq.heappush(self.heap, val)
>         if len(self.heap) > self.k:
>             heapq.heappop(self.heap)
>         return self.heap[0]
> ```

> [!success] Complexity
> Init O(n log k), add O(log k), Space O(k).

> [!tip] Alternatives
> Balanced BST / order-statistics tree for O(log n) add and O(1) kth query. Overkill for fixed k.

---

### Find Median from Data Stream (LC 295)

> [!example] Problem
> The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.
> Implement the MedianFinder class
> 
> **Example 1:**
> ```
> Input
> ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
> [[], [1], [2], [], [3], []]
> Output
> [null, null, null, 1.5, null, 2.0]
> 
> Explanation
> MedianFinder medianFinder = new MedianFinder();
> medianFinder.addNum(1);    // arr = [1]
> medianFinder.addNum(2);    // arr = [1, 2]
> medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
> medianFinder.addNum(3);    // arr[1, 2, 3]
> medianFinder.findMedian(); // return 2.0
> ```
> 
> **Constraints:**
> - -10^5 <= num <= 10^5
> - There will be at least one element in the data structure before calling findMedian.
> - At most 5 * 10^4 calls will be made to addNum and findMedian.

> [!info] Approach
> Two heaps maintain a balanced partition: a max-heap for the lower half and a min-heap for the upper half. Median is always accessible at the tops. `lo` = max-heap (negate values for Python's min-heap), `hi` = min-heap. Invariant: `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`. Median = `lo[0]` if odd total, else `(-lo[0] + hi[0]) / 2`. On add: push to `lo` (negate), rebalance by moving top of `lo` to `hi`, then if `len(hi) > len(lo)` move top of `hi` back to `lo`.


> [!note]- Python Solution
> ```python
> import heapq
> class MedianFinder:
>     def __init__(self):
>         self.lo = []  # max-heap (negated)
>         self.hi = []  # min-heap
>     def add_num(self, num):
>         heapq.heappush(self.lo, -num)
>         heapq.heappush(self.hi, -heapq.heappop(self.lo))
>         if len(self.hi) > len(self.lo):
>             heapq.heappush(self.lo, -heapq.heappop(self.hi))
>     def find_median(self):
>         if len(self.lo) > len(self.hi):
>             return -self.lo[0]
>         return (-self.lo[0] + self.hi[0]) / 2
> ```

> [!success] Complexity
> addNum O(log n), findMedian O(1), Space O(n).

> [!tip] Alternatives
> Sorted list with bisect — O(n) insert, O(1) median. Order-statistics tree — O(log n) insert/query. For follow-up: if values are bounded integers, use two BITs for O(log M) all operations.

---

### Sliding Window Median (LC 480)

> [!example] Problem
> The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle values.
> You are given an integer array nums and an integer k. There is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
> Return the median array for each window in the original array. Answers within 10-5 of the actual value will be accepted.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
> Output: [1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]
> Explanation: 
> Window position                Median
> ---------------                -----
> [1  3  -1] -3  5  3  6  7        1
>  1 [3  -1  -3] 5  3  6  7       -1
>  1  3 [-1  -3  5] 3  6  7       -1
>  1  3  -1 [-3  5  3] 6  7        3
>  1  3  -1  -3 [5  3  6] 7        5
>  1  3  -1  -3  5 [3  6  7]       6
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,4,2,3,1,4,2], k = 3
> Output: [2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]
> ```
> 
> **Constraints:**
> - 1 <= k <= nums.length <= 10^5
> - -2^{31} <= nums[i] <= 2^{31} - 1

> [!info] Approach
> Extends the two-heap median approach with lazy deletion to handle outgoing elements. Two heaps (`lo` max-heap, `hi` min-heap) as in LC 295. Keep a `to_remove` counter map. When sliding the window, mark the outgoing element for lazy removal. Rebalance heap sizes. Before reading median, skip heap tops that are flagged for removal. Rebalance: after each add/remove, ensure `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`. Lazy removal: pop from heap top while `heap[0]` is in `to_remove`.


> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> def median_sliding_window(nums, k):
>     lo, hi = [], []  # lo: max-heap (neg), hi: min-heap
>     remove = defaultdict(int)
> >
>     def push(x):
>         if lo and -lo[0] >= x:
>             heapq.heappush(lo, -x)
>         else:
>             heapq.heappush(hi, x)
> >
>     def rebalance():
>         while lo and remove[-lo[0]]:
>             remove[-lo[0]] -= 1; heapq.heappop(lo)
>         while hi and remove[hi[0]]:
>             remove[hi[0]] -= 1; heapq.heappop(hi)
>         while len(lo) > len(hi) + 1:
>             heapq.heappush(hi, -heapq.heappop(lo))
>         while len(hi) > len(lo):
>             heapq.heappush(lo, -heapq.heappop(hi))
> >
>     def get_median():
>         rebalance()
>         if k % 2 == 1:
>             return float(-lo[0])
>         return (-lo[0] + hi[0]) / 2.0
> >
>     for x in nums[:k]:
>         push(x)
>     rebalance()
>     result = [get_median()]
>     for i in range(k, len(nums)):
>         push(nums[i])
>         remove[nums[i - k]] += 1
>         rebalance()
>         result.append(get_median())
>     return result
> ```

> [!success] Complexity
> Time O(n log k), Space O(k).

> [!tip] Alternatives
> Two `SortedList` (from `sortedcontainers`) — O(n log k), cleaner code. Segment tree on compressed coordinates — O(n log n).

---

## See Also

[[divide-and-conquer]] | [[heap]] | [[binary-search]] | [[greedy]]
### Wiggle Sort II (Median Split)

> [!example] Problem
> Given an integer array nums, reorder it such that nums[0]  nums[2] < nums[3]....
> You may assume the input array always has a valid answer.
> 
> **Example 1:**
> ```
> Input: nums = [1,5,1,1,6,4]
> Output: [1,6,1,5,1,4]
> Explanation: [1,4,1,5,1,6] is also accepted.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,3,2,2,3,1]
> Output: [2,3,1,3,1,2]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 5 * 10^4
> - 0 <= nums[i] <= 5000
> - It is guaranteed that there will be an answer for the given input nums.

> [!info] Approach
> The median separates smaller and larger elements. Interleaving the two halves around the median avoids adjacent violations. Find the median, then place elements using virtual indexing so the larger half fills odd positions and the smaller half fills even positions. Sort and split around the median; place the larger half into odd slots and the smaller half into even slots in reverse order.


> [!note]- Python Solution
> ```python
> def wiggle_sort(nums):
>     nums.sort()
>     half = (len(nums) + 1) // 2
>     small = nums[:half][::-1]
>     large = nums[half:][::-1]
>     nums[::2] = small
>     nums[1::2] = large
> ```

> [!success] Complexity
> O(n log n) time for the simple sort-based version, O(n) extra space.

> [!tip] Alternatives
> An O(n) quickselect + 3-way partition version exists, but the sort-based solution is easier to reason about in interviews.

---

## Sorting Applications

### Maximum Gap (LC 164)

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
> Sorting is O(n log n). For O(n), use bucket sort (pigeonhole principle). If `n` numbers span range `[min, max]`, with `n-1` gaps, the maximum gap is at least `(max - min) / (n - 1)`. Place each number in a bucket of that size — the maximum gap must span at least two buckets, so we only compare adjacent bucket boundaries. Create `n-1` buckets. For each number, assign it to bucket `(num - min_val) * (n - 1) // (max_val - min_val)`. Track min and max within each bucket. The answer is the maximum `bucket[i+1].min - bucket[i].max` across adjacent non-empty buckets. Edge cases: if all elements are equal, return 0. If n < 2, return 0.


> [!note]- Python Solution
> ```python
> def maximum_gap(nums):
>     n = len(nums)
>     if n < 2:
>         return 0
>     min_val = min(nums)
>     max_val = max(nums)
>     if min_val == max_val:
>         return 0
>     bucket_size = max(1, (max_val - min_val) // (n - 1))
>     num_buckets = (max_val - min_val) // bucket_size + 1
>     buckets = [[float('inf'), float('-inf')] for _ in range(num_buckets)]
>     for num in nums:
>         idx = (num - min_val) // bucket_size
>         buckets[idx][0] = min(buckets[idx][0], num)
>         buckets[idx][1] = max(buckets[idx][1], num)
>     max_gap = 0
>     prev_max = min_val
>     for bucket_min, bucket_max in buckets:
>         if bucket_min == float('inf'):
>             continue
>         max_gap = max(max_gap, bucket_min - prev_max)
>         prev_max = bucket_max
>     return max_gap
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Radix sort: also O(n) time and space, achieves the same goal but harder to implement correctly in an interview.
> - Key insight: elements within the same bucket can never be the maximum gap pair (bucket size ≤ max gap), so we only compare across bucket boundaries.

---

### Relative Sort Array (LC 1122)

> [!example] Problem
> Given two arrays arr1 and arr2, the elements of arr2 are distinct, and all elements in arr2 are also in arr1.
> Sort the elements of arr1 such that the relative ordering of items in arr1 are the same as in arr2. Elements that do not appear in arr2 should be placed at the end of arr1 in ascending order.
> 
> **Example 1:**
> ```
> Input: arr1 = [2,3,1,3,2,4,6,7,9,2,19], arr2 = [2,1,4,3,9,6]
> Output: [2,2,2,1,4,3,3,9,6,7,19]
> ```
> 
> **Example 2:**
> ```
> Input: arr1 = [28,6,22,8,44,17], arr2 = [22,28,8,6]
> Output: [22,28,8,6,17,44]
> ```
> 
> **Constraints:**
> - 1 <= arr1.length, arr2.length <= 1000
> - 0 <= arr1[i], arr2[i] <= 1000
> - All the elements of arr2 are distinct.
> - Each arr2[i] is in arr1.

> [!info] Approach
> Standard sorting can't directly encode a custom ordering defined by another array. We need a custom comparator key that maps `arr2` elements to their positions, and sends missing elements to the back. Build a rank map from `arr2`. Sort `arr1` using key: elements in `arr2` get rank `0..len(arr2)-1`, elements not in `arr2` get rank `len(arr2) + value` (ensuring ascending order after all arr2 elements). `rank = {v: i for i, v in enumerate(arr2)}`. Sort with `key = lambda x: rank[x] if x in rank else len(arr2) + x`.


> [!note]- Python Solution
> ```python
> def relative_sort_array(arr1, arr2):
>     rank = {v: i for i, v in enumerate(arr2)}
>     def sort_key(x):
>         if x in rank:
>             return (0, rank[x])
>         return (1, x)
>     arr1.sort(key=sort_key)
>     return arr1
> ```

> [!success] Complexity
> Time O(n log n + m) where n = len(arr1), m = len(arr2). Space O(m).

> [!tip] Alternatives
> - Counting sort: count frequencies in arr1, emit arr2 elements first (using their counts), then remaining elements in sorted order. O(n + m + max_value) — O(n) but requires bounded values.

---

## See Also

[[array]] | [[binary-search]] | [[greedy]] | [[two-pointers]]
