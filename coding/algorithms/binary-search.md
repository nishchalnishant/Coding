---
tags: [coding, algorithms, binary-search]
topic: Binary Search
difficulty: mixed
---

# Binary Search — Problem Set

---

## Lower Bound / Upper Bound

> [!info] Approach
> Lower bound: find the leftmost index where a predicate flips from False to True. Upper bound: find the leftmost index where the value strictly exceeds the target. Both use the same converging template — only the comparison changes.

---

### Search Insert Position (LC 35)

> [!example] Problem
> Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.
> You must write an algorithm with O(log n) runtime complexity.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,5,6], target = 5
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,3,5,6], target = 2
> Output: 1
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,3,5,6], target = 7
> Output: 4
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - -10^4 <= nums[i] <= 10^4
> - nums contains distinct values sorted in ascending order.
> - -10^4 <= target <= 10^4

> [!info] Approach
> Need the leftmost index where `arr[i] >= target` — classic lower bound problem. Binary search with `hi = len(nums)` because the answer may be one past the last element. If `nums[mid] < target` → `lo = mid + 1`; else `hi = mid`. Loop terminates at `lo == hi`.


> [!note]- Python Solution
> ```python
> def search_insert(nums, target):
>     lo, hi = 0, len(nums)
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if nums[mid] < target:
>             lo = mid + 1
>         else:
>             hi = mid
>     return lo
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

> [!tip] Alternatives
> Linear scan O(n) — correct but unnecessary; Python `bisect_left(nums, target)` gives same result.

---

### First Bad Version (LC 278)

> [!example] Problem
> You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.
> Suppose you have n versions [1, 2, ..., n] and you want to find out the first bad one, which causes all the following ones to be bad.
> You are given an API bool isBadVersion(version) which returns whether version is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.
> 
> **Example 1:**
> ```
> Input: n = 5, bad = 4
> Output: 4
> Explanation:
> call isBadVersion(3) -> false
> call isBadVersion(5) -> true
> call isBadVersion(4) -> true
> Then 4 is the first bad version.
> ```
> 
> **Example 2:**
> ```
> Input: n = 1, bad = 1
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= bad <= n <= 2^{31} - 1

