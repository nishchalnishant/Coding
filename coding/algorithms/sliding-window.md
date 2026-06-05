---
tags: [coding, algorithms, sliding-window]
topic: Sliding Window
difficulty: mixed
---

# Sliding Window — Problem Set

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop. Do not move on until these are reflexive.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Highly probable; know the core patterns cold. Edge cases matter less.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Know what it is conceptually; skip deep implementation practice.





---

## Fixed-Size Window

> [!info] Approach
> For a window of exactly size `k`, every slide adds one element on the right and removes one on the left. Maintain state incrementally in O(1) per step rather than recomputing from scratch — reduces O(nk) to O(n).

---

### Find All Anagrams in a String (LC 438) `⚡ T1`

> [!example] Problem
> Given two strings s and p, return an array of all the start indices of p's anagrams in s. You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: s = "cbaebabacd", p = "abc"
> Output: [0,6]
> Explanation:
> The substring with start index = 0 is "cba", which is an anagram of "abc".
> The substring with start index = 6 is "bac", which is an anagram of "abc".
> ```
> 
> **Example 2:**
> ```
> Input: s = "abab", p = "ab"
> Output: [0,1,2]
> Explanation:
> The substring with start index = 0 is "ab", which is an anagram of "ab".
> The substring with start index = 1 is "ba", which is an anagram of "ab".
> The substring with start index = 2 is "ab", which is an anagram of "ab".
> ```
> 
> **Constraints:**
> - 1 <= s.length, p.length <= 3 * 10^4
> - s and p consist of lowercase English letters.

> [!info] Approach
> An anagram is a permutation — same character frequencies, different order. Fixed window of size `len(p)`. Maintain a frequency diff between window and `need`. Track how many characters are "satisfied" with a `matches` counter — avoids O(26) dict comparison each step. On adding `s[right]`: if freq reaches exactly `need[c]` → `matches += 1`. On removing `s[left]`: if freq drops below `need[c]` → `matches -= 1`. When `matches == len(need)` → anagram found.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def find_anagrams(s, p):
>     need = Counter(p)
>     window = {}
>     matches = 0
>     required = len(need)
>     result = []
>     k = len(p)
> 
>     for right in range(len(s)):
>         c = s[right]
>         window[c] = window.get(c, 0) + 1
>         if c in need and window[c] == need[c]:
>             matches += 1
> 
>         if right >= k:   # window overflows — remove leftmost
>             lc = s[right - k]
>             if lc in need and window[lc] == need[lc]:
>                 matches -= 1
>             window[lc] -= 1
>             if window[lc] == 0:
>                 del window[lc]
> 
>         if right >= k - 1 and matches == required:
>             result.append(right - k + 1)
> 
>     return result
> ```

> [!success] Complexity
> O(n) time, O(|alphabet|) space.

> [!tip] Alternatives
> Compare `Counter` dicts directly each step — O(26) per slide vs O(1) with match counter; both O(n) overall but match counter is cleaner.

---

### Maximum Average Subarray I (LC 643)

> [!example] Problem
> You are given an integer array nums consisting of n elements, and an integer k.
> Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value. Any answer with a calculation error less than 10-5 will be accepted.
> 
> **Example 1:**
> ```
> Input: nums = [1,12,-5,-6,50,3], k = 4
> Output: 12.75000
> Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5], k = 1
> Output: 5.00000
> ```
> 
> **Constraints:**
> - n == nums.length
> - 1 <= k <= n <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> Maximizing average is equivalent to maximizing sum (k is fixed). Fixed-size sliding window on sum. Build initial window sum for first `k` elements. Slide: add `nums[i]`, remove `nums[i-k]`, update max. Trivial incremental sum — no auxiliary data structure needed.

> [!note]- Python Solution
> ```python
> def find_max_average(nums, k):
>     window_sum = sum(nums[:k])
>     best = window_sum
>     for i in range(k, len(nums)):
>         window_sum += nums[i] - nums[i - k]
>         best = max(best, window_sum)
>     return best / k
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Compute sum for every window from scratch O(nk) — unnecessary; prefix sum O(n) equivalent.

---

### Permutation in String (LC 567) `⚡ T1`

> [!example] Problem
> Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.
> In other words, return true if one of s1's permutations is the substring of s2.
> 
> **Example 1:**
> ```
> Input: s1 = "ab", s2 = "eidbaooo"
> Output: true
> Explanation: s2 contains one permutation of s1 ("ba").
> ```
> 
> **Example 2:**
> ```
> Input: s1 = "ab", s2 = "eidboaoo"
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s1.length, s2.length <= 10^4
> - s1 and s2 consist of lowercase English letters.

> [!info] Approach
> A permutation has the same character frequencies. Fixed window of size `len(s1)` with frequency matching. Same match-counter technique as Find All Anagrams — identical logic, just return True/False. When `matches == required` at any valid window position → return True.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def check_inclusion(s1, s2):
>     if len(s1) > len(s2):
>         return False
>     need = Counter(s1)
>     window = {}
>     matches = 0
>     required = len(need)
>     k = len(s1)
> 
>     for right in range(len(s2)):
>         c = s2[right]
>         window[c] = window.get(c, 0) + 1
>         if c in need and window[c] == need[c]:
>             matches += 1
> 
>         if right >= k:
>             lc = s2[right - k]
>             if lc in need and window[lc] == need[lc]:
>                 matches -= 1
>             window[lc] -= 1
>             if window[lc] == 0:
>                 del window[lc]
> 
>         if right >= k - 1 and matches == required:
>             return True
> 
>     return False
> ```

> [!success] Complexity
> O(n) time where n = len(s2), O(|alphabet|) space.

> [!tip] Alternatives
> Sort both strings per window O(nk log k) — too slow; direct Counter comparison O(n · 26) — correct but slower constant.

---

## Variable Window — At Most K

> [!info] Approach
> Expand `right` greedily; when the constraint is violated, shrink `left` until it's satisfied again. Each element enters and exits the window exactly once → O(n) amortized. Window length `right - left + 1` at any valid state is a candidate for the maximum.

---

### Longest Substring Without Repeating Characters (LC 3) `⚡ T1`

> [!example] Problem
> Given a string s, find the length of the longest substring without duplicate characters.
> 
> **Example 1:**
> ```
> Input: s = "abcabcbb"
> Output: 3
> Explanation: The answer is "abc", with the length of 3.
> ```
> 
> **Example 2:**
> ```
> Input: s = "bbbbb"
> Output: 1
> Explanation: The answer is "b", with the length of 1.
> ```
> 
> **Example 3:**
> ```
> Input: s = "pwwkew"
> Output: 3
> Explanation: The answer is "wke", with the length of 3.
> Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
> ```
> 
> **Constraints:**
> - 0 <= s.length <= 5 * 10^4
> - s consists of English letters, digits, symbols and spaces.

> [!info] Approach
> At most 0 duplicate characters per window. Expanding right adds a character; if it duplicates, shrink left past the previous occurrence. Track last-seen index of each character. On duplicate: `left = last_seen[c] + 1` (jump, not step-by-step). Only jump `left` if `last_seen[c] >= left` (character might be outside current window — stale).

> [!note]- Python Solution
> ```python
> def length_of_longest_substring(s):
>     last_seen = {}
>     left = 0
>     best = 0
>     for right, c in enumerate(s):
>         if c in last_seen and last_seen[c] >= left:
>             left = last_seen[c] + 1   # jump past previous occurrence
>         last_seen[c] = right
>         best = max(best, right - left + 1)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(|alphabet|) space.

