---
module: 02-algorithms
topic: String Algorithms
tags: [algorithms, string, kmp, rabin-karp, z-algorithm, manacher]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)
## First-Principles Map

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Highly probable; know the core patterns cold.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Know it conceptually; skip deep implementation.

> [!warning] L3 scope note
> **Expand-around-center and rolling hash are the only two you must be able to write cold.** KMP and Z are "explain the idea, derive if pushed." Manacher and suffix arrays are `💤 T3` — recognize the name, state the complexity, move on. Reaching for Manacher when expand-around-center passes the constraints is a negative signal, not a positive one.

```text
WHY String Algorithms exist
├── Naive substring search is O(n·m) — recompares characters already known to match
│   ├── After a mismatch, the naive shift throws away everything learned from the partial match
│   └── The pattern's own self-similarity predicts how far it is safe to shift
WHAT they are
├── Preprocessing the PATTERN to skip redundant comparisons
│   ├── KMP        — failure function: longest proper prefix that is also a suffix
│   └── Z-function — for each i, length of longest substring at i matching a prefix of s
├── Hashing the WINDOW so comparison is O(1)
│   └── Rabin-Karp — rolling polynomial hash, updated in O(1) per shift
└── Exploiting SYMMETRY around centers
    ├── Expand-around-center — O(n²), the expected L3 answer
    └── Manacher — O(n), reuses mirror information across centers
HOW they work
├── KMP: build lps[] in O(m), scan text once — on mismatch jump to lps[j-1], never rewind text
├── Z:   build z[] in O(n) via a [l, r] window; concat pattern + '#' + text to search
├── Rabin-Karp: hash(next) = (hash(cur) - s[l]·base^(m-1))·base + s[r]; verify on hash hit
└── Manacher: insert '#' separators to make every palindrome odd-length, then mirror-reuse
WHEN to use
├── "find pattern in text", single pattern            → KMP or Z (both O(n+m))
├── "longest duplicate/repeated substring"            → binary search on length + rolling hash
├── "any anagram/permutation of p in s"               → sliding window + freq counts, not KMP
├── "longest palindromic substring"                   → expand-around-center; Manacher only if pushed
├── "shortest palindrome by prepending"               → KMP lps on s + '#' + reverse(s)
└── "count distinct substrings"                       → suffix array/trie `💤 T3`
WHAT can go wrong
├── Rolling hash without verification → false positives on collision; always confirm the match
├── Single modulus hash → adversarial anti-hash tests; use double hashing or a random base
├── KMP lps off-by-one: lps[i] is a length, and the fallback is lps[j-1] not lps[j]
├── Manacher written from memory under pressure → high bug rate for near-zero payoff at L3
└── Reaching for KMP when a hashmap/sliding window solves it in fewer lines
DECISION
├── Fixed pattern, need O(n+m) worst case          → KMP (deterministic, no collisions)
├── Multiple patterns / substring-set membership   → rolling hash or trie
├── Palindromes                                    → expand-around-center first, always
└── Constraint n ≤ 1000 → O(n²) passes; do not over-engineer
```

## First-Principles Breakdown

- **Root problem**: Locate or count structure inside a string faster than comparing every position against every offset.
- **Core insight**: A string's own prefix/suffix self-similarity tells you how far you can safely shift after a mismatch — the pattern encodes its own skip table. Hashing attacks the same problem from the other side: make each comparison O(1) instead of reducing the number of comparisons.
- **Invariant (KMP)**: `lps[i]` = length of the longest proper prefix of `pat[0..i]` that is also a suffix of it. The text pointer never moves backward, which is what buys O(n+m).
- **Why it works**: Each character of the text is examined a constant number of times amortized — the failure-function fallback total is bounded by the number of increments, so the scan is linear.
- **Where it breaks**: Hashing is probabilistic — without verifying a hash hit against the actual characters, collisions produce wrong answers. And all of these lose to a plain hashmap when the problem is really about character *counts* rather than character *order*.

---

# String Algorithms

```
[STRING ALGORITHMS — MINDMAP]
├── WHY IT EXISTS
│   └── Naive search re-compares known-matching characters → O(n·m)
├── PREPROCESS THE PATTERN
│   ├── KMP — failure function lps[]        O(n+m), deterministic
│   └── Z-function — prefix-match lengths   O(n+m), often simpler to derive
├── HASH THE WINDOW
│   └── Rabin-Karp — rolling hash           O(n+m) expected, verify on hit
├── EXPLOIT SYMMETRY
│   ├── Expand around center                O(n²)  ← the L3 answer
│   └── Manacher                            O(n)   ← 💤 T3
└── HEAVY MACHINERY (💤 T3 — name only)
    ├── Suffix array / suffix automaton
    └── Aho-Corasick (multi-pattern)
```

## The Four Techniques

| Technique | Preprocess | Search | Space | When it's the right call |
|---|---|---|---|---|
| **Expand around center** | — | O(n²) | O(1) | Any palindrome question. Start here. |
| **Rabin-Karp** `⚡ T1` | O(m) | O(n+m) exp. | O(1) | Duplicate substrings, binary-search-on-length |
| **KMP** `🎯 T2` | O(m) | O(n) | O(m) | Single-pattern search, worst-case guarantee |
| **Z-function** `🎯 T2` | O(n) | O(n) | O(n) | Same as KMP; easier to reconstruct live |
| **Manacher** `💤 T3` | — | O(n) | O(n) | Only when asked "better than O(n²)?" |

---

## KMP — the failure function

