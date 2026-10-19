---
module: striver/17-strings-basic-medium
lesson: 7
topic: Sum of Beauty of All Substrings
difficulty: Medium
source: https://takeuforward.org/learning/dsa/sum-of-beauty-of-all-substrings?category=substrings&source=strivers-a2z-dsa-sheet
tags: [striver, strings-basic-and-medium, string, hashing, counting]
---
# 7. Sum of Beauty of All Substrings

← [Longest Palindromic Substring](06-longest-palindromic-substring.md) · [Part 17 index](README.md) · Next → [Part 18: Recursion](../18-recursion/README.md)

> [!abstract] Problem at a glance
> **Task:** Sum, over every substring, the difference between its most and least frequent characters' counts.
> **Key insight:** Fix the start, extend the end one char at a time, and update a 26-entry count array incrementally — no recount per substring. Max/min over 26 counts is O(26), giving O(26 · n²).
> **Difficulty:** Medium · **Pattern:** Enumerate substrings with incremental counts · **Also on:** [LC 1781](https://leetcode.com/problems/sum-of-beauty-of-all-substrings/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sum-of-beauty-of-all-substrings?category=substrings&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recount each substring](#3-recount-each-substring) · [4. Incremental counts per start](#4-incremental-counts-per-start) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

The **beauty** of a string is (frequency of the most frequent character) − (frequency of the least frequent character), counting only characters that appear. Given lowercase `s`, return the sum of beauties of all its substrings.

| Input | Output | Why |
|---|---|---|
| `s = "aabcb"` | `5` | aab, aabc, aabcb, abcb, bcb have beauty 1 each |
| `s = "aabcbaa"` | `17` |  |

**Constraints:** `1 ≤ |s| ≤ 500`, lowercase letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recount each substring | for every (i, j), count chars from scratch | O(n³) | O(26) |
| Incremental counts per start | fix i; extend j, cnt[s[j]]++, add max − min of non-zero counts | O(26 · n²) | O(26) |

> [!tip] Interview angle
> The constraint (n ≤ 500) tells you O(n²) with a small constant is intended. The point is recognising that recounting each substring (O(n³)) is wasteful — extending the end by one changes exactly one count. Ignore zero counts when taking the minimum.

---

## 3. Recount each substring

**Intuition.** Correct baseline: for every substring build `Counter(s[i:j+1])` and take max − min. 500³/6 ≈ 2·10⁷ char ops — passes in C++, slow in Python.

```python
from collections import Counter
def beauty_brute(s):
    n, total = len(s), 0
    for i in range(n):
        for j in range(i, n):
            c = Counter(s[i:j + 1]).values()
            total += max(c) - min(c)
    return total
```

**Complexity:** time **O(n³)**, space **O(26)**.

---

## 4. Incremental counts per start

**Intuition.** For each start `i`, reset `cnt`. For `j = i … n − 1`, increment `cnt[s[j]]` and scan the 26 entries for max and min among non-zero ones. Each substring costs O(26) instead of O(length).

**Dry run** — `aab`: i = 0 → `a` (0), `aa` (0), `aab` max 2 min 1 → 1. i = 1 → `a`, `ab` → 0. i = 2 → 0. Contribution 1.

**Faster max:** the max can be maintained in O(1) since counts only increase (`mx = max(mx, cnt[c])`); the min still needs the scan (or a frequency-of-frequencies array).

**C++**
```cpp
int beautySum(string s) {
    int n = s.size(), total = 0;
    for (int i = 0; i < n; i++) {
        int cnt[26] = {0};
        for (int j = i; j < n; j++) {
            cnt[s[j] - 'a']++;
            int mx = 0, mn = INT_MAX;
            for (int c : cnt) if (c) { mx = max(mx, c); mn = min(mn, c); }
            total += mx - mn;
        }
    }
    return total;
}
```

**Java**
```java
static int beautySum(String s) {
    int n = s.length(), total = 0;
    for (int i = 0; i < n; i++) {
        int[] cnt = new int[26];
        for (int j = i; j < n; j++) {
            cnt[s.charAt(j) - 'a']++;
            int mx = 0, mn = Integer.MAX_VALUE;
            for (int c : cnt) if (c > 0) { mx = Math.max(mx, c); mn = Math.min(mn, c); }
            total += mx - mn;
        }
    }
    return total;
}
```

**Python**
```python
def beauty_sum(s):
    n, total = len(s), 0
    for i in range(n):
        cnt = [0] * 26
        for j in range(i, n):
            cnt[ord(s[j]) - 97] += 1
            nz = [c for c in cnt if c]
            total += max(nz) - min(nz)
    return total
```

**Complexity:** time **O(26 · n²)**, space **O(26)** — n(n + 1)/2 substrings, O(26) each; max total ≈ 500 · 500 · 500/2 fits in int.

---

## Edge cases

- All distinct → every beauty 0.
- Single char → 0.
- All same char → every beauty 0 (max = min).

---

## Common mistakes

1. Including zero counts in the min — makes min 0 everywhere.
2. Recounting from scratch per substring.
3. Resetting `cnt` inside the inner loop.

---

## Follow-ups

1. n up to 10⁵.
2. Return the max beauty over substrings.

<details><summary>Answer sketches</summary>

**#1:** Can't enumerate substrings; this problem has no known near-linear solution — clarify constraints.

**#2:** Kadane-style over pairs of chars (LC 2272, Substring With Largest Variance): O(26² · n).
</details>

---

## Flashcards

**Why is sum of beauty O(26 · n²), not O(n³)?** #flashcard
Extending the end changes one count; max/min over 26 entries is O(26).

**Beauty's min ignores which counts?** #flashcard
Zero counts — characters absent from the substring.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String walkthroughs](../../coding/data-structures/03-string.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
