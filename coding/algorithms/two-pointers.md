---
tags: [coding, algorithms, two-pointers]
topic: Two Pointers
difficulty: mixed
---

# Two Pointers — Problem Set

---

## Opposite Ends (Sorted Array)

> [!info] Approach
> On a sorted array, `arr[lo] + arr[hi]` is controlled: too small → move `lo` right (increase); too large → move `hi` left (decrease). Every comparison eliminates an entire row or column of pairs, reducing O(n²) brute force to O(n).

---

### Two Sum II — Input Array is Sorted (LC 167)

> [!example] Problem
> Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.
> Return the indices of the two numbers, index1 and index2, added by one as an integer array [index1, index2] of length 2.
> The tests are generated such that there is exactly one solution. You may not use the same element twice.
> Your solution must use only constant extra space.
> 
> **Example 1:**
> ```
> Input: numbers = [2,7,11,15], target = 9
> Output: [1,2]
> Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
> ```
> 
> **Example 2:**
> ```
> Input: numbers = [2,3,4], target = 6
> Output: [1,3]
> Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].
> ```
> 
> **Example 3:**
> ```
> Input: numbers = [-1,0], target = -1
> Output: [1,2]
> Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].
> ```
> 
> **Constraints:**
> - 2 <= numbers.length <= 3 * 10^4
> - -1000 <= numbers[i] <= 1000
> - numbers is sorted in non-decreasing order.
> - -1000 <= target <= 1000
> - The tests are generated such that there is exactly one solution.

> [!info] Approach
> Array is sorted — sum is monotonically controlled by which endpoints we choose. Brute force O(n²) is unnecessary. Converging pointers `lo = 0, hi = n-1`. Sum < target → `lo += 1`; sum > target → `hi -= 1`; sum == target → return. Each step either finds the answer or eliminates at least one impossible pair. Total: O(n) steps.


> [!note]- Python Solution
> ```python
> def two_sum_sorted(numbers, target):
>     lo, hi = 0, len(numbers) - 1
>     while lo < hi:
>         s = numbers[lo] + numbers[hi]
>         if s == target:
>             return [lo + 1, hi + 1]   # problem wants 1-based indices
>         elif s < target:
>             lo += 1
>         else:
>             hi -= 1
>     return []   # guaranteed to find
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> HashMap O(n) time + O(n) space — use when array is unsorted; sorted input makes two pointers strictly better.

---

### 3Sum (LC 15)

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
> O(n³) brute force is too slow. Fix one element; remaining two-sum on sorted subarray reduces to O(n²) total. Sort array. For each anchor `i`, run converging two-pointer on `[i+1, n-1]`. Skip duplicate anchors (`nums[i] == nums[i-1]`). On finding a triplet, skip duplicate inner pointers before advancing.


> [!note]- Python Solution
> ```python
> def three_sum(nums):
>     nums.sort()
>     result = []
>     for i in range(len(nums) - 2):
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue   # skip duplicate anchor
>         lo, hi = i + 1, len(nums) - 1
>         while lo < hi:
>             s = nums[i] + nums[lo] + nums[hi]
>             if s == 0:
>                 result.append([nums[i], nums[lo], nums[hi]])
>                 while lo < hi and nums[lo] == nums[lo + 1]: lo += 1
>                 while lo < hi and nums[hi] == nums[hi - 1]: hi -= 1
>                 lo += 1; hi -= 1
>             elif s < 0:
>                 lo += 1
>             else:
>                 hi -= 1
>     return result
> ```

> [!success] Complexity
> O(n²) time, O(1) extra space (output excluded).

> [!tip] Alternatives
> HashSet for the inner search — same O(n²) but O(n) space; sorting + two-pointer is cache-friendlier.

---

### 4Sum (LC 18)

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
> Fix two anchors, run two-pointer for the remaining pair. O(n³) total. Double outer loop (indices `i`, `j`), two-pointer inner loop `[j+1, n-1]`. Deduplicate both outer anchors separately. Same skip-duplicate pattern as 3Sum on inner pointers.


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
>             lo, hi = j + 1, n - 1
>             while lo < hi:
>                 s = nums[i] + nums[j] + nums[lo] + nums[hi]
>                 if s == target:
>                     result.append([nums[i], nums[j], nums[lo], nums[hi]])
>                     while lo < hi and nums[lo] == nums[lo + 1]: lo += 1
>                     while lo < hi and nums[hi] == nums[hi - 1]: hi -= 1
>                     lo += 1; hi -= 1
>                 elif s < target:
>                     lo += 1
>                 else:
>                     hi -= 1
>     return result
> ```

> [!success] Complexity
> O(n³) time, O(1) extra space.

> [!tip] Alternatives
> HashMap approach — same asymptotic; k-sum generalizes recursively to O(n^(k-1)).

---

### Container With Most Water (LC 11)

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
> Volume = `min(height[lo], height[hi]) * (hi - lo)`. Moving the taller bar inward can only decrease or keep width the same while min height can only stay equal or decrease — it can never improve the result. So always move the shorter bar. Start with widest container `lo=0, hi=n-1`. Move the shorter side inward. `if height[lo] <= height[hi]: lo += 1` else `hi -= 1`. Record max at each step.


