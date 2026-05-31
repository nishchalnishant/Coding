---
tags: [coding, algorithms, maths]
topic: Mathematics
difficulty: mixed
---

# Mathematics — Problem Reference by Pattern

> [!info] First Principles
> Mathematical patterns collapse O(n) or O(n²) simulations to O(√n) or O(log n) using number-theoretic identities. Core toolkit: (1) Sieve — all primes in O(n log log n); (2) Euclidean GCD — O(log min(a,b)); (3) Fast exponentiation — O(log n); (4) Modular arithmetic — mod at every + and ×; (5) Precomputed factorials + inverse factorials — O(n) build, O(1) query for nCr.

---

## Number Theory — Primes / Sieve

### Count Primes (Sieve of Eratosthenes)

> [!example] Problem
> Count the number of prime numbers strictly less than n.

> [!info] Approach
> - **WHY:** Trial division per number is O(√n) × O(n) = O(n√n). The Sieve marks composites in bulk: starting from p², every multiple of p is composite. Each composite is marked once by its smallest prime factor → O(n log log n) total work.
> - **WHAT:** Boolean array `is_prime[0..n-1]`; mark composites; count remaining True entries.
> - **HOW:** Initialize all True. Set `is_prime[0]=is_prime[1]=False`. For each `p` from 2 to √n: if `is_prime[p]`, mark `p*p, p*p+p, ...` False. Starting at `p²` (not `2p`) because smaller multiples were already marked by smaller primes.

> [!note]- Python Solution
> ```python
> def countPrimes(n: int) -> int:
>     if n < 2:
>         return 0
>     is_prime = [True] * n
>     is_prime[0] = is_prime[1] = False
>     p = 2
>     while p * p < n:
>         if is_prime[p]:
>             for multiple in range(p * p, n, p):
>                 is_prime[multiple] = False
>         p += 1
>     return sum(is_prime)
> ```

> [!success] Complexity
> Time O(n log log n). Space O(n).

> [!tip] Alternatives
> Linear sieve (smallest prime factor) — O(n) time, each composite marked exactly once. Segmented sieve for n > 10^7 (memory constraint). Trial division per number — O(√n) per number, O(n√n) total.

---

### Closest Prime Numbers in Range

> [!example] Problem
> Find the two closest primes in range `[left, right]`. Return the pair with minimum gap, or `[-1, -1]` if fewer than 2 primes exist in range.

> [!info] Approach
> - **WHY:** Collect all primes in `[left, right]` efficiently; scan adjacent pairs for minimum gap.
> - **WHAT:** Sieve `[0, right]` or a segmented sieve for large ranges; filter to `[left, right]`; find min adjacent gap.
> - **HOW:** Standard sieve up to `right`. Collect primes in range. If fewer than 2, return `[-1, -1]`. Linear scan for minimum gap between consecutive primes.

> [!note]- Python Solution
> ```python
> def closestPrimes(left: int, right: int) -> list[int]:
>     if right < 2:
>         return [-1, -1]
>     is_prime = [True] * (right + 1)
>     is_prime[0] = is_prime[1] = False
>     p = 2
>     while p * p <= right:
>         if is_prime[p]:
>             for m in range(p * p, right + 1, p):
>                 is_prime[m] = False
>         p += 1
>     primes = [i for i in range(max(2, left), right + 1) if is_prime[i]]
>     if len(primes) < 2:
>         return [-1, -1]
>     best = None
>     for i in range(len(primes) - 1):
>         gap = primes[i+1] - primes[i]
>         if best is None or gap < best[1] - best[0]:
>             best = [primes[i], primes[i+1]]
>     return best
> ```

> [!success] Complexity
> Time O(right log log right + (right - left)). Space O(right).

> [!tip] Alternatives
> Segmented sieve for very large `right` (memory constrained). Note: twin primes (gap=2) like (3,5), (11,13) are often the answer for large ranges — can exit early on gap=2.

---

## GCD / LCM

### GCD of Strings

> [!example] Problem
> Largest string `t` that divides both strings `s1` and `s2` (i.e., concatenating copies of `t` produces each string).

> [!info] Approach
> - **WHY:** If a GCD string exists, `s1 + s2 == s2 + s1` (necessary condition — both must be periodic with the same period). The GCD string's length = `gcd(len(s1), len(s2))`.
> - **WHAT:** Verify concatenation commutativity; if valid, return `s1[:gcd(len(s1),len(s2))]`.
> - **HOW:** Check `s1 + s2 == s2 + s1`. If True, `gcd_len = gcd(len(s1), len(s2))`; return `s1[:gcd_len]`. If False, return `""`.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def gcdOfStrings(str1: str, str2: str) -> str:
>     if str1 + str2 != str2 + str1:
>         return ""
>     return str1[:gcd(len(str1), len(str2))]
> ```

> [!success] Complexity
> Time O(m + n) for concatenation check. Space O(m + n) for concatenated strings.

> [!tip] Alternatives
> Check divisibility directly by verifying each string is a repetition of the prefix — O(m + n) but more verbose.

---

### Find Greatest Common Divisor of Array

> [!example] Problem
> Find GCD of the maximum and minimum elements of an array.

> [!info] Approach
> - **WHY:** By property of GCD: `gcd(array) = gcd(gcd(a1, a2), a3, ...)`. For GCD of just max and min: `gcd(min(nums), max(nums))`.
> - **WHAT:** `gcd(min(nums), max(nums))` — the GCD of any set is bounded by the GCD of its extremes.
> - **HOW:** Single pass to find min and max; apply Euclidean GCD.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def findGCD(nums: list[int]) -> int:
>     return gcd(min(nums), max(nums))
> ```

