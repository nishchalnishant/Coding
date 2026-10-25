---
module: striver-a2z/31-maths
lesson: 5
topic: Modular arithmetic and combinatorics — mod rules, binary exponentiation, modular inverse (Fermat, extended Euclid), nCr mod p, Pascal's triangle, Catalan numbers, inclusion–exclusion
source: https://takeuforward.org/learning/dsa/print-all-primes-till-n?category=sieve-of-eratosthenes&source=strivers-a2z-dsa-sheet
tags: [striver, maths, theory, modular-arithmetic, combinatorics, enrichment]
---
# 5. Modular Arithmetic and Combinatorics

← [Count primes in range L to R](04-count-primes-in-range-l-to-r.md) · [Part 31 index](README.md) · Next → [Part 32: Beyond the sheet](../32-beyond-the-sheet/README.md)

> [!abstract] What this covers
> **Core idea:** Any "return the answer modulo 10⁹+7" problem needs four tools: the mod rules, fast exponentiation, the modular inverse and precomputed factorials. Together they let you count huge things (paths, arrangements, subsets) without overflow.
> **You'll be able to:** compute aᵇ mod m in O(log b); invert mod a prime; answer nCr mod p in O(1) after O(n) precomputation; use Pascal's rule when p is not prime or n is small; and recognise Catalan and inclusion–exclusion counts.
> **Source:** enrichment beyond the A2Z Maths category (it builds on [Pow(x, n)](../18-recursion/02-pow-x-n.md) and [GCD](../08-basic-maths/11-gcd-of-two-numbers.md)). · **Time:** 45 min

