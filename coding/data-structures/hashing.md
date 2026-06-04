---
tags: [coding, data-structures, hashing]
topic: hashing
difficulty: mixed
---

# Hashing Problems


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## Complement Map

### Two Sum `🔥 Google`

> [!example] Problem
> Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
> You may assume that each input would have exactly one solution, and you may not use the same element twice.
> You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [2,7,11,15], target = 9
> Output: [0,1]
> Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,4], target = 6
> Output: [1,2]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [3,3], target = 6
> Output: [0,1]
> ```
> 
> **Constraints:**
> - 2 <= nums.length <= 10^4
> - -10^9 <= nums[i] <= 10^9
> - -10^9 <= target <= 10^9
> - Only one valid answer exists.

> [!info] Approach
> Brute force checks every pair — O(n²). We need to answer "have I seen the complement of this number?" in O(1). A hash map from value to index. For each `x`, check if `target - x` is already stored. Single pass. Before storing `x`, look up `target - x`. If found, return `[seen[complement], i]`. Store `x → i` after checking to avoid using the same index twice.

> [!note]- Python Solution
> ```python
> def two_sum(nums, target):
>     seen = {}
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

### 3Sum (hash-based) `🔥 Google`

> [!example] Problem
> Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
> Notice that the solution set must not contain duplicate triplets.
> 
> **Example 1:**
> ```
> Input: nums = [-1,0,1,2,-1,-4]
> Output: [[-1,-1,2],[-1,0,1]]
> Explanation: 
> nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
> nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
> nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
> The distinct triplets are [-1,0,1] and [-1,-1,2].
> Notice that the order of the output and the order of the triplets does not matter.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,1]
> Output: []
> Explanation: The only possible triplet does not sum up to 0.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,0,0]
> Output: [[0,0,0]]
> Explanation: The only possible triplet sums up to 0.
> ```
> 
> **Constraints:**
> - 3 <= nums.length <= 3000
> - -10^5 <= nums[i] <= 10^5

> [!info] Approach
> Reduce to two-sum: fix element `a`, find pair `(b, c)` with `b + c = -a` in the remaining array. Sort first to handle duplicates. For each index `i`, use a set to find complements in `nums[i+1:]`. Sort. Skip duplicate values of `a`. For the inner scan, use a seen set: if `target - b` in seen, record triplet; else add `b` to seen.

> [!note]- Python Solution
> ```python
> def three_sum(nums):
>     nums.sort()
>     result = []
>     seen_triplets = set()
>     for i in range(len(nums) - 2):
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue
>         target = -nums[i]
>         seen = set()
>         j = i + 1
>         while j < len(nums):
>             complement = target - nums[j]
>             if complement in seen:
>                 triplet = (nums[i], complement, nums[j])
>                 if triplet not in seen_triplets:
>                     seen_triplets.add(triplet)
>                     result.append(list(triplet))
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

### 4Sum (hash-based) `⭐ Google`

> [!example] Problem
> Given an array nums of n integers, return an array of all the unique quadruplets [nums[a], nums[b], nums[c], nums[d]] such that:
> You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,0,-1,0,-2,2], target = 0
> Output: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,2,2,2,2], target = 8
> Output: [[2,2,2,2]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 200
> - -10^9 <= nums[i] <= 10^9
> - -10^9 <= target <= 10^9

> [!info] Approach
> Reduce to 3Sum by fixing one element. Reduce 3Sum to 2Sum by fixing another. Sort + two outer loops (skip duplicates) + hash set inner two-sum. Fix `nums[i]` and `nums[j]`. Inner target is `target - nums[i] - nums[j]`. Use seen set for two-sum on remaining elements.

> [!note]- Python Solution
> ```python
> def four_sum(nums, target):
>     nums.sort()
>     result = []
>     seen_quads = set()
>     n = len(nums)
>     for i in range(n - 3):
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue
>         for j in range(i + 1, n - 2):
>             if j > i + 1 and nums[j] == nums[j - 1]:
>                 continue
>             need = target - nums[i] - nums[j]
>             seen = set()
>             k = j + 1
>             while k < n:
>                 if need - nums[k] in seen:
>                     quad = (nums[i], nums[j], need - nums[k], nums[k])
>                     if quad not in seen_quads:
>                         seen_quads.add(quad)
>                         result.append(list(quad))
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
> You are given an integer array nums and an integer k.
> In one operation, you can pick two numbers from the array whose sum equals k and remove them from the array.
> Return the maximum number of operations you can perform on the array.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3,4], k = 5
> Output: 2
> Explanation: Starting with nums = [1,2,3,4]:
> - Remove numbers 1 and 4, then nums = [2,3]
> - Remove numbers 2 and 3, then nums = []
> There are no more pairs that sum up to 5, hence a total of 2 operations.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,1,3,4,3], k = 6
> Output: 1
> Explanation: Starting with nums = [3,1,3,4,3]:
> - Remove the first two 3's, then nums = [1,4,3]
> There are no more pairs that sum up to 6, hence a total of 1 operation.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - 1 <= nums[i] <= 10^9
> - 1 <= k <= 10^9

