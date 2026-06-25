---
tags: [coding, algorithms, maths]
topic: Mathematics
difficulty: mixed
---

# Mathematics — Amazon SDE-2

---

## GCD and LCM

### Euclidean Algorithm (GCD)

Subtract-based reduces to mod-based: `gcd(a, b) = gcd(b, a % b)`. Base case: `gcd(a, 0) = a`. O(log min(a, b)).

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a // gcd(a, b) * b   # divide first to prevent overflow
```

---

### Find Greatest Common Divisor of Array

> [!example] Problem
> Given array nums, return GCD of the largest and smallest element. LeetCode 1979.

> [!note]- Python Solution
> ```python
> from math import gcd
>
> def find_gcd(nums):
>     return gcd(min(nums), max(nums))
> ```

> [!success] Complexity
> Time O(n + log(max)) | Space O(1).

---

### Simplified Fractions

> [!example] Problem
> Return all simplified fractions with denominator from 2 to n. LeetCode 1447.

> [!note]- Python Solution
> ```python
> from math import gcd
>
> def simplified_fractions(n):
>     return [f"{i}/{j}" for j in range(2, n + 1)
>             for i in range(1, j) if gcd(i, j) == 1]
> ```

> [!success] Complexity
> Time O(n² log n) | Space O(1) output aside.

---

## Prime Sieve (Sieve of Eratosthenes)

Build a boolean array where `is_prime[i]` is True iff i is prime. For each prime p, mark all multiples of p starting at p² as composite. Only need to sieve up to √n.

```python
def sieve(n):
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p < n:
        if is_prime[p]:
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
        p += 1
    return is_prime
```

**Complexity**: Time O(n log log n) | Space O(n).

---

### Count Primes

> [!example] Problem
> Return the number of primes strictly less than n. LeetCode 204.

> [!note]- Python Solution
> ```python
> def count_primes(n):
>     if n < 2:
>         return 0
>     is_prime = [True] * n
>     is_prime[0] = is_prime[1] = False
>     for p in range(2, int(n**0.5) + 1):
>         if is_prime[p]:
>             for m in range(p * p, n, p):
>                 is_prime[m] = False
>     return sum(is_prime)
> ```

> [!success] Complexity
> Time O(n log log n) | Space O(n).

---

## Check Prime in O(√n)

```python
def is_prime(n):
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
```

**Why i += 6**: All primes > 3 are of the form 6k ± 1. Skip multiples of 2 and 3 automatically.

---

## Modular Arithmetic

**Why mod is needed**: intermediate products in combinatorics and exponentiation overflow 64-bit integers. Keep taking mod after every multiply/add.

```
(a + b) % m = ((a % m) + (b % m)) % m
(a * b) % m = ((a % m) * (b % m)) % m
(a - b) % m = ((a % m) - (b % m) + m) % m   # +m prevents negative
```

Division under mod requires modular inverse: `a/b mod m = a * pow(b, m-2, m) mod m` (only valid when m is prime, by Fermat's little theorem).

---

## Fast Power (Binary Exponentiation)

Compute `x^n mod m` in O(log n) by repeated squaring.

```python
def fast_pow(x, n, mod):
    result = 1
    x %= mod
    while n > 0:
        if n & 1:
            result = result * x % mod
        x = x * x % mod
        n >>= 1
    return result