> [!info] Approach
> The version sequence has a monotone predicate: False…False, True…True. First True is a lower bound problem. Binary search on `[1, n]`. If `isBadVersion(mid)` is True, the first bad version is at `mid` or earlier. `if isBadVersion(mid): hi = mid` (don't discard mid); else `lo = mid + 1`. Terminates at `lo == hi`.


> [!note]- Python Solution
> ```python
> def first_bad_version(n):
>     lo, hi = 1, n
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if isBadVersion(mid):
>             hi = mid        # mid could be first bad; don't discard
>         else:
>             lo = mid + 1
>     return lo
> ```

> [!success] Complexity
> O(log n) time, O(1) space. Minimizes API calls vs linear O(n) scan.

> [!tip] Alternatives
> Linear scan — exceeds constraints for large n.

---

### Find Smallest Letter Greater Than Target (LC 744)

> [!example] Problem
> You are given an array of characters letters that is sorted in non-decreasing order, and a character target. There are at least two different characters in letters.
> Return the smallest character in letters that is lexicographically greater than target. If such a character does not exist, return the first character in letters.
> 
> **Example 1:**
> ```
> Input: letters = ["c","f","j"], target = "a"
> Output: "c"
> Explanation: The smallest character that is lexicographically greater than 'a' in letters is 'c'.
> ```
> 
> **Example 2:**
> ```
> Input: letters = ["c","f","j"], target = "c"
> Output: "f"
> Explanation: The smallest character that is lexicographically greater than 'c' in letters is 'f'.
> ```
> 
> **Example 3:**
> ```
> Input: letters = ["x","x","y","y"], target = "z"
> Output: "x"
> Explanation: There are no characters in letters that is lexicographically greater than 'z' so we return letters[0].
> ```
> 
> **Constraints:**
> - 2 <= letters.length <= 10^4
> - letters[i] is a lowercase English letter.
> - letters is sorted in non-decreasing order.
> - letters contains at least two different characters.
> - target is a lowercase English letter.

> [!info] Approach
> Upper bound variant — find first index where `letters[i] > target`. Binary search; if `lo` ends at `len(letters)`, no letter qualifies → wrap to `letters[0]`. If `letters[mid] <= target` → `lo = mid + 1`; else `hi = mid`. Answer is `letters[lo % len]`.


> [!note]- Python Solution
> ```python
> def next_greatest_letter(letters, target):
>     lo, hi = 0, len(letters)
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if letters[mid] <= target:
>             lo = mid + 1
>         else:
>             hi = mid
>     return letters[lo % len(letters)]  # modulo handles circular wrap
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

> [!tip] Alternatives
> `bisect_right` gives the insertion index directly; linear scan O(n).

---

### H-Index II (LC 275)

> [!example] Problem
> Given an array of integers citations where citations[i] is the number of citations a researcher received for their ith paper and citations is sorted in non-descending order, return the researcher's h-index.
> According to the definition of h-index on Wikipedia: The h-index is defined as the maximum value of h such that the given researcher has published at least h papers that have each been cited at least h times.
> You must write an algorithm that runs in logarithmic time.
> 
> **Example 1:**
> ```
> Input: citations = [0,1,3,5,6]
> Output: 3
> Explanation: [0,1,3,5,6] means the researcher has 5 papers in total and each of them had received 0, 1, 3, 5, 6 citations respectively.
> Since the researcher has 3 papers with at least 3 citations each and the remaining two with no more than 3 citations each, their h-index is 3.
> ```
> 
> **Example 2:**
> ```
> Input: citations = [1,2,100]
> Output: 2
> ```
> 
> **Constraints:**
> - n == citations.length
> - 1 <= n <= 10^5
> - 0 <= citations[i] <= 1000
> - citations is sorted in ascending order.

> [!info] Approach
> Array is sorted. For index `i`, there are `n - i` papers with at least `citations[i]` citations. Need the leftmost `i` where `citations[i] >= n - i`. Binary search for the leftmost valid index. Then `h = n - i`. If `citations[mid] < n - mid` → not enough citations here → `lo = mid + 1`; else `hi = mid`.


> [!note]- Python Solution
> ```python
> def h_index(citations):
>     n = len(citations)
>     lo, hi = 0, n
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if citations[mid] < n - mid:
>             lo = mid + 1
>         else:
>             hi = mid
>     return n - lo
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

> [!tip] Alternatives
> Linear scan from right O(n); unsorted version (LC 274) requires counting sort + O(n).

---

## Binary Search on Answer (Predicate Pattern)

> [!info] Approach
> When asked to *minimize the maximum* or *maximize the minimum* under a constraint, define a monotone feasibility predicate `f(x)` and binary search on `x` directly. The feasibility check is typically O(n) greedy, making the whole solution O(n log W).

---

### Koko Eating Bananas (LC 875)

> [!example] Problem
> Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.
> Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.
> Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.
> Return the minimum integer k such that she can eat all the bananas within h hours.
> 
> **Example 1:**
> ```
> Input: piles = [3,6,7,11], h = 8
> Output: 4
> ```
> 
> **Example 2:**
> ```
> Input: piles = [30,11,23,4,20], h = 5
> Output: 30
> ```
> 
> **Example 3:**
> ```
> Input: piles = [30,11,23,4,20], h = 6
> Output: 23
> ```
> 
> **Constraints:**
> - 1 <= piles.length <= 10^4
> - piles.length <= h <= 10^9
> - 1 <= piles[i] <= 10^9

> [!info] Approach
> Larger `k` → fewer hours needed. Monotone: if speed `k` works, any speed `k' > k` also works. Binary search on `k`. Search `k` in `[1, max(piles)]`. Feasibility: `sum(ceil(p/k)) <= h`. `ceil(p/k)` without `math.ceil` → `-(-p // k)`. If feasible → `hi = mid` (try slower); else `lo = mid + 1`.


> [!note]- Python Solution
> ```python
> def min_eating_speed(piles, h):
>     def feasible(speed):
>         return sum(-(-p // speed) for p in piles) <= h
> 
>     lo, hi = 1, max(piles)
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if feasible(mid):
>             hi = mid
>         else:
>             lo = mid + 1
>     return lo
> ```

> [!success] Complexity
> O(n log(max_pile)) time, O(1) space.

> [!tip] Alternatives
> Linear scan over speeds O(n · max_pile) — TLE. `(p + k - 1) // k` is equivalent ceiling formula.

---

### Capacity To Ship Packages Within D Days (LC 1011)

> [!example] Problem
> A conveyor belt has packages that must be shipped from one port to another within days days.
> The ith package on the conveyor belt has a weight of weights[i]. Each day, we load the ship with packages on the conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship.
> Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.
> 
> **Example 1:**
> ```
> Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
> Output: 15
> Explanation: A ship capacity of 15 is the minimum to ship all the packages in 5 days like this:
> 1st day: 1, 2, 3, 4, 5
> 2nd day: 6, 7
> 3rd day: 8
> 4th day: 9
> 5th day: 10
> 
> Note that the cargo must be shipped in the order given, so using a ship of capacity 14 and splitting the packages into parts like (2, 3, 4, 5), (1, 6, 7), (8), (9), (10) is not allowed.
> ```
> 
> **Example 2:**
> ```
> Input: weights = [3,2,2,4,1,4], days = 3
> Output: 6
> Explanation: A ship capacity of 6 is the minimum to ship all the packages in 3 days like this:
> 1st day: 3, 2
> 2nd day: 2, 4
> 3rd day: 1, 4
> ```
> 
> **Example 3:**
> ```
> Input: weights = [1,2,3,1,1], days = 4
> Output: 3
> Explanation:
> 1st day: 1
> 2nd day: 2
> 3rd day: 3
> 4th day: 1, 1
> ```
> 
> **Constraints:**
> - 1 <= days <= weights.length <= 5 * 10^4
> - 1 <= weights[i] <= 500

> [!info] Approach
> Larger capacity → fewer days. Monotone predicate on capacity. Search capacity in `[max(weights), sum(weights)]` — minimum needed to ship heaviest package; maximum ships all in one day. Greedy feasibility: greedily fill each day; when adding next weight exceeds capacity, start a new day.


> [!note]- Python Solution
> ```python
> def ship_within_days(weights, days):
>     def feasible(cap):
>         day_count, load = 1, 0
>         for w in weights:
>             if load + w > cap:
>                 day_count += 1
>                 load = 0
>             load += w
>         return day_count <= days
> 
>     lo, hi = max(weights), sum(weights)
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if feasible(mid):
>             hi = mid
>         else:
>             lo = mid + 1
>     return lo
> ```

> [!success] Complexity
> O(n log(sum - max)) time, O(1) space.

> [!tip] Alternatives
> Structurally identical to Split Array Largest Sum — same template applies.

---

### Split Array Largest Sum (LC 410)

> [!example] Problem
> Given an integer array nums and an integer k, split nums into k non-empty subarrays such that the largest sum of any subarray is minimized.
> Return the minimized largest sum of the split.
> A subarray is a contiguous part of the array.
> 
> **Example 1:**
> ```
> Input: nums = [7,2,5,10,8], k = 2
> Output: 18
> Explanation: There are four ways to split nums into two subarrays.
> The best way is to split it into [7,2,5] and [10,8], where the largest sum among the two subarrays is only 18.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,4,5], k = 2
> Output: 9
> Explanation: There are four ways to split nums into two subarrays.
> The best way is to split it into [1,2,3] and [4,5], where the largest sum among the two subarrays is only 9.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 1000
> - 0 <= nums[i] <= 10^6
> - 1 <= k <= min(50, nums.length)

> [!info] Approach
> Larger allowed max-sum → easier to fit into `k` parts. Monotone predicate on the answer value. Binary search on `max_sum` in `[max(nums), sum(nums)]`. Feasibility: greedy partition counting. Greedily extend current subarray; when adding next element would exceed `max_sum`, start new part. If parts ≤ k → feasible.


> [!note]- Python Solution
> ```python
> def split_array(nums, k):
>     def feasible(max_sum):
>         parts, curr = 1, 0
>         for n in nums:
>             if curr + n > max_sum:
>                 parts += 1
>                 curr = 0
>             curr += n
>         return parts <= k
> 
>     lo, hi = max(nums), sum(nums)
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if feasible(mid):
>             hi = mid
>         else:
>             lo = mid + 1
>     return lo
> ```

> [!success] Complexity
> O(n log(sum)) time, O(1) space.

> [!tip] Alternatives
> DP O(n² · k) — feasible only for small n; BS + greedy is strictly better.

---

### Minimize Max Distance to Gas Station (LC 774)

> [!example] Problem
> You are given an integer array `stations` that represents the positions of the gas stations on the **x-axis**. You are also given an integer `k`.
> 
> You should add `k` new gas stations. You can add the stations anywhere on the **x-axis**, and not necessarily on an integer position.
> 
> Let `penalty()` be the maximum distance between **adjacent** gas stations after adding the `k` new stations.
> 
> Return *the smallest possible value of* `penalty()`. Answers within `10^-6` of the actual answer will be accepted.
> 
>  
> 
> Example 1:
> 
> ```
> **Input:** stations = [1,2,3,4,5,6,7,8,9,10], k = 9
> **Output:** 0.50000
> 
> ```
> 
> Example 2:
> 
> ```
> **Input:** stations = [23,24,36,39,46,56,57,65,84,98], k = 1
> **Output:** 14.00000
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `10 <= stations.length <= 2000`
> 	
> - `0 <= stations[i] <= 10^8`
> 	
> - `stations` is sorted in a **strictly increasing** order.
> 	
> - `1 <= k <= 10^6`

> [!info] Approach
> Smaller allowed gap → more stations needed. Monotone on gap size → binary search on floating-point answer. Search `d` in `[0, stations[-1] - stations[0]]`. For each existing gap `g`, stations needed = `floor(g / d)`. 100 iterations of binary search achieves precision ~1e-30, well within the required 1e-6.


> [!note]- Python Solution
> ```python
> def min_max_gas_dist(stations, k):
>     def feasible(d):
>         return sum(int((stations[i] - stations[i-1]) / d)
>                    for i in range(1, len(stations))) <= k
> 
>     lo, hi = 0.0, stations[-1] - stations[0]
>     for _ in range(100):  # fixed iterations for floating-point precision
>         mid = (lo + hi) / 2
>         if feasible(mid):
>             hi = mid
>         else:
>             lo = mid
>     return lo
> ```

> [!success] Complexity
> O(100 · n) ≈ O(n) time, O(1) space.

> [!tip] Alternatives
> Priority queue O(k log n) — exact integer answer approach; float BS is simpler to implement.

---

### Minimum Speed to Arrive on Time (LC 1870)

> [!example] Problem
> You are given a floating-point number hour, representing the amount of time you have to reach the office. To commute to the office, you must take n trains in sequential order. You are also given an integer array dist of length n, where dist[i] describes the distance (in kilometers) of the ith train ride.
> Each train can only depart at an integer hour, so you may need to wait in between each train ride.
> Return the minimum positive integer speed (in kilometers per hour) that all the trains must travel at for you to reach the office on time, or -1 if it is impossible to be on time.
> Tests are generated such that the answer will not exceed 107 and hour will have at most two digits after the decimal point.
> 
> **Example 1:**
> ```
> Input: dist = [1,3,2], hour = 6
> Output: 1
> Explanation: At speed 1:
> - The first train ride takes 1/1 = 1 hour.
> - Since we are already at an integer hour, we depart immediately at the 1 hour mark. The second train takes 3/1 = 3 hours.
> - Since we are already at an integer hour, we depart immediately at the 4 hour mark. The third train takes 2/1 = 2 hours.
> - You will arrive at exactly the 6 hour mark.
> ```
> 
> **Example 2:**
> ```
> Input: dist = [1,3,2], hour = 2.7
> Output: 3
> Explanation: At speed 3:
> - The first train ride takes 1/3 = 0.33333 hours.
> - Since we are not at an integer hour, we wait until the 1 hour mark to depart. The second train ride takes 3/3 = 1 hour.
> - Since we are already at an integer hour, we depart immediately at the 2 hour mark. The third train takes 2/3 = 0.66667 hours.
> - You will arrive at the 2.66667 hour mark.
> ```
> 
> **Example 3:**
> ```
> Input: dist = [1,3,2], hour = 1.9
> Output: -1
> Explanation: It is impossible because the earliest the third train can depart is at the 2 hour mark.
> ```
> 
> **Constraints:**
> - n == dist.length
> - 1 <= n <= 10^5
> - 1 <= dist[i] <= 10^5
> - 1 <= hour <= 10^9
> - There will be at most two digits after the decimal point in hour.

> [!info] Approach
> Higher speed → arrive earlier. Monotone integer predicate. Search `v` in `[1, 10^7]`. Each intermediate leg takes `ceil(d/v)` hours; last leg takes `d/v` (fractional OK). Early exit: if `hour <= n - 1`, impossible (each of `n-1` waits costs at least 1 hour).


> [!note]- Python Solution
> ```python
> import math
> 
> def min_speed_on_time(dist, hour):
>     n = len(dist)
>     if hour <= n - 1:
>         return -1   # each intermediate stop waits for next integer hour
> 
>     def feasible(v):
>         total = sum(math.ceil(d / v) for d in dist[:-1])
>         total += dist[-1] / v
>         return total <= hour
> 
>     lo, hi = 1, 10**7
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if feasible(mid):
>             hi = mid
>         else:
>             lo = mid + 1
>     return lo if feasible(lo) else -1
> ```

> [!success] Complexity
> O(n log(10^7)) time, O(1) space.

> [!tip] Alternatives
> None — the monotone structure makes BS the natural approach.

---

## Rotated Sorted Array

> [!info] Approach
> In a rotated sorted array, splitting at `mid` always yields one sorted half and one possibly-unsorted half. Determine which half is sorted by comparing endpoints, then check if the target lies within the sorted half.

---

### Search in Rotated Sorted Array (LC 33)

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
> Not fully sorted, but one half around any `mid` is always sorted. Use that to make a binary decision. Standard BS with an extra check — determine the sorted half, test if target is in it. If `nums[lo] <= nums[mid]`, left half `[lo, mid]` is sorted. If target in `[nums[lo], nums[mid])` → go left; else go right.


> [!note]- Python Solution
> ```python
> def search(nums, target):
>     lo, hi = 0, len(nums) - 1
>     while lo <= hi:
>         mid = lo + (hi - lo) // 2
>         if nums[mid] == target:
>             return mid
>         if nums[lo] <= nums[mid]:               # left half is sorted
>             if nums[lo] <= target < nums[mid]:
>                 hi = mid - 1
>             else:
>                 lo = mid + 1
>         else:                                   # right half is sorted
>             if nums[mid] < target <= nums[hi]:
>                 lo = mid + 1
>             else:
>                 hi = mid - 1
>     return -1
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

> [!tip] Alternatives
> Find pivot index first (O(log n)) then BS in correct half — two passes, same asymptotic.

---

### Find Minimum in Rotated Sorted Array (LC 153)

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
> Minimum is the rotation boundary. Compare `nums[mid]` with `nums[hi]`: if `nums[mid] > nums[hi]`, the minimum must be to the right. Binary search shrinking toward the minimum. Invariant: minimum is always in `[lo, hi]`. `if nums[mid] > nums[hi]: lo = mid + 1` else `hi = mid`. Do NOT compare with `nums[lo]`.


> [!note]- Python Solution
> ```python
> def find_min(nums):
>     lo, hi = 0, len(nums) - 1
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if nums[mid] > nums[hi]:
>             lo = mid + 1   # min is in right half
>         else:
>             hi = mid       # mid could be the minimum
>     return nums[lo]
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

> [!tip] Alternatives
> Compare with `nums[hi]` not `nums[lo]` — the latter breaks the invariant when `lo == mid`.

---

### Search in Rotated Sorted Array II (LC 81)

> [!example] Problem
> There is an integer array nums sorted in non-decreasing order (not necessarily with distinct values).
> Before being passed to your function, nums is rotated at an unknown pivot index k (0 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,4,4,5,6,6,7] might be rotated at pivot index 5 and become [4,5,6,6,7,0,1,2,4,4].
> Given the array nums after the rotation and an integer target, return true if target is in nums, or false if it is not in nums.
> You must decrease the overall operation steps as much as possible.
> 
> **Example 1:**
> ```
> Input: nums = [2,5,6,0,0,1,2], target = 0
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,5,6,0,0,1,2], target = 3
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 5000
> - -10^4 <= nums[i] <= 10^4
> - nums is guaranteed to be rotated at some pivot.
> - -10^4 <= target <= 10^4

> [!info] Approach
> Duplicates create ambiguity: when `nums[lo] == nums[mid] == nums[hi]`, we cannot determine which half is sorted. Same logic as LC 33 with an extra degenerate case to shrink both boundaries. On ambiguity → `lo += 1; hi -= 1`. Worst case O(n) for all-same arrays.


> [!note]- Python Solution
> ```python
> def search_with_dups(nums, target):
>     lo, hi = 0, len(nums) - 1
>     while lo <= hi:
>         mid = lo + (hi - lo) // 2
>         if nums[mid] == target:
>             return True
>         if nums[lo] == nums[mid] == nums[hi]:
>             lo += 1; hi -= 1   # can't determine sorted half; shrink both
>         elif nums[lo] <= nums[mid]:            # left half sorted
>             if nums[lo] <= target < nums[mid]:
>                 hi = mid - 1
>             else:
>                 lo = mid + 1
>         else:                                  # right half sorted
>             if nums[mid] < target <= nums[hi]:
>                 lo = mid + 1
>             else:
>                 hi = mid - 1
>     return False
> ```

> [!success] Complexity
> O(log n) average, O(n) worst case. O(1) space.

---

### Find Minimum in Rotated Sorted Array II (LC 154)

> [!example] Problem
> Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,4,4,5,6,7] might become:
> Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].
> Given the sorted rotated array nums that may contain duplicates, return the minimum element of this array.
> You must decrease the overall operation steps as much as possible.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,5]
> Output: 1
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,2,2,0,1]
> Output: 0
> ```
> 
> **Constraints:**
> - n == nums.length
> - 1 <= n <= 5000
> - -5000 <= nums[i] <= 5000
> - nums is sorted and rotated between 1 and n times.

> [!info] Approach
> Same as LC 153 but `nums[mid] == nums[hi]` is now possible — can't determine which half contains the minimum. When equal, safely shrink `hi` by 1 (minimum is not lost since `nums[mid] == nums[hi]`). Three-way branch on `nums[mid]` vs `nums[hi]`.


> [!note]- Python Solution
> ```python
> def find_min_with_dups(nums):
>     lo, hi = 0, len(nums) - 1
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if nums[mid] > nums[hi]:
>             lo = mid + 1
>         elif nums[mid] < nums[hi]:
>             hi = mid
>         else:
>             hi -= 1   # nums[mid] == nums[hi]: can't tell, shrink hi safely
>     return nums[lo]
> ```

> [!success] Complexity
> O(log n) average, O(n) worst case (all equal elements). O(1) space.

---

## Peak Element

> [!info] Approach
> A peak always exists (guaranteed by boundary conditions). Moving toward the uphill neighbor never discards all peaks — a peak is "reachable" by always climbing. This is the binary search invariant.

---

### Find Peak Element (LC 162)

> [!example] Problem
> A peak element is an element that is strictly greater than its neighbors.
> Given a 0-indexed integer array nums, find a peak element, and return its index. If the array contains multiple peaks, return the index to any of the peaks.
> You may imagine that nums[-1] = nums[n] = -∞. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.
> You must write an algorithm that runs in O(log n) time.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3,1]
> Output: 2
> Explanation: 3 is a peak element and your function should return the index number 2.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,1,3,5,6,4]
> Output: 5
> Explanation: Your function can return either index number 1 where the peak element is 2, or index number 5 where the peak element is 6.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 1000
> - -2^{31} <= nums[i] <= 2^{31} - 1
> - nums[i] != nums[i + 1] for all valid i.

