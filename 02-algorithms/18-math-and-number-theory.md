---
module: 02-algorithms
topic: Math & Number Theory
tags: [algorithms, math, number-theory]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Know patterns cold.
> `💤 T3` — **TIER 3 · Skim or Skip**: Conceptual awareness only.

## First-Principles Map

```
WHY math tricks exist → WHEN to use → WHAT can go wrong
        │                    │               │
  [Integer division,    ["Happy Number",  [Integer overflow
   modular arithmetic,   "Palindrome       (use Python — no
   prime testing,        Number", digits,  overflow); off-by-
   GCD/LCM show up       overflow, prime   one in prime sieve;
   in ~1 problem per     tests, count      double-to-int
   5 Google rounds —     ways (modular)]   precision loss]
   fast recognition
   beats derivation]
```

---

# Math & Number Theory — L3 Reference

---

## 1. Integer & Digit Tricks

### Digit Extraction Pattern

```python
def digit_operations(n: int) -> None:
    # Extract digits one by one (right to left)
    while n > 0:
        digit = n % 10      # last digit
        n //= 10            # remove last digit

def reverse_integer(x: int) -> int:
    sign = -1 if x < 0 else 1
    x = abs(x)
    rev = int(str(x)[::-1])
    # Clamp to 32-bit signed range
    return sign * rev if rev <= 2**31 - 1 else 0

def is_palindrome_number(x: int) -> bool:
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    reverted = 0
    while x > reverted:
        reverted = reverted * 10 + x % 10
        x //= 10
    return x == reverted or x == reverted // 10  # even/odd length
```

> [!TIP]
> **Palindrome Number** without string conversion: reverse only the second half of the number, then compare. Stop when `x <= reverted`. Works in O(log N) without strings.

---

## 2. Happy Number

> [!IMPORTANT]
> **The Click Moment**: "Sum of squares of digits" — detect a cycle using Floyd's algorithm (fast/slow) or a hash set. If 1 is reached → happy. If cycle contains any non-1 value → not happy.

```python
def is_happy(n: int) -> bool:
    def digit_square_sum(x: int) -> int:
        total = 0
        while x:
            total += (x % 10) ** 2
            x //= 10
        return total

    seen = set()
    while n != 1:
        if n in seen:
            return False
        seen.add(n)
        n = digit_square_sum(n)
    return True
```

**Known fact**: unhappy numbers always cycle back to 4. So an alternative check is `n == 4`.

---

## 3. GCD, LCM, and Euclidean Algorithm

```python
import math

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)

# Python built-in
math.gcd(12, 8)   # → 4
math.lcm(4, 6)    # → 12  (Python 3.9+)
```

**Euclidean algorithm intuition**: `gcd(a, b) = gcd(b, a % b)`. The remainder gets strictly smaller each step → terminates in O(log min(a,b)).

**When to use**: LCM for "after how many steps do X and Y sync?"; GCD for "reduce a fraction" or "tile a rectangle with squares".

---

## 4. Prime Testing & Sieve

### Is Prime (single number)?

```python
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:           # only check up to √n
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
```

> [!TIP]
> **Why √n?** Any composite number `n` has a factor ≤ √n. If you checked all numbers up to √n and found none, `n` must be prime.

### Sieve of Eratosthenes (all primes ≤ N)

```python
def sieve_of_eratosthenes(n: int) -> list[int]:
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i, v in enumerate(is_prime) if v]
    # Time: O(N log log N) | Space: O(N)
```

**LeetCode context**: Count Primes (LC 204) uses this directly.

---

## 5. Fast Power (Modular Exponentiation)

> [!IMPORTANT]
> **The Click Moment**: "x^n mod m" or just "x to the power n" with n up to 10^9. Naive O(n) → TLE. Binary exponentiation → O(log n).

