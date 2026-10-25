---
module: striver-a2z/28-dynamic-programming
lesson: 42
topic: Shortest common supersequence
difficulty: Hard
source: https://takeuforward.org/learning/dsa/shortest-common-supersequence?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings, lcs, reconstruction]
---
# 42. Shortest common supersequence

← [Minimum insertions or deletions to convert string A to B](41-min-insertions-deletions-a-to-b.md) · [Part 28 index](README.md) · Next → [Distinct subsequences](43-distinct-subsequences.md)

> [!abstract] Problem at a glance
> **Task:** Return a shortest string that has both `a` and `b` as subsequences.
> **Key insight:** Its length is `|a| + |b| − LCS` (shared characters are written once). To **build** it, walk the LCS table back from `(n, m)`: on a match emit the character once and go diagonal; otherwise emit the character of the side you move away from (toward the larger neighbour). Then flush the leftovers and reverse.
> **Difficulty:** Hard · **Pattern:** LCS table reconstruction · **Also on:** LC 1092
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/shortest-common-supersequence?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. LCS table + backward walk](#3-lcs-table--backward-walk) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `str1` and `str2`, return the shortest string that has both as subsequences. If several exist, return any.

| Input | Output | Why |
|---|---|---|
| `"brute", "groot"` | `"bgruoote"` | length 8 = 5 + 5 − 2 (LCS "rt") |
| `"abac", "cab"` | `"cabac"` |  |

**Constraints:** `1 ≤ |a|, |b| ≤ 1000`, lowercase.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| LCS table + backward walk | match → emit once, else emit the dropped char | O(n·m) | O(n·m) |

> [!tip] Interview angle
> State the length formula first, then reconstruct. The key detail is that on a non-match you emit the character you **leave behind** (`a[i−1]` when moving up, `b[j−1]` when moving left).

---

## 3. LCS table + backward walk

**Intuition.** The full 2D table is required for reconstruction.

**Algorithm**

1. Build `dp[i][j]` = LCS of prefixes.
2. From `(n, m)`: match → emit, `i−−, j−−`; elif `dp[i−1][j] > dp[i][j−1]` → emit `a[i−1]`, `i−−`; else emit `b[j−1]`, `j−−`.
3. Emit the remaining `a[0..i)` and `b[0..j)`, then reverse.

**Dry run** — "abac"/"cab": walk emits c, a, b, a, c (reversed: "cabac").

**C++**
```cpp
string shortestCommonSupersequence(string a, string b) {
    int n = a.size(), m = b.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
            dp[i][j] = a[i - 1] == b[j - 1] ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);
    string res;
    int i = n, j = m;
    while (i > 0 && j > 0) {
        if (a[i - 1] == b[j - 1]) { res += a[i - 1]; i--; j--; }
        else if (dp[i - 1][j] > dp[i][j - 1]) { res += a[i - 1]; i--; }
        else { res += b[j - 1]; j--; }
    }
    while (i > 0) res += a[--i];
    while (j > 0) res += b[--j];
    reverse(res.begin(), res.end());
    return res;
}
```

**Java**
```java
static String shortestCommonSupersequence(String a, String b) {
    int n = a.length(), m = b.length();
    int[][] dp = new int[n + 1][m + 1];
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
            dp[i][j] = a.charAt(i - 1) == b.charAt(j - 1) ? dp[i - 1][j - 1] + 1 : Math.max(dp[i - 1][j], dp[i][j - 1]);
    StringBuilder res = new StringBuilder();
    int i = n, j = m;
    while (i > 0 && j > 0) {
        if (a.charAt(i - 1) == b.charAt(j - 1)) { res.append(a.charAt(i - 1)); i--; j--; }
        else if (dp[i - 1][j] > dp[i][j - 1]) { res.append(a.charAt(i - 1)); i--; }
        else { res.append(b.charAt(j - 1)); j--; }
    }
    while (i > 0) res.append(a.charAt(--i));
    while (j > 0) res.append(b.charAt(--j));
    return res.reverse().toString();
}
```

**Python**
```python
def shortest_common_supersequence(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(dp[i - 1][j], dp[i][j - 1])
    res, i, j = [], n, m
    while i and j:
        if a[i - 1] == b[j - 1]:
            res.append(a[i - 1]); i -= 1; j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            res.append(a[i - 1]); i -= 1
        else:
            res.append(b[j - 1]); j -= 1
    res.extend(reversed(a[:i]))
    res.extend(reversed(b[:j]))
    return "".join(reversed(res))
```

**Complexity:** time **O(n·m)**, space **O(n·m)** — one table, one O(n + m) walk.

---

## Edge cases

- Identical strings: the string itself.
- No common characters: the concatenation.

---

## Common mistakes

1. Emitting the character of the side you move toward instead of the one you leave.
2. Forgetting the leftover prefixes after the main loop.

---

## Follow-ups

1. Length only?
2. Lexicographically smallest SCS?

<details><summary>Answer sketches</summary>

**#1:** `n + m − LCS`.

**#2:** Break ties in the walk by comparing candidate characters (careful: this needs suffix-based DP).
</details>

---

## Flashcards

**SCS length?** #flashcard
|a| + |b| − LCS.

**SCS walk on mismatch?** #flashcard
Move toward the larger neighbour; emit the character you leave behind.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
