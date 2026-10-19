---
module: striver/28-dynamic-programming
lesson: 38
topic: Longest common substring
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-common-substring?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings]
---
# 38. Longest common substring

← [Longest common subsequence](37-longest-common-subsequence.md) · [Part 28 index](README.md) · Next → [Longest palindromic subsequence](39-longest-palindromic-subsequence.md)

> [!abstract] Problem at a glance
> **Task:** Length of the longest **contiguous** substring common to both strings.
> **Key insight:** Contiguity changes the recurrence: `dp[i][j]` = length of the common substring **ending exactly** at `a[i−1]` and `b[j−1]`. Match → `1 + dp[i−1][j−1]`; mismatch → **0** (the run breaks). The answer is the max over all cells, not `dp[n][m]`.
> **Difficulty:** Medium · **Pattern:** Two-string DP (ending-at)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-common-substring?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All substrings of a, search in b](#3-all-substrings-of-a-search-in-b) · [4. Ending-at DP, two rows](#4-ending-at-dp-two-rows) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given strings `s1` and `s2`, return the length of the longest common substring.

| Input | Output | Why |
|---|---|---|
| `"abcjklp", "acjkp"` | `3` | cjk |
| `"wasdijkl", "wsdjkl"` | `3` | jkl |
| `"abc", "xyz"` | `0` |  |

**Constraints:** `1 ≤ |s1|, |s2| ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All substrings of a, search in b | O(n²) substrings × find | O(n²·m) | O(n) |
| Ending-at DP, two rows | match → diag + 1, else 0; track max | O(n·m) | O(m) |

> [!tip] Interview angle
> Contrast with LCS in one sentence: "Mismatch resets to 0 instead of taking a max, and I track a global max." Mention suffix automaton / binary search + hashing for O((n+m) log) if asked about scale.

---

## 3. All substrings of a, search in b

**Intuition.** Try every substring of `a`, longest first, and check `in b`.

```python
def lcsub_brute(a, b):
    for L in range(len(a), 0, -1):
        for i in range(len(a) - L + 1):
            if a[i:i + L] in b:
                return L
    return 0
```

**Complexity:** time **O(n²·m)**, space **O(n)**.

---

## 4. Ending-at DP, two rows

**Intuition.** Only the diagonal neighbour matters, so one previous row suffices.

**Algorithm**

1. `prev = [0]*(m+1)`, `best = 0`.
2. For each `i`, `j`: `cur[j] = prev[j−1] + 1` on match, else 0; `best = max(best, cur[j])`.
3. Return `best`.

**Dry run** — "abcjklp" / "acjkp": the diagonal run c-j-k reaches 3.

**C++**
```cpp
int longestCommonSubstr(string a, string b) {
    int n = a.size(), m = b.size(), best = 0;
    vector<int> prev(m + 1, 0), cur(m + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cur[j] = a[i - 1] == b[j - 1] ? prev[j - 1] + 1 : 0;
            best = max(best, cur[j]);
        }
        prev = cur;
    }
    return best;
}
```

**Java**
```java
static int longestCommonSubstr(String a, String b) {
    int n = a.length(), m = b.length(), best = 0;
    int[] prev = new int[m + 1], cur = new int[m + 1];
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cur[j] = a.charAt(i - 1) == b.charAt(j - 1) ? prev[j - 1] + 1 : 0;
            best = Math.max(best, cur[j]);
        }
        int[] t = prev; prev = cur; cur = t;
    }
    return best;
}
```

**Python**
```python
def longest_common_substr(a, b):
    m, best = len(b), 0
    prev = [0] * (m + 1)
    for ca in a:
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if ca == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best
```

**Complexity:** time **O(n·m)**, space **O(m)** — n·m, two rows.

---

## Edge cases

- No common character: 0.
- One string inside the other: its length.

---

## Common mistakes

1. Returning `dp[n][m]`.
2. Taking `max(up, left)` on mismatch (that's LCS).

---

## Follow-ups

1. Return the substring.
2. Maximum length of repeated subarray (LC 718)?

<details><summary>Answer sketches</summary>

**#1:** Record the `i` where `best` was achieved; slice `a[i−best : i]`.

**#2:** The same DP on integer arrays.
</details>

---

## Flashcards

**Common substring mismatch value?** #flashcard
0, because the run breaks.

**Common substring answer cell?** #flashcard
Max over all cells.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
