---
module: 02-algorithms
topic: Miscellaneous
subtopic: 
status: unread
tags: [algorithms, miscellaneous]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)
## First-Principles Map

> [!abstract] Amazon SDE-2 scope: Boyer-Moore Voting, Reservoir Sampling, Fisher-Yates, LRU Cache.
> Fenwick/BIT, Segment tree, Sparse table, LFU Cache, Mo's algorithm are SDE-3 / competitive programming — removed.


```
WHY Miscellaneous Algorithms exist
├── Real problems don't always map cleanly to one paradigm
│   ├── Random sampling from unknown-size streams → Reservoir Sampling
│   ├── Unbiased in-place shuffle with no extra space → Fisher-Yates
│   ├── Find majority without sorting or hash map → Boyer-Moore Voting
│   └── Randomized algorithms trade determinism for average-case speed
│
WHAT they are
├── Reservoir Sampling — uniformly sample k items from stream of unknown size n
│   ├── Fill reservoir with first k items
│   └── For item i (i > k): keep with prob k/i; replace random reservoir element
├── Fisher-Yates Shuffle — generate unbiased random permutation in O(n) time
│   ├── For i from n-1 down to 1: swap A[i] with A[rand(0..i)]
│   └── Each permutation equally likely; proof: n! outcomes, each with prob 1/n!
├── Boyer-Moore Voting — find majority element (appears > n/2 times) in O(n), O(1)
│   ├── Maintain candidate + count; increment if same, decrement otherwise
│   ├── Reset candidate when count hits 0
│   └── Invariant: if majority exists, it survives cancellation
├── Randomized Algorithms
│   ├── Las Vegas: always correct, random runtime (quicksort with random pivot)
│   └── Monte Carlo: always fast, correct with high probability (Miller-Rabin)
│
HOW they work
├── Reservoir Sampling (k=1 for simplicity):
│   ├── i=1: keep item 1 (prob 1/1)
│   ├── i=2: keep item 2 with prob 1/2; item 1 survives with prob 1/2
│   ├── i=n: each item kept with prob 1/n → uniform  [by induction]
│   └── General k: item i kept with prob k/i; displaced with prob k/i · 1/k = 1/i
├── Fisher-Yates:
│   ├── At step i, n-i elements remain unshuffled
│   ├── Pick any of (i+1) positions uniformly → correct marginal probability
│   └── Total: n · (n-1) · ... · 1 = n! equally likely permutations
├── Boyer-Moore:
│   ├── Each "cancellation" removes one majority + one non-majority element
│   ├── After all cancellations, majority element has remaining count > 0
│   └── Verification pass required if majority not guaranteed to exist
│
WHEN to use
├── Reservoir Sampling: streaming data, unknown n, need uniform k samples
│   └── Never load full stream; sample in single pass
├── Fisher-Yates: shuffle array in-place, unbiased, O(n) time
│   └── DO NOT use sort with random comparator — biased and O(n log n)
├── Boyer-Moore: "majority element" in O(n) time, O(1) space
│   └── Requires majority to exist OR add verification pass
├── Randomized algorithms: when deterministic worst case is too slow
│   └── Quicksort random pivot avoids O(n²) adversarial input
│
WHAT can go wrong
├── Reservoir Sampling: using biased RNG or wrong probability → non-uniform sample
├── Fisher-Yates: swapping A[i] with A[rand(0..n-1)] instead of A[rand(0..i)] → biased
├── Boyer-Moore: claiming majority without verification → wrong if no majority exists
├── Monte Carlo: not running enough iterations → failure probability too high
└── Randomized quicksort: not randomizing pivot → adversarial sorted input → O(n²)

Decision tree
├── Need k random samples from unknown-length stream? → Reservoir Sampling
├── Need unbiased shuffle in-place? → Fisher-Yates (rand in [0..i], not [0..n-1])
├── Find element appearing > n/2 times, O(1) space? → Boyer-Moore Voting
│   └── Not guaranteed majority? → add verification pass after
├── Deterministic worst case is O(n²) or worse? → Randomize (random pivot, hashing)
└── Need primality check for large numbers? → Miller-Rabin (Monte Carlo, run 20x)
```

## First-Principles Breakdown

