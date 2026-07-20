---
module: 01-data-structures
topic: String
tags: [data-structures, string]
---

← [Data structures index](./README.md) · [DS decision tree](./ds_tree.md)
## First-Principles Map

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.


```
WHY string algorithms exist → WHAT strings are → HOW they work → WHEN to use → WHAT can go wrong
       │                             │                  │               │               │
  [Naive substring search         [immutable array    [sliding window: [pattern match,  [O(n×m) naive
   is O(n×m); many problems        of characters;      two pointers    anagram detect,  search TLEs on
   reduce to string matching,      encoding matters    over chars;     palindrome,      large inputs;
   palindromes, anagrams —         (ASCII vs UTF-8     hashing for     longest without  off-by-one in
   need specialized techniques]    affects indexing)]  rolling hash;   repeat, KMP/     two-pointer
                                                        KMP failure     Rabin-Karp]     window updates]
       │                             │                  │
  [real-world:                    [invariant:         [KMP: precompute failure
   grep, DNA sequence               string index is    function (proper prefix = suffix)
   matching, search engine          byte offset not    to skip O(m) work on mismatch;
   autocomplete]                    char offset in     Rabin-Karp: rolling hash O(1)
                                    multibyte]         slide; Z-function: O(n) prefix match]
       ↓
[Decision: String technique vs alternatives]
  ├── vs Trie          → trie for prefix/dictionary queries; sliding window for substrings
  ├── vs KMP vs Rabin-Karp → KMP O(n+m) worst case; R-K O(n) avg but hash collision risk
  └── vs Suffix Array  → suffix array for all substring queries; KMP for single pattern match
```

## First-Principles Breakdown
- **Root problem**: Naive pattern matching checks all O(n×m) positions; string problems need O(n) or O(n+m) techniques.
- **Core insight**: Precompute structure (KMP failure function, rolling hash, Z-array) to avoid redundant comparisons on mismatch — reuse already-matched information.
- **Invariant**: In a valid sliding window, the window contains exactly the characters satisfying the constraint; expanding/shrinking maintains the invariant.
- **Why it's fast**: KMP's failure function means each character is processed at most twice total — O(n+m) not O(n×m); rolling hash updates in O(1) per slide.
- **Where it breaks**: Multibyte encodings (UTF-8) make character indexing non-trivial; rolling hash has collision probability; KMP's failure function precomputation is easy to implement incorrectly.

# Strings — Data Structure Deep-Dive

```
[STRINGS (DATA STRUCTURE) — MINDMAP]
├── WHY IT EXISTS
│   ├── Problem it solves: represent and manipulate ordered sequences of characters — the most common interview input type
│   ├── Alphabet structure (finite σ) unlocks optimizations impossible on generic arrays
│   └── Analogy: string is a 1-D array with a fixed alphabet — every array technique applies, plus character-specific ones
├── WHAT IT IS (First Principles)
│   ├── Core definition: contiguous array of characters; indexable in O(1); immutable in Python/Java
│   ├── Immutability consequence: s + t creates a new object → O(N) per concatenation → use list + ''.join()
│   ├── Substring s[i:j]: O(j-i) in Python (copy); O(1) view possible in C++ with string_view
│   └── Character encoding: ASCII (128), Extended ASCII (256), Unicode (21-bit code points, UTF-8 variable-byte)
├── HOW IT WORKS — CORE TECHNIQUES
│   ├── Frequency Array / Counter
│   │   ├── 26-bucket array for lowercase letters: freq[c - 'a']++
│   │   ├── Replaces hash map for alphabet-bounded problems — O(1) space (constant 26 or 128)
│   │   └── Anagram check: compare two freq arrays in O(1) after O(N) build
│   ├── Two Pointers on Strings
│   │   ├── Palindrome check: l=0, r=len-1; move inward comparing s[l] and s[r]
│   │   └── Reverse / partition in-place: swap s[l] and s[r] — works only on mutable string (char array)
│   ├── Sliding Window
│   │   ├── Fixed window: maintain freq of window; slide by adding right char, removing left char
│   │   └── Variable window: expand right until constraint violated; shrink left to restore
│   ├── Prefix Hashing (Rolling Hash)
│   │   ├── Precompute hash[i] = hash of s[0..i-1] using polynomial base and mod prime
│   │   ├── Substring hash in O(1): hash(s[l..r]) = (hash[r+1] - hash[l] * pow[r-l+1]) mod prime
│   │   └── Use: check substring equality in O(1) — enables O(N) duplicate detection
│   ├── Palindrome Techniques
│   │   ├── Expand around center: O(N²) — check both odd (center=i) and even (center=i,i+1) cases
│   │   ├── DP table dp[i][j] = True if s[i..j] is palindrome: O(N²) time and space
│   │   └── Manacher: O(N) — insert '#' sentinels, exploit symmetry of already-computed radii
│   └── String DP
│       ├── LCS (Longest Common Subsequence): dp[i][j] = LCS of s1[:i] and s2[:j] — O(N·M)
│       ├── Edit Distance: dp[i][j] = min ops to convert s1[:i] to s2[:j] — O(N·M)
│       └── Longest Palindromic Subsequence: LCS(s, reverse(s)) — O(N²)
├── COMPLEXITY SUMMARY
│   ├── Frequency array build: O(N) | compare: O(σ) = O(1) for fixed alphabet
│   ├── Sliding window (fixed/variable): O(N)
│   ├── Rolling hash build: O(N) | substring query: O(1)
│   ├── Expand-around-center palindrome: O(N²)
│   ├── String DP (LCS, edit distance): O(N·M)
│   └── Concatenation in loop: O(N²) — always use join
├── WHEN TO USE
│   ├── Signal: "anagram / permutation check" → freq array or Counter comparison
│   ├── Signal: "longest substring with at most K distinct chars" → sliding window + hash map
│   ├── Signal: "check if s2 contains a permutation of s1" → sliding window + freq array
│   ├── Signal: "longest palindromic substring" → expand-around-center or Manacher
│   ├── Signal: "minimum window substring" → variable sliding window
│   ├── Signal: "edit distance / longest common subsequence" → 2D DP
│   └── Avoid freq array when: alphabet is not fixed/small — use hash map instead
└── COMMON MISTAKES / GOTCHAS
    ├── Concatenation in loop: O(N²) — always accumulate in list then join
    ├── Palindrome even-length: must check both (i,i) and (i,i+1) centers — missing one gives wrong answer
    ├── Sliding window character removal: decrement freq before or after moving left pointer determines correctness
    ├── Unicode pitfall: len("😀") == 1 in Python (code points) but 4 bytes in UTF-8 — differs by language
    ├── Prefix hash overflow: in languages with fixed-width ints, always apply mod to avoid overflow
    └── LCS vs edit distance: LCS counts matches; edit distance counts operations — different recurrences
```

