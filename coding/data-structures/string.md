---
tags: [coding, data-structures, string]
topic: String
difficulty: mixed
---

# String Problems — Deep Dive

Pattern tags: frequency map, two pointers, sliding window, hashing, parsing.


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## Frequency Map / Anagram

### Valid Anagram `🔥 Google`

> [!example] Problem
> Given two strings s and t, return true if t is an anagram of s, and false otherwise.
> 
> **Example 1:**
> ```
> Input: s = "anagram", t = "nagaram"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: s = "rat", t = "car"
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s.length, t.length <= 5 * 10^4
> - s and t consist of lowercase English letters.

> [!info] Approach
> Two strings are anagrams iff they are identical after sorting. Sorting is O(n log n). We can do O(n) by comparing character frequency vectors. A 26-bucket frequency array (fixed alphabet) or a `Counter`. Two strings are anagrams iff their frequency maps are equal. Build `Counter(s)` and `Counter(t)`. Return `Counter(s) == Counter(t)`. For pure lowercase ASCII, use `[0]*26` and compare arrays — same asymptotic cost, better constant.


> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def is_anagram(s, t):
>     if len(s) != len(t):
>         return False
>     return Counter(s) == Counter(t)
> 
> # O(1) space variant for lowercase a-z only
> def is_anagram_array(s, t):
>     if len(s) != len(t):
>         return False
>     freq = [0] * 26
>     for c in s:
>         freq[ord(c) - ord('a')] += 1
>     for c in t:
>         freq[ord(c) - ord('a')] -= 1
>     return all(f == 0 for f in freq)
> ```

> [!success] Complexity
> Time O(n). Space O(1) for fixed alphabet (26 buckets), O(n) for general `Counter`.

> [!tip] Alternatives
> - Sorting: `sorted(s) == sorted(t)` — O(n log n), simpler to write, correct for Unicode.
> - XOR trick: works only if each character appears an even number of times — too restrictive for general anagram check.

---

### Group Anagrams `🔥 Google`

> [!example] Problem
> Given an array of strings strs, group the anagrams together. You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: strs = ["eat","tea","tan","ate","nat","bat"]
> Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
> Explanation:
> ```
> 
> **Example 2:**
> ```
> Input: strs = [""]
> Output: [[""]]
> ```
> 
> **Example 3:**
> ```
> Input: strs = ["a"]
> Output: [["a"]]
> ```
> 
> **Constraints:**
> - 1 <= strs.length <= 10^4
> - 0 <= strs[i].length <= 100
> - strs[i] consists of lowercase English letters.

> [!info] Approach
> All anagrams share the same canonical form — their sorted version. Use that as a hash map key. HashMap from canonical key → list of anagrams. For pure lowercase ASCII, use a tuple of 26 frequency counts as key (avoids O(L log L) sort per word). For each word, compute `key = tuple(freq_array)` or `key = "".join(sorted(word))`. Append word to `groups[key]`. Return `list(groups.values())`.


> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def group_anagrams(strs):
>     groups = defaultdict(list)
>     for word in strs:
>         freq = [0] * 26
>         for c in word:
>             freq[ord(c) - ord('a')] += 1
>         groups[tuple(freq)].append(word)
>     return list(groups.values())
> ```

> [!success] Complexity
> Time O(N × L) where N = number of words, L = max word length. Space O(N × L).

> [!tip] Alternatives
> - Sort-based key `sorted(word)`: O(N × L log L) — simpler but slower due to the sort.
> - Prime product key: assign each letter a prime, key = product of primes for each char. O(N × L) but product overflows for long words — not safe.

---

### Find All Anagrams in a String `⭐ Google`

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
> We need a fixed-size sliding window of length `len(p)`. Comparing two frequency arrays is O(26) = O(1) per step. Fixed-size window sliding over `s`, maintaining a frequency array for the current window. Compare it to the target frequency array of `p`. Build `p_freq`. Maintain `w_freq` for the window. Add the incoming character on the right; evict the outgoing character on the left when the window exceeds `len(p)`. If arrays match, record the left index. Use a `matches` counter to avoid O(26) comparison: track how many of the 26 buckets currently match between `w_freq` and `p_freq`.


> [!note]- Python Solution
> ```python
> def find_anagrams(s, p):
>     if len(p) > len(s):
>         return []
>     p_freq = [0] * 26
>     w_freq = [0] * 26
>     for c in p:
>         p_freq[ord(c) - ord('a')] += 1
> 
>     matches = sum(1 for i in range(26) if p_freq[i] == w_freq[i])
>     result = []
> 
>     for i, c in enumerate(s):
>         # add right character
>         idx = ord(c) - ord('a')
>         if w_freq[idx] == p_freq[idx]:
>             matches -= 1
>         w_freq[idx] += 1
>         if w_freq[idx] == p_freq[idx]:
>             matches += 1
>         # remove left character
>         if i >= len(p):
>             out_idx = ord(s[i - len(p)]) - ord('a')
>             if w_freq[out_idx] == p_freq[out_idx]:
>                 matches -= 1
>             w_freq[out_idx] -= 1
>             if w_freq[out_idx] == p_freq[out_idx]:
>                 matches += 1
>         if matches == 26:
>             result.append(i - len(p) + 1)
>     return result
> ```

> [!success] Complexity
> Time O(|s| + |p|). Space O(1) — two fixed 26-element arrays.

> [!tip] Alternatives
> - Full array comparison `w_freq == p_freq` per step: O(26 × |s|) = O(|s|) — same asymptotics but worse constant than the `matches` counter.
> - Rolling hash: O(|s|) average, but hash collisions require O(|p|) verification — less reliable.

---

## Two Pointers — Palindrome

### Valid Palindrome `🔥 Google`

> [!example] Problem
> A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.
> Given a string s, return true if it is a palindrome, or false otherwise.
> 
> **Example 1:**
> ```
> Input: s = "A man, a plan, a canal: Panama"
> Output: true
> Explanation: "amanaplanacanalpanama" is a palindrome.
> ```
> 
> **Example 2:**
> ```
> Input: s = "race a car"
> Output: false
> Explanation: "raceacar" is not a palindrome.
> ```
> 
> **Example 3:**
> ```
> Input: s = " "
> Output: true
> Explanation: s is an empty string "" after removing non-alphanumeric characters.
> Since an empty string reads the same forward and backward, it is a palindrome.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 2 * 10^5
> - s consists only of printable ASCII characters.

> [!info] Approach
> After filtering to alphanumeric + lowercase, a palindrome reads the same forwards and backwards. Two pointers moving inward compare characters without allocating a filtered string. Left pointer starts at 0, right pointer starts at end. Skip non-alphanumeric characters. Compare lowercase versions. While `l < r`: skip `l` while not alphanumeric, skip `r` while not alphanumeric. If `s[l].lower() != s[r].lower()`, return False. Advance both pointers inward.


> [!note]- Python Solution
> ```python
> def is_palindrome(s):
>     l, r = 0, len(s) - 1
>     while l < r:
>         while l < r and not s[l].isalnum():
>             l += 1
>         while l < r and not s[r].isalnum():
>             r -= 1
>         if s[l].lower() != s[r].lower():
>             return False
>         l += 1
>         r -= 1
>     return True
> ```

> [!success] Complexity
> Time O(n). Space O(1).

> [!tip] Alternatives
> - Filter then compare: `clean = [c.lower() for c in s if c.isalnum()]; return clean == clean[::-1]` — O(n) time, O(n) space, less elegant.
> - Regex filter: `re.sub(r'[^a-z0-9]', '', s.lower())` then compare to its reverse — same complexity, cleaner for production code.

---

### Longest Palindromic Substring `🔥 Google`

> [!example] Problem
> Given a string s, return the longest palindromic substring in s.
> 
> **Example 1:**
> ```
> Input: s = "babad"
> Output: "bab"
> Explanation: "aba" is also a valid answer.
> ```
> 
> **Example 2:**
> ```
> Input: s = "cbbd"
> Output: "bb"
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 1000
> - s consist of only digits and English letters.

