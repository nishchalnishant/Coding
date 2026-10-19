---
module: striver/30-strings-advanced
lesson: 8
topic: Shortest palindrome
difficulty: Hard
source: https://takeuforward.org/learning/dsa/shortest-palindrome?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet
tags: [striver, strings--advanced-algo, string, kmp, palindrome]
---
# 8. Shortest palindrome

← [KMP algorithm (LPS array)](07-kmp-algorithm-lps-array.md) · [Part 30 index](README.md) · Next → [Longest happy prefix](09-longest-happy-prefix.md)

> [!abstract] Problem at a glance
> **Task:** Prepend the fewest characters to `s` to make it a palindrome; return the result.
> **Key insight:** Only the part after the **longest palindromic prefix** must be mirrored in front. That prefix is the longest prefix of `s` equal to a suffix of `rev(s)`, which is exactly `lps` of `s + '#' + rev(s)` at the last position. The answer is `rev(s)[:n − k] + s`.
> **Difficulty:** Hard · **Pattern:** KMP on s + '#' + reverse(s) · **Also on:** [LC 214](https://leetcode.com/problems/shortest-palindrome/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/shortest-palindrome?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Longest palindromic prefix by checking](#3-longest-palindromic-prefix-by-checking) · [4. KMP on s#rev(s)](#4-kmp-on-srevs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s`, you may add characters only to its front. Return the shortest palindrome you can get.

| Input | Output | Why |
|---|---|---|
| `"aacecaaa"` | `"aaacecaaa"` | palindromic prefix aacecaa, mirror the last a |
| `"abcd"` | `"dcbabcd"` | palindromic prefix a |

**Constraints:** `0 ≤ |s| ≤ 5·10⁴`, lowercase letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Longest palindromic prefix by checking | try k = n, n − 1, … until s[:k] is a palindrome | O(n²) | O(n) |
| KMP on s#rev(s) | k = lps[-1] = longest palindromic prefix | O(n) | O(n) |

> [!tip] Interview angle
> Reduce first: 'prepend the minimum' ⇔ 'find the longest palindromic prefix'. Brute force checks each prefix (O(n²)). Then the trick: a prefix `P` is a palindrome iff `P == rev(P)`, and `rev(P)` is a suffix of `rev(s)`, so we want the longest prefix of `s` that is a suffix of `rev(s)`: one LPS computation. The `#` stops the border from crossing into `rev(s)`.

---

## 3. Longest palindromic prefix by checking

**Intuition.** For `k` from `n` down to 0, test whether `s[:k]` reads the same backwards. The first success is the longest palindromic prefix; mirror the rest.

```python
def shortest_pal_brute(s):
    for k in range(len(s), -1, -1):
        if s[:k] == s[:k][::-1]:
            return s[k:][::-1] + s
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. KMP on s#rev(s)

**Intuition.** Build `t = s + '#' + rev(s)` and its LPS array. `k = lps[|t| − 1]` is the length of the longest prefix of `s` that is also a suffix of `rev(s)`, i.e. the longest palindromic prefix. Prepend `rev(s)[:n − k]`.

**Algorithm**

1. `r = reverse(s)`, `t = s + '#' + r`.
2. Compute `lps` of `t`.
3. `k = lps.back()`.
4. Return `r.substr(0, n − k) + s`.

**Dry run** — abcd: t = abcd#dcba, lps ends at 1 ('a') → prepend r[:3] = dcb → dcbabcd.

**C++**
```cpp
string shortestPalindrome(const string& s) {
    string r(s.rbegin(), s.rend()), t = s + '#' + r;
    int n = t.size();
    vector<int> lps(n, 0);
    for (int i = 1, len = 0; i < n; i++) {
        while (len > 0 && t[i] != t[len]) len = lps[len - 1];
        if (t[i] == t[len]) len++;
        lps[i] = len;
    }
    return r.substr(0, s.size() - lps[n - 1]) + s;
}
```

**Java**
```java
static String shortestPalindrome(String s) {
    String r = new StringBuilder(s).reverse().toString(), t = s + "#" + r;
    int n = t.length();
    int[] lps = new int[n];
    for (int i = 1, len = 0; i < n; i++) {
        while (len > 0 && t.charAt(i) != t.charAt(len)) len = lps[len - 1];
        if (t.charAt(i) == t.charAt(len)) len++;
        lps[i] = len;
    }
    return r.substring(0, s.length() - lps[n - 1]) + s;
}
```

**Python**
```python
def shortest_palindrome(s):
    r = s[::-1]
    t = s + '#' + r
    lps = [0] * len(t)
    length = 0
    for i in range(1, len(t)):
        while length and t[i] != t[length]:
            length = lps[length - 1]
        if t[i] == t[length]:
            length += 1
        lps[i] = length
    return r[:len(s) - lps[-1]] + s
```

**Complexity:** time **O(n)**, space **O(n)** — one prefix-function pass over a string of length 2n + 1.

---

## Edge cases

- Empty string → "".
- Already a palindrome → unchanged.
- All characters distinct → mirror n − 1 chars.

---

## Common mistakes

1. Omitting the separator, so the border can be longer than `s` (e.g. `aaaa`).
2. Appending instead of prepending.
3. Using the whole `lps` max instead of the last value.

---

## Follow-ups

1. Using hashing instead?
2. Append to the end instead?

<details><summary>Answer sketches</summary>

**#1:** Roll forward and backward hashes of each prefix; the largest k with equal hashes is the palindromic prefix (O(n) expected).

**#2:** Symmetric: longest palindromic suffix, via lps of rev(s) + '#' + s.
</details>

---

## Flashcards

**Shortest palindrome reduction?** #flashcard
Longest palindromic prefix k; answer = rev(s)[:n − k] + s.

**How does KMP find the longest palindromic prefix?** #flashcard
Last lps value of s + '#' + rev(s).

**Interview track →** [String algorithms deep-dive](../../02-algorithms/02-string-algorithms.md) · [String algorithm walkthroughs](../../coding/algorithms/02-string-algorithms.md)