## Mental Model

A string is an **immutable array of characters**. Every array technique applies — two pointers, sliding window, prefix sum (on char frequencies). The extra surface area comes from the alphabet structure: 26 lowercase letters → frequency arrays replace hash maps; character relationships (anagram, palindrome, subsequence) define most problem classes.

**Complexity at a glance**

| Operation | Time | Notes |
|-----------|------|-------|
| Access char at index | O(1) | Direct index |
| Substring (Python) | O(k) | k = length of slice |
| Concatenation in loop | O(n²) | Use `"".join(list)` instead |
| String comparison | O(n) | Character by character |
| Sort characters | O(n log n) | Or O(n) with counting sort |




---

## Core Properties

**Immutability (Python/Java):** Strings cannot be modified in-place. Every `s += c` creates a new string object → O(n²) in a loop. Always build into a list and `"".join()` at the end.

**Character frequency array:** For lowercase a–z, a `freq = [0] * 26` array is faster and cleaner than a dict. Index with `ord(c) - ord('a')`.

**Sliding window is the dominant technique.** Most substring problems → variable-size window. Most subarray problems that happen to be strings → same playbook.

---

## Key Patterns

### 1. Frequency Map / Anagram Check

**Trigger:** "same characters", "anagram", "permutation exists in string"

```python
from collections import Counter

def is_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)

# Sliding window anagram check — O(n)
def find_anagrams(s: str, p: str) -> list[int]:
    need = Counter(p)
    window = Counter()
    result = []
    left = 0
    for right, c in enumerate(s):
        window[c] += 1
        if right - left + 1 > len(p):
            lc = s[left]
            window[lc] -= 1
            if window[lc] == 0:
                del window[lc]
            left += 1
        if window == need:
            result.append(left)
    return result
```

### 2. Two Pointers — Palindrome / Reverse

**Trigger:** "palindrome", "reverse", "symmetric"

```python
def is_palindrome(s: str) -> bool:
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum(): l += 1
        while l < r and not s[r].isalnum(): r -= 1
        if s[l].lower() != s[r].lower(): return False
        l += 1; r -= 1
    return True

def longest_palindrome_expand(s: str) -> str:
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return s[l+1:r]
    best = ""
    for i in range(len(s)):
        for sub in (expand(i, i), expand(i, i+1)):  # odd, even
            if len(sub) > len(best): best = sub
    return best
```

### 3. Sliding Window — Substring with Constraint

**Trigger:** "longest substring without", "minimum window", "at most K distinct"

```python
def length_of_longest_substring(s: str) -> int:
    freq = {}
    left = best = 0
    for right, c in enumerate(s):
        freq[c] = freq.get(c, 0) + 1
        while freq[c] > 1:          # window invalid
            lc = s[left]
            freq[lc] -= 1
            if freq[lc] == 0: del freq[lc]
            left += 1
        best = max(best, right - left + 1)
    return best

def min_window_substring(s: str, t: str) -> str:
    need = Counter(t)
    have, total = {}, len(need)
    formed = 0
    left = 0
    best = (float('inf'), 0, 0)
    for right, c in enumerate(s):
        have[c] = have.get(c, 0) + 1
        if c in need and have[c] == need[c]:
            formed += 1
        while formed == total:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            lc = s[left]
            have[lc] -= 1
            if lc in need and have[lc] < need[lc]:
                formed -= 1
            left += 1
    return s[best[1]:best[2]+1] if best[0] != float('inf') else ""
```

### 4. Prefix Sum on Characters