> [!success] Complexity
> Time O(n) for min/max + O(log min) for GCD. Space O(1).

> [!tip] Alternatives
> `functools.reduce(gcd, nums)` computes GCD of entire array — not what's asked here but a useful pattern.

---

### Simplified Fractions

> [!example] Problem
> Return all simplified fractions `a/b` with `0 < a < b ≤ n`.

> [!info] Approach
> - **WHY:** Fraction `a/b` is simplified iff `gcd(a, b) = 1` (coprime). Iterate all pairs and filter.
> - **WHAT:** For each `b` from 2 to `n`, for each `a` from 1 to `b-1`, include `a/b` if `gcd(a, b) == 1`.
> - **HOW:** Double loop; GCD check per pair. O(n²) pairs, each O(log n) GCD check.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def simplifiedFractions(n: int) -> list[str]:
>     return [
>         f"{a}/{b}"
>         for b in range(2, n + 1)
>         for a in range(1, b)
>         if gcd(a, b) == 1
>     ]
> ```

> [!success] Complexity
> Time O(n² log n). Space O(n²) output.

> [!tip] Alternatives
> Euler's totient function to count coprime pairs per denominator — more efficient counting but same output list size.

---

### Water Jug Problem (Bézout's Identity)

> [!example] Problem
> Can you measure exactly `target` liters using two jugs of capacities `x` and `y`?

> [!info] Approach
> - **WHY:** By Bézout's Identity, integers `ax + by = z` has a solution iff `z` is a multiple of `gcd(x, y)`. Pouring between jugs is equivalent to computing integer linear combinations of `x` and `y`.
> - **WHAT:** `target` is achievable iff `target ≤ x + y` and `target % gcd(x, y) == 0`.
> - **HOW:** Check both conditions. No simulation needed.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def canMeasureWater(x: int, y: int, target: int) -> bool:
>     if target > x + y:
>         return False
>     if target == 0:
>         return True
>     return target % gcd(x, y) == 0
> ```

> [!success] Complexity
> Time O(log min(x, y)). Space O(1).

> [!tip] Alternatives
> BFS on `(amount_in_jug1, amount_in_jug2)` states — O(x × y) time and space, correct but unnecessary given the math insight.

---

## Modular Arithmetic

### Pow(x, n) (Fast Exponentiation with Mod)

> [!example] Problem
> Compute `x^n` efficiently; handle negative exponents.

> [!info] Approach
> - **WHY:** Naive O(n) multiplication. D&C: `x^n = (x^(n/2))^2`. Each level halves the exponent → O(log n) multiplications.
> - **WHAT:** Iterative binary exponentiation — process bits of `n` from LSB to MSB.
> - **HOW:** If `n` negative: `x = 1/x`, `n = -n`. While `n > 0`: if LSB set, multiply result by `x`; square `x`; right-shift `n`.

> [!note]- Python Solution
> ```python
> def myPow(x: float, n: int) -> float:
>     if n < 0:
>         x, n = 1.0 / x, -n
>     result = 1.0
>     while n:
>         if n & 1:
>             result *= x
>         x *= x
>         n >>= 1
>     return result
> ```

> [!success] Complexity
> Time O(log n). Space O(1).

> [!tip] Alternatives
> Recursive: cleaner but O(log n) stack. `pow(base, exp, mod)` in Python handles modular exponentiation natively and efficiently.

---

### Super Pow (Modular Exponentiation, Non-Prime Mod)

> [!example] Problem
> Compute `a^b mod 1337` where `b` is a large integer given as an array of digits.

> [!info] Approach
> - **WHY:** `b` is too large to compute as an integer. Use the identity: `a^[d1,...,dk] = (a^[d1,...,dk-1])^10 × a^dk`. Process one digit at a time; apply mod throughout.
> - **WHAT:** Iterate digits left to right; maintain running result raised to 10th power each step, multiplied by `a^digit`.
> - **HOW:** `1337 = 7 × 191` (not prime), so Fermat's little theorem doesn't directly apply — use direct modular exponentiation.

> [!note]- Python Solution
> ```python
> def superPow(a: int, b: list[int]) -> int:
>     MOD = 1337
> 
>     def pow_mod(base: int, exp: int) -> int:
>         result, base = 1, base % MOD
>         while exp:
>             if exp & 1:
>                 result = result * base % MOD
>             base = base * base % MOD
>             exp >>= 1
>         return result
> 
>     result = 1
>     for digit in b:
>         result = pow_mod(result, 10) * pow_mod(a, digit) % MOD
>     return result
> ```

> [!success] Complexity
> Time O(n log 1337) ≈ O(n) where n = len(b). Space O(1).

> [!tip] Alternatives
> Euler's theorem: `a^phi(m) ≡ 1 (mod m)` when `gcd(a,m)=1`. Compute `b mod phi(1337)` to reduce exponent. Requires handling `gcd(a,1337) != 1` via CRT.

---

### Count Good Numbers

> [!example] Problem
> A number of length `n` is good if even-indexed positions (0,2,4...) have even digits and odd-indexed positions have prime digits. Count good numbers of length `n` mod 10^9+7.

> [!info] Approach
> - **WHY:** Even positions: 5 choices (0,2,4,6,8); odd positions: 4 choices (2,3,5,7). Positions are independent → multiply. Use fast exponentiation for large `n`.
> - **WHAT:** `answer = 5^(ceil(n/2)) × 4^(floor(n/2)) mod (10^9+7)`.
> - **HOW:** `even_count = (n + 1) // 2` (positions 0, 2, 4, ...); `odd_count = n // 2`. Fast pow for each.

