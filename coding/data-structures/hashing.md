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

### Top K Frequent Elements

> [!example] Problem
> Given an integer array `nums` and integer `k`, return the `k` most frequent elements. Order of output does not matter.

> [!info] Approach
> - **WHY:** Sorting by frequency is O(n log n). Bucket sort on frequency gives O(n).
> - **WHAT:** Count frequencies, then place each number into a bucket indexed by its frequency. Collect from the highest-frequency buckets downward.
> - **HOW:** `Counter` → buckets list of size `n+1` where `buckets[f]` holds all numbers with frequency `f`. Iterate from index `n` down and collect until we have `k` elements.

> [!note]- Python Solution
> ```python
> from collections import Counter
>
> def top_k_frequent(nums: list[int], k: int) -> list[int]:
>     freq = Counter(nums)
>     buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
>     for num, count in freq.items():
>         buckets[count].append(num)
>     result: list[int] = []
>     for i in range(len(buckets) - 1, 0, -1):
>         for num in buckets[i]:
>             result.append(num)
>             if len(result) == k:
>                 return result
>     return result
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> `heapq.nlargest(k, freq, key=freq.get)` — O(n log k), clean one-liner but not O(n). QuickSelect on frequencies — O(n) average, O(n²) worst.

---

### Subdomain Visit Count

> [!example] Problem
> Each entry in `cpdomains` is `"count domain"`. A visit to `a.b.c` also counts as a visit to `b.c` and `c`. Return the count for every subdomain.

> [!info] Approach
> - **WHY:** Each domain contributes its count to itself and all suffix domains. Aggregate with a frequency map.
> - **WHAT:** Parse count and domain. Split domain on `.` and generate all suffixes. Accumulate counts.
> - **HOW:** For `"9 discuss.leetcode.com"` add 9 to `discuss.leetcode.com`, `leetcode.com`, and `com`. Format output as `"count domain"` strings.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def subdomain_visits(cpdomains: list[str]) -> list[str]:
>     counts: dict[str, int] = defaultdict(int)
>     for entry in cpdomains:
>         count_str, domain = entry.split()
>         count = int(count_str)
>         parts = domain.split('.')
>         for i in range(len(parts)):
>             subdomain = '.'.join(parts[i:])
>             counts[subdomain] += count
>     return [f"{v} {k}" for k, v in counts.items()]
> ```

> [!success] Complexity
> Time O(n * L) where L = max domain depth; Space O(n * L).

> [!tip] Alternatives
> No significantly different approach — the suffix enumeration is inherent.

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

### Longest Subarray with Sum K

> [!example] Problem
> Find the maximum length of a contiguous subarray with sum equal to `k`. Array may contain negatives.

> [!info] Approach
> - **WHY:** Sliding window fails with negatives. Prefix sum trick: subarray `[i+1, j]` has sum `k` iff `prefix[j] - prefix[i] = k`, i.e., `prefix[i] = prefix[j] - k`.
> - **WHAT:** For maximum length, store the *first* occurrence of each prefix sum. When we see `prefix - k` again later, the gap is as large as possible.
> - **HOW:** `first_seen = {0: -1}`. At index `i`, if `prefix - k` in map, update `best = max(best, i - first_seen[prefix - k])`. Only insert prefix if not already present (preserve earliest index).

