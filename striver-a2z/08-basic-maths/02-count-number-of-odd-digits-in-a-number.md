---
module: striver-a2z/08-basic-maths
lesson: 2
topic: Count Number of Odd Digits in a Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/count-number-of-odd-digits-in-a-number?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, digits]
---
# 2. Count Number of Odd Digits in a Number

← [Count All Digits of a Number](01-count-all-digits-of-a-number.md) · [Part 8 index](README.md) · Next → [Reverse a Number](03-reverse-a-number.md)

> [!abstract] Problem at a glance
> **Task:** Count the digits of `n` that are odd.
> **Key insight:** Use the digit loop and test each digit `d` with `d % 2 == 1`.
> **Difficulty:** Easy · **Pattern:** Digit loop
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-number-of-odd-digits-in-a-number?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — string scan](#3-brute--string-scan) · [4. Optimal — digit loop](#4-optimal--digit-loop) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `n`, return how many of its digits are odd (1, 3, 5, 7, 9).

| Input | Output | Why |
|---|---|---|
| `n = 5` | `1` | 5 is odd |
| `n = 25` | `1` | 2 even, 5 odd |
| `n = 15` | `2` | 1 and 5 |
| `n = 0` | `0` | 0 is even |

**Constraints:** `0 ≤ n ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — string scan | scan characters | O(d) | O(d) |
| Optimal — digit loop | `d = n % 10`; test parity | O(log₁₀ n) | O(1) |

---

## 3. Brute — string scan

**Intuition.** Convert to a string and test each character's integer value.

```python
def count_odd_str(n):
    return sum(1 for ch in str(n) if int(ch) % 2 == 1)
```

**Complexity:** time **O(d)**, space **O(d)**.

---

## 4. Optimal — digit loop

**Intuition.** Peel off digits right to left. Each digit is checked once, and no extra storage is needed.

**Algorithm**

1. `cnt = 0`.
2. While `n > 0`: `d = n % 10`; if `d % 2 == 1`, `cnt += 1`; `n //= 10`.
3. Return `cnt`. For `n = 0` the loop doesn't run and the answer 0 is correct, since 0 is even.

**Dry run** — `n = 1572`

| d | odd? | cnt | n after |
|---|---|---|---|
| 2 | no | 0 | 157 |
| 7 | yes | 1 | 15 |
| 5 | yes | 2 | 1 |
| 1 | yes | 3 | 0 |

**C++**
```cpp
int countOddDigit(int n) {
    int cnt = 0;
    while (n > 0) {
        int d = n % 10;
        if (d % 2 == 1) cnt++;
        n /= 10;
    }
    return cnt;
}
```

**Java**
```java
static int countOddDigit(int n) {
    int cnt = 0;
    while (n > 0) {
        int d = n % 10;
        if (d % 2 == 1) cnt++;
        n /= 10;
    }
    return cnt;
}
```

**Python**
```python
def count_odd_digit(n):
    cnt = 0
    while n > 0:
        d = n % 10
        if d % 2 == 1:
            cnt += 1
        n //= 10
    return cnt
```

**Complexity:** time **O(log₁₀ n)**, space **O(1)**.

---

## Edge cases

- `n = 0` → 0, and here the loop gives the right answer without a special case.
- All-even input → 0.
- Negative `n`: in C++/Java `-7 % 2 == -1`, so `d % 2 == 1` fails. Use `d % 2 != 0` or take `abs(n)` first.

---

## Common mistakes

1. Checking `n % 2` (the parity of the whole number) instead of `d % 2`.
2. In C++/Java, testing negative digits with `== 1`. Prefer `!= 0`, or `(d & 1)`.

---

## Follow-ups

1. Return the sum of the odd digits instead.
2. Count digits that are prime (2, 3, 5, 7).

<details><summary>Answer sketches</summary>

**#1:** Replace `cnt += 1` with `s += d`.

**#2:** Test `d in {2, 3, 5, 7}`. It's a constant-size set, so the cost stays O(1) per digit.
</details>

---

## Flashcards

**Odd test that is safe for negatives in C++?** #flashcard
`d % 2 != 0` or `(d & 1)`. With `d % 2 == 1`, `-3 % 2` is `-1`.

**Does `n = 0` need a special case for counting odd digits?** #flashcard
No. Zero odd digits is the correct answer.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
