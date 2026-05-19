# Advanced Data Structures: Tries and Segment Trees

## Tries (Prefix Trees)
Tries are mainly used in SDE 3 interviews for problems involving prefix matching, wildcard string searches, or bitwise XOR maximization.

### Node Structure
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
```

### 1. Standard Trie Implementation
```python
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

### Common SDE 3 Trie Problems:
1.  **Word Search II**: Use a Trie to store words, then perform backtracking on the grid to search for them efficiently.
2.  **Maximum XOR of Two Numbers**: Use a Binary Trie. Insert numbers into the Trie, and for each number, try to greedily find the path corresponding to its bitwise complement.

---

---

## Segment Trees
Crucial for answering range sum/min/max queries over an array, with the ability to update the array in $O(\log n)$.

> [!TIP]
> **Full Deep Dive**: See the dedicated [Segment Trees Guide](segment-tree.md) for canonical implementations, Lazy Propagation, and SDE-3 Interview variants.

---

## Fenwick Tree (Binary Indexed Tree)
More memory efficient `O(N)` and easier to implement than segment trees for simple sum queries.
```python
class FenwickTree:
    def __init__(self, size):
        self.tree = [0] * (size + 1)

    def update(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
```

---

## Pattern Recognition

- **Trie**: Prefix match, autocomplete, word search in grid (store words, backtrack). Binary Trie: max XOR (prefer opposite bit).
- **Segment Tree**: Range sum/min/max with point or range updates; O(log N) query/update. Lazy propagation for range add/update.
- **Fenwick**: Range sum + point update; simpler than segment tree; O(N) space.
- **LRU Cache**: O(1) get/put → HashMap + Doubly Linked List.
- **LFU Cache**: O(1) get/put → HashMap of key→node + HashMap of freq→DLL + min_freq tracker.

## Interview Strategy

- **Identify**: "Prefix" / "autocomplete" / "word dictionary" → Trie. "Range query" with updates → Segment tree or Fenwick.
- **Common mistakes**: Trie — forgetting is_end; Segment tree — wrong segment bounds; Fenwick — 1-indexed.

## Quick Revision

- **Trie**: insert/search/startsWith O(L). Binary trie for max XOR. Word Search II: Trie + backtrack.
- **Segment tree**: 4*N nodes; build O(N); query/update O(log N). Lazy for range update.
- **Fenwick**: update(i, delta), query(i) prefix sum; i += i&-i / i -= i&-i.

---

## LRU Cache — O(1) Implementation

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

**Manual DLL version (interview gold standard):**
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

**Harder than LRU.** Three hash maps + min_freq tracker.

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
            # Evict LFU (then LRU within LFU)
            evict, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict]
            del self.key_to_freq[evict]
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1
```

**Key insight**: `min_freq` can only increase by 1 on `_touch` and resets to 1 on `put`. The `OrderedDict` within each frequency bucket handles the LRU tie-breaking in O(1).

---

## Skip List

Probabilistic alternative to balanced BSTs. Each element is in multiple "lanes" with decreasing probability. Level 1 = all elements. Higher levels = express lanes (each element promoted with probability p = 0.5).

**Complexity**: O(log n) average search/insert/delete. O(n) worst case (rare).

**Use in practice**: Redis sorted sets use a skip list internally. Java's `ConcurrentSkipListMap` is the thread-safe sorted map.

**When interviewers ask**: "Design a sorted set with O(log n) insert/delete/range-query" — mention skip list as an alternative to a balanced BST, noting simpler lock-free concurrency.

```python
import random

class SkipNode:
    def __init__(self, val, level):
        self.val = val
        self.forward = [None] * (level + 1)

class SkipList:
    MAX_LEVEL = 16
    P = 0.5

    def __init__(self):
        self.header = SkipNode(float('-inf'), self.MAX_LEVEL)
        self.level = 0

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def search(self, target: int) -> bool:
        cur = self.header
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].val < target:
                cur = cur.forward[i]
        cur = cur.forward[0]
        return cur is not None and cur.val == target

    def insert(self, val: int):
        update = [self.header] * (self.MAX_LEVEL + 1)
        cur = self.header
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].val < val:
                cur = cur.forward[i]
            update[i] = cur
        new_level = self._random_level()
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level
        new_node = SkipNode(val, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
```
