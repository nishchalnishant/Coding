---
tags: [coding, algorithms, string-algorithms]
topic: String Algorithms
difficulty: mixed
---

# String Algorithms

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.





---

## KMP (Knuth-Morris-Pratt)

---

### Implement KMP — Failure Function + Search

> [!example] Problem
> Implement the KMP algorithm: given pattern P and text T, return all start indices where P occurs in T.

> [!info] Approach
> [!info] Approach
> Naive search rescans characters already matched; O(nm) is unacceptable for large text. Pre-process the pattern once into an LPS (Longest Proper Prefix which is also Suffix) array that encodes where to restart matching on mismatch. `lps[i]` = length of longest proper prefix of `P[0..i]` that is also a suffix. On mismatch at pattern position `j`, jump to `lps[j-1]`; the text pointer `i` never moves backward. O(n+m) total because every character is "visited" at most twice.

> [!note]- Python Solution
> ```python
> def build_lps(pattern):
>     m = len(pattern)
>     lps = [0] * m
>     length = 0  # length of current matching border
>     i = 1
>     while i < m:
>         if pattern[i] == pattern[length]:
>             length += 1
>             lps[i] = length
>             i += 1
>         elif length:
>             length = lps[length - 1]   # fall back
>             do NOT increment i
>         else:
>             lps[i] = 0
>             i += 1
>     return lps
> 
> def kmp_search(text, pattern):
>     if not pattern:
>         return list(range(len(text) + 1))
>     n, m = len(text), len(pattern)
>     lps = build_lps(pattern)
>     matches = []
>     i = j = 0
>     while i < n:
>         if text[i] == pattern[j]:
>             i += 1
>             j += 1
>         if j == m:
>             matches.append(i - j)
>             j = lps[j - 1]
>         elif i < n and text[i] != pattern[j]:
>             if j:
>                 j = lps[j - 1]
>             else:
>                 i += 1
>     return matches
> ```

> [!success] Complexity
> Time O(n+m) | Space O(m) for LPS.

> [!tip] Alternatives
> - Z-algorithm: conceptually equivalent, different encoding. Concatenate `P + '#' + T`, compute Z-array; positions where `Z[i] == m` are matches.
> - Rabin-Karp: O(n+m) average but O(nm) worst (collisions); simpler to implement, less predictable.

---

### Find All Occurrences of Pattern in Text

> [!example] Problem
> Return all start indices where pattern P occurs in text T (overlapping matches allowed).

> [!info] Approach
> [!info] Approach
> Standard substring search is O(nm); we need every occurrence, not just the first. KMP search as above, but after each match at `i - j`, reset `j = lps[j-1]` (not 0) to allow overlapping. The line `j = lps[j-1]` after a match is the key — it reuses the overlap, so overlapping occurrences like `"aaa"` in `"aaaa"` are all found.

> [!note]- Python Solution
> ```python
> def find_all_occurrences(text, pattern):
>     if not pattern:
>         return list(range(len(text) + 1))
>     n, m = len(text), len(pattern)
>     lps = build_lps(pattern)   # same build_lps as above
>     matches = []
>     i = j = 0
>     while i < n:
>         if text[i] == pattern[j]:
>             i += 1
>             j += 1
>         if j == m:
>             matches.append(i - j)
>             j = lps[j - 1]    # allow overlap by not resetting j to 0
>         elif i < n and text[i] != pattern[j]:
>             j = lps[j - 1] if j else 0
>             if not j:
>                 i += 1
>     return matches
> ```

> [!success] Complexity
> Time O(n+m) | Space O(m).

> [!tip] Alternatives
> Z-algorithm handles overlapping matches identically. Python `re.finditer` with `(?=pattern)` lookahead for overlapping matches in practice.

---

### Add Minimum Characters to Make String a Palindrome

> [!example] Problem
> Find the minimum number of characters to add to the front of `s` to make it a palindrome. (Equivalently: find the longest palindromic prefix.)

> [!info] Approach
> [!info] Approach
> We need the longest prefix of s that is already a palindrome; characters after that prefix must be reflected at the front. Concatenate `s + '#' + reverse(s)`. The LPS value at the last position gives the length of the longest prefix of s that matches a suffix of `reverse(s)` — that's the longest palindromic prefix. `LPS[last]` on the concatenated string = length of longest palindromic prefix. Minimum additions = `n - LPS[last]`.