- **Root problem:** Certain problems — uniform streaming samples, unbiased permutations, majority detection — have no obvious reduction to standard sorting/searching paradigms; each requires a dedicated algorithmic idea exploiting a specific structural property.
- **Core insight:** Reservoir sampling maintains a uniform invariant at every stream position i by adjusting acceptance probability to k/i; Fisher-Yates maintains uniform distribution over permutations by choosing from shrinking prefix; Boyer-Moore exploits the arithmetic fact that a majority element cannot be fully cancelled by minorities.
- **Invariant:** Reservoir: after processing i items, each is in the reservoir with probability k/i. Fisher-Yates: after processing position i, the suffix A[0..i] is a uniformly random permutation of its original elements. Boyer-Moore: if a majority element exists, its net count after all cancellations is strictly positive.
- **Why it's fast:** All three run in a single linear pass with O(1) extra space; no sorting, no hashing, no auxiliary arrays — the cleverness is entirely in maintaining the invariant incrementally.
- **Where it breaks:** Boyer-Moore gives a wrong answer (not just incorrect candidate) if you skip the verification pass when majority existence is not guaranteed; Fisher-Yates is subtly biased if the random index is drawn from [0, n-1] instead of [0, i] at each step — a mistake that produces non-uniform shuffles even though the code "looks right."




---

# Miscellaneous Algorithms — Amazon SDE-2 Essentials

Core algorithmic patterns that don't fit one category but appear frequently in SDE-2 interviews.

---

## 1. Core Algorithms (SDE-2 in-scope)

### Design Pattern — LRU Cache (Least Recently Used)

> [!IMPORTANT]
> **The Click Moment**: "O(1) access and eviction based on **recency**" — OR — "System Design in Code". SDE-3 candidates must be able to hand-roll a doubly linked list + hash map perfectly in 10 minutes, without relying on Python's `OrderedDict`.

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        # Dummy head and tail to avoid edge cases
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p

    def _add_to_head(self, node: Node) -> None:
        # Insert immediately after dummy head
        n = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = n
        n.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_head(node)  # crucial: mark as recently used
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self._add_to_head(node)
        self.cache[key] = node
        
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

#### Common Variants & Twists
1. **LFU Cache (Least Frequently Used)**:
   - **What (The Problem & Goal):** Similar to LRU, but evict the item with the lowest frequency. On tie, use LRU.
   - **How (Intuition & Mental Model):** Maintain two maps: `key_to_node` and `freq_to_dll`. Each frequency `f` points to a doubly linked list of nodes with that frequency. Also track `min_freq`. When a key is accessed, move it from `freq_to_dll[f]` to `freq_to_dll[f+1]`.
2. **LRU with Expiration (TTL)**:
   - **What (The Problem & Goal):** Items in the cache have a Time-To-Live (TTL).
   - **How (Intuition & Mental Model):** In the `get` method, check if the item has expired before returning it. For active eviction of expired items, use a priority queue of `(expiration_time, key)` or periodically sweep the head of a chronologically sorted DLL.
