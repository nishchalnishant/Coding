---
module: striver/23-stack-and-queues
lesson: 30
topic: LFU Cache
difficulty: Hard
source: https://takeuforward.org/learning/dsa/lfu-cache?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, design, hashmap, linked-list]
---
# 30. LFU Cache

← [LRU Cache](29-lru-cache.md) · [Part 23 index](README.md) · Next → [Number of Greater Elements to the Right](31-count-greater-to-the-right.md)

> [!abstract] Problem at a glance
> **Task:** Cache that evicts the **least frequently used** key, breaking ties by least recently used; O(1) ops.
> **Key insight:** Group keys into **buckets by frequency**, each bucket an LRU list. Track `minFreq`. An access moves a key from bucket `f` to `f + 1`; if bucket `f` empties and `f == minFreq`, `minFreq++`. Eviction takes the LRU key of bucket `minFreq`. A new key always resets `minFreq = 1`.
> **Difficulty:** Hard · **Pattern:** Hashmap of frequency → LRU list · **Also on:** [LC 460](https://leetcode.com/problems/lfu-cache/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/lfu-cache?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 40 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Scan for the victim](#3-scan-for-the-victim) · [4. Frequency buckets + minFreq](#4-frequency-buckets--minfreq) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement `LFUCache(capacity)`, `get(key)` and `put(key, value)`. Each `get`/`put` on a key increments its use count. On overflow, evict the key with the smallest count; on ties, the least recently used one. Both O(1) average.

| Input | Output | Why |
|---|---|---|
| `cap 2: put(1,1), put(2,2), get(1), put(3,3), get(2), get(3), put(4,4), get(1), get(3), get(4)` | `1, -1, 3, -1, 3, 4` | put(3,3) evicts 2 (freq 1); put(4,4) evicts 1 (freq tie with 3, 1 is older) |

**Constraints:** `1 ≤ capacity ≤ 10⁴`; up to `2·10⁵` calls.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Scan for the victim | map key → (value, freq, last use); evict by linear scan | get O(1), put O(capacity) | O(capacity) |
| Frequency buckets + minFreq | freq → ordered set of keys; evict LRU of minFreq | O(1) per op | O(capacity) |

> [!tip] Interview angle
> Hard design problem; correctness of `minFreq` is the usual bug. Explain why `minFreq` only ever needs to increase by 1 on access (the touched key moves to `f + 1`, which then becomes the new minimum) and resets to 1 on insert.

---

## 3. Scan for the victim

**Intuition.** Keep a global clock. Eviction scans all keys for the minimum `(freq, lastUsed)`.

```python
class ScanLFU:
    def __init__(self, capacity):
        self.cap, self.d, self.t = capacity, {}, 0   # key -> [value, freq, last]
    def get(self, key):
        if key not in self.d:
            return -1
        self.t += 1
        e = self.d[key]
        e[1] += 1
        e[2] = self.t
        return e[0]
    def put(self, key, value):
        if self.cap == 0:
            return
        self.t += 1
        if key in self.d:
            e = self.d[key]
            e[0], e[1], e[2] = value, e[1] + 1, self.t
            return
        if len(self.d) == self.cap:
            victim = min(self.d, key=lambda k: (self.d[k][1], self.d[k][2]))
            del self.d[victim]
        self.d[key] = [value, 1, self.t]
```

**Complexity:** time **get O(1), put O(capacity)**, space **O(capacity)**.

---

## 4. Frequency buckets + minFreq

**Intuition.** `kv`: key → (value, freq). `bucket[f]`: keys with frequency `f` in recency order. `touch(key)` moves a key from `f` to `f + 1` and fixes `minFreq` when its bucket empties. Eviction pops the oldest key in `bucket[minFreq]`.

**Algorithm**

1. `touch(k)`: remove `k` from `bucket[f]`; if empty, delete it and, if `minFreq == f`, `minFreq++`. Append `k` to `bucket[f+1]`.
2. `get(k)`: miss → −1; else `touch`, return value.
3. `put(k, v)`: hit → update value, `touch`. Miss: if full, evict the oldest key in `bucket[minFreq]`. Insert with freq 1 and set `minFreq = 1`.

**Dry run** — cap 2: put 1, put 2 → b1 [1,2]. get 1 → b1 [2], b2 [1], min 1. put 3 → evict 2; b1 [3], min 1. get 2 → −1. get 3 → b2 [1,3], min 2. put 4 → evict oldest of b2 = 1; b1 [4], min 1. get 1 −1, get 3 → 3, get 4 → 4.

**C++**
```cpp
class LFUCache {
    int cap, minf = 0;
    unordered_map<int, pair<int, int>> kv;               // key -> {value, freq}
    unordered_map<int, list<int>> bucket;                // freq -> keys, most recent at front
    unordered_map<int, list<int>::iterator> pos;         // key -> position in its bucket
    void touch(int key) {
        int f = kv[key].second;
        bucket[f].erase(pos[key]);
        if (bucket[f].empty()) { bucket.erase(f); if (minf == f) minf++; }
        kv[key].second = f + 1;
        bucket[f + 1].push_front(key);
        pos[key] = bucket[f + 1].begin();
    }
public:
    LFUCache(int capacity) : cap(capacity) {}
    int get(int key) {
        if (!kv.count(key)) return -1;
        touch(key);
        return kv[key].first;
    }
    void put(int key, int value) {
        if (cap == 0) return;
        if (kv.count(key)) { kv[key].first = value; touch(key); return; }
        if ((int)kv.size() == cap) {
            int old = bucket[minf].back();
            bucket[minf].pop_back();
            if (bucket[minf].empty()) bucket.erase(minf);
            kv.erase(old); pos.erase(old);
        }
        kv[key] = {value, 1};
        bucket[1].push_front(key);
        pos[key] = bucket[1].begin();
        minf = 1;
    }
};
```

**Java**
```java
static class LFUCache {
    private final int cap;
    private int minf = 0;
    private final Map<Integer, int[]> kv = new HashMap<>();                     // key -> {value, freq}
    private final Map<Integer, LinkedHashSet<Integer>> bucket = new HashMap<>(); // freq -> keys, oldest first
    LFUCache(int capacity) { cap = capacity; }
    private void touch(int key) {
        int[] e = kv.get(key);
        int f = e[1];
        LinkedHashSet<Integer> b = bucket.get(f);
        b.remove(key);
        if (b.isEmpty()) { bucket.remove(f); if (minf == f) minf++; }
        e[1] = f + 1;
        bucket.computeIfAbsent(f + 1, z -> new LinkedHashSet<>()).add(key);
    }
    int get(int key) {
        if (!kv.containsKey(key)) return -1;
        touch(key);
        return kv.get(key)[0];
    }
    void put(int key, int value) {
        if (cap == 0) return;
        if (kv.containsKey(key)) { kv.get(key)[0] = value; touch(key); return; }
        if (kv.size() == cap) {
            LinkedHashSet<Integer> b = bucket.get(minf);
            int old = b.iterator().next();
            b.remove(old);
            if (b.isEmpty()) bucket.remove(minf);
            kv.remove(old);
        }
        kv.put(key, new int[]{value, 1});
        bucket.computeIfAbsent(1, z -> new LinkedHashSet<>()).add(key);
        minf = 1;
    }
}
```

**Python**
```python
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.cap, self.minf = capacity, 0
        self.kv = {}                              # key -> [value, freq]
        self.bucket = defaultdict(OrderedDict)    # freq -> keys, oldest first
    def _touch(self, key):
        f = self.kv[key][1]
        del self.bucket[f][key]
        if not self.bucket[f]:
            del self.bucket[f]
            if self.minf == f:
                self.minf += 1
        self.kv[key][1] = f + 1
        self.bucket[f + 1][key] = None
    def get(self, key):
        if key not in self.kv:
            return -1
        self._touch(key)
        return self.kv[key][0]
    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.kv:
            self.kv[key][0] = value
            self._touch(key)
            return
        if len(self.kv) == self.cap:
            old, _ = self.bucket[self.minf].popitem(last=False)
            if not self.bucket[self.minf]:
                del self.bucket[self.minf]
            del self.kv[old]
        self.kv[key] = [value, 1]
        self.bucket[1][key] = None
        self.minf = 1
```

**Complexity:** time **O(1) per op**, space **O(capacity)** — every step is a hashmap or linked-list operation on a known node.

---

## Edge cases

- Capacity 0: every put is a no-op.
- `put` on an existing key counts as a use.
- Frequency tie: evict the least recently used within the bucket.

---

## Common mistakes

1. Not updating `minFreq` when its bucket empties on touch.
2. Forgetting to reset `minFreq = 1` on insert.
3. Evicting after inserting the new key (the new key could be evicted itself).

---

## Follow-ups

1. Why can minFreq only go up by one in touch?
2. LRU vs LFU in practice?

<details><summary>Answer sketches</summary>

**#1:** Only the touched key leaves bucket f, and it lands in f + 1, so f + 1 is non-empty.

**#2:** LRU adapts quickly to shifting workloads; LFU keeps long-term hot keys but suffers from stale high counts (fixed with aging / windowed counts, e.g. TinyLFU).
</details>

---

## Flashcards

**LFU cache structure?** #flashcard
key → (value, freq); freq → LRU-ordered keys; plus minFreq.

**When does LFU's minFreq change?** #flashcard
+1 when touch empties the minFreq bucket; reset to 1 on inserting a new key.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
