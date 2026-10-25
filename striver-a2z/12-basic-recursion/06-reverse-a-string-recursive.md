---
module: striver-a2z/12-basic-recursion
lesson: 6
topic: Reverse a String (Recursive)
difficulty: Easy
source: https://takeuforward.org/learning/dsa/reverse-a-string-i?category=basic-recursion&source=strivers-a2z-dsa-sheet
tags: [striver, basic-recursion, recursion, strings, two-pointers]
---
# 6. Reverse a String (Recursive)

← [Sum of Array Elements](05-sum-of-array-elements.md) · [Part 12 index](README.md) · Next → [Check if String is Palindrome or Not](07-check-if-string-is-palindrome.md)

> [!abstract] Problem at a glance
> **Task:** Return the reverse of string `s`, using recursion.
> **Key insight:** Swap the ends and recurse inward on `(l + 1, r − 1)`, stopping at `l ≥ r`. This is the two-pointer loop from Part 11, written as recursion.
> **Difficulty:** Easy · **Pattern:** Two-ended recursion
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-a-string-i?category=basic-recursion&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — last char + reverse(rest)](#3-brute--last-char--reverserest) · [4. Optimal — swap ends, recurse inward](#4-optimal--swap-ends-recurse-inward) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s`, return it reversed. Use recursion.

| Input | Output | Why |
|---|---|---|
| `s = "hello"` | `"olleh"` |  |
| `s = "a"` | `"a"` |  |
| `s = "ab"` | `"ba"` |  |

**Constraints:** `1 ≤ n ≤ 10³`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — last char + reverse(rest) | s[-1] + f(s[:-1]) | O(n²) | O(n²) |
| Optimal — swap ends, recurse inward | swap(l, r); f(l + 1, r − 1) | O(n) | O(n) stack + O(n) buffer |

---

## 3. Brute — last char + reverse(rest)

**Intuition.** Each level slices and concatenates, which costs O(n) per level.

```python
def rev_concat(s):
    if len(s) <= 1:
        return s
    return s[-1] + rev_concat(s[:-1])
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 4. Optimal — swap ends, recurse inward

**Intuition.** Work on a mutable copy: a `char` list in Python, `char[]` in Java, or the `std::string` itself in C++. Each call fixes one pair. The base `l >= r` covers the middle char (odd n) and the crossing point (even n).

**Algorithm**

1. Copy `s` into a mutable buffer `b`.
2. `f(l, r)`: if `l >= r` return; swap `b[l]`, `b[r]`; `f(l + 1, r − 1)`.
3. Call `f(0, n − 1)`, return `b` as a string.

**Dry run** — `hello`: swap(0, 4) `oellh` → swap(1, 3) `olleh` → l = r = 2, stop.

**C++**
```cpp
void revHelper(string& s, int l, int r) {
    if (l >= r) return;
    swap(s[l], s[r]);
    revHelper(s, l + 1, r - 1);
}
string reverseString(string s) {
    revHelper(s, 0, (int)s.size() - 1);
    return s;
}
```

**Java**
```java
static void revHelper(char[] b, int l, int r) {
    if (l >= r) return;
    char t = b[l]; b[l] = b[r]; b[r] = t;
    revHelper(b, l + 1, r - 1);
}
static String reverseString(String s) {
    char[] b = s.toCharArray();
    revHelper(b, 0, b.length - 1);
    return new String(b);
}
```

**Python**
```python
def reverse_string(s):
    b = list(s)
    def f(l, r):
        if l >= r:
            return
        b[l], b[r] = b[r], b[l]
        f(l + 1, r - 1)
    f(0, len(b) - 1)
    return "".join(b)
```

**Complexity:** time **O(n)**, space **O(n) stack + O(n) buffer** — n/2 calls; the depth is n/2.

---

## Edge cases

- Length 1 → unchanged.
- Even vs odd length: both stop at `l >= r`.

---

## Common mistakes

1. Base case `l == r` only: for even n the pointers cross and never become equal → infinite recursion / out of bounds.
2. Recursing with `f(l + 1, r)`, which moves only one side.

---

## Follow-ups

1. Reverse using a single index parameter.
2. Reverse the words of a sentence recursively.

<details><summary>Answer sketches</summary>

**#1:** `f(i)`: if `i >= n/2` return; swap `b[i]`, `b[n−1−i]`; `f(i + 1)`.

**#2:** Split; `f(words, i) = f(words, i + 1) + [words[i]]`, or two-ended on the word list.
</details>

---

## Flashcards

**Two-ended recursion base case?** #flashcard
l >= r (covers both odd and even lengths).

**Why is `s[-1] + f(s[:-1])` O(n²)?** #flashcard
Each level slices and concatenates O(n) chars.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