> [!note]- Python Solution
> ```python
> def max_area(height):
>     lo, hi = 0, len(height) - 1
>     best = 0
>     while lo < hi:
>         area = min(height[lo], height[hi]) * (hi - lo)
>         best = max(best, area)
>         if height[lo] <= height[hi]:
>             lo += 1   # move shorter bar; taller side moving can't improve
>         else:
>             hi -= 1
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> O(n²) brute force — check all pairs. No better than O(n) is known.

---

### Trapping Rain Water (LC 42)

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
> Water at position `i` = `min(max_left, max_right) - height[i]`. Two pointers maintain running left/right maxima without two passes. Converging pointers. Whichever side has the smaller max — that side's water is determined by its own max (the other side can only be higher). Process that side. `if left_max <= right_max: water += left_max - height[lo]; lo += 1` else process right side.


> [!note]- Python Solution
> ```python
> def trap(height):
>     lo, hi = 0, len(height) - 1
>     left_max = right_max = 0
>     water = 0
>     while lo < hi:
>         if height[lo] <= height[hi]:
>             left_max = max(left_max, height[lo])
>             water += left_max - height[lo]
>             lo += 1
>         else:
>             right_max = max(right_max, height[hi])
>             water += right_max - height[hi]
>             hi -= 1
>     return water
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Precompute prefix/suffix max arrays O(n) time + O(n) space; monotonic stack O(n) time + O(n) space — both more complex than two-pointer.

---

## Same Direction (Fast/Slow)

> [!info] Approach
> A `read` pointer scans every element; a `write` pointer only advances when the current element should be kept. The gap between them encodes how many elements have been removed. Both move left-to-right, giving O(n) total.

---

### Remove Duplicates from Sorted Array (LC 26)

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
> Array is sorted — duplicates are contiguous. A write pointer marks the last accepted position. `write = 1` (index 0 always kept). For each `read >= 1`, copy to `write` only if `nums[read] != nums[read-1]`. Each non-duplicate advances `write`. Duplicates are simply skipped.


> [!note]- Python Solution
> ```python
> def remove_duplicates(nums):
>     if not nums:
>         return 0
>     write = 1
>     for read in range(1, len(nums)):
>         if nums[read] != nums[read - 1]:
>             nums[write] = nums[read]
>             write += 1
>     return write
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Python `list(dict.fromkeys(nums))` — not in-place; interviewer expects in-place two-pointer.

---

### Remove Element (LC 27)

> [!example] Problem
> Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the elements may be changed. Then return the number of elements in nums which are not equal to val.
> Consider the number of elements in nums which are not equal to val be k, to get accepted, you need to do the following things:
> Custom Judge:
> The judge will test your solution with the following code:
> If all assertions pass, then your solution will be accepted.
> 
> **Example 1:**
> ```
> int[] nums = [...]; // Input array
> int val = ...; // Value to remove
> int[] expectedNums = [...]; // The expected answer with correct length.
>                             // It is sorted with no values equaling val.
> 
> int k = removeElement(nums, val); // Calls your implementation
> 
> assert k == expectedNums.length;
> sort(nums, 0, k); // Sort the first k elements of nums
> for (int i = 0; i < actualLength; i++) {
>     assert nums[i] == expectedNums[i];
> }
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,2,3], val = 3
> Output: 2, nums = [2,2,_,_]
> Explanation: Your function should return k = 2, with the first two elements of nums being 2.
> It does not matter what you leave beyond the returned k (hence they are underscores).
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,1,2,2,3,0,4,2], val = 2
> Output: 5, nums = [0,1,4,0,3,_,_,_]
> Explanation: Your function should return k = 5, with the first five elements of nums containing 0, 0, 1, 3, and 4.
> Note that the five elements can be returned in any order.
> It does not matter what you leave beyond the returned k (hence they are underscores).
> ```
> 
> **Constraints:**
> - 0 <= nums.length <= 100
> - 0 <= nums[i] <= 50
> - 0 <= val <= 100

> [!info] Approach
> Need to compact array without extra space. Read scans forward; write only advances on non-val elements. `write = 0`. For each `read`, if `nums[read] != val` → copy to `nums[write]` and `write += 1`. Alternatively, swap with the end when val is found — useful when val is rare (avoids shifting).


> [!note]- Python Solution
> ```python
> def remove_element(nums, val):
>     write = 0
>     for read in range(len(nums)):
>         if nums[read] != val:
>             nums[write] = nums[read]
>             write += 1
>     return write
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Swap-with-end variant O(n) — fewer writes when val is rare but order isn't preserved.

---

### Move Zeroes (LC 283)

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
> Two-step: compact non-zeros forward (remove-element pattern), then fill tail with zeros. `write` pointer collects non-zeros. After loop, fill `nums[write:]` with zeros. Avoids unnecessary writes for zeros — write pointer skips over zero positions and fills at the end.


> [!note]- Python Solution
> ```python
> def move_zeroes(nums):
>     write = 0
>     for read in range(len(nums)):
>         if nums[read] != 0:
>             nums[write] = nums[read]
>             write += 1
>     for i in range(write, len(nums)):
>         nums[i] = 0
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Swap `nums[write]` and `nums[read]` when `nums[read] != 0` — single pass but does redundant swaps of 0s.

---

### Squares of a Sorted Array (LC 977)

> [!example] Problem
> Given an integer array nums sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.
> 
> **Example 1:**
> ```
> Input: nums = [-4,-1,0,3,10]
> Output: [0,1,9,16,100]
> Explanation: After squaring, the array becomes [16,1,0,9,100].
> After sorting, it becomes [0,1,9,16,100].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [-7,-3,2,3,11]
> Output: [4,9,9,49,121]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - -10^4 <= nums[i] <= 10^4
> - nums is sorted in non-decreasing order.

> [!info] Approach
> Squares of negatives can be large. Largest squares are at the two ends. Fill result from the back. Converging pointers from both ends. Compare absolute values; place the larger square at `result[pos]` and advance that pointer. `pos = n-1`. While `lo <= hi`: if `abs(nums[lo]) >= abs(nums[hi])` → `result[pos] = nums[lo]**2; lo += 1`; else process hi.


