---
module: 01-data-structures
topic: Hashing
subtopic: 
status: unread
tags: [data-structures, hashing]
---

← [Data structures index](./README.md) · [DS decision tree](./ds_tree.md)
## First-Principles Map

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop. Do not move on until these are reflexive.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Highly probable; know the core patterns cold. Edge cases matter less.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Know what it is conceptually; skip deep implementation practice.


```
WHY hashing exists → WHAT it is → HOW it works → WHEN to use → WHAT can go wrong
       │                  │               │               │               │
  [O(1) lookup by key  [deterministic  [hash(key) →    [frequency      [hash collisions
   is impossible with   function maps   index in array;  count, cache,   degrade to O(n);
   arrays (unknown      arbitrary key   collision        two-sum, anagram poor hash
   key space) or        to bounded       handled by       detection,      function clusters
   trees (O(log n))]    integer index]   chaining or      grouping,       keys; worst-case
                                         open addressing]  LRU cache]      is always O(n)]
       │                  │               │
  [real-world:          [invariant:     [load factor α = n/m;
   dictionary —          same key always  resize when α > 0.7;
   word → page           same bucket;     amortized O(1) insert;
   number in O(1)]       hash is          chaining: O(1+α) lookup;
                         deterministic]   open addressing: O(1/(1-α))]
       ↓
[Decision: HashMap vs alternatives]
  ├── vs Array        → hash for arbitrary key types; array for integer 0..n index
  ├── vs BST/TreeMap  → hash O(1) avg vs BST O(log n); BST supports range queries
  └── vs Trie         → trie for prefix operations; hash for exact key lookup
```

## First-Principles Breakdown
- **Root problem**: Need O(1) lookup for arbitrary key types (strings, objects) — arrays only handle integer indices in a known range.
- **Core insight**: A good hash function uniformly distributes keys across buckets, making collision probability O(1/m) per pair — effectively O(1) lookup.
- **Invariant**: Same key always hashes to the same bucket; the hash function is deterministic and stable during a session.
- **Why it's fast**: With low load factor, expected chain length is ≈1 — lookup touches ~1 element regardless of table size.
- **Where it breaks**: Adversarial inputs can force all keys to one bucket (hash DoS); ordering is lost; worst-case is O(n); non-hashable types (mutable lists) cannot be keys.

# Hashing — L3 Core

```
[HASHING — MINDMAP]
├── WHY IT EXISTS
│   ├── Problem it solves: O(1) average lookup/insert/delete regardless of dataset size
│   ├── Alternative (sorted array) gives O(log N) search but O(N) insert — too slow for frequent mutations
│   └── Analogy: a hash table is a post-office with numbered boxes — hash function is the address formula
├── WHAT IT IS (First Principles)
│   ├── Core definition: map arbitrary keys → fixed-range indices via a hash function h(k) = k mod M
│   ├── Hash function requirements: deterministic, uniform distribution, fast to compute
│   ├── Load factor α = n/M: keep α < 0.7 for open addressing; < 1.0 for chaining
│   └── Collision: two keys map to the same slot — unavoidable by pigeonhole; strategy determines performance
├── HOW IT WORKS
│   ├── Collision Resolution
│   │   ├── Chaining: each slot holds a linked list; worst case O(N) if all keys collide
│   │   ├── Open Addressing (Linear Probing): probe slot+1, +2, ... — cache friendly, clustering issue
│   │   ├── Quadratic Probing: probe slot+1², +2², ... — reduces primary clustering
│   │   └── Double Hashing: probe slot + i·h2(k) — best distribution, harder to implement
│   ├── Resizing (Dynamic Array Analogy)
│   │   ├── When α exceeds threshold: allocate new table (2× size), rehash all keys — O(N) amortized O(1)
│   │   └── Shrink when α < 0.25 to reclaim memory
│   ├── Hash Functions
│   │   ├── Integer keys: multiply-shift (k * A mod 2^w >> (w-p)) or k mod prime
│   │   ├── String keys: polynomial rolling hash h = Σ s[i] * base^i mod prime
│   │   └── Cryptographic (SHA-256): not for hash tables — too slow; used for integrity checks
│   ├── Consistent Hashing (Distributed Systems)
│   │   ├── Map both nodes and keys onto a ring [0, 2^32)
│   │   ├── Key goes to first node clockwise on ring — adding/removing node moves only K/N keys on average
│   │   └── Virtual nodes: each physical node owns multiple ring positions → more uniform load
├── COMPLEXITY SUMMARY
│   ├── Insert / Lookup / Delete: O(1) average, O(N) worst (all collisions)
│   ├── Resize: O(N) amortized O(1) per operation
│   └── Bloom filter insert/query: O(k) — constant if k is fixed
├── WHEN TO USE
│   ├── Signal: "two-sum / find complement" → hash map for O(N) vs O(N log N) sort
│   ├── Signal: "group by property / frequency count" → hash map / Counter
│   ├── Signal: "seen before / deduplication" → hash set
│   ├── Signal: "cache with O(1) eviction" → hash map + doubly linked list (LRU)
│   ├── Signal: "distributed key-value / load balancing" → consistent hashing
│   ├── Signal: "membership test with low memory, false positives ok" → bloom filter
│   └── Avoid when: need sorted order (use TreeMap/SortedDict) or worst-case O(1) (use perfect hashing)
└── COMMON MISTAKES / GOTCHAS
    ├── Mutable keys: using list/dict as key → TypeError; use tuple or frozenset
    ├── Default hash in Python: custom objects use id() — must implement __hash__ + __eq__ together
    ├── Integer overflow in rolling hash: use mod prime; Python arbitrary ints hide this in other languages
    ├── Load factor neglect: never pre-size a hash map too small in hot paths — triggers repeated rehash
    └── Bloom filter: cannot remove elements; false positives increase as n grows beyond design capacity
```