> [!info] Approach
> If `nums[mid] < nums[mid+1]`, the slope is ascending to the right — a peak must exist in `[mid+1, hi]`. Symmetric for descending slope. Invariant: a peak always exists in `[lo, hi]`. Shrink toward the uphill side. `if nums[mid] < nums[mid+1]: lo = mid + 1` else `hi = mid`. Terminates at `lo == hi` which is a peak.


> [!note]- Python Solution
> ```python
> def find_peak_element(nums):
>     lo, hi = 0, len(nums) - 1
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if nums[mid] < nums[mid + 1]:
>             lo = mid + 1   # ascending → peak to the right
>         else:
>             hi = mid       # descending or at peak → peak at mid or left
>     return lo
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

> [!tip] Alternatives
> Linear scan O(n) — valid; BS is expected in interviews. Any valid peak index is accepted.

---

### Peak Index in a Mountain Array (LC 852)

> [!example] Problem
> You are given an integer mountain array arr of length n where the values increase to a peak element and then decrease.
> Return the index of the peak element.
> Your task is to solve it in O(log(n)) time complexity.
> 
> **Example 1:**
> ```
> Input: arr = [0,1,0]
> Output: 1
> ```
> 
> **Example 2:**
> ```
> Input: arr = [0,2,1,0]
> Output: 1
> ```
> 
> **Example 3:**
> ```
> Input: arr = [0,10,5,2]
> Output: 1
> ```
> 
> **Constraints:**
> - 3 <= arr.length <= 10^5
> - 0 <= arr[i] <= 10^6
> - arr is guaranteed to be a mountain array.

> [!info] Approach
> Strictly unimodal — same ascending/descending slope argument as LC 162. Unique peak guaranteed. Identical binary search structure. `nums[mid] < nums[mid+1]` → still ascending → peak is right. Same code as LC 162; mountain guarantee makes the result unique.


> [!note]- Python Solution
> ```python
> def peak_index_in_mountain_array(arr):
>     lo, hi = 0, len(arr) - 1
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if arr[mid] < arr[mid + 1]:
>             lo = mid + 1
>         else:
>             hi = mid
>     return lo
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