> [!info] Approach
> A palindrome is symmetric around its center. Expanding outward from each possible center checks all palindromes in O(n²) without a 2D DP table. Expand-around-center. For each of the `2n - 1` possible centers (n odd-length centers at each character, n-1 even-length centers between adjacent characters), expand outward while characters match. `expand(l, r)` expands while `s[l] == s[r]` and indices are in bounds, returning the palindrome substring. For each index `i`, try both `expand(i, i)` (odd length) and `expand(i, i+1)` (even length). Track the longest result.


> [!note]- Python Solution
> ```python
> def longest_palindrome(s):
>     def expand(l, r):
>         while l >= 0 and r < len(s) and s[l] == s[r]:
>             l -= 1
>             r += 1
>         return s[l + 1:r]   # last valid range before mismatch
> 
>     best = ""
>     for i in range(len(s)):
>         for candidate in (expand(i, i), expand(i, i + 1)):
>             if len(candidate) > len(best):
>                 best = candidate
>     return best
> ```

> [!success] Complexity
> Time O(n²). Space O(1) ignoring the output string.

> [!tip] Alternatives
> - DP table `dp[i][j]`: `dp[i][j] = True` if `s[i..j]` is a palindrome. O(n²) time and space — same time but uses O(n²) memory vs O(1).
> - Manacher's algorithm: O(n) — insert `#` sentinels between chars, exploit palindrome symmetry to skip recomputation. Optimal but complex to implement in an interview.

---

### Palindromic Substrings (Count All Palindromic Substrings)

> [!example] Problem
> Given a string s, return the number of palindromic substrings in it.
> A string is a palindrome when it reads the same backward as forward.
> A substring is a contiguous sequence of characters within the string.
> 
> **Example 1:**
> ```
> Input: s = "abc"
> Output: 3
> Explanation: Three palindromic strings: "a", "b", "c".
> ```
> 
> **Example 2:**
> ```
> Input: s = "aaa"
> Output: 6
> Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 1000
> - s consists of lowercase English letters.

> [!info] Approach
> Same expand-around-center logic as Longest Palindromic Substring, but instead of tracking the longest, count every expansion that succeeds. For each center, count how many times we can expand — each successful expansion is one more palindromic substring. For each of the `2n - 1` centers, expand while `s[l] == s[r]`. Each valid `(l, r)` pair is one palindromic substring — increment count by 1 each step.


> [!note]- Python Solution
> ```python
> def count_substrings(s):
>     count = 0
> 
>     def expand(l, r):
>         nonlocal count
>         while l >= 0 and r < len(s) and s[l] == s[r]:
>             count += 1
>             l -= 1
>             r += 1
> 
>     for i in range(len(s)):
>         expand(i, i)       # odd length: center at i
>         expand(i, i + 1)   # even length: center between i and i+1
> 
>     return count
> ```

> [!success] Complexity
> Time O(n²). Space O(1).

> [!tip] Alternatives
> - DP table `dp[i][j]`: `dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]`. O(n²) time and space — count every `True` cell. Easier to understand but uses more memory.
> - Manacher's: O(n) — derive palindrome radii array, sum `ceil(radius[i] / 2)` for each center. Optimal, rarely needed in interviews.

---

## Sliding Window

### Longest Substring Without Repeating Characters `🔥 Google`

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
> A valid window has all unique characters. The window must shrink from the left when a duplicate enters — a variable-size sliding window maintains this invariant. Variable-size window with a set tracking current characters. Shrink left until the duplicate is gone. Track `max(right - left + 1)`. For each `right`: if `s[right]` is in the set, remove `s[left]` and advance `left` until the duplicate is gone. Then add `s[right]` and update max.


> [!note]- Python Solution
> ```python
> def length_of_longest_substring(s):
>     seen = set()
>     left = 0
>     best = 0
>     for right, ch in enumerate(s):
>         while ch in seen:
>             seen.remove(s[left])
>             left += 1
>         seen.add(ch)
>         best = max(best, right - left + 1)
>     return best
> ```

> [!success] Complexity
> Time O(n) — each character enters and exits the window at most once. Space O(min(n, |alphabet|)).

> [!tip] Alternatives
> - HashMap of last-seen index: `left = max(left, last_seen[ch] + 1)` — jumps left directly instead of stepping. O(n), better constant in practice but `left` must only move forward.
> - Array as hash map for ASCII: replace `set` with `int[128]` — same asymptotics, better constant factor.

---

### Minimum Window Substring `🔥 Google`

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
> We need the smallest window satisfying all character demands from `t`. Expanding right adds characters; once the window is valid, shrink left to minimize it. The `formed` counter makes validity check O(1). Variable-size sliding window with two frequency maps (`need` for t, `have` for current window) and a `formed` count of satisfied characters. Expand right: add `s[right]` to `have`; if `have[c] == need[c]`, increment `formed`. When `formed == len(need)` (window valid): record min window, shrink from left — decrement `have[s[left]]`; if it drops below `need[s[left]]`, decrement `formed`. Repeat shrinking until no longer valid.


> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def min_window(s, t):
>     if not t or not s:
>         return ""
>     need = Counter(t)
>     have = {}
>     formed = 0
>     required = len(need)
>     left = 0
>     best = (float('inf'), 0, 0)   # (length, left, right)
> 
>     for right, ch in enumerate(s):
>         have[ch] = have.get(ch, 0) + 1
>         if ch in need and have[ch] == need[ch]:
>             formed += 1
>         while formed == required:
>             if right - left + 1 < best[0]:
>                 best = (right - left + 1, left, right)
>             out = s[left]
>             have[out] -= 1
>             if out in need and have[out] < need[out]:
>                 formed -= 1
>             left += 1
> 
>     return s[best[1]:best[2] + 1] if best[0] != float('inf') else ""
> ```

> [!success] Complexity
> Time O(|s| + |t|). Space O(|s| + |t|).

> [!tip] Alternatives
> - Filtered `s` optimization: if `|t| << |s|`, filter `s` to only characters in `t` and their indices — reduces constant factor for large sparse inputs.
> - Brute force O(|s|²): for each left, find smallest valid right — baseline only.

---

### Longest Repeating Character Replacement `🔥 Google`

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
> A window is valid iff `window_length - max_frequency_in_window <= k`. Slide and never contract the window below its historical maximum — we only care about longer windows. Sliding window with a frequency map. `max_freq` tracks the frequency of the most common character seen so far (across all window positions — it is allowed to be slightly stale when shrinking because we only care about longer windows). Expand right: update `count[s[right]]` and `max_freq`. If `(window_size - max_freq) > k`, slide left by 1 — don't shrink, just slide. The window grows when a valid longer window is found.


