---
tags: [coding, data-structures, array]
topic: array
difficulty: mixed
---

# Array Problems — Deep Dive

---

## Two Pointers

### Two Sum (sorted variant)

> [!example] Problem
> Given a 1-indexed sorted array and a target, return the indices of the two numbers that add up to the target. Exactly one solution exists.

> [!info] Approach
> **Two Pointers on sorted array.**
> WHY: The array is sorted — we can exploit this. A pair either has too-small a sum (advance left) or too-large a sum (advance right). No pair is missed because every skip is provably invalid.
> WHAT: Two pointers at opposite ends converging inward based on sum comparison.
> HOW: `l=0, r=n-1`. If `numbers[l] + numbers[r] == target`, done. If sum < target, `l++` (we need larger). If sum > target, `r--` (we need smaller). The sorted invariant guarantees we never skip valid pairs.

> [!note]- Python Solution
> ```python
> def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
>     l, r = 0, len(numbers) - 1
>     while l < r:
>         s = numbers[l] + numbers[r]
>         if s == target:
>             return [l + 1, r + 1]  # 1-indexed
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

### 3Sum

> [!example] Problem
> Given an unsorted array, find all unique triplets that sum to zero.

> [!info] Approach
> **Fix + Two Pointers.**
> WHY: Brute force O(n³) is too slow. Fixing one element reduces it to a 2Sum on the remaining sorted suffix.
> WHAT: Sort once, fix `nums[i]`, run two pointers on `i+1..n-1`.
> HOW: Sort. For each `i`, if `nums[i] > 0` break (sorted — no triplet can sum to 0). Skip duplicate `i`. Run two-pointer on the suffix. On match, skip duplicate `left` and `right` before advancing both. Three deduplication sites: `i`, `left`, `right`.
> Interview note: sorting is what makes the duplicate skipping and early break safe, so this pattern is usually the cleanest solution in interviews.

> [!note]- Python Solution
> ```python
> def three_sum(nums: list[int]) -> list[list[int]]:
>     nums.sort()
>     result: list[list[int]] = []
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

### 3Sum Closest

> [!example] Problem
> Find the triplet whose sum is closest to a given target. Return the sum.

> [!info] Approach
> **Sort + Two Pointers with closest tracking.**
> WHY: Same sorted + two-pointer framework as 3Sum, but instead of equality we track the minimum distance.
> WHAT: Track `closest` as best sum seen. After computing current sum, advance `l` or `r` to pull sum toward target.
> HOW: Sort. For each `i`, two-pointer on suffix. Compute `s = nums[i]+nums[l]+nums[r]`. Update `closest` if `|s - target| < |closest - target|`. If `s < target`, `l++`. If `s > target`, `r--`. If exact match, return immediately.

> [!note]- Python Solution
> ```python
> def three_sum_closest(nums: list[int], target: int) -> int:
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

### 4Sum

> [!example] Problem
> Find all unique quadruplets in an array that sum to a target.

> [!info] Approach
> **Two nested loops + Two Pointers.**
> WHY: Generalizes 3Sum by adding one more fixed element. Fix two elements (i, j) and run two pointers on the rest.
> WHAT: Two nested loops fix first two elements; two pointers find the last two. Deduplicate at all four levels.
> HOW: Sort. Outer loop `i`, inner loop `j = i+1`. Skip duplicate `i` and `j`. Two pointers `l=j+1, r=n-1`. Same pointer logic as 3Sum. Early termination: if the smallest possible sum for the current `i` is already too large, break; if the largest possible sum is still too small, continue.

> [!note]- Python Solution
> ```python
> def four_sum(nums: list[int], target: int) -> list[list[int]]:
>     nums.sort()
>     n = len(nums)
>     result: list[list[int]] = []
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

### Container with Most Water

> [!example] Problem
> Given heights of vertical lines, find the two lines that form a container holding the maximum water.

> [!info] Approach
> **Two Pointers — advance the shorter line.**
> WHY: Area = min(height[l], height[r]) × (r - l). To maximize, we must consider both height and width. Brute force O(n²) tries all pairs.
> WHAT: Two pointers. The width decreases as pointers converge, so we must compensate with greater height.
> HOW: `l=0, r=n-1`. Compute area. Always advance the pointer pointing to the shorter line — moving the taller line can never increase `min(h[l], h[r])` while width also decreases.

> [!note]- Python Solution
> ```python
> def max_area(height: list[int]) -> int:
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

### Trapping Rain Water

> [!example] Problem
> Given an elevation map, compute how much water can be trapped after raining.

> [!info] Approach
> **Two Pointers — binding constraint side.**
> WHY: Water at index `i` is bounded by `min(max_left, max_right) - height[i]`. We need left-max and right-max for every position.
> WHAT: Two pointers eliminating the need for prefix/suffix arrays. The side with the smaller max is the binding constraint.
> HOW: `l=0, r=n-1`, `l_max=r_max=0`. If `l_max <= r_max`, the left side is the constraint, so water at `l` is `l_max - height[l]` and we advance `l`. Otherwise, the right side is the constraint, so water at `r` is `r_max - height[r]` and we decrement `r`.

> [!note]- Python Solution
> ```python
> def trap(height: list[int]) -> int:
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
> Remove duplicates from a sorted array in-place; return the new length. Relative order must be preserved.

> [!info] Approach
> **Two Pointers — slow/fast write pattern.**
> WHY: Sorted guarantees duplicates are adjacent. We need one pointer tracking the write position (valid prefix) and one scanning forward.
> WHAT: Two pointers — `slow` marks next write index, `fast` scans for new values.
> HOW: `slow=1`. For `fast` in `1..n-1`: if `nums[fast] != nums[slow-1]`, write `nums[slow] = nums[fast]`, `slow++`. Return `slow`.

> [!note]- Python Solution
> ```python
> def remove_duplicates(nums: list[int]) -> int:
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

### Next Permutation

> [!example] Problem
> Rearrange `nums` into the lexicographically next greater permutation in-place. If it's the largest, rearrange to the smallest (ascending order).

> [!info] Approach
> **Three-step: find rightmost descent, swap, reverse suffix.**
> WHY: A permutation is "next" if we increment the rightmost possible position. We find the rightmost "dip" — a position where the element is smaller than something to its right.
> WHAT: Three-step algorithm: find rightmost descent, swap with next-larger suffix element, reverse the suffix.
> HOW:
> 1. Scan right-to-left to find index `i` where `nums[i] < nums[i+1]` (rightmost ascending pair from the right).
> 2. If none found, the whole array is descending — just reverse it.
> 3. From the right, find the smallest element greater than `nums[i]`; swap them.
> 4. Reverse `nums[i+1:]` to get the smallest permutation of the suffix.

> [!note]- Python Solution
> ```python
> def next_permutation(nums: list[int]) -> None:
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
> Given a binary array, you can flip at most `k` zeros to ones. Return the maximum length of a subarray of all ones.