> [!info] Approach
> Each number can only pair once — we need to greedily match available complements, consuming them. Frequency map. For each `x`, check if `k - x` has remaining count. If yes, form a pair and decrement both counts. Build `Counter`. For each unique `x`, pairs formed = `min(freq[x], freq[k - x])` if `x != k - x`, else `freq[x] // 2`. Sum all.

> [!note]- Python Solution
> ```python
> from collections import Counter
> >
> def max_operations(nums, k):
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

### First Unique Character in a String

> [!example] Problem
> Given a string s, find the first non-repeating character in it and return its index. If it does not exist, return -1.
> 
> **Example 1:**
> ```
> Input: s = "leetcode"
> Output: 0
> Explanation:
> The character 'l' at index 0 is the first character that does not occur at any other index.
> ```
> 
> **Example 2:**
> ```
> Input: s = "loveleetcode"
> Output: 2
> ```
> 
> **Example 3:**
> ```
> Input: s = "aabb"
> Output: -1
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s consists of only lowercase English letters.

> [!info] Approach
> Need both frequency (to identify unique) and order (to find the first). Count all frequencies, then scan left to right for the first character with count 1. `Counter` in one pass; second pass finds first with count 1. Two O(n) passes.

> [!note]- Python Solution
> ```python
> from collections import Counter
> >
> def first_uniq_char(s):
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

### Ransom Note

> [!example] Problem
> Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine and false otherwise.
> Each letter in magazine can only be used once in ransomNote.
> 
> **Example 1:**
> ```
> Input: ransomNote = "a", magazine = "b"
> Output: false
> ```
> 
> **Example 2:**
> ```
> Input: ransomNote = "aa", magazine = "ab"
> Output: false
> ```
> 
> **Example 3:**
> ```
> Input: ransomNote = "aa", magazine = "aab"
> Output: true
> ```
> 
> **Constraints:**
> - 1 <= ransomNote.length, magazine.length <= 10^5
> - ransomNote and magazine consist of lowercase English letters.

> [!info] Approach
> This is a frequency matching problem; each character in the note must be available at least as many times as needed. Count letters in the magazine and decrement as you consume letters from the note. Use a hash map or `Counter`; if any needed character drops below zero, return `false`. A quick length check can short-circuit impossible cases.

> [!note]- Python Solution
> ```python
> from collections import Counter
> >
> def can_construct(ransom_note, magazine):
>     if len(ransom_note) > len(magazine):
>         return False
>     count = Counter(magazine)
>     for ch in ransom_note:
>         if count[ch] == 0:
>             return False
>         count[ch] -= 1
>     return True
> ```

> [!success] Complexity
> Time O(m + n); Space O(1) extra for lowercase letters.

> [!tip] Alternatives
> Sort + two pointers works too, but frequency counting is the direct interview answer.

---

### Top K Frequent Elements `🔥 Google`

> [!example] Problem
> Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,1,2,2,3], k = 2
> Output: [1,2]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1], k = 1
> Output: [1]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4
> - k is in the range [1, the number of unique elements in the array].
> - It is guaranteed that the answer is unique.

> [!info] Approach
> Sorting by frequency is O(n log n). Bucket sort on frequency gives O(n). Count frequencies, then place each number into a bucket indexed by its frequency. Collect from the highest-frequency buckets downward. `Counter` → buckets list of size `n+1` where `buckets[f]` holds all numbers with frequency `f`. Iterate from index `n` down and collect until we have `k` elements.

> [!note]- Python Solution
> ```python
> from collections import Counter
> >
> def top_k_frequent(nums, k):
>     freq = Counter(nums)
>     buckets = [[] for _ in range(len(nums) + 1)]
>     for num, count in freq.items():
>         buckets[count].append(num)
>     result = []
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
> A website domain "discuss.leetcode.com" consists of various subdomains. At the top level, we have "com", at the next level, we have "leetcode.com" and at the lowest level, "discuss.leetcode.com". When we visit a domain like "discuss.leetcode.com", we will also visit the parent domains "leetcode.com" and "com" implicitly.
> A count-paired domain is a domain that has one of the two formats "rep d1.d2.d3" or "rep d1.d2" where rep is the number of visits to the domain and d1.d2.d3 is the domain itself.
> Given an array of count-paired domains cpdomains, return an array of the count-paired domains of each subdomain in the input. You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: cpdomains = ["9001 discuss.leetcode.com"]
> Output: ["9001 leetcode.com","9001 discuss.leetcode.com","9001 com"]
> Explanation: We only have one website domain: "discuss.leetcode.com".
> As discussed above, the subdomain "leetcode.com" and "com" will also be visited. So they will all be visited 9001 times.
> ```
> 
> **Example 2:**
> ```
> Input: cpdomains = ["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"]
> Output: ["901 mail.com","50 yahoo.com","900 google.mail.com","5 wiki.org","5 org","1 intel.mail.com","951 com"]
> Explanation: We will visit "google.mail.com" 900 times, "yahoo.com" 50 times, "intel.mail.com" once and "wiki.org" 5 times.
> For the subdomains, we will visit "mail.com" 900 + 1 = 901 times, "com" 900 + 50 + 1 = 951 times, and "org" 5 times.
> ```
> 
> **Constraints:**
> - 1 <= cpdomain.length <= 100
> - 1 <= cpdomain[i].length <= 100
> - cpdomain[i] follows either the "repi d1i.d2i.d3i" format or the "repi d1i.d2i" format.
> - repi is an integer in the range [1, 10^4].
> - d1i, d2i, and d3i consist of lowercase English letters.

> [!info] Approach
> Each domain contributes its count to itself and all suffix domains. Aggregate with a frequency map. Parse count and domain. Split domain on `.` and generate all suffixes. Accumulate counts. For `"9 discuss.leetcode.com"` add 9 to `discuss.leetcode.com`, `leetcode.com`, and `com`. Format output as `"count domain"` strings.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def subdomain_visits(cpdomains):
>     counts = defaultdict(int)
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
> Given a string s, sort it in decreasing order based on the frequency of the characters. The frequency of a character is the number of times it appears in the string.
> Return the sorted string. If there are multiple answers, return any of them.
> 
> **Example 1:**
> ```
> Input: s = "tree"
> Output: "eert"
> Explanation: 'e' appears twice while 'r' and 't' both appear once.
> So 'e' must appear before both 'r' and 't'. Therefore "eetr" is also a valid answer.
> ```
> 
> **Example 2:**
> ```
> Input: s = "cccaaa"
> Output: "aaaccc"
> Explanation: Both 'c' and 'a' appear three times, so both "cccaaa" and "aaaccc" are valid answers.
> Note that "cacaca" is incorrect, as the same characters must be together.
> ```
> 
> **Example 3:**
> ```
> Input: s = "Aabb"
> Output: "bbAa"
> Explanation: "bbaA" is also a valid answer, but "Aabb" is incorrect.
> Note that 'A' and 'a' are treated as two different characters.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 5 * 10^5
> - s consists of uppercase and lowercase English letters and digits.

