# Combination Problems — Complete Family

All combination-type recursive problems unified. The key distinction: **order matters (permutations)** vs **order doesn't matter (combinations)** vs **unlimited reuse vs single use**. For the pattern foundation see [aditya-verma.md](aditya-verma.md).

---

## Theory — The Combination Decision Tree

**Combinations vs Permutations:**
- **Combinations:** `{1,2,3}` and `{3,2,1}` are the **same** — order doesn't matter.
- **Permutations:** `[1,2,3]` and `[3,2,1]` are **different** — order matters.

**Key trick for combinations:** Pass a `start` index. Each recursive call only considers elements from `start` onward — this prevents using elements that were already considered at a higher level, which is what produces unordered subsets.

```
Permutations: loop over ALL unused elements each time
Combinations: loop from START index each time (no backwards)
```

---

## Problem 1 — Combinations (LC 77)

**Problem:** Choose exactly K numbers from 1..N. Return all combinations.

```python
def combine(n: int, k: int) -> list[list[int]]:
    result = []

    def backtrack(start: int, current: list[int]) -> None:
        if len(current) == k:
            result.append(current[:])
            return
        # Pruning: need (k - len(current)) more elements; can only go to n
        for i in range(start, n - (k - len(current)) + 2):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()

    backtrack(1, [])
    return result
```

> [!TIP]
> **Pruning:** If you need `k - len(current)` more elements, the loop only needs to run until `n - (k - len(current)) + 1`. Beyond that, not enough elements remain to form a valid combination. This prunes roughly half the tree.

---

## Problem 2 — Combination Sum I — Unlimited Reuse (LC 39)

**Problem:** Find all combinations of `candidates` (distinct) that sum to `target`. Each candidate can be reused unlimited times.

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()   # enables early termination
    result = []

    def backtrack(start: int, remaining: int, current: list[int]) -> None:
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                   # sorted: all subsequent are also too large
            current.append(candidates[i])
            backtrack(i, remaining - candidates[i], current)   # i not i+1: reuse allowed
            current.pop()

    backtrack(0, target, [])
    return result
