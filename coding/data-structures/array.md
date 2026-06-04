---
tags: [coding, data-structures, array]
topic: array
difficulty: mixed
---

# Array Problems — Deep Dive


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## Two Pointers

### Two Sum (sorted variant) `🔥 Google`

> [!example] Problem
> Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
> You may assume that each input would have exactly one solution, and you may not use the same element twice.
> You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [2,7,11,15], target = 9
> Output: [0,1]
> Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,4], target = 6
> Output: [1,2]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [3,3], target = 6
> Output: [0,1]
> ```
> 
> **Constraints:**
> - 2 <= nums.length <= 10^4
> - -10^9 <= nums[i] <= 10^9
> - -10^9 <= target <= 10^9
> - Only one valid answer exists.

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

### 3Sum `🔥 Google`

> [!example] Problem
> Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
> Notice that the solution set must not contain duplicate triplets.
> 
> **Example 1:**
> ```
> Input: nums = [-1,0,1,2,-1,-4]
> Output: [[-1,-1,2],[-1,0,1]]
> Explanation: 
> nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
> nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
> nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
> The distinct triplets are [-1,0,1] and [-1,-1,2].
> Notice that the order of the output and the order of the triplets does not matter.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,1]
> Output: []
> Explanation: The only possible triplet does not sum up to 0.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,0,0]
> Output: [[0,0,0]]
> Explanation: The only possible triplet sums up to 0.
> ```
> 
> **Constraints:**
> - 3 <= nums.length <= 3000
> - -10^5 <= nums[i] <= 10^5

> [!info] Approach
> **Fix + Two Pointers.** Brute force O(n³) is too slow. Fixing one element reduces it to a 2Sum on the remaining sorted suffix. Sort once, fix `nums[i]`, run two pointers on `i+1..n-1`. Sort. For each `i`, if `nums[i] > 0` break (sorted — no triplet can sum to 0). Skip duplicate `i`. Run two-pointer on the suffix. On match, skip duplicate `left` and `right` before advancing both. Three deduplication sites: `i`, `left`, `right`.

> In an interview: sorting is what makes the duplicate skipping and early break safe, so this pattern is usually the cleanest solution in interviews.

> [!note]- Python Solution
> ```python
> def three_sum(nums):
>     nums.sort()
>     result = []
>     for i in range(len(nums) - 2):
>         if nums[i] > 0:
>             break
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue
>         l, r = i + 1, len(nums) - 1
>         while l < r:
>             s = nums[i] + nums[l] + nums[r]
>             if s == 0:
>                 result.append([nums[i], nums[l], nums[r]])
>                 while l < r and nums[l] == nums[l + 1]:
>                     l += 1
>                 while l < r and nums[r] == nums[r - 1]:
>                     r -= 1
>                 l += 1
>                 r -= 1
>             elif s < 0:
>                 l += 1
>             else:
>                 r -= 1
>     return result
> ```

> [!success] Complexity
> Time O(n²), Space O(1) extra (output excluded).

> [!tip] Edge cases
> - If the array has fewer than 3 elements, return `[]`.
> - After sorting, all-positive arrays can exit immediately once the first fixed element becomes positive.

> [!tip] Alternatives
> - Hash set for third element: O(n²) time, O(n) space. Harder deduplication logic.
> - Brute force O(n³): never acceptable.

---

### 3Sum Closest `🔥 Google`

> [!example] Problem
> Given an integer array nums of length n and an integer target, find three integers in nums such that the sum is closest to target.
> Return the sum of the three integers.
> You may assume that each input would have exactly one solution.
> 
> **Example 1:**
> ```
> Input: nums = [-1,2,1,-4], target = 1
> Output: 2
> Explanation: The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,0,0], target = 1
> Output: 0
> Explanation: The sum that is closest to the target is 0. (0 + 0 + 0 = 0).
> ```
> 
> **Constraints:**
> - 3 <= nums.length <= 500
> - -1000 <= nums[i] <= 1000
> - -10^4 <= target <= 10^4

> [!info] Approach
> **Sort + Two Pointers with closest tracking.** Same sorted + two-pointer framework as 3Sum, but instead of equality we track the minimum distance. Track `closest` as best sum seen. After computing current sum, advance `l` or `r` to pull sum toward target. Sort. For each `i`, two-pointer on suffix. Compute `s = nums[i]+nums[l]+nums[r]`. Update `closest` if `|s - target| < |closest - target|`. If `s < target`, `l++`. If `s > target`, `r--`. If exact match, return immediately.

> [!note]- Python Solution
> ```python
> def three_sum_closest(nums, target):
>     nums.sort()
>     closest = nums[0] + nums[1] + nums[2]
>     for i in range(len(nums) - 2):
>         l, r = i + 1, len(nums) - 1
>         while l < r:
>             s = nums[i] + nums[l] + nums[r]
>             if abs(s - target) < abs(closest - target):
>                 closest = s
>             if s < target:
>                 l += 1
>             elif s > target:
>                 r -= 1
>             else:
>                 return s
>     return closest
> ```

> [!success] Complexity
> Time O(n²), Space O(1).

> [!tip] Edge cases
> - Initialize `closest` from the first three numbers so negative targets and large magnitudes work naturally.
> - If you find an exact match, return immediately — it is already optimal.

> [!tip] Alternatives
> - Brute force O(n³): always infeasible. No O(n log n) solution known for the general case.

---

### 4Sum `⭐ Google`

> [!example] Problem
> Given an array nums of n integers, return an array of all the unique quadruplets [nums[a], nums[b], nums[c], nums[d]] such that:
> You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,0,-1,0,-2,2], target = 0
> Output: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,2,2,2,2], target = 8
> Output: [[2,2,2,2]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 200
> - -10^9 <= nums[i] <= 10^9
> - -10^9 <= target <= 10^9

> [!info] Approach
> **Two nested loops + Two Pointers.** Generalizes 3Sum by adding one more fixed element. Fix two elements (i, j) and run two pointers on the rest. Two nested loops fix first two elements; two pointers find the last two. Deduplicate at all four levels. Sort. Outer loop `i`, inner loop `j = i+1`. Skip duplicate `i` and `j`. Two pointers `l=j+1, r=n-1`. Same pointer logic as 3Sum. Early termination: if the smallest possible sum for the current `i` is already too large, break; if the largest possible sum is still too small, continue.

> [!note]- Python Solution
> ```python
> def four_sum(nums, target):
>     nums.sort()
>     n = len(nums)
>     result = []
>     for i in range(n - 3):
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue
>         for j in range(i + 1, n - 2):
>             if j > i + 1 and nums[j] == nums[j - 1]:
>                 continue
>             l, r = j + 1, n - 1
>             while l < r:
>                 s = nums[i] + nums[j] + nums[l] + nums[r]
>                 if s == target:
>                     result.append([nums[i], nums[j], nums[l], nums[r]])
>                     while l < r and nums[l] == nums[l + 1]:
>                         l += 1
>                     while l < r and nums[r] == nums[r - 1]:
>                         r -= 1
>                     l += 1
>                     r -= 1
>                 elif s < target:
>                     l += 1
>                 else:
>                     r -= 1
>     return result
> ```

> [!success] Complexity
> Time O(n³), Space O(1) extra.

> [!tip] Edge cases
> - Four numbers can overflow 32-bit arithmetic in some languages; use a wider type if needed.
> - Deduplicate at each level in the order `i`, `j`, `l`, `r` to avoid repeated quadruplets.

> [!tip] Alternatives
> - Hash map approach: O(n²) average using pair-sum hash map. Complex deduplication; O(n²) space. Rarely worth it over the clean O(n³) two-pointer.

---

### Container with Most Water `🔥 Google`

> [!example] Problem
> You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).
> Find two lines that together with the x-axis form a container, such that the container contains the most water.
> Return the maximum amount of water a container can store.
> Notice that you may not slant the container.
> 
> **Example 1:**
> ```
> Input: height = [1,8,6,2,5,4,8,3,7]
> Output: 49
> Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
> ```
> 
> **Example 2:**
> ```
> Input: height = [1,1]
> Output: 1
> ```
> 
> **Constraints:**
> - n == height.length
> - 2 <= n <= 10^5
> - 0 <= height[i] <= 10^4

> [!info] Approach
> **Two Pointers — advance the shorter line.** Area = min(height[l], height[r]) × (r - l). To maximize, we must consider both height and width. Brute force O(n²) tries all pairs. Two pointers. The width decreases as pointers converge, so we must compensate with greater height. `l=0, r=n-1`. Compute area. Always advance the pointer pointing to the shorter line — moving the taller line can never increase `min(h[l], h[r])` while width also decreases.

> [!note]- Python Solution
> ```python
> def max_area(height):
>     l, r = 0, len(height) - 1
>     best = 0
>     while l < r:
>         area = min(height[l], height[r]) * (r - l)
>         best = max(best, area)
>         if height[l] <= height[r]:
>             l += 1
>         else:
>             r -= 1
>     return best
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Brute force O(n²): check all pairs. Never acceptable.
> - Moving the taller pointer is also correct but suboptimal — both converge. Only advancing the shorter is the standard proof-based argument.

