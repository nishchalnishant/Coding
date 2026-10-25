---
module: striver-a2z/28-dynamic-programming
lesson: 43
topic: Distinct subsequences
difficulty: Hard
source: https://takeuforward.org/learning/dsa/distinct-subsequences?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings, counting]
---
# 43. Distinct subsequences

← [Shortest common supersequence](42-shortest-common-supersequence.md) · [Part 28 index](README.md) · Next → [Edit distance](44-edit-distance.md)

> [!abstract] Problem at a glance
> **Task:** Count the ways `t` occurs as a subsequence of `s`.
> **Key insight:** `dp[i][j]` = ways to form `t[0..j)` from `s[0..i)`. If `s[i−1] == t[j−1]`: use it (`dp[i−1][j−1]`) + skip it (`dp[i−1][j]`). Else skip only. Base: `dp[·][0] = 1` (the empty `t` is formed once). In 1D, iterate `j` **descending**, like 0/1 knapsack.
> **Difficulty:** Hard · **Pattern:** Two-string counting DP · **Also on:** LC 115
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/distinct-subsequences?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized f(i, j)](#3-memoized-fi-j) · [4. 1D DP, j descending](#4-1d-dp-j-descending) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given strings `s` and `t`, return the number of distinct subsequences of `s` that equal `t` (as index sets). The answer fits in a 32-bit signed integer.

| Input | Output | Why |
|---|---|---|
| `"rabbbit", "rabbit"` | `3` | choose which b to drop |
| `"babgbag", "bag"` | `5` |  |

**Constraints:** `1 ≤ |s|, |t| ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized f(i, j) | take-if-match + skip | O(n·m) | O(n·m) |
| 1D DP, j descending | dp[j] += dp[j−1] on match | O(n·m) | O(m) |

> [!tip] Interview angle
> Spell out the base cases: `t` empty → 1; `s` empty with non-empty `t` → 0. Overflow: intermediate cells can exceed 32 bits even though the final answer doesn't. Unsigned 64-bit arithmetic wraps mod 2⁶⁴ but stays exact for the final value, because only additions are involved. (Striver's version uses mod 10⁹+7.)

---

## 3. Memoized f(i, j)

**Intuition.** `f(i, j)`: `j == m` → 1; `i == n` → 0; else `f(i+1, j) + (s[i] == t[j] ? f(i+1, j+1) : 0)`.

```python
def ds_memo(s, t):
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if j == len(t):
            return 1
        if i == len(s):
            return 0
        r = f(i + 1, j)
        if s[i] == t[j]:
            r += f(i + 1, j + 1)
        return r
    return f(0, 0)
```

**Complexity:** time **O(n·m)**, space **O(n·m)**.

---

## 4. 1D DP, j descending

**Intuition.** `dp[j]` = ways to form `t[0..j)` so far. For each character of `s`, update `j` from `m` down so `dp[j−1]` is the old value.

**Algorithm**

1. `dp = [1, 0, …, 0]` (size m+1).
2. For each `c` in `s`: for `j = m..1`: if `c == t[j−1]`: `dp[j] += dp[j−1]`.
3. Return `dp[m]`.

**Dry run** — "babgbag" / "bag": dp over b,a,b,g,b,a,g ends with dp[3] = 5.

**C++**
```cpp
int numDistinct(string s, string t) {
    int m = t.size();
    vector<unsigned long long> dp(m + 1, 0);
    dp[0] = 1;
    for (char c : s)
        for (int j = m; j >= 1; j--)
            if (c == t[j - 1]) dp[j] += dp[j - 1];
    return (int)dp[m];
}
```

**Java**
```java
static int numDistinct(String s, String t) {
    int m = t.length();
    long[] dp = new long[m + 1];
    dp[0] = 1;
    for (char c : s.toCharArray())
        for (int j = m; j >= 1; j--)
            if (c == t.charAt(j - 1)) dp[j] += dp[j - 1];
    return (int) dp[m];
}
```

**Python**
```python
def num_distinct(s, t):
    m = len(t)
    dp = [1] + [0] * m
    for c in s:
        for j in range(m, 0, -1):
            if c == t[j - 1]:
                dp[j] += dp[j - 1]
    return dp[m]
```

**Complexity:** time **O(n·m)**, space **O(m)** — n·m additions, one row.

---

## Edge cases

- `t` empty: 1.
- `|t| > |s|`: 0.

---

## Common mistakes

1. Ascending `j` in 1D (reuses the same `s` character twice).
2. Base `dp[0] = 0`.

---

## Follow-ups

1. Count distinct subsequences of s (LC 940)?
2. Mod variant?

<details><summary>Answer sketches</summary>

**#1:** `dp[i] = 2·dp[i−1] − dp[last[c]−1]`.

**#2:** Add `% MOD` to each update.
</details>

---

## Flashcards

**Distinct subsequences match transition?** #flashcard
use (diag) + skip (up).

**Base case?** #flashcard
dp[·][0] = 1.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