> [!note]- Python Solution
> ```python
> def sorted_squares(nums):
>     n = len(nums)
>     result = [0] * n
>     lo, hi = 0, n - 1
>     pos = n - 1
>     while lo <= hi:
>         if abs(nums[lo]) >= abs(nums[hi]):
>             result[pos] = nums[lo] ** 2
>             lo += 1
>         else:
>             result[pos] = nums[hi] ** 2
>             hi -= 1
>         pos -= 1
>     return result
> ```

> [!success] Complexity
> O(n) time, O(n) space (output array).

> [!tip] Alternatives
> Square all then sort O(n log n) — simple but unnecessary given sorted input.

---

## Partition / Dutch National Flag

---

### Sort Colors (LC 75)

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
> Standard sort is O(n log n). Three distinct values allow O(n) single-pass partitioning. Three pointers: `lo` (next 0 position), `mid` (current element), `hi` (next 2 position from right). Process `nums[mid]`: if 0 → swap with `lo`, advance both `lo` and `mid`; if 1 → advance `mid` only; if 2 → swap with `hi`, decrement `hi` but do NOT advance `mid` (swapped element is unseen).


> [!note]- Python Solution
> ```python
> def sort_colors(nums):
>     lo, mid, hi = 0, 0, len(nums) - 1
>     while mid <= hi:
>         if nums[mid] == 0:
>             nums[lo], nums[mid] = nums[mid], nums[lo]
>             lo += 1
>             mid += 1
>         elif nums[mid] == 1:
>             mid += 1
>         else:  # nums[mid] == 2
>             nums[mid], nums[hi] = nums[hi], nums[mid]
>             hi -= 1
>             # do NOT increment mid: swapped element from hi is unseen
> ```

> [!success] Complexity
> O(n) time, O(1) space. Single pass.

> [!tip] Alternatives
> Count occurrences then overwrite — two passes, also O(n); DNF is strictly single-pass. Standard sort O(n log n) — overkill.

---

## Linked List Two Pointers

> [!info] Approach
> Linked lists lack random access. Two pointers with different speeds (fast/slow) or different start offsets simulate the "looking ahead" that indices would provide in arrays.

---

### Linked List Cycle (LC 141)

> [!example] Problem
> Given head, the head of a linked list, determine if the linked list has a cycle in it.
> There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to. Note that pos is not passed as a parameter.
> Return true if there is a cycle in the linked list. Otherwise, return false.
> 
> **Example 1:**
> ```
> Input: head = [3,2,0,-4], pos = 1
> Output: true
> Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2], pos = 0
> Output: true
> Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.
> ```
> 
> **Example 3:**
> ```
> Input: head = [1], pos = -1
> Output: false
> Explanation: There is no cycle in the linked list.
> ```
> 
> **Constraints:**
> - The number of the nodes in the list is in the range [0, 10^4].
> - -10^5 <= Node.val <= 10^5
> - pos is -1 or a valid index in the linked-list.

> [!info] Approach
> No random access → can't track visited nodes without O(n) space. Floyd's: if a cycle exists, a faster pointer will lap the slower one. `slow` moves 1 step/iteration; `fast` moves 2. If they meet → cycle. If `fast` reaches None → no cycle. Check `fast and fast.next` before each step to avoid null pointer dereference.


> [!note]- Python Solution
> ```python
> from typing import Optional
> 
> class ListNode:
>     def __init__(self, val=0, next=None):
>         self.val = val
>         self.next = next
> 
> def has_cycle(head):
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>         if slow is fast:
>             return True
>     return False
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> HashSet of visited nodes O(n) space — simpler code but violates space constraint.

---

### Find Duplicate Number — Floyd's (LC 287)

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
> Treat the array as a function `f(i) = nums[i]` — following indices creates a linked list with a cycle (since one value appears twice, two indices map to the same "next"). Floyd's cycle detection finds the cycle entry = duplicate. Phase 1: find meeting point (inside cycle). Phase 2: reset one pointer to 0, step both by 1 until they meet — meeting point is the duplicate. Phase 1 uses `slow = nums[slow]; fast = nums[nums[fast]]`. Phase 2: `slow = 0; while slow != fast: slow = nums[slow]; fast = nums[fast]`.


> [!note]- Python Solution
> ```python
> def find_duplicate(nums):
>     # Phase 1: detect meeting point inside cycle
>     slow = fast = nums[0]
>     while True:
>         slow = nums[slow]
>         fast = nums[nums[fast]]
>         if slow == fast:
>             break
> 
>     # Phase 2: find cycle entry (= duplicate value)
>     slow = nums[0]
>     while slow != fast:
>         slow = nums[slow]
>         fast = nums[fast]
>     return slow
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Sort O(n log n); HashSet O(n) space; binary search on value O(n log n) — all inferior for this constraint set.

---

### Middle of the Linked List (LC 876)

> [!example] Problem
> Given the head of a singly linked list, return the middle node of the linked list.
> If there are two middle nodes, return the second middle node.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5]
> Output: [3,4,5]
> Explanation: The middle node of the list is node 3.
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2,3,4,5,6]
> Output: [4,5,6]
> Explanation: Since the list has two middle nodes with values 3 and 4, we return the second one.
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [1, 100].
> - 1 <= Node.val <= 100

> [!info] Approach
> Length unknown without full traversal. Fast/slow pointers: by the time `fast` reaches the end, `slow` is at the midpoint. `fast` moves 2 steps per iteration; `slow` moves 1. When `fast` or `fast.next` is None, `slow` is at the middle. Condition `while fast and fast.next` — for even-length lists, `slow` stops at the second middle (upper-mid). This matches the problem requirement.


> [!note]- Python Solution
> ```python
> def middle_node(head):
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>     return slow
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Count length then traverse `n//2` — two passes, same O(n) time.

