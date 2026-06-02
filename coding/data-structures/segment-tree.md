---
tags: [coding, data-structures, segment-tree]
topic: Segment Tree & Binary Indexed Tree
difficulty: mixed
---

# Segment Tree & Binary Indexed Tree

Use a segment tree when you need fast range queries and fast updates on the same array, and the operation is associative (`sum`, `min`, `max`, `gcd`, etc.). For many prefix-sum-style problems, a BIT/Fenwick tree is simpler; for static queries, sparse table or prefix sums can be better.

---

## Interview Checklist

- Define the merge function first: `sum`, `min`, `max`, or another associative op.
- Choose the correct identity element for out-of-range nodes: `0`, `+inf`, `-inf`, etc.
- Keep the tree 0-indexed in code and remember to guard the empty-array case.
- For range updates, decide whether you need lazy propagation before writing code.

## Core Segment Tree

### Range Sum Query — Mutable (Point Update, Range Query)

> [!example] Problem
> Given an array of integers, support two operations: (1) update a single element, (2) query the sum over a range `[l, r]`. LeetCode 307.

> [!info] Approach
> - **WHY:** A flat array allows O(1) point update but O(n) range sum. A prefix sum array allows O(1) range sum but O(n) update. A segment tree achieves O(log n) for both by partitioning the array into a binary tree of intervals.
> - **WHAT:** Build a binary tree where each node stores the sum of its interval. Leaves store individual elements. Internal nodes aggregate child sums. Tree height = O(log n); 4n nodes suffice.
> - **HOW:**
>   - Build: recursively split `[l, r]` into `[l, mid]` and `[mid+1, r]`; leaf stores `nums[l]`; internal node stores left.sum + right.sum. O(n).
>   - Update: traverse root to leaf updating sums on the path back up. O(log n).
>   - Query: decompose `[ql, qr]` into O(log n) nodes that collectively cover the range without overlap. O(log n).
> - **EDGE CASES:** Empty arrays, single-element arrays, and query/update boundaries should be handled explicitly.

> [!note]- Python Solution
> ```python
> class SegmentTree:
>     def __init__(self, nums: list[int]) -> None:
>         self.n = len(nums)
>         self.tree = [0] * (4 * self.n)
>         if self.n:
>             self._build(nums, 0, 0, self.n - 1)
> 
>     def _build(self, nums: list[int], node: int, start: int, end: int) -> None:
>         if start == end:
>             self.tree[node] = nums[start]
>             return
>         mid = (start + end) // 2
>         self._build(nums, 2 * node + 1, start, mid)
>         self._build(nums, 2 * node + 2, mid + 1, end)
>         self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
> 
>     def update(self, idx: int, val: int) -> None:
>         if not self.n:
>             return
>         self._update(0, 0, self.n - 1, idx, val)
> 
>     def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
>         if start == end:
>             self.tree[node] = val
>             return
>         mid = (start + end) // 2
>         if idx <= mid:
>             self._update(2 * node + 1, start, mid, idx, val)
>         else:
>             self._update(2 * node + 2, mid + 1, end, idx, val)
>         self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
> 
>     def query(self, ql: int, qr: int) -> int:
>         if not self.n:
>             return 0
>         return self._query(0, 0, self.n - 1, ql, qr)
> 
>     def _query(self, node: int, start: int, end: int, ql: int, qr: int) -> int:
>         if qr < start or end < ql:
>             return 0           # out of range: identity for sum
>         if ql <= start and end <= qr:
>             return self.tree[node]   # fully covered
>         mid = (start + end) // 2
>         return (self._query(2 * node + 1, start, mid, ql, qr) +
>                 self._query(2 * node + 2, mid + 1, end, ql, qr))
> ```

> [!success] Complexity
> Build O(n) | Update O(log n) | Query O(log n) | Space O(n).

> [!tip] Alternatives
> Binary Indexed Tree (BIT/Fenwick): simpler code for prefix sums, same O(log n) but restricted to invertible operations (sum/XOR, not min/max). Sqrt decomposition: O(√n) per operation, O(1) to implement.

---

## Common Interview Patterns

### Point Update + Range Query

- Use a segment tree when the array changes often and queries are over arbitrary ranges.
- Typical examples: range sum, range min/max, range gcd, and frequency counts.

### Range Update + Range Query

- Add lazy propagation when updates affect a whole interval and you still need fast queries.
- Typical examples: range add + range min/max/sum, interval coloring, and delayed assignment.

### Static Query Only

- Prefer prefix sums, sparse table, or monotonic deque when there are no updates.
- This is often a better interview answer if the problem is static and the query type is specialized.

### Range Minimum Query with Lazy Propagation

> [!example] Problem
> Given an array, support: (1) range update (add a value to all elements in `[l, r]`), (2) range minimum query. (General lazy propagation template.)

> [!info] Approach
> - **WHY:** Without lazy propagation, a range update touches O(n) nodes in the worst case. Lazy propagation defers updates: store a "pending" delta at each node and push it down only when a child is accessed.
> - **WHAT:** Each node stores `min_val` (minimum in its interval) and `lazy` (pending additive update not yet propagated to children). The invariant: `node.min_val` reflects all lazy values above it (already applied), but its children may be stale.
> - **HOW:**
>   - Range update `[ul, ur]` with delta: if node's interval is fully covered, add delta to `node.min_val` and `node.lazy`; otherwise `push_down` first, recurse on children, pull up.
>   - Push down: apply `parent.lazy` to both children (add to their `min_val` and `lazy`), then clear parent's `lazy`.
>   - Range min query: standard decomposition, same as sum query but return min of left/right.
> - **EDGE CASES:** Never push past a leaf; handle the empty-array case up front.

