---
module: striver/12-basic-recursion
lesson: 8
topic: Check if a Number is Prime or Not
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-a-number-is-prime-or-not?category=basic-recursion&source=strivers-a2z-dsa-sheet
tags: [striver, basic-recursion, recursion, math, primes]
---
# 8. Check if a Number is Prime or Not

← [Check if String is Palindrome or Not](07-check-if-string-is-palindrome.md) · [Part 12 index](README.md) · Next → [Reverse an Array (Recursive)](09-reverse-an-array-recursive.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `num` is prime, using recursion over the candidate divisors.
> **Key insight:** Only divisors up to `√num` matter. Recurse on the divisor `i`: `f(i) = (num % i ≠ 0) and f(i + 1)`, base `i·i > num → true`.
> **Difficulty:** Easy · **Pattern:** Linear recursion over a divisor
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-a-number-is-prime-or-not?category=basic-recursion&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — recurse over 2..n−1](#3-brute--recurse-over-2n1) · [4. Optimal — recurse over 2..√n](#4-optimal--recurse-over-2n) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer `num`, return `true` if it is prime: greater than 1, with no divisors other than 1 and itself.

| Input | Output | Why |
|---|---|---|
| `num = 7` | `true` |  |
| `num = 1` | `false` | 1 is not prime |
| `num = 25` | `false` | 5 · 5 |

**Constraints:** `1 ≤ num ≤ 10⁵` here, so that the depth √num ≤ 317 stays safe in Python. For 10⁹ use the loop.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — recurse over 2..n−1 | check every candidate below n | O(n) | O(n) stack |
| Optimal — recurse over 2..√n | stop when i·i > num | O(√n) | O(√n) stack |

> [!tip] Interview angle
> Lead with the √n bound. The divisor-pair argument (if `a·b = n` and `a ≤ b` then `a ≤ √n`) is the proof interviewers want to hear.

---

## 3. Brute — recurse over 2..n−1

**Intuition.** Correct but deep: recursion depth n crashes Python for n > ~1000.

```python
def prime_brute(num, i=2):
    if num < 2:
        return False
    if i >= num:
        return True
    if num % i == 0:
        return False
    return prime_brute(num, i + 1)
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## 4. Optimal — recurse over 2..√n

**Intuition.** If `num = a·b` with `a ≤ b`, then `a ≤ √num`. So when no `i ≤ √num` divides it, it's prime. Compare `i·i > num` instead of computing `sqrt` (no floating point).

**Algorithm**

1. If `num < 2` return false.
2. `f(i)`: if `i·i > num` return true; if `num % i == 0` return false; return `f(i + 1)`.
3. Answer = `f(2)`.

**Dry run** — `25`: i = 2 ✗, 3 ✗, 4 ✗, 5 → 25 % 5 = 0 → **false**. `29`: i = 2..5 don't divide; i = 6 → 36 > 29 → **true**.

**Faster loop:** test 2 and 3, then only `6k ± 1` (5, 7, 11, 13, …), which is ~3× fewer checks. For many queries up to N, use the Sieve of Eratosthenes (see [Basic Maths](../08-basic-maths/README.md)).

**C++**
```cpp
bool primeFrom(int num, int i) {
    if ((long long)i * i > num) return true;
    if (num % i == 0) return false;
    return primeFrom(num, i + 1);
}
bool checkPrime(int num) { return num >= 2 && primeFrom(num, 2); }
```

**Java**
```java
static boolean primeFrom(int num, int i) {
    if ((long) i * i > num) return true;
    if (num % i == 0) return false;
    return primeFrom(num, i + 1);
}
static boolean checkPrime(int num) { return num >= 2 && primeFrom(num, 2); }
```

**Python**
```python
def check_prime(num, i=2):
    if num < 2:
        return False
    if i * i > num:
        return True
    if num % i == 0:
        return False
    return check_prime(num, i + 1)
```

**Complexity:** time **O(√n)**, space **O(√n) stack** — `(long long) i * i` avoids overflow as `i` approaches √INT_MAX.

---

## Edge cases

- 1 → false; 2 → true (the loop never runs, since 4 > 2).
- Perfect squares (25, 49): `i·i == num` must still be checked, so the base is `>` not `>=`.

---

## Common mistakes

1. Treating 1 as prime.
2. Base `i·i >= num` misses perfect squares.
3. `i * i` overflow in 32-bit for num near 2³¹.

---

## Follow-ups

1. Count the primes below n (LC 204).
2. Primality for n up to 10¹⁸.

<details><summary>Answer sketches</summary>

**#1:** Sieve of Eratosthenes, O(n log log n).

**#2:** Deterministic Miller–Rabin with fixed bases; out of interview scope beyond a mention.
</details>

---

## Flashcards

**Why check divisors only up to √n?** #flashcard
If n = a·b with a ≤ b, then a ≤ √n.

**Stop condition without sqrt?** #flashcard
i·i > n (use 64-bit for the product).

**Is 1 prime?** #flashcard
No.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
