---
tags: [coding, algorithms, binary-search]
topic: Binary Search
difficulty: mixed
---

# Binary Search — Amazon SDE-2

## Core Templates

**Exact search (find target):** `lo=0, hi=n-1`, `while lo <= hi`, return `mid` on hit or `-1`.
**Lower bound (leftmost insert):** `lo=0, hi=n`, `while lo < hi`, `hi=mid` on `arr[mid] >= target`. Returns `lo`.
**Upper bound (first strictly greater):** same but `hi=mid` on `arr[mid] > target`.

Key: use `mid = lo + (hi - lo) // 2` to avoid overflow.

---

## Sorted Array Search

### Search Insert Position (LC 35)

> [!info] Approach
> Leftmost index where `arr[i] >= target` — lower bound. `hi = len(nums)` because answer may be one past last. `if nums[mid] < target: lo = mid+1` else `hi = mid`.

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

---

### Find First and Last Position (LC 34)

> [!info] Approach
> Two lower-bound searches. First = `bisect_left(target)`. If `nums[first] != target` → not found. Last = `bisect_left(target+1) - 1`.

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
>     return [first, lower_bound(target + 1) - 1]
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

---

### First Bad Version (LC 278)

> [!info] Approach
> Sequence is False...True. First True = lower bound. `if isBadVersion(mid): hi = mid` else `lo = mid + 1`. Never discard mid when it could be the answer.

> [!note]- Python Solution
> ```python
> def first_bad_version(n):
>     lo, hi = 1, n
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if isBadVersion(mid):
>             hi = mid
>         else:
>             lo = mid + 1
>     return lo
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

---

## Rotated Sorted Array

> [!info] Pattern
> Split at `mid` always yields one sorted half and one unsorted half. Determine which half is sorted by comparing endpoints, then test if target is in the sorted half.

### Search in Rotated Sorted Array (LC 33)

> [!note]- Python Solution
> ```python
> def search(nums, target):
>     lo, hi = 0, len(nums) - 1
>     while lo <= hi:
>         mid = lo + (hi - lo) // 2
>         if nums[mid] == target:
>             return mid
>         if nums[lo] <= nums[mid]:               # left half sorted
>             if nums[lo] <= target < nums[mid]:
>                 hi = mid - 1
>             else:
>                 lo = mid + 1
>         else:                                   # right half sorted
>             if nums[mid] < target <= nums[hi]:
>                 lo = mid + 1
>             else:
>                 hi = mid - 1
>     return -1
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

---

### Find Minimum in Rotated Sorted Array (LC 153)

> [!info] Approach
> Compare `nums[mid]` with `nums[hi]`. If `nums[mid] > nums[hi]` → min is in right half. Never compare with `nums[lo]`.

> [!note]- Python Solution
> ```python
> def find_min(nums):
>     lo, hi = 0, len(nums) - 1
>     while lo < hi:
>         mid = lo + (hi - lo) // 2
>         if nums[mid] > nums[hi]:
>             lo = mid + 1
>         else:
>             hi = mid
>     return nums[lo]
> ```

> [!success] Complexity
> O(log n) time, O(1) space.

---

## Search on Answer Space (Predicate Pattern)

> [!info] Pattern
> When asked to *minimize the maximum* or *maximize the minimum*, define a monotone feasibility predicate `f(x)` and binary search on `x` directly. Feasibility check is typically O(n) greedy → whole solution O(n log W).
> Template: `if feasible(mid): hi = mid` else `lo = mid + 1`. Answer is `lo`.

### Koko Eating Bananas (LC 875)

> [!info] Approach
> Larger speed → fewer hours. Search speed in `[1, max(piles)]`. Feasibility: `sum(ceil(p/k)) <= h`. Use `-(-p // speed)` for ceiling without `math.ceil`.

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

---

### Capacity to Ship Packages (LC 1011)

> [!info] Approach
> Larger capacity → fewer days. Search capacity in `[max(weights), sum(weights)]`. Greedy feasibility: fill each day greedily; start new day when next weight exceeds capacity.

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

> [!tip] Note
> Structurally identical to Split Array Largest Sum (LC 410) — same template.

---

### Split Array Largest Sum (LC 410)

> [!info] Approach
> Larger allowed max-sum → easier to fit `k` parts. Search `max_sum` in `[max(nums), sum(nums)]`. Greedy feasibility: count partitions needed.

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

---

## See Also

[[two-pointers]] | [[sliding-window]] | [[sorting]] | [[dynamic-programming]]