> [!info] Approach
> **Variable sliding window — zero count tracking.**
> WHY: We want the longest window containing at most `k` zeros. This is monotone: a larger window is valid as long as zero-count ≤ k.
> WHAT: Variable sliding window tracking zero count.
> HOW: Expand `r`. If `nums[r] == 0`, increment zero count. If zeros > k, shrink `l` until zeros ≤ k (moving `l` past a zero decrements zero count). Track `r - l + 1` as window size.

> [!note]- Python Solution
> ```python
> def longest_ones(nums: list[int], k: int) -> int:
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

### Longest Repeating Character Replacement

> [!example] Problem
> Given a string and integer `k`, replace at most `k` characters to make the longest substring of a single repeating character.

> [!info] Approach
> **Variable window with monotone max_freq trick.**
> WHY: The valid condition for a window is: `window_len - max_freq_char ≤ k`. Characters that aren't the majority must be replaced.
> WHAT: Variable window with frequency map. Track `max_freq` (highest frequency of any character in window).
> HOW: Expand `r`. Update freq map. If `(r - l + 1) - max_freq > k`, shrink `l` by one (decrement freq of `s[l]`). Key insight: `max_freq` never needs to decrease — a smaller `max_freq` cannot yield a larger valid window.

> [!note]- Python Solution
> ```python
> def character_replacement(s: str, k: int) -> int:
>     freq: dict[str, int] = {}
>     l = max_freq = best = 0
>     for r, ch in enumerate(s):
>         freq[ch] = freq.get(ch, 0) + 1
>         max_freq = max(max_freq, freq[ch])
>         if (r - l + 1) - max_freq > k:
>             freq[s[l]] -= 1
>             l += 1
>         best = max(best, r - l + 1)
>     return best
> ```

> [!success] Complexity
> Time O(n), Space O(1) (26 letters max).

> [!tip] Alternatives
> - Recompute max freq on every shrink: O(26n) = O(n). Correct but `max_freq` monotone trick avoids it.
> - Binary search on answer: O(n log n). Not needed.

---

### Subarrays with K Different Integers

> [!example] Problem
> Count subarrays with exactly `k` distinct integers.

> [!info] Approach
> **Exactly-k = at_most(k) − at_most(k−1).**
> WHY: Sliding window with exact count is non-monotone — a window can become invalid as it grows but also as elements fall out. Direct counting is intractable.
> WHAT: Transform "exactly k" to "at most k" − "at most k−1". The "at most k" function is monotone.
> HOW: `at_most(k)` counts subarrays with ≤ k distinct integers. Use standard sliding window: expand right, if distinct count > k shrink left, add `r - l + 1` (all subarrays ending at `r` and starting at `l..r`). Answer = `at_most(k) - at_most(k-1)`.

> [!note]- Python Solution
> ```python
> def subarrays_with_k_distinct(nums: list[int], k: int) -> int:
>     def at_most(k: int) -> int:
>         count: dict[int, int] = {}
>         l = res = 0
>         for r, x in enumerate(nums):
>             count[x] = count.get(x, 0) + 1
>             while len(count) > k:
>                 count[nums[l]] -= 1
>                 if count[nums[l]] == 0:
>                     del count[nums[l]]
>                 l += 1
>             res += r - l + 1
>         return res
> 
>     return at_most(k) - at_most(k - 1)
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Direct exact-k sliding window with two pointers marking left boundary range: O(n), same complexity, more complex implementation.

---

### Minimum Window Substring

> [!example] Problem
> Find the minimum window in `s` that contains all characters of `t` (including duplicates).

> [!info] Approach
> **Sliding window with `have` counter.**
> WHY: We need to find a window satisfying a multi-character frequency requirement. The window is shrinkable once all requirements are met.
> WHAT: Sliding window with a `have` counter tracking how many distinct characters have met their required frequency.
> HOW: Build `need` freq map for `t`. Expand `r`. For each char, if its count in window hits required count, `have++`. When `have == len(need)`, try to shrink: record window, shrink `l`. If removing `s[l]` drops a count below required, `have--`.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def min_window(s: str, t: str) -> str:
>     if not t or not s:
>         return ""
>     need = Counter(t)
>     have, required = 0, len(need)
>     window: dict[str, int] = {}
>     best_l, best_r = 0, float('inf')
>     l = 0
>     for r, ch in enumerate(s):
>         window[ch] = window.get(ch, 0) + 1
>         if ch in need and window[ch] == need[ch]:
>             have += 1
>         while have == required:
>             if r - l < best_r - best_l:
>                 best_l, best_r = l, r
>             lch = s[l]
>             window[lch] -= 1
>             if lch in need and window[lch] < need[lch]:
>                 have -= 1
>             l += 1
>     return s[best_l:best_r + 1] if best_r != float('inf') else ""
> ```

> [!success] Complexity
> Time O(|s| + |t|), Space O(|t|).

> [!tip] Alternatives
> - Filter `s` to only positions containing characters in `t` (optimized for sparse `t`): reduces effective n. Same asymptotic, better constant when `|t| << |s|`.

---

### Sliding Window Maximum

> [!example] Problem
> Return the maximum in each sliding window of size `k`.

> [!info] Approach
> **Monotonic decreasing deque.**
> WHY: Naively recomputing max per window is O(nk). We need a structure that maintains max as the window slides.
> WHAT: Monotonic decreasing deque — front is always the current window max. Rear elements smaller than the incoming element are useless (they'll never be max while this element is in window).
> HOW: For each `r`: pop rear of deque while `deque` is non-empty and `nums[deque[-1]] <= nums[r]`. Append `r`. Pop front if `deque[0] <= r - k` (out of window). Once `r >= k-1`, the front index gives the current window max.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def max_sliding_window(nums: list[int], k: int) -> list[int]:
>     dq: deque[int] = deque()  # stores indices
>     result: list[int] = []
>     for r in range(len(nums)):
>         # Remove elements outside window
>         while dq and dq[0] <= r - k:
>             dq.popleft()
>         # Maintain decreasing order
>         while dq and nums[dq[-1]] <= nums[r]:
>             dq.pop()
>         dq.append(r)
>         if r >= k - 1:
>             result.append(nums[dq[0]])
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(k).

> [!tip] Alternatives
> - Segment tree or sparse table: O(n log n) build, O(1) query. Overkill; deque is optimal.
> - Max-heap: O(n log n) — need lazy deletion to remove expired elements; more complex.

---

## Prefix Sum

### Subarray Sum Equals K

> [!example] Problem
> Count the number of contiguous subarrays whose sum equals `k`. Array can contain negative numbers.

> [!info] Approach
> **Prefix sum + hash map complement lookup.**
> WHY: Sliding window fails with negatives (sum not monotone). Prefix sum enables O(1) range sum computation.
> WHAT: For any subarray `[l, r]`: `sum = prefix[r] - prefix[l-1]`. We need `prefix[r] - prefix[l-1] == k`, i.e., `prefix[l-1] == prefix[r] - k`. Count previous prefix sums equal to `prefix[r] - k`.
> HOW: Scan left to right, maintaining `running_sum` and a hash map `seen` of count of each prefix sum seen so far. Seed `seen[0] = 1` (empty prefix). For each element, `count += seen[running_sum - k]`.

> [!note]- Python Solution
> ```python
> def subarray_sum(nums: list[int], k: int) -> int:
>     seen: dict[int, int] = {0: 1}
>     running = count = 0
>     for x in nums:
>         running += x
>         count += seen.get(running - k, 0)
>         seen[running] = seen.get(running, 0) + 1
>     return count
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Brute force O(n²): compute all subarray sums directly. Too slow for large n.
> - Sliding window: fails on arrays with negative numbers.

