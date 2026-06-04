---
tags: [coding, algorithms, string-algorithms]
topic: String Algorithms
difficulty: mixed
---

# String Algorithms

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
>             length = lps[length - 1]   # fall back; do NOT increment i
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
>             i += 1; j += 1
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
>             i += 1; j += 1
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

### Repeated Substring Pattern

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
> [!info] Approach
> Brute-force tries every divisor length — O(n√n). KMP gives O(n). If s has period p (smallest repeating unit), then `n % p == 0` and the LPS value encodes that period: period = `n - lps[n-1]`. Build LPS of the full string s. If `lps[n-1] > 0` and `n % (n - lps[n-1]) == 0`, a valid period exists. Equivalently, check if s appears in `(s+s)[1:-1]`.



> [!note]- Python Solution
> ```python
> def repeated_substring_pattern(s):
>     n = len(s)
>     lps = build_lps(s)
>     period = n - lps[n - 1]
>     return lps[n - 1] > 0 and n % period == 0
> ```

> [!success] Complexity
> Time O(n) | Space O(n).

> [!tip] Alternatives
> `s in (s+s)[1:-1]` — one-liner using string containment; O(n) via Python's internal search (Boyer-Moore-Horspool), but less explicit about why it works.

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

### Longest Duplicate Substring

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

