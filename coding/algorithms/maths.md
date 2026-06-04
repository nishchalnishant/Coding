---
tags: [coding, algorithms, maths]
topic: Mathematics
difficulty: mixed
---

# Mathematics — Problem Reference by Pattern

> [!info] First Principles
> Mathematical patterns collapse O(n) or O(n²) simulations to O(√n) or O(log n) using number-theoretic identities. Core toolkit: (1) Sieve — all primes in O(n log log n); (2) Euclidean GCD — O(log min(a,b)); (3) Fast exponentiation — O(log n); (4) Modular arithmetic — mod at every + and ×; (5) Precomputed factorials + inverse factorials — O(n) build, O(1) query for nCr.


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## Number Theory — Primes / Sieve

### Count Primes (Sieve of Eratosthenes) `⭐ Google`

> [!example] Problem
> Given an integer n, return the number of prime numbers that are strictly less than n.
> 
> **Example 1:**
> ```
> Input: n = 10
> Output: 4
> Explanation: There are 4 prime numbers less than 10, they are 2, 3, 5, 7.
> ```
> 
> **Example 2:**
> ```
> Input: n = 0
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: n = 1
> Output: 0
> ```
> 
> **Constraints:**
> - 0 <= n <= 5 * 10^6

> [!info] Approach
> Trial division per number is O(√n) × O(n) = O(n√n). The Sieve marks composites in bulk: starting from p², every multiple of p is composite. Each composite is marked once by its smallest prime factor → O(n log log n) total work. Boolean array `is_prime[0..n-1]`; mark composites; count remaining True entries. Initialize all True. Set `is_prime[0]=is_prime[1]=False`. For each `p` from 2 to √n: if `is_prime[p]`, mark `p*p, p*p+p, ...` False. Starting at `p²` (not `2p`) because smaller multiples were already marked by smaller primes.

> [!note]- Python Solution
> ```python
> def count_primes(n):
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
> Given two positive integers left and right, find the two integers num1 and num2 such that:
> Return the positive integer array ans = [num1, num2]. If there are multiple pairs satisfying these conditions, return the one with the smallest num1 value. If no such numbers exist, return [-1, -1].
> 
> **Example 1:**
> ```
> Input: left = 10, right = 19
> Output: [11,13]
> Explanation: The prime numbers between 10 and 19 are 11, 13, 17, and 19.
> The closest gap between any pair is 2, which can be achieved by [11,13] or [17,19].
> Since 11 is smaller than 17, we return the first pair.
> ```
> 
> **Example 2:**
> ```
> Input: left = 4, right = 6
> Output: [-1,-1]
> Explanation: There exists only one prime number in the given range, so the conditions cannot be satisfied.
> ```
> 
> **Constraints:**
> - 1 <= left <= right <= 10^6

> [!info] Approach
> Collect all primes in `[left, right]` efficiently; scan adjacent pairs for minimum gap. Sieve `[0, right]` or a segmented sieve for large ranges; filter to `[left, right]`; find min adjacent gap. Standard sieve up to `right`. Collect primes in range. If fewer than 2, return `[-1, -1]`. Linear scan for minimum gap between consecutive primes.

> [!note]- Python Solution
> ```python
> def closest_primes(left, right):
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

### Find Greatest Common Divisor of Array

> [!example] Problem
> Given an integer array nums, return the greatest common divisor of the smallest number and largest number in nums.
> The greatest common divisor of two numbers is the largest positive integer that evenly divides both numbers.
> 
> **Example 1:**
> ```
> Input: nums = [2,5,6,9,10]
> Output: 2
> Explanation:
> The smallest number in nums is 2.
> The largest number in nums is 10.
> The greatest common divisor of 2 and 10 is 2.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [7,5,6,8,3]
> Output: 1
> Explanation:
> The smallest number in nums is 3.
> The largest number in nums is 8.
> The greatest common divisor of 3 and 8 is 1.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [3,3]
> Output: 3
> Explanation:
> The smallest number in nums is 3.
> The largest number in nums is 3.
> The greatest common divisor of 3 and 3 is 3.
> ```
> 
> **Constraints:**
> - 2 <= nums.length <= 1000
> - 1 <= nums[i] <= 1000

