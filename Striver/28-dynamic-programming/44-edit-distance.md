---
module: striver/28-dynamic-programming
lesson: 44
topic: Edit distance
difficulty: Hard
source: https://takeuforward.org/learning/dsa/edit-distance?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings]
---
# 44. Edit distance

← [Distinct subsequences](43-distinct-subsequences.md) · [Part 28 index](README.md) · Next → [Wildcard matching](45-wildcard-matching.md)

> [!abstract] Problem at a glance
> **Task:** Fewest insert / delete / replace operations turning `a` into `b`.
> **Key insight:** `dp[i][j]` for prefixes. Match → `dp[i−1][j−1]` (free). Else `1 + min(dp[i−1][j]` (delete `a[i−1]`), `dp[i][j−1]` (insert `b[j−1]`), `dp[i−1][j−1]` (replace)`)`. Bases: `dp[i][0] = i`, `dp[0][j] = j`.
> **Difficulty:** Hard · **Pattern:** Two-string DP (min ops) · **Also on:** LC 72
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/edit-distance?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized f(i, j)](#3-memoized-fi-j) · [4. Two-row tabulation](#4-two-row-tabulation) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `word1` and `word2`, return the minimum number of operations (insert, delete, or replace a character) to convert `word1` into `word2`.

| Input | Output | Why |
|---|---|---|
| `"horse", "ros"` | `3` | replace h→r, delete r, delete e |
| `"intention", "execution"` | `5` |  |

**Constraints:** `0 ≤ |a|, |b| ≤ 500`, lowercase.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized f(i, j) | three ops on mismatch | O(n·m) | O(n·m) |
| Two-row tabulation | prev / cur with cur[0] = i | O(n·m) | O(m) |

> [!tip] Interview angle
> Name each transition as an operation; interviewers check that you know which neighbour means what. The bases are `i` and `j`, not 0. With two rows, `cur[0] = i` must be set for each row.

---

## 3. Memoized f(i, j)

**Intuition.** On suffixes: either string exhausted → the other's remaining length.

```python
def ed_memo(a, b):
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return f(i + 1, j + 1)
        return 1 + min(f(i + 1, j), f(i, j + 1), f(i + 1, j + 1))
    return f(0, 0)
```

**Complexity:** time **O(n·m)**, space **O(n·m)**.

---

## 4. Two-row tabulation

**Intuition.** The 2D recurrence with rolling rows.

**Algorithm**

1. `prev[j] = j`.
2. For `i = 1..n`: `cur[0] = i`; match → `prev[j−1]`, else `1 + min(prev[j], cur[j−1], prev[j−1])`.
3. Swap; return `prev[m]`.

**Dry run** — "horse"/"ros": final row [5,4,4,3] → 3.

**C++**
```cpp
int minDistance(string a, string b) {
    int n = a.size(), m = b.size();
    vector<int> prev(m + 1), cur(m + 1);
    for (int j = 0; j <= m; j++) prev[j] = j;
    for (int i = 1; i <= n; i++) {
        cur[0] = i;
        for (int j = 1; j <= m; j++)
            cur[j] = a[i - 1] == b[j - 1] ? prev[j - 1] : 1 + min({prev[j], cur[j - 1], prev[j - 1]});
        prev = cur;
    }
    return prev[m];
}
```

**Java**
```java
static int minDistance(String a, String b) {
    int n = a.length(), m = b.length();
    int[] prev = new int[m + 1], cur = new int[m + 1];
    for (int j = 0; j <= m; j++) prev[j] = j;
    for (int i = 1; i <= n; i++) {
        cur[0] = i;
        for (int j = 1; j <= m; j++)
            cur[j] = a.charAt(i - 1) == b.charAt(j - 1) ? prev[j - 1] : 1 + Math.min(prev[j], Math.min(cur[j - 1], prev[j - 1]));
        int[] t = prev; prev = cur; cur = t;
    }
    return prev[m];
}
```

**Python**
```python
def min_distance(a, b):
    m = len(b)
    prev = list(range(m + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cur[j] = prev[j - 1] if ca == b[j - 1] else 1 + min(prev[j], cur[j - 1], prev[j - 1])
        prev = cur
    return prev[m]
```

**Complexity:** time **O(n·m)**, space **O(m)** — n·m, two rows.

---

## Edge cases

- Either string empty: the other's length.
- Equal strings: 0.

---

## Common mistakes

1. Base row/column set to 0.
2. Forgetting `cur[0] = i` in the rolling version.
3. Adding 1 on a match.

---

## Follow-ups

1. Only insert/delete?
2. One edit away (LC 161)?
3. Reconstruct the operations.

<details><summary>Answer sketches</summary>

**#1:** `n + m − 2·LCS`.

**#2:** Linear two-pointer check, no DP.

**#3:** Keep the full table and walk back, labelling each move.
</details>

---

## Flashcards

**Edit distance moves?** #flashcard
up = delete, left = insert, diagonal = replace (or free on match).

**Edit distance bases?** #flashcard
dp[i][0] = i, dp[0][j] = j.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
