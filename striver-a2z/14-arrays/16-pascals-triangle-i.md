---
module: striver-a2z/14-arrays
lesson: 16
topic: Pascal's Triangle I
difficulty: Easy
source: https://takeuforward.org/learning/dsa/pascals-triangle-i?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, math, combinatorics, pascal]
---
# 16. Pascal's Triangle I

← [Print the Matrix in Spiral Manner](15-spiral-matrix.md) · [Part 14 index](README.md) · Next → [Pascal's Triangle II](17-pascals-triangle-ii.md)

> [!abstract] Problem at a glance
> **Task:** Return the element at row `r`, column `c` (both 1-indexed) of Pascal's triangle.
> **Key insight:** That element is C(r − 1, c − 1). Compute it in O(c) with the running product `res = res · (n − i) / (i + 1)`, which stays an integer at every step, instead of building the whole triangle or using factorials that overflow.
> **Difficulty:** Easy · **Pattern:** Combinatorics: nCr
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/pascals-triangle-i?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Factorials](#3-factorials) · [4. Running product nCr](#4-running-product-ncr) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two integers `r` and `c`, return the value at the `r`-th row and `c`-th column (1-indexed) of Pascal's triangle. Row 1 is `[1]`; each inner value is the sum of the two values above it.

| Input | Output | Why |
|---|---|---|
| `r = 4, c = 2` | `3` | row 4 = 1 3 3 1 |
| `r = 5, c = 3` | `6` | row 5 = 1 4 6 4 1 |

**Constraints:** `1 ≤ c ≤ r ≤ 30` (the answer fits in a 32-bit int).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Factorials | n! / (k! (n−k)!) | O(n) | O(1) |
| Running product nCr | res = res·(n − i)/(i + 1), i < k | O(min(k, n − k)) | O(1) |

---

## 3. Factorials

**Intuition.** Direct formula, but `n!` overflows 64-bit integers past 20!, so it only works for tiny `n` in C++/Java. Python's big ints hide the issue.

```python
def pascal_fact(r, c):
    from math import factorial as f
    n, k = r - 1, c - 1
    return f(n) // (f(k) * f(n - k))
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Running product nCr

**Intuition.** `C(n, k) = (n/1) · ((n−1)/2) · … · ((n−k+1)/k)`. After `i + 1` factors the partial product is `C(n, i + 1)`, an integer, so multiplying first and then dividing is exact. Use `k = min(k, n − k)` to halve the work.

**Dry run** — r = 5, c = 3 → n = 4, k = 2: res = 1 → 1·4/1 = 4 → 4·3/2 = 6.

**Why C(r − 1, c − 1)?** Each value counts the paths from the apex down to it, choosing "left" or "right" at each of `r − 1` steps with `c − 1` rights.

**C++**
```cpp
long long nCr(int n, int k) {
    k = min(k, n - k);
    long long res = 1;
    for (int i = 0; i < k; i++) res = res * (n - i) / (i + 1);
    return res;
}
int pascalTriangleI(int r, int c) { return (int)nCr(r - 1, c - 1); }
```

**Java**
```java
static long nCr(int n, int k) {
    k = Math.min(k, n - k);
    long res = 1;
    for (int i = 0; i < k; i++) res = res * (n - i) / (i + 1);
    return res;
}
static int pascalTriangleI(int r, int c) { return (int) nCr(r - 1, c - 1); }
```

**Python**
```python
def pascal_element(r, c):
    n, k = r - 1, min(c - 1, r - c)
    res = 1
    for i in range(k):
        res = res * (n - i) // (i + 1)
    return res
```

**Complexity:** time **O(min(k, n − k))**, space **O(1)**.

---

## Edge cases

- c = 1 or c = r → 1.
- Largest middle value at r = 30 still fits in int; the intermediate product needs 64-bit.

---

## Common mistakes

1. Off-by-one: using C(r, c) instead of C(r − 1, c − 1).
2. Dividing before multiplying → fractional truncation.
3. `int` for the intermediate product → overflow.

---

## Follow-ups

1. C(n, k) mod 1e9+7 for large n.
2. Unique paths in an m × n grid (LC 62).

<details><summary>Answer sketches</summary>

**#1:** Precompute factorials and inverse factorials (Fermat's little theorem) ([Part 31](../31-maths/README.md)).

**#2:** C(m + n − 2, m − 1), same running product.
</details>

---

## Flashcards

**Pascal (r, c), 1-indexed, equals?** #flashcard
C(r − 1, c − 1).

**Overflow-safe nCr loop?** #flashcard
res = res · (n − i) / (i + 1) for i in 0..k−1, with k = min(k, n − k).

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
