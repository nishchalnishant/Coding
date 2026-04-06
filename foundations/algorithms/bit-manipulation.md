# Bit Manipulation — SDE-3 Level

Use binary representation and bitwise operators for compact state and fast operations. SDE-3: masking, subset enumeration, XOR properties, and bitmask DP (N ≤ 20).

---

## 1. Concept Overview

**Problem space**: Single number (XOR), power of 2, count set bits, subset generation (bitmask), bitmask DP (TSP, partition), XOR trie (max XOR pair), low-level optimizations.

**When to use**: "Unique number" in duplicates → XOR. "All subsets" with small n → iterate mask 0 to 2^n-1. "State as set" with n≤20 → bitmask DP. "Max XOR" → binary trie.

---

## 2. Core Operators & Tricks

- **AND `&`**: Mask/clear bits. `n & 1` = last bit (even/odd). `n & (n-1)` clears lowest set bit (count bits, power of 2).
- **OR `|`**: Set bits. `n | (1<<k)` set k-th bit.
- **XOR `^`**: Toggle; `a^a=0`, `a^0=a`. Unique in pairs → XOR all.
- **Left/Right shift**: `<< k` = *2^k; `>> k` = /2^k (unsigned).
- **Power of 2**: `n > 0 && (n & (n-1)) == 0`.
- **Count set bits**: While n: n &= n-1, count++. Or popcount (built-in in many languages).

---

## 3. Advanced Variations

- **Subsets via bitmask**: For n elements, for mask in 0..2^n-1: element i included if (mask >> i) & 1. O(2^n).
- **Bitmask DP**: State = mask (visited set); e.g., TSP dp[mask][i] = min cost to visit mask ending at i. Transition: try unvisited j. O(2^n * n^2).
- **Single Number II**: Count bits mod 3 per position; result = bits that are 1 mod 3. Or state machine (ones, twos).
- **Max XOR of two numbers**: Binary trie (each number as 31-bit); for each number traverse trie preferring opposite bit; update max XOR.

### Edge Cases
- Negative numbers (signed right shift); overflow in left shift; 0 (power of 2 false); empty array (single number).

---

## 4. Common Interview Problems

**Easy**: Number of 1 Bits, Power of Two, Missing Number (XOR), Single Number.  
**Medium**: Bitwise AND of Numbers Range, Subsets (bitmask), Single Number II/III, Maximum XOR of Two Numbers.  
**Hard**: Min Time to Finish All Jobs (bitmask DP), N-Queens (bitmask for columns/diagonals).

---

## 5. Pattern Recognition

- **XOR**: Pairs cancel; single number; XOR of two numbers (a^b with a,b from two groups).
- **Bitmask**: Subset (include/exclude per bit); state = set of indices → integer mask.
- **Bitmask DP**: TSP, partition to K subsets, "assign N items with constraints" when N small.
- **Trie**: Max XOR = trie with opposite-bit preference.

---

## 6. Code Implementations

```python
def count_set_bits(n):
    c = 0
    while n:
        n &= n - 1
        c += 1
    return c

def single_number(nums):
    return 0 if not nums else __import__('functools').reduce(lambda a, b: a ^ b, nums)

def subsets_bitmask(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):
        result.append([nums[i] for i in range(n) if (mask >> i) & 1])
    return result
```

---

## 7. SDE-3 Level Thinking

- **Trade-offs**: Bitmask for small n (cache-friendly, one integer); for large n use set or recursive backtracking. XOR for constant space "unique" problems.
- **Memory**: Bitmask O(1) for state; bitmask DP O(2^n * ...) — only feasible for n ≤ ~20.

---

## 8. Interview Strategy

- **Identify**: "Unique" / "pairs" → XOR. "All subsets" / "assign N items" with N small → bitmask. "Max XOR" → trie.
- **Common mistakes**: Signed vs unsigned right shift; 1<<k for k>= word size; forgetting to handle 0.

---

## 9. Quick Revision

- **Formulas**: Clear lowest bit: n & (n-1). Set k-th: n | (1<<k). Check k-th: (n >> k) & 1.
- **Tricks**: XOR all for single number; mask loop for subsets; bitmask DP for TSP/partition.
- **Edge cases**: Negative; zero; k out of range.
- **Pattern tip**: "State as set" + small N → bitmask DP.

---

## See also

- [Dynamic Programming](dynamic-programming/README.md) — bitmask DP  
- [Backtracking](backtracking.md) — N-Queens with bit masks  
- [Maths](maths.md) — modular arithmetic with bits
