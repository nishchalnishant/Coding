---
module: striver-a2z/16-binary-search
lesson: 15
topic: Find Nth Root of a Number
difficulty: Medium
source: https://takeuforward.org/learning/dsa/find-nth-root-of-a-number?category=on-answers&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer, math]
---
# 15. Find Nth Root of a Number

← [Find Square Root of a Number](14-square-root.md) · [Part 16 index](README.md) · Next → [Find the Smallest Divisor](16-smallest-divisor.md)

> [!abstract] Problem at a glance
> **Task:** Return the integer `x` with `xⁿ = m`, or −1 if `m` is not a perfect n-th power.
> **Key insight:** Binary search `x` in `[1, m]`. Compute `midⁿ` with early exit: stop multiplying as soon as the product exceeds `m` — no overflow and no floating point.
> **Difficulty:** Medium · **Pattern:** Binary search on answer — exact match
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-nth-root-of-a-number?category=on-answers&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear search](#3-linear-search) · [4. Binary search with capped power](#4-binary-search-with-capped-power) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given positive integers `n` and `m`, return the positive integer `x` such that `xⁿ = m`, or `-1` if no such integer exists.

| Input | Output | Why |
|---|---|---|
| `n = 3, m = 27` | `3` |  |
| `n = 4, m = 69` | `-1` | 2⁴ = 16, 3⁴ = 81 |
| `n = 1, m = 14` | `14` |  |

**Constraints:** `1 ≤ n ≤ 30`, `1 ≤ m ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear search | x = 1, 2, … while xⁿ ≤ m | O(m^(1/n) · n) | O(1) |
| Binary search with capped power | pow(mid, n) returns 0/1/2 for < / = / > m | O(n log m) | O(1) |

---

## 3. Linear search

**Intuition.** Stops at the first `xⁿ ≥ m`.

```python
def nth_root_linear(n, m):
    x = 1
    while x ** n < m:
        x += 1
    return x if x ** n == m else -1
```

**Complexity:** time **O(m^(1/n) · n)**, space **O(1)**.

---

## 4. Binary search with capped power

**Intuition.** A helper multiplies `mid` up to `n` times and bails out with "greater" once the running product passes `m`. That caps every intermediate at ≤ `m · mid` ≤ 10¹⁸, which fits in 64-bit. Then ordinary binary search: equal → return, less → right, greater → left.

**Dry run** — n = 3, m = 27: lo 1 hi 27 mid 14 (> 27) hi 13; mid 7 (> 27) hi 6; mid 3 (27 = 27) → 3.

**Why not `pow(mid, n)` from the library?** Floating-point rounding: `pow(5, 3)` may come back as 124.9999… and cast to 124.

**C++**
```cpp
int cmpPow(long long mid, int n, int m) {
    long long r = 1;
    for (int i = 0; i < n; i++) {
        r *= mid;
        if (r > m) return 2;
    }
    return r == m ? 1 : 0;
}
int nthRoot(int n, int m) {
    int lo = 1, hi = m;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int c = cmpPow(mid, n, m);
        if (c == 1) return mid;
        if (c == 0) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

**Java**
```java
static int cmpPow(long mid, int n, int m) {
    long r = 1;
    for (int i = 0; i < n; i++) {
        r *= mid;
        if (r > m) return 2;
    }
    return r == m ? 1 : 0;
}
static int nthRoot(int n, int m) {
    int lo = 1, hi = m;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int c = cmpPow(mid, n, m);
        if (c == 1) return mid;
        if (c == 0) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

**Python**
```python
def nth_root(n, m):
    def cmp(mid):
        r = 1
        for _ in range(n):
            r *= mid
            if r > m:
                return 2
        return 1 if r == m else 0
    lo, hi = 1, m
    while lo <= hi:
        mid = (lo + hi) // 2
        c = cmp(mid)
        if c == 1:
            return mid
        if c == 0:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

**Complexity:** time **O(n log m)**, space **O(1)** — log m iterations, each ≤ n multiplications.

---

## Edge cases

- n = 1 → answer m.
- m = 1 → answer 1.
- Large n with m ≤ 10⁹ — only 1 and 2 can work.

---

## Common mistakes

1. Library `pow` + cast — rounding errors.
2. Computing midⁿ fully — overflows for mid ~ 10⁹, n ~ 30.

---

## Follow-ups

1. Real-valued n-th root to 6 decimals.
2. Faster power.

<details><summary>Answer sketches</summary>

**#1:** Binary search on doubles for ~60 iterations.

**#2:** Fast exponentiation with the same early cap: O(log n) per check.
</details>

---

## Flashcards

**Nth root without overflow?** #flashcard
Multiply step by step and stop once the product exceeds m.

**Why avoid library pow for exact roots?** #flashcard
Floating-point rounding can make 5³ come out as 124.999…

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
