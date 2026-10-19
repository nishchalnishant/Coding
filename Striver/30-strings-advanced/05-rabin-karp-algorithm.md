---
module: striver/30-strings-advanced
lesson: 5
topic: Rabin-Karp algorithm
difficulty: Hard
source: https://takeuforward.org/learning/dsa/rabin-karp-algorithm?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet
tags: [striver, strings--advanced-algo, string, hashing, rolling-hash, pattern-matching]
---
# 5. Rabin-Karp algorithm

← [Count and say](04-count-and-say.md) · [Part 30 index](README.md) · Next → [Z-function](06-z-function.md)

> [!abstract] Problem at a glance
> **Task:** Return every start index where `pat` occurs in `text`, using a rolling hash.
> **Key insight:** Hash the pattern and the first window as base-B polynomials mod a prime. Slide the window in O(1): subtract the outgoing char × `B^(m−1)`, multiply by `B`, add the incoming char. Compare characters **only when the hashes match**, so collisions can't produce wrong answers. Expected O(n + m).
> **Difficulty:** Hard · **Pattern:** Rolling polynomial hash · **Also on:** [LC 28](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/rabin-karp-algorithm?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute-force window comparison](#3-brute-force-window-comparison) · [4. Rabin-Karp rolling hash](#4-rabin-karp-rolling-hash) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given strings `text` and `pat`, return the 0-based indices of all occurrences of `pat` in `text` in increasing order (possibly overlapping). Return an empty list if there are none.

| Input | Output | Why |
|---|---|---|
| `text = "abababc", pat = "aba"` | `[0, 2]` | overlapping occurrences count |
| `text = "aaaa", pat = "aa"` | `[0, 1, 2]` |  |
| `text = "abc", pat = "d"` | `[]` |  |

**Constraints:** `1 ≤ |pat| ≤ |text| ≤ 10⁵` (patterns longer than the text return `[]`).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute-force window comparison | compare pat at every start | O(n·m) | O(1) |
| Rabin-Karp rolling hash | O(1) window hash update + verify on match | O(n + m) expected, O(n·m) worst | O(1) extra |

> [!tip] Interview angle
> Define the hash `h(s) = Σ s[i]·B^(m−1−i) mod M`, then derive the roll in one line. Mention: (1) keep values non-negative after subtracting (`+ M`); (2) verify on a hash hit, so the worst case is O(nm) when everything collides; (3) double hashing (two moduli) makes collisions negligible if you skip the verification.

---

## 3. Brute-force window comparison

**Intuition.** For each start `i` in `0..n−m`, compare `text[i..i+m−1]` with `pat` character by character.

```python
def search_brute(text, pat):
    n, m = len(text), len(pat)
    return [i for i in range(n - m + 1) if text[i:i + m] == pat]
```

**Complexity:** time **O(n·m)**, space **O(1)**.

---

## 4. Rabin-Karp rolling hash

**Intuition.** `hp = h(pat)`, `ht = h(text[0..m−1])`, `pw = B^(m−1) mod M`. At start `i`: if `hp == ht`, verify and record. Then roll: `ht = ((ht − text[i]·pw)·B + text[i+m]) mod M`.

**Algorithm**

1. If `m > n`, return `[]`.
2. Compute `hp`, `ht` and `pw = B^(m−1) mod M`.
3. For `i = 0..n−m`: on `hp == ht`, compare the window and record `i`.
4. If `i + m < n`, roll `ht` forward (adding `M` before the modulo to stay non-negative).

**Dry run** — B=10 with digits for intuition: text 31415, pat 14. h(31) = 31 → roll: (31 − 3·10)·10 + 4 = 14 = hp → verify → index 1.

**C++**
```cpp
vector<int> rabinKarp(const string& t, const string& p) {
    const long long B = 131, M = 1000000007;
    int n = t.size(), m = p.size();
    vector<int> res;
    if (m > n) return res;
    long long hp = 0, ht = 0, pw = 1;
    for (int i = 0; i < m; i++) {
        hp = (hp * B + p[i]) % M;
        ht = (ht * B + t[i]) % M;
        if (i) pw = pw * B % M;                     // pw = B^(m-1)
    }
    for (int i = 0; ; i++) {
        if (hp == ht && t.compare(i, m, p) == 0) res.push_back(i);
        if (i + m == n) break;
        ht = ((ht - t[i] * pw % M + M) * B + t[i + m]) % M;
    }
    return res;
}
```

**Java**
```java
static List<Integer> rabinKarp(String t, String p) {
    final long B = 131, M = 1_000_000_007L;
    int n = t.length(), m = p.length();
    List<Integer> res = new ArrayList<>();
    if (m > n) return res;
    long hp = 0, ht = 0, pw = 1;
    for (int i = 0; i < m; i++) {
        hp = (hp * B + p.charAt(i)) % M;
        ht = (ht * B + t.charAt(i)) % M;
        if (i > 0) pw = pw * B % M;
    }
    for (int i = 0; ; i++) {
        if (hp == ht && t.regionMatches(i, p, 0, m)) res.add(i);
        if (i + m == n) break;
        ht = ((ht - t.charAt(i) * pw % M + M) * B + t.charAt(i + m)) % M;
    }
    return res;
}
```

**Python**
```python
def rabin_karp(text, pat):
    B, M = 131, 10**9 + 7
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
        if hp == ht and text[i:i + m] == pat:
            res.append(i)
        if i + m < n:
            ht = ((ht - ord(text[i]) * pw) * B + ord(text[i + m])) % M
    return res
```

**Complexity:** time **O(n + m) expected, O(n·m) worst**, space **O(1) extra** — O(m) setup, O(1) per roll, and verification is only paid on (rare) hash hits plus real matches.

---

## Edge cases

- Pattern longer than the text.
- Pattern equals the text.
- Overlapping matches (`aaaa` / `aa`).

---

## Common mistakes

1. Negative hash after the subtraction (C++/Java `%` keeps the sign).
2. `pw = B^m` instead of `B^(m−1)`.
3. Overflow: `ht * B` must fit in 64 bits, so keep `M < 2³¹` and `B` small.
4. Trusting a hash match without verifying.

---

## Follow-ups

1. Search many patterns of the same length?
2. Longest duplicate substring (LC 1044)?

<details><summary>Answer sketches</summary>

**#1:** Put all pattern hashes in a set and roll once over the text.

**#2:** Binary search the length; for each length, roll hashes and look for a repeat.
</details>

---

## Flashcards

**Rabin-Karp roll?** #flashcard
ht = ((ht − out·B^(m−1))·B + in) mod M.

**Why verify on a hash hit?** #flashcard
Different strings can share a hash (collision); verification makes the output exact.

**Rabin-Karp complexity?** #flashcard
O(n + m) expected; O(nm) worst if every window collides.

**Interview track →** [String algorithms deep-dive](../../02-algorithms/02-string-algorithms.md) · [String algorithm walkthroughs](../../coding/algorithms/02-string-algorithms.md)
