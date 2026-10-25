---
module: striver-a2z/08-basic-maths
lesson: 9
topic: Check for Prime Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-for-prime-number?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, primes, sqrt]
---
# 9. Check for Prime Number

← [Check for Perfect Number](08-check-for-perfect-number.md) · [Part 8 index](README.md) · Next → [Count of Prime Numbers till N](10-count-of-prime-numbers-till-n.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `n` is prime.
> **Key insight:** Composite `n` has a factor ≤ √n, so trial division up to √n settles it. Skipping evens and multiples of 3 (the 6k ± 1 trick) cuts the work by a factor of 3.
> **Difficulty:** Easy · **Pattern:** √n trial division
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-for-prime-number?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — count divisors](#3-brute--count-divisors) · [4. Better — √n trial division](#4-better--n-trial-division) · [5. Optimal — 6k ± 1](#5-optimal--6k--1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A **prime** is an integer `> 1` whose only positive divisors are 1 and itself. Given `n`, return whether it is prime.

| Input | Output | Why |
|---|---|---|
| `n = 5` | `true` |  |
| `n = 8` | `false` | 2 × 4 |
| `n = 1` | `false` | 1 is not prime by definition |
| `n = 2` | `true` | the only even prime |

**Constraints:** `1 ≤ n ≤ 10⁹`. O(√n) ≈ 3·10⁴ steps per query.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — count divisors | count i in 1..n with n % i == 0 | O(n) | O(1) |
| Better — √n trial division | test 2..√n | O(√n) | O(1) |
| Optimal — 6k ± 1 | after 2 and 3, test only 6k±1 | O(√n / 3) | O(1) |

> [!tip] Interview angle
> If you're asked about many queries, switch to a sieve (next problem). If n is up to 10¹⁸, name Miller–Rabin and don't implement it unless asked.

---

## 3. Brute — count divisors

**Intuition.** A prime has exactly two divisors. Counting them all is a direct translation of the definition.

```python
def is_prime_brute(n):
    return sum(1 for i in range(1, n + 1) if n % i == 0) == 2
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Better — √n trial division

**Intuition.** If `n = a · b` with `a ≤ b`, then `a ≤ √n`. Finding no divisor in `[2, √n]` proves primality.

```python
def is_prime_sqrt(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
```

**Complexity:** time **O(√n)**, space **O(1)**.

---

## 5. Optimal — 6k ± 1

**Intuition.** Every integer is `6k + r` with `r ∈ {0..5}`. `6k, 6k+2, 6k+4` are even and `6k+3` is divisible by 3. Once 2 and 3 are handled, any remaining prime factor has the form `6k ± 1`, so test `i` and `i + 2` for `i = 5, 11, 17, …`.

**Algorithm**

1. `n < 2` → false; `n ≤ 3` → true.
2. If `n % 2 == 0` or `n % 3 == 0` → false.
3. For `i = 5` while `i * i ≤ n`, step 6: if `n % i == 0` or `n % (i + 2) == 0` → false.
4. Return true.

**Dry run** — `n = 97`: not divisible by 2 or 3. i = 5: 97 % 5 = 2, 97 % 7 = 6. i = 11: 121 > 97, stop → **prime**.

**C++**
```cpp
bool isPrime(int n) {
    if (n < 2) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (long long i = 5; i * i <= n; i += 6)
        if (n % i == 0 || n % (i + 2) == 0) return false;
    return true;
}
```

**Java**
```java
static boolean isPrime(int n) {
    if (n < 2) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (long i = 5; i * i <= n; i += 6)
        if (n % i == 0 || n % (i + 2) == 0) return false;
    return true;
}
```

**Python**
```python
def is_prime(n):
    if n < 2:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
```

**Complexity:** time **O(√n / 3)**, space **O(1)** — 2 candidates per 6 numbers, so a third of the √n loop; still O(√n) asymptotically.

---

## Edge cases

- `n = 1` → false; `n ≤ 0` → false.
- `2` and `3` must short-circuit before the 6k loop.
- Squares of primes (`25`, `49`): the `≤` in `i * i ≤ n` is what catches them.

---

## Common mistakes

1. Writing `i * i < n`, which misses perfect squares like 25.
2. Calling 1 prime.
3. Checking `i <= n / 2`. It's correct but O(n), and that's the answer that fails the interview.

---

## Follow-ups

1. Prime factorisation of n.
2. Many queries up to 10⁶.

<details><summary>Answer sketches</summary>

**#1:** Trial-divide by each `i` up to √n, dividing out `i` while it divides. Whatever remains above 1 is the last prime factor. O(√n).

**#2:** Precompute a sieve once, O(N log log N); each query is then O(1).
</details>

---

## Flashcards

**Why is √n enough for a primality test?** #flashcard
A composite n = a·b with a ≤ b has a ≤ √n.

**What is the 6k ± 1 trick?** #flashcard
Every prime > 3 is ≡ ±1 (mod 6), so after 2 and 3 you only test 5, 7, 11, 13, …

**Is 1 prime?** #flashcard
No. A prime needs exactly two distinct divisors.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
