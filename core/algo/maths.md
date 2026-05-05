# Mathematics — SDE-3 Gold Standard

Mathematical patterns that collapse O(N) loops to O(√N) or O(log N). SDE-3 expects: sieve correctness, fast exponentiation, modular arithmetic fluency, and knowing when geometry reduces to integer algebra.

---

## Theory & Mental Models

**What it is.** Number theory, combinatorics, and modular arithmetic underlie a class of problems where the mathematical structure *is* the algorithm. Core invariant: find the formula or mathematical shortcut rather than simulating step by step.

**Why it exists.** Brute-force simulation of prime checking, large powers, or combinatorics is too slow. Mathematical identities collapse these: trial division checks primality in O(√N) instead of O(N); binary exponentiation computes a^n in O(log n) instead of O(n); precomputed factorials answer nCr in O(1) instead of O(r).

**The mental model.** Math problems have closed-form or formula-based solutions. The skill is recognizing which formula applies, not re-deriving it: "count primes ≤ N" → sieve; "GCD of two numbers" → Euclidean; "large power mod M" → fast exponentiation; "number of ways to choose k from n" → precomputed nCr.

**Complexity at a glance.**

| Algorithm | Time | Space |
| :--- | :--- | :--- |
| Primality test (trial division) | O(√N) | O(1) |
| Sieve of Eratosthenes | O(N log log N) | O(N) |
| Euclidean GCD | O(log min(a, b)) | O(1) |
| Fast exponentiation | O(log n) | O(1) |
| nCr with factorial precomputation | O(N) build, O(1) query | O(N) |

**When to reach for it.**
- Prime factorization or counting primes up to N — sieve.
- Combinatorics (number of ways to choose, arrange, partition) — precomputed nCr or Pascal's triangle.
- Large numbers mod M — apply mod at every multiplication step; use Fermat's little theorem for division.
- Geometry that involves collinearity or slope comparison — use GCD-normalized integer tuples, not floats.
- Digit-based problems or number-structure problems (trailing zeros, ugly numbers, digital root).

**When NOT to use it.**
- No mathematical formula exists — simulate directly.
- K is large in counting sort / sieve — memory blowup.

**Common mistakes.**
- Integer overflow: `a * b mod m` — compute `(a mod m) * (b mod m) mod m`; in Python big int is automatic but state it for other languages.
- Floating-point slope comparison — use GCD-normalized integer tuples `(dy//g, dx//g)` to avoid rounding errors.
- Forgetting modular inverse for division under modulo — `a / b mod m = a * b^(m-2) mod m` when m is prime (Fermat).
- `n // 2` vs `n / 2` type mismatch — integer division in Python 3 requires `//`.

---

## 1. Algorithm Selection

> [!IMPORTANT]
> **The Click Moment**: "Count **primes** up to N" → Sieve. "**Divisible** / GCD / LCM" → Euclidean. "Large power **mod M**" → binary exponentiation. "Overflow in a×b before mod" → divide first: `a // gcd(a,b) * b`. "**Same line** / collinear" → cross product (no floats). "**Modular inverse**" → Fermat's little theorem when M is prime; Extended Euclidean otherwise.

| Goal | Algorithm | Complexity |
| :--- | :--- | :--- |
| All primes ≤ N | Sieve of Eratosthenes | O(N log log N) |
| Is N prime? | Trial division | O(√N) |
| GCD of a, b | Euclidean algorithm | O(log min(a,b)) |
| a^n mod M | Binary exponentiation | O(log n) |
| nCr mod prime p | Precomputed factorials + Fermat inverse | O(N + log N) |
| Collinear points | Cross product / GCD-normalized slope | O(1), no float error |

---

## 2. Core Algorithms & Click Moments

### Sieve of Eratosthenes — All Primes ≤ N

