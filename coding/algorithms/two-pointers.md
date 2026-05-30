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
> Sorted 1-indexed array. Find two numbers summing to target. Return their 1-indexed positions. Exactly one solution guaranteed.

> [!info] Approach
> - WHY: Array is sorted — sum is monotonically controlled by which endpoints we choose. Brute force O(n²) is unnecessary.
> - WHAT: Converging pointers `lo = 0, hi = n-1`. Sum < target → `lo += 1`; sum > target → `hi -= 1`; sum == target → return.
> - HOW: Each step either finds the answer or eliminates at least one impossible pair. Total: O(n) steps.

> [!note]- Python Solution
> ```python
> def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
>     lo, hi = 0, len(numbers) - 1
>     while lo < hi:
>         s = numbers[lo] + numbers[hi]
>         if s == target:
>             return [lo + 1, hi + 1]   # 1-indexed
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
> Find all unique triplets in an unsorted array that sum to zero.

> [!info] Approach
> - WHY: O(n³) brute force is too slow. Fix one element; remaining two-sum on sorted subarray reduces to O(n²) total.
> - WHAT: Sort array. For each anchor `i`, run converging two-pointer on `[i+1, n-1]`.
> - HOW: Skip duplicate anchors (`nums[i] == nums[i-1]`). On finding a triplet, skip duplicate inner pointers before advancing.

> [!note]- Python Solution
> ```python
> def three_sum(nums: list[int]) -> list[list[int]]:
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
> Find all unique quadruplets summing to target in an unsorted array.

> [!info] Approach
> - WHY: Fix two anchors, run two-pointer for the remaining pair. O(n³) total.
> - WHAT: Double outer loop (indices `i`, `j`), two-pointer inner loop `[j+1, n-1]`.
> - HOW: Deduplicate both outer anchors separately. Same skip-duplicate pattern as 3Sum on inner pointers.

> [!note]- Python Solution
> ```python
> def four_sum(nums: list[int], target: int) -> list[list[int]]:
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
> Array `height` where `height[i]` is a vertical bar. Pick two bars to form a container. Maximize water volume.

> [!info] Approach
> - WHY: Volume = `min(height[lo], height[hi]) * (hi - lo)`. Moving the taller bar inward can only decrease or keep width the same while min height can only stay equal or decrease — it can never improve the result. So always move the shorter bar.
> - WHAT: Start with widest container `lo=0, hi=n-1`. Move the shorter side inward.
> - HOW: `if height[lo] <= height[hi]: lo += 1` else `hi -= 1`. Record max at each step.

> [!note]- Python Solution
> ```python
> def max_area(height: list[int]) -> int:
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
> Array of bar heights. Compute total water trapped between bars after rain.

> [!info] Approach
> - WHY: Water at position `i` = `min(max_left, max_right) - height[i]`. Two pointers maintain running left/right maxima without two passes.
> - WHAT: Converging pointers. Whichever side has the smaller max — that side's water is determined by its own max (the other side can only be higher). Process that side.
> - HOW: `if left_max <= right_max: water += left_max - height[lo]; lo += 1` else process right side.

> [!note]- Python Solution
> ```python
> def trap(height: list[int]) -> int:
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
> Sorted array in-place. Remove duplicates, return the new length `k`. First `k` elements must contain unique values in order.

> [!info] Approach
> - WHY: Array is sorted — duplicates are contiguous. A write pointer marks the last accepted position.
> - WHAT: `write = 1` (index 0 always kept). For each `read >= 1`, copy to `write` only if `nums[read] != nums[read-1]`.
> - HOW: Each non-duplicate advances `write`. Duplicates are simply skipped.

> [!note]- Python Solution
> ```python
> def remove_duplicates(nums: list[int]) -> int:
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
> Remove all occurrences of `val` in-place. Return new length. Order of remaining elements doesn't matter.

> [!info] Approach
> - WHY: Need to compact array without extra space. Read scans forward; write only advances on non-val elements.
> - WHAT: `write = 0`. For each `read`, if `nums[read] != val` → copy to `nums[write]` and `write += 1`.
> - HOW: Alternatively, swap with the end when val is found — useful when val is rare (avoids shifting).