### Longest Palindromic Substring — Expand Around Center

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
>                 l -= 1; r += 1
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
>                 l -= 1; r += 1
>     return count
> ```

> [!success] Complexity
> Time O(n²) | Space O(1).

> [!tip] Alternatives
> Manacher's: O(n) — `P[i]` (palindrome radius at i) directly gives the count contribution for center i; total = `sum((P[i] + 1) // 2 for all i)`. DP table `is_pal[i][j]`: O(n²) time and space.

---

### Palindrome Partitioning II — Minimum Cuts

> [!example] Problem
> Given a string s, partition s such that every substring of the partition is a palindrome.
> Return the minimum cuts needed for a palindrome partitioning of s.
> 
> **Example 1:**
> ```
> Input: s = "aab"
> Output: 1
> Explanation: The palindrome partitioning ["aa","b"] could be produced using 1 cut.
> ```
> 
> **Example 2:**
> ```
> Input: s = "a"
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: s = "ab"
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 2000
> - s consists of lowercase English letters only.

> [!info] Approach
> [!info] Approach
> We want the minimum cuts — this is an optimization problem over all valid partitions. `dp[i]` = minimum cuts to partition `s[0..i]` into palindromes. For each i, find all palindromes ending at i and update: if `s[j..i]` is a palindrome, `dp[i] = min(dp[i], dp[j-1] + 1)`. Pre-compute `is_pal[i][j]` using expand-around-center in O(n²). Then linear scan for `dp[i]`. Base: `dp[i] = i` (cut every character). If `s[0..i]` is itself a palindrome, `dp[i] = 0`.



> [!note]- Python Solution
> ```python
> def min_cut(s):
>     n = len(s)
>     # Precompute palindrome table via expand-around-center
>     is_pal = [[False] * n for _ in range(n)]
>     for center in range(2 * n - 1):
>         l, r = center // 2, (center + 1) // 2
>         while l >= 0 and r < n and s[l] == s[r]:
>             is_pal[l][r] = True
>             l -= 1; r += 1
> 
>     dp = list(range(n))   # dp[i] = i means i cuts (all single chars)
>     for i in range(1, n):
>         if is_pal[0][i]:
>             dp[i] = 0
>             continue
>         for j in range(1, i + 1):
>             if is_pal[j][i]:
>                 dp[i] = min(dp[i], dp[j - 1] + 1)
>     return dp[n - 1]
> ```

> [!success] Complexity
> Time O(n²) | Space O(n²) for palindrome table; reducible to O(n) by computing palindromes on-the-fly.

> [!tip] Alternatives
> Manacher's for O(n) palindrome precomputation, then same DP: still O(n²) overall due to DP transitions. O(n) DP using palindrome center expansions to push updates forward exists but is complex.

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
>             left -= 1; right += 1
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

## Suffix Array / Trie Based

---

### Number of Distinct Substrings

> [!example] Problem
> Count the number of distinct substrings in string `s` (including empty string is sometimes excluded — confirm per problem).

> [!info] Approach
> [!info] Approach
> Total substrings = n(n+1)/2. Duplicates arise when multiple suffixes share a common prefix. The LCP array captures exactly this overlap. Build suffix array SA (sorted order of all suffixes). Build LCP array via Kasai's algorithm: `LCP[i]` = longest common prefix between `SA[i]` and `SA[i-1]`. Each suffix contributes `(n - SA[i]) - LCP[i]` new distinct substrings (total length minus the shared prefix already counted). Distinct substrings = `n(n+1)/2 - sum(LCP)`.



> [!note]- Python Solution
> ```python
> def count_distinct_substrings(s):
>     n = len(s)
> 
>     # O(n log^2 n) suffix array via prefix doubling
>     sa = sorted(range(n), key=lambda i: s[i:])  # O(n^2 log n) — use SA-IS for large n
> 
>     # Kasai's algorithm for LCP array — O(n)
>     rank = [0] * n
>     for i, suffix_start in enumerate(sa):
>         rank[suffix_start] = i
>     lcp = [0] * n
>     h = 0
>     for i in range(n):
>         if rank[i] > 0:
>             j = sa[rank[i] - 1]
>             while i + h < n and j + h < n and s[i + h] == s[j + h]:
>                 h += 1
>             lcp[rank[i]] = h
>             if h > 0:
>                 h -= 1
> 
>     total = n * (n + 1) // 2
>     return total - sum(lcp)
> ```

> [!success] Complexity
> Time O(n log² n) for suffix array (O(n log n) with radix sort), O(n) for LCP via Kasai | Space O(n).

> [!tip] Alternatives
> Suffix automaton (SAM): O(n) build, counts distinct substrings as sum of `len[v] - len[link[v]]` over all states. More complex to implement but strictly O(n).

---

### Longest Common Prefix of All Suffixes

> [!example] Problem
> Build the LCP array for a string and answer: what is the longest string that appears as a prefix in at least two suffixes?

> [!info] Approach
> [!info] Approach
> Brute-force LCP computation between all suffix pairs is O(n²). Kasai's algorithm exploits the rank structure to do it in O(n). After building the suffix array SA, `LCP[i]` = length of common prefix between suffix `SA[i]` and suffix `SA[i-1]` in sorted order. The maximum LCP value = longest repeated substring. Kasai's key insight: if suffix starting at i has LCP of h with its SA predecessor, then suffix starting at `i+1` has LCP ≥ h-1 with its SA predecessor. This means we can start each computation from `h-1` and `h` only ever decreases by 1 between iterations → O(n) total.



> [!note]- Python Solution
> ```python
> def build_suffix_array_and_lcp(s):
>     n = len(s)
>     sa = sorted(range(n), key=lambda i: s[i:])   # simple O(n^2 log n); replace with DC3 for O(n)
> 
>     rank = [0] * n
>     for i, v in enumerate(sa):
>         rank[v] = i
>     lcp = [0] * n
>     h = 0
>     for i in range(n):
>         if rank[i] > 0:
>             j = sa[rank[i] - 1]
>             while i + h < n and j + h < n and s[i + h] == s[j + h]:
>                 h += 1
>             lcp[rank[i]] = h
>             if h:
>                 h -= 1
>     return sa, lcp
> 
> def longest_repeated_substring(s):
>     sa, lcp = build_suffix_array_and_lcp(s)
>     max_lcp = max(lcp)
>     idx = lcp.index(max_lcp)
>     return s[sa[idx]: sa[idx] + max_lcp]
> ```

> [!success] Complexity
> Time O(n log² n) build + O(n) Kasai | Space O(n).

> [!tip] Alternatives
> Rolling hash + binary search: O(n log n) with collision risk. Suffix automaton: O(n) but complex.

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

### Permutation in String

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

### Minimum Window Substring

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
> [!info] Approach
> We need the minimum-length window — expand to satisfy the constraint, then shrink to minimize. `need` = frequency of chars in t. `have` = frequency in current window. `formed` = distinct chars satisfying their required count. Expand right; when `formed == len(need)`, shrink left until invalid, recording minimum window. `formed` increments only when `have[c] == need[c]` (exact threshold), not on every increment. This makes the condition O(1) to check per step.



> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def min_window(s, t):
>     if not t or not s:
>         return ""
>     need = Counter(t)
>     have = {}
>     formed = required = len(need)
>     left = 0
>     best = (float('inf'), 0, 0)   # (length, left, right)
> 
>     for right in range(len(s)):
>         c = s[right]
>         have[c] = have.get(c, 0) + 1
>         if c in need and have[c] == need[c]:
>             formed -= 1
>         while formed == 0:
>             if right - left + 1 < best[0]:
>                 best = (right - left + 1, left, right)
>             lc = s[left]
>             have[lc] -= 1
>             if lc in need and have[lc] < need[lc]:
>                 formed += 1
>             left += 1
> 
>     return s[best[1]:best[2] + 1] if best[0] != float('inf') else ""
> ```

> [!success] Complexity
> Time O(|s| + |t|) | Space O(|s| + |t|) (bounded by alphabet size in practice).

> [!tip] Alternatives
> Filtered array (pre-filter s to only chars in t): reduces inner work when |t| << |s|, same asymptotic but better constant. Brute force: O(|s|² · |t|).

---

## Classic String Problems

---

### Valid Palindrome

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
> [!info] Approach
> Strip down to the essential characters and apply the two-pointer palindrome check. Two pointers from both ends. Skip non-alphanumeric characters; compare lowercase. No extra string creation needed — move pointers in-place.



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
>         l += 1; r -= 1
>     return True
> ```

> [!success] Complexity
> Time O(n) | Space O(1).

> [!tip] Alternatives
> Build cleaned string then compare to reverse: O(n) time, O(n) space — simpler but wasteful.

---

### Valid Anagram

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
> [!info] Approach
> Anagrams are the same multiset of characters. Checking multiset equality is the core. Build frequency arrays (or Counter). If they match, anagram. One pass to build, one pass to compare. O(n) time. For Unicode inputs use Counter (not fixed 26-array).



> [!note]- Python Solution
> ```python
> def is_anagram(s, t):
>     if len(s) != len(t):
>         return False
>     count = [0] * 26
>     for a, b in zip(s, t):
>         count[ord(a) - ord('a')] += 1
>         count[ord(b) - ord('a')] -= 1
>     return all(c == 0 for c in count)
> ```

> [!success] Complexity
> Time O(n) | Space O(1).

> [!tip] Alternatives
> Sort both and compare: O(n log n). Counter subtraction: `Counter(s) == Counter(t)` — O(n), Pythonic.

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
> [!info] Approach
> The LCP can be at most the length of the shortest string, and is bounded by where any string diverges. Vertical scanning — for each character position, check if all strings agree. Stop at first disagreement. Compare position by position across all strings. Return the prefix up to the first mismatch.



> [!note]- Python Solution
> ```python
> def longest_common_prefix(strs):
>     if not strs:
>         return ""
>     for i, chars in enumerate(zip(*strs)):
>         if len(set(chars)) > 1:
>             return strs[0][:i]
>     return min(strs, key=len)
> ```

> [!success] Complexity
> Time O(S) where S = total characters | Space O(1).

> [!tip] Alternatives
> Sort the array; LCP of first and last string = answer (they're the most different). Binary search on prefix length, O(S log(min_len)). Trie: overkill for a single query but useful for repeated LCP queries.

---

### Group Anagrams

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
> [!info] Approach
> Anagrams share the same character multiset — use a canonical key that encodes the multiset. For each string, compute a canonical key (sorted string or 26-char tuple). Group strings by key using a hash map. Sorting each string: O(k log k) per string where k = max length. Total: O(nk log k). Alternatively, use a tuple of 26 counts as key: O(nk) total.



> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def group_anagrams(strs):
>     groups = defaultdict(list)
>     for s in strs:
>         key = tuple(sorted(s))   # or: key = count_key(s)
>         groups[key].append(s)
>     return list(groups.values())
> ```

> [!success] Complexity
> Time O(nk log k) with sort key, O(nk) with count-tuple key | Space O(nk).

> [!tip] Alternatives
> Prime product key: assign a prime to each letter, multiply. Unique per anagram group but risks integer overflow for long strings.

---

### Longest Substring Without Repeating Characters

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
> [!info] Approach
> Classic sliding window — maintain the invariant that the window has no duplicate. Track the last seen index of each character. When a character reappears inside the window, advance `left` to `last_seen[c] + 1`. Direct index tracking is more efficient than a frequency-decrement approach for this problem.



> [!note]- Python Solution
> ```python
> def length_of_longest_substring(s):
>     last_seen = {}
>     left = result = 0
>     for right, c in enumerate(s):
>         if c in last_seen and last_seen[c] >= left:
>             left = last_seen[c] + 1
>         last_seen[c] = right
>         result = max(result, right - left + 1)
>     return result
> ```

> [!success] Complexity
> Time O(n) | Space O(min(n, alphabet_size)).

> [!tip] Alternatives
> Set-based sliding window: `while c in window: remove s[left]; left++`. Same O(n) but more operations. Frequency map: also O(n), more general.

---

### Find All Anagrams in a String

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
> [!info] Approach
> An anagram of p is a fixed-size window in s with the same character frequencies. Sliding window of fixed size `len(p)`. Track matches (same `matches` counter as Permutation in String). Identical to Permutation in String but collect all starting indices where `matches == 26` instead of returning True on first match.



> [!note]- Python Solution
> ```python
> def find_anagrams(s, p):
>     if len(p) > len(s):
>         return []
>     need = [0] * 26
>     have = [0] * 26
>     for c in p:
>         need[ord(c) - ord('a')] += 1
>     matches = sum(1 for i in range(26) if need[i] == 0)
>     result = []
>     k = len(p)
> 
>     def update(c, delta):
>         nonlocal matches
>         idx = ord(c) - ord('a')
>         old, have[idx] = have[idx], have[idx] + delta
>         if old == need[idx]:
>             matches -= 1
>         if have[idx] == need[idx]:
>             matches += 1
> 
>     for i in range(k):
>         update(s[i], 1)
>     if matches == 26:
>         result.append(0)
>     for i in range(k, len(s)):
>         update(s[i], 1)
>         update(s[i - k], -1)
>         if matches == 26:
>             result.append(i - k + 1)
>     return result
> ```

> [!success] Complexity
> Time O(|s| + |p|) | Space O(1).

> [!tip] Alternatives
> Counter comparison per window: O(26 · |s|) = O(|s|). Sorting each window: O(|s| · k log k) — too slow.

---

## DP on Strings

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

### Distinct Subsequences (LC 115)

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

### Palindrome Pairs (LC 336)

> [!example] Problem
> You are given a 0-indexed array of unique strings words.
> A palindrome pair is a pair of integers (i, j) such that:
> Return an array of all the palindrome pairs of words.
> You must write an algorithm with O(sum of words[i].length) runtime complexity.
> 
> **Example 1:**
> ```
> Input: words = ["abcd","dcba","lls","s","sssll"]
> Output: [[0,1],[1,0],[3,2],[2,4]]
> Explanation: The palindromes are ["abcddcba","dcbaabcd","slls","llssssll"]
> ```
> 
> **Example 2:**
> ```
> Input: words = ["bat","tab","cat"]
> Output: [[0,1],[1,0]]
> Explanation: The palindromes are ["battab","tabbat"]
> ```
> 
> **Example 3:**
> ```
> Input: words = ["a",""]
> Output: [[0,1],[1,0]]
> Explanation: The palindromes are ["a","a"]
> ```
> 
> **Constraints:**
> - 1 <= words.length <= 5000
> - 0 <= words[i].length <= 300
> - words[i] consists of lowercase English letters.

> [!info] Approach
> Brute force O(n² * k) is too slow. For each word, consider all ways to split it: if the prefix is a palindrome and the reverse of the suffix exists in the word list, we have a valid pair (and vice versa). Build `word_map = {word: index}`. For each word `w` at index `i`, for every split point `k` in `0..len(w)`:

>   - If `w[:k]` is palindrome and `reverse(w[k:])` is in map: pair `(map[rev(w[k:])], i)`.
>   - If `w[k:]` is palindrome and `reverse(w[:k])` is in map (and `k > 0` to avoid double-counting): pair `(i, map[rev(w[:k])])`.
> Skip pairing a word with itself (`j != i`).

> [!note]- Python Solution
> ```python
> def palindrome_pairs(words):
>     word_map = {word: i for i, word in enumerate(words)}
>     result = []
> >
>     def is_palindrome(s):
>         return s == s[::-1]
> >
>     for i, word in enumerate(words):
>         n = len(word)
>         for k in range(n + 1):
>             prefix = word[:k]
>             suffix = word[k:]
>             if is_palindrome(prefix):
>                 rev_suffix = suffix[::-1]
>                 if rev_suffix in word_map and word_map[rev_suffix] != i:
>                     result.append([word_map[rev_suffix], i])
>             if k > 0 and is_palindrome(suffix):
>                 rev_prefix = prefix[::-1]
>                 if rev_prefix in word_map and word_map[rev_prefix] != i:
>                     result.append([i, word_map[rev_prefix]])
>     return result
> ```

> [!success] Complexity
> Time O(n * k²) where k = average word length (each split checks palindrome in O(k) and hash lookup in O(k)). Space O(n * k).

> [!tip] Alternatives
> - Trie-based approach: insert reversed words into a trie, walk each word through the trie checking palindrome conditions. Same asymptotic, higher constant.
> - Key insight: every valid pair falls into one of two split cases — don't try to think of other cases.

---

## See Also

[[trie]] | [[dynamic-programming]] | [[hashing]] | [[sliding-window]]