> [!IMPORTANT]
> **The Click Moment**: "Count primes" — OR — "is each number prime?" — OR — "smallest prime factor of every number" (linear sieve). Sieve is the canonical O(N log log N) all-primes algorithm; trial division per number would be O(N √N).

```python
def sieve(n: int) -> list[bool]:
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1
    return is_prime

def count_primes(n: int) -> int:
    return sum(sieve(n - 1)) if n > 1 else 0  # count primes strictly less than n

def smallest_prime_factor(n: int) -> list[int]:
    spf = list(range(n + 1))
    p = 2
    while p * p <= n:
        if spf[p] == p:  # p is still prime
            for multiple in range(p * p, n + 1, p):
                if spf[multiple] == multiple:
                    spf[multiple] = p
        p += 1
    return spf

def factorize(x: int, spf: list[int]) -> list[int]:
    factors = []
    while x > 1:
        factors.append(spf[x])
        x //= spf[x]
    return factors

#### Common Variants & Twists
1. **Four Divisors**:
   - **What (The Problem & Goal):** Given an array of integers, return the sum of divisors of integers in the array that have exactly four divisors.
   - **How (Intuition & Mental Model):** A number has exactly 4 divisors if it's either `p * q` (where `p, q` are distinct primes) or `p^3` (where `p` is prime). Use a sieve to precompute primes or smallest prime factors to check this condition efficiently.
2. **Closest Prime Numbers in Range**:
   - **What (The Problem & Goal):** Find the two closest primes in the range `[left, right]`.
   - **How (Intuition & Mental Model):** Use a segmented sieve if the range is far from zero, or a standard sieve if `right` is within a few millions. Collect all primes in the range and find the pair with the minimum difference.
```

> [!TIP]
> **Smallest Prime Factor (SPF) sieve**: `spf[i]` = smallest prime dividing i. Factorize any number k in O(log k) after O(N log log N) precomputation — `while k > 1: factors.append(spf[k]); k //= spf[k]`. This is the engine for "count divisors" and "group numbers by prime factor" problems (e.g., Largest Component Size by Common Factor).

---

### GCD, LCM, and Extended Euclidean

