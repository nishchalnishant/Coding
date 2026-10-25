---
module: striver-a2z/12-basic-recursion
lesson: 11
topic: Sum of Digits in a Given Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/sum-of-digits-in-a-given-number?category=basic-recursion&source=strivers-a2z-dsa-sheet
tags: [striver, basic-recursion, recursion, math, digits]
---
# 11. Sum of Digits in a Given Number

← [Check if the Array is Sorted](10-check-if-the-array-is-sorted-recursive.md) · [Part 12 index](README.md) · Next → [Fibonacci Number](12-fibonacci-number.md)

> [!abstract] Problem at a glance
> **Task:** Return the sum of the decimal digits of the non-negative integer `num`, using recursion.
> **Key insight:** Peel off the last digit: `f(n) = n % 10 + f(n / 10)`, `f(0) = 0`. The depth is the digit count, ⌊log₁₀ n⌋ + 1.
> **Difficulty:** Easy · **Pattern:** Digit recursion
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sum-of-digits-in-a-given-number?category=basic-recursion&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Via string](#3-via-string) · [4. Optimal — % 10 recursion](#4-optimal---10-recursion) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `num`, return the sum of its digits.

| Input | Output | Why |
|---|---|---|
| `num = 529` | `16` | 5 + 2 + 9 |
| `num = 0` | `0` |  |
| `num = 1000` | `1` |  |

**Constraints:** `0 ≤ num ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Via string | sum of int(c) for c in str(num) | O(d) | O(d) |
| Optimal — % 10 recursion | n % 10 + f(n // 10) | O(d) = O(log n) | O(log n) stack |

---

## 3. Via string

**Intuition.** Convert to text and add the digit values.

```python
def digits_str(num):
    return sum(int(c) for c in str(num))
```

**Complexity:** time **O(d)**, space **O(d)**.

---

## 4. Optimal — % 10 recursion

**Intuition.** `n % 10` is the last digit and `n / 10` drops it. Each call removes one digit until 0.

**Algorithm**

1. If `n == 0` return 0.
2. Return `n % 10 + f(n / 10)`.

**Dry run** — `529`: 9 + f(52) = 9 + 2 + f(5) = 9 + 2 + 5 + f(0) = 16.

**C++**
```cpp
int sumOfDigits(int num) {
    if (num == 0) return 0;
    return num % 10 + sumOfDigits(num / 10);
}
```

**Java**
```java
static int sumOfDigits(int num) {
    if (num == 0) return 0;
    return num % 10 + sumOfDigits(num / 10);
}
```

**Python**
```python
def sum_of_digits(num):
    if num == 0:
        return 0
    return num % 10 + sum_of_digits(num // 10)
```

**Complexity:** time **O(d) = O(log n)**, space **O(log n) stack**.

---

## Edge cases

- 0 → 0.
- Trailing zeros contribute 0.

---

## Common mistakes

1. Python `/` instead of `//`: float division never reaches 0 cleanly.
2. Negative input: `%` signs differ by language, so take `abs` first if negatives are allowed.

---

## Follow-ups

1. Repeat the digit sum until one digit remains (LC 258, Add Digits).
2. Count the digits recursively.

<details><summary>Answer sketches</summary>

**#1:** Digital root: `0 if n == 0 else 1 + (n − 1) % 9`, O(1). The recursive version is `f(n) = n if n < 10 else f(digitSum(n))`.

**#2:** `1 + f(n / 10)` for `n ≥ 10`, else 1.
</details>

---

## Flashcards

**Digit-sum recursion?** #flashcard
f(n) = n % 10 + f(n / 10), f(0) = 0.

**Digital root O(1)?** #flashcard
1 + (n − 1) % 9 for n > 0.

**Recursion depth of digit recursion?** #flashcard
Number of digits, O(log₁₀ n).

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
