---
tags: [coding, algorithms, divide-and-conquer]
topic: Divide and Conquer
difficulty: mixed
---

# Divide and Conquer — Problem Reference by Pattern

> [!info] First Principles
> D&C = split into *independent* subproblems of the same type, solve each recursively, combine results. Complexity is governed by the Master Theorem: T(n) = aT(n/b) + f(n). The key invariant: subproblems share *no* state — solving the left half never influences the right half. When subproblems overlap, use DP instead.

---

## Classic D&C

### Merge Sort (Implementation)

> [!example] Problem
> Sort an array in guaranteed O(n log n).

> [!info] Approach
> - **WHY:** Split into two independent halves; sorting each independently produces sorted sub-arrays whose combination (merge) is O(n). T(n) = 2T(n/2) + O(n) → O(n log n) by Master Theorem Case 2.
> - **WHAT:** Recursively split at midpoint; merge two sorted halves with two-pointer technique.
> - **HOW:** Base case len ≤ 1. Recurse left and right. Merge: advance the smaller of two pointers into result; append remainders. The combine step is the algorithm's core.

> [!note]- Python Solution
> ```python
> def merge_sort(nums: list[int]) -> list[int]:
>     if len(nums) <= 1:
>         return nums
>     mid = len(nums) // 2
>     left = merge_sort(nums[:mid])
>     right = merge_sort(nums[mid:])
>     return _merge(left, right)
> 
> def _merge(left: list[int], right: list[int]) -> list[int]:
>     result: list[int] = []
>     i = j = 0
>     while i < len(left) and j < len(right):
>         if left[i] <= right[j]:
>             result.append(left[i]); i += 1
>         else:
>             result.append(right[j]); j += 1
>     result.extend(left[i:])
>     result.extend(right[j:])
>     return result
> ```

> [!success] Complexity
> Time O(n log n) — all cases. Space O(n) merge buffer + O(log n) call stack.