Map keys to indices via hash function for O(1) average lookup/insert/delete. L3: collision strategies, load factor tuning, consistent hashing for distributed systems, and bloom filters.




---

## Theory & Mental Models

**What it is:** A data structure that maps keys to array indices via a hash function, enabling O(1) average-case insert, lookup, and delete. Core invariant: `bucket_index = hash(key) % capacity`; collisions (two keys mapping to same bucket) are resolved by chaining or open addressing.

**Why it exists:** Solves the problem of O(1) arbitrary-key lookup — something arrays (index-only) and BSTs (O(log N)) cannot match. Real-world analogy: a library index card system — look up a book by title (key), get the shelf location (value) instantly without scanning every shelf.

**Memory layout:** An array of buckets. Each bucket is a linked list (chaining) or a probe sequence (open addressing). Load factor α = n/m (n = stored items, m = capacity). Python dict rehashes when α > ~0.66, doubling capacity.

**Key invariants:**
- `hash(key) % capacity` must be deterministic and uniform across key space.
- Load factor α must stay below a threshold (typically 0.7) to keep O(1) average.
- Collision resolution must guarantee every key is findable — no silent overwrites.
- In Python, only immutable (hashable) types can be keys: `int`, `str`, `tuple` (of hashables), `frozenset`. Lists and dicts cannot be keys.

**Complexity at a glance:**

| Operation | Average | Worst Case | Notes |
| :--- | :--- | :--- | :--- |
| Insert | O(1) | O(N) | Worst case: all keys collide |
| Lookup | O(1) | O(N) | Worst case: all keys collide |
| Delete | O(1) | O(N) | Worst case: all keys collide |
| Rehash | O(N) | O(N) | Amortized over all inserts |

**When to reach for it:**
- Frequency counting — `Counter` or `defaultdict(int)`.
- Complement/pair lookups — two-sum: check if `target - x` already seen.
- Grouping by property — anagram grouping, event bucketing.
- O(1) membership test — set lookups vs linear scan.
- Sliding window character counts — track window state with a frequency map.

**Common mistakes:**
- Using mutable objects (lists, dicts) as keys — raises `TypeError`; convert to `tuple` first.
- Not initializing `seen = {0: 1}` or `first_seen = {0: -1}` in prefix-sum hash map patterns.
- Comparing floats as dict keys — floating point imprecision makes equality unreliable.
- Forgetting that Python `dict` preserves insertion order (3.7+) — can be an asset or a surprise.

---

## 1. Concept Overview

**Problem space**: Frequency count, existence check (set), two-sum (complement map), grouping by key (anagrams), subarray sum = K (prefix sum → count map), LRU cache (map + DLL), deduplication.

---

## 2. Core Algorithms & Click Moments

### Complement Map — Two Sum Pattern

