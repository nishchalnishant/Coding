---
module: striver-a2z/30-strings-advanced
lesson: 9
topic: Longest happy prefix
difficulty: Hard
source: https://takeuforward.org/learning/dsa/longest-happy-prefix?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet
tags: [striver, strings--advanced-algo, string, kmp, prefix-function, hashing]
---
# 9. Longest happy prefix

← [Shortest palindrome](08-shortest-palindrome.md) · [Part 30 index](README.md) · Next → [Part 31: Maths](../31-maths/README.md)

> [!abstract] Problem at a glance
> **Task:** Return the longest proper prefix of `s` that is also a suffix (a 'happy prefix'), or `""`.
> **Key insight:** This is literally `lps[n − 1]`, the last value of the KMP prefix function. Return `s[:lps[n − 1]]`. A rolling-hash scan over all lengths also works in O(n) expected time.
> **Difficulty:** Hard · **Pattern:** Prefix function (last value) · **Also on:** [LC 1392](https://leetcode.com/problems/longest-happy-prefix/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-happy-prefix?category=advanced-problems-(less-asked)&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Check every length](#3-check-every-length) · [4. Prefix function](#4-prefix-function) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A happy prefix is a non-empty prefix of `s` that is also a suffix, excluding `s` itself. Return the longest one, or `""` if none exists.

| Input | Output | Why |
|---|---|---|
| `"level"` | `"l"` | borders: l |
| `"ababab"` | `"abab"` | prefix and suffix may overlap |

**Constraints:** `1 ≤ |s| ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Check every length | k from n − 1 down to 1 | O(n²) | O(n) |
| Prefix function | answer = s[:lps[n − 1]] | O(n) | O(n) |

> [!tip] Interview angle
> Recognise it as the definition of the border, so `lps[n − 1]`. If you can't recall KMP under pressure, rolling hashes are the fallback: maintain the hash of `s[:k]` growing left-to-right and the hash of `s[n−k:]` growing right-to-left, and record the largest `k` where they agree (verify to be safe).

---

## 3. Check every length

**Intuition.** Compare `s[:k]` with `s[n − k:]` for each `k`, longest first. The first equal pair is the answer.

```python
def happy_brute(s):
    for k in range(len(s) - 1, 0, -1):
        if s[:k] == s[-k:]:
            return s[:k]
    return ""
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Prefix function

**Intuition.** Compute the LPS array once; its last value is the length of the longest proper border of the whole string.

**Algorithm**

1. Compute `lps` of `s`.
2. Return `s.substr(0, lps[n − 1])`.

**Dry run** — ababab: lps = [0, 0, 1, 2, 3, 4] → s[:4] = abab.

**C++**
```cpp
string longestPrefix(const string& s) {
    int n = s.size();
    vector<int> lps(n, 0);
    for (int i = 1, len = 0; i < n; i++) {
        while (len > 0 && s[i] != s[len]) len = lps[len - 1];
        if (s[i] == s[len]) len++;
        lps[i] = len;
    }
    return s.substr(0, lps[n - 1]);
}
```

**Java**
```java
static String longestPrefix(String s) {
    int n = s.length();
    int[] lps = new int[n];
    for (int i = 1, len = 0; i < n; i++) {
        while (len > 0 && s.charAt(i) != s.charAt(len)) len = lps[len - 1];
        if (s.charAt(i) == s.charAt(len)) len++;
        lps[i] = len;
    }
    return s.substring(0, lps[n - 1]);
}
```

**Python**
```python
def longest_prefix(s):
    lps = [0] * len(s)
    length = 0
    for i in range(1, len(s)):
        while length and s[i] != s[length]:
            length = lps[length - 1]
        if s[i] == s[length]:
            length += 1
        lps[i] = length
    return s[:lps[-1]]
```

**Complexity:** time **O(n)**, space **O(n)** — one linear prefix-function pass.

---

## Edge cases

- Length 1 → "".
- All the same character → s minus one char.
- Overlapping border (`ababab` → `abab`).

---

## Common mistakes

1. Returning `s` itself (the border must be proper).
2. Rolling hash without verification on a hit (rare wrong answers).

---

## Follow-ups

1. All borders, not just the longest?
2. Minimum characters to append to make s periodic?

<details><summary>Answer sketches</summary>

**#1:** Follow the chain lps[n−1], lps[lps[n−1]−1], … down to 0.

**#2:** p = n − lps[n−1]; append (p − n % p) % p characters.
</details>

---

## Flashcards

**Longest happy prefix?** #flashcard
s[:lps[n − 1]].

**How do you list all borders?** #flashcard
Follow k → lps[k − 1] starting at k = lps[n − 1].

**Interview track →** [String algorithms deep-dive](../../02-algorithms/02-string-algorithms.md) · [String algorithm walkthroughs](../../04-practice/algorithms/02-string-algorithms.md)
