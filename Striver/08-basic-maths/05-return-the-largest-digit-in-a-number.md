---
module: striver/08-basic-maths
lesson: 5
topic: Return the Largest Digit in a Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/return-the-largest-digit-in-a-number?category=basic-maths&source=strivers-a2z-dsa-sheet
tags: [striver, basic-maths, digits]
---
# 5. Return the Largest Digit in a Number

← [Palindrome Number](04-palindrome-number.md) · [Part 8 index](README.md) · Next → [Factorial of a Given Number](06-factorial-of-a-given-number.md)

> [!abstract] Problem at a glance
> **Task:** Return the maximum digit of `n`.
> **Key insight:** Use the digit loop with a running max. Stop early once you see a 9.
> **Difficulty:** Easy · **Pattern:** Digit loop + running max
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/return-the-largest-digit-in-a-number?category=basic-maths&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — string max](#3-brute--string-max) · [4. Optimal — digit loop](#4-optimal--digit-loop) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer `n`, return its largest digit.

| Input | Output | Why |
|---|---|---|
| `n = 25` | `5` |  |
| `n = 99` | `9` |  |
| `n = 0` | `0` | loop never runs; the initial max 0 is correct |
| `n = 1203` | `3` |  |

**Constraints:** `0 ≤ n ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — string max | `max(str(n))` | O(d) | O(d) |
| Optimal — digit loop | `best = max(best, n % 10)` | O(log₁₀ n) | O(1) |

---

## 3. Brute — string max

**Intuition.** Characters `'0'..'9'` sort in the same order as their values, so the max character is the max digit.

```python
def largest_digit_str(n):
    return int(max(str(n)))
```

**Complexity:** time **O(d)**, space **O(d)**.

---

## 4. Optimal — digit loop

**Intuition.** Keep a running maximum over the digits. Starting at 0 makes `n = 0` correct with no special case, because 0 is the smallest possible digit.

**Algorithm**

1. `best = 0`.
2. While `n > 0`: `best = max(best, n % 10)`; if `best == 9`, break; `n //= 10`.
3. Return `best`.

**Dry run** — `n = 1203`: digits 3, 0, 2, 1 → best goes 3, 3, 3, 3 → **3**.

**C++**
```cpp
int largestDigit(int n) {
    int best = 0;
    while (n > 0) {
        best = max(best, n % 10);
        if (best == 9) break;
        n /= 10;
    }
    return best;
}
```

**Java**
```java
static int largestDigit(int n) {
    int best = 0;
    while (n > 0) {
        best = Math.max(best, n % 10);
        if (best == 9) break;
        n /= 10;
    }
    return best;
}
```

**Python**
```python
def largest_digit(n):
    best = 0
    while n > 0:
        best = max(best, n % 10)
        if best == 9:
            break
        n //= 10
    return best
```

**Complexity:** time **O(log₁₀ n)**, space **O(1)** — the early exit on 9 doesn't change the worst case.

---

## Edge cases

- `n = 0` → 0.
- All digits equal (`7777`) → 7.
- Contains 9 → you can exit immediately.

---

## Common mistakes

1. Initialising `best = -1` and then returning -1 for `n = 0`.
2. Comparing the remaining `n` instead of the digit `n % 10`.

---

## Follow-ups

1. Return the smallest digit.
2. Largest number you can form by rearranging the digits.

<details><summary>Answer sketches</summary>

**#1:** Initialise `best = 9` and special-case `n = 0` → 0, since the loop won't run.

**#2:** Count the digits 0–9 into a size-10 array, then emit them from 9 down to 0. O(d), a counting sort.
</details>

---

## Flashcards

**Initial value for largest digit, and why?** #flashcard
0. It's the smallest digit, so it's safe, and it also covers n = 0.

**Early exit for largest digit?** #flashcard
Stop as soon as you see 9; nothing can beat it.

**Interview track →** [Math & number theory](../../02-algorithms/18-math-and-number-theory.md) · [Concept: basic maths](../07-concept-basics/01-basic-maths.md)
