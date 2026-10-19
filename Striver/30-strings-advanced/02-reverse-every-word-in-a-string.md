---
module: striver/30-strings-advanced
lesson: 2
topic: Reverse every word in a string
difficulty: Medium
source: https://takeuforward.org/learning/dsa/reverse-every-word-in-a-string?category=medium-problems&source=strivers-a2z-dsa-sheet
tags: [striver, strings--advanced-algo, string, two-pointers]
---
# 2. Reverse every word in a string

← [String Hashing and Pattern Matching](01-string-hashing-and-matching-theory.md) · [Part 30 index](README.md) · Next → [Minimum number of bracket reversals to balance an expression](03-minimum-number-of-bracket-reversals-to-balance-an-expression.md)

> [!abstract] Problem at a glance
> **Task:** Reverse the order of the words in `s`, dropping leading, trailing and repeated spaces.
> **Key insight:** Scan from the **right**: skip spaces, mark the end of a word, walk left to its start, and append it. Every word comes out in reversed order with exactly one space between words. The in-place C++ trick is to reverse the whole string, then reverse each word back while compacting the spaces.
> **Difficulty:** Medium · **Pattern:** Two pointers from the end / reverse-all-then-each · **Also on:** [LC 151](https://leetcode.com/problems/reverse-words-in-a-string/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-every-word-in-a-string?category=medium-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Split, reverse, join](#3-split-reverse-join) · [4. Scan from the right](#4-scan-from-the-right) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s` of words separated by one or more spaces, return the words in reverse order joined by single spaces, with no leading or trailing spaces.

| Input | Output | Why |
|---|---|---|
| `"the sky is blue"` | `"blue is sky the"` |  |
| `"  hello world  "` | `"world hello"` | trim the outer spaces |
| `"a good   example"` | `"example good a"` | collapse the inner spaces |

**Constraints:** `1 ≤ |s| ≤ 10⁴`; letters, digits and spaces; at least one word.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Split, reverse, join | library split on whitespace | O(n) | O(n) |
| Scan from the right | find each word's [j+1, i] going leftwards | O(n) | O(n) output (O(1) extra in-place in C++) |

> [!tip] Interview angle
> Ask whether extra spaces must be collapsed (yes here). Start with `split` + reverse + `join` to show you know the library route, then offer the O(1)-extra in-place version (C++ `string` is mutable): reverse everything, reverse each word, compact.

---

## 3. Split, reverse, join

**Intuition.** `split()` with no argument already drops empty tokens. Reverse the list and join with single spaces.

```python
def reverse_words_split(s):
    return " ".join(reversed(s.split()))
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Scan from the right

**Intuition.** Let `i` start at the last index. Skip spaces leftwards; if `i < 0` stop. Move `j` left from `i` until a space, so the word is `s[j+1..i]`. Append it, with a separator if the output is non-empty, and continue from `j`.

**Algorithm**

1. `i = n − 1`, `out = ""`.
2. While `i ≥ 0`: skip spaces; if `i < 0` break.
3. `j = i`; move `j` left while `s[j]` is not a space.
4. Append a space if `out` is non-empty, then `s[j+1..i]`; set `i = j`.

**Dry run** — "a good   example": i at 'e' → word example; skip 3 spaces → good; skip 1 → a. Output "example good a".

**C++**
```cpp
string reverseWords(string s) {
    reverse(s.begin(), s.end());                 // whole string reversed
    int n = s.size(), w = 0;                     // w = write index
    for (int i = 0; i < n; ) {
        if (s[i] == ' ') { i++; continue; }
        if (w) s[w++] = ' ';
        int st = w;
        while (i < n && s[i] != ' ') s[w++] = s[i++];
        reverse(s.begin() + st, s.begin() + w);  // fix this word back
    }
    s.resize(w);
    return s;
}
```

**Java**
```java
static String reverseWords(String s) {
    StringBuilder sb = new StringBuilder();
    int i = s.length() - 1;
    while (i >= 0) {
        while (i >= 0 && s.charAt(i) == ' ') i--;
        if (i < 0) break;
        int j = i;
        while (j >= 0 && s.charAt(j) != ' ') j--;
        if (sb.length() > 0) sb.append(' ');
        sb.append(s, j + 1, i + 1);
        i = j;
    }
    return sb.toString();
}
```

**Python**
```python
def reverse_words(s):
    out, i = [], len(s) - 1
    while i >= 0:
        while i >= 0 and s[i] == ' ':
            i -= 1
        if i < 0:
            break
        j = i
        while j >= 0 and s[j] != ' ':
            j -= 1
        out.append(s[j + 1:i + 1])
        i = j
    return " ".join(out)
```

**Complexity:** time **O(n)**, space **O(n) output (O(1) extra in-place in C++)** — each character is visited a constant number of times.

---

## Edge cases

- A single word with surrounding spaces.
- Many spaces between words.
- Only one character.

---

## Common mistakes

1. Splitting on `' '` (Python `split(' ')`, Java `split(" ")`), which keeps empty tokens.
2. Leaving a trailing space after the last word.
3. Java: building with `+=` in a loop (O(n²)).

---

## Follow-ups

1. Reverse the characters of each word but keep the word order?
2. Input is a char array and must be O(1) extra?

<details><summary>Answer sketches</summary>

**#1:** Reverse each maximal non-space run in place (LC 557).

**#2:** Reverse all, reverse each word, then compact the spaces with a write pointer (the C++ version above).
</details>

---

## Flashcards

**Reverse words in O(1) extra space?** #flashcard
Reverse the whole string, then reverse each word, compacting spaces with a write index.

**Python pitfall with split?** #flashcard
`split(' ')` keeps empty strings; `split()` doesn't.

**Interview track →** [String algorithms deep-dive](../../02-algorithms/02-string-algorithms.md) · [String algorithm walkthroughs](../../coding/algorithms/02-string-algorithms.md)