> [!tip] Alternatives
> Frequency map + step-by-step shrink — also O(n) but more steps; jump optimization is constant-factor faster.

---

### Longest Repeating Character Replacement (LC 424) `⚡ T1`

> [!example] Problem
> You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.
> Return the length of the longest substring containing the same letter you can get after performing the above operations.
> 
> **Example 1:**
> ```
> Input: s = "ABAB", k = 2
> Output: 4
> Explanation: Replace the two 'A's with two 'B's or vice versa.
> ```
> 
> **Example 2:**
> ```
> Input: s = "AABABBA", k = 1
> Output: 4
> Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
> The substring "BBBB" has the longest repeating letters, which is 4.
> There may exists other ways to achieve this answer too.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s consists of only uppercase English letters.
> - 0 <= k <= s.length

> [!info] Approach
> In a window of length `L`, we need `L - max_count <= k` (replace all non-max-frequency characters). Expand while valid; shrink otherwise. Track `max_count` — the frequency of the most common character in the window. When `(window_size - max_count) > k` → shrink. Key insight: `max_count` never needs to decrease (we only care about the *best* window seen so far). When we shrink, `max_count` stays the same, and the window stays the same size or shrinks — we're looking for a *longer* window.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def character_replacement(s, k):
>     freq = defaultdict(int)
>     max_count = 0
>     left = 0
>     best = 0
> 
>     for right, c in enumerate(s):
>         freq[c] += 1
>         max_count = max(max_count, freq[c])
>         # Window invalid: replacements needed exceed k
>         if (right - left + 1) - max_count > k:
>             freq[s[left]] -= 1
>             left += 1   # shrink by 1
>             don't update max_count (intentional)
>         best = max(best, right - left + 1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(26) = O(1) space.

> [!tip] Alternatives
> Binary search on answer + sliding window validation — O(n log n); direct sliding window is O(n).

---

### Fruits Into Baskets (At Most 2 Distinct) (LC 904)

> [!example] Problem
> You are visiting a farm that has a single row of fruit trees arranged from left to right. The trees are represented by an integer array fruits where fruits[i] is the type of fruit the ith tree produces.
> You want to collect as much fruit as possible. However, the owner has some strict rules that you must follow:
> Given the integer array fruits, return the maximum number of fruits you can pick.
> 
> **Example 1:**
> ```
> Input: fruits = [1,2,1]
> Output: 3
> Explanation: We can pick from all 3 trees.
> ```
> 
> **Example 2:**
> ```
> Input: fruits = [0,1,2,2]
> Output: 3
> Explanation: We can pick from trees [1,2,2].
> If we had started at the first tree, we would only pick from trees [0,1].
> ```
> 
> **Example 3:**
> ```
> Input: fruits = [1,2,3,2,2]
> Output: 4
> Explanation: We can pick from trees [2,3,2,2].
> If we had started at the first tree, we would only pick from trees [1,2].
> ```
> 
> **Constraints:**
> - 1 <= fruits.length <= 10^5
> - 0 <= fruits[i] < fruits.length

> [!info] Approach
> Longest subarray with at most 2 distinct values. Direct application of at-most-K window. Frequency map. While `len(freq) > 2` → shrink left: decrement `freq[s[left]]`; delete key if 0. Window length `right - left + 1` after shrinking is the candidate answer.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def total_fruit(fruits):
>     freq = defaultdict(int)
>     left = 0
>     best = 0
> 
>     for right, f in enumerate(fruits):
>         freq[f] += 1
>         while len(freq) > 2:
>             freq[fruits[left]] -= 1
>             if freq[fruits[left]] == 0:
>                 del freq[fruits[left]]
>             left += 1
>         best = max(best, right - left + 1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space (at most 3 keys ever in freq map).

> [!tip] Alternatives
> Identical to "Longest Substring with At Most K Distinct" with k=2.

---

### Longest Substring with At Most K Distinct Characters (LC 340)

> [!example] Problem
> Given a string `s` and an integer `k`, return *the length of the longest **substring** of* `s` *that contains at most* `k` ***distinct `🎯 T2`** characters*.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** s = "eceba", k = 2
> **Output:** 3
> **Explanation:** The substring is "ece" with length 3.
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** s = "aa", k = 1
> **Output:** 2
> **Explanation:** The substring is "aa" with length 2.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= s.length <= 5 * 10^4`
> 	
> - `0 <= k <= 50`

> [!info] Approach
> General form of the "at most K distinct" pattern. Shrink window when distinct count exceeds k. Frequency map. While `len(freq) > k` → shrink left. Window length is candidate answer. Remove key from freq map when its count reaches 0 to keep `len(freq)` accurate.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def length_of_longest_substring_k_distinct(s, k):
>     freq = defaultdict(int)
>     left = 0
>     best = 0
> 
>     for right, c in enumerate(s):
>         freq[c] += 1
>         while len(freq) > k:
>             freq[s[left]] -= 1
>             if freq[s[left]] == 0:
>                 del freq[s[left]]
>             left += 1
>         best = max(best, right - left + 1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> For k=1 or k=2, trivial optimizations possible but not needed.

---

## Variable Window — Exactly K

> [!info] Approach
> "Exactly K" windows are hard to count directly because shrinking can overshoot. The trick: `exactly(k) = at_most(k) - at_most(k-1)`. Both `at_most` calls are O(n), giving O(n) total.

---

### Subarrays with K Different Integers (LC 992) `⚡ T1`

> [!example] Problem
> Given an integer array nums and an integer k, return the number of good subarrays of nums.
> A good array is an array where the number of different integers in that array is exactly k.
> A subarray is a contiguous part of an array.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,1,2,3], k = 2
> Output: 7
> Explanation: Subarrays formed with exactly 2 different integers: [1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2], [1,2,1,2]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,1,3,4], k = 3
> Output: 3
> Explanation: Subarrays formed with exactly 3 different integers: [1,2,1,3], [2,1,3], [1,3,4].
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - 1 <= nums[i], k <= nums.length

> [!info] Approach
> The "exactly k" constraint is not monotone for a window — adding elements can go over or under. Reframe as difference of two at-most problems. `at_most(k)` counts subarrays with ≤ k distinct values. Use a window where every valid `[left, right]` contributes `right - left + 1` subarrays (all subarrays ending at `right`). `count(exactly k) = at_most(k) - at_most(k-1)`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def subarrays_with_k_distinct(nums, k):
>     def at_most(k):
>         freq = defaultdict(int)
>         left = count = 0
>         for right, n in enumerate(nums):
>             freq[n] += 1
>             while len(freq) > k:
>                 freq[nums[left]] -= 1
>                 if freq[nums[left]] == 0:
>                     del freq[nums[left]]
>                 left += 1
>             count += right - left + 1   # all subarrays [left..right], [left+1..right], ...
>         return count
> 
>     return at_most(k) - at_most(k - 1)
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Prefix sums + hashing O(n) — more complex; sliding window `exactly` without the trick requires two separate left pointers.