> [!note]- Python Solution
> ```python
> def remove_element(nums: list[int], val: int) -> int:
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
> Move all zeros to the end in-place while maintaining relative order of non-zero elements.

> [!info] Approach
> - WHY: Two-step: compact non-zeros forward (remove-element pattern), then fill tail with zeros.
> - WHAT: `write` pointer collects non-zeros. After loop, fill `nums[write:]` with zeros.
> - HOW: Avoids unnecessary writes for zeros — write pointer skips over zero positions and fills at the end.

> [!note]- Python Solution
> ```python
> def move_zeroes(nums: list[int]) -> None:
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
> Sorted array (may include negatives). Return sorted array of squares.

> [!info] Approach
> - WHY: Squares of negatives can be large. Largest squares are at the two ends. Fill result from the back.
> - WHAT: Converging pointers from both ends. Compare absolute values; place the larger square at `result[pos]` and advance that pointer.
> - HOW: `pos = n-1`. While `lo <= hi`: if `abs(nums[lo]) >= abs(nums[hi])` → `result[pos] = nums[lo]**2; lo += 1`; else process hi.

> [!note]- Python Solution
> ```python
> def sorted_squares(nums: list[int]) -> list[int]:
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
> Array with values 0, 1, 2. Sort in-place in a single pass. (Dutch National Flag problem.)

> [!info] Approach
> - WHY: Standard sort is O(n log n). Three distinct values allow O(n) single-pass partitioning.
> - WHAT: Three pointers: `lo` (next 0 position), `mid` (current element), `hi` (next 2 position from right).
> - HOW: Process `nums[mid]`: if 0 → swap with `lo`, advance both `lo` and `mid`; if 1 → advance `mid` only; if 2 → swap with `hi`, decrement `hi` but do NOT advance `mid` (swapped element is unseen).

> [!note]- Python Solution
> ```python
> def sort_colors(nums: list[int]) -> None:
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
> Determine if a linked list contains a cycle.

> [!info] Approach
> - WHY: No random access → can't track visited nodes without O(n) space. Floyd's: if a cycle exists, a faster pointer will lap the slower one.
> - WHAT: `slow` moves 1 step/iteration; `fast` moves 2. If they meet → cycle. If `fast` reaches None → no cycle.
> - HOW: Check `fast and fast.next` before each step to avoid null pointer dereference.

> [!note]- Python Solution
> ```python
> from typing import Optional
> 
> class ListNode:
>     def __init__(self, val=0, next=None):
>         self.val = val
>         self.next = next
> 
> def has_cycle(head: Optional[ListNode]) -> bool:
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
> Array of `n+1` integers in `[1, n]`. Exactly one duplicate. Find it without modifying the array. O(1) space.

> [!info] Approach
> - WHY: Treat the array as a function `f(i) = nums[i]` — following indices creates a linked list with a cycle (since one value appears twice, two indices map to the same "next"). Floyd's cycle detection finds the cycle entry = duplicate.
> - WHAT: Phase 1: find meeting point (inside cycle). Phase 2: reset one pointer to 0, step both by 1 until they meet — meeting point is the duplicate.
> - HOW: Phase 1 uses `slow = nums[slow]; fast = nums[nums[fast]]`. Phase 2: `slow = 0; while slow != fast: slow = nums[slow]; fast = nums[fast]`.

> [!note]- Python Solution
> ```python
> def find_duplicate(nums: list[int]) -> int:
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
> Return the middle node. If even length, return the second middle.

> [!info] Approach
> - WHY: Length unknown without full traversal. Fast/slow pointers: by the time `fast` reaches the end, `slow` is at the midpoint.
> - WHAT: `fast` moves 2 steps per iteration; `slow` moves 1. When `fast` or `fast.next` is None, `slow` is at the middle.
> - HOW: Condition `while fast and fast.next` — for even-length lists, `slow` stops at the second middle (upper-mid). This matches the problem requirement.