**Trigger:** "number of substrings with exactly K vowels/distinct chars"

```python
# Substrings with sum == k (binary string, treat 0→-1)
def num_subarrays_with_sum(s: str, goal: int) -> int:
    prefix = {0: 1}
    total = count = 0
    for c in s:
        total += int(c)
        count += prefix.get(total - goal, 0)
        prefix[total] = prefix.get(total, 0) + 1
    return count
```

### 5. String Hashing — Duplicate / Equal Substrings

**Trigger:** "find duplicate substring", "longest duplicate substring", "repeated pattern"

```python
# Check if substring of length L exists twice — O(n)
def has_duplicate_of_length(s: str, L: int) -> bool:
    seen = set()
    for i in range(len(s) - L + 1):
        sub = s[i:i+L]
        if sub in seen: return True
        seen.add(sub)
    return False
```

---

## Canonical Problems

| Problem | Pattern | Key Insight |
|---------|---------|-------------|
| Valid Anagram | Frequency map | Counter(s) == Counter(t) |
| Group Anagrams | Frequency map + grouping | sorted(word) as key |
| Longest Substring Without Repeat | Sliding window | shrink when freq[c] > 1 |
| Minimum Window Substring | Sliding window + frequency | two counters: need vs have |
| Find All Anagrams in String | Sliding window fixed | fixed-size window, compare counters |
| Longest Palindromic Substring | Expand around center | O(n²); Manacher's for O(n) |
| Palindromic Substrings (count) | Expand around center | count both odd and even expansions |
| Encode/Decode Strings | Delimiter encoding | length-prefix: "4#word" |
| Longest Repeating Char Replacement | Sliding window | window valid if len - max_freq ≤ k |
| String to Integer (atoi) | Parsing | handle sign, overflow, non-digits |

---

## Common Mistakes

- **`s += c` in a loop** — O(n²). Use `chars = []; chars.append(c); "".join(chars)`.
- **Case sensitivity** — always `s.lower()` before comparing unless the problem is case-sensitive.
- **Unicode vs ASCII** — `ord(c) - ord('a')` only valid for lowercase a–z; use `Counter` for general case.
- **Off-by-one in substrings** — `s[l:r]` excludes `r`; `s[l:r+1]` includes it.
- **Palindrome check skipping non-alphanumeric** — use `isalnum()` and `lower()` together.

---

# Advanced String Algorithms

```
[STRINGS (ALGORITHMS) — MINDMAP]
├── WHY IT EXISTS
│   ├── Problem it solves: efficient search, match, and transform operations over character sequences
│   ├── Naive matching is O(N·M) — unacceptable for large texts; algorithms cut this to O(N+M)
│   └── Analogy: a string is a 1-D array with an alphabet constraint — that constraint is the key to all optimizations
├── WHAT IT IS (First Principles)
│   ├── Core definition: ordered sequence of characters over a finite alphabet Σ
│   ├── Immutability (Python/Java): concatenation creates a new object → O(N) per concat → use StringBuilder/join
│   ├── Key properties
│   │   ├── Substring: contiguous slice s[i..j]
│   │   ├── Subsequence: non-contiguous characters preserving order
│   │   └── Prefix / Suffix: special substrings anchored at start / end
│   └── Alphabet size matters: 26 → freq arrays; 128 → ASCII array; arbitrary → hash map
├── HOW IT WORKS
│   ├── KMP (Knuth-Morris-Pratt)
│   │   ├── Build failure function (LPS array): lps[i] = length of longest proper prefix of pattern[0..i] that is also suffix
│   │   ├── Match phase: mismatch → jump via lps, never rewind text pointer
│   │   └── Time: O(N+M) | Space: O(M)
│   ├── Rabin-Karp (Rolling Hash)
│   │   ├── Hash pattern; slide hash over text in O(1) per step using polynomial rolling hash
│   │   ├── Collision → verify character by character
│   │   ├── Power: find multiple patterns simultaneously (multi-hash)
│   │   └── Time: O(N+M) average, O(N·M) worst | Space: O(1)
│   ├── Z-Algorithm
│   │   ├── Z[i] = length of longest substring starting at i that matches a prefix of s
│   │   ├── Pattern search: concat pattern + '$' + text; Z[i] == len(pattern) → match
│   │   └── Time: O(N+M) | Space: O(N+M)
│   ├── Manacher's Algorithm
│   │   ├── Finds ALL palindromic substrings in O(N) — classic O(N²) DP is insufficient at L3
│   │   ├── Transform: insert '#' between characters to unify odd/even cases
│   │   └── P[i] = radius of palindrome centered at i; exploit symmetry to skip recomputation
│   ├── Suffix Array + LCP
│   │   ├── Suffix array: sorted order of all suffixes — built in O(N log N) or O(N)
│   │   ├── LCP array: longest common prefix between adjacent suffixes in sorted order
│   │   └── Enables: longest repeated substring, number of distinct substrings, pattern search — all O(N log N)
│   └── Trie-based Matching
│       └── Build trie of patterns + failure links (like KMP but for a set of patterns)
├── COMPLEXITY SUMMARY
│   ├── Naive pattern match: O(N·M)
│   ├── KMP / Z / Rabin-Karp: O(N+M)
│   ├── Manacher: O(N)
│   ├── Suffix array build: O(N log N) or O(N)
├── WHEN TO USE
│   ├── Signal: "does pattern P occur in text T?" → KMP (single pattern, linear guaranteed)
│   ├── Signal: "longest palindromic substring" → Manacher or expand-around-center O(N²)
│   ├── Signal: "repeated substring / longest common substring" → suffix array + LCP
│   ├── Signal: "rolling / sliding window over string with hash" → Rabin-Karp
│   ├── Signal: "anagram / permutation in string" → sliding window + freq array
└── COMMON MISTAKES / GOTCHAS
    ├── String concatenation in loop: O(N²) — always use list + join or StringBuilder
    ├── KMP lps build: off-by-one in the mismatch branch (lps[len-1], not lps[len])
    ├── Unicode vs ASCII: len() counts code points, not bytes — matters for emoji / CJK
    ├── Palindrome even/even: expand-around-center needs TWO starting positions (i,i) and (i,i+1)
    ├── Rabin-Karp collision: always verify on hash match — never skip verification
    └── Suffix array indexing: SA[i] is the start index of the i-th lexicographically smallest suffix
```

