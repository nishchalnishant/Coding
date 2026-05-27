---
tags: [coding, data-structures, string]
topic: String
difficulty: mixed
---

# String Problems — Deep Dive

Pattern tags: frequency map, two pointers, sliding window, hashing, parsing.

---

## Frequency Map / Anagram

### Valid Anagram

> [!example] Problem
> Given two strings `s` and `t`, return true if `t` is an anagram of `s` — i.e., they contain the same characters with the same frequencies.

> [!info] Approach
> - **WHY:** Two strings are anagrams iff they are identical after sorting. Sorting is O(n log n). We can do O(n) by comparing character frequency vectors.
> - **WHAT:** A 26-bucket frequency array (fixed alphabet) or a `Counter`. Two strings are anagrams iff their frequency maps are equal.
> - **HOW:** Build `Counter(s)` and `Counter(t)`. Return `Counter(s) == Counter(t)`. For pure lowercase ASCII, use `[0]*26` and compare arrays — same asymptotic cost, better constant.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def isAnagram(s: str, t: str) -> bool:
>     if len(s) != len(t):
>         return False
>     return Counter(s) == Counter(t)
> 
> # O(1) space variant for lowercase a-z only
> def isAnagram_array(s: str, t: str) -> bool:
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

### Group Anagrams

> [!example] Problem
> Given a list of strings, group all anagrams together. Return the groups in any order.

> [!info] Approach
> - **WHY:** All anagrams share the same canonical form — their sorted version. Use that as a hash map key.
> - **WHAT:** HashMap from canonical key → list of anagrams. For pure lowercase ASCII, use a tuple of 26 frequency counts as key (avoids O(L log L) sort per word).
> - **HOW:** For each word, compute `key = tuple(freq_array)` or `key = "".join(sorted(word))`. Append word to `groups[key]`. Return `list(groups.values())`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def groupAnagrams(strs: list[str]) -> list[list[str]]:
>     groups: dict[tuple, list[str]] = defaultdict(list)
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

### Find All Anagrams in a String

> [!example] Problem
> Given strings `s` and `p`, return all starting indices in `s` where a substring is an anagram of `p`.

> [!info] Approach
> - **WHY:** We need a fixed-size sliding window of length `len(p)`. Comparing two frequency arrays is O(26) = O(1) per step.
> - **WHAT:** Fixed-size window sliding over `s`, maintaining a frequency array for the current window. Compare it to the target frequency array of `p`.
> - **HOW:** Build `p_freq`. Maintain `w_freq` for the window. Add the incoming character on the right; evict the outgoing character on the left when the window exceeds `len(p)`. If arrays match, record the left index. Use a `matches` counter to avoid O(26) comparison: track how many of the 26 buckets currently match between `w_freq` and `p_freq`.

> [!note]- Python Solution
> ```python
> def findAnagrams(s: str, p: str) -> list[int]:
>     if len(p) > len(s):
>         return []
>     p_freq = [0] * 26
>     w_freq = [0] * 26
>     for c in p:
>         p_freq[ord(c) - ord('a')] += 1
> 
>     matches = sum(1 for i in range(26) if p_freq[i] == w_freq[i])
>     result: list[int] = []
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

### Valid Palindrome

> [!example] Problem
> Given string `s`, return true if it is a palindrome considering only alphanumeric characters and ignoring case.

> [!info] Approach
> - **WHY:** After filtering to alphanumeric + lowercase, a palindrome reads the same forwards and backwards. Two pointers moving inward compare characters without allocating a filtered string.
> - **WHAT:** Left pointer starts at 0, right pointer starts at end. Skip non-alphanumeric characters. Compare lowercase versions.
> - **HOW:** While `l < r`: skip `l` while not alphanumeric, skip `r` while not alphanumeric. If `s[l].lower() != s[r].lower()`, return False. Advance both pointers inward.

> [!note]- Python Solution
> ```python
> def isPalindrome(s: str) -> bool:
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

### Longest Palindromic Substring

> [!example] Problem
> Given string `s`, return the longest substring that is a palindrome.

> [!info] Approach
> - **WHY:** A palindrome is symmetric around its center. Expanding outward from each possible center checks all palindromes in O(n²) without a 2D DP table.
> - **WHAT:** Expand-around-center. For each of the `2n - 1` possible centers (n odd-length centers at each character, n-1 even-length centers between adjacent characters), expand outward while characters match.
> - **HOW:** `expand(l, r)` expands while `s[l] == s[r]` and indices are in bounds, returning the palindrome substring. For each index `i`, try both `expand(i, i)` (odd length) and `expand(i, i+1)` (even length). Track the longest result.

