---
module: striver-a2z/30-strings-advanced
lesson: 1
topic: String hashing (polynomial rolling hash, collisions, double hashing), Rabin-Karp, Z-function, KMP prefix function, separator tricks, borders and periods
source: https://takeuforward.org/learning/dsa/hashing-in-strings-theory?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet
tags: [striver, string, hashing, rolling-hash, rabin-karp, z-function, kmp, prefix-function, theory]
---
# 1. String Hashing and Pattern Matching

← [Part 30 index](README.md) · Next → [Reverse every word in a string](02-reverse-every-word-in-a-string.md)

> [!abstract] What this covers
> **Core idea:** Naive matching re-compares characters it has already seen, which costs O(n·m). Three tools avoid that and run in linear time:
> - A **rolling hash** turns each window into a number that updates in O(1) per slide.
> - The **Z-function** reuses the rightmost prefix match it has found.
> - The **KMP prefix function** falls back along *borders* instead of restarting.
>
> Glue the strings with a separator (`pat#text`, `s#rev(s)`) and the same three tools answer search, palindromic-prefix, border and period questions.
>
> **You'll be able to:** define and roll a polynomial hash without overflow or negative values; estimate collision risk and choose between verifying and double hashing; write the Z-algorithm and the prefix function from memory and explain why each is O(n); run KMP search; and read periods and borders off the `lps` array.
> **Source:** [Striver: Hashing in strings](https://takeuforward.org/learning/dsa/hashing-in-strings-theory?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet) · **Time:** 60 min

**Sections:** [1. Why naive matching is slow](#1-why-naive-matching-is-slow) · [2. Polynomial hash](#2-polynomial-hash) · [3. Rolling the window](#3-rolling-the-window) · [4. Prefix hashes and substring hashes](#4-prefix-hashes-and-substring-hashes) · [5. Collisions and double hashing](#5-collisions-and-double-hashing) · [6. Z-function](#6-z-function) · [7. KMP prefix function](#7-kmp-prefix-function) · [8. KMP search](#8-kmp-search) · [9. Separator tricks](#9-separator-tricks) · [10. Borders and periods](#10-borders-and-periods) · [11. Choosing a tool](#11-choosing-a-tool) · [12. Manacher](#12-manacher-all-palindromes-in-on) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Key terms](#key-terms) · [Flashcards](#flashcards)

---

## 1. Why naive matching is slow

Naive search tries every start `i` and compares `pat` character by character:

```
text = a a a a a a b      pat = a a a b
       ^ ^ ^ x             start 0: 3 matches, then fail
         ^ ^ ^ x           start 1: the same 3 characters compared again
```

The worst case is O(n·m), for example `text = aⁿ` and `pat = aᵐ⁻¹b`. Each linear algorithm reuses work in its own way:

| Algorithm | What it reuses | Worst case |
|---|---|---|
| Rabin-Karp | the previous window's hash | O(n·m) if everything collides; O(n + m) expected |
| Z-function | the rightmost prefix match `[l, r)` | O(n + m) |
| KMP | the longest border of the matched part | O(n + m) |

---

## 2. Polynomial hash

Treat the string as digits of a number in base `B`, reduced mod a prime `M`:

```
h(s) = s[0]·B^(m−1) + s[1]·B^(m−2) + … + s[m−1]·B^0   (mod M)
```

Compute it with Horner's rule: `h = (h·B + s[i]) mod M`.

| Choice | Typical value | Why |
|---|---|---|
| Character value | `ord(c)`, or `c − 'a' + 1` | Never map a character to **0**, or `"a"` and `"aa"` collide (both 0) |
| Base `B` | 31, 131, or random in `[256, M)` | Larger than the alphabet; random defeats adversarial (anti-hash) tests |
| Modulus `M` | `10⁹ + 7`, `998244353` | Prime, and `M² < 2⁶³`, so `h·B` fits in a 64-bit integer |

> [!tip] Overflow rule
> In C++/Java keep every value `< M` and multiply two values `< M` in `long long`/`long`. With `M ≈ 10⁹` the product is below `10¹⁸ < 9.2·10¹⁸`. Python has big integers but still needs `% M` to stay fast.

---

## 3. Rolling the window

To slide from `text[i..i+m−1]` to `text[i+1..i+m]`:

```
h_new = ( (h_old − text[i]·B^(m−1)) · B + text[i+m] )  mod M
         └ remove the leading digit ┘ └shift┘ └ add the new digit ┘
```

Precompute `pw = B^(m−1) mod M` once.

```python
def rabin_karp(text, pat, B=131, M=10**9 + 7):
    n, m = len(text), len(pat)
    if m > n:
        return []
    hp = ht = 0
    for i in range(m):
        hp = (hp * B + ord(pat[i])) % M
        ht = (ht * B + ord(text[i])) % M
    pw = pow(B, m - 1, M)
    res = []
    for i in range(n - m + 1):
        if hp == ht and text[i:i + m] == pat:   # verify: collisions are possible
            res.append(i)
        if i + m < n:
            ht = ((ht - ord(text[i]) * pw) * B + ord(text[i + m])) % M
    return res
```

> [!warning] Negative modulo
> In C++/Java, `(a − b) % M` is negative when `a < b`. Write `(ht − x·pw % M + M) % M` before multiplying. Python's `%` already returns a non-negative result.

---

## 4. Prefix hashes and substring hashes

When you need the hash of **any** substring, not just a sliding window, precompute prefix hashes:

```
H[0] = 0,   H[i+1] = H[i]·B + s[i]          (mod M)
P[0] = 1,   P[i+1] = P[i]·B                 (mod M)
hash(s[l..r)) = H[r] − H[l]·P[r − l]          (mod M)
```

With O(n) preprocessing, every substring comparison costs O(1). That unlocks:

| Problem | Use |
|---|---|
| Longest duplicate substring | Binary search the length; a set of window hashes finds a repeat |
| Longest palindromic prefix / suffix | Compare the forward hash with the hash of the reversed string |
| Count distinct substrings of length k | Set of window hashes |
| LCP of two suffixes | Binary search on the length with substring hashes, O(log n) per query |

---

## 5. Collisions and double hashing

Two different strings can share a hash. For a random base and a prime `M`, a **single** comparison of two distinct length-L strings collides with probability at most about `(L − 1)/M`, which is tiny.

The danger is **many** comparisons. Putting `k` hashes in a set gives about `k²/(2M)` expected colliding pairs (the birthday paradox):

| `k` hashes in a set | `M = 10⁹+7` | Two moduli (`M₁·M₂ ≈ 10¹⁸`) |
|---|---|---|
| 10³ | ~0.0005 | ≈ 0 |
| 10⁵ | **~5 collisions** | ~5·10⁻⁹ |

Three ways to stay correct:
1. **Verify on a hit.** Compare the characters whenever the hashes match. The output is exact, but adversarial input can make it O(n·m).
2. **Double hash.** Use two `(B, M)` pairs and compare the pair. Collisions become negligible, so you can skip verification.
3. **Random base.** Choose `B` at runtime so no fixed input can be built to break you.

> [!tip] Interview default
> Single hash plus verification for "find all occurrences". Double hash for "set of substrings" or "binary search + hashes", where verifying would be expensive.

---

## 6. Z-function

`z[i]` is the length of the longest common prefix of `s` and `s[i:]`. Set `z[0] = 0` by convention.

```
s  = a a b x a a b
z  = 0 1 0 0 3 1 0
```

The **Z-box** `[l, r)` is the matched window `s[l..r) == s[0..r−l)` that reaches furthest right. For each `i`:
- **`i ≥ r`:** nothing is known, so compare from scratch.
- **`i < r`:** `s[i..r)` equals `s[i−l..r−l)`, so `z[i] ≥ min(r − i, z[i − l])`. Start there and extend.
- If `i + z[i] > r`, move the box to `[i, i + z[i])`.

```python
def z_array(s):
    n = len(s)
    z = [0] * n
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

**Why it's O(n):** every successful comparison in the `while` loop moves `r` right, and `r` never exceeds `n`. Each `i` has at most one failing comparison.

**Search:** compute `z` of `pat + '#' + text`. The pattern starts at text index `i − m − 1` wherever `z[i] == m`. The separator caps `z` at `m`.

---

## 7. KMP prefix function

A **border** of a string is a proper prefix that is also a suffix. `lps[i]` (the prefix function `π[i]`) is the length of the longest border of `s[0..i]`.

```
s   = a a b a a a b
lps = 0 1 0 1 2 2 3
```

**Key fact:** the borders of `s[0..i]` are the borders of `s[0..i−1]` extended by `s[i]`. The borders of `s[0..i−1]`, longest first, form the chain `len → lps[len − 1] → lps[lps[len − 1] − 1] → … → 0`. So for each `i`, walk that chain until `s[len] == s[i]`:

```python
def compute_lps(s):
    lps = [0] * len(s)
    length = 0
    for i in range(1, len(s)):
        while length and s[i] != s[length]:
            length = lps[length - 1]        # next-shorter border
        if s[i] == s[length]:
            length += 1
        lps[i] = length
    return lps
```

**Why it's O(n):** `length` rises by at most 1 per `i`, and every fallback lowers it by at least 1. So there are at most `n` fallbacks in total.

```
i=5 in "aabaaab":  len=2 ("aa"), s[5]='a' vs s[2]='b' ✗
                   fall back: len = lps[1] = 1 ("a"), s[5]='a' vs s[1]='a' ✓ → len = 2
```

---

## 8. KMP search

Run the same loop over `text`, where `length` is how much of `pat` currently matches:

```python
def kmp_search(text, pat):
    lps, res, length = compute_lps(pat), [], 0
    for i, c in enumerate(text):
        while length and c != pat[length]:
            length = lps[length - 1]
        if c == pat[length]:
            length += 1
        if length == len(pat):
            res.append(i - len(pat) + 1)
            length = lps[length - 1]        # keep overlapping matches
    return res
```

The search runs in O(n + m) and never moves backwards in `text`, so it works on a **stream**. That is its practical edge over Z, which needs the concatenated string.

---

## 9. Separator tricks

Glue strings with a character that appears in neither, so no match can cross the join:

| Build | Read off | Answers |
|---|---|---|
| `pat + '#' + text` | positions where `z[i] == m`, or `lps[i] == m` | All occurrences of `pat` |
| `s + '#' + rev(s)` | `k = lps[last]` | Longest palindromic prefix → shortest palindrome by prepending `rev(s)[:n−k]` |
| `rev(s) + '#' + s` | `lps[last]` | Longest palindromic suffix → shortest palindrome by appending |
| `a + '#' + b` | `lps[last]` | Longest prefix of `a` that is a suffix of `b` |

> [!warning] Why the separator matters
> Without it, `s = "aaaa"` gives `s + rev(s) = "aaaaaaaa"` and `lps[last] = 7 > n`. The border spills over the join. `#` caps every border at the length of the first part.

---

## 10. Borders and periods

`p` is a **period** of `s` if `s[i] == s[i + p]` for every valid `i`. Borders and periods are two views of the same thing: `s` has a border of length `k` ⇔ `s` has period `n − k`.

| Question | Formula |
|---|---|
| Longest border (longest happy prefix) | `lps[n − 1]` |
| All borders | the chain `k = lps[n−1], lps[k−1], …` down to 0 |
| Smallest period | `p = n − lps[n − 1]` |
| Is `s` a repetition of a block (LC 459)? | `lps[n−1] > 0` and `n % p == 0` |
| Characters to append to make `s` periodic | `(p − n % p) % p` |
| Smallest period via Z | first `i` with `i + z[i] == n` (else `n`) |

```
s = abcabcab   lps[n−1] = 5   p = 3   8 % 3 ≠ 0 → not a full repetition
s = abcabc     lps[n−1] = 3   p = 3   6 % 3 = 0 → (abc)²
```

---

## 11. Choosing a tool

| Need | Pick | Why |
|---|---|---|
| One pattern, exact output, interview | **KMP** (or Z) | Deterministic O(n + m), short code |
| "Prefix match at every position" | **Z** | `z[i]` is exactly that quantity |
| Border, period, happy prefix | **Prefix function** | `lps[n − 1]` and its chain |
| Many patterns of the same length | **Rolling hash** | Pattern hashes in a set, one pass over the text |
| Arbitrary substring equality, binary search on length | **Prefix hashes** (double) | O(1) per comparison |
| Many different patterns at once | Aho-Corasick | Out of scope here; a trie + KMP failure links |
| Language built-in | `str.find` / `indexOf` | Fine in practice; know its worst case can be O(n·m) |

---

## 12. Manacher (all palindromes in O(n))

*Enrichment, not in the sheet.* Transform `s` to `t = "^#a#b#…#$"` so that every palindrome has odd length in `t`. `p[i]` is the palindrome radius at i in `t`. Keep the rightmost palindrome `[C − R, C + R]`:

```text
for i in 1..len(t)−2:
    mirror = 2C − i
    p[i] = (i < C + R) ? min(C + R − i, p[mirror]) : 0
    while t[i + p[i] + 1] == t[i − p[i] − 1]: p[i]++
    if i + p[i] > C + R: C = i, R = p[i]
```

- The longest palindrome in `s` has length `max p[i]`. It starts at `(i − p[i]) / 2` in `s`.
- The count of palindromic substrings is `Σ ceil(p[i] / 2)`.
- It runs in O(n) because R only moves right. In interviews, expand-around-centre at O(n²) ([Part 17](../17-strings-basic-medium/00-string-basics-theory.md)) is usually accepted. Mention Manacher as the follow-up.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Character mapped to 0 (`c − 'a'`) | Use `c − 'a' + 1` or `ord(c)` |
| Negative hash after subtracting (C++/Java) | Add `M` before the final `%` |
| `pw = B^m` in the roll | It's `B^(m−1)`, the weight of the leading character |
| `h·B` overflow | `M < 2³¹`, 64-bit arithmetic |
| Trusting a single hash in a big set | Double hash, or verify on hits |
| KMP fallback with `if` | It's a `while`: follow the whole border chain |
| Fallback to `lps[len]` | `lps[len − 1]` |
| Forgetting `length = lps[m − 1]` after a match | Otherwise overlapping matches are missed, or the code indexes out of bounds |
| Z without the `r − i` cap | `min(r − i, z[i − l])`; the copy is only valid inside the box |
| Separator that can appear in the input | Pick a character outside the alphabet (`#`, `$`, `\0`) |

---

## Practice

<details><summary>1. Compute the Z array of "aabxaab".</summary>

`[0, 1, 0, 0, 3, 1, 0]`.
- `z[1] = 1`: "a" matches, then 'b' ≠ 'a'.
- `z[4] = 3`: "aab" matches the prefix.
- `z[5]` starts inside the box `[4, 7)` at `min(2, z[1]) = 1`, and `s[6] = 'b'` ≠ `s[1] = 'a'` stops the extension, so it stays 1.
</details>

<details><summary>2. Compute lps of "abacaba". What are its borders and smallest period?</summary>

`lps = [0, 0, 1, 0, 1, 2, 3]`. The border chain is 3 ("aba") → `lps[2]` = 1 ("a") → 0. The smallest period is `7 − 3 = 4` ("abac"). Since `7 % 4 ≠ 0`, it isn't a full repetition.
</details>

<details><summary>3. Roll the hash with B = 10, M = 10⁹+7 over text "31415", window 3.</summary>

`h(314) = 314`. Roll with `pw = 10² = 100`:
- `(314 − 3·100)·10 + 1 = 141`
- `(141 − 1·100)·10 + 5 = 415`

Each window's hash is the window read as a number. That is the intuition behind the polynomial hash.
</details>

<details><summary>4. You put 10⁵ substring hashes (mod 10⁹+7) in a set. Is a single hash safe?</summary>

No. The birthday bound gives about `k²/(2M) ≈ 10¹⁰ / (2·10⁹) ≈ 5` expected colliding pairs. Use two moduli (about `10¹⁸` combined) or verify on hits.
</details>

<details><summary>5. Why does s + rev(s) without '#' break shortest palindrome?</summary>

For `s = "aa"`, `s + rev(s) = "aaaa"` and `lps[last] = 3`, more than `n = 2`. The prepend length `n − k` becomes negative. The separator caps `k ≤ n`.
</details>

<details><summary>6. Why does KMP set length = lps[m − 1] after a full match?</summary>

To keep **overlapping** matches. The suffix of the match that is also a prefix of `pat` may start the next match, as in `aaaa` / `aa`. Resetting to 0 would miss them, and leaving `length = m` would index `pat[m]` out of bounds.
</details>

<details><summary>7. Give an input where Rabin-Karp with verification degrades to O(n·m).</summary>

`text = aⁿ` and `pat = aᵐ`. Every window is a **true** match, so each one is verified in O(m). That cost is unavoidable when you report all matches by comparison. The real adversarial case is crafted collisions against a fixed `(B, M)`, which a random base prevents.
</details>

<details><summary>8. Is "abab" a repeated-block string? Is "aba"?</summary>

"abab": `lps[3] = 2`, `p = 2`, and `4 % 2 = 0`, so yes, it is (ab)². "aba": `lps[2] = 1`, `p = 2`, and `3 % 2 ≠ 0`, so no.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Polynomial (rolling) hash | String read as base-B digits mod M; slides in O(1) |
| Collision | Distinct strings with equal hashes |
| Double hashing | Two independent (B, M) pairs compared together |
| Z-function | `z[i]` = LCP of `s` and `s[i:]` |
| Z-box | Rightmost window `[l, r)` matching a prefix |
| Border | Proper prefix that is also a suffix |
| Prefix function / LPS | `lps[i]` = longest border of `s[0..i]` |
| Period | `p` with `s[i] = s[i + p]` for all valid `i`; equals `n − border` |
| Separator | Character outside the alphabet that stops matches crossing a join |

---

## Flashcards

**Polynomial hash formula?** #flashcard
h(s) = Σ s[i]·B^(m−1−i) mod M, computed by Horner: h = h·B + c.

**Rolling update?** #flashcard
h = ((h − out·B^(m−1))·B + in) mod M; add M first in C++/Java.

**Why never map a char to 0?** #flashcard
Leading zero digits vanish, so "a" and "aa" would hash equal.

**Substring hash from prefix hashes?** #flashcard
H[r] − H[l]·P[r − l] mod M.

**Birthday risk for k hashes?** #flashcard
≈ k²/(2M) collisions; 10⁵ hashes mod 10⁹ ≈ 5, so double hash.

**Define z[i].** #flashcard
Length of the longest common prefix of s and s[i:].

**Z-box start value?** #flashcard
z[i] = min(r − i, z[i − l]) when i < r, then extend.

**Why is the Z-algorithm linear?** #flashcard
Each successful comparison moves r right; r ≤ n.

**Define lps[i].** #flashcard
Longest proper prefix of s[0..i] that is also a suffix of it.

**KMP fallback?** #flashcard
while s[i] != s[len]: len = lps[len − 1].

**After a KMP match?** #flashcard
Record i − m + 1, set len = lps[m − 1].

**Shortest palindrome trick?** #flashcard
k = lps[last] of s + '#' + rev(s); answer rev(s)[:n − k] + s.

**Smallest period?** #flashcard
p = n − lps[n − 1]; a full repetition iff lps[n−1] > 0 and n % p == 0.

**KMP vs Z?** #flashcard
Same power; KMP streams the text, Z directly gives the prefix match at every index.

**Interview track →** [String algorithms deep-dive](../../02-algorithms/02-string-algorithms.md) · [String algorithm walkthroughs](../../04-practice/algorithms/02-string-algorithms.md)
