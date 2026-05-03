# Arrays — SDE-3 Gold Standard

Fixed-size sequential collection in contiguous memory. Mastery at SDE-3 means choosing the right technique, proving it correct, knowing when sliding window fails (negatives), and handling range updates at scale.

---

## Theory & Mental Models

**What it is:** A contiguous block of memory where elements are stored sequentially and accessed in O(1) by index. Core invariant: `address(i) = base_address + i × element_size`.

**Why it exists:** Solves the problem of storing and accessing ordered data efficiently. Real-world analogy: numbered parking spots in a row — you jump directly to spot #42 without checking every spot before it.

**Memory layout:** All elements live in adjacent memory cells. This enables CPU cache prefetching — iterating an array is cache-friendly; pointer-chasing structures (linked lists) are not.

**Key invariants:**
- Fixed allocation size (in low-level sense); dynamic arrays (Python list) amortize reallocation at 2× growth.
- Index is always O(1): direct address arithmetic, no traversal.
- Insert/delete at arbitrary index requires shifting all subsequent elements — O(N).

**Complexity at a glance:**

| Operation | Time | Notes |
| :--- | :--- | :--- |
| Access by index | O(1) | Direct address arithmetic |
| Search (unsorted) | O(N) | Linear scan |
| Search (sorted) | O(log N) | Binary search |
| Insert at end | O(1) amortized | Dynamic array reallocation |
| Insert at arbitrary index | O(N) | Shifting required |
| Delete at arbitrary index | O(N) | Shifting required |

**When to reach for it:**
- Random access by index is needed (O(1) read/write by position).
- Cache locality matters — sequential processing of large data.
- Sliding window or two-pointer patterns (requires index arithmetic).
- Prefix sum precomputation for range queries.
- Input is already sorted and binary search applies.

**Common mistakes:**
- Off-by-one errors in slice bounds (`nums[l:r]` excludes `r`; `nums[l:r+1]` includes it).
- Forgetting to handle the empty array edge case before accessing `nums[0]`.
- Mutating the array while iterating over it (use a copy or two-pointer approach).
- Using sliding window when negatives exist and sum isn't monotone — switch to prefix sum + map.

---

## 1. Technique Selection Guide

| Constraint | Technique | Complexity |
| :--- | :--- | :--- |
| Pairs in sorted array / validity from both ends | Two pointers (opposite ends) | O(N) |
| Contiguous segment satisfying a condition | Sliding window | O(N) |
| Range sum queries (static data) | Prefix sum | O(1) per query after O(N) build |
| Many range-add updates, one final read | Difference array | O(1) update, O(N) reconstruct |
| Maximum contiguous subarray sum | Kadane's algorithm | O(N) |
| Partition into 3 groups in-place | Dutch National Flag | O(N) |
| Random sample of size K from stream | Reservoir sampling | O(N) |

---

## 2. Core Algorithms & Click Moments

### Two Pointers — Opposite Ends

> [!IMPORTANT]
> **The Click Moment**: "**Sorted** array + find a pair/triplet summing to target" — OR — "**maximize container** size" — OR — "**compare from both ends**". The invariant: if the current sum is too small, advance left; if too large, advance right. This only works on sorted or structurally symmetric arrays.

```python
def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []  # no pair found

def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue  # skip duplicate fixed element
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]: left += 1
                while left < right and nums[right] == nums[right-1]: right -= 1
                left += 1; right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return result
```

> [!CAUTION]
> **3Sum duplicate skipping has three sites**: skip duplicate `i` at the outer loop, and skip duplicate `left`/`right` after recording a valid triplet. Missing any one of the three causes duplicate results.

---

### Sliding Window — Variable or Fixed Size

> [!IMPORTANT]
> **The Click Moment**: "**Longest/shortest** contiguous subarray/substring satisfying a condition" — OR — "**at most K distinct** characters/elements" — OR — "**contains all characters** of T". The window expands right; when the condition breaks, it contracts from the left.

> [!CAUTION]
> **Sliding window requires monotonicity**: the window only shrinks when the condition breaks, and it only breaks once per expansion. This fails for "subarray sum equals K" when negatives exist — a negative element can restore validity after shrinking would normally stop. Use **prefix sum + hash map** for arbitrary integers.

