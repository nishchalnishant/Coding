---
tags: [coding, data-structures, advanced]
topic: Advanced Data Structures
difficulty: mixed
---

# Advanced Data Structures


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## Skip List (Conceptual)

> **WHY it exists.** Balanced BSTs (AVL, Red-Black) achieve O(log n) search/insert/delete but require complex rotations. Skip lists achieve the same expected O(log n) bounds probabilistically using a layered linked list — simpler to implement and reason about. Used in Redis (sorted sets), LevelDB (memtable).

>
> **WHAT it is.** A hierarchy of linked lists. Level 0 = complete sorted linked list. Each higher level is a random subset: each node is promoted to the next level with probability p (typically 1/2). A node at level k appears in all levels 0..k.
>
> **HOW it works.**
> - Search: start at the topmost level of the head sentinel. At each node, if `next.key <= target`, advance right; else drop down one level. Repeat until level 0.
> - Insert: search to find predecessor at each level (record in `update[]` array). Randomly determine new node's height by flipping coins. Link into all levels ≤ height.
> - Delete: find predecessors at all levels, unlink the node.

```
Level 3: head ──────────────────────────> 50 ──> tail
Level 2: head ──────────> 20 ──────────> 50 ──> tail
Level 1: head ──> 10 ──> 20 ──> 30 ──> 50 ──> tail
Level 0: head ──> 10 ──> 20 ──> 30 ──> 40 ──> 50 ──> tail
```

> [!success] Complexity
> Expected O(log n) search, insert, delete | Space O(n log n) expected.

> [!tip] When to use
> When you need a sorted dynamic set with simple implementation. In practice, Python's `sortedcontainers.SortedList` is a B-tree-based skip-list alternative used in competitive programming.
>
> **Key insight.** Randomization replaces balancing — the expected height of any node is O(log n), which bounds the number of "drop-down" operations during search.

---

## Disjoint Set Union (see union-find.md for full coverage)

