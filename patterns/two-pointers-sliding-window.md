# Two Pointers & Sliding Window — Pattern Summary

Quick reference for when to use each pattern. Full content: [Arrays](../foundations/data-structures/array.md), [Strings](../foundations/algorithms/string.md).

---

## Two Pointers

### Opposite ends (sorted array)
- **When**: Pairs, triplets (fix one + two pointers), validity from both ends.
- **Examples**: Two Sum (if sorted), 3Sum, Container With Most Water, Valid Palindrome.
- **Template**: `left=0`, `right=n-1`; move left or right based on comparison; O(N) or O(N²) with fix.

### Same direction (fast & slow)
- **When**: Partition (move zeros), remove duplicates in-place, or "fast/slow" on linked list (see [Linked List](../foundations/data-structures/linked-list.md)).
- **Examples**: Move Zeroes, Remove Duplicates from Sorted Array, Linked List cycle/middle.

---

## Sliding Window

### Variable size
- **When**: "Longest/shortest contiguous subarray/substring" with constraint (sum, at most K distinct, etc.).
- **Template**: Expand `j`, then shrink `i` until valid; update answer. O(N).
- **Examples**: Longest Substring Without Repeating Characters, Minimum Window Substring, Longest Substring with At Most K Distinct Characters.

### Fixed size K
- **When**: "Max/min in every window of size K" or "all subarrays of size K".
- **Examples**: Max in sliding window → monotonic deque; or simple scan per window O(N*K) → O(N) with deque.
- **See**: [Queue](../foundations/data-structures/queue.md) for monotonic deque implementation.

---

## Pattern Recognition

| Clue | Pattern |
|------|--------|
| Sorted array + pair/triplet | Two pointers (opposite ends) |
| Contiguous + "longest/shortest" + condition | Sliding window (variable) |
| "Max/min in each window of size K" | Monotonic deque (or two pointers) |
| In-place partition / move | Two pointers (same direction) |
| "At most K" distinct/sum | Sliding window + map/count |

---

## Quick Revision

- **Two pointers opposite**: left/right; move based on value vs target; never miss in sorted array.
- **Sliding window**: [i,j); add j, then while invalid remove i; candidate = j-i+1.
- **Edge cases**: Empty; K=0; all same; negative numbers (window sum).
