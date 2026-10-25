---
module: striver-a2z/20-bit-manipulation
lesson: 3
topic: Check if a Number is Odd
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-a-number-is-odd-or-not?category=bit-fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits]
---
# 3. Check if a Number is Odd

← [Check if the i-th Bit is Set](02-check-if-the-i-th-bit-is-set.md) · [Part 20 index](README.md) · Next → [Check if a Number is Power of 2](04-check-if-a-number-is-power-of-2.md)

> [!abstract] Problem at a glance
> **Task:** Return whether `n` is odd using bit operations.
> **Key insight:** Every power of two except 2⁰ is even, so parity is decided entirely by bit 0: `n & 1`. In two's complement this also works for negatives.
> **Difficulty:** Easy · **Pattern:** LSB test
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-a-number-is-odd-or-not?category=bit-fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 3 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Modulo](#3-modulo) · [4. AND with 1](#4-and-with-1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer `n`, return `true` if `n` is odd, otherwise `false`.

| Input | Output | Why |
|---|---|---|
| `n = 7` | `true` | 111₂ |
| `n = 10` | `false` | 1010₂ |
| `n = -3` | `true` | two's complement ends in 1 |

**Constraints:** `−10⁹ ≤ n ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Modulo | n % 2 != 0 | O(1) | O(1) |
| AND with 1 | n & 1 | O(1) | O(1) |

> [!tip] Interview angle
> Trivial on its own — the follow-up is why `n % 2 == 1` is wrong for negatives in C++/Java (`-3 % 2 == -1`) while `n & 1` is correct.

---

## 3. Modulo

**Intuition.** Correct if you compare with `!= 0`. `== 1` fails for negative n in C/C++/Java because `%` keeps the dividend's sign.

```python
def is_odd_mod(n):
    return n % 2 != 0
```

**Complexity:** time **O(1)**, space **O(1)**.

---

## 4. AND with 1

**Intuition.** `n = Σ bᵢ·2ⁱ`; every term with i ≥ 1 is even, so n is odd iff b₀ = 1. Two's complement of a negative odd number also ends in 1.

**C++**
```cpp
bool isOdd(int n) {
    return (n & 1) == 1;
}
```

**Java**
```java
static boolean isOdd(int n) {
    return (n & 1) == 1;
}
```

**Python**
```python
def is_odd(n):
    return n & 1 == 1
```

**Complexity:** time **O(1)**, space **O(1)** — single AND.

---

## Edge cases

- 0 is even.
- Negative numbers — `n & 1` still works.

---

## Common mistakes

1. `n % 2 == 1` for negatives in C++/Java.
2. `n & 1 == 1` without parentheses in C/C++/Java (`==` binds tighter).

---

## Follow-ups

1. n mod 2ᵏ for non-negative n.
2. Is n divisible by 4?

<details><summary>Answer sketches</summary>

**#1:** `n & ((1 << k) − 1)`.

**#2:** `(n & 3) == 0`.
</details>

---

## Flashcards

**Parity via bits?** #flashcard
`n & 1` — 1 means odd, also for negatives in two's complement.

**n mod 2ᵏ (n ≥ 0)?** #flashcard
`n & ((1 << k) − 1)`.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