> [!note]- Python Solution
> ```python
> def min_chars_to_palindrome(s):
>     combined = s + '#' + s[::-1]
>     lps = build_lps(combined)
>     longest_palindromic_prefix = lps[-1]
>     return len(s) - longest_palindromic_prefix
> 
> def make_palindrome(s):
>     combined = s + '#' + s[::-1]
>     lps = build_lps(combined)
>     suffix_to_add = s[lps[-1]:][::-1]
>     return suffix_to_add + s
> ```

> [!success] Complexity
> Time O(n) | Space O(n).

> [!tip] Alternatives
> Two-pointer from both ends with backtracking: O(n²) worst case. Rolling hash + binary search: O(n log n), harder to implement correctly.

---

## Rabin-Karp (Rolling Hash)

---

### Implement Rabin-Karp

> [!example] Problem
> Find all occurrences of pattern in text using rolling hash.

> [!info] Approach
> [!info] Approach
> Direct character-by-character comparison at each position is O(nm). Hashing reduces window comparison to O(1) per step. Represent each window as a polynomial hash. Sliding the window right removes the leftmost character and adds the rightmost: `hash(new) = (hash(old) - text[i]*BASE^(m-1)) * BASE + text[i+m]`. Pre-compute `BASE^(m-1) mod MOD`. On hash match, verify character-by-character to rule out collisions. Double hashing (two independent mod values) reduces false positive probability to ~1/(p₁·p₂).

> [!note]- Python Solution
> ```python
> def rabin_karp(text, pattern):
>     n, m = len(text), len(pattern)
>     if m > n:
>         return []
>     BASE, MOD = 131, (1 << 61) - 1   # Mersenne prime for fast mod
> 
>     def hval(c):
>         return ord(c)
> 
>     # precompute BASE^(m-1) mod MOD
>     power = pow(BASE, m - 1, MOD)
>     pat_hash = win_hash = 0
>     for i in range(m):
>         pat_hash = (pat_hash * BASE + hval(pattern[i])) % MOD
>         win_hash = (win_hash * BASE + hval(text[i])) % MOD
> 
>     matches = []
>     if win_hash == pat_hash and text[:m] == pattern:
>         matches.append(0)
> 
>     for i in range(1, n - m + 1):
>         win_hash = (win_hash - hval(text[i - 1]) * power) % MOD
>         win_hash = (win_hash * BASE + hval(text[i + m - 1])) % MOD
>         win_hash %= MOD
>         if win_hash == pat_hash and text[i:i + m] == pattern:
>             matches.append(i)
>     return matches
> ```

> [!success] Complexity
> Time O(n+m) average, O(nm) worst (all collisions) | Space O(1).

> [!tip] Alternatives
> KMP: O(n+m) guaranteed worst case. Z-algorithm: same O(n+m) guaranteed. Rabin-Karp preferred when: simpler code acceptable, or multi-pattern (hash all patterns into a set, O(1) lookup per window).

---

### Longest Duplicate Substring `⚡ T1`

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
> [!info] Approach
> Checking all substrings for duplicates is O(n³). We need a smarter search space reduction. Binary search on length L. For each L, use rolling hash to collect all length-L substring hashes in a set; if any hash appears twice (and verification confirms no collision), a duplicate of length L exists. Binary search `[1, n-1]`. `check(L)`: slide window of size L, compute hash in O(1) per step, store in set. If duplicate found, record it; search larger L. If not, search smaller. Total: O(n log n).

> [!note]- Python Solution
> ```python
> def longest_dup_substring(s):
>     BASE, MOD = 131, (1 << 61) - 1
>     n = len(s)
>     nums = [ord(c) for c in s]
> 
>     def check(length):
>         power = pow(BASE, length, MOD)
>         h = 0
>         for c in nums[:length]:
>             h = (h * BASE + c) % MOD
>         seen = {h: [0]}
>         for i in range(1, n - length + 1):
>             h = (h * BASE - nums[i - 1] * power + nums[i + length - 1]) % MOD
>             if h in seen:
>                 for start in seen[h]:
>                     if s[start:start + length] == s[i:i + length]:
>                         return s[i:i + length]
>                 seen[h].append(i)
>             else:
>                 seen[h] = [i]
>         return ""
> 
>     lo, hi = 1, n - 1
>     result = ""
>     while lo <= hi:
>         mid = (lo + hi) // 2
>         candidate = check(mid)
>         if candidate:
>             result = candidate
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return result
> ```

