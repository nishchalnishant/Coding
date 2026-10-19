---
module: striver/08-basic-maths
lesson: 8
topic: Check for Perfect Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-for-perfect-number?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, divisors, sqrt]
---
# 8. Check for Perfect Number

← [Check if the Number is Armstrong](07-check-if-the-number-is-armstrong.md) · [Part 8 index](README.md) · Next → [Check for Prime Number](09-check-for-prime-number.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `n` equals the sum of its proper divisors (all divisors except `n`).
> **Key insight:** Divisors come in pairs `(i, n/i)` with `i ≤ √n`. Sum both members of each pair, and count a square root only once.
> **Difficulty:** Easy · **Pattern:** √n divisor pairing · **Also on:** LC 507
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-for-perfect-number?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — all i < n](#3-brute--all-i--n) · [4. Optimal — √n pairs](#4-optimal--n-pairs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A **perfect number** equals the sum of its positive divisors excluding itself. Example: `28 = 1 + 2 + 4 + 7 + 14`.

| Input | Output | Why |
|---|---|---|
| `n = 6` | `true` | 1 + 2 + 3 |
| `n = 28` | `true` | 1+2+4+7+14 |
| `n = 15` | `false` | 1+3+5 = 9 |
| `n = 1` | `false` | no proper divisors; sum 0 |

**Constraints:** `1 ≤ n ≤ 10⁸`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — all i < n | test every i from 1 to n−1 | O(n) | O(1) |
| Optimal — √n pairs | sum i and n/i for i ≤ √n | O(√n) | O(1) |

---

## 3. Brute — all i < n

**Intuition.** Add every `i < n` that divides `n`. Correct, but 10⁸ iterations is too slow at the top of the range.

```python
def is_perfect_brute(n):
    return n > 1 and sum(i for i in range(1, n) if n % i == 0) == n
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Optimal — √n pairs

**Intuition.** If `i` divides `n`, so does `n / i`, and one of the two is always ≤ √n. Looping `i` up to √n therefore finds every divisor. Start the sum at 1 (always a proper divisor for n > 1) and loop from 2, so `n` itself is never added.

**Algorithm**

1. If `n == 1` return false.
2. `s = 1`.
3. For `i = 2` while `i * i ≤ n`: if `n % i == 0`: `s += i`; if `i != n / i`, `s += n / i`.
4. Return `s == n`.

**Dry run** — `n = 28`, √28 ≈ 5.3

| i | divides? | add | s |
|---|---|---|---|
| — | — | 1 | 1 |
| 2 | yes | 2 + 14 | 17 |
| 3 | no | | 17 |
| 4 | yes | 4 + 7 | 28 |
| 5 | no | | 28 |

`s == 28` → **true**.

**C++**
```cpp
bool isPerfect(int n) {
    if (n == 1) return false;
    long long s = 1;
    for (long long i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            s += i;
            if (i != n / i) s += n / i;
        }
    }
    return s == n;
}
```

**Java**
```java
static boolean isPerfect(int n) {
    if (n == 1) return false;
    long s = 1;
    for (long i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            s += i;
            if (i != n / i) s += n / i;
        }
    }
    return s == n;
}
```

**Python**
```python
def is_perfect(n):
    if n == 1:
        return False
    s, i = 1, 2
    while i * i <= n:
        if n % i == 0:
            s += i
            if i != n // i:
                s += n // i
        i += 1
    return s == n
```

**Complexity:** time **O(√n)**, space **O(1)** — the loop stops at √n; `i * i ≤ n` avoids floating `sqrt`.

---

## Edge cases

- `n = 1` → false. Its only divisor is itself.
- Perfect squares: don't add `√n` twice (`16`: 4 is paired with itself).
- Writing `i * i` in 32-bit int can overflow near `INT_MAX`; use a 64-bit `i`.

---

## Common mistakes

1. Including `n` itself in the sum, by starting with `s = 1 + n` or looping from `i = 1` and adding `n / 1`.
2. Double-counting the square root.
3. Using `i <= sqrt(n)` with floating point, which can be off by one for large perfect squares.

---

## Follow-ups

1. Classify `n` as deficient, perfect, or abundant.
2. All perfect numbers below 10⁸?

<details><summary>Answer sketches</summary>

**#1:** Compare the proper-divisor sum `s` with `n`: less, equal, greater.

**#2:** 6, 28, 496, 8128, 33 550 336. They're Euclid–Euler numbers `2^(p−1)(2^p − 1)` with `2^p − 1` prime.
</details>

---

## Flashcards

**Why does divisor search stop at √n?** #flashcard
Divisors pair as (i, n/i) and one member of each pair is ≤ √n.

**Perfect-square pitfall in divisor sums?** #flashcard
When i = n/i, add it once.

**First four perfect numbers?** #flashcard
6, 28, 496, 8128.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
