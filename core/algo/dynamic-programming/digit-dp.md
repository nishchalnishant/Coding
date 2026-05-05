# Digit DP — Count Numbers with Digit-Level Properties

Count integers in `[L, R]` satisfying a digit-level property. Converts to `f(R) − f(L−1)` where `f(X)` counts valid numbers in `[0, X]`, building numbers digit-by-digit with a `tight` flag.

For the broader DP guide see [README.md](README.md).

---

## Theory & Mental Model

**The `tight` constraint.** If `tight=True`, the digit at `pos` can be at most `limit[pos]`. Once you pick a digit strictly less than `limit[pos]`, all future digits are free (`tight` becomes False).

**The `started` flag.** Handles leading zeros. Don't update state (digit sum, mask, remainder) while `started=False`. The number `007` is `7`, not a 3-digit number.

**Standard state:** `dp[pos][tight][started][extra]`
- `pos` — current digit position (MSB = 0)
- `tight` — still bounded by limit?
- `started` — non-zero digit placed yet?
- `extra` — problem-specific (digit sum, last digit, remainder mod K, bitmask of used digits…)

**Complexity.** O(D × |extra_state| × 10) where D ≈ 18 digits.

> [!IMPORTANT]
> **Always call `dp.cache_clear()` between `f(R)` and `f(L-1)`.** The `digits` string lives in the closure; cached results for `f(R)` are wrong for `f(L-1)`.

---

## Universal Template

```python
from functools import lru_cache

def count_up_to(limit: int, K: int) -> int:
    digits = str(limit)
    n = len(digits)

    @lru_cache(maxsize=None)
    def dp(pos: int, tight: bool, started: bool, state: int) -> int:
        if pos == n:
            return 1 if started and is_valid(state, K) else 0
        max_d = int(digits[pos]) if tight else 9
        total = 0
        for d in range(0, max_d + 1):
            new_started = started or d != 0
            new_state = update(state, d) if new_started else state
            total += dp(pos + 1, tight and d == max_d, new_started, new_state)
        return total

    result = dp(0, True, False, 0)
    dp.cache_clear()          # ← critical: clear before next call
    return result

def count_in_range(L: int, R: int, K: int) -> int:
    return count_up_to(R, K) - count_up_to(L - 1, K)
```

---

## Problem 1 — Count Numbers with Digit Sum = K

**State extra:** running digit sum.

```python
from functools import lru_cache

def count_digit_sum(L: int, R: int, K: int) -> int:
    def count_up_to(limit: int) -> int:
        s = str(limit); n = len(s)
        @lru_cache(maxsize=None)
        def dp(pos, tight, started, curr_sum):
            if curr_sum > K: return 0          # prune early
            if pos == n: return 1 if started and curr_sum == K else 0
            max_d = int(s[pos]) if tight else 9
            total = 0
            for d in range(0, max_d + 1):
                new_started = started or d != 0
                new_sum = (curr_sum + d) if new_started else 0
                total += dp(pos+1, tight and d==max_d, new_started, new_sum)
            return total
        result = dp(0, True, False, 0); dp.cache_clear(); return result
    return count_up_to(R) - count_up_to(L - 1)
```

---

## Problem 2 — No Consecutive Same Digits

**State extra:** last digit placed.

```python
from functools import lru_cache

def count_no_consecutive(N: int) -> int:
    s = str(N); n = len(s)
    @lru_cache(maxsize=None)
    def dp(pos, tight, started, last):
        if pos == n: return 1 if started else 0
        max_d = int(s[pos]) if tight else 9
        total = 0
        for d in range(0, max_d + 1):
            if started and d == last: continue    # consecutive same — skip
            new_started = started or d != 0
            new_last = d if new_started else -1
            total += dp(pos+1, tight and d==max_d, new_started, new_last)
        return total
    result = dp(0, True, False, -1); dp.cache_clear(); return result
```

---

## Problem 3 — Count Numbers Divisible by K

**State extra:** `number mod K` (updated as `(rem * 10 + d) % K`).

```python
from functools import lru_cache

def count_divisible(L: int, R: int, K: int) -> int:
    def count_up_to(limit: int) -> int:
        s = str(limit); n = len(s)
        @lru_cache(maxsize=None)
        def dp(pos, tight, started, rem):
            if pos == n: return 1 if started and rem == 0 else 0
            max_d = int(s[pos]) if tight else 9
            total = 0
            for d in range(0, max_d + 1):
                new_started = started or d != 0
                new_rem = (rem * 10 + d) % K if new_started else 0
                total += dp(pos+1, tight and d==max_d, new_started, new_rem)
            return total
        result = dp(0, True, False, 0); dp.cache_clear(); return result
    return count_up_to(R) - count_up_to(L - 1)
```

---

## Problem 4 — Count Numbers with All Unique Digits (LeetCode 357)

**State extra:** 10-bit `mask` of digits used. Only works for N ≤ 10 digit numbers.