> [!note]- Python Solution
> ```python
> def max_subarray_len(nums: list[int], k: int) -> int:
>     first_seen: dict[int, int] = {0: -1}
>     prefix = 0
>     best = 0
>     for i, x in enumerate(nums):
>         prefix += x
>         if prefix - k in first_seen:
>             best = max(best, i - first_seen[prefix - k])
>         if prefix not in first_seen:
>             first_seen[prefix] = i
>     return best
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> For non-negative arrays only: sliding window O(n) O(1). For the general case this prefix-map approach is optimal.

---

### Count Number of Nice Subarrays

> [!example] Problem
> Count subarrays with exactly `k` odd numbers (LC 1248).

> [!info] Approach
> - **WHY:** Map odd/even to 1/0. Problem becomes: count subarrays with sum exactly `k` — identical to LC 560.
> - **WHAT:** Parity prefix sum. `prefix[j] - prefix[i] = k` means subarray `[i+1, j]` has exactly `k` odd numbers.
> - **HOW:** `seen = {0: 1}`. Running sum increments by 1 for odd elements, 0 for even. Look up `prefix - k` in `seen` before updating map.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def number_of_subarrays(nums: list[int], k: int) -> int:
>     seen: dict[int, int] = defaultdict(int)
>     seen[0] = 1
>     prefix = 0
>     count = 0
>     for x in nums:
>         prefix += x & 1  # 1 if odd, 0 if even
>         count += seen[prefix - k]
>         seen[prefix] += 1
>     return count
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> `exactly(k) = at_most(k) - at_most(k-1)` sliding window decomposition — O(n) O(1) space, useful when "at most k" variant is easy.

---

### Binary Subarrays with Sum

> [!example] Problem
> Binary array `nums`, count subarrays with sum equal to `goal` (LC 930).

> [!info] Approach
> - **WHY:** Same prefix sum framework as LC 560. Binary values make the prefix strictly non-decreasing.
> - **WHAT:** `seen = {0: 1}`. At each index track running sum; add `seen[prefix - goal]` to answer.
> - **HOW:** Identical to subarray sum equals k. The binary constraint doesn't change the algorithm, only guarantees prefix is non-negative.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def num_subarrays_with_sum(nums: list[int], goal: int) -> int:
>     seen: dict[int, int] = defaultdict(int)
>     seen[0] = 1
>     prefix = 0
>     count = 0
>     for x in nums:
>         prefix += x
>         count += seen[prefix - goal]
>         seen[prefix] += 1
>     return count
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> `at_most(goal) - at_most(goal - 1)` with sliding window — O(n) O(1) space, exploits binary non-negativity.

---

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

## Set Operations

### Contains Duplicate

> [!example] Problem
> Return `true` if any value appears at least twice in `nums` (LC 217).

> [!info] Approach
> - **WHY:** Membership check in O(1) is exactly what a hash set provides.
> - **WHAT:** Insert elements one by one. If an element is already in the set, a duplicate exists.
> - **HOW:** Single pass: if `x in seen` return True; else `seen.add(x)`. Short-circuits on first duplicate.

> [!note]- Python Solution
> ```python
> def contains_duplicate(nums: list[int]) -> bool:
>     seen: set[int] = set()
>     for x in nums:
>         if x in seen:
>             return True
>         seen.add(x)
>     return False
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> `len(nums) != len(set(nums))` — one-liner, same complexity. Sort and scan adjacent pairs — O(n log n) O(1) space.

---

### Intersection of Two Arrays

> [!example] Problem
> Return an array of unique elements that appear in both `nums1` and `nums2` (LC 349).

> [!info] Approach
> - **WHY:** Set intersection directly models the problem. O(1) membership check makes it efficient.
> - **WHAT:** Convert both to sets. Return their intersection as a list.
> - **HOW:** `set(nums1) & set(nums2)` in Python. For an explicit approach: iterate the smaller set, check membership in the larger.

> [!note]- Python Solution
> ```python
> def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
>     set1, set2 = set(nums1), set(nums2)
>     return list(set1 & set2)
> ```

> [!success] Complexity
> Time O(n + m); Space O(min(n, m)) for the result.

> [!tip] Alternatives
> Sort both + two pointers — O(n log n + m log m), O(1) extra space. Use for follow-up "what if arrays are sorted?"

---

### Two Sum Less Than K

> [!example] Problem
> Find the maximum sum of two distinct elements in `nums` that is strictly less than `k`. Return -1 if no such pair exists.

> [!info] Approach
> - **WHY:** We want the largest valid pair sum — greedy with two pointers after sorting is cleanest. Hash set alternative: for each `x`, check if any value in `[k - x - (n-1)..k - x - 1]` is present.
> - **WHAT:** Sort. Use two pointers. If `nums[l] + nums[r] < k`, record sum and advance `l`. Else shrink `r`.
> - **HOW:** After sort, `l = 0`, `r = n - 1`. Converge inward. Track `best = max(best, sum)` when `sum < k`.

> [!note]- Python Solution
> ```python
> def two_sum_less_than_k(nums: list[int], k: int) -> int:
>     nums.sort()
>     l, r = 0, len(nums) - 1
>     best = -1
>     while l < r:
>         s = nums[l] + nums[r]
>         if s < k:
>             best = max(best, s)
>             l += 1
>         else:
>             r -= 1
>     return best
> ```

> [!success] Complexity
> Time O(n log n); Space O(1).

> [!tip] Alternatives
> Hash set per element: O(n * k) worst case — avoid. Counting sort if values are bounded (e.g., 1–1000): O(max_val) space.

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

## Rolling Hash / Dedup

### Longest Duplicate Substring (Rabin-Karp)

> [!example] Problem
> Find the longest substring that appears at least twice in `s`. Return `""` if none. (LC 1044)

> [!info] Approach
> - **WHY:** Binary search on length `L`: if a duplicate of length `L` exists, so does one of length `L-1`. Check feasibility via rolling hash to avoid O(n²) string comparison.
> - **WHAT:** Binary search `L` in `[1, n-1]`. For each `L`, use Rabin-Karp: compute polynomial rolling hash for every window of length `L`; if any hash repeats, verify the match (hash collision guard).
> - **HOW:** Hash = `sum(ord(s[i]) * base^(L-1-i)) % mod` for window. Rolling update: `new_hash = (old_hash * base - ord(left) * base^L + ord(right)) % mod`. Store hashes in a set. Return the window on collision.