```

> [!IMPORTANT]
> **Reuse = recurse with same `i`** (not `i+1`). This is the only difference from Combination Sum II. The `start=i` in the recursive call allows picking the same element again.

---

## Problem 3 — Combination Sum II — Each Used Once, Duplicates in Input (LC 40)

**Problem:** Find all unique combinations of `candidates` (may have duplicates) that sum to `target`. Each candidate used at most once.

```python
def combination_sum_ii(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    result = []

    def backtrack(start: int, remaining: int, current: list[int]) -> None:
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            if i > start and candidates[i] == candidates[i-1]:
                continue               # skip duplicate at same level
            current.append(candidates[i])
            backtrack(i + 1, remaining - candidates[i], current)   # i+1: no reuse
            current.pop()

    backtrack(0, target, [])
    return result
```

> [!CAUTION]
> The duplicate-skip condition is `i > start` (not `i > 0`). This skips duplicates at the **same recursion level** but allows the same value to appear across different levels (e.g., using two 1s from `[1, 1, 2]` is valid — they come from different positions).

---

## Problem 4 — Combination Sum III — Exactly K Numbers from 1–9 (LC 216)

**Problem:** Find all combinations of exactly K numbers from 1..9 that sum to N. Each number used at most once.

```python
def combination_sum_iii(k: int, n: int) -> list[list[int]]:
    result = []

    def backtrack(start: int, remaining: int, current: list[int]) -> None:
        if len(current) == k and remaining == 0:
            result.append(current[:])
            return
        if len(current) == k or remaining <= 0:
            return
        for i in range(start, 10):
            current.append(i)
            backtrack(i + 1, remaining - i, current)
            current.pop()

    backtrack(1, n, [])
    return result
```

---

## Problem 5 — Combination Sum IV — Count Ordered Combinations (LC 377)

**Problem:** Count the number of ways to reach `target` using `nums` with repetition, where **order matters** (so [1,2] and [2,1] are different).

> **Note:** This is really a **permutation with repetition** problem, but it's in the "combination sum" family. Because order matters, use DP (not backtracking recursion).

```python
def combination_sum_iv(nums: list[int], target: int) -> int:
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(remaining: int) -> int:
        if remaining == 0: return 1
        if remaining < 0:  return 0
        return sum(dp(remaining - n) for n in nums)

    return dp(target)

# Bottom-up version:
def combination_sum_iv_dp(nums: list[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1
    for t in range(1, target + 1):    # amount outer = permutations (order matters)
        for n in nums:
            if t >= n:
                dp[t] += dp[t - n]
    return dp[target]
```

> [!TIP]
> **Order matters → amount outer loop.** In Coin Change II (combinations, order doesn't matter), you put coins in the outer loop. Here, target in the outer loop considers all orderings. This is the fundamental loop-order distinction.

---

## Problem 6 — Subsets → Combinations Relationship

Subsets (Power Set) generates ALL combinations of ALL sizes. Combinations restricts to size exactly K.

```python
def subsets(nums: list[int]) -> list[list[int]]:
    """All combinations of all sizes (power set)."""
    result = []
    def backtrack(start, current):
        result.append(current[:])    # record at EVERY node (not just leaves)
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    backtrack(0, [])
    return result

def combinations_of_size_k(nums: list[int], k: int) -> list[list[int]]:
    """Only size-k combinations — add size check."""
    result = []
    def backtrack(start, current):
        if len(current) == k:
            result.append(current[:])
            return                   # don't go deeper — already at size k
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    backtrack(0, [])
    return result
```

---

## Problem 7 — Letter Combinations of a Phone Number (LC 17)

```python
def letter_combinations(digits: str) -> list[str]:
    if not digits: return []   # edge case: empty input returns [], NOT ['']
    mapping = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    result = []

    def backtrack(i: int, current: list[str]) -> None:
        if i == len(digits):
            result.append(''.join(current))
            return
        for ch in mapping[digits[i]]:
            current.append(ch)
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

> [!CAUTION]
> Empty input → return `[]`, not `['']`. This is a classic edge case. One digit maps to up to 4 letters; `'7'` and `'9'` have 4 letters each.

---

## Problem 8 — Restore IP Addresses (LC 93)

```python
def restore_ip_addresses(s: str) -> list[str]:
    result = []

    def backtrack(start: int, parts: list[str]) -> None:
        if len(parts) == 4:
            if start == len(s):
                result.append('.'.join(parts))
            return
        for length in range(1, 4):   # each segment: 1-3 digits
            if start + length > len(s): break
            segment = s[start:start+length]
            if len(segment) > 1 and segment[0] == '0': break   # no leading zeros
            if int(segment) > 255: break
            parts.append(segment)
            backtrack(start + length, parts)
            parts.pop()

    backtrack(0, [])
    return result
```

---

## Problem 9 — Count Subsets with Given Sum

```python
def count_subsets_with_sum(nums: list[int], target: int) -> int:
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def solve(i: int, remaining: int) -> int:
        if remaining == 0: return 1     # found valid subset
        if i == len(nums) or remaining < 0: return 0
        return (solve(i+1, remaining - nums[i]) +   # include
                solve(i+1, remaining))               # exclude

    return solve(0, target)

# Bottom-up (0/1 knapsack counting variant):
def count_subsets_dp(nums: list[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1
    for num in nums:
        for w in range(target, num-1, -1):   # backward = 0/1
            dp[w] += dp[w - num]
    return dp[target]
```

---

## Comparison Table

| Problem | Reuse | Duplicates in input | Order matters | Key trick |
| :--- | :--- | :--- | :--- | :--- |
| **Subsets** | No | No | No | Record at every node |
| **Subsets II** | No | Yes | No | Sort + skip `nums[j]==nums[j-1]` when `j>start` |
| **Combinations** | No | No | No | Prune: loop to `n-(k-len)+1` |
| **Combination Sum I** | Yes | No | No | Recurse with same `i` |
| **Combination Sum II** | No | Yes | No | Sort + skip `candidates[i]==candidates[i-1]` when `i>start` |
| **Combination Sum III** | No | No | No | Both size and sum constraints |
| **Combination Sum IV** | Yes | No | **Yes** | DP with amount in outer loop |
| **Permutations** | No | No | Yes | `used[]` array or swap-based |
| **Permutations II** | No | Yes | Yes | Sort + `not used[i-1]` guard |

---

## Interview Questions — Logic & Trickiness

| Problem | LC # | Click Moment | Key Code Pattern | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| **Combinations** | 77 | "Choose K of N, order doesn't matter" | `start` index; prune loop end | Pruning: `n - (k-len) + 2` as upper bound |
| **Combination Sum I** | 39 | "Unlimited reuse + sum target" | `backtrack(i, ...)` — same index | Sort + `break` when `candidates[i] > remaining` |
| **Combination Sum II** | 40 | "Each once, duplicates in input" | `backtrack(i+1, ...)` + skip guard | `i > start` not `i > 0` for skip condition |
| **Combination Sum III** | 216 | "Exactly K digits 1-9 summing to N" | Both `len==k` AND `remaining==0` at base | Range is 1..9 (not all integers) |
| **Combination Sum IV** | 377 | "Order matters → DP not backtrack" | Amount outer loop → counts permutations | This is really unbounded knapsack counting with order |
| **Phone Letter Combos** | 17 | "Map each digit to chars; all strings" | IP/OP: digit index, char list | Empty digits → `[]` not `['']` |
| **Restore IP Addresses** | 93 | "Partition into 4 valid 0-255 parts" | Exactly 4 parts; break on leading zero or > 255 | Leading zero: `len > 1 and segment[0]=='0'` |
| **Subsets** | 78 | "Record at every node (not just leaves)" | `result.append(current[:])` before loop | Record before loop, not inside |
| **Subsets II** | 90 | "Dedup: sort + skip same value at same level" | `if j > start and nums[j] == nums[j-1]: continue` | `j > start` allows same value in different levels |

---

## See also

- [aditya-verma.md](aditya-verma.md) — Include/Exclude (Pattern 1) and Permutations (Pattern 2)
- [README.md](README.md) — Recursion theory
- [../dynamic-programming/dp-aditya-verma.md](../dynamic-programming/dp-aditya-verma.md) — 0/1 Knapsack for subset sum counting
- [questions-bank.md](questions-bank.md) — Tiered drill questions