---

### Trapping Rain Water `🔥 Google`

> [!example] Problem
> Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
> 
> **Example 1:**
> ```
> Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
> Output: 6
> Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
> ```
> 
> **Example 2:**
> ```
> Input: height = [4,2,0,3,2,5]
> Output: 9
> ```
> 
> **Constraints:**
> - n == height.length
> - 1 <= n <= 2 * 10^4
> - 0 <= height[i] <= 10^5

> [!info] Approach
> **Two Pointers — binding constraint side.** Water at index `i` is bounded by `min(max_left, max_right) - height[i]`. We need left-max and right-max for every position. Two pointers eliminating the need for prefix/suffix arrays. The side with the smaller max is the binding constraint. `l=0, r=n-1`, `l_max=r_max=0`. If `l_max <= r_max`, the left side is the constraint, so water at `l` is `l_max - height[l]` and we advance `l`. Otherwise, the right side is the constraint, so water at `r` is `r_max - height[r]` and we decrement `r`.

> [!note]- Python Solution
> ```python
> def trap(height):
>     l, r = 0, len(height) - 1
>     l_max = r_max = 0
>     water = 0
>     while l < r:
>         if l_max <= r_max:
>             l_max = max(l_max, height[l])
>             water += l_max - height[l]
>             l += 1
>         else:
>             r_max = max(r_max, height[r])
>             water += r_max - height[r]
>             r -= 1
>     return water
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Edge cases
> - Empty arrays or arrays with fewer than 3 bars trap no water.
> - Flat or monotonic terrain also returns 0; the algorithm naturally handles both.

> [!tip] Alternatives
> - Prefix/suffix max arrays: O(n) time, O(n) space. More intuitive, same time.
> - Monotonic stack: O(n) time, O(n) space. Computes water layer by layer horizontally. Useful for the histogram variant.

---

### Remove Duplicates from Sorted Array

> [!example] Problem
> Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in nums.
> Consider the number of unique elements of nums to be k, to get accepted, you need to do the following things:
> Custom Judge:
> The judge will test your solution with the following code:
> If all assertions pass, then your solution will be accepted.
> 
> **Example 1:**
> ```
> int[] nums = [...]; // Input array
> int[] expectedNums = [...]; // The expected answer with correct length
> 
> int k = removeDuplicates(nums); // Calls your implementation
> 
> assert k == expectedNums.length;
> for (int i = 0; i < k; i++) {
>     assert nums[i] == expectedNums[i];
> }
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,1,2]
> Output: 2, nums = [1,2,_]
> Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
> It does not matter what you leave beyond the returned k (hence they are underscores).
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,0,1,1,1,2,2,3,3,4]
> Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
> Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
> It does not matter what you leave beyond the returned k (hence they are underscores).
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - -100 <= nums[i] <= 100
> - nums is sorted in non-decreasing order.

