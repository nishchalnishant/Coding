---
module: 01-data-structures
topic: String
subtopic: 
status: unread
tags: [data-structures, string]
---

← [Data structures index](./README.md) · [DS decision tree](./ds_tree.md)
## First-Principles Map

> [!abstract] Amazon SDE-2 Priority Legend
> `⚡ T1` — **Must Master**: High-frequency Amazon problems. Do not move on until these are reflexive.
> `🎯 T2` — **Build Fluidity**: Know the pattern cold; minor edge cases matter less.
> `💤 T3` — **Awareness Only**: Not expected at SDE-2. Know what it does; skip deep implementation.


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

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click moment | Core logic | Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Valid Anagram `🎯 T2`** | Frequency map | Same multiset of chars | `Counter(s) == Counter(t)` or 26-count array | Unicode: use Counter, not fixed 26-array. |
| **Group Anagrams `⚡ T1`** | Hash by canonical key | Same letters → same key | Key = `tuple(sorted(w))` or 26-count tuple | Sort key is O(k log k); count tuple is O(k). |
| **Longest Substring Without Repeat** | Sliding window | Shrink while duplicate | `while c in seen: left++`; update max | Store **last index** of char to jump `left` in O(1). |
| **Minimum Window Substring `⚡ T1`** | Window + frequency | Expand until valid; shrink while valid | Track `have` vs `need` per char, not total count | Empty `t` or impossible → return `""`. |
| **Find All Anagrams `⚡ T1`** | Fixed window | Window size = len(p) | Compare frequency maps each step | Use 26-array diff count for O(1) compare. |
| **Longest Palindromic Substring `🎯 T2`** | Expand around center | Every center → expand | O(n²) expand; Manacher O(n) stretch | Check **odd and even** centers. |
| **Longest Repeating Char Replacement** | Window + max freq | Valid if `len - max_freq <= k` | Track max frequency **in current window** | max_freq can decrease when shrinking — still correct for max **length**. |
| **Decode String** | Stack | Push context on `[` | Stack of `(built, repeat_k)` | Multi-digit k: parse full number before `[`. |
| **String to Integer (atoi)** | Parsing | Sign → digits → clamp overflow | Stop at first non-digit; clamp to 32-bit | Leading spaces and lone `'+'` / `'-'`. |

More walkthroughs: [problem-deep-dives.md](../02-algorithms/problem-deep-dives.md). String **algorithms** (KMP, Rabin-Karp detail): [string.md](../02-algorithms/string.md) in `02-algorithms/`.

---

## Quick Revision Triggers

- If the problem is **substring / subarray with constraint** → sliding window (variable or fixed size).
- If the problem is **anagram or same multiset** → frequency map or sorted/canonical key.
- If the problem is **palindrome `🎯 T2`** → expand around center (O(n²)) unless asked for O(n) (Manacher).
- If the problem is **pattern in text, many queries** → KMP or Rabin-Karp; **many patterns** → trie / Aho-Corasick ([trie.md](./trie.md)).
- If you need **O(1) char lookup in window** → array of size 26 or hash map; sliding window fails on **negative numbers** in numeric arrays — use prefix sum ([array.md](./array.md)).
- If building strings in a loop → **list + join**, never `s += c` in Python.

---

## See also

- [array.md](./array.md) — sliding window and two pointers on numeric arrays
- [hashing.md](./hashing.md) — frequency maps, group-by-key
- [trie.md](./trie.md) — prefix dictionary, word search II
- [stack.md](./stack.md) — decode string, parenthesis parsing
- [02-algorithms/string.md](../02-algorithms/string.md) — KMP, Rabin-Karp, Z-function
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

