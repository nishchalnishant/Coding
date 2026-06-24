---
tags: [coding, data-structures, advanced]
topic: Advanced Data Structures — Amazon SDE-2
difficulty: mixed
---

# Advanced Data Structures — Amazon SDE-2

Scope: LRU/LFU cache (tested), monotonic stack/deque (tested), Bloom filter (awareness), Fenwick tree basics (awareness). Exotic structures removed.

---

## LRU Cache (LC 146)

> **Pattern**: doubly linked list + hash map. O(1) get and put.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

**Complexity**: O(1) get/put. Space O(capacity).

**Follow-up**: If asked for a manual implementation without OrderedDict, use a doubly linked list + dict: maintain `head` (LRU) and `tail` (MRU); on access, move node to tail; on eviction, remove head.

---

## LFU Cache (LC 460) — O(1)

> **Pattern**: three maps — key→value, key→freq, freq→OrderedDict(keys). Track `min_freq`.

```python
from collections import OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.key_to_val = {}
        self.key_to_freq = {}
        self.freq_to_keys = {}  # freq → OrderedDict of keys (insertion order = LRU)
        self.min_freq = 0

    def _increment_freq(self, key):
        freq = self.key_to_freq[key]
        self.key_to_freq[key] = freq + 1
        self.freq_to_keys[freq].pop(key)
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        self.freq_to_keys.setdefault(freq + 1, OrderedDict())[key] = None

    def get(self, key):
        if key not in self.key_to_val:
            return -1
        self._increment_freq(key)
        return self.key_to_val[key]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._increment_freq(key)
            return
        if len(self.key_to_val) == self.cap:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys.setdefault(1, OrderedDict())[key] = None
        self.min_freq = 1
```

**Complexity**: O(1) get/put. Space O(capacity).

**Key insight**: New keys always start at freq=1, so `min_freq = 1` on every insert. On eviction, `min_freq` is exact because we bump it only when the current min bucket becomes empty.

---

## Monotonic Stack

**Trigger**: "next/previous greater/smaller element", "largest rectangle", "daily temperatures", "sum of subarray min/max"

```python
# Next Greater Element — O(n)
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []  # indices; values are decreasing
    for i, n in enumerate(nums):
        while stack and nums[stack[-1]] < n:
            result[stack.pop()] = n
        stack.append(i)
    return result

# Largest Rectangle in Histogram — O(n)
def largest_rectangle(heights):
    stack = []  # (index, height)
    max_area = 0
    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))
    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))
    return max_area
```

---

## Monotonic Deque (Sliding Window Maximum)

**Trigger**: "maximum/minimum in every window of size k"

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()   # indices; values are decreasing (front = max)
    result = []
    for i, v in enumerate(nums):
        while dq and nums[dq[-1]] <= v:
            dq.pop()
        dq.append(i)
        if dq[0] < i - k + 1:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

**Complexity**: O(n). Each element pushed/popped at most once.

---

## Fenwick Tree (BIT) — Awareness

Not likely asked to implement from scratch at SDE-2, but you should know what it does:

- Supports **point update** and **prefix sum query** in O(log n).
- More concise than a segment tree for prefix-sum problems.
- `update(i, delta)`: add delta at index i, propagate via `i += i & -i`.
- `query(i)`: sum from 1 to i, walk via `i -= i & -i`.
- For range sum: `query(r) - query(l-1)`.

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, delta):  # 1-indexed
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def query(self, i):  # prefix sum [1..i]
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s
```

---

## Bloom Filter — Awareness

**Not tested at SDE-2 as an implementation.** Know the concept:

- A probabilistic data structure for membership testing.
- Uses k hash functions + a bit array of size m.
- **False positives possible** (says "maybe in set" when it's not); **no false negatives** (says "definitely not in set" only when truly absent).
- Space-efficient: does not store actual elements.
- Used in: databases (avoid disk lookup for missing keys), caches (avoid fetching items not in cache), spam filters.
- Trade-off: larger bit array → fewer false positives; more hash functions → more hash overhead.

---

## Skip List — Awareness

**Not tested at SDE-2.** Know the concept:

- Randomized ordered structure; expected O(log n) search/insert/delete.
- Used in Redis sorted sets. Python's `sortedcontainers.SortedList` is the practical equivalent.
- Layered linked list where each node is promoted to higher levels with probability p.
- Alternatives: balanced BST (AVL, Red-Black), treap.

---

## See Also

- [patterns-quick-reference.md](../patterns-quick-reference.md) — LRU cache template
- [stack.md](./stack.md) — monotonic stack problems
- [queue.md](./queue.md) — monotonic deque problems
