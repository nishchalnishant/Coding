---
module: striver-a2z/31-maths
lesson: 2
topic: Print all primes till N
difficulty: Easy
source: https://takeuforward.org/learning/dsa/print-all-primes-till-n?category=sieve-of-eratosthenes&source=strivers-a2z-dsa-sheet
tags: [striver, maths, math, primes, sieve]
---
# 2. Print all primes till N

← [Primes and the Sieve](01-sieve-theory.md) · [Part 31 index](README.md) · Next → [Prime factorisation of a number](03-prime-factorisation-of-a-number.md)

> [!abstract] Problem at a glance
> **Task:** Return every prime `≤ n` in increasing order.
> **Key insight:** Mark multiples instead of testing each number. For each `i` still marked prime with `i·i ≤ n`, cross out `i², i² + i, …`. Smaller multiples `k·i` with `k < i` were already crossed out by the prime factor of `k`. Total work is `Σ n/p` over primes `p ≤ √n`, which is O(n log log n).
> **Difficulty:** Easy · **Pattern:** Sieve of Eratosthenes · **Also on:** [LC 204](https://leetcode.com/problems/count-primes/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/print-all-primes-till-n?category=sieve-of-eratosthenes&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Trial division per number](#3-trial-division-per-number) · [4. Sieve of Eratosthenes](#4-sieve-of-eratosthenes) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer `n`, return all prime numbers between 1 and `n` inclusive, in increasing order.

| Input | Output | Why |
|---|---|---|
| `10` | `[2, 3, 5, 7]` |  |
| `2` | `[2]` |  |
| `1` | `[]` | 1 is not prime |

**Constraints:** `1 ≤ n ≤ 10⁶`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Trial division per number | x is prime iff no d in [2, √x] divides it | O(n√n) | O(1) extra |
| Sieve of Eratosthenes | cross out multiples from i², i up to √n | O(n log log n) | O(n) |

> [!tip] Interview angle
> Start with trial division up to `√x` per number, O(n√n). Then the sieve: explain both optimisations (outer loop to `√n`, inner loop from `i²`) and quote O(n log log n) time and O(n) memory. For `n` near 10⁹, say a **segmented sieve** is needed (sieve primes to √R, then mark one block of `[L, R]` at a time).

---

## 3. Trial division per number

**Intuition.** Check each `x` from 2 to `n` by trying divisors up to `√x`. A composite `x = a·b` with `a ≤ b` always has `a ≤ √x`.

```python
def primes_trial(n):
    res = []
    for x in range(2, n + 1):
        d = 2
        while d * d <= x and x % d:
            d += 1
        if d * d > x:
            res.append(x)
    return res
```

**Complexity:** time **O(n√n)**, space **O(1) extra**.

---

## 4. Sieve of Eratosthenes

**Intuition.** `prime[0..n] = true`, then set 0 and 1 false. For `i = 2` while `i·i ≤ n`: if `prime[i]`, set `prime[j] = false` for `j = i², i² + i, …, ≤ n`. Collect the indices still true.

**Algorithm**

1. `prime = [true] * (n + 1)`; `prime[0] = prime[1] = false` (guard n < 2).
2. For `i = 2; i·i ≤ n; i++`: if `prime[i]`, mark `j = i·i, i·i + i, …` false.
3. Return every `i` with `prime[i]`.

**Dry run** — n = 30: i=2 crosses 4, 6, …, 30; i=3 crosses 9, 15, 21, 27 (the even ones are already gone); i=4 skipped; i=5 crosses 25; 6·6 > 30 stop. Left: 2 3 5 7 11 13 17 19 23 29.

**C++**
```cpp
vector<int> sieve(int n) {
    vector<int> res;
    if (n < 2) return res;
    vector<bool> prime(n + 1, true);
    prime[0] = prime[1] = false;
    for (long long i = 2; i * i <= n; i++)
        if (prime[i])
            for (long long j = i * i; j <= n; j += i) prime[j] = false;
    for (int i = 2; i <= n; i++) if (prime[i]) res.push_back(i);
    return res;
}
```

**Java**
```java
static List<Integer> sieve(int n) {
    List<Integer> res = new ArrayList<>();
    if (n < 2) return res;
    boolean[] composite = new boolean[n + 1];
    for (long i = 2; i * i <= n; i++)
        if (!composite[(int) i])
            for (long j = i * i; j <= n; j += i) composite[(int) j] = true;
    for (int i = 2; i <= n; i++) if (!composite[i]) res.add(i);
    return res;
}
```

**Python**
```python
def sieve(n):
    if n < 2:
        return []
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False
    i = 2
    while i * i <= n:
        if prime[i]:
            prime[i * i::i] = [False] * len(range(i * i, n + 1, i))
        i += 1
    return [i for i in range(n + 1) if prime[i]]
```

**Complexity:** time **O(n log log n)**, space **O(n)** — Σ_{p ≤ √n} n/p = n · Σ 1/p ≈ n ln ln n by Mertens' theorem.

---

## Edge cases

- n < 2 → empty.
- n itself prime (inclusive bound).
- n a perfect square of a prime (25: the inner loop must reach i²).

---

## Common mistakes

1. Treating 1 as prime.
2. `i * i` overflowing `int` for large n (use 64-bit).
3. Inner loop from `2·i`: correct but slower.
4. Outer `i < √n` instead of `i·i ≤ n`, so 25 or 49 survive.

---

## Follow-ups

1. n up to 10⁹ but only [L, R] with R − L ≤ 10⁶?
2. Linear sieve?

<details><summary>Answer sketches</summary>

**#1:** Segmented sieve: primes to √R, then for each one cross out its multiples within [L, R] starting at max(p², ⌈L/p⌉·p).

**#2:** Each composite is crossed out exactly once by its smallest prime factor: O(n), and it yields the SPF array as a by-product.
</details>

---

## Flashcards

**Sieve inner loop start?** #flashcard
i², because smaller multiples were crossed out by smaller primes.

**Sieve complexity?** #flashcard
O(n log log n) time, O(n) memory.

**Outer loop bound?** #flashcard
i·i ≤ n: any composite ≤ n has a prime factor ≤ √n.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md)