> [!tip] Alternatives
> Ternary search also O(log n) — compare `f(m1)` vs `f(m2)` at two points; BS is simpler here.

---

### Find a Peak Element in a 2D Grid (LC 1901)

> [!example] Problem
> A peak element in a 2D grid is an element that is strictly greater than all of its adjacent neighbors to the left, right, top, and bottom.
> Given a 0-indexed m x n matrix mat where no two adjacent cells are equal, find any peak element mat[i][j] and return the length 2 array [i,j].
> You may assume that the entire matrix is surrounded by an outer perimeter with the value -1 in each cell.
> You must write an algorithm that runs in O(m log(n)) or O(n log(m)) time.
> 
> **Example 1:**
> ```
> Input: mat = [[1,4],[3,2]]
> Output: [0,1]
> Explanation: Both 3 and 4 are peak elements so [1,0] and [0,1] are both acceptable answers.
> ```
> 
> **Example 2:**
> ```
> Input: mat = [[10,20,15],[21,30,14],[7,16,32]]
> Output: [1,1]
> Explanation: Both 30 and 32 are peak elements so [1,1] and [2,2] are both acceptable answers.
> ```
> 
> **Constraints:**
> - m == mat.length
> - n == mat[i].length
> - 1 <= m, n <= 500
> - 1 <= mat[i][j] <= 10^5
> - No two adjacent cells are equal.

> [!info] Approach
> Binary search on columns. At column `mid`, find the row with the maximum value in that column. That row-maximum is either a 2D peak (exceeds left/right neighbors), or its larger neighbor points us toward a column containing a peak. Binary search on columns `[lo, hi]`. At `mid_col`, find `max_row`. Compare with left/right columns. If `mat[max_row][mid_col] < mat[max_row][mid_col+1]` → a peak exists to the right; else left or at mid.


> [!note]- Python Solution
> ```python
> def find_peak_grid(mat):
>     m, n = len(mat), len(mat[0])
>     lo, hi = 0, n - 1
>     while lo <= hi:
>         mid_col = lo + (hi - lo) // 2
>         max_row = max(range(m), key=lambda r: mat[r][mid_col])
> 
>         left  = mat[max_row][mid_col - 1] if mid_col > 0     else -1
>         right = mat[max_row][mid_col + 1] if mid_col < n - 1 else -1
> 
>         if mat[max_row][mid_col] > left and mat[max_row][mid_col] > right:
>             return [max_row, mid_col]
>         elif right > mat[max_row][mid_col]:
>             lo = mid_col + 1
>         else:
>             hi = mid_col - 1
>     return [-1, -1]
> ```