> [!note]- Python Solution
> ```python
> def character_replacement(s, k):
>     count = {}
>     left = 0
>     max_freq = 0
>     for right, ch in enumerate(s):
>         count[ch] = count.get(ch, 0) + 1
>         max_freq = max(max_freq, count[ch])
>         # window_size = right - left + 1
>         if (right - left + 1) - max_freq > k:
>             count[s[left]] -= 1
>             left += 1
>     return len(s) - left   # final window size
> ```

> [!success] Complexity
> Time O(n). Space O(1) — at most 26 keys.

> [!tip] Alternatives
> - Per-character pass: for each of the 26 characters, find the longest window where that character is dominant with at most k others — O(26n). Easier to reason about correctness.
> - Binary search on window length: binary search on L, check if any window of size L is valid — O(n log n). Useful when the monotone property isn't immediately obvious.

---

## Prefix Sum on Characters

### Prefix Sum on Characters Pattern

> Count substrings satisfying a character-frequency constraint in O(n) using prefix sum + hash map — the exact same technique as numeric subarray sum problems. Map characters to numbers (e.g., vowel=1/non-vowel=0, or treat a binary string as 0/1). Build a running sum; use a hash map to count valid pairs. For "exactly k" problems use the at-most trick: `exactly(k) = atMost(k) - atMost(k-1)`. `prefix_count = {0: 1}; running = 0`. For each element: `running += value(element)`. `answer += prefix_count.get(running - target, 0)`. `prefix_count[running] += 1`.


---

### Number of Substrings Containing All Three Characters

> [!example] Problem
> Given a string s consisting only of characters a, b and c.
> Return the number of substrings containing at least one occurrence of all these characters a, b and c.
> 
> **Example 1:**
> ```
> Input: s = "abcabc"
> Output: 10
> Explanation: The substrings containing at least one occurrence of the characters a, b and c are "abc", "abca", "abcab", "abcabc", "bca", "bcab", "bcabc", "cab", "cabc" and "abc" (again).
> ```
> 
> **Example 2:**
> ```
> Input: s = "aaacb"
> Output: 3
> Explanation: The substrings containing at least one occurrence of the characters a, b and c are "aaacb", "aacb" and "acb".
> ```
> 
> **Example 3:**
> ```
> Input: s = "abc"
> Output: 1
> ```
> 
> **Constraints:**
> - 3 <= s.length <= 5 x 10^4
> - s only consists of a, b or c characters.

> [!info] Approach
> For any right endpoint `r`, the valid left endpoints form a contiguous suffix — as soon as all three chars appear, every further-left start also works. Track the rightmost position where each character was last seen. Single pass tracking `last[a]`, `last[b]`, `last[c]` (most recent index of each). At each `r`, the number of valid starting points ending at `r` is `min(last_a, last_b, last_c) + 1` (all positions from 0 to that minimum). Maintain `last = [-1, -1, -1]` for a/b/c. For each `r`, update `last[ord(s[r]) - ord('a')] = r`. Add `min(last) + 1` to answer (clamped to 0 when any char unseen).


> [!note]- Python Solution
> ```python
> def number_of_substrings(s):
>     last = [-1, -1, -1]
>     count = 0
>     for r, ch in enumerate(s):
>         last[ord(ch) - ord('a')] = r
>         count += min(last) + 1   # -1 if any char unseen → contributes 0
>     return count
> >
> # Alternative: prefix count approach
> def number_of_substrings_prefix(s):
>     from collections import Counter
>     count = 0
>     left = 0
>     freq: Counter = Counter()
>     for right, ch in enumerate(s):
>         freq[ch] += 1
>         while len(freq) == 3:
>             count += len(s) - right
>             freq[s[left]] -= 1
>             if freq[s[left]] == 0:
>                 del freq[s[left]]
>             left += 1
>     return count
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Sliding window (shrink-and-count): count all subarrays where window contains all 3 — same O(n), slightly more code.
> - Brute force O(n²): for each (l, r), check if all 3 present using frequency map.

---

### Count Vowel Substrings of a Word

> [!example] Problem
> Count substrings that contain only vowels (`a, e, i, o, u`) and include every vowel at least once.

> [!info] Approach
> Direct sliding window with "exactly 5 distinct vowels" is non-monotone. Use the at-most trick: `exactly(5) = atMost(5) - atMost(4)`. `atMost(k)` counts substrings made of vowels only, with at most k distinct vowels. For each right pointer, advance left until only-vowels and ≤ k distinct. Add `r - l + 1`. `atMost(k)`: `l = 0, freq = {}`. For each `r`: if `s[r]` not a vowel, reset window (`l = r+1, freq = {}`). Else update `freq[s[r]]`. While `len(freq) > k`, shrink `l`. Add `r - l + 1`. Answer = `atMost(5) - atMost(4)`.


> [!note]- Python Solution
> ```python
> def count_vowel_substrings(word):
>     VOWELS = set('aeiou')
> >
>     def at_most(k):
>         freq = {}
>         l = result = 0
>         for r, ch in enumerate(word):
>             if ch not in VOWELS:
>                 freq.clear()
>                 l = r + 1
>                 continue
>             freq[ch] = freq.get(ch, 0) + 1
>             while len(freq) > k:
>                 left_ch = word[l]
>                 freq[left_ch] -= 1
>                 if freq[left_ch] == 0:
>                     del freq[left_ch]
>                 l += 1
>             result += r - l + 1
>         return result
> >
>     return at_most(5) - at_most(4)
> ```

> [!success] Complexity
> Time O(n), Space O(1) (at most 5 keys).

> [!tip] Alternatives
> - Brute force O(n²): for each (l, r), check both conditions. Fine for small inputs.
> - Bitmask DP: track which vowels seen in a 5-bit mask. O(n × 32) — same asymptotic, different constant.

---

### Binary Subarrays With Sum

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
> Binary array can have negative-like complications if solved with sliding window (zero elements don't shrink the sum). Prefix sum + hash map handles it cleanly. Alternatively, at-most trick works since elements are non-negative. Prefix sum approach: `prefix_count[0] = 1`. Running sum; `answer += prefix_count[running - goal]`. `seen = {0: 1}, running = count = 0`. For each `x`: `running += x`, `count += seen.get(running - goal, 0)`, `seen[running] = seen.get(running, 0) + 1`.


> [!note]- Python Solution
> ```python
> def num_subarrays_with_sum(nums, goal):
>     from collections import defaultdict
>     prefix_count = defaultdict(int)
>     prefix_count[0] = 1
>     running = count = 0
>     for x in nums:
>         running += x
>         count += prefix_count[running - goal]
>         prefix_count[running] += 1
>     return count
> >
> # At-most sliding window variant
> def num_subarrays_with_sum_window(nums, goal):
>     def at_most(k):
>         if k < 0:
>             return 0
>         l = result = running = 0
>         for r, x in enumerate(nums):
>             running += x
>             while running > k:
>                 running -= nums[l]
>                 l += 1
>             result += r - l + 1
>         return result
>     return at_most(goal) - at_most(goal - 1)
> ```

> [!success] Complexity
> Time O(n), Space O(n) for prefix map / O(1) for sliding window.

> [!tip] Alternatives
> - Sliding window at-most trick: `exactly(k) = atMost(k) - atMost(k-1)`. O(n) time, O(1) space. Works because elements are non-negative.
> - Brute force O(n²): prefix sum array + nested loop over all (l, r) pairs.

---

### Subarray Sum Equals K (character version) `🔥 Google`

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
> Map target character to 1, all others to 0 — identical to the numeric subarray sum equals k problem. Standard prefix sum + hash map. `prefix_count[0] = 1`. Running sum of mapped values; `answer += prefix_count[running - k]`. For each character `ch`: `running += (1 if ch == target else 0)`. `count += prefix_count[running - k]`. `prefix_count[running] += 1`.


> [!note]- Python Solution
> ```python
> def count_substrings_with_k_chars(s, target, k):
>     from collections import defaultdict
>     prefix_count = defaultdict(int)
>     prefix_count[0] = 1
>     running = count = 0
>     for ch in s:
>         running += 1 if ch == target else 0
>         count += prefix_count[running - k]
>         prefix_count[running] += 1
>     return count
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - At-most sliding window: `exactly(k) = atMost(k) - atMost(k-1)`. O(n) time, O(1) space — preferred when memory is constrained.