---

### Count Number of Nice Subarrays (LC 1248)

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
> Remap: odd → 1, even → 0. Problem becomes: count subarrays with sum exactly k. Same `at_most(k) - at_most(k-1)` trick applies. `at_most(k)` counts subarrays with at most k odd numbers. Sum of `right - left + 1` across valid windows. Window is valid when count of odds ≤ k. Shrink when count > k.

> [!note]- Python Solution
> ```python
> def number_of_subarrays(nums, k):
>     def at_most(k):
>         left = count = odds = 0
>         for right in range(len(nums)):
>             if nums[right] % 2 == 1:
>                 odds += 1
>             while odds > k:
>                 if nums[left] % 2 == 1:
>                     odds -= 1
>                 left += 1
>             count += right - left + 1
>         return count
> 
>     return at_most(k) - at_most(k - 1)
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix sum approach: count prefix sums, use `prefix[i] - prefix[j] == k` → O(n) with hashmap. Equivalent in complexity.

---

## Variable Window — Minimum Length

> [!info] Approach
> Expand `right` until the window satisfies the constraint (becomes valid). Then shrink `left` as long as the window remains valid, recording the minimum length. Swap the "update answer" location from the expansion step to the shrink step.

---

### Minimum Size Subarray Sum (LC 209)

> [!example] Problem
> Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.
> 
> **Example 1:**
> ```
> Input: target = 7, nums = [2,3,1,2,4,3]
> Output: 2
> Explanation: The subarray [4,3] has the minimal length under the problem constraint.
> ```
> 
> **Example 2:**
> ```
> Input: target = 4, nums = [1,4,4]
> Output: 1
> ```
> 
> **Example 3:**
> ```
> Input: target = 11, nums = [1,1,1,1,1,1,1,1]
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= target <= 10^9
> - 1 <= nums.length <= 10^5
> - 1 <= nums[i] <= 10^4

> [!info] Approach
> Positive integers mean adding elements always increases sum, removing always decreases. Window constraint is monotone → shrink while valid. Expand right; once sum ≥ target, shrink left while still valid. Record minimum length at each valid state. Inner while loop shrinks and records — the answer is updated at the tightest valid window for each right.

> [!note]- Python Solution
> ```python
> def min_subarray_len(target, nums):
>     left = 0
>     window_sum = 0
>     best = float('inf')
> 
>     for right in range(len(nums)):
>         window_sum += nums[right]
>         while window_sum >= target:
>             best = min(best, right - left + 1)
>             window_sum -= nums[left]
>             left += 1
> 
>     return best if best != float('inf') else 0
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Binary search on length + prefix sum O(n log n) — works but unnecessary here; negative numbers would break window approach → use Kadane-style DP instead.

---

### Minimum Window Substring (LC 76) `⚡ T1`

> [!example] Problem
> Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".
> The testcases will be generated such that the answer is unique.
> 
> **Example 1:**
> ```
> Input: s = "ADOBECODEBANC", t = "ABC"
> Output: "BANC"
> Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.
> ```
> 
> **Example 2:**
> ```
> Input: s = "a", t = "a"
> Output: "a"
> Explanation: The entire string s is the minimum window.
> ```
> 
> **Example 3:**
> ```
> Input: s = "a", t = "aa"
> Output: ""
> Explanation: Both 'a's from t must be included in the window.
> Since the largest window of s only has one 'a', return empty string.
> ```
> 
> **Constraints:**
> - m == s.length
> - n == t.length
> - 1 <= m, n <= 10^5
> - s and t consist of uppercase and lowercase English letters.

> [!info] Approach
> Need to cover all characters of `t`. Use a `missing` counter — total characters still needed. Once 0 → window is valid → shrink. Expand right: if `need[c] > 0` before decrement, `missing -= 1`. Shrink while `missing == 0`: advance left past non-required characters (those with `need[s[left]] < 0`), record window, then remove `s[left]` from window. `need` can go negative (excess characters) — only decrement `missing` when `need[c]` was positive (character was still required).

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def min_window(s, t):
>     need = Counter(t)
>     missing = len(t)    # total characters still needed
>     best_start = best_len = 0
>     found = False
>     left = 0
> 
>     for right, c in enumerate(s):
>         if need[c] > 0:
>             missing -= 1
>         need[c] -= 1
> 
>         if missing == 0:                    # valid window found
>             while need[s[left]] < 0:       # shrink: skip excess characters
>                 need[s[left]] += 1
>                 left += 1
>             # s[left] is now required — record this tightest window
>             if not found or right - left + 1 < best_len:
>                 best_start = left
>                 best_len = right - left + 1
>                 found = True
>             # Slide: invalidate window to search for next candidate
>             need[s[left]] += 1
>             missing += 1
>             left += 1
> 
>     return s[best_start:best_start + best_len] if found else ""
> ```

> [!success] Complexity
> O(|s| + |t|) time, O(|alphabet|) space.

> [!tip] Alternatives
> Two-pointer with explicit char counts O(n) — equivalent; the `missing` trick avoids full dict comparison.

---

## Sliding Window + Monotonic Deque

> [!info] Approach
> A monotonic deque stores indices in order of decreasing value (for max) or increasing value (for min). The front always holds the extreme element for the current window. Amortized O(1) per element: each index is pushed and popped at most once.

---

### Sliding Window Maximum (LC 239) `⚡ T1`

> [!example] Problem
> You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
> Return the max sliding window.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
> Output: [3,3,5,5,6,7]
> Explanation: 
> Window position                Max
> ---------------               -----
> [1  3  -1] -3  5  3  6  7       3
>  1 [3  -1  -3] 5  3  6  7       3
>  1  3 [-1  -3  5] 3  6  7       5
>  1  3  -1 [-3  5  3] 6  7       5
>  1  3  -1  -3 [5  3  6] 7       6
>  1  3  -1  -3  5 [3  6  7]      7
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
> - 1 <= k <= nums.length

> [!info] Approach
> Recomputing max per window is O(nk). A deque maintaining a decreasing sequence of indices gives O(1) max lookup. Deque stores indices in decreasing order of their values. Front = index of max for current window. Before adding `i`: (1) pop front if it's outside window `[i-k+1, i]`; (2) pop back while `nums[deque[-1]] <= nums[i]` (smaller elements can never be max while `i` is in window). Append `i`. Record `nums[deque[0]]` once `i >= k-1`.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def max_sliding_window(nums, k):
>     dq: deque[int] = deque()  # stores indices
>     front = max of current window
>     result = []
> 
>     for i, val in enumerate(nums):
>         # Remove indices outside current window
>         if dq and dq[0] < i - k + 1:
>             dq.popleft()
>         # Maintain decreasing order: evict smaller elements from back
>         while dq and nums[dq[-1]] < val:
>             dq.pop()
>         dq.append(i)
>         if i >= k - 1:
>             result.append(nums[dq[0]])
> 
>     return result
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Segment tree or sparse table — O(n log n) build + O(1) query; overkill. Max-heap O(n log k) — correct but slower. Deque is optimal for this specific problem.