---

### Remove Nth Node From End of List (LC 19)

> [!example] Problem
> Given the head of a linked list, remove the nth node from the end of the list and return its head.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5], n = 2
> Output: [1,2,3,5]
> ```
> 
> **Example 2:**
> ```
> Input: head = [1], n = 1
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: head = [1,2], n = 1
> Output: [1]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is sz.
> - 1 <= sz <= 30
> - 0 <= Node.val <= 100
> - 1 <= n <= sz

> [!info] Approach
> To reach the nth-from-end, the fast pointer must be exactly n steps ahead of slow. When fast reaches the end, slow is at the node before the target. Advance `fast` n+1 steps (so slow stops at the node *before* the one to delete). Then move both until `fast` is None. Use a dummy head to handle edge case of deleting the first node. `slow.next = slow.next.next` removes the target.


> [!note]- Python Solution
> ```python
> def remove_nth_from_end(head, n):
>     dummy = ListNode(0, head)
>     slow = fast = dummy
>     # Advance fast n+1 steps so slow stops before target
>     for _ in range(n + 1):
>         fast = fast.next
>     while fast:
>         slow = slow.next
>         fast = fast.next
>     slow.next = slow.next.next   # remove nth from end
>     return dummy.next
> ```

> [!success] Complexity
> O(L) time where L is list length. O(1) space.

> [!tip] Alternatives
> Two-pass — count length then delete at `L - n`; same O(L) but two traversals.

---

## Palindrome Two Pointers

---

### Valid Palindrome II (LC 680)

> [!example] Problem
> Given a string s, return true if the s can be palindrome after deleting at most one character from it.
> 
> **Example 1:**
> ```
> Input: s = "aba"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: s = "abca"
> Output: true
> Explanation: You could delete the character 'c'.
> ```
> 
> **Example 3:**
> ```
> Input: s = "abc"
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s consists of lowercase English letters.

> [!info] Approach
> A standard two-pointer palindrome check fails at the first mismatch. But we have one deletion budget — try skipping s[l] OR s[r] and check if either remainder is a palindrome. Two pointers from both ends. On mismatch at (l, r): check is_palindrome(s, l+1, r) OR is_palindrome(s, l, r-1). Helper function checks palindrome in a range. O(n) total — we branch at most once.


> [!note]- Python Solution
> ```python
> def valid_palindrome(s):
>     def is_palindrome(s, l, r):
>         while l < r:
>             if s[l] != s[r]:
>                 return False
>             l += 1
>             r -= 1
>         return True
> 
>     l, r = 0, len(s) - 1
>     while l < r:
>         if s[l] != s[r]:
>             # one deletion budget: skip left or skip right
>             return is_palindrome(s, l + 1, r) or is_palindrome(s, l, r - 1)
>         l += 1
>         r -= 1
>     return True
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> DP O(n²) — finds longest palindromic subsequence but overkill here; brute force try all single deletions O(n²) — unnecessary when branching once suffices.

---

### 3Sum Closest (LC 16)

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
> Same scaffold as 3Sum — fix anchor, converging two-pointer on remainder. Track closest sum instead of exact match. Sort array. For each anchor `i`, run `lo = i+1, hi = n-1`. Update best if `|s - target| < |best - target|`. Move pointer based on whether sum is too small or too large. If `s < target` → `lo += 1` (need larger sum); if `s > target` → `hi -= 1`; if equal → return immediately.


> [!note]- Python Solution
> ```python
> def three_sum_closest(nums, target):
>     nums.sort()
>     best = float('inf')
>     for i in range(len(nums) - 2):
>         lo, hi = i + 1, len(nums) - 1
>         while lo < hi:
>             s = nums[i] + nums[lo] + nums[hi]
>             if abs(s - target) < abs(best - target):
>                 best = s
>             if s < target:
>                 lo += 1
>             elif s > target:
>                 hi -= 1
>             else:
>                 return s   # exact match
>     return best
> ```

> [!success] Complexity
> O(n²) time, O(1) extra space.

> [!tip] Alternatives
> Brute force O(n³) — no benefit; three nested loops. Sorting + two-pointer is optimal.

---

## Hash Map Two-Sum Variant

---

### 4Sum II (LC 454)

> [!example] Problem
> Given four integer arrays nums1, nums2, nums3, and nums4 all of length n, return the number of tuples (i, j, k, l) such that
> 
> **Example 1:**
> ```
> Input: nums1 = [1,2], nums2 = [-2,-1], nums3 = [-1,2], nums4 = [0,2]
> Output: 2
> Explanation:
> The two tuples are:
> 1. (0, 0, 0, 1) -> nums1[0] + nums2[0] + nums3[0] + nums4[1] = 1 + (-2) + (-1) + 2 = 0
> 2. (1, 1, 0, 0) -> nums1[1] + nums2[1] + nums3[0] + nums4[0] = 2 + (-1) + (-1) + 0 = 0
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [0], nums2 = [0], nums3 = [0], nums4 = [0]
> Output: 1
> ```
> 
> **Constraints:**
> - n == nums1.length
> - n == nums2.length
> - n == nums3.length
> - n == nums4.length
> - 1 <= n <= 200
> - -228 <= nums1[i], nums2[i], nums3[i], nums4[i] <= 228

> [!info] Approach
> O(n⁴) brute force is infeasible. Split into two pairs: store all A+B sums in a hash map, then check if -(C+D) exists in it. Build `count` map of all `a + b` sums → frequency. For every `c + d`, add `count[-(c+d)]` to result. Two nested loops each O(n²) rather than O(n⁴). This is a hash-map complement pattern, not classic two-pointer, but pairs with kSum problems.


> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def four_sum_count(
>     nums1: list[int], nums2: list[int],
>     nums3: list[int], nums4: list[int]
> ) -> int:
>     ab = defaultdict(int)
>     for a in nums1:
>         for b in nums2:
>             ab[a + b] += 1
>     count = 0
>     for c in nums3:
>         for d in nums4:
>             count += ab[-(c + d)]
>     return count
> ```

> [!success] Complexity
> O(n²) time, O(n²) space for the hash map.

> [!tip] Alternatives
> Sort all four arrays and use four pointers — O(n³) and complex; hash-map split is strictly better here.

---

## Partition Variants

---

### Partition Array According to Given Pivot (LC 2161)

> [!example] Problem
> You are given a 0-indexed integer array nums and an integer pivot. Rearrange nums such that the following conditions are satisfied:
> Return nums after the rearrangement.
> 
> **Example 1:**
> ```
> Input: nums = [9,12,5,10,14,3,10], pivot = 10
> Output: [9,5,3,10,10,12,14]
> Explanation: 
> The elements 9, 5, and 3 are less than the pivot so they are on the left side of the array.
> The elements 12 and 14 are greater than the pivot so they are on the right side of the array.
> The relative ordering of the elements less than and greater than pivot is also maintained. [9, 5, 3] and [12, 14] are the respective orderings.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [-3,4,3,2], pivot = 2
> Output: [-3,2,4,3]
> Explanation: 
> The element -3 is less than the pivot so it is on the left side of the array.
> The elements 4 and 3 are greater than the pivot so they are on the right side of the array.
> The relative ordering of the elements less than and greater than pivot is also maintained. [-3] and [4, 3] are the respective orderings.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^6 <= nums[i] <= 10^6
> - pivot equals to an element of nums.

> [!info] Approach
> Relative order must be preserved, so an in-place swap (DNF-style) would break ordering. A stable partition using three buckets is correct and O(n). Single pass: collect elements into `less`, `equal`, `greater` lists. Concatenate. `less + equal + greater` preserves original relative order within each group.


> [!note]- Python Solution
> ```python
> def pivot_array(nums, pivot):
>     less, equal, greater = [], [], []
>     for x in nums:
>         if x < pivot:
>             less.append(x)
>         elif x == pivot:
>             equal.append(x)
>         else:
>             greater.append(x)
>     return less + equal + greater
> ```

> [!success] Complexity
> O(n) time, O(n) space.

> [!tip] Alternatives
> In-place DNF (LC 75 style) — O(1) extra space but does not preserve relative order; only valid when order doesn't matter.

---

### Minimum Difference Between Highest and Lowest of K Scores (LC 1984)

> [!example] Problem
> You are given a 0-indexed integer array nums, where nums[i] represents the score of the ith student. You are also given an integer k.
> Pick the scores of any k students from the array so that the difference between the highest and the lowest of the k scores is minimized.
> Return the minimum possible difference.
> 
> **Example 1:**
> ```
> Input: nums = [90], k = 1
> Output: 0
> Explanation: There is one way to pick score(s) of one student:
> - [90]. The difference between the highest and lowest score is 90 - 90 = 0.
> The minimum possible difference is 0.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [9,4,1,7], k = 2
> Output: 2
> Explanation: There are six ways to pick score(s) of two students:
> - [9,4,1,7]. The difference between the highest and lowest score is 9 - 4 = 5.
> - [9,4,1,7]. The difference between the highest and lowest score is 9 - 1 = 8.
> - [9,4,1,7]. The difference between the highest and lowest score is 9 - 7 = 2.
> - [9,4,1,7]. The difference between the highest and lowest score is 4 - 1 = 3.
> - [9,4,1,7]. The difference between the highest and lowest score is 7 - 4 = 3.
> - [9,4,1,7]. The difference between the highest and lowest score is 7 - 1 = 6.
> The minimum possible difference is 2.
> ```
> 
> **Constraints:**
> - 1 <= k <= nums.length <= 1000
> - 0 <= nums[i] <= 10^5

> [!info] Approach
> After sorting, the k elements with minimum spread must be contiguous (any non-contiguous selection can be improved by replacing the outlier with a neighbor). So the answer is the minimum of `nums[i+k-1] - nums[i]` over all valid windows. Sort then slide a fixed window of size k, record `nums[i + k - 1] - nums[i]`. This is a two-pointer fixed window (lo = i, hi = i + k - 1). Single pass after sort.


> [!note]- Python Solution
> ```python
> def minimum_difference(nums, k):
>     nums.sort()
>     return min(nums[i + k - 1] - nums[i] for i in range(len(nums) - k + 1))
> ```

> [!success] Complexity
> O(n log n) time (sort dominates), O(1) extra space.

> [!tip] Alternatives
> Brute force all k-subsets — exponential; sorting + sliding window is the canonical approach.

---

## Sorted Array / Two-Pointer Greedy

---

### Number of Subsequences That Satisfy the Given Sum Condition (LC 1498)

