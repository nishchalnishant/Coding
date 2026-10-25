---
module: striver-a2z/18-recursion
lesson: 2
topic: Pow(x, n)
difficulty: Medium
source: https://takeuforward.org/learning/dsa/pow(x,n)?category=implementation-problems&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, math, divide-and-conquer]
---
# 2. Pow(x, n)

← [Subsequence Patterns](01-subsequence-patterns.md) · [Part 18 index](README.md) · Next → [Generate Parentheses](03-generate-parentheses.md)

> [!abstract] Problem at a glance
> **Task:** Compute xⁿ for a double `x` and a 32-bit integer `n` (possibly negative) in O(log n).
> **Key insight:** xⁿ = (x^(n/2))² when n is even, and x · xⁿ⁻¹ when odd. Halving the exponent gives O(log n). For negative n, compute (1/x)^|n| — using a 64-bit copy of n, since |INT_MIN| overflows int.
> **Difficulty:** Medium · **Pattern:** Binary exponentiation (divide and conquer) · **Also on:** [LC 50](https://leetcode.com/problems/powx-n/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/pow(x,n)?category=implementation-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Repeated multiplication](#3-repeated-multiplication) · [4. Recursive fast power](#4-recursive-fast-power) · [5. Iterative binary exponentiation](#5-iterative-binary-exponentiation) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement `pow(x, n)`, which returns `x` raised to the power `n`. `n` may be negative or zero.

| Input | Output | Why |
|---|---|---|
| `x = 2.0, n = 10` | `1024.0` |  |
| `x = 2.1, n = 3` | `9.261` |  |
| `x = 2.0, n = −2` | `0.25` | 2⁻² = 1/4 |

**Constraints:** `−100 < x < 100`, `−2³¹ ≤ n ≤ 2³¹ − 1`, `x ≠ 0` or `n > 0`, `|xⁿ| ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Repeated multiplication | multiply x |n| times | O(|n|) | O(1) |
| Recursive fast power | half = pow(x, n/2); half² (· x if odd) | O(log n) | O(log n) stack |
| Iterative binary exponentiation | walk the bits of n; square x each step, multiply when the bit is set | O(log n) | O(1) |

> [!tip] Interview angle
> The classic first recursion question that's really about complexity. Expected: O(n) loop → O(log n) recursion → iterative bit version. The trap they wait for is `n = −2³¹`: `-n` overflows int, so convert to `long` first. The same squaring trick powers modular exponentiation (Count Good Numbers, next).

---

## 3. Repeated multiplication

**Intuition.** Multiply `|n|` times and invert for negative n. Correct but 2³¹ iterations in the worst case — too slow.

```python
def pow_loop(x, n):
    r = 1.0
    for _ in range(abs(n)):
        r *= x
    return 1 / r if n < 0 else r
```

**Complexity:** time **O(|n|)**, space **O(1)**.

---

## 4. Recursive fast power

**Intuition.** Compute `half = pow(x, n // 2)` **once** and square it. Calling `pow(x, n/2) * pow(x, n/2)` recomputes the half and is O(n) again. Base case `n == 0 → 1`.

```python
def pow_rec(x, n):
    if n < 0:
        return 1 / pow_rec(x, -n)
    if n == 0:
        return 1.0
    half = pow_rec(x, n // 2)
    return half * half * (x if n % 2 else 1)
```

**Complexity:** time **O(log n)**, space **O(log n) stack**.

---

## 5. Iterative binary exponentiation

**Intuition.** Write `n` in binary: x¹³ = x⁸ · x⁴ · x¹. Keep `base = x, x², x⁴, …` by squaring, and multiply it into the result when the current bit of `N` is 1. Do it on `N = |n|` as a 64-bit value; invert at the end if `n < 0`.

**Algorithm**

1. `N = |n|` as long, `res = 1`.
2. While `N > 0`: if `N & 1` → `res *= x`; `x *= x`; `N >>= 1`.
3. Return `n < 0 ? 1/res : res`.

**Dry run** — x = 2, n = 10 (1010₂): bit0 0 → x = 4; bit1 1 → res 4, x = 16; bit2 0 → x = 256; bit3 1 → res 1024.

**C++**
```cpp
double myPow(double x, int n) {
    long long N = n;
    if (N < 0) { x = 1 / x; N = -N; }
    double res = 1;
    while (N > 0) {
        if (N & 1) res *= x;
        x *= x;
        N >>= 1;
    }
    return res;
}
```

**Java**
```java
static double myPow(double x, int n) {
    long N = n;
    if (N < 0) { x = 1 / x; N = -N; }
    double res = 1;
    while (N > 0) {
        if ((N & 1) == 1) res *= x;
        x *= x;
        N >>= 1;
    }
    return res;
}
```

**Python**
```python
def my_pow(x, n):
    N = abs(n)
    if n < 0:
        x = 1 / x
    res = 1.0
    while N:
        if N & 1:
            res *= x
        x *= x
        N >>= 1
    return res
```

**Complexity:** time **O(log n)**, space **O(1)** — one iteration per bit of |n|, at most 32.

---

## Edge cases

- `n = 0` → 1.
- `n = −2³¹` — negating in 32 bits overflows.
- Negative base with odd/even exponent.
- `x = 1` or `−1` with huge n.

---

## Common mistakes

1. `pow(x, n/2) * pow(x, n/2)` — two recursive calls make it O(n).
2. `n = -n` on an int when n = INT_MIN.
3. Inverting inside the loop instead of once.

---

## Follow-ups

1. Modular power `aᵇ mod m` (LC 372, Count Good Numbers).
2. Matrix power for Fibonacci in O(log n).

<details><summary>Answer sketches</summary>

**#1:** Same loop with `% m` after each multiply; use 64-bit products.

**#2:** Square the 2×2 matrix `[[1,1],[1,0]]` the same way.
</details>

---

## Flashcards

**Binary exponentiation step?** #flashcard
If bit set: res *= base; then base *= base; n >>= 1.

**pow(x, INT_MIN) pitfall?** #flashcard
−INT_MIN overflows int; copy n into a 64-bit variable first.

**Why compute half once?** #flashcard
Two calls on n/2 give T(n) = 2T(n/2) + 1 = O(n).

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../04-practice/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../04-practice/algorithms/12-backtracking.md)
