---
module: striver-a2z/12-basic-recursion
lesson: 3
topic: Sum of First N Numbers
difficulty: Easy
source: https://takeuforward.org/learning/dsa/sum-of-first-n-numbers?category=basic-recursion&source=strivers-a2z-dsa-sheet
tags: [striver, basic-recursion, recursion, math]
---
# 3. Sum of First N Numbers

← [Recursion Concepts with Parameters](02-recursion-concepts-with-parameters.md) · [Part 12 index](README.md) · Next → [Factorial of a Given Number](04-factorial-of-a-given-number.md)

> [!abstract] Problem at a glance
> **Task:** Return `1 + 2 + … + N` using recursion.
> **Key insight:** `S(N) = N + S(N − 1)`, with `S(0) = 0`. This is the first recursion to write in both styles, even though Gauss's `N(N+1)/2` is O(1).
> **Difficulty:** Easy · **Pattern:** Linear recursion
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sum-of-first-n-numbers?category=basic-recursion&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Iterative loop](#3-iterative-loop) · [4. Parameterised recursion](#4-parameterised-recursion) · [5. Functional recursion](#5-functional-recursion) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `N`, return the sum of the first `N` natural numbers.

| Input | Output | Why |
|---|---|---|
| `N = 4` | `10` | 1 + 2 + 3 + 4 |
| `N = 1` | `1` |  |
| `N = 0` | `0` | empty sum |

**Constraints:** `0 ≤ N ≤ 10³` (kept small so that the recursion depth is safe in Python).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Iterative loop | accumulate 1..N | O(N) | O(1) |
| Parameterised recursion | f(i, acc + i), print/return acc at base | O(N) | O(N) stack |
| Functional recursion | return N + f(N − 1) | O(N) | O(N) stack |

> [!tip] Interview angle
> Write the recursive version because that's what is asked, then mention `N(N+1)/2` in O(1). Showing you know the closed form, and the stack cost of the recursion, is the signal.

---

## 3. Iterative loop

**Intuition.** The baseline the recursion replaces.

```python
def sum_loop(N):
    s = 0
    for i in range(1, N + 1):
        s += i
    return s
```

**Complexity:** time **O(N)**, space **O(1)**.

---

## 4. Parameterised recursion

**Intuition.** Carry the running sum down. At `i == 0` the accumulator holds the answer.

```python
def sum_param(N, acc=0):
    if N == 0:
        return acc
    return sum_param(N - 1, acc + N)
```

**Complexity:** time **O(N)**, space **O(N) stack**.

---

## 5. Functional recursion

**Intuition.** Assume `f(N − 1)` is the correct sum of `1..N−1`; then `N + f(N − 1)` is the sum of `1..N`. The base `f(0) = 0` is the identity for +.

**Algorithm**

1. If `N == 0` return 0.
2. Return `N + f(N − 1)`.

**Dry run** — `f(3) = 3 + f(2) = 3 + (2 + f(1)) = 3 + (2 + (1 + f(0))) = 3 + 2 + 1 + 0 = 6`.

**O(1) alternative:** `N * (N + 1) / 2`, using a 64-bit type once N exceeds ~65 000.

**C++**
```cpp
int NnumbersSum(int N) {
    if (N == 0) return 0;
    return N + NnumbersSum(N - 1);
}
```

**Java**
```java
static int NnumbersSum(int N) {
    if (N == 0) return 0;
    return N + NnumbersSum(N - 1);
}
```

**Python**
```python
def n_numbers_sum(N):
    if N == 0:
        return 0
    return N + n_numbers_sum(N - 1)
```

**Complexity:** time **O(N)**, space **O(N) stack**.

---

## Edge cases

- N = 0 → 0 (the base case).
- Large N: the recursion overflows the stack before the int overflows the sum.

---

## Common mistakes

1. Base case `N == 1` only, which recurses forever on `N = 0`.
2. Forgetting `return` on the recursive line in Python (returns `None`).

---

## Follow-ups

1. Sum of squares 1² + … + N² recursively.
2. Make the recursion O(log N) depth.

<details><summary>Answer sketches</summary>

**#1:** `N*N + f(N − 1)`; closed form `N(N+1)(2N+1)/6`.

**#2:** Split the range: `sum(l, r) = sum(l, m) + sum(m+1, r)`, depth log N, still O(N) calls.
</details>

---

## Flashcards

**Recurrence for sum 1..N?** #flashcard
S(N) = N + S(N − 1), S(0) = 0.

**Closed form of 1 + … + N?** #flashcard
N(N + 1)/2.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
