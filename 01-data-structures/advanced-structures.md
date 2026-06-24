---
module: 01-data-structures
topic: Advanced Structures
status: partial — SDE-2 relevant sections only
tags: [data-structures, advanced-structures]
---

← [Data structures index](./README.md) · [DS decision tree](./ds_tree.md)

# Advanced Data Structures — Amazon SDE-2 Scope

> **LRU Cache and LFU Cache** are high-frequency Amazon SDE-2 topics — implement both from scratch.
> Segment tree, Fenwick tree, skip list, and persistent structures are **not expected at SDE-2** — awareness only.

---

## LRU Cache — O(1) Implementation

**Must implement from scratch at SDE-2.** Amazon asks this frequently as a standalone problem and as the design component of a larger system design question.

**Data structures**: `HashMap[key → Node]` + doubly linked list (head = MRU, tail = LRU).

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = OrderedDict()  # key → value; MRU at end

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)  # evict LRU (front)
```

**Manual DLL version (interview gold standard — shows you understand internals):**
```python
class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.head, self.tail = Node(), Node()  # dummy sentinels
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node):  # insert after head (MRU)
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._insert_front(node)
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

**Gotchas**: Dummy head/tail avoids null checks. Delete from `cache` using `lru.key` — not possible without storing key in Node.

---

## LFU Cache — O(1) Implementation

**Harder than LRU. Asked at SDE-2/SDE-3 boundary.** Three hash maps + min_freq tracker.

```python
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.min_freq = 0
        self.key_to_val = {}           # key → value
        self.key_to_freq = {}          # key → freq
        self.freq_to_keys = defaultdict(OrderedDict)  # freq → OrderedDict of keys (LRU within freq)

    def _touch(self, key: int):
        freq = self.key_to_freq[key]
        self.key_to_freq[key] += 1
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        self.freq_to_keys[freq + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        self._touch(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._touch(key)
            return
        if len(self.key_to_val) >= self.cap:
            evict, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict]
            del self.key_to_freq[evict]
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1
```

**Key insight**: `min_freq` can only increase by 1 on `_touch` and resets to 1 on `put`. The `OrderedDict` within each frequency bucket handles LRU tie-breaking in O(1).

---

## Awareness-Only Structures

These will not be implemented in an Amazon SDE-2 interview. Know what problem each solves.

### Segment Tree
Range query (sum/min/max) + point/range update, both O(log N). When prefix sum (static-only) is insufficient. Build is O(N); needs 4N nodes. Lazy propagation defers range updates. **Not tested at SDE-2.**

### Fenwick Tree (Binary Indexed Tree)
Compact prefix-sum array with O(log N) point update and prefix query. Simpler than segment tree but handles only prefix sums (not arbitrary range aggregates). Update: `i += i & -i`. Query: `i -= i & -i`. **Not tested at SDE-2.**

### Skip List
Probabilistic sorted structure with express lanes; O(log N) average search/insert/delete. Used in Redis sorted sets and Java `ConcurrentSkipListMap` as a simpler-to-make-concurrent alternative to balanced BSTs. **Know what it is; no implementation expected.**

### Self-Balancing BSTs (AVL, Red-Black)
Maintain O(log N) height via rotations on insert/delete. AVL is stricter (|balance| ≤ 1); Red-Black is looser and faster in practice (used in `std::map`, Java `TreeMap`). **Know they exist and that Python's `SortedList` / Java's `TreeMap` gives you O(log N) sorted ops without implementing rotations.**

### Bloom Filter
Space-efficient probabilistic set. k hash functions + bit array. Insert: set k bits. Query: if all k bits set → probably present; any 0 → definitely absent. False positives possible; false negatives impossible. Used in CDN cache checks, database query optimizers. **Awareness only.**

---

## Pattern Recognition (SDE-2 scope)

- **LRU Cache**: O(1) get/put → HashMap + Doubly Linked List.
- **LFU Cache**: O(1) get/put → key→val + key→freq + freq→OrderedDict(keys) + min_freq.
- **Range sum, static data** → Prefix sum array (not segment tree).
- **Dynamic range sum + updates** → Segment tree / Fenwick (not SDE-2; mention if asked about trade-offs).

---

## Flashcards

**What are the data structures used in an O(1) LRU Cache?** #flashcard
HashMap[key → Node] + doubly linked list. HashMap gives O(1) access to the node. DLL lets you remove/re-insert a node in O(1) with dummy head (MRU end) and tail (LRU end). On get/put: move node to front. On evict: remove from tail. Store key in Node to enable `del cache[lru.key]`.

**How does an O(1) LFU Cache resolve frequency ties?** #flashcard
`freq_to_keys` maps each frequency to an `OrderedDict` of keys maintaining LRU order within that frequency. `min_freq` tracks the current minimum. On `_touch`: move key from `freq` bucket to `freq+1` bucket; if `freq` bucket empties and was `min_freq`, increment `min_freq`. On `put` of new key: always set `min_freq = 1`.

**What is a Bloom filter and what guarantee does it provide?** #flashcard
A probabilistic set using k hash functions over a bit array. Insert sets k bits. Query: if all k bits set → probably in set (false positives possible); if any bit is 0 → definitely not in set (no false negatives). Used when space matters and occasional false positives are acceptable (e.g., cache hit checks).
