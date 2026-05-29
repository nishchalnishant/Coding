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
> Given a sorted array and a target, return the index where target is found, or the index to insert it to keep sorted order.

> [!info] Approach
> - WHY: Need the leftmost index where `arr[i] >= target` — classic lower bound problem.
> - WHAT: Binary search with `hi = len(nums)` because the answer may be one past the last element.
> - HOW: If `nums[mid] < target` → `lo = mid + 1`; else `hi = mid`. Loop terminates at `lo == hi`.

> [!note]- Python Solution
> ```python
> def search_insert(nums: list[int], target: int) -> int:
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
> `isBadVersion(v)` API returns True if version `v` is bad. Bad versions propagate forward. Find the first bad version among `[1..n]`.

> [!info] Approach
> - WHY: The version sequence has a monotone predicate: False…False, True…True. First True is a lower bound problem.
> - WHAT: Binary search on `[1, n]`. If `isBadVersion(mid)` is True, the first bad version is at `mid` or earlier.
> - HOW: `if isBadVersion(mid): hi = mid` (don't discard mid); else `lo = mid + 1`. Terminates at `lo == hi`.

> [!note]- Python Solution
> ```python
> def first_bad_version(n: int) -> int:
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
> Sorted circular list of lowercase letters. Find the smallest letter strictly greater than `target`. Wraps around if no letter qualifies.

> [!info] Approach
> - WHY: Upper bound variant — find first index where `letters[i] > target`.
> - WHAT: Binary search; if `lo` ends at `len(letters)`, no letter qualifies → wrap to `letters[0]`.
> - HOW: If `letters[mid] <= target` → `lo = mid + 1`; else `hi = mid`. Answer is `letters[lo % len]`.

> [!note]- Python Solution
> ```python
> def next_greatest_letter(letters: list[str], target: str) -> str:
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
> Sorted array `citations` in ascending order. Find the largest `h` such that at least `h` papers have ≥ `h` citations.

> [!info] Approach
> - WHY: Array is sorted. For index `i`, there are `n - i` papers with at least `citations[i]` citations. Need the leftmost `i` where `citations[i] >= n - i`.
> - WHAT: Binary search for the leftmost valid index. Then `h = n - i`.
> - HOW: If `citations[mid] < n - mid` → not enough citations here → `lo = mid + 1`; else `hi = mid`.

> [!note]- Python Solution
> ```python
> def h_index(citations: list[int]) -> int:
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
> `piles` of bananas. Eat at constant speed `k` bananas/hour, one pile at a time. Must finish all piles in `h` hours. Minimize `k`.

> [!info] Approach
> - WHY: Larger `k` → fewer hours needed. Monotone: if speed `k` works, any speed `k' > k` also works. Binary search on `k`.
> - WHAT: Search `k` in `[1, max(piles)]`. Feasibility: `sum(ceil(p/k)) <= h`.
> - HOW: `ceil(p/k)` without `math.ceil` → `-(-p // k)`. If feasible → `hi = mid` (try slower); else `lo = mid + 1`.

> [!note]- Python Solution
> ```python
> def min_eating_speed(piles: list[int], h: int) -> int:
>     def feasible(speed: int) -> bool:
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
> Ship packages in order. Ship has fixed capacity per day. Minimize capacity to ship all within `days` days.

> [!info] Approach
> - WHY: Larger capacity → fewer days. Monotone predicate on capacity.
> - WHAT: Search capacity in `[max(weights), sum(weights)]` — minimum needed to ship heaviest package; maximum ships all in one day.
> - HOW: Greedy feasibility: greedily fill each day; when adding next weight exceeds capacity, start a new day.

> [!note]- Python Solution
> ```python
> def ship_within_days(weights: list[int], days: int) -> int:
>     def feasible(cap: int) -> bool:
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
> Split `nums` into exactly `k` non-empty contiguous subarrays. Minimize the largest subarray sum.