> [!success] Complexity
> O(m log n) time, O(1) space.

> [!tip] Alternatives
> Brute force O(mn); binary search on rows O(n log m) — symmetric variant.

---

## Median / Order Statistics

---

### Median of Two Sorted Arrays (LC 4)

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
> Merging is O(m+n). The median partitions the combined array so the left half has `(m+n)//2` elements. Binary search on the partition in the smaller array. For each partition `i` in `nums1`, the partition `j = half - i` in `nums2` is determined. Valid when `max_left_A ≤ min_right_B` AND `max_left_B ≤ min_right_A`. If `max_left1 > min_right2` → partition too far right in nums1 → `hi = i - 1`; else `lo = i + 1`.


> [!note]- Python Solution
> ```python
> def find_median_sorted_arrays(nums1, nums2):
>     if len(nums1) > len(nums2):
>         nums1, nums2 = nums2, nums1   # ensure nums1 is smaller
>     m, n = len(nums1), len(nums2)
>     half = (m + n) // 2
> 
>     lo, hi = 0, m
>     while lo <= hi:
>         i = lo + (hi - lo) // 2    # partition in nums1
>         j = half - i               # partition in nums2
> 
>         max_left1  = nums1[i-1] if i > 0 else float('-inf')
>         min_right1 = nums1[i]   if i < m else float('inf')
>         max_left2  = nums2[j-1] if j > 0 else float('-inf')
>         min_right2 = nums2[j]   if j < n else float('inf')
> 
>         if max_left1 <= min_right2 and max_left2 <= min_right1:
>             if (m + n) % 2 == 1:
>                 return float(min(min_right1, min_right2))
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
> Merge both O(m+n); general kth-element recursive approach O(log(m+n)).

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
> "How many elements ≤ x?" is a monotone function of x. Binary search on the value range. Search value `d` in `[matrix[0][0], matrix[n-1][n-1]]`. Count elements ≤ d using staircase traversal O(n). Start top-right. If `matrix[row][col] <= d` → all `col+1` elements in this row qualify → `row += 1`; else `col -= 1`. If count ≥ k → `hi = mid`; else `lo = mid + 1`. Answer is always an actual matrix element.


> [!note]- Python Solution
> ```python
> def kth_smallest(matrix, k):
>     n = len(matrix)
> 
>     def count_le(d):
>         count, row, col = 0, 0, n - 1
>         while row < n and col >= 0:
>             if matrix[row][col] <= d:
>                 count += col + 1
>                 row += 1
>             else:
>                 col -= 1
>         return count
> 
>     lo, hi = matrix[0][0], matrix[n-1][n-1]
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if count_le(mid) >= k:
>             hi = mid
>         else:
>             lo = mid + 1
>     return lo
> ```

> [!success] Complexity
> O(n log(max - min)) time, O(1) space.

> [!tip] Alternatives
> Min-heap O(k log n) — better when k is small; BS on value dominates for large k.

---

### Find K-th Smallest Pair Distance (LC 719)

> [!example] Problem
> The distance of a pair of integers a and b is defined as the absolute difference between a and b.
> Given an integer array nums and an integer k, return the kth smallest distance among all the pairs nums[i] and nums[j] where 0 <= i < j < nums.length.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,1], k = 1
> Output: 0
> Explanation: Here are all the pairs:
> (1,3) -> 2
> (1,1) -> 0
> (3,1) -> 2
> Then the 1st smallest distance pair is (1,1), and its distance is 0.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,1,1], k = 2
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,6,1], k = 3
> Output: 5
> ```
> 
> **Constraints:**
> - n == nums.length
> - 2 <= n <= 10^4
> - 0 <= nums[i] <= 10^6
> - 1 <= k <= n * (n - 1) / 2

> [!info] Approach
> Cannot enumerate all O(n²) pairs. "How many pairs have distance ≤ d?" is monotone in d → binary search on distance. Sort array. Search distance `d` in `[0, nums[-1] - nums[0]]`. Count pairs with distance ≤ d via two-pointer sliding window. For each `right`, advance `left` while `nums[right] - nums[left] > d`. Pairs ending at `right` with distance ≤ d = `right - left`. If count ≥ k → `hi = mid`; else `lo = mid + 1`.


> [!note]- Python Solution
> ```python
> def smallest_distance_pair(nums, k):
>     nums.sort()
>     n = len(nums)
> 
>     def count_pairs_le(d):
>         count = left = 0
>         for right in range(n):
>             while nums[right] - nums[left] > d:
>                 left += 1
>             count += right - left
>         return count
> 
>     lo, hi = 0, nums[-1] - nums[0]
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if count_pairs_le(mid) >= k:
>             hi = mid
>         else:
>             lo = mid + 1
>     return lo
> ```

> [!success] Complexity
> O(n log n + n log W) time where W = max - min. O(1) extra space after sort.

> [!tip] Alternatives
> Sort all pair distances O(n² log n) — TLE; bucket counting for small W O(n + W).

---

## 2D Matrix Binary Search

---

### Search a 2D Matrix (LC 74)

> [!example] Problem
> You are given an m x n integer matrix matrix with the following two properties:
> Given an integer target, return true if target is in matrix or false otherwise.
> You must write a solution in O(log(m * n)) time complexity.
> 
> **Example 1:**
> ```
> Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
> Output: false
> ```
> 
> **Constraints:**
> - m == matrix.length
> - n == matrix[i].length
> - 1 <= m, n <= 100
> - -10^4 <= matrix[i][j], target <= 10^4

> [!info] Approach
> Matrix has a total order — treat it as a 1D sorted array of m*n elements. Virtual binary search on index 0..m*n-1. Map mid → row=mid//n, col=mid%n. lo=0, hi=m*n-1. While lo<=hi: mid=(lo+hi)//2; val=matrix[mid//n][mid%n]. Compare with target, standard binary search logic.


> [!note]- Python Solution
> ```python
> def search_matrix(matrix, target):
>     m, n = len(matrix), len(matrix[0])
>     lo, hi = 0, m * n - 1
>     while lo <= hi:
>         mid = lo + (hi - lo) // 2
>         val = matrix[mid // n][mid % n]
>         if val == target:
>             return True
>         elif val < target:
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return False
> ```

> [!success] Complexity
> O(log(m*n)) time, O(1) space.

> [!tip] Alternatives
> Row-by-row binary search O(m log n) — valid but slower; staircase search O(m+n) — works but overkill when total order exists.

---

### Search a 2D Matrix II (LC 240)

> [!example] Problem
> Write an efficient algorithm that searches for a value target in an m x n integer matrix matrix. This matrix has the following properties
> 
> **Example 1:**
> ```
> Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 20
> Output: false
> ```
> 
> **Constraints:**
> - m == matrix.length
> - n == matrix[i].length
> - 1 <= n, m <= 300
> - -10^9 <= matrix[i][j] <= 10^9
> - All the integers in each row are sorted in ascending order.
> - All the integers in each column are sorted in ascending order.
> - -10^9 <= target <= 10^9