> [!IMPORTANT]
> **The Click Moment**: "Find a **pair** with a given sum" — OR — "check if a **complement exists**" — OR — "**two sum / 3-sum / k-sum `⚡ T1`**". For each element, check if `target - element` is already in the map. This converts O(N²) brute force to O(N).

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []  # no pair found

def four_sum_count(A: list[int], B: list[int], C: list[int], D: list[int]) -> int:
    ab_sums: dict[int, int] = {}
    for a in A:
        for b in B:
            ab_sums[a + b] = ab_sums.get(a + b, 0) + 1
    return sum(ab_sums.get(-(c + d), 0) for c in C for d in D)
```

#### Common Variants & Twists
1. **3Sum / 4Sum `⚡ T1`**:
   - **What (The Problem & Goal):** Find unique triplets (or quadruplets) that sum to zero (or a target).
   - **How (Intuition & Mental Model):** Use the Two-Sum map logic as the inner loop, reducing the complexity by one degree of `N` compared to brute force. For 4Sum Count (where you just need the number of tuples from 4 different arrays), hash all sums of `A + B`, then for every `c` and `d`, look up `-(c + d)` in the hash map.
2. **Max Number of K-Sum Pairs**:
   - **What (The Problem & Goal):** Find the maximum number of pairs that sum to `k`. Each element can only be used in one pair.
   - **How (Intuition & Mental Model):** A twist where each number can only be used once. Instead of just storing the index, store the *count* of available numbers in the hash map. When a pair is formed `(x, target - x)`, decrement the count of both numbers to "consume" them.

---

### Frequency Map — Counting and Grouping

> [!IMPORTANT]
> **The Click Moment**: "**Anagram** detection" — OR — "group strings by pattern" — OR — "top-K frequent elements" — OR — "**at most K distinct** in a window". The hash map stores counts; the key design determines correctness.

```python
from collections import Counter, defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: dict[tuple, list[str]] = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # or tuple(Counter(s).items()) for stability
        groups[key].append(s)
    return list(groups.values())

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    # Bucket sort: index = frequency, O(N) time
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        result.extend(buckets[freq])
        if len(result) >= k:
            return result[:k]
    return result
```

> [!TIP]
> **Anagram key choice**: `tuple(sorted(s))` is O(K log K) per word where K is word length. For very long words, use a 26-integer count tuple: `tuple(Counter(s).get(c, 0) for c in 'abcdefghijklmnopqrstuvwxyz')`. For Unicode strings, the 26-array assumption fails — use `Counter` directly as the key (but `Counter` is not hashable; convert to `tuple(sorted(Counter(s).items()))`).

#### Common Variants & Twists
1. **Find All Anagrams in a String `⚡ T1`**:
   - **What (The Problem & Goal):** Find all starting indices of substrings in `s` that are anagrams of `p`.
   - **How (Intuition & Mental Model):** Sliding window + frequency map. Maintain a frequency map of the target string `p`. Slide a window of size `len(p)` across `s`, maintaining a running frequency map of the window. If the window's map equals `p`'s map, record the start index.
2. **Sort Characters By Frequency**:
   - **What (The Problem & Goal):** Sort a string in decreasing order based on the frequency of its characters.
   - **How (Intuition & Mental Model):** Count characters into a frequency map, then sort the characters based on their count (or use bucket sort where the index is the frequency). Rebuild the result string by appending `char * count`.
3. **Minimum Window Substring `⚡ T1`**:
   - **What (The Problem & Goal):** Find the shortest substring containing all characters of a target string.
   - **How (Intuition & Mental Model):** You need a frequency map of the target string, and a running frequency map of the current sliding window. The critical condition is maintaining a `have` counter vs `required_unique_chars`. Only increment `have` when the window's count for a char matches the target's exact requirement.

---

### Prefix Sum + Map — Subarray Sum Queries

> [!IMPORTANT]
> **The Click Moment**: "Count subarrays with **sum equal to K**" — OR — "longest subarray with **sum 0**" — OR — "subarray sum **divisible by K**". Combine a running prefix sum with a hash map to find all valid `[l, r]` pairs in O(N) — without a nested loop.

```python
def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    count = 0
    prefix = 0
    seen: dict[int, int] = {0: 1}  # empty subarray has sum 0
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count