> [!info] Approach
> - WHY: Larger allowed max-sum → easier to fit into `k` parts. Monotone predicate on the answer value.
> - WHAT: Binary search on `max_sum` in `[max(nums), sum(nums)]`. Feasibility: greedy partition counting.
> - HOW: Greedily extend current subarray; when adding next element would exceed `max_sum`, start new part. If parts ≤ k → feasible.

> [!note]- Python Solution
> ```python
> def split_array(nums: list[int], k: int) -> int:
>     def feasible(max_sum: int) -> bool:
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
> Sorted gas station positions. Add `k` new stations anywhere. Minimize the maximum gap between adjacent stations.

> [!info] Approach
> - WHY: Smaller allowed gap → more stations needed. Monotone on gap size → binary search on floating-point answer.
> - WHAT: Search `d` in `[0, stations[-1] - stations[0]]`. For each existing gap `g`, stations needed = `floor(g / d)`.
> - HOW: 100 iterations of binary search achieves precision ~1e-30, well within the required 1e-6.

> [!note]- Python Solution
> ```python
> def min_max_gas_dist(stations: list[int], k: int) -> float:
>     def feasible(d: float) -> bool:
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
> `n` sequential trains at integer speed `v`. Each intermediate train departs on the next integer hour. Last train can stop mid-hour. Minimize speed to arrive within `hour`.

> [!info] Approach
> - WHY: Higher speed → arrive earlier. Monotone integer predicate.
> - WHAT: Search `v` in `[1, 10^7]`. Each intermediate leg takes `ceil(d/v)` hours; last leg takes `d/v` (fractional OK).
> - HOW: Early exit: if `hour <= n - 1`, impossible (each of `n-1` waits costs at least 1 hour).

> [!note]- Python Solution
> ```python
> import math
> 
> def min_speed_on_time(dist: list[int], hour: float) -> int:
>     n = len(dist)
>     if hour <= n - 1:
>         return -1   # each intermediate stop waits for next integer hour
> 
>     def feasible(v: int) -> bool:
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
> Array sorted then rotated at unknown pivot. No duplicates. Return index of target or -1.

> [!info] Approach
> - WHY: Not fully sorted, but one half around any `mid` is always sorted. Use that to make a binary decision.
> - WHAT: Standard BS with an extra check — determine the sorted half, test if target is in it.
> - HOW: If `nums[lo] <= nums[mid]`, left half `[lo, mid]` is sorted. If target in `[nums[lo], nums[mid])` → go left; else go right.

> [!note]- Python Solution
> ```python
> def search(nums: list[int], target: int) -> int:
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
> Rotated sorted array, no duplicates. Find the minimum element.

> [!info] Approach
> - WHY: Minimum is the rotation boundary. Compare `nums[mid]` with `nums[hi]`: if `nums[mid] > nums[hi]`, the minimum must be to the right.
> - WHAT: Binary search shrinking toward the minimum. Invariant: minimum is always in `[lo, hi]`.
> - HOW: `if nums[mid] > nums[hi]: lo = mid + 1` else `hi = mid`. Do NOT compare with `nums[lo]`.

> [!note]- Python Solution
> ```python
> def find_min(nums: list[int]) -> int:
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
> Rotated sorted array *with duplicates*. Return True if target exists.

> [!info] Approach
> - WHY: Duplicates create ambiguity: when `nums[lo] == nums[mid] == nums[hi]`, we cannot determine which half is sorted.
> - WHAT: Same logic as LC 33 with an extra degenerate case to shrink both boundaries.
> - HOW: On ambiguity → `lo += 1; hi -= 1`. Worst case O(n) for all-same arrays.

> [!note]- Python Solution
> ```python
> def search_with_dups(nums: list[int], target: int) -> bool:
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
> Rotated sorted array with duplicates. Find the minimum.

> [!info] Approach
> - WHY: Same as LC 153 but `nums[mid] == nums[hi]` is now possible — can't determine which half contains the minimum.
> - WHAT: When equal, safely shrink `hi` by 1 (minimum is not lost since `nums[mid] == nums[hi]`).
> - HOW: Three-way branch on `nums[mid]` vs `nums[hi]`.