> [!note]- Python Solution
> ```python
> def longestPalindrome(s: str) -> str:
>     def expand(l: int, r: int) -> str:
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
> Given string `s`, return the total count of substrings that are palindromes (single characters count too).

> [!info] Approach
> - **WHY:** Same expand-around-center logic as Longest Palindromic Substring, but instead of tracking the longest, count every expansion that succeeds.
> - **WHAT:** For each center, count how many times we can expand — each successful expansion is one more palindromic substring.
> - **HOW:** For each of the `2n - 1` centers, expand while `s[l] == s[r]`. Each valid `(l, r)` pair is one palindromic substring — increment count by 1 each step.

> [!note]- Python Solution
> ```python
> def countSubstrings(s: str) -> int:
>     count = 0
> 
>     def expand(l: int, r: int) -> None:
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

### Longest Substring Without Repeating Characters

> [!example] Problem
> Given string `s`, return the length of the longest substring with all unique characters.

> [!info] Approach
> - **WHY:** A valid window has all unique characters. The window must shrink from the left when a duplicate enters — a variable-size sliding window maintains this invariant.
> - **WHAT:** Variable-size window with a set tracking current characters. Shrink left until the duplicate is gone. Track `max(right - left + 1)`.
> - **HOW:** For each `right`: if `s[right]` is in the set, remove `s[left]` and advance `left` until the duplicate is gone. Then add `s[right]` and update max.

> [!note]- Python Solution
> ```python
> def lengthOfLongestSubstring(s: str) -> int:
>     seen: set[str] = set()
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

### Minimum Window Substring

> [!example] Problem
> Given strings `s` and `t`, find the minimum length substring of `s` that contains all characters of `t` (including duplicates). Return `""` if none exists.

> [!info] Approach
> - **WHY:** We need the smallest window satisfying all character demands from `t`. Expanding right adds characters; once the window is valid, shrink left to minimize it. The `formed` counter makes validity check O(1).
> - **WHAT:** Variable-size sliding window with two frequency maps (`need` for t, `have` for current window) and a `formed` count of satisfied characters.
> - **HOW:** Expand right: add `s[right]` to `have`; if `have[c] == need[c]`, increment `formed`. When `formed == len(need)` (window valid): record min window, shrink from left — decrement `have[s[left]]`; if it drops below `need[s[left]]`, decrement `formed`. Repeat shrinking until no longer valid.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def minWindow(s: str, t: str) -> str:
>     if not t or not s:
>         return ""
>     need = Counter(t)
>     have: dict[str, int] = {}
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

### Longest Repeating Character Replacement

> [!example] Problem
> Given string `s` and integer `k`, find the length of the longest substring where you can replace at most `k` characters to make all characters in the window the same.

> [!info] Approach
> - **WHY:** A window is valid iff `window_length - max_frequency_in_window <= k`. Slide and never contract the window below its historical maximum — we only care about longer windows.
> - **WHAT:** Sliding window with a frequency map. `max_freq` tracks the frequency of the most common character seen so far (across all window positions — it is allowed to be slightly stale when shrinking because we only care about longer windows).
> - **HOW:** Expand right: update `count[s[right]]` and `max_freq`. If `(window_size - max_freq) > k`, slide left by 1 — don't shrink, just slide. The window grows when a valid longer window is found.

> [!note]- Python Solution
> ```python
> def characterReplacement(s: str, k: int) -> int:
>     count: dict[str, int] = {}
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

> [!info] Approach
> WHY: Count substrings satisfying a character-frequency constraint in O(n) using prefix sum + hash map — the exact same technique as numeric subarray sum problems.
> WHAT: Map characters to numbers (e.g., vowel=1/non-vowel=0, or treat a binary string as 0/1). Build a running sum; use a hash map to count valid pairs. For "exactly k" problems use the at-most trick: `exactly(k) = atMost(k) - atMost(k-1)`.
> HOW: `prefix_count = {0: 1}; running = 0`. For each element: `running += value(element)`. `answer += prefix_count.get(running - target, 0)`. `prefix_count[running] += 1`.

---

### Number of Substrings Containing All Three Characters

> [!example] Problem
> Given string `s` containing only characters `a`, `b`, and `c`, return the number of substrings containing all three characters at least once.

