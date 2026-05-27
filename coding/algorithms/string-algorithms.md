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
> - **WHY → WHAT → HOW.**
> - WHY: Naive search rescans characters already matched; O(nm) is unacceptable for large text.
> - WHAT: Pre-process the pattern once into an LPS (Longest Proper Prefix which is also Suffix) array that encodes where to restart matching on mismatch.
> - HOW: `lps[i]` = length of longest proper prefix of `P[0..i]` that is also a suffix. On mismatch at pattern position `j`, jump to `lps[j-1]`; the text pointer `i` never moves backward. O(n+m) total because every character is "visited" at most twice.

> [!note]- Python Solution
> ```python
> def build_lps(pattern: str) -> list[int]:
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
> def kmp_search(text: str, pattern: str) -> list[int]:
>     if not pattern:
>         return list(range(len(text) + 1))
>     n, m = len(text), len(pattern)
>     lps = build_lps(pattern)
>     matches: list[int] = []
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
> - **WHY → WHAT → HOW.**
> - WHY: Standard substring search is O(nm); we need every occurrence, not just the first.
> - WHAT: KMP search as above, but after each match at `i - j`, reset `j = lps[j-1]` (not 0) to allow overlapping.
> - HOW: The line `j = lps[j-1]` after a match is the key — it reuses the overlap, so overlapping occurrences like `"aaa"` in `"aaaa"` are all found.

> [!note]- Python Solution
> ```python
> def find_all_occurrences(text: str, pattern: str) -> list[int]:
>     if not pattern:
>         return list(range(len(text) + 1))
>     n, m = len(text), len(pattern)
>     lps = build_lps(pattern)   # same build_lps as above
>     matches: list[int] = []
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
> Given string `s`, check if it can be constructed by repeating a substring of it.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Brute-force tries every divisor length — O(n√n). KMP gives O(n).
> - WHAT: If s has period p (smallest repeating unit), then `n % p == 0` and the LPS value encodes that period: period = `n - lps[n-1]`.
> - HOW: Build LPS of the full string s. If `lps[n-1] > 0` and `n % (n - lps[n-1]) == 0`, a valid period exists. Equivalently, check if s appears in `(s+s)[1:-1]`.

> [!note]- Python Solution
> ```python
> def repeated_substring_pattern(s: str) -> bool:
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
> - **WHY → WHAT → HOW.**
> - WHY: We need the longest prefix of s that is already a palindrome; characters after that prefix must be reflected at the front.
> - WHAT: Concatenate `s + '#' + reverse(s)`. The LPS value at the last position gives the length of the longest prefix of s that matches a suffix of `reverse(s)` — that's the longest palindromic prefix.
> - HOW: `LPS[last]` on the concatenated string = length of longest palindromic prefix. Minimum additions = `n - LPS[last]`.

> [!note]- Python Solution
> ```python
> def min_chars_to_palindrome(s: str) -> int:
>     combined = s + '#' + s[::-1]
>     lps = build_lps(combined)
>     longest_palindromic_prefix = lps[-1]
>     return len(s) - longest_palindromic_prefix
> 
> def make_palindrome(s: str) -> str:
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
> - **WHY → WHAT → HOW.**
> - WHY: Direct character-by-character comparison at each position is O(nm). Hashing reduces window comparison to O(1) per step.
> - WHAT: Represent each window as a polynomial hash. Sliding the window right removes the leftmost character and adds the rightmost: `hash(new) = (hash(old) - text[i]*BASE^(m-1)) * BASE + text[i+m]`.
> - HOW: Pre-compute `BASE^(m-1) mod MOD`. On hash match, verify character-by-character to rule out collisions. Double hashing (two independent mod values) reduces false positive probability to ~1/(p₁·p₂).