> [!note]- Python Solution
> ```python
> class LazySegTree:
>     def __init__(self, nums: list[int]) -> None:
>         self.n = len(nums)
>         self.tree = [float('inf')] * (4 * self.n)
>         self.lazy = [0] * (4 * self.n)
>         if self.n:
>             self._build(nums, 0, 0, self.n - 1)
> 
>     def _build(self, nums: list[int], node: int, start: int, end: int) -> None:
>         if start == end:
>             self.tree[node] = nums[start]
>             return
>         mid = (start + end) // 2
>         self._build(nums, 2*node+1, start, mid)
>         self._build(nums, 2*node+2, mid+1, end)
>         self.tree[node] = min(self.tree[2*node+1], self.tree[2*node+2])
> 
>     def _push_down(self, node: int, start: int, end: int) -> None:
>         if self.lazy[node] and start != end:
>             for child in (2*node+1, 2*node+2):
>                 self.tree[child] += self.lazy[node]
>                 self.lazy[child] += self.lazy[node]
>             self.lazy[node] = 0
> 
>     def range_add(self, ql: int, qr: int, delta: int) -> None:
>         if not self.n:
>             return
>         self._update(0, 0, self.n-1, ql, qr, delta)
> 
>     def _update(self, node: int, start: int, end: int, ql: int, qr: int, delta: int) -> None:
>         if qr < start or end < ql:
>             return
>         if ql <= start and end <= qr:
>             self.tree[node] += delta
>             self.lazy[node] += delta
>             return
>         self._push_down(node, start, end)
>         mid = (start + end) // 2
>         self._update(2*node+1, start, mid, ql, qr, delta)
>         self._update(2*node+2, mid+1, end, ql, qr, delta)
>         self.tree[node] = min(self.tree[2*node+1], self.tree[2*node+2])
> 
>     def range_min(self, ql: int, qr: int) -> int | float:
>         if not self.n:
>             return float('inf')
>         return self._query(0, 0, self.n-1, ql, qr)
> 
>     def _query(self, node: int, start: int, end: int, ql: int, qr: int) -> int | float:
>         if qr < start or end < ql:
>             return float('inf')
>         if ql <= start and end <= qr:
>             return self.tree[node]
>         self._push_down(node, start, end)
>         mid = (start + end) // 2
>         return min(self._query(2*node+1, start, mid, ql, qr),
>                    self._query(2*node+2, mid+1, end, ql, qr))
> ```

> [!success] Complexity
> Build O(n) | Range update O(log n) | Range min O(log n) | Space O(n).

> [!tip] Alternatives
> Sparse table: O(n log n) build, O(1) query for static RMQ (no updates). BIT does not support min queries (non-invertible). Sqrt decomposition: O(√n) per operation.

---

### Range Maximum Query

> [!example] Problem
> Given an array, support point updates and range maximum queries.

