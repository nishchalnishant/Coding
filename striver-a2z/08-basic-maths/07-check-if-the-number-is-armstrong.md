---
module: striver-a2z/08-basic-maths
lesson: 7
topic: Check if the Number is Armstrong
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-the-number-if-armstrong?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, digits]
---
# 7. Check if the Number is Armstrong

← [Factorial of a Given Number](06-factorial-of-a-given-number.md) · [Part 8 index](README.md) · Next → [Check for Perfect Number](08-check-for-perfect-number.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `n` equals the sum of its digits each raised to the number of digits.
> **Key insight:** Use two digit loops: one counts the digits `k`, the other sums `dᵏ`.
> **Difficulty:** Easy · **Pattern:** Digit loop × 2
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-the-number-if-armstrong?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — string](#3-brute--string) · [4. Optimal — two digit loops](#4-optimal--two-digit-loops) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A number with `k` digits is an **Armstrong** (narcissistic) number if the sum of each digit raised to the power `k` equals the number itself. Example: `153 = 1³ + 5³ + 3³`.

| Input | Output | Why |
|---|---|---|
| `n = 153` | `true` | 1 + 125 + 27 |
| `n = 12` | `false` | 1² + 2² = 5 |
| `n = 9474` | `true` | 9⁴+4⁴+7⁴+4⁴ |
| `n = 5` | `true` | every single digit: d¹ = d |

**Constraints:** `0 ≤ n ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — string | `sum(int(c)**k)` | O(d) | O(d) |
| Optimal — two digit loops | count k, then sum dᵏ | O(d · log k) ≈ O(log n) | O(1) |

---

## 3. Brute — string

**Intuition.** `k = len(str(n))`, then sum `int(c) ** k` over the characters.

```python
def is_armstrong_str(n):
    s = str(n)
    k = len(s)
    return sum(int(c) ** k for c in s) == n
```

**Complexity:** time **O(d)**, space **O(d)**.

---

## 4. Optimal — two digit loops

**Intuition.** You need `k` before you can raise anything to it, so count the digits first. Then loop again, raising each digit to `k` with integer arithmetic. Avoid floating `pow`, which can return `124.9999` for `5³`.

**Algorithm**

1. `k` = digit count of `n` (1 if `n == 0`).
2. `s = 0`, `t = n`; while `t > 0`: `d = t % 10`; `s += d^k` (integer power); `t //= 10`.
3. Return `s == n`.

**Dry run** — `n = 153`, `k = 3`: 3³ = 27, 5³ = 125, 1³ = 1 → s = 153 → **true**.

**C++**
```cpp
long long ipow(long long b, int e) {
    long long r = 1;
    while (e--) r *= b;
    return r;
}
bool isArmstrong(int n) {
    int k = 0;
    for (int t = n; t > 0; t /= 10) k++;
    if (n == 0) k = 1;
    long long s = 0;
    for (int t = n; t > 0; t /= 10) s += ipow(t % 10, k);
    return s == n;
}
```

**Java**
```java
static long ipow(long b, int e) {
    long r = 1;
    while (e-- > 0) r *= b;
    return r;
}
static boolean isArmstrong(int n) {
    int k = 0;
    for (int t = n; t > 0; t /= 10) k++;
    if (n == 0) k = 1;
    long s = 0;
    for (int t = n; t > 0; t /= 10) s += ipow(t % 10, k);
    return s == n;
}
```

**Python**
```python
def is_armstrong(n):
    k = len(str(n)) if n else 1
    s, t = 0, n
    while t > 0:
        s += (t % 10) ** k
        t //= 10
    return s == n
```

**Complexity:** time **O(d · log k) ≈ O(log n)**, space **O(1)** — k ≤ 10, so each power costs at most 10 multiplies.

---

## Edge cases

- Single digits 0–9 are all Armstrong.
- `9⁹ × 10` fits in 64-bit; with `int` the sum can overflow for 10-digit inputs.

---

## Common mistakes

1. Always cubing (`d³`) instead of raising to the digit count `k`.
2. Using floating `pow(d, k)` and comparing the result as an int, which can be off by one after truncation.
3. Consuming `n` in the first loop and then having nothing left for the second. Use a copy.

---

## Follow-ups

1. List all Armstrong numbers in `[1, N]`.
2. Sum of digits raised to a fixed power p.

<details><summary>Answer sketches</summary>

**#1:** Run the check for each number, O(N log N). There are only 88 Armstrong numbers in all, so you could also hard-code them.

**#2:** Same loop with a constant exponent.
</details>

---

## Flashcards

**Armstrong condition?** #flashcard
Σ dᵏ = n, where k = number of digits.

**Why avoid `pow()` here?** #flashcard
It returns a double. Truncation can turn 124.99999 into 124 and break the equality.

**3-digit Armstrong numbers?** #flashcard
153, 370, 371, 407.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