---

### Subarray Sums Divisible by K

> [!example] Problem
> Count subarrays whose sum is divisible by `k`.

> [!info] Approach
> **Prefix modulo — same remainder pairs.**
> WHY: `sum(l..r) % k == 0` iff `prefix[r] % k == prefix[l-1] % k`. Two positions with the same remainder have a "zero-remainder" gap between them.
> WHAT: Store frequency of each `prefix % k` seen. Count same-remainder pairs.
> HOW: Scan with `running % k`. Handle negative modulo: `(running % k + k) % k`. Seed `seen[0] = 1`. For each position, `count += seen[running % k]` before incrementing.

> [!note]- Python Solution
> ```python
> def subarrays_div_by_k(nums: list[int], k: int) -> int:
>     seen: dict[int, int] = {0: 1}
>     running = count = 0
>     for x in nums:
>         running += x
>         rem = (running % k + k) % k  # normalize negative modulo
>         count += seen.get(rem, 0)
>         seen[rem] = seen.get(rem, 0) + 1
>     return count
> ```

> [!success] Complexity
> Time O(n), Space O(k) (at most k distinct remainders).

> [!tip] Alternatives
> - Brute force O(n²): compute subarray sums directly.
> - Python's `%` is always non-negative so normalization is Python-specific bonus; in Java/C++, it's essential.

---

### Continuous Subarray Sum

> [!example] Problem
> Check if there exists a subarray of length ≥ 2 whose sum is a multiple of `k`.

> [!info] Approach
> **Prefix modulo — first-occurrence index map.**
> WHY: Same modulo insight as above. `sum(l..r) % k == 0` iff `prefix[r] % k == prefix[l-1] % k`. Additionally require length ≥ 2, meaning indices must be at least 2 apart.
> WHAT: Map `remainder → first index` seen. On seeing the same remainder again, check index gap ≥ 2.
> HOW: Seed `seen[0] = -1` (empty prefix at index -1). For each index `i`, compute `rem`. If `rem in seen` and `i - seen[rem] >= 2`, return True. Otherwise, record `rem → i` only if not already present (want first occurrence).

> [!note]- Python Solution
> ```python
> def check_subarray_sum(nums: list[int], k: int) -> bool:
>     seen: dict[int, int] = {0: -1}
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

### Product of Array Except Self

> [!example] Problem
> Return an array where `output[i]` is the product of all elements except `nums[i]`. No division. O(n) time, O(1) extra space.

> [!info] Approach
> **Two-pass left/right product accumulation.**
> WHY: Division is disallowed (and breaks on zeros). We can compute left-product prefix and right-product suffix.
> WHAT: Two-pass: first build left products into output, then multiply by right products on a second right-to-left pass using a running variable.
> HOW: Pass 1: `output[i] = product of nums[0..i-1]`. Pass 2: maintain `right = 1`, scan right to left, multiply `output[i] *= right`, then `right *= nums[i]`.

> [!note]- Python Solution
> ```python
> def product_except_self(nums: list[int]) -> list[int]:
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

### Maximum Subarray

> [!example] Problem
> Find the contiguous subarray with the largest sum. Return the sum.

> [!info] Approach
> **Kadane's algorithm — local reset on negative prefix.**
> WHY: At each position, either start a new subarray here or extend the current one — whichever is larger. The decision is local and optimal.
> WHAT: Kadane's algorithm: `cur = max(nums[i], cur + nums[i])`. This captures "reset if current prefix hurts".
> HOW: Initialize `cur = best = nums[0]` (handles all-negative case). For each subsequent element: `cur = max(x, cur + x)`. Update `best = max(best, cur)`.

> [!note]- Python Solution
> ```python
> def max_subarray(nums: list[int]) -> int:
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

### Maximum Product Subarray

> [!example] Problem
> Find the contiguous subarray with the largest product. Return the product.

> [!info] Approach
> **Track max and min simultaneously.**
> WHY: Products differ from sums: a large negative × large negative = large positive. We can't just track max — we must also track min (most negative) because a future negative can flip it to max.
> WHAT: Track `max_prod` and `min_prod` at each position. On negative element, swap them before multiplying.
> HOW: At each element `x`: new `max_prod = max(x, max_prod * x, min_prod * x)`, new `min_prod = min(x, max_prod * x, min_prod * x)`. Use temps to avoid overwriting. Update global best.

> [!note]- Python Solution
> ```python
> def max_product(nums: list[int]) -> int:
>     max_p = min_p = best = nums[0]
>     for x in nums[1:]:
>         candidates = (x, max_p * x, min_p * x)
>         max_p, min_p = max(candidates), min(candidates)
>         best = max(best, max_p)
>     return best
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Prefix/suffix product scan: For each zero crossing, products reset. Scan left-to-right and right-to-left, skip zeros; take max of both scans. O(n) time, O(1) space. Different mental model but equivalent.

---

### Maximum Circular Subarray Sum (Maximum Sum Circular Subarray)

> [!example] Problem
> Find the maximum subarray sum in a circular array (the subarray may wrap around).

> [!info] Approach
> **Kadane's max + Kadane's min on total sum.**
> WHY: Two cases: (1) max subarray is non-wrapping — standard Kadane's; (2) it wraps around the ends. The wrap-around case is equivalent to the total sum minus the minimum subarray (the middle we exclude).
> WHAT: Run Kadane's twice: once for max subarray, once for min subarray. Answer = max(kadane_max, total - kadane_min).
> HOW: Edge case: if all elements are negative, `total - kadane_min` = 0 (the empty subarray), which is wrong. In this case, return `kadane_max`.

