---
module: striver-a2z/12-basic-recursion
lesson: 7
topic: Check if String is Palindrome or Not
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-string-is-palindrome-or-not-?category=basic-recursion&source=strivers-a2z-dsa-sheet
tags: [striver, basic-recursion, recursion, strings, two-pointers]
---
# 7. Check if String is Palindrome or Not

← [Reverse a String (Recursive)](06-reverse-a-string-recursive.md) · [Part 12 index](README.md) · Next → [Check if a Number is Prime or Not](08-check-if-a-number-is-prime.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `s` is a palindrome, using recursion.
> **Key insight:** `isPal(l, r) = s[l] == s[r] and isPal(l + 1, r − 1)`, with `l ≥ r → true`. The `and` short-circuits, so the first mismatch stops the recursion.
> **Difficulty:** Easy · **Pattern:** Two-ended recursion
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-string-is-palindrome-or-not-?category=basic-recursion&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — compare with a recursive reverse](#3-brute--compare-with-a-recursive-reverse) · [4. Optimal — recurse on (l, r)](#4-optimal--recurse-on-l-r) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s`, return `true` if it reads the same forwards and backwards. Use recursion.

| Input | Output | Why |
|---|---|---|
| `s = "abba"` | `true` |  |
| `s = "abc"` | `false` |  |
| `s = "a"` | `true` |  |

**Constraints:** `1 ≤ n ≤ 10³`, lowercase.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — compare with a recursive reverse | s == reverse(s) | O(n) | O(n) |
| Optimal — recurse on (l, r) | s[l]==s[r] and f(l+1, r−1) | O(n) | O(n) stack |

---

## 3. Brute — compare with a recursive reverse

**Intuition.** Build the reverse (recursively, or by slicing), then compare. It always does all the work.

```python
def pal_rev(s):
    return s == s[::-1]
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Optimal — recurse on (l, r)

**Intuition.** A string is a palindrome iff its outer chars match and its inner part is a palindrome. The empty or single-char middle is the base case.

**Algorithm**

1. `f(l, r)`: if `l >= r` return true.
2. If `s[l] != s[r]` return false.
3. Return `f(l + 1, r − 1)`.

**Dry run** — `abba`: (a, a) ✓ → (b, b) ✓ → l = 2 > r = 1 → true.

**C++**
```cpp
bool palHelper(string& s, int l, int r) {
    if (l >= r) return true;
    if (s[l] != s[r]) return false;
    return palHelper(s, l + 1, r - 1);
}
bool palindromeCheck(string& s) { return palHelper(s, 0, (int)s.size() - 1); }
```

**Java**
```java
static boolean palHelper(String s, int l, int r) {
    if (l >= r) return true;
    if (s.charAt(l) != s.charAt(r)) return false;
    return palHelper(s, l + 1, r - 1);
}
static boolean palindromeCheck(String s) { return palHelper(s, 0, s.length() - 1); }
```

**Python**
```python
def palindrome_check(s, l=0, r=None):
    if r is None:
        r = len(s) - 1
    if l >= r:
        return True
    if s[l] != s[r]:
        return False
    return palindrome_check(s, l + 1, r - 1)
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## Edge cases

- Length 1 → true.
- Mismatch at the outermost pair → returns after one call.

---

## Common mistakes

1. `r = len(s) − 1` as a Python default argument: it would be evaluated once at definition time, so use `None`.
2. Passing `s[1:-1]` instead of indices (O(n²)).

---

## Follow-ups

1. Palindrome ignoring non-alphanumerics and case.
2. Count the palindromic substrings.

<details><summary>Answer sketches</summary>

**#1:** In `f(l, r)`: if `s[l]` isn't alnum, return `f(l + 1, r)`; same for `r`; compare `lower()`.

**#2:** Expand around each centre (O(n²)), or DP on `isPal[l][r]` ([Part 28](../28-dynamic-programming/README.md)).
</details>

---

## Flashcards

**Recursive palindrome definition?** #flashcard
s[l] == s[r] and isPal(l + 1, r − 1); base l >= r → true.

**Python default-arg trap?** #flashcard
Defaults are evaluated once; use None and compute inside.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