> [!info] Approach
> **Two Pointers — slow/fast write pattern.** Sorted guarantees duplicates are adjacent. We need one pointer tracking the write position (valid prefix) and one scanning forward. Two pointers — `slow` marks next write index, `fast` scans for new values. `slow=1`. For `fast` in `1..n-1`: if `nums[fast] != nums[slow-1]`, write `nums[slow] = nums[fast]`, `slow++`. Return `slow`.

> [!note]- Python Solution
> ```python
> def remove_duplicates(nums):
>     if not nums:
>         return 0
>     slow = 1
>     for fast in range(1, len(nums)):
>         if nums[fast] != nums[slow - 1]:
>             nums[slow] = nums[fast]
>             slow += 1
>     return slow
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Python `list(dict.fromkeys(nums))`: O(n), but creates new list — violates in-place constraint.
> - Using a set: O(n) space, doesn't exploit sorted order.

---

### Next Permutation `⭐ Google`

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

### Max Consecutive Ones III

> [!example] Problem
> Given a binary array nums and an integer k, return the maximum number of consecutive 1's in the array if you can flip at most k 0's.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
> Output: 6
> Explanation: [1,1,1,0,0,1,1,1,1,1,1]
> Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
> Output: 10
> Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
> Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - nums[i] is either 0 or 1.
> - 0 <= k <= nums.length

> [!info] Approach
> **Variable sliding window — zero count tracking.** We want the longest window containing at most `k` zeros. This is monotone: a larger window is valid as long as zero-count ≤ k. Variable sliding window tracking zero count. Expand `r`. If `nums[r] == 0`, increment zero count. If zeros > k, shrink `l` until zeros ≤ k (moving `l` past a zero decrements zero count). Track `r - l + 1` as window size.

> [!note]- Python Solution
> ```python
> def longest_ones(nums, k):
>     l = zeros = best = 0
>     for r in range(len(nums)):
>         if nums[r] == 0:
>             zeros += 1
>         while zeros > k:
>             if nums[l] == 0:
>                 zeros -= 1
>             l += 1
>         best = max(best, r - l + 1)
>     return best
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Prefix sum counting zeros: O(n) time, O(n) space. Overkill for this structure.
> - The window can only grow (never shrink smaller than `best`) — optimization: replace `while` with `if` to achieve O(n) with fixed-size window advance.

---

### Subarrays with K Different Integers

> [!example] Problem
> Given an integer array nums and an integer k, return the number of good subarrays of nums.
> A good array is an array where the number of different integers in that array is exactly k.
> A subarray is a contiguous part of an array.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,1,2,3], k = 2
> Output: 7
> Explanation: Subarrays formed with exactly 2 different integers: [1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2], [1,2,1,2]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,1,3,4], k = 3
> Output: 3
> Explanation: Subarrays formed with exactly 3 different integers: [1,2,1,3], [2,1,3], [1,3,4].
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - 1 <= nums[i], k <= nums.length