> [!note]- Python Solution
> ```python
> def max_subarray_circular(nums: list[int]) -> int:
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

### Sort Colors

> [!example] Problem
> Sort an array containing only 0s, 1s, and 2s in-place in one pass.

> [!info] Approach
> **Dutch National Flag — three-pointer partition.**
> WHY: We can't use comparison sort and achieve O(n) with O(1) space in one pass. Three distinct values → three-way partition.
> WHAT: Dutch National Flag algorithm: three pointers maintain invariant regions: `[0..lo)` are 0s, `[lo..mid)` are 1s, `(hi..n-1]` are 2s. `[mid..hi]` is unexamined.
> HOW: `lo=0, mid=0, hi=n-1`. While `mid <= hi`: if `nums[mid]==0`, swap with `lo`, advance both; if `nums[mid]==1`, advance `mid`; if `nums[mid]==2`, swap with `hi`, decrement `hi` — do NOT advance `mid` (swapped element from `hi` is unexamined).

> [!note]- Python Solution
> ```python
> def sort_colors(nums: list[int]) -> None:
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
> Given an array of n integers where values are in range [1, n], return all integers in [1, n] not appearing in the array.

> [!info] Approach
> **Sign-flip in-place visited marking.**
> WHY: We need to mark visited values without extra space. The array indices themselves serve as a hash table.
> WHAT: Use sign-flip as an in-place "visited" marker. Index `i` being negative means value `i+1` has been seen.
> HOW: For each value `x = abs(nums[i])`, negate `nums[x-1]`. After marking, collect all indices where value is still positive — those indices +1 are the missing values.

> [!note]- Python Solution
> ```python
> def find_disappeared_numbers(nums: list[int]) -> list[int]:
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

### Majority Element

> [!example] Problem
> Find the element appearing more than ⌊n/2⌋ times. Guaranteed to exist. Use O(1) space.

> [!info] Approach
> **Boyer-Moore voting — cancellation argument.**
> WHY: Hash map O(n) space, sorting O(n log n). Boyer-Moore pairs different elements and cancels them. The majority element (count > n/2) outlasts all others combined.
> WHAT: Maintain `candidate` and `count`. If count hits 0, pick current element as new candidate. Increment on same, decrement on different.
> HOW: This works because: imagine each "non-candidate" vote cancels one "candidate" vote. Since majority has > n/2 votes, it survives after all cancellations.

> [!note]- Python Solution
> ```python
> def majority_element(nums: list[int]) -> int:
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

### Majority Element II

> [!example] Problem
> Find all elements appearing more than ⌊n/3⌋ times. At most two such elements can exist.

> [!info] Approach
> **Boyer-Moore with two candidates.**
> WHY: There can be at most 2 elements with count > n/3. Boyer-Moore generalizes to track 2 candidates.
> WHAT: Two candidates, two counts. Decrement both when a third distinct value appears. Verify both candidates in a second pass.
> HOW: Maintain `c1, c2, cnt1, cnt2`. For each `x`: if `x == c1`, cnt1++; elif `x == c2`, cnt2++; elif `cnt1 == 0`, c1=x, cnt1=1; elif `cnt2 == 0`, c2=x, cnt2=1; else cnt1--, cnt2--. Second pass: count actual frequencies and filter `> n/3`.

> [!note]- Python Solution
> ```python
> def majority_element_ii(nums: list[int]) -> list[int]:
>     c1 = c2 = None
>     cnt1 = cnt2 = 0
>     for x in nums:
>         if x == c1:
>             cnt1 += 1
>         elif x == c2:
>             cnt2 += 1
>         elif cnt1 == 0:
>             c1, cnt1 = x, 1
>         elif cnt2 == 0:
>             c2, cnt2 = x, 1
>         else:
>             cnt1 -= 1
>             cnt2 -= 1
>     n = len(nums)
>     return [c for c in (c1, c2) if c is not None and nums.count(c) > n // 3]
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Hash map: O(n) time, O(n) space. Safe when you forget the voting trick.
> - The order of the if-elif chain matters — check equality first, then zero-count adoption, then decrement.

---

## Floyd's Cycle Detection (on Arrays)

### Find the Duplicate Number

> [!example] Problem
> Given an array of n+1 integers where each integer is in [1, n], find the one duplicate without modifying the array and using O(1) extra space.

> [!info] Approach
> **Floyd's cycle detection on implicit linked list.**
> WHY: Values in [1, n] can be treated as "next pointers" — `nums[i]` says "go to index nums[i]". Since multiple indices point to the same value, a cycle must exist. The duplicate is the cycle entry.
> WHAT: Floyd's cycle detection on the implicit linked list defined by `next(i) = nums[i]`. Start from index 0 (guaranteed outside cycle since all values ≥ 1).
> HOW: Phase 1 — slow = nums[slow], fast = nums[nums[fast]] until they meet (inside cycle). Phase 2 — reset slow = nums[0] (the start), advance both at speed 1; they meet at the cycle entry = duplicate.

> [!note]- Python Solution
> ```python
> def find_duplicate(nums: list[int]) -> int:
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

> [!info] Approach
> WHY: When you need to apply many range updates `[l, r] += val` and then query final values, the naive approach is O(n) per update — O(n × q) total for q updates. Difference array makes each update O(1) and reconstruction O(n), giving O(q + n) overall.
> WHAT: Build `diff[]` where `diff[i] = arr[i] - arr[i-1]`. To add `val` to range `[l, r]`: `diff[l] += val`, `diff[r+1] -= val`. Reconstruct prefix sum to get the final array.
> HOW: Initialize `diff = [0] * (n + 1)`. For each update `(l, r, val)`: `diff[l] += val; diff[r+1] -= val`. After all updates, compute prefix sum of `diff` to get the result array.

---

### Car Pooling

> [!example] Problem
> A vehicle can take `capacity` passengers. Given `trips[i] = [numPassengers, from, to]`, return true if it is possible to pick up and drop off all passengers without exceeding capacity at any stop.

> [!info] Approach
> WHY: Each trip is a range update — passengers board at `from` and alight at `to`. We need to check the running passenger count never exceeds `capacity` at any stop.
> WHAT: Difference array on stops (up to 1000 stops). `diff[from] += numPassengers`, `diff[to] -= numPassengers` (drop-off happens at `to`, so the open interval is `[from, to)`).
> HOW: Build `diff[0..1001]`. For each trip: `diff[from] += num; diff[to] -= num`. Reconstruct prefix sum; if any prefix sum > `capacity`, return False.