The one idea: after matching `j` characters and then failing, you do not restart at `j = 0`. You restart at `lps[j-1]` — the longest proper prefix of what you matched that is also a suffix of it, because that prefix is already aligned.

```python
def build_lps(pat):
    lps = [0] * len(pat)
    length = 0
    i = 1
    while i < len(pat):
        if pat[i] == pat[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]   # fall back, do NOT reset to 0
        else:
            lps[i] = 0
            i += 1
    return lps
```

**Derivation to say out loud:** "`lps[i]` answers — if I've matched up to `i` and the next character fails, what's the longest already-matched prefix I can keep? That's the longest border of `pat[0..i]`."

**The classic bug:** falling back to `lps[j]` instead of `lps[j-1]`, or resetting `length = 0` on mismatch instead of cascading through the fallback chain.

---

## Rabin-Karp — rolling hash

Hash a window, slide it, update in O(1). This is the technique most worth real fluency at L3, because it unlocks *binary search on answer length*.

```python
def rolling_hashes(s, m, base=257, mod=(1 << 61) - 1):
    h = 0
    for c in s[:m]:
        h = (h * base + ord(c)) % mod
    yield h
    power = pow(base, m - 1, mod)
    for i in range(m, len(s)):
        h = ((h - ord(s[i - m]) * power) * base + ord(s[i])) % mod
        yield h
```

**Always verify.** A hash match is a *candidate*, not a match — compare the actual substrings before accepting, or use double hashing (two independent moduli) if verification is too expensive.

**The pattern that pays off:** "longest duplicate substring" — binary search the length `L`, and for each `L` ask "does any hash repeat?" via a set. Monotone (if length `L` repeats, so does `L-1`), so binary search is valid → O(n log n).

---

## Z-function

`z[i]` = length of the longest substring starting at `i` that matches a prefix of `s`. Same power as KMP, and most people find it easier to re-derive under pressure.

```python
def z_function(s):
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
```

**To search:** build `z` over `pattern + '#' + text`; any `z[i] == len(pattern)` marks an occurrence. The `'#'` must not appear in either string.

---

## Palindromes — start at the center

Expand-around-center is the expected answer. `2n-1` centers (n odd, n-1 even), expand while characters match.

**Only mention Manacher if the interviewer explicitly asks for sub-quadratic.** State the idea — transform with `#` separators so all palindromes are odd-length, then reuse mirror information within the current rightmost palindrome — and offer to write it. Volunteering it unprompted signals poor calibration far more often than it signals depth.

---

## Decision Guide

| Prompt | Reach for | Not |
|---|---|---|
| "Find all occurrences of `p` in `s`" | KMP or Z | Manacher |
| "Longest duplicate substring" | Binary search + rolling hash | Suffix array |
| "Longest palindromic substring" | Expand around center | Manacher (unless pushed) |
| "Shortest palindrome by prepending" | KMP lps on `s + '#' + rev(s)` | Brute force |
| "Any permutation of `p` inside `s`" | Sliding window + counts | KMP |
| "Is `t` an anagram of `s`" | Counter comparison | Any of the above |
| "Count distinct substrings" | Suffix trie/array `💤 T3` | — |

> [!tip] The most common mistake
> Pattern-matching on the word "string" and reaching for KMP. Most Google string questions are really **hashmap, sliding-window, or two-pointer** questions wearing a string costume. Check those three first — if a frequency map solves it, KMP is the wrong answer even though it "works."

---

Practice → [`coding/algorithms/02-string-algorithms.md`](../coding/algorithms/02-string-algorithms.md) (tier-tagged walkthroughs)

---

## Flashcards

**What does `lps[i]` actually mean in KMP, and why does it make matching linear?** #flashcard
The length of the longest proper prefix of `pattern[:i+1]` that is also a suffix of it. On a mismatch you jump to `lps[j-1]` instead of restarting, so the text pointer never moves backwards — O(N+M) total.

**"Longest proper prefix that is also a suffix" — what is the one-line answer?** #flashcard
`lps[-1]` from the KMP failure function. Building the LPS array *is* the whole problem (Longest Happy Prefix); no search phase needed.

**Shortest Palindrome: add minimum chars to the front of `s`. What is the trick?** #flashcard
Run KMP on `s + '#' + reverse(s)`. The final LPS value is the length of the longest palindromic *prefix* of `s`; reverse the remaining suffix and prepend it. The `'#'` separator is mandatory — without it the border can straddle the join and overcount.

**Rabin-Karp: what is the failure mode, and how do you handle it?** #flashcard
Hash collisions give false positives, so a hash match must be confirmed by an actual string comparison. Use a large prime modulus (e.g. `10**9 + 7`) and a random base to make adversarial collisions unlikely; worst case degrades to O(NM).

**Longest Duplicate Substring is O(N log N) — what makes binary search valid here?** #flashcard
Monotonicity: if a duplicate of length `L` exists, duplicates of every length `< L` also exist. So binary search the length and use Rabin-Karp with a hash set to test each candidate in O(N).

**Palindromes: when do you expand-around-center vs. reach for Manacher's?** #flashcard
Expand-around-center is O(N²) and is the correct L3 answer — 2N-1 centers, handling odd and even lengths separately. Manacher's is O(N) but `💤 T3`: mention it exists, don't write it under time pressure.

**Substring search shows up in an interview. When is KMP the wrong instinct?** #flashcard
When the question is about *anagrams or permutations* rather than exact order (Permutation in String) — that is a sliding window with a frequency map. KMP matches an exact sequence; it cannot express "same multiset, any order."

---

## See Also

[[string]] | [[sliding-window]] | [[trie]] | [[hashing]] | [[dynamic-programming]]