```python
def length_of_longest_substring(s: str) -> int:
    char_idx: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in char_idx and char_idx[ch] >= left:
            left = char_idx[ch] + 1  # shrink window past the duplicate
        char_idx[ch] = right
        best = max(best, right - left + 1)
    return best

def min_window_substring(s: str, t: str) -> str:
    from collections import Counter
    need = Counter(t)
    have, required = 0, len(need)
    window: dict[str, int] = {}
    result = ""
    result_len = float('inf')
    left = 0
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            have += 1
        while have == required:
            if right - left + 1 < result_len:
                result_len = right - left + 1
                result = s[left:right+1]
            lch = s[left]
            window[lch] -= 1
            if lch in need and window[lch] < need[lch]:
                have -= 1
            left += 1
    return result
```

---

### Prefix Sum — Range Queries

> [!IMPORTANT]
> **The Click Moment**: "**Subarray sum equals K**" — OR — "**range sum** query" — OR — "how many subarrays have sum divisible by K". Once you build the prefix array, any range sum is O(1). Combined with a hash map, it enables counting subarrays with any target sum in O(N).

```python
def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    count = 0
    prefix = 0
    seen: dict[int, int] = {0: 1}  # prefix sum 0 seen once (empty subarray)
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count

def range_sum_query(nums: list[int]) -> callable:
    prefix = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        prefix[i+1] = prefix[i] + x
    def query(left: int, right: int) -> int:
        return prefix[right+1] - prefix[left]
    return query
```

---

### Kadane's Algorithm — Maximum Subarray Sum

> [!IMPORTANT]
> **The Click Moment**: "**Maximum contiguous subarray** sum" — OR — "**largest gain** from sequential elements" — OR — any problem reducible to "best window with no lower bound on size". Kadane's is the O(N) optimal — reject any D&C or DP solution that is O(N log N) or O(N²).

```python
def max_subarray(nums: list[int]) -> int:
    if not nums:
        raise ValueError("nums must be non-empty")
    cur = best = nums[0]  # handles all-negative case correctly
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

def max_subarray_with_indices(nums: list[int]) -> tuple[int, int, int]:
    cur = best = nums[0]
    start = end = best_start = 0
    for i, x in enumerate(nums[1:], 1):
        if x > cur + x:
            cur = x
            start = i
        else:
            cur += x
        if cur > best:
            best = cur
            best_start = start
            end = i
    return best, best_start, end
```

> [!CAUTION]
> Initializing `cur = best = 0` is wrong when all elements are negative — it returns 0 instead of the least-negative element. Always initialize to `nums[0]` and start the loop from index 1.

---

### Difference Array — Bulk Range Updates

> [!IMPORTANT]
> **The Click Moment**: "Apply **many range updates** (add value to all elements in [l, r])" — AND — "only need to **read final values**, not intermediate state". A difference array converts O(N) range updates to O(1) each, with a single O(N) prefix-sum pass to recover the final array.

```python
def apply_range_updates(n: int, updates: list[tuple[int, int, int]]) -> list[int]:
    diff = [0] * (n + 1)
    for left, right, val in updates:
        diff[left] += val
        if right + 1 <= n:
            diff[right + 1] -= val
    # Reconstruct via prefix sum
    result = []
    running = 0
    for i in range(n):
        running += diff[i]
        result.append(running)
    return result
```

---

### Dutch National Flag — 3-Way Partition

> [!IMPORTANT]
> **The Click Moment**: "Sort array of **three distinct values** (0, 1, 2)" — OR — "**partition** elements into three groups in one pass". Three pointers: `lo` (boundary of 0s), `mid` (current), `hi` (boundary of 2s). Elements between `mid` and `hi` are unexamined.

```python
def sort_colors(nums: list[int]) -> None:
    lo, mid, hi = 0, 0, len(nums) - 1
    while mid <= hi:
        if nums[mid] == 0:
            nums[lo], nums[mid] = nums[mid], nums[lo]
            lo += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[hi] = nums[hi], nums[mid]
            hi -= 1  # don't increment mid — swapped element from hi is unexamined
```

---

## 3. SDE-3 Deep Dives

### Scalability: Streaming and Out-of-Core Arrays

> [!TIP]
> When data doesn't fit in RAM:
> - **Top-K from stream**: min-heap of size K; O(N log K) time, O(K) space.
> - **Streaming median**: Two heaps (max-lo + min-hi); O(log N) per element.
> - **Count distinct in stream** (approximate): HyperLogLog — O(1) space with configurable error rate (±2% with ~1 KB memory). Used in Redis `PFCOUNT`, Google Analytics.
> - **Reservoir sampling**: Uniform random sample of K from a stream of unknown size N — each element i has probability K/i of being included.

