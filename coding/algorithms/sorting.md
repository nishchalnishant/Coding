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
> Given a list of intervals `[start, end]`, merge all overlapping intervals.

> [!info] Approach
> - WHY: Overlapping intervals can't be detected in arbitrary order. Sorting by start makes all potential overlaps adjacent — reduces O(n²) pair checks to one linear scan.
> - WHAT: Sort by start; greedily extend the last merged interval if `current.start ≤ last.end`.
> - HOW: For each interval after sort, either extend `merged[-1][1] = max(merged[-1][1], end)` or append a new interval.

> [!note]- Python Solution
> ```python
> def merge(intervals: list[list[int]]) -> list[list[int]]:
>     intervals.sort(key=lambda x: x[0])
>     merged: list[list[int]] = []
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
> Sort a linked list in O(n log n) time and O(1) auxiliary space.

> [!info] Approach
> - WHY: Array sorts require O(1) random access; linked lists have O(1) split/merge — merge sort is a natural fit. Top-down recursion uses O(log n) stack; bottom-up avoids even that.
> - WHAT: Find midpoint via slow/fast pointers; recursively sort halves; merge in O(n).
> - HOW: `get_mid` severs the list at the middle. Merge uses dummy head and two pointers.

> [!note]- Python Solution
> ```python
> from typing import Optional
> 
> class ListNode:
>     def __init__(self, val: int = 0, next: 'Optional[ListNode]' = None):
>         self.val = val; self.next = next
> 
> def sortList(head: Optional[ListNode]) -> Optional[ListNode]:
>     if not head or not head.next:
>         return head
> 
>     def get_mid(node: ListNode) -> ListNode:
>         slow, fast = node, node.next
>         while fast and fast.next:
>             slow = slow.next; fast = fast.next.next
>         mid = slow.next
>         slow.next = None  # sever
>         return mid
> 
>     def merge(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
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
> For each `nums[i]`, count how many elements to its right are strictly smaller.

> [!info] Approach
> - WHY: Brute force O(n²). During merge sort, every time a right-half element is placed before remaining left-half elements, those left elements each have a right-smaller count increment of exactly 1. The merge step naturally counts cross-half inversions.
> - WHAT: Tag each element with its original index. In the merge step, when right-half element at position `r` is selected, all remaining left-half elements get `+r` to their count.
> - HOW: Sort `(original_index, value)` pairs; accumulate into `result[original_index]` during merge.

> [!note]- Python Solution
> ```python
> def countSmaller(nums: list[int]) -> list[int]:
>     n = len(nums)
>     result = [0] * n
>     indexed = list(enumerate(nums))  # (orig_idx, value)
> 
>     def merge_sort(arr: list[tuple[int, int]]) -> list[tuple[int, int]]:
>         if len(arr) <= 1:
>             return arr
>         mid = len(arr) // 2
>         left = merge_sort(arr[:mid])
>         right = merge_sort(arr[mid:])
>         merged: list[tuple[int, int]] = []
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
> Count pairs (i, j) with i ≤ j where `lower ≤ sum(nums[i..j]) ≤ upper`.

> [!info] Approach
> - WHY: `sum(nums[i..j]) = prefix[j+1] - prefix[i]`. Need to count pairs in prefix array. Merge sort on prefix array lets us count valid pairs across halves in O(n) per level using two monotone pointers.
> - WHAT: Build prefix sum array (size n+1). Merge sort it counting valid (right - left) pairs.
> - HOW: For each right-half prefix `r`, maintain two pointers `lo, hi` on sorted left half: `lo` = first index where `r - left[lo] ≤ upper`, `hi` = first where `r - left[hi] < lower`. Count = `hi - lo`.

> [!note]- Python Solution
> ```python
> def countRangeSum(nums: list[int], lower: int, upper: int) -> int:
>     from itertools import accumulate
>     prefix = [0] + list(accumulate(nums))
>     count = 0
> 
>     def merge_sort(arr: list[int]) -> list[int]:
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
> Count pairs (i, j) with i < j and `nums[i] > 2 * nums[j]`.

> [!info] Approach
> - WHY: Same merge-sort inversion insight. During merge, left is sorted ascending. For a fixed right element `r`, all left elements `l` with `l > 2*r` form a contiguous suffix (since left is sorted). Advance pointer j monotonically per right element → O(n) counting pass per merge level.
> - WHAT: Separate counting pass before standard merge; two-pointer on sorted left for each right element.
> - HOW: Inner loop: for each `left[i]`, advance `j` while `left[i] > 2 * right[j]`. Count += j per left element.

> [!note]- Python Solution
> ```python
> def reversePairs(nums: list[int]) -> int:
>     count = 0
> 
>     def merge_sort(arr: list[int]) -> list[int]:
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
> - WHY: Brute force O(n²). Merge sort naturally counts inversions — when a right half element is placed before left half elements, each remaining left half element contributes one inversion.
> - WHAT: Modified merge sort. During merge, when right[j] < left[i], add (mid - left_ptr) to count.
> - HOW: Recursive merge sort returning (sorted_array, inversion_count). Standard merge with count accumulation.

> [!note]- Python Solution
> ```python
> def countInversions(arr: list[int]) -> int:
>     def merge_sort(a: list[int]) -> tuple[list[int], int]:
>         if len(a) <= 1:
>             return a, 0
>         mid = len(a) // 2
>         left, lc = merge_sort(a[:mid])
>         right, rc = merge_sort(a[mid:])
>         merged: list[int] = []
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
> Find the kth largest element (not kth distinct).

> [!info] Approach
> - WHY: Full sort O(n log n) computes all ranks; we need only one. QuickSelect partitions around a pivot and recurses into exactly one half — average O(n) total work.
> - WHAT: Randomized partition into [≥pivot | pivot | <pivot]. After partitioning, pivot is at its final rank. Recurse left or right based on pivot rank vs target.
> - HOW: Target rank = k-1 (0-indexed from largest). Stop when pivot index == target.

> [!note]- Python Solution
> ```python
> import random
> 
> def findKthLargest(nums: list[int], k: int) -> int:
>     def partition(lo: int, hi: int) -> int:
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
> Return the k closest points to origin from a list of 2D points.

> [!info] Approach
> - WHY: Need top-k by distance. QuickSelect finds the exact boundary at rank k in O(n) average without sorting all n points. Squared distance avoids sqrt and preserves order.
> - WHAT: QuickSelect partitioning by dist²; once pivot lands at index k, indices 0..k-1 are the k closest.
> - HOW: Partition by dist² ascending; recurse until pivot == k.

> [!note]- Python Solution
> ```python
> def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
>     def dist(p: list[int]) -> int:
>         return p[0] * p[0] + p[1] * p[1]
> 
>     def partition(lo: int, hi: int) -> int:
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
> Return the k most frequent elements in nums.

> [!info] Approach
> - WHY: Count frequencies O(n), then need top-k by frequency. Frequencies are bounded by n — bucket sort on frequency is O(n) total, beating any comparison-based approach.
> - WHAT: Count with hashmap; bucket[freq].append(num) where index = frequency; scan from high to low collecting k elements.
> - HOW: len(nums)+1 buckets (freq ranges 1..n); linear scan backward.

> [!note]- Python Solution
> ```python
> def topKFrequent(nums: list[int], k: int) -> list[int]:
>     from collections import Counter
>     freq = Counter(nums)
>     buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
>     for num, f in freq.items():
>         buckets[f].append(num)
>     result: list[int] = []
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
> Sort array of 0s, 1s, 2s in-place in a single pass (Dutch National Flag).

> [!info] Approach
> - WHY: Only 3 distinct values — counting sort requires two passes. DNF achieves one pass, O(n), O(1) space by maintaining three invariant regions simultaneously.
> - WHAT: Three pointers `lo, mid, hi` partitioning array into [0s | 1s | unexplored | 2s]. Advance mid, swapping 0s left and 2s right.
> - HOW: nums[mid]==0: swap(lo,mid), lo++, mid++. nums[mid]==1: mid++. nums[mid]==2: swap(mid,hi), hi-- (don't advance mid — swapped value is unexplored).

> [!note]- Python Solution
> ```python
> def sortColors(nums: list[int]) -> None:
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
> Find the maximum gap between successive elements in sorted order. Must run in O(n) time.

> [!info] Approach
> - WHY: Comparison sort O(n log n) is too slow. Key insight (Pigeonhole): n elements span [min, max]; the n-1 gaps average `(max-min)/(n-1)`. The maximum gap must be ≥ this average, meaning it must straddle at least one bucket boundary. So intra-bucket gaps are irrelevant — only inter-bucket gaps matter.
> - WHAT: Create n-1 buckets of width `ceil((max-min)/(n-1))`. Track only min/max per bucket. Max gap = max over consecutive non-empty bucket pairs of `next_bucket.min - prev_bucket.max`.
> - HOW: bucket_idx = `(num - min_v) // bucket_width`; scan pairs of consecutive non-empty buckets.

> [!note]- Python Solution
> ```python
> def maximumGap(nums: list[int]) -> int:
>     if len(nums) < 2:
>         return 0
>     min_v, max_v = min(nums), max(nums)
>     if min_v == max_v:
>         return 0
>     n = len(nums)
>     bucket_width = max(1, (max_v - min_v) // (n - 1))
>     num_buckets = (max_v - min_v) // bucket_width + 1
>     # Each bucket stores [min, max] or None
>     buckets: list[Optional[list[int]]] = [None] * num_buckets
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
> Sort a string so characters appear in decreasing order of frequency.

> [!info] Approach
> - WHY: Comparison sort O(n log n). Frequencies are bounded by n — bucket sort achieves O(n).
> - WHAT: Count frequencies; bucket[freq].append(char); build result concatenating `char * freq` from high freq down.
> - HOW: At most n distinct frequencies; linear scan of buckets from top.

> [!note]- Python Solution
> ```python
> def frequencySort(s: str) -> str:
>     from collections import Counter
>     freq = Counter(s)
>     buckets: list[list[str]] = [[] for _ in range(len(s) + 1)]
>     for char, f in freq.items():
>         buckets[f].append(char)
>     result: list[str] = []
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
> Sort array using only "pancake flip" — reverse a prefix of length k. Return sequence of k values used.

> [!info] Approach
> - WHY: Standard swaps aren't available; only prefix reversals. Think selection sort analog: place the largest unsorted element at the correct position using at most 2 flips — bring it to front (flip 1), then flip to final position (flip 2).
> - WHAT: For each size from n down to 2: find max in arr[0..size-1], flip it to front if not there, then flip to position size-1.
> - HOW: At most 2(n-1) flips total.

> [!note]- Python Solution
> ```python
> def pancakeSort(arr: list[int]) -> list[int]:
>     result: list[int] = []
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
> Reconstruct queue from `(height, k)` pairs where k = # people in front with height ≥ this person.

> [!info] Approach
> - WHY: Taller people are unaffected by shorter people's positions. If we insert tallest first, each person's k-value is exact at insertion time (all people in the result list so far are ≥ their height).
> - WHAT: Sort descending by height (ties: ascending by k). Insert each person at index `person[1]`.
> - HOW: Python list.insert(k, person) shifts subsequent elements right — their k values remain valid since all have height ≤ current.

> [!note]- Python Solution
> ```python
> def reconstructQueue(people: list[list[int]]) -> list[list[int]]:
>     people.sort(key=lambda x: (-x[0], x[1]))
>     result: list[list[int]] = []
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
> Sort string `s` using relative order defined by string `order`. Characters not in `order` can be placed anywhere at the end.

> [!info] Approach
> - WHY: Standard sort knows nothing about the custom ordering. Assign integer ranks from `order`; sort `s` by those ranks.
> - WHAT: `rank = {c: i for i, c in enumerate(order)}`; sort `s` with `key=lambda c: rank.get(c, len(order))`.
> - HOW: O(n log n) sort; unranked characters get a default rank beyond the end.

> [!note]- Python Solution
> ```python
> def customSortString(order: str, s: str) -> str:
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
> Arrange non-negative integers to form the largest possible number as a string.

> [!info] Approach
> - WHY: Numeric sort fails (e.g., 9 vs 91: "991" > "919" so 9 should precede 91). The correct ordering is: a before b if str(a)+str(b) > str(b)+str(a). This comparison is transitive and defines a total order.
> - WHAT: Convert to strings; sort with `functools.cmp_to_key` using concatenation comparison.
> - HOW: Edge case: all zeros → return "0".

> [!note]- Python Solution
> ```python
> from functools import cmp_to_key
> 
> def largestNumber(nums: list[int]) -> str:
>     strs = list(map(str, nums))
> 
>     def compare(a: str, b: str) -> int:
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
> Given envelopes [w,h], find the maximum number you can Russian-doll (fit one inside another). Envelope a fits in b if a[0]<b[0] and a[1]<b[1].

> [!info] Approach
> - WHY: Sort by width ascending. For equal widths, sort height DESCENDING — this prevents using two same-width envelopes in the LIS. Then the problem reduces to LIS on heights.
> - WHAT: Sort + LIS with binary search (patience sorting).
> - HOW: Sort envelopes by (w asc, h desc). Extract heights. Find LIS length using binary search on tails array.

> [!note]- Python Solution
> ```python
> import bisect
> 
> def maxEnvelopes(envelopes: list[list[int]]) -> int:
>     envelopes.sort(key=lambda x: (x[0], -x[1]))
>     heights = [e[1] for e in envelopes]
>     tails: list[int] = []
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
> Rearrange array such that nums[0] < nums[1] > nums[2] < nums[3] ...

> [!info] Approach
> - WHY: Find median, then place larger-than-median elements at odd indices and smaller-than-median elements at even indices, both in reverse order to avoid equal adjacent elements.
> - WHAT: QuickSelect for median + index mapping.
> - HOW: Find median (QuickSelect O(n)). Use 3-way partition (Dutch flag). Place using index map i → (1+2*i)%(n|1) to interleave.

> [!note]- Python Solution
> ```python
> def wiggleSort(nums: list[int]) -> None:
>     n = len(nums)
>     # index mapping: virtual index i -> actual index (1+2*i)%(n|1)
>     def idx(i: int) -> int:
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
> Given a citations array, find h such that h papers have at least h citations each.

> [!info] Approach
> - WHY: After sorting descending, at position i (0-indexed), if citations[i] >= i+1 then at least i+1 papers have >= i+1 citations. Track the largest such i+1.
> - WHAT: Sort descending; scan linearly to find max h.
> - HOW: For each i, if citations[i] >= i+1, update h = i+1. Return max h found.

> [!note]- Python Solution
> ```python
> def hIndex(citations: list[int]) -> int:
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
> Given intervals [start, end], find the minimum number of conference rooms required.

> [!info] Approach
> - WHY: Sort by start time. Use a min-heap of end times. For each new meeting, if the earliest-ending room frees up before this meeting starts, reuse it (pop). Push this meeting's end time. Heap size = rooms needed.
> - WHAT: Sort by start + min-heap of end times.
> - HOW: Sort intervals by start. For each interval: if heap and heap[0] <= start, heappop (reuse). heappush(end). Return heap size.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def minMeetingRooms(intervals: list[list[int]]) -> int:
>     if not intervals:
>         return 0
>     intervals.sort(key=lambda x: x[0])
>     heap: list[int] = []  # end times
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
> Merge two sorted linked lists into one sorted linked list.

> [!info] Approach
> - WHY: Both lists are sorted — no need to re-sort. Compare heads; greedily take the smaller head, advancing that pointer. One pass O(m+n).
> - WHAT: Dummy head + two pointers. Attach smaller node at each step; attach remainder when one list exhausts.
> - HOW: Dummy head avoids null-checking the result head. After loop, `cur.next = l1 or l2`.

> [!note]- Python Solution
> ```python
> def mergeTwoLists(
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
> Merge k sorted linked lists into one sorted linked list.

> [!info] Approach
> - WHY: Sequential merge of k lists: O(nk). Min-heap always extracts the globally smallest current head in O(log k); total O(n log k) where n = total nodes.
> - WHAT: Push all list heads into min-heap. Repeatedly pop min node, append to result, push its successor.
> - HOW: Heap entries are `(val, tie_break_id, node)` — tie-break prevents comparing ListNode objects on equal values.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def mergeKLists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
>     heap: list[tuple[int, int, ListNode]] = []
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
> Find the median of two sorted arrays in O(log(m+n)) time.

> [!info] Approach
> - WHY: Merging is O(m+n); need O(log). The median partitions the combined array at position `(m+n)//2`. Binary search on the partition point in the smaller array determines where to cut both arrays such that all left elements ≤ all right elements.
> - WHAT: Binary search on `i` (cut in A); j = `(m+n+1)//2 - i` (cut in B). Valid partition when `A[i-1] ≤ B[j]` and `B[j-1] ≤ A[i]`.
> - HOW: Always binary search on the shorter array. Handle edge cases with ±inf.

> [!note]- Python Solution
> ```python
> def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
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
> Find the element appearing more than n/2 times. Guaranteed to exist.

> [!info] Approach
> - WHY: The majority element has count > n/2, so it outnumbers all others combined. Boyer-Moore voting: each non-majority element can "cancel" one majority element, but majority still survives.
> - WHAT: Maintain `(candidate, count)`. Increment count if current matches candidate; decrement otherwise; reset candidate when count hits 0.
> - HOW: The surviving candidate after one pass is the majority. (If majority not guaranteed, do a second pass to verify.)

> [!note]- Python Solution
> ```python
> def majorityElement(nums: list[int]) -> int:
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
> Find all elements appearing more than n/3 times.

> [!info] Approach
> - WHY: At most 2 elements can satisfy `count > n/3` (since 3 × (⌊n/3⌋+1) > n). Extend Boyer-Moore to track 2 candidates simultaneously.
> - WHAT: Two `(candidate, count)` pairs. Each number either reinforces a candidate, claims a vacant slot (count=0), or decrements both when it matches neither.
> - HOW: After the voting pass, verify both candidates have true count > n/3 (the vote may admit false positives for the second candidate).

> [!note]- Python Solution
> ```python
> def majorityElement2(nums: list[int]) -> list[int]:
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
> Sort an array of integers in O(n) when values are bounded (LC 912 variant). Use counting sort when the value range is small relative to n.

> [!info] Approach
> - WHY: Comparison-based sorts bottom out at O(n log n); counting sort exploits a bounded integer domain to achieve O(n + k).
> - WHAT: Build a frequency array of size `max - min + 1`, accumulate prefix counts, then scatter elements into output in stable order.
> - HOW: Shift values by `min` so indices stay non-negative. Reconstruct the sorted array by iterating the count array.

> [!note]- Python Solution
> ```python
> def sortArray(nums: list[int]) -> list[int]:
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
> - WHY: Achieves O(d · (n + b)) where d = number of digits, b = base (10). Beats comparison sort when d is small.
> - WHAT: For each digit position (units, tens, hundreds, …), perform a stable counting sort keyed on that digit only.
> - HOW: Extract digit with `(x // exp) % base`. Counting sort must be stable so relative order from previous passes is preserved.

> [!note]- Python Solution
> ```python
> def radixSort(nums: list[int]) -> list[int]:
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
> Given a positive integer `num`, swap digits that are at even indices (0-indexed from the left) with digits at even indices only (similarly odd with odd) any number of times. Return the maximum number obtainable.

> [!info] Approach
> - WHY: Digits at even positions can only be rearranged among themselves; same for odd positions. Maximize each group independently.
> - WHAT: Use counting sort (digit frequency array) to greedily fill even positions with the largest available even-position digits, then do the same for odd positions.
> - HOW: Collect digits at even indices into a sorted (descending) pool, refill positions left-to-right from the pool; repeat for odd indices.

> [!note]- Python Solution
> ```python
> def maximumSwap(num: int) -> int:
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
> Given a list of non-overlapping intervals sorted by start time and a new interval, insert the new interval and merge if necessary. Return the resulting list.

> [!info] Approach
> - WHY: The list is already sorted — no re-sort needed. A single linear pass suffices to find overlap and merge.
> - WHAT: Three phases: (1) copy all intervals that end before the new interval starts, (2) merge all overlapping intervals into the new interval, (3) copy remaining intervals.
> - HOW: Overlap condition: `existing.end >= new.start` AND `existing.start <= new.end`.

> [!note]- Python Solution
> ```python
> def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
>     res = []
>     i, n = 0, len(intervals)
>     while i < n and intervals[i][1] < newInterval[0]:
>         res.append(intervals[i]); i += 1
>     while i < n and intervals[i][0] <= newInterval[1]:
>         newInterval[0] = min(newInterval[0], intervals[i][0])
>         newInterval[1] = max(newInterval[1], intervals[i][1])
>         i += 1
>     res.append(newInterval)
>     res.extend(intervals[i:])
>     return res
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> Binary search to find insertion point — still O(n) for the merge phase but reduces comparisons in phase 1.

---

### Non-overlapping Intervals (LC 435)

> [!example] Problem
> Given a list of intervals, find the minimum number of intervals to remove so the rest are non-overlapping.

> [!info] Approach
> - WHY: Greedy by earliest end time maximizes the number of non-overlapping intervals kept (classic activity selection).
> - WHAT: Sort by end time. Keep a running `last_end`. For each interval: if it starts ≥ `last_end`, keep it (update `last_end`); otherwise, discard it (increment removal count).
> - HOW: Removals = total − number kept. Ties in end time: keep the one with the earlier end (already handled by sort).

> [!note]- Python Solution
> ```python
> def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
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
> Balloons are represented as horizontal intervals on the x-axis. An arrow shot vertically at x bursts all balloons whose interval includes x. Find the minimum number of arrows needed to burst all balloons.

> [!info] Approach
> - WHY: Same greedy activity-selection structure as LC 435. Sort by end point; one arrow at the earliest end bursts as many overlapping balloons as possible.
> - WHAT: Sort intervals by end. Fire an arrow at the first interval's end. Skip all balloons burst by this arrow. Fire again at the next unbursted balloon's end.
> - HOW: A balloon `[start, end]` is burst by arrow at position `pos` iff `start <= pos <= end`.

> [!note]- Python Solution
> ```python
> def findMinArrowShots(points: list[list[int]]) -> int:
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
> Given an array of integers, move all even integers to the front and all odd integers to the back. Order within each group does not matter.

> [!info] Approach
> - WHY: Classic two-pointer Dutch-flag-style partition. O(n) time, O(1) extra space.
> - WHAT: Left pointer seeks odd from the left; right pointer seeks even from the right. Swap when both are found.
> - HOW: Invariant: everything left of `lo` is even; everything right of `hi` is odd.

> [!note]- Python Solution
> ```python
> def sortArrayByParity(nums: list[int]) -> list[int]:
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
> Given `arr1` and `arr2` (all elements of `arr2` are distinct and present in `arr1`), sort `arr1` so that elements appearing in `arr2` come first in the relative order defined by `arr2`. Elements not in `arr2` follow in ascending order.

> [!info] Approach
> - WHY: Custom rank sort: elements in `arr2` get rank equal to their index in `arr2`; elements not in `arr2` get rank `len(arr2) + value` to sort them ascending after the defined group.
> - WHAT: Build a rank map from `arr2`. Sort `arr1` with a key function using this rank map.
> - HOW: Key = `rank[x]` if `x in rank` else `len(arr2) + x`.

> [!note]- Python Solution
> ```python
> def relativeSortArray(arr1: list[int], arr2: list[int]) -> list[int]:
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
> Given `nums1` and `nums2` of equal length, reorder `nums1` to maximize the number of positions where `nums1[i] > nums2[i]`. Return the reordered `nums1`.

> [!info] Approach
> - WHY: Greedy: for each element of `nums2` (sorted descending), try to "beat" it with the smallest element of `nums1` that is still larger. If none can beat it, assign the globally smallest remaining element (sacrifice it).
> - WHAT: Sort `nums1`. Use a deque sorted ascending. Process `nums2` sorted by value descending. For each `nums2[i]`, if `nums1`'s max > `nums2[i]`, assign that max; otherwise assign the min (sacrifice).
> - HOW: Track original indices of `nums2` to place answers correctly.

> [!note]- Python Solution
> ```python
> from collections import deque
> def advantageCount(nums1: list[int], nums2: list[int]) -> list[int]:
>     nums1.sort()
>     order = sorted(range(len(nums2)), key=lambda i: -nums2[i])
>     lo, hi = 0, len(nums1) - 1
>     res = [0] * len(nums1)
>     dq = deque(sorted(nums1))
>     for i in order:
>         if dq[-1] > nums2[i]:
>             res[i] = dq.pop()
>         else:
>             res[i] = dq.popleft()
>     return res
> ```

> [!success] Complexity
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> Two-pointer on sorted `nums1` and sorted `(value, original_index)` pairs from `nums2` — same complexity, slightly cleaner.

---

## Topological Sort

### Course Schedule II (LC 210)

> [!example] Problem
> There are `n` courses labeled 0 to n-1 with prerequisites as directed edges. Return a valid order to finish all courses, or an empty list if a cycle exists.

> [!info] Approach
> - WHY: Topological sort detects cycles and produces a valid linear ordering of a DAG. Kahn's BFS is iterative and cycle-detection falls out naturally (unprocessed nodes remain).
> - WHAT: Build adjacency list + in-degree array. Enqueue all nodes with in-degree 0. BFS: pop node → add to order → decrement neighbors' in-degrees → enqueue any that reach 0.
> - HOW: If `len(order) < n`, a cycle exists → return `[]`.

> [!note]- Python Solution
> ```python
> from collections import deque
> def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
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
> Given a sorted list of words in an alien language, derive the character ordering (alphabet order) of the alien language. Return any valid ordering, or `""` if contradictory.

> [!info] Approach
> - WHY: Adjacent words in the sorted list reveal relative character ordering. Build a directed graph from these relations, then topological sort gives the alphabet.
> - WHAT: Compare each consecutive pair of words character-by-character; the first mismatch gives an edge `u → v` (u comes before v). Detect invalid input: if word A is a prefix of shorter word B, that's impossible.
> - HOW: Kahn's BFS topological sort on the character graph. Cycle → return `""`. Unconnected characters can appear anywhere.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> def alienOrder(words: list[str]) -> str:
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
> Given two sorted arrays `nums1` and `nums2`, find the k pairs `(nums1[i], nums2[j])` with the smallest sums.

> [!info] Approach
> - WHY: K-way merge pattern: each row `i` of the implicit (nums1 × nums2) matrix is sorted. A min-heap efficiently extracts the global minimum at each step.
> - WHAT: Seed the heap with `(nums1[i] + nums2[0], i, 0)` for all i < min(k, len(nums1)). Each pop yields the next best pair; push the next pair in the same row (increment j).
> - HOW: At most k pops → O(k log k) after O(min(k, m) log min(k, m)) initial heapify.

> [!note]- Python Solution
> ```python
> import heapq
> def kSmallestPairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
>     if not nums1 or not nums2:
>         return []
>     heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
>     heapq.heapify(heap)
>     res = []
>     while heap and len(res) < k:
>         _, i, j = heapq.heappop(heap)
>         res.append([nums1[i], nums2[j]])
>         if j + 1 < len(nums2):
>             heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
>     return res
> ```

> [!success] Complexity
> Time O(k log k), Space O(k).

> [!tip] Alternatives
> Binary search on sum value + counting — complex but useful when k is very large. Brute force: generate all pairs and heap-select top-k — O(mn log k).

---

### Kth Smallest Element in a Sorted Matrix (LC 378)

> [!example] Problem
> Given an n × n matrix where each row and column is sorted in ascending order, find the kth smallest element.

> [!info] Approach
> - WHY: Two canonical approaches — heap-based k-way merge and binary search on value range. Binary search is O(n log(max − min)) and avoids heap overhead.
> - WHAT (binary search): Binary search on the answer value in [matrix[0][0], matrix[n-1][n-1]]. Count elements ≤ mid using a two-pointer staircase from top-right corner.
> - HOW: Count function: start at top-right; if `matrix[r][c] <= mid` → add `r+1` to count, move right; else move up. O(n) per count call.

> [!note]- Python Solution
> ```python
> def kthSmallest(matrix: list[list[int]], k: int) -> int:
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
> Design a class that finds the kth largest element in a stream. Initialize with k and an initial list; support `add(val)` returning the kth largest after each insertion.

> [!info] Approach
> - WHY: A min-heap of size k maintains exactly the k largest elements seen so far. The heap root is always the kth largest.
> - WHAT: On initialization, add all elements and trim to size k. On `add`: push new value, pop if size > k, return heap[0].
> - HOW: Heap size invariant: always ≤ k. After each add, heap[0] = k-th largest among all seen elements.

> [!note]- Python Solution
> ```python
> import heapq
> class KthLargest:
>     def __init__(self, k: int, nums: list[int]):
>         self.k = k
>         self.heap = nums[:]
>         heapq.heapify(self.heap)
>         while len(self.heap) > k:
>             heapq.heappop(self.heap)
>     def add(self, val: int) -> int:
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
> Design a data structure that supports adding integers and querying the current median at any time.

> [!info] Approach
> - WHY: Two heaps maintain a balanced partition: a max-heap for the lower half and a min-heap for the upper half. Median is always accessible at the tops.
> - WHAT: `lo` = max-heap (negate values for Python's min-heap), `hi` = min-heap. Invariant: `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`. Median = `lo[0]` if odd total, else `(-lo[0] + hi[0]) / 2`.
> - HOW: On add: push to `lo` (negate), rebalance by moving top of `lo` to `hi`, then if `len(hi) > len(lo)` move top of `hi` back to `lo`.

> [!note]- Python Solution
> ```python
> import heapq
> class MedianFinder:
>     def __init__(self):
>         self.lo = []  # max-heap (negated)
>         self.hi = []  # min-heap
>     def addNum(self, num: int) -> None:
>         heapq.heappush(self.lo, -num)
>         heapq.heappush(self.hi, -heapq.heappop(self.lo))
>         if len(self.hi) > len(self.lo):
>             heapq.heappush(self.lo, -heapq.heappop(self.hi))
>     def findMedian(self) -> float:
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
> Given an array and window size k, return the median of each sliding window as it moves from left to right.

> [!info] Approach
> - WHY: Extends the two-heap median approach with lazy deletion to handle outgoing elements.
> - WHAT: Two heaps (`lo` max-heap, `hi` min-heap) as in LC 295. Keep a `to_remove` counter map. When sliding the window, mark the outgoing element for lazy removal. Rebalance heap sizes. Before reading median, skip heap tops that are flagged for removal.
> - HOW: Rebalance: after each add/remove, ensure `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`. Lazy removal: pop from heap top while `heap[0]` is in `to_remove`.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> def medianSlidingWindow(nums: list[int], k: int) -> list[float]:
>     lo, hi = [], []  # lo: max-heap (neg), hi: min-heap
>     remove = defaultdict(int)
>
>     def push(x):
>         if lo and -lo[0] >= x:
>             heapq.heappush(lo, -x)
>         else:
>             heapq.heappush(hi, x)
>
>     def rebalance():
>         while lo and remove[-lo[0]]:
>             remove[-lo[0]] -= 1; heapq.heappop(lo)
>         while hi and remove[hi[0]]:
>             remove[hi[0]] -= 1; heapq.heappop(hi)
>         while len(lo) > len(hi) + 1:
>             heapq.heappush(hi, -heapq.heappop(lo))
>         while len(hi) > len(lo):
>             heapq.heappush(lo, -heapq.heappop(hi))
>
>     def get_median():
>         rebalance()
>         if k % 2 == 1:
>             return float(-lo[0])
>         return (-lo[0] + hi[0]) / 2.0
>
>     for x in nums[:k]:
>         push(x)
>     rebalance()
>     res = [get_median()]
>     for i in range(k, len(nums)):
>         push(nums[i])
>         remove[nums[i - k]] += 1
>         rebalance()
>         res.append(get_median())
>     return res
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
> Rearrange an array so that `nums[0] < nums[1] > nums[2] < nums[3]...`.

> [!info] Approach
> - **WHY:** The median separates smaller and larger elements. Interleaving the two halves around the median avoids adjacent violations.
> - **WHAT:** Find the median, then place elements using virtual indexing so the larger half fills odd positions and the smaller half fills even positions.
> - **HOW:** Sort and split around the median; place the larger half into odd slots and the smaller half into even slots in reverse order.

> [!note]- Python Solution
> ```python
> def wiggle_sort(nums: list[int]) -> None:
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
> Given an unsorted array, find the maximum difference between successive elements in its sorted form. Must run in O(n) time and space.

> [!info] Approach
> - **WHY:** Sorting is O(n log n). For O(n), use bucket sort (pigeonhole principle). If `n` numbers span range `[min, max]`, with `n-1` gaps, the maximum gap is at least `(max - min) / (n - 1)`. Place each number in a bucket of that size — the maximum gap must span at least two buckets, so we only compare adjacent bucket boundaries.
> - **WHAT:** Create `n-1` buckets. For each number, assign it to bucket `(num - min_val) * (n - 1) // (max_val - min_val)`. Track min and max within each bucket. The answer is the maximum `bucket[i+1].min - bucket[i].max` across adjacent non-empty buckets.
> - **HOW:** Edge cases: if all elements are equal, return 0. If n < 2, return 0.

> [!note]- Python Solution
> ```python
> def maximum_gap(nums: list[int]) -> int:
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
> Given two arrays `arr1` and `arr2`, sort `arr1` such that elements appearing in `arr2` come first in the order of `arr2`, followed by remaining elements in ascending order.

> [!info] Approach
> - **WHY:** Standard sorting can't directly encode a custom ordering defined by another array. We need a custom comparator key that maps `arr2` elements to their positions, and sends missing elements to the back.
> - **WHAT:** Build a rank map from `arr2`. Sort `arr1` using key: elements in `arr2` get rank `0..len(arr2)-1`, elements not in `arr2` get rank `len(arr2) + value` (ensuring ascending order after all arr2 elements).
> - **HOW:** `rank = {v: i for i, v in enumerate(arr2)}`. Sort with `key = lambda x: rank[x] if x in rank else len(arr2) + x`.

> [!note]- Python Solution
> ```python
> def relative_sort_array(arr1: list[int], arr2: list[int]) -> list[int]:
>     rank = {v: i for i, v in enumerate(arr2)}
>     def sort_key(x: int) -> tuple:
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