**Sections:** [1. Mod rules](#1-mod-rules) · [2. Binary exponentiation](#2-binary-exponentiation) · [3. GCD and extended Euclid](#3-gcd-and-extended-euclid) · [4. Modular inverse](#4-modular-inverse) · [5. nCr mod p](#5-ncr-mod-p) · [6. Counting toolkit](#6-counting-toolkit) · [7. Number-theory facts](#7-number-theory-facts)

---

## 1. Mod rules

With `M = 1_000_000_007`, which is prime and fits in int32. Its square fits in int64.

| Operation | Safe form | Note |
|---|---|---|
| Add | `(a + b) % M` | both < M ⇒ the sum < 2³¹ |
| Subtract | `((a - b) % M + M) % M` | C++/Java `%` can be negative |
| Multiply | `(a * b) % M` using 64-bit | `1LL * a * b % M` in C++; Java `(long) a * b % M` |
| Divide | `a * inv(b) % M` | **never** `(a / b) % M` |
| Power | binary exponentiation | §2 |

- **Reduce often.** Apply the mod after every operation, not only at the end.
- **Python** has big ints but still slows down, so reduce there too. `pow(a, b, M)` is built in.
- **Comparisons stop working once you reduce.** You cannot compare reduced values to find a max. If you need the max, compare in logs or with exact values.

---

## 2. Binary exponentiation

`aᵇ = (a^(b/2))²·(a if b is odd)`. This takes O(log b) multiplications.

```cpp
long long power(long long a, long long b, long long m) {
    long long r = 1; a %= m;
    while (b > 0) {
        if (b & 1) r = r * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return r;
}
```

- **Pow(x, n) with doubles and negative n:** compute `1 / power(x, -n)`. Watch out for `n = INT_MIN`: negate it as a `long`.
- The same squaring loop works for **matrix exponentiation**. The k-th Fibonacci number in O(log k) is `[[1,1],[1,0]]^k`, which is O(d³ log k) for d×d matrices.
- **Euler's theorem** reduces huge exponents: `a^b ≡ a^(b mod φ(m))` when gcd(a, m) = 1. For a prime p this is `a^(b mod (p−1))`.

---

## 3. GCD and extended Euclid

- `gcd(a, b) = gcd(b, a mod b)`, which is O(log min). Also `lcm(a, b) = a / gcd(a, b) * b`: divide first to avoid overflow.
- **Extended Euclid** finds x, y with `ax + by = gcd(a, b)`:

```text
ext(a, b): if b == 0: return (a, 1, 0)
           (g, x1, y1) = ext(b, a % b)
           return (g, y1, x1 - (a / b) * y1)
```

- `ax ≡ 1 (mod m)` is solvable **iff gcd(a, m) = 1**, and the inverse is x mod m. This works for **any** m, prime or not.
- **Bézout's identity:** `ax + by = c` has integer solutions iff `gcd(a, b) | c`. This is the "water jug" problem.

---

## 4. Modular inverse

| Method | Condition | Cost |
|---|---|---|
| Fermat: `a^(p−2) mod p` | p prime, p ∤ a | O(log p) |
| Extended Euclid | gcd(a, m) = 1 | O(log m) |
| All inverses 1..n | p prime | `inv[i] = −(p / i) · inv[p mod i] mod p`, O(n) total |
| Inverse factorials | p prime | `invFact[n] = fact[n]^(p−2)`, then `invFact[i−1] = invFact[i]·i` |

---

## 5. nCr mod p

| Situation | Method | Pre / query |
|---|---|---|
| n ≤ 10⁶, p prime > n | `fact[n] · invFact[r] · invFact[n−r]` | O(n) / O(1) |
| n ≤ ~5000, any modulus | Pascal: `C[n][r] = C[n−1][r−1] + C[n−1][r]` | O(n²) / O(1) |
| One nCr, no mod, fits in 64 bits | multiplicative: `res = res·(n−i)/(i+1)` for i < r, in order (always exact) | O(r) |
| n huge, p small prime | Lucas: `C(n, r) ≡ ∏ C(nᵢ, rᵢ)` over the base-p digits | O(p + log_p n) |

```cpp
const int N = 1e6 + 5, M = 1e9 + 7;
long long f[N], inf[N];
void init() {
    f[0] = 1; for (int i = 1; i < N; i++) f[i] = f[i-1] * i % M;
    inf[N-1] = power(f[N-1], M-2, M);
    for (int i = N-1; i > 0; i--) inf[i-1] = inf[i] * i % M;
}
long long C(int n, int r) { return (r < 0 || r > n) ? 0 : f[n] * inf[r] % M * inf[n-r] % M; }
```

**Pascal's triangle** is A2Z Part 14: row r, the element at (r, c), and printing the whole triangle. Row n has `C(n, k)` for k = 0..n. Generate a row in O(n) with `C(n, k) = C(n, k−1) · (n−k+1) / k`.

---

## 6. Counting toolkit

| Count | Formula | Example problem |
|---|---|---|
| Grid paths m×n (right/down) | `C(m+n−2, m−1)` | Unique Paths (Part 28 DP gives the same answer) |
| Arrangements of a multiset | `n! / (c₁!·c₂!·…)` | Distinct permutations of "aabb" = 6 |
| Stars and bars | k non-negative ints summing to n: `C(n+k−1, k−1)` | Distributing candies |
| Subsets | 2ⁿ, `C(n, k)` of size k | Power set (Part 18/19) |
| Catalan `Cₙ = C(2n, n)/(n+1)` | 1, 1, 2, 5, 14, 42 | Unique BSTs, valid parentheses, triangulations, Dyck paths |
| Derangements | `D(n) = (n−1)(D(n−1) + D(n−2))` | No element in its own position |
| Inclusion–exclusion | `|A∪B| = |A|+|B|−|A∩B|` and beyond | Count numbers ≤ N divisible by 2, 3 or 5 |
| Pigeonhole | n+1 items in n boxes ⇒ some box has 2 | Find the duplicate (Floyd), prefix sum mod k |

---

## 7. Number-theory facts

- **Divisor count** from `n = ∏ pᵢ^eᵢ` is `∏(eᵢ + 1)`. **Divisor sum** is `∏ (pᵢ^(eᵢ+1) − 1)/(pᵢ − 1)`.
- **Euler's φ(n)** is `n · ∏(1 − 1/p)`, counting the 1..n coprime to n. Sieve it over a range in O(n log log n).
- **Perfect squares** are exactly the numbers with an odd number of divisors (the Bulb Switcher answer is ⌊√n⌋).
- **Trailing zeros of n!** are `Σ ⌊n / 5ᵏ⌋` (Legendre's formula with p = 5).
- **Divisibility rules:** 3 and 9 use the digit sum, 11 uses the alternating digit sum.
- **Mod of a huge string number:** process it digit by digit with `r = (r·10 + d) % m`.
- **Prime counting:** about `n / ln n` primes are ≤ n. Prime gaps are small, so "next prime" searches are cheap.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| `a * b % M` overflowing 32-bit | Cast to 64-bit before multiplying |
| Negative result after subtraction | `(x % M + M) % M` |
| Dividing under mod | Multiply by the inverse |
| Fermat inverse with a non-prime modulus | Extended Euclid, and check gcd = 1 |
| Using factorials without a mod for n > 20 | 21! overflows int64 |
| `lcm = a*b/gcd` overflowing | `a / gcd * b` |
| Pow(x, n) with n = INT_MIN | Negate it as a long |

---

## Practice

<details><summary>1. 3¹³ mod 7 using binary exponentiation?</summary>

13 = 1101₂. The squares are 3, 2, 4, 2 (mod 7). Take the factors for bits 0, 2 and 3: 3·4·2 = 24 ≡ 3. Check: 3⁶ ≡ 1, so 3¹³ = 3¹²·3 ≡ 3.
</details>

<details><summary>2. Inverse of 3 mod 11?</summary>

3⁹ mod 11 = 4, and 3·4 = 12 ≡ 1. ✓
</details>

<details><summary>3. Unique paths in a 3×7 grid?</summary>

C(8, 2) = 28.
</details>

<details><summary>4. Number of structurally unique BSTs with 4 nodes?</summary>

Catalan C₄ = 14.
</details>

<details><summary>5. Trailing zeros of 100!?</summary>

20 + 4 = 24.
</details>

<details><summary>6. Why can't you compute nCr mod 10⁹ with factorials and Fermat?</summary>

10⁹ is not prime (it is 2⁹·5⁹), so many factorials have no inverse. Use Pascal for small n, or the CRT with prime-power Lucas.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Modular inverse | x with ax ≡ 1 (mod m) |
| Fermat's little theorem | a^(p−1) ≡ 1 (mod p) for p ∤ a |
| Bézout | ax + by = gcd(a, b) has an integer solution |
| Catalan number | C(2n, n)/(n+1), counting balanced structures |
| φ(n) | Count of 1..n coprime to n |

---

## Flashcards

**Why 10⁹+7?** #flashcard
It is prime (so inverses exist), it fits in int32, and its square fits in int64.

**Modular inverse when p is prime?** #flashcard
a^(p−2) mod p, by Fermat.

**nCr mod p in O(1) per query?** #flashcard
Precompute fact and invFact up to n; then fact[n]·invFact[r]·invFact[n−r].

**Inverse factorials in O(n)?** #flashcard
invFact[n] = fact[n]^(p−2), then go downwards: invFact[i−1] = invFact[i]·i.

**Catalan applications?** #flashcard
Unique BSTs, balanced parentheses, triangulations, Dyck paths.

**Safe modular subtraction?** #flashcard
((a − b) % M + M) % M.

---

**Interview track →** [Math and number theory](../../02-algorithms/18-math-and-number-theory.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md)