Arrays of characters with immutability constraints. L3 expects: KMP for O(N+M) pattern matching, rolling hash for multi-pattern problems, Manacher awareness, and production-grade handling of Unicode and concatenation cost.

---

## Theory & Mental Models

**What it is.** Strings are immutable sequences of characters with rich algorithmic structure — pattern matching, palindrome detection, anagram grouping, and compression. Core invariant: most string algorithms reduce to "find a structure in the character sequence" — a window, a prefix, a suffix, or a pattern.

**Why it exists.** Naive pattern matching is O(N × M); KMP achieves O(N + M) by precomputing the failure function (LPS) so the text pointer never backtracks. Rolling hash computes string hashes in O(1) per shift. These optimizations matter at scale: searching for patterns in gigabyte log streams requires sub-linear methods.

**The mental model.** Strings are arrays with character semantics. The key insight per problem type: pattern matching → KMP / Rabin-Karp; palindrome → expand from center (2N-1 centers); anagram detection → frequency tuple as hash key; sliding window → expand right until valid, shrink left to minimize; subsequence vs substring — non-contiguous vs contiguous (these are different problems).

**Complexity at a glance.**

| Algorithm | Preprocessing | Search | Space |
| :--- | :--- | :--- | :--- |
| Naive | O(1) | O(N × M) | O(1) |
| KMP | O(M) LPS | O(N) | O(M) |
| Rabin-Karp | O(M) hash | O(N) avg | O(1) |
| Z-algorithm | O(N + M) | O(N + M) | O(N + M) |
| Manacher | O(N) | — | O(N) |
| Sliding window | O(1) | O(N) | O(alphabet) |

**When to reach for it.**
- Pattern matching (single pattern, no preprocessing budget) → KMP.
- Palindrome detection (contiguous) → expand from center O(N²) or Manacher O(N).
- Anagram grouping → sorted key or 26-count frequency tuple as hash key.
- Minimum window containing all characters of T → sliding window with `have`/`required` counters.
- Prefix/suffix structure (trie for word routing, Z-array for pattern search).

**When NOT to use it.**
- The "string" is really a number sequence — treat as array, not string (different algorithms apply).
- Concatenating strings in a loop — O(N²) in Python/Java; use `''.join(parts)` or `StringBuilder`.

**Common mistakes.**
- Python string immutability: concatenation in a loop is O(N²) — always use list accumulation + `''.join()`.
- KMP LPS off-by-one: `lps[length - 1]` on mismatch, not `lps[length]`; `lps[0]` is always 0.
- Not handling Unicode vs ASCII — 26-char frequency array breaks for Unicode; use `Counter` or dict.
- Confusing substring (contiguous, sliding window) with subsequence (non-contiguous, DP on two strings).

---

## 1. Concept Overview

**Problem space**: Pattern matching (KMP, Rabin-Karp), longest palindromic substring (expand or Manacher), anagram detection (hash/count), sliding window (min window substring), DP (LCS, edit distance), parsing (valid number, decode string).

---

## 2. Core Algorithms & Click Moments

### KMP — O(N+M) Pattern Matching

> [!IMPORTANT]
> **The Click Moment**: "Find **all occurrences** of pattern P in text T" — OR — "implement `strStr()`" — OR — "**repeated string match** (how many copies of A needed to contain B?)". KMP's key insight: when a mismatch occurs, the LPS (Longest Proper Prefix which is also Suffix) array tells you how far to "shift" the pattern without re-scanning the text.

```python
def build_lps(pattern: str) -> list[int]:
    n = len(pattern)
    lps = [0] * n
    length = 0  # length of previous longest border
    i = 1
    while i < n:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]  # fall back without incrementing i
        else:
            lps[i] = 0
            i += 1
    return lps

def kmp_search(text: str, pattern: str) -> list[int]:
    if not pattern:
        return list(range(len(text) + 1))
    lps = build_lps(pattern)
    matches = []
    i = j = 0  # i = text index, j = pattern index
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1; j += 1
        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and text[i] != pattern[j]:
            if j:
                j = lps[j - 1]
            else:
                i += 1
    return matches
```

