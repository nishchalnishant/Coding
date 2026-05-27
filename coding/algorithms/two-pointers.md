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

## See Also

[[binary-search]] | [[sliding-window]] | [[array]] | [[linked-list]]
