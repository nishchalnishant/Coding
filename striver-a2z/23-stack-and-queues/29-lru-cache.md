---
module: striver-a2z/23-stack-and-queues
lesson: 29
topic: LRU Cache
difficulty: Hard
source: https://takeuforward.org/learning/dsa/lru-cache?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, design, hashmap, linked-list]
---
# 29. LRU Cache

← [The Celebrity Problem](28-celebrity-problem.md) · [Part 23 index](README.md) · Next → [LFU Cache](30-lfu-cache.md)

> [!abstract] Problem at a glance
> **Task:** Cache of fixed capacity with O(1) `get`/`put` that evicts the least recently used key.
> **Key insight:** Recency order needs O(1) **move-to-front** and O(1) **remove-from-back**: a **doubly linked list**. Finding a key's node in O(1) needs a **hashmap key → node**. Sentinel head/tail nodes remove all the null checks.
> **Difficulty:** Hard · **Pattern:** Hashmap + doubly linked list · **Also on:** [LC 146](https://leetcode.com/problems/lru-cache/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/lru-cache?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. List in recency order](#3-list-in-recency-order) · [4. Hashmap + doubly linked list](#4-hashmap--doubly-linked-list) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement `LRUCache(capacity)`, `get(key)` (value or −1, marks the key as used) and `put(key, value)` (insert or update, marks as used; on overflow evict the least recently used key). Both O(1) average.

| Input | Output | Why |
|---|---|---|
| `cap 2: put(1,1), put(2,2), get(1), put(3,3), get(2), put(4,4), get(1), get(3), get(4)` | `1, -1, -1, 3, 4` | put(3,3) evicts 2; put(4,4) evicts 1 |

**Constraints:** `1 ≤ capacity ≤ 3000`; up to `2·10⁵` calls.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| List in recency order | linear search and move on every access | O(capacity) per op | O(capacity) |
| Hashmap + doubly linked list | map key → node; DLL head = most recent | O(1) per op | O(capacity) |

> [!tip] Interview angle
> Expect to write the DLL by hand (no `OrderedDict` / `LinkedHashMap` unless they allow it; mention that you know them). Keep two helpers, `remove(node)` and `insertFront(node)`, and build both operations from them. Remember to store the key in the node, because eviction needs it to delete from the map.

---

## 3. List in recency order

**Intuition.** Keep `[key, value]` pairs with the most recent at the end. Every access searches the list and moves the pair to the end; eviction pops the front.

```python
class ListLRU:
    def __init__(self, capacity):
        self.cap, self.items = capacity, []
    def _find(self, key):
        for i, (k, _) in enumerate(self.items):
            if k == key:
                return i
        return -1
    def get(self, key):
        i = self._find(key)
        if i < 0:
            return -1
        kv = self.items.pop(i)
        self.items.append(kv)
        return kv[1]
    def put(self, key, value):
        i = self._find(key)
        if i >= 0:
            self.items.pop(i)
        elif len(self.items) == self.cap:
            self.items.pop(0)
        self.items.append([key, value])
```

**Complexity:** time **O(capacity) per op**, space **O(capacity)**.

---

## 4. Hashmap + doubly linked list

**Intuition.** The DLL stores nodes from most recent (after `head`) to least recent (before `tail`). `get` unlinks the node and re-inserts it after `head`. `put` updates in place and moves it to the front, or, for a new key, evicts `tail.prev` when full and inserts a new node at the front.

**Algorithm**

1. `get(k)`: miss → −1. Hit → `remove(node)`, `insertFront(node)`, return value.
2. `put(k, v)`: hit → update value, move to front.
3. Miss: if full, `lru = tail.prev`; `remove(lru)`; delete `map[lru.key]`. Create the node, insert at front, add it to the map.

**Dry run** — cap 2: put 1, put 2 → [2,1]. get 1 → [1,2], 1. put 3: evict 2 → [3,1]. get 2 → −1. put 4: evict 1 → [4,3]. get 1 −1, get 3 → 3, get 4 → 4.

**C++**
```cpp
class LRUCache {
    struct Node { int k, v; Node *prev = nullptr, *next = nullptr; Node(int k, int v) : k(k), v(v) {} };
    int cap;
    unordered_map<int, Node*> mp;
    Node *head = new Node(0, 0), *tail = new Node(0, 0);
    void unlink(Node* n) { n->prev->next = n->next; n->next->prev = n->prev; }
    void pushFront(Node* n) { n->next = head->next; n->prev = head; head->next->prev = n; head->next = n; }
public:
    LRUCache(int capacity) : cap(capacity) { head->next = tail; tail->prev = head; }
    int get(int key) {
        auto it = mp.find(key);
        if (it == mp.end()) return -1;
        Node* n = it->second;
        unlink(n); pushFront(n);
        return n->v;
    }
    void put(int key, int value) {
        auto it = mp.find(key);
        if (it != mp.end()) { Node* n = it->second; n->v = value; unlink(n); pushFront(n); return; }
        if ((int)mp.size() == cap) { Node* lru = tail->prev; unlink(lru); mp.erase(lru->k); delete lru; }
        Node* n = new Node(key, value);
        mp[key] = n;
        pushFront(n);
    }
};
```

**Java**
```java
static class LRUCache {
    static class Node { int k, v; Node prev, next; Node(int k, int v) { this.k = k; this.v = v; } }
    private final int cap;
    private final Map<Integer, Node> mp = new HashMap<>();
    private final Node head = new Node(0, 0), tail = new Node(0, 0);
    LRUCache(int capacity) { cap = capacity; head.next = tail; tail.prev = head; }
    private void unlink(Node n) { n.prev.next = n.next; n.next.prev = n.prev; }
    private void pushFront(Node n) { n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; }
    int get(int key) {
        Node n = mp.get(key);
        if (n == null) return -1;
        unlink(n); pushFront(n);
        return n.v;
    }
    void put(int key, int value) {
        Node n = mp.get(key);
        if (n != null) { n.v = value; unlink(n); pushFront(n); return; }
        if (mp.size() == cap) { Node lru = tail.prev; unlink(lru); mp.remove(lru.k); }
        n = new Node(key, value);
        mp.put(key, n);
        pushFront(n);
    }
}
```

**Python**
```python
class Node:
    __slots__ = ("k", "v", "prev", "next")
    def __init__(self, k=0, v=0):
        self.k, self.v, self.prev, self.next = k, v, None, None

class LRUCache:
    def __init__(self, capacity):
        self.cap, self.mp = capacity, {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head
    def _unlink(self, n):
        n.prev.next, n.next.prev = n.next, n.prev
    def _push_front(self, n):
        n.next, n.prev = self.head.next, self.head
        self.head.next.prev = n
        self.head.next = n
    def get(self, key):
        n = self.mp.get(key)
        if n is None:
            return -1
        self._unlink(n)
        self._push_front(n)
        return n.v
    def put(self, key, value):
        n = self.mp.get(key)
        if n:
            n.v = value
            self._unlink(n)
            self._push_front(n)
            return
        if len(self.mp) == self.cap:
            lru = self.tail.prev
            self._unlink(lru)
            del self.mp[lru.k]
        n = Node(key, value)
        self.mp[key] = n
        self._push_front(n)
```

**Complexity:** time **O(1) per op**, space **O(capacity)** — hashmap lookup plus a constant number of pointer updates.

---

## Edge cases

- `put` on an existing key: update and move to front, no eviction.
- Capacity 1.
- `get` on a missing key must not change the order.

---

## Common mistakes

1. Not storing the key in the node, so eviction can't remove the map entry.
2. Evicting before checking whether the key already exists (evicts needlessly).
3. Forgetting to move the node to the front on `put`-update.

---

## Follow-ups

1. Thread-safe LRU?
2. Built-ins?
3. TTL expiry?

<details><summary>Answer sketches</summary>

**#1:** Lock around both ops, or segment the cache (striped locks); reads also mutate order, so a plain RW-lock doesn't help.

**#2:** Python `OrderedDict.move_to_end` / `popitem(last=False)`; Java `LinkedHashMap(cap, 0.75f, true)` with `removeEldestEntry`.

**#3:** Add a timestamp per node and check on access, or a min-heap of expiry times.
</details>

---

## Flashcards

**LRU cache data structures?** #flashcard
Hashmap key → node + doubly linked list ordered by recency (sentinels at both ends).

**Why must an LRU node store its key?** #flashcard
On eviction you only have the tail node and need the key to delete it from the map.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