#### Common Variants & Twists
1. **Shortest Palindrome**:
   - **What (The Problem & Goal):** Add minimum characters to the front of a string to make it a palindrome.
   - **How (Intuition & Mental Model):** Create a new string `s + '#' + reverse(s)`. Find the LPS value of the last character. This value is the length of the longest palindromic prefix of the original string. The characters to add are the remaining suffix of the reversed string.
2. **Repeated Substring Pattern**:
   - **What (The Problem & Goal):** Check if a string can be constructed by repeating a substring.
   - **How (Intuition & Mental Model):** If a string `s` of length `n` has a repeated pattern, then `n % (n - lps[n-1]) == 0` and `lps[n-1] > 0`. Alternatively, check if `s` is in `(s + s)[1:-1]`.
```

> [!CAUTION]
> **LPS off-by-one**: The LPS table uses **0-indexed** access (`lps[length - 1]`, not `lps[length]`). This is the most common KMP implementation bug. Also: `lps[0]` is always 0 (no proper prefix of length 1 can also be a suffix).

---
```

### Rabin-Karp — Rolling Hash

> [!IMPORTANT]
> **The Click Moment**: "Find pattern in text — **simpler implementation** than KMP acceptable" — OR — "**multiple patterns** to match simultaneously" — OR — "**Longest Duplicate Substring** (binary search + rolling hash)". Rolling hash updates the window hash in O(1) using the previous hash.

```python
def rabin_karp(text: str, pattern: str) -> list[int]:
    n, m = len(text), len(pattern)
    if m > n:
        return []
    BASE, MOD = 31, 10**9 + 7
    POW = pow(BASE, m - 1, MOD)

    def char_val(c: str) -> int:
        return ord(c) - ord('a') + 1

    pat_hash = 0
    win_hash = 0
    for i in range(m):
        pat_hash = (pat_hash * BASE + char_val(pattern[i])) % MOD
        win_hash = (win_hash * BASE + char_val(text[i])) % MOD

    matches = []
    if win_hash == pat_hash and text[:m] == pattern:
        matches.append(0)

    for i in range(1, n - m + 1):
        win_hash = (win_hash - char_val(text[i-1]) * POW) % MOD
        win_hash = (win_hash * BASE + char_val(text[i+m-1])) % MOD
        win_hash = (win_hash + MOD) % MOD  # ensure non-negative
        if win_hash == pat_hash and text[i:i+m] == pattern:
            matches.append(i)
    return matches
```

#### Common Variants & Twists
1. **Longest Duplicate Substring**:
   - **What (The Problem & Goal):** Find the longest substring that appears at least twice.
   - **How (Intuition & Mental Model):** Binary search on the length `L`. For each `L`, use Rabin-Karp to find if any hash is duplicated (using a set of hashes).
2. **Distinct Echo Substrings**:
   - **What (The Problem & Goal):** Find the number of distinct substrings that can be written as `a + a`.
   - **How (Intuition & Mental Model):** Iterate through all possible lengths `L` of `a`. For each `L`, slide a window and check if `hash(s[i:i+L]) == hash(s[i+L:i+2L])`.
```

> [!CAUTION]
> **Hash collisions**: Always verify `text[i:i+m] == pattern` on hash match — rolling hash can produce false positives. For security-critical applications (e.g., anti-plagiarism), use **double hashing** (two independent hash functions) to reduce collision probability to ~1/p₁×p₂.

---
```

### Longest Palindromic Substring — Expand from Center

> [!IMPORTANT]
> **The Click Moment**: "Longest **palindromic substring**" (must be contiguous) — OR — "expand to find palindromes". Expand around each center: `2N-1` centers (N for odd-length, N-1 for even-length palindromes). O(N²) — often the expected solution.

```python
def longest_palindromic_substring(s: str) -> str:
    if not s:
        return ""
    start = end = 0

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1; right += 1
        return left + 1, right - 1  # last valid palindrome bounds

    for i in range(len(s)):
        l1, r1 = expand(i, i)      # odd length
        l2, r2 = expand(i, i + 1)  # even length
        if r1 - l1 > end - start:
            start, end = l1, r1
        if r2 - l2 > end - start:
            start, end = l2, r2

    return s[start:end+1]
```

#### Common Variants & Twists
1. **Palindrome Partitioning II**:
   - **What (The Problem & Goal):** Find the minimum cuts needed to partition a string into palindromes.
   - **How (Intuition & Mental Model):** Use DP where `dp[i]` is the min cuts for `s[:i]`. To optimize, use the "Expand from Center" idea to find all palindromes and update `dp[right+1] = min(dp[right+1], dp[left] + 1)`.
2. **Count Palindromic Substrings**:
   - **What (The Problem & Goal):** Count total number of palindromic substrings.
   - **How (Intuition & Mental Model):** Standard "Expand from Center". For each center, increment count for every valid palindrome found during expansion.