---

### Sliding Window Minimum (LC variant)

> [!example] Problem
> Array of integers, window size `k`. Return min of each window as it slides.

> [!info] Approach
> Symmetric to sliding window maximum. Monotonic increasing deque where front = current min. Deque stores indices in increasing order of their values. Pop back while `nums[deque[-1]] >= val` (larger elements evicted — they can never be min while `val` is in window). Only change from max version: reverse comparison `nums[dq[-1]] > val` (use `>=` to maintain strictly increasing, or `>` for non-strictly).

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def min_sliding_window(nums, k):
>     dq: deque[int] = deque()  # stores indices
>     front = min of current window
>     result = []
> 
>     for i, val in enumerate(nums):
>         if dq and dq[0] < i - k + 1:
>             dq.popleft()
>         while dq and nums[dq[-1]] > val:
>             dq.pop()
>         dq.append(i)
>         if i >= k - 1:
>             result.append(nums[dq[0]])
> 
>     return result
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Same as sliding window maximum — deque is optimal at O(n).

> [!info] Deque Invariant
> For max → deque is decreasing (pop smaller from back). For min → deque is increasing (pop larger from back). Front always holds the extreme index for the current window; expiry check (`dq[0] < i - k + 1`) ensures it stays within bounds.

---

## Fixed Window — Threshold & Uniqueness

---

### Number of Sub-arrays of Size K and Average ≥ Threshold (LC 1343)

> [!example] Problem
> Given an array of integers arr and two integers k and threshold, return the number of sub-arrays of size k and average greater than or equal to threshold.
> 
> **Example 1:**
> ```
> Input: arr = [2,2,2,2,5,5,5,8], k = 3, threshold = 4
> Output: 3
> Explanation: Sub-arrays [2,5,5],[5,5,5] and [5,5,8] have averages 4, 5 and 6 respectively. All other sub-arrays of size 3 have averages less than 4 (the threshold).
> ```
> 
> **Example 2:**
> ```
> Input: arr = [11,13,17,23,29,31,7,5,2,3], k = 3, threshold = 5
> Output: 6
> Explanation: The first 6 sub-arrays of size 3 have averages greater than 5. Note that averages are not integers.
> ```
> 
> **Constraints:**
> - 1 <= arr.length <= 10^5
> - 1 <= arr[i] <= 10^4
> - 1 <= k <= arr.length
> - 0 <= threshold <= 10^4

> [!info] Approach
> Fixed window of size `k`; average ≥ threshold ↔ sum ≥ k * threshold. Avoids float division per window. Maintain a sliding sum over every window of length `k`. Count windows where sum ≥ `k * threshold`. Seed with sum of first `k` elements. Slide: add `arr[i]`, subtract `arr[i-k]`, check threshold.

> [!note]- Python Solution
> ```python
> def num_of_subarrays(arr, k, threshold):
>     target = k * threshold
>     window_sum = sum(arr[:k])
>     count = 1 if window_sum >= target else 0
>     for i in range(k, len(arr)):
>         window_sum += arr[i] - arr[i - k]
>         if window_sum >= target:
>             count += 1
>     return count
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix sums give the same O(n) but with O(n) extra space; sliding sum is strictly better here.

---

### Maximum Sum of Almost Unique Subarray (LC 2841)

> [!example] Problem
> You are given an integer array nums and two positive integers m and k.
> Return the maximum sum out of all almost unique subarrays of length k of nums. If no such subarray exists, return 0.
> A subarray of nums is almost unique if it contains at least m distinct elements.
> A subarray is a contiguous non-empty sequence of elements within an array.
> 
> **Example 1:**
> ```
> Input: nums = [2,6,7,3,1,7], m = 3, k = 4
> Output: 18
> Explanation: There are 3 almost unique subarrays of size k = 4. These subarrays are [2, 6, 7, 3], [6, 7, 3, 1], and [7, 3, 1, 7]. Among these subarrays, the one with the maximum sum is [2, 6, 7, 3] which has a sum of 18.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5,9,9,2,4,5,4], m = 1, k = 3
> Output: 23
> Explanation: There are 5 almost unique subarrays of size k. These subarrays are [5, 9, 9], [9, 9, 2], [9, 2, 4], [2, 4, 5], and [4, 5, 4]. Among these subarrays, the one with the maximum sum is [5, 9, 9] which has a sum of 23.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,2,1,2,1,2,1], m = 3, k = 3
> Output: 0
> Explanation: There are no subarrays of size k = 3 that contain at least m = 3 distinct elements in the given array [1,2,1,2,1,2,1]. Therefore, no almost unique subarrays exist, and the maximum sum is 0.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - 1 <= m <= k <= nums.length
> - 1 <= nums[i] <= 10^9

> [!info] Approach
> Fixed window of size `k`; track distinct count in the window alongside the running sum. Maintain a frequency map and window sum. A window qualifies when `len(freq) >= m`. Slide in O(1): add right element to freq/sum, remove left element from freq/sum (delete key at 0). Check qualification after each full window.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def max_sum(nums, m, k):
>     freq = defaultdict(int)
>     window_sum = 0
>     best = 0
> 
>     for i in range(len(nums)):
>         freq[nums[i]] += 1
>         window_sum += nums[i]
>         if i >= k:
>             old = nums[i - k]
>             window_sum -= old
>             freq[old] -= 1
>             if freq[old] == 0:
>                 del freq[old]
>         if i >= k - 1 and len(freq) >= m:
>             best = max(best, window_sum)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Sorting within each window O(nk log k) — far too slow. Sliding window with freq map is optimal.

---

### Sliding Window Average from Data Stream (LC 346)

> [!example] Problem
> Given a stream of integers and a window size, calculate the moving average of all integers in the sliding window.
> 
> Implement the `MovingAverage` class:
> 
> 	
> - `MovingAverage(int size)` Initializes the object with the size of the window `size`.
> 	
> - `double next(int val)` Returns the moving average of the last `size` values of the stream.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input**
> ["MovingAverage", "next", "next", "next", "next"]
> [[3], [1], [10], [3], [5]]
> **Output**
> [null, 1.0, 5.5, 4.66667, 6.0]
> 
> **Explanation**
> MovingAverage movingAverage = new MovingAverage(3);
> movingAverage.next(1); // return 1.0 = 1 / 1
> movingAverage.next(10); // return 5.5 = (1 + 10) / 2
> movingAverage.next(3); // return 4.66667 = (1 + 10 + 3) / 3
> movingAverage.next(5); // return 6.0 = (10 + 3 + 5) / 3
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= size <= 1000`
> 	
> - `-10^5 <= val <= 10^5`
> 	
> - At most `10^4` calls will be made to `next`.

> [!info] Approach
> Classic FIFO fixed window over a stream. Use a circular buffer (deque) of size `k`. Maintain a running sum. When deque reaches size `k`, subtract the oldest element before appending new one. `deque.popleft()` evicts oldest; `deque.append(val)` adds newest. No need to resum — O(1) update.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> class MovingAverage:
>     def __init__(self, size):
>         self.k = size
>         self.window: deque[int] = deque()
>         self.total = 0
> 
>     def next(self, val):
>         if len(self.window) == self.k:
>             self.total -= self.window.popleft()
>         self.window.append(val)
>         self.total += val
>         return self.total / len(self.window)
> ```