> [!info] Approach
> Need characters ordered by count descending. Count frequencies, then rebuild string: higher-frequency characters first. `Counter`, then sort by count descending, rebuild via `ch * count` concatenation.

> [!note]- Python Solution
> ```python
> from collections import Counter
> >
> def frequency_sort(s):
>     freq = Counter(s)
>     sorted_chars = sorted(freq.keys(), key=lambda c: -freq[c])
>     return ''.join(c * freq[c] for c in sorted_chars)
> ```

> [!success] Complexity
> Time O(n + k log k) where k = distinct chars; Space O(n).

> [!tip] Alternatives
> Bucket sort by frequency — O(n) time. Index is frequency, bucket contains chars with that frequency. Iterate buckets high to low.

---

### Longest Subarray with Sum K

> [!example] Problem
> Find the maximum length of a contiguous subarray with sum equal to `k`. Array may contain negatives.

> [!info] Approach
> Sliding window fails with negatives. Prefix sum trick: subarray `[i+1, j]` has sum `k` iff `prefix[j] - prefix[i] = k`, i.e., `prefix[i] = prefix[j] - k`. For maximum length, store the *first* occurrence of each prefix sum. When we see `prefix - k` again later, the gap is as large as possible. `first_seen = {0: -1}`. At index `i`, if `prefix - k` in map, update `best = max(best, i - first_seen[prefix - k])`. Only insert prefix if not already present (preserve earliest index).