> [!example] Problem
> You are given an array of integers nums and an integer target.
> Return the number of non-empty subsequences of nums such that the sum of the minimum and maximum element on it is less or equal to target. Since the answer may be too large, return it modulo 109 + 7.
> 
> **Example 1:**
> ```
> Input: nums = [3,5,6,7], target = 9
> Output: 4
> Explanation: There are 4 subsequences that satisfy the condition.
> [3] -> Min value + max value  (3 + 5  (3 + 6  (3 + 6 <= 9)
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,3,6,8], target = 10
> Output: 6
> Explanation: There are 6 subsequences that satisfy the condition. (nums can have repeated numbers).
> [3] , [3] , [3,3], [3,6] , [3,6] , [3,3,6]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [2,3,3,4,6,7], target = 12
> Output: 61
> Explanation: There are 63 non-empty subsequences, two of them do not satisfy the condition ([6,7], [7]).
> Number of valid subsequences (63 - 2 = 61).
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - 1 <= nums[i] <= 10^6
> - 1 <= target <= 10^6

> [!info] Approach
> After sorting, for a fixed minimum at index `lo`, find the furthest `hi` where `nums[lo] + nums[hi] <= target`. Every subset of elements between `lo+1` and `hi` can pair with `nums[lo]` as min — there are `2^(hi-lo)` such subsequences. Converging two-pointer. Precompute powers of 2 mod MOD. For each `lo`, binary-search or slide `hi` left until valid; add `pow2[hi - lo]`. `hi` never moves right (as `lo` increases, the valid range can only shrink), so two-pointer is O(n).


> [!note]- Python Solution
> ```python
> def num_subseq(nums, target):
>     MOD = 10**9 + 7
>     nums.sort()
>     n = len(nums)
>     pow2 = [1] * n
>     for i in range(1, n):
>         pow2[i] = pow2[i - 1] * 2 % MOD
> 
>     lo, hi = 0, n - 1
>     result = 0
>     while lo <= hi:
>         if nums[lo] + nums[hi] <= target:
>             result = (result + pow2[hi - lo]) % MOD
>             lo += 1
>         else:
>             hi -= 1
>     return result
> ```

> [!success] Complexity
> O(n log n) time (sort), O(n) space for power table.

> [!tip] Alternatives
> Binary search for `hi` given each `lo` — O(n log n) same asymptotic but with log factor in the main loop; sliding hi is cleaner.

---

### Boats to Save People (LC 881)

> [!example] Problem
> You are given an array people where people[i] is the weight of the ith person, and an infinite number of boats where each boat can carry a maximum weight of limit. Each boat carries at most two people at the same time, provided the sum of the weight of those people is at most limit.
> Return the minimum number of boats to carry every given person.
> 
> **Example 1:**
> ```
> Input: people = [1,2], limit = 3
> Output: 1
> Explanation: 1 boat (1, 2)
> ```
> 
> **Example 2:**
> ```
> Input: people = [3,2,2,1], limit = 3
> Output: 3
> Explanation: 3 boats (1, 2), (2) and (3)
> ```
> 
> **Example 3:**
> ```
> Input: people = [3,5,3,4], limit = 5
> Output: 4
> Explanation: 4 boats (3), (3), (4), (5)
> ```
> 
> **Constraints:**
> - 1 <= people.length <= 5 * 10^4
> - 1 <= people[i] <= limit <= 3 * 10^4

> [!info] Approach
> Greedily pair the heaviest person with the lightest. If they fit together, both board one boat; otherwise the heaviest goes alone. Sorting enables this pairing in O(n). Sort weights. `lo = 0, hi = n-1`. If `weights[lo] + weights[hi] <= limit` → both fit, `lo += 1`; always `hi -= 1` (heaviest always takes a boat). Boats += 1 per iteration. The greedy is optimal: the heaviest person must go on some boat — it's never worse to pair them with the lightest available.


> [!note]- Python Solution
> ```python
> def num_rescue_boats(people, limit):
>     people.sort()
>     lo, hi = 0, len(people) - 1
>     boats = 0
>     while lo <= hi:
>         if people[lo] + people[hi] <= limit:
>             lo += 1   # lightest fits with heaviest
>         hi -= 1       # heaviest always takes a boat
>         boats += 1
>     return boats
> ```

> [!success] Complexity
> O(n log n) time (sort), O(1) space.

> [!tip] Alternatives
> Priority queue / greedy simulation — O(n log n) but more complex; sorted two-pointer is cleaner.

---

### Max Number of K-Sum Pairs (LC 1679)

> [!example] Problem
> You are given an integer array nums and an integer k.
> In one operation, you can pick two numbers from the array whose sum equals k and remove them from the array.
> Return the maximum number of operations you can perform on the array.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3,4], k = 5
> Output: 2
> Explanation: Starting with nums = [1,2,3,4]:
> - Remove numbers 1 and 4, then nums = [2,3]
> - Remove numbers 2 and 3, then nums = []
> There are no more pairs that sum up to 5, hence a total of 2 operations.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,1,3,4,3], k = 6
> Output: 1
> Explanation: Starting with nums = [3,1,3,4,3]:
> - Remove the first two 3's, then nums = [1,4,3]
> There are no more pairs that sum up to 6, hence a total of 1 operation.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - 1 <= nums[i] <= 10^9
> - 1 <= k <= 10^9

> [!info] Approach
> Each operation removes a pair summing to k. After sorting, the same converging two-pointer as Two Sum II finds all such pairs greedily. Sort. `lo = 0, hi = n-1`. If sum == k → count++, lo++, hi--; if sum < k → lo++; if sum > k → hi--. Greedy pairing of smallest + largest exhausts all valid pairs optimally (each element can only be used once).


> [!note]- Python Solution
> ```python
> def max_operations(nums, k):
>     nums.sort()
>     lo, hi = 0, len(nums) - 1
>     ops = 0
>     while lo < hi:
>         s = nums[lo] + nums[hi]
>         if s == k:
>             ops += 1
>             lo += 1
>             hi -= 1
>         elif s < k:
>             lo += 1
>         else:
>             hi -= 1
>     return ops
> ```

> [!success] Complexity
> O(n log n) time (sort), O(1) space.

> [!tip] Alternatives
> HashMap: count frequencies, for each x check if k-x exists — O(n) time, O(n) space. Use when extra space is acceptable and sorting is undesirable.

---

### Bag of Tokens (LC 948)

> [!example] Problem
> You start with an initial power of power, an initial score of 0, and a bag of tokens given as an integer array tokens, where each tokens[i] denotes the value of tokeni.
> Your goal is to maximize the total score by strategically playing these tokens. In one move, you can play an unplayed token in one of the two ways (but not both for the same token):
> Return the maximum possible score you can achieve after playing any number of tokens.
> 
> **Example 1:**
> ```
> Input: tokens = [100], power = 50
> Output: 0
> Explanation : Since your score is 0 initially, you cannot play the token face-down. You also cannot play it face-up since your power ( 50 ) is less than tokens[0] ( 100 ).
> ```
> 
> **Example 2:**
> ```
> Input: tokens = [200,100], power = 150
> Output: 1
> Explanation: Play token 1 ( 100 ) face-up, reducing your power to 50 and increasing your score to 1 .
> There is no need to play token 0 , since you cannot play it face-up to add to your score. The maximum score achievable is 1 .
> ```
> 
> **Example 3:**
> ```
> Input: tokens = [100,200,300,400], power = 200
> Output: 2
> Explanation: Play the tokens in this order to get a score of 2 :
> The maximum score achievable is 2 .
> ```
> 
> **Constraints:**
> - 0 <= tokens.length <= 1000
> - 0 <= tokens[i], power < 10^4

> [!info] Approach
> To maximize points, spend power on the cheapest token (face-up) and spend points on the most expensive token to regain power (face-down). Sorting enables greedy selection of cheapest/most-expensive with two pointers. Sort tokens. Greedily: if `power >= tokens[lo]` → play face-up (lo++, points++, power -= tokens[lo]); else if `points > 0` → play face-down (hi--, points--, power += tokens[hi]); else break. Always track `best = max(best, points)` — we may want to stop before spending all points.


> [!note]- Python Solution
> ```python
> def bag_of_tokens_score(tokens, power):
>     tokens.sort()
>     lo, hi = 0, len(tokens) - 1
>     points = 0
>     best = 0
>     while lo <= hi:
>         if power >= tokens[lo]:
>             power -= tokens[lo]
>             points += 1
>             lo += 1
>             best = max(best, points)
>         elif points > 0:
>             power += tokens[hi]
>             points -= 1
>             hi -= 1
>         else:
>             break
>     return best
> ```

> [!success] Complexity
> O(n log n) time (sort), O(1) space.

> [!tip] Alternatives
> DP — token values can be large so DP state space is infeasible; greedy two-pointer is the only practical approach.

---

## Two-Pointer on Strings

---

### Reverse String (LC 344)

> [!example] Problem
> Write a function that reverses a string. The input string is given as an array of characters s.
> You must do this by modifying the input array in-place with O(1) extra memory.
> 
> **Example 1:**
> ```
> Input: s = ["h","e","l","l","o"]
> Output: ["o","l","l","e","h"]
> ```
> 
> **Example 2:**
> ```
> Input: s = ["H","a","n","n","a","h"]
> Output: ["h","a","n","n","a","H"]
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s[i] is a printable ascii character.

