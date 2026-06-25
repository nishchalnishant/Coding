---
tags: [coding, algorithms, bit-manipulation]
topic: Bit Manipulation
difficulty: mixed
---

# Bit Manipulation — Amazon SDE-2

---

## Basics Reference

| Operation | Expression | Notes |
|---|---|---|
| AND | `a & b` | Both bits must be 1 |
| OR | `a \| b` | Either bit is 1 |
| XOR | `a ^ b` | Bits differ |
| NOT | `~a` | Flip all bits |
| Left shift | `a << k` | Multiply by 2^k |
| Right shift | `a >> k` | Divide by 2^k (arithmetic in Python) |
| Check bit k | `(a >> k) & 1` | Returns 0 or 1 |
| Set bit k | `a \| (1 << k)` | |
| Clear bit k | `a & ~(1 << k)` | |
| Clear lowest set bit | `a & (a - 1)` | |
| Isolate lowest set bit | `a & (-a)` | |

**Power of 2 check**: `n > 0 and (n & (n - 1)) == 0`

---

## XOR to Find Single Number

---

### Single Number

> [!example] Problem
> Every element appears twice except for one. Find that single element. LeetCode 136.

> [!info] Approach
> XOR is self-inverse: `a ^ a = 0`, `a ^ 0 = a`. All paired elements cancel; the unique element survives.

> [!note]- Python Solution
> ```python
> from functools import reduce
> from operator import xor
>
> def single_number(nums):
>     return reduce(xor, nums)
> ```

> [!success] Complexity
> Time O(n) | Space O(1).

---

### Single Number III (Two Unique Values)

> [!example] Problem
> Exactly two elements appear only once; all others appear twice. Find both. LeetCode 260.

> [!info] Approach
> XOR all elements → `xor_sum = x ^ y`. Since `x != y`, at least one bit differs. Use `xor_sum & (-xor_sum)` to isolate the rightmost differing bit. Partition the array on that bit; XOR each partition to isolate each unique value.

> [!note]- Python Solution
> ```python
> def single_number_iii(nums):
>     xor_sum = 0
>     for n in nums:
>         xor_sum ^= n
>     diff_bit = xor_sum & (-xor_sum)
>     x = y = 0
>     for num in nums:
>         if num & diff_bit:
>             x ^= num
>         else:
>             y ^= num
>     return [x, y]
> ```

> [!success] Complexity
> Time O(n) | Space O(1).

---

### Missing Number

> [!example] Problem
> Array contains n distinct numbers in range [0, n]. Find the missing one. LeetCode 268.

> [!info] Approach
> XOR all indices `0..n` with all values in `nums`. Missing value survives.

> [!note]- Python Solution
> ```python
> def missing_number(nums):
>     n = len(nums)
>     result = n
>     for i, v in enumerate(nums):
>         result ^= i ^ v
>     return result
> ```

> [!success] Complexity
> Time O(n) | Space O(1).

> [!tip] Alternatives
> Gauss sum: `n*(n+1)//2 - sum(nums)` — simpler, same complexity, no overflow in Python.

---

## Count Set Bits — Brian Kernighan's Algorithm

`n & (n-1)` clears the lowest set bit. Each iteration removes exactly one set bit — O(k) not O(32).

### Number of 1 Bits (Hamming Weight)

> [!example] Problem
> Return the number of set bits in the binary representation of n. LeetCode 191.

> [!note]- Python Solution
> ```python
> def hamming_weight(n):
>     count = 0
>     while n:
>         n &= n - 1    # clear lowest set bit
>         count += 1
>     return count
> ```

> [!success] Complexity
> Time O(k) where k = set bits ≤ 32 | Space O(1).

> [!tip] Alternatives
> `bin(n).count('1')` or `n.bit_count()` (Python 3.10+). Brian Kernighan's is expected when "without built-ins".

---

### Hamming Distance

> [!example] Problem
> Return the number of bit positions where two integers differ. LeetCode 461.

> [!info] Approach
> `hamming_distance(x, y) = popcount(x ^ y)`. XOR marks positions where bits differ; count those.

> [!note]- Python Solution
> ```python
> def hamming_distance(x, y):
>     diff = x ^ y
>     count = 0
>     while diff:
>         diff &= diff - 1
>         count += 1
>     return count
> ```

> [!success] Complexity
> Time O(k) | Space O(1).

---

### Counting Bits

> [!example] Problem
> Return array of length n+1 where `ans[i]` = number of 1s in binary representation of i. LeetCode 338.

> [!info] Approach
> DP recurrence: `dp[i] = dp[i >> 1] + (i & 1)`. Each number equals its right-shift (already computed) plus its lowest bit.

> [!note]- Python Solution
> ```python
> def count_bits(n):
>     dp = [0] * (n + 1)
>     for i in range(1, n + 1):
>         dp[i] = dp[i >> 1] + (i & 1)
>     return dp
> ```

> [!success] Complexity
> Time O(n) | Space O(n).

---

## Power of 2 Check

### Power of Two

> [!example] Problem
> Return true if n is a power of two. LeetCode 231.

> [!info] Approach
> A power of two has exactly one set bit. `n & (n-1)` clears the lowest set bit — result is 0 iff n is a power of two. Guard `n > 0` is mandatory (0 would pass the bit check).

> [!note]- Python Solution
> ```python
> def is_power_of_two(n):
>     return n > 0 and (n & (n - 1)) == 0
> ```

> [!success] Complexity
> Time O(1) | Space O(1).

---

## Bit Masking for Subset Enumeration

Iterate `mask` from `0` to `(1 << n) - 1`. Each integer bijects to a subset — bit `k` set means element `k` is included.

### Subsets via Bitmask

> [!example] Problem
> Given a set of n elements, enumerate all 2^n subsets. LeetCode 78.

> [!note]- Python Solution
> ```python
> def subsets(nums):
>     n = len(nums)
>     result = []
>     for mask in range(1 << n):
>         subset = [nums[k] for k in range(n) if mask & (1 << k)]
>         result.append(subset)
>     return result
> ```

> [!success] Complexity
> Time O(2^n · n) | Space O(2^n · n).

> [!tip] Use case
> Bitmask subset enumeration is the go-to for brute-force optimization over small sets (n ≤ 20). Common in Amazon problems about team selection, covering sets, or assignment problems.

---

## Swap Without Temp Variable

XOR swap: `a ^= b; b ^= a; a ^= b`. After step 1, `a = a^b`. After step 2, `b = (a^b)^b = a`. After step 3, `a = (a^b)^a = b`. Works only when `a` and `b` are distinct memory locations.

```python
def xor_swap(a, b):
    a ^= b
    b ^= a
    a ^= b
    return a, b
```

---

## Reverse Bits

> [!example] Problem
> Reverse bits of a 32-bit unsigned integer. LeetCode 190.

> [!info] Approach
> Extract LSB of n, OR into result, shift result left, shift n right. Repeat 32 times.

> [!note]- Python Solution
> ```python
> def reverse_bits(n):
>     result = 0
>     for _ in range(32):
>         result = (result << 1) | (n & 1)
>         n >>= 1
>     return result & 0xFFFFFFFF
> ```

> [!success] Complexity
> Time O(32) = O(1) | Space O(1).

---

## See Also

[[dynamic-programming]] | [[graph-algorithms]] | [[trie]]