> [!note]- Python Solution
> ```python
> def max_subarray_len(nums, k):
>     first_seen = {0: -1}
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
> Given an array of integers nums and an integer k. A continuous subarray is called nice if there are k odd numbers on it.
> Return the number of nice sub-arrays.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,2,1,1], k = 3
> Output: 2
> Explanation: The only sub-arrays with 3 odd numbers are [1,1,2,1] and [1,2,1,1].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,4,6], k = 1
> Output: 0
> Explanation: There are no odd numbers in the array.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [2,2,2,1,2,2,1,2,2,2], k = 2
> Output: 16
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 50000
> - 1 <= nums[i] <= 10^5
> - 1 <= k <= nums.length

> [!info] Approach
> Map odd/even to 1/0. Problem becomes: count subarrays with sum exactly `k` — identical to LC 560. Parity prefix sum. `prefix[j] - prefix[i] = k` means subarray `[i+1, j]` has exactly `k` odd numbers. `seen = {0: 1}`. Running sum increments by 1 for odd elements, 0 for even. Look up `prefix - k` in `seen` before updating map.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def number_of_subarrays(nums, k):
>     seen = defaultdict(int)
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

### Subarray Sum Equals K `🔥 Google`

> [!example] Problem
> Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.
> A subarray is a contiguous non-empty sequence of elements within an array.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,1], k = 2
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3], k = 3
> Output: 2
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - -1000 <= nums[i] <= 1000
> - -10^7 <= k <= 10^7

> [!info] Approach
> Sliding window fails with negatives (sum can decrease when adding elements). Need a different invariant. prefix[j] - prefix[i] = k implies prefix[i] = prefix[j] - k. Count how many times each prefix sum has appeared. Maintain running prefix sum. Before updating the map, check `seen[prefix - k]`. Initialize `seen = {0: 1}` to handle subarrays starting at index 0.

> [!note]- Python Solution
> ```python
> def subarray_sum(nums, k):
>     count = 0
>     prefix = 0
>     seen = {0: 1}
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
> Given a binary array nums, return the maximum length of a contiguous subarray with an equal number of 0 and 1.
> 
> **Example 1:**
> ```
> Input: nums = [0,1]
> Output: 2
> Explanation: [0, 1] is the longest contiguous subarray with an equal number of 0 and 1.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,0]
> Output: 2
> Explanation: [0, 1] (or [1, 0]) is a longest contiguous subarray with equal number of 0 and 1.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,1,1,1,1,1,0,0,0]
> Output: 6
> Explanation: [1,1,1,0,0,0] is the longest contiguous subarray with equal number of 0 and 1.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - nums[i] is either 0 or 1.

> [!info] Approach
> "Equal 0s and 1s" means the difference between 0-count and 1-count is 0 over the subarray. Replace 0 with -1. Problem becomes: longest subarray with sum 0. Use prefix sum + first-seen map. Track running sum with 0→-1 transform. When `prefix` repeats, the subarray between the two occurrences has sum 0. Store `first_seen = {0: -1}` and compare `i - first_seen[prefix]`.

> [!note]- Python Solution
> ```python
> def find_max_length(nums):
>     first_seen = {0: -1}
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
> We want `(total - subarray_sum) % P == 0`, i.e., `subarray_sum % P == total % P`. Find the shortest subarray with that remainder. Prefix sums mod P. For each `j`, want the most recent `i` where `prefix[i] % P == (prefix[j] - rem) % P`. `rem = sum(nums) % P`. If `rem == 0`, return 0. Use `seen = {0: -1}`. At each step store `prefix % P → i`. Look up `(prefix - rem) % P`.

> [!note]- Python Solution
> ```python
> def min_subarray(nums, p):
>     rem = sum(nums) % p
>     if rem == 0:
>         return 0
>     seen = {0: -1}
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
> Given an integer array nums and an integer k, return the number of non-empty subarrays that have a sum divisible by k.
> A subarray is a contiguous part of an array.
> 
> **Example 1:**
> ```
> Input: nums = [4,5,0,-2,-3,1], k = 5
> Output: 7
> Explanation: There are 7 subarrays with a sum divisible by k = 5:
> [4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5], k = 9
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - -10^4 <= nums[i] <= 10^4
> - 2 <= k <= 10^4

> [!info] Approach
> `(prefix[j] - prefix[i]) % K == 0` iff `prefix[j] % K == prefix[i] % K`. Count pairs of equal remainders. Frequency map of prefix sums mod K. Each pair of indices with equal remainder contributes one valid subarray. `seen = {0: 1}`. For each element, compute `prefix % K` (handle negatives: `% K` in Python already returns non-negative). Add `seen[(prefix % K)]` to count. Increment map.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def subarrays_div_by_k(nums, k):
>     count = 0
>     prefix = 0
>     seen = defaultdict(int)
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

### Insert Delete GetRandom O(1) `🔥 Google`

> [!example] Problem
> Implement the RandomizedSet class:
> You must implement the functions of the class such that each function works in average O(1) time complexity.
> 
> **Example 1:**
> ```
> Input
> ["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
> [[], [1], [2], [2], [], [1], [2], []]
> Output
> [null, true, false, true, 2, true, false, 2]
> 
> Explanation
> RandomizedSet randomizedSet = new RandomizedSet();
> randomizedSet.insert(1); // Inserts 1 to the set. Returns true as 1 was inserted successfully.
> randomizedSet.remove(2); // Returns false as 2 does not exist in the set.
> randomizedSet.insert(2); // Inserts 2 to the set, returns true. Set now contains [1,2].
> randomizedSet.getRandom(); // getRandom() should return either 1 or 2 randomly.
> randomizedSet.remove(1); // Removes 1 from the set, returns true. Set now contains [2].
> randomizedSet.insert(2); // 2 was already in the set, so return false.
> randomizedSet.getRandom(); // Since 2 is the only number in the set, getRandom() will always return 2.
> ```
> 
> **Constraints:**
> - -2^{31} <= val <= 2^{31} - 1
> - At most 2 * 10^5 calls will be made to insert, remove, and getRandom.
> - There will be at least one element in the data structure when getRandom is called.