```

Python's built-in `pow(x, n, mod)` uses the same algorithm — prefer it unless the problem asks for manual implementation.

---

### Pow(x, n) (No Mod)

> [!example] Problem
> Implement `pow(x, n)` for real x and integer n (including negative). LeetCode 50.

> [!info] Approach
> Handle negative n: `pow(x, -n) = 1 / pow(x, n)`. Binary exponentiation: if n is odd, multiply by x once; always square x and halve n.

> [!note]- Python Solution
> ```python
> def my_pow(x, n):
>     if n < 0:
>         x, n = 1 / x, -n
>     result = 1.0
>     while n:
>         if n & 1:
>             result *= x
>         x *= x
>         n >>= 1
>     return result
> ```

> [!success] Complexity
> Time O(log n) | Space O(1).

---

### Count Good Numbers

> [!example] Problem
> Return the count of "good" digit strings of length n, mod 10^9+7. LeetCode 1922.

> [!info] Approach
> Even positions (0-indexed) can be 5 digits (0,2,4,6,8), odd positions can be 4 digits (2,3,5,7). Count = `5^(ceil(n/2)) * 4^(floor(n/2))` mod 10^9+7.

> [!note]- Python Solution
> ```python
> def count_good_numbers(n):
>     MOD = 10**9 + 7
>     return pow(5, (n + 1) // 2, MOD) * pow(4, n // 2, MOD) % MOD
> ```

> [!success] Complexity
> Time O(log n) | Space O(1).

---

## Digit Math

### Factorial Trailing Zeroes

> [!example] Problem
> Return the number of trailing zeroes in n!. LeetCode 172.

> [!info] Approach
> Trailing zeroes = factors of 10 = min(factors of 2, factors of 5) = factors of 5 (always fewer). Count: `n//5 + n//25 + n//125 + ...`.

> [!note]- Python Solution
> ```python
> def trailing_zeroes(n):
>     count = 0
>     while n >= 5:
>         n //= 5
>         count += n
>     return count
> ```

> [!success] Complexity
> Time O(log n) | Space O(1).

---

### Palindrome Number

> [!example] Problem
> Determine whether an integer is a palindrome without converting to string. LeetCode 9.

> [!info] Approach
> Negative numbers are not palindromes. Numbers ending in 0 (except 0 itself) are not. Reverse only the second half: stop when `reversed_half >= x`. Then check `x == reversed_half` (even digits) or `x == reversed_half // 10` (odd digits).

> [!note]- Python Solution
> ```python
> def is_palindrome(x):
>     if x < 0 or (x != 0 and x % 10 == 0):
>         return False
>     rev = 0
>     while x > rev:
>         rev = rev * 10 + x % 10
>         x //= 10
>     return x == rev or x == rev // 10
> ```

> [!success] Complexity
> Time O(log n) | Space O(1).

---

### Integer Square Root (Newton's Method)

> [!example] Problem
> Return floor(√x) for non-negative integer x. LeetCode 69.

> [!note]- Python Solution
> ```python
> def my_sqrt(x):
>     if x < 2:
>         return x
>     lo, hi = 1, x // 2
>     while lo <= hi:
>         mid = (lo + hi) // 2
>         if mid * mid == x:
>             return mid
>         elif mid * mid < x:
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return hi
> ```

> [!success] Complexity
> Time O(log x) | Space O(1).

---

## Combinatorics

### Pascal's Triangle

> [!example] Problem
> Return the first numRows rows of Pascal's triangle. LeetCode 118.

> [!note]- Python Solution
> ```python
> def generate(numRows):
>     triangle = [[1]]
>     for i in range(1, numRows):
>         prev = triangle[-1]
>         row = [1] + [prev[j] + prev[j+1] for j in range(len(prev)-1)] + [1]
>         triangle.append(row)
>     return triangle
> ```

> [!success] Complexity
> Time O(numRows²) | Space O(numRows²).

---

### Unique Paths (Combinatorics)

> [!example] Problem
> Count paths in m×n grid moving only right or down. LeetCode 62.

> [!info] Approach
> Must take exactly (m-1) down moves and (n-1) right moves in some order: C(m+n-2, m-1). Use `math.comb` or DP.

> [!note]- Python Solution
> ```python
> from math import comb
>
> def unique_paths(m, n):
>     return comb(m + n - 2, m - 1)
> ```

> [!success] Complexity
> Time O(m+n) for comb computation | Space O(1).

---

## Array Math

### Count Subarrays Divisible by K

> [!example] Problem
> Return the number of subarrays whose sum is divisible by k. LeetCode 974.

> [!info] Approach
> Prefix sum mod k. If `prefix[i] % k == prefix[j] % k`, then `sum(i+1..j)` is divisible by k. Count pairs with equal prefix mod. Use a frequency map, seed with `{0: 1}`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> def subarrays_div_by_k(nums, k):
>     count = defaultdict(int)
>     count[0] = 1
>     prefix = result = 0
>     for n in nums:
>         prefix = (prefix + n) % k
>         result += count[prefix]
>         count[prefix] += 1
>     return result
> ```

> [!success] Complexity
> Time O(n) | Space O(k).

---

### Minimum Moves to Equal Array Elements (Median)

> [!example] Problem
> Minimum number of moves to make all array elements equal (each move increments or decrements one element). LeetCode 462.

> [!info] Approach
> Cost function is sum of absolute differences — minimized at the median. Sort, pick median, sum distances.

> [!note]- Python Solution
> ```python
> def min_moves2(nums):
>     nums.sort()
>     mid = nums[len(nums) // 2]
>     return sum(abs(n - mid) for n in nums)
> ```

> [!success] Complexity
> Time O(n log n) | Space O(1).

---

## See Also

[[dynamic-programming]] | [[bit-manipulation]] | [[graph]]
