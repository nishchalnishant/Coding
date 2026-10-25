---
module: striver-a2z/28-dynamic-programming
lesson: 37
topic: Longest common subsequence
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-common-subsequence?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings, lcs]
---
# 37. Longest common subsequence

← [Number of longest increasing subsequences](36-number-of-longest-increasing-subsequences.md) · [Part 28 index](README.md) · Next → [Longest common substring](38-longest-common-substring.md)

> [!abstract] Problem at a glance
> **Task:** Length of the longest subsequence common to both strings.
> **Key insight:** `dp[i][j]` = LCS of prefixes `a[0..i)` and `b[0..j)`. Characters match → `1 + dp[i−1][j−1]`; else `max(dp[i−1][j], dp[i][j−1])`. Shifting indices by one (row/column 0 = empty prefix) removes the negative-index base cases. **Most of the string DPs below are LCS in disguise.**
> **Difficulty:** Medium · **Pattern:** Two-string DP (LCS) · **Also on:** LC 1143
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-common-subsequence?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized f(i, j)](#3-memoized-fi-j) · [4. Two-row tabulation](#4-two-row-tabulation) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given strings `text1` and `text2`, return the length of their longest common subsequence (0 if none).

| Input | Output | Why |
|---|---|---|
| `"abcde", "ace"` | `3` | ace |
| `"abc", "abc"` | `3` |  |
| `"abc", "def"` | `0` |  |

**Constraints:** `1 ≤ |text1|, |text2| ≤ 1000`, lowercase.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized f(i, j) | match → diagonal, else max of drops | O(n·m) | O(n·m) |
| Two-row tabulation | prev / cur rows over prefixes | O(n·m) | O(m) |

> [!tip] Interview angle
> Write the 1-indexed recurrence with the empty-prefix base row. Then reduce space to two rows. Interviewers often ask you to print the LCS; walk back from `dp[n][m]`.

---

## 3. Memoized f(i, j)

**Intuition.** `f(i, j)` on suffixes from `i`, `j`. Stop when either string is exhausted.

```python
def lcs_memo(a, b):
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)
```

**Complexity:** time **O(n·m)**, space **O(n·m)**.

---

## 4. Two-row tabulation

**Intuition.** `cur[j]` needs `prev[j−1]` (diagonal), `prev[j]` (up) and `cur[j−1]` (left).

**Algorithm**

1. `prev = [0]*(m+1)`.
2. For `i = 1..n`: `cur[0] = 0`; for `j = 1..m`: match → `prev[j−1] + 1`, else `max(prev[j], cur[j−1])`.
3. `prev = cur`; return `prev[m]`.

**Dry run** — "abcde" vs "ace": final row [0,1,2,3] → 3.

**C++**
```cpp
int longestCommonSubsequence(string a, string b) {
    int n = a.size(), m = b.size();
    vector<int> prev(m + 1, 0), cur(m + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++)
            cur[j] = a[i - 1] == b[j - 1] ? prev[j - 1] + 1 : max(prev[j], cur[j - 1]);
        prev = cur;
    }
    return prev[m];
}
```

**Java**
```java
static int longestCommonSubsequence(String a, String b) {
    int n = a.length(), m = b.length();
    int[] prev = new int[m + 1], cur = new int[m + 1];
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++)
            cur[j] = a.charAt(i - 1) == b.charAt(j - 1) ? prev[j - 1] + 1 : Math.max(prev[j], cur[j - 1]);
        int[] t = prev; prev = cur; cur = t;
    }
    return prev[m];
}
```

**Python**
```python
def longest_common_subsequence(a, b):
    m = len(b)
    prev = [0] * (m + 1)
    for ca in a:
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            cur[j] = prev[j - 1] + 1 if ca == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[m]
```

**Complexity:** time **O(n·m)**, space **O(m)** — n·m cells, two rows.

---

## Edge cases

- No common character: 0.
- Identical strings: the length.

---

## Common mistakes

1. Off-by-one between dp index `i` and character `a[i−1]`.
2. Swapping rows by reference in Java without a temporary.

---

## Follow-ups

1. Print the LCS.
2. LCS of three strings?
3. Very long strings, small alphabet?

<details><summary>Answer sketches</summary>

**#1:** From `(n, m)`: on match take the char and go diagonal; else move toward the larger neighbour; reverse.

**#2:** 3D DP, O(n·m·k).

**#3:** Hirschberg gives O(min) space with reconstruction.
</details>

---

## Flashcards

**LCS recurrence?** #flashcard
Match → 1 + dp[i−1][j−1]; else max(dp[i−1][j], dp[i][j−1]).

**Why 1-indexed dp?** #flashcard
Row/column 0 = empty prefix, no negative-index cases.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