def longest_subarray_sum_zero(nums: list[int]) -> int:
    first_seen: dict[int, int] = {0: -1}
    prefix, best = 0, 0
    for i, x in enumerate(nums):
        prefix += x
        if prefix in first_seen:
            best = max(best, i - first_seen[prefix])
        else:
            first_seen[prefix] = i
    return best
```

> [!CAUTION]
> Always initialize `seen = {0: 1}` (for counting) or `first_seen = {0: -1}` (for length). This accounts for subarrays starting from index 0. Missing this initialization causes wrong answers when the entire prefix is the valid subarray.

#### Common Variants & Twists
1. **Contiguous Array**:
   - **What (The Problem & Goal):** Find the maximum length of a contiguous subarray with an equal number of 0s and 1s.
   - **How (Intuition & Mental Model):** Replace all `0`s with `-1`. The problem then exactly transforms into finding the longest subarray with a sum of `0`. Store the `first_seen` index of each prefix sum in the hash map.
2. **Make Sum Divisible by P**:
   - **What (The Problem & Goal):** Remove the shortest subarray so that the sum of the remaining elements is divisible by `P`.
   - **How (Intuition & Mental Model):** Find the remainder of the total sum: `rem = sum(nums) % P`. The problem reduces to finding the shortest subarray with `sum % P == rem`. As you iterate, calculate `current_prefix % P` and use `(current_prefix - rem) % P` for the map lookup.
3. **Subarray Sums Divisible by K**:
   - **What (The Problem & Goal):** Count the number of subarrays whose sum is divisible by `K`.
   - **How (Intuition & Mental Model):** Store `running_sum % K` in the map instead of the raw sum. A valid subarray exists ending at the current index if you have seen the exact same remainder before (because `(prefix_j - prefix_i) % K == 0` implies `prefix_j % K == prefix_i % K`).

---

### Design: Hash Table Internals

> [!IMPORTANT]
> **The Click Moment**: "Design a **hash map from scratch**" — OR — "explain collision handling". Two strategies: **chaining** (linked list per bucket) and **open addressing** (probe for next slot). Know the trade-offs.

> [!TIP]
> If two students are assigned the same locker (collision), they need a rule — either wait in a chain outside the locker (chaining) or look for the next free locker (open addressing). Chaining tolerates high load factors because each bucket can hold an unlimited chain; open addressing requires free slots in the array so its load factor must stay below ~0.7 before rehashing.

```python
class HashMap:
    def __init__(self, capacity: int = 1009):  # prime capacity reduces clustering
        self._capacity = capacity
        self._buckets: list[list] = [[] for _ in range(capacity)]

    def _hash(self, key: int) -> int:
        return key % self._capacity

    def put(self, key: int, value: int) -> None:
        bucket = self._buckets[self._hash(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key: int) -> int:
        bucket = self._buckets[self._hash(key)]
        for k, v in bucket:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self._buckets[self._hash(key)]
        self._buckets[self._hash(key)] = [(k, v) for k, v in bucket if k != key]
```

---

### Insert-Delete-GetRandom O(1)

> [!IMPORTANT]
> **The Click Moment**: "Design a set supporting **insert, delete, and getRandom** all in O(1)". The trick: hash map stores `value → index` in a dynamic array. Delete swaps the target with the last element (to avoid gaps) then pops.

```python
import random

class RandomizedSet:
    def __init__(self):
        self._vals: list[int] = []
        self._idx_map: dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self._idx_map:
            return False
        self._idx_map[val] = len(self._vals)
        self._vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self._idx_map:
            return False
        idx = self._idx_map[val]
        last = self._vals[-1]
        self._vals[idx] = last
        self._idx_map[last] = idx
        self._vals.pop()
        del self._idx_map[val]
        return True

    def get_random(self) -> int:
        return random.choice(self._vals)
```

---

## 3. Production Context (L3 Note)

> [!NOTE]
> Distributed systems details (consistent hashing, lock-free structures, bloom filters, skip lists, etc.) are **L3+ system design** topics. For Google L3 coding interviews, focus on the patterns in sections 1–2 and the interview problems below.

---

## 4. Common Interview Problems

### Easy
- Two Sum — Complement map; single pass.
- **Valid Anagram `🎯 T2`** — `Counter(s) == Counter(t)`.
- **First Unique Character** — `Counter`; find first with count 1.

### Medium
- Group Anagrams — `sorted(word)` or count-tuple as key.
- Subarray Sum Equals K — Prefix sum + count map; `seen = {0:1}`.
- Longest Consecutive Sequence — Set lookup; only start chain from `x` if `x-1` not in set.
- LRU Cache — Map + DLL; dummy head/tail.
- **Insert Delete GetRandom O(1) `⚡ T1`** — Map + array; swap-with-last on delete.
- **Contiguous Array (equal 0/1)** — Map `0→-1`; prefix sum + first-seen map.

### Hard
- **Minimum Window Substring `⚡ T1`** — Sliding window + need/have count maps.
- **Substring with Concatenation of All Words** — Fixed word-length window; multiset comparison.
- **Max Points on a Line** — Slope map with `gcd` normalization; handle vertical lines.
- **Design HashMap** — Chaining with prime-sized bucket array; handle resize.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Group Anagrams `⚡ T1`** | Hash by Canonical Key | "Same letters, group together" | Key = `sorted(s)` or 26-count tuple | 26-array fails for Unicode; `sorted` is O(K log K) vs O(K) count. |
| **Longest Consecutive `⚡ T1`** | "Longest streak, unsorted" | Set; only start chain if `x-1` not in set | Without the "start only" guard: O(N²); with it: amortized O(N). |
| **LRU Cache `🎯 T2`** | "O(1) get/put with eviction" | Map `key→DLL node`; move on access; evict tail | Dummy head/tail eliminate all null-check edge cases in `_remove`. |
| **Subarray Sum = K** | "Count subarrays with exact sum" | `seen={0:1}`; `count += seen[prefix-K]` | Works with negatives; sliding window doesn't. `seen[0]=1` is critical. |
| **Contiguous Array** | "Equal 0s and 1s in subarray" | Map `0→-1`; find longest zero-sum subarray | Reduces to "longest subarray with sum 0" — recognize the transformation. |
| **Minimum Window `⚡ T1`** | "Smallest window containing all of T" | Expand right until valid; shrink left while valid | `have == required` condition based on frequency saturation, not total count. |
| **Insert Delete GetRandom `⚡ T1`** | "O(1) all three operations" | Map + array; swap-with-last on delete | Update `_idx_map[last] = idx` before deleting the target's entry. |
| **Design HashMap** | "Hash map from scratch" | Array of buckets; chaining with linear scan | Prime capacity; handle `equals` by value; tombstone for open addressing delete. |
| **4Sum Count `⚡ T1`** | "Count quadruples summing to 0" | Hash sums of `A+B`; count complements in `C+D` | O(N²) space and time — better than O(N⁴) brute force. |
| **Max Points on a Line** | "Max collinear points" | Slope map per anchor; `gcd` normalize slope fraction | Vertical line (`dx=0`); same point (`dy=dx=0`); negative slopes in fraction. |
| **Two Sum `⚡ T1`** [E] | "Find two indices summing to target" | Complement map: store `val → index`; look up `target - val` | Return indices, not values — clarify. Handle same index: check before inserting. |
| **Valid Anagram `🎯 T2`** [E] | "Do two strings use same characters?" | Frequency count: increment for s, decrement for t; all zeros = anagram | `Counter(s) == Counter(t)` is clean; for follow-up (Unicode), same approach applies. |
| **Word Pattern** [E] | "Bijection between pattern chars and words" | Two maps: `char→word` and `word→char`; check both directions | Bijection requires both maps — `a→dog` and `b→dog` is invalid even if one map is fine. |
| **Longest Subarray with At Most K Distinct** [M] | "Sliding window, count distinct ≤ K" | Sliding window; map counts elements in window; shrink left when distinct > K | Decrement count and delete key only when count reaches 0 — not just on any shrink. |
| **Top K Frequent Words `⚡ T1`** [M] | "K most frequent strings, ties alphabetical" | Count frequencies; sort by `(-freq, word)`; take first K | Heap alternative: `heapq.nsmallest(k, ...)` with `(-freq, word)` avoids full sort. |
| **Ransom Note** [E] | "Can you build ransom string from magazine?" | Count magazine letters; check ransom has no unsatisfied letter | `Counter(ransomNote) - Counter(magazine)` — if any key remains, return False. |
| **Find Duplicate File in System** [M] | "Group files by content" | Map `content → [path/file]`; collect groups with ≥ 2 | Parse path+content from each entry; content is key, list of full paths is value. |
| **Longest Palindrome** [M] | "Longest palindrome buildable from letters" | Count frequencies; all even-count chars contribute fully; one odd-count char can be center | Add 1 if any odd-frequency char exists (it becomes the center). |
| **Isomorphic Strings** [E] | "Bijection between characters of s and t" | Map `s[i]→t[i]` and `t[i]→s[i]`; conflict = not isomorphic | Same structure as Word Pattern bijection — need both maps for correctness. |
| **Subarray Sum Equals K `⚡ T1`** [M] | "Count subarrays with exact sum K" | Prefix sum + map; `count += prefix_map[running_sum - K]`; init `prefix_map[0] = 1` | Sliding window fails with negatives — prefix map handles all cases. |
| **Longest Increasing Subsequence (via hash) `⚡ T1`** [M] | "LIS via patience sort + bisect" | Maintain `tails` list; `bisect_left` for replacement index | `tails` is not the LIS itself — only its length. Reconstruct via parent tracking if sequence needed. |

---

## Quick Revision Triggers

- If the problem says "find pair summing to target" → think Complement Map; store `x → index` and look up `target - x`.
- If the problem says "count subarrays with sum = K" (with negatives) → think Prefix Sum + Hash Map; initialize `seen = {0: 1}` before the loop.
- If the problem says "group strings by pattern" or "anagrams" → think Frequency-Key Map; key = `tuple(sorted(s))` or 26-count tuple.
- If the problem says "O(1) insert, delete, getRandom" → think Hash Map + Array; swap-with-last on delete to preserve O(1) random access.
- If the problem says "longest consecutive sequence" → think Hash Set; only start a chain from `x` if `x-1` is not in the set.
- If the problem says "sliding window with at most K distinct" → think Frequency Map as window state; delete key only when its count drops to 0.
- If the problem involves custom hash map design → think Prime-sized bucket array + chaining; rehash when load factor exceeds 0.7.

## See also

- [Array](01-array.md) — prefix sum + map for subarray problems
- [String](../01-data-structures/03-string.md) — anagram key design; rolling hash (Rabin-Karp)
- [Linked List](07-linked-list.md) — LRU cache DLL component
- [Patterns Master](../03-patterns/patterns-master.md) — complement map and frequency map triggers

## Flashcards

**Explain the Swap-with-Last optimization used to support O(1) getRandom alongside O(1) insert and delete.** #flashcard
Combine a dynamic array `list` and a hash map `val_to_idx` mapping values to their array index:
- **Insert `🎯 T2`**: Append value to `list`, record its index in `val_to_idx`.
- **Delete**: Retrieve the target index `idx` from `val_to_idx`. Swap the element at `idx` with the last element of `list` in $O(1)$. Update the index of the swapped element in `val_to_idx`, delete the target from the map, and pop the last element from `list`.
- **GetRandom**: Return a random element from `list` in $O(1)$ by generating an index in range.

**Why must we initialize the prefix sum hash map with `{0: 1}` for the "Subarray Sum Equals K" problem?** #flashcard
The key `0` with value `1` represents an empty prefix subarray. If a subarray starting at index 0 sums to exactly $K$, its prefix sum is $K$. The check `prefix_sum - K` evaluates to `0`. Without `{0: 1}` in the map, this subarray would be missed.

**How does the "Longest Consecutive Sequence" algorithm achieve O(N) time using a HashSet?** #flashcard
Push all numbers into a HashSet. Iterate through each number $X$:
1. Check if $X - 1$ is in the set. If yes, skip (since $X$ is not the start of a sequence).
2. If no, start counting a sequence: check $X + 1, X + 2, \dots$ in the set until a mismatch occurs.
Each number is visited at most twice (once in the outer loop, and once as part of a sequence), resulting in $O(N)$ time.

**What is a load factor in Hash Maps, and how is rehashing implemented?** #flashcard
The load factor is the ratio $\alpha = \frac{\text{number of elements}}{\text{number of buckets}}$. When $\alpha$ exceeds a threshold (typically 0.7 or 0.75), rehashing is triggered:
1. Allocate a new bucket array (typically $2\times$ size, ideally a prime number).
2. Iterate through all key-value pairs in the old table.
3. Compute their new bucket indices (`hash(key) % new_size`) and insert them into the new table.

- **Trade-off**: It can yield false positives (stating an element is present when it is not) but never false negatives.
- **Limitation**: Elements cannot be easily deleted, and the actual values are not stored.