> [!note]- Python Solution
> ```python
> def carPooling(trips: list[list[int]], capacity: int) -> bool:
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
> There are `n` flights numbered 1 to n. `bookings[i] = [first, last, seats]` means `seats` seats are booked for every flight from `first` to `last` (inclusive). Return an array of length n where `answer[i]` is the total seats booked for flight `i+1`.

> [!info] Approach
> WHY: Each booking is a range update over flight indices. Naively applying each booking to every flight in range is O(n × b). Difference array reduces this to O(b + n).
> WHAT: Difference array over 1-indexed flights. For booking `[first, last, seats]`: `diff[first] += seats; diff[last+1] -= seats`. Prefix sum of diff gives total bookings per flight.
> HOW: Build `diff[0..n+1]`. For each booking: `diff[first] += seats; diff[last+1] -= seats`. Prefix sum of `diff[1..n]` is the answer.

> [!note]- Python Solution
> ```python
> def corpFlightBookings(bookings: list[list[int]], n: int) -> list[int]:
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
> Given a length-n array initialized to all zeros and a list of `updates[i] = [startIndex, endIndex, inc]`, return the modified array after applying all increments.

> [!info] Approach
> WHY: Classic difference array application — multiple range increments on an initially zero array.
> WHAT: For each update `[l, r, inc]`: `diff[l] += inc; diff[r+1] -= inc`. Prefix sum of `diff` is the final array.
> HOW: Build `diff[0..n]` (size n+1 to handle r+1 = n). Apply all updates. Prefix-sum `diff[0..n-1]` in-place.

> [!note]- Python Solution
> ```python
> def getModifiedArray(length: int, updates: list[list[int]]) -> list[int]:
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

### Best Time to Buy and Sell Stock

> [!example] Problem
> Given an array `prices` where `prices[i]` is the price of a stock on day `i`, find the maximum profit from a single buy-sell transaction. You cannot sell before buying.

> [!info] Approach
> WHY: Track the minimum price seen so far. Profit at day `i` = `prices[i] - min_so_far`. The best sell day for any buy day is always the global minimum to the left.
> WHAT: Single pass — maintain `min_price` and `max_profit`.
> HOW: `min_price = inf, max_profit = 0`. For each price: `min_price = min(min_price, price)`, `max_profit = max(max_profit, price - min_price)`.

> [!note]- Python Solution
> ```python
> def maxProfit(prices: list[int]) -> int:
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

### Move Zeroes

> [!example] Problem
> Move all 0s in the array to the end while maintaining the relative order of non-zero elements. Do it in-place.

> [!info] Approach
> WHY: We need to compact non-zero elements to the front, preserving order, without allocating extra space.
> WHAT: Two-pointer — `slow` tracks the next write position for non-zero elements; `fast` scans forward.
> HOW: `slow = 0`. For each `fast`: if `nums[fast] != 0`, set `nums[slow] = nums[fast]`, `slow++`. After the loop, zero out `nums[slow..n-1]`.

> [!note]- Python Solution
> ```python
> def moveZeroes(nums: list[int]) -> None:
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

### Two Sum (hash map variant)

> [!example] Problem
> Given an unsorted array and a target, return indices of two numbers that sum to target. Exactly one solution, each element used once.

> [!info] Approach
> **Hash map complement lookup.**
> WHY: Unsorted array → can't use two pointers (no sorted invariant). We need O(1) complement lookup.
> WHAT: Hash map storing `value → index`. Single pass: check if complement exists before recording current.
> HOW: For each `(i, x)`: compute `complement = target - x`. If in map, return `[map[complement], i]`. Else record `x → i`. Checking before recording ensures we don't use same index twice.

> [!note]- Python Solution
> ```python
> def two_sum(nums: list[int], target: int) -> list[int]:
>     seen: dict[int, int] = {}  # value -> index
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

### Jump Game II

> [!example] Problem
> Given an array where `nums[i]` is the max jump from index `i`, return the minimum number of jumps to reach the last index. Always reachable.

> [!info] Approach
> **Greedy BFS — level-by-level farthest reach.**
> WHY: BFS in levels — each "level" is the set of positions reachable in exactly `jumps` steps. The next level is everything reachable from this level. We want the level containing `n-1`.
> WHAT: Greedy BFS: track `current_end` (end of current BFS level) and `farthest` (max reachable from this level).
> HOW: Advance `i` from `0` to `n-2`. Update `farthest = max(farthest, i + nums[i])`. When `i == current_end`: a new jump is needed, `jumps++`, `current_end = farthest`. Stop when `current_end >= n-1`.

> [!note]- Python Solution
> ```python
> def jump(nums: list[int]) -> int:
>     jumps = current_end = farthest = 0
>     for i in range(len(nums) - 1):
>         farthest = max(farthest, i + nums[i])
>         if i == current_end:
>             jumps += 1
>             current_end = farthest
>     return jumps
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - DP `dp[i] = min jumps to reach i`: O(n²). Too slow.
> - BFS with queue: O(n) but O(n) space. The greedy version is equivalent and optimal.

---

### Spiral Matrix

> [!example] Problem
> Return all elements of an m×n matrix in spiral order.

> [!info] Approach
> **Boundary shrinking — four-direction cycling.**
> WHY: Spiral traversal has four directions cycling with shrinking boundaries.
> WHAT: Maintain four boundary pointers: `top, bottom, left, right`. Traverse right, down, left, up, then shrink boundaries inward.
> HOW: While `top <= bottom and left <= right`: traverse right along `top` row, `top++`; traverse down along `right` col, `right--`; if `top <= bottom`, traverse left along `bottom` row, `bottom--`; if `left <= right`, traverse up along `left` col, `left++`. The inner checks prevent double-counting for single row/col cases.

> [!note]- Python Solution
> ```python
> def spiral_order(matrix: list[list[int]]) -> list[int]:
>     top, bottom = 0, len(matrix) - 1
>     left, right = 0, len(matrix[0]) - 1
>     result: list[int] = []
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
> If a cell is zero, set its entire row and column to zero. Do it in-place.

> [!info] Approach
> **Use first row/col as markers — O(1) space.**
> WHY: Marking naively while iterating spreads zeros incorrectly. We must first record which rows/cols to zero, then apply.
> WHAT: O(1) space trick: use the first row and first column as markers. Handle them last.
> HOW: Record if row 0 or col 0 should be zeroed (check for existing zeros). For all other cells, if `matrix[i][j] == 0`, set `matrix[i][0] = 0` and `matrix[0][j] = 0`. Then zero out rows and cols using those markers. Finally handle row 0 and col 0 separately.