> [!info] Approach
> **Exactly-k = at_most(k) − at_most(k−1).** Sliding window with exact count is non-monotone — a window can become invalid as it grows but also as elements fall out. Direct counting is intractable. Transform "exactly k" to "at most k" − "at most k−1". The "at most k" function is monotone. `at_most(k)` counts subarrays with ≤ k distinct integers. Use standard sliding window: expand right, if distinct count > k shrink left, add `r - l + 1` (all subarrays ending at `r` and starting at `l..r`). Answer = `at_most(k) - at_most(k-1)`.

> [!note]- Python Solution
> ```python
> def subarrays_with_k_distinct(nums, k):
>     def at_most(k):
>         count = {}
>         l = result = 0
>         for r, x in enumerate(nums):
>             count[x] = count.get(x, 0) + 1
>             while len(count) > k:
>                 count[nums[l]] -= 1
>                 if count[nums[l]] == 0:
>                     del count[nums[l]]
>                 l += 1
>             result += r - l + 1
>         return result
> 
>     return at_most(k) - at_most(k - 1)
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Direct exact-k sliding window with two pointers marking left boundary range: O(n), same complexity, more complex implementation.

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

### Product of Array Except Self `🔥 Google`

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

### Maximum Subarray `🔥 Google`

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

### Sort Colors `⭐ Google`

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
> **Dutch National Flag — three-pointer partition.** We can't use comparison sort and achieve O(n) with O(1) space in one pass. Three distinct values → three-way partition. Dutch National Flag algorithm: three pointers maintain invariant regions: `[0..lo)` are 0s, `[lo..mid)` are 1s, `(hi..n-1]` are 2s. `[mid..hi]` is unexamined. `lo=0, mid=0, hi=n-1`. While `mid <= hi`: if `nums[mid]==0`, swap with `lo`, advance both; if `nums[mid]==1`, advance `mid`; if `nums[mid]==2`, swap with `hi`, decrement `hi` — do NOT advance `mid` (swapped element from `hi` is unexamined).

> [!note]- Python Solution
> ```python
> def sort_colors(nums):
>     lo = mid = 0
>     hi = len(nums) - 1
>     while mid <= hi:
>         if nums[mid] == 0:
>             nums[lo], nums[mid] = nums[mid], nums[lo]
>             lo += 1
>             mid += 1
>         elif nums[mid] == 1:
>             mid += 1
>         else:
>             nums[mid], nums[hi] = nums[hi], nums[mid]
>             hi -= 1
>             # mid stays — swapped element from hi is unexamined
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Count 0s, 1s, 2s and overwrite: two passes, O(n) time, O(1) space. Simpler but two passes.
> - `nums.sort()`: O(n log n). Never acceptable when O(n) exists.

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

### Majority Element `⭐ Google`

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

### Find the Duplicate Number `⭐ Google`

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

### Difference Array Pattern

> When you need to apply many range updates `[l, r] += val` and then query final values, the naive approach is O(n) per update — O(n × q) total for q updates. Difference array makes each update O(1) and reconstruction O(n), giving O(q + n) overall. Build `diff[]` where `diff[i] = arr[i] - arr[i-1]`. To add `val` to range `[l, r]`: `diff[l] += val`, `diff[r+1] -= val`. Reconstruct prefix sum to get the final array. Initialize `diff = [0] * (n + 1)`. For each update `(l, r, val)`: `diff[l] += val; diff[r+1] -= val`. After all updates, compute prefix sum of `diff` to get the result array.

---

### Car Pooling

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

### Best Time to Buy and Sell Stock `🔥 Google`

> [!example] Problem
> You are given an array prices where prices[i] is the price of a given stock on the ith day.
> You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
> Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
> 
> **Example 1:**
> ```
> Input: prices = [7,1,5,3,6,4]
> Output: 5
> Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
> Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
> ```
> 
> **Example 2:**
> ```
> Input: prices = [7,6,4,3,1]
> Output: 0
> Explanation: In this case, no transactions are done and the max profit = 0.
> ```
> 
> **Constraints:**
> - 1 <= prices.length <= 10^5
> - 0 <= prices[i] <= 10^4

> [!info] Approach
> Track the minimum price seen so far. Profit at day `i` = `prices[i] - min_so_far`. The best sell day for any buy day is always the global minimum to the left. Single pass — maintain `min_price` and `max_profit`. `min_price = inf, max_profit = 0`. For each price: `min_price = min(min_price, price)`, `max_profit = max(max_profit, price - min_price)`.

