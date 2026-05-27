---
tags: [coding, data-structures, hashing]
topic: hashing
difficulty: mixed
---

# Hashing Problems

---

## Complement Map

### Two Sum

> [!example] Problem
> Given an integer array `nums` and target, return indices of two numbers that sum to `target`. Exactly one solution exists.

> [!info] Approach
> - **WHY:** Brute force checks every pair — O(n²). We need to answer "have I seen the complement of this number?" in O(1).
> - **WHAT:** A hash map from value to index. For each `x`, check if `target - x` is already stored.
> - **HOW:** Single pass. Before storing `x`, look up `target - x`. If found, return `[seen[complement], i]`. Store `x → i` after checking to avoid using the same index twice.

> [!note]- Python Solution
> ```python
> def two_sum(nums: list[int], target: int) -> list[int]:
>     seen: dict[int, int] = {}
>     for i, x in enumerate(nums):
>         complement = target - x
>         if complement in seen:
>             return [seen[complement], i]
>         seen[x] = i
>     return []
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Sort + two pointers — O(n log n) and destroys original indices. Only valid if indices don't matter.

---

### 3Sum (hash-based)

> [!example] Problem
> Find all unique triplets `[a, b, c]` in `nums` with `a + b + c = 0`. No duplicate triplets.

> [!info] Approach
> - **WHY:** Reduce to two-sum: fix element `a`, find pair `(b, c)` with `b + c = -a` in the remaining array.
> - **WHAT:** Sort first to handle duplicates. For each index `i`, use a set to find complements in `nums[i+1:]`.
> - **HOW:** Sort. Skip duplicate values of `a`. For the inner scan, use a seen set: if `target - b` in seen, record triplet; else add `b` to seen.

> [!note]- Python Solution
> ```python
> def three_sum(nums: list[int]) -> list[list[int]]:
>     nums.sort()
>     result: list[list[int]] = []
>     for i in range(len(nums) - 2):
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue
>         target = -nums[i]
>         seen: set[int] = set()
>         j = i + 1
>         while j < len(nums):
>             complement = target - nums[j]
>             if complement in seen:
>                 result.append([nums[i], complement, nums[j]])
>                 while j + 1 < len(nums) and nums[j] == nums[j + 1]:
>                     j += 1
>             seen.add(nums[j])
>             j += 1
>     return result
> ```

> [!success] Complexity
> Time O(n²); Space O(n) for the seen set.

> [!tip] Alternatives
> Two-pointer after sort — same O(n²) time, O(1) extra space. Cleaner and preferred in interviews.

---

### 4Sum (hash-based)

> [!example] Problem
> Find all unique quadruplets summing to `target`.

> [!info] Approach
> - **WHY:** Reduce to 3Sum by fixing one element. Reduce 3Sum to 2Sum by fixing another.
> - **WHAT:** Sort + two outer loops (skip duplicates) + hash set inner two-sum.
> - **HOW:** Fix `nums[i]` and `nums[j]`. Inner target is `target - nums[i] - nums[j]`. Use seen set for two-sum on remaining elements.

> [!note]- Python Solution
> ```python
> def four_sum(nums: list[int], target: int) -> list[list[int]]:
>     nums.sort()
>     result: list[list[int]] = []
>     n = len(nums)
>     for i in range(n - 3):
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue
>         for j in range(i + 1, n - 2):
>             if j > i + 1 and nums[j] == nums[j - 1]:
>                 continue
>             need = target - nums[i] - nums[j]
>             seen: set[int] = set()
>             k = j + 1
>             while k < n:
>                 if need - nums[k] in seen:
>                     quad = [nums[i], nums[j], need - nums[k], nums[k]]
>                     result.append(quad)
>                     while k + 1 < n and nums[k] == nums[k + 1]:
>                         k += 1
>                 seen.add(nums[k])
>                 k += 1
>     return result
> ```

> [!success] Complexity
> Time O(n³); Space O(n).

> [!tip] Alternatives
> Four-pointer two-pointer approach O(n³) O(1) space. For exactly 4 arrays (4Sum II), hash all A+B sums then count complementary C+D — O(n²) time and space.

---

### Max Number of K-Sum Pairs

> [!example] Problem
> In one operation pick two elements summing to `k` and remove them. Return maximum number of operations.

> [!info] Approach
> - **WHY:** Each number can only pair once — we need to greedily match available complements, consuming them.
> - **WHAT:** Frequency map. For each `x`, check if `k - x` has remaining count. If yes, form a pair and decrement both counts.
> - **HOW:** Build `Counter`. For each unique `x`, pairs formed = `min(freq[x], freq[k - x])` if `x != k - x`, else `freq[x] // 2`. Sum all.

