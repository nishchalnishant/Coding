---
module: striver/18-recursion
lesson: 5
topic: Count Good Numbers
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-good-numbers?category=implementation-problems&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, math, modular-arithmetic]
---
# 5. Count Good Numbers

← [Power Set](04-power-set.md) · [Part 18 index](README.md) · Next → [Reverse a Stack](06-reverse-a-stack.md)

> [!abstract] Problem at a glance
> **Task:** Count length-n digit strings with even digits at even indices and prime digits at odd indices, mod 10⁹ + 7.
> **Key insight:** Positions are independent: ⌈n/2⌉ even indices with 5 choices {0,2,4,6,8}, ⌊n/2⌋ odd indices with 4 choices {2,3,5,7}. Answer = 5^⌈n/2⌉ · 4^⌊n/2⌋ mod p, with n up to 10¹⁵ — so fast modular power.
> **Difficulty:** Medium · **Pattern:** Counting + modular binary exponentiation · **Also on:** [LC 1922](https://leetcode.com/problems/count-good-numbers/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-good-numbers?category=implementation-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Loop over positions](#3-loop-over-positions) · [4. Fast modular power](#4-fast-modular-power) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A digit string is **good** if digits at even indices (0-based) are even and digits at odd indices are prime (2, 3, 5, 7). Given `n`, return the number of good digit strings of length `n` modulo 10⁹ + 7. Leading zeros are allowed.

| Input | Output | Why |
|---|---|---|
| `n = 1` | `5` | 0, 2, 4, 6, 8 |
| `n = 4` | `400` | 5 · 4 · 5 · 4 |
| `n = 50` | `564908303` |  |

**Constraints:** `1 ≤ n ≤ 10¹⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Loop over positions | multiply 5 or 4 per index | O(n) | O(1) |
| Fast modular power | pow(5, ⌈n/2⌉) · pow(4, ⌊n/2⌋) mod p | O(log n) | O(1) |

> [!tip] Interview angle
> Two steps: (1) the combinatorics — multiply choices per position; (2) the constraint 10¹⁵ rules out a loop, so modular fast power. Watch the 64-bit products: `(a · b) % MOD` with both < 10⁹ + 7 fits in a signed 64-bit integer.

---

## 3. Loop over positions

**Intuition.** Walk indices 0 … n − 1, multiply by 5 on even, 4 on odd, mod each step. Correct but 10¹⁵ iterations.

```python
def good_loop(n):
    MOD, r = 10**9 + 7, 1
    for i in range(n):
        r = r * (5 if i % 2 == 0 else 4) % MOD
    return r
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Fast modular power

**Intuition.** Use binary exponentiation with `% MOD` after every multiply. Python's built-in `pow(b, e, m)` does exactly this; write the loop in C++/Java.

**Dry run** — n = 4: even positions 2, odd 2 → 5² · 4² = 25 · 16 = 400.

**C++**
```cpp
long long powmod(long long b, long long e, long long m) {
    long long r = 1;
    b %= m;
    while (e > 0) {
        if (e & 1) r = r * b % m;
        b = b * b % m;
        e >>= 1;
    }
    return r;
}
int countGoodNumbers(long long n) {
    const long long MOD = 1e9 + 7;
    return powmod(5, (n + 1) / 2, MOD) * powmod(4, n / 2, MOD) % MOD;
}
```

**Java**
```java
static long powmod(long b, long e, long m) {
    long r = 1;
    b %= m;
    while (e > 0) {
        if ((e & 1) == 1) r = r * b % m;
        b = b * b % m;
        e >>= 1;
    }
    return r;
}
static int countGoodNumbers(long n) {
    final long MOD = 1_000_000_007L;
    return (int) (powmod(5, (n + 1) / 2, MOD) * powmod(4, n / 2, MOD) % MOD);
}
```

**Python**
```python
def count_good_numbers(n):
    MOD = 10**9 + 7
    def powmod(b, e):
        r = 1
        while e:
            if e & 1:
                r = r * b % MOD
            b = b * b % MOD
            e >>= 1
        return r
    return powmod(5, (n + 1) // 2) * powmod(4, n // 2) % MOD
```

**Complexity:** time **O(log n)**, space **O(1)** — two exponentiations of ≤ 50 bits each.

---

## Edge cases

- n = 1 → 5 (only one even index).
- Odd n: one more even index than odd.
- n = 10¹⁵ — exponent needs 64 bits.

---

## Common mistakes

1. Swapping ⌈n/2⌉ and ⌊n/2⌋ (index 0 is even).
2. Counting 1 or 9 as prime / missing 0 as even.
3. Taking `% MOD` only at the end — intermediate overflow.
4. Int exponent when n is 10¹⁵.

---

## Follow-ups

1. Digits restricted further (no leading zero).
2. Super Pow aᵇ with b as a digit array (LC 372).

<details><summary>Answer sketches</summary>

**#1:** First position gets 4 choices; multiply separately.

**#2:** aᵇ = (a^(b without last digit))¹⁰ · a^(last digit), all mod 1337.
</details>

---

## Flashcards

**Count Good Numbers formula?** #flashcard
5^⌈n/2⌉ · 4^⌊n/2⌋ mod 10⁹ + 7.

**Why is (a · b) % MOD safe in 64 bits?** #flashcard
a, b < 10⁹ + 7 ≈ 2³⁰, product < 2⁶⁰ < 2⁶³.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