> [!info] Approach
> WHY: For any right endpoint `r`, the valid left endpoints form a contiguous suffix — as soon as all three chars appear, every further-left start also works. Track the rightmost position where each character was last seen.
> WHAT: Single pass tracking `last[a]`, `last[b]`, `last[c]` (most recent index of each). At each `r`, the number of valid starting points ending at `r` is `min(last_a, last_b, last_c) + 1` (all positions from 0 to that minimum).
> HOW: Maintain `last = [-1, -1, -1]` for a/b/c. For each `r`, update `last[ord(s[r]) - ord('a')] = r`. Add `min(last) + 1` to answer (clamped to 0 when any char unseen).

> [!note]- Python Solution
> ```python
> def numberOfSubstrings(s: str) -> int:
>     last = [-1, -1, -1]
>     count = 0
>     for r, ch in enumerate(s):
>         last[ord(ch) - ord('a')] = r
>         count += min(last) + 1   # -1 if any char unseen → contributes 0
>     return count
>
> # Alternative: prefix count approach
> def numberOfSubstrings_prefix(s: str) -> int:
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
> WHY: Direct sliding window with "exactly 5 distinct vowels" is non-monotone. Use the at-most trick: `exactly(5) = atMost(5) - atMost(4)`.
> WHAT: `atMost(k)` counts substrings made of vowels only, with at most k distinct vowels. For each right pointer, advance left until only-vowels and ≤ k distinct. Add `r - l + 1`.
> HOW: `atMost(k)`: `l = 0, freq = {}`. For each `r`: if `s[r]` not a vowel, reset window (`l = r+1, freq = {}`). Else update `freq[s[r]]`. While `len(freq) > k`, shrink `l`. Add `r - l + 1`. Answer = `atMost(5) - atMost(4)`.

> [!note]- Python Solution
> ```python
> def countVowelSubstrings(word: str) -> int:
>     VOWELS = set('aeiou')
>
>     def at_most(k: int) -> int:
>         freq: dict[str, int] = {}
>         l = res = 0
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
>             res += r - l + 1
>         return res
>
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
> Given a binary array `nums` and integer `goal`, return the number of non-empty subarrays with sum equal to `goal`.