```python
from functools import lru_cache

def count_numbers_with_unique_digits(n: int) -> int:
    limit = 10**n - 1
    s = str(limit); L = len(s)
    @lru_cache(maxsize=None)
    def dp(pos, tight, started, mask):
        if pos == L: return 1 if started else 0
        max_d = int(s[pos]) if tight else 9
        total = 0
        for d in range(0, max_d + 1):
            if started and (mask >> d & 1): continue   # digit already used
            new_started = started or d != 0
            new_mask = mask | (1 << d) if new_started else 0
            total += dp(pos+1, tight and d==max_d, new_started, new_mask)
        return total
    result = dp(0, True, False, 0); dp.cache_clear(); return result
```

> [!TIP]
> Total states: 18 × 4 × 2^10 ≈ 73K. Perfectly feasible. Leading zero does not "use" a digit — only apply the mask update when `new_started=True`.

---

## Problem 5 — Count Numbers with No Forbidden Digits

```python
from functools import lru_cache

def count_without_forbidden(N: int, forbidden: frozenset) -> int:
    s = str(N); n = len(s)
    @lru_cache(maxsize=None)
    def dp(pos, tight, started):
        if pos == n: return 1 if started else 0
        max_d = int(s[pos]) if tight else 9
        total = 0
        for d in range(0, max_d + 1):
            if d in forbidden: continue
            total += dp(pos+1, tight and d==max_d, started or d!=0)
        return total
    result = dp(0, True, False); dp.cache_clear(); return result
```

---

## Problem 6 — Digit Occurrence Count in [1, N] (LeetCode 233)

Count total appearances of digit `d` across ALL numbers from 1 to N.

**State extra:** cumulative count of `d` seen so far — return the accumulated total at base case.

```python
from functools import lru_cache

def count_digit_occurrences(N: int, d: int) -> int:
    s = str(N); n = len(s)
    @lru_cache(maxsize=None)
    def dp(pos, tight, started, cnt):
        if pos == n: return cnt if started else 0
        max_d = int(s[pos]) if tight else 9
        total = 0
        for dig in range(0, max_d + 1):
            new_started = started or dig != 0
            new_cnt = cnt + (1 if new_started and dig == d else 0)
            total += dp(pos+1, tight and dig==max_d, new_started, new_cnt)
        return total
    result = dp(0, True, False, 0); dp.cache_clear(); return result
```

---

## Problem 7 — Numbers At Most N Given Digit Set (LeetCode 902)

Given a sorted list of allowed digits (as strings), count integers ≤ N you can build.

```python
def at_most_n_given_digit_set(digits: list[str], n: int) -> int:
    allowed = [int(d) for d in digits]
    s = str(n); L = len(s)

    from functools import lru_cache
    @lru_cache(maxsize=None)
    def dp(pos, tight):
        if pos == L: return 1
        max_d = int(s[pos]) if tight else 9
        total = 0
        for d in allowed:
            if d > max_d: break
            total += dp(pos+1, tight and d==max_d)
        return total

    result = dp(0, True); dp.cache_clear(); return result
```

> [!TIP]
> No `started` flag needed here since all digits are 1–9 (no 0 in the allowed set). If 0 is allowed, re-add `started`.

---

## Interview Questions Table

| Problem | LC # | Key State | Click Moment | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| Count Numbers with Unique Digits | 357 | `digit_mask` | 10-bit bitmask tracks used digits | Leading zero ≠ used digit |
| Numbers At Most N Given Digit Set | 902 | `tight` only | Free positions multiply by `len(digits)` | Sort allowed digits; break early |
| Digit Count in Range | 1067 | `count_of_d` | Return accumulated cnt at base | Different from counting valid numbers |
| Non-neg Integers Without Consecutive Ones | 600 | `last_bit` | Binary `tight` DP | Tight applies to binary string of N |
| Number of Digit One | 233 | `cnt` accumulator | Classic occurrence counting | Math formula also exists (O(log N)) |
| Monotone Increasing Digits | 738 | `last_digit` | `d ≥ last` constraint | Greedy O(N) also works |
| Strobogrammatic Number II | 247 | Build from outside in | Not standard digit DP | Construct, don't count |
| Sum of All Odd Length Subarrays | 1588 | Not digit DP | Contribution counting | Misclassified — use math |

---

## Common Pitfalls

> [!CAUTION]
> **Cache invalidation between `f(R)` and `f(L-1)`** — always call `dp.cache_clear()` after each call. The `digits` closure changes; stale cache gives wrong results.

> [!CAUTION]
> **State during leading zeros** — do NOT update digit sum, mask, or remainder when `started=False`. `007` is `7`; its "digit sum" is 7, not 0+0+7=7 by coincidence — but `006` would wrongly have digit sum 6 if you count the leading zeros.

> [!TIP]
> **Iterative digit DP for very deep recursion** — fill table `dp[pos][state]` from `pos=n-1` down to `pos=0` to avoid Python's recursion limit on 18-digit numbers.

---

## Quick Reference

```
f(R) - f(L-1)                            → always decompose [L,R]
State = (pos, tight, started, extra)     → standard tuple
tight' = tight AND d == max_d            → propagation rule
Update extra only when started=True      → no leading-zero state pollution
dp.cache_clear() after every f(x) call  → critical correctness
```

---

## See also

- [README.md](README.md) — Overview and 4-step framework
- [advanced-dp-optimizations.md](advanced-dp-optimizations.md) — SOS DP for subset-sum over bitmasks
- [questions-bank.md](questions-bank.md) — Tiered drill problems including digit DP
