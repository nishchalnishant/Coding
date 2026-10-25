---
module: striver-a2z/11-basic-strings
lesson: 1
topic: Reverse a String
difficulty: Easy
source: https://takeuforward.org/learning/dsa/reverse-a-string-ii?category=basic-strings&source=strivers-a2z-dsa-sheet
tags: [striver, basic-strings, strings, two-pointers]
---
# 1. Reverse a String

← [Part 11 index](README.md) · Next → [Palindrome Check](02-palindrome-check.md)

> [!abstract] Problem at a glance
> **Task:** Reverse the character array `s` in place.
> **Key insight:** This is the array reverse from Part 9 on chars: swap `s[l]` and `s[r]`, move inward, stop at `l ≥ r`.
> **Difficulty:** Easy · **Pattern:** Two pointers (opposite ends) · **Also on:** 344
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-a-string-ii?category=basic-strings&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — reversed copy](#3-brute--reversed-copy) · [4. Optimal — two pointers](#4-optimal--two-pointers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a character array `s`, reverse it in place with O(1) extra memory.

| Input | Output | Why |
|---|---|---|
| `s = ["h","e","l","l","o"]` | `["o","l","l","e","h"]` |  |
| `s = ["H","a","n","n","a","h"]` | `["h","a","n","n","a","H"]` | case is preserved |

**Constraints:** `1 ≤ n ≤ 10⁵`, printable ASCII.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — reversed copy | build a reversed copy, write it back | O(n) | O(n) |
| Optimal — two pointers | swap ends, move inward | O(n) | O(1) |

> [!tip] Interview angle
> It's given as a char array because strings are immutable in Python and Java. Ask whether you can modify the input.

---

## 3. Brute — reversed copy

**Intuition.** Read from the back into a new list, then copy it over `s`. This breaks the O(1)-memory requirement.

```python
def reverse_copy(s):
    s[:] = [s[i] for i in range(len(s) - 1, -1, -1)]
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Optimal — two pointers

**Intuition.** Index `l` and its mirror `n − 1 − l` swap. Stop once the pointers meet or cross.

**Algorithm**

1. `l = 0`, `r = n − 1`.
2. While `l < r`: swap `s[l]`, `s[r]`; `l++`, `r--`.

**Dry run** — `h e l l o` → swap(0, 4) `o e l l h` → swap(1, 3) `o l l e h` → l = r = 2, stop.

**C++**
```cpp
void reverseString(vector<char>& s) {
    int l = 0, r = (int)s.size() - 1;
    while (l < r) swap(s[l++], s[r--]);
}
```

**Java**
```java
static void reverseString(char[] s) {
    int l = 0, r = s.length - 1;
    while (l < r) {
        char t = s[l];
        s[l++] = s[r];
        s[r--] = t;
    }
}
```

**Python**
```python
def reverse_string(s):
    l, r = 0, len(s) - 1
    while l < r:
        s[l], s[r] = s[r], s[l]
        l += 1
        r -= 1
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- Length 1: no swaps.
- Even length: the pointers cross with no shared middle.

---

## Common mistakes

1. `s = s[::-1]` in Python rebinds the local name; the caller's list is unchanged. Use `s[:] = s[::-1]` or `s.reverse()`.
2. Unsigned `size() - 1` underflow in C++ on an empty vector.

---

## Follow-ups

1. Reverse only the vowels (LC 345).
2. Reverse each word, keep the order (LC 557).

<details><summary>Answer sketches</summary>

**#1:** Same two pointers; each side skips non-vowels before swapping.

**#2:** Find each word's `[start, end]` and reverse that range in place.
</details>

---

## Flashcards

**Why does `s = s[::-1]` fail an in-place reverse in Python?** #flashcard
It rebinds the local name. Use `s[:] = …` or `s.reverse()`.

**Reverse-string loop?** #flashcard
while l < r: swap, l++, r--.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String algorithms](../../02-algorithms/02-string-algorithms.md) · [Concept: basic strings](../07-concept-basics/04-basic-string.md)
