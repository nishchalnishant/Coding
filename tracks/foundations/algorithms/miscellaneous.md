# Miscellaneous Algorithms — SDE-3 Gold Standard

Advanced data structures and cross-cutting patterns that don't fit neatly into one category. SDE-3 expects: Fenwick tree for dynamic prefix sums, segment tree for range queries, and rapid problem-category recognition for "disguised" problems.

---

## Theory & Mental Models

**What it is.** Advanced data structures (Fenwick tree, Segment tree, Sparse table) and sweep-line / design patterns that don't fit a single algorithmic paradigm. Core invariant: each structure exploits a specific structural property of its problem class — binary index tricks for prefix sums, interval trees for range aggregation, event sorting for sweep line.

**Why it exists.** Many competitive and SDE-3 interview problems require operations that prefix arrays can't support (point updates) or that Fenwick trees can't express (range min/max). These structures fill those gaps at O(log N) per operation rather than O(N) brute force.

**The mental model.** Power tools for specific problem shapes. Fenwick tree = "dynamic prefix sum with a 10-line implementation"; Segment tree = "any associative range operation + lazy propagation"; Sweep line = "sort events by x, process with an active set"; LRU/LFU = "system design in code using standard data structure combos".

**Complexity at a glance.**

| Structure | Build | Point Update | Range Query | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Prefix array (static) | O(N) | O(N) rebuild | O(1) | Read-only; no updates |
| Fenwick tree (BIT) | O(N log N) | O(log N) | O(log N) prefix sum | Supports sum and count; not min/max |
| Segment tree | O(N) | O(log N) | O(log N) | Any associative op; lazy prop for range update |
| Sparse table | O(N log N) | — (static) | O(1) | Idempotent ops only (min, max, GCD); no updates |
| Sweep line | O(N log N) | — | — | Sort + active set; O(N log N) total |

**When to reach for it.**
- Range sum/min/max with point updates → Fenwick (sum only) or Segment tree (general).
- Sliding window with complex queries → monotonic deque.
- Building data structures in code (LRU = HashMap + doubly linked list; LFU = three maps + min_freq).
- Event-based geometry (skyline problem, rectangle area union) → sweep line.
- Count inversions dynamically → Fenwick tree on coordinate-compressed values.

**When NOT to use it.**
- N is small (≤ 1000) — brute force is cleaner and faster to code.
- Array is read-only — a prefix sum array handles range sum in O(1) with O(N) precompute; no Fenwick needed.
- Range update + range query is needed — Segment tree with lazy propagation; Fenwick alone cannot do this cleanly.

**Common mistakes.**
- Fenwick tree is 1-indexed — `update(0, ...)` is wrong; all indices must be ≥ 1.
- Segment tree: lazy propagation must be pushed down before querying children — missed push-down produces stale values.
- LRU: "move to head on get" is required, not just on put — forgetting this breaks the recency invariant.
- LFU: `min_freq` must be reset to 1 on every new key insertion — not resetting causes wrong eviction.

---

## 1. Advanced Data Structures

### Fenwick Tree (Binary Indexed Tree) — Dynamic Prefix Sums

> [!IMPORTANT]
> **The Click Moment**: "**Point update + prefix sum query**" — OR — "count of elements ≤ x in a **dynamic** array" — OR — "**inversion count** (merge sort alternative)". Fenwick tree gives O(log N) update and O(log N) prefix sum with ~5× less code than a segment tree.

```python
class FenwickTree:
    def __init__(self, n: int) -> None:
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    def update(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)  # move to responsible parent

    def prefix_sum(self, i: int) -> int:
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)  # move to responsible ancestor
        return total

    def range_sum(self, l: int, r: int) -> int:
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

def count_inversions_fenwick(nums: list[int]) -> int:
    sorted_unique = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(sorted_unique)}
    tree = FenwickTree(len(sorted_unique))
    inversions = 0
    for i in range(len(nums) - 1, -1, -1):
        r = rank[nums[i]]
        inversions += tree.prefix_sum(r - 1)  # count smaller elements to the right
        tree.update(r, 1)
    return inversions
```

> [!TIP]
> `i & (-i)` isolates the lowest set bit of i. This is the entire indexing trick: `update` adds the lowest bit to climb to parent; `prefix_sum` subtracts the lowest bit to climb to the responsible ancestor. Memorize both directions — the asymmetry is why the tree works.

---

### Segment Tree — Range Query + Range Update

> [!IMPORTANT]
> **The Click Moment**: "**Range update + range query**" — OR — "**minimum / maximum / GCD** over a subarray" — OR — "dynamic range problems where Fenwick tree can't express the aggregation (min, max, GCD)". Segment tree handles any associative operation over ranges in O(log N).

