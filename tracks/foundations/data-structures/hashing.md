# Hashing — SDE-3 Gold Standard

Map keys to indices via hash function for O(1) average lookup/insert/delete. SDE-3: collision strategies, load factor tuning, consistent hashing for distributed systems, and bloom filters.

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
> **The Click Moment**: "Find a **pair** with a given sum" — OR — "check if a **complement exists**" — OR — "**two sum / 3-sum / k-sum**". For each element, check if `target - element` is already in the map. This converts O(N²) brute force to O(N).

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
1. **3Sum / 4Sum**:
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
1. **Find All Anagrams in a String**:
   - **What (The Problem & Goal):** Find all starting indices of substrings in `s` that are anagrams of `p`.
   - **How (Intuition & Mental Model):** Sliding window + frequency map. Maintain a frequency map of the target string `p`. Slide a window of size `len(p)` across `s`, maintaining a running frequency map of the window. If the window's map equals `p`'s map, record the start index.
2. **Sort Characters By Frequency**:
   - **What (The Problem & Goal):** Sort a string in decreasing order based on the frequency of its characters.
   - **How (Intuition & Mental Model):** Count characters into a frequency map, then sort the characters based on their count (or use bucket sort where the index is the frequency). Rebuild the result string by appending `char * count`.
3. **Minimum Window Substring**:
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

## 3. SDE-3 Deep Dives

### Scalability: Consistent Hashing

> [!TIP]
> In a distributed cache (N nodes), naive `key % N` routing breaks when a node is added or removed — nearly all keys remap. **Consistent hashing** places both nodes and keys on a logical ring (hash → position on [0, 2^32)). Each key routes to the **first node clockwise** from its hash.
>
> Adding/removing one node only remaps `1/N` of the keys on average — vs `(N-1)/N` for naive hashing. Used in: Amazon DynamoDB, Apache Cassandra, Memcached (ketama), Redis Cluster.
>
> **Virtual nodes**: Each physical node appears K times on the ring with different hashes — improves load balance and handles heterogeneous node capacities.

### Scalability: Bloom Filters

> [!TIP]
> A bloom filter answers "is this element **probably** in the set?" with:
> - **No false negatives** — if it says "not present", definitely not present.
> - **Possible false positives** — if it says "present", it might not be.
>
> Space: O(K) bits per element where K = number of hash functions. Deletion not supported (use counting bloom filter).
>
> Used in: Google BigTable (avoid disk reads for missing rows), Cassandra (skip SSTables), Chrome's malware URL filter.

### Scalability: Rolling Hash for Large Text

> [!TIP]
> **Rabin-Karp rolling hash**: hash of sliding window updated in O(1) using:
> `hash(s[i+1:i+m+1]) = (hash(s[i:i+m]) - s[i] * base^(m-1)) * base + s[i+m]`
>
> On hash match, verify with direct string comparison to handle collisions. Use double hashing (two different primes) to reduce false-positive rate to ~1/p² for billion-character text.

```python
def rabin_karp_search(text: str, pattern: str) -> list[int]:
    n, m = len(text), len(pattern)
    if m == 0 or n < m:
        return []
        
    BASE, MOD = 256, 10**9 + 7
    # Precompute BASE^(m-1) % MOD for removing leading character
    base_m_minus_1 = pow(BASE, m - 1, MOD)
    
    pat_hash = 0
    text_hash = 0
    
    # Compute initial hash for pattern and first window of text
    for i in range(m):
        pat_hash = (pat_hash * BASE + ord(pattern[i])) % MOD
        text_hash = (text_hash * BASE + ord(text[i])) % MOD
        
    results = []
    
    # Slide the window
    for i in range(n - m + 1):
        if pat_hash == text_hash:
            # Hash match -> verify character by character to handle collision
            if text[i:i+m] == pattern:
                results.append(i)
                
        # Calculate hash for next window (remove leading char, add trailing char)
        if i < n - m:
            # (current_hash - leading_char * BASE^(m-1)) * BASE + next_char
            text_hash = (text_hash - ord(text[i]) * base_m_minus_1) % MOD
            text_hash = (text_hash * BASE + ord(text[i + m])) % MOD
            text_hash = (text_hash + MOD) % MOD  # Handle negative modulo in some languages
            
    return results
```