---

## Encoding / Hashing

### Encode and Decode Strings `🔥 Google`

> [!example] Problem
> Design an algorithm to encode **a list of strings** to **a string**. The encoded string is then sent over the network and is decoded back to the original list of strings.
> 
> Machine 1 (sender) has the function:
> 
> ```
> 
> string encode(vector<string> strs) {
>   // ... your code
>   return encoded_string;
> }
> ```
> 
> Machine 2 (receiver) has the function:
> 
> ```
> 
> vector<string> decode(string s) {
>   //... your code
>   return strs;
> }
> 
> ```
> 
> So Machine 1 does:
> 
> ```
> 
> string encoded_string = encode(strs);
> 
> ```
> 
> and Machine 2 does:
> 
> ```
> 
> vector<string> strs2 = decode(encoded_string);
> 
> ```
> 
> `strs2` in Machine 2 should be the same as `strs` in Machine 1.
> 
> Implement the `encode` and `decode` methods.
> 
> You are not allowed to solve the problem using any serialize methods (such as `eval`).
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** dummy_input = ["Hello","World"]
> **Output:** ["Hello","World"]
> **Explanation:**
> Machine 1:
> Codec encoder = new Codec();
> String msg = encoder.encode(strs);
> Machine 1 ---msg---> Machine 2
> 
> Machine 2:
> Codec decoder = new Codec();
> String[] strs = decoder.decode(msg);
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** dummy_input = [""]
> **Output:** [""]
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= strs.length <= 200`
> 	
> - `0 <= strs[i].length <= 200`
> 	
> - `strs[i]` contains any possible characters out of `256` valid ASCII characters.
> 
>  
> 
> **Follow up: **Could you write a generalized algorithm to work on any possible set of characters?

> [!info] Approach
> Simple delimiters (`,`, `#`) fail if the strings contain those characters. A length-prefix scheme is delimiter-free and unambiguous. Encode each string as `{length}#{string}`. The `#` here marks the end of the length field, not a content separator — the length tells us exactly how many bytes to read. Encode: for each string, emit `str(len(s)) + '#' + s`. Decode: read digits up to `#` to get length L; read exactly L characters as the next string; advance pointer past them; repeat.


> [!note]- Python Solution
> ```python
> def encode(strs):
>     return "".join(f"{len(s)}#{s}" for s in strs)
> 
> def decode(s):
>     result = []
>     i = 0
>     while i < len(s):
>         j = s.index('#', i)
>         length = int(s[i:j])
>         result.append(s[j + 1: j + 1 + length])
>         i = j + 1 + length
>     return result
> ```

> [!success] Complexity
> Time O(total characters) for both encode and decode. Space O(total characters).

> [!tip] Alternatives
> - Escape-character scheme: prefix special chars with `\` — O(n) but encoding complexity grows with character set.
> - Fixed-width length field (e.g., always 4 bytes big-endian): avoids the `#` separator entirely — used in binary protocols like protobuf.

---

### String Hashing (Duplicate Substring Detection)

> [!example] Problem
> Given string `s` and integer `length`, determine if any substring of that length appears more than once. (Foundation for "Longest Duplicate Substring" via binary search.)

> [!info] Approach
> Comparing every pair of substrings of length L is O(n × L) per comparison and O(n²L) total. A rolling hash computes each substring's hash in O(1) after O(n) preprocessing. Polynomial rolling hash: `hash(s[i..i+L-1]) = s[i] * base^(L-1) + s[i+1] * base^(L-2) + ... + s[i+L-1]`. Slide by subtracting the leftmost character's contribution and adding the rightmost — O(1) per step. Compute `hash(s[0..L-1])`. For each subsequent position, update the hash by the sliding formula. Store hashes in a set. On collision, verify with string comparison to rule out false positives.


> [!note]- Python Solution
> ```python
> def has_duplicate_of_length(s, L):
>     if L == 0:
>         return True
>     BASE, MOD = 31, (1 << 61) - 1   # Mersenne prime for low collision rate
>     # Use Python's set of substrings for simplicity (avoids collision handling)
>     seen = set()
>     for i in range(len(s) - L + 1):
>         sub = s[i:i + L]
>         if sub in seen:
>             return True
>         seen.add(sub)
>     return False
> 
> # Rolling hash variant — O(n) without substring creation
> def has_duplicate_of_length_fast(s, L):
>     """Returns start index of first duplicate or None."""
>     BASE, MOD = 26, (1 << 61) - 1
>     h = 0
>     for c in s[:L]:
>         h = (h * BASE + ord(c)) % MOD
>     power = pow(BASE, L, MOD)
>     seen = {h: 0}
>     for i in range(1, len(s) - L + 1):
>         h = (h * BASE - ord(s[i - 1]) * power + ord(s[i + L - 1])) % MOD
>         if h in seen:
>             # verify to handle collisions
>             j = seen[h]
>             if s[j:j + L] == s[i:i + L]:
>                 return i
>         seen[h] = i
>     return None
> ```

> [!success] Complexity
> Time O(n) per length check (amortized). Space O(n).

> [!tip] Alternatives
> - Suffix array + LCP array: O(n log n) build, O(1) per query — optimal for many length queries but complex to implement.
> - Naive O(n²): store all substrings in a set — O(nL) per insertion due to string hashing; total O(n²L). Simpler, acceptable for small inputs.

---

## Parsing / Simulation

### String to Integer (atoi)

> [!example] Problem
> Implement the myAtoi(string s) function, which converts a string to a 32-bit signed integer.
> The algorithm for myAtoi(string s) is as follows:
> Return the integer as the final result.
> 
> **Example 1:**
> ```
> The underlined characters are what is read in and the caret is the current reader position.
> Step 1: "42" (no characters read because there is no leading whitespace)
>          ^
> Step 2: "42" (no characters read because there is neither a '-' nor '+')
>          ^
> Step 3: "42" ("42" is read in)
>            ^
> ```
> 
> **Example 2:**
> ```
> Step 1: "   -042" (leading whitespace is read and ignored)
>             ^
> Step 2: "   -042" ('-' is read, so the result should be negative)
>              ^
> Step 3: "   -042" ("042" is read in, leading zeros ignored in the result)
>                ^
> ```
> 
> **Example 3:**
> ```
> Step 1: "1337c0d3" (no characters read because there is no leading whitespace)
>          ^
> Step 2: "1337c0d3" (no characters read because there is neither a '-' nor '+')
>          ^
> Step 3: "1337c0d3" ("1337" is read in; reading stops because the next character is a non-digit)
>              ^
> ```
> 
> **Example 4:**
> ```
> Step 1: "0-1" (no characters read because there is no leading whitespace)
>          ^
> Step 2: "0-1" (no characters read because there is neither a '-' nor '+')
>          ^
> Step 3: "0-1" ("0" is read in; reading stops because the next character is a non-digit)
>           ^
> ```
> 
> **Constraints:**
> - 0 <= s.length <= 200
> - s consists of English letters (lower-case and upper-case), digits (0-9), ' ', '+', '-', and '.'.

