---
module: striver/28-dynamic-programming
lesson: 41
topic: Minimum insertions or deletions to convert string A to B
difficulty: Medium
source: https://takeuforward.org/learning/dsa/minimum-insertions-or-deletions-to-convert-string-a-to-b?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings, lcs]
---
# 41. Minimum insertions or deletions to convert string A to B

← [Minimum insertions to make string palindrome](40-minimum-insertions-to-make-string-palindrome.md) · [Part 28 index](README.md) · Next → [Shortest common supersequence](42-shortest-common-supersequence.md)

> [!abstract] Problem at a glance
> **Task:** Fewest single-character insertions + deletions turning `a` into `b`.
> **Key insight:** Keep their LCS untouched: delete the other `|a| − LCS` characters of `a`, insert the other `|b| − LCS` characters of `b`. **Answer = |a| + |b| − 2·LCS.** The cost can't be lower because whatever survives from `a` must be a common subsequence.
> **Difficulty:** Medium · **Pattern:** LCS reduction · **Also on:** LC 583 (variant)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-insertions-or-deletions-to-convert-string-a-to-b?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. |a| + |b| − 2·LCS](#3-a--b--2lcs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given strings `str1` and `str2`, return the minimum number of operations (insert or delete one character) to convert `str1` into `str2`.

| Input | Output | Why |
|---|---|---|
| `"abcd", "anc"` | `3` | delete b, d; insert n |
| `"sea", "eat"` | `2` |  |
| `"leetcode", "etco"` | `4` |  |

**Constraints:** `1 ≤ |a|, |b| ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| |a| + |b| − 2·LCS | LCS kept, rest deleted/inserted | O(n·m) | O(m) |

> [!tip] Interview angle
> One line of algebra on top of LCS. If replace is also allowed, it becomes edit distance, which needs its own DP.

---

## 3. |a| + |b| − 2·LCS

**Intuition.** Compute LCS with two rows and plug into the formula.

**Algorithm**

1. `L = LCS(a, b)`.
2. Return `(|a| − L) + (|b| − L)`.

**Dry run** — "abcd" / "anc": LCS "ac" = 2 → 4 + 3 − 4 = 3.

**C++**
```cpp
int minOperations(string a, string b) {
    int n = a.size(), m = b.size();
    vector<int> prev(m + 1, 0), cur(m + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++)
            cur[j] = a[i - 1] == b[j - 1] ? prev[j - 1] + 1 : max(prev[j], cur[j - 1]);
        prev = cur;
    }
    return n + m - 2 * prev[m];
}
```

**Java**
```java
static int minOperations(String a, String b) {
    int n = a.length(), m = b.length();
    int[] prev = new int[m + 1], cur = new int[m + 1];
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++)
            cur[j] = a.charAt(i - 1) == b.charAt(j - 1) ? prev[j - 1] + 1 : Math.max(prev[j], cur[j - 1]);
        int[] t = prev; prev = cur; cur = t;
    }
    return n + m - 2 * prev[m];
}
```

**Python**
```python
def min_operations(a, b):
    m = len(b)
    prev = [0] * (m + 1)
    for ca in a:
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            cur[j] = prev[j - 1] + 1 if ca == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return len(a) + m - 2 * prev[m]
```

**Complexity:** time **O(n·m)**, space **O(m)** — one LCS.

---

## Edge cases

- Equal strings: 0.
- Nothing in common: |a| + |b|.

---

## Common mistakes

1. Using edit distance (replace isn't allowed here).
2. Returning `|a| − LCS` only.

---

## Follow-ups

1. Minimum ASCII delete sum (LC 712)?
2. Replace allowed too?

<details><summary>Answer sketches</summary>

**#1:** Weighted LCS: maximise the kept ASCII sum, or a direct min-cost DP.

**#2:** Edit distance.
</details>

---

## Flashcards

**Insert/delete distance?** #flashcard
|a| + |b| − 2·LCS.

**Deletions vs insertions split?** #flashcard
|a| − LCS deletions, |b| − LCS insertions.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