> [!success] Complexity
> O(1) per `next` call, O(k) space.

> [!tip] Alternatives
> Recompute sum each call O(k) per call — unnecessary; circular array with modulo index works but deque is cleaner.

---

## Variable Window — Max Length (Flip / Delete)

> [!info] Approach
> A class of problems where you can "spend" a budget (flip zeros, delete elements) to extend a valid window. The window tracks how much budget has been used; shrink when budget is exceeded. Equivalent to "at most K bad elements".

---

### Max Consecutive Ones III (LC 1004) `⚡ T1`

> [!example] Problem
> Given a binary array nums and an integer k, return the maximum number of consecutive 1's in the array if you can flip at most k 0's.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
> Output: 6
> Explanation: [1,1,1,0,0,1,1,1,1,1,1]
> Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
> Output: 10
> Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
> Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - nums[i] is either 0 or 1.
> - 0 <= k <= nums.length

> [!info] Approach
> Window contains at most `k` zeros. Expanding right adds ones (free) or zeros (costs 1 from budget). When zeros in window exceed `k`, shrink left. Track `zeros` count in the window. While `zeros > k` → if `nums[left] == 0`, decrement zeros; advance left. Answer is `right - left + 1` after each valid step — window never shrinks below the best size seen (LC 424 trick not needed here since we do want exact max).

> [!note]- Python Solution
> ```python
> def longest_ones(nums, k):
>     left = zeros = best = 0
>     for right in range(len(nums)):
>         if nums[right] == 0:
>             zeros += 1
>         while zeros > k:
>             if nums[left] == 0:
>                 zeros -= 1
>             left += 1
>         best = max(best, right - left + 1)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Same as "Longest Repeating Character Replacement" restricted to binary input. For k=0 this degenerates to counting max run of ones.

---

### Longest Subarray of 1s After Deleting One Element (LC 1493)

> [!example] Problem
> Given a binary array nums, you should delete one element from it.
> Return the size of the longest non-empty subarray containing only 1's in the resulting array. Return 0 if there is no such subarray.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,0,1]
> Output: 3
> Explanation: After deleting the number in position 2, [1,1,1] contains 3 numbers with value of 1's.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,1,1,0,1,1,0,1]
> Output: 5
> Explanation: After deleting the number in position 4, [0,1,1,1,1,1,0,1] longest subarray with value of 1's is [1,1,1,1,1].
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,1,1]
> Output: 2
> Explanation: You must delete one element.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - nums[i] is either 0 or 1.

> [!info] Approach
> Deleting one element = flipping one 0 to nothing, or dropping one 1. Equivalent to: longest window with at most one 0, minus 1 (for the deleted element). Slide window keeping `zeros <= 1`. The answer is `window_size - 1` at maximum valid window. Exact same code as LC 1004 with `k=1`, subtract 1 from result. Edge: if whole array is ones, deleting one element gives `n-1`.

> [!note]- Python Solution
> ```python
> def longest_subarray(nums):
>     left = zeros = best = 0
>     for right in range(len(nums)):
>         if nums[right] == 0:
>             zeros += 1
>         while zeros > 1:
>             if nums[left] == 0:
>                 zeros -= 1
>             left += 1
>         best = max(best, right - left + 1)
>     return best - 1   # subtract the one deleted element
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> LC 1004 with k=1 is identical before the -1 adjustment. If the array has no zeros, the answer is `len(nums) - 1`.

---

### Binary Subarrays with Sum (LC 930)

> [!example] Problem
> Given a binary array nums and an integer goal, return the number of non-empty subarrays with a sum goal.
> A subarray is a contiguous part of the array.
> 
> **Example 1:**
> ```
> Input: nums = [1,0,1,0,1], goal = 2
> Output: 4
> Explanation: The 4 subarrays are bolded and underlined below:
> [1,0,1,0,1]
> [1,0,1,0,1]
> [1,0,1,0,1]
> [1,0,1,0,1]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,0,0,0,0], goal = 0
> Output: 15
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - nums[i] is either 0 or 1.
> - 0 <= goal <= nums.length

> [!info] Approach
> Exactly-k trick: binary values make at_most well-defined. `exactly(goal) = at_most(goal) - at_most(goal-1)`. `at_most(k)` counts subarrays with sum ≤ k. Each right position contributes `right - left + 1` valid subarrays when window is valid. Shrink while sum > k. Handle `k < 0` edge case (return 0) to avoid infinite loop when goal=0.

> [!note]- Python Solution
> ```python
> def num_subarrays_with_sum(nums, goal):
>     def at_most(k):
>         if k < 0:
>             return 0
>         left = total = count = 0
>         for right in range(len(nums)):
>             total += nums[right]
>             while total > k:
>                 total -= nums[left]
>                 left += 1
>             count += right - left + 1
>         return count
> 
>     return at_most(goal) - at_most(goal - 1)
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix sum + hashmap: `count[prefix_sum - goal]` at each position — O(n) time, O(n) space. Both are valid; at_most trick is more uniform with other sliding window problems.

---

## Variable Window — Minimum Length (All Characters / Distinct)

---

### Minimum Window with All Characters Including Duplicates

> [!example] Problem
> Generalisation of LC 76: given `s` and `t` (with duplicate characters in `t`), find the shortest window in `s` containing all characters of `t` with correct multiplicities.

