---
tags: [coding, data-structures, array]
topic: array
difficulty: mixed
---
# Array Problems — Deep Dive

## What this covers

> [!abstract] In this file
> **Covers:** Worked array problems grouped by technique: two pointers, sliding window, Kadane, partitioning, Boyer-Moore, difference array, prefix sum.
> **You'll be able to:** Solve the T1 array set cold in ≤25 min each.
> **Prereqs:** Array lecture · **Pair with:** [Array lecture](../../01-data-structures/01-array.md) · **Time:** 4–6 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/l3-google-roadmap.md#tier-legend))

**Sections:** [Two Pointers](#two-pointers) · [Sliding Window](#sliding-window) · [Kadane's Algorithm](#kadanes-algorithm) · [Dutch National Flag / Partitioning](#dutch-national-flag--partitioning) · [Boyer-Moore Voting](#boyer-moore-voting) · [Difference Array](#difference-array) · [Miscellaneous Array Techniques](#miscellaneous-array-techniques) · [Matrix](#matrix) · [Prefix Sum](#prefix-sum)

> [!tip] If you only have 20 minutes
> **Do these first:** [Two Sum (hash map variant)](#two-sum-hash-map-variant--t1) · [Best Time to Buy and Sell Stock](#best-time-to-buy-and-sell-stock--t2) · [Maximum Subarray](#maximum-subarray--t2) · [Product of Array Except Self](#product-of-array-except-self--t2) · [Merge Intervals](#merge-intervals-lc-56--t2) · [Insert Interval](#insert-interval-lc-57--t2) · [Sort Colors](#sort-colors--t1) · [Next Permutation](#next-permutation--t2) · [Rotate Image](#rotate-image-lc-48)
> **Template:** Kadane: `cur = max(x, cur + x); best = max(best, cur)`.
> **Template:** Prefix/suffix pass: left products into `ans`, then multiply by a running right product — O(1) extra space.
> **Gotchas:** All-negative input for Kadane (init with `a[0]`, not 0) · in-place matrix ops: transpose then reverse rows · Next Permutation: find pivot from the right, swap with the next larger, **reverse** the suffix · difference arrays for range-add.

---

## Two Pointers

---

### Two Sum (sorted variant) `⚡ T1`

> [!example] Problem
> Same problem as [Two Sum](02-hashing.md#two-sum--t1) — this section covers the alternative approach only.

> [!info] Approach
> **Two Pointers on sorted array.** The array is sorted — we can exploit this. A pair either has too-small a sum (advance left) or too-large a sum (advance right). No pair is missed because every skip is provably invalid. Two pointers at opposite ends converging inward based on sum comparison. `l=0, r=n-1`. If `numbers[l] + numbers[r] == target`, done. If sum < target, `l++` (we need larger). If sum > target, `r--` (we need smaller). The sorted invariant guarantees we never skip valid pairs.

> [!note]- Python Solution
> ```python
> def two_sum_sorted(numbers, target):
>     l, r = 0, len(numbers) - 1
>     while l < r:
>         s = numbers[l] + numbers[r]
>         if s == target:
>             return [l + 1, r + 1]  # problem wants 1-based indices
>         elif s < target:
>             l += 1
>         else:
>             r -= 1
>     return []
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Edge cases
> - The prompt is already sorted and 1-indexed, so the returned indices must be shifted by `+1`.
> - The original LeetCode-style prompt guarantees exactly one solution; in a no-solution variant, follow the interviewer’s output convention explicitly.

> [!tip] Alternatives
> - Hash map complement lookup: O(n) time, O(n) space. Works on unsorted arrays; doesn't exploit sorted order.
> - Binary search for complement: O(n log n). Worse than two pointers — use two pointers when sorted.

---

### 3Sum `⚡ T1`

> Full walkthrough: [3Sum (LC 15)](../algorithms/03-two-pointers.md#3sum-lc-15--t1).

---

### 3Sum Closest `⚡ T1`

> Full walkthrough: [3Sum Closest (LC 16)](../algorithms/03-two-pointers.md#3sum-closest-lc-16--t1).

---

### 4Sum `⚡ T1`

> Full walkthrough: [4Sum (LC 18)](../algorithms/03-two-pointers.md#4sum-lc-18--t1).

---

### Container with Most Water `⚡ T1`

> Full walkthrough: [Container With Most Water (LC 11)](../algorithms/03-two-pointers.md#container-with-most-water-lc-11--t1).

---

### Trapping Rain Water `⚡ T1`

> Full walkthrough: [Trapping Rain Water (LC 42)](../algorithms/03-two-pointers.md#trapping-rain-water-lc-42--t1).

---

### Remove Duplicates from Sorted Array `⚡ T1`

> Full walkthrough: [Remove Duplicates from Sorted Array (LC 26)](../algorithms/03-two-pointers.md#remove-duplicates-from-sorted-array-lc-26--t1).

---

### Next Permutation `🎯 T2`

> [!example] Problem
> A permutation of an array of integers is an arrangement of its members into a sequence or linear order.
> The next permutation of an array of integers is the next lexicographically greater permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the next permutation of that array is the permutation that follows it in the sorted container. If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order).
> Given an array of integers nums, find the next permutation of nums.
> The replacement must be in place and use only constant extra memory.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3]
> Output: [1,3,2]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,1]
> Output: [1,2,3]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,1,5]
> Output: [1,5,1]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 100
> - 0 <= nums[i] <= 100

> [!info] Approach
> **Three-step: find rightmost descent, swap, reverse suffix.** A permutation is "next" if we increment the rightmost possible position. We find the rightmost "dip" — a position where the element is smaller than something to its right. Three-step algorithm: find rightmost descent, swap with next-larger suffix element, reverse the suffix.

> 1. Scan right-to-left to find index `i` where `nums[i] < nums[i+1]` (rightmost ascending pair from the right).
> 2. If none found, the whole array is descending — just reverse it.
> 3. From the right, find the smallest element greater than `nums[i]`; swap them.
> 4. Reverse `nums[i+1:]` to get the smallest permutation of the suffix.

> [!note]- Python Solution
> ```python
> def next_permutation(nums):
>     n = len(nums)
>     i = n - 2
>     while i >= 0 and nums[i] >= nums[i + 1]:
>         i -= 1
>     if i >= 0:
>         j = n - 1
>         while nums[j] <= nums[i]:
>             j -= 1
>         nums[i], nums[j] = nums[j], nums[i]
>     # Reverse the suffix
>     l, r = i + 1, n - 1
>     while l < r:
>         nums[l], nums[r] = nums[r], nums[l]
>         l += 1
>         r -= 1
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Generate all permutations and find the next: O(n! × n). Completely unacceptable.
> - The suffix after the swap point is guaranteed to be descending (we found the rightmost descent), so reversing it is always correct.

---

## Sliding Window

---

### Max Consecutive Ones III `⚡ T1`

> Full walkthrough: [Max Consecutive Ones III (LC 1004)](../algorithms/04-sliding-window.md#max-consecutive-ones-iii-lc-1004--t1).

---

### Subarrays with K Different Integers `⚡ T1`

> Full walkthrough: [Subarrays with K Different Integers (LC 992)](../algorithms/04-sliding-window.md#subarrays-with-k-different-integers-lc-992--t1).

---

### Continuous Subarray Sum

> [!example] Problem
> Given an integer array nums and an integer k, return true if nums has a good subarray or false otherwise.
> A good subarray is a subarray where:
> Note that
> 
> **Example 1:**
> ```
> Input: nums = [23,2,4,6,7], k = 6
> Output: true
> Explanation: [2, 4] is a continuous subarray of size 2 whose elements sum up to 6.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [23,2,6,4,7], k = 6
> Output: true
> Explanation: [23, 2, 6, 4, 7] is an continuous subarray of size 5 whose elements sum up to 42.
> 42 is a multiple of 6 because 42 = 7 * 6 and 7 is an integer.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [23,2,6,4,7], k = 13
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - 0 <= nums[i] <= 10^9
> - 0 <= sum(nums[i]) <= 2^{31} - 1
> - 1 <= k <= 2^{31} - 1

> [!info] Approach
> **Prefix modulo — first-occurrence index map.** Same modulo insight as above. `sum(l..r) % k == 0` iff `prefix[r] % k == prefix[l-1] % k`. Additionally require length ≥ 2, meaning indices must be at least 2 apart. Map `remainder → first index` seen. On seeing the same remainder again, check index gap ≥ 2. Seed `seen[0] = -1` (empty prefix at index -1). For each index `i`, compute `rem`. If `rem in seen` and `i - seen[rem] >= 2`, return True. Otherwise, record `rem → i` only if not already present (want first occurrence).

> [!note]- Python Solution
> ```python
> def check_subarray_sum(nums, k):
>     seen = {0: -1}
>     running = 0
>     for i, x in enumerate(nums):
>         running += x
>         rem = running % k
>         if rem in seen:
>             if i - seen[rem] >= 2:
>                 return True
>         else:
>             seen[rem] = i
>     return False
> ```

> [!success] Complexity
> Time O(n), Space O(k).

> [!tip] Alternatives
> - Brute force O(n²): sum all subarrays. Too slow.
> - Do not overwrite `seen[rem]` — always keep the earliest index to maximize gap.

---

### Product of Array Except Self `🎯 T2`

> [!example] Problem
> Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].
> The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
> You must write an algorithm that runs in O(n) time and without using the division operation.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3,4]
> Output: [24,12,8,6]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [-1,1,0,-3,3]
> Output: [0,0,9,0,0]
> ```
> 
> **Constraints:**
> - 2 <= nums.length <= 10^5
> - -30 <= nums[i] <= 30
> - The input is generated such that answer[i] is guaranteed to fit in a 32-bit integer.

> [!tip] Recognize · Gotcha
> **Signal:** Prefix/suffix without division · **Gotcha:** **Zeros** — one zero → all zero except that index; two zeros → all zero. **No division** constraint.

> [!info] Approach
> **Two-pass left/right product accumulation.** Division is disallowed (and breaks on zeros). We can compute left-product prefix and right-product suffix. Two-pass: first build left products into output, then multiply by right products on a second right-to-left pass using a running variable. Pass 1: `output[i] = product of nums[0..i-1]`. Pass 2: maintain `right = 1`, scan right to left, multiply `output[i] *= right`, then `right *= nums[i]`.

> [!note]- Python Solution
> ```python
> def product_except_self(nums):
>     n = len(nums)
>     output = [1] * n
>     # Left products
>     for i in range(1, n):
>         output[i] = output[i - 1] * nums[i - 1]
>     # Multiply by right products in-place
>     right = 1
>     for i in range(n - 1, -1, -1):
>         output[i] *= right
>         right *= nums[i]
>     return output
> ```

> [!success] Complexity
> Time O(n), Space O(1) extra (output array not counted).

> [!tip] Alternatives
> - Division approach with zero-count tracking: handles zeros but violates problem constraint.
> - Separate left/right arrays: O(n) space. Same logic, less elegant.

---

## Kadane's Algorithm

---

### Maximum Subarray `🎯 T2`

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

> [!tip] Recognize · Gotcha
> **Signal:** "max contiguous sum" · **Gotcha:** All-negative input → init with `nums[0]`, not 0

> [!info] Approach
> **Kadane's algorithm — local reset on negative prefix.** At each position, either start a new subarray here or extend the current one — whichever is larger. The decision is local and optimal. Kadane's algorithm: `cur = max(nums[i], cur + nums[i])`. This captures "reset if current prefix hurts". Initialize `cur = best = nums[0]` (handles all-negative case). For each subsequent element: `cur = max(x, cur + x)`. Update `best = max(best, cur)`.

> [!note]- Python Solution
> ```python
> def max_subarray(nums):
>     cur = best = nums[0]
>     for x in nums[1:]:
>         cur = max(x, cur + x)
>         best = max(best, cur)
>     return best
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - D&C: O(n log n). Correct but suboptimal.
> - DP table O(n) space: `dp[i] = max subarray ending at i`. Same logic, more memory.
> - Critical: never initialize to 0. `cur = 0` returns 0 for all-negative arrays — wrong.

---

### Maximum Circular Subarray Sum (Maximum Sum Circular Subarray)

> [!example] Problem
> Find the maximum subarray sum in a circular array (the subarray may wrap around).

> [!info] Approach
> **Kadane's max + Kadane's min on total sum.** Two cases: (1) max subarray is non-wrapping — standard Kadane's; (2) it wraps around the ends. The wrap-around case is equivalent to the total sum minus the minimum subarray (the middle we exclude). Run Kadane's twice: once for max subarray, once for min subarray. Answer = max(kadane_max, total - kadane_min). Edge case: if all elements are negative, `total - kadane_min` = 0 (the empty subarray), which is wrong. In this case, return `kadane_max`.

> [!note]- Python Solution
> ```python
> def max_subarray_circular(nums):
>     total = sum(nums)
>     # Kadane's for max
>     cur_max = best_max = nums[0]
>     for x in nums[1:]:
>         cur_max = max(x, cur_max + x)
>         best_max = max(best_max, cur_max)
>     # Kadane's for min
>     cur_min = best_min = nums[0]
>     for x in nums[1:]:
>         cur_min = min(x, cur_min + x)
>         best_min = min(best_min, cur_min)
>     # If all negative, total - best_min = 0, use best_max
>     if total == best_min:
>         return best_max
>     return max(best_max, total - best_min)
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Concatenate array with itself and run sliding window max of length n: O(n), O(n) space. More complex.

---

## Dutch National Flag / Partitioning

---

### Sort Colors `⚡ T1`

> Full walkthrough: [Sort Colors (LC 75)](../algorithms/03-two-pointers.md#sort-colors-lc-75--t1).

---

### Find All Numbers Disappeared in an Array

> [!example] Problem
> Given an array nums of n integers where nums[i] is in the range [1, n], return an array of all the integers in the range [1, n] that do not appear in nums.
> 
> **Example 1:**
> ```
> Input: nums = [4,3,2,7,8,2,3,1]
> Output: [5,6]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,1]
> Output: [2]
> ```
> 
> **Constraints:**
> - n == nums.length
> - 1 <= n <= 10^5
> - 1 <= nums[i] <= n

> [!info] Approach
> **Sign-flip in-place visited marking.** We need to mark visited values without extra space. The array indices themselves serve as a hash table. Use sign-flip as an in-place "visited" marker. Index `i` being negative means value `i+1` has been seen. For each value `x = abs(nums[i])`, negate `nums[x-1]`. After marking, collect all indices where value is still positive — those indices +1 are the missing values.

> [!note]- Python Solution
> ```python
> def find_disappeared_numbers(nums):
>     for x in nums:
>         idx = abs(x) - 1
>         if nums[idx] > 0:
>             nums[idx] = -nums[idx]
>     return [i + 1 for i, v in enumerate(nums) if v > 0]
> ```

> [!success] Complexity
> Time O(n), Space O(1) extra.

> [!tip] Alternatives
> - Use a set of seen values, return `set(range(1,n+1)) - seen`: O(n) time, O(n) space.
> - Sort and scan: O(n log n) time. Too slow.

---

## Boyer-Moore Voting

---

### Majority Element `🎯 T2`

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
> **Boyer-Moore voting — cancellation argument.** Hash map O(n) space, sorting O(n log n). Boyer-Moore pairs different elements and cancels them. The majority element (count > n/2) outlasts all others combined. Maintain `candidate` and `count`. If count hits 0, pick current element as new candidate. Increment on same, decrement on different. This works because: imagine each "non-candidate" vote cancels one "candidate" vote. Since majority has > n/2 votes, it survives after all cancellations.

> [!note]- Python Solution
> ```python
> def majority_element(nums):
>     candidate = nums[0]
>     count = 1
>     for x in nums[1:]:
>         if count == 0:
>             candidate = x
>             count = 1
>         elif x == candidate:
>             count += 1
>         else:
>             count -= 1
>     return candidate
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Hash map counting: O(n) time, O(n) space. Simpler; use when majority not guaranteed (need to verify).
> - Sorted middle element `nums[n//2]` after sort: O(n log n). Majority must occupy the middle.
> - When majority not guaranteed: add a second verification pass `nums.count(candidate) > n // 2`.

---

### Find the Duplicate Number `🎯 T2`

> [!example] Problem
> Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.
> There is only one repeated number in nums, return this repeated number.
> You must solve the problem without modifying the array nums and using only constant extra space.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,4,2,2]
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,1,3,4,2]
> Output: 3
> ```
> 
> **Example 3:**
> ```
> Input: nums = [3,3,3,3,3]
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= n <= 10^5
> - nums.length == n + 1
> - 1 <= nums[i] <= n
> - All the integers in nums appear only once except for precisely one integer which appears two or more times.

> [!info] Approach
> **Floyd's cycle detection on implicit linked list.** Values in [1, n] can be treated as "next pointers" — `nums[i]` says "go to index nums[i]". Since multiple indices point to the same value, a cycle must exist. The duplicate is the cycle entry. Floyd's cycle detection on the implicit linked list defined by `next(i) = nums[i]`. Start from index 0 (guaranteed outside cycle since all values ≥ 1). Phase 1 — slow = nums[slow], fast = nums[nums[fast]] until they meet (inside cycle). Phase 2 — reset slow = nums[0] (the start), advance both at speed 1; they meet at the cycle entry = duplicate.

> [!note]- Python Solution
> ```python
> def find_duplicate(nums):
>     # Phase 1: find intersection inside cycle
>     slow = fast = nums[0]
>     while True:
>         slow = nums[slow]
>         fast = nums[nums[fast]]
>         if slow == fast:
>             break
>     # Phase 2: find cycle entry (the duplicate)
>     slow = nums[0]
>     while slow != fast:
>         slow = nums[slow]
>         fast = nums[fast]
>     return slow
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Sort and scan for adjacent equal elements: O(n log n), modifies array (if in-place sort).
> - Sign-flip marking: O(n) time, O(1) space but modifies the array — violates constraint.
> - Binary search on value range: O(n log n) time, O(1) space. Count elements ≤ mid; if > mid, duplicate is in [1..mid] by pigeonhole.

---

## Difference Array

---

### Difference Array Pattern

> When you need to apply many range updates `[l, r] += val` and then query final values, the naive approach is O(n) per update — O(n × q) total for q updates. Difference array makes each update O(1) and reconstruction O(n), giving O(q + n) overall. Build `diff[]` where `diff[i] = arr[i] - arr[i-1]`. To add `val` to range `[l, r]`: `diff[l] += val`, `diff[r+1] -= val`. Reconstruct prefix sum to get the final array. Initialize `diff = [0] * (n + 1)`. For each update `(l, r, val)`: `diff[l] += val; diff[r+1] -= val`. After all updates, compute prefix sum of `diff` to get the result array.

---

### Car Pooling `🎯 T2`

> [!example] Problem
> There is a car with capacity empty seats. The vehicle only drives east (i.e., it cannot turn around and drive west).
> You are given the integer capacity and an array trips where trips[i] = [numPassengersi, fromi, toi] indicates that the ith trip has numPassengersi passengers and the locations to pick them up and drop them off are fromi and toi respectively. The locations are given as the number of kilometers due east from the car's initial location.
> Return true if it is possible to pick up and drop off all passengers for all the given trips, or false otherwise.
> 
> **Example 1:**
> ```
> Input: trips = [[2,1,5],[3,3,7]], capacity = 4
> Output: false
> ```
> 
> **Example 2:**
> ```
> Input: trips = [[2,1,5],[3,3,7]], capacity = 5
> Output: true
> ```
> 
> **Constraints:**
> - 1 <= trips.length <= 1000
> - trips[i].length == 3
> - 1 <= numPassengersi <= 100
> - 0 <= fromi < toi <= 1000
> - 1 <= capacity <= 10^5

> [!info] Approach
> Each trip is a range update — passengers board at `from` and alight at `to`. We need to check the running passenger count never exceeds `capacity` at any stop. Difference array on stops (up to 1000 stops). `diff[from] += numPassengers`, `diff[to] -= numPassengers` (drop-off happens at `to`, so the open interval is `[from, to)`). Build `diff[0..1001]`. For each trip: `diff[from] += num; diff[to] -= num`. Reconstruct prefix sum; if any prefix sum > `capacity`, return False.

> [!note]- Python Solution
> ```python
> def car_pooling(trips, capacity):
>     diff = [0] * 1001
>     for num, frm, to in trips:
>         diff[frm] += num
>         diff[to] -= num   # passengers leave at 'to', not 'to+1'
>     running = 0
>     for d in diff:
>         running += d
>         if running > capacity:
>             return False
>     return True
> ```

> [!success] Complexity
> Time O(n + S) where n = number of trips, S = number of stops (≤ 1001). Space O(S).

> [!tip] Alternatives
> - Sort events by time: O(n log n). Process (stop, +num) and (stop, -num) events in order. Same result, slightly higher constant.
> - Brute force simulation: O(n × S). Too slow for large inputs.

---

### Corporate Flight Bookings

> [!example] Problem
> There are n flights that are labeled from 1 to n.
> You are given an array of flight bookings bookings, where bookings[i] = [firsti, lasti, seatsi] represents a booking for flights firsti through lasti (inclusive) with seatsi seats reserved for each flight in the range.
> Return an array answer of length n, where answer[i] is the total number of seats reserved for flight i.
> 
> **Example 1:**
> ```
> Input: bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5
> Output: [10,55,45,25,25]
> Explanation:
> Flight labels:        1   2   3   4   5
> Booking 1 reserved:  10  10
> Booking 2 reserved:      20  20
> Booking 3 reserved:      25  25  25  25
> Total seats:         10  55  45  25  25
> Hence, answer = [10,55,45,25,25]
> ```
> 
> **Example 2:**
> ```
> Input: bookings = [[1,2,10],[2,2,15]], n = 2
> Output: [10,25]
> Explanation:
> Flight labels:        1   2
> Booking 1 reserved:  10  10
> Booking 2 reserved:      15
> Total seats:         10  25
> Hence, answer = [10,25]
> ```
> 
> **Constraints:**
> - 1 <= n <= 2 * 10^4
> - 1 <= bookings.length <= 2 * 10^4
> - bookings[i].length == 3
> - 1 <= firsti <= lasti <= n
> - 1 <= seatsi <= 10^4

> [!info] Approach
> Each booking is a range update over flight indices. Naively applying each booking to every flight in range is O(n × b). Difference array reduces this to O(b + n). Difference array over 1-indexed flights. For booking `[first, last, seats]`: `diff[first] += seats; diff[last+1] -= seats`. Prefix sum of diff gives total bookings per flight. Build `diff[0..n+1]`. For each booking: `diff[first] += seats; diff[last+1] -= seats`. Prefix sum of `diff[1..n]` is the answer.

> [!note]- Python Solution
> ```python
> def corp_flight_bookings(bookings, n):
>     diff = [0] * (n + 2)
>     for first, last, seats in bookings:
>         diff[first] += seats
>         diff[last + 1] -= seats
>     result = []
>     running = 0
>     for i in range(1, n + 1):
>         running += diff[i]
>         result.append(running)
>     return result
> ```

> [!success] Complexity
> Time O(b + n) where b = number of bookings. Space O(n).

> [!tip] Alternatives
> - Brute force: for each booking, increment each flight in range — O(b × n). Too slow.
> - Segment tree with lazy propagation: O((b + n) log n). Overkill; difference array is optimal for this offline batch-update pattern.

---

### Range Addition

> [!example] Problem
> You are given an integer `length` and an array `updates` where `updates[i] = [startIdx_i, endIdx_i, inc_i]`.
> 
> You have an array `arr` of length `length` with all zeros, and you have some operation to apply on `arr`. In the `i^th` operation, you should increment all the elements `arr[startIdx_i], arr[startIdx_i + 1], ..., arr[endIdx_i]` by `inc_i`.
> 
> Return `arr` *after applying all the* `updates`.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** length = 5, updates = [[1,3,2],[2,4,3],[0,2,-2]]
> **Output:** [-2,0,3,5,3]
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** length = 10, updates = [[2,4,6],[5,6,8],[1,9,-4]]
> **Output:** [0,-4,2,2,2,4,4,-4,-4,-4]
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= length <= 10^5`
> 	
> - `0 <= updates.length <= 10^4`
> 	
> - `0 <= startIdx_i <= endIdx_i < length`
> 	
> - `-1000 <= inc_i <= 1000`

> [!info] Approach
> Classic difference array application — multiple range increments on an initially zero array. For each update `[l, r, inc]`: `diff[l] += inc; diff[r+1] -= inc`. Prefix sum of `diff` is the final array. Build `diff[0..n]` (size n+1 to handle r+1 = n). Apply all updates. Prefix-sum `diff[0..n-1]` in-place.

> [!note]- Python Solution
> ```python
> def get_modified_array(length, updates):
>     diff = [0] * (length + 1)
>     for l, r, inc in updates:
>         diff[l] += inc
>         diff[r + 1] -= inc
>     result = []
>     running = 0
>     for i in range(length):
>         running += diff[i]
>         result.append(running)
>     return result
> ```

> [!success] Complexity
> Time O(u + n) where u = number of updates. Space O(n).

> [!tip] Alternatives
> - Brute force O(u × n): apply each update to every index in range. Too slow for large inputs.
> - Segment tree: O(u log n + n). Overkill — difference array is optimal when all queries come after all updates.

---

## Miscellaneous Array Techniques

---

### Best Time to Buy and Sell Stock `🎯 T2`

> Full walkthrough: [Best Time to Buy and Sell Stock (All Variants)](../algorithms/15-dynamic-programming.md#best-time-to-buy-and-sell-stock-all-variants--t2).

---

### Move Zeroes `⚡ T1`

> Full walkthrough: [Move Zeroes (LC 283)](../algorithms/03-two-pointers.md#move-zeroes-lc-283--t1).

---

### Two Sum (hash map variant) `⚡ T1`

> Full walkthrough: [Two Sum](02-hashing.md#two-sum--t1).

---

### Spiral Matrix

> [!example] Problem
> Given an m x n matrix, return all elements of the matrix in spiral order.
> 
> **Example 1:**
> ```
> Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
> Output: [1,2,3,6,9,8,7,4,5]
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
> Output: [1,2,3,4,8,12,11,10,9,5,6,7]
> ```
> 
> **Constraints:**
> - m == matrix.length
> - n == matrix[i].length
> - 1 <= m, n <= 10
> - -100 <= matrix[i][j] <= 100

> [!tip] Recognize · Gotcha
> **Signal:** "print in spiral order" · **Gotcha:** Re-check `top <= bot` / `left <= right` before the reverse passes

> [!info] Approach
> **Boundary shrinking — four-direction cycling.** Spiral traversal has four directions cycling with shrinking boundaries. Maintain four boundary pointers: `top, bottom, left, right`. Traverse right, down, left, up, then shrink boundaries inward. While `top <= bottom and left <= right`: traverse right along `top` row, `top++`; traverse down along `right` col, `right--`; if `top <= bottom`, traverse left along `bottom` row, `bottom--`; if `left <= right`, traverse up along `left` col, `left++`. The inner checks prevent double-counting for single row/col cases.

> [!note]- Python Solution
> ```python
> def spiral_order(matrix):
>     top, bottom = 0, len(matrix) - 1
>     left, right = 0, len(matrix[0]) - 1
>     result = []
>     while top <= bottom and left <= right:
>         for c in range(left, right + 1):
>             result.append(matrix[top][c])
>         top += 1
>         for r in range(top, bottom + 1):
>             result.append(matrix[r][right])
>         right -= 1
>         if top <= bottom:
>             for c in range(right, left - 1, -1):
>                 result.append(matrix[bottom][c])
>             bottom -= 1
>         if left <= right:
>             for r in range(bottom, top - 1, -1):
>                 result.append(matrix[r][left])
>             left += 1
>     return result
> ```

> [!success] Complexity
> Time O(m×n), Space O(1) extra.

> [!tip] Alternatives
> - DFS with direction array: more complex code, same complexity.
> - Recursive peeling: elegant but O(mn) call stack in worst case.

---

### Set Matrix Zeroes

> [!example] Problem
> Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0's.
> You must do it in place.
> 
> **Example 1:**
> ```
> Input: matrix = [[1,1,1],[1,0,1],[1,1,1]]
> Output: [[1,0,1],[0,0,0],[1,0,1]]
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
> Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]
> ```
> 
> **Constraints:**
> - m == matrix.length
> - n == matrix[0].length
> - 1 <= m, n <= 200
> - -2^{31} <= matrix[i][j] <= 2^{31} - 1

> [!tip] Recognize · Gotcha
> **Signal:** "O(1) extra space" · **Gotcha:** Separate flag for whether col 0 itself had a zero

> [!info] Approach
> **Use first row/col as markers — O(1) space.** Marking naively while iterating spreads zeros incorrectly. We must first record which rows/cols to zero, then apply. O(1) space trick: use the first row and first column as markers. Handle them last. Record if row 0 or col 0 should be zeroed (check for existing zeros). For all other cells, if `matrix[i][j] == 0`, set `matrix[i][0] = 0` and `matrix[0][j] = 0`. Then zero out rows and cols using those markers. Finally handle row 0 and col 0 separately.

> [!note]- Python Solution
> ```python
> def set_zeroes(matrix):
>     m, n = len(matrix), len(matrix[0])
>     first_row_zero = False
>     for j in range(n):
>         if matrix[0][j] == 0:
>             first_row_zero = True
>             break
>     first_col_zero = False
>     for i in range(m):
>         if matrix[i][0] == 0:
>             first_col_zero = True
>             break
>     # Use first row/col as markers for other rows/cols
>     for i in range(1, m):
>         for j in range(1, n):
>             if matrix[i][j] == 0:
>                 matrix[i][0] = 0
>                 matrix[0][j] = 0
>     # Zero out marked rows and cols (excluding row 0 and col 0)
>     for i in range(1, m):
>         if matrix[i][0] == 0:
>             for j in range(1, n):
>                 matrix[i][j] = 0
>     for j in range(1, n):
>         if matrix[0][j] == 0:
>             for i in range(1, m):
>                 matrix[i][j] = 0
>     # Handle first row and col
>     if first_row_zero:
>         for j in range(n):
>             matrix[0][j] = 0
>     if first_col_zero:
>         for i in range(m):
>             matrix[i][0] = 0
> ```

> [!success] Complexity
> Time O(m×n), Space O(1).

> [!tip] Alternatives
> - Store zeroed rows/cols in two sets: O(m+n) space. Simpler logic.

---

### Rotate Array

> [!example] Problem
> Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3,4,5,6,7], k = 3
> Output: [5,6,7,1,2,3,4]
> Explanation:
> rotate 1 steps to the right: [7,1,2,3,4,5,6]
> rotate 2 steps to the right: [6,7,1,2,3,4,5]
> rotate 3 steps to the right: [5,6,7,1,2,3,4]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [-1,-100,3,99], k = 2
> Output: [3,99,-1,-100]
> Explanation: 
> rotate 1 steps to the right: [99,-1,-100,3]
> rotate 2 steps to the right: [3,99,-1,-100]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -2^{31} <= nums[i] <= 2^{31} - 1
> - 0 <= k <= 10^5

> [!info] Approach
> **Triple reversal trick.** Naively rotating element-by-element takes O(n×k). Reverse-trick achieves O(n) in-place. Three reversal operations: reverse all, reverse first k, reverse last n-k. Composing these reversal operations achieves the rotation. Normalize `k = k % n`. Reverse `nums[0:n]`. Reverse `nums[0:k]`. Reverse `nums[k:n]`.

> [!note]- Python Solution
> ```python
> def rotate(nums, k):
>     n = len(nums)
>     k %= n
>     def reverse(l, r):
>         while l < r:
>             nums[l], nums[r] = nums[r], nums[l]
>             l += 1
>             r -= 1
>     reverse(0, n - 1)
>     reverse(0, k - 1)
>     reverse(k, n - 1)
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Extra array: `return nums[-k:] + nums[:-k]`. O(n) space.
> - Cyclic replacement: O(n) time, O(1) space. Complex to implement correctly (GCD-based grouping).

---

### Range Sum Query — Immutable (LC 303) `🎯 T2`

> [!example] Problem
> Given an integer array nums, handle multiple queries of the following type:
> Implement the NumArray class
> 
> **Example 1:**
> ```
> Input
> ["NumArray", "sumRange", "sumRange", "sumRange"]
> [[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]
> Output
> [null, 1, -1, -3]
> 
> Explanation
> NumArray numArray = new NumArray([-2, 0, 3, -5, 2, -1]);
> numArray.sumRange(0, 2); // return (-2) + 0 + 3 = 1
> numArray.sumRange(2, 5); // return 3 + (-5) + 2 + (-1) = -1
> numArray.sumRange(0, 5); // return (-2) + 0 + 3 + (-5) + 2 + (-1) = -3
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - -10^5 <= nums[i] <= 10^5
> - 0 <= left <= right < nums.length
> - At most 10^4 calls will be made to sumRange.

> [!info] Approach
> **Prefix sum array — O(1) per query.** Recomputing a range sum from scratch is O(n) per query. A prefix sum table converts any range-sum query to O(1) subtraction. Build `prefix[i] = nums[0] + ... + nums[i-1]` (1-indexed offset). Then `sum(l, r) = prefix[r+1] - prefix[l]`. Precompute `prefix[0..n]` where `prefix[0] = 0` and `prefix[i] = prefix[i-1] + nums[i-1]`. Each query: return `prefix[right+1] - prefix[left]`.

> [!note]- Python Solution
> ```python
> class NumArray:
>     def __init__(self, nums):
>         self.prefix = [0] * (len(nums) + 1)
>         for i, x in enumerate(nums):
>             self.prefix[i + 1] = self.prefix[i] + x
> >
>     def sum_range(self, left, right):
>         return self.prefix[right + 1] - self.prefix[left]
> ```

> [!success] Complexity
> Time O(n) build, O(1) per query. Space O(n).

> [!tip] Alternatives
> - Brute-force sum each query: O(n) per query — unacceptable for many queries.
> - Segment tree / BIT: O(n) build, O(log n) query — only needed when the array is mutable (LC 307).

---

### Jump Game (LC 55) `🎯 T2`

> Full walkthrough: [Jump Game (can reach?)](../algorithms/16-greedy.md#jump-game-can-reach--t2).

---

### Gas Station (LC 134) `🎯 T2`

> Full walkthrough: [Gas Station](../algorithms/16-greedy.md#gas-station--t2).

---

### First Missing Positive (LC 41)

> [!example] Problem
> Given an unsorted integer array nums. Return the smallest positive integer that is not present in nums.
> You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,0]
> Output: 3
> Explanation: The numbers in the range [1,2] are all in the array.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,4,-1,1]
> Output: 2
> Explanation: 1 is in the array but 2 is missing.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [7,8,9,11,12]
> Output: 1
> Explanation: The smallest positive integer 1 is missing.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -2^{31} <= nums[i] <= 2^{31} - 1

> [!info] Approach
> **Index-as-hash — cyclic placement of values in range [1, n].** Any value outside [1, n] is irrelevant (answer is in [1, n+1]). We can treat the array itself as a hash table mapping value `v` to index `v-1`. Place each value `v` in [1, n] at index `v-1` by swapping. After rearrangement, the first index `i` where `nums[i] != i+1` gives answer `i+1`. Swap phase: for each `i`, while `1 <= nums[i] <= n` and `nums[nums[i]-1] != nums[i]`, swap `nums[i]` with `nums[nums[i]-1]`. Scan phase: return first `i+1` where `nums[i] != i+1`, else return `n+1`.

> [!note]- Python Solution
> ```python
> def first_missing_positive(nums):
>     n = len(nums)
>     # Place each number in its correct bucket
>     for i in range(n):
>         while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
>             correct = nums[i] - 1
>             nums[i], nums[correct] = nums[correct], nums[i]
>     # Find first position where value is wrong
>     for i in range(n):
>         if nums[i] != i + 1:
>             return i + 1
>     return n + 1
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Hash set of positives, scan 1..n+1: O(n) time, O(n) space. Simpler but violates space constraint.
> - Sign-flip marking (negating values): O(n) time, O(1) space. Requires two clean-up passes; works but swapping approach is cleaner.
> - The while-loop swap looks O(n²) but is O(n) amortized — each element is swapped into its correct slot at most once.

---

## Matrix

---

### Rotate Image (LC 48)

> Full walkthrough: [Rotate Image](04-matrix.md#rotate-image--t2).

---

### Merge Intervals (LC 56) `🎯 T2`

> Full walkthrough: [Merge Intervals](../algorithms/16-greedy.md#merge-intervals--t2).

---

### Insert Interval (LC 57) `🎯 T2`

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
> **Three-phase linear scan: before, overlap, after.** The existing intervals are already sorted and non-overlapping. We can scan in one pass: collect all intervals that end before the new one starts, merge all that overlap, collect the rest. Three phases: (1) add intervals entirely before new interval; (2) merge all overlapping intervals into new interval; (3) add remaining intervals. Phase 1: while `intervals[i].end < new.start`, append. Phase 2: while `intervals[i].start <= new.end`, extend `new.start = min(new.start, ...)` and `new.end = max(new.end, ...)`. Append merged. Phase 3: append remaining.

> [!note]- Python Solution
> ```python
> def insert(intervals, newInterval):
>     result = []
>     i = 0
>     n = len(intervals)
>     # Phase 1: intervals entirely before newInterval
>     while i < n and intervals[i][1] < newInterval[0]:
>         result.append(intervals[i])
>         i += 1
>     # Phase 2: merge overlapping intervals
>     while i < n and intervals[i][0] <= newInterval[1]:
>         newInterval[0] = min(newInterval[0], intervals[i][0])
>         newInterval[1] = max(newInterval[1], intervals[i][1])
>         i += 1
>     result.append(newInterval)
>     # Phase 3: intervals entirely after newInterval
>     while i < n:
>         result.append(intervals[i])
>         i += 1
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Add new interval and run full Merge Intervals: O(n log n). Wastes the pre-sorted property.
> - Binary search for insertion point: O(log n) to find start, but merging still O(n) — same overall.

---

### Non-overlapping Intervals (LC 435) `🎯 T2`

> Full walkthrough: [Non-overlapping Intervals (Minimum number to remove)](../algorithms/16-greedy.md#non-overlapping-intervals-minimum-number-to-remove--t2).

---

## Prefix Sum

---

### Subarray Sum Equals K (with negative numbers) `⚡ T1`

> Full walkthrough: [Subarray Sum Equals K](02-hashing.md#subarray-sum-equals-k--t1).

---

### Contiguous Array (Equal 0s and 1s) `⚡ T1`

> Full walkthrough: [Contiguous Array (LC 525)](02-hashing.md#contiguous-array-lc-525--t1).

---

## See Also

[[sliding-window]] | [[two-pointers]] | [[binary-search]] | [[hashing]] | [[sorting]]