```

> [!CAUTION]
> **LRU Gotchas**: 
> 1. Updating an existing key in `put` must also move it to the head.
> 2. `get` must move the accessed node to the head (many forget this).
> 3. You MUST store the `key` inside the DLL node. Why? When capacity is reached, you find the tail node to evict, but you also need to delete it from the `cache` hash map. Without the key in the node, you don't know what to delete!

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

## 3. Common Interview Problems

### Medium (High Frequency)
- **Merge Intervals `🎯 T2`** — Sort by start; extend `end = max(end, interval[1])` while overlapping.
- **Meeting Rooms II** — Min-heap of end times; count concurrent meetings = heap size.
- **Task Scheduler `⚡ T1`** — Greedy: arrange most-frequent tasks with cooldown gaps; `ceil((max_count-1) * (n+1) + count_max)`.
- **Design LRU Cache** — HashMap + doubly linked list; O(1) get/put.
- **Range Sum Query (Mutable) `💤 T3`** — Fenwick tree; O(log N) update and prefix query.

### Hard
- **The Skyline Problem** — Sweep line on building start/end events; max-heap of active heights.
- **Data Stream as Disjoint Intervals** — `SortedList` + binary search; merge left/right neighbors on insert.
- **Find Median from Data Stream** — Two heaps (max-heap lower half, min-heap upper half); rebalance on insert.
- **Minimum Interval to Include Each Query** — Sort queries + intervals; min-heap sweep; lazy-remove expired.

> [!note] Count of Smaller Numbers After Self and Count of Range Sum require Fenwick/merge sort (SDE-3). Skip for Amazon SDE-2.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Merge Intervals `🎯 T2`** | Sort + Greedy Merge | "Combine overlapping [l, r] ranges" | Sort by start; extend `end` greedily while `interval[0] <= end` | Touching intervals `[1,2]` and `[2,3]` — confirm merging rule. Sort by start, not end. |
| **Meeting Rooms II** | "Minimum rooms for N meetings" | Min-heap of end times; if `heap[0] <= start`, reuse room (pop + push new end) | Heap size at any moment = answer (max concurrent meetings). Sort by start first. |
| **The Skyline Problem** | "Height profile of buildings as events" | Sweep line on start/end events; max-heap of `(-height, end)` for active buildings | Lazy deletion from heap (check if top is still active). Critical point = when max height changes. |
| **Non-Overlapping Intervals `🎯 T2`** | "Min removals to make disjoint" | Sort by **end**; greedily keep interval with earliest end; count removals | Sort by end (not start): earliest end leaves max room for future intervals. |
| **Data Stream Intervals** | "Maintain disjoint intervals dynamically" | Binary search for left/right overlap; merge on insert | Handle both neighbors: merge left if `new.start <= left.end + 1`; merge right if `new.end >= right.start - 1`. |
| **Design HashSet [E]** | "Implement a hash set without built-in hash" | Array of buckets (chaining); `hash(key) = key % size`; linked list per bucket | Choose bucket count as a prime (e.g., 1009) to reduce collisions. Handle remove in chained list carefully. |
| **Design Hit Counter [E]** | "Count hits in the past 5 minutes" | Circular array of 300 slots (seconds); slot = `(timestamp, count)`; reset stale slot on write | `timestamp % 300` gives slot index. Reading: sum all slots where `timestamp - slot_time < 300`. |
| **LRU Cache [M] `🎯 T2`** | "O(1) get/put with eviction of least recently used" | `OrderedDict` or HashMap + doubly linked list; move to head on access; evict tail on overflow | Python `OrderedDict.move_to_end(key)` + `popitem(last=False)` gives O(1). Hand-roll DLL for interviews expecting lower-level answer. |
| **Design Twitter [M] `⚡ T1`** | "In-memory Twitter: post tweet, follow, getNewsFeed" | Per-user tweet list (most recent first); `getNewsFeed` = K-way merge of followees' lists via min-heap | K-way merge with heap: push `(timestamp, user, tweet_idx)`; pop 10 times. Follow/unfollow update a set. |
| **Range Sum Query — Immutable [E] `💤 T3`** | "Precompute prefix sums for O(1) range queries" | `prefix[i] = prefix[i-1] + nums[i-1]`; `query(l,r) = prefix[r+1] - prefix[l]` | 1-indexed prefix array avoids boundary check. `prefix[0] = 0` sentinel. |
| **Snapshot Array [M]** | "Array with snapshot: get value at past snapshot" | Per-index list of `(snap_id, val)`; binary search on snap_id for reads | Store only changed values (copy-on-write). Binary search via `bisect_right(snaps, snap_id) - 1`. |
| **Find Median from Data Stream [H] `⚡ T1`** | "Maintain running median as numbers are inserted" | Two heaps: max-heap for lower half, min-heap for upper half; balance sizes | Max-heap in Python: negate values. Rebalance after every insert: sizes differ by at most 1. Median = top of larger heap or average of both tops. |
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

- "Find majority element (appears > n/2 times), O(1) space" → Boyer-Moore Voting; add verification pass if majority not guaranteed.
- "Random sample from unknown-length stream" → Reservoir Sampling; keep with prob k/i.
- "Unbiased shuffle in-place" → Fisher-Yates; draw from [0..i], not [0..n-1].
- "O(1) get/put with LRU eviction" → HashMap + doubly linked list; move node to head on every access.
- "Events at coordinates: intervals, skyline" → sweep line; sort events by x, process with sorted structure or heap.
- "Running median" → two heaps (max-heap lower half, min-heap upper half); keep sizes balanced.
- "Merge overlapping intervals" → sort by start; extend end greedily.
- "Meeting rooms / concurrent interval count" → min-heap of end times; heap size = max concurrent.

---

## See also

- [Patterns Master](../../03-patterns/patterns-master.md) — 30-second recognition triggers for all patterns
- [Dynamic Programming](dynamic-programming/README.md) — optimal substructure; overlapping subproblems
- [Sorting](sorting.md) — sort key choices; when sort unlocks a greedy solution
- [Mathematics](maths.md) — number theory tricks; modular arithmetic
- [Graph Algorithms](graph.md) — when a problem is really a graph in disguise

## Flashcards

**Boyer-Moore Voting: what does the candidate hold after all cancellations?** #flashcard
If a majority element (>n/2) exists, it survives — net count > 0. Always verify with a second pass if majority not guaranteed.

**Reservoir Sampling: probability that item i ends up in the reservoir of size k?** #flashcard
k/i — maintained by accepting item i with prob k/i and replacing a random reservoir element.

**Fisher-Yates: what range should the random index be drawn from at step i?** #flashcard
[0, i] — NOT [0, n-1]. Drawing from [0, n-1] produces biased shuffles.

**LRU Cache: what must happen on a `get` call besides returning the value?** #flashcard
Move the accessed node to the head (mark as most recently used). Forgetting this breaks the recency invariant.