> [!info] Approach
> By property of GCD: `gcd(array) = gcd(gcd(a1, a2), a3, ...)`. For GCD of just max and min: `gcd(min(nums), max(nums))`. `gcd(min(nums), max(nums))` — the GCD of any set is bounded by the GCD of its extremes. Single pass to find min and max; apply Euclidean GCD.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def find_gcd(nums):
>     return gcd(min(nums), max(nums))
> ```

> [!success] Complexity
> Time O(n) for min/max + O(log min) for GCD. Space O(1).

> [!tip] Alternatives
> `functools.reduce(gcd, nums)` computes GCD of entire array — not what's asked here but a useful pattern.

---

### Simplified Fractions

> [!example] Problem
> Given an integer n, return a list of all simplified fractions between 0 and 1 (exclusive) such that the denominator is less-than-or-equal-to n. You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: n = 2
> Output: ["1/2"]
> Explanation: "1/2" is the only unique fraction with a denominator less-than-or-equal-to 2.
> ```
> 
> **Example 2:**
> ```
> Input: n = 3
> Output: ["1/2","1/3","2/3"]
> ```
> 
> **Example 3:**
> ```
> Input: n = 4
> Output: ["1/2","1/3","1/4","2/3","3/4"]
> Explanation: "2/4" is not a simplified fraction because it can be simplified to "1/2".
> ```
> 
> **Constraints:**
> - 1 <= n <= 100

> [!info] Approach
> Fraction `a/b` is simplified iff `gcd(a, b) = 1` (coprime). Iterate all pairs and filter. For each `b` from 2 to `n`, for each `a` from 1 to `b-1`, include `a/b` if `gcd(a, b) == 1`. Double loop; GCD check per pair. O(n²) pairs, each O(log n) GCD check.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def simplified_fractions(n):
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
> By Bézout's Identity, integers `ax + by = z` has a solution iff `z` is a multiple of `gcd(x, y)`. Pouring between jugs is equivalent to computing integer linear combinations of `x` and `y`. `target` is achievable iff `target ≤ x + y` and `target % gcd(x, y) == 0`. Check both conditions. No simulation needed.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def can_measure_water(x, y, target):
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

### Pow(x, n) (Fast Exponentiation with Mod) `🔥 Google`

> [!example] Problem
> Compute `x^n` efficiently; handle negative exponents.

> [!info] Approach
> Naive O(n) multiplication. D&C: `x^n = (x^(n/2))^2`. Each level halves the exponent → O(log n) multiplications. Iterative binary exponentiation — process bits of `n` from LSB to MSB. If `n` negative: `x = 1/x`, `n = -n`. While `n > 0`: if LSB set, multiply result by `x`; square `x`; right-shift `n`.

> [!note]- Python Solution
> ```python
> def my_pow(x, n):
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
> Your task is to calculate ab mod 1337 where a is a positive integer and b is an extremely large positive integer given in the form of an array.
> 
> **Example 1:**
> ```
> Input: a = 2, b = [3]
> Output: 8
> ```
> 
> **Example 2:**
> ```
> Input: a = 2, b = [1,0]
> Output: 1024
> ```
> 
> **Example 3:**
> ```
> Input: a = 1, b = [4,3,3,8,5,2]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= a <= 2^{31} - 1
> - 1 <= b.length <= 2000
> - 0 <= b[i] <= 9
> - b does not contain leading zeros.

> [!info] Approach
> `b` is too large to compute as an integer. Use the identity: `a^[d1,...,dk] = (a^[d1,...,dk-1])^10 × a^dk`. Process one digit at a time; apply mod throughout. Iterate digits left to right; maintain running result raised to 10th power each step, multiplied by `a^digit`. `1337 = 7 × 191` (not prime), so Fermat's little theorem doesn't directly apply — use direct modular exponentiation.

> [!note]- Python Solution
> ```python
> def super_pow(a, b):
>     MOD = 1337
> 
>     def pow_mod(base, exp):
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
> A digit string is good if the digits (0-indexed) at even indices are even and the digits at odd indices are prime (2, 3, 5, or 7).
> Given an integer n, return the total number of good digit strings of length n. Since the answer may be large, return it modulo 109 + 7.
> A digit string is a string consisting of digits 0 through 9 that may contain leading zeros.
> 
> **Example 1:**
> ```
> Input: n = 1
> Output: 5
> Explanation: The good numbers of length 1 are "0", "2", "4", "6", "8".
> ```
> 
> **Example 2:**
> ```
> Input: n = 4
> Output: 400
> ```
> 
> **Example 3:**
> ```
> Input: n = 50
> Output: 564908303
> ```
> 
> **Constraints:**
> - 1 <= n <= 1015

> [!info] Approach
> Even positions: 5 choices (0,2,4,6,8); odd positions: 4 choices (2,3,5,7). Positions are independent → multiply. Use fast exponentiation for large `n`. `answer = 5^(ceil(n/2)) × 4^(floor(n/2)) mod (10^9+7)`. `even_count = (n + 1) // 2` (positions 0, 2, 4, ...); `odd_count = n // 2`. Fast pow for each.