```python
class SegmentTree:
    def __init__(self, nums: list[int]) -> None:
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        if nums:
            self._build(nums, 0, 0, self.n - 1)

    def _build(self, nums: list[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = nums[start]
            return
        mid = (start + end) // 2
        self._build(nums, 2 * node + 1, start, mid)
        self._build(nums, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]

    def update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self.update(2*node+1, start, mid, idx, val)
        else:
            self.update(2*node+2, mid+1, end, idx, val)
        self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]

    def query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return 0  # identity for sum; float('inf') for min; 0 for max
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self.query(2*node+1, start, mid, l, r) +
                self.query(2*node+2, mid+1, end, l, r))
```

> [!CAUTION]
> **Allocate 4×n nodes**, not 2×n. A complete binary tree on n leaves needs at most 4n array slots when n is not a power of 2. Off-by-one: node indices are 0-based, but range `[start, end]` is inclusive on both ends. The identity element for `query` out-of-range must match the aggregation (`0` for sum, `inf` for min, `-inf` for max).

---

### Sparse Table — O(1) Range Minimum Query (Static Arrays)

> [!IMPORTANT]
> **The Click Moment**: "**Static array**, many range min/max queries, O(1) per query". No updates allowed. Precompute in O(N log N); query in O(1) using overlapping power-of-2 intervals. Used as the engine for LCA (Lowest Common Ancestor) via Euler tour.

```python
import math

def build_sparse_table(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    k = max(1, math.floor(math.log2(n)) + 1)
    table = [nums[:]]
    for j in range(1, k):
        row = []
        for i in range(n - (1 << j) + 1):
            row.append(min(table[j-1][i], table[j-1][i + (1 << (j-1))]))
        table.append(row)
    return table

def rmq(table: list[list[int]], l: int, r: int) -> int:
    k = int(math.log2(r - l + 1))
    return min(table[k][l], table[k][r - (1 << k) + 1])
```

> [!TIP]
> Overlapping intervals are valid for **idempotent** operations (min, max, GCD) — taking the min of two overlapping ranges that cover `[l, r]` gives the correct answer. This does **not** work for sum (double-counting). For sum: use prefix array (static) or Fenwick tree (dynamic).

---

## 2. Cross-Topic Pattern Recognition

> [!IMPORTANT]
> **The Click Moment for "disguised" problems**: Ask — "What are the **nodes and edges**?" (→ graph). "Does it have **optimal substructure + overlapping subproblems**?" (→ DP). "Does a **local greedy choice** lead to global optimum?" (→ greedy). "Do I need **prefix aggregation** over a dynamic array?" (→ Fenwick/segment tree). "Is there a **monotonic structure**?" (→ stack/deque).

### Four-Step Problem Decomposition

1. **Identify the shape**: Array? Grid? Tree? Implicit graph (words, states, intervals)?
2. **Identify the operation**: Count? Shortest path? Max/min? Ordering?
3. **Match to pattern**: Use the trigger table below.
4. **State complexity**: Time + space before coding.

### Cross-Topic Trigger Table

| Pattern | Keywords / Shape | Core Idea | Complexity |
| :--- | :--- | :--- | :--- |
| **Intervals** | Merge, overlap, schedule, meeting rooms | Sort by start (merge) or end (greedy select); sweep + heap for count | O(N log N) |
| **Graph disguised** | Word ladder, evaluate division, course deps | Build adjacency from rules; BFS (unweighted) or Dijkstra (weighted) | O(V + E) |
| **Simulation / matrix** | Rotate, spiral, game of life, battleships | Direction array `(dr, dc)`; boundary tracking; in-place layer rotation | O(RC) |
| **Prefix + map** | Subarray sum = K, contiguous range | `prefix[j] - prefix[i] = K` → count `prefix[j] - K` in map | O(N) |
| **Fenwick / segment tree** | Range sum with updates, rank queries | Point update O(log N), range query O(log N) | O(N log N) pre |
| **Bitmask / bit DP** | N ≤ 20, all subsets, TSP-like | State = bitmask of included elements; enumerate `submask` or transitions | O(2^N · N) |
| **Math + implementation** | Trailing zeros, integer sqrt, max points | Number-theory shortcuts (Legendre, sieve, GCD normalize) | Varies |
| **Design / streaming** | LRU, LFU, rate limiter, moving average | Amortized O(1) via combined data structures; two-pointer / hash + DLL | O(1) amortized |

---

## 3. SDE-3 Deep Dives

### Scalability: Persistent Segment Tree

