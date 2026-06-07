---
tags: [coding, algorithms, sorting]
topic: Sorting
difficulty: mixed
---

# Sorting — Problem Compendium

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.


> [!info] Approach
> Identify what property sorting exposes (adjacency, rank, monotone structure), then apply the right sort variant. Non-comparison sorts (counting/radix/bucket) bypass O(n log n) when keys are bounded integers. QuickSelect gets rank-k in O(n) avg. Merge sort naturally counts cross-half inversions.




---

## Merge Sort Variants

## QuickSort / QuickSelect

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

### Majority Element (Boyer-Moore) `🎯 T2`

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

### Course Schedule II (LC 210) `⚡ T1`

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

### Alien Dictionary (LC 269) `⚡ T1`

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

### Find K Pairs with Smallest Sums (LC 373) `⚡ T1`

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

### Kth Largest Element in a Stream (LC 703) `⚡ T1`

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

### Find Median from Data Stream (LC 295) `⚡ T1`

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