> [!note]- Python Solution
> ```python
> def max_profit(prices):
>     min_price = float('inf')
>     max_profit = 0
>     for price in prices:
>         min_price = min(min_price, price)
>         max_profit = max(max_profit, price - min_price)
>     return max_profit
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - DP: `dp[i] = max(dp[i-1], prices[i] - min_prices[i])` — same logic made explicit. O(n) time, O(n) space.
> - Two-pass: first pass builds prefix-min array, second pass computes max profit. O(n) time, O(n) space. Same idea, less elegant.
> - Brute force O(n²): check all (buy, sell) pairs. Never acceptable.

---

### Move Zeroes `🔥 Google`

> [!example] Problem
> Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.
> Note that you must do this in-place without making a copy of the array.
> 
> **Example 1:**
> ```
> Input: nums = [0,1,0,3,12]
> Output: [1,3,12,0,0]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0]
> Output: [0]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - -2^{31} <= nums[i] <= 2^{31} - 1

> [!info] Approach
> We need to compact non-zero elements to the front, preserving order, without allocating extra space. Two-pointer — `slow` tracks the next write position for non-zero elements; `fast` scans forward. `slow = 0`. For each `fast`: if `nums[fast] != 0`, set `nums[slow] = nums[fast]`, `slow++`. After the loop, zero out `nums[slow..n-1]`.

> [!note]- Python Solution
> ```python
> def move_zeroes(nums):
>     slow = 0
>     for fast in range(len(nums)):
>         if nums[fast] != 0:
>             nums[slow] = nums[fast]
>             slow += 1
>     for i in range(slow, len(nums)):
>         nums[i] = 0
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Swap variant: swap `nums[slow]` and `nums[fast]` instead of overwrite — avoids the second zero-fill pass but does more swaps. Correct when the array is sparse in non-zeros.
> - `nums.sort(key=lambda x: x == 0)`: O(n log n), not in-place in CPython, loses relative order if not stable (it is stable in Python, but still O(n log n) — worse).

---

### Two Sum (hash map variant) `🔥 Google`

> [!example] Problem
> Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
> You may assume that each input would have exactly one solution, and you may not use the same element twice.
> You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [2,7,11,15], target = 9
> Output: [0,1]
> Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,4], target = 6
> Output: [1,2]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [3,3], target = 6
> Output: [0,1]
> ```
> 
> **Constraints:**
> - 2 <= nums.length <= 10^4
> - -10^9 <= nums[i] <= 10^9
> - -10^9 <= target <= 10^9
> - Only one valid answer exists.

> [!info] Approach
> **Hash map complement lookup.** Unsorted array → can't use two pointers (no sorted invariant). We need O(1) complement lookup. Hash map storing `value → index`. Single pass: check if complement exists before recording current. For each `(i, x)`: compute `complement = target - x`. If in map, return `[map[complement], i]`. Else record `x → i`. Checking before recording ensures we don't use same index twice.

> [!note]- Python Solution
> ```python
> def two_sum(nums, target):
>     seen = {}  # value -> index
>     for i, x in enumerate(nums):
>         complement = target - x
>         if complement in seen:
>             return [seen[complement], i]
>         seen[x] = i
>     return []
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Sort + two pointers: O(n log n) time, O(1) space but loses original indices unless you store them.
> - Brute force O(n²): never.

---

### Spiral Matrix `🔥 Google`

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

### Set Matrix Zeroes `🔥 Google`

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

### Range Sum Query — Immutable (LC 303) `⭐ Google`

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

### Range Sum Query 2D — Immutable (LC 304) `⭐ Google`

> [!example] Problem
> Given a 2D matrix matrix, handle multiple queries of the following type:
> Implement the NumMatrix class:
> You must design an algorithm where sumRegion works on O(1) time complexity.
> 
> **Example 1:**
> ```
> Input
> ["NumMatrix", "sumRegion", "sumRegion", "sumRegion"]
> [[[[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]], [2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]
> Output
> [null, 8, 11, 12]
> 
> Explanation
> NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
> numMatrix.sumRegion(2, 1, 4, 3); // return 8 (i.e sum of the red rectangle)
> numMatrix.sumRegion(1, 1, 2, 2); // return 11 (i.e sum of the green rectangle)
> numMatrix.sumRegion(1, 2, 2, 4); // return 12 (i.e sum of the blue rectangle)
> ```
> 
> **Constraints:**
> - m == matrix.length
> - n == matrix[i].length
> - 1 <= m, n <= 200
> - -10^4 <= matrix[i][j] <= 10^4
> - 0 <= row1 <= row2 < m
> - 0 <= col1 <= col2 < n
> - At most 10^4 calls will be made to sumRegion.

> [!info] Approach
> **2D prefix sum (inclusion-exclusion).** Each query touching O(m×n) cells is too slow for many queries. 2D prefix sums extend the 1D idea: `prefix[i][j]` = sum of the rectangle from `(0,0)` to `(i-1, j-1)`. Build `prefix[i][j] = prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1] + matrix[i-1][j-1]`. Query: inclusion-exclusion of four corners. `sum(r1,c1,r2,c2) = prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]`.

> [!note]- Python Solution
> ```python
> class NumMatrix:
>     def __init__(self, matrix):
>         m, n = len(matrix), len(matrix[0])
>         self.prefix = [[0] * (n + 1) for _ in range(m + 1)]
>         for i in range(1, m + 1):
>             for j in range(1, n + 1):
>                 self.prefix[i][j] = (matrix[i-1][j-1]
>                                      + self.prefix[i-1][j]
>                                      + self.prefix[i][j-1]
>                                      - self.prefix[i-1][j-1])
> >
>     def sum_region(self, row1, col1, row2, col2):
>         p = self.prefix
>         return (p[row2+1][col2+1]
>                 - p[row1][col2+1]
>                 - p[row2+1][col1]
>                 + p[row1][col1])
> ```

> [!success] Complexity
> Time O(m×n) build, O(1) per query. Space O(m×n).

> [!tip] Alternatives
> - Row-wise prefix sums only: O(n) per query. Acceptable for skinny matrices, not general.
> - 2D BIT / segment tree: O(log²(mn)) updates and queries — only if the matrix is mutable.

---

### Jump Game (LC 55) `🔥 Google`

> [!example] Problem
> You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.
> Return true if you can reach the last index, or false otherwise.
> 
> **Example 1:**
> ```
> Input: nums = [2,3,1,1,4]
> Output: true
> Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,1,0,4]
> Output: false
> Explanation: You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - 0 <= nums[i] <= 10^5

