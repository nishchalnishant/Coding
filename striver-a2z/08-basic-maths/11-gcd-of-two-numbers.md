---
module: striver-a2z/08-basic-maths
lesson: 11
topic: GCD of Two Numbers
difficulty: Easy
source: https://takeuforward.org/learning/dsa/gcd-of-two-numbers?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, gcd]
---
# 11. GCD of Two Numbers

← [Count of Prime Numbers till N](10-count-of-prime-numbers-till-n.md) · [Part 8 index](README.md) · Next → [LCM of Two Numbers](12-lcm-of-two-numbers.md)

> [!abstract] Problem at a glance
> **Task:** Return the greatest common divisor of `a` and `b`.
> **Key insight:** Euclid: `gcd(a, b) = gcd(b, a mod b)`, and `gcd(a, 0) = a`. The numbers shrink at least by half every two steps → O(log min(a, b)).
> **Difficulty:** Easy · **Pattern:** Euclidean algorithm
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/gcd-of-two-numbers?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — count down](#3-brute--count-down) · [4. Better — subtraction Euclid](#4-better--subtraction-euclid) · [5. Optimal — modulo Euclid](#5-optimal--modulo-euclid) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two positive integers `a` and `b`, return the largest integer that divides both.

| Input | Output | Why |
|---|---|---|
| `a = 4, b = 6` | `2` |  |
| `a = 9, b = 8` | `1` | coprime |
| `a = 12, b = 36` | `12` | one divides the other |
| `a = 7, b = 0` | `7` | gcd(a, 0) = a |

**Constraints:** `0 ≤ a, b ≤ 10⁹`, not both zero.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — count down | try d = min(a,b) … 1 | O(min(a,b)) | O(1) |
| Better — subtraction Euclid | replace larger by larger − smaller | O(max(a,b)) worst | O(1) |
| Optimal — modulo Euclid | `a, b = b, a % b` | O(log min(a,b)) | O(1) |

> [!tip] Interview angle
> Give the one-line proof: any `d` dividing `a` and `b` also divides `a − q·b = a mod b`, and the reverse holds too. So the pairs `(a, b)` and `(b, a mod b)` have the same common divisors.

---

## 3. Brute — count down

**Intuition.** Test every candidate from `min(a, b)` downward and return the first that divides both.

```python
def gcd_brute(a, b):
    if a == 0 or b == 0:
        return a or b
    for d in range(min(a, b), 0, -1):
        if a % d == 0 and b % d == 0:
            return d
```

**Complexity:** time **O(min(a,b))**, space **O(1)**.

---

## 4. Better — subtraction Euclid

**Intuition.** Euclid's original version: `gcd(a, b) = gcd(a − b, b)`. It's correct, but `gcd(10⁹, 1)` needs 10⁹ subtractions. Repeated subtraction is just division, which leads to the modulo form.

```python
def gcd_sub(a, b):
    if a == 0 or b == 0:
        return a or b
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a
```

**Complexity:** time **O(max(a,b)) worst**, space **O(1)**.

---

## 5. Optimal — modulo Euclid

**Intuition.** Replace the subtraction loop with one `%`. After two steps the larger number has at least halved, so the step count is logarithmic. The worst case is consecutive Fibonacci numbers (Lamé's theorem).

**Algorithm**

1. While `b != 0`: `a, b = b, a % b`.
2. Return `a`.

**Dry run** — `gcd(48, 18)`

| a | b | a % b |
|---|---|---|
| 48 | 18 | 12 |
| 18 | 12 | 6 |
| 12 | 6 | 0 |
| 6 | 0 | — |

→ **6**.

**Library:** C++17 `std::gcd` (`<numeric>`), Python `math.gcd`, Java `BigInteger.gcd` (for primitives, write your own).

**Recursive one-liner:** `gcd(a, b) = b == 0 ? a : gcd(b, a % b)`.

**C++**
```cpp
int gcdOf(int a, int b) {
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}
```

**Java**
```java
static int gcdOf(int a, int b) {
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}
```

**Python**
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
```

**Complexity:** time **O(log min(a,b))**, space **O(1)** — Lamé: steps ≤ 5 × (decimal digits of the smaller number).

---

## Edge cases

- One input is 0 → the other one.
- `a < b` → the first step swaps them automatically (`a % b = a`).
- Negative inputs: use `abs` first; C++ `%` keeps the sign of the dividend.

---

## Common mistakes

1. Using the subtraction version in an interview without mentioning its O(max) worst case.
2. Returning `b` instead of `a` after the loop (`b` is 0 by then).
3. Forgetting the temporary when swapping in C++/Java.

---

## Follow-ups

1. GCD of an array.
2. Extended Euclid: find x, y with ax + by = gcd(a, b).
3. Binary GCD (Stein).

<details><summary>Answer sketches</summary>

**#1:** Fold: `g = gcd(g, x)` across the array; exit early once `g == 1`.

**#2:** Recurse to get `(x', y')` for `(b, a % b)`, then `x = y'`, `y = x' − (a // b)·y'`. It's used for modular inverses.

**#3:** Replace `%` with shifts: pull out common factors of 2, strip 2s from odd/even pairs, subtract. Useful on hardware where division is slow.
</details>

---

## Flashcards

**Euclid's recurrence?** #flashcard
gcd(a, b) = gcd(b, a mod b); gcd(a, 0) = a.

**Euclid's complexity?** #flashcard
O(log min(a, b)). The worst case is consecutive Fibonacci numbers.

**Why is gcd(a, b) = gcd(b, a mod b)?** #flashcard
a mod b = a − qb, so the two pairs have exactly the same common divisors.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
