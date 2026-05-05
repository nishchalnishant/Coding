# Strings — SDE-3 Gold Standard

Arrays of characters with immutability constraints. SDE-3 expects: KMP for O(N+M) pattern matching, rolling hash for multi-pattern problems, Manacher awareness, and production-grade handling of Unicode and concatenation cost.

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
- Multiple pattern matching simultaneously → Aho-Corasick.
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

#### Common Variants & Twists
1. **Palindrome Partitioning II**:
   - **What (The Problem & Goal):** Find the minimum cuts needed to partition a string into palindromes.
   - **How (Intuition & Mental Model):** Use DP where `dp[i]` is the min cuts for `s[:i]`. To optimize, use the "Expand from Center" idea to find all palindromes and update `dp[right+1] = min(dp[right+1], dp[left] + 1)`.
2. **Count Palindromic Substrings**:
   - **What (The Problem & Goal):** Count total number of palindromic substrings.
   - **How (Intuition & Mental Model):** Standard "Expand from Center". For each center, increment count for every valid palindrome found during expansion.
```

> [!TIP]
> **Manacher's Algorithm** (O(N)): Uses a `radius` array and a "rightmost palindrome" invariant to reuse previously computed radii. State it as an O(N) alternative: "Manacher's achieves O(N) using the fact that palindrome radii are symmetric around the center of the rightmost palindrome." For SDE-3, knowing the idea and complexity is sufficient — full implementation is rarely required.

---

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

#### Common Variants & Twists
1. **Longest Happy Prefix**:
   - **What (The Problem & Goal):** Find the longest proper prefix that is also a suffix.
   - **How (Intuition & Mental Model):** This is exactly what the last value of the LPS array in KMP tells you. Alternatively, use the Z-algorithm: the answer is the largest `Z[i]` such that `i + Z[i] == len(s)`.
```

---

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

#### Common Variants & Twists
1. **Map Sum Pairs**:
   - **What (The Problem & Goal):** Implement a map that supports `insert(key, val)` and `sum(prefix)` (sum of values of all keys starting with `prefix`).
   - **How (Intuition & Mental Model):** In each Trie node, store the sum of values of all keys passing through that node. On `insert`, update the delta along the path.
2. **Stream of Characters**:
   - **What (The Problem & Goal):** Given a stream of characters, check if any suffix of the stream is a word in a given dictionary.
   - **How (Intuition & Mental Model):** Insert words into the Trie **in reverse**. Keep the last `max_word_length` characters of the stream and search in the Trie starting from the most recent character.