> [!note]- Python Solution
> ```python
> from collections import Counter
>
> def max_operations(nums: list[int], k: int) -> int:
>     freq = Counter(nums)
>     ops = 0
>     for x in list(freq.keys()):
>         complement = k - x
>         if complement not in freq:
>             continue
>         if x == complement:
>             ops += freq[x] // 2
>         elif x < complement:  # process each pair once
>             ops += min(freq[x], freq[complement])
>     return ops
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Sort + two pointers — O(n log n) time, O(1) space. Cleaner for an interview.

---

## Frequency Map

### Valid Anagram

> [!example] Problem
> Return true if `t` is an anagram of `s` (same characters, same counts).

> [!info] Approach
> - **WHY:** Anagram = identical character frequency distributions.
> - **WHAT:** Count character frequencies for both strings and compare.
> - **HOW:** `Counter(s) == Counter(t)`. Or use a single 26-element array: increment for `s`, decrement for `t`, check all zeros.

> [!note]- Python Solution
> ```python
> from collections import Counter
>
> def is_anagram(s: str, t: str) -> bool:
>     if len(s) != len(t):
>         return False
>     return Counter(s) == Counter(t)
> ```

> [!success] Complexity
> Time O(n); Space O(1) — at most 26 distinct characters.

> [!tip] Alternatives
> Sort both strings and compare — O(n log n), simpler but slower.

---

### First Unique Character in a String

> [!example] Problem
> Return the index of the first non-repeating character in `s`, or `-1` if none.

> [!info] Approach
> - **WHY:** Need both frequency (to identify unique) and order (to find the first).
> - **WHAT:** Count all frequencies, then scan left to right for the first character with count 1.
> - **HOW:** `Counter` in one pass; second pass finds first with count 1. Two O(n) passes.

> [!note]- Python Solution
> ```python
> from collections import Counter
>
> def first_uniq_char(s: str) -> int:
>     freq = Counter(s)
>     for i, ch in enumerate(s):
>         if freq[ch] == 1:
>             return i
>     return -1
> ```

> [!success] Complexity
> Time O(n); Space O(1) — 26-character alphabet.

> [!tip] Alternatives
> OrderedDict to track first occurrence — same complexity, more verbose.

---

### Group Anagrams

> [!example] Problem
> Group strings that are anagrams of each other.

> [!info] Approach
> - **WHY:** Anagrams share a canonical form. Grouping by canonical key clusters anagrams.
> - **WHAT:** Map from canonical key to list of strings. Key = sorted tuple of characters.
> - **HOW:** For each string, compute `tuple(sorted(s))` as key, append to `defaultdict(list)`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def group_anagrams(strs: list[str]) -> list[list[str]]:
>     groups: dict[tuple, list[str]] = defaultdict(list)
>     for s in strs:
>         key = tuple(sorted(s))
>         groups[key].append(s)
>     return list(groups.values())
> ```

> [!success] Complexity
> Time O(nk log k) where k = max string length; Space O(nk).

> [!tip] Alternatives
> 26-count tuple key — O(nk) time, avoids sort. Better for long strings with limited alphabet.

---

### Find All Anagrams in a String

> [!example] Problem
> Find all starting indices where a substring of `s` is an anagram of `p`.