### Concurrency: Thread-Safe Hash Maps

> [!TIP]
> **Java**: `ConcurrentHashMap` uses **segment locking** (Java 7) or **CAS + `synchronized` per bucket** (Java 8+). Reads are lock-free; writes lock only the affected bucket. 16× better throughput than `Hashtable` under high concurrency.
>
> **Python**: `dict` is thread-safe for single operations in CPython (GIL), but not for multi-step sequences. Use `threading.Lock` around multi-step operations (check-then-insert, read-modify-write).
>
> **Lock-free hash map**: Use CAS on bucket head pointer for insert. Google's Abseil `flat_hash_map` and Facebook's Folly `AtomicHashMap` achieve lock-free reads and writes via open addressing with CAS probing.

> [!CAUTION]
> **Hash collision attacks**: If user-controlled input keys are hashed with a predictable hash function, attackers can craft inputs that all land in the same bucket → O(N) per lookup (hash DoS). Python randomizes `str`/`bytes` hash seeds per process (since 3.3) to mitigate this. For high-security systems, use SipHash or a HMAC-keyed hash.

### Trade-offs: Collision Strategies

| Strategy | Lookup | Space | Cache Efficiency | When to Prefer |
| :--- | :--- | :--- | :--- | :--- |
| Chaining (linked list) | O(1) avg, O(N) worst | O(N + M) | Poor (pointer chasing) | High load factor tolerated; simple implementation |
| Open addressing (linear) | O(1) avg | O(M) | Excellent | Low load factor; cache-sensitive systems |
| Open addressing (quadratic) | O(1) avg | O(M) | Good | Reduces primary clustering vs linear |
| Robin Hood hashing | O(1) avg | O(M) | Good | Minimizes max probe length; predictable latency |
| Cuckoo hashing | O(1) worst-case lookup | O(M) | Good | Guaranteed O(1) lookup critical |

---

## 4. Common Interview Problems