> [!note]- Python Solution
> ```python
> def rabin_karp(text: str, pattern: str) -> list[int]:
>     n, m = len(text), len(pattern)
>     if m > n:
>         return []
>     BASE, MOD = 131, (1 << 61) - 1   # Mersenne prime for fast mod
> 
>     def hval(c: str) -> int:
>         return ord(c)
> 
>     # precompute BASE^(m-1) mod MOD
>     power = pow(BASE, m - 1, MOD)
>     pat_hash = win_hash = 0
>     for i in range(m):
>         pat_hash = (pat_hash * BASE + hval(pattern[i])) % MOD
>         win_hash = (win_hash * BASE + hval(text[i])) % MOD
> 
>     matches: list[int] = []
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
> Find the longest substring of `s` that appears at least twice (positions may overlap). LeetCode 1044.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Checking all substrings for duplicates is O(n³). We need a smarter search space reduction.
> - WHAT: Binary search on length L. For each L, use rolling hash to collect all length-L substring hashes in a set; if any hash appears twice (and verification confirms no collision), a duplicate of length L exists.
> - HOW: Binary search `[1, n-1]`. `check(L)`: slide window of size L, compute hash in O(1) per step, store in set. If duplicate found, record it; search larger L. If not, search smaller. Total: O(n log n).

> [!note]- Python Solution
> ```python
> def longest_dup_substring(s: str) -> str:
>     BASE, MOD = 131, (1 << 61) - 1
>     n = len(s)
>     nums = [ord(c) for c in s]
> 
>     def check(length: int) -> str:
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
> - **WHY → WHAT → HOW.**
> - WHY: We need to find all substrings of even length where both halves are identical — checking naively is O(n³).
> - WHAT: For each possible half-length `L` (1 to n//2), slide a window of size `2L` and check if the left half hash equals the right half hash. Count distinct matches using a set.
> - HOW: Maintain two rolling hashes (left window and right window of size L) simultaneously. When both hashes match, store the canonical string in a set for deduplication.

> [!note]- Python Solution
> ```python
> def count_distinct_echo_substrings(s: str) -> int:
>     BASE, MOD = 131, (1 << 61) - 1
>     n = len(s)
>     nums = [ord(c) for c in s]
>     seen: set[str] = set()
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
> - **WHY → WHAT → HOW.**
> - WHY: Same goal as KMP — O(n+m) pattern matching. Z-algorithm is sometimes easier to reason about.
> - WHAT: `Z[i]` = length of the longest substring starting at position i of the concatenated string `P + '$' + T` that matches a prefix of the whole string. When `Z[i] == len(P)`, a match starts at `i - len(P) - 1` in T.
> - HOW: Maintain a Z-box `[l, r]` — the rightmost interval where a match with a prefix is known. For each i: if `i <= r`, initialize `Z[i] = min(r - i + 1, Z[i - l])`; then try to extend. The total number of character comparisons is O(n+m) because the right boundary r only moves right.

> [!note]- Python Solution
> ```python
> def z_function(s: str) -> list[int]:
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
> def z_search(text: str, pattern: str) -> list[int]:
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
> Given strings A and B, find the minimum number of times A must be repeated so that B is a substring of the repeated A. Return -1 if impossible. LeetCode 686.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: B can span at most `ceil(len(B)/len(A)) + 1` copies of A. We only need to check a bounded repetition.
> - WHAT: Repeat A enough times to be at least as long as B, then check if B is a substring. If not, try once more repetition.
> - HOW: The minimum repetitions needed is `ceil(len(B) / len(A))`. If B isn't found there, try `ceil + 1` (B might straddle one more copy). Use KMP or Z-algorithm for the search to stay O(|A| + |B|).

> [!note]- Python Solution
> ```python
> import math
> 
> def repeated_string_match(a: str, b: str) -> int:
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
> Find the longest contiguous palindromic substring in `s`. LeetCode 5.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: A palindrome reads the same forwards and backwards; the structural invariant is symmetry around a center.
> - WHAT: There are `2n - 1` possible centers (n single characters + n-1 gaps between characters). From each center, expand outward while `s[l] == s[r]`.
> - HOW: For each i, try both odd-center `(i, i)` and even-center `(i, i+1)`. Track the longest expansion. No extra space needed.

> [!note]- Python Solution
> ```python
> def longest_palindrome(s: str) -> str:
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
> Count the total number of palindromic substrings in `s`. LeetCode 647.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Each center expansion contributes one palindrome per step. Counting is a minor modification of the longest palindrome approach.
> - WHAT: For each center, expand as long as characters match; each valid `(l, r)` pair is one palindromic substring.
> - HOW: Same 2n-1 centers. For each center, count the number of valid expansions (each step adds 1 to count).

> [!note]- Python Solution
> ```python
> def count_substrings(s: str) -> int:
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
> Given string `s`, find the minimum number of cuts so every substring in the partition is a palindrome. LeetCode 132.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: We want the minimum cuts — this is an optimization problem over all valid partitions.
> - WHAT: `dp[i]` = minimum cuts to partition `s[0..i]` into palindromes. For each i, find all palindromes ending at i and update: if `s[j..i]` is a palindrome, `dp[i] = min(dp[i], dp[j-1] + 1)`.
> - HOW: Pre-compute `is_pal[i][j]` using expand-around-center in O(n²). Then linear scan for `dp[i]`. Base: `dp[i] = i` (cut every character). If `s[0..i]` is itself a palindrome, `dp[i] = 0`.

> [!note]- Python Solution
> ```python
> def min_cut(s: str) -> int:
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
> - **WHY → WHAT → HOW.**
> - WHY: Naive expand-around-center is O(n²) because each center expands independently. Manacher reuses overlap between palindromes.
> - WHAT: Transform `s` by inserting `#` between every character (`a#b#b#a` → `#a#b#b#a#`) to unify odd and even cases. Maintain the rightmost palindrome center `c` and its right boundary `r`. For each position i: mirror `i` across `c` to get `mirror = 2c - i`. Initialize `P[i] = min(r - i, P[mirror])` — reuse what's already known. Then try to extend beyond that. Update `c, r` when a new palindrome extends past `r`.
> - HOW: Each character is "extended past" at most once (because r only increases), so total comparisons = O(n).

> [!note]- Python Solution
> ```python
> def manacher(s: str) -> list[int]:
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
> def longest_palindrome_manacher(s: str) -> str:
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
> - **WHY → WHAT → HOW.**
> - WHY: Total substrings = n(n+1)/2. Duplicates arise when multiple suffixes share a common prefix. The LCP array captures exactly this overlap.
> - WHAT: Build suffix array SA (sorted order of all suffixes). Build LCP array via Kasai's algorithm: `LCP[i]` = longest common prefix between `SA[i]` and `SA[i-1]`. Each suffix contributes `(n - SA[i]) - LCP[i]` new distinct substrings (total length minus the shared prefix already counted).
> - HOW: Distinct substrings = `n(n+1)/2 - sum(LCP)`.

> [!note]- Python Solution
> ```python
> def count_distinct_substrings(s: str) -> int:
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
> - **WHY → WHAT → HOW.**
> - WHY: Brute-force LCP computation between all suffix pairs is O(n²). Kasai's algorithm exploits the rank structure to do it in O(n).
> - WHAT: After building the suffix array SA, `LCP[i]` = length of common prefix between suffix `SA[i]` and suffix `SA[i-1]` in sorted order. The maximum LCP value = longest repeated substring.
> - HOW: Kasai's key insight: if suffix starting at i has LCP of h with its SA predecessor, then suffix starting at `i+1` has LCP ≥ h-1 with its SA predecessor. This means we can start each computation from `h-1` and `h` only ever decreases by 1 between iterations → O(n) total.

> [!note]- Python Solution
> ```python
> def build_suffix_array_and_lcp(s: str) -> tuple[list[int], list[int]]:
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
> def longest_repeated_substring(s: str) -> str:
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
> - **WHY → WHAT → HOW.**
> - WHY: We want the longest window satisfying a constraint on character diversity — a classic sliding window.
> - WHAT: Maintain a frequency map of characters in the current window. The window is valid iff `len(freq) <= K`. Expand right always; when invalid (K+1 distinct chars), shrink left until valid again.
> - HOW: When `freq[s[left]] == 0` after decrement, delete from map — this decrements distinct count. Window size at each valid state is a candidate answer.

> [!note]- Python Solution
> ```python
> def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
>     if k == 0:
>         return 0
>     freq: dict[str, int] = {}
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
> Given strings `s1` and `s2`, return True if any permutation of `s1` is a substring of `s2`. LeetCode 567.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: A permutation of `s1` is any arrangement of its characters; we need a window in `s2` with the same character frequencies.
> - WHAT: Fixed-size sliding window of size `len(s1)`. Compare character frequency arrays. When `matches == 26`, a permutation is found.
> - HOW: Track `matches` = number of characters (out of 26) where window frequency equals s1 frequency. Slide window: add right char, remove left char, update `matches` accordingly. Avoids O(26) comparison per step.

> [!note]- Python Solution
> ```python
> def check_inclusion(s1: str, s2: str) -> bool:
>     if len(s1) > len(s2):
>         return False
>     need = [0] * 26
>     have = [0] * 26
>     for c in s1:
>         need[ord(c) - ord('a')] += 1
> 
>     matches = sum(1 for i in range(26) if need[i] == 0)  # chars not needed start matched
> 
>     def update(c: str, delta: int) -> int:
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
> Find the shortest substring of `s` containing all characters of `t` (with duplicates). LeetCode 76.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: We need the minimum-length window — expand to satisfy the constraint, then shrink to minimize.
> - WHAT: `need` = frequency of chars in t. `have` = frequency in current window. `formed` = distinct chars satisfying their required count. Expand right; when `formed == len(need)`, shrink left until invalid, recording minimum window.
> - HOW: `formed` increments only when `have[c] == need[c]` (exact threshold), not on every increment. This makes the condition O(1) to check per step.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def min_window(s: str, t: str) -> str:
>     if not t or not s:
>         return ""
>     need = Counter(t)
>     have: dict[str, int] = {}
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
> Given string `s` (with non-alphanumeric characters), check if it reads the same forwards and backwards ignoring case and non-alphanumeric characters. LeetCode 125.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Strip down to the essential characters and apply the two-pointer palindrome check.
> - WHAT: Two pointers from both ends. Skip non-alphanumeric characters; compare lowercase.
> - HOW: No extra string creation needed — move pointers in-place.

> [!note]- Python Solution
> ```python
> def is_palindrome(s: str) -> bool:
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
> Check if string `t` is an anagram of `s`. LeetCode 242.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Anagrams are the same multiset of characters. Checking multiset equality is the core.
> - WHAT: Build frequency arrays (or Counter). If they match, anagram.
> - HOW: One pass to build, one pass to compare. O(n) time. For Unicode inputs use Counter (not fixed 26-array).

> [!note]- Python Solution
> ```python
> def is_anagram(s: str, t: str) -> bool:
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
> Find the longest common prefix string among an array of strings. LeetCode 14.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: The LCP can be at most the length of the shortest string, and is bounded by where any string diverges.
> - WHAT: Vertical scanning — for each character position, check if all strings agree. Stop at first disagreement.
> - HOW: Compare position by position across all strings. Return the prefix up to the first mismatch.

> [!note]- Python Solution
> ```python
> def longest_common_prefix(strs: list[str]) -> str:
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
> Given an array of strings, group all anagrams together. LeetCode 49.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Anagrams share the same character multiset — use a canonical key that encodes the multiset.
> - WHAT: For each string, compute a canonical key (sorted string or 26-char tuple). Group strings by key using a hash map.
> - HOW: Sorting each string: O(k log k) per string where k = max length. Total: O(nk log k). Alternatively, use a tuple of 26 counts as key: O(nk) total.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def group_anagrams(strs: list[str]) -> list[list[str]]:
>     groups: dict[tuple, list[str]] = defaultdict(list)
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
> Find the length of the longest substring with all unique characters. LeetCode 3.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: Classic sliding window — maintain the invariant that the window has no duplicate.
> - WHAT: Track the last seen index of each character. When a character reappears inside the window, advance `left` to `last_seen[c] + 1`.
> - HOW: Direct index tracking is more efficient than a frequency-decrement approach for this problem.

> [!note]- Python Solution
> ```python
> def length_of_longest_substring(s: str) -> int:
>     last_seen: dict[str, int] = {}
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
> Find all start indices of anagrams of `p` in `s`. LeetCode 438.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: An anagram of p is a fixed-size window in s with the same character frequencies.
> - WHAT: Sliding window of fixed size `len(p)`. Track matches (same `matches` counter as Permutation in String).
> - HOW: Identical to Permutation in String but collect all starting indices where `matches == 26` instead of returning True on first match.

> [!note]- Python Solution
> ```python
> def find_anagrams(s: str, p: str) -> list[int]:
>     if len(p) > len(s):
>         return []
>     need = [0] * 26
>     have = [0] * 26
>     for c in p:
>         need[ord(c) - ord('a')] += 1
>     matches = sum(1 for i in range(26) if need[i] == 0)
>     result: list[int] = []
>     k = len(p)
> 
>     def update(c: str, delta: int) -> None:
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
> Given string `s` and pattern `p` with `'.'` (any single char) and `'*'` (zero or more of preceding element), implement full regex matching. Must match the entire string.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: `'*'` creates a choice — use the preceding element 0 times (skip `pattern[i-1]` and `'*'`) or 1+ times (consume `s[j]` if it matches). These choices overlap across subproblems → DP.
> - WHAT: `dp[i][j]` = True if `s[:i]` matches `p[:j]`.
> - HOW:
>   - Base: `dp[0][0] = True`. `dp[0][j] = True` if `p[j-1] == '*'` and `dp[0][j-2] == True` (star eliminates the preceding element).
>   - Transition: if `p[j-1] in {s[i-1], '.'}`: `dp[i][j] = dp[i-1][j-1]`.
>   - Else if `p[j-1] == '*'`: `dp[i][j] = dp[i][j-2]` (zero uses) OR (`dp[i-1][j]` if `p[j-2] in {s[i-1], '.'}`) (one or more uses).

> [!note]- Python Solution
> ```python
> def is_match(s: str, p: str) -> bool:
>     m, n = len(s), len(p)
>     dp = [[False] * (n + 1) for _ in range(m + 1)]
>     dp[0][0] = True
>     # Base: patterns like a*, a*b*, a*b*c* can match empty string
>     for j in range(2, n + 1):
>         if p[j - 1] == '*':
>             dp[0][j] = dp[0][j - 2]
>
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
> Given string `s` and pattern `p` with `'?'` (any single char) and `'*'` (any sequence including empty), return True if `p` matches `s` entirely.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: `'*'` can match any sequence — creates branching over all possible lengths. DP avoids recomputing overlapping subproblems.
> - WHAT: `dp[i][j]` = True if `s[:i]` matches `p[:j]`.
> - HOW:
>   - Base: `dp[0][0] = True`. `dp[0][j] = True` if `p[:j]` is all `'*'` (each star matches empty).
>   - Transition: if `p[j-1] in {s[i-1], '?'}`: `dp[i][j] = dp[i-1][j-1]`.
>   - Else if `p[j-1] == '*'`: `dp[i][j] = dp[i-1][j]` (star matches one char) OR `dp[i][j-1]` (star matches empty).

> [!note]- Python Solution
> ```python
> def is_match_wildcard(s: str, p: str) -> bool:
>     m, n = len(s), len(p)
>     dp = [[False] * (n + 1) for _ in range(m + 1)]
>     dp[0][0] = True
>     for j in range(1, n + 1):
>         if p[j - 1] == '*':
>             dp[0][j] = dp[0][j - 1]
>
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
> Count the number of distinct ways to form string `t` as a subsequence of string `s`.

> [!info] Approach
> - **WHY → WHAT → HOW.**
> - WHY: At each character of `s`, we choose to include it (matching `t[j]`) or skip it. These choices create overlapping subproblems → DP.
> - WHAT: `dp[i][j]` = number of ways to form `t[:j]` from `s[:i]`.
> - HOW:
>   - Base: `dp[i][0] = 1` for all i (empty `t` matched by any prefix of `s`). `dp[0][j] = 0` for j > 0.
>   - Transition: if `s[i-1] == t[j-1]`: `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]` (use this char OR skip it).
>   - Else: `dp[i][j] = dp[i-1][j]` (must skip `s[i-1]`).

> [!note]- Python Solution
> ```python
> def num_distinct(s: str, t: str) -> int:
>     m, n = len(s), len(t)
>     # Space-optimized 1D DP (process j in reverse to avoid overwrite)
>     dp = [0] * (n + 1)
>     dp[0] = 1  # empty t matched by empty prefix
>
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