> [!info] Approach
> - **WHY:** Check every substring of length `len(p)` — O(n * |p|) naively. Sliding window amortizes character counting.
> - **WHAT:** Maintain a frequency diff between current window and `p`. Track how many characters are "satisfied".
> - **HOW:** Use two Counter maps (window and p). Track `have` = number of chars where window count equals p count. When `have == len(p_count)`, record the start.

> [!note]- Python Solution
> ```python
> from collections import Counter
>
> def find_anagrams(s: str, p: str) -> list[int]:
>     if len(p) > len(s):
>         return []
>     p_count = Counter(p)
>     window = Counter(s[:len(p)])
>     result: list[int] = []
>     have = sum(1 for c in p_count if window[c] == p_count[c])
>     need = len(p_count)
>     if have == need:
>         result.append(0)
>     for i in range(len(p), len(s)):
>         # Add right character
>         right = s[i]
>         if right in p_count:
>             if window[right] == p_count[right]:
>                 have -= 1
>             window[right] += 1
>             if window[right] == p_count[right]:
>                 have += 1
>         # Remove left character
>         left = s[i - len(p)]
>         if left in p_count:
>             if window[left] == p_count[left]:
>                 have -= 1
>             window[left] -= 1
>             if window[left] == p_count[left]:
>                 have += 1
>         if have == need:
>             result.append(i - len(p) + 1)
>     return result
> ```

> [!success] Complexity
> Time O(n); Space O(1) — 26-character alphabet.

> [!tip] Alternatives
> Compare full Counter objects each step — O(n * 26), effectively O(n) but with higher constant.

---

### Sort Characters by Frequency

> [!example] Problem
> Sort a string in decreasing order of character frequency.

> [!info] Approach
> - **WHY:** Need characters ordered by count descending.
> - **WHAT:** Count frequencies, then rebuild string: higher-frequency characters first.
> - **HOW:** `Counter`, then sort by count descending, rebuild via `ch * count` concatenation.

> [!note]- Python Solution
> ```python
> from collections import Counter
>
> def frequency_sort(s: str) -> str:
>     freq = Counter(s)
>     sorted_chars = sorted(freq.keys(), key=lambda c: -freq[c])
>     return ''.join(c * freq[c] for c in sorted_chars)
> ```

> [!success] Complexity
> Time O(n + k log k) where k = distinct chars; Space O(n).

> [!tip] Alternatives
> Bucket sort by frequency — O(n) time. Index is frequency, bucket contains chars with that frequency. Iterate buckets high to low.

---

### Minimum Window Substring

> [!example] Problem
> Find the smallest substring of `s` containing all characters of `t` (with multiplicity).

> [!info] Approach
> - **WHY:** Enumerate all substrings — O(n²). Shrinkable window: expand right until valid, shrink left while still valid.
> - **WHAT:** `t_count` maps required frequencies. `window` tracks current window frequencies. `have` counts how many distinct chars are "satisfied" (window count >= required).
> - **HOW:** Expand right, update `have` when a char's count first meets requirement. Shrink left while `have == need`. Record minimum window during each valid state.

> [!note]- Python Solution
> ```python
> from collections import Counter
>
> def min_window(s: str, t: str) -> str:
>     if not t or not s:
>         return ''
>     t_count = Counter(t)
>     need = len(t_count)
>     window: dict[str, int] = {}
>     have = 0
>     left = 0
>     best_len = float('inf')
>     best_left = 0
>     for right, ch in enumerate(s):
>         window[ch] = window.get(ch, 0) + 1
>         if ch in t_count and window[ch] == t_count[ch]:
>             have += 1
>         while have == need:
>             if right - left + 1 < best_len:
>                 best_len = right - left + 1
>                 best_left = left
>             left_ch = s[left]
>             window[left_ch] -= 1
>             if left_ch in t_count and window[left_ch] < t_count[left_ch]:
>                 have -= 1
>             left += 1
>     return s[best_left:best_left + best_len] if best_len != float('inf') else ''
> ```

