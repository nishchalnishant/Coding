---
module: striver/28-dynamic-programming
lesson: 39
topic: Longest palindromic subsequence
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-palindromic-subsequence?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings, lcs, palindrome]
---
# 39. Longest palindromic subsequence

← [Longest common substring](38-longest-common-substring.md) · [Part 28 index](README.md) · Next → [Minimum insertions to make string palindrome](40-minimum-insertions-to-make-string-palindrome.md)

> [!abstract] Problem at a glance
> **Task:** Length of the longest subsequence of `s` that is a palindrome.
> **Key insight:** **LPS(s) = LCS(s, reverse(s))**. A palindromic subsequence reads the same both ways, so it is common to `s` and its reverse. The direct interval form: `dp[i][j] = 2 + dp[i+1][j−1]` if `s[i] == s[j]`, else `max(dp[i+1][j], dp[i][j−1])`.
> **Difficulty:** Medium · **Pattern:** LCS with reverse / interval DP · **Also on:** LC 516
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-palindromic-subsequence?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Interval DP dp[i][j]](#3-interval-dp-dpij) · [4. LCS(s, reverse(s)), two rows](#4-lcss-reverses-two-rows) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `s`, return the length of its longest palindromic subsequence.

| Input | Output | Why |
|---|---|---|
| `"bbbab"` | `4` | bbbb |
| `"cbbd"` | `2` | bb |
| `"bbabcbcab"` | `7` | babcbab |

**Constraints:** `1 ≤ |s| ≤ 1000`, lowercase.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Interval DP dp[i][j] | ends match → 2 + inside | O(n²) | O(n²) |
| LCS(s, reverse(s)), two rows | reuse LCS | O(n²) | O(n) |

> [!tip] Interview angle
> Lead with the reduction to LCS (one line, reuses code). Then show the interval version, which generalises to palindromic-substring problems and partitioning.

---

## 3. Interval DP dp[i][j]

**Intuition.** Fill by increasing length or by `i` descending. `dp[i][i] = 1`.

```python
def lps_interval(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            dp[i][j] = 2 + dp[i + 1][j - 1] if s[i] == s[j] else max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 4. LCS(s, reverse(s)), two rows

**Intuition.** Reverse `s` and run the space-optimised LCS.

**Algorithm**

1. `t = reverse(s)`.
2. Two-row LCS of `s`, `t`.
3. Return `prev[n]`.

**Dry run** — "bbbab" vs "babbb": LCS "bbbb" → 4.

**C++**
```cpp
int longestPalindromeSubseq(string s) {
    string t(s.rbegin(), s.rend());
    int n = s.size();
    vector<int> prev(n + 1, 0), cur(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++)
            cur[j] = s[i - 1] == t[j - 1] ? prev[j - 1] + 1 : max(prev[j], cur[j - 1]);
        prev = cur;
    }
    return prev[n];
}
```

**Java**
```java
static int longestPalindromeSubseq(String s) {
    String t = new StringBuilder(s).reverse().toString();
    int n = s.length();
    int[] prev = new int[n + 1], cur = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++)
            cur[j] = s.charAt(i - 1) == t.charAt(j - 1) ? prev[j - 1] + 1 : Math.max(prev[j], cur[j - 1]);
        int[] tmp = prev; prev = cur; cur = tmp;
    }
    return prev[n];
}
```

**Python**
```python
def longest_palindrome_subseq(s):
    t, n = s[::-1], len(s)
    prev = [0] * (n + 1)
    for c in s:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            cur[j] = prev[j - 1] + 1 if c == t[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]
```

**Complexity:** time **O(n²)**, space **O(n)** — one LCS, O(n) memory.

---

## Edge cases

- Single character: 1.
- All distinct: 1.

---

## Common mistakes

1. Confusing this with the longest palindromic **substring** (LC 5, expand-around-centre).
2. Interval fill order: `dp[i+1][…]` must be ready, so loop `i` downward.

---

## Follow-ups

1. Minimum insertions to make a palindrome?
2. Longest palindromic substring?

<details><summary>Answer sketches</summary>

**#1:** Next problem: `n − LPS`.

**#2:** Expand around 2n−1 centres in O(n²), or Manacher in O(n).
</details>

---

## Flashcards

**LPS reduction?** #flashcard
LCS(s, reverse(s)).

**LPS interval recurrence?** #flashcard
Equal ends → 2 + dp[i+1][j−1]; else max(dp[i+1][j], dp[i][j−1]).

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