> [!note]- Python Solution
> ```python
> def set_zeroes(matrix: list[list[int]]) -> None:
>     m, n = len(matrix), len(matrix[0])
>     first_row_zero = any(matrix[0][j] == 0 for j in range(n))
>     first_col_zero = any(matrix[i][0] == 0 for i in range(m))
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

### Longest Consecutive Sequence

> [!example] Problem
> Find the length of the longest consecutive elements sequence. Must run in O(n).

> [!info] Approach
> **Hash set — start sequences only from minimums.**
> WHY: Sorting is O(n log n). We need O(n) — use a hash set for O(1) membership tests.
> WHAT: Only start counting a sequence from its minimum element (where `n-1` is not in the set). This ensures each element is processed at most once across all sequences.
> HOW: Insert all values into a set. For each `n`, if `n-1` not in set (start of sequence), count consecutive `n, n+1, n+2, ...` until gap. Update best length.

> [!note]- Python Solution
> ```python
> def longest_consecutive(nums: list[int]) -> int:
>     num_set = set(nums)
>     best = 0
>     for n in num_set:
>         if n - 1 not in num_set:  # start of a sequence
>             cur = n
>             length = 1
>             while cur + 1 in num_set:
>                 cur += 1
>                 length += 1
>             best = max(best, length)
>     return best
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Sort and scan: O(n log n) time. Simpler to reason about but violates O(n) requirement.
> - Union-Find: O(n α(n)) ≈ O(n). More complex; no advantage here.

---

### Rotate Array

> [!example] Problem
> Rotate array to the right by `k` steps in-place.

> [!info] Approach
> **Triple reversal trick.**
> WHY: Naively rotating element-by-element takes O(n×k). Reverse-trick achieves O(n) in-place.
> WHAT: Three reversal operations: reverse all, reverse first k, reverse last n-k. Composing these reversal operations achieves the rotation.
> HOW: Normalize `k = k % n`. Reverse `nums[0:n]`. Reverse `nums[0:k]`. Reverse `nums[k:n]`.

> [!note]- Python Solution
> ```python
> def rotate(nums: list[int], k: int) -> None:
>     n = len(nums)
>     k %= n
>     def reverse(l: int, r: int) -> None:
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

### Median of Two Sorted Arrays

> [!example] Problem
> Find the median of two sorted arrays in O(log(m+n)) time.

> [!info] Approach
> **Binary search on shorter array partition.**
> WHY: Merging takes O(m+n). We need O(log(m+n)) — binary search.
> WHAT: Binary search on the partition of the shorter array. Find split points such that `left_half` contains the (m+n+1)//2 smaller elements and `max(left_half) <= min(right_half)`.
> HOW: Binary search on shorter array (WLOG `m <= n`). Partition `nums1` at `i`, derive `nums2` partition `j = half - i`. Check: `nums1[i-1] <= nums2[j]` and `nums2[j-1] <= nums1[i]`. Adjust binary search accordingly. For odd total, median = `max(left sides)`. For even, median = `(max(left) + min(right)) / 2`.

> [!note]- Python Solution
> ```python
> def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
>     if len(nums1) > len(nums2):
>         nums1, nums2 = nums2, nums1
>     m, n = len(nums1), len(nums2)
>     half = (m + n + 1) // 2
>     lo, hi = 0, m
>     while lo <= hi:
>         i = (lo + hi) // 2
>         j = half - i
>         l1 = nums1[i - 1] if i > 0 else float('-inf')
>         r1 = nums1[i] if i < m else float('inf')
>         l2 = nums2[j - 1] if j > 0 else float('-inf')
>         r2 = nums2[j] if j < n else float('inf')
>         if l1 <= r2 and l2 <= r1:
>             if (m + n) % 2 == 1:
>                 return float(max(l1, l2))
>             return (max(l1, l2) + min(r1, r2)) / 2
>         elif l1 > r2:
>             hi = i - 1
>         else:
>             lo = i + 1
>     return 0.0
> ```

> [!success] Complexity
> Time O(log(min(m,n))), Space O(1).

> [!tip] Alternatives
> - Merge both arrays: O(m+n) time, O(m+n) space. Too slow.
> - k-th element selection: O(log(m+n)) with a different recursive approach. Same complexity, different reasoning.

---

## Range / Immutable Prefix Queries

### Range Sum Query — Immutable (LC 303)

> [!example] Problem
> Given an integer array, handle multiple queries each asking for the sum of elements between indices `left` and `right` (inclusive). Preprocess once, answer each query in O(1).

> [!info] Approach
> **Prefix sum array — O(1) per query.**
> - **WHY:** Recomputing a range sum from scratch is O(n) per query. A prefix sum table converts any range-sum query to O(1) subtraction.
> - **WHAT:** Build `prefix[i] = nums[0] + ... + nums[i-1]` (1-indexed offset). Then `sum(l, r) = prefix[r+1] - prefix[l]`.
> - **HOW:** Precompute `prefix[0..n]` where `prefix[0] = 0` and `prefix[i] = prefix[i-1] + nums[i-1]`. Each query: return `prefix[right+1] - prefix[left]`.

> [!note]- Python Solution
> ```python
> class NumArray:
>     def __init__(self, nums: list[int]) -> None:
>         self.prefix = [0] * (len(nums) + 1)
>         for i, x in enumerate(nums):
>             self.prefix[i + 1] = self.prefix[i] + x
>
>     def sumRange(self, left: int, right: int) -> int:
>         return self.prefix[right + 1] - self.prefix[left]
> ```

> [!success] Complexity
> Time O(n) build, O(1) per query. Space O(n).

> [!tip] Alternatives
> - Brute-force sum each query: O(n) per query — unacceptable for many queries.
> - Segment tree / BIT: O(n) build, O(log n) query — only needed when the array is mutable (LC 307).

---

### Range Sum Query 2D — Immutable (LC 304)

> [!example] Problem
> Given a 2D matrix, handle multiple queries each returning the sum of elements in the sub-rectangle defined by its upper-left `(row1, col1)` and lower-right `(row2, col2)` corners.

> [!info] Approach
> **2D prefix sum (inclusion-exclusion).**
> - **WHY:** Each query touching O(m×n) cells is too slow for many queries. 2D prefix sums extend the 1D idea: `prefix[i][j]` = sum of the rectangle from `(0,0)` to `(i-1, j-1)`.
> - **WHAT:** Build `prefix[i][j] = prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1] + matrix[i-1][j-1]`. Query: inclusion-exclusion of four corners.
> - **HOW:** `sum(r1,c1,r2,c2) = prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]`.

> [!note]- Python Solution
> ```python
> class NumMatrix:
>     def __init__(self, matrix: list[list[int]]) -> None:
>         m, n = len(matrix), len(matrix[0])
>         self.prefix = [[0] * (n + 1) for _ in range(m + 1)]
>         for i in range(1, m + 1):
>             for j in range(1, n + 1):
>                 self.prefix[i][j] = (matrix[i-1][j-1]
>                                      + self.prefix[i-1][j]
>                                      + self.prefix[i][j-1]
>                                      - self.prefix[i-1][j-1])
>
>     def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
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

