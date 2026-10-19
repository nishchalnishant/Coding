---
module: striver/08-basic-maths
lesson: 1
topic: Count All Digits of a Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/count-all-digits-of-a-number?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, digits]
---
# 1. Count All Digits of a Number

← [Part 8 index](README.md) · Next → [Count Number of Odd Digits in a Number](02-count-number-of-odd-digits-in-a-number.md)

> [!abstract] Problem at a glance
> **Task:** Return how many digits the non-negative integer `n` has.
> **Key insight:** Each `n //= 10` strips one digit, so the loop runs once per digit; `0` has one digit.
> **Difficulty:** Easy · **Pattern:** Digit loop
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-all-digits-of-a-number?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — convert to string](#3-brute--convert-to-string) · [4. Better — digit loop](#4-better--digit-loop) · [5. Optimal — logarithm](#5-optimal--logarithm) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `n`, return the number of digits in its decimal representation.

| Input | Output | Why |
|---|---|---|
| `n = 4` | `1` | single digit |
| `n = 12345` | `5` | five digits |
| `n = 0` | `1` | zero is written with one digit |

**Constraints:** `0 ≤ n ≤ 10⁹` (fits in a 32-bit int).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — convert to string | `len(str(n))` | O(d) | O(d) |
| Better — digit loop | strip digits with `//10` | O(log₁₀ n) | O(1) |
| Optimal — logarithm | `⌊log₁₀ n⌋ + 1` | O(1) | O(1) |

> [!tip] Interview angle
> Say up front that `0` is a special case. That one sentence shows you test boundaries before coding.

---

## 3. Brute — convert to string

**Intuition.** The string form has exactly one character per digit. It works, but it allocates a string and hides the arithmetic the interviewer wants to see.

```python
def count_digits_str(n):
    return len(str(n))
```

**Complexity:** time **O(d)**, space **O(d)**.

---

## 4. Better — digit loop

**Intuition.** `n % 10` is the last digit and `n // 10` removes it. Count how many times you can remove a digit before `n` becomes 0.

**Algorithm**

1. If `n == 0` return 1.
2. `cnt = 0`; while `n > 0`: `cnt += 1`, `n //= 10`.
3. Return `cnt`.

**Dry run** — `n = 12345`

| iter | n before | n after | cnt |
|---|---|---|---|
| 1 | 12345 | 1234 | 1 |
| 2 | 1234 | 123 | 2 |
| 3 | 123 | 12 | 3 |
| 4 | 12 | 1 | 4 |
| 5 | 1 | 0 | 5 |

```python
def count_digits_loop(n):
    if n == 0:
        return 1
    cnt = 0
    while n > 0:
        cnt += 1
        n //= 10
    return cnt
```

**Complexity:** time **O(log₁₀ n)**, space **O(1)**.

---

## 5. Optimal — logarithm

**Intuition.** A number with `d` digits satisfies `10^(d-1) ≤ n < 10^d`. Taking log₁₀ gives `d - 1 ≤ log₁₀ n < d`, so `d = ⌊log₁₀ n⌋ + 1`.

> [!warning] Floating point
> `log10` works for 32-bit inputs. For values near `10^15` and above, rounding can make `log10(999…9)` come out as an exact integer. In an interview, give the loop as the safe answer and mention the log trick as an extra.

**C++**
```cpp
int countDigits(int n) {
    if (n == 0) return 1;
    return (int)log10((double)n) + 1;
}
```

**Java**
```java
static int countDigits(int n) {
    if (n == 0) return 1;
    return (int) Math.log10(n) + 1;
}
```

**Python**
```python
import math

def count_digits(n):
    if n == 0:
        return 1
    return int(math.log10(n)) + 1
```

**Complexity:** time **O(1)**, space **O(1)** — one log call; correct for every 32-bit input.

---

## Edge cases

- `n = 0` → 1, not 0. The loop alone returns 0.
- Powers of ten (`10`, `100`, `10⁹`) are where the log formula is most likely to break. Test them.
- Negative input: count the digits of `abs(n)`; the sign is not a digit.

---

## Common mistakes

1. Forgetting the `n == 0` case.
2. Using `/` instead of `//` in Python, which turns `n` into a float that never reaches 0 exactly.
3. Mutating the caller's variable in a language where it matters. Copy `n` first if you need the original later.

---

## Follow-ups

1. Count only the digits that divide `n` evenly.
2. Count digits of `n` in base `b`.

<details><summary>Answer sketches</summary>

**#1:** Keep the original in `orig`; in the loop, `if d != 0 and orig % d == 0: cnt += 1`.

**#2:** Same loop with `n //= b`, or `⌊log_b n⌋ + 1`.
</details>

---

## Flashcards

**Why is the digit loop O(log₁₀ n)?** #flashcard
Each iteration divides `n` by 10, so it runs once per digit, and a number has about log₁₀ n digits.

**Digits of n by formula?** #flashcard
`⌊log₁₀ n⌋ + 1` for n ≥ 1.

**Digit count of 0?** #flashcard
1. Special-case it, because `while n > 0` never runs.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