> [!note]- Python Solution
> ```python
> def countGoodNumbers(n: int) -> int:
>     MOD = 10**9 + 7
>     even_count = (n + 1) // 2
>     odd_count = n // 2
>     return pow(5, even_count, MOD) * pow(4, odd_count, MOD) % MOD
> ```

> [!success] Complexity
> Time O(log n). Space O(1).

> [!tip] Alternatives
> Linear O(n) via iterative multiplication — infeasible for n up to 10^15.

---

### Modular Inverse (Extended Euclidean)

> [!example] Problem
> Find `x` such that `a × x ≡ 1 (mod m)`. Works for any `m` (not just prime) when `gcd(a, m) = 1`.

> [!info] Approach
> - **WHY:** Fermat's little theorem (`a^(m-2) mod m`) only works for prime `m`. Extended Euclidean algorithm solves `ax + my = gcd(a,m) = 1` for any `m` coprime to `a`.
> - **WHAT:** Extended GCD returns `(g, x, y)` where `a×x + m×y = g`. If `g=1`, then `x mod m` is the inverse.
> - **HOW:** `extended_gcd(a, m)` → `(g, x, y)`. Inverse = `x % m` if `g == 1`, else no inverse.

> [!note]- Python Solution
> ```python
> def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
>     if b == 0:
>         return a, 1, 0
>     g, x, y = extended_gcd(b, a % b)
>     return g, y, x - (a // b) * y
> 
> def mod_inverse(a: int, m: int) -> int:
>     g, x, _ = extended_gcd(a % m, m)
>     if g != 1:
>         raise ValueError(f"No inverse: gcd({a},{m}) = {g}")
>     return x % m
> 
> # For prime mod: simpler
> def mod_inverse_prime(a: int, p: int) -> int:
>     return pow(a, p - 2, p)  # Fermat's little theorem
> ```

> [!success] Complexity
> Time O(log min(a, m)). Space O(log min(a, m)) recursion.

> [!tip] Alternatives
> Fermat's theorem — O(log p) but only for prime modulus. Iterative extended GCD — O(1) space.

---

## Combinatorics / nCr

### Pascal's Triangle

> [!example] Problem
> Return the first `numRows` rows of Pascal's triangle.

> [!info] Approach
> - **WHY:** Each interior element is the sum of two elements directly above: `C(n,k) = C(n-1,k-1) + C(n-1,k)`. This is the defining recurrence of binomial coefficients.
> - **WHAT:** Build rows iteratively; each row has one more element than the previous.
> - **HOW:** Row `i` has `i+1` elements. `row[j] = prev[j-1] + prev[j]`. Edges are always 1.

> [!note]- Python Solution
> ```python
> def generate(numRows: int) -> list[list[int]]:
>     triangle: list[list[int]] = [[1]]
>     for i in range(1, numRows):
>         row = [1]
>         for j in range(1, i):
>             row.append(triangle[i-1][j-1] + triangle[i-1][j])
>         row.append(1)
>         triangle.append(row)
>     return triangle
> ```

> [!success] Complexity
> Time O(numRows²). Space O(numRows²).

> [!tip] Alternatives
> `math.comb(n, k)` for individual entries. Combinatorial formula `n! / (k!(n-k)!)` for single values.

---

### Pascal's Triangle II

> [!example] Problem
> Return the kth row of Pascal's triangle (0-indexed) using O(k) space.

> [!info] Approach
> - **WHY:** Only need one row; can build in-place by updating right to left to avoid overwriting needed values.
> - **WHAT:** Start with `[1]`; for each new row, insert 1 at start and add adjacent pairs (right to left to avoid using updated values).
> - **HOW:** `row[j] += row[j-1]` from `j = len(row)-1` down to 1; append 1 at end each iteration.

> [!note]- Python Solution
> ```python
> def getRow(rowIndex: int) -> list[int]:
>     row = [1]
>     for i in range(1, rowIndex + 1):
>         for j in range(i - 1, 0, -1):
>             row[j] += row[j-1]
>         row.append(1)
>     return row
> ```

> [!success] Complexity
> Time O(k²). Space O(k).

> [!tip] Alternatives
> Direct formula: `C(k, j) = C(k, j-1) * (k-j+1) / j` — build row in O(k) time with O(k) space using integer arithmetic.

---

### Unique Paths (Combinatorics Approach)

> [!example] Problem
> Count distinct paths from top-left to bottom-right of m×n grid, moving only right or down.

> [!info] Approach
> - **WHY:** Any path makes exactly `(m-1)` down moves and `(n-1)` right moves in some order. Total moves = `m+n-2`; we choose which `m-1` are down moves → `C(m+n-2, m-1)`.
> - **WHAT:** `answer = math.comb(m + n - 2, m - 1)`.
> - **HOW:** Python's `math.comb` computes this exactly in O(min(m,n)) time without overflow using integer arithmetic.

> [!note]- Python Solution
> ```python
> from math import comb
> 
> def uniquePaths(m: int, n: int) -> int:
>     return comb(m + n - 2, m - 1)
> ```

> [!success] Complexity
> Time O(min(m,n)). Space O(1).

> [!tip] Alternatives
> DP: O(m×n) time, O(n) space — needed when obstacles are present. Precomputed factorials + modular inverse for large m,n with mod constraint.

---

## Geometric / Statistical

### Max Points on a Line (GCD-Based Slope)

> [!example] Problem
> Given an array of points, find the maximum number of points that lie on the same line.

