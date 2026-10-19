---
module: striver/30-strings-advanced
lesson: 7
topic: KMP algorithm (LPS array)
difficulty: Hard
source: https://takeuforward.org/learning/dsa/kmp-algorithm-or-lps-array?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet
tags: [striver, strings--advanced-algo, string, kmp, prefix-function, pattern-matching]
---
# 7. KMP algorithm (LPS array)

← [Z-function](06-z-function.md) · [Part 30 index](README.md) · Next → [Shortest palindrome](08-shortest-palindrome.md)

> [!abstract] Problem at a glance
> **Task:** Compute the LPS (prefix-function) array of `s`, the core of KMP.
> **Key insight:** `lps[i]` is the length of the longest proper prefix of `s[0..i]` that is also a suffix of it. Keep `len = lps[i − 1]`. If `s[i] == s[len]`, extend: `len + 1`. Otherwise fall back to the **next-shorter border**, `len = lps[len − 1]`, and try again. `len` rises by at most 1 per step, so the fallbacks total O(n).
> **Difficulty:** Hard · **Pattern:** Prefix function / border fallback · **Also on:** [LC 28](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/kmp-algorithm-or-lps-array?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute-force borders](#3-brute-force-borders) · [4. Prefix function with fallback](#4-prefix-function-with-fallback) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s`, return the array `lps` where `lps[i]` is the length of the longest proper prefix of `s[0..i]` that is also a suffix of `s[0..i]`. Then use it to search a pattern in linear time.

| Input | Output | Why |
|---|---|---|
| `"aabaaab"` | `[0, 1, 0, 1, 2, 2, 3]` | at i=5 the border aa fails ('b' vs 'a') → fall back to a |
| `"abcabcd"` | `[0, 0, 0, 1, 2, 3, 0]` |  |

**Constraints:** `1 ≤ |s| ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute-force borders | try every prefix length for every i | O(n³) | O(n) |
| Prefix function with fallback | extend or follow lps[len − 1] | O(n) | O(n) |

> [!tip] Interview angle
> State the definition with **proper** prefix (not the whole string). Show the fallback chain `len → lps[len−1]` as 'the next-longest border of the current border'. Then: KMP search = LPS of `pat`, then scan `text` with the same loop, reporting a match when `len == m` and continuing from `lps[m − 1]`.

---

## 3. Brute-force borders

**Intuition.** For each `i`, check every `k` from `i` down to 1: is `s[0..k−1] == s[i−k+1..i]`? The first success is `lps[i]`.

```python
def lps_brute(s):
    res = []
    for i in range(len(s)):
        best = 0
        for k in range(i, 0, -1):
            if s[:k] == s[i - k + 1:i + 1]:
                best = k
                break
        res.append(best)
    return res
```

**Complexity:** time **O(n³)**, space **O(n)**.

---

## 4. Prefix function with fallback

**Intuition.** Borders of `s[0..i]` are borders of `s[0..i−1]` extended by one char. Walk the border chain of `s[0..i−1]` (`len`, `lps[len−1]`, …) until `s[len] == s[i]` or `len == 0`.

**Algorithm**

1. `lps[0] = 0`, `len = 0`.
2. For `i = 1..n−1`: while `len > 0` and `s[i] != s[len]`: `len = lps[len − 1]`.
3. If `s[i] == s[len]`: `len++`.
4. `lps[i] = len`.

**Dry run** — aabaaab: i1 a=a → 1; i2 b≠a(s[1]) → len=lps[0]=0, b≠a → 0; i3 → 1; i4 → 2; i5: len=2, s[5]='a' ≠ s[2]='b' → len=lps[1]=1, s[1]='a' = 'a' → 2; i6: s[6]='b' = s[2] → 3.

**C++**
```cpp
vector<int> computeLPS(const string& s) {
    int n = s.size();
    vector<int> lps(n, 0);
    for (int i = 1, len = 0; i < n; i++) {
        while (len > 0 && s[i] != s[len]) len = lps[len - 1];
        if (s[i] == s[len]) len++;
        lps[i] = len;
    }
    return lps;
}
```

**Java**
```java
static int[] computeLPS(String s) {
    int n = s.length();
    int[] lps = new int[n];
    for (int i = 1, len = 0; i < n; i++) {
        while (len > 0 && s.charAt(i) != s.charAt(len)) len = lps[len - 1];
        if (s.charAt(i) == s.charAt(len)) len++;
        lps[i] = len;
    }
    return lps;
}
```

**Python**
```python
def compute_lps(s):
    lps = [0] * len(s)
    length = 0
    for i in range(1, len(s)):
        while length and s[i] != s[length]:
            length = lps[length - 1]
        if s[i] == s[length]:
            length += 1
        lps[i] = length
    return lps
```

**Complexity:** time **O(n)**, space **O(n)** — len increases by at most 1 per i and every fallback decreases it, so total fallbacks ≤ n.

---

## Edge cases

- All equal characters: lps = [0, 1, 2, …].
- No repeated characters: all zeros.
- Length 1: [0].

---

## Common mistakes

1. Using `if` instead of `while` for the fallback.
2. Falling back to `lps[len]` instead of `lps[len − 1]`.
3. Letting the border be the whole string (`lps[i] ≤ i`).

---

## Follow-ups

1. KMP search?
2. Repeated substring pattern (LC 459)?

<details><summary>Answer sketches</summary>

**#1:** Run the same loop over text with len tracking the matched pattern prefix; on len == m, record i − m + 1 and set len = lps[m − 1].

**#2:** p = n − lps[n−1]; s is a repetition iff lps[n−1] > 0 and n % p == 0.
</details>

---

## Flashcards

**Define lps[i].** #flashcard
Longest proper prefix of s[0..i] that is also its suffix.

**KMP fallback?** #flashcard
len = lps[len − 1] while s[i] != s[len].

**Why is the prefix function O(n)?** #flashcard
len grows ≤ 1 per step and each fallback shrinks it; total work is amortised linear.

**Smallest period from lps?** #flashcard
n − lps[n − 1].

**Interview track →** [String algorithms deep-dive](../../02-algorithms/02-string-algorithms.md) · [String algorithm walkthroughs](../../coding/algorithms/02-string-algorithms.md)
