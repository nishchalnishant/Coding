# Arrays — SDE-2+ Level

A fixed-size sequential collection of elements stored in contiguous memory. Mastery at SDE-3 means knowing when to use which technique, trade-offs, and production considerations.

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

## 2. Core Algorithms & Click Moments

### Two Pointers (Opposite Ends)
> [!IMPORTANT]
> **The Click Moment**: "Find a pair/triplet", "Sorted array", "Minimize/maximize container size", "Compare from ends".

- **Idea**: `left` at start, `right` at end; move based on comparison.
- **Pseudocode** (two sum in sorted array):
```python
while left < right:
    s = A[left] + A[right]
    if s == target: return [left, right]
    if s < target: left += 1
    else: right -= 1
```

### Sliding Window (Variable or Fixed Size)
> [!IMPORTANT]
> **The Click Moment**: "Longest/shortest contiguous subarray", "At most K distinct", "Contains all characters of T".

- **Idea**: Maintain `[i, j]` such that the window satisfies the invariant.
- **Pseudocode** (longest substring with at most K distinct):
```python
for j in range(n):
    freq[A[j]] += 1
    while len(freq) > K:
        freq[A[i]] -= 1
        if freq[A[i]] == 0: del freq[A[i]]
        i += 1
    best = max(best, j - i + 1)
```

### Prefix Sum
> [!IMPORTANT]
> **The Click Moment**: "Range sum queries", "Subarray sum equals K", "O(1) sum for any range".

- **Idea**: `P[i] = P[i-1] + A[i-1]`. Range sum `[l, r]` = `P[r+1] - P[l]`.

### Kadane's Algorithm
> [!IMPORTANT]
> **The Click Moment**: "Maximum contiguous subarray sum", "Largest gain", "Flip negative subarrays".

- **Idea**: `cur = max(x, cur + x)`.

---

## 3. Advanced Variations

- **Dutch National Flag**: Three-way partition (e.g., 0s, 1s, 2s).
- **Difference Array**: For range updates (add `c` to `[l, r]`): `diff[l]+=c`, `diff[r+1]-=c`.
- **Reservoir Sampling**: One-pass random sample of size k from stream.

> [!TIP]
> Use a **Difference Array** when you have many range updates but only need the final state once. It turns O(N) updates into O(1).

---

## 4. Common Interview Problems

### Easy
- [Two Sum](../google-sde2/PROBLEM_DETAILS.md#two-sum) — HashMap for complement or two pointers if sorted.
- **Best Time to Buy/Sell Stock** — Track min so far; max profit = current - min.

### Medium
- [3Sum](../google-sde2/PROBLEM_DETAILS.md#3sum) — Fix one index; two pointers on the rest. **Skip duplicates.**
- [Subarray Sum Equals K](../google-sde2/PROBLEM_DETAILS.md#subarray-sum-equals-k) — Prefix sum + HashMap. **Crucial for negatives.**

### Hard
- [Trapping Rain Water](../google-sde2/PROBLEM_DETAILS.md#trapping-rain-water) — Two pointers or monotonic stack.
- [Median of Two Sorted Arrays](../google-sde2/PROBLEM_DETAILS.md#median-of-two-sorted-arrays) — Binary search on smaller array's partition.

---

## 5. Pattern Recognition

- **"Contiguous"** → Prefix sum, Sliding window, or Kadane.
- **"Sorted"** → Binary search or Two pointers.
- **"Pairs/Triplets"** → Two pointers or Hash Map.
- **"Minimize the Maximum"** → Binary search on answer.

---

## 6. Interview Strategy

- **Derive Optimal**: Prove why the window never needs to "go back" (monotonicity).
- **Edge Cases**: Empty array, single element, all negative (Kadane), overflow.
- **Communication**: State brute force O(N²) then optimize with prefix map O(N).

---

## 7. Quick Revision

- **Formula**: Range sum `[l,r]` = `P[r+1]-P[l]`.
- **Kadane**: `cur = max(x, cur+x)`.
- **Tricks**: Skip duplicates in 3Sum: `if i > 0 and nums[i] == nums[i-1]: continue`.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Two Sum](../google-sde2/PROBLEM_DETAILS.md#two-sum)** | "Find target sum" | Complement map `target - x` | Return indices vs values. |
| **[3Sum](../google-sde2/PROBLEM_DETAILS.md#3sum)** | "Sum = 0" | Sort + Fix one + Two Pointers | **Skip duplicates** at `i`, `left`, and `right`. |
| **[Trapping Rain Water](../google-sde2/PROBLEM_DETAILS.md#trapping-rain-water)** | "Collect water" | Two pointers `l_max, r_max` | Move side with **smaller** max. |
| **Next Permutation** | "Lexicographic next" | Find pivot, swap, reverse | Edge case: last permutation. |

---

## See also

- [Hashing](hashing.md) — two sum, subarray sum = K  
- [Searching](../algorithms/searching.md) — binary search on answer  
- [Patterns Master](../../../reference/patterns/patterns-master.md)
- [two-pointers-sliding-window.md](../../patterns/two-pointers-sliding-window.md)
