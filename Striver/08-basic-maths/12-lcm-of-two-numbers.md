---
module: striver/08-basic-maths
lesson: 12
topic: LCM of Two Numbers
difficulty: Easy
source: https://takeuforward.org/learning/dsa/lcm-of-two-numbers?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, gcd, lcm, overflow]
---
# 12. LCM of Two Numbers

← [GCD of Two Numbers](11-gcd-of-two-numbers.md) · [Part 8 index](README.md) · Next → [Divisors of a Number](13-divisors-of-a-number.md)

> [!abstract] Problem at a glance
> **Task:** Return the least common multiple of `a` and `b`.
> **Key insight:** `lcm · gcd = a · b`, so `lcm = a / gcd(a, b) * b`. Divide first to avoid overflow.
> **Difficulty:** Easy · **Pattern:** Euclid → LCM
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/lcm-of-two-numbers?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — step through multiples](#3-brute--step-through-multiples) · [4. Optimal — via GCD](#4-optimal--via-gcd) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two positive integers `a` and `b`, return the smallest positive integer that both divide.

| Input | Output | Why |
|---|---|---|
| `a = 4, b = 6` | `12` |  |
| `a = 3, b = 5` | `15` | coprime → product |
| `a = 4, b = 12` | `12` | one divides the other |

**Constraints:** `1 ≤ a, b ≤ 10⁹`. The LCM can reach 10¹⁸, so **return 64-bit**.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — step through multiples | try max, 2·max, … | O(min(a,b)) | O(1) |
| Optimal — via GCD | `a / gcd * b` | O(log min(a,b)) | O(1) |

---

## 3. Brute — step through multiples

**Intuition.** Walk through the multiples of the larger number until one is divisible by the smaller. In the worst case (coprime inputs) that takes `min(a, b)` steps.

```python
def lcm_brute(a, b):
    hi, lo = max(a, b), min(a, b)
    m = hi
    while m % lo:
        m += hi
    return m
```

**Complexity:** time **O(min(a,b))**, space **O(1)**.

---

## 4. Optimal — via GCD

**Intuition.** For each prime, the gcd takes the minimum exponent and the lcm takes the maximum. `min + max = sum`, so `gcd · lcm = a · b`. Divide `a` by the gcd *before* multiplying so the intermediate value never exceeds the answer.

**Algorithm**

1. `g = gcd(a, b)`.
2. Return `(a / g) * b` in 64-bit.

**Dry run** — `a = 4 = 2²`, `b = 6 = 2·3`: g = 2 → 4 / 2 · 6 = **12**.

**Prime-exponent view**

| | 2 | 3 |
|---|---|---|
| 4 | 2 | 0 |
| 6 | 1 | 1 |
| gcd (min) | 1 | 0 → 2 |
| lcm (max) | 2 | 1 → 12 |

**C++**
```cpp
long long lcmOf(long long a, long long b) {
    long long x = a, y = b;
    while (y) { long long t = x % y; x = y; y = t; }
    return a / x * b;
}
```

**Java**
```java
static long lcmOf(long a, long b) {
    long x = a, y = b;
    while (y != 0) { long t = x % y; x = y; y = t; }
    return a / x * b;
}
```

**Python**
```python
def lcm(a, b):
    x, y = a, b
    while y:
        x, y = y, x % y
    return a // x * b
```

**Complexity:** time **O(log min(a,b))**, space **O(1)** — the cost is one gcd; dividing first keeps the intermediate ≤ the answer.

---

## Edge cases

- Coprime inputs → `a · b`. That's the largest possible answer, and it needs 64-bit.
- `a == b` → `a`.
- Either input 0 → the LCM is 0 by convention. Guard it, because gcd would be the other value and the division is still fine, but say so.

---

## Common mistakes

1. Computing `a * b / g`, where `a * b` overflows even when the LCM fits.
2. Returning a 32-bit int.
3. Recomputing the gcd from scratch inside a loop when folding over an array. Reuse the running LCM.

---

## Follow-ups

1. LCM of an array.
2. Count numbers ≤ N divisible by a or b.

<details><summary>Answer sketches</summary>

**#1:** Fold `L = lcm(L, x)`. Values can explode, so take `mod` if one is given, but note you can't take mod before the gcd. Use prime-exponent maxima instead.

**#2:** Inclusion–exclusion: `N/a + N/b − N/lcm(a, b)`.
</details>

---

## Flashcards

**gcd–lcm identity?** #flashcard
gcd(a, b) · lcm(a, b) = a · b.

**Overflow-safe LCM?** #flashcard
a / gcd(a, b) * b — divide first.

**lcm in prime-exponent terms?** #flashcard
The maximum exponent of each prime; gcd takes the minimum.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
