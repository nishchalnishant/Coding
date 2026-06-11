---
module: 02-algorithms
topic: Bit Manipulation
subtopic:
status: unread
tags: [algorithms, bit-manipulation]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. Appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Know the patterns cold.
> `💤 T3` — **TIER 3 · Skim or Skip**: Conceptual awareness only.

## First-Principles Map

```
WHY bit manipulation exists → WHAT it is → HOW it works → WHEN to use
        │                         │               │               │
  [CPUs operate on bits;     [direct operation  [bitwise AND     [constant-factor
   O(1) word-size operations  on binary         OR XOR NOT       speedup; XOR
   replace expensive          representation;   left/right-      tricks for
   arithmetic; interview      integers as bit   shift; each      duplicate/missing
   problems exploit XOR       arrays of width   op is 1 CPU      numbers; bitmask
   cancellation and           32 or 64]         instruction]     for subset DP
   masking tricks]                                               on N ≤ 20]
```

## First-Principles Breakdown

- **Root problem**: Many number-theory and set-membership problems have O(N) arithmetic solutions; bits reduce these to O(1) word operations.
- **Core insight**: XOR is its own inverse — `a ^ a = 0` and `a ^ 0 = a`. This cancellation property solves "find the odd one out" problems in O(N) time and O(1) space.
- **Key invariant**: `n & (n-1)` clears the lowest set bit of `n`. When `n` is a power of 2, this produces 0.
- **Where it breaks**: Bit tricks are unreadable — always add a comment explaining what the operation does. Sign extension in right-shift (`>>` arithmetic vs `>>>` logical) differs across languages.

---

# Bit Manipulation — L3 Gold Standard

## Operator Reference

