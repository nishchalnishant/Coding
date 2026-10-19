---
module: striver/16-binary-search
lesson: 14
topic: Find Square Root of a Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/find-square-root-of-a-number?category=on-answers&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer, math]
---
# 14. Find Square Root of a Number

← [Count Occurrences in a Sorted Array](13-count-occurrences.md) · [Part 16 index](README.md) · Next → [Find Nth Root of a Number](15-nth-root.md)

> [!abstract] Problem at a glance
> **Task:** Return `⌊√n⌋` without using a library square root.
> **Key insight:** `mid² ≤ n` is true for small `mid` and false for large — monotone. The answer is the **last true** in `[0, n]`. Compute `mid * mid` in 64-bit (or compare `mid ≤ n / mid`).
> **Difficulty:** Easy · **Pattern:** Binary search on answer — last true · **Also on:** [LC 69](https://leetcode.com/problems/sqrtx/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-square-root-of-a-number?category=on-answers&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear search](#3-linear-search) · [4. Newton's method](#4-newtons-method) · [5. Binary search on the answer](#5-binary-search-on-the-answer) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `n`, return the floor of its square root. Built-in exponent/sqrt functions are not allowed.

| Input | Output | Why |
|---|---|---|
| `n = 28` | `5` | 5² = 25 ≤ 28 < 36 |
| `n = 36` | `6` |  |
| `n = 0` | `0` |  |

**Constraints:** `0 ≤ n ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear search | increase i while (i+1)² ≤ n | O(√n) | O(1) |
| Newton's method | x ← (x + n/x) / 2 until x² ≤ n | O(log n), very fast in practice | O(1) |
| Binary search on the answer | mid² ≤ n → ans = mid, lo = mid + 1; else hi = mid − 1 | O(log n) | O(1) |

> [!tip] Interview angle
> This is the gateway to "binary search on the answer": the search space is the *range of possible answers*, not array indices. Say: "answers 0..n, predicate mid² ≤ n is monotone, I want the largest true."

---

## 3. Linear search

**Intuition.** Try every candidate from 0 upward.

```python
def floor_sqrt_linear(n):
    i = 0
    while (i + 1) * (i + 1) <= n:
        i += 1
    return i
```

**Complexity:** time **O(√n)**, space **O(1)**.

---

## 4. Newton's method

**Intuition.** Integer Newton iteration converges quadratically from above. Worth naming as a follow-up; binary search is what's expected.

```python
def floor_sqrt_newton(n):
    if n < 2:
        return n
    x = n
    while x * x > n:
        x = (x + n // x) // 2
    return x
```

**Complexity:** time **O(log n), very fast in practice**, space **O(1)**.

---

## 5. Binary search on the answer

**Intuition.** Search `[1, n]` (handle 0 separately or start at 0). When `mid² ≤ n`, `mid` is feasible and the answer is `mid` or larger. Otherwise it's smaller.

**Dry run** — n = 28: lo 1 hi 28 mid 14 (196 > 28) hi 13; mid 7 (49) hi 6; mid 3 (9 ≤ 28) ans 3, lo 4; mid 5 (25) ans 5, lo 6; mid 6 (36) hi 5 → 5.

**Last-true trick:** at loop exit (`lo > hi`), `hi` is the last true and `lo` the first false — so you can `return hi` without an `ans` variable.

**C++**
```cpp
int floorSqrt(int n) {
    long long lo = 0, hi = n, ans = 0;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (mid * mid <= n) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    return (int)ans;
}
```

**Java**
```java
static int floorSqrt(int n) {
    long lo = 0, hi = n, ans = 0;
    while (lo <= hi) {
        long mid = lo + (hi - lo) / 2;
        if (mid * mid <= n) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    return (int) ans;
}
```

**Python**
```python
def floor_sqrt(n):
    lo, hi, ans = 0, n, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= n:
            ans, lo = mid, mid + 1
        else:
            hi = mid - 1
    return ans
```

**Complexity:** time **O(log n)**, space **O(1)** — log₂ of the answer range.

---

## Edge cases

- n = 0, 1.
- n = INT_MAX — `mid * mid` overflows a 32-bit int.

---

## Common mistakes

1. 32-bit `mid * mid`.
2. Searching `[0, n/2]` and missing n = 1.

---

## Follow-ups

1. Precision to d decimals.
2. Is n a perfect square? (LC 367)

<details><summary>Answer sketches</summary>

**#1:** Binary search on doubles for a fixed number of iterations (~100), or integer search then refine digit by digit.

**#2:** `floor_sqrt(n)² == n`.
</details>

---

## Flashcards

**Binary search on answer — first question to ask?** #flashcard
What range can the answer lie in, and is the feasibility predicate monotone?

**Avoid overflow in mid² ≤ n?** #flashcard
64-bit, or mid ≤ n / mid.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
