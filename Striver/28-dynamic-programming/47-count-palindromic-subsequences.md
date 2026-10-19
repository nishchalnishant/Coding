---
module: striver/28-dynamic-programming
lesson: 47
topic: Count palindromic subsequences
difficulty: Hard
source: https://takeuforward.org/learning/dsa/count-palindromic-subsequences?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings, interval, palindrome]
---
# 47. Count palindromic subsequences

← [Word break](46-word-break.md) · [Part 28 index](README.md) · Next → [Matrix chain multiplication](48-matrix-chain-multiplication.md)

> [!abstract] Problem at a glance
> **Task:** Count the non-empty palindromic subsequences (by index set) of `s`, modulo 10⁹+7.
> **Key insight:** Interval DP with inclusion–exclusion: `dp[i][j] = dp[i+1][j] + dp[i][j−1] − dp[i+1][j−1]` counts subsequences avoiding at least one end. If `s[i] == s[j]`, add `dp[i+1][j−1] + 1` (wrap any inner palindrome, or the empty one, with the matching ends). Combined: equal ends → `dp[i+1][j] + dp[i][j−1] + 1`.
> **Difficulty:** Hard · **Pattern:** Interval DP + inclusion–exclusion
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-palindromic-subsequences?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized interval recursion](#3-memoized-interval-recursion) · [4. Bottom-up interval table](#4-bottom-up-interval-table) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `s`, return the number of palindromic subsequences (not necessarily distinct as strings; different index sets count separately), modulo 10⁹+7.

| Input | Output | Why |
|---|---|---|
| `"abcd"` | `4` | each single character |
| `"aab"` | `4` | a, a, b, aa |
| `"aaa"` | `7` | all 2³ − 1 non-empty subsets |

**Constraints:** `1 ≤ |s| ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized interval recursion | inclusion–exclusion on (i, j) | O(n²) | O(n²) |
| Bottom-up interval table | i descending, j ascending | O(n²) | O(n²) |

> [!tip] Interview angle
> Derive the formula with a Venn diagram: "without `s[i]`" plus "without `s[j]`" double-counts "without both". When the ends match, the extra term is every inner palindrome wrapped plus the pair itself. Handle a negative intermediate under the modulus.

---

## 3. Memoized interval recursion

**Intuition.** `f(i, j)`: `i > j` → 0; `i == j` → 1; equal ends → `f(i+1, j) + f(i, j−1) + 1`; else `f(i+1, j) + f(i, j−1) − f(i+1, j−1)`.

```python
def cps_memo(s):
    MOD = 10**9 + 7
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        if s[i] == s[j]:
            return (f(i + 1, j) + f(i, j - 1) + 1) % MOD
        return (f(i + 1, j) + f(i, j - 1) - f(i + 1, j - 1)) % MOD
    return f(0, len(s) - 1)
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 4. Bottom-up interval table

**Intuition.** Fill `i` from `n−1` down so `dp[i+1][…]` is ready. Add `MOD` before taking `%` to keep values non-negative.

**Algorithm**

1. `dp[i][i] = 1`.
2. For `i = n−2..0`, `j = i+1..n−1`: apply the equal / unequal formula.
3. Return `dp[0][n−1]`.

**Dry run** — "aab": dp[0][1] = 1+1+1 = 3, dp[1][2] = 2, dp[0][2] = 3 + 2 − 1 = 4.

**C++**
```cpp
int countPS(string s) {
    const long long MOD = 1e9 + 7;
    int n = s.size();
    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    for (int i = n - 1; i >= 0; i--) {
        dp[i][i] = 1;
        for (int j = i + 1; j < n; j++) {
            long long inner = i + 1 <= j - 1 ? dp[i + 1][j - 1] : 0;
            if (s[i] == s[j]) dp[i][j] = (dp[i + 1][j] + dp[i][j - 1] + 1) % MOD;
            else dp[i][j] = ((dp[i + 1][j] + dp[i][j - 1] - inner) % MOD + MOD) % MOD;
        }
    }
    return (int)dp[0][n - 1];
}
```

**Java**
```java
static int countPS(String s) {
    final long MOD = 1_000_000_007L;
    int n = s.length();
    long[][] dp = new long[n][n];
    for (int i = n - 1; i >= 0; i--) {
        dp[i][i] = 1;
        for (int j = i + 1; j < n; j++) {
            long inner = i + 1 <= j - 1 ? dp[i + 1][j - 1] : 0;
            if (s.charAt(i) == s.charAt(j)) dp[i][j] = (dp[i + 1][j] + dp[i][j - 1] + 1) % MOD;
            else dp[i][j] = ((dp[i + 1][j] + dp[i][j - 1] - inner) % MOD + MOD) % MOD;
        }
    }
    return (int) dp[0][n - 1];
}
```

**Python**
```python
def count_ps(s):
    MOD = 10**9 + 7
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = (dp[i + 1][j] + dp[i][j - 1] + 1) % MOD
            else:
                dp[i][j] = (dp[i + 1][j] + dp[i][j - 1] - dp[i + 1][j - 1]) % MOD
    return dp[0][n - 1]
```

**Complexity:** time **O(n²)**, space **O(n²)** — n²/2 cells, O(1) each.

---

## Edge cases

- Single character: 1.
- All equal: 2ⁿ − 1.

---

## Common mistakes

1. Negative values after subtraction under a modulus.
2. Reading `dp[i+1][j−1]` when `i + 1 > j − 1` (treat it as 0).

---

## Follow-ups

1. Distinct palindromic subsequences as strings (LC 730)?
2. Count palindromic substrings (LC 647)?

<details><summary>Answer sketches</summary>

**#1:** Much harder: track the next/previous occurrence of each character inside the interval.

**#2:** Expand around centres in O(n²).
</details>

---

## Flashcards

**Count PS, equal ends?** #flashcard
dp[i+1][j] + dp[i][j−1] + 1.

**Count PS, unequal ends?** #flashcard
dp[i+1][j] + dp[i][j−1] − dp[i+1][j−1].

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
