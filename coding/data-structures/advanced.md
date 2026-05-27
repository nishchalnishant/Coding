---
tags: [coding, data-structures, advanced]
topic: Advanced Data Structures
difficulty: mixed
---

# Advanced Data Structures

---

## Skip List (Conceptual)

> [!info] Approach
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

> [!info] Approach
> **Cross-reference.** Full implementation (union by rank + path compression), applications (connected components, Kruskal's MST, redundant connections), and complexity analysis are in `/Users/nishchalnishant/Documents/GitHub/Coding/coding/algorithms/union-find.md`.
>
> **Core idea in brief.** Each set is a rooted tree. `find(x)` walks to the root (with path compression: point every node on the path directly to the root in one pass). `union(x, y)` attaches the smaller tree's root under the larger's (union by rank or size). Near-O(1) amortized per operation via inverse Ackermann function.

> [!tip] When advanced DSU appears
> - Weighted DSU: track relative weights along edges (e.g., "how many times heavier is x than y").
> - Rollback DSU: offline algorithms requiring undo of union operations — use union by rank only (no path compression), store history as a stack.
> - Parallel DSU: for offline LCT-like problems on trees.

---

## Suffix Array

> [!info] Approach
> **WHY it exists.** Suffix trees are O(n) but use O(n) space with a large constant and are complex to implement. Suffix arrays are an array-based alternative: O(n log n) or O(n) to build, O(n) space, and enable the same queries via the LCP array.
>
> **WHAT it is.** `SA[i]` = start index of the i-th lexicographically smallest suffix of string `s`. `LCP[i]` = length of the longest common prefix between suffix `SA[i]` and suffix `SA[i-1]`.

---

### Number of Distinct Substrings

> [!example] Problem
> Count all distinct non-empty substrings of `s`.

> [!info] Approach
> - **WHY:** Total substrings = n(n+1)/2. Each pair of adjacent suffixes in SA shares a prefix of length `LCP[i]`; those are already counted by an earlier suffix. Subtract total LCP sum.
> - **WHAT:** Distinct substrings = `n(n+1)/2 - sum(LCP)`.
> - **HOW:** Build SA via prefix doubling (O(n log² n)) or SA-IS (O(n)). Build LCP via Kasai's O(n) algorithm.

> [!note]- Python Solution
> ```python
> def count_distinct_substrings(s: str) -> int:
>     n = len(s)
>     # Simple O(n^2 log n) SA — replace with DC3/SA-IS for large n
>     sa = sorted(range(n), key=lambda i: s[i:])
> 
>     # Kasai's LCP — O(n)
>     rank = [0] * n
>     for i, v in enumerate(sa):
>         rank[v] = i
>     lcp = [0] * n
>     h = 0
>     for i in range(n):
>         if rank[i] > 0:
>             j = sa[rank[i] - 1]
>             while i + h < n and j + h < n and s[i + h] == s[j + h]:
>                 h += 1
>             lcp[rank[i]] = h
>             if h:
>                 h -= 1
> 
>     return n * (n + 1) // 2 - sum(lcp)
> ```

> [!success] Complexity
> O(n log² n) build (O(n) with SA-IS) + O(n) LCP | Space O(n).

---

### Longest Common Prefix of Suffixes (LCP Array)

> [!example] Problem
> Build the LCP array and use it to find the longest repeated substring.

> [!info] Approach
> - **WHY:** LCP[i] tells us how many characters adjacent suffixes in SA share. Max LCP = longest repeated substring (appears at two positions = two adjacent suffixes in SA with high overlap).
> - **WHAT:** Kasai's algorithm exploits: if `LCP(SA[rank[i]], SA[rank[i]-1]) = h`, then `LCP(SA[rank[i+1]], SA[rank[i+1]-1]) >= h - 1`. This means `h` can only decrease by 1 per step across all i, so the total work is O(n).
> - **HOW:** See implementation in `count_distinct_substrings` above. Longest repeated = `s[sa[idx] : sa[idx] + max(lcp)]`.

> [!success] Complexity
> Kasai LCP: O(n) | Space O(n).

> [!tip] Alternatives
> Suffix automaton: O(n) build, longest repeated = longest path to a non-clone state with multiple end-positions. More powerful but harder to implement.

---

## Sparse Table (Range Minimum Query in O(1))

> [!info] Approach
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
>     def __init__(self, nums: list[int]) -> None:
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
>     def query_min(self, l: int, r: int) -> int:
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

> [!info] Approach
> **Cross-reference.** Full implementations of monotonic stack and monotonic deque (sliding window maximum) are in `/Users/nishchalnishant/Documents/GitHub/Coding/coding/data-structures/stack.md` and `queue.md`. This section provides the decision framework.
>
> **WHY monotonic stack exists.** Many problems ask "for each element, find the next/previous greater/smaller element." A brute-force nested loop is O(n²). A monotonic stack processes each element at most twice → O(n).
>
> **WHAT it is.** A stack that maintains elements in sorted order (monotonically increasing or decreasing). When a new element violates the order, pop until the invariant is restored — those popped elements have found their "answer."

**Core pattern — Next Greater Element.**

> [!note]- Python Solution
> ```python
> def next_greater(nums: list[int]) -> list[int]:
>     n = len(nums)
>     result = [-1] * n
>     stack: list[int] = []   # stores indices, stack values are decreasing
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
> def max_sliding_window(nums: list[int], k: int) -> list[int]:
>     dq: deque[int] = deque()   # stores indices, front = index of max
>     result: list[int] = []
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

### LFU Cache

> [!example] Problem
> Design a data structure for a Least Frequently Used (LFU) cache with O(1) `get` and `put`. On a frequency tie, evict the least recently used among the tied keys.

> [!info] Approach
> **WHY:** LRU evicts by recency. LFU evicts by frequency — harder because frequency tracking requires an extra dimension of state. You need to know both *how often* and *in what order* each key was used at that frequency.
>
> **WHAT:** Three hash maps — `key→value`, `key→freq`, `freq→OrderedDict(key→None)`. Also track `min_freq`.
>
> **HOW:**
> - `get(key)`: if key missing return -1. Increment `freq[key]`. Move key from `freq_to_keys[old_freq]` to `freq_to_keys[new_freq]`. Update `min_freq` if `old_freq == min_freq` and that bucket is now empty.
> - `put(key, value)`: if key exists, update value and call get logic (increment freq). If capacity full, evict: call `popitem(last=False)` (LRU) from `freq_to_keys[min_freq]`, remove from all maps. Insert new key with `freq=1`. Set `min_freq=1` (new insertions always land at freq 1).

> [!note]- Python Solution
> ```python
> from collections import OrderedDict
>
> class LFUCache:
>     def __init__(self, capacity: int) -> None:
>         self.cap = capacity
>         self.key_to_val: dict[int, int] = {}
>         self.key_to_freq: dict[int, int] = {}
>         self.freq_to_keys: dict[int, OrderedDict] = {}
>         self.min_freq = 0
>
>     def _increment_freq(self, key: int) -> None:
>         freq = self.key_to_freq[key]
>         self.key_to_freq[key] = freq + 1
>         self.freq_to_keys[freq].pop(key)
>         if not self.freq_to_keys[freq]:
>             del self.freq_to_keys[freq]
>             if self.min_freq == freq:
>                 self.min_freq += 1
>         self.freq_to_keys.setdefault(freq + 1, OrderedDict())[key] = None
>
>     def get(self, key: int) -> int:
>         if key not in self.key_to_val:
>             return -1
>         self._increment_freq(key)
>         return self.key_to_val[key]
>
>     def put(self, key: int, value: int) -> None:
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

## See Also

[[segment-tree]] | [[union-find]] | [[trie]] | [[string-algorithms]]
