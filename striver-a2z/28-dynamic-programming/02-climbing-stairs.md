---
module: striver-a2z/28-dynamic-programming
lesson: 2
topic: Climbing stairs
difficulty: Easy
source: https://takeuforward.org/learning/dsa/climbing-stairs?category=1d-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, 1d-dp, fibonacci]
---
# 2. Climbing stairs

← [Dynamic Programming: From Recursion to Tabulation](01-dp-theory.md) · [Part 28 index](README.md) · Next → [Frog Jump](03-frog-jump.md)

> [!abstract] Problem at a glance
> **Task:** Count the distinct ways to climb `n` steps when each move is 1 or 2 steps.
> **Key insight:** The last move was either a 1-step from `n−1` or a 2-step from `n−2`, so `ways(n) = ways(n−1) + ways(n−2)`, which is Fibonacci. Only the previous two values are ever read, so two variables replace the table.
> **Difficulty:** Easy · **Pattern:** 1D DP: Fibonacci recurrence · **Also on:** LC 70
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/climbing-stairs?category=1d-dp&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Plain recursion](#3-plain-recursion) · [4. Memoization (top-down)](#4-memoization-top-down) · [5. Tabulation with two variables](#5-tabulation-with-two-variables) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

You are at step 0 and want to reach step `n`. Each move climbs 1 or 2 steps. Return the number of distinct move sequences that land exactly on `n`.

| Input | Output | Why |
|---|---|---|
| `n = 2` | `2` | 1+1, 2 |
| `n = 3` | `3` | 1+1+1, 1+2, 2+1 |
| `n = 5` | `8` | ways(4) + ways(3) = 5 + 3 |

**Constraints:** `1 ≤ n ≤ 45` (the answer fits in a 32-bit int).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Plain recursion | f(n) = f(n−1) + f(n−2) | O(2ⁿ) | O(n) |
| Memoization (top-down) | cache f(k) the first time | O(n) | O(n) |
| Tabulation with two variables | iterate bottom-up keeping prev2, prev1 | O(n) | O(1) |

> [!tip] Interview angle
> This is the template for the whole DP part, so narrate all four stages: recurrence → memoization → tabulation → space optimisation. Interviewers often extend it to steps `{1, 2, …, k}` or forbidden steps.

---

## 3. Plain recursion

**Intuition.** Express the answer for `n` in terms of smaller answers. Base cases: `f(0) = 1` (one way to stand still) and `f(1) = 1`. The call tree recomputes the same `f(k)` exponentially often.

```python
def climb_rec(n):
    if n <= 1:
        return 1
    return climb_rec(n - 1) + climb_rec(n - 2)
```

**Complexity:** time **O(2ⁿ)**, space **O(n)**.

---

## 4. Memoization (top-down)

**Intuition.** There are only `n + 1` distinct states. Store each result in `dp[k]` (−1 = unknown) and return it on later calls. Every state is computed once.

```python
def climb_memo(n):
    dp = [-1] * (n + 1)
    def f(k):
        if k <= 1:
            return 1
        if dp[k] != -1:
            return dp[k]
        dp[k] = f(k - 1) + f(k - 2)
        return dp[k]
    return f(n)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 5. Tabulation with two variables

**Intuition.** Fill `dp[0..n]` from the base cases upward: `dp[i] = dp[i−1] + dp[i−2]`. Each entry needs only the two before it, so keep `prev2 = dp[i−2]` and `prev1 = dp[i−1]` and slide them forward.

**Algorithm**

1. `prev2 = 1` (dp[0]), `prev1 = 1` (dp[1]).
2. For `i = 2..n`: `cur = prev1 + prev2`; `prev2 = prev1`; `prev1 = cur`.
3. Return `prev1`.

**Dry run** — n = 5: (prev2, prev1) goes (1,1) → (1,2) → (2,3) → (3,5) → (5,8). Answer 8.

**C++**
```cpp
int climbStairs(int n) {
    int prev2 = 1, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int cur = prev1 + prev2;
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

**Java**
```java
static int climbStairs(int n) {
    int prev2 = 1, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int cur = prev1 + prev2;
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

**Python**
```python
def climb_stairs(n):
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1
```

**Complexity:** time **O(n)**, space **O(1)** — one pass with two variables.

---

## Edge cases

- `n = 1`: exactly one way, and the loop never runs.
- `n = 45`: 1 836 311 903, just under `INT_MAX`; `n = 46` would overflow.
- Defining `f(0) = 1` is what makes `f(2) = 2` come out right.

---

## Common mistakes

1. Base case `f(0) = 0`, which makes every answer wrong.
2. Returning `prev2` instead of `prev1` after the loop.
3. Memo array of size `n` instead of `n + 1`.

---

## Follow-ups

1. Steps can be any of `1..k`.
2. Some steps are broken.
3. `n` up to 10¹⁸, answer mod p.

<details><summary>Answer sketches</summary>

**#1:** `f(n) = Σ_{j=1..k} f(n−j)`. Keep a running window sum to stay O(n).

**#2:** Set `f(i) = 0` for a broken step and keep the same recurrence.

**#3:** Use 2×2 matrix exponentiation of `[[1,1],[1,0]]`, O(log n).
</details>

---

## Flashcards

**Climbing stairs recurrence?** #flashcard
`f(n) = f(n−1) + f(n−2)`, `f(0) = f(1) = 1`.

**Four stages of a DP solution?** #flashcard
Recurrence → memoization → tabulation → space optimisation.

**Why is memoization O(n) here?** #flashcard
There are n + 1 states and each does O(1) work once.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
