---
module: striver/28-dynamic-programming
lesson: 51
topic: Evaluate boolean expression to true
difficulty: Hard
source: https://takeuforward.org/learning/dsa/different-ways-to-evaluate-a-boolean-expression?category=mcm-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, partition-dp, counting]
---
# 51. Evaluate boolean expression to true

← [Burst balloons](50-burst-balloons.md) · [Part 28 index](README.md) · Next → [Palindrome partitioning II](52-palindrome-partitioning-ii.md)

> [!abstract] Problem at a glance
> **Task:** Count the parenthesisations of a `T/F` expression with `& | ^` that evaluate to true, modulo 10⁹+7.
> **Key insight:** Track **both** counts per interval: `T(i, j)` and `F(i, j)`. Splitting at operator `k` combines `(lT, lF) × (rT, rF)` by the truth table: `&` is true only on `lT·rT`; `|` is false only on `lF·rF`; `^` is true on `lT·rF + lF·rT`. True-only DP fails because `^` and `|` need the false counts.
> **Difficulty:** Hard · **Pattern:** Partition DP (two-valued)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/different-ways-to-evaluate-a-boolean-expression?category=mcm-dp&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized f(i, j) → (T, F)](#3-memoized-fi-j--t-f) · [4. Bottom-up T / F tables](#4-bottom-up-t--f-tables) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an expression `s` whose even indices are `T`/`F` and odd indices are `&`, `|`, `^`, count the ways to fully parenthesise it so that it evaluates to `T`. Return the count mod 10⁹+7.

| Input | Output | Why |
|---|---|---|
| `"T|T&F"` | `1` | (T|T)&F = F, T|(T&F) = T |
| `"F|T^F"` | `2` | both groupings give T |
| `"T^F&T"` | `2` |  |

**Constraints:** `1 ≤ |s| ≤ 199`, `|s|` odd.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized f(i, j) → (T, F) | combine by the truth table at each operator | O(n³) | O(n²) |
| Bottom-up T / F tables | i descending over symbols, j ascending | O(n³) | O(n²) |

> [!tip] Interview angle
> Lead with "I need both the true and false counts per interval, because XOR and OR depend on the false side." Splits are only at odd indices. The state can be `(i, j, wantTrue)`, as in Striver, or a pair returned per interval, as here.

---

## 3. Memoized f(i, j) → (T, F)

**Intuition.** The base case is one symbol. Iterate operators `k = i+1, i+3, …, j−1`.

```python
def bool_memo(s):
    MOD = 10**9 + 7
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if i == j:
            return (1, 0) if s[i] == "T" else (0, 1)
        t = fl = 0
        for k in range(i + 1, j, 2):
            lt, lf = f(i, k - 1)
            rt, rf = f(k + 1, j)
            tot = (lt + lf) * (rt + rf)
            if s[k] == "&":
                good = lt * rt
            elif s[k] == "|":
                good = tot - lf * rf
            else:
                good = lt * rf + lf * rt
            t += good
            fl += tot - good
        return t % MOD, fl % MOD
    return f(0, len(s) - 1)[0]
```

**Complexity:** time **O(n³)**, space **O(n²)**.

---

## 4. Bottom-up T / F tables

**Intuition.** Two `n × n` tables. Only even `i`, `j` are symbol positions, so step by 2.

**Algorithm**

1. `T[i][i]`, `F[i][i]` from the symbol.
2. For `i = n−1..0` step −2, `j = i+2..n−1` step 2: for each operator `k`, add `good` to `T[i][j]` and `tot − good` to `F[i][j]`, mod 10⁹+7.
3. Return `T[0][n−1]`.

**Dry run** — "T|T&F": split at `|`: T·(T&F) → (1,0)×(0,1) gives 1 true; split at `&`: (T|T)&F → (1,0)×(0,1) gives 0 true → 1.

**C++**
```cpp
int countWays(string s) {
    const long long MOD = 1e9 + 7;
    int n = s.size();
    vector<vector<long long>> T(n, vector<long long>(n, 0)), F(n, vector<long long>(n, 0));
    for (int i = n - 1; i >= 0; i -= 2) {
        T[i][i] = s[i] == 'T';
        F[i][i] = s[i] == 'F';
        for (int j = i + 2; j < n; j += 2)
            for (int k = i + 1; k < j; k += 2) {
                long long lt = T[i][k - 1], lf = F[i][k - 1], rt = T[k + 1][j], rf = F[k + 1][j];
                long long tot = (lt + lf) % MOD * ((rt + rf) % MOD) % MOD, good;
                if (s[k] == '&') good = lt * rt % MOD;
                else if (s[k] == '|') good = (tot - lf * rf % MOD + MOD) % MOD;
                else good = (lt * rf + lf * rt) % MOD;
                T[i][j] = (T[i][j] + good) % MOD;
                F[i][j] = (F[i][j] + tot - good + MOD) % MOD;
            }
    }
    return (int)T[0][n - 1];
}
```

**Java**
```java
static int countWays(String s) {
    final long MOD = 1_000_000_007L;
    int n = s.length();
    long[][] T = new long[n][n], F = new long[n][n];
    for (int i = n - 1; i >= 0; i -= 2) {
        T[i][i] = s.charAt(i) == 'T' ? 1 : 0;
        F[i][i] = s.charAt(i) == 'F' ? 1 : 0;
        for (int j = i + 2; j < n; j += 2)
            for (int k = i + 1; k < j; k += 2) {
                long lt = T[i][k - 1], lf = F[i][k - 1], rt = T[k + 1][j], rf = F[k + 1][j];
                long tot = (lt + lf) % MOD * ((rt + rf) % MOD) % MOD, good;
                char op = s.charAt(k);
                if (op == '&') good = lt * rt % MOD;
                else if (op == '|') good = (tot - lf * rf % MOD + MOD) % MOD;
                else good = (lt * rf + lf * rt) % MOD;
                T[i][j] = (T[i][j] + good) % MOD;
                F[i][j] = (F[i][j] + tot - good + MOD) % MOD;
            }
    }
    return (int) T[0][n - 1];
}
```

**Python**
```python
def count_ways(s):
    MOD = 10**9 + 7
    n = len(s)
    T = [[0] * n for _ in range(n)]
    F = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -2):
        T[i][i], F[i][i] = int(s[i] == "T"), int(s[i] == "F")
        for j in range(i + 2, n, 2):
            for k in range(i + 1, j, 2):
                lt, lf, rt, rf = T[i][k - 1], F[i][k - 1], T[k + 1][j], F[k + 1][j]
                tot = (lt + lf) * (rt + rf)
                good = lt * rt if s[k] == "&" else tot - lf * rf if s[k] == "|" else lt * rf + lf * rt
                T[i][j] = (T[i][j] + good) % MOD
                F[i][j] = (F[i][j] + tot - good) % MOD
    return T[0][n - 1]
```

**Complexity:** time **O(n³)**, space **O(n²)** — (n/2)² intervals × n/2 operators.

---

## Edge cases

- A single symbol: 1 or 0.
- Large counts (Catalan growth): reduce mod at every step.

---

## Common mistakes

1. Tracking only the true count.
2. Splitting at symbol positions instead of operator positions.
3. A negative value after `tot − good` under the modulus.

---

## Follow-ups

1. Different ways to add parentheses (LC 241)?
2. Count parenthesisations evaluating to false?

<details><summary>Answer sketches</summary>

**#1:** Same split recursion, returning the list of values per interval.

**#2:** Return `F[0][n−1]`.
</details>

---

## Flashcards

**Boolean parenthesisation state?** #flashcard
Per interval: (#true, #false).

**XOR true count?** #flashcard
lT·rF + lF·rT.

**OR true count?** #flashcard
total − lF·rF.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