> [!info] Approach
> Swapping from both ends converges in n/2 steps — the simplest two-pointer pattern. `lo = 0, hi = n-1`. Swap `s[lo]` and `s[hi]`, advance both, until they meet. Loop condition `lo < hi`; each iteration does one swap and two pointer moves.


> [!note]- Python Solution
> ```python
> def reverse_string(s):
>     lo, hi = 0, len(s) - 1
>     while lo < hi:
>         s[lo], s[hi] = s[hi], s[lo]
>         lo += 1
>         hi -= 1
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Python slice `s[::-1]` — not in-place (creates new list); in-place two-pointer is the expected interview answer.

---

### Long Pressed Name (LC 925)

> [!example] Problem
> Your friend is typing his name into a keyboard. Sometimes, when typing a character c, the key might get long pressed, and the character will be typed 1 or more times.
> You examine the typed characters of the keyboard. Return True if it is possible that it was your friends name, with some characters (possibly none) being long pressed.
> 
> **Example 1:**
> ```
> Input: name = "alex", typed = "aaleex"
> Output: true
> Explanation: 'a' and 'e' in 'alex' were long pressed.
> ```
> 
> **Example 2:**
> ```
> Input: name = "saeed", typed = "ssaaedd"
> Output: false
> Explanation: 'e' must have been pressed twice, but it was not in the typed output.
> ```
> 
> **Constraints:**
> - 1 <= name.length, typed.length <= 1000
> - name and typed consist of only lowercase English letters.

> [!info] Approach
> Both strings share a subsequence structure — `name` characters must appear in `typed` in order, with possible repetitions in `typed`. Two pointers on both strings handles this in a single pass. Pointer `i` on `name`, `j` on `typed`. Advance both when chars match. If `typed[j] == typed[j-1]`, it's a long press — advance `j` only. Otherwise mismatch → false. After the loop, `i` must have consumed all of `name`.


> [!note]- Python Solution
> ```python
> def is_long_pressed_name(name, typed):
>     i = 0
>     for j in range(len(typed)):
>         if i < len(name) and name[i] == typed[j]:
>             i += 1
>         elif j == 0 or typed[j] != typed[j - 1]:
>             return False
>         # else: typed[j] == typed[j-1] — long press, skip
>     return i == len(name)
> ```

> [!success] Complexity
> O(n + m) time where n = len(name), m = len(typed). O(1) space.

> [!tip] Alternatives
> Regex matching — `re.fullmatch` with a pattern built from name; more code, harder to reason about; two-pointer is cleaner.

---

## See Also

[[binary-search]] | [[sliding-window]] | [[array]] | [[linked-list]]
### Reverse Vowels of a String

> [!example] Problem
> Given a string s, reverse only all the vowels in the string and return it.
> The vowels are 'a', 'e', 'i', 'o', and 'u', and they can appear in both lower and upper cases, more than once.
> 
> **Example 1:**
> ```
> Input: s = "IceCreAm"
> Output: "AceCreIm"
> Explanation:
> The vowels in s are ['I', 'e', 'e', 'A'] . On reversing the vowels, s becomes "AceCreIm" .
> ```
> 
> **Example 2:**
> ```
> Input: s = "leetcode"
> Output: "leotcede"
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 3 * 10^5
> - s consist of printable ASCII characters.

