---
module: striver-a2z/08-basic-maths
lesson: 4
topic: Palindrome Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/palindrome-number?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, digits, palindrome]
---
# 4. Palindrome Number

← [Reverse a Number](03-reverse-a-number.md) · [Part 8 index](README.md) · Next → [Return the Largest Digit in a Number](05-return-the-largest-digit-in-a-number.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `n` reads the same forwards and backwards.
> **Key insight:** Reverse only the back half of the digits and compare it with the front half. No overflow is possible.
> **Difficulty:** Easy · **Pattern:** Digit loop + reverse · **Also on:** LC 9
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/palindrome-number?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — string compare](#3-brute--string-compare) · [4. Better — full reverse](#4-better--full-reverse) · [5. Optimal — reverse half](#5-optimal--reverse-half) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer `n`, return `true` if its decimal representation is a palindrome. Negative numbers are not palindromes (`-121` reads `121-`).

| Input | Output | Why |
|---|---|---|
| `n = 121` | `true` |  |
| `n = 123` | `false` |  |
| `n = -121` | `false` | the minus sign breaks symmetry |
| `n = 10` | `false` | reverse is 01 = 1 |
| `n = 0` | `true` |  |

**Constraints:** `-2³¹ ≤ n ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — string compare | `s == s[::-1]` | O(d) | O(d) |
| Better — full reverse | reverse all digits and compare | O(log₁₀ n) | O(1) |
| Optimal — reverse half | stop when `rev ≥ n` | O(log₁₀ n) | O(1) |

---

## 3. Brute — string compare

**Intuition.** Compare the string with its reverse.

```python
def is_pal_str(n):
    s = str(n)
    return s == s[::-1]
```

**Complexity:** time **O(d)**, space **O(d)**.

---

## 4. Better — full reverse

**Intuition.** Reuse *Reverse a Number*. If the reverse equals the original, it's a palindrome. In C++/Java the reverse can overflow, so use 64-bit.

```python
def is_pal_full(n):
    if n < 0:
        return False
    orig, rev = n, 0
    while n > 0:
        rev = rev * 10 + n % 10
        n //= 10
    return rev == orig
```

**Complexity:** time **O(log₁₀ n)**, space **O(1)**.

---

## 5. Optimal — reverse half

**Intuition.** Move digits from `n` onto `rev` until `rev` is at least as big as what's left. Now `n` holds the front half and `rev` holds the reversed back half. For an odd digit count, the middle digit ends up on `rev`, so drop it with `rev // 10`.

**Algorithm**

1. If `n < 0`, or `n` ends in 0 but isn't 0, return false. A number ending in 0 would need to start with 0.
2. While `n > rev`: `rev = rev * 10 + n % 10`; `n //= 10`.
3. Return `n == rev or n == rev // 10`.

**Dry run** — `n = 12321`

| n | rev |
|---|---|
| 12321 | 0 |
| 1232 | 1 |
| 123 | 12 |
| 12 | 123 | ← stop: n ≤ rev

`n = 12`, `rev // 10 = 12` → palindrome.

**C++**
```cpp
bool isPalindrome(int n) {
    if (n < 0 || (n % 10 == 0 && n != 0)) return false;
    int rev = 0;
    while (n > rev) {
        rev = rev * 10 + n % 10;
        n /= 10;
    }
    return n == rev || n == rev / 10;
}
```

**Java**
```java
static boolean isPalindrome(int n) {
    if (n < 0 || (n % 10 == 0 && n != 0)) return false;
    int rev = 0;
    while (n > rev) {
        rev = rev * 10 + n % 10;
        n /= 10;
    }
    return n == rev || n == rev / 10;
}
```

**Python**
```python
def is_palindrome(n):
    if n < 0 or (n % 10 == 0 and n != 0):
        return False
    rev = 0
    while n > rev:
        rev = rev * 10 + n % 10
        n //= 10
    return n == rev or n == rev // 10
```

**Complexity:** time **O(log₁₀ n)**, space **O(1)** — half the digits are processed, and `rev` never exceeds about √INT_MAX, so 32-bit is safe.

---

## Edge cases

- Negative → false.
- Trailing zero (`10`, `100`) → false, except `0` itself.
- Odd length: the middle digit is discarded with `rev // 10`.
- Single digit → true.

---

## Common mistakes

1. Running the half-reverse without the trailing-zero guard. For `10`: step 1 → `n = 1, rev = 0`; step 2 → `n = 0, rev = 1`; then `rev // 10 == 0 == n` wrongly returns true.
2. Using 32-bit full reverse on a number like `1 000 000 009`. It overflows and the comparison breaks.

---

## Follow-ups

1. Check whether `n` is a palindrome in binary.
2. Nearest palindrome (LC 564).

<details><summary>Answer sketches</summary>

**#1:** Reverse its bits up to the highest set bit and compare, or build the bit string and compare it with its reverse.

**#2:** Mirror the left half; try the half, half ± 1, and the edge forms `99…9` and `10…01`; pick the closest. A hard problem.
</details>

---

## Flashcards

**Half-reverse palindrome loop condition?** #flashcard
`while n > rev` — stop once the reversed back half has caught up with the front.

**Why the trailing-zero guard?** #flashcard
A number ending in 0 would have to start with 0, which is impossible unless n = 0. Without the guard, the half method returns true for 10.

**Final comparison for odd length?** #flashcard
`n == rev // 10`, which drops the middle digit.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
