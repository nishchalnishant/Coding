---
module: striver/20-bit-manipulation
lesson: 12
topic: Divide Two Integers
difficulty: Medium
source: https://takeuforward.org/learning/dsa/divide-two-numbers-without-multiplication-and-division?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, bit-manipulation, bits, math]
---
# 12. Divide Two Integers

← [Single Number III](11-single-number-iii.md) · [Part 20 index](README.md) · Next → [Power Set (Bit Manipulation)](13-power-set.md)

> [!abstract] Problem at a glance
> **Task:** Compute `dividend / divisor` truncated toward zero without `*`, `/` or `%`, clamped to 32-bit.
> **Key insight:** Repeated subtraction is O(quotient). Instead subtract the largest `divisor · 2ᵏ` (built by left shifts) that fits — that's long division in base 2, O(log² n) or O(log n).
> **Difficulty:** Medium · **Pattern:** Shift-and-subtract (binary long division) · **Also on:** [LC 29](https://leetcode.com/problems/divide-two-integers/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/divide-two-numbers-without-multiplication-and-division?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Repeated subtraction](#3-repeated-subtraction) · [4. Shift and subtract](#4-shift-and-subtract) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `dividend` and `divisor`, divide without using multiplication, division or mod. Truncate toward zero. If the quotient is outside `[−2³¹, 2³¹ − 1]`, return `2³¹ − 1`.

| Input | Output | Why |
|---|---|---|
| `dividend = 10, divisor = 3` | `3` |  |
| `dividend = 7, divisor = -3` | `-2` | truncate toward zero |
| `dividend = -2147483648, divisor = -1` | `2147483647` | overflow → clamp |

**Constraints:** `−2³¹ ≤ dividend, divisor ≤ 2³¹ − 1`, `divisor ≠ 0`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Repeated subtraction | subtract divisor until it doesn't fit | O(quotient) | O(1) |
| Shift and subtract | subtract the biggest divisor·2ᵏ that fits | O(log² n) | O(1) |

> [!tip] Interview angle
> Ask about overflow up front (the only case is `INT_MIN / −1`). Work on absolute values in 64-bit, compute the sign with XOR of signs, and explain the doubling loop as binary long division.

---

## 3. Repeated subtraction

**Intuition.** Correct but O(2³¹) for `INT_MAX / 1` — TLE.

```python
def divide_sub(dividend, divisor):
    if dividend == -2**31 and divisor == -1:
        return 2**31 - 1
    neg = (dividend < 0) != (divisor < 0)
    a, b, q = abs(dividend), abs(divisor), 0
    while a >= b:
        a -= b
        q += 1
    return -q if neg else q
```

**Complexity:** time **O(quotient)**, space **O(1)**.

---

## 4. Shift and subtract

**Intuition.** Any quotient is a sum of powers of two. For the current remainder `a`, find the largest k with `b << k ≤ a`, subtract it and add `1 << k` to the quotient. Repeat. Each outer step clears at least the top bit of the remaining quotient.

**Algorithm**

1. Handle `INT_MIN / −1` → INT_MAX.
2. `neg = (dividend < 0) ^ (divisor < 0)`; `a, b = |dividend|, |divisor|` as 64-bit.
3. While `a ≥ b`: grow k while `b << (k+1) ≤ a`; `a −= b << k`; `q += 1 << k`.
4. Return `−q` if neg else `q`.

**Dry run** — 22 / 3: 3<<2 = 12 ≤ 22 < 24 → a = 10, q = 4; 3<<1 = 6 ≤ 10 → a = 4, q = 6; 3 ≤ 4 → a = 1, q = 7. → 7.

**O(log n) variant:** loop k from 31 down to 0 once: if `(a >> k) ≥ b`, then `a −= b << k`, `q |= 1 << k`. Uses only shifts on the dividend, no inner loop.

**C++**
```cpp
int divide(int dividend, int divisor) {
    if (dividend == INT_MIN && divisor == -1) return INT_MAX;
    bool neg = (dividend < 0) ^ (divisor < 0);
    long long a = llabs((long long)dividend), b = llabs((long long)divisor), q = 0;
    while (a >= b) {
        int k = 0;
        while (a >= (b << (k + 1))) k++;
        a -= b << k;
        q += 1LL << k;
    }
    return (int)(neg ? -q : q);
}
```

**Java**
```java
static int divide(int dividend, int divisor) {
    if (dividend == Integer.MIN_VALUE && divisor == -1) return Integer.MAX_VALUE;
    boolean neg = (dividend < 0) ^ (divisor < 0);
    long a = Math.abs((long) dividend), b = Math.abs((long) divisor), q = 0;
    while (a >= b) {
        int k = 0;
        while (a >= (b << (k + 1))) k++;
        a -= b << k;
        q += 1L << k;
    }
    return (int) (neg ? -q : q);
}
```

**Python**
```python
def divide(dividend, divisor):
    if dividend == -2**31 and divisor == -1:
        return 2**31 - 1
    neg = (dividend < 0) != (divisor < 0)
    a, b, q = abs(dividend), abs(divisor), 0
    while a >= b:
        k = 0
        while a >= b << (k + 1):
            k += 1
        a -= b << k
        q += 1 << k
    return -q if neg else q
```

**Complexity:** time **O(log² n)**, space **O(1)** — ≤ 31 outer steps, each with ≤ 31 doublings.

---

## Edge cases

- `INT_MIN / −1` → clamp to INT_MAX.
- `|INT_MIN|` doesn't fit in int — use 64-bit (or work in negatives).
- dividend = 0.
- divisor = ±1.

---

## Common mistakes

1. `abs(INT_MIN)` in 32-bit — still negative.
2. Rounding toward −∞ instead of 0 for negative results.
3. `b << (k+1)` overflowing 32-bit — use 64-bit.

---

## Follow-ups

1. No 64-bit allowed.
2. Return the remainder too.

<details><summary>Answer sketches</summary>

**#1:** Convert both to **negative** (range is larger) and run the doubling with `≥`/`≤` flipped, guarding `b + b` against overflow with `b ≥ INT_MIN/2`.

**#2:** It's the final `a` with the dividend's sign.
</details>

---

## Flashcards

**Divide without * / %: idea?** #flashcard
Subtract the largest divisor·2ᵏ that fits; add 2ᵏ to the quotient.

**The only overflow case?** #flashcard
INT_MIN / −1 → return INT_MAX.

**Sign of the quotient?** #flashcard
`(dividend < 0) ^ (divisor < 0)`.

**Interview track →** [Bit manipulation deep-dive](../../02-algorithms/17-bit-manipulation.md)