> [!info] Approach
> This is a state-machine / parsing problem. The transformation rules are explicit — model each parsing phase as a step. Sequential parsing: (1) strip leading whitespace, (2) read optional sign, (3) accumulate digits, (4) stop at first non-digit, (5) clamp to 32-bit range. Advance `i` past spaces. Read sign. Accumulate `result = result * 10 + digit` for each digit character. Before adding, check for overflow: if `result > (INT_MAX - digit) // 10`, clamp and return. Return `sign * result`.


> [!note]- Python Solution
> ```python
> def my_atoi(s):
>     INT_MAX = 2**31 - 1
>     INT_MIN = -(2**31)
>     i, n = 0, len(s)
> 
>     # 1. strip leading whitespace
>     while i < n and s[i] == ' ':
>         i += 1
> 
>     # 2. read optional sign
>     sign = 1
>     if i < n and s[i] in ('+', '-'):
>         sign = -1 if s[i] == '-' else 1
>         i += 1
> 
>     # 3. accumulate digits
>     result = 0
>     while i < n and s[i].isdigit():
>         digit = int(s[i])
>         # overflow check before multiplying
>         if result > (INT_MAX - digit) // 10:
>             return INT_MAX if sign == 1 else INT_MIN
>         result = result * 10 + digit
>         i += 1
> 
>     return sign * result
> ```

> [!success] Complexity
> Time O(n). Space O(1).

> [!tip] Alternatives
> - Regex: `re.match(r'^\s*([+-]?\d+)', s)` — one line, but doesn't teach the parsing logic. Overflow must still be handled manually.
> - `int()` with try/except: `int(s.strip())` — works for valid inputs only, not for atoi's partial-parse semantics.

---

### Longest Common Prefix

> [!example] Problem
> Write a function to find the longest common prefix string amongst an array of strings.
> If there is no common prefix, return an empty string "".
> 
> **Example 1:**
> ```
> Input: strs = ["flower","flow","flight"]
> Output: "fl"
> ```
> 
> **Example 2:**
> ```
> Input: strs = ["dog","racecar","car"]
> Output: ""
> Explanation: There is no common prefix among the input strings.
> ```
> 
> **Constraints:**
> - 1 <= strs.length <= 200
> - 0 <= strs[i].length <= 200
> - strs[i] consists of only lowercase English letters if it is non-empty.

> [!info] Approach
> The longest common prefix is bounded by the shortest string. Compare column by column: the prefix ends at the first position where any string differs. Vertical scanning — for each character position `i`, check if all strings have the same character at `i`. Stop at the first mismatch or when any string ends. Take `strs[0]` as the reference. For each character index `i` in `strs[0]`, check every other string at position `i`. If any string is shorter than `i` or differs at `i`, return `strs[0][:i]`.


> [!note]- Python Solution
> ```python
> def longest_common_prefix(strs):
>     if not strs:
>         return ""
>     for i, char in enumerate(strs[0]):
>         for s in strs[1:]:
>             if i == len(s) or s[i] != char:
>                 return strs[0][:i]
>     return strs[0]
> 
> # Alternative: binary search on prefix length
> def longest_common_prefix_binary_search(strs):
>     def all_match(length):
>         prefix = strs[0][:length]
>         return all(s[:length] == prefix for s in strs[1:])
> 
>     lo, hi = 0, min(len(s) for s in strs)
>     while lo < hi:
>         mid = (lo + hi + 1) // 2
>         if allMatch(mid):
>             lo = mid
>         else:
>             hi = mid - 1
>     return strs[0][:lo]
> ```

> [!success] Complexity
> Time O(S) where S = total characters across all strings (vertical scan terminates early). Space O(1).

> [!tip] Alternatives
> - Sort and compare first/last: `strs.sort()` then compare `strs[0]` and `strs[-1]` character by character — O(N log N + L). Sorting is overkill for the problem.
> - Binary search on prefix length: O(S log L) — useful when L is very long and most strings share a long common prefix.
> - Trie: O(S) build, O(1) LCP query if queried many times — overkill for a one-time query.

---

## Two Pointers — Reverse / Subsequence

### Reverse String

> [!example] Problem
> Write a function that reverses a string. The input string is given as an array of characters s.
> You must do this by modifying the input array in-place with O(1) extra memory.
> 
> **Example 1:**
> ```
> Input: s = ["h","e","l","l","o"]
> Output: ["o","l","l","e","h"]
> ```
> 
> **Example 2:**
> ```
> Input: s = ["H","a","n","n","a","h"]
> Output: ["h","a","n","n","a","H"]
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s[i] is a printable ascii character.

> [!info] Approach
> Classic two-pointer swap. No extra allocation needed. Left pointer at 0, right pointer at end. Swap and advance inward until they meet. `while l < r: s[l], s[r] = s[r], s[l]; l += 1; r -= 1`.


> [!note]- Python Solution
> ```python
> def reverse_string(s):
>     l, r = 0, len(s) - 1
>     while l < r:
>         s[l], s[r] = s[r], s[l]
>         l += 1
>         r -= 1
> ```

> [!success] Complexity
> Time O(n). Space O(1).

> [!tip] Alternatives
> - `s.reverse()` or `s[:] = s[::-1]` — one-liner but allocates O(n) for slice.
> - XOR swap: `s[l] ^= s[r]; s[r] ^= s[l]; s[l] ^= s[r]` — avoids temp variable, but only works for integers/bytes, not characters.

---

### Is Subsequence

> [!example] Problem
> Given two strings s and t, return true if s is a subsequence of t, or false otherwise.
> A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (i.e., "ace" is a subsequence of "abcde" while "aec" is not).
> 
> **Example 1:**
> ```
> Input: s = "abc", t = "ahbgdc"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: s = "axc", t = "ahbgdc"
> Output: false
> ```
> 
> **Constraints:**
> - 0 <= s.length <= 100
> - 0 <= t.length <= 10^4
> - s and t consist only of lowercase English letters.

> [!info] Approach
> Greedy two-pointer: advance through `t` trying to match characters of `s` in order. As soon as all of `s` is matched, return True. Pointer `i` for `s`, pointer `j` for `t`. Advance `j` always; advance `i` only when `s[i] == t[j]`. Return `i == len(s)`. Single pass through `t`. If `i` reaches `len(s)`, all characters matched — return True.


> [!note]- Python Solution
> ```python
> def is_subsequence(s, t):
>     i = 0
>     for ch in t:
>         if i < len(s) and ch == s[i]:
>             i += 1
>     return i == len(s)
> 
> # Follow-up: many queries with same t — preprocess t with binary search
> from collections import defaultdict
> import bisect
> 
> def is_subsequence_batch(s, t_index, list[int]]):
>     """t_index: char -> sorted list of positions in t."""
>     pos = 0
>     for ch in s:
>         if ch not in t_index:
>             return False
>         idx = bisect.bisect_left(t_index[ch], pos)
>         if idx == len(t_index[ch]):
>             return False
>         pos = t_index[ch][idx] + 1
>     return True
> ```

> [!success] Complexity
> Time O(|t|) single query. O(|t|) preprocessing + O(|s| log |t|) per query for batch variant. Space O(1) / O(|t|).

> [!tip] Alternatives
> - Recursive with memoization: overkill for O(n) problem.
> - DP table `dp[i][j]`: `dp[i][j] = True` if `s[:i]` is subseq of `t[:j]` — O(|s| × |t|) space, unnecessary.

---

## Parsing / Simulation (Extended)

### Decode String `⭐ Google`

> [!example] Problem
> Given an encoded string, return its decoded string.
> The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly k times. Note that k is guaranteed to be a positive integer.
> You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc. Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, k. For example, there will not be input like 3a or 2[4].
> The test cases are generated so that the length of the output will never exceed 105.
> 
> **Example 1:**
> ```
> Input: s = "3[a]2[bc]"
> Output: "aaabcbc"
> ```
> 
> **Example 2:**
> ```
> Input: s = "3[a2[c]]"
> Output: "accaccacc"
> ```
> 
> **Example 3:**
> ```
> Input: s = "2[abc]3[cd]ef"
> Output: "abcabccdcdcdef"
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 30
> - s consists of lowercase English letters, digits, and square brackets '[]'.
> - s is guaranteed to be a valid input.
> - All the integers in s are in the range [1, 300].