> [!info] Approach
> This IS LC 76 — the standard minimum window already handles duplicates via `missing` counter. `need[c]` tracks remaining required copies. `missing` = total characters still needed. Shrink while `missing == 0`. On add: decrement `need[c]`; if it was positive, decrement `missing`. On remove: increment `need[s[left]]`; if it becomes positive, increment `missing`. This correctly handles excess copies.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def min_window_with_duplicates(s, t):
>     need = Counter(t)
>     missing = len(t)
>     left = best_start = 0
>     best_len = float('inf')
> 
>     for right, c in enumerate(s):
>         if need[c] > 0:
>             missing -= 1
>         need[c] -= 1
> 
>         if missing == 0:
>             # Tighten from left: skip characters in excess
>             while need[s[left]] < 0:
>                 need[s[left]] += 1
>                 left += 1
>             if right - left + 1 < best_len:
>                 best_len = right - left + 1
>                 best_start = left
>             # Advance left to look for next candidate
>             need[s[left]] += 1
>             missing += 1
>             left += 1
> 
>     return s[best_start: best_start + best_len] if best_len != float('inf') else ""
> ```

> [!success] Complexity
> O(|s| + |t|) time, O(|alphabet|) space.

> [!tip] Alternatives
> Two separate left pointers (one for shrinking to exact fit, one for advancing) — functionally identical but more bookkeeping.

---

### Smallest Subarray with Distinct Element Count K

> [!example] Problem
> Given array `nums` and integer `k`, find the length of the shortest contiguous subarray that contains exactly `k` distinct elements.

> [!info] Approach
> Minimum-length window with an exact distinct count. Expand until we have ≥ k distinct, then shrink while we still have ≥ k distinct, recording the minimum. Frequency map tracks distinct count. Once `len(freq) >= k` → window is valid → shrink left while still valid. Shrink: remove `nums[left]` from freq (delete at 0); stop when `len(freq) < k`. Record window size before overshoot.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def smallest_subarray_k_distinct(nums, k):
>     freq = defaultdict(int)
>     left = 0
>     best = float('inf')
> 
>     for right in range(len(nums)):
>         freq[nums[right]] += 1
>         while len(freq) >= k:
>             best = min(best, right - left + 1)
>             freq[nums[left]] -= 1
>             if freq[nums[left]] == 0:
>                 del freq[nums[left]]
>             left += 1
> 
>     return best if best != float('inf') else -1
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Outer loop on left + inner scan right O(n²) — brute force. Sliding window is O(n).

---

## Sliding Window + Monotonic Deque — Variable Window

---

### Longest Continuous Subarray with Absolute Diff ≤ Limit (LC 1438)

> [!example] Problem
> Given an array of integers nums and an integer limit, return the size of the longest non-empty subarray such that the absolute difference between any two elements of this subarray is less than or equal to limit.
> 
> **Example 1:**
> ```
> Input: nums = [8,2,4,7], limit = 4
> Output: 2 
> Explanation: All subarrays are: 
> [8] with maximum absolute diff |8-8| = 0  4. 
> [8,2,4] with maximum absolute diff |8-2| = 6 > 4.
> [8,2,4,7] with maximum absolute diff |8-2| = 6 > 4.
> [2] with maximum absolute diff |2-2| = 0  4.
> [4] with maximum absolute diff |4-4| = 0 <= 4.
> [4,7] with maximum absolute diff |4-7| = 3 <= 4.
> [7] with maximum absolute diff |7-7| = 0 <= 4. 
> Therefore, the size of the longest subarray is 2.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [10,1,2,4,7,2], limit = 5
> Output: 4 
> Explanation: The subarray [2,4,7,2] is the longest since the maximum absolute diff is |2-7| = 5 <= 5.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [4,2,2,2,4,4,2,2], limit = 0
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - 1 <= nums[i] <= 10^9
> - 0 <= limit <= 10^9