> [!note]- Python Solution
> ```python
> def longest_dup_substring(s: str) -> str:
>     n = len(s)
>     BASE, MOD = 31, (1 << 61) - 1  # Mersenne prime
>     nums = [ord(c) - ord('a') + 1 for c in s]
>
>     def search(length: int) -> str:
>         h = 0
>         power = pow(BASE, length, MOD)
>         for i in range(length):
>             h = (h * BASE + nums[i]) % MOD
>         seen: dict[int, list[int]] = {h: [0]}
>         for i in range(1, n - length + 1):
>             h = (h * BASE - nums[i - 1] * power + nums[i + length - 1]) % MOD
>             if h in seen:
>                 candidate = s[i:i + length]
>                 for start in seen[h]:
>                     if s[start:start + length] == candidate:
>                         return candidate
>                 seen[h].append(i)
>             else:
>                 seen[h] = [i]
>         return ""
>
>     lo, hi, result = 1, n - 1, ""
>     while lo <= hi:
>         mid = (lo + hi) // 2
>         found = search(mid)
>         if found:
>             result = found
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return result
> ```

> [!success] Complexity
> Time O(n log n) expected; Space O(n).

> [!tip] Alternatives
> Suffix array + LCP array — O(n log n) deterministic, no hash collisions. Binary search + suffix array is the production approach.

---

### Find Duplicate File in System

> [!example] Problem
> Given a list of path strings `"root/dir file1.txt(content1) file2.txt(content2)"`, group files with identical content (LC 609).

> [!info] Approach
> - **WHY:** Files with the same content are duplicates. Content is the natural key for a hash map.
> - **WHAT:** Parse each string into `(directory, filename, content)`. Group file paths by content string.
> - **HOW:** For each entry split on spaces: first token is directory, rest are `name(content)` tokens. Extract content between `(` and `)`. Map `content → list[full_path]`. Return groups with size ≥ 2.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def find_duplicate(paths: list[str]) -> list[list[str]]:
>     content_map: dict[str, list[str]] = defaultdict(list)
>     for path in paths:
>         parts = path.split()
>         directory = parts[0]
>         for file_entry in parts[1:]:
>             name, _, content = file_entry.partition('(')
>             content = content.rstrip(')')
>             content_map[content].append(f"{directory}/{name}")
>     return [files for files in content_map.values() if len(files) > 1]
> ```

> [!success] Complexity
> Time O(total characters); Space O(total characters).

> [!tip] Alternatives
> Real-world: hash file contents (MD5/SHA) rather than store raw content — avoids loading entire files. Then group by hash, verify collisions by byte comparison.

---

### 4Sum II

> [!example] Problem
> Given four integer arrays `A, B, C, D`, count tuples `(i, j, k, l)` such that `A[i] + B[j] + C[k] + D[l] == 0` (LC 454).

> [!info] Approach
> - **WHY:** Brute force O(n⁴). Split into two pairs: count all `A[i] + B[j]` sums, then for each `C[k] + D[l]` check if its negation was seen.
> - **WHAT:** Hash map `ab_sum → count`. Then iterate all C, D pairs and look up `-(C[k] + D[l])`.
> - **HOW:** Two nested loops for AB → Counter. Two nested loops for CD → look up complement. Sum all matching counts.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def four_sum_count(nums1: list[int], nums2: list[int],
>                    nums3: list[int], nums4: list[int]) -> int:
>     ab: dict[int, int] = defaultdict(int)
>     for a in nums1:
>         for b in nums2:
>             ab[a + b] += 1
>     count = 0
>     for c in nums3:
>         for d in nums4:
>             count += ab[-(c + d)]
>     return count
> ```

> [!success] Complexity
> Time O(n²); Space O(n²).

> [!tip] Alternatives
> Meet-in-the-middle generalizes: split k arrays into two halves of k/2, hash one half's sums, probe with the other. Always yields O(n^(k/2)) for k-sum variants.

---

## See Also

[[array]] | [[sliding-window]] | [[string]] | [[two-pointers]]
### Ransom Note

> [!example] Problem
> Determine whether a ransom note can be constructed from the letters in a magazine string.