> [!note]- Python Solution
> ```python
> def find_min_with_dups(nums: list[int]) -> int:
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
> Array with no adjacent equal elements, `nums[-1] = nums[n] = -∞`. Find any peak index (element > both neighbors).

> [!info] Approach
> - WHY: If `nums[mid] < nums[mid+1]`, the slope is ascending to the right — a peak must exist in `[mid+1, hi]`. Symmetric for descending slope.
> - WHAT: Invariant: a peak always exists in `[lo, hi]`. Shrink toward the uphill side.
> - HOW: `if nums[mid] < nums[mid+1]: lo = mid + 1` else `hi = mid`. Terminates at `lo == hi` which is a peak.

> [!note]- Python Solution
> ```python
> def find_peak_element(nums: list[int]) -> int:
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
> Array guaranteed to be strictly unimodal (increases then decreases). Find the peak index.

> [!info] Approach
> - WHY: Strictly unimodal — same ascending/descending slope argument as LC 162. Unique peak guaranteed.
> - WHAT: Identical binary search structure. `nums[mid] < nums[mid+1]` → still ascending → peak is right.
> - HOW: Same code as LC 162; mountain guarantee makes the result unique.

> [!note]- Python Solution
> ```python
> def peak_index_in_mountain_array(arr: list[int]) -> int:
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
> m × n matrix. Find any cell strictly greater than all 4-directional neighbors (edges treated as -∞).

> [!info] Approach
> - WHY: Binary search on columns. At column `mid`, find the row with the maximum value in that column. That row-maximum is either a 2D peak (exceeds left/right neighbors), or its larger neighbor points us toward a column containing a peak.
> - WHAT: Binary search on columns `[lo, hi]`. At `mid_col`, find `max_row`. Compare with left/right columns.
> - HOW: If `mat[max_row][mid_col] < mat[max_row][mid_col+1]` → a peak exists to the right; else left or at mid.

> [!note]- Python Solution
> ```python
> def find_peak_grid(mat: list[list[int]]) -> list[int]:
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
> Two sorted arrays. Find the median in O(log(m+n)) time.

> [!info] Approach
> - WHY: Merging is O(m+n). The median partitions the combined array so the left half has `(m+n)//2` elements. Binary search on the partition in the smaller array.
> - WHAT: For each partition `i` in `nums1`, the partition `j = half - i` in `nums2` is determined. Valid when `max_left_A ≤ min_right_B` AND `max_left_B ≤ min_right_A`.
> - HOW: If `max_left1 > min_right2` → partition too far right in nums1 → `hi = i - 1`; else `lo = i + 1`.

> [!note]- Python Solution
> ```python
> def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
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
> n × n matrix, each row and column sorted ascending. Find the kth smallest element.

> [!info] Approach
> - WHY: "How many elements ≤ x?" is a monotone function of x. Binary search on the value range.
> - WHAT: Search value `d` in `[matrix[0][0], matrix[n-1][n-1]]`. Count elements ≤ d using staircase traversal O(n).
> - HOW: Start top-right. If `matrix[row][col] <= d` → all `col+1` elements in this row qualify → `row += 1`; else `col -= 1`. If count ≥ k → `hi = mid`; else `lo = mid + 1`. Answer is always an actual matrix element.

> [!note]- Python Solution
> ```python
> def kth_smallest(matrix: list[list[int]], k: int) -> int:
>     n = len(matrix)
> 
>     def count_le(d: int) -> int:
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
> Array of integers. Among all O(n²) pairs `(i, j)` with `i < j`, find the kth smallest absolute difference.

> [!info] Approach
> - WHY: Cannot enumerate all O(n²) pairs. "How many pairs have distance ≤ d?" is monotone in d → binary search on distance.
> - WHAT: Sort array. Search distance `d` in `[0, nums[-1] - nums[0]]`. Count pairs with distance ≤ d via two-pointer sliding window.
> - HOW: For each `right`, advance `left` while `nums[right] - nums[left] > d`. Pairs ending at `right` with distance ≤ d = `right - left`. If count ≥ k → `hi = mid`; else `lo = mid + 1`.