```

> [!TIP]
> **Manacher's Algorithm** (O(N)): Uses a `radius` array and a "rightmost palindrome" invariant to reuse previously computed radii. State it as an O(N) alternative: "Manacher's achieves O(N) using the fact that palindrome radii are symmetric around the center of the rightmost palindrome." For L3, knowing the idea and complexity is sufficient — full implementation is rarely required.

---
```

### Sliding Window — Minimum Window Substring

> [!IMPORTANT]
> **The Click Moment**: "Find the **smallest substring** containing all characters of T" — OR — "**window** satisfying a character count constraint". Expand right until valid (`have == required`), then shrink left to minimize the window.

```python
from collections import Counter

def min_window_substring(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = Counter(t)
    have, required = 0, len(need)
    window: dict[str, int] = {}
    best = ""
    best_len = float('inf')
    left = 0
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            have += 1
        while have == required:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best = s[left:right+1]
            lch = s[left]
            window[lch] -= 1
            if lch in need and window[lch] < need[lch]:
                have -= 1
            left += 1
    return best
```

#### Common Variants & Twists
1. **Longest Substring with At Most K Distinct Characters**:
   - **What (The Problem & Goal):** Find the length of the longest substring with `<= k` distinct characters.
   - **How (Intuition & Mental Model):** Sliding window with a frequency map. Expand `right`. If `len(map) > k`, shrink `left` until `len(map) == k`.
2. **Permutation in String**:
   - **What (The Problem & Goal):** Check if `s2` contains a permutation of `s1`.
   - **How (Intuition & Mental Model):** This is a fixed-size sliding window of length `len(s1)`. Compare the character frequency map of the window with that of `s1`.
```

> [!CAUTION]
> **`have` tracks frequency saturation, not total count**: `have` increments only when `window[ch] == need[ch]` (exactly met), not when `window[ch] >= need[ch]`. This correctly handles characters that appear multiple times in T — you need exactly `need[ch]` of each, not more.

---
```

### Z-Algorithm — Global Pattern Matching

> [!IMPORTANT]
> **The Click Moment**: "Build LPS table alternative" — OR — "find all occurrences of P in T using linear space" — OR — "string matching where preprocessing must be on the concatenated string". Z[i] = length of longest substring starting at i that matches a prefix of the string.

```python
def z_function(s: str) -> list[int]:
    n = len(s)
    z = [0] * n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z

def z_search(text: str, pattern: str) -> list[int]:
    combined = pattern + '$' + text  # '$' is a sentinel not in the alphabet
    z = z_function(combined)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] == m]
```

#### Common Variants & Twists
1. **Longest Happy Prefix**:
   - **What (The Problem & Goal):** Find the longest proper prefix that is also a suffix.
   - **How (Intuition & Mental Model):** This is exactly what the last value of the LPS array in KMP tells you. Alternatively, use the Z-algorithm: the answer is the largest `Z[i]` such that `i + Z[i] == len(s)`.
```

---
```

### Trie (Prefix Tree) — Fast Prefix Matching

> [!IMPORTANT]
> **The Click Moment**: "Find all words starting with **prefix**" — OR — "search for a word character-by-character" — OR — "Word Search II (DFS on grid + Trie)". A Trie optimizes prefix lookups to O(L) where L is word length, drastically outperforming hash sets for prefix queries.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
        
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word
        
    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

#### Common Variants & Twists
1. **Map Sum Pairs**:
   - **What (The Problem & Goal):** Implement a map that supports `insert(key, val)` and `sum(prefix)` (sum of values of all keys starting with `prefix`).
   - **How (Intuition & Mental Model):** In each Trie node, store the sum of values of all keys passing through that node. On `insert`, update the delta along the path.
2. **Stream of Characters**:
   - **What (The Problem & Goal):** Given a stream of characters, check if any suffix of the stream is a word in a given dictionary.
   - **How (Intuition & Mental Model):** Insert words into the Trie **in reverse**. Keep the last `max_word_length` characters of the stream and search in the Trie starting from the most recent character.
```

---
```

## 3. Pattern Matching Quick Reference

| Algorithm | Preprocessing | Search | Space | Best For |
| :--- | :--- | :--- | :--- | :--- |
| Naive | O(1) | O(N×M) | O(1) | Very short patterns; one-off search |
| KMP | O(M) LPS | O(N) | O(M) | Single pattern; streaming |
| Rabin-Karp | O(M) hash | O(N) avg | O(1) | Multiple patterns; probabilistic |
| Boyer-Moore | O(M + Σ) | O(N/M) best | O(M + Σ) | Long patterns; practical fastest |

> [!NOTE]
> Aho-Corasick multi-pattern matching and Suffix Arrays are **L4+ / competitive programming** topics. Know they exist but don't spend time implementing them for L3.

---

## 4. Common Interview Problems

### Easy
- **Valid Palindrome `🎯 T2`** — Two pointers; skip non-alphanumeric; compare `lower()`.
- **Valid Anagram `🎯 T2`** — `Counter(s) == Counter(t)` or sort both.
- **Longest Common Prefix** — Vertical scan or binary search on length.

