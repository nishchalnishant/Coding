---
module: striver/12-basic-recursion
lesson: 4
topic: Factorial of a Given Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/factorial-of-a-given-number-ii?category=basic-recursion&source=strivers-a2z-dsa-sheet
tags: [striver, basic-recursion, recursion, math]
---
# 4. Factorial of a Given Number

← [Sum of First N Numbers](03-sum-of-first-n-numbers.md) · [Part 12 index](README.md) · Next → [Sum of Array Elements](05-sum-of-array-elements.md)

> [!abstract] Problem at a glance
> **Task:** Return `n!` using recursion.
> **Key insight:** `n! = n · (n − 1)!` with `0! = 1! = 1`. Use a 64-bit type: `int` overflows at 13!, `long` at 21!.
> **Difficulty:** Easy · **Pattern:** Linear recursion
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/factorial-of-a-given-number-ii?category=basic-recursion&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Iterative](#3-iterative) · [4. Parameterised recursion](#4-parameterised-recursion) · [5. Functional recursion](#5-functional-recursion) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `n`, return `n! = 1 · 2 · … · n` (with `0! = 1`).

| Input | Output | Why |
|---|---|---|
| `n = 5` | `120` |  |
| `n = 0` | `1` | empty product |
| `n = 20` | `2432902008176640000` | largest factorial that fits in a signed 64-bit integer |

**Constraints:** `0 ≤ n ≤ 20`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Iterative | multiply 2..n | O(n) | O(1) |
| Parameterised recursion | f(i − 1, acc · i), acc = 1 | O(n) | O(n) stack |
| Functional recursion | return n · f(n − 1) | O(n) | O(n) stack |

---

## 3. Iterative

**Intuition.** Running product.

```python
def fact_loop(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Parameterised recursion

**Intuition.** The identity for × is 1, so the accumulator starts at 1.

```python
def fact_param(n, acc=1):
    if n <= 1:
        return acc
    return fact_param(n - 1, acc * n)
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## 5. Functional recursion

**Intuition.** Directly the mathematical definition. The base `n ≤ 1` covers both 0 and 1.

**Algorithm**

1. If `n <= 1` return 1.
2. Return `n * f(n − 1)`.

**Dry run** — `f(4) = 4 · f(3) = 4 · 3 · f(2) = 4 · 3 · 2 · f(1) = 24`.

**C++**
```cpp
long long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

**Java**
```java
static long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

**Python**
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## Edge cases

- `0! = 1`.
- 13! = 6 227 020 800 > 2³¹ − 1, so it needs 64 bits.

---

## Common mistakes

1. Base case returning 0, which makes every product 0.
2. An `int` return type: 13! silently overflows.
3. Base `n == 1` only: `n = 0` recurses into negatives.

---

## Follow-ups

1. n! mod 1e9+7 for n up to 10⁶.
2. Number of trailing zeros of n! (LC 172).

<details><summary>Answer sketches</summary>

**#1:** Iterate, taking `% MOD` after each multiply; precompute a table for many queries.

**#2:** Count the factors of 5: `n/5 + n/25 + n/125 + …`, in O(log n).
</details>

---

## Flashcards

**Largest n with n! in signed 64-bit?** #flashcard
20.

**Trailing zeros of n!?** #flashcard
Σ ⌊n / 5ᵏ⌋.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