> [!info] Approach
> **Greedy — track farthest reachable index.** We don't need to know which path reaches the end, only whether any path does. A greedy max-reach scan is sufficient. Single pass maintaining `reach = max index reachable so far`. If current index `i > reach`, we're stuck. `reach = 0`. For each `i` in `0..n-1`: if `i > reach`, return False. Update `reach = max(reach, i + nums[i])`. If `reach >= n-1` at any point, return True.

> [!note]- Python Solution
> ```python
> def can_jump(nums):
>     reach = 0
>     for i, v in enumerate(nums):
>         if i > reach:
>             return False
>         reach = max(reach, i + v)
>     return True
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - DP `dp[i] = True if reachable`: O(n²) worst case (inner loop per position). Correct but slow.
> - Backward scan (find last "good" index): O(n), same greedy idea in reverse.

---

### Gas Station (LC 134)

> [!example] Problem
> There are n gas stations along a circular route, where the amount of gas at the ith station is gas[i].
> You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from the ith station to its next (i + 1)th station. You begin the journey with an empty tank at one of the gas stations.
> Given two integer arrays gas and cost, return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return -1. If there exists a solution, it is guaranteed to be unique.
> 
> **Example 1:**
> ```
> Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
> Output: 3
> Explanation:
> Start at station 3 (index 3) and fill up with 4 unit of gas. Your tank = 0 + 4 = 4
> Travel to station 4. Your tank = 4 - 1 + 5 = 8
> Travel to station 0. Your tank = 8 - 2 + 1 = 7
> Travel to station 1. Your tank = 7 - 3 + 2 = 6
> Travel to station 2. Your tank = 6 - 4 + 3 = 5
> Travel to station 3. The cost is 5. Your gas is just enough to travel back to station 3.
> Therefore, return 3 as the starting index.
> ```
> 
> **Example 2:**
> ```
> Input: gas = [2,3,4], cost = [3,4,3]
> Output: -1
> Explanation:
> You can't start at station 0 or 1, as there is not enough gas to travel to the next station.
> Let's start at station 2 and fill up with 4 unit of gas. Your tank = 0 + 4 = 4
> Travel to station 0. Your tank = 4 - 3 + 2 = 3
> Travel to station 1. Your tank = 3 - 3 + 3 = 3
> You cannot travel back to station 2, as it requires 4 unit of gas but you only have 3.
> Therefore, you can't travel around the circuit once no matter where you start.
> ```
> 
> **Constraints:**
> - n == gas.length == cost.length
> - 1 <= n <= 10^5
> - 0 <= gas[i], cost[i] <= 10^4
> - The input is generated such that the answer is unique.

> [!info] Approach
> **Greedy — reset start on deficit.** If total gas < total cost, no solution exists. Otherwise, a solution always exists. The greedy key: if we can't reach station `j` starting from `start`, then no station between `start` and `j` can be a valid start either (they would start with less surplus). Single pass tracking cumulative surplus. Reset start candidate whenever cumulative drops below zero. `total = 0, tank = 0, start = 0`. For each `i`: `tank += gas[i] - cost[i]`, `total += gas[i] - cost[i]`. If `tank < 0`, set `start = i + 1`, reset `tank = 0`. Return `start` if `total >= 0` else `-1`.

> [!note]- Python Solution
> ```python
> def can_complete_circuit(gas, cost):
>     total = tank = start = 0
>     for i in range(len(gas)):
>         diff = gas[i] - cost[i]
>         tank += diff
>         total += diff
>         if tank < 0:
>             start = i + 1
>             tank = 0
>     return start if total >= 0 else -1
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Brute force: try each starting station — O(n²). Too slow.
> - Two-pointer circular simulation: equivalent logic, no asymptotic improvement.