### Medium
- **Longest Substring Without Repeating Chars** — Sliding window + last-seen index map.
- **Longest Palindromic Substring `🎯 T2`** — Expand from center; O(N²).
- Group Anagrams — `sorted(word)` or 26-count tuple as key.
- **Find All Anagrams in String** — Fixed-size sliding window + counter comparison.
- **Encode and Decode Strings `🎯 T2`** — Length-prefixed encoding: `f"{len(s)}#{s}"`.
- **Longest Palindromic Subsequence `🎯 T2`** — DP or LCS with `reversed(s)`.

### Hard
- Minimum Window Substring — Sliding window + `have`/`required` count logic.
- **Edit Distance `🎯 T2`** — 2D DP; space-optimize to 1D rolling array.
- **Implement strStr() (KMP)** — Build LPS; scan without backtracking text pointer.
- **Regular Expression Matching** — 2D DP; handle `*` = zero or more of preceding.
- **Wildcard Matching** — DP; `*` matches any sequence including empty.
- **Distinct Subsequences `🎯 T2`** — Count ways to form T as subsequence of S.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Longest Palindromic Substring `🎯 T2`** | Expand Around Center | "Longest contiguous palindrome" | Expand around each of 2N-1 centers | Even-length palindromes need `expand(i, i+1)` — don't only check `expand(i, i)`. |
| **Longest Palindromic Subsequence `🎯 T2`** | "Longest non-contiguous palindrome" | DP or `LCS(s, reversed(s))` | Subsequence ≠ substring; LCS reduction is the cleanest approach. |
| **Min Window Substring** | "Smallest window containing all of T" | Expand right; shrink left while `have==required` | `have` tracks saturation (== need[ch]), not total count. Unicode: use full Counter, not 26-char array. |
| **Substring with Concatenation** | "Window containing all words exactly once" | Fixed word-length window; multiset word comparison | Multiple occurrences of same word require multiset, not set. O(N×W×K) with rolling word-hash. |
| **Group Anagrams `⚡ T1`** | "Same letters, different order" | Key = `sorted(s)` or 26-count tuple | 26-array fails for Unicode; `sorted` O(K log K) vs count O(K). |
| **Valid Parenthesis String** | "`*` can be `(`, `)`, or empty" | Greedy range `[lo, hi]` of possible open-count | `lo = max(0, lo-1)` (can't go negative); `hi` increases on `*`. |
| **Valid Anagram `🎯 T2`** [E] | "Same multiset of chars" | `Counter(s) == Counter(t)` or 26-count array | Unicode: use Counter, not fixed 26-array. |
| **Decode String** [M] | "Nested `k[...]` expansion" | Stack of `(built_string, repeat_k)`; push on `[`, pop+expand on `]` | Multi-digit k: parse full number before `[`. |
| **KMP strStr** | "First occurrence of needle in haystack" | Build LPS; scan text without backtracking text pointer | LPS `length = lps[length-1]` on mismatch — not `length -= 1`. |
| **Repeated String Match** | "Minimum copies of A to contain B" | Build `A * ceil(len(B)/len(A)) + 1`; KMP/find | At most `ceil(len(B)/len(A)) + 1` copies suffice — prove bound. |
| **Edit Distance `🎯 T2`** | "Min ops to convert word1 to word2" | 2D DP; `dp[i][j]` from 3 neighbors | Initialize `dp[0][j]=j` and `dp[i][0]=i`; space-optimize to 1D with `prev` diagonal. |
| **Distinct Subsequences `🎯 T2`** | "Ways to form T as subsequence of S" | `dp[i][j]` = count ways for `s[:i]` containing `t[:j]` | Mod by large prime for large inputs; base case `dp[i][0]=1` (empty T always 1 way). |
| **Valid Palindrome `🎯 T2`** [E] | "Ignore non-alphanumeric; check palindrome" | Two pointers; `isalnum()` skip; compare `lower()` | `''.join(c.lower() for c in s if c.isalnum())` then `== reversed` is also clean. |
| **Reverse Words in a String** [E] | "Reverse word order, single spaces, no leading/trailing" | `' '.join(reversed(s.split()))` in Python | In-place without split: reverse entire string, then reverse each word. |
| **Longest Common Prefix** [E] | "Prefix shared by all strings" | Sort lexicographically; compare only first and last | Only need to compare extremes after sort — all others are bounded by these two. |
| **String to Integer (atoi)** [M] | "Parse integer with sign, overflow, invalid chars" | Skip whitespace; read sign; accumulate digits; stop on non-digit; clamp to [INT_MIN, INT_MAX] | Test: leading spaces, sign-only, overflow, empty string, non-digit prefix. |
| **Count and Say** [M] | "RLE encoding applied iteratively" | Expand each sequence by counting consecutive runs | Use `itertools.groupby` or two-pointer; off-by-one when counting final group. |
| **Longest Repeating Character Replacement `⚡ T1`** [M] | "Max window where replacing ≤ K chars makes it uniform" | Sliding window; track `max_freq` in window; `window_size - max_freq > K` → shrink | `max_freq` never decreases — we only care about windows larger than current best. |
| **Minimum Remove to Make Valid Parentheses** [M] | "Remove min chars to balance parentheses" | Stack of unmatched `(` indices; set of unmatched `)` indices; remove both | Convert string to list; remove indices from set; join remainder. |
| **Longest Substring Without Repeating Characters `⚡ T1`** [M] | "Max length window with all unique chars" | Sliding window with set or last-seen map; shrink `left` on duplicate | Map approach: `left = max(left, last_seen[c] + 1)` — jump past duplicate directly. |
| **Find All Anagrams in a String `⚡ T1`** [M] | "All start indices where substring is anagram of p" | Fixed-size sliding window; frequency array comparison | Compare full frequency arrays each step is O(26) = O(1) — not O(N). |
| **Palindromic Substrings** [M] | "Count all palindromic substrings" | Expand around every center (N single + N-1 double centers) | Total O(N²) centers; Manacher's O(N) for follow-up — know it exists. |
| **Word Search `⚡ T1`** [M] | "Find word in 2D board via adjacent cells" | DFS with in-place visited marking (replace with `#`); restore after | Mark before recursing — not after; otherwise you might revisit within one DFS path. |
| **Wildcard Matching** [H] | "Pattern match with `?` (any char) and `*` (any sequence)" | 2D DP; `*` can match zero (`dp[i][j-1]`) or one-more (`dp[i-1][j]`) | Unlike regex, `*` here matches any sequence directly (not "zero or more of preceding"). |
| **Regular Expression Matching** [H] | "Match with `.` and `*`; `*` means zero-or-more of preceding" | `dp[i][j]`: match char/dot; `*` = zero occurrences `dp[i][j-2]` or consume one `dp[i-1][j]` | `*` zero occurrences is the tricky case: skip pattern char + `*` with `dp[i][j-2]`. |

---

## Quick Revision Triggers

- "Find pattern P in text T efficiently" → KMP, O(N+M); build LPS array first.
- "Check if two strings are anagrams / find all anagram windows" → sliding window with frequency map, O(N).
- "Longest palindromic substring" → Manacher O(N) or expand-around-center O(N²); never O(N³) brute force.
- "Find repeated substring / detect substring hash collisions" → Rabin-Karp rolling hash, O(N+M) expected.
- "Minimum window containing all characters of T" → sliding window with two pointers and character count.
- "Build result string by repeated concatenation in a loop" → use `''.join(list)` not `s += char` (O(N²) vs O(N)).
- "Search for MANY patterns in one text" → Trie + DFS (L3 approach) or Aho-Corasick awareness.
- "Strings compared with `is` give wrong results" → always use `==`; `is` checks identity, not value.

---



## See also

- [array.md](./01-array.md) — sliding window and two pointers on numeric arrays
- [hashing.md](./02-hashing.md) — frequency maps, group-by-key
- [trie.md](./09-trie.md) — prefix dictionary, word search II
- [stack.md](./05-stack.md) — decode string, parenthesis parsing
- [03-patterns/patterns-master.md](../03-patterns/patterns-master.md) — string pattern triggers

---

## Flashcards

**Why is building a string using `s += char` inside a loop inefficient in Python, and what is the optimal O(N) alternative?** #flashcard
Strings in Python are immutable. Doing `s += char` copies the entire string at each step, resulting in a total time complexity of $O(N^2)$. The optimal alternative is to append characters to a list and join them at the end: `''.join(char_list)`.

**What is the canonical key representation to group anagrams in a hash map, and what are the time complexity differences?** #flashcard
- **Sorted string key**: Key is `tuple(sorted(s))` (or `"".join(sorted(s))`). Time: $O(N \cdot L \log L)$ where $L$ is the string length.
- **Char count tuple**: Key is a 26-element tuple containing counts of each letter. Time: $O(N \cdot L)$, which is faster for long strings.

**What is the difference in sliding window state-tracking between checking for "longest substring without repeating characters" vs "minimum window substring"?** #flashcard
- **Longest substring**: Track character indices in a map. Jump the left pointer `left = max(left, char_idx[ch] + 1)` on duplicates.
- **Minimum window `⚡ T1`**: Maintain a frequency target `need` and current count `window`. Increment a `have` tracker when `window[ch] == need[ch]` and expand/shrink based on `have == len(need)`.

**How do you find the longest palindromic substring in O(N^2) time and O(1) space, and what are the two centers to consider?** #flashcard
Iterate through the string and treat each index as a center. Expand outward while characters match. You must expand from two distinct centers at each index $i$:
1. **Odd-length center**: `expand(i, i)`
2. **Even-length center**: `expand(i, i+1)`


**Find pattern P in text T efficiently — what technique, and why?** #flashcard
KMP, O(N+M); build LPS array first.

**Check if two strings are anagrams / find all anagram windows — what technique, and why?** #flashcard
sliding window with frequency map, O(N).

**Longest palindromic substring — what technique, and why?** #flashcard
Manacher O(N) or expand-around-center O(N²); never O(N³) brute force.

**Find repeated substring / detect substring hash collisions — what technique, and why?** #flashcard
Rabin-Karp rolling hash, O(N+M) expected.

**Minimum window containing all characters of T — what technique, and why?** #flashcard
sliding window with two pointers and character count.

**Build result string by repeated concatenation in a loop — what technique, and why?** #flashcard
use `''.join(list)` not `s += char` (O(N²) vs O(N)).

**Strings compared with `is` give wrong results — what technique, and why?** #flashcard
always use `==`; `is` checks identity, not value.