### Contiguous Array (LC 525)

> [!example] Problem
> Find the maximum length of a contiguous subarray with equal numbers of 0s and 1s.

> [!info] Approach
> **Prefix sum with 0→−1 transform + first-occurrence hash map.**
> - **WHY:** Replace every 0 with −1. A balanced subarray now has sum 0. We need the longest subarray with sum 0 — classic prefix-sum problem.
> - **WHAT:** Track running sum. If `prefix[j] == prefix[i]`, then `sum(i+1..j) == 0`. Maximize `j - i` using first-occurrence map.
> - **HOW:** Seed `seen = {0: -1}`. For each index `i`, update `running`. If `running` in `seen`, candidate length = `i - seen[running]`. Else store `seen[running] = i`. Never overwrite (want earliest occurrence for max length).

> [!note]- Python Solution
> ```python
> def findMaxLength(nums: list[int]) -> int:
>     seen: dict[int, int] = {0: -1}
>     running = best = 0
>     for i, x in enumerate(nums):
>         running += 1 if x == 1 else -1
>         if running in seen:
>             best = max(best, i - seen[running])
>         else:
>             seen[running] = i
>     return best
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Brute force O(n²): count 0s and 1s for all subarrays. Too slow.
> - The 0→−1 substitution is the key insight; without it, prefix sums don't detect balance directly.

---

## Two-pass / Greedy

### Jump Game (LC 55)

> [!example] Problem
> Given an array where `nums[i]` is the max jump length from index `i`, determine if you can reach the last index.

> [!info] Approach
> **Greedy — track farthest reachable index.**
> - **WHY:** We don't need to know which path reaches the end, only whether any path does. A greedy max-reach scan is sufficient.
> - **WHAT:** Single pass maintaining `reach = max index reachable so far`. If current index `i > reach`, we're stuck.
> - **HOW:** `reach = 0`. For each `i` in `0..n-1`: if `i > reach`, return False. Update `reach = max(reach, i + nums[i])`. If `reach >= n-1` at any point, return True.

> [!note]- Python Solution
> ```python
> def canJump(nums: list[int]) -> bool:
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

### Candy (LC 135)

> [!example] Problem
> `n` children stand in a line. Each child has a rating. Each child must receive at least one candy. Children with a higher rating than their immediate neighbor must receive more candies. Return the minimum total candies.

> [!info] Approach
> **Two-pass greedy — left then right.**
> - **WHY:** The constraints are local (left neighbor, right neighbor). A single left-to-right pass satisfies left neighbors; a right-to-left pass fixes right neighbors without breaking left.
> - **WHAT:** Pass 1 (L→R): if `ratings[i] > ratings[i-1]`, `candy[i] = candy[i-1] + 1`, else `candy[i] = 1`. Pass 2 (R→L): if `ratings[i] > ratings[i+1]`, `candy[i] = max(candy[i], candy[i+1] + 1)`.
> - **HOW:** Initialize all to 1. Left pass enforces left-rising constraint. Right pass enforces right-rising constraint using `max` to preserve the larger requirement.

> [!note]- Python Solution
> ```python
> def candy(ratings: list[int]) -> int:
>     n = len(ratings)
>     candies = [1] * n
>     for i in range(1, n):
>         if ratings[i] > ratings[i - 1]:
>             candies[i] = candies[i - 1] + 1
>     for i in range(n - 2, -1, -1):
>         if ratings[i] > ratings[i + 1]:
>             candies[i] = max(candies[i], candies[i + 1] + 1)
>     return sum(candies)
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Single-pass with slope tracking (ascending/descending run lengths): O(n) time, O(1) space. More complex; handles "valley" ties.
> - Greedy priority queue: O(n log n). No benefit over two-pass.

---

### Gas Station (LC 134)

> [!example] Problem
> There are `n` gas stations in a circle. `gas[i]` is the gas available at station `i`; `cost[i]` is the cost to travel from `i` to `i+1`. Find the starting station index from which you can complete the full circle, or return −1 if impossible.

> [!info] Approach
> **Greedy — reset start on deficit.**
> - **WHY:** If total gas < total cost, no solution exists. Otherwise, a solution always exists. The greedy key: if we can't reach station `j` starting from `start`, then no station between `start` and `j` can be a valid start either (they would start with less surplus).
> - **WHAT:** Single pass tracking cumulative surplus. Reset start candidate whenever cumulative drops below zero.
> - **HOW:** `total = 0, tank = 0, start = 0`. For each `i`: `tank += gas[i] - cost[i]`, `total += gas[i] - cost[i]`. If `tank < 0`, set `start = i + 1`, reset `tank = 0`. Return `start` if `total >= 0` else `-1`.

> [!note]- Python Solution
> ```python
> def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
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

### Rotate Image (LC 48)

> [!example] Problem
> Rotate an n×n matrix 90 degrees clockwise in-place.

> [!info] Approach
> **Transpose then reverse each row.**
> - **WHY:** A 90° clockwise rotation of a matrix equals: transpose (swap `matrix[i][j]` with `matrix[j][i]`) followed by reversing each row. Both operations are O(n²) and in-place.
> - **WHAT:** Step 1: Transpose — swap upper-triangle elements across the main diagonal. Step 2: Reverse each row.
> - **HOW:** Transpose: `for i in range(n): for j in range(i+1, n): swap matrix[i][j] and matrix[j][i]`. Reverse: `for row in matrix: row.reverse()`.

> [!note]- Python Solution
> ```python
> def rotate(matrix: list[list[int]]) -> None:
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

### Search a 2D Matrix (LC 74)

> [!example] Problem
> Given an m×n matrix where each row is sorted and the first element of each row is greater than the last element of the previous row, search for a target value in O(log(m×n)).

> [!info] Approach
> **Binary search treating the matrix as a flat sorted array.**
> - **WHY:** The matrix is essentially a sorted 1D array laid out in rows. We can map a 1D index to 2D coordinates: `row = mid // n`, `col = mid % n`.
> - **WHAT:** Single binary search over the virtual index range `[0, m*n - 1]`.
> - **HOW:** `lo=0, hi=m*n-1`. At each `mid`: `val = matrix[mid//n][mid%n]`. Compare with target; adjust `lo`/`hi` accordingly.