> [!note]- Python Solution
> ```python
> def smallest_distance_pair(nums: list[int], k: int) -> int:
>     nums.sort()
>     n = len(nums)
> 
>     def count_pairs_le(d: int) -> int:
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
> Given an m×n matrix where each row is sorted and the first element of each row is greater than the last element of the previous row. Search for a target. Return true/false.

> [!info] Approach
> - WHY: Matrix has a total order — treat it as a 1D sorted array of m*n elements.
> - WHAT: Virtual binary search on index 0..m*n-1. Map mid → row=mid//n, col=mid%n.
> - HOW: lo=0, hi=m*n-1. While lo<=hi: mid=(lo+hi)//2; val=matrix[mid//n][mid%n]. Compare with target, standard binary search logic.

> [!note]- Python Solution
> ```python
> def search_matrix(matrix: list[list[int]], target: int) -> bool:
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
> Given an m×n matrix where each row and each column is sorted in ascending order. Search for a target. Return true/false.

> [!info] Approach
> - WHY: Rows AND columns are sorted but rows don't have total order (first of row i+1 may be less than last of row i). Can't treat as a 1D sorted array.
> - WHAT: Staircase search — start from the top-right corner. If matrix[r][c] == target: found. If > target: go left (c--). If < target: go down (r++).
> - HOW: Each step eliminates a row or column. O(m+n) total.

> [!note]- Python Solution
> ```python
> def search_matrix_ii(matrix: list[list[int]], target: int) -> bool:
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
> A number is picked in `[1, n]`. An API `guess(num)` returns -1 (pick < num), 1 (pick > num), or 0 (correct). Find the picked number.

> [!info] Approach
> - WHY: Search space `[1, n]` is totally ordered and the API gives three-way comparison — textbook binary search.
> - WHAT: Standard BS template with the API replacing a direct comparison.
> - HOW: `lo=1, hi=n`. While `lo <= hi`: if `guess(mid)==0` return mid; if `guess(mid)==-1` the answer is lower → `hi=mid-1`; else `lo=mid+1`.

> [!note]- Python Solution
> ```python
> def guess_number(n: int) -> int:
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
> Sorted array of integers, possibly with duplicates. Find the starting and ending position of a given target. Return `[-1, -1]` if not found.

> [!info] Approach
> - WHY: Need leftmost and rightmost occurrence — two separate lower/upper bound searches.
> - WHAT: `bisect_left` gives the first index where `nums[i] >= target`; `bisect_right` gives the first index where `nums[i] > target` (so last occurrence = that - 1).
> - HOW: First = lower_bound(target). If `nums[first] != target` → not found. Last = upper_bound(target) - 1.

> [!note]- Python Solution
> ```python
> def search_range(nums: list[int], target: int) -> list[int]:
>     def lower_bound(val: int) -> int:
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
> `bloomDay[i]` = day flower `i` blooms. Make `m` bouquets, each requiring `k` **adjacent** bloomed flowers. Minimum day to make all `m` bouquets (or -1 if impossible).

> [!info] Approach
> - WHY: More days → more flowers bloomed → easier to form bouquets. Monotone predicate on day.
> - WHAT: Binary search on `day` in `[min(bloomDay), max(bloomDay)]`. Feasibility: scan the array counting consecutive bloomed flowers; form a bouquet every time we accumulate `k` in a row.
> - HOW: Count bouquets formed; if `>= m` → feasible. Early exit: if `m * k > len(bloomDay)` → impossible.

> [!note]- Python Solution
> ```python
> def min_days(bloomDay: list[int], m: int, k: int) -> int:
>     n = len(bloomDay)
>     if m * k > n:
>         return -1
> 
>     def feasible(day: int) -> bool:
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
> Sorted array `arr` and integers `k`, `x`. Return the `k` closest elements to `x`, sorted ascending. Ties broken by smaller value.

