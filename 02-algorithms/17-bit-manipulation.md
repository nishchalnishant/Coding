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

| Problem | Tier | Core Trick | Key Insight |
|:--------|:-----|:-----------|:------------|
| **Single Number `⚡ T1`** | Easy | XOR cancellation | `a^a=0`, `a^0=a`; XOR all → lone number |
| **Number of 1 Bits `⚡ T1`** | Easy | Brian Kernighan | `n &= n-1` clears LSB; count iterations |
| **Counting Bits `⚡ T1`** | Easy | DP on bits | `dp[i] = dp[i >> 1] + (i & 1)` |
| **Reverse Bits `🎯 T2`** | Easy | Bit shifting | Extract LSB, build reversed 32-bit int |
| **Missing Number `⚡ T1`** | Easy | XOR or Gauss sum | XOR 0..n with all nums; or `n(n+1)/2 - sum` |
| **Power of Two `⚡ T1`** | Easy | `n & (n-1) == 0` | Power of 2 → exactly one set bit |
| **Sum of Two Integers `🎯 T2`** | Medium | XOR + carry | XOR = addition without carry; AND<<1 = carry |
| **Reverse Integer `🎯 T2`** | Medium | Modular arithmetic | Check overflow before each digit |
| **Single Number III `🎯 T2`** | Medium | XOR + LSB partition | XOR all → `a^b`; use LSB to separate |
| **Bitwise AND of Numbers Range `🎯 T2`** | Medium | Common prefix | AND of range = common bit prefix |
| **Maximum XOR of Two Numbers `💤 T3`** | Hard | Trie on bits | Build bit-trie; greedy pick opposite bit |

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Gotchas |
|:---------|:-------------|:-----------|:--------|
| **Single Number `⚡ T1`** | "All duplicates cancel via XOR" | XOR all numbers; pairs become 0 | Python handles arbitrary-size ints — no overflow |
| **Counting Bits `⚡ T1`** | "Use previously computed answer" | `dp[i] = dp[i>>1] + (i&1)` | Both O(N) and O(N log N) bit-count loop are accepted |
| **Missing Number `⚡ T1`** | "XOR 0..n with array → unpaired index survives" | `res = n; for i,v: res ^= i^v` | Can also do `n*(n+1)//2 - sum(nums)` — simpler but needs overflow check |
| **Power of Two `⚡ T1`** | "`n & (n-1)` clears one bit; power of 2 has exactly one" | `n > 0 and (n & (n-1)) == 0` | n=0 edge case: must check `n > 0` |
| **Number of 1 Bits `⚡ T1`** | "Brian Kernighan: each `n & n-1` removes one set bit" | Loop while `n`; `n &= n-1`; count | Python's `bin(n).count('1')` works but know the algorithm |
| **Bitwise AND of Range `🎯 T2`** | "Common prefix of all numbers in range" | Right-shift both m and n until equal; shift back | The number of shifts = how many trailing bits diverge |

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