> [!info] Approach
> - **WHY:** Floating-point slope representation causes rounding errors — two points with the same true slope may produce different floats. GCD-normalized integer `(dy, dx)` tuple is exact.
> - **WHAT:** For each anchor point, compute normalized slope to every other point; use frequency map to find the most common slope (+ handle duplicates).
> - **HOW:** For each pair `(anchor, other)`: `dx = other.x - anchor.x`, `dy = other.y - anchor.y`. Normalize: `g = gcd(|dy|, |dx|)`, `slope = (dy//g, dx//g)`. Force canonical sign: if `dx < 0`, negate both. Duplicates (same point) counted separately.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def maxPoints(points: list[list[int]]) -> int:
>     if len(points) <= 2:
>         return len(points)
>     max_pts = 1
>     for i in range(len(points)):
>         slopes: dict[tuple, int] = {}
>         duplicates = 1
>         for j in range(i + 1, len(points)):
>             dx = points[j][0] - points[i][0]
>             dy = points[j][1] - points[i][1]
>             if dx == 0 and dy == 0:
>                 duplicates += 1
>                 continue
>             g = gcd(abs(dy), abs(dx))
>             slope = (dy // g, dx // g)
>             if dx < 0:  # canonical: keep dx non-negative
>                 slope = (-slope[0], -slope[1])
>             slopes[slope] = slopes.get(slope, 0) + 1
>         local_max = max(slopes.values()) if slopes else 0
>         max_pts = max(max_pts, local_max + duplicates)
>     return max_pts
> ```

> [!success] Complexity
> Time O(n² log M) where M = max coordinate magnitude (log M for GCD). Space O(n) per anchor for slope map.

> [!tip] Alternatives
> Never use `dy/dx` float — two slopes equal in exact arithmetic diverge in float representation. Cross-product collinearity check avoids division entirely for 3-point tests.

---

### Minimum Moves to Equal Array Elements (Median)

> [!example] Problem
> In each move, increment n-1 elements by 1 (or equivalently, decrement 1 element by 1). Find minimum moves to make all elements equal.

> [!info] Approach
> - **WHY:** Incrementing `n-1` elements by 1 is equivalent to decrementing 1 element by 1. Minimum total absolute deviation from a central value is minimized at the **median** (not mean).
> - **WHAT:** Sort; find median; sum of absolute differences from median.
> - **HOW:** Sort `nums`. Median = `nums[n//2]`. Answer = `sum(|x - median|)`.

> [!note]- Python Solution
> ```python
> def minMoves2(nums: list[int]) -> int:
>     nums.sort()
>     median = nums[len(nums) // 2]
>     return sum(abs(x - median) for x in nums)
> ```

> [!success] Complexity
> Time O(n log n) for sort. Space O(1).

> [!tip] Alternatives
> QuickSelect to find median in O(n) → reduces total to O(n). The "Minimum Moves I" variant (increment n-1 elements) reduces to `sum(nums) - n * min(nums)` without sorting.

---

## Digit / Sequence Math

### Factorial Trailing Zeroes

> [!example] Problem
> Count trailing zeroes in n!.

> [!info] Approach
> - **WHY:** Trailing zeros come from factors of 10 = 2 × 5. There are always more factors of 2 than 5 in n!, so count factors of 5. Each multiple of 5 contributes one 5; multiples of 25 contribute an extra; etc.
> - **WHAT:** `count = n//5 + n//25 + n//125 + ...` until power of 5 exceeds n (Legendre's formula).
> - **HOW:** Iteratively add `n // (5^k)` while `5^k ≤ n`.

> [!note]- Python Solution
> ```python
> def trailingZeroes(n: int) -> int:
>     count = 0
>     power_of_5 = 5
>     while power_of_5 <= n:
>         count += n // power_of_5
>         power_of_5 *= 5
>     return count
> ```

> [!success] Complexity
> Time O(log n). Space O(1).

> [!tip] Alternatives
> Count all prime factors of n! using Legendre's formula — generalizes to any prime p, not just 5.

---

### Integer Square Root (Newton's Method)

> [!example] Problem
> Compute floor of square root of `x` without using `math.sqrt`.

> [!info] Approach
> - **WHY:** Binary search or Newton's method both give O(log x) convergence. Newton's: `r = (r + x//r) // 2` converges quadratically.
> - **WHAT:** Binary search on `[0, x]` for largest `m` where `m² ≤ x`.
> - **HOW:** `lo=0, hi=x`. While `lo ≤ hi`: `mid=(lo+hi)//2`; if `mid*mid ≤ x`, try larger (`lo=mid+1`); else smaller (`hi=mid-1`).

> [!note]- Python Solution
> ```python
> def mySqrt(x: int) -> int:
>     if x < 2:
>         return x
>     lo, hi = 1, x // 2
>     while lo <= hi:
>         mid = lo + (hi - lo) // 2
>         if mid * mid == x:
>             return mid
>         elif mid * mid < x:
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return hi  # floor of sqrt
> 
> # Newton's method variant
> def mySqrt_newton(x: int) -> int:
>     r = x
>     while r * r > x:
>         r = (r + x // r) // 2
>     return r
> ```

> [!success] Complexity
> Binary search O(log x); Newton's O(log log x) iterations (quadratic convergence). Space O(1).

> [!tip] Alternatives
> `int(x**0.5)` — fast but floating-point precision can fail for large x. Always verify with `r*r ≤ x < (r+1)*(r+1)`.

---

### Nth Digit

> [!example] Problem
> Find the nth digit in the infinite sequence `123456789101112131415...`.

> [!info] Approach
> - **WHY:** Group digits by number of digits: 1-digit (9 numbers, 9 digits), 2-digit (90 numbers, 180 digits), etc. Determine which group `n` falls in, then pinpoint the exact number and digit within it.
> - **WHAT:** Subtract group sizes until finding the right group; compute offset.
> - **HOW:** For each digit count `d`: group has `9 × 10^(d-1)` numbers contributing `d × 9 × 10^(d-1)` digits. When `n` falls in group `d`: `num = 10^(d-1) + (n-1)//d`; digit index within `num` = `(n-1) % d`.

> [!note]- Python Solution
> ```python
> def findNthDigit(n: int) -> int:
>     digit_len = 1
>     count = 9
>     start = 1
>     while n > digit_len * count:
>         n -= digit_len * count
>         digit_len += 1
>         count *= 10
>         start *= 10
>     # n is now the nth digit within the digit_len-digit numbers
>     num = start + (n - 1) // digit_len
>     digit_index = (n - 1) % digit_len
>     return int(str(num)[digit_index])
> ```

> [!success] Complexity
> Time O(log n) — at most log₁₀(n) groups. Space O(log n) for string conversion.

> [!tip] Alternatives
> Precompute group boundaries in a table — same asymptotic, avoids recomputation.

---

### Nth Ugly Number (PQ + 3 Pointers)

> [!example] Problem
> Find the nth ugly number (positive integer whose prime factors are only 2, 3, 5).

> [!info] Approach
> - **WHY:** Generate ugly numbers in order; each ugly number = another ugly number × {2, 3, or 5}. Three-pointer approach tracks which ugly number to multiply next by each prime.
> - **WHAT:** Maintain three pointers `p2, p3, p5` into the `ugly` list. Each step: `next = min(ugly[p2]*2, ugly[p3]*3, ugly[p5]*5)`; advance all pointers that produced the minimum.
> - **HOW:** Initialize `ugly=[1]`, `p2=p3=p5=0`. Repeat n-1 times. Advancing all tied pointers prevents duplicates.

> [!note]- Python Solution
> ```python
> def nthUglyNumber(n: int) -> int:
>     ugly = [1]
>     p2 = p3 = p5 = 0
>     for _ in range(n - 1):
>         next2, next3, next5 = ugly[p2]*2, ugly[p3]*3, ugly[p5]*5
>         next_ugly = min(next2, next3, next5)
>         ugly.append(next_ugly)
>         if next_ugly == next2: p2 += 1
>         if next_ugly == next3: p3 += 1
>         if next_ugly == next5: p5 += 1
>     return ugly[-1]
> ```

> [!success] Complexity
> Time O(n). Space O(n).

> [!tip] Alternatives
> Min-heap: push 2, 3, 5; pop min, push × 2, × 3, × 5 with de-duplication via set. O(n log n) — slower than 3-pointer.

---

### Sum of Divisors with 4 Divisors

> [!example] Problem
> Given an integer array, return the sum of all divisors of elements that have exactly 4 divisors.

> [!info] Approach
> - **WHY:** A number n has exactly 4 divisors iff: (1) `n = p³` for prime `p` (divisors: 1, p, p², p³) or (2) `n = p × q` for distinct primes `p, q` (divisors: 1, p, q, pq). Check factorization up to √n.
> - **WHAT:** For each number, count distinct divisors up to √n; accumulate sum if exactly 4 found.
> - **HOW:** For each `num`, trial divide. If exactly 4 divisors, add their sum to result.

> [!note]- Python Solution
> ```python
> def sumFourDivisors(nums: list[int]) -> int:
>     def four_div_sum(n: int) -> int:
>         divisors = []
>         i = 1
>         while i * i <= n:
>             if n % i == 0:
>                 divisors.append(i)
>                 if i != n // i:
>                     divisors.append(n // i)
>             if len(divisors) > 4:
>                 return 0
>             i += 1
>         return sum(divisors) if len(divisors) == 4 else 0
> 
>     return sum(four_div_sum(n) for n in nums)
> ```

> [!success] Complexity
> Time O(n√M) where M = max value. Space O(1) per number.

> [!tip] Alternatives
> SPF (smallest prime factor) sieve — precompute for O(√M) factorization each; faster if range is known.

---

### Min Moves to Equal Array Elements II (Median)

> [!example] Problem
> Each move increments or decrements one element by 1. Minimum moves to make all elements equal.

> [!info] Approach
> - **WHY:** Total moves = sum of absolute differences from the target value. This is minimized at the **median** by the L1 regression property — the median minimizes sum of absolute deviations.
> - **WHAT:** Sort; find median; sum `|x - median|` for all x.
> - **HOW:** Same as "Minimum Moves to Equal Array Elements" variant above.

> [!note]- Python Solution
> ```python
> def minMoves2(nums: list[int]) -> int:
>     nums.sort()
>     median = nums[len(nums) // 2]
>     return sum(abs(x - median) for x in nums)
> ```

> [!success] Complexity
> Time O(n log n). Space O(1).

> [!tip] Alternatives
> QuickSelect for O(n) median → O(n) total. Proof: moving from any non-median target toward the median strictly reduces the total distance.

---

### Count Subarrays Divisible by K

> [!example] Problem
> Count contiguous subarrays whose sum is divisible by k.

> [!info] Approach
> - **WHY:** Subarray sum `sum(i+1..j) = prefix[j] - prefix[i]`. Divisible by k iff `prefix[j] ≡ prefix[i] (mod k)`. So count pairs of equal prefix sums mod k.
> - **WHAT:** Frequency map of `prefix_sum % k`. Each pair of equal remainders contributes one valid subarray.
> - **HOW:** Initialize `remainder_count = {0: 1}` (empty prefix). For each element, update `prefix_sum`, compute `r = prefix_sum % k`; add `remainder_count.get(r, 0)` to answer; increment `remainder_count[r]`. Handle negative remainders: `r = (prefix_sum % k + k) % k`.

> [!note]- Python Solution
> ```python
> def subarraysDivByK(nums: list[int], k: int) -> int:
>     remainder_count: dict[int, int] = {0: 1}
>     prefix_sum = 0
>     count = 0
>     for n in nums:
>         prefix_sum += n
>         r = prefix_sum % k
>         if r < 0:
>             r += k
>         count += remainder_count.get(r, 0)
>         remainder_count[r] = remainder_count.get(r, 0) + 1
>     return count
> ```

> [!success] Complexity
> Time O(n). Space O(k) for remainder frequency map.

> [!tip] Alternatives
> Prefix sum array + O(n²) brute force check — infeasible. Sort remainders and count pairs — O(n log n), unnecessary.

---

## Number Encoding / Conversion

### Integer to Roman

> [!example] Problem
> Convert integer `num` (1 ≤ num ≤ 3999) to its Roman numeral representation.

> [!info] Approach
> - **WHY:** Roman numerals are a greedy positional system. Subtractive forms (IV=4, IX=9, XL=40, ...) can be handled by including them as explicit "values" in the table. Greedily subtract the largest fitting value.
> - **WHAT:** Table of `(value, symbol)` pairs in descending order including all 13 subtractive forms. While `num > 0`: find largest value ≤ num, append symbol, subtract value.
> - **HOW:** 13 symbols: 1000→M, 900→CM, 500→D, 400→CD, 100→C, 90→XC, 50→L, 40→XL, 10→X, 9→IX, 5→V, 4→IV, 1→I.

> [!note]- Python Solution
> ```python
> def intToRoman(num: int) -> str:
>     vals = [
>         (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
>         (100, "C"),  (90, "XC"), (50, "L"),  (40, "XL"),
>         (10, "X"),   (9, "IX"),  (5, "V"),   (4, "IV"),  (1, "I"),
>     ]
>     result = []
>     for value, symbol in vals:
>         while num >= value:
>             result.append(symbol)
>             num -= value
>     return "".join(result)
> ```

> [!success] Complexity
> Time O(1) — num ≤ 3999, loop is bounded. Space O(1).

> [!tip] Alternatives
> Digit-by-digit lookup table for thousands/hundreds/tens/ones — same complexity, more verbose but no loop.

---

### Roman to Integer

> [!example] Problem
> Convert Roman numeral string to integer.

> [!info] Approach
> - **WHY:** Subtractive rule: if a smaller value appears before a larger value, subtract it (e.g., IV = 5-1 = 4). Otherwise add. Scan left to right: if `val[s[i]] < val[s[i+1]]`, subtract; else add.
> - **WHAT:** Map each symbol to its value; single pass with lookahead.
> - **HOW:** For each character (except last): if its value is less than the next character's value, subtract; else add. Add the last character unconditionally.

> [!note]- Python Solution
> ```python
> def romanToInt(s: str) -> int:
>     val = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
>            'C': 100, 'D': 500, 'M': 1000}
>     result = 0
>     for i in range(len(s) - 1):
>         if val[s[i]] < val[s[i + 1]]:
>             result -= val[s[i]]
>         else:
>             result += val[s[i]]
>     return result + val[s[-1]]
> ```

> [!success] Complexity
> Time O(n). Space O(1).

> [!tip] Alternatives
> Replace subtractive pairs before parsing: `s.replace("IV","IIII")` etc. — simpler logic but mutates string.

---

### Excel Sheet Column Number

> [!example] Problem
> Given a column title (e.g., "A"→1, "Z"→26, "AA"→27, "AB"→28), return its column number.

> [!info] Approach
> - **WHY:** This is base-26 to base-10 conversion where 'A'=1, ..., 'Z'=26 (1-indexed, not 0-indexed). Same as positional notation: `result = result * 26 + digit_value`.
> - **WHAT:** Scan left to right; multiply running total by 26 and add current letter's value.
> - **HOW:** `result = 0`. For each char `c`: `result = result * 26 + (ord(c) - ord('A') + 1)`.

> [!note]- Python Solution
> ```python
> def titleToNumber(columnTitle: str) -> int:
>     result = 0
>     for c in columnTitle:
>         result = result * 26 + (ord(c) - ord('A') + 1)
>     return result
> ```

> [!success] Complexity
> Time O(n). Space O(1).

> [!tip] Alternatives
> Reverse: `columnNumberToTitle` — reverse base-26 with 1-indexed adjustment: `(num - 1) % 26` maps to 'A'–'Z'.

---

### Happy Number

> [!example] Problem
> A happy number reaches 1 when repeatedly replaced by the sum of squares of its digits. Detect if n is happy (vs. entering an infinite loop).

> [!info] Approach
> - **WHY:** Unhappy numbers enter a cycle. Classic cycle detection: Floyd's (slow/fast pointer) or a seen-set. For sum-of-squares, any cycle for non-happy numbers passes through 4 (known fact), but seen-set is simpler and general.
> - **WHAT:** Apply digit-square-sum repeatedly; if we hit 1 → happy; if we see a repeated number → not happy.
> - **HOW:** Floyd's two-pointer on the implicit sequence — slow moves one step, fast moves two steps. Cycle iff `slow == fast`; happy iff that meeting point is 1.

> [!note]- Python Solution
> ```python
> def isHappy(n: int) -> bool:
>     def digit_sq_sum(x: int) -> int:
>         total = 0
>         while x:
>             x, d = divmod(x, 10)
>             total += d * d
>         return total
> 
>     slow, fast = n, digit_sq_sum(n)
>     while fast != 1 and slow != fast:
>         slow = digit_sq_sum(slow)
>         fast = digit_sq_sum(digit_sq_sum(fast))
>     return fast == 1
> ```

> [!success] Complexity
> Time O(log n) per step, O(log n) steps until cycle detected. Space O(1) with Floyd's.

> [!tip] Alternatives
> Seen-set: `while n not in seen: seen.add(n); n = digit_sq_sum(n)`. O(log n) space. Hardcode: all unhappy numbers cycle through 4 — can check `if n == 4: return False` as early exit.

---

### Palindrome Number

> [!example] Problem
> Determine if an integer is a palindrome without converting to string.

> [!info] Approach
> - **WHY:** Negative numbers and numbers ending in 0 (except 0 itself) are never palindromes. Reverse only the second half — avoids overflow and is more elegant than reversing the entire number.
> - **WHAT:** Repeatedly pop the last digit and build a reversed half. When `x ≤ reversed_half`, we've processed at least half the digits.
> - **HOW:** `while x > reversed_half: reversed_half = reversed_half * 10 + x % 10; x //= 10`. Then `x == reversed_half` (even) or `x == reversed_half // 10` (odd length).

> [!note]- Python Solution
> ```python
> def isPalindrome(x: int) -> bool:
>     if x < 0 or (x % 10 == 0 and x != 0):
>         return False
>     reversed_half = 0
>     while x > reversed_half:
>         reversed_half = reversed_half * 10 + x % 10
>         x //= 10
>     return x == reversed_half or x == reversed_half // 10
> ```

> [!success] Complexity
> Time O(log₁₀ n). Space O(1).

> [!tip] Alternatives
> `str(x) == str(x)[::-1]` — one-liner but uses O(log n) space. Reverse full integer — risks overflow in languages without big integers.

---

### Multiply Strings

> [!example] Problem
> Multiply two non-negative integers represented as strings; return the product as a string. Do not convert to integer directly.

> [!info] Approach
> - **WHY:** Grade-school multiplication: digit `num1[i]` × digit `num2[j]` contributes to position `i + j` (units) and `i + j + 1` (carry). Work with a result array of size `len1 + len2`.
> - **WHAT:** Allocate `pos[len1 + len2]`. For each pair `(i, j)` (right to left): `prod = (num1[i] - '0') × (num2[j] - '0') + pos[i+j+1]`; `pos[i+j+1] = prod % 10`; `pos[i+j] += prod // 10`.
> - **HOW:** Iterate `i` from end of num1, `j` from end of num2. Final answer: strip leading zeros; `"0"` if all zeros.

> [!note]- Python Solution
> ```python
> def multiply(num1: str, num2: str) -> str:
>     m, n = len(num1), len(num2)
>     pos = [0] * (m + n)
>     for i in range(m - 1, -1, -1):
>         for j in range(n - 1, -1, -1):
>             mul = (ord(num1[i]) - ord('0')) * (ord(num2[j]) - ord('0'))
>             p1, p2 = i + j, i + j + 1
>             total = mul + pos[p2]
>             pos[p2] = total % 10
>             pos[p1] += total // 10
>     result = ''.join(str(d) for d in pos).lstrip('0')
>     return result or '0'
> ```

> [!success] Complexity
> Time O(m × n). Space O(m + n).

> [!tip] Alternatives
> Python's arbitrary-precision integers make `str(int(num1) * int(num2))` trivial — but the manual approach is what interviews test. FFT-based multiplication: O(n log n) — overkill for string multiply.

---

## Probability / Sampling

### Random Pick with Weight

> [!example] Problem
> Given weights `w[i]`, implement `pickIndex()` which returns index `i` with probability `w[i] / sum(w)`.

> [!info] Approach
> - **WHY:** Weighted sampling = prefix-sum + binary search. Build prefix sum array; generate a random float in `[0, total_weight)`. The correct index is the first prefix sum strictly greater than the random value.
> - **WHAT:** Precompute prefix sums. Each call: `r = random.random() * total`; binary search for first prefix sum > r → that index.
> - **HOW:** `bisect_left` on prefix sums after multiplying random by total; or `bisect_right` on the raw prefix sum array after scaling.

> [!note]- Python Solution
> ```python
> import random
> import bisect
> 
> class Solution:
>     def __init__(self, w: list[int]):
>         self.prefix = []
>         total = 0
>         for weight in w:
>             total += weight
>             self.prefix.append(total)
>         self.total = total
> 
>     def pickIndex(self) -> int:
>         target = random.random() * self.total
>         # find first prefix sum strictly greater than target
>         return bisect.bisect_right(self.prefix, target)
> ```

> [!success] Complexity
> `__init__` O(n). `pickIndex` O(log n). Space O(n).

> [!tip] Alternatives
> Alias method: O(n) setup, O(1) per pick — optimal for high-frequency sampling. Linear scan: O(n) per pick — correct but slow. Note: `bisect_right` handles the case where target equals a prefix boundary correctly (moves to next bucket).

---

### Reservoir Sampling

> [!example] Problem
> Given a stream of unknown length, return a uniformly random sample of size k. Each element must have equal probability k/n of being selected (where n is the total stream length seen so far).

> [!info] Approach
> - **WHY:** Can't store the entire stream. Reservoir: keep a reservoir of k items. For item i (1-indexed): with probability `k/i`, replace a random reservoir element. Mathematical induction shows this maintains uniform distribution at every step.
> - **WHAT:** Fill reservoir with first k items. For each subsequent item i: pick `j = random(0, i)`. If `j < k`, replace `reservoir[j]` with `stream[i]`.
> - **HOW:** Prove invariant: after seeing i items, each item has probability k/i of being in reservoir. Inductive step: item i+1 chosen with prob k/(i+1); each existing item survives with prob 1 - (k/(i+1)) × (1/k) = i/(i+1); combined probability for old items: k/i × i/(i+1) = k/(i+1). ✓

> [!note]- Python Solution
> ```python
> import random
> 
> def reservoir_sample(stream, k: int) -> list:
>     reservoir = []
>     for i, item in enumerate(stream):
>         if i < k:
>             reservoir.append(item)
>         else:
>             j = random.randint(0, i)  # inclusive on both ends
>             if j < k:
>                 reservoir[j] = item
>     return reservoir
> 
> # LeetCode 382 variant: linked list random node (k=1)
> class LinkedListRandomNode:
>     def __init__(self, head):
>         self.head = head
> 
>     def getRandom(self) -> int:
>         result, node, i = self.head.val, self.head.next, 1
>         while node:
>             if random.randint(0, i) == 0:
>                 result = node.val
>             node = node.next
>             i += 1
>         return result
> ```

> [!success] Complexity
> Time O(n) for full stream. Space O(k) for reservoir.

> [!tip] Alternatives
> Fisher-Yates shuffle on a known array — O(n) but requires knowing n upfront. Reservoir with random sort key (Knuth): assign each item a `random()` key; keep top-k by key — equivalent distribution. For large k relative to n, just shuffle and take first k.

---

## See Also

[[dynamic-programming]] | [[binary-search]] | [[sorting]]
### Bulb Switcher

> [!example] Problem
> There are `n` bulbs, all initially off. On round `i`, toggle every `i`th bulb. Return how many bulbs remain on after `n` rounds.

> [!info] Approach
> - **WHY:** A bulb ends up on only if it is toggled an odd number of times. A bulb at position `k` is toggled once for every divisor of `k`.
> - **WHAT:** Count numbers with an odd number of divisors. Only perfect squares have an odd divisor count because one divisor pairs with each complementary divisor, except the square root.
> - **HOW:** Return the integer square root of `n`.

> [!note]- Python Solution
> ```python
> import math
> 
> def bulb_switch(n: int) -> int:
>     return math.isqrt(n)
> ```

> [!success] Complexity
> O(1) time, O(1) space.

> [!tip] Alternatives
> The divisor-count argument is the key interview proof. Simulation is O(n log n) and unnecessary.

---

## Mathematics — More Problems

### Water Jug Problem (LC 365)

> [!example] Problem
> Given two jugs of capacity `x` and `y` liters and infinite water, determine whether it's possible to measure exactly `z` liters using the two jugs.

> [!info] Approach
> - **WHY:** This is Bézout's identity. You can measure any amount that is a multiple of `gcd(x, y)`, up to `x + y`. So the condition is: `z <= x + y` AND `z % gcd(x, y) == 0`.
> - **WHAT:** Compute `g = gcd(x, y)`. Return `z <= x + y and z % g == 0`.
> - **HOW:** `math.gcd(x, y)` — Python standard library.

> [!note]- Python Solution
> ```python
> import math
>
> def can_measure_water(x: int, y: int, z: int) -> bool:
>     if z == 0:
>         return True
>     if x + y < z:
>         return False
>     return z % math.gcd(x, y) == 0
> ```

> [!success] Complexity
> Time O(log(min(x, y))) for gcd, Space O(1).

> [!tip] Alternatives
> - BFS simulation: states are `(amount_in_jug1, amount_in_jug2)`. Valid operations: fill, empty, pour between. O(x * y) states. Correct but slow — only use if you forget the number theory.
> - Bézout's: ax + by = z has an integer solution iff gcd(x, y) | z.

---

### Matrix Exponentiation — Fibonacci in O(log n)

> [!example] Problem
> Compute the n-th Fibonacci number in O(log n) time using matrix exponentiation.

> [!info] Approach
> - **WHY:** Fibonacci satisfies `[F(n+1), F(n)] = [[1,1],[1,0]]^n * [F(1), F(0)]`. Matrix exponentiation computes `M^n` in O(log n) matrix multiplications. Each multiplication is O(1) for 2×2 matrices.
> - **WHAT:** Define `mat_pow(M, n)` using repeated squaring: `M^n = (M^(n//2))^2` if n even, else `M * M^(n-1)`.
> - **HOW:** Base matrix `M = [[1,1],[1,0]]`. Multiply using 2×2 matrix multiply. Return `result[0][1]` which is `F(n)`.

> [!note]- Python Solution
> ```python
> def fib(n: int) -> int:
>     if n <= 1:
>         return n
>
>     def mat_mul(A, B):
>         return [
>             [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
>             [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]],
>         ]
>
>     def mat_pow(M, p):
>         if p == 1:
>             return M
>         if p % 2 == 0:
>             half = mat_pow(M, p // 2)
>             return mat_mul(half, half)
>         return mat_mul(M, mat_pow(M, p - 1))
>
>     result = mat_pow([[1, 1], [1, 0]], n)
>     return result[0][1]
> ```

> [!success] Complexity
> Time O(log n), Space O(log n) recursion depth.

> [!tip] Alternatives
> - Closed-form (Binet's formula): O(1) but involves floating point — precision fails for large n.
> - DP: O(n) time — fine for small n but the matrix method is the interview show-stopper for "can you do better than O(n)?"
> - Also applies to: linear recurrences (tribonacci, counting paths in graphs), `dp[n] = a*dp[n-1] + b*dp[n-2]`.

---

## See Also

[[dynamic-programming]] | [[binary-search]] | [[bit-manipulation]]