> [!success] Complexity
> Time O(n + m) where m = len(t); Space O(m).

> [!tip] Alternatives
> No fundamentally better approach. Optimized version: pre-filter `s` to only characters in `t` before sliding — reduces work when t is small and s has many irrelevant chars.

---

## Prefix Sum + Map

### Subarray Sum Equals K

> [!example] Problem
> Count the number of contiguous subarrays with sum equal to `k`. Array may contain negatives.

> [!info] Approach
> - **WHY:** Sliding window fails with negatives (sum can decrease when adding elements). Need a different invariant.
> - **WHAT:** prefix[j] - prefix[i] = k implies prefix[i] = prefix[j] - k. Count how many times each prefix sum has appeared.
> - **HOW:** Maintain running prefix sum. Before updating the map, check `seen[prefix - k]`. Initialize `seen = {0: 1}` to handle subarrays starting at index 0.

> [!note]- Python Solution
> ```python
> def subarray_sum(nums: list[int], k: int) -> int:
>     count = 0
>     prefix = 0
>     seen: dict[int, int] = {0: 1}
>     for x in nums:
>         prefix += x
>         count += seen.get(prefix - k, 0)
>         seen[prefix] = seen.get(prefix, 0) + 1
>     return count
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> O(n²) prefix sum array with nested loop — correct but slow. Sliding window — only works for positive numbers.

---

### Contiguous Array (Max Equal 0/1 Subarray)

> [!example] Problem
> Find the maximum length of a contiguous subarray with equal number of 0s and 1s.

> [!info] Approach
> - **WHY:** "Equal 0s and 1s" means the difference between 0-count and 1-count is 0 over the subarray.
> - **WHAT:** Replace 0 with -1. Problem becomes: longest subarray with sum 0. Use prefix sum + first-seen map.
> - **HOW:** Track running sum with 0→-1 transform. When `prefix` repeats, the subarray between the two occurrences has sum 0. Store `first_seen = {0: -1}` and compare `i - first_seen[prefix]`.

> [!note]- Python Solution
> ```python
> def find_max_length(nums: list[int]) -> int:
>     first_seen: dict[int, int] = {0: -1}
>     prefix = 0
>     best = 0
>     for i, x in enumerate(nums):
>         prefix += 1 if x == 1 else -1
>         if prefix in first_seen:
>             best = max(best, i - first_seen[prefix])
>         else:
>             first_seen[prefix] = i
>     return best
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> O(n²) brute force with 0-1 counts — no practical alternative.

---

### Make the Array Sum Divisible by P

> [!example] Problem
> Remove the shortest subarray so that the remaining sum is divisible by `P`.

> [!info] Approach
> - **WHY:** We want `(total - subarray_sum) % P == 0`, i.e., `subarray_sum % P == total % P`. Find the shortest subarray with that remainder.
> - **WHAT:** Prefix sums mod P. For each `j`, want the most recent `i` where `prefix[i] % P == (prefix[j] - rem) % P`.
> - **HOW:** `rem = sum(nums) % P`. If `rem == 0`, return 0. Use `seen = {0: -1}`. At each step store `prefix % P → i`. Look up `(prefix - rem) % P`.