> [!info] Approach
> - WHY: The answer is always a contiguous subarray of length `k`. Binary search for the left boundary of this window.
> - WHAT: Search left index `i` in `[0, len(arr) - k]`. Window `[i, i+k)` is optimal if `x - arr[i] <= arr[i+k] - x` (left element is at least as close as the right element just outside).
> - HOW: If `x - arr[mid] > arr[mid+k] - x` → window is too far left → `lo = mid + 1`; else `hi = mid`. Answer is `arr[lo : lo + k]`.

> [!note]- Python Solution
> ```python
> def find_closest_elements(arr: list[int], k: int, x: int) -> list[int]:
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
> For each `nums[i]`, count how many elements to its right are strictly smaller. Return the counts array.

> [!info] Approach
> - WHY: Process right to left, maintaining a sorted structure. Binary search for insertion position gives the count of smaller elements already seen.
> - WHAT: Build a sorted list of "seen" elements (right to left). For each new element, `bisect_left` gives its insertion rank = count of smaller elements to its right.
> - HOW: Insert `nums[i]` into the sorted list (using `insort`). Count = `bisect_left(sorted_list, nums[i])`.

> [!note]- Python Solution
> ```python
> from bisect import bisect_left, insort
> 
> def count_smaller(nums: list[int]) -> list[int]:
>     sorted_seen: list[int] = []
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
> Same as LC 74 but solved explicitly with two binary searches: first find the row, then search within it.

> [!info] Approach
> - WHY: Useful when the single-index trick is not obvious in an interview. Also illustrates composing two independent binary searches.
> - WHAT: BS on rows: find the last row where `matrix[row][0] <= target` (this is the only row that can contain target). Then BS within that row.
> - HOW: Row search: `if matrix[mid][0] <= target: lo = mid` else `hi = mid - 1`. Then standard column search.

> [!note]- Python Solution
> ```python
> def search_matrix_two_pass(matrix: list[list[int]], target: int) -> bool:
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
> Given a non-negative integer `x`, return the integer square root (floor). Do not use `sqrt()`.

> [!info] Approach
> - WHY: Find the largest integer `k` such that `k² <= x`. Classic "find upper bound of predicate" problem.
> - WHAT: Binary search `k` in `[0, x]` (or `[0, x//2 + 1]` for efficiency). Find the last `k` where `k*k <= x`.
> - HOW: If `mid * mid <= x` → `lo = mid + 1` (can go larger); else `hi = mid - 1`. Answer is `hi` (the last valid mid).

> [!note]- Python Solution
> ```python
> def my_sqrt(x: int) -> int:
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
> Array of `n+1` integers, each in `[1, n]`. Exactly one duplicate (may repeat multiple times). Find it. O(1) extra space required.

> [!info] Approach
> - WHY: Count of integers in `[1, mid]` that appear in `nums` — if > `mid`, by pigeonhole the duplicate is ≤ `mid`. Monotone predicate → binary search on value.
> - WHAT: Search `mid` in `[1, n]`. Count elements in `nums` that are `<= mid`. If count > mid → duplicate in lower half.
> - HOW: `if count > mid: hi = mid` else `lo = mid + 1`. Not a standard in-place BS — it's BS on the value space, not the index space.

> [!note]- Python Solution
> ```python
> def find_duplicate(nums: list[int]) -> int:
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
> Find the length of the longest strictly increasing subsequence in `nums`.

> [!info] Approach
> - WHY: Patience sorting uses a `tails` array where `tails[i]` is the smallest tail of all LIS of length `i+1`. `tails` is always sorted → binary search for insertion point.
> - WHAT: For each element, `bisect_left(tails, num)` gives the position to replace (or extend if at end). The length of `tails` at the end is the LIS length.
> - HOW: If `num > tails[-1]` → append (extend LIS). Else → replace `tails[pos]` = num (maintain smallest tails for future options).

> [!note]- Python Solution
> ```python
> from bisect import bisect_left
> 
> def length_of_lis(nums: list[int]) -> int:
>     tails: list[int] = []
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