### Easy
- [Two Sum](../../google-sde2/PROBLEM_DETAILS.md#two-sum) — Complement map; single pass.
- **Valid Anagram** — `Counter(s) == Counter(t)`.
- **First Unique Character** — `Counter`; find first with count 1.

### Medium
- [Group Anagrams](../../google-sde2/PROBLEM_DETAILS.md#group-anagrams) — `sorted(word)` or count-tuple as key.
- [Subarray Sum Equals K](../../google-sde2/PROBLEM_DETAILS.md#subarray-sum-equals-k) — Prefix sum + count map; `seen = {0:1}`.
- [Longest Consecutive Sequence](../../google-sde2/PROBLEM_DETAILS.md#longest-consecutive-sequence) — Set lookup; only start chain from `x` if `x-1` not in set.
- [LRU Cache](../../google-sde2/PROBLEM_DETAILS.md#lru-cache) — Map + DLL; dummy head/tail.
- **Insert Delete GetRandom O(1)** — Map + array; swap-with-last on delete.
- **Contiguous Array (equal 0/1)** — Map `0→-1`; prefix sum + first-seen map.

### Hard
- **Minimum Window Substring** — Sliding window + need/have count maps.
- **Substring with Concatenation of All Words** — Fixed word-length window; multiset comparison.
- **Max Points on a Line** — Slope map with `gcd` normalization; handle vertical lines.
- **Design HashMap** — Chaining with prime-sized bucket array; handle resize.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **[Group Anagrams](../../google-sde2/PROBLEM_DETAILS.md#group-anagrams)** | Hash by Canonical Key | "Same letters, group together" | Key = `sorted(s)` or 26-count tuple | 26-array fails for Unicode; `sorted` is O(K log K) vs O(K) count. |
| **[Longest Consecutive](../../google-sde2/PROBLEM_DETAILS.md#longest-consecutive-sequence)** | "Longest streak, unsorted" | Set; only start chain if `x-1` not in set | Without the "start only" guard: O(N²); with it: amortized O(N). |
| **[LRU Cache](../../google-sde2/PROBLEM_DETAILS.md#lru-cache)** | "O(1) get/put with eviction" | Map `key→DLL node`; move on access; evict tail | Dummy head/tail eliminate all null-check edge cases in `_remove`. |
| **[Subarray Sum = K](../../google-sde2/PROBLEM_DETAILS.md#subarray-sum-equals-k)** | "Count subarrays with exact sum" | `seen={0:1}`; `count += seen[prefix-K]` | Works with negatives; sliding window doesn't. `seen[0]=1` is critical. |
| **Contiguous Array** | "Equal 0s and 1s in subarray" | Map `0→-1`; find longest zero-sum subarray | Reduces to "longest subarray with sum 0" — recognize the transformation. |
| **[Minimum Window](../../google-sde2/PROBLEM_DETAILS.md#minimum-window-substring)** | "Smallest window containing all of T" | Expand right until valid; shrink left while valid | `have == required` condition based on frequency saturation, not total count. |
| **Insert Delete GetRandom** | "O(1) all three operations" | Map + array; swap-with-last on delete | Update `_idx_map[last] = idx` before deleting the target's entry. |
| **Design HashMap** | "Hash map from scratch" | Array of buckets; chaining with linear scan | Prime capacity; handle `equals` by value; tombstone for open addressing delete. |
| **4Sum Count** | "Count quadruples summing to 0" | Hash sums of `A+B`; count complements in `C+D` | O(N²) space and time — better than O(N⁴) brute force. |
| **Max Points on a Line** | "Max collinear points" | Slope map per anchor; `gcd` normalize slope fraction | Vertical line (`dx=0`); same point (`dy=dx=0`); negative slopes in fraction. |
| **Two Sum** [E] | "Find two indices summing to target" | Complement map: store `val → index`; look up `target - val` | Return indices, not values — clarify. Handle same index: check before inserting. |
| **Valid Anagram** [E] | "Do two strings use same characters?" | Frequency count: increment for s, decrement for t; all zeros = anagram | `Counter(s) == Counter(t)` is clean; for follow-up (Unicode), same approach applies. |
| **Word Pattern** [E] | "Bijection between pattern chars and words" | Two maps: `char→word` and `word→char`; check both directions | Bijection requires both maps — `a→dog` and `b→dog` is invalid even if one map is fine. |
| **Longest Subarray with At Most K Distinct** [M] | "Sliding window, count distinct ≤ K" | Sliding window; map counts elements in window; shrink left when distinct > K | Decrement count and delete key only when count reaches 0 — not just on any shrink. |
| **Top K Frequent Words** [M] | "K most frequent strings, ties alphabetical" | Count frequencies; sort by `(-freq, word)`; take first K | Heap alternative: `heapq.nsmallest(k, ...)` with `(-freq, word)` avoids full sort. |
| **Ransom Note** [E] | "Can you build ransom string from magazine?" | Count magazine letters; check ransom has no unsatisfied letter | `Counter(ransomNote) - Counter(magazine)` — if any key remains, return False. |
| **Find Duplicate File in System** [M] | "Group files by content" | Map `content → [path/file]`; collect groups with ≥ 2 | Parse path+content from each entry; content is key, list of full paths is value. |
| **Longest Palindrome** [M] | "Longest palindrome buildable from letters" | Count frequencies; all even-count chars contribute fully; one odd-count char can be center | Add 1 if any odd-frequency char exists (it becomes the center). |
| **Isomorphic Strings** [E] | "Bijection between characters of s and t" | Map `s[i]→t[i]` and `t[i]→s[i]`; conflict = not isomorphic | Same structure as Word Pattern bijection — need both maps for correctness. |
| **Subarray Sum Equals K** [M] | "Count subarrays with exact sum K" | Prefix sum + map; `count += prefix_map[running_sum - K]`; init `prefix_map[0] = 1` | Sliding window fails with negatives — prefix map handles all cases. |
| **Longest Increasing Subsequence (via hash)** [M] | "LIS via patience sort + bisect" | Maintain `tails` list; `bisect_left` for replacement index | `tails` is not the LIS itself — only its length. Reconstruct via parent tracking if sequence needed. |

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

- [Array](array.md) — prefix sum + map for subarray problems
- [String](../algorithms/string.md) — anagram key design; rolling hash (Rabin-Karp)
- [Linked List](linked-list.md) — LRU cache DLL component
- [Patterns Master](../../../reference/patterns/patterns-master.md) — complement map and frequency map triggers