> [!info] Approach
> Nested brackets suggest a stack. When we hit `]`, we pop until `[` to find the current segment and its repeat count. Stack-based. Push characters as we scan. On `]`: pop characters until `[` to build the inner string, then pop digits to build the multiplier, push the repeated string back. Two stacks (`count_stack`, `string_stack`) or a single character stack. On digit: accumulate `k`. On `[`: push current string and k onto stacks, reset. On `]`: pop string and k, append `k * current_string` to the popped prefix.


> [!note]- Python Solution
> ```python
> def decode_string(s):
>     count_stack = []
>     string_stack = []
>     current = ""
>     k = 0
>     for ch in s:
>         if ch.isdigit():
>             k = k * 10 + int(ch)
>         elif ch == '[':
>             count_stack.append(k)
>             string_stack.append(current)
>             current = ""
>             k = 0
>         elif ch == ']':
>             repeat = count_stack.pop()
>             prefix = string_stack.pop()
>             current = prefix + repeat * current
>         else:
>             current += ch
>     return current
> ```

> [!success] Complexity
> Time O(output length) — each character of the decoded string is written once. Space O(depth × max_segment_length).

> [!tip] Alternatives
> - Recursive descent parser: function returns decoded string and next index — elegant, same complexity.
> - Regex iterative substitution: replace innermost `k[...]` repeatedly with `re.sub` — O(output × depth), slow for deep nesting.

---

### Compare Version Numbers

> [!example] Problem
> Given two version strings, version1 and version2, compare them. A version string consists of revisions separated by dots '.'. The value of the revision is its integer conversion ignoring leading zeros.
> To compare version strings, compare their revision values in left-to-right order. If one of the version strings has fewer revisions, treat the missing revision values as 0.
> Return the following
> 
> **Example 1:**
> ```
> Input: version1 = "1.2", version2 = "1.10"
> Output: -1
> Explanation:
> version1's second revision is "2" and version2's second revision is "10": 2 < 10, so version1 < version2.
> ```
> 
> **Example 2:**
> ```
> Input: version1 = "1.01", version2 = "1.001"
> Output: 0
> Explanation:
> Ignoring leading zeroes, both "01" and "001" represent the same integer "1".
> ```
> 
> **Example 3:**
> ```
> Input: version1 = "1.0", version2 = "1.0.0.0"
> Output: 0
> Explanation:
> version1 has less revisions, which means every missing revision are treated as "0".
> ```
> 
> **Constraints:**
> - 1 <= version1.length, version2.length <= 500
> - version1 and version2 only contain digits and '.'.
> - version1 and version2 are valid version numbers.
> - All the given revisions in version1 and version2 can be stored in a 32-bit integer.

> [!info] Approach
> Split on `.` gives revision tokens. Parse each as an integer (handles leading zeros automatically). Compare pair by pair; missing revisions default to 0. Split both strings by `.`. Zip-extend to equal length with 0 padding. Compare integer values of corresponding revisions. `v1 = list(map(int, version1.split('.')))`. Pad shorter list with zeros. Compare element by element.


> [!note]- Python Solution
> ```python
> def compare_version(version1, version2):
>     v1 = list(map(int, version1.split('.')))
>     v2 = list(map(int, version2.split('.')))
>     # pad shorter version with zeros
>     length = max(len(v1), len(v2))
>     v1 += [0] * (length - len(v1))
>     v2 += [0] * (length - len(v2))
>     for a, b in zip(v1, v2):
>         if a < b:
>             return -1
>         if a > b:
>             return 1
>     return 0
> ```

> [!success] Complexity
> Time O(max(|v1|, |v2|)). Space O(max(|v1|, |v2|)).

> [!tip] Alternatives
> - Two-pointer without splitting: parse digits between dots manually — O(1) extra space, more code.
> - `zip_longest` from itertools: cleaner padding — `from itertools import zip_longest; for a, b in zip_longest(v1, v2, fillvalue=0)`.

---

### Integer to English Words

> [!example] Problem
> Convert a non-negative integer num to its English words representation.
> 
> **Example 1:**
> ```
> Input: num = 123
> Output: "One Hundred Twenty Three"
> ```
> 
> **Example 2:**
> ```
> Input: num = 12345
> Output: "Twelve Thousand Three Hundred Forty Five"
> ```
> 
> **Example 3:**
> ```
> Input: num = 1234567
> Output: "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
> ```
> 
> **Constraints:**
> - 0 <= num <= 2^{31} - 1

> [!info] Approach
> Numbers follow a recursive pattern: every 3-digit group is described the same way, then suffixed with Billion/Million/Thousand. Handle the hundreds/tens/ones within each group using lookup tables. Define lookup tables for ones (1-19) and tens (20, 30, …, 90). `helper(n)` converts a number < 1000 to words. Iterate over billion/million/thousand groups. Process groups of 3 digits from largest to smallest. For each non-zero group, call `helper(group)` and append the appropriate suffix. Special-case 0.


> [!note]- Python Solution
> ```python
> def number_to_words(num):
>     if num == 0:
>         return "Zero"
> 
>     ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
>             "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
>             "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
>     tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty",
>             "Sixty", "Seventy", "Eighty", "Ninety"]
> 
>     def helper(n):
>         if n == 0:
>             return ""
>         elif n < 20:
>             return ones[n] + " "
>         elif n < 100:
>             return tens[n // 10] + " " + helper(n % 10)
>         else:
>             return ones[n // 100] + " Hundred " + helper(n % 100)
> 
>     suffixes = [(10**9, "Billion"), (10**6, "Million"), (10**3, "Thousand"), (1, "")]
>     result = ""
>     for value, suffix in suffixes:
>         if num >= value:
>             result += helper(num // value)
>             if suffix:
>                 result += suffix + " "
>             num %= value
>     return result.strip()
> ```