```

---

## 3. SDE-3 Deep Dives

### Scalability: Streaming Pattern Matching

> [!TIP]
> For pattern matching over a **continuous data stream** (log ingestion, network packets):
> - **KMP** is naturally streaming: maintain state `j` (position in pattern) across chunks. When a chunk arrives, continue the KMP scan from the saved `j` — no need to re-process previous data. O(chunk_size) per chunk.
> - **Rabin-Karp** is also streaming: maintain the rolling hash across chunk boundaries. The last `m-1` characters of each chunk must be prepended to the next chunk for correct window computation.
>
> For **multi-pattern streaming** (thousands of patterns): **Aho-Corasick automaton** — build a trie of all patterns with failure links; scan text once in O(N + M) total where M = sum of pattern lengths. Used in antivirus engines, network intrusion detection (Snort), and content moderation.

### Scalability: Suffix Arrays for Large-Scale Text

> [!TIP]
> For **longest repeated substring**, **substring search across multiple queries**, or **text compression**:
> - **Suffix array** + **LCP array** gives O(N log N) build, O(log N) per query.
> - **Suffix automaton** gives O(N) build and O(N) total size for all suffixes — used in Google's text indexing.
>
> In competitive programming: longest duplicate substring = binary search on length + rolling hash (O(N log N)); suffix array gives exact O(N log N) or O(N) with SA-IS.

### Concurrency: String Immutability and StringBuilder

> [!CAUTION]
> **String concatenation in a loop is O(N²)** in languages where strings are immutable (Python, Java, JavaScript). Each `s += part` creates a new string object — N concatenations of total length L take O(L²) time. Use:
> - Python: `''.join(parts)` — O(N) total.
> - Java: `StringBuilder.append()` — amortized O(1) per append.
> - JavaScript: `Array.join('')` — O(N) total.
>
> This is a frequent Google interview performance trap — mention it proactively.

### Trade-offs: Pattern Matching Algorithms

| Algorithm | Preprocessing | Search | Space | Best For |
| :--- | :--- | :--- | :--- | :--- |
| Naive | O(1) | O(N×M) | O(1) | Very short patterns; one-off search |
| KMP | O(M) LPS | O(N) | O(M) | Single pattern; streaming |
| Rabin-Karp | O(M) hash | O(N) avg | O(1) | Multiple patterns; probabilistic |
| Aho-Corasick | O(Σ patterns) trie | O(N + matches) | O(Σ patterns) | Many patterns simultaneously |
| Boyer-Moore | O(M + Σ) | O(N/M) best | O(M + Σ) | Long patterns; practical fastest |
| Suffix Array | O(N log N) | O(M log N) | O(N) | Many queries on same text |

---

## 4. Common Interview Problems

### Easy
- **Valid Palindrome** — Two pointers; skip non-alphanumeric; compare `lower()`.
- **Valid Anagram** — `Counter(s) == Counter(t)` or sort both.
- **Longest Common Prefix** — Vertical scan or binary search on length.

### Medium
- **Longest Substring Without Repeating Chars** — Sliding window + last-seen index map.
- **Longest Palindromic Substring** — Expand from center; O(N²).
- [Group Anagrams](problem-deep-dives.md#group-anagrams) — `sorted(word)` or 26-count tuple as key.
- **Find All Anagrams in String** — Fixed-size sliding window + counter comparison.
- **Encode and Decode Strings** — Length-prefixed encoding: `f"{len(s)}#{s}"`.
- **Longest Palindromic Subsequence** — DP or LCS with `reversed(s)`.

### Hard
- [Minimum Window Substring](problem-deep-dives.md#minimum-window-substring) — Sliding window + `have`/`required` count logic.
- **Edit Distance** — 2D DP; space-optimize to 1D rolling array.
- **Implement strStr() (KMP)** — Build LPS; scan without backtracking text pointer.
- **Regular Expression Matching** — 2D DP; handle `*` = zero or more of preceding.
- **Wildcard Matching** — DP; `*` matches any sequence including empty.
- **Distinct Subsequences** — Count ways to form T as subsequence of S.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Longest Palindromic Substring** | Expand Around Center | "Longest contiguous palindrome" | Expand around each of 2N-1 centers | Even-length palindromes need `expand(i, i+1)` — don't only check `expand(i, i)`. |
| **Longest Palindromic Subsequence** | "Longest non-contiguous palindrome" | DP or `LCS(s, reversed(s))` | Subsequence ≠ substring; LCS reduction is the cleanest approach. |
| **[Min Window Substring](problem-deep-dives.md#minimum-window-substring)** | "Smallest window containing all of T" | Expand right; shrink left while `have==required` | `have` tracks saturation (== need[ch]), not total count. Unicode: use full Counter, not 26-char array. |
| **Substring with Concatenation** | "Window containing all words exactly once" | Fixed word-length window; multiset word comparison | Multiple occurrences of same word require multiset, not set. O(N×W×K) with rolling word-hash. |
| **[Group Anagrams](problem-deep-dives.md#group-anagrams)** | "Same letters, different order" | Key = `sorted(s)` or 26-count tuple | 26-array fails for Unicode; `sorted` O(K log K) vs count O(K). |
| **Valid Parenthesis String** | "`*` can be `(`, `)`, or empty" | Greedy range `[lo, hi]` of possible open-count | `lo = max(0, lo-1)` (can't go negative); `hi` increases on `*`. |
| **KMP strStr** | "First occurrence of needle in haystack" | Build LPS; scan text without backtracking text pointer | LPS `length = lps[length-1]` on mismatch — not `length -= 1`. |
| **Repeated String Match** | "Minimum copies of A to contain B" | Build `A * ceil(len(B)/len(A)) + 1`; KMP/find | At most `ceil(len(B)/len(A)) + 1` copies suffice — prove bound. |
| **[Edit Distance](problem-deep-dives.md#edit-distance)** | "Min ops to convert word1 to word2" | 2D DP; `dp[i][j]` from 3 neighbors | Initialize `dp[0][j]=j` and `dp[i][0]=i`; space-optimize to 1D with `prev` diagonal. |
| **Distinct Subsequences** | "Ways to form T as subsequence of S" | `dp[i][j]` = count ways for `s[:i]` containing `t[:j]` | Mod by large prime for large inputs; base case `dp[i][0]=1` (empty T always 1 way). |
| **Valid Palindrome** [E] | "Ignore non-alphanumeric; check palindrome" | Two pointers; `isalnum()` skip; compare `lower()` | `''.join(c.lower() for c in s if c.isalnum())` then `== reversed` is also clean. |
| **Reverse Words in a String** [E] | "Reverse word order, single spaces, no leading/trailing" | `' '.join(reversed(s.split()))` in Python | In-place without split: reverse entire string, then reverse each word. |
| **Longest Common Prefix** [E] | "Prefix shared by all strings" | Sort lexicographically; compare only first and last | Only need to compare extremes after sort — all others are bounded by these two. |
| **String to Integer (atoi)** [M] | "Parse integer with sign, overflow, invalid chars" | Skip whitespace; read sign; accumulate digits; stop on non-digit; clamp to [INT_MIN, INT_MAX] | Test: leading spaces, sign-only, overflow, empty string, non-digit prefix. |
| **Count and Say** [M] | "RLE encoding applied iteratively" | Expand each sequence by counting consecutive runs | Use `itertools.groupby` or two-pointer; off-by-one when counting final group. |
| **Longest Repeating Character Replacement** [M] | "Max window where replacing ≤ K chars makes it uniform" | Sliding window; track `max_freq` in window; `window_size - max_freq > K` → shrink | `max_freq` never decreases — we only care about windows larger than current best. |
| **Minimum Remove to Make Valid Parentheses** [M] | "Remove min chars to balance parentheses" | Stack of unmatched `(` indices; set of unmatched `)` indices; remove both | Convert string to list; remove indices from set; join remainder. |
| **Longest Substring Without Repeating Characters** [M] | "Max length window with all unique chars" | Sliding window with set or last-seen map; shrink `left` on duplicate | Map approach: `left = max(left, last_seen[c] + 1)` — jump past duplicate directly. |
| **Find All Anagrams in a String** [M] | "All start indices where substring is anagram of p" | Fixed-size sliding window; frequency array comparison | Compare full frequency arrays each step is O(26) = O(1) — not O(N). |
| **Palindromic Substrings** [M] | "Count all palindromic substrings" | Expand around every center (N single + N-1 double centers) | Total O(N²) centers; Manacher's O(N) for follow-up — know it exists. |
| **Word Search** [M] | "Find word in 2D board via adjacent cells" | DFS with in-place visited marking (replace with `#`); restore after | Mark before recursing — not after; otherwise you might revisit within one DFS path. |
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
- "Strings compared with `is` give wrong results" → always use `==`; `is` checks identity, not value.

---

## See also

- [Array](../data-structures/array.md) — sliding window on arrays applies identically to strings
- [Hashing](../data-structures/hashing.md) — frequency maps for anagram detection; rolling hash
- [Dynamic Programming](dynamic-programming/README.md) — LCS, edit distance, LPS
- [Patterns Master](../../../reference/patterns/patterns-master.md) — string pattern recognition triggers