```python
def my_pow(x: float, n: int) -> float:
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n:
        if n % 2 == 1:        # odd exponent: multiply result by x
            result *= x
        x *= x                # square the base
        n //= 2
    return result

def pow_mod(base: int, exp: int, mod: int) -> int:
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = result * base % mod
        base = base * base % mod
        exp //= 2
    return result

# Python built-in (preferred)
pow(2, 100, 10**9 + 7)   # fast modular power built-in
```

---

## 6. Modular Arithmetic

```python
MOD = 10**9 + 7   # standard Google/LeetCode prime modulus

# Addition and multiplication are safe with mod
(a + b) % MOD
(a * b) % MOD

# Subtraction: prevent negative result
(a - b + MOD) % MOD

# Division (modular inverse via Fermat's little theorem for prime MOD)
# a / b mod p = a * pow(b, p-2, p) mod p
def mod_div(a: int, b: int, p: int) -> int:
    return a * pow(b, p - 2, p) % p
```

> [!CAUTION]
> **Never compute `(a + b) % MOD` with Python's `//` for division.** Modular division requires the modular inverse: `a * pow(b, MOD-2, MOD) % MOD` (only valid when MOD is prime — which 10^9+7 is).

---

## 7. Factorial & Combinatorics

```python
import math

math.factorial(10)   # 3628800

def n_choose_k(n: int, k: int) -> int:
    return math.comb(n, k)   # Python 3.8+

# Iterative nCr without overflow (Python ints are arbitrary-size)
def comb_iter(n: int, k: int) -> int:
    k = min(k, n - k)   # symmetry
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result
```

---

## 8. Roman Numerals & Number Conversion

```python
def int_to_roman(num: int) -> str:
    val = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
    syms = ["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
    result = ""
    for v, s in zip(val, syms):
        while num >= v:
            result += s
            num -= v
    return result

def roman_to_int(s: str) -> int:
    table = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    result = 0
    for i in range(len(s)):
        if i + 1 < len(s) and table[s[i]] < table[s[i+1]]:
            result -= table[s[i]]
        else:
            result += table[s[i]]
    return result
```

---

## 9. Overflow & Edge Cases in Python

> [!NOTE]
> Python integers have **arbitrary precision** — no integer overflow. However:
> - Problems that simulate 32-bit signed integer behavior (e.g. `atoi`, `Add Two Numbers`) require explicit clamping to `[-2^31, 2^31 - 1]`.
> - Float precision: use `math.isclose(a, b)` instead of `==` for floats.
> - For languages like Java/C++ where overflow matters: check before multiply with `Integer.MAX_VALUE / a >= b`.

```python
INT_MAX = 2**31 - 1   # 2147483647
INT_MIN = -(2**31)    # -2147483648

def clamp_32bit(n: int) -> int:
    return max(INT_MIN, min(INT_MAX, n))
```

---

## Canonical Interview Problems