```python
import random

def reservoir_sample(stream, k: int) -> list:
    reservoir = []
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = item
    return reservoir
```

### Scalability: Prefix Sums in Distributed Systems

> [!TIP]
> Prefix sums parallelize via **parallel prefix scan** (Blelloch scan): O(N/P) work per processor with O(log N) parallel depth. Used in GPU prefix sums (CUDA `thrust::inclusive_scan`), SIMD vectorized scan on CPU, and MapReduce-style distributed aggregation.

### Concurrency: Concurrent Array Access

> [!TIP]
> For concurrent reads with rare writes: use a **copy-on-write array** (Java's `CopyOnWriteArrayList`). Writes create a new copy; readers always see a consistent snapshot. Zero contention for reads — ideal for read-heavy access patterns like event listener lists.
>
> For high-write concurrent counters in an array: use `AtomicIntegerArray` (Java) or `numpy` arrays with explicit locking in Python — element-level CAS avoids locking the full array.

### Trade-offs: Choosing the Right Array Technique

| Problem Type | Wrong Approach | Right Approach | Why |
| :--- | :--- | :--- | :--- |
| Subarray sum = K (with negatives) | Sliding window | Prefix sum + map | Sliding window assumes monotone sums |
| K-th largest (streaming) | Full sort | Min-heap of K | O(N log K) vs O(N log N) |
| Range updates + point queries | Update each element | Difference array | O(1) vs O(N) per update |
| Many range sum queries | Linear scan each | Prefix sum | O(1) vs O(N) per query |
| Sorted array pair-sum | Nested loop | Two pointers | O(N) vs O(N²) |

---

## 4. Common Interview Problems

### Easy
- [Two Sum](../../google-sde2/PROBLEM_DETAILS.md#two-sum) — Hash map for complement; or two pointers if sorted.
- **Best Time to Buy/Sell Stock** — Track min so far; `profit = max(profit, price - min_price)`.
- **Move Zeros** — Two-pointer: maintain `write_idx` for non-zeros.

### Medium
- [3Sum](../../google-sde2/PROBLEM_DETAILS.md#3sum) — Sort + fix one + two pointers; skip duplicates at all three sites.
- [Subarray Sum Equals K](../../google-sde2/PROBLEM_DETAILS.md#subarray-sum-equals-k) — Prefix sum + count map; `seen[0] = 1`.
- **Longest Subarray with K Distinct** — Sliding window + frequency map.
- **Product of Array Except Self** — Prefix product from left × suffix product from right; O(1) extra space.
- **Container with Most Water** — Two pointers; advance the side with shorter height.
- **Next Permutation** — Find rightmost descent, swap with next larger, reverse suffix.
- **Jump Game** — Track `farthest` reachable; unreachable if `i > farthest`.

### Hard
- [Trapping Rain Water](../../google-sde2/PROBLEM_DETAILS.md#trapping-rain-water) — Two pointers `l_max, r_max`; advance side with smaller max.
- [Median of Two Sorted Arrays](../../google-sde2/PROBLEM_DETAILS.md#median-of-two-sorted-arrays) — Binary search on partition of shorter array.
- **Sliding Window Maximum** — Monotonic deque; O(N).
- **Count of Smaller Numbers After Self** — Merge sort augmentation or BIT.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **[Two Sum](../../google-sde2/PROBLEM_DETAILS.md#two-sum)** | Complement Map | "Pair summing to target" | Complement map `target - x` | Return **indices** vs values — clarify with interviewer. |
| **[3Sum](../../google-sde2/PROBLEM_DETAILS.md#3sum)** | "Triplets summing to 0, no duplicates" | Sort + fix i + two pointers | Skip duplicates at **three** sites: i, left, right — miss one, get duplicates. |
| **[Trapping Rain Water](../../google-sde2/PROBLEM_DETAILS.md#trapping-rain-water)** | "Water level bounded by shorter wall" | Two pointers; advance smaller max side | Level at position i = `min(l_max, r_max) - height[i]`; advance the smaller-max side. |
| **[Subarray Sum = K](../../google-sde2/PROBLEM_DETAILS.md#subarray-sum-equals-k)** | "Count subarrays with exact sum K" | Prefix sum + `seen[0]=1`; `count += seen[prefix-K]` | Sliding window **fails** with negatives — always use prefix map. |
| **Product Except Self** | "Product of all but self, no division" | Left-pass product × right-pass product | Division approach fails on zeros; two-pass achieves O(1) extra space. |
| **Container with Most Water** | "Max area between two lines" | Two pointers; advance shorter side | Area = `min(h[l], h[r]) * (r - l)`; advancing taller side never improves. |
| **Next Permutation** | "Lexicographic next arrangement" | Find rightmost descent; swap with next larger; reverse suffix | Rightmost **ascending** pair from the right = descent point; edge case: fully descending → reverse all. |
| **Jump Game II** | "Minimum jumps to reach end" | Greedy BFS levels; extend `current_end` | Track `farthest` in current level; when `i == current_end`, increment jumps. |
| **Sliding Window Maximum** | "Max in each window of size K" | Monotonic deque (decreasing); front = max of window | Remove from front if out of window `deque[0] <= i - k`; remove from back if smaller than current. |
| **Median of Two Arrays** | "Median without merging" | Binary search partition on shorter array | Partition so `len(left_half) == len(right_half)±1`; compare `max_left <= min_right`. |
| **Best Time to Buy and Sell Stock** [E] | "One transaction, maximize profit" | Single pass: track `min_price` so far; `max_profit = max(max_profit, price - min_price)` | Only one buy before one sell — not two-pointer; `min_price` resets naturally. |
| **Remove Duplicates from Sorted Array** [E] | "In-place, return new length" | Two pointers: `slow` marks write position; `slow` advances only on new value | Write `nums[slow] = nums[fast]`; return `slow + 1`; array is modified in-place. |
| **Find All Disappearing Numbers** [E] | "Numbers in [1,N] absent from array" | Negate `nums[abs(val)-1]`; collect indices still positive | O(1) space trick: use the array itself as a visited marker via sign flipping. |
| **Maximum Subarray** [M] | "Contiguous subarray with max sum" | Kadane: `cur = max(nums[i], cur + nums[i])`; update global max | Don't reset `cur` to 0 — that misses all-negative arrays; reset to `nums[i]`. |
| **Rotate Array** [M] | "Rotate right by K steps in-place" | Reverse all; reverse `[0:k]`; reverse `[k:]` | Normalize `k = k % n` first; forgetting this causes wrong answers for k > n. |
| **Find the Duplicate Number** [M] | "One duplicate in [1,N], O(1) space" | Floyd's cycle detection: treat array as linked list with `next = nums[i]` | Requires O(1) space — XOR or sum tricks fail when duplicates appear more than twice. |
| **Spiral Matrix** [M] | "Traverse matrix in spiral order" | Shrink boundaries: `top`, `bottom`, `left`, `right`; advance after each direction | After each row/col traversal, check `top <= bottom` and `left <= right` before next direction. |
| **Set Matrix Zeroes** [M] | "Zero out row and col for each zero cell" | First pass: record zeroed rows/cols; second pass: apply | O(1) space: use first row and col as markers; handle them last with a separate `first_row_zero` flag. |
| **Longest Consecutive Sequence** [H] | "Longest run, O(N) time" | Hash set; only start counting from `n` if `n-1` not in set | Starting only from sequence beginnings avoids O(N²) — each element processed once. |
| **Minimum Window Substring** [H] | "Smallest window containing all of T" | Sliding window; `have` tracks satisfied char counts | `have` tracks characters meeting their target count — not just counts; `have == need` means window is valid. |

---

## Quick Revision Triggers

- If the problem needs O(1) access by position → think Array because index = base + i×size.
- If the problem says "contiguous subarray satisfying a condition" → think Sliding Window (monotone) or Prefix Sum + Map (with negatives).
- If the problem says "range sum queries on static data" → think Prefix Sum; O(1) per query after O(N) build.
- If the problem says "many range-add updates, read final values" → think Difference Array; O(1) update, O(N) reconstruct.
- If the problem says "maximum subarray sum" → think Kadane's; initialize to `nums[0]`, not 0.
- If the problem says "sorted array + find pair/triplet with target sum" → think Two Pointers; advance the side that moves you toward the target.
- If the problem says "partition into 3 groups in one pass" → think Dutch National Flag; three-pointer dance.

## See also

- [Hashing](hashing.md) — two sum, subarray sum = K complement maps
- [Searching](../algorithms/searching.md) — binary search on answer for array problems
- [Stack](stack.md) — monotonic stack/deque for sliding window max and histogram
- [Patterns Master](../../../reference/patterns/patterns-master.md) — sliding window and two-pointer triggers
