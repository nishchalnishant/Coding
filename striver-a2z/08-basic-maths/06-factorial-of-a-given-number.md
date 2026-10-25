---
module: striver-a2z/08-basic-maths
lesson: 6
topic: Factorial of a Given Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/factorial-of-a-given-number-i?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, overflow]
---
# 6. Factorial of a Given Number

← [Return the Largest Digit in a Number](05-return-the-largest-digit-in-a-number.md) · [Part 8 index](README.md) · Next → [Check if the Number is Armstrong](07-check-if-the-number-is-armstrong.md)

> [!abstract] Problem at a glance
> **Task:** Return `n! = 1 × 2 × … × n`.
> **Key insight:** Use a running product with `0! = 1`. 64-bit holds results up to `20!`; past that you need big integers or a modulus.
> **Difficulty:** Easy · **Pattern:** Running product
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/factorial-of-a-given-number-i?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — recursion](#3-brute--recursion) · [4. Optimal — iterative product](#4-optimal--iterative-product) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `n`, return `n!`. By definition `0! = 1`.

| Input | Output | Why |
|---|---|---|
| `n = 0` | `1` | empty product |
| `n = 3` | `6` | 1·2·3 |
| `n = 5` | `120` |  |
| `n = 20` | `2432902008176640000` | largest that fits in signed 64-bit |

**Constraints:** `0 ≤ n ≤ 20` so the answer fits in `long long` / `long`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — recursion | `n * fact(n-1)` | O(n) | O(n) stack |
| Optimal — iterative product | `res *= i` for i in 2..n | O(n) | O(1) |

> [!tip] Interview angle
> Say the overflow boundary aloud: "`12!` is the last that fits in int and `20!` the last that fits in long, so I'll return long." If they push for larger `n`, offer `% (10⁹+7)` or a big-integer type.

---

## 3. Brute — recursion

**Intuition.** This is the textbook recursive definition, and it maps straight to code. It uses one stack frame per level. That's fine for n ≤ 20, but it's the classic example of recursion that a loop should replace.

```python
def fact_rec(n):
    return 1 if n <= 1 else n * fact_rec(n - 1)
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## 4. Optimal — iterative product

**Intuition.** Multiply an accumulator by each integer from 2 to n. Starting at `res = 1` handles `n = 0` and `n = 1`.

**Algorithm**

1. `res = 1` (64-bit).
2. For `i` in `2..n`: `res *= i`.
3. Return `res`.

**Dry run** — `n = 5`: 1 → 2 → 6 → 24 → 120.

| Type | Largest n with n! in range |
|---|---|
| 32-bit `int` | 12 (`479 001 600`) |
| 64-bit `long long` | 20 (`2.43 × 10¹⁸`) |
| Python `int` | unbounded (big-int) |

**C++**
```cpp
long long factorial(int n) {
    long long res = 1;
    for (int i = 2; i <= n; i++) res *= i;
    return res;
}
```

**Java**
```java
static long factorial(int n) {
    long res = 1;
    for (int i = 2; i <= n; i++) res *= i;
    return res;
}
```

**Python**
```python
def factorial(n):
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- `n = 0` → 1.
- `n = 13` already overflows a 32-bit int.
- `n > 20` overflows 64-bit; the problem must then give a modulus.

---

## Common mistakes

1. Starting `res = 0`, which makes every answer 0.
2. Using `int` for the accumulator.
3. Recursing without a base case for `n = 0`.

---

## Follow-ups

1. Compute `n! mod (10⁹+7)` for n up to 10⁶.
2. How many trailing zeros does `n!` have? (LC 172)
3. List all factorials ≤ n (Striver variant II).

<details><summary>Answer sketches</summary>

**#1:** Apply `res = res * i % MOD` at each step. Precompute a prefix array of factorials if there are many queries.

**#2:** Count the factors of 5: `n//5 + n//25 + n//125 + …`, in O(log₅ n).

**#3:** Keep multiplying while `fact * (i+1) ≤ n` and append each value.
</details>

---

## Flashcards

**Largest n! that fits in a 64-bit signed integer?** #flashcard
20!

**Largest n! that fits in a 32-bit int?** #flashcard
12!

**Trailing zeros of n!?** #flashcard
Σ ⌊n / 5ᵏ⌋, counting the factors of 5.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