| Problem | Tier | Pattern | Key Insight |
|:--------|:-----|:--------|:------------|
| **Palindrome Number `⚡ T1`** | Easy | Digit reversal | Reverse second half; compare; handle negatives and trailing-zero edge cases |
| **Reverse Integer `🎯 T2`** | Easy | Digit extraction | `rev = rev * 10 + n % 10`; clamp to 32-bit before returning |
| **Happy Number `⚡ T1`** | Easy | Cycle detection | Sum of digit squares; Floyd's or hash set; unhappy → cycle hits 4 |
| **Count Primes `🎯 T2`** | Medium | Sieve of Eratosthenes | Mark composite from `i*i`; O(N log log N) |
| **Pow(x, n) `⚡ T1`** | Medium | Binary exponentiation | Square and halve; handle negative `n` |
| **Roman to Integer `⚡ T1`** | Easy | Greedy subtraction rule | If current < next, subtract; else add |
| **Integer to Roman `🎯 T2`** | Medium | Greedy max-value match | Descend table; subtract while `num >= val` |
| **Excel Sheet Column Number `🎯 T2`** | Easy | Base-26 conversion | `result = result * 26 + ord(c) - ord('A') + 1` |
| **Factorial Trailing Zeroes `🎯 T2`** | Medium | Count factor-5 | `n//5 + n//25 + n//125 + ...` (each 5 pairs with a 2 to make 10) |
| **Sqrt(x) `🎯 T2`** | Easy | Binary search | BS on `[0, x]`; find largest `m` with `m*m <= x` |
| **GCD of Strings `⚡ T1`** | Easy | GCD property | If `s + t == t + s` then divisor exists; answer is `s[:gcd(len(s), len(t))]` |
| **Nth Digit `💤 T3`** | Medium | Digit math | Count digits in 1-digit, 2-digit, … groups; locate the number and digit position |

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Gotchas |
|:---------|:-------------|:-----------|:--------|
| **Happy Number `⚡ T1`** | "Sum of squares of digits — detect cycle" | Set or Floyd's; if `n == 1` → happy; if revisit → not happy | Unhappy numbers always converge to 4 — can short-circuit on 4 |
| **Palindrome Number `⚡ T1`** | "Reverse second half, compare" | `while x > reverted`; handle even/odd length | Negatives and numbers ending in 0 (except 0 itself) are not palindromes |
| **Pow(x, n) `⚡ T1`** | "Binary exponentiation — halve n at each step" | `n & 1` check; `x *= x`; `n >>= 1` | `n` can be negative — flip `x` and negate `n`; Python's `**` does not simulate the bit approach |
| **GCD of Strings `⚡ T1`** | "If a common divisor exists, `s+t == t+s`" | `if s+t != t+s: return ""`; `return s[:gcd(len(s), len(t))]` | Check the concat equality first — avoids checking all divisors |
| **Factorial Trailing Zeroes `🎯 T2`** | "Count factor-5 pairs" | `count = n//5 + n//25 + ...` | Factor 2 is always more frequent than 5 — only count 5s |

---

## Quick Revision Triggers

- If "sum of squares of digits, detect loop" → **Happy Number** — hash set or Floyd's.
- If "x^n" with large n → **binary exponentiation** O(log n); never compute naively.
- If "count trailing zeroes in n!" → count factors of 5: `sum(n // 5**i while 5**i <= n)`.
- If "is N prime?" → check divisors up to √N only.
- If "all primes ≤ N" → **Sieve of Eratosthenes** O(N log log N).
- If "GCD" → Euclidean algorithm `while b: a,b = b, a%b`.
- If "(a * b) % MOD needed" → always apply mod after multiply, not before; use Python `pow(b, MOD-2, MOD)` for modular division.

---

## See Also

- [Bit Manipulation](./17-bit-manipulation.md) — XOR tricks, bitmask
- [Binary Search](./11-binary-search.md) — Sqrt(x) via BS on answer
- [Dynamic Programming](./15-dynamic-programming.md) — Combinatorics via DP

---

## Flashcards

**What is binary exponentiation (fast power), and why is it O(log N)?** #flashcard
Binary exponentiation computes `x^n` by squaring `x` and halving `n` at each step. At each iteration: if `n` is odd, multiply the result by the current `x`; always square `x` and halve `n`. Because `n` halves each time, it reaches 0 in `log₂(n)` steps. Time: O(log N), Space: O(1).

**What is the Sieve of Eratosthenes, and what is its time complexity?** #flashcard
Start with a boolean array `is_prime[0..N]` = True. Mark 0 and 1 as False. For each `i` from 2 to √N, if `is_prime[i]` is True, mark all multiples from `i²` onward as False. All remaining True entries are prime. Time: O(N log log N). Space: O(N).

**How do you test if a single integer N is prime efficiently?** #flashcard
Check divisibility by 2 and 3 first, then check only numbers of the form `6k ± 1` up to √N. This works because all primes > 3 are of that form. Time: O(√N).

**How does the Euclidean GCD algorithm work?** #flashcard
`gcd(a, b) = gcd(b, a % b)`. Base case: `gcd(a, 0) = a`. Each step the remainder strictly decreases, so this terminates in O(log min(a, b)) steps. LCM is then `a * b // gcd(a, b)`.