> [!note]- Python Solution
> ```python
> def min_subarray(nums: list[int], p: int) -> int:
>     rem = sum(nums) % p
>     if rem == 0:
>         return 0
>     seen: dict[int, int] = {0: -1}
>     prefix = 0
>     best = len(nums)
>     for i, x in enumerate(nums):
>         prefix = (prefix + x) % p
>         target = (prefix - rem) % p
>         if target in seen:
>             best = min(best, i - seen[target])
>         seen[prefix] = i
>     return best if best < len(nums) else -1
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> No better approach — this is the canonical O(n) solution.

---

### Subarray Sums Divisible by K

> [!example] Problem
> Count the number of subarrays whose sum is divisible by `K`.

> [!info] Approach
> - **WHY:** `(prefix[j] - prefix[i]) % K == 0` iff `prefix[j] % K == prefix[i] % K`. Count pairs of equal remainders.
> - **WHAT:** Frequency map of prefix sums mod K. Each pair of indices with equal remainder contributes one valid subarray.
> - **HOW:** `seen = {0: 1}`. For each element, compute `prefix % K` (handle negatives: `% K` in Python already returns non-negative). Add `seen[(prefix % K)]` to count. Increment map.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def subarrays_div_by_k(nums: list[int], k: int) -> int:
>     count = 0
>     prefix = 0
>     seen: dict[int, int] = defaultdict(int)
>     seen[0] = 1
>     for x in nums:
>         prefix = (prefix + x) % k
>         count += seen[prefix]
>         seen[prefix] += 1
>     return count
> ```

> [!success] Complexity
> Time O(n); Space O(k) — at most k distinct remainders.

> [!tip] Alternatives
> Prefix array + O(n²) nested loop — correct, slow. This is optimal.

---

## Design

### LRU Cache

> [!example] Problem
> Design a cache with O(1) `get` and `put` operations, evicting the Least Recently Used item when capacity is exceeded.

> [!info] Approach
> - **WHY:** O(1) access requires a hash map. O(1) eviction (remove oldest access) requires a doubly linked list (DLL) so we can splice out any node in O(1).
> - **WHAT:** `key → DLL node` map for O(1) lookup. DLL ordered by recency: head = MRU, tail = LRU. Dummy head and tail eliminate null checks.
> - **HOW:** On `get`: look up node, move to front, return val. On `put`: if key exists update and move to front; else insert at front; if over capacity evict tail.

> [!note]- Python Solution
> ```python
> class DLLNode:
>     def __init__(self, key: int = 0, val: int = 0) -> None:
>         self.key = key
>         self.val = val
>         self.prev: 'DLLNode | None' = None
>         self.next: 'DLLNode | None' = None
>
> class LRUCache:
>     def __init__(self, capacity: int) -> None:
>         self.cap = capacity
>         self.map: dict[int, DLLNode] = {}
>         self.head = DLLNode()  # dummy MRU
>         self.tail = DLLNode()  # dummy LRU
>         self.head.next = self.tail
>         self.tail.prev = self.head
>
>     def _remove(self, node: DLLNode) -> None:
>         node.prev.next = node.next  # type: ignore
>         node.next.prev = node.prev  # type: ignore
>
>     def _insert_front(self, node: DLLNode) -> None:
>         node.next = self.head.next
>         node.prev = self.head
>         self.head.next.prev = node  # type: ignore
>         self.head.next = node
>
>     def get(self, key: int) -> int:
>         if key not in self.map:
>             return -1
>         node = self.map[key]
>         self._remove(node)
>         self._insert_front(node)
>         return node.val
>
>     def put(self, key: int, value: int) -> None:
>         if key in self.map:
>             self._remove(self.map[key])
>         node = DLLNode(key, value)
>         self.map[key] = node
>         self._insert_front(node)
>         if len(self.map) > self.cap:
>             lru = self.tail.prev  # type: ignore
>             self._remove(lru)
>             del self.map[lru.key]
> ```

> [!success] Complexity
> Time O(1) all ops; Space O(capacity).

> [!tip] Alternatives
> Python `OrderedDict` — `move_to_end` and `popitem(last=False)` give same semantics in 5 lines. Mention in interviews, but know the DLL approach.

---

### Insert Delete GetRandom O(1)

> [!example] Problem
> Design a set with O(1) `insert`, `remove`, and `getRandom` (uniform).

> [!info] Approach
> - **WHY:** Hash map gives O(1) insert/delete/lookup. But random access requires an array. Combining both enables all three in O(1).
> - **WHAT:** `vals` list for O(1) random access. `idx_map` maps value to its index in `vals`. Delete: swap target with last element to avoid gaps, then pop.
> - **HOW:** Insert appends to list and stores index in map. Remove swaps target with last element, updates map for the moved element, pops the list, deletes map entry for removed value.