> [!TIP]
> A **persistent segment tree** stores all historical versions after each update by sharing unchanged nodes. Memory: O(N log N) for N updates (each update creates O(log N) new nodes). Used for: "count elements in range `[l, r]` with value in `[a, b]`" — query two prefix versions and subtract. Also called a "merge sort tree" or "wavelet tree" in competitive programming.

### Scalability: Mo's Algorithm — Offline Range Queries

> [!TIP]
> **Mo's algorithm** processes offline range queries in O((N + Q) √N) by sorting queries into √N-sized blocks to minimize element additions/removals. For each step, move `[l, r]` to `[l±1, r±1]` in O(1). Used when you need "count distinct in range" or frequency-based queries where a segment tree would be complex. Block size = √N is optimal.

### Concurrency: Concurrent Segment Tree

> [!TIP]
> For a read-heavy segment tree with infrequent updates: use a **readers-writer lock** (`threading.RLock` in Python; `ReentrantReadWriteLock` in Java). Multiple readers acquire shared mode concurrently; writers acquire exclusive mode. For extreme read throughput: maintain two copies and **atomically swap a pointer** on update — readers always see a consistent snapshot (MVCC). This is the pattern used in time-series databases.

### Trade-offs: Fenwick vs Segment Tree vs Prefix Array

| Capability | Prefix Array | Fenwick Tree | Segment Tree |
| :--- | :--- | :--- | :--- |
| Point update | O(N) rebuild | **O(log N)** | **O(log N)** |
| Range sum query | **O(1)** | **O(log N)** | **O(log N)** |
| Range min/max query | Sparse table O(1) static | ❌ Not natural | **O(log N)** |
| Range update + range query | ❌ | O(log N) with difference BIT | **O(log N)** with lazy prop |
| Code complexity | Minimal | Low (10 lines) | High (40+ lines) |

---

## 4. Common Interview Problems

### Medium (High Frequency)
- **Merge Intervals** — Sort by start; extend `end = max(end, interval[1])` while overlapping.
- **Meeting Rooms II** — Min-heap of end times; count concurrent meetings = heap size.
- **Task Scheduler** — Greedy: arrange most-frequent tasks with cooldown gaps; `ceil((max_count-1) * (n+1) + count_max)`.
- **Design LRU Cache** — HashMap + doubly linked list; O(1) get/put.
- **Range Sum Query (Mutable)** — Fenwick tree; O(log N) update and prefix query.