> [!IMPORTANT]
> **The Click Moment**: "Greatest common divisor" — OR — "reduce a fraction" — OR — "coprime check" — OR — "**modular inverse**" (use Extended Euclidean when M is not prime, or Fermat's little theorem when M is prime). `gcd(0, a) = a` — handle zeros explicitly.

```python
import math

def gcd(a: int, b: int) -> int:
    return a if b == 0 else gcd(b, a % b)  # or math.gcd(a, b)

def lcm(a: int, b: int) -> int:
    return a // math.gcd(a, b) * b  # divide BEFORE multiply to prevent overflow

def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y  # g, x, y such that a*x + b*y = g

def modular_inverse(a: int, m: int) -> int:
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse mod {m} (not coprime)")
    return x % m

#### Common Variants & Twists
1. **Water and Jug Problem**:
   - **What (The Problem & Goal):** You have two jugs with capacities `x` and `y`. Can you measure exactly `z` liters using these jugs?
   - **How (Intuition & Mental Model):** This is a direct application of Bézout's Identity. You can measure `z` liters if and only if `z <= x + y` and `z` is a multiple of `gcd(x, y)`.
2. **Simplified Fractions**:
   - **What (The Problem & Goal):** Given `n`, return a list of all simplified fractions `a/b` such that `0 < a < b <= n`.
   - **How (Intuition & Mental Model):** A fraction `a/b` is simplified if `gcd(a, b) == 1`. Iterate through all `b` from `2` to `n` and `a` from `1` to `b-1`, checking the GCD.
```

> [!CAUTION]
> **LCM overflow**: `a * b // gcd(a, b)` computes `a*b` first — overflows in Java/C++ for large inputs. Always write `a // gcd(a, b) * b` (divide before multiply). Python integers are arbitrary precision but the habit matters when reasoning about other languages in interviews.

---

### Binary Exponentiation (Fast Power)

> [!IMPORTANT]
> **The Click Moment**: "Compute **x^n mod M**" — OR — "**Fibonacci in O(log N)** via matrix exponentiation" — OR — "**modular inverse** when M is prime" (`x^(M-2) mod M` by Fermat's little theorem). Halving the exponent at each step → O(log n).

```python
def fast_pow(base: int, exp: int, mod: int = 0) -> int:
    if exp < 0:
        base, exp = modular_inverse(base, mod), -exp
    result = 1
    base = base % mod if mod else base
    while exp:
        if exp & 1:
            result = result * base % mod if mod else result * base
        base = base * base % mod if mod else base * base
        exp >>= 1
    return result

def matrix_mult(A: list[list[int]], B: list[list[int]], mod: int) -> list[list[int]]:
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k] == 0:
                continue
            for j in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def fibonacci_log_n(n: int, mod: int = 10**9 + 7) -> int:
    if n <= 1:
        return n

    def mat_pow(M: list[list[int]], p: int) -> list[list[int]]:
        result = [[1, 0], [0, 1]]  # identity
        while p:
            if p & 1:
                result = matrix_mult(result, M, mod)
            M = matrix_mult(M, M, mod)
            p >>= 1
        return result

    M = [[1, 1], [1, 0]]
    return mat_pow(M, n)[0][1]

#### Common Variants & Twists
1. **Modular Inverse when M is NOT prime**:
   - **What (The Problem & Goal):** Find `x` such that `ax ≡ 1 (mod m)` where `m` is not prime but `gcd(a, m) = 1`.
   - **How (Intuition & Mental Model):** Fermat's Little Theorem fails here. Use the Extended Euclidean Algorithm to solve `ax + my = 1`. The value `x % m` is the modular inverse.
2. **Count Good Numbers**:
   - **What (The Problem & Goal):** A number is "good" if digits at even indices are even (0, 2, 4, 6, 8) and digits at odd indices are prime (2, 3, 5, 7). Find the count of good numbers of length `n` mod `10^9 + 7`.
   - **How (Intuition & Mental Model):** There are `ceil(n/2)` even indices and `floor(n/2)` odd indices. The answer is `5^(ceil(n/2)) * 4^(floor(n/2)) % (10^9 + 7)`. Use fast exponentiation to compute this in O(log n).
```

> [!CAUTION]
> **INT_MIN overflow in Java/C++**: Negating `exp` when `exp = INT_MIN` (-2^31) overflows to INT_MIN again because INT_MAX = 2^31 - 1. Cast to `long` before negating. Python integers are arbitrary precision — not an issue here, but mention it in interviews.

---

### Modular Arithmetic — Large Combinations

> [!IMPORTANT]
> **The Click Moment**: "Answer **mod 10^9+7**" — OR — "**large nCr** mod prime". Apply mod at every addition and multiplication step. Precompute factorials and inverse factorials once in O(N); then each nCr query is O(1).

```python
MOD = 10**9 + 7

def precompute_factorials(n: int, mod: int = MOD) -> tuple[list[int], list[int]]:
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i-1] * i % mod
    inv_fact = [1] * (n + 1)
    inv_fact[n] = fast_pow(fact[n], mod - 2, mod)  # Fermat: fact[n]^(mod-2) mod mod
    for i in range(n - 1, -1, -1):
        inv_fact[i] = inv_fact[i+1] * (i+1) % mod
    return fact, inv_fact

def nCr_mod(n: int, r: int, fact: list[int], inv_fact: list[int], mod: int = MOD) -> int:
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % mod * inv_fact[n-r] % mod

#### Common Variants & Twists
1. **Lucas Theorem for nCr mod p**:
   - **What (The Problem & Goal):** Compute `nCr mod p` where `n` is very large but `p` is a small prime.
   - **How (Intuition & Mental Model):** Break `n` and `r` into their base-p representations. `nCr mod p ≡ Π (n_i C r_i) mod p`. This allows computing `nCr` for `n > 10^9` as long as `p` is small.
2. **Count Subarrays with Sum Divisible by K**:
   - **What (The Problem & Goal):** Find the number of non-empty subarrays whose sum is divisible by `k`.
   - **How (Intuition & Mental Model):** Use prefix sums and modular arithmetic. If `prefix_sum[j] % k == prefix_sum[i] % k`, then the subarray `sum(i+1, j)` is divisible by `k`. Use a frequency map to count occurrences of each remainder.
```

---

### Number Theory Tricks

```python
def count_trailing_zeros_factorial(n: int) -> int:
    count = 0
    power_of_5 = 5
    while power_of_5 <= n:
        count += n // power_of_5
        power_of_5 *= 5
    return count

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def max_points_on_line(points: list[list[int]]) -> int:
    if len(points) <= 2:
        return len(points)
    max_pts = 1
    for i in range(len(points)):
        slopes: dict = {}
        duplicate = 1
        for j in range(i + 1, len(points)):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            if dx == 0 and dy == 0:
                duplicate += 1
                continue
            g = math.gcd(abs(dy), abs(dx))
            slope = (dy // g, dx // g)
            if dx < 0:  # normalize sign: always keep dx non-negative
                slope = (-slope[0], -slope[1])
            slopes[slope] = slopes.get(slope, 0) + 1
        local_max = max(slopes.values()) if slopes else 0
        max_pts = max(max_pts, local_max + duplicate)
    return max_pts

#### Common Variants & Twists
1. **Ugly Number III**:
   - **What (The Problem & Goal):** Find the n-th "ugly" number which is divisible by `a`, `b`, or `c`.
   - **How (Intuition & Mental Model):** Use binary search on the answer. To count how many numbers `<= x` are divisible by `a, b, or c`, use the Principle of Inclusion-Exclusion: `count = x/a + x/b + x/c - x/lcm(a,b) - x/lcm(b,c) - x/lcm(a,c) + x/lcm(a,b,c)`.
2. **Minimum Moves to Equal Array Elements II**:
   - **What (The Problem & Goal):** Given an array, find the minimum moves (increment/decrement) to make all elements equal.
   - **How (Intuition & Mental Model):** The target value must be the **median** of the array. The sum of absolute differences from the median is the minimum possible sum.
```

> [!CAUTION]
> **Max Points on a Line gotchas**: (1) Represent slope as `(dy/g, dx/g)` with GCD normalization — `(-2/3)` and `(2/-3)` must map to the same key. (2) Normalize the sign (keep dx ≥ 0). (3) Count **duplicate points** separately — they lie on every line through the anchor. Missing duplicates is the #1 bug.

---

## 3. SDE-3 Deep Dives

### Scalability: Segmented Sieve for Huge N

> [!TIP]
> Standard sieve uses O(N) memory — infeasible for N = 10^12. **Segmented sieve**: first sieve primes up to √N (fits in RAM), then process the range [lo, hi] in √N-sized blocks. Each block is O(√N) memory. Total time is still O(N log log N). Used in competitive programming for N up to 10^10 and in distributed prime generation systems.

### Scalability: Chinese Remainder Theorem (CRT)

> [!TIP]
> CRT lets you reconstruct a large number from remainders modulo small coprime moduli. Application: compute a huge product modulo multiple small primes in parallel on different machines, then combine with CRT. Used in FFT-based polynomial multiplication (number-theoretic transform) and multi-party computation protocols.

### Concurrency: Thread-Safe Prime Cache

> [!TIP]
> A sieve computed once at startup is read-only and needs no locking — safe for concurrent reads. For an incremental primality service: maintain a sorted set of known primes protected by a `ReadWriteLock` (Java) or `threading.RLock` (Python). On query for n: acquire read lock, trial-divide against known primes ≤ √n; if n is new prime, upgrade to write lock and insert. The read path scales linearly with threads.

### Trade-offs: Float vs Integer Arithmetic

| Problem | Float approach | Integer approach | Prefer |
| :--- | :--- | :--- | :--- |
| Slope of two points | `dy/dx` | `(dy//g, dx//g)` tuple | **Integer** — no rounding error |
| Distance comparison | `math.hypot(dx,dy)` | `dx*dx + dy*dy` (compare squared) | Integer for comparison, float for output |
| nCr | `math.comb(n,r)` | Precomputed factorials + modular inverse | **Modular integer** when answer is large |
| Primality | Miller-Rabin (probabilistic) | Trial division | Trial div for N ≤ 10^7; Miller-Rabin for N ≤ 10^18 |

---

## 4. Common Interview Problems

### Easy / Medium
- **Count Primes** — Sieve of Eratosthenes; count `True` values in `is_prime[:n]`.
- **Pow(x, n)** — Binary exponentiation; handle `n < 0` by inverting x.
- **GCD / LCM of Array** — Reduce with `math.gcd`; LCM: `a // gcd(a,b) * b`.
- **Factorial Trailing Zeros** — Count factors of 5 via Legendre's formula.
- **Integer Square Root** — Binary search on `[0, x]` with `mid <= x // mid`.

### Hard
- **Max Points on a Line** — Per anchor: GCD-normalized slope frequency map.
- **Super Pow** — `a^(b mod phi(mod)) mod mod` via Euler's theorem; handle non-coprime case.
- **Count of Range Sum** — Merge sort on prefix sums; count cross-half pairs in `[lower, upper]`.
- **Nth Digit** — Determine which digit group (1-digit, 2-digit…); offset within the number.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Pow(x, n)** | Exponentiation by Squaring | "Fast exponentiation; n can be negative" | Square x, halve n; if n odd multiply result by x once | `n = INT_MIN` overflow in Java/C++ — use `long`. Negative n: `base = 1/base, exp = -exp`. |
| **Sqrt(x)** | "Integer square root without `math.sqrt`" | Binary search `[0, x]` with `mid <= x // mid` | `mid*mid` overflow — compare as `mid <= x // mid` (integer division). Floor vs ceiling. |
| **Count Primes** | "Count primes strictly less than n" | Sieve: mark composites from each prime p starting p² | `is_prime[0] = is_prime[1] = False`. Inner loop starts at `p*p`, not `2*p`. |
| **Factorial Trailing Zeros** | "Count (2,5) factor pairs = count 5s in n!" | Sum `n//5 + n//25 + n//125 + …` until power > n | More 2s than 5s — count only 5-factors. Integer division, no floats. |
| **Max Points on a Line** | "Group by slope; find max frequency" | Per anchor: GCD-normalize `(dy, dx)` slope; count per slope | Same point = duplicate, not a slope. Normalize sign: `dx < 0 → flip both`. |
| **Random Pick with Weight** | "Weighted random choice" | Prefix sums + binary search on random value in `[0, total)` | `random.randint(0, total-1)` is inclusive; `random.random() * total` is `[0, total)`. Zero weights excluded. |
| **Integer Break** | "Split n to maximize product" | Break into 3s for n≥4; avoid breaking into 1s | AM-GM: e≈2.718 → 3 is optimal integer. Handle n=2 (→1×1=1? No, must split: return 1), n=3 (→ 1×2=2). |
| **Bulb Switcher** | "How many bulbs on after n rounds?" | Bulb i toggled by each of its divisors; odd count ↔ perfect square | Divisors pair up except for perfect squares. Answer = `int(n**0.5)`. |
| **GCD of Array** | "Reduce via Euclidean iteratively" | `functools.reduce(math.gcd, nums)` | `gcd(0, a) = a` — handle zeros. LCM can overflow for large arrays; use Python big int. |
| **Add Digits [E]** | "Repeat digit sum until single digit" | Digital root: `1 + (n-1) % 9`; special case n=0 | O(1) formula, not a loop. `n=0` → 0; otherwise digital root formula. |
| **Excel Sheet Column Number [E]** | "Convert Excel column title (A, Z, AA…) to number" | Treat as base-26: `result = result * 26 + ord(ch) - ord('A') + 1` | 1-indexed not 0-indexed ('A'=1, not 0). No zero in this base-26 encoding. |
| **Happy Number [E]** | "Does repeated digit-square-sum reach 1?" | Floyd's cycle detection or known cycle set `{4,16,37,58,89,145,42,20}` | If not happy, always cycles through `{4,...,20}`. Stop when `n==1` (happy) or `n in cycle`. |
| **Ugly Number II [M]** | "Nth number whose only prime factors are 2, 3, 5" | Three pointers for multiples of 2, 3, 5; advance min pointer each step | Tie case: all three pointers at same value → advance all three to avoid duplicates. |
| **Perfect Squares [M]** | "Minimum number of perfect squares summing to n" | DP: `dp[i] = min(dp[i - j*j] + 1)` for all j; or Lagrange's 4-square theorem | Lagrange theorem: answer ≤ 4. Check 1, then 2 (two-sum of squares), else answer is 3 or 4. |
| **Fraction to Recurring Decimal [M]** | "Detect repeating decimal in long division" | Map remainder → position; repeat starts when remainder seen again | Handle sign separately: XOR numerator and denominator signs. `denominator = 0` not tested but guard anyway. |
| **Nth Digit [M]** | "Find nth digit in infinite sequence 123456789101112…" | Determine which digit group (d-digit numbers); offset within the number | d-digit numbers: count = 9×10^(d-1); total digits = count×d. Use integer division to pinpoint exact digit. |
| **Count Different Palindromic Subsequences [H]** | "Count distinct palindromic subsequences in string" | DP: `dp[i][j]` = count in `s[i..j]`; case on `s[i]==s[j]` and inner occurrences | When `s[i]==s[j]`: add `dp[i+1][j-1]*2 + 2` if no inner match, `+1` if one inner match, `+0` if two inner matches (avoids double-count). Answer mod 10^9+7. |
| **Super Pow [H]** | "Compute a^b mod 1337 where b is huge integer array" | `a^(b mod phi(m)) mod m` via Euler's theorem; process b digit by digit | Euler's theorem requires gcd(a,m)=1. 1337=7×191 (not prime) — use CRT or direct modular exponentiation cycling. |

---

## Quick Revision Triggers

- "Is N prime?" → trial division up to √N; sieve if checking many numbers.
- "All primes up to N" → Sieve of Eratosthenes, O(N log log N).
- "GCD / LCM of two numbers" → `math.gcd(a, b)`; `lcm = a * b // gcd`.
- "Compute `a^b mod m` efficiently" → `pow(a, b, m)` in Python (built-in fast exponentiation).
- "Division under modular arithmetic (mod is prime)" → Fermat: `a^(-1) mod p = pow(a, p-2, p)`.
- "Count combinations `nCr mod p`" → precompute factorials and inverse factorials; `nCr = fact[n] * inv_fact[r] * inv_fact[n-r] % p`.
- "Avoid float for slope / ratio comparisons" → normalize to `(dy/gcd, dx/gcd)` tuple; use integer arithmetic.

---

## See also

- [Bit Manipulation](bit-manipulation.md) — powers of two, parity, GCD via binary method
- [Divide and Conquer](divide-and-conquer.md) — fast exponentiation derivation; Master Theorem
- [Dynamic Programming](dynamic-programming/README.md) — DP for combinatorics (ways to sum, partition)
- [Patterns Master](../../../reference/patterns/patterns-master.md) — math pattern recognition triggers