> [!note]- Python Solution
> ```python
> import random
>
> class RandomizedSet:
>     def __init__(self) -> None:
>         self._vals: list[int] = []
>         self._idx: dict[int, int] = {}
>
>     def insert(self, val: int) -> bool:
>         if val in self._idx:
>             return False
>         self._idx[val] = len(self._vals)
>         self._vals.append(val)
>         return True
>
>     def remove(self, val: int) -> bool:
>         if val not in self._idx:
>             return False
>         idx = self._idx[val]
>         last = self._vals[-1]
>         self._vals[idx] = last
>         self._idx[last] = idx
>         self._vals.pop()
>         del self._idx[val]
>         return True
>
>     def get_random(self) -> int:
>         return random.choice(self._vals)
> ```

> [!success] Complexity
> Time O(1) amortized all ops; Space O(n).

> [!tip] Alternatives
> No simpler structure achieves O(1) for all three. The swap-with-last trick is the canonical insight.

---

### Design HashMap

> [!example] Problem
> Implement a hash map from scratch with `put`, `get`, and `remove`.

> [!info] Approach
> - **WHY:** Understand collision resolution. Chaining: each bucket holds a list of `(key, value)` pairs.
> - **WHAT:** Array of `capacity` buckets. Hash function: `key % capacity` with prime capacity to reduce clustering.
> - **HOW:** `put` scans bucket for existing key (update) or appends. `get` scans for key, returns -1 if absent. `remove` filters out the key.

> [!note]- Python Solution
> ```python
> class MyHashMap:
>     def __init__(self, capacity: int = 1009) -> None:  # prime capacity
>         self._cap = capacity
>         self._buckets: list[list[tuple[int, int]]] = [[] for _ in range(capacity)]
>
>     def _idx(self, key: int) -> int:
>         return key % self._cap
>
>     def put(self, key: int, value: int) -> None:
>         bucket = self._buckets[self._idx(key)]
>         for i, (k, _) in enumerate(bucket):
>             if k == key:
>                 bucket[i] = (key, value)
>                 return
>         bucket.append((key, value))
>
>     def get(self, key: int) -> int:
>         for k, v in self._buckets[self._idx(key)]:
>             if k == key:
>                 return v
>         return -1
>
>     def remove(self, key: int) -> None:
>         idx = self._idx(key)
>         self._buckets[idx] = [(k, v) for k, v in self._buckets[idx] if k != key]
> ```

> [!success] Complexity
> Time O(1) average, O(n) worst (all keys collide); Space O(n + capacity).

> [!tip] Alternatives
> Open addressing (linear probing) — better cache locality, needs tombstones for delete. Robin Hood hashing — minimizes max probe length.

---

## Miscellaneous

### Longest Consecutive Sequence

> [!example] Problem
> Find the length of the longest consecutive elements sequence in an unsorted array. O(n) required.

> [!info] Approach
> - **WHY:** Sorting is O(n log n). We need O(n). Hash set enables O(1) membership checks.
> - **WHAT:** Only start counting a sequence from `x` if `x - 1` is NOT in the set. This prevents redundant work — each element is visited at most twice total.
> - **HOW:** Build set. For each `x`, if `x - 1 not in set`, extend the chain `x, x+1, x+2, ...` while each successor is in the set.

> [!note]- Python Solution
> ```python
> def longest_consecutive(nums: list[int]) -> int:
>     num_set = set(nums)
>     best = 0
>     for x in num_set:
>         if x - 1 not in num_set:  # only start from sequence heads
>             length = 1
>             while x + length in num_set:
>                 length += 1
>             best = max(best, length)
>     return best
> ```

> [!success] Complexity
> Time O(n) — each element processed at most twice; Space O(n).

> [!tip] Alternatives
> Sort + scan — O(n log n), simpler but doesn't meet the O(n) constraint. Union-Find — O(n α(n)), correct but overkill.