---

## Matrix

### Rotate Image (LC 48) `🔥 Google`

> [!example] Problem
> You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).
> You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.
> 
> **Example 1:**
> ```
> Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
> Output: [[7,4,1],[8,5,2],[9,6,3]]
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
> Output: [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
> ```
> 
> **Constraints:**
> - n == matrix.length == matrix[i].length
> - 1 <= n <= 20
> - -1000 <= matrix[i][j] <= 1000

> [!info] Approach
> **Transpose then reverse each row.** A 90° clockwise rotation of a matrix equals: transpose (swap `matrix[i][j]` with `matrix[j][i]`) followed by reversing each row. Both operations are O(n²) and in-place. Step 1: Transpose — swap upper-triangle elements across the main diagonal. Step 2: Reverse each row. Transpose: `for i in range(n): for j in range(i+1, n): swap matrix[i][j] and matrix[j][i]`. Reverse: `for row in matrix: row.reverse()`.

> [!note]- Python Solution
> ```python
> def rotate(matrix):
>     n = len(matrix)
>     # Transpose
>     for i in range(n):
>         for j in range(i + 1, n):
>             matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
>     # Reverse each row
>     for row in matrix:
>         row.reverse()
> ```

> [!success] Complexity
> Time O(n²), Space O(1).

> [!tip] Alternatives
> - Four-way simultaneous swap per cell: O(n²) time, O(1) space. Rotates groups of 4 in a single pass — no transpose step. Harder to index correctly.
> - Counterclockwise 90°: transpose then reverse each column (or reverse rows then transpose).
> - 180°: reverse each row then reverse the matrix rows order.

---

### Merge Intervals (LC 56) `🔥 Google`

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
> **Sort by start, linear merge scan.** After sorting by start time, overlapping intervals are adjacent. We only need to check if the current interval overlaps with the last merged one. Sort, then greedily extend the last merged interval or append a new one. Sort by `start`. Initialize `merged = [intervals[0]]`. For each subsequent interval: if `interval.start <= merged[-1].end`, merge by updating `merged[-1].end = max(merged[-1].end, interval.end)`. Else append.

> [!note]- Python Solution
> ```python
> def merge(intervals):
>     intervals.sort(key=lambda x: x[0])
>     merged = [intervals[0]]
>     for start, end in intervals[1:]:
>         if start <= merged[-1][1]:
>             merged[-1][1] = max(merged[-1][1], end)
>         else:
>             merged.append([start, end])
>     return merged
> ```

> [!success] Complexity
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> - Without sorting: O(n²) — check every pair. Never acceptable.
> - Event-based (sweep line): same O(n log n). More general but more code.

---

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

### Non-overlapping Intervals (LC 435) `🔥 Google`

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
> **Greedy — sort by end, keep earliest-ending non-conflicting interval.** Classic interval scheduling maximization (keep max non-overlapping intervals). Minimum removals = n − max kept. The greedy is: always keep the interval that ends earliest — it leaves the most room for future intervals. Sort by end time. Greedily keep an interval if it starts at or after the previous kept interval's end. Sort by `end`. `prev_end = -inf, kept = 0`. For each interval: if `start >= prev_end`, keep it (`kept++`, update `prev_end = end`). Else skip (remove it). Answer = `n - kept`.

> [!note]- Python Solution
> ```python
> def erase_overlap_intervals(intervals):
>     intervals.sort(key=lambda x: x[1])
>     prev_end = float('-inf')
>     kept = 0
>     for start, end in intervals:
>         if start >= prev_end:
>             kept += 1
>             prev_end = end
>     return len(intervals) - kept
> ```

> [!success] Complexity
> Time O(n log n), Space O(1).

> [!tip] Alternatives
> - Sort by start, keep track of min end among conflicting: equivalent logic, less intuitive.
> - DP `dp[i]` = max intervals ending at i: O(n²). Too slow.
> - Key insight: sort by end (not start) for greedy interval scheduling.

---

## Miscellaneous (Continued)

### First Missing Positive (LC 41) `⭐ Google`

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

## See Also

[[sliding-window]] | [[two-pointers]] | [[binary-search]] | [[hashing]] | [[sorting]]
### First Missing Positive `⭐ Google`

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
> Values in `[1..n]` can be placed into their correct indices in-place. Anything outside that range can be ignored. Cyclic sort: keep swapping `nums[i]` into position `nums[i] - 1` while it is in range and not already placed. After placement, scan left to right; the first index `i` where `nums[i] != i + 1` gives the answer.

> [!note]- Python Solution
> ```python
> def first_missing_positive(nums):
>     n = len(nums)
>     i = 0
>     while i < n:
>         x = nums[i]
>         if 1 <= x <= n and nums[x - 1] != x:
>             nums[i], nums[x - 1] = nums[x - 1], nums[i]
>         else:
>             i += 1
>     for i, x in enumerate(nums):
>         if x != i + 1:
>             return i + 1
>     return n + 1
> ```