> [!note]- Python Solution
> ```python
> def searchMatrix(matrix: list[list[int]], target: int) -> bool:
>     m, n = len(matrix), len(matrix[0])
>     lo, hi = 0, m * n - 1
>     while lo <= hi:
>         mid = (lo + hi) // 2
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
> Time O(log(m×n)), Space O(1).

> [!tip] Alternatives
> - Staircase search (top-right to bottom-left): O(m+n). Used for LC 240 (Search a 2D Matrix II) where rows and cols are independently sorted but the stronger "row-start > prev row-end" property doesn't hold.
> - Binary search per row: O(m log n). Suboptimal.

---

## Intervals

### Merge Intervals (LC 56)

> [!example] Problem
> Given a list of intervals, merge all overlapping intervals and return the result.

> [!info] Approach
> **Sort by start, linear merge scan.**
> - **WHY:** After sorting by start time, overlapping intervals are adjacent. We only need to check if the current interval overlaps with the last merged one.
> - **WHAT:** Sort, then greedily extend the last merged interval or append a new one.
> - **HOW:** Sort by `start`. Initialize `merged = [intervals[0]]`. For each subsequent interval: if `interval.start <= merged[-1].end`, merge by updating `merged[-1].end = max(merged[-1].end, interval.end)`. Else append.

> [!note]- Python Solution
> ```python
> def merge(intervals: list[list[int]]) -> list[list[int]]:
>     intervals.sort(key=lambda x: x[0])
>     merged: list[list[int]] = [intervals[0]]
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
> Given a list of non-overlapping intervals sorted by start, insert a new interval (merging as needed) and return the result.

> [!info] Approach
> **Three-phase linear scan: before, overlap, after.**
> - **WHY:** The existing intervals are already sorted and non-overlapping. We can scan in one pass: collect all intervals that end before the new one starts, merge all that overlap, collect the rest.
> - **WHAT:** Three phases: (1) add intervals entirely before new interval; (2) merge all overlapping intervals into new interval; (3) add remaining intervals.
> - **HOW:** Phase 1: while `intervals[i].end < new.start`, append. Phase 2: while `intervals[i].start <= new.end`, extend `new.start = min(new.start, ...)` and `new.end = max(new.end, ...)`. Append merged. Phase 3: append remaining.

> [!note]- Python Solution
> ```python
> def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
>     result: list[list[int]] = []
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

### Non-overlapping Intervals (LC 435)

> [!example] Problem
> Find the minimum number of intervals to remove so that the rest are non-overlapping.

> [!info] Approach
> **Greedy — sort by end, keep earliest-ending non-conflicting interval.**
> - **WHY:** Classic interval scheduling maximization (keep max non-overlapping intervals). Minimum removals = n − max kept. The greedy is: always keep the interval that ends earliest — it leaves the most room for future intervals.
> - **WHAT:** Sort by end time. Greedily keep an interval if it starts at or after the previous kept interval's end.
> - **HOW:** Sort by `end`. `prev_end = -inf, kept = 0`. For each interval: if `start >= prev_end`, keep it (`kept++`, update `prev_end = end`). Else skip (remove it). Answer = `n - kept`.

> [!note]- Python Solution
> ```python
> def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
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

### First Missing Positive (LC 41)

> [!example] Problem
> Given an unsorted integer array, return the smallest missing positive integer. Must run in O(n) time and O(1) extra space.

> [!info] Approach
> **Index-as-hash — cyclic placement of values in range [1, n].**
> - **WHY:** Any value outside [1, n] is irrelevant (answer is in [1, n+1]). We can treat the array itself as a hash table mapping value `v` to index `v-1`.
> - **WHAT:** Place each value `v` in [1, n] at index `v-1` by swapping. After rearrangement, the first index `i` where `nums[i] != i+1` gives answer `i+1`.
> - **HOW:** Swap phase: for each `i`, while `1 <= nums[i] <= n` and `nums[nums[i]-1] != nums[i]`, swap `nums[i]` with `nums[nums[i]-1]`. Scan phase: return first `i+1` where `nums[i] != i+1`, else return `n+1`.

> [!note]- Python Solution
> ```python
> def firstMissingPositive(nums: list[int]) -> int:
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
### First Missing Positive

> [!example] Problem
> Given an unsorted array, return the smallest missing positive integer.

> [!info] Approach
> - **WHY:** Values in `[1..n]` can be placed into their correct indices in-place. Anything outside that range can be ignored.
> - **WHAT:** Cyclic sort: keep swapping `nums[i]` into position `nums[i] - 1` while it is in range and not already placed.
> - **HOW:** After placement, scan left to right; the first index `i` where `nums[i] != i + 1` gives the answer.

> [!note]- Python Solution
> ```python
> def first_missing_positive(nums: list[int]) -> int:
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

### Subarray Sum Equals K (with negative numbers)

> [!example] Problem
> Given an integer array (may contain negatives) and an integer `k`, return the total number of subarrays whose elements sum to `k` (LC 560).

> [!info] Approach
> - **WHY:** Two-pointer/sliding-window breaks with negatives. Prefix sums let us reframe: subarray `[i+1..j]` sums to `k` iff `prefix[j] - prefix[i] == k`, i.e., `prefix[i] == prefix[j] - k`.
> - **WHAT:** Track prefix sum frequency in a hash map. For each new prefix sum, check how many prior prefix sums equal `current - k`.
> - **HOW:** Initialize map with `{0: 1}` (empty prefix). Walk the array accumulating `running_sum`; add `count_map[running_sum - k]` to the answer; then increment `count_map[running_sum]`.

> [!note]- Python Solution
> ```python
> def subarray_sum(nums: list[int], k: int) -> int:
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
> Given a binary array, find the maximum length subarray with equal numbers of 0s and 1s (LC 525).

> [!info] Approach
> - **WHY:** Replace 0 with -1. Now "equal 0s and 1s" becomes "subarray sum = 0", which is exactly the prefix sum problem.
> - **WHAT:** Track the first index at which each prefix sum occurs. When a prefix sum repeats, the subarray between the two occurrences has sum 0.
> - **HOW:** Initialize `{0: -1}`. For each index, compute prefix sum (treating 0 as -1). If seen before, update `max_len = max(max_len, i - first_seen[prefix])`. Otherwise, store `first_seen[prefix] = i`.

> [!note]- Python Solution
> ```python
> def find_max_length(nums: list[int]) -> int:
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

### Product of Array Except Self (no division)

> [!example] Problem
> Return an array `output` where `output[i]` is the product of all elements except `nums[i]`. Must run in O(n) without using division (LC 238).

> [!info] Approach
> - **WHY:** Division breaks on zeros. Without it, for each position we need the product of everything to the left and to the right.
> - **WHAT:** Two passes. First pass (left to right) builds the running left-product into the output array. Second pass (right to left) multiplies in the running right-product in-place.
> - **HOW:** `output[i]` after left pass = product of `nums[0..i-1]`. Then walk right to left with a `right_product` variable, multiply `output[i] *= right_product`, then `right_product *= nums[i]`.

> [!note]- Python Solution
> ```python
> def product_except_self(nums: list[int]) -> list[int]:
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