> [!info] Approach
> `max(window) - min(window) <= limit`. Need O(1) running max and min under variable window. Two deques: one decreasing (max), one increasing (min). Maintain `max_dq` (decreasing) and `min_dq` (increasing). Both store indices. When `max_dq[0] - min_dq[0] > limit` → shrink left, evicting stale front indices from both deques. Shrink by advancing `left`; pop deque fronts when they equal `left` (no longer in window). Record `right - left + 1` after each valid state.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def longest_subarray(nums, limit):
>     max_dq: deque[int] = deque()  # decreasing → front is max
>     min_dq: deque[int] = deque()  # increasing → front is min
>     left = best = 0
> 
>     for right, val in enumerate(nums):
>         while max_dq and nums[max_dq[-1]] <= val:
>             max_dq.pop()
>         while min_dq and nums[min_dq[-1]] >= val:
>             min_dq.pop()
>         max_dq.append(right)
>         min_dq.append(right)
> 
>         while nums[max_dq[0]] - nums[min_dq[0]] > limit:
>             left += 1
>             if max_dq[0] < left:
>                 max_dq.popleft()
>             if min_dq[0] < left:
>                 min_dq.popleft()
> 
>         best = max(best, right - left + 1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(n) space (deques store at most n indices total).

> [!tip] Alternatives
> Sorted container (SortedList) O(n log n) — valid but slower; segment tree O(n log n) — overkill. Two-deque is optimal O(n).

---

### Jump Game VI (LC 1696) `🎯 T2`

> [!example] Problem
> You are given a 0-indexed integer array nums and an integer k.
> You are initially standing at index 0. In one move, you can jump at most k steps forward without going outside the boundaries of the array. That is, you can jump from index i to any index in the range [i + 1, min(n - 1, i + k)] inclusive.
> You want to reach the last index of the array (index n - 1). Your score is the sum of all nums[j] for each index j you visited in the array.
> Return the maximum score you can get.
> 
> **Example 1:**
> ```
> Input: nums = [1,-1,-2,4,-7,3], k = 2
> Output: 7
> Explanation: You can choose your jumps forming the subsequence [1,-1,4,3] (underlined above). The sum is 7.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [10,-5,-2,4,0,3], k = 3
> Output: 17
> Explanation: You can choose your jumps forming the subsequence [10,4,3] (underlined above). The sum is 17.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,-5,-20,4,-1,3,-6,-3], k = 2
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= nums.length, k <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> DP recurrence: `dp[i] = nums[i] + max(dp[i-k], ..., dp[i-1])`. Naive O(nk). Optimize with a decreasing deque of the last `k` dp values — front = max in range. `dp[i] = nums[i] + dp[deque_front]`. Maintain deque in decreasing dp-value order. Evict front when it's outside the `k`-window. Before computing `dp[i]`: evict stale front (`dq[0] < i - k`). After computing `dp[i]`: evict back while `dp[dq[-1]] <= dp[i]`; append `i`. Space-optimise by storing dp in original array.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def max_result(nums, k):
>     n = len(nums)
>     dp = [0] * n
>     dp[0] = nums[0]
>     dq: deque[int] = deque()
>     dq.append(0)
> 
>     for i in range(1, n):
>         # Evict indices outside the k-window
>         while dq and dq[0] < i - k:
>             dq.popleft()
>         dp[i] = nums[i] + dp[dq[0]]
>         # Maintain decreasing deque by dp value
>         while dq and dp[dq[-1]] <= dp[i]:
>             dq.pop()
>         dq.append(i)
> 
>     return dp[n - 1]
> ```

> [!success] Complexity
> O(n) time, O(n) space (dp array + deque).

> [!tip] Alternatives
> Priority heap O(n log k) — correct but slower; sparse table for range max O(n log n) build + O(1) query, O(n log n) overall — more complex. Deque DP is the idiomatic O(n) solution.

---

## More Variable Window Problems

---

### Subarray Product Less Than K (LC 713)

> [!example] Problem
> Given an array of integers nums and an integer k, return the number of contiguous subarrays where the product of all the elements in the subarray is strictly less than k.
> 
> **Example 1:**
> ```
> Input: nums = [10,5,2,6], k = 100
> Output: 8
> Explanation: The 8 subarrays that have product less than 100 are:
> [10], [5], [2], [6], [10, 5], [5, 2], [2, 6], [5, 2, 6]
> Note that [10, 5, 2] is not included as the product of 100 is not strictly less than k.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3], k = 0
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - 1 <= nums[i] <= 1000
> - 0 <= k <= 10^6

> [!info] Approach
> All elements are positive → product is monotonically non-decreasing as window expands. Shrink when product ≥ k. Maintain running product. Each valid window `[left, right]` contributes `right - left + 1` subarrays ending at `right` (all subarrays `[left..right], [left+1..right], ..., [right..right]` are valid). Shrink by dividing out `nums[left]` and advancing left. Handle edge `k <= 1` upfront (product of positives is always ≥ 1).

> [!note]- Python Solution
> ```python
> def num_subarray_product_less_than_k(nums, k):
>     if k <= 1:
>         return 0
>     left = count = 0
>     product = 1
>     for right in range(len(nums)):
>         product *= nums[right]
>         while product >= k:
>             product //= nums[left]
>             left += 1
>         count += right - left + 1
>     return count
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix products + binary search O(n log n) — works but unnecessary. Sliding window is O(n).

---

### Longest Subarray with Sum ≤ K (Nonnegative)

> [!example] Problem
> Array of non-negative integers `nums` and integer `k`. Find the length of the longest subarray with sum ≤ `k`.

> [!info] Approach
> Non-negative elements ensure monotone sum — expanding can only increase sum, so shrink-when-violated is valid. Expand right; when sum > k, shrink left. Track max window length after each step. The while-loop shrink guarantees the window is valid at every right before recording length.

> [!note]- Python Solution
> ```python
> def longest_subarray_sum_leq_k(nums, k):
>     left = window_sum = best = 0
>     for right in range(len(nums)):
>         window_sum += nums[right]
>         while window_sum > k:
>             window_sum -= nums[left]
>             left += 1
>         best = max(best, right - left + 1)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> With negative numbers: monotone queue approach or Kadane variant needed — shrink-when-violated breaks without non-negativity guarantee.

---

### Diet Plan Performance (LC 1176)

> [!example] Problem
> A dieter consumes `calories[i]` calories on the `i`-th day. 
> 
> Given an integer `k`, for **every** consecutive sequence of `k` days (`calories[i], calories[i+1], ..., calories[i+k-1]` for all `0 <= i <= n-k`), they look at *T*, the total calories consumed during that sequence of `k` days (`calories[i] + calories[i+1] + ... + calories[i+k-1]`):
> 
> 	
> - If `T < lower`, they performed poorly on their diet and lose 1 point; 
> 	
> - If `T > upper`, they performed well on their diet and gain 1 point;
> 	
> - Otherwise, they performed normally and there is no change in points.
> 
> Initially, the dieter has zero points. Return the total number of points the dieter has after dieting for `calories.length` days.
> 
> Note that the total points can be negative.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** calories = [1,2,3,4,5], k = 1, lower = 3, upper = 3
> **Output:** 0
> **Explanation**: Since k = 1, we consider each element of the array separately and compare it to lower and upper.
> calories[0] and calories[1] are less than lower so 2 points are lost.
> calories[3] and calories[4] are greater than upper so 2 points are gained.
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** calories = [3,2], k = 2, lower = 0, upper = 1
> **Output:** 1
> **Explanation**: Since k = 2, we consider subarrays of length 2.
> calories[0] + calories[1] > upper so 1 point is gained.
> 
> ```
> 
> Example 3:
> 
> ```
> 
> **Input:** calories = [6,5,0,0], k = 2, lower = 1, upper = 5
> **Output:** 0
> **Explanation**:
> calories[0] + calories[1] > upper so 1 point is gained.
> lower <= calories[1] + calories[2] <= upper so no change in points.
> calories[2] + calories[3] < lower so 1 point is lost.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= k <= calories.length <= 10^5`
> 	
> - `0 <= calories[i] <= 20000`
> 	
> - `0 <= lower <= upper`

> [!info] Approach
> Straightforward fixed window of size `k`. No state needed beyond running sum. Maintain sliding sum of exactly `k` elements. Compare to `lower` and `upper` each step. Seed with first `k` elements. Slide: add right, remove left-k, evaluate.

> [!note]- Python Solution
> ```python
> def diet_plan_performance(calories, k, lower, upper):
>     window_sum = sum(calories[:k])
>     score = 0
>     if window_sum < lower:
>         score -= 1
>     elif window_sum > upper:
>         score += 1
>     for i in range(k, len(calories)):
>         window_sum += calories[i] - calories[i - k]
>         if window_sum < lower:
>             score -= 1
>         elif window_sum > upper:
>             score += 1
>     return score
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Prefix sums O(n) time, O(n) space — equivalent. Sliding sum is strictly more space-efficient.

---

### Count Vowel Substrings of a Word (LC 2062)

> [!example] Problem
> A substring is a contiguous (non-empty) sequence of characters within a string.
> A vowel substring is a substring that only consists of vowels ('a', 'e', 'i', 'o', and 'u') and has all five vowels present in it.
> Given a string word, return the number of vowel substrings in word.
> 
> **Example 1:**
> ```
> Input: word = "aeiouu"
> Output: 2
> Explanation: The vowel substrings of word are as follows (underlined):
> - "aeiouu"
> - "aeiouu"
> ```
> 
> **Example 2:**
> ```
> Input: word = "unicornarihan"
> Output: 0
> Explanation: Not all 5 vowels are present, so there are no vowel substrings.
> ```
> 
> **Example 3:**
> ```
> Input: word = "cuaieuouac"
> Output: 7
> Explanation: The vowel substrings of word are as follows (underlined):
> - "cuaieuouac"
> - "cuaieuouac"
> - "cuaieuouac"
> - "cuaieuouac"
> - "cuaieuouac"
> - "cuaieuouac"
> - "cuaieuouac"
> ```
> 
> **Constraints:**
> - 1 <= word.length <= 100
> - word consists of lowercase English letters only.

> [!info] Approach
> Exactly-5-distinct-vowels, all characters must be vowels. Use the at_most trick restricted to vowel-only substrings. `at_most(k)` counts substrings (all vowels) with ≤ k distinct vowels. Filter non-vowels by resetting window. On encountering a consonant, reset `left = right + 1` and clear freq. `exactly(5) = at_most(5) - at_most(4)`.

> [!note]- Python Solution
> ```python
> def count_vowel_substrings(word):
>     vowels = set("aeiou")
> 
>     def at_most(k):
>         freq = {}
>         left = count = 0
>         for right, c in enumerate(word):
>             if c not in vowels:
>                 freq.clear()
>                 left = right + 1
>                 continue
>             freq[c] = freq.get(c, 0) + 1
>             while len(freq) > k:
>                 lc = word[left]
>                 freq[lc] -= 1
>                 if freq[lc] == 0:
>                     del freq[lc]
>                 left += 1
>             count += right - left + 1
>         return count
> 
>     return at_most(5) - at_most(4)
> ```

> [!success] Complexity
> O(n) time, O(1) space (at most 5 keys in freq).

> [!tip] Alternatives
> Enumerate all substrings O(n²) with O(1) check — acceptable for small input but O(n) sliding window is preferred.

---

## See Also

[[two-pointers]] | [[hashing]] | [[string]] | [[queue]]
### Maximum Number of Vowels in a Substring of Given Length

> [!example] Problem
> Given a string s and an integer k, return the maximum number of vowel letters in any substring of s with length k.
> Vowel letters in English are 'a', 'e', 'i', 'o', and 'u'.
> 
> **Example 1:**
> ```
> Input: s = "abciiidef", k = 3
> Output: 3
> Explanation: The substring "iii" contains 3 vowel letters.
> ```
> 
> **Example 2:**
> ```
> Input: s = "aeiou", k = 2
> Output: 2
> Explanation: Any substring of length 2 contains 2 vowels.
> ```
> 
> **Example 3:**
> ```
> Input: s = "leetcode", k = 3
> Output: 2
> Explanation: "lee", "eet" and "ode" contain 2 vowels.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s consists of lowercase English letters.
> - 1 <= k <= s.length

> [!info] Approach
> The window size is fixed, so every move only removes one character and adds one character. That makes the update O(1) per step. Maintain a running vowel count for the current window and slide it across the string. Initialize the first window, then for each step subtract the left character, add the new right character, and update the best count.

> [!note]- Python Solution
> ```python
> def max_vowels(s, k):
>     vowels = set("aeiou")
>     cur = sum(ch in vowels for ch in s[:k])
>     best = cur
>     for i in range(k, len(s)):
>         cur += s[i] in vowels
>         cur -= s[i - k] in vowels
>         best = max(best, cur)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> The same fixed-window pattern works for average, distinct counts, and frequency-based substring problems.

---

## Sliding Window — More Problems

### Grumpy Bookstore Owner (LC 1052) `⚡ T1`

> [!example] Problem
> There is a bookstore owner that has a store open for n minutes. You are given an integer array customers of length n where customers[i] is the number of the customers that enter the store at the start of the ith minute and all those customers leave after the end of that minute.
> During certain minutes, the bookstore owner is grumpy. You are given a binary array grumpy where grumpy[i] is 1 if the bookstore owner is grumpy during the ith minute, and is 0 otherwise.
> When the bookstore owner is grumpy, the customers entering during that minute are not satisfied. Otherwise, they are satisfied.
> The bookstore owner knows a secret technique to remain not grumpy for minutes consecutive minutes, but this technique can only be used once.
> Return the maximum number of customers that can be satisfied throughout the day.
> 
> **Example 1:**
> ```
> Input: customers = [1,0,1,2,1,1,7,5], grumpy = [0,1,0,1,0,1,0,1], minutes = 3
> Output: 16
> Explanation:
> The bookstore owner keeps themselves not grumpy for the last 3 minutes.
> The maximum number of customers that can be satisfied = 1 + 1 + 1 + 1 + 7 + 5 = 16.
> ```
> 
> **Example 2:**
> ```
> Input: customers = [1], grumpy = [0], minutes = 1
> Output: 1
> ```
> 
> **Constraints:**
> - n == customers.length == grumpy.length
> - 1 <= minutes <= n <= 2 * 10^4
> - 0 <= customers[i] <= 1000
> - grumpy[i] is either 0 or 1.

> [!info] Approach
> Customers at non-grumpy minutes are always satisfied. Customers at grumpy minutes are only satisfied during the technique window. We want to choose the `minutes`-long window that maximises the extra customers gained. Base count = sum of `customers[i]` where `grumpy[i] == 0`. Extra count for a window = sum of `customers[i]` where `grumpy[i] == 1` within the window. Slide a fixed window of size `minutes` to find the maximum extra. Compute base. Slide window: at each step, add `customers[right] * grumpy[right]` and subtract `customers[right - minutes] * grumpy[right - minutes]`. Track max window extra.

> [!note]- Python Solution
> ```python
> def max_satisfied(customers, grumpy, minutes):
>     n = len(customers)
>     base = sum(customers[i] for i in range(n) if grumpy[i] == 0)
>     window_extra = sum(customers[i] * grumpy[i] for i in range(minutes))
>     max_extra = window_extra
>     for i in range(minutes, n):
>         window_extra += customers[i] * grumpy[i]
>         window_extra -= customers[i - minutes] * grumpy[i - minutes]
>         max_extra = max(max_extra, window_extra)
>     return base + max_extra
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Brute force O(n * minutes): slide and recompute the window sum from scratch each step.
> - Key insight: separate "always satisfied" from "sometimes satisfied" — only the grumpy minutes within the window contribute to the extra gain.

---

### Minimum Number of Flips to Make Binary String Alternating (LC 1888)

> [!example] Problem
> You are given a binary string s. You are allowed to perform two types of operations on the string in any sequence:
> Return the minimum number of type-2 operations you need to perform such that s becomes alternating.
> The string is called alternating if no two adjacent characters are equal.
> 
> **Example 1:**
> ```
> Input: s = "111000"
> Output: 2
> Explanation: Use the first operation two times to make s = "100011".
> Then, use the second operation on the third and sixth elements to make s = "101010".
> ```
> 
> **Example 2:**
> ```
> Input: s = "010"
> Output: 0
> Explanation: The string is already alternating.
> ```
> 
> **Example 3:**
> ```
> Input: s = "1110"
> Output: 1
> Explanation: Use the second operation on the second element to make s = "1010".
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s[i] is either '0' or '1'.

> [!info] Approach
> There are only two valid alternating patterns: "0101..." and "1010...". Simulate all cyclic shifts by doubling the string and using a sliding window of length `n`. Double the string (`s + s`). For each window of length `n`, count the differences from both target patterns. Take the minimum differences seen across all windows. Use a sliding window on `s + s`. Maintain the count of mismatches with pattern "010101..." and "101010...". Slide: subtract the outgoing character's mismatch contribution, add the incoming character's. Track the minimum.

> [!note]- Python Solution
> ```python
> def min_flips(s):
>     n = len(s)
>     doubled = s + s
>     diff0 = 0   # mismatches vs "010101..."
>     diff1 = 0   # mismatches vs "101010..."
>     for i in range(n):
>         expected0 = '0' if i % 2 == 0 else '1'
>         expected1 = '1' if i % 2 == 0 else '0'
>         if doubled[i] != expected0:
>             diff0 += 1
>         if doubled[i] != expected1:
>             diff1 += 1
>     result = min(diff0, diff1)
>     for i in range(n, 2 * n):
>         incoming_pos = i % n
>         expected0_in = '0' if i % 2 == 0 else '1'
>         expected1_in = '1' if i % 2 == 0 else '0'
>         if doubled[i] != expected0_in:
>             diff0 += 1
>         if doubled[i] != expected1_in:
>             diff1 += 1
>         outgoing_pos = i - n
>         expected0_out = '0' if outgoing_pos % 2 == 0 else '1'
>         expected1_out = '1' if outgoing_pos % 2 == 0 else '0'
>         if doubled[outgoing_pos] != expected0_out:
>             diff0 -= 1
>         if doubled[outgoing_pos] != expected1_out:
>             diff1 -= 1
>         result = min(result, diff0, diff1)
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(n) for the doubled string.

> [!tip] Alternatives
> - O(n²) brute force: try every cyclic shift, count flips each time.
> - Key insight: doubling the string converts cyclic shifts into a standard sliding window on a linear string.

---

## See Also

[[two-pointers]] | [[array]] | [[hashing]] | [[string-algorithms]]
