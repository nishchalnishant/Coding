# Hashing — SDE-2+ Level

Map keys to indices via hash function for O(1) average lookup/insert/delete. SDE-3: collision strategies, load factor, consistent hashing (distributed), and when to use set vs map.

---

## 1. Concept Overview

**Problem space**: Frequency count, existence (set), two-sum (complement map), grouping (anagrams, by key), subarray sum = K (prefix sum → count map), LRU (map + DLL).

**When to use**: O(1) lookup by key; counting; deduplication; "find pair with sum" → complement in map.

---

## 2. Core Algorithms

### Hash Table Operations
- **Insert**: hash(key) → bucket; handle collision (chain or open addressing). Amortized O(1) with resizing.
- **Lookup/Delete**: Same hash; in chain traverse list; in open addressing probe. O(1) average.
- **Load factor** α = n/m; resize when α > threshold (e.g., 0.75); rehash all. Amortized O(1).

### Collision Handling
- **Chaining**: List (or tree) per bucket. Simple; cache-unfriendly for long chains.
- **Open addressing**: Linear/quadratic/double hashing. Better cache; clustering risk (linear).

### Subarray Sum Equals K
- Prefix sum P; for each P[j], count of indices i < j with P[i] = P[j] - K. Single pass with count map. O(N).

---

## 3. Advanced Variations

- **Consistent hashing**: Ring; keys and nodes hashed; assign key to first node clockwise. Minimal reassignment when nodes join/leave. Used in distributed caches.
- **Bloom filter**: Multiple hashes; set bits; no false negatives, possible false positives; no deletion (or counting bloom filter). O(k) space per element, k = hash count.
- **Rabin-Karp**: Rolling hash for substring; hash(s[i:j+1]) from hash(s[i:j]) in O(1). Collision check with equality.

### Edge Cases
- Empty array; single element; all same; negative K; prefix sum 0 (count as one: one subarray from start); integer overflow in sum.

---

## 4. Common Interview Problems

**Easy**: Two Sum, Valid Anagram, First Unique Character.  
**Medium**: Group Anagrams, Subarray Sum Equals K, Longest Consecutive Sequence, LRU Cache.  
**Hard**: Minimum Window Substring (map for count), Max Points on a Line (slope map), Substring with Concatenation of All Words.

---

## 5. Pattern Recognition

- **Complement map**: Two sum, 3-sum (fix one, two-sum on rest with set/map).
- **Frequency map**: Anagrams, majority, "at most K distinct" in window.
- **Prefix map**: Subarray sum = K (count of prefix sums); longest subarray with sum 0 (first occurrence of prefix).
- **Group by key**: Anagrams (sorted word or count tuple as key); design key for grouping.

---

## 6. Code Implementations

More SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/arrays.py` (prefix sums), `../../google-sde2/snippets/python/two_pointers_window.py` (window maps).

```python
def subarray_sum_equals_k(nums, k):
    count = 0
    prefix = 0
    seen = {0: 1}
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count

def group_anagrams(strs):
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```

---

## 7. Trade-offs & Scaling (optional)

- **Trade-offs**: Chaining vs open addressing — chaining simpler, open addressing better cache and one allocation. Load factor vs space vs collision rate.
- **Scalability**: Distributed systems → consistent hashing. Huge key space with small set → bloom filter. LRU at scale → sharded maps + TTL.
- **Concurrency**: ConcurrentHashMap-style locking or lock-free per bucket.

---

## 8. Interview Strategy

- **Identify**: "Pair with sum" → complement map. "Count subarray sum K" → prefix + count map. "Group by" → design key, map to list.
- **Common mistakes**: Forgetting prefix 0 (subarray from start); off-by-one in window problems; treating anagram key as string (tuple of counts or sorted).

---

## 9. Quick Revision

- **Tricks**: Prefix sum + map for subarray sum; sorted string or count tuple for anagram key; complement = target - x.
- **Edge cases**: K=0; prefix 0; empty; duplicates.
- **Pattern tip**: "Find pair" / "subarray sum" → map; "group" → key design.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **Group Anagrams** | Key: **sorted string** O(k log k) per word, or **count tuple** (26 or Unicode-sized array → tuple). Bucket by key. | **Unicode:** 26 letters assumption fails—use map or sort. **Space:** storing sorted string vs count vector. |
| **Longest Consecutive Sequence** | `set(nums)`; for each `x`, if `x-1` not in set, walk `x, x+1, ...` and count length. | **Amortized O(n):** each number in at most one chain. **Sort** is O(n log n)—worse but simpler. |
| **LRU Cache** | `HashMap` key→`Node`; **DLL** for recency (head=MRU, tail=LRU); `get`/`put` splice node; evict tail if size > cap. | **O(1)** only with DLL pointers correct; **capacity 1**; **update** existing key moves node. |
| **Subarray Sum Equals K** | `count[prefix]` frequency; `ans += count[prefix - K]`; `count[0]=1`. | Works with **negatives**; **sliding window** wrong for arbitrary integers. |
| **Contiguous Array** (equal 0/1) | Map **prefix balance** (count1−count0) to **first index**; max length with same balance. | Transform `0→-1` then same as “subarray sum 0”. |
| **Copy List with Random Pointer** | Map original→clone; two passes. Or **interleave** clones for O(1) extra. | **Random** pointer graph structure. |
| **Design HashMap** | **Chaining:** array of buckets, linked list on collision. **Open addressing:** linear/quadratic probe. | **Rehash** when load factor high; **`equals`/`hashCode`** contract in Java; **delete** tombstones in probing. |
| **Insert Delete GetRandom O(1)** | `map val→index` + **dynamic array**; swap-with-last on delete to keep indices compact. | **Duplicate** values need multiset or map to **set of indices** variant. |
| **Minimum Window Substring** | Sliding window + **need** counts for `t`; shrink when valid to minimize. | **Unicode** counts; **multiple** same chars in `t`. |
| **Logger Rate Limiter** | Map `msg → last_timestamp`; allow if `now ≥ last+10`. | **Prune** old entries if memory bound (follow-up). |

---

## See also

- [Array](array.md) — prefix sum + map  
- [String](../algorithms/string.md) — anagrams, rolling hash  
- [Graph](../algorithms/graph.md) — adjacency list is a hash map of lists
