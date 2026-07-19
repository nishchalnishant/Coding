---
tags: [coding, data-structures, design]
topic: design-a-data-structure
difficulty: mixed
---

# Design-a-Data-Structure Problems (L4 signature family)

> [!abstract] Tier Legend (L4 tiers)
> `⚡ T1` — **Must Master**: the Google L4 design family. Every problem here is "support ops X/Y/Z in O(1) or O(log n)".
> `🎯 T2` — **Build Fluidity**: know the composition cold; edge cases matter less.
>
> Derivation ladder for this family: [Pattern Ladders — Ladder 12](../../03-patterns/PATTERN_LADDERS.md#ladder-12--design-a-data-structure-l4-signature).
> Already covered elsewhere: **Min Stack** → [stack](05-stack.md), **LRU Cache** → [linked list](07-linked-list.md), **Kth Largest in Stream / Find Median** → [heap](10-heap.md).

## Design Interview Checklist

- **Start with the ops table**: list each required operation and its target complexity *before* choosing structures. The problem is the table.
- The universal move: **compose two structures so each covers the other's weak op**, then keep them in sync on every mutation.
- Swap-with-last turns "delete from middle of array" into O(1) — if order doesn't matter.
- When a heap must support arbitrary deletion: **lazy deletion** (validate top against a source of truth on pop).
- When history/versions are needed: append `(version, value)` pairs and binary-search them.
- Say the sync invariant out loud ("map and list always agree because…") — that sentence is what's graded.

---

### Logger Rate Limiter `💤 warm-up`

> [!example] Problem
> Design a logger that receives a stream of `(timestamp, message)` calls. `shouldPrintMessage` returns true only if the same message has not printed in the last 10 seconds.

> [!info] Approach
> A map `message → last printed timestamp`. Print iff the message is unseen or `timestamp - last >= 10`, updating the map only when you print. The trap: updating the timestamp on *rejected* messages, which lets a spammed message suppress itself forever.

> [!note]- Python Solution
> ```python
> class Logger:
>     def __init__(self):
>         self.last = {}
> >
>     def shouldPrintMessage(self, timestamp, message):
>         if message not in self.last or timestamp - self.last[message] >= 10:
>             self.last[message] = timestamp
>             return True
>         return False
> ```

> [!success] Complexity
> Time O(1) per call; Space O(#distinct messages).

> [!tip] Follow-up
> "Memory grows forever" → evict old entries lazily on each call, or keep a deque of (ts, msg) and purge entries older than 10s.

---

### Design Hit Counter `⚡ T1`

> [!example] Problem
> Count hits in the past 5 minutes (300 seconds). `hit(timestamp)` records a hit; `getHits(timestamp)` returns hits in `[timestamp-299, timestamp]`. Timestamps are non-decreasing.

> [!info] Approach
> A deque of timestamps. On `getHits`, pop from the left while the front is `<= timestamp - 300`. Because timestamps only increase, each hit enters and leaves the deque once — amortized O(1).

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> class HitCounter:
>     def __init__(self):
>         self.q = deque()
> >
>     def hit(self, timestamp):
>         self.q.append(timestamp)
> >
>     def getHits(self, timestamp):
>         while self.q and self.q[0] <= timestamp - 300:
>             self.q.popleft()
>         return len(self.q)
> ```

> [!success] Complexity
> Time amortized O(1); Space O(hits in window).

> [!tip] Follow-up
> "Millions of hits per second" — the deque explodes. Switch to a **300-slot circular buffer** of `(time, count)`: `idx = timestamp % 300`; if the stored time differs, reset the slot. Space becomes O(300) regardless of traffic. This follow-up is the reason the problem is asked.

---

### Insert Delete GetRandom O(1) `⚡ T1`

> [!example] Problem
> Implement a set supporting `insert(val)`, `remove(val)`, and `getRandom()` — each O(1) average, with every element equally likely for `getRandom`.

> [!info] Approach
> Ops table: hashset does insert/remove but can't do uniform random; array does random (`random.choice`) but O(n) remove. Compose: array of values + map `val → index`. Remove = **swap the target with the last element, then pop** — O(1), and only one map entry needs fixing. Order is destroyed, but nothing required order.

> [!note]- Python Solution
> ```python
> import random
> >
> class RandomizedSet:
>     def __init__(self):
>         self.arr = []
>         self.idx = {}
> >
>     def insert(self, val):
>         if val in self.idx:
>             return False
>         self.idx[val] = len(self.arr)
>         self.arr.append(val)
>         return True
> >
>     def remove(self, val):
>         if val not in self.idx:
>             return False
>         i, last = self.idx[val], self.arr[-1]
>         self.arr[i] = last
>         self.idx[last] = i
>         self.arr.pop()
>         del self.idx[val]
>         return True
> >
>     def getRandom(self):
>         return random.choice(self.arr)
> ```

> [!success] Complexity
> Time O(1) average per op; Space O(n).

> [!warning] Gotcha
> Update `idx[last]` **before** deleting `idx[val]` — when removing the last element itself they are the same key, and the order above handles that case for free (dry-run it).

> [!tip] Follow-up
> "Allow duplicates" (LC 381) → map value → *set of indices*; swap-with-last now must pick any index of `val` and update the moved element's index set.

---

### Random Pick with Weight `⚡ T1`

> [!example] Problem
> Given weights `w`, implement `pickIndex()` returning index `i` with probability `w[i] / sum(w)`.

> [!info] Approach
> Build the prefix-sum array once. Draw a uniform random integer in `[1, total]` and binary-search (`bisect_left`) for the first prefix ≥ it. Each index owns a segment of the number line proportional to its weight. This is two T1 patterns (prefix sums, binary search) composed — say that.

> [!note]- Python Solution
> ```python
> import random, bisect
> from itertools import accumulate
> >
> class Solution:
>     def __init__(self, w):
>         self.prefix = list(accumulate(w))
>         self.total = self.prefix[-1]
> >
>     def pickIndex(self):
>         target = random.randint(1, self.total)
>         return bisect.bisect_left(self.prefix, target)
> ```

> [!success] Complexity
> Time O(n) init, O(log n) per pick; Space O(n).

> [!tip] Follow-up
> "Weights get updated" → now you need O(log n) update + prefix query; *name* Fenwick/segment tree as the tool, don't implement ([skip policy](../../00-L3-EXECUTION-META/L3_CHEATSHEET.md)).

---

### Snapshot Array `🎯 T2`

> [!example] Problem
> `set(index, val)`, `snap()` returns a snapshot id, `get(index, snap_id)` returns the value at that index as of that snapshot.

> [!info] Approach
> Copying the array per snapshot is the trap (O(n) per snap). Instead, each index keeps its own history list `[(snap_id, val)]`, appended only when written. `get` = binary search for the last entry with `snap_id <=` the requested one. Versioning by history + bisect is a reusable L4 idea.

> [!note]- Python Solution
> ```python
> import bisect
> >
> class SnapshotArray:
>     def __init__(self, length):
>         self.hist = [[(-1, 0)] for _ in range(length)]
>         self.snap_id = 0
> >
>     def set(self, index, val):
>         h = self.hist[index]
>         if h[-1][0] == self.snap_id:
>             h[-1] = (self.snap_id, val)
>         else:
>             h.append((self.snap_id, val))
> >
>     def snap(self):
>         self.snap_id += 1
>         return self.snap_id - 1
> >
>     def get(self, index, snap_id):
>         h = self.hist[index]
>         i = bisect.bisect_right(h, (snap_id, float('inf'))) - 1
>         return h[i][1]
> ```

> [!success] Complexity
> Time O(1) set/snap, O(log s) get (s = snapshots that wrote this index); Space O(total writes).

---

### Stock Price Fluctuation `🎯 T2`

> [!example] Problem
> A stream of `(timestamp, price)` records where a timestamp may be **corrected** by a later call. Support `current()` (price at latest timestamp), `maximum()`, `minimum()`.

> [!info] Approach
> Map `timestamp → price` is the source of truth (+ track latest timestamp). Max/min need heaps — but corrections invalidate heap entries. **Lazy deletion**: push `(price, timestamp)` on every update; on `maximum()`/`minimum()`, pop while the heap top's price disagrees with the map. Same trick as Sliding Window Median.

> [!note]- Python Solution
> ```python
> import heapq
> >
> class StockPrice:
>     def __init__(self):
>         self.price = {}
>         self.latest = 0
>         self.maxh, self.minh = [], []
> >
>     def update(self, timestamp, price):
>         self.price[timestamp] = price
>         self.latest = max(self.latest, timestamp)
>         heapq.heappush(self.maxh, (-price, timestamp))
>         heapq.heappush(self.minh, (price, timestamp))
> >
>     def current(self):
>         return self.price[self.latest]
> >
>     def maximum(self):
>         while -self.maxh[0][0] != self.price[self.maxh[0][1]]:
>             heapq.heappop(self.maxh)
>         return -self.maxh[0][0]
> >
>     def minimum(self):
>         while self.minh[0][0] != self.price[self.minh[0][1]]:
>             heapq.heappop(self.minh)
>         return self.minh[0][0]
> ```

> [!success] Complexity
> Time O(log n) update, amortized O(log n) max/min; Space O(n updates).

> [!tip] Alternatives
> A sorted container (`SortedList`) makes max/min O(1) with true O(log n) deletes — mention it, but lazy-delete heaps are the portable answer.

---

### LFU Cache `⚡ T1`

> [!example] Problem
> Like LRU, but evict the **least frequently used** key; break frequency ties by least *recently* used. `get` and `put` in O(1).

> [!info] Approach
> Three synced parts: `key → (val, freq)`; `freq → OrderedDict of keys` (each an LRU list within that frequency); and `min_freq`. On any access, move the key from bucket `f` to `f+1`; if bucket `min_freq` emptied, `min_freq += 1`. On insert, evict the LRU key of bucket `min_freq` if full, then set `min_freq = 1`. It's LRU plus one more dimension — derive it from LRU, don't recall it.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, OrderedDict
> >
> class LFUCache:
>     def __init__(self, capacity):
>         self.cap = capacity
>         self.kv = {}                     # key -> (val, freq)
>         self.buckets = defaultdict(OrderedDict)  # freq -> keys (LRU order)
>         self.min_freq = 0
> >
>     def _touch(self, key):
>         val, f = self.kv[key]
>         del self.buckets[f][key]
>         if not self.buckets[f] and self.min_freq == f:
>             self.min_freq = f + 1
>         self.kv[key] = (val, f + 1)
>         self.buckets[f + 1][key] = None
> >
>     def get(self, key):
>         if key not in self.kv:
>             return -1
>         self._touch(key)
>         return self.kv[key][0]
> >
>     def put(self, key, value):
>         if self.cap == 0:
>             return
>         if key in self.kv:
>             self._touch(key)
>             self.kv[key] = (value, self.kv[key][1])
>             return
>         if len(self.kv) == self.cap:
>             old, _ = self.buckets[self.min_freq].popitem(last=False)
>             del self.kv[old]
>         self.kv[key] = (value, 1)
>         self.buckets[1][key] = None
>         self.min_freq = 1
> ```

> [!success] Complexity
> Time O(1) per op; Space O(capacity).

> [!warning] Gotcha
> `min_freq` only ever needs to increment by exactly 1 on a touch (the moved key was in the min bucket), and resets to 1 on every insert — if you find yourself scanning for the new min, the design is wrong.

---

### Peeking Iterator / Flatten Nested List Iterator `🎯 T2`

> [!example] Problem
> (a) Wrap an iterator to support `peek()`. (b) Given a nested list of integers and lists, implement an iterator returning integers in flattened order.

> [!info] Approach
> (a) Cache one element ahead; `peek` returns the cache, `next` returns it and refills.
> (b) The lazy version (what's graded): a stack holding the elements **reversed**; `hasNext` pops lists and pushes their reversed contents until the top is an integer. Flattening everything in the constructor works but fails the follow-up ("the list is huge / infinite").

> [!note]- Python Solution
> ```python
> class NestedIterator:
>     def __init__(self, nestedList):
>         self.stack = nestedList[::-1]
> >
>     def next(self):
>         return self.stack.pop().getInteger()
> >
>     def hasNext(self):
>         while self.stack:
>             top = self.stack[-1]
>             if top.isInteger():
>                 return True
>             self.stack.pop()
>             self.stack.extend(top.getList()[::-1])
>         return False
> ```

> [!success] Complexity
> Time amortized O(1) per element overall; Space O(depth + width).

> [!warning] Gotcha
> All the work lives in `hasNext`, and `next` must assume `hasNext` was called — say this contract out loud; it's the design point.