> [!info] Approach
> Hash map gives O(1) insert/delete/lookup. But random access requires an array. Combining both enables all three in O(1). `vals` list for O(1) random access. `idx_map` maps value to its index in `vals`. Delete: swap target with last element to avoid gaps, then pop. Insert appends to list and stores index in map. Remove swaps target with last element, updates map for the moved element, pops the list, deletes map entry for removed value.

> [!note]- Python Solution
> ```python
> import random
> >
> class RandomizedSet:
>     def __init__(self):
>         self._vals: list[int] = []
>         self._idx: dict[int, int] = {}
> >
>     def insert(self, val):
>         if val in self._idx:
>             return False
>         self._idx[val] = len(self._vals)
>         self._vals.append(val)
>         return True
> >
>     def remove(self, val):
>         if val not in self._idx:
>             return False
>         idx = self._idx[val]
>         last = self._vals[-1]
>         self._vals[idx] = last
>         self._idx[last] = idx
>         self._vals.pop()
>         del self._idx[val]
>         return True
> >
>     def get_random(self):
>         return random.choice(self._vals)
> ```

> [!success] Complexity
> Time O(1) amortized all ops; Space O(n).

> [!tip] Alternatives
> No simpler structure achieves O(1) for all three. The swap-with-last trick is the canonical insight.

---

### Design HashMap `⭐ Google`

> [!example] Problem
> Design a HashMap without using any built-in hash table libraries.
> Implement the MyHashMap class
> 
> **Example 1:**
> ```
> Input
> ["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"]
> [[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
> Output
> [null, null, null, 1, -1, null, 1, null, -1]
> 
> Explanation
> MyHashMap myHashMap = new MyHashMap();
> myHashMap.put(1, 1); // The map is now [[1,1]]
> myHashMap.put(2, 2); // The map is now [[1,1], [2,2]]
> myHashMap.get(1);    // return 1, The map is now [[1,1], [2,2]]
> myHashMap.get(3);    // return -1 (i.e., not found), The map is now [[1,1], [2,2]]
> myHashMap.put(2, 1); // The map is now [[1,1], [2,1]] (i.e., update the existing value)
> myHashMap.get(2);    // return 1, The map is now [[1,1], [2,1]]
> myHashMap.remove(2); // remove the mapping for 2, The map is now [[1,1]]
> myHashMap.get(2);    // return -1 (i.e., not found), The map is now [[1,1]]
> ```
> 
> **Constraints:**
> - 0 <= key, value <= 10^6
> - At most 10^4 calls will be made to put, get, and remove.

> [!info] Approach
> Understand collision resolution. Chaining: each bucket holds a list of `(key, value)` pairs. Array of `capacity` buckets. Hash function: `key % capacity` with prime capacity to reduce clustering. `put` scans bucket for existing key (update) or appends. `get` scans for key, returns -1 if absent. `remove` filters out the key.

> [!note]- Python Solution
> ```python
> class MyHashMap:
>     def __init__(self, capacity=1009):  # prime capacity
>         self._cap = capacity
>         self._buckets: list[list[tuple[int, int]]] = [[] for _ in range(capacity)]
> >
>     def _idx(self, key):
>         return key % self._cap
> >
>     def put(self, key, value):
>         bucket = self._buckets[self._idx(key)]
>         for i, (k, _) in enumerate(bucket):
>             if k == key:
>                 bucket[i] = (key, value)
>                 return
>         bucket.append((key, value))
> >
>     def get(self, key):
>         for k, v in self._buckets[self._idx(key)]:
>             if k == key:
>                 return v
>         return -1
> >
>     def remove(self, key):
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
> Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3,1]
> Output: true
> Explanation:
> The element 1 occurs at the indices 0 and 3.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,4]
> Output: false
> Explanation:
> All elements are distinct.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,1,1,3,3,4,3,2,4,2]
> Output: true
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^9 <= nums[i] <= 10^9

> [!info] Approach
> Membership check in O(1) is exactly what a hash set provides. Insert elements one by one. If an element is already in the set, a duplicate exists. Single pass: if `x in seen` return True; else `seen.add(x)`. Short-circuits on first duplicate.

> [!note]- Python Solution
> ```python
> def contains_duplicate(nums):
>     seen = set()
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
> Given two integer arrays nums1 and nums2, return an array of their intersection. Each element in the result must be unique and you may return the result in any order.
> 
> **Example 1:**
> ```
> Input: nums1 = [1,2,2,1], nums2 = [2,2]
> Output: [2]
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
> Output: [9,4]
> Explanation: [4,9] is also accepted.
> ```
> 
> **Constraints:**
> - 1 <= nums1.length, nums2.length <= 1000
> - 0 <= nums1[i], nums2[i] <= 1000

> [!info] Approach
> Set intersection directly models the problem. O(1) membership check makes it efficient. Convert both to sets. Return their intersection as a list. `set(nums1) & set(nums2)` in Python. For an explicit approach: iterate the smaller set, check membership in the larger.