> [!note]- Python Solution
> ```python
> def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
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
> Remove the nth node from the end in a single pass. Return modified list head.

> [!info] Approach
> - WHY: To reach the nth-from-end, the fast pointer must be exactly n steps ahead of slow. When fast reaches the end, slow is at the node before the target.
> - WHAT: Advance `fast` n+1 steps (so slow stops at the node *before* the one to delete). Then move both until `fast` is None.
> - HOW: Use a dummy head to handle edge case of deleting the first node. `slow.next = slow.next.next` removes the target.

> [!note]- Python Solution
> ```python
> def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
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
> Given string s, return true if it can become a palindrome by removing at most one character.

> [!info] Approach
> - WHY: A standard two-pointer palindrome check fails at the first mismatch. But we have one deletion budget — try skipping s[l] OR s[r] and check if either remainder is a palindrome.
> - WHAT: Two pointers from both ends. On mismatch at (l, r): check is_palindrome(s, l+1, r) OR is_palindrome(s, l, r-1).
> - HOW: Helper function checks palindrome in a range. O(n) total — we branch at most once.

> [!note]- Python Solution
> ```python
> def valid_palindrome(s: str) -> bool:
>     def is_palindrome(s: str, l: int, r: int) -> bool:
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
> Find three integers in `nums` whose sum is closest to `target`. Return the sum. Exactly one answer guaranteed.

> [!info] Approach
> - WHY: Same scaffold as 3Sum — fix anchor, converging two-pointer on remainder. Track closest sum instead of exact match.
> - WHAT: Sort array. For each anchor `i`, run `lo = i+1, hi = n-1`. Update best if `|s - target| < |best - target|`. Move pointer based on whether sum is too small or too large.
> - HOW: If `s < target` → `lo += 1` (need larger sum); if `s > target` → `hi -= 1`; if equal → return immediately.

> [!note]- Python Solution
> ```python
> def three_sum_closest(nums: list[int], target: int) -> int:
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
> Four integer arrays A, B, C, D each of length n. Count tuples (i, j, k, l) such that `A[i] + B[j] + C[k] + D[l] == 0`.

> [!info] Approach
> - WHY: O(n⁴) brute force is infeasible. Split into two pairs: store all A+B sums in a hash map, then check if -(C+D) exists in it.
> - WHAT: Build `count` map of all `a + b` sums → frequency. For every `c + d`, add `count[-(c+d)]` to result.
> - HOW: Two nested loops each O(n²) rather than O(n⁴). This is a hash-map complement pattern, not classic two-pointer, but pairs with kSum problems.

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
> Rearrange `nums` so all elements less than `pivot` come first, then elements equal to `pivot`, then elements greater — maintaining relative order within each group. Return the rearranged array.

> [!info] Approach
> - WHY: Relative order must be preserved, so an in-place swap (DNF-style) would break ordering. A stable partition using three buckets is correct and O(n).
> - WHAT: Single pass: collect elements into `less`, `equal`, `greater` lists. Concatenate.
> - HOW: `less + equal + greater` preserves original relative order within each group.

> [!note]- Python Solution
> ```python
> def pivot_array(nums: list[int], pivot: int) -> list[int]:
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
> Given an unsorted array `nums` and integer `k`, return the minimum difference between the highest and lowest score of any `k` students.

> [!info] Approach
> - WHY: After sorting, the k elements with minimum spread must be contiguous (any non-contiguous selection can be improved by replacing the outlier with a neighbor). So the answer is the minimum of `nums[i+k-1] - nums[i]` over all valid windows.
> - WHAT: Sort then slide a fixed window of size k, record `nums[i + k - 1] - nums[i]`.
> - HOW: This is a two-pointer fixed window (lo = i, hi = i + k - 1). Single pass after sort.

> [!note]- Python Solution
> ```python
> def minimum_difference(nums: list[int], k: int) -> int:
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
> Given sorted array `nums` and `target`, count non-empty subsequences where `min + max <= target`. Return count mod 1e9+7.

> [!info] Approach
> - WHY: After sorting, for a fixed minimum at index `lo`, find the furthest `hi` where `nums[lo] + nums[hi] <= target`. Every subset of elements between `lo+1` and `hi` can pair with `nums[lo]` as min — there are `2^(hi-lo)` such subsequences.
> - WHAT: Converging two-pointer. Precompute powers of 2 mod MOD. For each `lo`, binary-search or slide `hi` left until valid; add `pow2[hi - lo]`.
> - HOW: `hi` never moves right (as `lo` increases, the valid range can only shrink), so two-pointer is O(n).

