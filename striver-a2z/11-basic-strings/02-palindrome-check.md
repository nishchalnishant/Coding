---
module: striver-a2z/11-basic-strings
lesson: 2
topic: Palindrome Check
difficulty: Easy
source: https://takeuforward.org/learning/dsa/palindrome-check?category=basic-strings&source=strivers-a2z-dsa-sheet
tags: [striver, basic-strings, strings, two-pointers]
---
# 2. Palindrome Check

← [Reverse a String](01-reverse-a-string.md) · [Part 11 index](README.md) · Next → [Largest Odd Number in a String](03-largest-odd-number-in-a-string.md)

> [!abstract] Problem at a glance
> **Task:** Return true if string `s` reads the same forwards and backwards.
> **Key insight:** Compare `s[l]` with `s[r]` while moving inward. The first mismatch means false, and you never build a reversed copy.
> **Difficulty:** Easy · **Pattern:** Two pointers (opposite ends)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/palindrome-check?category=basic-strings&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — compare with reverse](#3-brute--compare-with-reverse) · [4. Optimal — two pointers](#4-optimal--two-pointers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s`, return `true` if it is a palindrome, i.e. `s[i] == s[n−1−i]` for every `i`.

| Input | Output | Why |
|---|---|---|
| `s = "hannah"` | `true` |  |
| `s = "aabbaaa"` | `false` | s[0] = a, s[6] = a ✓; s[1] = a, s[5] = a ✓; s[2] = b, s[4] = a ✗ |
| `s = "a"` | `true` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, lowercase letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — compare with reverse | `s == s[::-1]` | O(n) | O(n) |
| Optimal — two pointers | compare ends, move inward | O(n) | O(1) |

---

## 3. Brute — compare with reverse

**Intuition.** Build the reversed string and compare. It's one line, but it allocates n chars and always does the full comparison.

```python
def is_pal_rev(s):
    return s == s[::-1]
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Optimal — two pointers

**Intuition.** A palindrome is its own mirror, so check mirrored pairs and stop at the first one that differs.

**Algorithm**

1. `l = 0`, `r = n − 1`.
2. While `l < r`: if `s[l] != s[r]` return false; `l++`, `r--`.
3. Return true.

**Dry run** — `hannah`: (h, h) (a, a) (n, n) → true.

**C++**
```cpp
bool palindromeCheck(string& s) {
    int l = 0, r = (int)s.size() - 1;
    while (l < r)
        if (s[l++] != s[r--]) return false;
    return true;
}
```

**Java**
```java
static boolean palindromeCheck(String s) {
    int l = 0, r = s.length() - 1;
    while (l < r)
        if (s.charAt(l++) != s.charAt(r--)) return false;
    return true;
}
```

**Python**
```python
def palindrome_check(s):
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True
```

**Complexity:** time **O(n)**, space **O(1)** — at most n/2 comparisons, with early exit.

---

## Edge cases

- Length 1 → true.
- Odd length: the middle char is never compared, and doesn't need to be.

---

## Common mistakes

1. Comparing `s[i]` with `s[n − i]`, which is off by one.
2. In Java, comparing two `String` objects with `==` instead of `.equals` when you use the reverse approach.

---

## Follow-ups

1. Valid Palindrome (LC 125): ignore non-alphanumerics and case.
2. Valid Palindrome II (LC 680): may delete one char.
3. Longest palindromic substring.

<details><summary>Answer sketches</summary>

**#1:** Skip with `while l < r and not s[l].isalnum(): l += 1` (same on the right), and compare `lower()`.

**#2:** On the first mismatch, return `isPal(l+1, r) or isPal(l, r−1)`. O(n).

**#3:** Expand around each of the 2n−1 centres, O(n²); covered in [Part 17](../17-strings-basic-medium/README.md).
</details>

---

## Flashcards

**Palindrome check in O(1) space?** #flashcard
Two pointers, compare mirrored chars, exit on the first mismatch.

**Palindrome after deleting at most one char?** #flashcard
On the first mismatch, try skipping the left or the right char.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String algorithms](../../02-algorithms/02-string-algorithms.md) · [Concept: basic strings](../07-concept-basics/04-basic-string.md)