> [!info] Approach
> Rows AND columns are sorted but rows don't have total order (first of row i+1 may be less than last of row i). Can't treat as a 1D sorted array. Staircase search — start from the top-right corner. If matrix[r][c] == target: found. If > target: go left (c--). If < target: go down (r++). Each step eliminates a row or column. O(m+n) total.


> [!note]- Python Solution
> ```python
> def search_matrix_ii(matrix, target):
>     if not matrix or not matrix[0]:
>         return False
>     m, n = len(matrix), len(matrix[0])
>     r, c = 0, n - 1          # start top-right
>     while r < m and c >= 0:
>         val = matrix[r][c]
>         if val == target:
>             return True
>         elif val > target:
>             c -= 1            # eliminate this column
>         else:
>             r += 1            # eliminate this row
>     return False
> ```

> [!success] Complexity
> O(m+n) time, O(1) space.

> [!tip] Alternatives
> Binary search each row O(m log n) — worse than staircase when m and n are comparable.

---

## Classic / Miscellaneous

---

### Guess Number Higher or Lower (LC 374)

> [!example] Problem
> We are playing the Guess Game. The game is as follows:
> I pick a number from 1 to n. You have to guess which number I picked.
> Every time you guess wrong, I will tell you whether the number I picked is higher or lower than your guess.
> You call a pre-defined API int guess(int num), which returns three possible results:
> Return the number that I picked.
> 
> **Example 1:**
> ```
> Input: n = 10, pick = 6
> Output: 6
> ```
> 
> **Example 2:**
> ```
> Input: n = 1, pick = 1
> Output: 1
> ```
> 
> **Example 3:**
> ```
> Input: n = 2, pick = 1
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= n <= 2^{31} - 1
> - 1 <= pick <= n

> [!info] Approach
> Search space `[1, n]` is totally ordered and the API gives three-way comparison — textbook binary search. Standard BS template with the API replacing a direct comparison. `lo=1, hi=n`. While `lo <= hi`: if `guess(mid)==0` return mid; if `guess(mid)==-1` the answer is lower → `hi=mid-1`; else `lo=mid+1`.


> [!note]- Python Solution
> ```python
> def guess_number(n):
>     lo, hi = 1, n
>     while lo <= hi:
>         mid = lo + (hi - lo) // 2
>         result = guess(mid)   # API call
>         if result == 0:
>             return mid
>         elif result == -1:    # picked number < mid
>             hi = mid - 1
>         else:                 # picked number > mid
>             lo = mid + 1
>     return -1
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

> [!tip] Alternatives
> Linear scan O(n); ternary search O(log n) — but BS is simpler and has lower constant.

---

### Find First and Last Position (LC 34)

> [!example] Problem
> Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value.
> If target is not found in the array, return [-1, -1].
> You must write an algorithm with O(log n) runtime complexity.
> 
> **Example 1:**
> ```
> Input: nums = [5,7,7,8,8,10], target = 8
> Output: [3,4]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5,7,7,8,8,10], target = 6
> Output: [-1,-1]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [], target = 0
> Output: [-1,-1]
> ```
> 
> **Constraints:**
> - 0 <= nums.length <= 10^5
> - -10^9 <= nums[i] <= 10^9
> - nums is a non-decreasing array.
> - -10^9 <= target <= 10^9

> [!info] Approach
> Need leftmost and rightmost occurrence — two separate lower/upper bound searches. `bisect_left` gives the first index where `nums[i] >= target`; `bisect_right` gives the first index where `nums[i] > target` (so last occurrence = that - 1). First = lower_bound(target). If `nums[first] != target` → not found. Last = upper_bound(target) - 1.


> [!note]- Python Solution
> ```python
> def search_range(nums, target):
>     def lower_bound(val):
>         lo, hi = 0, len(nums)
>         while lo < hi:
>             mid = lo + (hi - lo) // 2
>             if nums[mid] < val:
>                 lo = mid + 1
>             else:
>                 hi = mid
>         return lo
> 
>     first = lower_bound(target)
>     if first == len(nums) or nums[first] != target:
>         return [-1, -1]
>     last = lower_bound(target + 1) - 1
>     return [first, last]
> ```

> [!success] Complexity
> O(log n) time, O(1) space. Two binary search passes.

> [!tip] Alternatives
> `bisect.bisect_left` / `bisect.bisect_right` from stdlib; single linear scan O(n) trivial but not O(log n).

---

### Minimum Number of Days to Make m Bouquets (LC 1482)

> [!example] Problem
> You are given an integer array bloomDay, an integer m and an integer k.
> You want to make m bouquets. To make a bouquet, you need to use k adjacent flowers from the garden.
> The garden consists of n flowers, the ith flower will bloom in the bloomDay[i] and then can be used in exactly one bouquet.
> Return the minimum number of days you need to wait to be able to make m bouquets from the garden. If it is impossible to make m bouquets return -1.
> 
> **Example 1:**
> ```
> Input: bloomDay = [1,10,3,10,2], m = 3, k = 1
> Output: 3
> Explanation: Let us see what happened in the first three days. x means flower bloomed and _ means flower did not bloom in the garden.
> We need 3 bouquets each should contain 1 flower.
> After day 1: [x, _, _, _, _]   // we can only make one bouquet.
> After day 2: [x, _, _, _, x]   // we can only make two bouquets.
> After day 3: [x, _, x, _, x]   // we can make 3 bouquets. The answer is 3.
> ```
> 
> **Example 2:**
> ```
> Input: bloomDay = [1,10,3,10,2], m = 3, k = 2
> Output: -1
> Explanation: We need 3 bouquets each has 2 flowers, that means we need 6 flowers. We only have 5 flowers so it is impossible to get the needed bouquets and we return -1.
> ```
> 
> **Example 3:**
> ```
> Input: bloomDay = [7,7,7,7,12,7,7], m = 2, k = 3
> Output: 12
> Explanation: We need 2 bouquets each should have 3 flowers.
> Here is the garden after the 7 and 12 days:
> After day 7: [x, x, x, x, _, x, x]
> We can make one bouquet of the first three flowers that bloomed. We cannot make another bouquet from the last three flowers that bloomed because they are not adjacent.
> After day 12: [x, x, x, x, x, x, x]
> It is obvious that we can make two bouquets in different ways.
> ```
> 
> **Constraints:**
> - bloomDay.length == n
> - 1 <= n <= 10^5
> - 1 <= bloomDay[i] <= 10^9
> - 1 <= m <= 10^6
> - 1 <= k <= n

> [!info] Approach
> More days → more flowers bloomed → easier to form bouquets. Monotone predicate on day. Binary search on `day` in `[min(bloomDay), max(bloomDay)]`. Feasibility: scan the array counting consecutive bloomed flowers; form a bouquet every time we accumulate `k` in a row. Count bouquets formed; if `>= m` → feasible. Early exit: if `m * k > len(bloomDay)` → impossible.


> [!note]- Python Solution
> ```python
> def min_days(bloomDay, m, k):
>     n = len(bloomDay)
>     if m * k > n:
>         return -1
> 
>     def feasible(day):
>         bouquets = consecutive = 0
>         for d in bloomDay:
>             if d <= day:
>                 consecutive += 1
>                 if consecutive == k:
>                     bouquets += 1
>                     consecutive = 0
>             else:
>                 consecutive = 0
>         return bouquets >= m
> 
>     lo, hi = min(bloomDay), max(bloomDay)
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if feasible(mid):
>             hi = mid
>         else:
>             lo = mid + 1
>     return lo
> ```

