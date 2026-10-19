---
module: striver/08-basic-maths
lesson: 3
topic: Reverse a Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/reverse-a-number?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, digits, overflow]
---
# 3. Reverse a Number

← [Count Number of Odd Digits in a Number](02-count-number-of-odd-digits-in-a-number.md) · [Part 8 index](README.md) · Next → [Palindrome Number](04-palindrome-number.md)

> [!abstract] Problem at a glance
> **Task:** Return the integer whose digits are those of `n` in reverse order.
> **Key insight:** `rev = rev * 10 + n % 10` shifts the reversed number left by one digit and appends the next digit.
> **Difficulty:** Easy · **Pattern:** Digit loop + build · **Also on:** LC 7 (Reverse Integer, signed + overflow)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-a-number?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — string reverse](#3-brute--string-reverse) · [4. Optimal — arithmetic build](#4-optimal--arithmetic-build) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `n`, return the number formed by reversing its digits. Leading zeros in the result are dropped (`1200 → 21`).

| Input | Output | Why |
|---|---|---|
| `n = 25` | `52` | swap |
| `n = 123` | `321` |  |
| `n = 1200` | `21` | trailing zeros become leading zeros and vanish |
| `n = 0` | `0` |  |

**Constraints:** `0 ≤ n ≤ 10⁹`. The reverse of `1 000 000 009` is `9 000 000 001`, which **does not fit in 32 bits**, so return a 64-bit value.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — string reverse | `int(str(n)[::-1])` | O(d) | O(d) |
| Optimal — arithmetic build | `rev = rev*10 + d` | O(log₁₀ n) | O(1) |

> [!tip] Interview angle
> This problem tests overflow awareness. Say "the reverse can exceed INT_MAX, so I'll accumulate in a long" before you write the loop.

---

## 3. Brute — string reverse

**Intuition.** Reverse the string and parse it back. Parsing drops leading zeros for free.

```python
def reverse_str(n):
    return int(str(n)[::-1])
```

**Complexity:** time **O(d)**, space **O(d)**.

---

## 4. Optimal — arithmetic build

**Intuition.** Take digits from the right with `% 10` and push them onto the right of `rev`. Multiplying `rev` by 10 moves everything one place left to make room.

**Algorithm**

1. `rev = 0` (64-bit).
2. While `n > 0`: `rev = rev * 10 + n % 10`; `n //= 10`.
3. Return `rev`.

**Dry run** — `n = 1200`

| d | rev | n after |
|---|---|---|
| 0 | 0 | 120 |
| 0 | 0 | 12 |
| 2 | 2 | 1 |
| 1 | 21 | 0 |

The zeros arrive first, while `rev` is still 0, so they never show up.

**Signed 32-bit variant (LC 7):** return 0 if the result overflows. Before `rev = rev*10 + d`, check `rev > (INT_MAX - d) / 10` (and the mirror check for negatives), or accumulate in 64-bit and compare at the end.

**C++**
```cpp
long long reverseNumber(int n) {
    long long rev = 0;
    while (n > 0) {
        rev = rev * 10 + n % 10;
        n /= 10;
    }
    return rev;
}
```

**Java**
```java
static long reverseNumber(int n) {
    long rev = 0;
    while (n > 0) {
        rev = rev * 10 + n % 10;
        n /= 10;
    }
    return rev;
}
```

**Python**
```python
def reverse_number(n):
    rev = 0
    while n > 0:
        rev = rev * 10 + n % 10
        n //= 10
    return rev
```

**Complexity:** time **O(log₁₀ n)**, space **O(1)** — one pass over the digits; `rev` is a single 64-bit accumulator.

---

## Edge cases

- Trailing zeros: `1200 → 21`.
- `n = 0` → 0.
- Overflow: `1 000 000 009 → 9 000 000 001 > 2³¹ − 1`.
- Negative input (LC 7): reverse `abs(n)` and reapply the sign. In C++, `abs(INT_MIN)` overflows.

---

## Common mistakes

1. Accumulating in `int`, which silently wraps on overflow.
2. Writing `rev = rev + d * 10` (wrong order) instead of `rev * 10 + d`.
3. Trying to keep leading zeros. Integers can't hold them, so return a string if they matter.

---

## Follow-ups

1. Reverse with a 32-bit overflow check (LC 7).
2. Reverse in base 2 (reverse the bits).

<details><summary>Answer sketches</summary>

**#1:** Before each step: `if rev > (INT_MAX - d) // 10: return 0`. For negatives, use C++ truncating `%` and the mirror check against INT_MIN.

**#2:** Same build: `rev = (rev << 1) | (n & 1)`; `n >>= 1`, run for a fixed 32 iterations.
</details>

---

## Flashcards

**Reverse-build recurrence?** #flashcard
`rev = rev * 10 + n % 10`, then `n //= 10`.

**Why does 1200 reverse to 21?** #flashcard
The zeros are added while `rev = 0`, so `0 * 10 + 0` is still 0.

**Overflow pre-check for reverse?** #flashcard
`rev > (INT_MAX - d) / 10` means the next step would overflow.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