> [!note]- Python Solution
> ```python
> def num_subseq(nums: list[int], target: int) -> int:
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
> Each person has a weight. Each boat carries at most 2 people with weight sum ≤ `limit`. Find minimum number of boats needed.

> [!info] Approach
> - WHY: Greedily pair the heaviest person with the lightest. If they fit together, both board one boat; otherwise the heaviest goes alone. Sorting enables this pairing in O(n).
> - WHAT: Sort weights. `lo = 0, hi = n-1`. If `weights[lo] + weights[hi] <= limit` → both fit, `lo += 1`; always `hi -= 1` (heaviest always takes a boat). Boats += 1 per iteration.
> - HOW: The greedy is optimal: the heaviest person must go on some boat — it's never worse to pair them with the lightest available.

> [!note]- Python Solution
> ```python
> def num_rescue_boats(people: list[int], limit: int) -> int:
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
> Array of integers. In one operation pick two elements summing to `k` and remove them. Maximize number of operations.

> [!info] Approach
> - WHY: Each operation removes a pair summing to k. After sorting, the same converging two-pointer as Two Sum II finds all such pairs greedily.
> - WHAT: Sort. `lo = 0, hi = n-1`. If sum == k → count++, lo++, hi--; if sum < k → lo++; if sum > k → hi--.
> - HOW: Greedy pairing of smallest + largest exhausts all valid pairs optimally (each element can only be used once).

> [!note]- Python Solution
> ```python
> def max_operations(nums: list[int], k: int) -> int:
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
> Tokens with power values. Play a token face-up (costs `tokens[i]` power, gains 1 point) or face-down (costs 1 point, gains `tokens[i]` power). Start with `power` and 0 points. Maximize points.

> [!info] Approach
> - WHY: To maximize points, spend power on the cheapest token (face-up) and spend points on the most expensive token to regain power (face-down). Sorting enables greedy selection of cheapest/most-expensive with two pointers.
> - WHAT: Sort tokens. Greedily: if `power >= tokens[lo]` → play face-up (lo++, points++, power -= tokens[lo]); else if `points > 0` → play face-down (hi--, points--, power += tokens[hi]); else break.
> - HOW: Always track `best = max(best, points)` — we may want to stop before spending all points.

> [!note]- Python Solution
> ```python
> def bag_of_tokens_score(tokens: list[int], power: int) -> int:
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
> Reverse a character array in-place using O(1) extra memory.

> [!info] Approach
> - WHY: Swapping from both ends converges in n/2 steps — the simplest two-pointer pattern.
> - WHAT: `lo = 0, hi = n-1`. Swap `s[lo]` and `s[hi]`, advance both, until they meet.
> - HOW: Loop condition `lo < hi`; each iteration does one swap and two pointer moves.

> [!note]- Python Solution
> ```python
> def reverse_string(s: list[str]) -> None:
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
> Someone types `name` but keys can be long-pressed (a character typed once can appear multiple times). Return true if `typed` could result from typing `name` with some long presses.

> [!info] Approach
> - WHY: Both strings share a subsequence structure — `name` characters must appear in `typed` in order, with possible repetitions in `typed`. Two pointers on both strings handles this in a single pass.
> - WHAT: Pointer `i` on `name`, `j` on `typed`. Advance both when chars match. If `typed[j] == typed[j-1]`, it's a long press — advance `j` only. Otherwise mismatch → false.
> - HOW: After the loop, `i` must have consumed all of `name`.

> [!note]- Python Solution
> ```python
> def is_long_pressed_name(name: str, typed: str) -> bool:
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
> Reverse only the vowels in a string, leaving all other characters in place.

> [!info] Approach
> - **WHY:** The vowels to swap form a sparse subset, so moving two pointers inward and skipping non-vowels is optimal.
> - **WHAT:** Two pointers from the ends; advance each pointer until it points to a vowel, then swap.
> - **HOW:** Maintain a vowel set; while `left < right`, skip non-vowels on both sides and swap the vowel pair.

> [!note]- Python Solution
> ```python
> def reverse_vowels(s: str) -> str:
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