| Operator | Symbol | Example | Result | What It Does |
|:---------|:-------|:--------|:-------|:-------------|
| AND | `&` | `5 & 3` | `1` | 1 only where BOTH bits are 1 |
| OR | `\|` | `5 \| 3` | `7` | 1 where EITHER bit is 1 |
| XOR | `^` | `5 ^ 3` | `6` | 1 where bits DIFFER |
| NOT | `~` | `~5` | `-6` | Flip all bits (two's complement) |
| Left shift | `<<` | `1 << 3` | `8` | Multiply by 2^n |
| Right shift | `>>` | `8 >> 2` | `2` | Divide by 2^n (arithmetic) |

---

## Core Tricks — The Essential 8

### Trick 1: XOR Cancellation — Find the Single Number

> [!IMPORTANT]
> **The Click Moment**: "Every element appears twice except one" — OR — "find the missing/unique number". XOR cancellation is the O(1) space solution.

```python
def single_number(nums: list[int]) -> int:
    result = 0
    for n in nums:
        result ^= n
    return result
    # All pairs cancel: a^a = 0; the lone number remains

def missing_number(nums: list[int]) -> int:
    # XOR all indices 0..n with all values
    result = len(nums)
    for i, n in enumerate(nums):
        result ^= i ^ n
    return result
```

**Variants:**
1. **Single Number II `🎯 T2`** — Every element appears *three* times except one. Use bit counting: for each bit position, `count % 3` gives the surviving number's bit.
2. **Single Number III `🎯 T2`** — Two elements appear once. XOR all → get `a^b`. Find any set bit (e.g. `diff & -diff`), partition numbers by that bit → XOR each partition → `a` and `b`.

---

### Trick 2: Power of Two Check

> [!TIP]
> A power of 2 in binary is exactly one 1-bit. Subtracting 1 flips that bit and all lower bits. So `n & (n-1) == 0` iff `n` is a power of 2.

```python
def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0

def is_power_of_four(n: int) -> bool:
    # Power of 4: power of 2 AND the set bit is at an even position
    # 0xAAAAAAAA = ...10101010 (bits at odd positions)
    return n > 0 and (n & (n - 1)) == 0 and (n & 0xAAAAAAAA) == 0
```

---

### Trick 3: Count Set Bits (Hamming Weight / Popcount)

```python
def hamming_weight(n: int) -> int:
    count = 0
    while n:
        n &= (n - 1)   # clear lowest set bit — Brian Kernighan's algorithm
        count += 1
    return count

# Built-in alternative (Python 3.10+)
def hamming_weight_builtin(n: int) -> int:
    return bin(n).count('1')
```

**Brian Kernighan intuition**: `n & (n-1)` always clears exactly one bit (the lowest set bit). So the loop runs exactly `popcount(n)` times.

---

### Trick 4: Get / Set / Clear / Toggle a Specific Bit

```python
def get_bit(n: int, i: int) -> int:
    return (n >> i) & 1            # shift i right, check last bit

def set_bit(n: int, i: int) -> int:
    return n | (1 << i)            # OR with a mask that has only bit i set

def clear_bit(n: int, i: int) -> int:
    return n & ~(1 << i)           # AND with complement (bit i = 0, rest = 1)

def toggle_bit(n: int, i: int) -> int:
    return n ^ (1 << i)            # XOR flips only bit i
```

---

### Trick 5: Two's Complement — Lowest Set Bit

```python
def lowest_set_bit(n: int) -> int:
    return n & (-n)   # -n = ~n + 1 in two's complement; AND keeps only LSB
```

Used in Fenwick trees, partitioning for Single Number III.

---

### Trick 6: Reverse Bits

```python
def reverse_bits(n: int) -> int:
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

---

### Trick 7: Add Two Integers Without `+`

```python
def get_sum(a: int, b: int) -> int:
    # Python integers are arbitrary precision — mask to 32-bit
    mask = 0xFFFFFFFF
    while b & mask:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    # Handle negative number (sign extension)
    return a if b == 0 else ~(a ^ mask)
```

---

### Trick 8: Subsets via Bitmask

```python
def all_subsets(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    result = []
    for mask in range(1 << n):   # 2^n masks
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result
```

> [!TIP]
> **Bitmask DP** uses this pattern when N ≤ 20: state `dp[mask]` represents "what is the optimal answer having visited the set of nodes encoded in mask".

---

## Canonical Interview Problems

| Problem | Diff | Tier | Core Trick | Key Insight |
|:--------|:-----|:-----|:-----------|:------------|
| Single Number | Easy | `⚡ T1` | XOR cancellation | `a^a=0`; XOR all → lone number |
| Number of 1 Bits | Easy | `⚡ T1` | Brian Kernighan | `n &= n-1` clears LSB; count iterations |
| Counting Bits | Easy | `⚡ T1` | DP on bits | `dp[i] = dp[i >> 1] + (i & 1)` |
| Missing Number | Easy | `⚡ T1` | XOR or Gauss sum | XOR `0..n` with values; or `n(n+1)/2 - sum` |
| Power of Two | Easy | `⚡ T1` | `n & (n-1) == 0` | Exactly one set bit |
| Reverse Bits | Easy | `🎯 T2` | Bit shifting | Build reversed 32-bit int LSB-first |
| Sum of Two Integers | Medium | `🎯 T2` | XOR + carry | XOR = sum without carry; `&<<1` = carry |
| Single Number II | Medium | `🎯 T2` | Bit count mod 3 | Per-bit sum mod 3 across all numbers |
| Single Number III | Medium | `🎯 T2` | XOR + LSB partition | XOR all → `a^b`; split by any set bit |
| Bitwise AND of Numbers Range | Medium | `🎯 T2` | Common prefix | Strip trailing bits until `m == n` |
| Reverse Integer | Medium | `🎯 T2` | Modular arithmetic | Check 32-bit overflow before append digit |
| Maximum XOR of Two Numbers | Hard | `💤 T3` | Bit trie | Greedy opposite bit at each level |

---

## Interview Questions — Deep Dive

### Single Number `⚡ T1`

> [!example] Problem
> Given an integer array `nums` where every element appears **twice** except for one element which appears **once**, find and return that single element.
> You must implement a solution with **linear runtime** and use only **constant extra space**.
>
> **Example 1:**
> ```
> Input: nums = [2,2,1]
> Output: 1
> ```
>
> **Example 2:**
> ```
> Input: nums = [4,1,2,1,2]
> Output: 4
> ```
>
> **Constraints:**
> - `1 <= nums.length <= 3 * 10^4`
> - `-3 * 10^4 <= nums[i] <= 3 * 10^4`
> - Each element appears twice except for one element that appears once.

> [!info] Approach
> XOR is associative and commutative. Duplicates cancel: `x ^ x = 0`. XOR-ing every element leaves the unique number. One pass, O(1) extra space.

> [!note]- Python Solution
> ```python
> def single_number(nums: list[int]) -> int:
>     result = 0
>     for n in nums:
>         result ^= n
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Gotchas
> - Works for negative numbers — XOR sign follows two's complement rules.
> - Do not sort + scan — that is O(n log n) and wastes the bit trick.

---

### Single Number II `🎯 T2`

> [!example] Problem
> Given an integer array `nums` where every element appears **three times** except for one element which appears **once**, find the single element.
> Your algorithm should have **linear runtime** and use only **constant extra space**.
>
> **Example:**
> ```
> Input: nums = [2,2,3,2]
> Output: 3
> ```
>
> **Constraints:**
> - `1 <= nums.length <= 3 * 10^4`
> - `-2^31 <= nums[i] <= 2^31 - 1`
> - Each element appears three times except for one.

> [!info] Approach
> Count each bit position across all numbers. If a bit appears `3k+1` times total, it belongs to the single number. Maintain `ones` and `twos` bitmasks (state machine) or use an array of 32 counters mod 3.

> [!note]- Python Solution
> ```python
> def single_number_ii(nums: list[int]) -> int:
>     ones = twos = 0
>     for n in nums:
>         ones = (ones ^ n) & ~twos
>         twos = (twos ^ n) & ~ones
>     return ones
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Gotchas
> - XOR-all alone fails — triples do not cancel to zero.
> - Alternative: `sum(bits[i] for n in nums for i in range(32)) % 3` per bit — clearer but slower constant factor.

---

### Single Number III `🎯 T2`

> [!example] Problem
> Given an integer array `nums` in which **exactly two** elements appear once and all other elements appear **twice**, return the two single elements in **any order**.
>
> **Example:**
> ```
> Input: nums = [1,2,1,3,2,5]
> Output: [3,5]
> ```
>
> **Constraints:**
> - `2 <= nums.length <= 3 * 10^4`
> - `-2^31 <= nums[i] <= 2^31 - 1`
> - Each integer appears exactly once or twice.

> [!info] Approach
> XOR all numbers → `xor = a ^ b` (the two singles). Any set bit in `xor` differs between `a` and `b`. Use `bit = xor & (-xor)` (lowest set bit) to partition nums into two groups; XOR each group separately.

> [!note]- Python Solution
> ```python
> def single_number_iii(nums: list[int]) -> list[int]:
>     xor_all = 0
>     for n in nums:
>         xor_all ^= n
>     bit = xor_all & (-xor_all)
>     a = 0
>     for n in nums:
>         if n & bit:
>             a ^= n
>     return [a, xor_all ^ a]
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Gotchas
> - `xor_all` is zero only if the two singles are equal — impossible under problem constraints.
> - Any set bit works for partitioning; LSB is the usual choice.

---

### Number of 1 Bits (Hamming Weight) `⚡ T1`

> [!example] Problem
> Write a function that takes the unsigned integer `n` and returns the number of `'1'` bits in its binary representation (also known as the **Hamming weight**).
>
> **Example 1:**
> ```
> Input: n = 11   (binary 1011)
> Output: 3
> ```
>
> **Example 2:**
> ```
> Input: n = 128  (binary 10000000)
> Output: 1
> ```
>
> **Constraints:**
> - The input must be a **unsigned** 32-bit integer.

> [!info] Approach
> **Brian Kernighan:** `n & (n-1)` clears the lowest set bit. Loop until `n == 0`, incrementing count each iteration. Exactly `popcount(n)` iterations.

> [!note]- Python Solution
> ```python
> def hamming_weight(n: int) -> int:
>     count = 0
>     while n:
>         n &= n - 1
>         count += 1
>     return count
> ```

> [!success] Complexity
> Time O(k) where k = number of set bits; Space O(1).

> [!tip] Gotchas
> - Python: `bin(n).count('1')` is acceptable in interviews if you also know Brian Kernighan.
> - For signed negative `n`, mask to 32 bits: `n &= 0xFFFFFFFF`.

---

### Counting Bits `⚡ T1`

> [!example] Problem
> Given an integer `n`, return an array `ans` of length `n + 1` where `ans[i]` is the number of `'1'` bits in the binary representation of `i`.
>
> **Example:**
> ```
> Input: n = 5
> Output: [0,1,1,2,1,2]
> Explanation:
> 0 → 0
> 1 → 1
> 2 → 10
> 3 → 11
> 4 → 100
> 5 → 101
> ```
>
> **Constraints:**
> - `0 <= n <= 10^5`

> [!info] Approach
> **DP recurrence:** dropping the last bit (`i >> 1`) removes exactly one bit if `i` is odd.
> `dp[i] = dp[i >> 1] + (i & 1)`. O(n) single pass.

> [!note]- Python Solution
> ```python
> def count_bits(n: int) -> list[int]:
>     dp = [0] * (n + 1)
>     for i in range(1, n + 1):
>         dp[i] = dp[i >> 1] + (i & 1)
>     return dp
> ```

> [!success] Complexity
> Time O(n), Space O(n) for output.

> [!tip] Gotchas
> - Naive `bin(i).count('1')` per i is O(n log n) — too slow for n = 10^5.
> - `dp[i] = dp[i & (i-1)] + 1` also works (Brian Kernighan on predecessor).

---

### Missing Number `⚡ T1`

> [!example] Problem
> Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is **missing** from the array.
>
> **Example 1:**
> ```
> Input: nums = [3,0,1]
> Output: 2
> ```
>
> **Example 2:**
> ```
> Input: nums = [0,1]
> Output: 2
> ```
>
> **Constraints:**
> - `n == nums.length`
> - `1 <= n <= 10^4`
> - `0 <= nums[i] <= n`
> - All numbers are unique.

> [!info] Approach
> **XOR:** XOR all indices `0..n` with all values. Paired `(index, value)` for present numbers cancel; missing index/value survives.
> **Alternative:** Gauss sum `n*(n+1)//2 - sum(nums)`.

> [!note]- Python Solution
> ```python
> def missing_number(nums: list[int]) -> int:
>     result = len(nums)
>     for i, v in enumerate(nums):
>         result ^= i ^ v
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Gotchas
> - Gauss formula is simpler to explain but mention overflow on other languages (Python handles big ints).
> - Sort and scan is O(n log n) — unnecessary.

---

### Power of Two `⚡ T1`

> [!example] Problem
> Given an integer `n`, return `true` if it is a **power of two**. Otherwise, return `false`.
> An integer `n` is a power of two if there exists an integer `x` such that `n == 2^x`.
>
> **Example 1:**
> ```
> Input: n = 1
> Output: true   (2^0)
> ```
>
> **Example 2:**
> ```
> Input: n = 16
> Output: true
> ```
>
> **Example 3:**
> ```
> Input: n = 3
> Output: false
> ```
>
> **Constraints:**
> - `-2^31 <= n <= 2^31 - 1`

> [!info] Approach
> Powers of two have exactly one set bit. `n & (n-1)` clears the lowest set bit; result is 0 iff `n` had only one bit. Require `n > 0` (0 and negatives fail).

> [!note]- Python Solution
> ```python
> def is_power_of_two(n: int) -> bool:
>     return n > 0 and (n & (n - 1)) == 0
> ```

> [!success] Complexity
> Time O(1), Space O(1).

> [!tip] Gotchas
> - `n = 0` → false (not a power of two).
> - `n = 1` → true (`2^0`).

---

### Reverse Bits `🎯 T2`

> [!example] Problem
> Reverse bits of a given **32-bit unsigned** integer `n` and return the result.
>
> **Example:**
> ```
> Input: n = 43261596  (00000010100101000001111010011100)
> Output: 964176192   (00111001011110000010100101000000)
> ```
>
> **Constraints:**
> - The input must be a **unsigned** 32-bit integer.

> [!info] Approach
> Extract LSB of `n` with `n & 1`, append to `result` via `(result << 1) | bit`, then shift `n` right. Repeat 32 times.

> [!note]- Python Solution
> ```python
> def reverse_bits(n: int) -> int:
>     result = 0
>     for _ in range(32):
>         result = (result << 1) | (n & 1)
>         n >>= 1
>     return result
> ```

> [!success] Complexity
> Time O(32) = O(1), Space O(1).

> [!tip] Gotchas
> - Must process exactly 32 bits even if leading bits are zero.
> - Python ints are unbounded — problem expects 32-bit wrap semantics.

---

### Sum of Two Integers `🎯 T2`

> [!example] Problem
> Given two integers `a` and `b`, return the **sum** of the two integers **without using** the operators `+` and `-`.
>
> **Example 1:**
> ```
> Input: a = 1, b = 2
> Output: 3
> ```
>
> **Example 2:**
> ```
> Input: a = 2, b = 3
> Output: 5
> ```
>
> **Constraints:**
> - `-1000 <= a, b <= 1000`

> [!info] Approach
> Binary addition: **sum without carry** = `a ^ b`; **carry** = `(a & b) << 1`. Repeat until carry is 0. Mask to 32 bits in languages with fixed width; handle sign extension in Python.

> [!note]- Python Solution
> ```python
> def get_sum(a: int, b: int) -> int:
>     mask = 0xFFFFFFFF
>     while b & mask:
>         carry = (a & b) << 1
>         a = (a ^ b) & mask
>         b = carry & mask
>     if b > mask // 2:
>         return ~(a ^ mask)
>     return a
> ```

> [!success] Complexity
> Time O(32) per carry propagation in worst case, Space O(1).

> [!tip] Gotchas
> - Python arbitrary precision — mask each iteration or result may grow unbounded.
> - Interviewers often accept `while b: a, b = a ^ b, (a & b) << 1` with a verbal 32-bit note.

---

### Bitwise AND of Numbers Range `🎯 T2`

> [!example] Problem
> Given two integers `left` and `right` that represent the range `[left, right]` inclusive, return the **bitwise AND** of all numbers in this range, inclusive.
>
> **Example 1:**
> ```
> Input: left = 5, right = 7
> Output: 4
> Explanation: 5 & 6 & 7 = 4
> ```
>
> **Example 2:**
> ```
> Input: left = 0, right = 0
> Output: 0
> ```
>
> **Constraints:**
> - `0 <= left <= right <= 2^31 - 1`

> [!info] Approach
> AND of a range equals the **common binary prefix** of `left` and `right`. While `left < right`, shift both right (strip divergent trailing bits). Shift accumulated prefix back left by the same count.

> [!note]- Python Solution
> ```python
> def range_bitwise_and(left: int, right: int) -> int:
>     shift = 0
>     while left < right:
>         left >>= 1
>         right >>= 1
>         shift += 1
>     return left << shift
> ```

> [!success] Complexity
> Time O(log n), Space O(1).

> [!tip] Gotchas
> - Brute force AND loop TLEs when `right - left` is huge.
> - Intuition: once range spans a bit flip, that bit is 0 in the answer.

---

### Reverse Integer `🎯 T2`

> [!example] Problem
> Given a signed 32-bit integer `x`, return `x` with its digits **reversed**. If reversing causes the value to go outside the signed 32-bit range `[-2^31, 2^31 - 1]`, return **0**.
> Assume the environment does not allow 64-bit integers.
>
> **Example 1:**
> ```
> Input: x = 123
> Output: 321
> ```
>
> **Example 2:**
> ```
> Input: x = -123
> Output: -321
> ```
>
> **Example 3:**
> ```
> Input: x = 120
> Output: 21
> ```
>
> **Constraints:**
> - `-2^31 <= x <= 2^31 - 1`

> [!info] Approach
> Pop last digit: `digit = x % 10` (handle sign). Check overflow **before** `result = result * 10 + digit`. Bounds: `result > INT_MAX // 10` or `(result == INT_MAX // 10 and digit > 7)`.

> [!note]- Python Solution
> ```python
> def reverse(x: int) -> int:
>     INT_MAX, INT_MIN = 2**31 - 1, -2**31
>     sign = -1 if x < 0 else 1
>     x = abs(x)
>     result = 0
>     while x:
>         digit = x % 10
>         x //= 10
>         if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
>             return 0
>         result = result * 10 + digit
>     return sign * result
> ```

> [!success] Complexity
> Time O(log x), Space O(1).

> [!tip] Gotchas
> - Trailing zeros in input → reversed number has fewer digits (e.g. 120 → 21).
> - Classic overflow check is the main interview signal — not strictly bit manipulation but grouped here often.

---

### Maximum XOR of Two Numbers in an Array `💤 T3`

> [!example] Problem
> Given an integer array `nums`, return the **maximum result** of `nums[i] XOR nums[j]` where `0 <= i <= j < n`.
>
> **Example:**
> ```
> Input: nums = [3,10,5,25,2,8]
> Output: 28
> Explanation: 5 XOR 25 = 28
> ```
>
> **Constraints:**
> - `1 <= nums.length <= 2 * 10^5`
> - `0 <= nums[i] <= 2^31 - 1`

> [!info] Approach
> Build a **binary trie** (MSB → LSB). For each number, walk the trie greedily choosing the **opposite** bit when available to maximize XOR. O(n · 32) time.

> [!note]- Python Solution
> ```python
> class TrieNode:
>     __slots__ = ('child',)
>     def __init__(self):
>         self.child = [None, None]

> def find_maximum_xor(nums: list[int]) -> int:
>     root = TrieNode()
>     for n in nums:
>         node = root
>         for i in range(31, -1, -1):
>             bit = (n >> i) & 1
>             if node.child[bit] is None:
>                 node.child[bit] = TrieNode()
>             node = node.child[bit]
>     best = 0
>     for n in nums:
>         node = root
>         curr = 0
>         for i in range(31, -1, -1):
>             bit = (n >> i) & 1
>             want = 1 - bit
>             if node.child[want]:
>                 curr |= 1 << i
>                 node = node.child[want]
>             else:
>                 node = node.child[bit]
>         best = max(best, curr)
>     return best
> ```

> [!success] Complexity
> Time O(n · 32), Space O(n · 32) for trie nodes.

> [!tip] Gotchas
> - `💤 T3` for L3 — know the trie-on-bits idea; full implementation is rare at L3.
> - Brute force O(n²) fails on n = 2 × 10^5.

---

## Interview Questions — Quick Reference

| Question | Diff | Click Moment | Core Logic | Gotchas |
|:---------|:-----|:-------------|:-----------|:--------|
| **Single Number `⚡ T1`** | E | All duplicates cancel via XOR | XOR all numbers | Pairs become 0; lone survives |
| **Single Number II `🎯 T2`** | M | Triples need per-bit mod 3 | `ones`/`twos` state machine | XOR-all alone fails |
| **Single Number III `🎯 T2`** | M | Two singles → partition by set bit | XOR all → `a^b`; split groups | `bit = xor & (-xor)` |
| **Number of 1 Bits `⚡ T1`** | E | Brian Kernighan clears LSB | `while n: n &= n-1; count++` | Know algorithm, not only `bin().count` |
| **Counting Bits `⚡ T1`** | E | Reuse smaller index | `dp[i] = dp[i>>1] + (i&1)` | O(n) not O(n log n) |
| **Missing Number `⚡ T1`** | E | XOR indices with values | `res ^= i ^ v`; start `res = n` | Gauss sum alternative |
| **Power of Two `⚡ T1`** | E | One set bit only | `n > 0 and (n & (n-1)) == 0` | `n = 0` is false |
| **Reverse Bits `🎯 T2`** | E | Build from LSB | 32 iterations shift/or | Exactly 32 bits |
| **Sum of Two Integers `🎯 T2`** | M | XOR + carry loop | `a^b` sum; `(a&b)<<1` carry | Mask in Python |
| **Bitwise AND of Range `🎯 T2`** | M | Common prefix of m and n | Shift until equal; shift back | Brute AND TLEs |
| **Reverse Integer `🎯 T2`** | M | Check overflow before multiply | Pop digit; pre-check bounds | Returns 0 on overflow |
| **Maximum XOR `💤 T3`** | H | Trie on bits MSB→LSB | Greedy opposite bit | L3: concept > code |

---

## Quick Revision Triggers

- If "find the unique / lone element in a sea of duplicates" → **XOR all**.
- If "is this number a power of 2?" → `n > 0 and (n & (n-1)) == 0`.
- If "count set bits in N" → Brian Kernighan `n &= n-1` loop, or `bin(n).count('1')`.
- If "enumerate all subsets of N elements" → bitmask loop `for mask in range(1<<N)`.
- If "manipulate specific bit position i" → get: `(n>>i)&1`; set: `n|(1<<i)`; clear: `n&~(1<<i)`; toggle: `n^(1<<i)`.
- If N ≤ 20 and problem involves "visited sets or subset enumeration" → **Bitmask DP**.

---

## See Also

- [Dynamic Programming](./15-dynamic-programming.md) — Bitmask DP for TSP / subset problems
- [Backtracking](./12-backtracking.md) — Alternative to bitmask for subset enumeration
- [Math & Number Theory](./18-math-and-number-theory.md) — GCD, prime, modular arithmetic

---

## Flashcards

**What is the XOR cancellation property and what interview problem type does it solve?** #flashcard
`a ^ a = 0` and `a ^ 0 = a`. XOR is its own inverse. If every number appears twice except one, XOR-ing all numbers cancels all pairs and leaves the single unique number. Time O(N), space O(1).

**How does `n & (n-1)` work, and what are its two main uses?** #flashcard
`n & (n-1)` clears the lowest set bit of `n` because subtracting 1 flips the lowest 1-bit and all lower bits, and AND with the original keeps everything above. Uses: (1) Check `n & (n-1) == 0` to test if `n` is a power of 2. (2) Loop while `n != 0`, doing `n &= (n-1)` and incrementing count — this is Brian Kernighan's algorithm for counting set bits in exactly `popcount(n)` iterations.

**What are the four fundamental single-bit operations (get/set/clear/toggle)?** #flashcard
- **Get bit i**: `(n >> i) & 1`
- **Set bit i**: `n | (1 << i)`
- **Clear bit i**: `n & ~(1 << i)`
- **Toggle bit i**: `n ^ (1 << i)`

**How does bitmask subset enumeration work, and what is its time complexity?** #flashcard
For N elements, there are `2^N` subsets. Loop `for mask in range(1 << N)`. For each mask, bit `i` being set means element `i` is included. To extract the subset: `[nums[i] for i in range(N) if mask & (1 << i)]`. Total time: O(N × 2^N). Used in bitmask DP when N ≤ 20.
