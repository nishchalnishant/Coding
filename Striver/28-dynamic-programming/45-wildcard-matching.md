---
module: striver/28-dynamic-programming
lesson: 45
topic: Wildcard matching
difficulty: Hard
source: https://takeuforward.org/learning/dsa/wildcard-matching?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings, pattern-matching]
---
# 45. Wildcard matching

← [Edit distance](44-edit-distance.md) · [Part 28 index](README.md) · Next → [Word break](46-word-break.md)

> [!abstract] Problem at a glance
> **Task:** Does pattern `p` (with `?` = any one char, `*` = any sequence) match all of `s`?
> **Key insight:** `dp[i][j]` = does `p[0..i)` match `s[0..j)`? A letter or `?` → `dp[i−1][j−1]` if compatible. `*` → `dp[i−1][j]` (match empty) **or** `dp[i][j−1]` (absorb one more char of `s`). Base: `dp[0][0] = true`; `dp[i][0]` is true only while `p[0..i)` is all `*`.
> **Difficulty:** Hard · **Pattern:** Two-string boolean DP · **Also on:** LC 44
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/wildcard-matching?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized f(i, j)](#3-memoized-fi-j) · [4. Two-row tabulation](#4-two-row-tabulation) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `s` and pattern `p` with `?` (matches any single character) and `*` (matches any sequence, including empty), return whether `p` matches the entire `s`.

| Input | Output | Why |
|---|---|---|
| `s = "aa", p = "a"` | `false` |  |
| `s = "aa", p = "*"` | `true` |  |
| `s = "cb", p = "?a"` | `false` |  |
| `s = "adceb", p = "*a*b"` | `true` |  |

**Constraints:** `0 ≤ |s|, |p| ≤ 2000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized f(i, j) | * → skip it or consume one | O(n·m) | O(n·m) |
| Two-row tabulation | prev = pattern row i−1 | O(n·m) | O(m) |

> [!tip] Interview angle
> Explain the `*` transition as "either it's done (empty) or it eats one more character and stays." That two-way choice keeps the DP O(n·m) instead of looping over every length. A greedy two-pointer with backtracking to the last `*` also works in O(n·m) worst case.

---

## 3. Memoized f(i, j)

**Intuition.** Recursion on pattern index `i` and string index `j`, from the front.

```python
def wild_memo(s, p):
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if i == len(p):
            return j == len(s)
        if p[i] == "*":
            return f(i + 1, j) or (j < len(s) and f(i, j + 1))
        return j < len(s) and p[i] in (s[j], "?") and f(i + 1, j + 1)
    return f(0, 0)
```

**Complexity:** time **O(n·m)**, space **O(n·m)**.

---

## 4. Two-row tabulation

**Intuition.** Rows over pattern prefixes, columns over string prefixes. `cur[0]` stays true only while the pattern prefix is all `*`.

**Algorithm**

1. `prev = [true, false, …]`.
2. For each pattern char `c`: `cur[0] = prev[0] && c == '*'`; for `j`: `*` → `prev[j] || cur[j−1]`; `?`/equal → `prev[j−1]`; else false.
3. Swap; return `prev[m]`.

**Dry run** — "adceb"/"*a*b": the `*` rows are all true, `a` matches at j = 1, the second `*` spreads, `b` closes at j = 5.

**C++**
```cpp
bool isMatch(string s, string p) {
    int m = s.size();
    vector<bool> prev(m + 1, false), cur(m + 1, false);
    prev[0] = true;
    for (char c : p) {
        cur[0] = prev[0] && c == '*';
        for (int j = 1; j <= m; j++) {
            if (c == '*') cur[j] = prev[j] || cur[j - 1];
            else cur[j] = (c == '?' || c == s[j - 1]) && prev[j - 1];
        }
        prev = cur;
    }
    return prev[m];
}
```

**Java**
```java
static boolean isMatch(String s, String p) {
    int m = s.length();
    boolean[] prev = new boolean[m + 1], cur = new boolean[m + 1];
    prev[0] = true;
    for (char c : p.toCharArray()) {
        cur[0] = prev[0] && c == '*';
        for (int j = 1; j <= m; j++) {
            if (c == '*') cur[j] = prev[j] || cur[j - 1];
            else cur[j] = (c == '?' || c == s.charAt(j - 1)) && prev[j - 1];
        }
        boolean[] t = prev; prev = cur; cur = t;
    }
    return prev[m];
}
```

**Python**
```python
def is_match(s, p):
    m = len(s)
    prev = [True] + [False] * m
    for c in p:
        cur = [prev[0] and c == "*"] + [False] * m
        for j in range(1, m + 1):
            if c == "*":
                cur[j] = prev[j] or cur[j - 1]
            else:
                cur[j] = (c == "?" or c == s[j - 1]) and prev[j - 1]
        prev = cur
    return prev[m]
```

**Complexity:** time **O(n·m)**, space **O(m)** — |p|·|s| cells, two rows.

---

## Edge cases

- Empty `s`: true only if `p` is all `*`.
- Consecutive `*`: equivalent to one (you can collapse them first).

---

## Common mistakes

1. `*` handled as "match exactly one".
2. `cur[0]` left true after a non-`*` character.

---

## Follow-ups

1. Regex `.` and `x*` (LC 10)?
2. Greedy O(1)-space?

<details><summary>Answer sketches</summary>

**#1:** A different `*`: it applies to the previous char, so the transition is `dp[i−2][j]` or (char match and `dp[i][j−1]`).

**#2:** Track the last `*` position and the `s` index it matched; on mismatch, backtrack there and extend by one.
</details>

---

## Flashcards

**Wildcard `*` transition?** #flashcard
`dp[i−1][j]` (empty) ∨ `dp[i][j−1]` (consume one).

**dp[i][0] true when?** #flashcard
The pattern prefix is all `*`.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
