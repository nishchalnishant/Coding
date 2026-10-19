---
module: striver/31-maths
lesson: 1
topic: Primality by trial division, sieve of Eratosthenes, n log log n bound, linear sieve, smallest prime factor table, factorisation and divisor functions, prefix counts, segmented sieve
source: https://takeuforward.org/learning/dsa/print-all-primes-till-n?category=maths&source=strivers-a2z-dsa-sheet
tags: [striver, math, primes, sieve, spf, factorization, segmented-sieve, theory]
---
# 1. Primes and the Sieve

← [Part 31 index](README.md) · Next → [Print all primes till N](02-print-all-primes-till-n.md)

> [!abstract] What this covers
> **Core idea:** Testing one number for primality costs O(√x). When you need primality, factors or prime counts for **every** number up to `n`, don't test each number. Cross out multiples once, with the **sieve of Eratosthenes**. Its by-products answer the other questions:
> - Recording *who* crossed a number out gives the **smallest prime factor** table, which factorises any `x ≤ n` in O(log x).
> - A running count gives **prefix prime counts**, which answer `[L, R]` queries in O(1).
> - Sieving one window at a time gives the **segmented sieve**, for ranges near 10¹².
>
> **You'll be able to:** justify the √x bound; write the sieve with both optimisations; derive O(n log log n); build an SPF table and factorise with it; compute divisor count and sum; answer range counts; and run a segmented sieve.
> **Source:** [Striver: Print all primes till N](https://takeuforward.org/learning/dsa/print-all-primes-till-n?category=maths&source=strivers-a2z-dsa-sheet) · **Time:** 40 min

**Sections:** [1. Trial division](#1-trial-division) · [2. Sieve of Eratosthenes](#2-sieve-of-eratosthenes) · [3. Why O(n log log n)](#3-why-on-log-log-n) · [4. Smallest prime factor table](#4-smallest-prime-factor-table) · [5. Linear sieve](#5-linear-sieve) · [6. Divisor functions](#6-divisor-functions) · [7. Prefix prime counts](#7-prefix-prime-counts) · [8. Segmented sieve](#8-segmented-sieve) · [9. Choosing a tool](#9-choosing-a-tool) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Key terms](#key-terms) · [Flashcards](#flashcards)

---

## 1. Trial division

If `x = a·b` with `a ≤ b`, then `a·a ≤ a·b = x`, so `a ≤ √x`. A composite therefore always has a divisor in `[2, √x]`, and it's enough to check divisors up to there.

```python
def is_prime(x):
    if x < 2:
        return False
    d = 2
    while d * d <= x:        # avoids float sqrt
        if x % d == 0:
            return False
        d += 1
    return True
```

- **Cost:** O(√x) per number. Testing every `x ≤ n` costs O(n√n), which is about 10⁹ for n = 10⁶. That's too slow.
- **Speed-up:** after checking 2 and 3, test only `6k ± 1`. Every prime above 3 has that form. This is a 3× constant-factor win.
- **Factorising:** use the same loop, but divide `d` out repeatedly. Whatever remains above 1 at the end is a single prime factor larger than √(original).

---

## 2. Sieve of Eratosthenes

Start with every number marked prime. Take each prime `i` in turn and cross out its multiples.

```python
def sieve(n):
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False
    i = 2
    while i * i <= n:                    # optimisation 1
        if prime[i]:
            for j in range(i * i, n + 1, i):   # optimisation 2
                prime[j] = False
        i += 1
    return prime
```

| Optimisation | Why it's safe |
|---|---|
| Outer loop stops at `i·i ≤ n` | Every composite `≤ n` has a prime factor `≤ √n`, so it has already been crossed out |
| Inner loop starts at `i²` | `k·i` for `k < i` has a prime factor `< i` and was crossed out earlier |

**Trace, n = 30:**

| i | Crosses out (new) |
|---|---|
| 2 | 4 6 8 10 12 14 16 18 20 22 24 26 28 30 |
| 3 | 9 15 21 27 |
| 4 | skipped (already crossed out) |
| 5 | 25 |
| 6 | stop, since 36 > 30 |

Survivors: **2 3 5 7 11 13 17 19 23 29**.

**Memory:** `n + 1` booleans. A `vector<bool>` or `bitset` packs 8 per byte, so 10⁸ fits in 12.5 MB. Sieving odd numbers only halves it again.

---

## 3. Why O(n log log n)

Prime `p` crosses out about `n/p` numbers, so the total work is

```
Σ_{p ≤ √n} n/p  =  n · Σ_{p ≤ √n} 1/p  ≈  n · ln ln √n  ≈  n · ln ln n
```

The sum of reciprocals of primes up to `m` grows like `ln ln m` (Mertens). Compare the harmonic sum over **all** `k`, which grows like `ln m`: summing over every `i` instead of only primes would give O(n log n). For n = 10⁷, ln ln n ≈ 2.8, so the sieve is effectively linear.

---

## 4. Smallest prime factor table

Store **which** prime crossed each number out first. That prime is its smallest prime factor.

```python
spf = list(range(n + 1))          # spf[x] = x means "prime so far"
i = 2
while i * i <= n:
    if spf[i] == i:               # i is prime
        for j in range(i * i, n + 1, i):
            if spf[j] == j:       # first (smallest) prime to reach j
                spf[j] = i
    i += 1

def factor(x):                    # O(log x)
    f = []
    while x > 1:
        f.append(spf[x])
        x //= spf[x]
    return f
```

Each step divides `x` by at least 2, so there are at most log₂ x steps. Factors come out in non-decreasing order.

**When it pays off:** many queries with values bounded by `X ≤ 10⁷`. One query, or values up to 10¹²: use trial division instead (√10¹² = 10⁶ steps).

---

## 5. Linear sieve

The classical sieve crosses some numbers out several times (12 by both 2 and 3). The linear sieve crosses out each composite **exactly once**, by its smallest prime factor:

```python
def linear_sieve(n):
    spf = [0] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > n:
                break
            spf[i * p] = p
    return primes, spf
```

`i·p` is assigned only while `p ≤ spf[i]`, so `p` is the smallest prime factor of `i·p`. Every composite `c = spf(c) · (c / spf(c))` is produced exactly once. The result is O(n) time, with the SPF array included. It's rarely needed in interviews, but it's a good follow-up answer.

---

## 6. Divisor functions

From `x = p₁^e₁ · p₂^e₂ · … · p_k^e_k`:

| Quantity | Formula | 360 = 2³·3²·5 |
|---|---|---|
| Number of divisors d(x) | Π (eᵢ + 1) | 4·3·2 = 24 |
| Sum of divisors σ(x) | Π (pᵢ^(eᵢ+1) − 1)/(pᵢ − 1) | 15·13·6 = 1170 |
| Euler's φ(x) | x · Π (1 − 1/pᵢ) | 360·½·⅔·⅘ = 96 |
| Distinct prime factors ω(x) | k | 3 |

Any `x ≤ 10⁹` has at most 9 distinct prime factors (2·3·5·7·11·13·17·19·23 ≈ 2.2·10⁸) and at most 1344 divisors.

All divisors in O(√x): for `d` from 1 while `d·d ≤ x`, if `d` divides `x`, record `d` and `x/d`. Skip the duplicate when `d = x/d`.

---

## 7. Prefix prime counts

Run the sieve to `M`, then build `pre[i] = #primes ≤ i`:

```python
pre = [0] * (M + 1)
for i in range(1, M + 1):
    pre[i] = pre[i - 1] + prime[i]
# primes in [L, R]  =  pre[R] - pre[L - 1]
```

This is the standard prefix-sum pattern ([Part 14](../14-arrays/README.md)) on an indicator array. The same idea answers "count of numbers in [L, R] with property P" whenever P is sieve-computable, such as being square-free or having exactly k prime factors.

Sanity values: π(10) = 4, π(100) = 25, π(1000) = 168, π(10⁶) = 78 498. In general π(n) ≈ n / ln n.

---

## 8. Segmented sieve

**Use it when** `R` is up to 10¹² but `R − L ≤ 10⁶`. A full sieve to `R` is impossible, but every composite in `[L, R]` has a prime factor `≤ √R ≤ 10⁶`.

1. Sieve the primes up to `√R` normally.
2. Allocate `mark[0..R−L]`, all true. Index `k` stands for `L + k`.
3. For each such prime `p`, cross out its multiples in the window, starting from `start = max(p·p, ⌈L/p⌉·p)`. The `p·p` term stops `p` itself from being crossed out.
4. If `L ≤ 1`, clear the entries for 0 and 1.

```python
def segmented(L, R):
    base = [p for p in range(2, int(R ** 0.5) + 1) if is_prime(p)]   # or sieve
    mark = [True] * (R - L + 1)
    for p in base:
        start = max(p * p, (L + p - 1) // p * p)
        for j in range(start, R + 1, p):
            mark[j - L] = False
    return [L + k for k, ok in enumerate(mark) if ok and L + k >= 2]
```

**Cost:** O(√R log log R + (R − L) log log R) time and O(√R + (R − L)) memory. The same windowing lets a sieve to 10⁹ run in cache-sized blocks.

---

## 9. Choosing a tool

| Situation | Tool |
|---|---|
| One `x ≤ 10¹²`: prime? factors? divisors? | trial division to √x |
| All `x ≤ n`, `n ≤ 10⁷`: which are prime? | sieve |
| Many factorisations, values ≤ 10⁷ | SPF table |
| Many `[L, R]` counts, `R ≤ 10⁷` | sieve + prefix |
| Huge `R`, short window | segmented sieve |
| `x` up to 10¹⁸ | Miller–Rabin (out of interview scope; just name it) |

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Treating 1 as prime | Set `prime[0] = prime[1] = false`; guard `n < 2` |
| `i * i` overflowing 32-bit `int` | Use a 64-bit loop variable or `i <= n / i` |
| `d <= sqrt(x)` with floating point | Use `d * d <= x` |
| Outer loop `i < sqrt(n)` | Use `i * i <= n`, otherwise 25 or 49 survive |
| SPF overwritten by a larger prime | Only set `spf[j]` while `spf[j] == j` |
| Range count `pre[R] − pre[L]` | Use `pre[R] − pre[L − 1]` |
| Segmented sieve crossing out `p` itself | Start at `max(p², ⌈L/p⌉·p)` |
| Forgetting the leftover factor after trial division | `if x > 1: factors.append(x)` |

---

## Practice

<details><summary>1. Why can the sieve's inner loop start at i² rather than 2i?</summary>

Any `k·i` with `k < i` has a prime factor `≤ k < i`, so a smaller prime already crossed it out.
</details>

<details><summary>2. How many primes are there below 100? Below 10⁶?</summary>

25 and 78 498.
</details>

<details><summary>3. Factorise 2310 with an SPF table. How many steps does it take?</summary>

2 → 1155, 3 → 385, 5 → 77, 7 → 11, 11 → 1. Five steps, giving [2, 3, 5, 7, 11].
</details>

<details><summary>4. How many divisors does 720 have?</summary>

720 = 2⁴·3²·5, so d = 5·3·2 = 30.
</details>

<details><summary>5. In a segmented sieve with L = 100 and p = 7, where does crossing out start?</summary>

⌈100/7⌉·7 = 105, and 105 > 49, so it starts at 105.
</details>

<details><summary>6. Why does the linear sieve break when p > spf[i]?</summary>

For `p > spf[i]`, the smallest prime factor of `i·p` is `spf[i]`, not `p`. That number will be produced later as `spf[i] · (i·p/spf[i])`, so crossing it out now would be a duplicate.
</details>

<details><summary>7. You need d(x) for every x ≤ 10⁶. What do you do?</summary>

Use a divisor sieve: for every `i`, add 1 to `cnt[j]` for each multiple `j` of `i`. That's Σ n/i = O(n log n). Alternatively, use the SPF table with the formula from §6, or a linear sieve that tracks the exponent of the smallest prime.
</details>

<details><summary>8. LC 204 asks for primes strictly less than n. What changes?</summary>

Sieve to `n − 1`, or count `prime[2..n−1]`, and return 0 for `n ≤ 2`.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Trial division | Testing divisors 2..√x |
| Sieve of Eratosthenes | Crossing out the multiples of each prime; O(n log log n) |
| SPF | Smallest prime factor; `spf[x] = x` for primes |
| Linear sieve | O(n) sieve that crosses each composite out once, via its SPF |
| π(n) | Number of primes ≤ n, ≈ n / ln n |
| d(x), σ(x), φ(x) | Divisor count, divisor sum, Euler's totient |
| Segmented sieve | Sieve one window [L, R] using the primes ≤ √R |

---

## Flashcards

**Why is √x enough for trial division?** #flashcard
A composite x = a·b with a ≤ b has a ≤ √x.

**Sieve's two optimisations?** #flashcard
Outer loop while i·i ≤ n; inner loop from i².

**Sieve complexity and why?** #flashcard
O(n log log n): Σ n/p over primes, and Σ 1/p ≈ ln ln n.

**SPF update rule?** #flashcard
For prime i and j = i², i²+i, …: if spf[j] == j then spf[j] = i.

**Factorise with SPF, cost?** #flashcard
while x > 1: record spf[x], x /= spf[x]. O(log x).

**Divisor count from factorisation?** #flashcard
Π (eᵢ + 1).

**Range prime count?** #flashcard
pre[R] − pre[L − 1].

**Segmented sieve start for prime p?** #flashcard
max(p², ⌈L/p⌉·p).

**π(10⁶)?** #flashcard
78 498.

**Linear sieve guarantee?** #flashcard
Each composite is crossed out once, by its smallest prime; O(n) total.

**Interview track →** [Math & number theory deep-dive](../../02-algorithms/18-math-and-number-theory.md)