> [!note]- Python Solution
> ```python
> def intersection(nums1, nums2):
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
> Given an array `nums` of integers and integer `k`, return the maximum `sum` such that there exists `i < j` with `nums[i] + nums[j] = sum` and `sum < k`. If no `i`, `j` exist satisfying this equation, return `-1`.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** nums = [34,23,1,24,75,33,54,8], k = 60
> **Output:** 58
> **Explanation: **We can use 34 and 24 to sum 58 which is less than 60.
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** nums = [10,20,30], k = 15
> **Output:** -1
> **Explanation: **In this case it is not possible to get a pair sum less that 15.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= nums.length <= 100`
> 	
> - `1 <= nums[i] <= 1000`
> 	
> - `1 <= k <= 2000`

> [!info] Approach
> We want the largest valid pair sum — greedy with two pointers after sorting is cleanest. Hash set alternative: for each `x`, check if any value in `[k - x - (n-1)..k - x - 1]` is present. Sort. Use two pointers. If `nums[l] + nums[r] < k`, record sum and advance `l`. Else shrink `r`. After sort, `l = 0`, `r = n - 1`. Converge inward. Track `best = max(best, sum)` when `sum < k`.

> [!note]- Python Solution
> ```python
> def two_sum_less_than_k(nums, k):
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

### Longest Consecutive Sequence `🔥 Google`

> [!example] Problem
> Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
> You must write an algorithm that runs in O(n) time.
> 
> **Example 1:**
> ```
> Input: nums = [100,4,200,1,3,2]
> Output: 4
> Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,3,7,2,5,8,4,6,0,1]
> Output: 9
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,0,1,2]
> Output: 3
> ```
> 
> **Constraints:**
> - 0 <= nums.length <= 10^5
> - -10^9 <= nums[i] <= 10^9

> [!info] Approach
> Sorting is O(n log n). We need O(n). Hash set enables O(1) membership checks. Only start counting a sequence from `x` if `x - 1` is NOT in the set. This prevents redundant work — each element is visited at most twice total. Build set. For each `x`, if `x - 1 not in set`, extend the chain `x, x+1, x+2, ...` while each successor is in the set.

> [!note]- Python Solution
> ```python
> def longest_consecutive(nums):
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
> You are given a string s and an array of strings words. All the strings of words are of the same length.
> A concatenated string is a string that exactly contains all the strings of any permutation of words concatenated.
> Return an array of the starting indices of all the concatenated substrings in s. You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: s = "barfoothefoobarman", words = ["foo","bar"]
> Output: [0,9]
> Explanation:
> The substring starting at 0 is "barfoo" . It is the concatenation of ["bar","foo"] which is a permutation of words . The substring starting at 9 is "foobar" . It is the concatenation of ["foo","bar"] which is a permutation of words .
> ```
> 
> **Example 2:**
> ```
> Input: s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]
> Output: []
> Explanation:
> There is no concatenated substring.
> ```
> 
> **Example 3:**
> ```
> Input: s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]
> Output: [6,9,12]
> Explanation:
> The substring starting at 6 is "foobarthe" . It is the concatenation of ["foo","bar","the"] . The substring starting at 9 is "barthefoo" . It is the concatenation of ["bar","the","foo"] . The substring starting at 12 is "thefoobar" . It is the concatenation of ["the","foo","bar"] .
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^4
> - 1 <= words.length <= 5000
> - 1 <= words[i].length <= 30
> - s and words[i] consist of lowercase English letters.

> [!info] Approach
> Words are fixed length. Enumerate all starting offsets 0 to `word_len - 1`. For each, slide a window of `num_words` words and compare word frequency maps. `words_count` = Counter of required words. Slide a window by one word at a time. Track current window word frequencies and a `have` count. For each offset in `[0, word_len)`, maintain a sliding window of exactly `num_words * word_len` characters. Add/remove one word at a time from window ends.