> [!tip] Alternatives
> Bottom-up iterative merge sort — same complexity, O(log n) stack eliminated. TimSort (Python's built-in) — adaptive, O(n) on nearly-sorted data. Quicksort — O(n log n) average, O(n²) worst, O(1) extra space.

---

### Merge Two Sorted Lists

> [!example] Problem
> Merge two sorted linked lists into one sorted linked list.

> [!info] Approach
> - **WHY:** This is the fundamental combine step of merge sort — two sorted sequences, advance the smaller head. Recursive version directly mirrors D&C structure.
> - **WHAT:** Compare heads; smaller one becomes next node; recurse on its tail.
> - **HOW:** Base: if either list is None, return the other. Compare `l1.val` vs `l2.val`; attach smaller, recurse.

> [!note]- Python Solution
> ```python
> class ListNode:
>     def __init__(self, val=0, next=None):
>         self.val = val; self.next = next
> 
> def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
>     if not l1:
>         return l2
>     if not l2:
>         return l1
>     if l1.val <= l2.val:
>         l1.next = mergeTwoLists(l1.next, l2)
>         return l1
>     else:
>         l2.next = mergeTwoLists(l2.next, l1)
>         return l2
> ```

> [!success] Complexity
> Time O(m + n). Space O(m + n) recursion stack.

> [!tip] Alternatives
> Iterative with a dummy head — O(1) extra space. `heapq.merge` for multiple lists.

---

### Merge K Sorted Lists

> [!example] Problem
> Merge k sorted linked lists into one sorted linked list.

> [!info] Approach
> - **WHY:** Naive k-way merge is O(n·k). D&C pairwise merging: merge k lists in pairs, each pass reduces list count by 2, giving O(log k) passes × O(n) merge cost = O(n log k). This mirrors merge sort's structure at the list level.
> - **WHAT:** Repeatedly merge pairs of lists until one remains.
> - **HOW:** While len(lists) > 1: pop two, merge them, push result back. Or recurse: merge(lists[:mid]) + merge(lists[mid:]) as left/right.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def mergeKLists(lists: list) -> ListNode:
>     # Heap-based O(n log k) — same complexity as D&C, simpler code
>     heap: list = []
>     counter = 0
>     for node in lists:
>         if node:
>             heapq.heappush(heap, (node.val, counter, node))
>             counter += 1
>     dummy = ListNode(0)
>     curr = dummy
>     while heap:
>         val, _, node = heapq.heappop(heap)
>         curr.next = node
>         curr = curr.next
>         if node.next:
>             heapq.heappush(heap, (node.next.val, counter, node.next))
>             counter += 1
>     return dummy.next
> 
> def mergeKLists_dc(lists: list) -> ListNode:
>     # Pure D&C: O(n log k) via pairwise merging
>     if not lists:
>         return None
>     while len(lists) > 1:
>         merged = []
>         for i in range(0, len(lists), 2):
>             l1 = lists[i]
>             l2 = lists[i + 1] if i + 1 < len(lists) else None
>             merged.append(mergeTwoLists(l1, l2))
>         lists = merged
>     return lists[0]
> ```

> [!success] Complexity
> Time O(n log k) where n = total nodes. Space O(log k) for D&C recursion; O(k) for heap.

> [!tip] Alternatives
> Insert all nodes into a min-heap directly — O(n log n), not O(n log k). Sequential merge — O(n·k).

---

### Median of Two Sorted Arrays

> [!example] Problem
> Find the median of two sorted arrays of sizes m and n. Time complexity O(log(min(m,n))).

> [!info] Approach
> - **WHY:** A median partitions elements into equal halves. Binary search on the partition point of the smaller array: if partition `i` of `A` and `j = (m+n+1)//2 - i` of `B` satisfy `A[i-1] ≤ B[j]` and `B[j-1] ≤ A[i]`, we found the correct split.
> - **WHAT:** Binary search on shorter array's partition index; adjust based on cross-comparisons.
> - **HOW:** Ensure `A` is shorter. Binary search `lo` to `hi` (size of `A`). At midpoint `i`, compute `j`. If `A[i-1] > B[j]`, go left; if `B[j-1] > A[i]`, go right; else compute median from boundary values.

> [!note]- Python Solution
> ```python
> def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
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

### Pow(x, n) (Fast Exponentiation)

> [!example] Problem
> Compute `x^n` where n can be negative.

> [!info] Approach
> - **WHY:** Naive multiplication is O(n). D&C: `x^n = (x^(n/2))^2` halves the problem each level → O(log n). Optimal substructure: `pow(x, n/2)` is fully computed and reused.
> - **WHAT:** If `n` is even: `pow(x, n) = half * half`; if odd: `half * half * x`.
> - **HOW:** Handle `n < 0` by inverting `x` and negating `n`. Iterative with bit manipulation is cleaner than recursive.

> [!note]- Python Solution
> ```python
> def myPow(x: float, n: int) -> float:
>     if n < 0:
>         x, n = 1.0 / x, -n
>     result = 1.0
>     while n:
>         if n & 1:
>             result *= x
>         x *= x
>         n >>= 1
>     return result
> ```

> [!success] Complexity
> Time O(log n). Space O(1) iterative; O(log n) recursive.

> [!tip] Alternatives
> Recursive: `myPow(x, n//2)` squared ± one factor. Python's `x**n` uses fast exponentiation internally.

---

## QuickSelect

### Kth Largest Element in an Array

> [!example] Problem
> Find the kth largest element without full sort.

> [!info] Approach
> - **WHY:** Full sort is O(n log n). QuickSelect: after partitioning, the pivot is at its final sorted position. Only recurse into the half containing the kth position → T(n) = T(n/2) + O(n) = O(n) average.
> - **WHAT:** Partition around a pivot; if pivot index == target, return it; else recurse into the correct half.
> - **HOW:** Randomize pivot to avoid O(n²) worst case on sorted input. `k`th largest = `(n-k)`th index in 0-indexed sorted array.

> [!note]- Python Solution
> ```python
> import random
> 
> def findKthLargest(nums: list[int], k: int) -> int:
>     target = len(nums) - k  # k-th largest = (n-k)-th smallest
> 
>     def partition(lo: int, hi: int) -> int:
>         rand_idx = random.randint(lo, hi)
>         nums[rand_idx], nums[hi] = nums[hi], nums[rand_idx]
>         pivot, i = nums[hi], lo - 1
>         for j in range(lo, hi):
>             if nums[j] <= pivot:
>                 i += 1
>                 nums[i], nums[j] = nums[j], nums[i]
>         nums[i+1], nums[hi] = nums[hi], nums[i+1]
>         return i + 1
> 
>     def quickselect(lo: int, hi: int) -> int:
>         if lo == hi:
>             return nums[lo]
>         p = partition(lo, hi)
>         if p == target:
>             return nums[p]
>         elif p < target:
>             return quickselect(p + 1, hi)
>         else:
>             return quickselect(lo, p - 1)
> 
>     return quickselect(0, len(nums) - 1)
> ```

> [!success] Complexity
> Time O(n) average, O(n²) worst (randomization makes worst case negligibly rare). Space O(log n) average call depth.

> [!tip] Alternatives
> Min-heap of size k — O(n log k). Full sort — O(n log n). Median-of-medians — O(n) worst case but large constant factor.

---

### K Closest Points to Origin

> [!example] Problem
> Given a list of points, return the k closest to (0,0) by Euclidean distance.

> [!info] Approach
> - **WHY:** Full sort gives O(n log n). QuickSelect on squared distances: find the kth smallest squared distance, then take all points at distance ≤ that value.
> - **WHAT:** Apply QuickSelect on `points` sorted by `x²+y²`; return points at indices `0..k-1` after selection.
> - **HOW:** Same partition logic; compare by `dist(p) = p[0]**2 + p[1]**2`. After QuickSelect, `points[:k]` are the answer.

> [!note]- Python Solution
> ```python
> def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
>     def dist(p: list[int]) -> int:
>         return p[0]**2 + p[1]**2
> 
>     def partition(lo: int, hi: int) -> int:
>         rand_idx = random.randint(lo, hi)
>         points[rand_idx], points[hi] = points[hi], points[rand_idx]
>         pivot_d, i = dist(points[hi]), lo - 1
>         for j in range(lo, hi):
>             if dist(points[j]) <= pivot_d:
>                 i += 1
>                 points[i], points[j] = points[j], points[i]
>         points[i+1], points[hi] = points[hi], points[i+1]
>         return i + 1
> 
>     lo, hi = 0, len(points) - 1
>     while lo < hi:
>         p = partition(lo, hi)
>         if p < k:
>             lo = p + 1
>         elif p > k:
>             hi = p - 1
>         else:
>             break
>     return points[:k]
> ```

> [!success] Complexity
> Time O(n) average. Space O(log n) call depth.

> [!tip] Alternatives
> Max-heap of size k: O(n log k). Full sort: O(n log n). `heapq.nsmallest(k, points, key=dist)` in Python.

---

### Top K Frequent Elements

> [!example] Problem
> Return the k most frequent elements in an array.

> [!info] Approach
> - **WHY:** Build frequency map in O(n); then find k largest by frequency using QuickSelect — O(n) average instead of O(n log n) sorting.
> - **WHAT:** Count frequencies, build unique-element list, QuickSelect on frequency values.
> - **HOW:** `freq = Counter(nums)`. Run QuickSelect on `list(freq.keys())` comparing by `freq[key]`. Target index = `n - k`.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def topKFrequent(nums: list[int], k: int) -> list[int]:
>     freq = Counter(nums)
>     unique = list(freq.keys())
>     n = len(unique)
>     target = n - k
> 
>     def partition(lo: int, hi: int) -> int:
>         rand_idx = random.randint(lo, hi)
>         unique[rand_idx], unique[hi] = unique[hi], unique[rand_idx]
>         pivot_f, i = freq[unique[hi]], lo - 1
>         for j in range(lo, hi):
>             if freq[unique[j]] <= pivot_f:
>                 i += 1
>                 unique[i], unique[j] = unique[j], unique[i]
>         unique[i+1], unique[hi] = unique[hi], unique[i+1]
>         return i + 1
> 
>     lo, hi = 0, n - 1
>     while lo < hi:
>         p = partition(lo, hi)
>         if p < target:
>             lo = p + 1
>         elif p > target:
>             hi = p - 1
>         else:
>             break
>     return unique[target:]
> ```

> [!success] Complexity
> Time O(n) average for QuickSelect after O(n) frequency count. Space O(n).

> [!tip] Alternatives
> Bucket sort on frequency — O(n) time and space, deterministic. `Counter.most_common(k)` — O(n log k) using a heap internally.

---

## Merge Sort Variants (D&C with Counting)

### Count of Smaller Numbers After Self

> [!example] Problem
> For each element, count how many elements to its right are smaller.

> [!info] Approach
> - **WHY:** During merge sort's combine step, when an element from the right half is merged before an element in the left half, it means all remaining left-half elements are larger — the count of such "right-picks" equals the count of smaller elements to the right.
> - **WHAT:** Augmented merge sort on `(value, original_index)` pairs. When a right element is placed, add the count of remaining left elements to all pending left elements' counts.
> - **HOW:** Track `right_picked` count during merge. Each time a right element is chosen over remaining `left[i:]` elements, increment `counts[left[i].index]`.

> [!note]- Python Solution
> ```python
> def countSmaller(nums: list[int]) -> list[int]:
>     n = len(nums)
>     counts = [0] * n
>     indexed = list(enumerate(nums))  # (original_index, value)
> 
>     def merge_sort(arr: list) -> list:
>         if len(arr) <= 1:
>             return arr
>         mid = len(arr) // 2
>         left = merge_sort(arr[:mid])
>         right = merge_sort(arr[mid:])
>         return merge_count(left, right)
> 
>     def merge_count(left: list, right: list) -> list:
>         result = []
>         i = j = right_used = 0
>         while i < len(left) and j < len(right):
>             if left[i][1] <= right[j][1]:
>                 counts[left[i][0]] += right_used
>                 result.append(left[i]); i += 1
>             else:
>                 right_used += 1
>                 result.append(right[j]); j += 1
>         while i < len(left):
>             counts[left[i][0]] += right_used
>             result.append(left[i]); i += 1
>         result.extend(right[j:])
>         return result
> 
>     merge_sort(indexed)
>     return counts
> ```

> [!success] Complexity
> Time O(n log n). Space O(n) for merge buffer and counts.

> [!tip] Alternatives
> Binary Indexed Tree / Fenwick Tree on coordinate-compressed values — O(n log n), same asymptotic. Segment tree for range count queries.

---

### Reverse Pairs

> [!example] Problem
> Count pairs `(i, j)` where `i < j` and `nums[i] > 2 * nums[j]`.

> [!info] Approach
> - **WHY:** Similar to counting inversions but with a scaled inequality. During merge, for each left element, count how many right elements satisfy `nums[i] > 2 * nums[j]` before the two halves are merged.
> - **WHAT:** Separate the counting step from the merge step — count cross-half pairs first, then merge normally.
> - **HOW:** Two-pointer count: for each `left[i]`, advance `j` while `left[i] > 2 * right[j]`; add `j` to total. Then perform standard merge.

> [!note]- Python Solution
> ```python
> def reversePairs(nums: list[int]) -> int:
>     total = [0]
> 
>     def merge_sort(arr: list[int]) -> list[int]:
>         if len(arr) <= 1:
>             return arr
>         mid = len(arr) // 2
>         left = merge_sort(arr[:mid])
>         right = merge_sort(arr[mid:])
>         # Count pairs
>         j = 0
>         for val in left:
>             while j < len(right) and val > 2 * right[j]:
>                 j += 1
>             total[0] += j
>         # Standard merge
>         return _merge(left, right)
> 
>     merge_sort(nums)
>     return total[0]
> ```

> [!success] Complexity
> Time O(n log n). Space O(n).

> [!tip] Alternatives
> Merge Sort with BIT. Note: counting step and merge step must be separate because merging would sort the arrays before counting completes.

---

### Count of Range Sum

> [!example] Problem
> Count subarrays with sum in `[lower, upper]`.

> [!info] Approach
> - **WHY:** Subarray sum = `prefix[j] - prefix[i]`. Need count of pairs `(i, j)` with `lower ≤ prefix[j] - prefix[i] ≤ upper`. During merge sort on prefix sums, count valid cross-half pairs.
> - **WHAT:** Augmented merge sort on prefix sums array. Use two sliding pointers during merge to count.
> - **HOW:** For each element in left half `L[i]`, find window `[lo, hi)` in right half where `lower ≤ R[k] - L[i] ≤ upper`. Two pointers maintain this window as `i` advances.

> [!note]- Python Solution
> ```python
> def countRangeSum(nums: list[int], lower: int, upper: int) -> int:
>     prefix = [0]
>     for n in nums:
>         prefix.append(prefix[-1] + n)
> 
>     total = [0]
> 
>     def merge_sort(arr: list[int]) -> list[int]:
>         if len(arr) <= 1:
>             return arr
>         mid = len(arr) // 2
>         left = merge_sort(arr[:mid])
>         right = merge_sort(arr[mid:])
>         # Count pairs
>         lo = hi = 0
>         for val in left:
>             while lo < len(right) and right[lo] - val < lower:
>                 lo += 1
>             while hi < len(right) and right[hi] - val <= upper:
>                 hi += 1
>             total[0] += hi - lo
>         return _merge(left, right)
> 
>     merge_sort(prefix)
>     return total[0]
> ```

> [!success] Complexity
> Time O(n log n). Space O(n).

> [!tip] Alternatives
> BIT / segment tree on coordinate-compressed prefix sums — O(n log n) but requires coordinate compression.

---

### Majority Element (D&C Approach)

> [!example] Problem
> Find the element appearing more than n/2 times. Guaranteed to exist.

> [!info] Approach
> - **WHY:** If an element is majority in the full array, it must be the majority in at least one half. D&C: find majority of left and right; if they agree, that's the answer; if not, verify each candidate against the full range.
> - **WHAT:** Recurse to find candidate in each half; verify both in current range.
> - **HOW:** Base: single element is its own majority. Count occurrences of left and right candidates in the full subarray; return whichever exceeds half.

> [!note]- Python Solution
> ```python
> def majorityElement(nums: list[int]) -> int:
>     def majority_range(lo: int, hi: int) -> int:
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

### Majority Element II

> [!example] Problem
> Find all elements appearing more than n/3 times (at most 2 such elements).

> [!info] Approach
> - **WHY:** At most 2 candidates can exceed n/3. Boyer-Moore extended to two candidates; then verify both in a second pass.
> - **WHAT:** Two-candidate Boyer-Moore voting; verify counts in second pass.
> - **HOW:** Maintain two `(candidate, count)` pairs. On each element: if matches candidate, increment; else decrement both; if count reaches 0, replace. Final verification pass confirms actual frequency.

> [!note]- Python Solution
> ```python
> def majorityElement(nums: list[int]) -> list[int]:
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
>             cnt1 -= 1; cnt2 -= 1
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
> Find the maximum difference between successive elements in a sorted form of the array.

> [!info] Approach
> - **WHY:** Sorting gives O(n log n). Bucket/radix approach: by pigeonhole, the maximum gap must span at least one empty bucket. Place elements into n-1 buckets of size `(max-min)/(n-1)`. Max gap = max over consecutive non-empty buckets.
> - **WHAT:** Bucket sort on the value range; track min/max within each bucket; scan gaps between consecutive non-empty buckets.
> - **HOW:** Bucket size = `ceil((max_val - min_val) / (n - 1))`. For each element, assign to bucket index. Track `(bucket_min, bucket_max)`. Answer = `max(next_min - curr_max)` across adjacent filled buckets.

> [!note]- Python Solution
> ```python
> import math
> 
> def maximumGap(nums: list[int]) -> int:
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

### Super Pow (Modular Exponentiation)

> [!example] Problem
> Compute `a^b mod 1337` where `b` is a very large integer represented as an array.

> [!info] Approach
> - **WHY:** `b` is too large to compute directly. Key identity: `a^[d1,d2,...,dk] = (a^[d1,...,dk-1])^10 * a^dk`. Process exponent digit by digit using D&C recursion.
> - **WHAT:** Recursive reduction: `pow(a, b) = pow(pow(a, b[:-1]), 10) * pow(a, b[-1])`.
> - **HOW:** Base case: `b` is empty → return 1. At each step, multiply `pow(pow(a, b[:-1]), 10, mod) * pow(a, b[-1], mod)`.

> [!note]- Python Solution
> ```python
> def superPow(a: int, b: list[int]) -> int:
>     MOD = 1337
> 
>     def fast_pow(base: int, exp: int) -> int:
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

### Matrix Exponentiation (Fibonacci in O(log n))

> [!example] Problem
> Compute Fibonacci(n) in O(log n) using matrix exponentiation.

> [!info] Approach
> - **WHY:** Fibonacci satisfies `[F(n+1), F(n)] = M * [F(n), F(n-1)]` where `M = [[1,1],[1,0]]`. Therefore `M^n * [1,0]^T = [F(n+1), F(n)]^T`. Fast matrix exponentiation computes `M^n` in O(log n) matrix multiplications.
> - **WHAT:** Apply fast exponentiation to the 2×2 matrix `M`. Each multiplication is O(1) for fixed-size matrix.
> - **HOW:** Same repeated-squaring loop as scalar fast pow; replace scalar mul with matrix mul.

> [!note]- Python Solution
> ```python
> def fibonacci_matrix(n: int, mod: int = 10**9 + 7) -> int:
>     if n <= 1:
>         return n
> 
>     def mat_mul(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
>         return [
>             [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % mod,
>              (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % mod],
>             [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % mod,
>              (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % mod]
>         ]
> 
>     def mat_pow(M: list[list[int]], p: int) -> list[list[int]]:
>         result = [[1, 0], [0, 1]]  # identity
>         while p:
>             if p & 1:
>                 result = mat_mul(result, M)
>             M = mat_mul(M, M)
>             p >>= 1
>         return result
> 
>     M = [[1, 1], [1, 0]]
>     return mat_pow(M, n)[0][1]
> ```

> [!success] Complexity
> Time O(log n) matrix multiplications × O(1) each = O(log n). Space O(1).

> [!tip] Alternatives
> Linear recurrence solver for arbitrary k-th order recurrences (same matrix technique). `O(n)` iterative DP for most interview purposes.

---

## Geometric D&C

### Closest Pair of Points

> [!example] Problem
> Find the minimum Euclidean distance between any two points in a 2D set. Achieve better than O(n²).

> [!info] Approach
> - **WHY:** Brute force checks all n(n-1)/2 pairs O(n²). D&C: minimum distance in each half is found recursively. Only points within a vertical strip of width `2δ` (δ = min of two halves' answers) can improve the global minimum. By geometric packing, each strip point has at most 7 candidates in the strip — so strip scan is O(n).
> - **WHAT:** Sort by x. Split at midpoint x-coordinate. Recurse each half. Check strip candidates within `δ` of the dividing line.
> - **HOW:** Sort strip points by y. For each strip point, check at most the next 7 points (geometric argument: in a δ×2δ rectangle, at most 8 points with pairwise distance ≥ δ).

> [!note]- Python Solution
> ```python
> import math
> 
> def closestPair(points: list[tuple[float, float]]) -> float:
>     pts = sorted(points)  # sort by x
> 
>     def dist(p1: tuple, p2: tuple) -> float:
>         return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
> 
>     def rec(arr: list[tuple]) -> float:
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

## See Also

[[sorting]] | [[recursion]] | [[binary-search]] | [[heap]]
