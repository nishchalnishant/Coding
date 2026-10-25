---
module: striver-a2z/28-dynamic-programming
lesson: 40
topic: Minimum insertions to make string palindrome
difficulty: Hard
source: https://takeuforward.org/learning/dsa/minimum-insertions-to-make-string-palindrome?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings, lcs, palindrome]
---
# 40. Minimum insertions to make string palindrome

← [Longest palindromic subsequence](39-longest-palindromic-subsequence.md) · [Part 28 index](README.md) · Next → [Minimum insertions or deletions to convert string A to B](41-min-insertions-deletions-a-to-b.md)

> [!abstract] Problem at a glance
> **Task:** Fewest characters to insert (anywhere) so `s` becomes a palindrome.
> **Key insight:** Keep the longest palindromic subsequence untouched. Each of the other `n − LPS` characters needs a mirror inserted, and none of them can be saved. **Answer = n − LPS(s) = n − LCS(s, rev(s)).**
> **Difficulty:** Hard · **Pattern:** LCS reduction · **Also on:** LC 1312
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-insertions-to-make-string-palindrome?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Interval recursion](#3-interval-recursion) · [4. n − LCS(s, reverse(s))](#4-n--lcss-reverses) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `s`, return the minimum number of insertions needed to make it a palindrome.

| Input | Output | Why |
|---|---|---|
| `"zzazz"` | `0` | already a palindrome |
| `"mbadm"` | `2` | mbdadbm |
| `"leetcode"` | `5` |  |

**Constraints:** `1 ≤ |s| ≤ 500`, lowercase.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Interval recursion | match → inside; else 1 + min(drop left, drop right) | O(n²) | O(n²) |
| n − LCS(s, reverse(s)) | reuse LPS | O(n²) | O(n) |

> [!tip] Interview angle
> Argue both directions: "`n − LPS` insertions suffice (mirror the rest), and fewer is impossible, because the final palindrome's restriction to the original characters is a palindromic subsequence." The equality is the proof.

---

## 3. Interval recursion

**Intuition.** `f(i, j)`: equal ends → `f(i+1, j−1)`; else `1 + min(f(i+1, j), f(i, j−1))`.

```python
def mi_interval(s):
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if i >= j:
            return 0
        if s[i] == s[j]:
            return f(i + 1, j - 1)
        return 1 + min(f(i + 1, j), f(i, j - 1))
    return f(0, len(s) - 1)
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 4. n − LCS(s, reverse(s))

**Intuition.** Compute LPS with the two-row LCS and subtract from `n`.

**Algorithm**

1. `L = LCS(s, reverse(s))`.
2. Return `n − L`.

**Dry run** — "mbadm": LPS "mam"/"mdm" = 3 → 5 − 3 = 2.

**C++**
```cpp
int minInsertions(string s) {
    string t(s.rbegin(), s.rend());
    int n = s.size();
    vector<int> prev(n + 1, 0), cur(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++)
            cur[j] = s[i - 1] == t[j - 1] ? prev[j - 1] + 1 : max(prev[j], cur[j - 1]);
        prev = cur;
    }
    return n - prev[n];
}
```

**Java**
```java
static int minInsertions(String s) {
    String t = new StringBuilder(s).reverse().toString();
    int n = s.length();
    int[] prev = new int[n + 1], cur = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++)
            cur[j] = s.charAt(i - 1) == t.charAt(j - 1) ? prev[j - 1] + 1 : Math.max(prev[j], cur[j - 1]);
        int[] tmp = prev; prev = cur; cur = tmp;
    }
    return n - prev[n];
}
```

**Python**
```python
def min_insertions(s):
    t, n = s[::-1], len(s)
    prev = [0] * (n + 1)
    for c in s:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            cur[j] = prev[j - 1] + 1 if c == t[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return n - prev[n]
```

**Complexity:** time **O(n²)**, space **O(n)** — one LCS.

---

## Edge cases

- Already a palindrome: 0.
- All distinct: n − 1.

---

## Common mistakes

1. Returning LPS instead of `n − LPS`.
2. Thinking deletions and insertions differ here: min deletions to a palindrome is the same `n − LPS`.

---

## Follow-ups

1. Min deletions to make a palindrome?
2. Only append at the front (LC 214)?

<details><summary>Answer sketches</summary>

**#1:** Also `n − LPS`.

**#2:** KMP/LPS-array on `s + '#' + rev(s)`; covered in Strings (Advanced).
</details>

---

## Flashcards

**Min insertions to palindrome?** #flashcard
n − LPS(s).

**Same answer for deletions?** #flashcard
Yes, n − LPS.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