---

### Substring with Concatenation of All Words

> [!example] Problem
> Find all starting indices in `s` where a substring is a concatenation of all words in `words` (each used exactly once, in any order).

> [!info] Approach
> - **WHY:** Words are fixed length. Enumerate all starting offsets 0 to `word_len - 1`. For each, slide a window of `num_words` words and compare word frequency maps.
> - **WHAT:** `words_count` = Counter of required words. Slide a window by one word at a time. Track current window word frequencies and a `have` count.
> - **HOW:** For each offset in `[0, word_len)`, maintain a sliding window of exactly `num_words * word_len` characters. Add/remove one word at a time from window ends.

> [!note]- Python Solution
> ```python
> from collections import Counter
>
> def find_substring(s: str, words: list[str]) -> list[int]:
>     if not s or not words:
>         return []
>     wlen = len(words[0])
>     num_words = len(words)
>     total = wlen * num_words
>     words_count = Counter(words)
>     result: list[int] = []
>     for offset in range(wlen):
>         window: dict[str, int] = {}
>         have = 0
>         left = offset
>         for right in range(offset, len(s) - wlen + 1, wlen):
>             word = s[right:right + wlen]
>             if word in words_count:
>                 window[word] = window.get(word, 0) + 1
>                 if window[word] == words_count[word]:
>                     have += 1
>                 while window[word] > words_count[word]:
>                     left_word = s[left:left + wlen]
>                     if window[left_word] == words_count.get(left_word, 0):
>                         have -= 1
>                     window[left_word] -= 1
>                     left += wlen
>                 if have == len(words_count):
>                     result.append(left)
>             else:
>                 window.clear()
>                 have = 0
>                 left = right + wlen
>     return result
> ```

> [!success] Complexity
> Time O(n * word_len); Space O(num_words).

> [!tip] Alternatives
> Brute force generating all permutations — O(n * n! * word_len), infeasible. The sliding window per offset is optimal.

---

### Max Points on a Line

> [!example] Problem
> Given `n` points, find the maximum number of points that lie on the same straight line.

> [!info] Approach
> - **WHY:** For each pair of points, their line is defined by slope. Points on the same line share the same slope relative to a fixed anchor.
> - **WHAT:** Fix each point as anchor. For all other points, compute the slope as a reduced fraction `(dy/gcd, dx/gcd)`. Count max slope frequency.
> - **HOW:** For each anchor `i`, build a slope map. Use `gcd` to normalize: slope = `(dy // g, dx // g)`. Handle vertical lines (`dx == 0`) and same-point duplicates separately.

> [!note]- Python Solution
> ```python
> from math import gcd
> from collections import defaultdict
>
> def max_points(points: list[list[int]]) -> int:
>     n = len(points)
>     if n <= 2:
>         return n
>     best = 2
>     for i in range(n):
>         slopes: dict[tuple, int] = defaultdict(int)
>         duplicates = 0
>         for j in range(i + 1, n):
>             dx = points[j][0] - points[i][0]
>             dy = points[j][1] - points[i][1]
>             if dx == 0 and dy == 0:
>                 duplicates += 1
>                 continue
>             g = gcd(abs(dx), abs(dy))
>             dx //= g; dy //= g
>             # Normalize sign: keep dx positive (or dy positive if dx == 0)
>             if dx < 0 or (dx == 0 and dy < 0):
>                 dx, dy = -dx, -dy
>             slopes[(dx, dy)] += 1
>         local_best = max(slopes.values(), default=0) + 1 + duplicates
>         best = max(best, local_best)
>     return best
> ```

> [!success] Complexity
> Time O(n² log(max_coord)); Space O(n).

> [!tip] Alternatives
> O(n³) brute force checking all triples for collinearity — correct but cubic. The slope map approach is canonical.

---

## See Also

[[array]] | [[sliding-window]] | [[string]] | [[two-pointers]]