> [!success] Complexity
> O(n log(max_day)) time, O(1) space.

> [!tip] Alternatives
> None practical — greedy simulation alone is O(n · max_day); BS + greedy is the canonical approach.

---

### Find K Closest Elements (LC 658)

> [!example] Problem
> Given a sorted integer array arr, two integers k and x, return the k closest integers to x in the array. The result should also be sorted in ascending order.
> An integer a is closer to x than an integer b if
> 
> **Example 1:**
> ```
> Input: arr = [1,2,3,4,5], k = 4, x = 3
> Output: [1,2,3,4]
> ```
> 
> **Example 2:**
> ```
> Input: arr = [1,1,2,3,4,5], k = 4, x = -1
> Output: [1,1,2,3]
> ```
> 
> **Constraints:**
> - 1 <= k <= arr.length
> - 1 <= arr.length <= 10^4
> - arr is sorted in ascending order.
> - -10^4 <= arr[i], x <= 10^4

> [!info] Approach
> The answer is always a contiguous subarray of length `k`. Binary search for the left boundary of this window. Search left index `i` in `[0, len(arr) - k]`. Window `[i, i+k)` is optimal if `x - arr[i] <= arr[i+k] - x` (left element is at least as close as the right element just outside). If `x - arr[mid] > arr[mid+k] - x` → window is too far left → `lo = mid + 1`; else `hi = mid`. Answer is `arr[lo : lo + k]`.


> [!note]- Python Solution
> ```python
> def find_closest_elements(arr, k, x):
>     lo, hi = 0, len(arr) - k
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if x - arr[mid] > arr[mid + k] - x:
>             lo = mid + 1   # left boundary too far left
>         else:
>             hi = mid
>     return arr[lo : lo + k]
> ```

> [!success] Complexity
> O(log(n - k) + k) time, O(1) extra space (output excluded).

> [!tip] Alternatives
> Sort by distance O(n log n) — correct but loses sorted order and is slower; two-pointer shrink from both ends O(n - k) — simpler to reason about but O(n).

---

### Count of Smaller Numbers After Self (LC 315)

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
> Process right to left, maintaining a sorted structure. Binary search for insertion position gives the count of smaller elements already seen. Build a sorted list of "seen" elements (right to left). For each new element, `bisect_left` gives its insertion rank = count of smaller elements to its right. Insert `nums[i]` into the sorted list (using `insort`). Count = `bisect_left(sorted_list, nums[i])`.


> [!note]- Python Solution
> ```python
> from bisect import bisect_left, insort
> 
> def count_smaller(nums):
>     sorted_seen = []
>     result = []
>     for num in reversed(nums):
>         count = bisect_left(sorted_seen, num)
>         result.append(count)
>         insort(sorted_seen, num)
>     result.reverse()
>     return result
> ```

> [!success] Complexity
> O(n²) worst case (insort is O(n) due to list shifts) — passes LC constraints for n ≤ 10^5. O(n log n) with a Fenwick tree or merge-sort.

> [!tip] Alternatives
> **Merge sort** O(n log n) — count inversions during merge; **Fenwick/BIT tree** O(n log n) with coordinate compression — optimal.

---

## Second Occurrence / Exact Match Variants

---

### Search a 2D Matrix — Row + Column BS (LC 74 variant note)

> [!example] Problem
> You are given an m x n integer matrix matrix with the following two properties:
> Given an integer target, return true if target is in matrix or false otherwise.
> You must write a solution in O(log(m * n)) time complexity.
> 
> **Example 1:**
> ```
> Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
> Output: false
> ```
> 
> **Constraints:**
> - m == matrix.length
> - n == matrix[i].length
> - 1 <= m, n <= 100
> - -10^4 <= matrix[i][j], target <= 10^4

> [!info] Approach
> Useful when the single-index trick is not obvious in an interview. Also illustrates composing two independent binary searches. BS on rows: find the last row where `matrix[row][0] <= target` (this is the only row that can contain target). Then BS within that row. Row search: `if matrix[mid][0] <= target: lo = mid` else `hi = mid - 1`. Then standard column search.


> [!note]- Python Solution
> ```python
> def search_matrix_two_pass(matrix, target):
>     m, n = len(matrix), len(matrix[0])
>     # find candidate row
>     lo, hi = 0, m - 1
>     while lo < hi:
>         mid = lo + (hi - lo + 1) // 2   # upper-mid to avoid infinite loop
>         if matrix[mid][0] <= target:
>             lo = mid
>         else:
>             hi = mid - 1
>     row = lo
>     # binary search within row
>     lo, hi = 0, n - 1
>     while lo <= hi:
>         mid = lo + (hi - lo) // 2
>         if matrix[row][mid] == target:
>             return True
>         elif matrix[row][mid] < target:
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return False
> ```

> [!success] Complexity
> O(log m + log n) = O(log(mn)) time, O(1) space.

> [!tip] Alternatives
> Single flattened-index BS is more concise; this form is useful for understanding the row-then-column decomposition.

---

### Sqrt(x) — Integer Square Root (LC 69)

> [!example] Problem
> Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.
> You must not use any built-in exponent function or operator.
> 
> **Example 1:**
> ```
> Input: x = 4
> Output: 2
> Explanation: The square root of 4 is 2, so we return 2.
> ```
> 
> **Example 2:**
> ```
> Input: x = 8
> Output: 2
> Explanation: The square root of 8 is 2.82842..., and since we round it down to the nearest integer, 2 is returned.
> ```
> 
> **Constraints:**
> - 0 <= x <= 2^{31} - 1

> [!info] Approach
> Find the largest integer `k` such that `k² <= x`. Classic "find upper bound of predicate" problem. Binary search `k` in `[0, x]` (or `[0, x//2 + 1]` for efficiency). Find the last `k` where `k*k <= x`. If `mid * mid <= x` → `lo = mid + 1` (can go larger); else `hi = mid - 1`. Answer is `hi` (the last valid mid).


> [!note]- Python Solution
> ```python
> def my_sqrt(x):
>     if x < 2:
>         return x
>     lo, hi = 1, x // 2
>     while lo <= hi:
>         mid = lo + (hi - lo) // 2
>         sq = mid * mid
>         if sq == x:
>             return mid
>         elif sq < x:
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return hi   # hi is the floor when loop ends
> ```

> [!success] Complexity
> O(log x) time, O(1) space.

> [!tip] Alternatives
> Newton's method converges faster in practice; `int(x**0.5)` uses hardware FP (may have precision issues for large x).

---

### Find the Duplicate Number (LC 287) — BS on Value

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
> Count of integers in `[1, mid]` that appear in `nums` — if > `mid`, by pigeonhole the duplicate is ≤ `mid`. Monotone predicate → binary search on value. Search `mid` in `[1, n]`. Count elements in `nums` that are `<= mid`. If count > mid → duplicate in lower half. `if count > mid: hi = mid` else `lo = mid + 1`. Not a standard in-place BS — it's BS on the value space, not the index space.


> [!note]- Python Solution
> ```python
> def find_duplicate(nums):
>     lo, hi = 1, len(nums) - 1
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         count = sum(1 for x in nums if x <= mid)
>         if count > mid:
>             hi = mid   # duplicate is in [lo, mid]
>         else:
>             lo = mid + 1
>     return lo
> ```