> [!info] Approach
> - **WHY:** Same motivation as range sum but with max aggregation (non-invertible, so BIT doesn't work directly).
> - **WHAT:** Segment tree where internal nodes store the maximum of their interval. Point update propagates new max up the path.
> - **HOW:** Identity for max is `-inf` (out-of-range nodes return this). Merge: `max(left_child, right_child)`.
> - **EDGE CASES:** Empty arrays should return `-inf` for queries or be guarded explicitly, depending on the API.

> [!note]- Python Solution
> ```python
> class MaxSegTree:
>     def __init__(self, nums: list[int]) -> None:
>         self.n = len(nums)
>         self.tree = [-float('inf')] * (4 * self.n)
>         if self.n:
>             self._build(nums, 0, 0, self.n - 1)
> 
>     def _build(self, nums: list[int], node: int, start: int, end: int) -> None:
>         if start == end:
>             self.tree[node] = nums[start]
>             return
>         mid = (start + end) // 2
>         self._build(nums, 2*node+1, start, mid)
>         self._build(nums, 2*node+2, mid+1, end)
>         self.tree[node] = max(self.tree[2*node+1], self.tree[2*node+2])
> 
>     def update(self, idx: int, val: int) -> None:
>         if not self.n:
>             return
>         self._update(0, 0, self.n-1, idx, val)
> 
>     def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
>         if start == end:
>             self.tree[node] = val
>             return
>         mid = (start + end) // 2
>         if idx <= mid:
>             self._update(2*node+1, start, mid, idx, val)
>         else:
>             self._update(2*node+2, mid+1, end, idx, val)
>         self.tree[node] = max(self.tree[2*node+1], self.tree[2*node+2])
> 
>     def query(self, ql: int, qr: int) -> int | float:
>         if not self.n:
>             return -float('inf')
>         return self._query(0, 0, self.n-1, ql, qr)
> 
>     def _query(self, node: int, start: int, end: int, ql: int, qr: int) -> int | float:
>         if qr < start or end < ql:
>             return -float('inf')
>         if ql <= start and end <= qr:
>             return self.tree[node]
>         mid = (start + end) // 2
>         return max(self._query(2*node+1, start, mid, ql, qr),
>                    self._query(2*node+2, mid+1, end, ql, qr))
> ```

> [!success] Complexity
> Build O(n) | Update O(log n) | Query O(log n) | Space O(n).

> [!tip] Alternatives
> Sparse table: O(1) query for static max with O(n log n) build. Monotonic deque: O(n) sliding window max for fixed-size windows only.

---

## Segment Tree Applications

### Count of Range Sum

> [!example] Problem
> Given array `nums`, count the number of range sums `S(i, j)` such that `lower <= S(i, j) <= upper`. LeetCode 327.

> [!info] Approach
> - **WHY:** Brute force O(n²) prefix sum checks are too slow. We need to count pairs efficiently.
> - **WHAT:** Let `prefix[i] = sum(nums[0..i-1])`. `S(i,j) = prefix[j] - prefix[i]`. We need to count pairs `(i, j)` with `i < j` and `lower <= prefix[j] - prefix[i] <= upper` → `prefix[j] - upper <= prefix[i] <= prefix[j] - lower`.
> - **HOW:** Merge sort approach — during merge, for each right-half element `prefix[j]`, count how many left-half elements fall in `[prefix[j] - upper, prefix[j] - lower]` using two pointers. O(n log n).
> - **ALTERNATIVE:** Coordinate compression + BIT works too, especially if you already have a Fenwick template in an interview.

> [!note]- Python Solution
> ```python
> def count_range_sum(nums: list[int], lower: int, upper: int) -> int:
>     prefix = [0] * (len(nums) + 1)
>     for i, x in enumerate(nums):
>         prefix[i + 1] = prefix[i] + x
>     count = 0
>     temp = [0] * len(prefix)
> 
>     def merge_sort(lo: int, hi: int) -> None:
>         nonlocal count
>         if hi - lo <= 1:
>             return
>         mid = (lo + hi) // 2
>         merge_sort(lo, mid)
>         merge_sort(mid, hi)
>         # Count pairs: left in [lo,mid), right in [mid,hi)
>         j = k = mid
>         for i in range(lo, mid):
>             while k < hi and prefix[k] - prefix[i] < lower:
>                 k += 1
>             while j < hi and prefix[j] - prefix[i] <= upper:
>                 j += 1
>             count += j - k
>         # Standard merge, in-place over prefix[lo:hi]
>         left, right, idx = lo, mid, lo
>         while left < mid and right < hi:
>             if prefix[left] <= prefix[right]:
>                 temp[idx] = prefix[left]
>                 left += 1
>             else:
>                 temp[idx] = prefix[right]
>                 right += 1
>             idx += 1
>         while left < mid:
>             temp[idx] = prefix[left]
>             left += 1
>             idx += 1
>         while right < hi:
>             temp[idx] = prefix[right]
>             right += 1
>             idx += 1
>         prefix[lo:hi] = temp[lo:hi]
> 
>     merge_sort(0, len(prefix))
>     return count
> ```

> [!success] Complexity
> Time O(n log n) | Space O(n).

> [!tip] Alternatives
> Coordinate-compressed segment tree or BIT: insert prefix sums left-to-right; for each new `prefix[j]`, query count of previously inserted values in `[prefix[j]-upper, prefix[j]-lower]`. O(n log n) with coordinate compression. Merge sort approach is simpler in Python.

---

### Number of Longest Increasing Subsequence

> [!example] Problem
> Find the number of longest increasing subsequences in `nums`. LeetCode 673.

> [!info] Approach
> - **WHY:** Standard LIS DP gives length only. We need both `length[i]` and `count[i]` for each index, updated optimally.
> - **WHAT:** `length[i]` = length of LIS ending at i. `count[i]` = number of such LIS. For each i, scan all j < i with `nums[j] < nums[i]`: if `length[j] + 1 > length[i]`, update length and reset count; if equal, add to count.
> - **HOW:** O(n²) DP is simple. Segment tree on values (coordinate compressed) can reduce to O(n log n): tree node stores `(max_length, total_count)` for values processed so far; query `[0, nums[i]-1]` for best, then update at `nums[i]`.

> [!note]- Python Solution
> ```python
> def find_number_of_lis(nums: list[int]) -> int:
>     if not nums:
>         return 0
>     n = len(nums)
>     length = [1] * n   # LIS length ending at i
>     count = [1] * n    # number of LIS ending at i
> 
>     for i in range(1, n):
>         for j in range(i):
>             if nums[j] < nums[i]:
>                 if length[j] + 1 > length[i]:
>                     length[i] = length[j] + 1
>                     count[i] = count[j]
>                 elif length[j] + 1 == length[i]:
>                     count[i] += count[j]
> 
>     max_len = max(length)
>     return sum(c for l, c in zip(length, count) if l == max_len)
> ```

> [!success] Complexity
> Time O(n²) | Space O(n). O(n log n) possible with segment tree on coordinate-compressed values.

> [!tip] Alternatives
> Segment tree approach: coordinate compress `nums`, build tree storing `(max_len, cnt)` pairs; combine as: if new_len > stored_len, replace; if equal, add counts. O(n log n) total.

---

### Queue Reconstruction by Height

> [!example] Problem
> People stand in a queue; each person `[h, k]` has height h and k taller-or-equal people in front. Reconstruct the queue. LeetCode 406.

> [!info] Approach
> - **WHY:** We need to place people such that their k-constraint is satisfied. Greedy insertion works by processing tallest first.
> - **WHAT:** Sort by height descending (ties broken by k ascending). Insert each person at position k in the result list. Since taller people are already placed and shorter people don't affect the count of taller people in front, inserting at index k is always valid.
> - **HOW:** This is a greedy O(n²) insertion. BIT/segment tree can optimize to O(n log n) by tracking the k-th empty slot.

> [!note]- Python Solution
> ```python
> def reconstruct_queue(people: list[list[int]]) -> list[list[int]]:
>     # Greedy: sort tallest first, ties by k ascending
>     people.sort(key=lambda x: (-x[0], x[1]))
>     result: list[list[int]] = []
>     for person in people:
>         result.insert(person[1], person)   # insert at index k — O(n) per insert
>     return result
> ```

> [!success] Complexity
> Greedy: O(n²) for list insertions, O(n log n) sort | Space O(n). BIT variant: O(n log n).

> [!tip] Alternatives
> **O(n log n) BIT approach:** After sorting, use a BIT to find the k-th empty position (1-indexed count of remaining empty slots). Binary search on the BIT prefix sum to find the index. O(n log² n) with binary search, O(n log n) with walking the BIT tree.

> Direct simulation with a linked list for O(n log n) insertions (linked list insert at position k after finding k-th node). SortedList (Python `sortedcontainers`): O(n log n) total.

---

## Binary Indexed Tree (Fenwick Tree)

### Range Sum Query — Mutable (BIT Implementation)

> [!example] Problem
> Point update, prefix sum query — the canonical BIT problem. LeetCode 307.

> [!info] Approach
> - **WHY:** BIT is a simpler, more cache-friendly alternative to the segment tree for prefix sum queries. Code is ~10 lines vs ~40 lines.
> - **WHAT:** BIT stores partial sums in an array where `tree[i]` covers the range `[i - lowbit(i) + 1, i]` where `lowbit(i) = i & (-i)`.
> - **HOW:**
>   - Query prefix sum `[1, i]`: sum up `tree[i], tree[i - lowbit(i)], ...` until index 0. Each step removes the lowest set bit → O(log n) steps.
>   - Update index i by delta: add delta to `tree[i], tree[i + lowbit(i)], ...` until index > n. Each step adds the lowest set bit → O(log n) steps.
>   - Range sum `[l, r]` = `prefix(r) - prefix(l-1)`.

> [!note]- Python Solution
> ```python
> class BIT:
>     def __init__(self, n: int) -> None:
>         self.n = n
>         self.tree = [0] * (n + 1)   # 1-indexed
> 
>     def update(self, i: int, delta: int) -> None:
>         while i <= self.n:
>             self.tree[i] += delta
>             i += i & (-i)   # add lowest set bit
> 
>     def prefix_sum(self, i: int) -> int:
>         s = 0
>         while i > 0:
>             s += self.tree[i]
>             i -= i & (-i)   # remove lowest set bit
>         return s
> 
>     def range_sum(self, l: int, r: int) -> int:
>         return self.prefix_sum(r) - self.prefix_sum(l - 1)
> 
> 
> class NumArray:
>     def __init__(self, nums: list[int]) -> None:
>         self.bit = BIT(len(nums))
>         self.nums = nums[:]
>         for i, v in enumerate(nums):
>             self.bit.update(i + 1, v)   # 1-indexed
> 
>     def update(self, index: int, val: int) -> None:
>         self.bit.update(index + 1, val - self.nums[index])
>         self.nums[index] = val
> 
>     def sum_range(self, left: int, right: int) -> int:
>         return self.bit.range_sum(left + 1, right + 1)
> ```

> [!success] Complexity
> Build O(n log n) | Update O(log n) | Query O(log n) | Space O(n).

> [!tip] Alternatives
> Segment tree: O(log n) same, but supports non-invertible operations (min/max). BIT preferred for sum/XOR due to simpler code and better cache performance.

---

### Count of Smaller Numbers After Self

> [!example] Problem
> For each element `nums[i]`, count how many elements to its right are strictly smaller. LeetCode 315.

> [!info] Approach
> - **WHY:** Brute force O(n²) compares every pair. We need a data structure that answers "how many inserted values are less than x" in O(log n).
> - **WHAT:** Process from right to left. Coordinate compress `nums` to range `[1, n]`. For each element, query BIT for prefix sum `[1, rank-1]` (count of smaller values already seen = values to the right), then update BIT at `rank`.
> - **HOW:** Coordinate compression maps values to 1..n. BIT query at `rank-1` = count of right-side elements smaller than current. Then insert current into BIT.

> [!note]- Python Solution
> ```python
> def count_smaller(nums: list[int]) -> list[int]:
>     # Coordinate compression
>     sorted_unique = sorted(set(nums))
>     rank = {v: i + 1 for i, v in enumerate(sorted_unique)}
>     n = len(nums)
>     bit = BIT(len(sorted_unique))   # BIT class from above
>     result = []
> 
>     for i in range(n - 1, -1, -1):
>         r = rank[nums[i]]
>         result.append(bit.prefix_sum(r - 1))   # count of smaller values to the right
>         bit.update(r, 1)
> 
>     return result[::-1]
> ```

> [!success] Complexity
> Time O(n log n) | Space O(n).

> [!tip] Alternatives
> Merge sort (modified merge sort counting inversions): O(n log n), no coordinate compression needed. Balanced BST (AVL/Red-Black): O(n log n) but complex to implement. Segment tree on coordinate-compressed values: equivalent to BIT for this problem.

---

### Reverse Pairs

> [!example] Problem
> Count pairs `(i, j)` with `i < j` and `nums[i] > 2 * nums[j]`. LeetCode 493.

> [!info] Approach
> - **WHY:** Checking all pairs is O(n²). The condition `nums[i] > 2 * nums[j]` (with index order constraint) is an inversion-like problem amenable to merge sort or BIT.
> - **WHAT:** Process right to left using BIT. For each `nums[i]`, count already-inserted values `v` (from positions j > i) where `nums[i] > 2v`, i.e., `v < nums[i] / 2`, i.e., BIT prefix sum at `rank(floor((nums[i]-1)/2))`. Then insert `nums[i]` into BIT.
> - **HOW:** Coordinate compress `nums` (and also `nums[i]//2` values for query). Two separate coordinate sets or unified set with both values.

> [!note]- Python Solution
> ```python
> def reverse_pairs(nums: list[int]) -> int:
>     # Merge sort approach: O(n log n), no coordinate compression issues
>     count = 0
> 
>     def merge_sort(arr: list[int]) -> list[int]:
>         nonlocal count
>         if len(arr) <= 1:
>             return arr
>         mid = len(arr) // 2
>         left = merge_sort(arr[:mid])
>         right = merge_sort(arr[mid:])
>         # Count pairs: left[i] > 2 * right[j]
>         j = 0
>         for x in left:
>             while j < len(right) and x > 2 * right[j]:
>                 j += 1
>             count += j
>         # Standard merge
>         return sorted(left + right)  # use proper merge for O(n log n)
> 
>     merge_sort(nums)
>     return count
> ```

> [!success] Complexity
> Time O(n log n) | Space O(n).

> [!tip] Alternatives
> BIT with coordinate compression: compress all values in `nums` plus `(nums[i]-1)//2` for query values; process right to left, query then update. O(n log n) same, but coordinate compression is finicky with the `2*` factor. Merge sort is cleaner for this specific problem.

---

## Segment Tree — Interval / Scheduling Problems

---

### My Calendar I (LC 729)

> [!example] Problem
> Implement a calendar that rejects double bookings. `book(start, end)` returns False if `[start, end)` overlaps any existing booking, True and inserts it otherwise.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Need to detect overlapping intervals efficiently on each insert.
> - WHAT: Maintain a sorted list of `(start, end)` pairs. Binary search to find neighbors; check only adjacent intervals for overlap.
> - HOW: Two intervals `[s1, e1)` and `[s2, e2)` overlap iff `s1 < e2 and s2 < e1`. For a new booking `[s, e)`:
>   - Find the insertion point `i` via `bisect_left` on starts.
>   - Check left neighbor (`i-1`): does it end after `s`?
>   - Check right neighbor (`i`): does it start before `e`?
>   - If neither overlaps, insert.

> [!note]- Python Solution
> ```python
> from sortedcontainers import SortedList
>
> class MyCalendar:
>     def __init__(self) -> None:
>         self.bookings = SortedList(key=lambda x: x[0])
>
>     def book(self, start: int, end: int) -> bool:
>         # Find position of new booking by start
>         idx = self.bookings.bisect_key_left(start)
>         # Check right neighbor
>         if idx < len(self.bookings) and self.bookings[idx][0] < end:
>             return False
>         # Check left neighbor
>         if idx > 0 and self.bookings[idx - 1][1] > start:
>             return False
>         self.bookings.add((start, end))
>         return True
>
> # Bisect-only alternative (no sortedcontainers):
> import bisect
>
> class MyCalendarBisect:
>     def __init__(self) -> None:
>         self.starts: list[int] = []
>         self.ends: list[int] = []
>
>     def book(self, start: int, end: int) -> bool:
>         idx = bisect.bisect_left(self.starts, start)
>         if idx < len(self.starts) and self.starts[idx] < end:
>             return False
>         if idx > 0 and self.ends[idx - 1] > start:
>             return False
>         self.starts.insert(idx, start)
>         self.ends.insert(idx, end)
>         return True
> ```

> [!success] Complexity
> Time O(log n) per query (bisect), O(n) per insert (list shift) | Space O(n). With a balanced BST (e.g., `SortedList`): O(log n) insert.

> [!tip] Alternatives
> - Segment tree with lazy propagation: O(log MAX) per operation, MAX = 10⁹ with coordinate compression — overkill for this problem but O(log n) insert guaranteed.
> - Interval tree: O(log n) insert and query theoretically; complex to implement.

---

### My Calendar II (LC 731)

> [!example] Problem
> Allow bookings unless they cause a triple booking (3 overlapping events at any point). `book(start, end)` returns False if it would create a triple overlap.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Track both single bookings and double-booked regions. A new booking is invalid iff it intersects any already double-booked interval.
> - WHAT: Two lists — `calendar` (all accepted bookings) and `overlaps` (intervals that are already double-booked).
> - HOW: For new `[s, e)`:
>   1. Check if `[s, e)` overlaps any interval in `overlaps`. If yes → return False.
>   2. Else: add intersection of `[s, e)` with each existing booking in `calendar` to `overlaps`.
>   3. Add `[s, e)` to `calendar`.

> [!note]- Python Solution
> ```python
> class MyCalendarTwo:
>     def __init__(self) -> None:
>         self.calendar: list[tuple[int, int]] = []
>         self.overlaps: list[tuple[int, int]] = []
>
>     def book(self, start: int, end: int) -> bool:
>         # Check against existing double-booked regions
>         for os, oe in self.overlaps:
>             if start < oe and os < end:  # overlap exists
>                 return False
>         # Add intersections with existing single bookings to overlaps
>         for s, e in self.calendar:
>             lo, hi = max(start, s), min(end, e)
>             if lo < hi:
>                 self.overlaps.append((lo, hi))
>         self.calendar.append((start, end))
>         return True
> ```

> [!success] Complexity
> Time O(n) per booking (scan both lists) | Space O(n).

> [!tip] Alternatives
> - Segment tree with range add + range max query (lazy propagation): O(log MAX) per booking — MAX coordinate-compressed. Query max in [start, end-1]; if < 2, range-add 1, else reject.
> - Difference array with sorted map: same event-sweep idea in O(n log n) per query.

---

### My Calendar III (LC 732)

> [!example] Problem
> After each `book(start, end)` call, return the maximum number of concurrent events (k-booking) at any point in time.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Need the global maximum overlap count after each insertion — segment tree with lazy range-add and range-max query gives O(log MAX) per operation.
> - WHAT: Two approaches — difference array / sorted map sweep (simpler, O(n) per query) or segment tree with lazy propagation (O(log MAX) per query).
> - HOW (difference array with SortedDict):
>   - On `book(s, e)`: `diff[s] += 1`, `diff[e] -= 1`. Sweep prefix sum, track max. O(n) per call.
> - HOW (segment tree):
>   - Range add `[start, end-1] += 1`. Query global max (root value). O(log MAX) per call.

> [!note]- Python Solution
> ```python
> # Approach 1: Sorted map difference array — O(n) per book
> from sortedcontainers import SortedDict
>
> class MyCalendarThree:
>     def __init__(self) -> None:
>         self.diff: SortedDict[int, int] = SortedDict()
>
>     def book(self, start: int, end: int) -> int:
>         self.diff[start] = self.diff.get(start, 0) + 1
>         self.diff[end] = self.diff.get(end, 0) - 1
>         cur = res = 0
>         for v in self.diff.values():
>             cur += v
>             res = max(res, cur)
>         return res
>
>
> # Approach 2: Segment tree with lazy propagation — O(log MAX) per book
> class SegTreeCalendar:
>     def __init__(self) -> None:
>         self.tree: dict[int, int] = {}  # node -> max value
>         self.lazy: dict[int, int] = {}  # node -> pending add
>
>     def _push_down(self, node: int) -> None:
>         if self.lazy.get(node, 0):
>             for child in (2 * node, 2 * node + 1):
>                 self.tree[child] = self.tree.get(child, 0) + self.lazy[node]
>                 self.lazy[child] = self.lazy.get(child, 0) + self.lazy[node]
>             self.lazy[node] = 0
>
>     def update(self, node: int, start: int, end: int, l: int, r: int) -> None:
>         if r < start or end < l:
>             return
>         if l <= start and end <= r:
>             self.tree[node] = self.tree.get(node, 0) + 1
>             self.lazy[node] = self.lazy.get(node, 0) + 1
>             return
>         self._push_down(node)
>         mid = (start + end) // 2
>         self.update(2 * node, start, mid, l, r)
>         self.update(2 * node + 1, mid + 1, end, l, r)
>         self.tree[node] = max(self.tree.get(2 * node, 0), self.tree.get(2 * node + 1, 0))
>
> class MyCalendarThreeST:
>     def __init__(self) -> None:
>         self.st = SegTreeCalendar()
>
>     def book(self, start: int, end: int) -> int:
>         self.st.update(1, 0, 10**9, start, end - 1)
>         return self.st.tree.get(1, 0)
> ```

> [!success] Complexity
> Sorted map: O(n) per book, O(n) space | Segment tree: O(log MAX) per book, O(n log MAX) space (dynamic nodes).

> [!tip] Alternatives
> - Coordinate compression + static segment tree: O(n log n) total if all queries known upfront.
> - Sweep line with heap: O(n log n) offline, not applicable here (online queries).

---

### The Skyline Problem (LC 218)

> [!example] Problem
> Given buildings `[left, right, height]`, output the skyline — a list of `[x, height]` key points where the visible height changes.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: At each x-coordinate, the visible height = max height of all buildings covering that x. Key points occur only at building left/right edges.
> - WHAT: Event-based sweep with a max-heap of active buildings.
> - HOW:
>   - Create events: `(left, -height, right)` for building starts (negative height for sort order), `(right, 0, 0)` for building ends.
>   - Sort all events by x, then by height (starts before ends at same x — negative heights sort first).
>   - Use a max-heap of `(-height, right)` for active buildings.
>   - At each x: remove expired buildings (right ≤ current x) from heap top. Current height = `-heap[0][0]`. If height changed from previous, add `[x, height]` to result.

> [!note]- Python Solution
> ```python
> import heapq
>
> def get_skyline(buildings: list[list[int]]) -> list[list[int]]:
>     events: list[tuple[int, int, int]] = []
>     for l, r, h in buildings:
>         events.append((l, -h, r))   # start event: negative height sorts before end
>         events.append((r, 0, 0))    # end event
>     events.sort()
>
>     result: list[list[int]] = []
>     heap: list[tuple[int, int]] = [(0, float('inf'))]  # (-height, right_boundary)
>     prev_max = 0
>
>     for x, neg_h, right in events:
>         if neg_h != 0:  # start of a building
>             heapq.heappush(heap, (neg_h, right))
>         # Remove buildings that have ended (lazy deletion)
>         while heap[0][1] <= x:
>             heapq.heappop(heap)
>         cur_max = -heap[0][0]
>         if cur_max != prev_max:
>             result.append([x, cur_max])
>             prev_max = cur_max
>
>     return result
> ```

> [!success] Complexity
> Time O(n log n) — sorting events + heap operations | Space O(n).

> [!tip] Alternatives
> - Segment tree with coordinate compression: O(n log n) — range max update for each building, sweep x-coordinates. Cleaner for many range queries but more code.
> - Multiset (SortedList): instead of lazy-deletion heap, maintain a multiset of active heights; remove exactly on end events. O(n log n), avoids lazy deletion complexity.

---

### Falling Squares (LC 699)

> [!example] Problem
> Squares fall from the sky at positions `(left, side_length)`. After each square falls, return the current maximum height of any stack. A square lands on top of whatever is below it in its x-range.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Each falling square lands at the max height currently in `[left, left+size)`. After landing, the height in that range becomes `bottom + size`. Need range max query + range assignment update.
> - WHAT: Segment tree with lazy propagation for range max update and global max query, using coordinate compression on the x-axis.
> - HOW (brute force for clarity):
>   - For each square `(left, size)`: `right = left + size`.
>   - `bottom = max height in [left, right)` over all previously placed squares.
>   - `new_height = bottom + size`.
>   - Update: set all heights in `[left, right)` to `max(current, new_height)`.
>   - Record global max after each square.

> [!note]- Python Solution
> ```python
> # Brute force O(n²) — clear and correct for interview
> def falling_squares_brute(positions: list[list[int]]) -> list[int]:
>     intervals: list[tuple[int, int, int]] = []  # (left, right, height)
>     result: list[int] = []
>     global_max = 0
>
>     for left, size in positions:
>         right = left + size
>         bottom = 0
>         for l, r, h in intervals:
>             if l < right and left < r:  # overlap
>                 bottom = max(bottom, h)
>         new_height = bottom + size
>         intervals.append((left, right, new_height))
>         global_max = max(global_max, new_height)
>         result.append(global_max)
>     return result
>
>
> # O(n log n) with coordinate compression + segment tree range-max assignment
> from typing import DefaultDict
> from collections import defaultdict
>
> def falling_squares(positions: list[list[int]]) -> list[int]:
>     # Coordinate compress x-values
>     coords = sorted({x for l, s in positions for x in (l, l + s)})
>     rank = {v: i for i, v in enumerate(coords)}
>     N = len(coords)
>
>     tree = [0] * (4 * N)
>     lazy = [0] * (4 * N)
>
>     def push_down(node: int) -> None:
>         if lazy[node]:
>             for c in (2*node+1, 2*node+2):
>                 tree[c] = max(tree[c], lazy[node])
>                 lazy[c] = max(lazy[c], lazy[node])
>             lazy[node] = 0
>
>     def update(node: int, start: int, end: int, l: int, r: int, val: int) -> None:
>         if r <= start or end <= l:
>             return
>         if l <= start and end <= r:
>             tree[node] = max(tree[node], val)
>             lazy[node] = max(lazy[node], val)
>             return
>         push_down(node)
>         mid = (start + end) // 2
>         update(2*node+1, start, mid, l, r, val)
>         update(2*node+2, mid, end, l, r, val)
>         tree[node] = max(tree[2*node+1], tree[2*node+2])
>
>     def query(node: int, start: int, end: int, l: int, r: int) -> int:
>         if r <= start or end <= l:
>             return 0
>         if l <= start and end <= r:
>             return tree[node]
>         push_down(node)
>         mid = (start + end) // 2
>         return max(query(2*node+1, start, mid, l, r),
>                    query(2*node+2, mid, end, l, r))
>
>     result: list[int] = []
>     global_max = 0
>     for left, size in positions:
>         l, r = rank[left], rank[left + size]
>         bottom = query(1, 0, N, l, r)
>         new_h = bottom + size
>         update(1, 0, N, l, r, new_h)
>         global_max = max(global_max, new_h)
>         result.append(global_max)
>     return result
> ```

> [!success] Complexity
> Brute force: O(n²) time, O(n) space | Segment tree: O(n log n) time, O(n) space with coordinate compression.

> [!tip] Alternatives
> - Interval dict / interval merge: track non-overlapping intervals with heights; merge on each drop. O(n²) worst case without balanced structure.
> - SortedList of disjoint intervals: similar to above but O(n log n) amortized with careful implementation.

---

## See Also

[[sorting]] | [[dynamic-programming]] | [[binary-search]]
### Range Add Range Sum with Lazy Propagation

> [!example] Problem
> Support range increment updates and range sum queries on an array efficiently.

> [!info] Approach
> - **WHY:** Updating every element in a range directly is O(n). Lazy propagation stores a postponed update at internal nodes so repeated range updates stay logarithmic.
> - **WHAT:** Each node stores the sum of its segment and a lazy tag for pending additions.
> - **HOW:** On full-cover update, modify the node sum and lazy tag. On partial overlap, push the lazy value to children before recursing.

> [!note]- Python Solution
> ```python
> class SegTree:
>     def __init__(self, nums: list[int]):
>         self.n = len(nums)
>         self.tree = [0] * (4 * self.n)
>         self.lazy = [0] * (4 * self.n)
> 
>     def _apply(self, idx: int, left: int, right: int, delta: int) -> None:
>         self.tree[idx] += (right - left + 1) * delta
>         self.lazy[idx] += delta
> ```

> [!success] Complexity
> O(log n) per update/query, O(n) space.

> [!tip] Alternatives
> For prefix-sum-friendly updates, a Fenwick tree may be simpler; lazy segment trees handle general range aggregates.

---

## Segment Tree Applications

### Falling Squares (LC 699)

> [!example] Problem
> Squares of given size fall at given positions. After each square lands, return the height of the tallest stack. Each square rests on the ground or on top of a previous overlapping square.

> [!info] Approach
> - **WHY:** After each square falls at `[left, left+size)`, its height = size + max existing height in `[left, left+size)`. We need range-max-query and range-update, which a segment tree with lazy propagation handles in O(log n) per operation.
> - **WHAT:** Coordinate-compress all left and right endpoints (since positions can be large). Use a segment tree supporting range max query and range assignment update.
> - **HOW:** For each square: query max height in its interval, compute new height = query result + size, update the interval to that new height, record the global max.

> [!note]- Python Solution
> ```python
> def falling_squares(positions: list[list[int]]) -> list[int]:
>     coords = set()
>     for left, size in positions:
>         coords.add(left)
>         coords.add(left + size)
>     sorted_coords = sorted(coords)
>     compress = {v: i for i, v in enumerate(sorted_coords)}
>     m = len(sorted_coords)
>
>     tree = [0] * (4 * m)
>     lazy = [0] * (4 * m)
>
>     def push_down(node: int) -> None:
>         if lazy[node] > 0:
>             for child in [2 * node, 2 * node + 1]:
>                 tree[child] = max(tree[child], lazy[node])
>                 lazy[child] = max(lazy[child], lazy[node])
>             lazy[node] = 0
>
>     def update(node: int, lo: int, hi: int, left: int, right: int, val: int) -> None:
>         if right <= lo or hi <= left:
>             return
>         if left <= lo and hi <= right:
>             tree[node] = max(tree[node], val)
>             lazy[node] = max(lazy[node], val)
>             return
>         push_down(node)
>         mid = (lo + hi) // 2
>         update(2 * node, lo, mid, left, right, val)
>         update(2 * node + 1, mid, hi, left, right, val)
>         tree[node] = max(tree[2 * node], tree[2 * node + 1])
>
>     def query(node: int, lo: int, hi: int, left: int, right: int) -> int:
>         if right <= lo or hi <= left:
>             return 0
>         if left <= lo and hi <= right:
>             return tree[node]
>         push_down(node)
>         mid = (lo + hi) // 2
>         left_max = query(2 * node, lo, mid, left, right)
>         right_max = query(2 * node + 1, mid, hi, left, right)
>         return max(left_max, right_max)
>
>     result = []
>     global_max = 0
>     for left, size in positions:
>         l = compress[left]
>         r = compress[left + size]
>         current_height = query(1, 0, m, l, r)
>         new_height = current_height + size
>         update(1, 0, m, l, r, new_height)
>         global_max = max(global_max, new_height)
>         result.append(global_max)
>     return result
> ```

> [!success] Complexity
> Time O(n log n) with coordinate compression. Space O(n).

> [!tip] Alternatives
> - Brute force: for each square, scan all previous squares for overlap — O(n²). Fine for small inputs.
> - Sorted intervals + ordered dict: can work but segment tree with coordinate compression is the clean solution.

---

### Count of Smaller Numbers After Self (LC 315) — BIT Approach

> [!example] Problem
> Given an integer array, return a count array where `count[i]` is the number of elements to the right of `nums[i]` that are smaller than `nums[i]`.

> [!info] Approach
> - **WHY:** Scanning right to left, for each element we need "how many elements seen so far are smaller than the current element." A BIT on coordinate-compressed values answers this as a prefix-sum query.
> - **WHAT:** Coordinate-compress all values. Scan right to left. For each `nums[i]`: query BIT for prefix sum up to `rank[nums[i]] - 1` (count of smaller values already processed), then update BIT at `rank[nums[i]]`.
> - **HOW:** Sort unique values to build rank map. Scan right to left: `count[i] = bit.query(rank[nums[i]] - 1)`. Then `bit.update(rank[nums[i]], 1)`.

> [!note]- Python Solution
> ```python
> def count_smaller(nums: list[int]) -> list[int]:
>     sorted_unique = sorted(set(nums))
>     rank = {v: i + 1 for i, v in enumerate(sorted_unique)}
>     m = len(sorted_unique)
>     bit = [0] * (m + 1)
>
>     def update(i: int) -> None:
>         while i <= m:
>             bit[i] += 1
>             i += i & -i
>
>     def query(i: int) -> int:
>         total = 0
>         while i > 0:
>             total += bit[i]
>             i -= i & -i
>         return total
>
>     result = []
>     for num in reversed(nums):
>         r = rank[num]
>         result.append(query(r - 1))
>         update(r)
>     result.reverse()
>     return result
> ```

> [!success] Complexity
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> - Merge sort (divide and conquer): count inversions during merge — also O(n log n). More complex but avoids coordinate compression.
> - Segment tree: equivalent to BIT for this problem; BIT is simpler to code.

---

### Range Sum Query 2D — Mutable (LC 308)

> [!example] Problem
> Design a data structure for a 2D matrix that supports point updates and rectangular range sum queries.

> [!info] Approach
> - **WHY:** A 2D Fenwick tree (BIT) extends the 1D BIT to two dimensions. Point update and range sum both run in O(log m * log n).
> - **WHAT:** Maintain a 2D BIT where `bit[i][j]` stores the sum for a "responsible region." Update propagates along both row and column axes simultaneously.
> - **HOW:** Update `(r, c)` by delta: iterate `i = r+1` by `i += i & -i`, and for each `i` iterate `j = c+1` by `j += j & -j`, adding delta to `bit[i][j]`. Query prefix sum up to `(r, c)`: sum over all `i` and `j` indices descending by clearing the lowest bit.

> [!note]- Python Solution
> ```python
> class NumMatrix:
>     def __init__(self, matrix: list[list[int]]):
>         self.m = len(matrix)
>         self.n = len(matrix[0])
>         self.matrix = [[0] * self.n for _ in range(self.m)]
>         self.bit = [[0] * (self.n + 1) for _ in range(self.m + 1)]
>         for r in range(self.m):
>             for c in range(self.n):
>                 self.update(r, c, matrix[r][c])
>
>     def update(self, row: int, col: int, val: int) -> None:
>         delta = val - self.matrix[row][col]
>         self.matrix[row][col] = val
>         i = row + 1
>         while i <= self.m:
>             j = col + 1
>             while j <= self.n:
>                 self.bit[i][j] += delta
>                 j += j & -j
>             i += i & -i
>
>     def _prefix_sum(self, row: int, col: int) -> int:
>         total = 0
>         i = row + 1
>         while i > 0:
>             j = col + 1
>             while j > 0:
>                 total += self.bit[i][j]
>                 j -= j & -j
>             i -= i & -i
>         return total
>
>     def sum_region(self, row1: int, col1: int, row2: int, col2: int) -> int:
>         total = self._prefix_sum(row2, col2)
>         total -= self._prefix_sum(row1 - 1, col2)
>         total -= self._prefix_sum(row2, col1 - 1)
>         total += self._prefix_sum(row1 - 1, col1 - 1)
>         return total
> ```

> [!success] Complexity
> Time O(log m * log n) per update/query, Space O(m * n).

> [!tip] Alternatives
> - 2D segment tree: more general (supports range updates) but much more complex to implement.
> - Recompute prefix sums on each query: O(mn) per query — fine for read-heavy workloads without updates.

---

## See Also

[[array]] | [[binary-search]] | [[sorting]] | [[dynamic-programming]]
