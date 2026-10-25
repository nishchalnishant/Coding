---
module: striver-a2z/11-basic-strings
lesson: 3
topic: Largest Odd Number in a String
difficulty: Easy
source: https://takeuforward.org/learning/dsa/largest-odd-number-in-a-string?category=basic-strings&source=strivers-a2z-dsa-sheet
tags: [striver, basic-strings, strings, greedy]
---
# 3. Largest Odd Number in a String

← [Palindrome Check](02-palindrome-check.md) · [Part 11 index](README.md) · Next → [Longest Common Prefix](04-longest-common-prefix.md)

> [!abstract] Problem at a glance
> **Task:** Return the largest odd integer that is a substring of the digit string `s`, without leading zeros, or `""`.
> **Key insight:** A number is odd iff its last digit is odd. The largest candidate starts as far left as possible and ends at the **rightmost** odd digit. Then strip the leading zeros.
> **Difficulty:** Easy · **Pattern:** Directed scan (from the right) · **Also on:** 1903
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/largest-odd-number-in-a-string?category=basic-strings&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — all substrings](#3-brute--all-substrings) · [4. Optimal — rightmost odd + strip zeros](#4-optimal--rightmost-odd--strip-zeros) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s` of digits, return the largest-valued odd integer, as a string, that is a non-empty substring of `s`, with leading zeros removed. Return `""` if none exists.

| Input | Output | Why |
|---|---|---|
| `s = "5347"` | `"5347"` | already ends in 7 |
| `s = "0214638"` | `"21463"` | rightmost odd digit is 3; drop the leading 0 |
| `s = "0000"` | `""` | no odd digit |

**Constraints:** `1 ≤ n ≤ 10⁵`, digits only. The value can be far beyond 64-bit, so never convert to an int.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — all substrings | check every substring, keep the best | O(n³) | O(n) |
| Optimal — rightmost odd + strip zeros | end at the rightmost odd digit, start at the first non-zero | O(n) | O(1) extra |

> [!tip] Interview angle
> The trap is converting to an integer: `n = 10⁵` digits overflows everything. Say up front that you'll compare by length and position, not numerically.

---

## 3. Brute — all substrings

**Intuition.** Enumerate the substrings that don't start with `0` and end in an odd digit. Compare candidates by `(length, lexicographic)`, which equals numeric order for same-length digit strings without leading zeros.

```python
def largest_odd_brute(s):
    best = ""
    n = len(s)
    for i in range(n):
        if s[i] == "0":
            continue
        for j in range(i, n):
            if int(s[j]) % 2 == 1:
                sub = s[i:j + 1]
                if (len(sub), sub) > (len(best), best):
                    best = sub
    return best
```

**Complexity:** time **O(n³)**, space **O(n)**.

---

## 4. Optimal — rightmost odd + strip zeros

**Intuition.** For the end: any odd substring must end at an odd digit, and ending further right gives a longer, larger number, so end at the rightmost odd index `r`. For the start: begin as far left as possible, but not on a `0`, so start at the first non-zero index `l`. If `l > r` there is nothing to return.

**Algorithm**

1. `r` = rightmost index with an odd digit; if none, return `""`.
2. `l` = first index with `s[l] != '0'`.
3. Return `s[l..r]` (`""` if `l > r`, which can't happen once r exists, because `s[r]` is non-zero).

**Dry run** — `0214638`: from the right, 8 is even, 3 is odd → r = 5. From the left, 0 is skipped → l = 1 → `s[1..5]` = **21463**.

**C++**
```cpp
string largeOddNum(string& s) {
    int r = (int)s.size() - 1;
    while (r >= 0 && (s[r] - '0') % 2 == 0) r--;
    if (r < 0) return "";
    int l = 0;
    while (l <= r && s[l] == '0') l++;
    return s.substr(l, r - l + 1);
}
```

**Java**
```java
static String largeOddNum(String s) {
    int r = s.length() - 1;
    while (r >= 0 && (s.charAt(r) - '0') % 2 == 0) r--;
    if (r < 0) return "";
    int l = 0;
    while (l <= r && s.charAt(l) == '0') l++;
    return s.substring(l, r + 1);
}
```

**Python**
```python
def large_odd_num(s):
    r = len(s) - 1
    while r >= 0 and int(s[r]) % 2 == 0:
        r -= 1
    if r < 0:
        return ""
    l = 0
    while l <= r and s[l] == "0":
        l += 1
    return s[l:r + 1]
```

**Complexity:** time **O(n)**, space **O(1) extra**.

---

## Edge cases

- No odd digit → `""`.
- Leading zeros before the odd digit (`00102` → `1`).
- Zeros inside the number stay (`10203` → `10203`).

---

## Common mistakes

1. `int(s)`: overflows in C++/Java and is slow for 10⁵ digits in Python.
2. Stripping trailing zeros as well. Only leading zeros go.
3. Scanning from the left for the first odd digit gives the shortest candidate, not the largest.

---

## Follow-ups

1. Largest number formed by rearranging digits that's divisible by 3.
2. Largest even number substring.

<details><summary>Answer sketches</summary>

**#1:** Count digits; digit sum mod 3 tells you which 1–2 smallest digits to drop; then output the digits descending.

**#2:** Same idea: end at the rightmost even digit.
</details>

---

## Flashcards

**Largest odd substring of a digit string?** #flashcard
Prefix ending at the rightmost odd digit, minus leading zeros.

**How do you compare huge numeric strings?** #flashcard
By length first, then lexicographically (no leading zeros).

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String algorithms](../../02-algorithms/02-string-algorithms.md) · [Concept: basic strings](../07-concept-basics/04-basic-string.md)