> [!info] Approach
> The vowels to swap form a sparse subset, so moving two pointers inward and skipping non-vowels is optimal. Two pointers from the ends; advance each pointer until it points to a vowel, then swap. Maintain a vowel set; while `left < right`, skip non-vowels on both sides and swap the vowel pair.


> [!note]- Python Solution
> ```python
> def reverse_vowels(s):
>     vowels = set("aeiouAEIOU")
>     chars = list(s)
>     left, right = 0, len(chars) - 1
>     while left < right:
>         while left < right and chars[left] not in vowels:
>             left += 1
>         while left < right and chars[right] not in vowels:
>             right -= 1
>         chars[left], chars[right] = chars[right], chars[left]
>         left += 1
>         right -= 1
>     return "".join(chars)
> ```

> [!success] Complexity
> O(n) time, O(n) space for the mutable character list.

> [!tip] Alternatives
> The same two-pointer skip pattern works for palindrome checks, partitioning, and sorted-array pair problems.

---

## Two Pointers — More Problems

### Minimum Operations to Reduce X to Zero (LC 1658)

> [!example] Problem
> You are given an integer array nums and an integer x. In one operation, you can either remove the leftmost or the rightmost element from the array nums and subtract its value from x. Note that this modifies the array for future operations.
> Return the minimum number of operations to reduce x to exactly 0 if it is possible, otherwise, return -1.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,4,2,3], x = 5
> Output: 2
> Explanation: The optimal solution is to remove the last two elements to reduce x to zero.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5,6,7,8,9], x = 4
> Output: -1
> ```
> 
> **Example 3:**
> ```
> Input: nums = [3,2,20,1,1,3], x = 10
> Output: 5
> Explanation: The optimal solution is to remove the last three elements and the first two elements (5 operations in total) to reduce x to zero.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - 1 <= nums[i] <= 10^4
> - 1 <= x <= 10^9

> [!info] Approach
> Removing from both ends to sum to `x` is equivalent to finding the longest subarray in the middle with sum = `total - x`. This is a sliding window on the middle subarray. Find the maximum-length subarray with sum = `total - x`. The answer is `n - max_length`. Two-pointer (sliding window): expand right to grow the window, shrink left when the window sum exceeds `target`. Track the maximum window length where sum equals `target`.


> [!note]- Python Solution
> ```python
> def min_operations(nums, x):
>     target = sum(nums) - x
>     if target < 0:
>         return -1
>     if target == 0:
>         return len(nums)
>     n = len(nums)
>     left = 0
>     current_sum = 0
>     max_len = -1
>     for right in range(n):
>         current_sum += nums[right]
>         while current_sum > target and left <= right:
>             current_sum -= nums[left]
>             left += 1
>         if current_sum == target:
>             max_len = max(max_len, right - left + 1)
>     if max_len == -1:
>         return -1
>     return n - max_len
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Prefix sum + hash map: store prefix sums, search for `prefix[i] == total - x - suffix_sum`. O(n) time but O(n) space.
> - Key insight: the "remove from both ends" framing is a classic redirect — always ask if the complement (middle subarray) is easier.

---

### Boats to Save People (LC 881)

> [!example] Problem
> You are given an array people where people[i] is the weight of the ith person, and an infinite number of boats where each boat can carry a maximum weight of limit. Each boat carries at most two people at the same time, provided the sum of the weight of those people is at most limit.
> Return the minimum number of boats to carry every given person.
> 
> **Example 1:**
> ```
> Input: people = [1,2], limit = 3
> Output: 1
> Explanation: 1 boat (1, 2)
> ```
> 
> **Example 2:**
> ```
> Input: people = [3,2,2,1], limit = 3
> Output: 3
> Explanation: 3 boats (1, 2), (2) and (3)
> ```
> 
> **Example 3:**
> ```
> Input: people = [3,5,3,4], limit = 5
> Output: 4
> Explanation: 4 boats (3), (3), (4), (5)
> ```
> 
> **Constraints:**
> - 1 <= people.length <= 5 * 10^4
> - 1 <= people[i] <= limit <= 3 * 10^4

> [!info] Approach
> Greedy: pair the heaviest person with the lightest person if their combined weight fits. Otherwise, the heaviest person gets a boat alone. Two pointers on a sorted array implements this efficiently. Sort people. Use `left` and `right` pointers. If `people[left] + people[right] <= limit`, both fit — move both pointers. Otherwise, only `right` fits — move only `right`. Each iteration uses one boat. Count iterations until `left > right`.


> [!note]- Python Solution
> ```python
> def num_rescue_boats(people, limit):
>     people.sort()
>     left = 0
>     right = len(people) - 1
>     boats = 0
>     while left <= right:
>         if people[left] + people[right] <= limit:
>             left += 1
>         right -= 1
>         boats += 1
>     return boats
> ```

> [!success] Complexity
> Time O(n log n) for sorting, O(n) for the scan. Space O(1).

> [!tip] Alternatives
> - Greedy with priority queue: overkill — the two-pointer on sorted array is optimal.
> - Key insight: always try to pair the heaviest with the lightest. If they don't fit, the heaviest must go alone.

---

## See Also

[[binary-search]] | [[sorting]] | [[sliding-window]] | [[array]]
