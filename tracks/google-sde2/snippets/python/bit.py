from __future__ import annotations

from typing import List


def single_number(nums: List[int]) -> int:
    x = 0
    for v in nums:
        x ^= v
    return x


def counting_bits(n: int) -> List[int]:
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits


def total_hamming_distance(nums: List[int]) -> int:
    ans = 0
    n = len(nums)
    for b in range(32):
        ones = 0
        for x in nums:
            ones += (x >> b) & 1
        ans += ones * (n - ones)
    return ans


def maximum_xor_pair(nums: List[int]) -> int:
    """Greedy bit-by-bit using prefixes (no trie)."""
    ans = 0
    mask = 0
    for b in range(31, -1, -1):
        mask |= 1 << b
        prefixes = {x & mask for x in nums}
        candidate = ans | (1 << b)
        if any((candidate ^ p) in prefixes for p in prefixes):
            ans = candidate
    return ans