> [!success] Complexity
> O(n) time, O(1) extra space.

> [!tip] Alternatives
> A hash set is simpler but uses O(n) extra space; cyclic sort is the canonical follow-up proof question.

---

## Prefix Sum

### Subarray Sum Equals K (with negative numbers) `🔥 Google`

> [!example] Problem
> Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.
> A subarray is a contiguous non-empty sequence of elements within an array.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,1], k = 2
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3], k = 3
> Output: 2
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - -1000 <= nums[i] <= 1000
> - -10^7 <= k <= 10^7

> [!info] Approach
> Two-pointer/sliding-window breaks with negatives. Prefix sums let us reframe: subarray `[i+1..j]` sums to `k` iff `prefix[j] - prefix[i] == k`, i.e., `prefix[i] == prefix[j] - k`. Track prefix sum frequency in a hash map. For each new prefix sum, check how many prior prefix sums equal `current - k`. Initialize map with `{0: 1}` (empty prefix). Walk the array accumulating `running_sum`; add `count_map[running_sum - k]` to the answer; then increment `count_map[running_sum]`.

> [!note]- Python Solution
> ```python
> def subarray_sum(nums, k):
>     count_map = {0: 1}
>     running_sum = 0
>     total = 0
>     for num in nums:
>         running_sum += num
>         needed = running_sum - k
>         total += count_map.get(needed, 0)
>         count_map[running_sum] = count_map.get(running_sum, 0) + 1
>     return total
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Brute force O(n²) with nested loops checking all subarrays — works but too slow.
> - Prefix sum array without hash map: still O(n²) for lookup.
> - Key insight: the `{0: 1}` initialization handles the case where a prefix starting from index 0 already sums to `k`.

---

### Contiguous Array (Equal 0s and 1s)

> [!example] Problem
> Given a binary array nums, return the maximum length of a contiguous subarray with an equal number of 0 and 1.
> 
> **Example 1:**
> ```
> Input: nums = [0,1]
> Output: 2
> Explanation: [0, 1] is the longest contiguous subarray with an equal number of 0 and 1.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,0]
> Output: 2
> Explanation: [0, 1] (or [1, 0]) is a longest contiguous subarray with equal number of 0 and 1.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,1,1,1,1,1,0,0,0]
> Output: 6
> Explanation: [1,1,1,0,0,0] is the longest contiguous subarray with equal number of 0 and 1.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - nums[i] is either 0 or 1.

> [!info] Approach
> Replace 0 with -1. Now "equal 0s and 1s" becomes "subarray sum = 0", which is exactly the prefix sum problem. Track the first index at which each prefix sum occurs. When a prefix sum repeats, the subarray between the two occurrences has sum 0. Initialize `{0: -1}`. For each index, compute prefix sum (treating 0 as -1). If seen before, update `max_len = max(max_len, i - first_seen[prefix])`. Otherwise, store `first_seen[prefix] = i`.

> [!note]- Python Solution
> ```python
> def find_max_length(nums):
>     first_seen = {0: -1}
>     prefix = 0
>     max_len = 0
>     for i, num in enumerate(nums):
>         prefix += 1 if num == 1 else -1
>         if prefix in first_seen:
>             max_len = max(max_len, i - first_seen[prefix])
>         else:
>             first_seen[prefix] = i
>     return max_len
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Brute force O(n²) — enumerate all subarrays and count 0s/1s.
> - Key insight: storing only the *first* occurrence of each prefix sum maximises the subarray length.

---

### Product of Array Except Self (no division) `🔥 Google`

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

> [!info] Approach
> Division breaks on zeros. Without it, for each position we need the product of everything to the left and to the right. Two passes. First pass (left to right) builds the running left-product into the output array. Second pass (right to left) multiplies in the running right-product in-place. `output[i]` after left pass = product of `nums[0..i-1]`. Then walk right to left with a `right_product` variable, multiply `output[i] *= right_product`, then `right_product *= nums[i]`.

> [!note]- Python Solution
> ```python
> def product_except_self(nums):
>     n = len(nums)
>     output = [1] * n
>     left_product = 1
>     for i in range(n):
>         output[i] = left_product
>         left_product *= nums[i]
>     right_product = 1
>     for i in range(n - 1, -1, -1):
>         output[i] *= right_product
>         right_product *= nums[i]
>     return output
> ```

> [!success] Complexity
> Time O(n), Space O(1) extra (output array doesn't count).

> [!tip] Alternatives
> - With division: count zeros separately, handle zero/two-zeros edge cases. More complex logic.
> - Three arrays (left products, right products, output): O(n) space but same idea, just less elegant.

---

## See Also

[[sliding-window]] | [[two-pointers]] | [[binary-search]] | [[hashing]] | [[sorting]]