### Hard
- **Count of Smaller Numbers After Self** — Fenwick tree on coordinate-compressed values; or merge sort augmented.
- **Count of Range Sum** — Merge sort on prefix sums; count cross-half pairs in `[lower, upper]`.
- **The Skyline Problem** — Sweep line on building start/end events; max-heap of active heights.
- **Data Stream as Disjoint Intervals** — `SortedList` + binary search; merge left/right neighbors on insert.
- **Design LFU Cache** — Three maps: `key→val`, `key→freq`, `freq→OrderedDict`; track `min_freq`; O(1) all ops.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Merge Intervals** | Sort + Greedy Merge | "Combine overlapping [l, r] ranges" | Sort by start; extend `end` greedily while `interval[0] <= end` | Touching intervals `[1,2]` and `[2,3]` — confirm merging rule. Sort by start, not end. |
| **Meeting Rooms II** | "Minimum rooms for N meetings" | Min-heap of end times; if `heap[0] <= start`, reuse room (pop + push new end) | Heap size at any moment = answer (max concurrent meetings). Sort by start first. |
| **Range Sum Query Mutable** | "Prefix sum with point updates" | Fenwick tree; `update(i, delta)` and `prefix_sum(i)` each O(log N) | 1-indexed; `i += i & (-i)` for update; `i -= i & (-i)` for query — opposite directions. |
| **Count Smaller After Self** | "For each i, count j>i where nums[j]<nums[i]" | Fenwick on coordinate-compressed values (right-to-left); or merge sort counting right-picks | Merge sort: pass `(value, original_index)` pairs to track positions through sorting. |
| **The Skyline Problem** | "Height profile of buildings as events" | Sweep line on start/end events; max-heap of `(-height, end)` for active buildings | Lazy deletion from heap (check if top is still active). Critical point = when max height changes. |
| **Design LFU Cache** | "Evict least-frequently used; ties → LRU" | `key→val`, `key→freq`, `freq→OrderedDict`; track global `min_freq` | Reset `min_freq = 1` on every `put` of a new key. Increment `min_freq` in `get` only when `freq_map[min_freq]` becomes empty. |
| **Non-Overlapping Intervals** | "Min removals to make disjoint" | Sort by **end**; greedily keep interval with earliest end; count removals | Sort by end (not start): earliest end leaves max room for future intervals. |
| **Data Stream Intervals** | "Maintain disjoint intervals dynamically" | Binary search for left/right overlap; merge on insert | Handle both neighbors: merge left if `new.start <= left.end + 1`; merge right if `new.end >= right.start - 1`. |
| **Design HashSet [E]** | "Implement a hash set without built-in hash" | Array of buckets (chaining); `hash(key) = key % size`; linked list per bucket | Choose bucket count as a prime (e.g., 1009) to reduce collisions. Handle remove in chained list carefully. |
| **Design Hit Counter [E]** | "Count hits in the past 5 minutes" | Circular array of 300 slots (seconds); slot = `(timestamp, count)`; reset stale slot on write | `timestamp % 300` gives slot index. Reading: sum all slots where `timestamp - slot_time < 300`. |
| **LRU Cache [M]** | "O(1) get/put with eviction of least recently used" | `OrderedDict` or HashMap + doubly linked list; move to head on access; evict tail on overflow | Python `OrderedDict.move_to_end(key)` + `popitem(last=False)` gives O(1). Hand-roll DLL for interviews expecting lower-level answer. |
| **Design Twitter [M]** | "In-memory Twitter: post tweet, follow, getNewsFeed" | Per-user tweet list (most recent first); `getNewsFeed` = K-way merge of followees' lists via min-heap | K-way merge with heap: push `(timestamp, user, tweet_idx)`; pop 10 times. Follow/unfollow update a set. |
| **Range Sum Query — Immutable [E]** | "Precompute prefix sums for O(1) range queries" | `prefix[i] = prefix[i-1] + nums[i-1]`; `query(l,r) = prefix[r+1] - prefix[l]` | 1-indexed prefix array avoids boundary check. `prefix[0] = 0` sentinel. |
| **Snapshot Array [M]** | "Array with snapshot: get value at past snapshot" | Per-index list of `(snap_id, val)`; binary search on snap_id for reads | Store only changed values (copy-on-write). Binary search via `bisect_right(snaps, snap_id) - 1`. |
| **Find Median from Data Stream [H]** | "Maintain running median as numbers are inserted" | Two heaps: max-heap for lower half, min-heap for upper half; balance sizes | Max-heap in Python: negate values. Rebalance after every insert: sizes differ by at most 1. Median = top of larger heap or average of both tops. |
| **The Skyline Problem [H]** | "Building silhouette as list of key (x, height) points" | Sweep line on start/end events; max-heap of `(-height, end)`; emit when max height changes | Lazy-delete from heap (check if top building has ended). Critical: emit only when height **changes**, not on every event. |
| **Minimum Interval to Include Each Query [H]** | "For each query point, find smallest interval containing it" | Sort queries and intervals by start; min-heap `(size, end)` of active intervals; sweep and pop expired | Offline processing: sort queries + intervals together by left endpoint. Lazy-remove intervals where `end < query`. |

---

## Four Priorities When Writing a Function

1. **Correctness** — For every valid input the function returns the expected result; no ambiguous behavior.
2. **Time** — Choose the right algorithm and data structure; state complexity before coding.
3. **Space** — Minimize extra memory; in-place when possible.
4. **Clarity** — Self-explanatory names; no clever tricks that obscure intent.

---

## Quick Revision Triggers

- "Range sum / frequency queries with point updates" → Fenwick tree (BIT), O(log N) per op; use 1-indexed.
- "Range min/max/sum queries with range updates" → Segment tree with lazy propagation, O(log N).
- "Range min/max queries, no updates" → Sparse table, O(N log N) build, O(1) query.
- "Events at coordinates: intervals, rectangles, skyline" → sweep line; sort events by x, process with sorted structure.
- "O(1) average get/put with eviction of least recently used" → LRU: `OrderedDict` or doubly-linked list + hash map.
- "O(1) average get/put with eviction of least frequently used" → LFU: two hash maps + min_freq pointer; reset min_freq=1 on put.
- "Need both prefix sums and point updates" → Fenwick tree beats prefix array (which is O(N) on update).

---

## See also

- [Patterns Master](../../../reference/patterns/patterns-master.md) — 30-second recognition triggers for all patterns
- [Dynamic Programming](dynamic-programming/README.md) — optimal substructure; overlapping subproblems
- [Sorting](sorting.md) — sort key choices; when sort unlocks a greedy solution
- [Mathematics](maths.md) — number theory tricks; modular arithmetic
- [Graph Algorithms](graph.md) — when a problem is really a graph in disguise
