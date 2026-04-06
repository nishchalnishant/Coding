# Arrays — SDE-3 Level

A fixed-size sequential collection of elements of the same type stored in contiguous memory. Mastery at SDE-3 means knowing when to use which technique, trade-offs, and production considerations.

---

## 1. Concept Overview

### Problem Space
- **Contiguous subarrays**: sum, product, max/min, condition (e.g., at most K distinct).
- **Pairs/triplets**: two sum, 3-sum, validity (e.g., triangle).
- **In-place operations**: move zeros, partition (Dutch national flag), reverse.
- **Range queries**: prefix sum, difference array for range updates.

### When to Use Which Technique
| Need | Technique | Typical complexity |
|------|------------|---------------------|
| Pairs in sorted array / validity from both ends | Two pointers (opposite ends) | O(N) |
| Contiguous segment with condition (sum, distinct count) | Sliding window | O(N) |
| Range sum queries (no updates) | Prefix sum | O(1) per query |
| Max contiguous sum | Kadane | O(N) |
| In-place partition / ordering | Two pointers or index manipulation | O(N) |

---

## 2. Core Algorithms

### Two Pointers (Opposite Ends)
- **Idea**: `left` at start, `right` at end; move based on comparison (e.g., `arr[left] + arr[right]` vs target).
- **Use when**: Sorted array, pairs, or validity from both ends.
- **Pseudocode** (two sum in sorted array):
```
sort(A)
left = 0, right = n - 1
while left < right:
  s = A[left] + A[right]
  if s == target: return [left, right]
  if s < target: left++
  else: right--
return not found
```
- **Complexity**: Time O(N) or O(N log N) if sort needed; Space O(1).

### Sliding Window (Variable or Fixed Size)
- **Idea**: Maintain `[i, j)` such that the window satisfies the invariant; advance `j` to extend, `i` to contract.
- **Use when**: "Longest/shortest contiguous subarray with …" or "subarray of size K with …".
- **Pseudocode** (longest substring with at most K distinct):
```
i = 0
for j in 0..n-1:
  add A[j] to window (e.g. freq[A[j]]++)
  while window invalid (e.g. distinct > K): remove A[i], i++
  candidate = j - i + 1; update best
return best
```
- **Complexity**: Time O(N); Space O(distinct elements).

### Prefix Sum
- **Idea**: `P[0]=0`, `P[i] = P[i-1] + A[i-1]`. Range sum `[l, r]` = `P[r+1] - P[l]`.
- **Complexity**: Preprocessing O(N); query O(1).

### Kadane's Algorithm (Max Contiguous Subarray Sum)
- **Idea**: `dp[i]` = max sum of contiguous subarray ending at `i` = `max(A[i], A[i] + dp[i-1])`. Use one variable in practice.
- **Pseudocode**:
```
best = -inf, cur = 0
for x in A:
  cur = max(x, cur + x)
  best = max(best, cur)
return best
```
- **Complexity**: Time O(N); Space O(1).

---

## 3. Advanced Variations

- **Dutch National Flag**: Three-way partition (e.g., 0s, 1s, 2s) with two boundaries; O(N), O(1).
- **Reservoir sampling**: One-pass random sample of size k from stream; equal probability per element.
- **Difference array**: For range updates (add `c` to `[l, r]`): `diff[l]+=c`, `diff[r+1]-=c`; prefix sum of `diff` gives final array.
- **Trapping Rain Water**: Two pointers (left max, right max) or monotonic stack; discuss trade-offs (stack generalizes to "next greater" thinking).

### Edge Cases
- Empty array; single element; all same; all negative (Kadane); integer overflow in sum/product; duplicates in two-sum (return first vs all).

---

## 4. Common Interview Problems

### Easy
- **Two Sum** — HashMap for complement or two pointers if sorted. Edge: duplicates, one solution vs all.
- **Best Time to Buy/Sell Stock** — Track min so far; max profit = current - min. O(N), O(1).
- **Move Zeroes** — Two pointers: write index and read index; swap or overwrite. O(N), O(1).
- **Missing Number** — XOR of index and value, or Gauss sum. Edge: 0..n vs 1..n.

