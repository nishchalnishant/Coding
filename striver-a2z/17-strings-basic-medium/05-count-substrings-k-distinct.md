---
module: striver-a2z/17-strings-basic-medium
lesson: 5
topic: Count Substrings with Exactly K Distinct Characters
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-number-of-substring?category=substrings&source=strivers-a2z-dsa-sheet
tags: [striver, strings-basic-and-medium, string, sliding-window, hashing]
---
# 5. Count Substrings with Exactly K Distinct Characters

← [String to Integer (atoi)](04-string-to-integer-atoi.md) · [Part 17 index](README.md) · Next → [Longest Palindromic Substring](06-longest-palindromic-substring.md)

> [!abstract] Problem at a glance
> **Task:** Count the substrings of a lowercase string that contain exactly `k` distinct characters.
> **Key insight:** "At most k distinct" is monotone, so a sliding window counts it in O(n): every valid window ending at `r` contributes `r − l + 1` substrings. Exactly k = atMost(k) − atMost(k − 1).
> **Difficulty:** Medium · **Pattern:** Sliding window, exactly = atMost(k) − atMost(k−1) · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/count-number-of-substrings4528/1) · LC 992 (same trick on arrays)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-number-of-substring?category=substrings&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All substrings with a set](#3-all-substrings-with-a-set) · [4. atMost(k) − atMost(k − 1)](#4-atmostk--atmostk--1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a lowercase string `s` and an integer `k`, return the number of substrings (contiguous, counted by position) with exactly `k` distinct characters.

| Input | Output | Why |
|---|---|---|
| `s = "aba", k = 2` | `3` | ab, ba, aba |
| `s = "abaaca", k = 1` | `7` | a, b, a, a, c, a, aa |
| `s = "abc", k = 3` | `1` |  |

**Constraints:** `1 ≤ |s| ≤ 10⁵`, `1 ≤ k ≤ 26`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All substrings with a set | fix i, extend j, track distinct count | O(n²) | O(26) |
| atMost(k) − atMost(k − 1) | window counts substrings with ≤ k distinct; subtract | O(n) | O(26) |

> [!tip] Interview angle
> The point is the subtraction trick. A direct window for "exactly k" fails: when the window has exactly k, you can't decide whether to grow or shrink. Explain why "at most" works (shrinking never breaks validity) and that the trick reappears in LC 992 and binary subarrays with sum.

---

## 3. All substrings with a set

**Intuition.** For each start `i`, extend `j` and keep a count array; add 1 when distinct == k, break once distinct > k (it can only grow).

```python
def count_k_brute(s, k):
    n, total = len(s), 0
    for i in range(n):
        cnt, distinct = [0] * 26, 0
        for j in range(i, n):
            c = ord(s[j]) - 97
            if cnt[c] == 0:
                distinct += 1
            cnt[c] += 1
            if distinct == k:
                total += 1
            elif distinct > k:
                break
    return total
```

**Complexity:** time **O(n²)**, space **O(26)**.

---

## 4. atMost(k) − atMost(k − 1)

**Intuition.** `atMost(k)`: grow `r`; while distinct > k, shrink `l`. Now every substring ending at `r` and starting in `[l, r]` has ≤ k distinct — that's `r − l + 1` of them. Summing over `r` counts all ≤ k substrings. Substrings with exactly k are those with ≤ k minus those with ≤ k − 1.

**Algorithm**

1. `atMost(m)`: `l = 0`, counts, distinct.
2. For each `r`: add `s[r]`; while distinct > m remove `s[l++]`; `total += r − l + 1`.
3. Return `atMost(k) − atMost(k − 1)`.

**Dry run** — `aba`, k = 2: atMost(2) = 1 + 2 + 3 = 6; atMost(1) = 1 + 1 + 1 = 3; answer 3.

**C++**
```cpp
long long atMost(const string& s, int k) {
    if (k < 0) return 0;
    int cnt[26] = {0}, distinct = 0, l = 0;
    long long total = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        if (cnt[s[r] - 'a']++ == 0) distinct++;
        while (distinct > k)
            if (--cnt[s[l++] - 'a'] == 0) distinct--;
        total += r - l + 1;
    }
    return total;
}
long long countSubstr(string s, int k) {
    return atMost(s, k) - atMost(s, k - 1);
}
```

**Java**
```java
static long atMost(String s, int k) {
    if (k < 0) return 0;
    int[] cnt = new int[26];
    int distinct = 0, l = 0;
    long total = 0;
    for (int r = 0; r < s.length(); r++) {
        if (cnt[s.charAt(r) - 'a']++ == 0) distinct++;
        while (distinct > k)
            if (--cnt[s.charAt(l++) - 'a'] == 0) distinct--;
        total += r - l + 1;
    }
    return total;
}
static long countSubstr(String s, int k) {
    return atMost(s, k) - atMost(s, k - 1);
}
```

**Python**
```python
def count_k(s, k):
    def at_most(m):
        if m < 0:
            return 0
        cnt, distinct, l, total = [0] * 26, 0, 0, 0
        for r, ch in enumerate(s):
            c = ord(ch) - 97
            if cnt[c] == 0:
                distinct += 1
            cnt[c] += 1
            while distinct > m:
                d = ord(s[l]) - 97
                cnt[d] -= 1
                if cnt[d] == 0:
                    distinct -= 1
                l += 1
            total += r - l + 1
        return total
    return at_most(k) - at_most(k - 1)
```

**Complexity:** time **O(n)**, space **O(26)** — each pointer moves n times per call; two calls.

---

## Edge cases

- k larger than the alphabet in `s` → 0.
- All same char, k = 1 → n(n + 1)/2 — overflows int for n = 10⁵, use 64-bit.
- k = 1 with alternating chars.

---

## Common mistakes

1. Trying to maintain an "exactly k" window directly.
2. Counting distinct windows instead of substrings ending at `r` (`r − l + 1`).
3. 32-bit total: n(n + 1)/2 ≈ 5·10⁹.

---

## Follow-ups

1. Subarrays with exactly k distinct integers (LC 992).
2. Longest substring with at most k distinct (LC 340).
3. Count substrings with at least k distinct.

<details><summary>Answer sketches</summary>

**#1:** Identical, with a hashmap instead of `int[26]`.

**#2:** Same window, track `max(r − l + 1)`.

**#3:** Total `n(n + 1)/2 − atMost(k − 1)`.
</details>

---

## Flashcards

**Exactly k via sliding window?** #flashcard
exactly(k) = atMost(k) − atMost(k − 1).

**In an at-most-k window ending at r, how many valid substrings end at r?** #flashcard
r − l + 1.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String walkthroughs](../../04-practice/data-structures/03-string.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