> [!note]- Python Solution
> ```python
> def count_good_numbers(n):
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
> Fermat's little theorem (`a^(m-2) mod m`) only works for prime `m`. Extended Euclidean algorithm solves `ax + my = gcd(a,m) = 1` for any `m` coprime to `a`. Extended GCD returns `(g, x, y)` where `a×x + m×y = g`. If `g=1`, then `x mod m` is the inverse. `extended_gcd(a, m)` → `(g, x, y)`. Inverse = `x % m` if `g == 1`, else no inverse.

> [!note]- Python Solution
> ```python
> def extended_gcd(a, b):
>     if b == 0:
>         return a, 1, 0
>     g, x, y = extended_gcd(b, a % b)
>     return g, y, x - (a // b) * y
> 
> def mod_inverse(a, m):
>     g, x, _ = extended_gcd(a % m, m)
>     if g != 1:
>         raise ValueError(f"No inverse: gcd({a},{m}) = {g}")
>     return x % m
> 
> # For prime mod: simpler
> def mod_inverse_prime(a, p):
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
> Given an integer numRows, return the first numRows of Pascal's triangle.
> In Pascal's triangle, each number is the sum of the two numbers directly above it as shown
> 
> **Example 1:**
> ```
> Input: numRows = 5
> Output: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
> ```
> 
> **Example 2:**
> ```
> Input: numRows = 1
> Output: [[1]]
> ```
> 
> **Constraints:**
> - 1 <= numRows <= 30

> [!info] Approach
> Each interior element is the sum of two elements directly above: `C(n,k) = C(n-1,k-1) + C(n-1,k)`. This is the defining recurrence of binomial coefficients. Build rows iteratively; each row has one more element than the previous. Row `i` has `i+1` elements. `row[j] = prev[j-1] + prev[j]`. Edges are always 1.

> [!note]- Python Solution
> ```python
> def generate(numRows):
>     triangle = [[1]]
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
> Given an integer rowIndex, return the rowIndexth (0-indexed) row of the Pascal's triangle.
> In Pascal's triangle, each number is the sum of the two numbers directly above it as shown
> 
> **Example 1:**
> ```
> Input: rowIndex = 3
> Output: [1,3,3,1]
> ```
> 
> **Example 2:**
> ```
> Input: rowIndex = 0
> Output: [1]
> ```
> 
> **Example 3:**
> ```
> Input: rowIndex = 1
> Output: [1,1]
> ```
> 
> **Constraints:**
> - 0 <= rowIndex <= 33

> [!info] Approach
> Only need one row; can build in-place by updating right to left to avoid overwriting needed values. Start with `[1]`; for each new row, insert 1 at start and add adjacent pairs (right to left to avoid using updated values). `row[j] += row[j-1]` from `j = len(row)-1` down to 1; append 1 at end each iteration.

> [!note]- Python Solution
> ```python
> def get_row(rowIndex):
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

### Unique Paths (Combinatorics Approach) `🔥 Google`

> [!example] Problem
> There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.
> Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.
> The test cases are generated so that the answer will be less than or equal to 2 * 109.
> 
> **Example 1:**
> ```
> Input: m = 3, n = 7
> Output: 28
> ```
> 
> **Example 2:**
> ```
> Input: m = 3, n = 2
> Output: 3
> Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
> 1. Right -> Down -> Down
> 2. Down -> Down -> Right
> 3. Down -> Right -> Down
> ```
> 
> **Constraints:**
> - 1 <= m, n <= 100

> [!info] Approach
> Any path makes exactly `(m-1)` down moves and `(n-1)` right moves in some order. Total moves = `m+n-2`; we choose which `m-1` are down moves → `C(m+n-2, m-1)`. `answer = math.comb(m + n - 2, m - 1)`. Python's `math.comb` computes this exactly in O(min(m,n)) time without overflow using integer arithmetic.

> [!note]- Python Solution
> ```python
> from math import comb
> 
> def unique_paths(m, n):
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
> Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane, return the maximum number of points that lie on the same straight line.
> 
> **Example 1:**
> ```
> Input: points = [[1,1],[2,2],[3,3]]
> Output: 3
> ```
> 
> **Example 2:**
> ```
> Input: points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]
> Output: 4
> ```
> 
> **Constraints:**
> - 1 <= points.length <= 300
> - points[i].length == 2
> - -10^4 <= xi, yi <= 10^4
> - All the points are unique.

> [!info] Approach
> Floating-point slope representation causes rounding errors — two points with the same true slope may produce different floats. GCD-normalized integer `(dy, dx)` tuple is exact. For each anchor point, compute normalized slope to every other point; use frequency map to find the most common slope (+ handle duplicates). For each pair `(anchor, other)`: `dx = other.x - anchor.x`, `dy = other.y - anchor.y`. Normalize: `g = gcd(|dy|, |dx|)`, `slope = (dy//g, dx//g)`. Force canonical sign: if `dx < 0`, negate both. Duplicates (same point) counted separately.

> [!note]- Python Solution
> ```python
> from math import gcd
> 
> def max_points(points):
>     if len(points) <= 2:
>         return len(points)
>     max_pts = 1
>     for i in range(len(points)):
>         slopes = {}
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
> Given an integer array nums of size n, return the minimum number of moves required to make all array elements equal.
> In one move, you can increment n - 1 elements of the array by 1.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3]
> Output: 3
> Explanation: Only three moves are needed (remember each move increments two elements):
> [1,2,3]  =>  [2,3,3]  =>  [3,4,3]  =>  [4,4,4]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,1,1]
> Output: 0
> ```
> 
> **Constraints:**
> - n == nums.length
> - 1 <= nums.length <= 10^5
> - -10^9 <= nums[i] <= 10^9
> - The answer is guaranteed to fit in a 32-bit integer.

> [!info] Approach
> Incrementing `n-1` elements by 1 is equivalent to decrementing 1 element by 1. Minimum total absolute deviation from a central value is minimized at the **median** (not mean). Sort; find median; sum of absolute differences from median. Sort `nums`. Median = `nums[n//2]`. Answer = `sum(|x - median|)`.

> [!note]- Python Solution
> ```python
> def min_moves2(nums):
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

### Factorial Trailing Zeroes `⭐ Google`

> [!example] Problem
> Given an integer n, return the number of trailing zeroes in n!.
> Note that n! = n * (n - 1) * (n - 2) * ... * 3 * 2 * 1.
> 
> **Example 1:**
> ```
> Input: n = 3
> Output: 0
> Explanation: 3! = 6, no trailing zero.
> ```
> 
> **Example 2:**
> ```
> Input: n = 5
> Output: 1
> Explanation: 5! = 120, one trailing zero.
> ```
> 
> **Example 3:**
> ```
> Input: n = 0
> Output: 0
> ```
> 
> **Constraints:**
> - 0 <= n <= 10^4

> [!info] Approach
> Trailing zeros come from factors of 10 = 2 × 5. There are always more factors of 2 than 5 in n!, so count factors of 5. Each multiple of 5 contributes one 5; multiples of 25 contribute an extra; etc. `count = n//5 + n//25 + n//125 + ...` until power of 5 exceeds n (Legendre's formula). Iteratively add `n // (5^k)` while `5^k ≤ n`.

> [!note]- Python Solution
> ```python
> def trailing_zeroes(n):
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
> Binary search or Newton's method both give O(log x) convergence. Newton's: `r = (r + x//r) // 2` converges quadratically. Binary search on `[0, x]` for largest `m` where `m² ≤ x`. `lo=0, hi=x`. While `lo ≤ hi`: `mid=(lo+hi)//2`; if `mid*mid ≤ x`, try larger (`lo=mid+1`); else smaller (`hi=mid-1`).

> [!note]- Python Solution
> ```python
> def my_sqrt(x):
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
> def my_sqrt_newton(x):
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

### Nth Digit `🔥 Google`

> [!example] Problem
> Given an integer n, return the nth digit of the infinite integer sequence [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...].
> 
> **Example 1:**
> ```
> Input: n = 3
> Output: 3
> ```
> 
> **Example 2:**
> ```
> Input: n = 11
> Output: 0
> Explanation: The 11th digit of the sequence 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ... is a 0, which is part of the number 10.
> ```
> 
> **Constraints:**
> - 1 <= n <= 2^{31} - 1

> [!info] Approach
> Group digits by number of digits: 1-digit (9 numbers, 9 digits), 2-digit (90 numbers, 180 digits), etc. Determine which group `n` falls in, then pinpoint the exact number and digit within it. Subtract group sizes until finding the right group; compute offset. For each digit count `d`: group has `9 × 10^(d-1)` numbers contributing `d × 9 × 10^(d-1)` digits. When `n` falls in group `d`: `num = 10^(d-1) + (n-1)//d`; digit index within `num` = `(n-1) % d`.

> [!note]- Python Solution
> ```python
> def find_nth_digit(n):
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
> Generate ugly numbers in order; each ugly number = another ugly number × {2, 3, or 5}. Three-pointer approach tracks which ugly number to multiply next by each prime. Maintain three pointers `p2, p3, p5` into the `ugly` list. Each step: `next = min(ugly[p2]*2, ugly[p3]*3, ugly[p5]*5)`; advance all pointers that produced the minimum. Initialize `ugly=[1]`, `p2=p3=p5=0`. Repeat n-1 times. Advancing all tied pointers prevents duplicates.

> [!note]- Python Solution
> ```python
> def nth_ugly_number(n):
>     ugly = [1]
>     two_back = p3 = p5 = 0
>     for _ in range(n - 1):
>         next2, next3, next5 = ugly[two_back]*2, ugly[p3]*3, ugly[p5]*5
>         next_ugly = min(next2, next3, next5)
>         ugly.append(next_ugly)
>         if next_ugly == next2: two_back += 1
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
> A number n has exactly 4 divisors iff: (1) `n = p³` for prime `p` (divisors: 1, p, p², p³) or (2) `n = p × q` for distinct primes `p, q` (divisors: 1, p, q, pq). Check factorization up to √n. For each number, count distinct divisors up to √n; accumulate sum if exactly 4 found. For each `num`, trial divide. If exactly 4 divisors, add their sum to result.

> [!note]- Python Solution
> ```python
> def sum_four_divisors(nums):
>     def four_div_sum(n):
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
> Total moves = sum of absolute differences from the target value. This is minimized at the **median** by the L1 regression property — the median minimizes sum of absolute deviations. Sort; find median; sum `|x - median|` for all x. Same as "Minimum Moves to Equal Array Elements" variant above.

> [!note]- Python Solution
> ```python
> def min_moves2(nums):
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
> Subarray sum `sum(i+1..j) = prefix[j] - prefix[i]`. Divisible by k iff `prefix[j] ≡ prefix[i] (mod k)`. So count pairs of equal prefix sums mod k. Frequency map of `prefix_sum % k`. Each pair of equal remainders contributes one valid subarray. Initialize `remainder_count = {0: 1}` (empty prefix). For each element, update `prefix_sum`, compute `r = prefix_sum % k`; add `remainder_count.get(r, 0)` to answer; increment `remainder_count[r]`. Handle negative remainders: `r = (prefix_sum % k + k) % k`.

> [!note]- Python Solution
> ```python
> def subarrays_div_by_k(nums, k):
>     remainder_count = {0: 1}
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

### Integer to Roman `⭐ Google`

> [!example] Problem
> Seven different symbols represent Roman numerals with the following values:
> Roman numerals are formed by appending the conversions of decimal place values from highest to lowest. Converting a decimal place value into a Roman numeral has the following rules:
> Given an integer, convert it to a Roman numeral.
> 
> **Example 1:**
> ```
> 3000 = MMM as 1000 (M) + 1000 (M) + 1000 (M)
>  700 = DCC as 500 (D) + 100 (C) + 100 (C)
>   40 = XL as 10 (X) less of 50 (L)
>    9 = IX as 1 (I) less of 10 (X)
> Note: 49 is not 1 (I) less of 50 (L) because the conversion is based on decimal places
> ```
> 
> **Example 2:**
> ```
> 50 = L
>  8 = VIII
> ```
> 
> **Example 3:**
> ```
> 1000 = M
>  900 = CM
>   90 = XC
>    4 = IV
> ```
> 
> **Constraints:**
> - 1 <= num <= 3999

> [!info] Approach
> Roman numerals are a greedy positional system. Subtractive forms (IV=4, IX=9, XL=40, ...) can be handled by including them as explicit "values" in the table. Greedily subtract the largest fitting value. Table of `(value, symbol)` pairs in descending order including all 13 subtractive forms. While `num > 0`: find largest value ≤ num, append symbol, subtract value. 13 symbols: 1000→M, 900→CM, 500→D, 400→CD, 100→C, 90→XC, 50→L, 40→XL, 10→X, 9→IX, 5→V, 4→IV, 1→I.

> [!note]- Python Solution
> ```python
> def int_to_roman(num):
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

### Roman to Integer `⭐ Google`

> [!example] Problem
> Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.
> For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.
> Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:
> Given a roman numeral, convert it to an integer.
> 
> **Example 1:**
> ```
> Symbol       Value
> I             1
> V             5
> X             10
> L             50
> C             100
> D             500
> M             1000
> ```
> 
> **Example 2:**
> ```
> Input: s = "III"
> Output: 3
> Explanation: III = 3.
> ```
> 
> **Example 3:**
> ```
> Input: s = "LVIII"
> Output: 58
> Explanation: L = 50, V= 5, III = 3.
> ```
> 
> **Example 4:**
> ```
> Input: s = "MCMXCIV"
> Output: 1994
> Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 15
> - s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M').
> - It is guaranteed that s is a valid roman numeral in the range [1, 3999].

> [!info] Approach
> Subtractive rule: if a smaller value appears before a larger value, subtract it (e.g., IV = 5-1 = 4). Otherwise add. Scan left to right: if `val[s[i]] < val[s[i+1]]`, subtract; else add. Map each symbol to its value; single pass with lookahead. For each character (except last): if its value is less than the next character's value, subtract; else add. Add the last character unconditionally.

> [!note]- Python Solution
> ```python
> def roman_to_int(s):
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

### Excel Sheet Column Number `⭐ Google`

> [!example] Problem
> Given a string columnTitle that represents the column title as appears in an Excel sheet, return its corresponding column number.
> For example
> 
> **Example 1:**
> ```
> A -> 1
> B -> 2
> C -> 3
> ...
> Z -> 26
> AA -> 27
> AB -> 28 
> ...
> ```
> 
> **Example 2:**
> ```
> Input: columnTitle = "A"
> Output: 1
> ```
> 
> **Example 3:**
> ```
> Input: columnTitle = "AB"
> Output: 28
> ```
> 
> **Example 4:**
> ```
> Input: columnTitle = "ZY"
> Output: 701
> ```
> 
> **Constraints:**
> - 1 <= columnTitle.length <= 7
> - columnTitle consists only of uppercase English letters.
> - columnTitle is in the range ["A", "FXSHRXW"].

> [!info] Approach
> This is base-26 to base-10 conversion where 'A'=1, ..., 'Z'=26 (1-indexed, not 0-indexed). Same as positional notation: `result = result * 26 + digit_value`. Scan left to right; multiply running total by 26 and add current letter's value. `result = 0`. For each char `c`: `result = result * 26 + (ord(c) - ord('A') + 1)`.

> [!note]- Python Solution
> ```python
> def title_to_number(columnTitle):
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

### Palindrome Number

> [!example] Problem
> Given an integer x, return true if x is a palindrome, and false otherwise.
> 
> **Example 1:**
> ```
> Input: x = 121
> Output: true
> Explanation: 121 reads as 121 from left to right and from right to left.
> ```
> 
> **Example 2:**
> ```
> Input: x = -121
> Output: false
> Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
> ```
> 
> **Example 3:**
> ```
> Input: x = 10
> Output: false
> Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
> ```
> 
> **Constraints:**
> - -2^{31} <= x <= 2^{31} - 1

> [!info] Approach
> Negative numbers and numbers ending in 0 (except 0 itself) are never palindromes. Reverse only the second half — avoids overflow and is more elegant than reversing the entire number. Repeatedly pop the last digit and build a reversed half. When `x ≤ reversed_half`, we've processed at least half the digits. `while x > reversed_half: reversed_half = reversed_half * 10 + x % 10; x //= 10`. Then `x == reversed_half` (even) or `x == reversed_half // 10` (odd length).

> [!note]- Python Solution
> ```python
> def is_palindrome(x):
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
> Given two non-negative integers num1 and num2 represented as strings, return the product of num1 and num2, also represented as a string.
> Note: You must not use any built-in BigInteger library or convert the inputs to integer directly.
> 
> **Example 1:**
> ```
> Input: num1 = "2", num2 = "3"
> Output: "6"
> ```
> 
> **Example 2:**
> ```
> Input: num1 = "123", num2 = "456"
> Output: "56088"
> ```
> 
> **Constraints:**
> - 1 <= num1.length, num2.length <= 200
> - num1 and num2 consist of digits only.
> - Both num1 and num2 do not contain any leading zero, except the number 0 itself.

> [!info] Approach
> Grade-school multiplication: digit `num1[i]` × digit `num2[j]` contributes to position `i + j` (units) and `i + j + 1` (carry). Work with a result array of size `len1 + len2`. Allocate `pos[len1 + len2]`. For each pair `(i, j)` (right to left): `prod = (num1[i] - '0') × (num2[j] - '0') + pos[i+j+1]`; `pos[i+j+1] = prod % 10`; `pos[i+j] += prod // 10`. Iterate `i` from end of num1, `j` from end of num2. Final answer: strip leading zeros; `"0"` if all zeros.

> [!note]- Python Solution
> ```python
> def multiply(num1, num2):
>     m, n = len(num1), len(num2)
>     pos = [0] * (m + n)
>     for i in range(m - 1, -1, -1):
>         for j in range(n - 1, -1, -1):
>             mul = (ord(num1[i]) - ord('0')) * (ord(num2[j]) - ord('0'))
>             one_back, two_back = i + j, i + j + 1
>             total = mul + pos[two_back]
>             pos[two_back] = total % 10
>             pos[one_back] += total // 10
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
> You are given a 0-indexed array of positive integers w where w[i] describes the weight of the ith index.
> You need to implement the function pickIndex(), which randomly picks an index in the range [0, w.length - 1] (inclusive) and returns it. The probability of picking an index i is w[i] / sum(w).
> 
> **Example 1:**
> ```
> Input
> ["Solution","pickIndex"]
> [[[1]],[]]
> Output
> [null,0]
> 
> Explanation
> Solution solution = new Solution([1]);
> solution.pickIndex(); // return 0. The only option is to return 0 since there is only one element in w.
> ```
> 
> **Example 2:**
> ```
> Input
> ["Solution","pickIndex","pickIndex","pickIndex","pickIndex","pickIndex"]
> [[[1,3]],[],[],[],[],[]]
> Output
> [null,1,1,1,1,0]
> 
> Explanation
> Solution solution = new Solution([1, 3]);
> solution.pickIndex(); // return 1. It is returning the second element (index = 1) that has a probability of 3/4.
> solution.pickIndex(); // return 1
> solution.pickIndex(); // return 1
> solution.pickIndex(); // return 1
> solution.pickIndex(); // return 0. It is returning the first element (index = 0) that has a probability of 1/4.
> 
> Since this is a randomization problem, multiple answers are allowed.
> All of the following outputs can be considered correct:
> [null,1,1,1,1,0]
> [null,1,1,1,1,1]
> [null,1,1,1,0,0]
> [null,1,1,1,0,1]
> [null,1,0,1,0,0]
> ......
> and so on.
> ```
> 
> **Constraints:**
> - 1 <= w.length <= 10^4
> - 1 <= w[i] <= 10^5
> - pickIndex will be called at most 10^4 times.

> [!info] Approach
> Weighted sampling = prefix-sum + binary search. Build prefix sum array; generate a random float in `[0, total_weight)`. The correct index is the first prefix sum strictly greater than the random value. Precompute prefix sums. Each call: `r = random.random() * total`; binary search for first prefix sum > r → that index. `bisect_left` on prefix sums after multiplying random by total; or `bisect_right` on the raw prefix sum array after scaling.

> [!note]- Python Solution
> ```python
> import random
> import bisect
> 
> class Solution:
>     def __init__(self, w):
>         self.prefix = []
>         total = 0
>         for weight in w:
>             total += weight
>             self.prefix.append(total)
>         self.total = total
> 
>     def pick_index(self):
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
> Can't store the entire stream. Reservoir: keep a reservoir of k items. For item i (1-indexed): with probability `k/i`, replace a random reservoir element. Mathematical induction shows this maintains uniform distribution at every step. Fill reservoir with first k items. For each subsequent item i: pick `j = random(0, i)`. If `j < k`, replace `reservoir[j]` with `stream[i]`. Prove invariant: after seeing i items, each item has probability k/i of being in reservoir. Inductive step: item i+1 chosen with prob k/(i+1); each existing item survives with prob 1 - (k/(i+1)) × (1/k) = i/(i+1); combined probability for old items: k/i × i/(i+1) = k/(i+1). ✓

> [!note]- Python Solution
> ```python
> import random
> 
> def reservoir_sample(stream, k):
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
>     def get_random(self):
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
> There are n bulbs that are initially off. You first turn on all the bulbs, then you turn off every second bulb.
> On the third round, you toggle every third bulb (turning on if it's off or turning off if it's on). For the ith round, you toggle every i bulb. For the nth round, you only toggle the last bulb.
> Return the number of bulbs that are on after n rounds.
> 
> **Example 1:**
> ```
> Input: n = 3
> Output: 1
> Explanation: At first, the three bulbs are [off, off, off].
> After the first round, the three bulbs are [on, on, on].
> After the second round, the three bulbs are [on, off, on].
> After the third round, the three bulbs are [on, off, off]. 
> So you should return 1 because there is only one bulb is on.
> ```
> 
> **Example 2:**
> ```
> Input: n = 0
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: n = 1
> Output: 1
> ```
> 
> **Constraints:**
> - 0 <= n <= 10^9

> [!info] Approach
> A bulb ends up on only if it is toggled an odd number of times. A bulb at position `k` is toggled once for every divisor of `k`. Count numbers with an odd number of divisors. Only perfect squares have an odd divisor count because one divisor pairs with each complementary divisor, except the square root. Return the integer square root of `n`.

> [!note]- Python Solution
> ```python
> import math
> 
> def bulb_switch(n):
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
> You are given two jugs with capacities x liters and y liters. You have an infinite water supply. Return whether the total amount of water in both jugs may reach target using the following operations
> 
> **Example 1:**
> ```
> Input: x = 3, y = 5, target = 4
> Output: true
> Explanation:
> Follow these steps to reach a total of 4 liters:
> Reference: The Die Hard example.
> ```
> 
> **Example 2:**
> ```
> Input: x = 2, y = 6, target = 5
> Output: false
> ```
> 
> **Example 3:**
> ```
> Input: x = 1, y = 2, target = 3
> Output: true
> Explanation: Fill both jugs. The total amount of water in both jugs is equal to 3 now.
> ```
> 
> **Constraints:**
> - 1 <= x, y, target <= 10^3

> [!info] Approach
> This is Bézout's identity. You can measure any amount that is a multiple of `gcd(x, y)`, up to `x + y`. So the condition is: `z <= x + y` AND `z % gcd(x, y) == 0`. Compute `g = gcd(x, y)`. Return `z <= x + y and z % g == 0`. `math.gcd(x, y)` — Python standard library.

> [!note]- Python Solution
> ```python
> import math
> >
> def can_measure_water(x, y, z):
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

### Matrix Exponentiation — Fibonacci in O(log n) `⭐ Google`

> [!example] Problem
> Compute the n-th Fibonacci number in O(log n) time using matrix exponentiation.

> [!info] Approach
> Fibonacci satisfies `[F(n+1), F(n)] = [[1,1],[1,0]]^n * [F(1), F(0)]`. Matrix exponentiation computes `M^n` in O(log n) matrix multiplications. Each multiplication is O(1) for 2×2 matrices. Define `mat_pow(M, n)` using repeated squaring: `M^n = (M^(n//2))^2` if n even, else `M * M^(n-1)`. Base matrix `M = [[1,1],[1,0]]`. Multiply using 2×2 matrix multiply. Return `result[0][1]` which is `F(n)`.

> [!note]- Python Solution
> ```python
> def fib(n):
>     if n <= 1:
>         return n
> >
>     def mat_mul(A, B):
>         return [
>             [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
>             [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]],
>         ]
> >
>     def mat_pow(M, p):
>         if p == 1:
>             return M
>         if p % 2 == 0:
>             half = mat_pow(M, p // 2)
>             return mat_mul(half, half)
>         return mat_mul(M, mat_pow(M, p - 1))
> >
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