### Medium
- **3Sum** — Fix one index; two pointers on the rest for two-sum. Skip duplicates. O(N²).
- **Product of Array Except Self** — Prefix product from left, then from right; or single pass with left product and right product variable.
- **Subarray Sum Equals K** — Prefix sum + HashMap (count of prefix sums = sum - K). Edge: negative numbers; prefix 0.
- **Merge Intervals** — Sort by start; merge if `curr.start <= prev.end`. O(N log N).

### Hard
- **Trapping Rain Water** — Two pointers: water at `i` = min(left_max, right_max) - height[i]. O(N), O(1).
- **Maximum Product Subarray** — Track max and min ending at i (negative flip). O(N), O(1).
- **Median of Two Sorted Arrays** — Binary search on smaller array's partition; balance left/right sizes and compare medians. O(log(min(n,m))).
- **Minimum Number of Operations to Make Array Continuous** — Sort + sliding window on unique; window size = n; minimize replacements. O(N log N).

---

## 5. Pattern Recognition

- **Two pointers (opposite)**: Sorted array, pairs, 3-sum, container with most water.
- **Two pointers (same direction)**: Sliding window, partition (move zeros), remove duplicates.
- **Prefix sum**: Subarray sum equals K, range sum queries.
- **Kadane**: Max (or min) contiguous sum/product; can be extended to circular (two passes or total - min subarray).
- **In-place**: Use same array with read/write indices; consider order of overwrite to avoid losing data.

---

## 6. Code Implementations

### Kadane (Max Subarray Sum)
```python
def max_subarray_sum(nums):
    if not nums:
        return 0
    best = cur = nums[0]
    for i in range(1, len(nums)):
        cur = max(nums[i], cur + nums[i])
        best = max(best, cur)
    return best
```

### Two Sum (Return One Pair; Hash Map)
```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        comp = target - x
        if comp in seen:
            return [seen[comp], i]
        seen[x] = i
    return []
```

### Sliding Window (Longest Substring with At Most K Distinct)
```python
def longest_substring_k_distinct(s, k):
    if k == 0:
        return 0
    i = 0
    freq = {}
    best = 0
    for j, c in enumerate(s):
        freq[c] = freq.get(c, 0) + 1
        while len(freq) > k:
            freq[s[i]] -= 1
            if freq[s[i]] == 0:
                del freq[s[i]]
            i += 1
        best = max(best, j - i + 1)
    return best
```

---

## 7. SDE-3 Level Thinking

- **Trade-offs**: Two pointers vs hash map for two-sum — hash map handles unsorted and gives O(N); two pointers need sort O(N log N) but O(1) space. For "all pairs" vs "one pair", design accordingly.
- **Scalability**: For very large arrays, consider streaming (Kadane, reservoir sampling); for range queries at scale, prefix sum is O(1) per query but no point updates (use segment tree if updates needed).
- **Memory**: In-place when possible (move zeros, Dutch flag); avoid copying if only reading.
- **Concurrency**: Parallel prefix sum (parallel scan); lock-free structures for high-throughput counters (advanced).

---

## 8. Interview Strategy

- **Identify**: "Contiguous" → prefix sum or sliding window or Kadane. "Pairs" / "triplets" → two pointers (if sorted) or hash. "In-place" → two pointers or overwrite indices.
- **Approach**: State brute force first (e.g., all subarrays O(N²)), then optimize with invariant (window, or prefix map).
- **Derive optimal**: Prove why the window never needs to "go back" (monotonicity) or why two pointers never miss (sorted order).
- **Common mistakes**: Off-by-one in window length; forgetting to handle empty or single element; integer overflow in sum/product; duplicate pairs in 3-sum.

---

## 9. Quick Revision

- **Formulas**: Range sum `[l,r]` = `P[r+1]-P[l]`. Kadane: `cur = max(x, cur+x)`.
- **Tricks**: Two pointers for sorted pairs; sliding window for "at most K" (shrink from left); difference array for range add.
- **Edge cases**: Empty, single element, all negative, duplicates, overflow.
- **Pattern tip**: "Subarray" + "sum" → prefix sum or sliding window; "subarray" + "max sum" → Kadane.

---

## See also

- [Hashing](hashing.md) — two sum, subarray sum = K  
- [Searching](../algorithms/searching.md) — binary search on answer  
- [two-pointers-sliding-window.md](../../patterns/two-pointers-sliding-window.md)