> [!info] Approach
> - **WHY:** This is a frequency matching problem; each character in the note must be available at least as many times as needed.
> - **WHAT:** Count letters in the magazine and decrement as you consume letters from the note.
> - **HOW:** Use a hash map or `Counter`; if any needed character drops below zero, return false.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def can_construct(ransom_note: str, magazine: str) -> bool:
>     count = Counter(magazine)
>     for ch in ransom_note:
>         if count[ch] == 0:
>             return False
>         count[ch] -= 1
>     return True
> ```

> [!success] Complexity
> O(m + n) time, O(1) extra space for lowercase letters.

> [!tip] Alternatives
> Sort + two pointers works too, but frequency counting is the direct interview answer.

---

## Prefix Sum + Hashing

### Subarray Sums Divisible by K (LC 974)

> [!example] Problem
> Given an integer array and an integer `k`, return the number of non-empty subarrays whose sum is divisible by `k`.

> [!info] Approach
> - **WHY:** `sum(i..j) % k == 0` iff `prefix[j] % k == prefix[i-1] % k`. So we count pairs of equal remainders among prefix sums.
> - **WHAT:** Track `remainder -> count` in a hash map. For each prefix sum, look up how many prior prefix sums had the same remainder mod `k`.
> - **HOW:** Initialize `{0: 1}`. For each element, compute `remainder = running_sum % k`. In Python, `%` always returns non-negative values, so no adjustment needed. Add `count_map[remainder]` to the answer, then increment `count_map[remainder]`.

> [!note]- Python Solution
> ```python
> def subarrays_div_by_k(nums: list[int], k: int) -> int:
>     count_map = {0: 1}
>     running_sum = 0
>     total = 0
>     for num in nums:
>         running_sum += num
>         remainder = running_sum % k
>         total += count_map.get(remainder, 0)
>         count_map[remainder] = count_map.get(remainder, 0) + 1
>     return total
> ```

> [!success] Complexity
> Time O(n), Space O(k).

> [!tip] Alternatives
> - O(n²) brute force: enumerate all subarray sums and check divisibility.
> - Key difference from "Subarray Sum Equals K": here we group by remainder, not by exact prefix sum value — the count map has at most `k` keys.

---

### Contiguous Array (LC 525)

> [!example] Problem
> Given a binary array, find the maximum length subarray with equal numbers of 0s and 1s.

> [!info] Approach
> - **WHY:** Map 0 → -1. Now "equal 0s and 1s" means "subarray sum = 0". A subarray `[i+1..j]` sums to zero iff `prefix[j] == prefix[i]`. We want the maximum `j - i` among equal prefix sums.
> - **WHAT:** Hash map of `prefix_sum -> first_index`. When a prefix sum repeats, the distance gives a candidate max length.
> - **HOW:** Initialize `{0: -1}`. For each index `i`, update `prefix`. If `prefix` is in the map, update `max_len = max(max_len, i - first_seen[prefix])`. Otherwise record `first_seen[prefix] = i`.

> [!note]- Python Solution
> ```python
> def find_max_length(nums: list[int]) -> int:
>     first_seen = {0: -1}
>     prefix = 0
>     max_len = 0
>     for i, num in enumerate(nums):
>         prefix += 1 if num == 1 else -1
>         if prefix in first_seen:
>             max_len = max(max_len, i - first_seen[prefix])
>         else:
>             first_seen[prefix] = i
>     return max_len
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Brute force O(n²): enumerate all subarrays, count 0s and 1s.
> - Key insight: store only the *first* occurrence of each prefix sum to maximise the gap.

---

### 4Sum II (LC 454)

> [!example] Problem
> Given four integer arrays A, B, C, D of the same length n, count tuples `(i, j, k, l)` such that `A[i] + B[j] + C[k] + D[l] == 0`.

> [!info] Approach
> - **WHY:** O(n⁴) brute force is too slow. Split the four arrays into two pairs. All pairwise sums from (A, B) can be stored in a hash map; then for each pairwise sum from (C, D), look up its negative.
> - **WHAT:** Build a frequency map of `a + b` for all pairs from A and B. Then for each pair `(c, d)`, query the map for `-(c + d)`.
> - **HOW:** `ab_count = Counter(a + b for a in A for b in B)`. Then `total = sum(ab_count[-(c + d)] for c in C for d in D)`.

> [!note]- Python Solution
> ```python
> from collections import Counter
>
> def four_sum_count(nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]) -> int:
>     ab_count = Counter(a + b for a in nums1 for b in nums2)
>     total = 0
>     for c in nums3:
>         for d in nums4:
>             total += ab_count.get(-(c + d), 0)
>     return total
> ```

> [!success] Complexity
> Time O(n²), Space O(n²).

> [!tip] Alternatives
> - No fundamentally better approach for the general case — O(n²) is optimal here.
> - Contrast with 4Sum (LC 18): there, the array is fixed, so sorting + two pointers avoids O(n²) space. Here, four separate arrays make that approach impractical.

---

## See Also

[[array]] | [[two-pointers]] | [[sliding-window]] | [[sorting]]