> [!success] Complexity
> Time O(log n) — at most ~10 groups of 3 digits. Space O(1) ignoring output.

> [!tip] Alternatives
> - Iterative with a stack: push word segments onto a stack, pop to assemble — same complexity, different code structure.
> - Library: `num2words` in Python — correct but not allowed in interviews.

---

## Pattern Matching

### Implement strStr (KMP)

> [!example] Problem
> Return the index of the first occurrence of `needle` in `haystack`. Return -1 if not present. (LC 28 — implement using KMP for O(n+m) worst case.)

> [!info] Approach
> Naive search is O(n×m) in the worst case (e.g., `haystack = "aaa…a"`, `needle = "aaa…ab"`). KMP preprocesses `needle` to build a failure function (also called LPS — Longest Proper Prefix which is also Suffix), enabling O(n+m) matching by never re-examining a haystack character. Build LPS array `lps[i]` = length of longest proper prefix of `needle[0..i]` that is also a suffix. During search, on mismatch at position `j`, jump `j = lps[j-1]` instead of resetting to 0. Build LPS: two pointers `len_ = 0, i = 1`. If `needle[i] == needle[len_]`, `lps[i] = len_ + 1; i++; len_++`. Else if `len_ > 0`, `len_ = lps[len_-1]`. Else `lps[i] = 0; i++`. Search: advance `i` (haystack), `j` (needle); on mismatch use `j = lps[j-1]`; when `j == len(needle)` record match.


> [!note]- Python Solution
> ```python
> def str_str(haystack, needle):
>     if not needle:
>         return 0
>     n, m = len(haystack), len(needle)
> 
>     # build LPS (failure function)
>     lps = [0] * m
>     len_ = 0
>     i = 1
>     while i < m:
>         if needle[i] == needle[len_]:
>             len_ += 1
>             lps[i] = len_
>             i += 1
>         elif len_ > 0:
>             len_ = lps[len_ - 1]
>         else:
>             lps[i] = 0
>             i += 1
> 
>     # KMP search
>     i = j = 0
>     while i < n:
>         if haystack[i] == needle[j]:
>             i += 1
>             j += 1
>         if j == m:
>             return i - j
>         elif i < n and haystack[i] != needle[j]:
>             if j > 0:
>                 j = lps[j - 1]
>             else:
>                 i += 1
>     return -1
> ```

> [!success] Complexity
> Time O(n + m). Space O(m) for the LPS array.

> [!tip] Alternatives
> - Naive: `for i in range(n-m+1): if haystack[i:i+m] == needle: return i` — O(nm) worst case, fine for interviews unless pushed.
> - Rabin-Karp rolling hash: O(n+m) average, O(nm) worst case without double hashing.
> - Boyer-Moore: better practical performance (sub-linear on average) via bad-character and good-suffix heuristics.
> - Python built-in: `haystack.find(needle)` — uses optimized C; not the point of this problem.

---

### Repeated Substring Pattern `⭐ Google`

> [!example] Problem
> Given a string s, check if it can be constructed by taking a substring of it and appending multiple copies of the substring together.
> 
> **Example 1:**
> ```
> Input: s = "abab"
> Output: true
> Explanation: It is the substring "ab" twice.
> ```
> 
> **Example 2:**
> ```
> Input: s = "aba"
> Output: false
> ```
> 
> **Example 3:**
> ```
> Input: s = "abcabcabcabc"
> Output: true
> Explanation: It is the substring "abc" four times or the substring "abcabc" twice.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^4
> - s consists of lowercase English letters.

> [!info] Approach
> If `s` is a repetition of some pattern `p`, then `s + s` contains `s` starting at a position other than 0 or `len(s)`. This is because the doubled string `ss` can align `p` blocks to reconstruct `s` shifted by one period. Concatenate `s` with itself, check if `s` appears in `s[1:-1]` (exclude the trivial positions at index 0 and `len(s)`). `return s in (s + s)[1:-1]`. Alternatively, use KMP: build LPS array for `s`; if `lps[-1] > 0` and `len(s) % (len(s) - lps[-1]) == 0`, the pattern length is `len(s) - lps[-1]`.


> [!note]- Python Solution
> ```python
> def repeated_substring_pattern(s):
>     # O(n) via rotation trick
>     return s in (s + s)[1:-1]
> 
> # KMP LPS approach — O(n) time, O(n) space
> def repeated_substring_pattern_kmp(s):
>     if not s:
>         return False
>     n = len(s)
>     lps = [0] * n
>     j = 0
>     for i in range(1, n):
>         while j > 0 and s[i] != s[j]:
>             j = lps[j - 1]
>         if s[i] == s[j]:
>             j += 1
>         lps[i] = j
>     period = n - lps[-1]
>     return lps[-1] > 0 and n % period == 0
> ```

> [!success] Complexity
> Time O(n) — the rotation trick relies on optimized substring search. Space O(n).

> [!tip] Alternatives
> - Brute force: try every divisor length of `n`, check if repeating the prefix reconstructs `s` — O(n × d(n)) where d(n) is the number of divisors.

---

### Longest Happy Prefix `⭐ Google`

> [!example] Problem
> A string is called a happy prefix if is a non-empty prefix which is also a suffix (excluding itself).
> Given a string s, return the longest happy prefix of s. Return an empty string "" if no such prefix exists.
> 
> **Example 1:**
> ```
> Input: s = "level"
> Output: "l"
> Explanation: s contains 4 prefix excluding itself ("l", "le", "lev", "leve"), and suffix ("l", "el", "vel", "evel"). The largest prefix which is also suffix is given by "l".
> ```
> 
> **Example 2:**
> ```
> Input: s = "ababab"
> Output: "abab"
> Explanation: "abab" is the largest prefix which is also suffix. They can overlap in the original string.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s contains only lowercase English letters.

> [!info] Approach
> This is exactly the KMP failure function / LPS (Longest Proper Prefix which is also Suffix) for the entire string. The last value in the LPS array gives the length of the longest happy prefix. Build the KMP LPS array for `s`. `lps[-1]` is the answer length. Standard LPS build (same as in Implement strStr). Return `s[:lps[-1]]`.


> [!note]- Python Solution
> ```python
> def longest_prefix(s):
>     if not s:
>         return ""
>     n = len(s)
>     lps = [0] * n
>     j = 0
>     for i in range(1, n):
>         while j > 0 and s[i] != s[j]:
>             j = lps[j - 1]
>         if s[i] == s[j]:
>             j += 1
>         lps[i] = j
>     return s[:lps[-1]]
> ```

> [!success] Complexity
> Time O(n). Space O(n) for LPS array.

> [!tip] Alternatives
> - Rolling hash: compute prefix hashes and suffix hashes, find longest matching — O(n) average but requires collision handling.
> - Z-function: `z[i]` = length of longest substring starting at `i` that matches a prefix of `s`. The answer is `max(z[i] for i if i + z[i] == n)`. O(n) — equivalent power to KMP.

---

## String Manipulation

### String Compression

