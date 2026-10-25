---
module: striver-a2z/20-bit-manipulation
lesson: 4
topic: Check if a Number is Power of 2
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-a-number-is-power-of-2-or-not?category=bit-fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits]
---
# 4. Check if a Number is Power of 2

← [Check if a Number is Odd](03-check-if-a-number-is-odd.md) · [Part 20 index](README.md) · Next → [Count the Number of Set Bits](05-count-the-number-of-set-bits.md)

> [!abstract] Problem at a glance
> **Task:** Return whether `n` is a power of two.
> **Key insight:** A power of two has exactly one set bit. `n − 1` flips that bit to 0 and all bits below it to 1, so `n & (n − 1) == 0` exactly when n has one set bit — plus the guard `n > 0`.
> **Difficulty:** Easy · **Pattern:** n & (n − 1) clears lowest set bit · **Also on:** [LC 231](https://leetcode.com/problems/power-of-two/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-a-number-is-power-of-2-or-not?category=bit-fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Repeated division](#3-repeated-division) · [4. Count set bits](#4-count-set-bits) · [5. n & (n − 1)](#5-n--n--1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer `n`, return `true` if there exists an integer `x ≥ 0` with `n == 2ˣ`.

| Input | Output | Why |
|---|---|---|
| `n = 16` | `true` | 10000₂ |
| `n = 6` | `false` | 110₂ |
| `n = 0` | `false` |  |

**Constraints:** `−2³¹ ≤ n ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Repeated division | divide by 2 while even | O(log n) | O(1) |
| Count set bits | popcount(n) == 1 | O(log n) | O(1) |
| n & (n − 1) | one set bit ⇔ clearing it gives 0 | O(1) | O(1) |

> [!tip] Interview angle
> The expected answer is the one-liner; what's being tested is the `n > 0` guard (0 and INT_MIN both satisfy `n & (n−1) == 0` style tricks incorrectly) and that you can explain *why* `n & (n − 1)` clears the lowest set bit.

---

## 3. Repeated division

**Intuition.** Keep halving while n is even; a power of two ends at exactly 1.

```python
def is_pow2_div(n):
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1
```

**Complexity:** time **O(log n)**, space **O(1)**.

---

## 4. Count set bits

**Intuition.** Powers of two are exactly the positive numbers with one set bit.

```python
def is_pow2_pop(n):
    return n > 0 and bin(n).count('1') == 1
```

**Complexity:** time **O(log n)**, space **O(1)**.

---

## 5. n & (n − 1)

**Intuition.** Subtracting 1 turns the lowest set bit into 0 and every bit below it into 1; bits above are untouched. ANDing with the original therefore clears exactly the lowest set bit. If that leaves 0, there was only one set bit.

**Dry run** — n = 8: 1000 & 0111 = 0 → true. n = 12: 1100 & 1011 = 1000 ≠ 0 → false.

**Alternative:** `n > 0 && (n & −n) == n` — `n & −n` isolates the lowest set bit.

**C++**
```cpp
bool isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```

**Java**
```java
static boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```

**Python**
```python
def is_power_of_two(n):
    return n > 0 and n & (n - 1) == 0
```

**Complexity:** time **O(1)**, space **O(1)** — constant number of operations.

---

## Edge cases

- n = 0 → false.
- Negative n → false (INT_MIN is a single set bit in two's complement!).
- n = 1 = 2⁰ → true.

---

## Common mistakes

1. Forgetting `n > 0`.
2. Precedence: `n & (n - 1) == 0` in C++/Java means `n & ((n-1) == 0)`.

---

## Follow-ups

1. Power of four (LC 342).
2. Next power of two ≥ n.

<details><summary>Answer sketches</summary>

**#1:** Power of two **and** the bit is at an even position: `(n & 0x55555555) != 0`.

**#2:** Smear bits right: `n−−; n |= n>>1; n |= n>>2; … n |= n>>16; n++`.
</details>

---

## Flashcards

**What does n & (n − 1) do?** #flashcard
Clears the lowest set bit.

**Power-of-two test?** #flashcard
`n > 0 && (n & (n − 1)) == 0`.

**What does n & −n give?** #flashcard
Only the lowest set bit.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