> **Cross-reference.** Full implementation (union by rank + path compression), applications (connected components, Kruskal's MST, redundant connections), and complexity analysis are in `/Users/nishchalnishant/Documents/GitHub/Coding/coding/algorithms/union-find.md`.

>
> **Core idea in brief.** Each set is a rooted tree. `find(x)` walks to the root (with path compression: point every node on the path directly to the root in one pass). `union(x, y)` attaches the smaller tree's root under the larger's (union by rank or size). Near-O(1) amortized per operation via inverse Ackermann function.

> [!tip] When advanced DSU appears
> - Weighted DSU: track relative weights along edges (e.g., "how many times heavier is x than y").
> - Rollback DSU: offline algorithms requiring undo of union operations — use union by rank only (no path compression), store history as a stack.
> - Parallel DSU: for offline LCT-like problems on trees.

---

## Suffix Array

> **WHY it exists.** Suffix trees are O(n) but use O(n) space with a large constant and are complex to implement. Suffix arrays are an array-based alternative: O(n log n) or O(n) to build, O(n) space, and enable the same queries via the LCP array.

>
> **WHAT it is.** `SA[i]` = start index of the i-th lexicographically smallest suffix of string `s`. `LCP[i]` = length of the longest common prefix between suffix `SA[i]` and suffix `SA[i-1]`.

---

### Longest Common Prefix of Suffixes (LCP Array)

> [!example] Problem
> Build the LCP array and use it to find the longest repeated substring.

> [!info] Approach
> LCP[i] tells us how many characters adjacent suffixes in SA share. Max LCP = longest repeated substring (appears at two positions = two adjacent suffixes in SA with high overlap). Kasai's algorithm exploits: if `LCP(SA[rank[i]], SA[rank[i]-1]) = h`, then `LCP(SA[rank[i+1]], SA[rank[i+1]-1]) >= h - 1`. This means `h` can only decrease by 1 per step across all i, so the total work is O(n). See implementation in `count_distinct_substrings` above. Longest repeated = `s[sa[idx] : sa[idx] + max(lcp)]`.

> [!success] Complexity
> Kasai LCP: O(n) | Space O(n).

> [!tip] Alternatives
> Suffix automaton: O(n) build, longest repeated = longest path to a non-clone state with multiple end-positions. More powerful but harder to implement.

---

## Sparse Table (Range Minimum Query in O(1))

> **WHY it exists.** Segment trees give O(log n) RMQ but require updates. When the array is static, we can precompute all power-of-2 range answers and answer any query in O(1) using the "overlap trick" — min is idempotent so overlapping ranges give the correct answer.

>
> **WHAT it is.** `sparse[k][i]` = minimum of `a[i..i+2^k-1]`. Query `[l, r]`: let `k = floor(log2(r-l+1))`; answer = `min(sparse[k][l], sparse[k][r-2^k+1])`. The two ranges overlap but that's fine because min is idempotent.
>
> **HOW it works.**
> - Build: `sparse[0][i] = a[i]`. For k = 1..log(n): `sparse[k][i] = min(sparse[k-1][i], sparse[k-1][i + 2^(k-1)])`.
> - Query: O(1) — compute k, look up two entries.

> [!note]- Python Solution
> ```python
> import math
> 
> class SparseTable:
>     def __init__(self, nums):
>         n = len(nums)
>         LOG = max(1, n.bit_length())
>         self.table = [[float('inf')] * n for _ in range(LOG)]
>         self.log2 = [0] * (n + 1)
>         for i in range(2, n + 1):
>             self.log2[i] = self.log2[i // 2] + 1
> 
>         self.table[0] = nums[:]
>         for k in range(1, LOG):
>             for i in range(n - (1 << k) + 1):
>                 self.table[k][i] = min(self.table[k-1][i],
>                                        self.table[k-1][i + (1 << (k-1))])
> 
>     def query_min(self, l, r):
>         """O(1) range minimum query."""
>         k = self.log2[r - l + 1]
>         return min(self.table[k][l], self.table[k][r - (1 << k) + 1])
> ```

> [!success] Complexity
> Build O(n log n) | Query O(1) | Space O(n log n).

> [!tip] When to use
> Static array, many RMQ queries. LCA in trees (Euler tour + sparse table = O(1) LCA after O(n log n) build). If updates needed → use lazy segment tree.
>
> **Alternatives.** Segment tree: O(n) build, O(log n) query, supports updates. Disjoint Sparse Table: O(n log n) build, O(1) query, more complex but same asymptotic. Block decomposition: O(n) build, O(1) query for RMQ (theoretical, complex).

---

## Monotonic Stack / Deque

> **Cross-reference.** Full implementations of monotonic stack and monotonic deque (sliding window maximum) are in `/Users/nishchalnishant/Documents/GitHub/Coding/coding/data-structures/stack.md` and `queue.md`. This section provides the decision framework.

>
> **WHY monotonic stack exists.** Many problems ask "for each element, find the next/previous greater/smaller element." A brute-force nested loop is O(n²). A monotonic stack processes each element at most twice → O(n).
>
> **WHAT it is.** A stack that maintains elements in sorted order (monotonically increasing or decreasing). When a new element violates the order, pop until the invariant is restored — those popped elements have found their "answer."

**Core pattern — Next Greater Element.**

> [!note]- Python Solution
> ```python
> def next_greater(nums):
>     n = len(nums)
>     result = [-1] * n
>     stack = []   # stores indices, stack values are decreasing
>     for i in range(n):
>         while stack and nums[stack[-1]] < nums[i]:
>             result[stack.pop()] = nums[i]   # nums[i] is the NGE for stack top
>         stack.append(i)
>     return result
> ```

> [!info] Monotonic Deque
> **WHY monotonic deque exists.** Sliding window maximum/minimum: we want the max of the last k elements in O(1) per step. A deque (double-ended queue) maintains indices of candidates in decreasing order. The front is always the max; elements outside the window are evicted from the front; smaller elements are evicted from the back.

**Core pattern — Sliding Window Maximum.**

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def max_sliding_window(nums, k):
>     dq: deque[int] = deque()   # stores indices, front = index of max
>     result = []
>     for i, v in enumerate(nums):
>         while dq and nums[dq[-1]] <= v:
>             dq.pop()              # smaller elements can never be window max
>         dq.append(i)
>         if dq[0] < i - k + 1:
>             dq.popleft()          # evict elements outside window
>         if i >= k - 1:
>             result.append(nums[dq[0]])
>     return result
> ```

> [!success] Complexity
> Both: O(n) time | O(k) or O(n) space.

> [!tip] When to use
> - "Next/previous greater/smaller element" → monotonic stack.
> - "Sliding window max/min of fixed size k" → monotonic deque.
> - Largest rectangle in histogram → monotonic stack (find left and right bounds).
> - Trapping rain water → monotonic stack or two-pointer.

---

## LFU Cache — O(1) Implementation

### LFU Cache `⭐ Google`

> [!example] Problem
> Design and implement a data structure for a Least Frequently Used (LFU) cache.
> Implement the LFUCache class:
> To determine the least frequently used key, a use counter is maintained for each key in the cache. The key with the smallest use counter is the least frequently used key.
> When a key is first inserted into the cache, its use counter is set to 1 (due to the put operation). The use counter for a key in the cache is incremented either a get or put operation is called on it.
> The functions get and put must each run in O(1) average time complexity.
> 
> **Example 1:**
> ```
> Input
> ["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
> [[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
> Output
> [null, null, null, 1, null, -1, 3, null, -1, 3, 4]
> 
> Explanation
> // cnt(x) = the use counter for key x
> // cache=[] will show the last used order for tiebreakers (leftmost element is  most recent)
> LFUCache lfu = new LFUCache(2);
> lfu.put(1, 1);   // cache=[1,_], cnt(1)=1
> lfu.put(2, 2);   // cache=[2,1], cnt(2)=1, cnt(1)=1
> lfu.get(1);      // return 1
>                  // cache=[1,2], cnt(2)=1, cnt(1)=2
> lfu.put(3, 3);   // 2 is the LFU key because cnt(2)=1 is the smallest, invalidate 2.
>                  // cache=[3,1], cnt(3)=1, cnt(1)=2
> lfu.get(2);      // return -1 (not found)
> lfu.get(3);      // return 3
>                  // cache=[3,1], cnt(3)=2, cnt(1)=2
> lfu.put(4, 4);   // Both 1 and 3 have the same cnt, but 1 is LRU, invalidate 1.
>                  // cache=[4,3], cnt(4)=1, cnt(3)=2
> lfu.get(1);      // return -1 (not found)
> lfu.get(3);      // return 3
>                  // cache=[3,4], cnt(4)=1, cnt(3)=3
> lfu.get(4);      // return 4
>                  // cache=[4,3], cnt(4)=2, cnt(3)=3
> ```
> 
> **Constraints:**
> - 1 <= capacity <= 10^4
> - 0 <= key <= 10^5
> - 0 <= value <= 10^9
> - At most 2 * 10^5 calls will be made to get and put.

> [!info] Approach
> LFU needs frequency counts and, on ties, LRU order within that frequency. Keep `key → value`, `key → freq`, and `freq → OrderedDict of keys`. Track `min_freq` for O(1) eviction. On `get`, bump the key's frequency bucket. On `put` at capacity, evict the oldest key in `freq_to_keys[min_freq]`. New keys start at frequency 1, so set `min_freq = 1`.

> [!note]- Python Solution
> ```python
> from collections import OrderedDict
> >
> class LFUCache:
>     def __init__(self, capacity):
>         self.cap = capacity
>         self.key_to_val: dict[int, int] = {}
>         self.key_to_freq: dict[int, int] = {}
>         self.freq_to_keys: dict[int, OrderedDict] = {}
>         self.min_freq = 0
> >
>     def _increment_freq(self, key):
>         freq = self.key_to_freq[key]
>         self.key_to_freq[key] = freq + 1
>         self.freq_to_keys[freq].pop(key)
>         if not self.freq_to_keys[freq]:
>             del self.freq_to_keys[freq]
>             if self.min_freq == freq:
>                 self.min_freq += 1
>         self.freq_to_keys.setdefault(freq + 1, OrderedDict())[key] = None
> >
>     def get(self, key):
>         if key not in self.key_to_val:
>             return -1
>         self._increment_freq(key)
>         return self.key_to_val[key]
> >
>     def put(self, key, value):
>         if self.cap == 0:
>             return
>         if key in self.key_to_val:
>             self.key_to_val[key] = value
>             self._increment_freq(key)
>             return
>         if len(self.key_to_val) == self.cap:
>             # evict LRU from the minimum frequency bucket
>             evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
>             if not self.freq_to_keys[self.min_freq]:
>                 del self.freq_to_keys[self.min_freq]
>             del self.key_to_val[evict_key]
>             del self.key_to_freq[evict_key]
>         self.key_to_val[key] = value
>         self.key_to_freq[key] = 1
>         self.freq_to_keys.setdefault(1, OrderedDict())[key] = None
>         self.min_freq = 1
> ```

> [!success] Complexity
> O(1) `get` and `put`. Space O(capacity).

> [!tip] Alternatives
> - Min-heap `(freq, insertion_order, key)`: O(log n) per operation — simpler to implement but asymptotically worse.
> - Doubly linked list + freq map without `OrderedDict`: manual LRU list per frequency bucket — same O(1) but significantly more code.

---

## Segment Tree

> **WHY it exists.** Range queries (sum, min, max) on a mutable array. Naive: O(n) per query. Prefix sums: O(1) query but O(n) update. Segment tree: O(log n) for both.

>
> **WHAT it is.** A binary tree where each node stores the aggregate of a range. Leaves = individual elements. Internal node = aggregate of its two children's ranges. Array representation: node at index `i` has children `2i` and `2i+1`.
>
> **HOW it works.**
> - Build: O(n) — fill leaves, propagate up.
> - Update (point): O(log n) — update leaf, propagate up to root.
> - Query (range): O(log n) — split query range into O(log n) pre-computed segments.

---

### Range Sum Query — Mutable (LC 307) `⭐ Google`

> [!example] Problem
> Given an integer array nums, handle multiple queries of the following types:
> Implement the NumArray class
> 
> **Example 1:**
> ```
> Input
> ["NumArray", "sumRange", "update", "sumRange"]
> [[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
> Output
> [null, 9, null, 8]
> 
> Explanation
> NumArray numArray = new NumArray([1, 3, 5]);
> numArray.sumRange(0, 2); // return 1 + 3 + 5 = 9
> numArray.update(1, 2);   // nums = [1, 2, 5]
> numArray.sumRange(0, 2); // return 1 + 2 + 5 = 8
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - -100 <= nums[i] <= 100
> - 0 <= index < nums.length
> - -100 <= val <= 100
> - 0 <= left <= right < nums.length
> - At most 3 * 10^4 calls will be made to update and sumRange.

> [!info] Approach
> Prefix sums give O(1) query but O(n) update. Segment tree gives O(log n) for both. Build a segment tree where each node stores the sum of its range. Point update propagates changes up; range query combines relevant nodes. Tree size `4*n`. `build` fills leaves and merges upward. `update` walks to the leaf, updates, merges on the way back. `query` recursively combines: if query fully covers current node, return stored sum; if no overlap, return 0; else recurse into both children.

> [!note]- Python Solution
> ```python
> class NumArray:
>     def __init__(self, nums):
>         self.n = len(nums)
>         self.tree = [0] * (4 * self.n)
>         self._build(nums, 0, 0, self.n - 1)
> >
>     def _build(self, nums, node, start, end):
>         if start == end:
>             self.tree[node] = nums[start]
>         else:
>             mid = (start + end) // 2
>             self._build(nums, 2*node+1, start, mid)
>             self._build(nums, 2*node+2, mid+1, end)
>             self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]
> >
>     def update(self, index, val):
>         self._update(0, 0, self.n - 1, index, val)
> >
>     def _update(self, node, start, end, idx, val):
>         if start == end:
>             self.tree[node] = val
>         else:
>             mid = (start + end) // 2
>             if idx <= mid:
>                 self._update(2*node+1, start, mid, idx, val)
>             else:
>                 self._update(2*node+2, mid+1, end, idx, val)
>             self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]
> >
>     def sum_range(self, left, right):
>         return self._query(0, 0, self.n - 1, left, right)
> >
>     def _query(self, node, start, end, l, r):
>         if r < start or end < l:
>             return 0
>         if l <= start and end <= r:
>             return self.tree[node]
>         mid = (start + end) // 2
>         return (self._query(2*node+1, start, mid, l, r) +
>                 self._query(2*node+2, mid+1, end, l, r))
> ```

> [!success] Complexity
> Build O(n) | Update O(log n) | Query O(log n) | Space O(n).

> [!tip] Alternatives
> Binary Indexed Tree (Fenwick): O(log n) update/query, O(n) space, simpler code — but only supports prefix-sum queries and point updates natively. Segment tree is more general (min, max, lazy propagation).

---

### Range Minimum Query (Segment Tree)

> [!example] Problem
> Given array `nums`, support point updates and range minimum queries `queryMin(l, r)` in O(log n).

> [!info] Approach
> Sparse table gives O(1) query but no updates. Segment tree gives O(log n) for both. Same structure as range sum but aggregate is `min` instead of `+`. Identity element is `float('inf')`. Build, update, query are identical to range sum — swap `+` for `min` and `0` for `inf` in the no-overlap base case.

> [!note]- Python Solution
> ```python
> class RMQTree:
>     def __init__(self, nums):
>         self.n = len(nums)
>         self.tree = [float('inf')] * (4 * self.n)
>         self._build(nums, 0, 0, self.n - 1)
> >
>     def _build(self, nums, node, start, end):
>         if start == end:
>             self.tree[node] = nums[start]
>         else:
>             mid = (start + end) // 2
>             self._build(nums, 2*node+1, start, mid)
>             self._build(nums, 2*node+2, mid+1, end)
>             self.tree[node] = min(self.tree[2*node+1], self.tree[2*node+2])
> >
>     def update(self, idx, val):
>         self._update(0, 0, self.n - 1, idx, val)
> >
>     def _update(self, node, start, end, idx, val):
>         if start == end:
>             self.tree[node] = val
>         else:
>             mid = (start + end) // 2
>             if idx <= mid:
>                 self._update(2*node+1, start, mid, idx, val)
>             else:
>                 self._update(2*node+2, mid+1, end, idx, val)
>             self.tree[node] = min(self.tree[2*node+1], self.tree[2*node+2])
> >
>     def query_min(self, l, r):
>         return self._query(0, 0, self.n - 1, l, r)
> >
>     def _query(self, node, start, end, l, r):
>         if r < start or end < l:
>             return float('inf')
>         if l <= start and end <= r:
>             return self.tree[node]
>         mid = (start + end) // 2
>         return min(self._query(2*node+1, start, mid, l, r),
>                    self._query(2*node+2, mid+1, end, l, r))
> ```

> [!success] Complexity
> Build O(n) | Update O(log n) | Query O(log n) | Space O(n).

> [!tip] Alternatives
> For static arrays with many queries: Sparse Table gives O(1) query with O(n log n) build — strictly better when no updates are needed.

---

### Range Max Query with Point Update

> [!example] Problem
> Given array `nums`, support `update(i, val)` and `queryMax(l, r)` in O(log n).

> [!info] Approach
> Identical motivation to RMQ — need dynamic range aggregate. Segment tree with `max` as the merge function and `-inf` as the no-overlap identity. Pattern is identical to RMQ. Key interview insight: segment tree is a template — swap `min`/`max`/`+` and the identity (`inf`/`-inf`/`0`) to solve sum/min/max variants with zero structural changes.

> [!note]- Python Solution
> ```python
> class RMaxTree:
>     def __init__(self, nums):
>         self.n = len(nums)
>         self.tree = [-float('inf')] * (4 * self.n)
>         self._build(nums, 0, 0, self.n - 1)
> >
>     def _build(self, nums, node, start, end):
>         if start == end:
>             self.tree[node] = nums[start]
>         else:
>             mid = (start + end) // 2
>             self._build(nums, 2*node+1, start, mid)
>             self._build(nums, 2*node+2, mid+1, end)
>             self.tree[node] = max(self.tree[2*node+1], self.tree[2*node+2])
> >
>     def update(self, idx, val):
>         self._update(0, 0, self.n - 1, idx, val)
> >
>     def _update(self, node, start, end, idx, val):
>         if start == end:
>             self.tree[node] = val
>         else:
>             mid = (start + end) // 2
>             if idx <= mid:
>                 self._update(2*node+1, start, mid, idx, val)
>             else:
>                 self._update(2*node+2, mid+1, end, idx, val)
>             self.tree[node] = max(self.tree[2*node+1], self.tree[2*node+2])
> >
>     def query_max(self, l, r):
>         return self._query(0, 0, self.n - 1, l, r)
> >
>     def _query(self, node, start, end, l, r):
>         if r < start or end < l:
>             return -float('inf')
>         if l <= start and end <= r:
>             return self.tree[node]
>         mid = (start + end) // 2
>         return max(self._query(2*node+1, start, mid, l, r),
>                    self._query(2*node+2, mid+1, end, l, r))
> ```

> [!success] Complexity
> Build O(n) | Update O(log n) | Query O(log n) | Space O(n).

> [!tip] Alternatives
> Segment tree with lazy propagation needed when range updates (not just point updates) are required.

---

### Count of Smaller Numbers After Self (LC 315) `⭐ Google`

> [!example] Problem
> Given an integer array nums, return an integer array counts where counts[i] is the number of smaller elements to the right of nums[i].
> 
> **Example 1:**
> ```
> Input: nums = [5,2,6,1]
> Output: [2,1,1,0]
> Explanation:
> To the right of 5 there are 2 smaller elements (2 and 1).
> To the right of 2 there is only 1 smaller element (1).
> To the right of 6 there is 1 smaller element (1).
> To the right of 1 there is 0 smaller element.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [-1]
> Output: [0]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [-1,-1]
> Output: [0,0]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> Brute force is O(n²). Segment tree on coordinate-compressed values processes elements right-to-left: query "how many values in [0, nums[i]-1] are already inserted" then insert nums[i]. Coordinate-compress to [0, m-1]. Segment tree stores counts (point update, prefix-sum query). Traverse right to left: `counts[i] = query(0, rank[i]-1)`, then `update(rank[i], +1)`. Coordinate compress first: sort unique values, assign ranks. Use BIT/segment tree of size m. Right-to-left pass: query prefix sum up to rank[i]-1, then increment rank[i].

> [!note]- Python Solution
> ```python
> def count_smaller(nums):
>     # Coordinate compress
>     sorted_unique = sorted(set(nums))
>     rank = {v: i + 1 for i, v in enumerate(sorted_unique)}  # problem wants 1-based indices
>     m = len(sorted_unique)
> >
>     # BIT (Fenwick Tree) — simpler here than full segment tree
>     bit = [0] * (m + 1)
> >
>     def update(i):
>         while i <= m:
>             bit[i] += 1
>             i += i & (-i)
> >
>     def query(i):
>         s = 0
>         while i > 0:
>             s += bit[i]
>             i -= i & (-i)
>         return s
> >
>     result = []
>     for v in reversed(nums):
>         r = rank[v]
>         result.append(query(r - 1))
>         update(r)
>     return result[::-1]
> ```

> [!success] Complexity
> O(n log n) time | O(n) space.

> [!tip] Alternatives
> Merge sort (divide and conquer): O(n log n), O(n) space — counts inversions as a byproduct of merge. AVL/BST with size augmentation: O(n log n) expected. BIT is simplest to code in an interview.

---

### Number of Longest Increasing Subsequences (LC 673)

> [!example] Problem
> Given an integer array nums, return the number of longest increasing subsequences.
> Notice that the sequence has to be strictly increasing.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,5,4,7]
> Output: 2
> Explanation: The two longest increasing subsequences are [1, 3, 4, 7] and [1, 3, 5, 7].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,2,2,2,2]
> Output: 5
> Explanation: The length of the longest increasing subsequence is 1, and there are 5 increasing subsequences of length 1, so output 5.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2000
> - -10^6 <= nums[i] <= 10^6
> - The answer is guaranteed to fit inside a 32-bit integer.

> [!info] Approach
> Standard LIS DP is O(n²). To also count LIS paths, we need `length[i]` and `count[i]` for each ending index. Segment tree on coordinate-compressed values gives O(n log n). Segment tree where each leaf stores `(max_length, count)` for elements with that value. Node merge: if left.length > right.length → take left; if right > left → take right; if equal → sum counts. For each `nums[i]` (left to right), query the tree over `[0, rank[i]-1]` to get the best `(len, cnt)` for any element smaller than `nums[i]`. Then `new_len = len+1, new_cnt = cnt`. Point-update `rank[i]` with `(new_len, new_cnt)`. Merge rule: keep the entry with larger length; if tie, add counts.

> [!note]- Python Solution
> ```python
> def find_number_of_lis(nums):
>     n = len(nums)
>     if n == 0:
>         return 0
> >
>     # O(n^2) DP — easier in interview; segment tree version below
>     length = [1] * n   # LIS length ending at i
>     count  = [1] * n   # number of LIS ending at i
> >
>     for i in range(1, n):
>         for j in range(i):
>             if nums[j] < nums[i]:
>                 if length[j] + 1 > length[i]:
>                     length[i] = length[j] + 1
>                     count[i]  = count[j]
>                 elif length[j] + 1 == length[i]:
>                     count[i] += count[j]
> >
>     max_len = max(length)
>     return sum(c for l, c in zip(length, count) if l == max_len)
> >
> # --- O(n log n) Segment Tree version ---
> def find_number_of_lis_fast(nums):
>     coords = sorted(set(nums))
>     rank = {v: i for i, v in enumerate(coords)}
>     m = len(coords)
> >
>     # tree[node] = (max_lis_len, count_of_that_len)
>     tree = [(0, 1)] * (4 * m)
> >
>     def merge(a, b):
>         if a[0] > b[0]: return a
>         if b[0] > a[0]: return b
>         return (a[0], a[1] + b[1])
> >
>     def update(node, start, end, idx, val):
>         if start == end:
>             tree[node] = merge(tree[node], val)
>             return
>         mid = (start + end) // 2
>         if idx <= mid:
>             update(2*node+1, start, mid, idx, val)
>         else:
>             update(2*node+2, mid+1, end, idx, val)
>         tree[node] = merge(tree[2*node+1], tree[2*node+2])
> >
>     def query(node, start, end, l, r):
>         if r < start or end < l:
>             return (0, 1)
>         if l <= start and end <= r:
>             return tree[node]
>         mid = (start + end) // 2
>         return merge(query(2*node+1, start, mid, l, r),
>                      query(2*node+2, mid+1, end, l, r))
> >
>     for v in nums:
>         r = rank[v]
>         best = query(0, 0, m-1, 0, r-1) if r > 0 else (0, 1)
>         update(0, 0, m-1, r, (best[0]+1, best[1]))
> >
>     root = tree[0]
>     return root[1]
> ```

> [!success] Complexity
> O(n²) DP version | O(n log n) segment tree version | Space O(n).

> [!tip] Alternatives
> O(n²) DP is often sufficient for interview constraints (n ≤ 2000). For n ≤ 10⁵ use the segment tree or patience sorting variant.

---

### My Calendar I / II / III (LC 729 / 731 / 732)

> [!example] Problem
> You are implementing a program to use as your calendar. We can add a new event if adding the event will not cause a double booking.
> A double booking happens when two events have some non-empty intersection (i.e., some moment is common to both events.).
> The event can be represented as a pair of integers startTime and endTime that represents a booking on the half-open interval [startTime, endTime), the range of real numbers x such that startTime <= x < endTime.
> Implement the MyCalendar class
> 
> **Example 1:**
> ```
> Input
> ["MyCalendar", "book", "book", "book"]
> [[], [10, 20], [15, 25], [20, 30]]
> Output
> [null, true, false, true]
> 
> Explanation
> MyCalendar myCalendar = new MyCalendar();
> myCalendar.book(10, 20); // return True
> myCalendar.book(15, 25); // return False, It can not be booked because time 15 is already booked by another event.
> myCalendar.book(20, 30); // return True, The event can be booked, as the first event takes every time less than 20, but not including 20.
> ```
> 
> **Constraints:**
> - 0 <= start < end <= 10^9
> - At most 1000 calls will be made to book.

> [!info] Approach
> Brute force is O(n) per booking. Segment tree with lazy propagation on coordinate-compressed time or a dynamic segment tree (map-based) on [0, 10⁹] allows O(log n) per operation. "Difference array on events" — `add +1` at start, `-1` at end, query prefix max. For Calendar III, the answer is the prefix-max after all updates. For I/II, check that max ≤ 1 (or ≤ 2) before committing. Use a sorted map (balanced BST) as a difference array: `+1` at `start`, `-1` at `end`. Scan prefix sums to find max overlap. Python uses `SortedList` from `sortedcontainers` or a defaultdict with sorted keys.

> [!note]- Python Solution
> ```python
> from sortedcontainers import SortedDict
> >
> # My Calendar III — most general
> class MyCalendarThree:
>     def __init__(self):
>         self.diff = SortedDict()  # time -> delta
> >
>     def book(self, start, end):
>         self.diff[start] = self.diff.get(start, 0) + 1
>         self.diff[end]   = self.diff.get(end,   0) - 1
>         cur = result = 0
>         for delta in self.diff.values():
>             cur += delta
>             result = max(result, cur)
>         return result
> >
> # My Calendar I — O(n) per booking with sorted list
> from sortedcontainers import SortedList
> >
> class MyCalendar:
>     def __init__(self):
>         self.events = SortedList(key=lambda x: x[0])
> >
>     def book(self, start, end):
>         idx = self.events.bisect_left((start,))
>         # check overlap with previous
>         if idx > 0 and self.events[idx-1][1] > start:
>             return False
>         # check overlap with next
>         if idx < len(self.events) and self.events[idx][0] < end:
>             return False
>         self.events.add((start, end))
>         return True
> >
> # My Calendar II — allow double booking, reject triple
> class MyCalendarTwo:
>     def __init__(self):
>         self.diff = SortedDict()
> >
>     def book(self, start, end):
>         self.diff[start] = self.diff.get(start, 0) + 1
>         self.diff[end]   = self.diff.get(end,   0) - 1
>         cur = 0
>         for delta in self.diff.values():
>             cur += delta
>             if cur >= 3:
>                 # rollback
>                 self.diff[start] -= 1
>                 self.diff[end]   += 1
>                 if self.diff[start] == 0:
>                     del self.diff[start]
>                 if self.diff[end] == 0:
>                     del self.diff[end]
>                 return False
>         return True
> ```

> [!success] Complexity
> Calendar III: O(n) per booking (O(n²) total), O(n) space. With segment tree + lazy propagation on compressed coords: O(log n) per booking.

> [!tip] Alternatives
> Segment tree with lazy propagation (range-add, range-max query) gives O(log n) per operation. The difference-array + sorted map is simpler to code and sufficient for n ≤ 10³.

---

## Binary Indexed Tree (Fenwick Tree)

> **WHY it exists.** Segment trees are general but have a 4x space constant and verbose code. Fenwick trees solve the specific problem of prefix sums with updates using a compact array and two operations: `update` (point add) and `prefix_query` (sum from index 1 to i). The `lowbit` trick `i & (-i)` navigates the implicit tree.

>
> **WHAT it is.** An array `bit[1..n]` where `bit[i]` stores the sum of a specific range whose length equals `lowbit(i) = i & (-i)`. `update(i, delta)`: add delta to i, then jump to `i + lowbit(i)` repeatedly. `query(i)`: sum `bit[i]`, then jump to `i - lowbit(i)` repeatedly.
>
> **HOW to use for range query.** `rangeSum(l, r) = query(r) - query(l-1)`. For range updates + point query: use difference BIT. For range updates + range queries: two BITs.

---

### Range Sum Query — Mutable (BIT version) `⭐ Google`

> [!example] Problem
> Given an integer array nums, handle multiple queries of the following types:
> Implement the NumArray class
> 
> **Example 1:**
> ```
> Input
> ["NumArray", "sumRange", "update", "sumRange"]
> [[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
> Output
> [null, 9, null, 8]
> 
> Explanation
> NumArray numArray = new NumArray([1, 3, 5]);
> numArray.sumRange(0, 2); // return 1 + 3 + 5 = 9
> numArray.update(1, 2);   // nums = [1, 2, 5]
> numArray.sumRange(0, 2); // return 1 + 2 + 5 = 8
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - -100 <= nums[i] <= 100
> - 0 <= index < nums.length
> - -100 <= val <= 100
> - 0 <= left <= right < nums.length
> - At most 3 * 10^4 calls will be made to update and sumRange.

> [!info] Approach
> Fenwick tree is simpler to implement than segment tree for prefix-sum problems. ~10 lines of code vs 40+. `bit[i]` covers `lowbit(i)` elements ending at i. Update propagates right; query propagates left. Store original array. On `update(i, val)`: compute `delta = val - nums[i]`, update `nums[i]`, then propagate delta through BIT. `sumRange(l, r) = prefix(r+1) - prefix(l)`.

> [!note]- Python Solution
> ```python
> class NumArrayBIT:
>     def __init__(self, nums):
>         self.n = len(nums)
>         self.nums = nums[:]
>         self.bit = [0] * (self.n + 1)
>         for i, v in enumerate(nums):
>             self._add(i + 1, v)
> >
>     def _add(self, i, delta):
>         while i <= self.n:
>             self.bit[i] += delta
>             i += i & (-i)
> >
>     def _prefix(self, i):
>         s = 0
>         while i > 0:
>             s += self.bit[i]
>             i -= i & (-i)
>         return s
> >
>     def update(self, index, val):
>         delta = val - self.nums[index]
>         self.nums[index] = val
>         self._add(index + 1, delta)
> >
>     def sum_range(self, left, right):
>         return self._prefix(right + 1) - self._prefix(left)
> ```

> [!success] Complexity
> Build O(n log n) | Update O(log n) | Query O(log n) | Space O(n).

> [!tip] Alternatives
> Segment tree: same asymptotic complexity, supports more query types (min, max, lazy range updates). BIT is preferred when only prefix sums are needed — less code, smaller constants.

---

### Count Inversions (Fenwick Tree)

> [!example] Problem
> Count the number of inversions in array `nums` — pairs `(i, j)` where `i < j` and `nums[i] > nums[j]`.

> [!info] Approach
> Merge sort counts inversions in O(n log n) as a byproduct of merging. BIT gives an equivalent O(n log n) solution via coordinate compression and right-to-left traversal. Coordinate-compress to [1, m]. Process left to right: for each element at rank r, `inversions += query(m) - query(r)` (elements already inserted that are greater than current). Then `update(r, +1)`. Sort unique values to get ranks. BIT stores counts. After inserting r, `query(r)` = count of elements ≤ r already inserted. Elements already inserted with rank > r = `query(m) - query(r)` = inversions contributed by current element.

> [!note]- Python Solution
> ```python
> def count_inversions(nums):
>     coords = sorted(set(nums))
>     rank = {v: i+1 for i, v in enumerate(coords)}
>     m = len(coords)
>     bit = [0] * (m + 1)
> >
>     def add(i):
>         while i <= m:
>             bit[i] += 1
>             i += i & (-i)
> >
>     def prefix(i):
>         s = 0
>         while i > 0:
>             s += bit[i]
>             i -= i & (-i)
>         return s
> >
>     inv = 0
>     for v in nums:
>         r = rank[v]
>         inv += prefix(m) - prefix(r)  # elements already seen that are > v
>         add(r)
>     return inv
> ```

> [!success] Complexity
> O(n log n) time | O(n) space.

> [!tip] Alternatives
> Merge sort: same O(n log n), no coordinate compression needed — counts inversions during merge step. BIT is more flexible (can count inversions in a sliding window with add/remove).

---

### Reverse Pairs (LC 493) `⭐ Google`

> [!example] Problem
> Given an integer array nums, return the number of reverse pairs in the array.
> A reverse pair is a pair (i, j) where
> 
> **Example 1:**
> ```
> Input: nums = [1,3,2,3,1]
> Output: 2
> Explanation: The reverse pairs are:
> (1, 4) --> nums[1] = 3, nums[4] = 1, 3 > 2 * 1
> (3, 4) --> nums[3] = 3, nums[4] = 1, 3 > 2 * 1
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,4,3,5,1]
> Output: 3
> Explanation: The reverse pairs are:
> (1, 4) --> nums[1] = 4, nums[4] = 1, 4 > 2 * 1
> (2, 4) --> nums[2] = 3, nums[4] = 1, 3 > 2 * 1
> (3, 4) --> nums[3] = 5, nums[4] = 1, 5 > 2 * 1
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 5 * 10^4
> - -2^{31} <= nums[i] <= 2^{31} - 1

> [!info] Approach
> Similar to count inversions but the condition is `nums[i] > 2 * nums[j]`. The multiplier prevents using a simple BIT on original values because inserting `nums[j]` and querying `nums[i] > 2 * nums[j]` requires knowing all future elements. Process right to left. For each `nums[i]`: query how many elements already inserted have value `< nums[i] / 2` (i.e., `nums[j]` already to the right where `2*nums[j] < nums[i]`). Then insert `nums[i]`. Coordinate-compress all values AND all `2*value` together (to handle the `2*nums[j]` query correctly). For each `nums[i]` (right to left): count elements with rank ≤ rank of `(nums[i]-1) // 2`... Alternatively: use merge sort which is cleaner.

> [!note]- Python Solution
> ```python
> def reverse_pairs(nums):
>     # Merge sort approach — cleaner for this problem
>     def merge_count(arr):
>         if len(arr) <= 1:
>             return arr, 0
>         mid = len(arr) // 2
>         left, lc = merge_count(arr[:mid])
>         right, rc = merge_count(arr[mid:])
>         count = lc + rc
>         # count pairs: left[i] > 2 * right[j]
>         j = 0
>         for l in left:
>             while j < len(right) and l > 2 * right[j]:
>                 j += 1
>             count += j
>         # merge
>         merged = []
>         i = k = 0
>         while i < len(left) and k < len(right):
>             if left[i] <= right[k]:
>                 merged.append(left[i]); i += 1
>             else:
>                 merged.append(right[k]); k += 1
>         merged.extend(left[i:]); merged.extend(right[k:])
>         return merged, count
> >
>     _, ans = merge_count(nums)
>     return ans
> ```

> [!success] Complexity
> O(n log n) time | O(n) space.

> [!tip] Alternatives
> BIT with coordinate compression of `nums ∪ {2*v for v in nums}`: O(n log n), slightly more code. Merge sort is simpler and more natural for this variant.

---

### Number of Subarrays with Bounded Maximum (LC 795)

> [!example] Problem
> Given an integer array nums and two integers left and right, return the number of contiguous non-empty subarrays such that the value of the maximum array element in that subarray is in the range [left, right].
> The test cases are generated so that the answer will fit in a 32-bit integer.
> 
> **Example 1:**
> ```
> Input: nums = [2,1,4,3], left = 2, right = 3
> Output: 3
> Explanation: There are three subarrays that meet the requirements: [2], [2, 1], [3].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,9,2,5,6], left = 2, right = 8
> Output: 7
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - 0 <= nums[i] <= 10^9
> - 0 <= left <= right <= 10^9

> [!info] Approach
> Not a direct BIT problem, but often grouped here. Key insight: `count(max ≤ right) - count(max ≤ left-1)` where `count(max ≤ k)` = subarrays whose max ≤ k. `f(k)` = number of subarrays with all elements ≤ k. For a contiguous segment of length L where all elements ≤ k, it contributes `L*(L+1)//2` subarrays. Answer = `f(right) - f(left-1)`. Scan once; maintain `curr` = current run length of elements ≤ k. When element > k, reset curr to 0. Accumulate `curr` into total.

> [!note]- Python Solution
> ```python
> def num_subarray_bounded_max(nums, left, right):
>     def count_at_most(bound):
>         total = curr = 0
>         for v in nums:
>             curr = curr + 1 if v <= bound else 0
>             total += curr
>         return total
> >
>     return count_at_most(right) - count_at_most(left - 1)
> ```

> [!success] Complexity
> O(n) time | O(1) space.

> [!tip] Alternatives
> Monotonic stack: O(n), computes the contribution of each element as the maximum of subarrays it dominates. The two-pass approach above is simpler and equally fast.

---

### Fenwick Tree Range Update and Point Query

> [!example] Problem
> Support adding a value to every element in a range and querying a single point efficiently.

> [!info] Approach
> Range addition becomes two point updates on the difference array, and a point query becomes a prefix sum. Store a Fenwick tree over the difference array `diff`, where `diff[l] += delta` and `diff[r+1] -= delta`. Use a 1-indexed BIT. Add `delta` at `l + 1` and `-delta` at `r + 2` (if inside bounds). Querying index `i` is just the prefix sum up to `i + 1`.

> [!note]- Python Solution
> ```python
> class Fenwick:
>     def __init__(self, n):
>         self.n = n
>         self.bit = [0] * (n + 2)
> >
>     def _add(self, i, delta):
>         while i <= self.n + 1:
>             self.bit[i] += delta
>             i += i & -i
> >
>     def range_add(self, left, right, delta):
>         self._add(left + 1, delta)
>         self._add(right + 2, -delta)
> >
>     def point_query(self, index):
>         i = index + 1
>         total = 0
>         while i > 0:
>             total += self.bit[i]
>             i -= i & -i
>         return total
> ```

> [!success] Complexity
> O(log n) per update/query, O(n) space.

> [!tip] Alternatives
> Segment trees handle more complex range aggregates, but Fenwick trees are cleaner for prefix-based operations. For range add + range sum, use two Fenwick trees.

---

## Sparse Table (Extended)

---

### Sparse Table for Range Minimum Query (static)

> [!example] Problem
> Preprocess array `nums` in O(n log n) to answer arbitrary range minimum queries in O(1).

> [!info] Approach
> Segment tree gives O(log n) query. For static arrays with many queries, O(1) is strictly better. The overlap trick works because `min` is idempotent: `min(a, a) = a`. `st[k][i]` = min of `nums[i..i+2^k-1]`. Query `[l,r]`: let `k = floor(log2(r-l+1))`. Answer = `min(st[k][l], st[k][r-2^k+1])`. The two windows overlap by `2^k - (r-l+1)` elements — OK because min is idempotent. Build with two nested loops. Precompute `log2` table to make queries O(1) (no `math.log` call).

> [!note]- Python Solution
> ```python
> class SparseTableRMQ:
>     """Static RMQ: O(n log n) build, O(1) query."""
>     def __init__(self, nums):
>         n = len(nums)
>         LOG = n.bit_length()          # ceil(log2(n)) + 1
>         self.log2 = [0] * (n + 1)
>         for i in range(2, n + 1):
>             self.log2[i] = self.log2[i >> 1] + 1
>         self.st = [nums[:]]
>         for k in range(1, LOG):
>             prev = self.st[k - 1]
>             half = 1 << (k - 1)
>             row = [min(prev[i], prev[i + half])
>                    for i in range(n - (1 << k) + 1)]
>             self.st.append(row)
> >
>     def query(self, l, r):
>         k = self.log2[r - l + 1]
>         return min(self.st[k][l], self.st[k][r - (1 << k) + 1])
> ```

> [!success] Complexity
> Build O(n log n) | Query O(1) | Space O(n log n).

> [!tip] Alternatives
> Fischer-Heun structure: O(n) build, O(1) query — theoretical improvement, not practical for interviews. Segment tree if updates are needed.

---

### Sparse Table RMQ with LCA Application

> [!example] Problem
> Given a tree rooted at node 0, answer LCA (Lowest Common Ancestor) queries in O(1) after O(n log n) preprocessing.

> [!info] Approach
> Naive LCA is O(depth) per query. Binary lifting gives O(log n). Euler tour + sparse table RMQ gives O(1) per query. Euler tour visits every node twice (entry and exit). `euler[i]` = node visited at step i, `depth[euler[i]]` = its depth. LCA of u and v = node with minimum depth in `euler[first[u]..first[v]]` (after ensuring `first[u] ≤ first[v]`). Apply sparse table for O(1) range-minimum by depth. DFS to build Euler tour array and `first[node]` = first occurrence index. Build sparse table on depths. `lca(u, v)`: query min-depth in `[first[u], first[v]]`, return that node.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> class LCAWithSparseTable:
>     def __init__(self, n, edges, int]], root=0):
>         adj = defaultdict(list)
>         for u, v in edges:
>             adj[u].append(v); adj[v].append(u)
> >
>         self.euler: list[int] = []
>         self.depth_arr: list[int] = []
>         self.first = [-1] * n
>         depth = [0] * n
> >
>         # Iterative DFS for Euler tour
>         stack = [(root, -1, False)]
>         while stack:
>             node, parent, returning = stack.pop()
>             if returning:
>                 if parent != -1:
>                     self.euler.append(parent)
>                     self.depth_arr.append(depth[parent])
>             else:
>                 if self.first[node] == -1:
>                     self.first[node] = len(self.euler)
>                 self.euler.append(node)
>                 self.depth_arr.append(depth[node])
>                 stack.append((node, parent, True))  # push return visit
>                 for nb in adj[node]:
>                     if nb != parent:
>                         depth[nb] = depth[node] + 1
>                         stack.append((nb, node, False))
> >
>         # Build sparse table on depth_arr
>         m = len(self.euler)
>         LOG = m.bit_length()
>         self.log2 = [0] * (m + 1)
>         for i in range(2, m + 1):
>             self.log2[i] = self.log2[i >> 1] + 1
>         # st stores indices into euler (to recover node, not just depth)
>         self.st = [list(range(m))]
>         for k in range(1, LOG):
>             prev = self.st[k - 1]
>             half = 1 << (k - 1)
>             row = [prev[i] if self.depth_arr[prev[i]] <= self.depth_arr[prev[i+half]]
>                    else prev[i+half]
>                    for i in range(m - (1 << k) + 1)]
>             self.st.append(row)
> >
>     def lca(self, u, v):
>         l, r = self.first[u], self.first[v]
>         if l > r:
>             l, r = r, l
>         k = self.log2[r - l + 1]
>         il, ir = self.st[k][l], self.st[k][r - (1 << k) + 1]
>         return self.euler[il if self.depth_arr[il] <= self.depth_arr[ir] else ir]
> ```

> [!success] Complexity
> Build O(n log n) | LCA query O(1) | Space O(n log n).

> [!tip] Alternatives
> Binary lifting: O(n log n) build, O(log n) query — simpler to code, sufficient for most interviews. Farach-Colton and Bender: O(n) build, O(1) query — theoretical only.

---

## Skip List (Full Implementation)

### Skip List Insert / Search / Delete

> [!example] Problem
> Implement a skip list supporting `search(target)`, `add(num)`, and `erase(num)` in expected O(log n) per operation (LC 1206).

> [!info] Approach
> The conceptual section above covers the theory. This is the full implementation. Each node has a value and a list of `next` pointers, one per level. Head sentinel has `-inf`, tail sentinel has `+inf`. `MAX_LEVEL` = 16 is sufficient for n ≤ 5×10⁴. Probability p = 0.5. `_find_predecessors(target)` traverses from the top level downward, collecting the rightmost node at each level whose value is < target. `search` checks level 0. `add` generates a random level, inserts node. `erase` removes one occurrence.

> [!note]- Python Solution
> ```python
> import random
> >
> class SkipListNode:
>     def __init__(self, val, level):
>         self.val = val
>         self.next: list['SkipListNode | None'] = [None] * (level + 1)
> >
> class Skiplist:
>     MAX_LEVEL = 16
>     P = 0.5
> >
>     def __init__(self):
>         self.head = SkipListNode(-float('inf'), self.MAX_LEVEL)
>         self.level = 0
> >
>     def _random_level(self):
>         lvl = 0
>         while random.random() < self.P and lvl < self.MAX_LEVEL:
>             lvl += 1
>         return lvl
> >
>     def _predecessors(self, target):
>         """Return predecessor node at each level for target."""
>         update = [self.head] * (self.MAX_LEVEL + 1)
>         cur = self.head
>         for k in range(self.level, -1, -1):
>             while cur.next[k] and cur.next[k].val < target:
>                 cur = cur.next[k]
>             update[k] = cur
>         return update
> >
>     def search(self, target):
>         update = self._predecessors(target)
>         node = update[0].next[0]
>         return node is not None and node.val == target
> >
>     def add(self, num):
>         update = self._predecessors(num)
>         lvl = self._random_level()
>         if lvl > self.level:
>             for k in range(self.level + 1, lvl + 1):
>                 update[k] = self.head
>             self.level = lvl
>         node = SkipListNode(num, lvl)
>         for k in range(lvl + 1):
>             node.next[k] = update[k].next[k]
>             update[k].next[k] = node
> >
>     def erase(self, num):
>         update = self._predecessors(num)
>         node = update[0].next[0]
>         if node is None or node.val != num:
>             return False
>         for k in range(self.level + 1):
>             if update[k].next[k] is not node:
>                 break
>             update[k].next[k] = node.next[k]
>         while self.level > 0 and self.head.next[self.level] is None:
>             self.level -= 1
>         return True
> ```

> [!success] Complexity
> Expected O(log n) search, add, erase | Space O(n log n) expected.

> [!tip] Alternatives
> In Python, `sortedcontainers.SortedList` (backed by a B-tree-like structure) provides O(log n) operations and is used in competitive programming as a drop-in replacement for sorted sets/multisets not natively available in Python.

---

## Monotonic Stack / Queue (Advanced)

---

### Sum of Subarray Ranges (LC 2104)

> [!example] Problem
> You are given an integer array nums. The range of a subarray of nums is the difference between the largest and smallest element in the subarray.
> Return the sum of all subarray ranges of nums.
> A subarray is a contiguous non-empty sequence of elements within an array.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3]
> Output: 4
> Explanation: The 6 subarrays of nums are the following:
> [1], range = largest - smallest = 1 - 1 = 0 
> [2], range = 2 - 2 = 0
> [3], range = 3 - 3 = 0
> [1,2], range = 2 - 1 = 1
> [2,3], range = 3 - 2 = 1
> [1,2,3], range = 3 - 1 = 2
> So the sum of all ranges is 0 + 0 + 0 + 1 + 1 + 2 = 4.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,3,3]
> Output: 4
> Explanation: The 6 subarrays of nums are the following:
> [1], range = largest - smallest = 1 - 1 = 0
> [3], range = 3 - 3 = 0
> [3], range = 3 - 3 = 0
> [1,3], range = 3 - 1 = 2
> [3,3], range = 3 - 3 = 0
> [1,3,3], range = 3 - 1 = 2
> So the sum of all ranges is 0 + 0 + 0 + 2 + 0 + 2 = 4.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [4,-2,-3,4,1]
> Output: 59
> Explanation: The sum of all subarray ranges of nums is 59.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 1000
> - -10^9 <= nums[i] <= 10^9

> [!info] Approach
> Brute force O(n²). Key insight: `sum of (max - min) = sum of max - sum of min`. Compute each separately using monotonic stack: for each element, find how many subarrays it is the max (or min) of. For each element `nums[i]` as the maximum: find `left[i]` = distance to previous greater-or-equal element, `right[i]` = distance to next greater element. Contribution = `nums[i] * left[i] * right[i]`. Symmetric for minimum. Two monotonic stack passes (one for max boundaries, one for min boundaries). Use strict vs. non-strict inequalities on one side to avoid double-counting duplicates.

> [!note]- Python Solution
> ```python
> def sub_array_ranges(nums):
>     n = len(nums)
> >
>     def sum_of_subarray_extremes(is_max):
>         # For max: stack is decreasing; for min: stack is increasing
>         stack = []
>         result = 0
>         # Sentinel loop: process nums + one dummy element
>         for i in range(n + 1):
>             while stack:
>                 if is_max:
>                     cond = i == n or nums[stack[-1]] >= nums[i]
>                 else:
>                     cond = i == n or nums[stack[-1]] <= nums[i]
>                 if not cond:
>                     break
>                 mid = stack.pop()
>                 left = stack[-1] if stack else -1
>                 # mid is the max/min for all subarrays with left < l <= mid <= r < i
>                 result += nums[mid] * (mid - left) * (i - mid)
>             stack.append(i)
>         return result
> >
>     return sum_of_subarray_extremes(True) - sum_of_subarray_extremes(False)
> ```

> [!success] Complexity
> O(n) time | O(n) space.

> [!tip] Alternatives
> O(n²) prefix-max/min arrays: `O(n²)` — simpler but too slow for n > 10⁴. The monotonic stack "contribution" technique appears in dozens of problems: largest rectangle in histogram, max width ramp, sum of subarray minimums (LC 907), etc.

---

### Number of Submatrices That Sum to Target (LC 1074)

> [!example] Problem
> Given a matrix and a target, return the number of non-empty submatrices that sum to target.
> A submatrix x1, y1, x2, y2 is the set of all cells matrix[x][y] with x1 <= x <= x2 and y1 <= y <= y2.
> Two submatrices (x1, y1, x2, y2) and (x1', y1', x2', y2') are different if they have some coordinate that is different: for example, if x1 != x1'.
> 
> **Example 1:**
> ```
> Input: matrix = [[0,1,0],[1,1,1],[0,1,0]], target = 0
> Output: 4
> Explanation: The four 1x1 submatrices that only contain 0.
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [[1,-1],[-1,1]], target = 0
> Output: 5
> Explanation: The two 1x2 submatrices, plus the two 2x1 submatrices, plus the 2x2 submatrix.
> ```
> 
> **Example 3:**
> ```
> Input: matrix = [[904]], target = 0
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= matrix.length <= 100
> - 1 <= matrix[0].length <= 100
> - -1000 <= matrix[i][j] <= 1000
> - -10^8 <= target <= 10^8

> [!info] Approach
> Brute force O(m²n²). Fix the top and bottom row of the submatrix → reduce to a 1D "subarray sum equals target" problem solvable in O(n) with a hash map. For each pair of rows `(r1, r2)`, compute column-wise prefix sums `colsum[c]` = sum of `matrix[r1..r2][c]`. Then count subarrays of `colsum` summing to `target` using prefix sum + hash map. Precompute 2D prefix sums. Outer two loops: fix `r1` and `r2`. Inner loop: build running column sum, use `prefixSum - target` in a hash map to count subarrays.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def num_submatrix_sum_target(matrix, target):
>     m, n = len(matrix), len(matrix[0])
>     # Row-prefix sums: prefix[i][j] = sum of matrix[i][0..j-1]
>     prefix = [[0] * (n + 1) for _ in range(m)]
>     for i in range(m):
>         for j in range(n):
>             prefix[i][j+1] = prefix[i][j] + matrix[i][j]
> >
>     count = 0
>     for c1 in range(n):
>         for c2 in range(c1 + 1, n + 1):
>             freq = defaultdict(int)
>             freq[0] = 1
>             running = 0
>             for r in range(m):
>                 running += prefix[r][c2] - prefix[r][c1]
>                 count += freq[running - target]
>                 freq[running] += 1
>     return count
> ```

> [!success] Complexity
> O(m² × n) time (fix two rows, scan columns) | O(m) space per pair of columns.

> [!tip] Alternatives
> For square matrices (m = n), the complexity is O(n³) — optimal for this problem. 2D prefix sums + 1D subarray sum = standard reduction technique. Same technique solves "max sum rectangle in a matrix."

---

## Sqrt Decomposition

> **WHY it exists.** Sometimes we can't afford O(n log n) preprocessing (e.g., online updates with complex aggregates), but O(n) per query is too slow. Sqrt decomposition gives a middle ground: O(√n) per query/update with O(n) preprocessing.

>
> **WHAT it is.** Divide array into blocks of size `B ≈ √n`. Precompute the aggregate (sum/min/max) for each block. `query(l, r)`: process partial left block, full middle blocks (O(n/B) = O(√n)), partial right block. `update(i, val)`: update element and its block aggregate — O(1).
>
> **HOW to tune.** Block size B is tunable. For queries of cost Q and updates of cost U: minimize `B * Q + (n/B) * U` → optimal B = √(nU/Q). For equal query/update: B = √n.

---

### Block Decomposition for Range Queries

> [!example] Problem
> Given array `nums` of size n, support two operations: `update(i, val)` — set `nums[i] = val`; `sumRange(l, r)` — return sum of `nums[l..r]`. Implement with sqrt decomposition.

> [!info] Approach
> Demonstrates the sqrt decomposition pattern. In practice, use a Fenwick tree for sum queries. Sqrt decomposition shines when the aggregate is complex (e.g., number of distinct elements, median) where segment trees require custom merge. Blocks of size `B = int(n**0.5)`. `block_sum[b]` = sum of `nums[b*B .. (b+1)*B - 1]`. Update: O(1) — update element and its block. Query: O(√n) — partial left + full middle blocks + partial right. For `sumRange(l, r)`: if l and r are in the same block, iterate directly. Otherwise: sum partial left block, sum full middle blocks via `block_sum`, sum partial right block.

> [!note]- Python Solution
> ```python
> import math
> >
> class SqrtDecomposition:
>     def __init__(self, nums):
>         self.n = len(nums)
>         self.B = max(1, int(math.isqrt(self.n)))
>         self.nums = nums[:]
>         num_blocks = (self.n + self.B - 1) // self.B
>         self.block_sum = [0] * num_blocks
>         for i, v in enumerate(nums):
>             self.block_sum[i // self.B] += v
> >
>     def update(self, index, val):
>         b = index // self.B
>         self.block_sum[b] += val - self.nums[index]
>         self.nums[index] = val
> >
>     def sum_range(self, l, r):
>         bl, br = l // self.B, r // self.B
>         if bl == br:
>             return sum(self.nums[l:r+1])
>         total = sum(self.nums[l : (bl+1)*self.B])  # partial left
>         total += sum(self.block_sum[bl+1:br])       # full middle blocks
>         total += sum(self.nums[br*self.B : r+1])    # partial right
>         return total
> >
> # Example: count distinct elements in range — where sqrt shines over seg tree
> class SqrtDistinct:
>     """Count distinct values in range [l, r] — hard with segment tree."""
>     def __init__(self, nums):
>         self.n = len(nums)
>         self.B = max(1, int(math.isqrt(self.n)))
>         self.nums = nums[:]
> >
>     def query_distinct(self, l, r):
>         return len(set(self.nums[l:r+1]))  # O(r-l+1) = O(n) worst case
>         # For O(sqrt n): maintain sorted blocks, binary search + merge
> ```

> [!success] Complexity
> Build O(n) | Update O(1) | Query O(√n) | Space O(n).

> [!tip] Alternatives
> Fenwick tree / segment tree: O(log n) update and query for sum — strictly better for sum queries. Sqrt decomposition wins when: (1) offline queries allow Mo's algorithm (O((n+q)√n)), (2) the aggregate doesn't support efficient segment tree merge (e.g., distinct count, median), (3) quick implementation is needed in a contest.

---

## See Also

[[segment-tree]] | [[union-find]] | [[trie]] | [[string-algorithms]]