> [!success] Complexity
> O(n log n) time, O(1) space (no extra data structures).

> [!tip] Alternatives
> Floyd's cycle detection O(n) O(1) — optimal; XOR/sum tricks work only when exactly one duplicate appears exactly twice.

---

### Longest Increasing Subsequence — Length via BS (LC 300)

> [!example] Problem
> Given an integer array nums, return the length of the longest strictly increasing subsequence.
> 
> **Example 1:**
> ```
> Input: nums = [10,9,2,5,3,7,101,18]
> Output: 4
> Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,0,3,2,3]
> Output: 4
> ```
> 
> **Example 3:**
> ```
> Input: nums = [7,7,7,7,7,7,7]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2500
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> Patience sorting uses a `tails` array where `tails[i]` is the smallest tail of all LIS of length `i+1`. `tails` is always sorted → binary search for insertion point. For each element, `bisect_left(tails, num)` gives the position to replace (or extend if at end). The length of `tails` at the end is the LIS length. If `num > tails[-1]` → append (extend LIS). Else → replace `tails[pos]` = num (maintain smallest tails for future options).


> [!note]- Python Solution
> ```python
> from bisect import bisect_left
> 
> def length_of_lis(nums):
>     tails = []
>     for num in nums:
>         pos = bisect_left(tails, num)
>         if pos == len(tails):
>             tails.append(num)
>         else:
>             tails[pos] = num
>     return len(tails)
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> DP O(n²) — classic; this BS approach is the O(n log n) optimisation. Note `tails` is NOT the actual LIS — only its length is correct.

---

## See Also

[[two-pointers]] | [[sliding-window]] | [[sorting]] | [[dynamic-programming]]
### Aggressive Cows / Maximize Minimum Distance

> [!example] Problem
> Given stall positions and `k` cows, place the cows so the minimum distance between any two cows is as large as possible.

> [!info] Approach
> If a distance `d` works, any smaller distance also works. That monotonic predicate makes the answer searchable. Sort positions and binary search the answer `d`. The feasibility check greedily places each cow at the earliest valid stall. Place the first cow at the first stall, then keep placing the next cow at the first position with gap `>= d`.


> [!note]- Python Solution
> ```python
> def aggressive_cows(positions, k):
>     positions.sort()
> 
>     def can_place(distance):
>         cows = 1
>         last = positions[0]
>         for pos in positions[1:]:
>             if pos - last >= distance:
>                 cows += 1
>                 last = pos
>                 if cows == k:
>                     return True
>         return False
> 
>     lo, hi = 1, positions[-1] - positions[0]
>     while lo < hi:
>         mid = lo + (hi - lo + 1) // 2
>         if can_place(mid):
>             lo = mid
>         else:
>             hi = mid - 1
>     return lo
> ```

> [!success] Complexity
> O(n log R) time, where `R = positions[-1] - positions[0]`; O(1) extra space.

> [!tip] Alternatives
> Reuse this template for router placement, aggressive seating, and maximize-minimum-distance questions.

---

## Binary Search on Answer — More Problems

### Find K-th Smallest Pair Distance (LC 719)

> [!example] Problem
> The distance of a pair of integers a and b is defined as the absolute difference between a and b.
> Given an integer array nums and an integer k, return the kth smallest distance among all the pairs nums[i] and nums[j] where 0 <= i < j < nums.length.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,1], k = 1
> Output: 0
> Explanation: Here are all the pairs:
> (1,3) -> 2
> (1,1) -> 0
> (3,1) -> 2
> Then the 1st smallest distance pair is (1,1), and its distance is 0.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,1,1], k = 2
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,6,1], k = 3
> Output: 5
> ```
> 
> **Constraints:**
> - n == nums.length
> - 2 <= n <= 10^4
> - 0 <= nums[i] <= 10^6
> - 1 <= k <= n * (n - 1) / 2

> [!info] Approach
> The distance range is `[0, max(nums) - min(nums)]`. Binary search on the answer: for a candidate distance `mid`, count how many pairs have distance ≤ `mid` using a two-pointer scan on the sorted array. Sort the array. Binary search on `mid`. For each index `i`, find the leftmost `j` such that `nums[i] - nums[j] <= mid` using two pointers. The count of such pairs is `i - j`. `lo = 0`, `hi = nums[-1] - nums[0]`. Count pairs with distance ≤ `mid`: two-pointer `left` tracking the start of the window for each `right`. Return the smallest `mid` where `count >= k`.


> [!note]- Python Solution
> ```python
> def smallest_distance_pair(nums, k):
>     nums.sort()
>     n = len(nums)
> >
>     def count_pairs(max_dist):
>         count = 0
>         left = 0
>         for right in range(n):
>             while nums[right] - nums[left] > max_dist:
>                 left += 1
>             count += right - left
>         return count
> >
>     lo = 0
>     hi = nums[-1] - nums[0]
>     while lo < hi:
>         mid = (lo + hi) // 2
>         if count_pairs(mid) >= k:
>             hi = mid
>         else:
>             lo = mid + 1
>     return lo
> ```

> [!success] Complexity
> Time O(n log n + n log W) where W = max distance. Space O(1).

> [!tip] Alternatives
> - Heap with all pairs: O(k log n²) — extremely slow.
> - Counting sort on distances: O(n² + W) — too slow for large inputs.
> - Key insight: "count pairs with distance ≤ mid" is the standard feasibility function for this binary search.

---

### Sqrt(x) — Integer Square Root (LC 69)

> [!example] Problem
> Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.
> You must not use any built-in exponent function or operator.
> 
> **Example 1:**
> ```
> Input: x = 4
> Output: 2
> Explanation: The square root of 4 is 2, so we return 2.
> ```
> 
> **Example 2:**
> ```
> Input: x = 8
> Output: 2
> Explanation: The square root of 8 is 2.82842..., and since we round it down to the nearest integer, 2 is returned.
> ```
> 
> **Constraints:**
> - 0 <= x <= 2^{31} - 1

> [!info] Approach
> Binary search on the answer: the answer lies in `[0, x]`. Find the largest integer `mid` such that `mid * mid <= x`. Classic binary search for the last True position in a boolean predicate `mid * mid <= x`. `lo = 0`, `hi = x`. While `lo <= hi`: `mid = (lo + hi) // 2`. If `mid * mid <= x` set `result = mid` and `lo = mid + 1`. Else `hi = mid - 1`.


> [!note]- Python Solution
> ```python
> def my_sqrt(x):
>     if x < 2:
>         return x
>     lo = 1
>     hi = x // 2
>     result = 1
>     while lo <= hi:
>         mid = lo + (hi - lo) // 2
>         squared = mid * mid
>         if squared == x:
>             return mid
>         if squared < x:
>             result = mid
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return result
> ```

> [!success] Complexity
> Time O(log x), Space O(1).

> [!tip] Alternatives
> - Newton's method: `x = x - (x*x - n) / (2*x)`. Converges in O(log log n) iterations — faster in practice.
> - Bit manipulation: set bits from high to low, keep if result doesn't exceed target. O(log n) but less readable.

---

## See Also

[[two-pointers]] | [[array]] | [[sorting]] | [[greedy]]