> [!info] Approach
> WHY: Binary array can have negative-like complications if solved with sliding window (zero elements don't shrink the sum). Prefix sum + hash map handles it cleanly. Alternatively, at-most trick works since elements are non-negative.
> WHAT: Prefix sum approach: `prefix_count[0] = 1`. Running sum; `answer += prefix_count[running - goal]`.
> HOW: `seen = {0: 1}, running = count = 0`. For each `x`: `running += x`, `count += seen.get(running - goal, 0)`, `seen[running] = seen.get(running, 0) + 1`.

> [!note]- Python Solution
> ```python
> def numSubarraysWithSum(nums: list[int], goal: int) -> int:
>     from collections import defaultdict
>     prefix_count: dict[int, int] = defaultdict(int)
>     prefix_count[0] = 1
>     running = count = 0
>     for x in nums:
>         running += x
>         count += prefix_count[running - goal]
>         prefix_count[running] += 1
>     return count
>
> # At-most sliding window variant
> def numSubarraysWithSum_window(nums: list[int], goal: int) -> int:
>     def at_most(k: int) -> int:
>         if k < 0:
>             return 0
>         l = res = running = 0
>         for r, x in enumerate(nums):
>             running += x
>             while running > k:
>                 running -= nums[l]
>                 l += 1
>             res += r - l + 1
>         return res
>     return at_most(goal) - at_most(goal - 1)
> ```

> [!success] Complexity
> Time O(n), Space O(n) for prefix map / O(1) for sliding window.

> [!tip] Alternatives
> - Sliding window at-most trick: `exactly(k) = atMost(k) - atMost(k-1)`. O(n) time, O(1) space. Works because elements are non-negative.
> - Brute force O(n²): prefix sum array + nested loop over all (l, r) pairs.

---

### Subarray Sum Equals K (character version)

> [!example] Problem
> Count subarrays of a string where a specific target character appears exactly `k` times.

> [!info] Approach
> WHY: Map target character to 1, all others to 0 — identical to the numeric subarray sum equals k problem.
> WHAT: Standard prefix sum + hash map. `prefix_count[0] = 1`. Running sum of mapped values; `answer += prefix_count[running - k]`.
> HOW: For each character `ch`: `running += (1 if ch == target else 0)`. `count += prefix_count[running - k]`. `prefix_count[running] += 1`.

> [!note]- Python Solution
> ```python
> def countSubstringsWithKChars(s: str, target: str, k: int) -> int:
>     from collections import defaultdict
>     prefix_count: dict[int, int] = defaultdict(int)
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

### Encode and Decode Strings

> [!example] Problem
> Design functions `encode(strs)` and `decode(s)` to encode a list of strings into a single string and decode it back. The encoding must handle strings that contain any character including `#` and `/`.

> [!info] Approach
> - **WHY:** Simple delimiters (`,`, `#`) fail if the strings contain those characters. A length-prefix scheme is delimiter-free and unambiguous.
> - **WHAT:** Encode each string as `{length}#{string}`. The `#` here marks the end of the length field, not a content separator — the length tells us exactly how many bytes to read.
> - **HOW:** Encode: for each string, emit `str(len(s)) + '#' + s`. Decode: read digits up to `#` to get length L; read exactly L characters as the next string; advance pointer past them; repeat.

> [!note]- Python Solution
> ```python
> def encode(strs: list[str]) -> str:
>     return "".join(f"{len(s)}#{s}" for s in strs)
> 
> def decode(s: str) -> list[str]:
>     result: list[str] = []
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
> - **WHY:** Comparing every pair of substrings of length L is O(n × L) per comparison and O(n²L) total. A rolling hash computes each substring's hash in O(1) after O(n) preprocessing.
> - **WHAT:** Polynomial rolling hash: `hash(s[i..i+L-1]) = s[i] * base^(L-1) + s[i+1] * base^(L-2) + ... + s[i+L-1]`. Slide by subtracting the leftmost character's contribution and adding the rightmost — O(1) per step.
> - **HOW:** Compute `hash(s[0..L-1])`. For each subsequent position, update the hash by the sliding formula. Store hashes in a set. On collision, verify with string comparison to rule out false positives.

> [!note]- Python Solution
> ```python
> def hasDuplicateOfLength(s: str, L: int) -> bool:
>     if L == 0:
>         return True
>     BASE, MOD = 31, (1 << 61) - 1   # Mersenne prime for low collision rate
>     # Use Python's set of substrings for simplicity (avoids collision handling)
>     seen: set[str] = set()
>     for i in range(len(s) - L + 1):
>         sub = s[i:i + L]
>         if sub in seen:
>             return True
>         seen.add(sub)
>     return False
> 
> # Rolling hash variant — O(n) without substring creation
> def hasDuplicateOfLengthFast(s: str, L: int) -> int | None:
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
> Implement `myAtoi(s)` that converts a string to a 32-bit signed integer. Handle leading whitespace, optional sign, digit parsing, non-digit termination, and overflow clamping to `[-2^31, 2^31-1]`.

> [!info] Approach
> - **WHY:** This is a state-machine / parsing problem. The transformation rules are explicit — model each parsing phase as a step.
> - **WHAT:** Sequential parsing: (1) strip leading whitespace, (2) read optional sign, (3) accumulate digits, (4) stop at first non-digit, (5) clamp to 32-bit range.
> - **HOW:** Advance `i` past spaces. Read sign. Accumulate `result = result * 10 + digit` for each digit character. Before adding, check for overflow: if `result > (INT_MAX - digit) // 10`, clamp and return. Return `sign * result`.

> [!note]- Python Solution
> ```python
> def myAtoi(s: str) -> int:
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
> Given a list of strings, return the longest common prefix shared by all strings. Return `""` if none exists.

> [!info] Approach
> - **WHY:** The longest common prefix is bounded by the shortest string. Compare column by column: the prefix ends at the first position where any string differs.
> - **WHAT:** Vertical scanning — for each character position `i`, check if all strings have the same character at `i`. Stop at the first mismatch or when any string ends.
> - **HOW:** Take `strs[0]` as the reference. For each character index `i` in `strs[0]`, check every other string at position `i`. If any string is shorter than `i` or differs at `i`, return `strs[0][:i]`.

> [!note]- Python Solution
> ```python
> def longestCommonPrefix(strs: list[str]) -> str:
>     if not strs:
>         return ""
>     for i, char in enumerate(strs[0]):
>         for s in strs[1:]:
>             if i == len(s) or s[i] != char:
>                 return strs[0][:i]
>     return strs[0]
> 
> # Alternative: binary search on prefix length
> def longestCommonPrefixBinarySearch(strs: list[str]) -> str:
>     def allMatch(length: int) -> bool:
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

## See Also

[[string-algorithms]] | [[sliding-window]] | [[hashing]] | [[two-pointers]] | [[dynamic-programming]]
