---
module: striver/31-maths
lesson: 3
topic: Prime factorisation of a number
difficulty: Medium
source: https://takeuforward.org/learning/dsa/prime-factorisation-of-a-number?category=sieve-of-eratosthenes&source=strivers-a2z-dsa-sheet
tags: [striver, maths, math, primes, sieve, factorization]
---
# 3. Prime factorisation of a number

← [Print all primes till N](02-print-all-primes-till-n.md) · [Part 31 index](README.md) · Next → [Count primes in range L to R](04-count-primes-in-range-l-to-r.md)

> [!abstract] Problem at a glance
> **Task:** For each query `x`, return its prime factors with multiplicity, ascending.
> **Key insight:** Precompute the **smallest prime factor** `spf[x]` for every `x ≤ max` with a sieve: when a prime `p` crosses out `j`, set `spf[j] = p` if it is still unset. Then factorise by repeatedly dividing by `spf[x]`. Each division at least halves `x`, so a query costs O(log x) after O(N log log N) preprocessing.
> **Difficulty:** Medium · **Pattern:** Smallest-prime-factor sieve · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/prime-factorization-using-sieve/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/prime-factorisation-of-a-number?category=sieve-of-eratosthenes&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Trial division per query](#3-trial-division-per-query) · [4. SPF sieve + repeated division](#4-spf-sieve--repeated-division) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `queries` of integers `x ≥ 2`, return for each one the list of its prime factors in non-decreasing order, repeated by multiplicity (e.g. `12 → [2, 2, 3]`).

| Input | Output | Why |
|---|---|---|
| `[12, 7]` | `[[2, 2, 3], [7]]` |  |
| `[60, 2, 97]` | `[[2, 2, 3, 5], [2], [97]]` |  |

**Constraints:** `1 ≤ |queries| ≤ 10⁵`; `2 ≤ x ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Trial division per query | divide out d = 2, 3, … while d·d ≤ x | O(q·√X) | O(1) extra |
| SPF sieve + repeated division | spf[x] then x /= spf[x] | O(X log log X + Σ log x) | O(X) |

> [!tip] Interview angle
> One query: trial division to `√x`, O(√x). Many queries with a bounded value: SPF sieve once, then O(log x) each. State the crossover: `q·√X` vs `X log log X + q log X`. Mention that a leftover `x > 1` after trial division is itself prime.

---

## 3. Trial division per query

**Intuition.** Divide out every `d` from 2 while `d·d ≤ x`. Whatever remains above 1 is a prime factor bigger than `√` of the original.

```python
def factorize_trial(queries):
    out = []
    for x in queries:
        f, d = [], 2
        while d * d <= x:
            while x % d == 0:
                f.append(d)
                x //= d
            d += 1
        if x > 1:
            f.append(x)
        out.append(f)
    return out
```

**Complexity:** time **O(q·√X)**, space **O(1) extra**.

---

## 4. SPF sieve + repeated division

**Intuition.** `spf[i] = i` initially. For each `i` with `spf[i] == i` (prime) and `i·i ≤ X`, for `j = i², i² + i, …`: if `spf[j] == j`, set `spf[j] = i`. To factor `x`: while `x > 1`, append `spf[x]` and divide `x` by it.

**Algorithm**

1. `X = max(queries)`; `spf[i] = i` for all i.
2. Sieve: for prime `i` with `i·i ≤ X`, set `spf[j] = i` on every still-unset multiple `j ≥ i²`.
3. Per query: while `x > 1`: push `spf[x]`, `x /= spf[x]`.
4. Factors come out non-decreasing automatically.

**Dry run** — spf[60] = 2 → 30, spf = 2 → 15, spf = 3 → 5, spf = 5 → 1. Factors [2, 2, 3, 5].

**C++**
```cpp
vector<vector<int>> factorize(const vector<int>& queries) {
    int X = *max_element(queries.begin(), queries.end());
    vector<int> spf(X + 1);
    for (int i = 0; i <= X; i++) spf[i] = i;
    for (long long i = 2; i * i <= X; i++)
        if (spf[i] == i)
            for (long long j = i * i; j <= X; j += i)
                if (spf[j] == j) spf[j] = i;
    vector<vector<int>> out;
    for (int x : queries) {
        vector<int> f;
        while (x > 1) { f.push_back(spf[x]); x /= spf[x]; }
        out.push_back(f);
    }
    return out;
}
```

**Java**
```java
static List<List<Integer>> factorize(int[] queries) {
    int X = 0;
    for (int x : queries) X = Math.max(X, x);
    int[] spf = new int[X + 1];
    for (int i = 0; i <= X; i++) spf[i] = i;
    for (long i = 2; i * i <= X; i++)
        if (spf[(int) i] == i)
            for (long j = i * i; j <= X; j += i)
                if (spf[(int) j] == j) spf[(int) j] = (int) i;
    List<List<Integer>> out = new ArrayList<>();
    for (int x : queries) {
        List<Integer> f = new ArrayList<>();
        while (x > 1) { f.add(spf[x]); x /= spf[x]; }
        out.add(f);
    }
    return out;
}
```

**Python**
```python
def factorize(queries):
    X = max(queries)
    spf = list(range(X + 1))
    i = 2
    while i * i <= X:
        if spf[i] == i:
            for j in range(i * i, X + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    out = []
    for x in queries:
        f = []
        while x > 1:
            f.append(spf[x])
            x //= spf[x]
        out.append(f)
    return out
```

**Complexity:** time **O(X log log X + Σ log x)**, space **O(X)** — sieve once; each query divides x by at least 2 per step, so at most log₂ x steps.

---

## Edge cases

- x prime → [x].
- x a prime power (64 → six 2s).
- Large prime near the bound (spf[x] = x).

---

## Common mistakes

1. Overwriting `spf[j]` with a larger prime (check `spf[j] == j` first).
2. Forgetting the leftover `x > 1` in trial division.
3. Sieving to a fixed bound smaller than the largest query.

---

## Follow-ups

1. Number of divisors / sum of divisors?
2. x up to 10¹² (single query)?

<details><summary>Answer sketches</summary>

**#1:** From x = Π pᵉ: d(x) = Π (e + 1); σ(x) = Π (p^(e+1) − 1)/(p − 1).

**#2:** Trial division to 10⁶ is fine; an SPF array of size 10¹² is not.
</details>

---

## Flashcards

**SPF sieve update?** #flashcard
For prime i and j = i², i²+i, …: if spf[j] == j, spf[j] = i.

**Factorise with SPF?** #flashcard
while x > 1: record spf[x]; x /= spf[x]. O(log x).

**Divisor count from factorisation?** #flashcard
Π (eᵢ + 1).

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md)