> [!example] Problem
> Given an array of characters chars, compress it using the following algorithm:
> Begin with an empty string s. For each group of consecutive repeating characters in chars:
> The compressed string s should not be returned separately, but instead, be stored in the input character array chars. Note that group lengths that are 10 or longer will be split into multiple characters in chars.
> After you are done modifying the input array, return the new length of the array.
> You must write an algorithm that uses only constant extra space.
> 
> **Example 1:**
> ```
> Input: chars = ["a","a","b","b","c","c","c"]
> Output: Return 6, and the first 6 characters of the input array should be: ["a","2","b","2","c","3"]
> Explanation: The groups are "aa", "bb", and "ccc". This compresses to "a2b2c3".
> ```
> 
> **Example 2:**
> ```
> Input: chars = ["a"]
> Output: Return 1, and the first character of the input array should be: ["a"]
> Explanation: The only group is "a", which remains uncompressed since it's a single character.
> ```
> 
> **Example 3:**
> ```
> Input: chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
> Output: Return 4, and the first 4 characters of the input array should be: ["a","b","1","2"].
> Explanation: The groups are "a" and "bbbbbbbbbbbb". This compresses to "ab12".
> ```
> 
> **Constraints:**
> - 1 <= chars.length <= 2000
> - chars[i] is a lowercase English letter, uppercase English letter, digit, or symbol.

> [!info] Approach
> We need to write compressed output back into the same array, so one pointer reads runs and another pointer writes results. Scan each run of identical characters, write the character once, then write the count digits if the run length is greater than one. Maintain `read` and `write` pointers. For each run, count length and emit the character plus its decimal digits.


> [!note]- Python Solution
> ```python
> def compress(chars):
>     write = 0
>     read = 0
>     while read < len(chars):
>         ch = chars[read]
>         start = read
>         while read < len(chars) and chars[read] == ch:
>             read += 1
>         chars[write] = ch
>         write += 1
>         count = read - start
>         if count > 1:
>             for digit in str(count):
>                 chars[write] = digit
>                 write += 1
>     return write
> ```

> [!success] Complexity
> O(n) time, O(1) extra space.

> [!tip] Alternatives
> This same read/write pointer idea is useful for deduplication, filtering, and in-place run-length encoding.

---

### Zigzag Conversion (LC 6) `⭐ Google`

> [!example] Problem
> The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)
> And then read line by line: "PAHNAPLSIIGYIR"
> Write the code that will take a string and make this conversion given a number of rows
> 
> **Example 1:**
> ```
> P   A   H   N
> A P L S I I G
> Y   I   R
> ```
> 
> **Example 2:**
> ```
> string convert(string s, int numRows);
> ```
> 
> **Example 3:**
> ```
> Input: s = "PAYPALISHIRING", numRows = 3
> Output: "PAHNAPLSIIGYIR"
> ```
> 
> **Example 4:**
> ```
> Input: s = "PAYPALISHIRING", numRows = 4
> Output: "PINALSIGYAHRPI"
> Explanation:
> P     I    N
> A   L S  I G
> Y A   H R
> P     I
> ```
> 
> **Example 5:**
> ```
> Input: s = "A", numRows = 1
> Output: "A"
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 1000
> - s consists of English letters (lower-case and upper-case), ',' and '.'.
> - 1 <= numRows <= 1000

> [!info] Approach
> Rather than simulating the 2D grid (wastes space), we can directly assign each character to its row number by tracking which row we're currently on and the direction we're moving. Maintain `numRows` string builders (one per row). Walk the characters, appending each to the current row's builder, while toggling direction at the top and bottom rows. Track `current_row` (starts at 0) and `direction` (+1 going down, -1 going up). Flip direction when `current_row == 0` or `current_row == numRows - 1`. Final answer = concatenation of all row strings.


> [!note]- Python Solution
> ```python
> def convert(s, num_rows):
>     if num_rows == 1 or num_rows >= len(s):
>         return s
>     rows = [''] * num_rows
>     current_row = 0
>     direction = -1
>     for ch in s:
>         rows[current_row] += ch
>         if current_row == 0 or current_row == num_rows - 1:
>             direction *= -1
>         current_row += direction
>     return ''.join(rows)
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Mathematical index formula: for each row `r`, characters fall at periodic positions. Row 0 and `numRows-1` have period `2*(numRows-1)`; middle rows have two characters per period. Direct but trickier to get indices right.

---

### Valid Palindrome II (LC 680) `🔥 Google`

> [!example] Problem
> Given a string s, return true if the s can be palindrome after deleting at most one character from it.
> 
> **Example 1:**
> ```
> Input: s = "aba"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: s = "abca"
> Output: true
> Explanation: You could delete the character 'c'.
> ```
> 
> **Example 3:**
> ```
> Input: s = "abc"
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s consists of lowercase English letters.

> [!info] Approach
> A standard two-pointer palindrome check stops at the first mismatch. At that point, removing either the left or right character might fix things — we just need to check both possibilities. Two pointers `left` and `right`. If characters match, move both inward. On mismatch, try removing `left` or removing `right` and check if the remainder is a palindrome. Helper `is_palindrome(l, r)` checks `s[l..r]`. Main: walk until mismatch, then return `is_palindrome(left+1, right) or is_palindrome(left, right-1)`.


> [!note]- Python Solution
> ```python
> def valid_palindrome(s):
>     def is_palindrome(left, right):
>         while left < right:
>             if s[left] != s[right]:
>                 return False
>             left += 1
>             right -= 1
>         return True
> >
>     left = 0
>     right = len(s) - 1
>     while left < right:
>         if s[left] != s[right]:
>             return is_palindrome(left + 1, right) or is_palindrome(left, right - 1)
>         left += 1
>         right -= 1
>     return True
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Check all single-character deletions: O(n²) — correct but too slow.
> - Key insight: once we find a mismatch, we only try removing one of the two mismatching characters — no need to try every position.

---

### Reverse Words in a String (LC 151)

> [!example] Problem
> Given an input string s, reverse the order of the words.
> A word is defined as a sequence of non-space characters. The words in s will be separated by at least one space.
> Return a string of the words in reverse order concatenated by a single space.
> Note that s may contain leading or trailing spaces or multiple spaces between two words. The returned string should only have a single space separating the words. Do not include any extra spaces.
> 
> **Example 1:**
> ```
> Input: s = "the sky is blue"
> Output: "blue is sky the"
> ```
> 
> **Example 2:**
> ```
> Input: s = "  hello world  "
> Output: "world hello"
> Explanation: Your reversed string should not contain leading or trailing spaces.
> ```
> 
> **Example 3:**
> ```
> Input: s = "a good   example"
> Output: "example good a"
> Explanation: You need to reduce multiple spaces between two words to a single space in the reversed string.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^4
> - s contains English letters (upper-case and lower-case), digits, and spaces ' '.
> - There is at least one word in s.

> [!info] Approach
> Python's `split()` without arguments handles multiple spaces and strips leading/trailing whitespace. Reverse the resulting list and rejoin. Split on whitespace, reverse the list, join with single space. `words = s.split()` → `words.reverse()` → `return ' '.join(words)`.


> [!note]- Python Solution
> ```python
> def reverse_words(s):
>     words = s.split()
>     words.reverse()
>     return ' '.join(words)
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - In-place (for C/C++): (1) reverse the entire string, (2) reverse each individual word, (3) remove extra spaces. O(n) time, O(1) space.
> - Key distinction: LC 151 asks for reversed *word order*, not reversed characters within words.

---

## See Also

[[two-pointers]] | [[sliding-window]] | [[hashing]] | [[string-algorithms]]
