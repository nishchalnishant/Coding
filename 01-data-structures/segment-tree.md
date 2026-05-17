# Segment Trees — SDE-3 Gold Standard

Manage **Range Queries** and **Point/Range Updates** in $O(\log N)$. When a simple Prefix Sum fails due to frequent updates, the Segment Tree is your best friend.

---

## 🎙️ The Coach's Dialogue: When to Reach for the Segment Tree

**Student:** "Coach, I'm confused. If I need a range sum, can't I just use a Prefix Sum array? It's O(1) for queries!"

**Coach:** "Great question. Prefix Sums are perfect for **static** data. But what if the numbers are constantly changing? If you update one element in a Prefix Sum array, you have to recompute the entire array, which is O(N). If you have 100,000 updates, you're looking at a TLE."

**Student:** "So Segment Tree is for **dynamic** range queries?"

**Coach:** "Exactly. It balances the cost. Both updates and queries become O(log N). Think of it as a middle ground between the O(1) query/O(N) update of Prefix Sums and the O(N) query/O(1) update of a raw array."

**Student:** "Is it always just for 'Sum'?"

**Coach:** "Not at all. You can use it for `min`, `max`, `GCD`, or even 'Longest Increasing Subsequence' in a range. Any operation that is **associative** can be 'segmented'."

---

## 1. Concept Overview

**What it is**: A binary tree where each node represents an interval (range) of the original array. The root represents `[0, n-1]`, and its children split that range in half.

**Why it exists**: To handle range queries (Sum, Min, Max) on an array while supporting efficient element-level or range-level updates.

**Complexity at a glance**:
- **Build**: $O(N)$
- **Point Update**: $O(\log N)$
- **Range Query**: $O(\log N)$
- **Range Update (Lazy Propagation)**: $O(\log N)$
- **Space**: $O(4N)$ (Standard array-based implementation)

---

## 2. Core Implementation (SDE-3 Canonical)

### 2.1 Recursive Segment Tree (Point Update + Range Sum)

```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self._build(data, 2 * node, start, mid)
        self._build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, idx, val):
        self._update(1, 0, self.n - 1, idx, val)

    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if start <= idx <= mid:
            self._update(2 * node, start, mid, idx, val)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, l, r):
        return self._query(1, 0, self.n - 1, l, r)

    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0  # Out of range
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        p1 = self._query(2 * node, start, mid, l, r)
        p2 = self._query(2 * node + 1, mid + 1, end, l, r)
        return p1 + p2
```

---

## 3. SDE-3 Deep Dive: Lazy Propagation

When you need to update an entire **range** (e.g., "Add 5 to every element from index 10 to 500"), updating each element individually is $O(K \log N)$. **Lazy Propagation** allows you to perform this range update in $O(\log N)$ by deferring updates until the nodes are actually needed.

### The "Aha!" Moment
Don't update the children until you're forced to visit them. Store the "pending work" in a `lazy` array. When you visit a node, "push" its lazy value down to its children.

---

## 4. Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Range Sum Query - Mutable [M]** | Segment Tree | Frequent point updates + range queries | Standard recursive Segment Tree | $O(4N)$ space — don't forget the size! |
| **Range Minimum Query [M]** | Segment Tree (Min) | Range min with updates | Same structure as sum tree; merge returns `min(left, right)` | Sentinel value is `float('inf')`, not `0` — wrong default silently breaks queries |
| **Falling Squares [H]** | Max-Segment Tree + Lazy | Range updates (new height) + Range max query | Store max height; lazy propagation for range update | The square "lands" on the max height of its range — relative, not absolute heights |
| **Count of Smaller Numbers After Self [H]** | Segment Tree / BIT | Frequency array update + Prefix sum query | Traverse right to left; query `sum(0, val-1)`, then `update(val)` | Coordinate compression required when values are large or negative |
| **The Skyline Problem [H]** | Max-Segment Tree | Max height at each x-coordinate | Coordinate-compress x values; sweep left-to-right updating max height | Usually solved with heap, but segment tree handles arbitrary range queries more robustly |
| **My Calendar I [M]** | Segment Tree / Sorted List | Overlap detection on interval add | Build lazily; query `[start, end-1]` before booking; set range to 1 | Booking requests can interleave unpredictably — segment tree handles non-sorted inserts naturally |
| **My Calendar II [M]** | Segment Tree (count) | Triple booking detection | Maintain `bookings` (≥1) and `overlaps` (≥2) trees; reject if query on `overlaps` hits the new range | Two separate trees for "at least once" and "at least twice" |
| **My Calendar III [H]** | Segment Tree + Lazy (max) | Max k concurrent events at any time | Range add +1 on `[start, end-1]`; global max query gives max concurrency | Lazy propagation critical — naive point updates are $O(N)$ per booking |
| **Count of Range Sum [H]** | Segment Tree / Merge Sort | Count prefix sum pairs where `lower ≤ P[j] - P[i] ≤ upper` | Coordinate-compress prefix sums; for each `P[j]`, query `[P[j]-upper, P[j]-lower]` | Off-by-one in coordinate compression kills accuracy; merge sort alternative avoids it |
| **Rectangle Area II [H]** | Segment Tree + Coordinate Compression | Union area of N rectangles | Sweep line over y; for active x-intervals, query covered length via segment tree | Counting distinct covered x-length via lazy tree is non-trivial — "count" node tracks segments |
| **Maximum Sum of Subarray No Larger Than K [H]** | Segment Tree / Sorted Set | For each `j`, find max `P[i]` ≤ `P[j] - k` | Keep sorted prefix sums; binary search for `ceil(P[j] - k)` | Sorted set (SortedList in Python) with `bisect` achieves O(N log N); Segment Tree approach needs coordinate compression |
| **Number of Longest Increasing Subsequences [M]** | Segment Tree on values | Max LIS length ending at val + count of such sequences | Maintain `(max_len, count)` pairs; query `[0, val-1]`, update at `val` | Merging `(len, count)` pairs requires handling ties correctly: same length → add counts |
| **Interval Sum with Range Add [M]** | Segment Tree + Lazy Propagation | Range add on `[l, r]` then range sum query | Lazy node stores pending addend; push down before traversal | Must push lazy down before recursing into children — missing push causes stale values |
| **Coordinate Compression Pattern** | Prerequisite technique | Values are too large for array indices | Map unique values to `[0, M)` range; use compressed index in the tree | Must sort **and** deduplicate; after compression, original problem logic is unchanged |
| **Segment Tree Beats (Ji Driver) [H]** | Advanced: Range min-chmin | Range `a[i] = min(a[i], v)` + range sum query | Maintain per-node `max1`, `max2`, `cnt_max`, `sum`; break if `v ≥ max1`, push if `v > max2` | Extremely hard to implement under pressure — know the concept and complexity ($O(N \log^2 N)$); rarely asked in interviews |

---

## 5. Quick Revision Triggers

- "Dynamic range queries (Sum/Min/Max/GCD) + Frequent updates" → Segment Tree.
- "Range Updates" (e.g., add `X` to `[L, R]`) → **Lazy Propagation**.
- "Values are too large for an array index" → **Coordinate Compression** first.
- "Memory is tight" → Consider a **Fenwick Tree** (BIT) if you only need Range Sums and Point Updates (it's O(N) space and simpler to code).

---

## See also

- [Fenwick Trees (BIT)](advanced-structures.md#fenwick-tree) — For simpler sum-based range queries.
- [Prefix Sums](array.md#prefix-sum) — For static data.
- [Coordinate Compression](miscellaneous.md#coordinate-compression) — Prerequisite for many Segment Tree problems.
