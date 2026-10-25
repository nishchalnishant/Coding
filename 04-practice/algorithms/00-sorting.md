---
tags: [coding, algorithms, sorting]
topic: Sorting
difficulty: mixed
---
# Sorting — Problem Compendium

## What this covers

> [!abstract] In this file
> **Covers:** Worked sorting problems: merge-sort variants (inversions), quickselect, bucket sort, intervals/sweep line, custom ordering, topological sort, K-way merge.
> **You'll be able to:** Use sort as the first step and know when quickselect/bucket sort beats it.
> **Prereqs:** Sorting lecture · **Pair with:** [Sorting lecture](../../02-algorithms/00-sorting.md) · **Time:** 3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/l3-google-roadmap.md#tier-legend))

**Sections:** [QuickSort / QuickSelect](#quicksort--quickselect) · [Bucket Sort](#bucket-sort) · [Interview Classics](#interview-classics) · [Classic Merge Variants](#classic-merge-variants) · [Interval / Sweep Line](#interval--sweep-line) · [Offline Sorting Tricks](#offline-sorting-tricks) · [Topological Sort](#topological-sort) · [External Sort / K-way Merge](#external-sort--k-way-merge) · [Sorting Applications](#sorting-applications)

---

> [!info] Approach
> Identify what property sorting exposes (adjacency, rank, monotone structure), then apply the right sort variant. Non-comparison sorts (counting/radix/bucket) bypass O(n log n) when keys are bounded integers. QuickSelect gets rank-k in O(n) avg. Merge sort naturally counts cross-half inversions.

---

## QuickSort / QuickSelect

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

---

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

> [!tip] Recognize · Gotcha
> **Signal:** QuickSelect for median; 3-way partition; interleave via index mapping · **Gotcha:** 1)` places larger half at odd indices without extra space.

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
>             lo += 1
>             mid += 1
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

---

### H-Index (LC 274) `⚡ T1`

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

> Full walkthrough: [Meeting Rooms II](16-greedy.md#meeting-rooms-ii).

---

## Classic Merge Variants

---

### Majority Element (Boyer-Moore) `🎯 T2`

> Full walkthrough: [Majority Element](../data-structures/01-array.md#majority-element--t2).

---

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
>             digits[i] = pool[j]
>             j += 1
>     return int("".join(digits))
> ```

> [!success] Complexity
> Time O(n log n) for the sort (n ≤ 9 digits → effectively O(1)), Space O(n).

> [!tip] Alternatives
> Counting sort bucket per parity group is O(n + 10) = O(n). Note: LC 2231 specifically restricts swaps to same-parity indices.

---

## Interval / Sweep Line

---

### Minimum Number of Arrows to Burst Balloons (LC 452)

> Full walkthrough: [Minimum Number of Arrows to Burst Balloons](16-greedy.md#minimum-number-of-arrows-to-burst-balloons).

---

## Offline Sorting Tricks

---

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
>         lo += 1
>         hi -= 1
>     return nums
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> `sorted(nums, key=lambda x: x % 2)` — O(n log n), stable but extra space. For stable in-place: insertion sort by parity — O(n²).

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

---

### Course Schedule II (LC 210) `⚡ T1`

> Full walkthrough: [Course Schedule II](../data-structures/13-graph.md#course-schedule-ii--t1).

---

### Alien Dictionary (LC 269) `⚡ T1`

> Full walkthrough: [Alien Dictionary](../data-structures/06-queue.md#alien-dictionary--t1).

---

## External Sort / K-way Merge

---

### Find K Pairs with Smallest Sums (LC 373) `⚡ T1`

> Full walkthrough: [Find K Pairs with Smallest Sums](../data-structures/10-heap.md#find-k-pairs-with-smallest-sums--t1).

---

### Kth Largest Element in a Stream (LC 703) `⚡ T1`

> Full walkthrough: [Kth Largest Element in a Stream](../data-structures/10-heap.md#kth-largest-element-in-a-stream--t1).

---

### Find Median from Data Stream (LC 295) `⚡ T1`

> Full walkthrough: [Find Median from Data Stream](../data-structures/06-queue.md#find-median-from-data-stream--t1).

---

## Sorting Applications

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
