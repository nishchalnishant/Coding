---
module: striver-a2z/08-basic-maths
lesson: 13
topic: Divisors of a Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/divisors-of-a-number?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, divisors, sqrt]
---
# 13. Divisors of a Number

← [LCM of Two Numbers](12-lcm-of-two-numbers.md) · [Part 8 index](README.md) · Next → [Part 9: Basic Arrays](../09-basic-arrays/README.md)

> [!abstract] Problem at a glance
> **Task:** Return all positive divisors of `n` in ascending order.
> **Key insight:** Loop `i` up to √n. Push `i` onto a small list and `n/i` onto a large list, then join `small + reversed(large)` for sorted output with no sort call.
> **Difficulty:** Easy · **Pattern:** √n divisor pairing
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/divisors-of-a-number?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — test every i](#3-brute--test-every-i) · [4. Better — √n pairs + sort](#4-better--n-pairs--sort) · [5. Optimal — two lists](#5-optimal--two-lists) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a positive integer `n`, return a list of all its positive divisors sorted in increasing order.

| Input | Output | Why |
|---|---|---|
| `n = 6` | `[1, 2, 3, 6]` |  |
| `n = 8` | `[1, 2, 4, 8]` |  |
| `n = 36` | `[1, 2, 3, 4, 6, 9, 12, 18, 36]` | 6 appears once |
| `n = 1` | `[1]` |  |

**Constraints:** `1 ≤ n ≤ 10⁹`. `n ≤ 10⁹` has at most 1344 divisors.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — test every i | i in 1..n | O(n) | O(d(n)) |
| Better — √n pairs + sort | collect pairs, then sort | O(√n + d log d) | O(d) |
| Optimal — two lists | small asc + large desc reversed | O(√n) | O(d) |

---

## 3. Brute — test every i

**Intuition.** Test every `i` from 1 to n. The output is sorted automatically, but this takes 10⁹ steps at the limit.

```python
def divisors_brute(n):
    return [i for i in range(1, n + 1) if n % i == 0]
```

**Complexity:** time **O(n)**, space **O(d(n))**.

---

## 4. Better — √n pairs + sort

**Intuition.** Collect both `i` and `n / i` for each `i ≤ √n`, then sort. The sort is cheap because `d(n)` is small, but you can avoid it entirely.

```python
def divisors_sort(n):
    res, i = [], 1
    while i * i <= n:
        if n % i == 0:
            res.append(i)
            if i != n // i:
                res.append(n // i)
        i += 1
    return sorted(res)
```

**Complexity:** time **O(√n + d log d)**, space **O(d)**.

---

## 5. Optimal — two lists

**Intuition.** As `i` increases, the small partners `i` come out ascending and the large partners `n / i` come out descending. Append the small ones to `lo` and the large ones to `hi`, then output `lo + reverse(hi)`. Skip the large partner when `i * i == n`.

**Algorithm**

1. `lo, hi = [], []`.
2. For `i = 1` while `i * i ≤ n`: if `n % i == 0`: `lo.append(i)`; if `i != n / i`, `hi.append(n / i)`.
3. Return `lo + reversed(hi)`.

**Dry run** — `n = 36`

| i | lo | hi |
|---|---|---|
| 1 | 1 | 36 |
| 2 | 1 2 | 36 18 |
| 3 | 1 2 3 | 36 18 12 |
| 4 | 1 2 3 4 | 36 18 12 9 |
| 6 | 1 2 3 4 6 | (6 = 36/6, skip) |

→ `1 2 3 4 6` + `9 12 18 36`.

**C++**
```cpp
vector<int> divisors(int n) {
    vector<int> lo, hi;
    for (long long i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            lo.push_back((int)i);
            if (i != n / i) hi.push_back((int)(n / i));
        }
    }
    lo.insert(lo.end(), hi.rbegin(), hi.rend());
    return lo;
}
```

**Java**
```java
static List<Integer> divisors(int n) {
    List<Integer> lo = new ArrayList<>(), hi = new ArrayList<>();
    for (long i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            lo.add((int) i);
            if (i != n / i) hi.add((int) (n / i));
        }
    }
    Collections.reverse(hi);
    lo.addAll(hi);
    return lo;
}
```

**Python**
```python
def divisors(n):
    lo, hi = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            lo.append(i)
            if i != n // i:
                hi.append(n // i)
        i += 1
    return lo + hi[::-1]
```

**Complexity:** time **O(√n)**, space **O(d)** — √n iterations; the output size d(n) ≤ 1344 for n ≤ 10⁹.

---

## Edge cases

- `n = 1` → `[1]`. Here `i = n / i`, so it must be added once.
- Perfect squares → the root appears once.
- Primes → `[1, n]`.

---

## Common mistakes

1. Adding `√n` twice for perfect squares.
2. Using floating `sqrt(n)` as the bound; use `i * i ≤ n`.
3. Sorting when two lists would do. It's harmless, but it misses the O(√n) bound the interviewer wants.

---

## Follow-ups

1. Count the divisors without listing them.
2. Sum of the divisors.
3. Divisors of every number up to N.

<details><summary>Answer sketches</summary>

**#1:** Factorise `n = Π pᵢ^eᵢ`; the count is `Π (eᵢ + 1)`.

**#2:** `σ(n) = Π (p^(e+1) − 1)/(p − 1)`, or sum the pairs in the √n loop.

**#3:** For each `i`, append `i` to the lists of `i, 2i, 3i, …`. That's a harmonic sum, so O(N log N) total.
</details>

---

## Flashcards

**Sorted divisors in O(√n)?** #flashcard
Small partners ascending into lo, large partners into hi, return lo + reversed(hi).

**Divisor count from the factorisation?** #flashcard
Π (eᵢ + 1).

**Max divisors of a number ≤ 10⁹?** #flashcard
1344 (735 134 400).

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
