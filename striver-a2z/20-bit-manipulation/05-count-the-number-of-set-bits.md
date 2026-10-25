---
module: striver-a2z/20-bit-manipulation
lesson: 5
topic: Count the Number of Set Bits
difficulty: Easy
source: https://takeuforward.org/learning/dsa/count-the-number-of-set-bits?category=bit-fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits, kernighan]
---
# 5. Count the Number of Set Bits

← [Check if a Number is Power of 2](04-check-if-a-number-is-power-of-2.md) · [Part 20 index](README.md) · Next → [Set the Rightmost Unset Bit](06-set-the-rightmost-unset-bit.md)

> [!abstract] Problem at a glance
> **Task:** Return the number of 1 bits in the binary representation of `n`.
> **Key insight:** Brian Kernighan: `n &= n − 1` deletes one set bit per iteration, so the loop runs popcount(n) times instead of 32.
> **Difficulty:** Easy · **Pattern:** Kernighan's bit count · **Also on:** [LC 191](https://leetcode.com/problems/number-of-1-bits/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-the-number-of-set-bits?category=bit-fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Check every bit](#3-check-every-bit) · [4. Brian Kernighan](#4-brian-kernighan) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `n`, return the number of set bits (Hamming weight).

| Input | Output | Why |
|---|---|---|
| `n = 11` | `3` | 1011₂ |
| `n = 128` | `1` | 10000000₂ |
| `n = 2147483645` | `30` |  |

**Constraints:** `0 ≤ n ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Check every bit | add n & 1, shift right | O(log n) | O(1) |
| Brian Kernighan | n &= n − 1 until 0 | O(popcount) | O(1) |

> [!tip] Interview angle
> Give the shift loop, then Kernighan as the improvement, and mention the built-ins (`__builtin_popcount`, `Integer.bitCount`, `int.bit_count()`). Interviewers like hearing the iteration count is the number of set bits.

---

## 3. Check every bit

**Intuition.** Look at bit 0, shift, repeat until n is 0. Use an unsigned / logical shift (`>>>` in Java) if n can be negative, or the loop never ends.

```python
def count_shift(n):
    c = 0
    while n:
        c += n & 1
        n >>= 1
    return c
```

**Complexity:** time **O(log n)**, space **O(1)**.

---

## 4. Brian Kernighan

**Intuition.** Each `n & (n − 1)` clears the lowest set bit (see power-of-two). Count how many times you can do that before n hits 0.

**Dry run** — 11 = 1011 → 1010 → 1000 → 0000: 3 iterations.

**C++**
```cpp
int countSetBits(int n) {
    int c = 0;
    while (n) {
        n &= n - 1;
        c++;
    }
    return c;
}
```

**Java**
```java
static int countSetBits(int n) {
    int c = 0;
    while (n != 0) {
        n &= n - 1;
        c++;
    }
    return c;
}
```

**Python**
```python
def count_set_bits(n):
    c = 0
    while n:
        n &= n - 1
        c += 1
    return c
```

**Complexity:** time **O(popcount)**, space **O(1)** — one iteration per set bit, ≤ 31.

---

## Edge cases

- n = 0 → 0.
- All 31 bits set.
- Negative input in Java/C++ — Kernighan still terminates (≤ 32 iterations); `>>` loop does not.

---

## Common mistakes

1. Using arithmetic `>>` on negative numbers → infinite loop (sign bit keeps refilling).
2. Counting via `n % 2` on negatives.

---

## Follow-ups

1. Total set bits in all numbers 1…n (Striver/GFG variant).
2. Counting bits for every i in 0…n (LC 338).
3. Hamming distance between x and y (LC 461).

<details><summary>Answer sketches</summary>

**#1:** Let x = highest power of 2 ≤ n, at bit position b. Numbers 1…2ᵇ − 1 contribute b·2ᵇ⁻¹; the MSB is set in n − 2ᵇ + 1 numbers; recurse on n − 2ᵇ. O(log² n), or O(log n) by counting each bit: bit i is set `(n+1) / 2ⁱ⁺¹ · 2ⁱ + max(0, (n+1) mod 2ⁱ⁺¹ − 2ⁱ)` times.

**#2:** DP: `bits[i] = bits[i >> 1] + (i & 1)` or `bits[i & (i−1)] + 1` — O(n).

**#3:** popcount(x ^ y).
</details>

---

## Flashcards

**Kernighan's loop?** #flashcard
`while n: n &= n − 1; c += 1` — runs popcount times.

**Built-in popcount (C++/Java/Py)?** #flashcard
`__builtin_popcount`, `Integer.bitCount`, `int.bit_count()`.

**bits[i] DP for LC 338?** #flashcard
`bits[i >> 1] + (i & 1)`.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