> [!note]- Python Solution
> ```python
> from collections import Counter
> >
> def find_substring(s, words):
>     if not s or not words:
>         return []
>     wlen = len(words[0])
>     num_words = len(words)
>     total = wlen * num_words
>     words_count = Counter(words)
>     result = []
>     for offset in range(wlen):
>         window = {}
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
> Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane, return the maximum number of points that lie on the same straight line.
> 
> **Example 1:**
> ```
> Input: points = [[1,1],[2,2],[3,3]]
> Output: 3
> ```
> 
> **Example 2:**
> ```
> Input: points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]
> Output: 4
> ```
> 
> **Constraints:**
> - 1 <= points.length <= 300
> - points[i].length == 2
> - -10^4 <= xi, yi <= 10^4
> - All the points are unique.

> [!info] Approach
> For each pair of points, their line is defined by slope. Points on the same line share the same slope relative to a fixed anchor. Fix each point as anchor. For all other points, compute the slope as a reduced fraction `(dy/gcd, dx/gcd)`. Count max slope frequency. For each anchor `i`, build a slope map. Use `gcd` to normalize: slope = `(dy // g, dx // g)`. Handle vertical lines (`dx == 0`) and same-point duplicates separately.

> [!note]- Python Solution
> ```python
> from math import gcd
> from collections import defaultdict
> >
> def max_points(points):
>     n = len(points)
>     if n <= 2:
>         return n
>     best = 2
>     for i in range(n):
>         slopes = defaultdict(int)
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
> Given a string s, consider all duplicated substrings: (contiguous) substrings of s that occur 2 or more times. The occurrences may overlap.
> Return any duplicated substring that has the longest possible length. If s does not have a duplicated substring, the answer is "".
> 
> **Example 1:**
> ```
> Input: s = "banana"
> Output: "ana"
> ```
> 
> **Example 2:**
> ```
> Input: s = "abcd"
> Output: ""
> ```
> 
> **Constraints:**
> - 2 <= s.length <= 3 * 10^4
> - s consists of lowercase English letters.

> [!info] Approach
> Binary search on length `L`: if a duplicate of length `L` exists, so does one of length `L-1`. Check feasibility via rolling hash to avoid O(n²) string comparison. Binary search `L` in `[1, n-1]`. For each `L`, use Rabin-Karp: compute polynomial rolling hash for every window of length `L`; if any hash repeats, verify the match (hash collision guard). Hash = `sum(ord(s[i]) * base^(L-1-i)) % mod` for window. Rolling update: `new_hash = (old_hash * base - ord(left) * base^L + ord(right)) % mod`. Store hashes in a set. Return the window on collision.

> [!note]- Python Solution
> ```python
> def longest_dup_substring(s):
>     n = len(s)
>     BASE, MOD = 31, (1 << 61) - 1  # Mersenne prime
>     nums = [ord(c) - ord('a') + 1 for c in s]
> >
>     def search(length):
>         h = 0
>         power = pow(BASE, length, MOD)
>         for i in range(length):
>             h = (h * BASE + nums[i]) % MOD
>         seen = {h: [0]}
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
> >
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
> Given a list paths of directory info, including the directory path, and all the files with contents in this directory, return all the duplicate files in the file system in terms of their paths. You may return the answer in any order.
> A group of duplicate files consists of at least two files that have the same content.
> A single directory info string in the input list has the following format:
> It means there are n files (f1.txt, f2.txt ... fn.txt) with content (f1_content, f2_content ... fn_content) respectively in the directory "root/d1/d2/.../dm". Note that n >= 1 and m >= 0. If m = 0, it means the directory is just the root directory.
> The output is a list of groups of duplicate file paths. For each group, it contains all the file paths of the files that have the same content. A file path is a string that has the following format
> 
> **Example 1:**
> ```
> Input: paths = ["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd)","root/c/d 4.txt(efgh)","root 4.txt(efgh)"]
> Output: [["root/a/2.txt","root/c/d/4.txt","root/4.txt"],["root/a/1.txt","root/c/3.txt"]]
> ```
> 
> **Example 2:**
> ```
> Input: paths = ["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd)","root/c/d 4.txt(efgh)"]
> Output: [["root/a/2.txt","root/c/d/4.txt"],["root/a/1.txt","root/c/3.txt"]]
> ```
> 
> **Constraints:**
> - 1 <= paths.length <= 2 * 10^4
> - 1 <= paths[i].length <= 3000
> - 1 <= sum(paths[i].length) <= 5 * 10^5
> - paths[i] consist of English letters, digits, '/', '.', '(', ')', and ' '.
> - You may assume no files or directories share the same name in the same directory.
> - You may assume each given directory info represents a unique directory. A single blank space separates the directory path and file info.

> [!info] Approach
> Files with the same content are duplicates. Content is the natural key for a hash map. Parse each string into `(directory, filename, content)`. Group file paths by content string. For each entry split on spaces: first token is directory, rest are `name(content)` tokens. Extract content between `(` and `)`. Map `content → list[full_path]`. Return groups with size ≥ 2.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def find_duplicate(paths):
>     content_map = defaultdict(list)
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

### 4Sum II `⭐ Google`

> [!example] Problem
> Given four integer arrays nums1, nums2, nums3, and nums4 all of length n, return the number of tuples (i, j, k, l) such that
> 
> **Example 1:**
> ```
> Input: nums1 = [1,2], nums2 = [-2,-1], nums3 = [-1,2], nums4 = [0,2]
> Output: 2
> Explanation:
> The two tuples are:
> 1. (0, 0, 0, 1) -> nums1[0] + nums2[0] + nums3[0] + nums4[1] = 1 + (-2) + (-1) + 2 = 0
> 2. (1, 1, 0, 0) -> nums1[1] + nums2[1] + nums3[0] + nums4[0] = 2 + (-1) + (-1) + 0 = 0
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [0], nums2 = [0], nums3 = [0], nums4 = [0]
> Output: 1
> ```
> 
> **Constraints:**
> - n == nums1.length
> - n == nums2.length
> - n == nums3.length
> - n == nums4.length
> - 1 <= n <= 200
> - -228 <= nums1[i], nums2[i], nums3[i], nums4[i] <= 228

> [!info] Approach
> Brute force O(n⁴). Split into two pairs: count all `A[i] + B[j]` sums, then for each `C[k] + D[l]` check if its negation was seen. Hash map `ab_sum → count`. Then iterate all C, D pairs and look up `-(C[k] + D[l])`. Two nested loops for AB → Counter. Two nested loops for CD → look up complement. Sum all matching counts.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def four_sum_count(nums1: list[int], nums2: list[int],
>                    nums3: list[int], nums4: list[int]) -> int:
>     ab = defaultdict(int)
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
### Subarray Sums Divisible by K (LC 974)

> [!example] Problem
> Given an integer array nums and an integer k, return the number of non-empty subarrays that have a sum divisible by k.
> A subarray is a contiguous part of an array.
> 
> **Example 1:**
> ```
> Input: nums = [4,5,0,-2,-3,1], k = 5
> Output: 7
> Explanation: There are 7 subarrays with a sum divisible by k = 5:
> [4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5], k = 9
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - -10^4 <= nums[i] <= 10^4
> - 2 <= k <= 10^4

> [!info] Approach
> `sum(i..j) % k == 0` iff `prefix[j] % k == prefix[i-1] % k`. So we count pairs of equal remainders among prefix sums. Track `remainder -> count` in a hash map. For each prefix sum, look up how many prior prefix sums had the same remainder mod `k`. Initialize `{0: 1}`. For each element, compute `remainder = running_sum % k`. In Python, `%` always returns non-negative values, so no adjustment needed. Add `count_map[remainder]` to the answer, then increment `count_map[remainder]`.

> [!note]- Python Solution
> ```python
> def subarrays_div_by_k(nums, k):
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
> Given a binary array nums, return the maximum length of a contiguous subarray with an equal number of 0 and 1.
> 
> **Example 1:**
> ```
> Input: nums = [0,1]
> Output: 2
> Explanation: [0, 1] is the longest contiguous subarray with an equal number of 0 and 1.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,0]
> Output: 2
> Explanation: [0, 1] (or [1, 0]) is a longest contiguous subarray with equal number of 0 and 1.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,1,1,1,1,1,0,0,0]
> Output: 6
> Explanation: [1,1,1,0,0,0] is the longest contiguous subarray with equal number of 0 and 1.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - nums[i] is either 0 or 1.

> [!info] Approach
> Map 0 → -1. Now "equal 0s and 1s" means "subarray sum = 0". A subarray `[i+1..j]` sums to zero iff `prefix[j] == prefix[i]`. We want the maximum `j - i` among equal prefix sums. Hash map of `prefix_sum -> first_index`. When a prefix sum repeats, the distance gives a candidate max length. Initialize `{0: -1}`. For each index `i`, update `prefix`. If `prefix` is in the map, update `max_len = max(max_len, i - first_seen[prefix])`. Otherwise record `first_seen[prefix] = i`.

> [!note]- Python Solution
> ```python
> def find_max_length(nums):
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

### 4Sum II (LC 454) `⭐ Google`

> [!example] Problem
> Given four integer arrays nums1, nums2, nums3, and nums4 all of length n, return the number of tuples (i, j, k, l) such that
> 
> **Example 1:**
> ```
> Input: nums1 = [1,2], nums2 = [-2,-1], nums3 = [-1,2], nums4 = [0,2]
> Output: 2
> Explanation:
> The two tuples are:
> 1. (0, 0, 0, 1) -> nums1[0] + nums2[0] + nums3[0] + nums4[1] = 1 + (-2) + (-1) + 2 = 0
> 2. (1, 1, 0, 0) -> nums1[1] + nums2[1] + nums3[0] + nums4[0] = 2 + (-1) + (-1) + 0 = 0
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [0], nums2 = [0], nums3 = [0], nums4 = [0]
> Output: 1
> ```
> 
> **Constraints:**
> - n == nums1.length
> - n == nums2.length
> - n == nums3.length
> - n == nums4.length
> - 1 <= n <= 200
> - -228 <= nums1[i], nums2[i], nums3[i], nums4[i] <= 228

> [!info] Approach
> O(n⁴) brute force is too slow. Split the four arrays into two pairs. All pairwise sums from (A, B) can be stored in a hash map; then for each pairwise sum from (C, D), look up its negative. Build a frequency map of `a + b` for all pairs from A and B. Then for each pair `(c, d)`, query the map for `-(c + d)`. `ab_count = Counter(a + b for a in A for b in B)`. Then `total = sum(ab_count[-(c + d)] for c in C for d in D)`.

> [!note]- Python Solution
> ```python
> from collections import Counter
> >
> def four_sum_count(nums1, nums2, nums3, nums4):
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
