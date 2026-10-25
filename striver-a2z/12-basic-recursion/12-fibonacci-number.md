---
module: striver-a2z/12-basic-recursion
lesson: 12
topic: Fibonacci Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/fibonacci-number?category=basic-recursion&source=strivers-a2z-dsa-sheet
tags: [striver, basic-recursion, recursion, dp, memoization]
---
# 12. Fibonacci Number

← [Sum of Digits in a Given Number](11-sum-of-digits.md) · [Part 12 index](README.md) · Next → [Part 13: Sorting](../13-sorting/README.md)

> [!abstract] Problem at a glance
> **Task:** Return the `n`-th Fibonacci number, with `F(0) = 0` and `F(1) = 1`.
> **Key insight:** Naive `F(n−1) + F(n−2)` recomputes the same subproblems, which is O(φⁿ). Memoising makes it O(n), and keeping only the last two values makes it O(1) space. This is the gateway to DP.
> **Difficulty:** Easy · **Pattern:** Multiple recursion → memoisation → DP · **Also on:** 509
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/fibonacci-number?category=basic-recursion&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — plain recursion](#3-brute--plain-recursion) · [4. Better — memoised recursion (top-down DP)](#4-better--memoised-recursion-top-down-dp) · [5. Optimal — bottom-up, two variables](#5-optimal--bottom-up-two-variables) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`F(0) = 0`, `F(1) = 1`, `F(n) = F(n − 1) + F(n − 2)` for `n > 1`. Given `n`, return `F(n)`.

| Input | Output | Why |
|---|---|---|
| `n = 2` | `1` |  |
| `n = 5` | `5` | 0 1 1 2 3 5 |
| `n = 0` | `0` |  |

**Constraints:** `0 ≤ n ≤ 30` (LeetCode). With 64-bit integers, `F(92)` is the largest that fits.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — plain recursion | F(n−1) + F(n−2) | O(φⁿ) ≈ O(1.618ⁿ) | O(n) stack |
| Better — memoised recursion (top-down DP) | cache F(k) the first time | O(n) | O(n) memo + O(n) stack |
| Optimal — bottom-up, two variables | roll (a, b) → (b, a + b) | O(n) | O(1) |

> [!tip] Interview angle
> Write the two-call recursion, draw the tree to show the repeated `F(n−2)`, then memoise, then go to two variables. That sequence is the whole DP story; [Part 28](../28-dynamic-programming/README.md) uses it everywhere.

---

## 3. Brute — plain recursion

**Intuition.** A direct translation of the definition. The recursion tree has ~φⁿ nodes because every value below n is recomputed many times. F(40) takes over 10⁸ calls.

```python
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
```

**Complexity:** time **O(φⁿ) ≈ O(1.618ⁿ)**, space **O(n) stack**.

---

## 4. Better — memoised recursion (top-down DP)

**Intuition.** There are only n + 1 distinct subproblems. Store each one when it's first computed, and every later call is O(1).

```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

**Complexity:** time **O(n)**, space **O(n) memo + O(n) stack**.

---

## 5. Optimal — bottom-up, two variables

**Intuition.** `F(k)` depends only on the previous two values, so fill from the bottom, keeping just `prev2` and `prev1`.

**Algorithm**

1. If `n <= 1` return n.
2. `a, b = 0, 1`.
3. Repeat `n − 1` times: `a, b = b, a + b`.
4. Return `b`.

**Dry run** — n = 5: (0, 1) → (1, 1) → (1, 2) → (2, 3) → (3, 5) → **5**.

**O(log n):** matrix power `[[1,1],[1,0]]ⁿ` or fast doubling (`F(2k) = F(k)·(2F(k+1) − F(k))`, `F(2k+1) = F(k)² + F(k+1)²`). It's worth a mention for `n ~ 10¹⁸ mod p`.

**C++**
```cpp
int fib(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}
```

**Java**
```java
static int fib(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}
```

**Python**
```python
def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- n = 0 and n = 1 are both base cases.
- `int` overflows after F(46); `long` after F(92).

---

## Common mistakes

1. Only `n == 1` as the base case: `F(0)` recurses into negatives.
2. A mutable default `memo={}` in Python that persists between calls. It happens to be harmless here, but it's a classic bug.
3. Calling naive recursion O(2ⁿ) *space*. The space is the depth, O(n).

---

## Follow-ups

1. Climbing Stairs (LC 70): 1 or 2 steps.
2. F(n) mod 1e9+7 for n ≤ 10¹⁸.
3. Tribonacci (LC 1137).

<details><summary>Answer sketches</summary>

**#1:** `ways(n) = ways(n−1) + ways(n−2)`, i.e. Fibonacci shifted by one.

**#2:** Matrix exponentiation or fast doubling, O(log n).

**#3:** Roll three variables.
</details>

---

## Flashcards

**Naive fib time and space?** #flashcard
O(φⁿ) time, O(n) stack.

**Fib in O(1) space?** #flashcard
Roll (a, b) → (b, a + b).

**Fib in O(log n)?** #flashcard
Matrix power of [[1,1],[1,0]] or fast doubling.

**Largest Fibonacci number in signed 64-bit?** #flashcard
F(92).

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
