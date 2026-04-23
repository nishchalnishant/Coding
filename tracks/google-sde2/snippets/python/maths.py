from __future__ import annotations

from typing import List


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    g = gcd(a, b)
    return 0 if g == 0 else (a // g) * b


def pow_fast(x: float, n: int) -> float:
    if n == 0:
        return 1.0
    if n < 0:
        x = 1.0 / x
        n = -n
    res = 1.0
    while n:
        if n & 1:
            res *= x
        x *= x
        n >>= 1
    return res


def count_primes(n: int) -> int:
    """Count primes < n (sieve)."""
    if n <= 2:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p < n:
        if is_prime[p]:
            step = p
            start = p * p
            is_prime[start:n:step] = [False] * (((n - 1 - start) // step) + 1)
        p += 1
    return sum(is_prime)


def trailing_zeroes_factorial(n: int) -> int:
    ans = 0
    while n:
        n //= 5
        ans += n
    return ans

