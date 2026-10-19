---
module: striver/17-strings-basic-medium
lesson: 0
topic: String fundamentals — representation, immutability and builder costs, character arithmetic, frequency tables, parsing, palindromes, substring enumeration, balance counters
source: https://takeuforward.org/learning/dsa/remove-outermost-parentheses?category=basic-and-easy-string-problems&source=strivers-a2z-dsa-sheet
tags: [striver, strings, theory, parsing, palindrome, frequency]
---
# 0. String Fundamentals

← [Part 17 index](README.md) · Next → [Remove Outermost Parentheses](01-remove-outermost-parentheses.md)

> [!abstract] What this covers
> **Core idea:** A string is an array of characters with two extra traps: **immutability** (repeated concatenation silently costs O(n²)) and a **small alphabet**, which makes a 26- or 128-slot array the right hash table. Most medium string problems combine five moves: frequency tables, two pointers, expand-around-centre, a balance counter and careful parsing.
> **You'll be able to:** build strings in O(n) in each language; do character arithmetic safely; write an overflow-safe atoi; enumerate substrings with incremental state; and solve palindrome and parentheses-depth problems with the right invariant.
> **Source:** enrichment for the [Strings category](https://takeuforward.org/learning/dsa/remove-outermost-parentheses?category=basic-and-easy-string-problems&source=strivers-a2z-dsa-sheet). The problems in this part, and [Basic Strings](../11-basic-strings/README.md), apply each move. · **Time:** 40 min

**Sections:** [1. Representation and costs](#1-representation-and-costs) · [2. Character arithmetic](#2-character-arithmetic) · [3. Frequency tables](#3-frequency-tables) · [4. Parsing](#4-parsing) · [5. Balance counters](#5-balance-counters) · [6. Palindromes](#6-palindromes) · [7. Substring enumeration](#7-substring-enumeration) · [8. Comparing and rotating](#8-comparing-and-rotating) · [9. Where the advanced tools live](#9-where-the-advanced-tools-live)

---

## 1. Representation and costs

| Language | Type | Mutable? | Build efficiently with | Trap |
|---|---|---|---|---|
| C++ | `std::string` | ✓ | `s += c`, `s.push_back(c)` (amortised O(1)), `reserve` | `s = s + c` copies, giving O(n²); `substr` is O(len) |
| Java | `String` | ✗ | `StringBuilder.append`, then `toString()` | `+=` in a loop is O(n²); `==` compares references, so use `equals` |
| Python | `str` | ✗ | collect parts in a list, then `"".join(parts)` | `s += c` in a loop is O(n²) in the worst case; slicing copies |

- Slices and `substr` cost O(length). A loop that calls `s.substr(i, k)` n times is O(nk), not O(n).
- Comparing two strings costs O(min length).
- Hashing a string key costs O(L). So "map of strings" operations are O(L), not O(1).

---

## 2. Character arithmetic

| Need | Expression |
|---|---|
| Letter index 0..25 | `c - 'a'` (Python: `ord(c) - 97`) |
| Digit value | `c - '0'` |
| Upper ↔ lower | `c ^ 32` for ASCII letters, or `tolower`/`toupper` |
| Is letter / digit / alnum | `isalpha`, `isdigit`, `isalnum` (Java: `Character.isLetterOrDigit`) |
| Index back to char | `(char)('a' + i)` / `chr(97 + i)` |

ASCII facts: `'0'` = 48, `'A'` = 65, `'a'` = 97, and lowercase minus uppercase is 32.

- **C++ `isalpha`:** calling it on a negative `char` (non-ASCII input) is undefined behaviour. Cast to `unsigned char` first.
- **Java:** `char` is UTF-16, so characters outside the BMP take two `char`s.

---

## 3. Frequency tables

Use `int cnt[26]` (lowercase), `int cnt[128]` (ASCII) or `int cnt[256]`. A hash map is needed only for Unicode or for word-level keys.

| Problem | Move |
|---|---|
| Anagram check | Increment for s and decrement for t, then check all zeros. O(n), O(1) space |
| Group anagrams | Key = sorted word (O(L log L)), or the 26-count tuple (O(L)) |
| Isomorphic strings | Two maps `s→t` and `t→s`, or the "last seen index" arrays must match |
| Sort characters by frequency | Count, then bucket by frequency (O(n)) or sort the (count, char) pairs |
| First unique character | Count, then a second scan |
| Sum of beauty (Part 17) | For each start, grow the end and update a 26-array; beauty = max − min over the non-zero counts |

An array comparison with 26 slots costs O(26) = O(1). This is how sliding-window anagram checks run in O(26n).

---

## 4. Parsing

The **atoi** checklist, in order:
1. Skip leading spaces.
2. Read an optional sign.
3. Read digits only, stopping at the first non-digit.
4. Clamp on overflow.

Detect overflow **before** multiplying:
```text
if res > (INT_MAX - d) / 10: return sign > 0 ? INT_MAX : INT_MIN
res = res * 10 + d
```
Alternatively, accumulate in 64 bits and clamp as soon as `res > 2³¹`.

**Roman to integer:** go left to right, and subtract a symbol's value when the next symbol is larger (IV, IX, XL, …). Otherwise add it. **Integer to Roman:** greedy over the 13 values `1000, 900, 500, 400, …, 4, 1`.

**Tokenising:** split on spaces while skipping repeated ones. *Reverse words* is easiest with a two-pointer scan that collects words. **Evaluate an expression:** use two stacks, or the standard calculator loop (`num`, `sign`, and a stack for parentheses).

---

## 5. Balance counters

For a single bracket type, a stack can often be replaced by one integer, `depth`:
- `(` → `depth++`, `)` → `depth--`. The string is valid iff `depth` never goes negative and ends at 0.
- **Maximum nesting depth** is the largest `depth` seen.
- **Remove outermost parentheses:** emit `(` only if `depth > 0` *before* incrementing, and emit `)` only if `depth > 0` *after* decrementing.
- **Minimum additions to make it valid:** count the unmatched `)` (each time depth would go below 0) and add the final depth.
- **With wildcards** (`*` can be `(`, `)` or empty): track the `[lo, hi]` range of possible depths.

Use a real stack when there are several bracket types, or when you need the matching indices.

---

## 6. Palindromes

| Task | Technique | Time |
|---|---|---|
| Check | Two pointers from both ends (skip non-alphanumerics if asked) | O(n) |
| Longest palindromic substring | **Expand around centre**: 2n − 1 centres (characters and gaps) | O(n²), O(1) space |
| Count palindromic substrings | Same expansion, counting each success | O(n²) |
| Longest palindromic subsequence | DP: LCS(s, reverse(s)) (Part 28) | O(n²) |
| Linear time | Manacher (Part 30 §12) | O(n) |
| Valid palindrome with ≤ 1 deletion | On the first mismatch, try skipping the left or right character | O(n) |

Expand from centre (`lo`, `hi`) while `s[lo] == s[hi]`. Call it as `(i, i)` for odd lengths and `(i, i+1)` for even lengths. The length is `hi − lo − 1` after the loop.

---

## 7. Substring enumeration

There are `n(n+1)/2` substrings. Brute force over all of them, with an O(n) check each, is O(n³). The standard improvement is **incremental state**: fix the start `i`, extend `j`, and update the state in O(1). That gives O(n²).

| Problem | Incremental state | Better |
|---|---|---|
| Count substrings with ≤ / exactly k distinct | 26-count + `distinct` counter | Sliding window: `exactly(k) = atMost(k) − atMost(k−1)`, O(n) |
| Sum of beauty | 26-count array | O(26 n²) is intended |
| Longest without repeating | last-seen index | Sliding window, O(n) (Part 22) |
| Distinct substrings | set of hashes / trie | Suffix trie O(n²) (Part 29), suffix automaton O(n) |

**Subsequences** number `2ⁿ`. Enumerating them is backtracking (Part 18), and counting or optimising over them is DP (Part 28).

---

## 8. Comparing and rotating

- **Rotation check:** `t` is a rotation of `s` iff `len(s) == len(t)` and `t` occurs in `s + s`. This is O(n) with KMP or Z, and O(n²) with a naive `find`.
- **Longest common prefix:** sort the strings and compare only the first and last, or scan vertically column by column.
- **Lexicographic order:** compare character by character. A proper prefix is smaller. `"apple" < "apply" < "b"`.
- **Largest number from an array:** sort with `a + b > b + a` (Part 13 §6).
- **Integer-like strings:** compare by length first, then lexicographically. This avoids overflow on huge numbers.

---

## 9. Where the advanced tools live

| Tool | Solves | Notes |
|---|---|---|
| KMP / prefix function | Pattern matching O(n + m), shortest period | [Part 30](../30-strings-advanced/README.md) |
| Z-function | Matching, all prefix-matches | Part 30 |
| Rolling hash (Rabin–Karp) | Matching, substring equality in O(1), longest duplicate substring | Part 30 |
| Trie | Prefix queries, word sets | [Part 29](../29-tries/README.md) |
| Manacher | All palindromes O(n) | [Part 30 §12](../30-strings-advanced/01-string-hashing-and-matching-theory.md) |
| Sliding window | Substrings with a constraint | [Part 22](../22-sliding-window-and-2-pointer/README.md) |
| String DP | LCS, edit distance, wildcard matching | [Part 28](../28-dynamic-programming/README.md) |

---

## Common mistakes

| Mistake | Fix |
|---|---|
| `s = s + c` / Java `+=` in a loop | Builder or `join` |
| `==` on Java strings | `.equals()` |
| atoi overflow check after multiplying | Check `res > (MAX − d) / 10` first |
| Only odd centres in palindrome expansion | Also expand `(i, i+1)` |
| `substr` inside an O(n²) loop | Track indices; build only the final answer |
| Using a map for lowercase letters | `int[26]`, which is faster and O(1) space |
| Isomorphic check with one map | Need a bijection: two maps |

---

## Practice

<details><summary>1. Why is `res = ""; for c in s: res = c + res` O(n²) in Python, and what do you use instead?</summary>

Each concatenation copies the string. Use `s[::-1]`, or collect characters in a list and `"".join(reversed(...))`.
</details>

<details><summary>2. atoi("  -0042abc")?</summary>

−42: skip the spaces, read the sign, read the digits 0042, stop at 'a'.
</details>

<details><summary>3. Maximum nesting depth of "(1+(2*3)+((8)/4))+1"?</summary>

3, reached at "((8".
</details>

<details><summary>4. Is "cdeab" a rotation of "abcde"?</summary>

Yes. "abcdeabcde" contains "cdeab".
</details>

<details><summary>5. Count substrings with exactly 2 distinct characters in O(n).</summary>

`atMost(2) − atMost(1)` using a sliding window with a 26-count.
</details>

<details><summary>6. Longest palindromic substring of "cbbd"?</summary>

"bb". It comes from the even centre between indices 1 and 2.
</details>

<details><summary>7. Why "badc"/"baba" is not isomorphic but passes a one-map check?</summary>

With the map s→t: b→b, a→a, d→b, c→a is consistent, but two different letters map to b. A reverse map catches this.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Immutable | Every modification creates a new string |
| Substring | Contiguous; n(n+1)/2 of them |
| Subsequence | Order-preserving subset; 2ⁿ of them |
| Lexicographic | Dictionary order, character by character |
| Centre | Character or gap from which a palindrome expands |

---

## Flashcards

**Efficient string building: C++, Java, Python?** #flashcard
`s += c` / `push_back` in C++, `StringBuilder` in Java, a list + `"".join` in Python.

**Overflow-safe atoi check?** #flashcard
Before `res = res*10 + d`, return the clamp if `res > (INT_MAX − d) / 10`.

**Valid parentheses with one bracket type in O(1) space?** #flashcard
Depth counter that never goes negative and ends at 0.

**Longest palindromic substring without DP?** #flashcard
Expand around all 2n − 1 centres: O(n²) time, O(1) space.

**Rotation check?** #flashcard
Equal length, and t is a substring of s + s.

**Anagram check in O(1) space?** #flashcard
A 26-count array: increment for s, decrement for t, all zero.

**Exactly-k-distinct substrings in O(n)?** #flashcard
atMost(k) − atMost(k − 1).

---

**Interview track →** [String deep-dive](../../01-data-structures/03-string.md) · [String algorithms](../../02-algorithms/02-string-algorithms.md) · [String walkthroughs](../../coding/data-structures/03-string.md)