> [!success] Complexity
> Time O(n log n) average | Space O(n).

> [!tip] Alternatives
> Suffix array + LCP array: O(n log n) build, then `max(LCP)` gives the answer in O(n). More complex to implement but same asymptotic and no collision risk.

---

### Count Distinct Doubled Substrings

> [!example] Problem
> Count distinct substrings `t` such that `t + t` (echo substring) appears in `s`.

> [!info] Approach
> [!info] Approach
> We need to find all substrings of even length where both halves are identical — checking naively is O(n³). For each possible half-length `L` (1 to n//2), slide a window of size `2L` and check if the left half hash equals the right half hash. Count distinct matches using a set. Maintain two rolling hashes (left window and right window of size L) simultaneously. When both hashes match, store the canonical string in a set for deduplication.

> [!note]- Python Solution
> ```python
> def count_distinct_echo_substrings(s):
>     BASE, MOD = 131, (1 << 61) - 1
>     n = len(s)
>     nums = [ord(c) for c in s]
>     seen = set()
> 
>     for L in range(1, n // 2 + 1):
>         power = pow(BASE, L, MOD)
>         lh = rh = 0
>         for i in range(L):
>             lh = (lh * BASE + nums[i]) % MOD
>             rh = (rh * BASE + nums[i + L]) % MOD
>         if lh == rh and s[:L] == s[L:2*L]:
>             seen.add(s[:L])
>         for i in range(1, n - 2 * L + 1):
>             lh = (lh * BASE - nums[i - 1] * power + nums[i + L - 1]) % MOD
>             rh = (rh * BASE - nums[i + L - 1] * power + nums[i + 2 * L - 1]) % MOD
>             if lh == rh and s[i:i+L] == s[i+L:i+2*L]:
>                 seen.add(s[i:i+L])
>     return len(seen)
> ```

> [!success] Complexity
> Time O(n²) — O(n/2) lengths × O(n) per length | Space O(n) for seen set.

> [!tip] Alternatives
> Suffix automaton can enumerate distinct substrings and check echo property in O(n log n) total, but is significantly more complex.

---

## Z-Function / Z-Algorithm

---

### Pattern Matching Using Z-Array

> [!example] Problem
> Find all occurrences of pattern P in text T using the Z-algorithm.

> [!info] Approach
> [!info] Approach
> Same goal as KMP — O(n+m) pattern matching. Z-algorithm is sometimes easier to reason about. `Z[i]` = length of the longest substring starting at position i of the concatenated string `P + '$' + T` that matches a prefix of the whole string. When `Z[i] == len(P)`, a match starts at `i - len(P) - 1` in T. Maintain a Z-box `[l, r]` — the rightmost interval where a match with a prefix is known. For each i: if `i <= r`, initialize `Z[i] = min(r - i + 1, Z[i - l])`; then try to extend. The total number of character comparisons is O(n+m) because the right boundary r only moves right.

> [!note]- Python Solution
> ```python
> def z_function(s):
>     n = len(s)
>     z = [0] * n
>     z[0] = n
>     l = r = 0
>     for i in range(1, n):
>         if i < r:
>             z[i] = min(r - i, z[i - l])
>         while i + z[i] < n and s[z[i]] == s[i + z[i]]:
>             z[i] += 1
>         if i + z[i] > r:
>             l, r = i, i + z[i]
>     return z
> 
> def z_search(text, pattern):
>     if not pattern:
>         return list(range(len(text) + 1))
>     combined = pattern + '$' + text
>     z = z_function(combined)
>     m = len(pattern)
>     return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] == m]
> ```

> [!success] Complexity
> Time O(n+m) | Space O(n+m).

> [!tip] Alternatives
> KMP: equivalent complexity, preserves text/pattern pointers separately (more natural for streaming). Z-algorithm: cleaner when you need the full Z-array for other purposes (e.g., repeated substring detection).

---

### Repeated String Match

> [!example] Problem
> Given two strings a and b, return the minimum number of times you should repeat string a so that string b is a substring of it. If it is impossible for b​​​​​​ to be a substring of a after repeating it, return -1.
> Notice: string "abc" repeated 0 times is "", repeated 1 time is "abc" and repeated 2 times is "abcabc".
> 
> **Example 1:**
> ```
> Input: a = "abcd", b = "cdabcdab"
> Output: 3
> Explanation: We return 3 because by repeating a three times "abcdabcdabcd", b is a substring of it.
> ```
> 
> **Example 2:**
> ```
> Input: a = "a", b = "aa"
> Output: 2
> ```
> 
> **Constraints:**
> - 1 <= a.length, b.length <= 10^4
> - a and b consist of lowercase English letters.

> [!info] Approach
> [!info] Approach
> B can span at most `ceil(len(B)/len(A)) + 1` copies of A. We only need to check a bounded repetition. Repeat A enough times to be at least as long as B, then check if B is a substring. If not, try once more repetition. The minimum repetitions needed is `ceil(len(B) / len(A))`. If B isn't found there, try `ceil + 1` (B might straddle one more copy). Use KMP or Z-algorithm for the search to stay O(|A| + |B|).

> [!note]- Python Solution
> ```python
> import math
> 
> def repeated_string_match(a, b):
>     min_reps = math.ceil(len(b) / len(a))
>     candidate = a * min_reps
>     # Use z-search or kmp_search for O(n+m)
>     if b in candidate:         # Python's `in` is O(n+m) via Boyer-Moore-Horspool
>         return min_reps
>     if b in candidate + a:
>         return min_reps + 1
>     return -1
> ```

> [!success] Complexity
> Time O(|A| + |B|) | Space O(|A| + |B|) for the repeated string.

> [!tip] Alternatives
> KMP on the cyclic string `a * (ceil + 1)` explicitly — same complexity, avoids string creation by using modular index `i % len(a)` during search.

---

## Palindrome Algorithms

---

### Longest Palindromic Substring — Expand Around Center `🎯 T2`

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
> [!info] Approach
> A palindrome reads the same forwards and backwards; the structural invariant is symmetry around a center. There are `2n - 1` possible centers (n single characters + n-1 gaps between characters). From each center, expand outward while `s[l] == s[r]`. For each i, try both odd-center `(i, i)` and even-center `(i, i+1)`. Track the longest expansion. No extra space needed.

> [!note]- Python Solution
> ```python
> def longest_palindrome(s):
>     best_l = best_r = 0
>     for i in range(len(s)):
>         for l, r in [(i, i), (i, i + 1)]:   # odd and even centers
>             while l >= 0 and r < len(s) and s[l] == s[r]:
>                 l -= 1
>                 r += 1
>             # palindrome is s[l+1 : r]
>             if r - l - 1 > best_r - best_l:
>                 best_l, best_r = l + 1, r
>     return s[best_l:best_r]
> ```

> [!success] Complexity
> Time O(n²) | Space O(1).

> [!tip] Alternatives
> Manacher's algorithm: O(n) by reusing previously computed expansions. DP `dp[i][j]` = is_palindrome: O(n²) time and space — no better than expand around center and uses more memory. Hashing + binary search: O(n log n).

---

### Palindromic Substrings — Count

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
> [!info] Approach
> Each center expansion contributes one palindrome per step. Counting is a minor modification of the longest palindrome approach. For each center, expand as long as characters match; each valid `(l, r)` pair is one palindromic substring. Same 2n-1 centers. For each center, count the number of valid expansions (each step adds 1 to count).

> [!note]- Python Solution
> ```python
> def count_substrings(s):
>     count = 0
>     for i in range(len(s)):
>         for l, r in [(i, i), (i, i + 1)]:
>             while l >= 0 and r < len(s) and s[l] == s[r]:
>                 count += 1
>                 l -= 1
>                 r += 1
>     return count
> ```

> [!success] Complexity
> Time O(n²) | Space O(1).

> [!tip] Alternatives
> Manacher's: O(n) — `P[i]` (palindrome radius at i) directly gives the count contribution for center i; total = `sum((P[i] + 1) // 2 for all i)`. DP table `is_pal[i][j]`: O(n²) time and space.

---

### Manacher's Algorithm — O(n) All Palindromes

> [!example] Problem
> Find the radius of the longest palindromic substring centered at every position in O(n). LeetCode 5 (O(n) solution).

> [!info] Approach
> [!info] Approach
> Naive expand-around-center is O(n²) because each center expands independently. Manacher reuses overlap between palindromes. Transform `s` by inserting `#` between every character (`a#b#b#a` → `#a#b#b#a#`) to unify odd and even cases. Maintain the rightmost palindrome center `c` and its right boundary `r`. For each position i: mirror `i` across `c` to get `mirror = 2c - i`. Initialize `P[i] = min(r - i, P[mirror])` — reuse what's already known. Then try to extend beyond that. Update `c, r` when a new palindrome extends past `r`. Each character is "extended past" at most once (because r only increases), so total comparisons = O(n).

> [!note]- Python Solution
> ```python
> def manacher(s):
>     # Transform: "abc" -> "#a#b#c#"
>     t = '#' + '#'.join(s) + '#'
>     n = len(t)
>     P = [0] * n   # P[i] = palindrome radius at i in transformed string
>     c = r = 0     # center and right boundary of rightmost palindrome
> 
>     for i in range(n):
>         mirror = 2 * c - i
>         if i < r:
>             P[i] = min(r - i, P[mirror])
>         # Attempt to expand beyond known boundary
>         left, right = i - P[i] - 1, i + P[i] + 1
>         while left >= 0 and right < n and t[left] == t[right]:
>             P[i] += 1
>             left -= 1
>             right += 1
>         # Update rightmost palindrome
>         if i + P[i] > r:
>             c, r = i, i + P[i]
>     return P
> 
> def longest_palindrome_manacher(s):
>     P = manacher(s)
>     t = '#' + '#'.join(s) + '#'
>     center = P.index(max(P))
>     radius = P[center]
>     # Map back: original index = (center - radius) // 2
>     start = (center - radius) // 2
>     return s[start: start + radius]
> ```

> [!success] Complexity
> Time O(n) | Space O(n).

> [!tip] Alternatives
> Expand around center: O(n²) but simpler code; sufficient for most interview constraints (n ≤ 10⁵). Use Manacher when explicitly asked for O(n) or n > 10⁵.

---

## Sliding Window on Strings

---

### Longest Substring with K Distinct Characters

> [!example] Problem
> Find the length of the longest substring containing at most K distinct characters. LeetCode 340.

> [!info] Approach
> [!info] Approach
> We want the longest window satisfying a constraint on character diversity — a classic sliding window. Maintain a frequency map of characters in the current window. The window is valid iff `len(freq) <= K`. Expand right always; when invalid (K+1 distinct chars), shrink left until valid again. When `freq[s[left]] == 0` after decrement, delete from map — this decrements distinct count. Window size at each valid state is a candidate answer.

> [!note]- Python Solution
> ```python
> def length_of_longest_substring_k_distinct(s, k):
>     if k == 0:
>         return 0
>     freq = {}
>     left = result = 0
>     for right in range(len(s)):
>         freq[s[right]] = freq.get(s[right], 0) + 1
>         while len(freq) > k:
>             freq[s[left]] -= 1
>             if freq[s[left]] == 0:
>                 del freq[s[left]]
>             left += 1
>         result = max(result, right - left + 1)
>     return result
> ```

> [!success] Complexity
> Time O(n) | Space O(k) for frequency map.

> [!tip] Alternatives
> Ordered dict (LinkedHashMap in Java) tracks insertion order for O(1) eviction of the least recently seen character — useful variant for "exactly K distinct" or streaming eviction. Binary search on window length: O(n log n), no benefit.

---

### Permutation in String `⚡ T1`

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
> [!info] Approach
> A permutation of `s1` is any arrangement of its characters; we need a window in `s2` with the same character frequencies. Fixed-size sliding window of size `len(s1)`. Compare character frequency arrays. When `matches == 26`, a permutation is found. Track `matches` = number of characters (out of 26) where window frequency equals s1 frequency. Slide window: add right char, remove left char, update `matches` accordingly. Avoids O(26) comparison per step.

> [!note]- Python Solution
> ```python
> def check_inclusion(s1, s2):
>     if len(s1) > len(s2):
>         return False
>     need = [0] * 26
>     have = [0] * 26
>     for c in s1:
>         need[ord(c) - ord('a')] += 1
> 
>     matches = sum(1 for i in range(26) if need[i] == 0)  # chars not needed start matched
> 
>     def update(c, delta):
>         nonlocal matches
>         idx = ord(c) - ord('a')
>         old = have[idx]
>         have[idx] += delta
>         new = have[idx]
>         if old == need[idx]:
>             matches -= 1   # was matched, now not
>         if new == need[idx]:
>             matches += 1   # now matched
>         return matches
> 
>     k = len(s1)
>     for i in range(k):
>         update(s2[i], 1)
>     if matches == 26:
>         return True
>     for i in range(k, len(s2)):
>         update(s2[i], 1)
>         update(s2[i - k], -1)
>         if matches == 26:
>             return True
>     return False
> ```

> [!success] Complexity
> Time O(|s1| + |s2|) | Space O(1) (26-element arrays).

> [!tip] Alternatives
> Sort both: O(n log n), only works for single query. Counter comparison per window: O(26n) = O(n) with worse constant.

---

### Regular Expression Matching (LC 10)

> [!example] Problem
> Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:
> The matching should cover the entire input string (not partial).
> 
> **Example 1:**
> ```
> Input: s = "aa", p = "a"
> Output: false
> Explanation: "a" does not match the entire string "aa".
> ```
> 
> **Example 2:**
> ```
> Input: s = "aa", p = "a*"
> Output: true
> Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".
> ```
> 
> **Example 3:**
> ```
> Input: s = "ab", p = ".*"
> Output: true
> Explanation: ".*" means "zero or more (*) of any character (.)".
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 20
> - 1 <= p.length <= 20
> - s contains only lowercase English letters.
> - p contains only lowercase English letters, '.', and '*'.
> - It is guaranteed for each appearance of the character '*', there will be a previous valid character to match.

> [!info] Approach
> [!info] Approach
> `'*'` creates a choice — use the preceding element 0 times (skip `pattern[i-1]` and `'*'`) or 1+ times (consume `s[j]` if it matches). These choices overlap across subproblems → DP. `dp[i][j]` = True if `s[:i]` matches `p[:j]`.

>   - Base: `dp[0][0] = True`. `dp[0][j] = True` if `p[j-1] == '*'` and `dp[0][j-2] == True` (star eliminates the preceding element).
>   - Transition: if `p[j-1] in {s[i-1], '.'}`: `dp[i][j] = dp[i-1][j-1]`.
>   - Else if `p[j-1] == '*'`: `dp[i][j] = dp[i][j-2]` (zero uses) OR (`dp[i-1][j]` if `p[j-2] in {s[i-1], '.'}`) (one or more uses).

> [!note]- Python Solution
> ```python
> def is_match(s, p):
>     m, n = len(s), len(p)
>     dp = [[False] * (n + 1) for _ in range(m + 1)]
>     dp[0][0] = True
>     # Base: patterns like a*, a*b*, a*b*c* can match empty string
>     for j in range(2, n + 1):
>         if p[j - 1] == '*':
>             dp[0][j] = dp[0][j - 2]
> >
>     for i in range(1, m + 1):
>         for j in range(1, n + 1):
>             if p[j - 1] in {s[i - 1], '.'}:
>                 dp[i][j] = dp[i - 1][j - 1]
>             elif p[j - 1] == '*':
>                 dp[i][j] = dp[i][j - 2]  # zero uses of preceding element
>                 if p[j - 2] in {s[i - 1], '.'}:
>                     dp[i][j] = dp[i][j] or dp[i - 1][j]  # one+ uses
>     return dp[m][n]
> ```

> [!success] Complexity
> Time O(m·n) | Space O(m·n). Space reducible to O(n) with rolling row.

> [!tip] Alternatives
> - Recursive with memoization: same O(m·n), often cleaner logic — top-down avoids filling unused states.
> - NFA simulation: O(m·n) advanced, treats `'*'` as epsilon transitions; naturally handles complex patterns but harder to code in interviews.

---

### Wildcard Matching (LC 44)

> [!example] Problem
> Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:
> The matching should cover the entire input string (not partial).
> 
> **Example 1:**
> ```
> Input: s = "aa", p = "a"
> Output: false
> Explanation: "a" does not match the entire string "aa".
> ```
> 
> **Example 2:**
> ```
> Input: s = "aa", p = "*"
> Output: true
> Explanation: '*' matches any sequence.
> ```
> 
> **Example 3:**
> ```
> Input: s = "cb", p = "?a"
> Output: false
> Explanation: '?' matches 'c', but the second letter is 'a', which does not match 'b'.
> ```
> 
> **Constraints:**
> - 0 <= s.length, p.length <= 2000
> - s contains only lowercase English letters.
> - p contains only lowercase English letters, '?' or '*'.

> [!info] Approach
> [!info] Approach
> `'*'` can match any sequence — creates branching over all possible lengths. DP avoids recomputing overlapping subproblems. `dp[i][j]` = True if `s[:i]` matches `p[:j]`.

>   - Base: `dp[0][0] = True`. `dp[0][j] = True` if `p[:j]` is all `'*'` (each star matches empty).
>   - Transition: if `p[j-1] in {s[i-1], '?'}`: `dp[i][j] = dp[i-1][j-1]`.
>   - Else if `p[j-1] == '*'`: `dp[i][j] = dp[i-1][j]` (star matches one char) OR `dp[i][j-1]` (star matches empty).

> [!note]- Python Solution
> ```python
> def is_match_wildcard(s, p):
>     m, n = len(s), len(p)
>     dp = [[False] * (n + 1) for _ in range(m + 1)]
>     dp[0][0] = True
>     for j in range(1, n + 1):
>         if p[j - 1] == '*':
>             dp[0][j] = dp[0][j - 1]
> >
>     for i in range(1, m + 1):
>         for j in range(1, n + 1):
>             if p[j - 1] in {s[i - 1], '?'}:
>                 dp[i][j] = dp[i - 1][j - 1]
>             elif p[j - 1] == '*':
>                 dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
>     return dp[m][n]
> ```

> [!success] Complexity
> Time O(m·n) | Space O(m·n). Space reducible to O(n) with rolling row.

> [!tip] Alternatives
> - Two-pointer greedy O(m+n): scan `s` and `p` linearly; on `'*'`, save position and backtrack on mismatch. O(m·n) worst case but no extra space and fast in practice.
> - NFA simulation: same O(m·n) structure.

---

### Distinct Subsequences (LC 115) `🎯 T2`

> [!example] Problem
> Given two strings s and t, return the number of distinct subsequences of s which equals t.
> The test cases are generated so that the answer fits on a 32-bit signed integer.
> 
> **Example 1:**
> ```
> Input: s = "rabbbit", t = "rabbit"
> Output: 3
> Explanation:
> As shown below, there are 3 ways you can generate "rabbit" from s.
> rabbbit
> rabbbit
> rabbbit
> ```
> 
> **Example 2:**
> ```
> Input: s = "babgbag", t = "bag"
> Output: 5
> Explanation:
> As shown below, there are 5 ways you can generate "bag" from s.
> babgbag
> babgbag
> babgbag
> babgbag
> babgbag
> ```
> 
> **Constraints:**
> - 1 <= s.length, t.length <= 1000
> - s and t consist of English letters.

> [!info] Approach
> [!info] Approach
> At each character of `s`, we choose to include it (matching `t[j]`) or skip it. These choices create overlapping subproblems → DP. `dp[i][j]` = number of ways to form `t[:j]` from `s[:i]`.

>   - Base: `dp[i][0] = 1` for all i (empty `t` matched by any prefix of `s`). `dp[0][j] = 0` for j > 0.
>   - Transition: if `s[i-1] == t[j-1]`: `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]` (use this char OR skip it).
>   - Else: `dp[i][j] = dp[i-1][j]` (must skip `s[i-1]`).

> [!note]- Python Solution
> ```python
> def num_distinct(s, t):
>     m, n = len(s), len(t)
>     # Space-optimized 1D DP (process j in reverse to avoid overwrite)
>     dp = [0] * (n + 1)
>     dp[0] = 1  # empty t matched by empty prefix
> >
>     for i in range(1, m + 1):
>         # Traverse right to left to use values from dp[i-1][...]
>         for j in range(n, 0, -1):
>             if s[i - 1] == t[j - 1]:
>                 dp[j] += dp[j - 1]
>         # dp[0] stays 1 (empty t always matchable)
>     return dp[n]
> ```

> [!success] Complexity
> Time O(m·n) | Space O(n) with 1D optimization.

> [!tip] Alternatives
> - Memoized recursion: same O(m·n) — `dfs(i, j)` returns ways to form `t[j:]` from `s[i:]`; cleaner top-down logic.
> - Early termination: if `len(s) - i < len(t) - j`, return 0 (impossible to match remaining t).

---

## See Also

[[string]] | [[trie]] | [[dynamic-programming]] | [[sliding-window]]
### Shortest Palindrome

> [!example] Problem
> You are given a string s. You can convert s to a palindrome by adding characters in front of it.
> Return the shortest palindrome you can find by performing this transformation.
> 
> **Example 1:**
> ```
> Input: s = "aacecaaa"
> Output: "aaacecaaa"
> ```
> 
> **Example 2:**
> ```
> Input: s = "abcd"
> Output: "dcbabcd"
> ```
> 
> **Constraints:**
> - 0 <= s.length <= 5 * 10^4
> - s consists of lowercase English letters only.

> [!info] Approach
> We need the longest palindromic prefix. Once we know that prefix, the remaining suffix must be reversed and prepended. Build a KMP prefix table on `s + '#' + reverse(s)` to find the longest prefix of `s` that matches a suffix of the reversed string. The LPS value at the end gives the longest palindromic prefix length. Prepend the reverse of the remaining suffix.

> [!note]- Python Solution
> ```python
> def shortest_palindrome(s):
>     rev = s[::-1]
>     t = s + "#" + rev
>     lps = [0] * len(t)
>     for i in range(1, len(t)):
>         j = lps[i - 1]
>         while j > 0 and t[i] != t[j]:
>             j = lps[j - 1]
>         if t[i] == t[j]:
>             j += 1
>         lps[i] = j
>     return rev[: len(s) - lps[-1]] + s
> ```

> [!success] Complexity
> O(n) time, O(n) space.

> [!tip] Alternatives
> Manacher's algorithm can also locate palindromic prefixes, but the KMP trick is the standard interview shortcut.

---

## String Algorithms — More Problems

### Add Minimum Characters to Make a String Palindrome

> [!example] Problem
> Given string `s`, find the minimum number of characters to insert (anywhere) to make it a palindrome.

> [!info] Approach
> Minimum insertions = `n - LPS(s)`, where LPS is the Longest Palindromic Subsequence. Alternatively: min insertions = n - LCS(s, reverse(s)), since the LCS of s with its reverse is the longest palindromic subsequence. Compute LCS of `s` and `reverse(s)` using DP. `lcs[i][j]` = LCS length of `s[:i]` and `rev[:j]`. Answer is `n - lcs[n][n]`. Standard O(n²) DP. Can space-optimise to O(n) using two rows.

> [!note]- Python Solution
> ```python
> def min_insertions_palindrome(s):
>     n = len(s)
>     rev = s[::-1]
>     prev = [0] * (n + 1)
>     for i in range(1, n + 1):
>         curr = [0] * (n + 1)
>         for j in range(1, n + 1):
>             if s[i-1] == rev[j-1]:
>                 curr[j] = prev[j-1] + 1
>             else:
>                 curr[j] = max(prev[j], curr[j-1])
>         prev = curr
>     lps = prev[n]
>     return n - lps
> ```

> [!success] Complexity
> Time O(n²), Space O(n).

> [!tip] Alternatives
> - Direct DP: `dp[i][j]` = min insertions to make `s[i..j]` a palindrome. If `s[i] == s[j]`: `dp[i][j] = dp[i+1][j-1]`. Else: `1 + min(dp[i+1][j], dp[i][j-1])`. Same O(n²) time/space.
> - Key equivalence: min insertions = n - LPS = n - LCS(s, reverse(s)).

---

