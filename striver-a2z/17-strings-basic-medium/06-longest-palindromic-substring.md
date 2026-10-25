---
module: striver-a2z/17-strings-basic-medium
lesson: 6
topic: Longest Palindromic Substring
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-palindromic-substring?category=substrings&source=strivers-a2z-dsa-sheet
tags: [striver, strings-basic-and-medium, string, dp, two-pointers]
---
# 6. Longest Palindromic Substring

← [Count Substrings with Exactly K Distinct Characters](05-count-substrings-k-distinct.md) · [Part 17 index](README.md) · Next → [Sum of Beauty of All Substrings](07-sum-of-beauty-of-all-substrings.md)

> [!abstract] Problem at a glance
> **Task:** Return the longest substring of `s` that is a palindrome.
> **Key insight:** Every palindrome mirrors around a centre — a character (odd length) or a gap (even length). There are 2n − 1 centres; expand each while the ends match. O(n²) time, O(1) space.
> **Difficulty:** Medium · **Pattern:** Expand around centre · **Also on:** [LC 5](https://leetcode.com/problems/longest-palindromic-substring/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-palindromic-substring?category=substrings&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Check every substring](#3-check-every-substring) · [4. Interval DP](#4-interval-dp) · [5. Expand around centre](#5-expand-around-centre) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `s`, return the longest palindromic substring. If several have the maximum length, return the one that starts first.

| Input | Output | Why |
|---|---|---|
| `s = "babad"` | `"bab"` | "aba" is equally long but starts later |
| `s = "cbbd"` | `"bb"` | even-length centre |
| `s = "a"` | `"a"` |  |

**Constraints:** `1 ≤ |s| ≤ 1000`, digits and English letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Check every substring | O(n²) substrings × O(n) check | O(n³) | O(1) |
| Interval DP | dp[i][j] = s[i]==s[j] and dp[i+1][j−1] | O(n²) | O(n²) |
| Expand around centre | 2n − 1 centres; widen while s[l] == s[r] | O(n²) | O(1) |

> [!tip] Interview angle
> Top-10 string question. Expected path: brute O(n³) → DP O(n²) time and space → expand around centre O(n²) time, O(1) space. Mention Manacher's O(n) by name and that it isn't expected at L3/L4. Forgetting even-length centres is the classic bug.

---

## 3. Check every substring

**Intuition.** For each `(i, j)`, two-pointer check whether `s[i..j]` is a palindrome; keep the longest. Only feasible for tiny n.

```python
def lps_brute(s):
    n, best = len(s), s[:1]
    for i in range(n):
        for j in range(i + len(best), n):
            sub = s[i:j + 1]
            if sub == sub[::-1]:
                best = sub
    return best
```

**Complexity:** time **O(n³)**, space **O(1)**.

---

## 4. Interval DP

**Intuition.** A substring is a palindrome iff its ends match and its inside is a palindrome. Fill by increasing length so `dp[i+1][j−1]` is ready. Length 1 and 2 are the base cases. Useful because the same table answers "is s[i..j] a palindrome?" in O(1) — needed for palindrome partitioning.

```python
def lps_dp(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start, length = 0, 1
    for L in range(1, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            if s[i] == s[j] and (L <= 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                if L > length:
                    start, length = i, L
    return s[start:start + length]
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 5. Expand around centre

**Intuition.** For each `i`, expand from `(i, i)` for odd lengths and `(i, i + 1)` for even. `expand` returns the length of the widest palindrome at that centre. Update the best with a strict `>` so ties keep the earliest start.

**Algorithm**

1. For each `i`: `len1 = expand(i, i)`, `len2 = expand(i, i + 1)`.
2. `L = max(len1, len2)`; if `L > best`: `start = i − (L − 1) / 2`.
3. Return `s[start : start + best]`.

**Dry run** — `cbbd`: i = 1 even centre (1, 2) 'b'='b' → expand to (0, 3) 'c'≠'d' → length 2, start 1 → `bb`.

**Manacher's algorithm** reuses mirror information inside the current rightmost palindrome to get O(n). Worth naming; see [Strings advanced](../30-strings-advanced/README.md).

**C++**
```cpp
int expand(const string& s, int l, int r) {
    while (l >= 0 && r < (int)s.size() && s[l] == s[r]) { l--; r++; }
    return r - l - 1;
}
string longestPalindrome(string s) {
    int start = 0, best = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        int L = max(expand(s, i, i), expand(s, i, i + 1));
        if (L > best) { best = L; start = i - (L - 1) / 2; }
    }
    return s.substr(start, best);
}
```

**Java**
```java
static int expand(String s, int l, int r) {
    while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
    return r - l - 1;
}
static String longestPalindrome(String s) {
    int start = 0, best = 0;
    for (int i = 0; i < s.length(); i++) {
        int L = Math.max(expand(s, i, i), expand(s, i, i + 1));
        if (L > best) { best = L; start = i - (L - 1) / 2; }
    }
    return s.substring(start, start + best);
}
```

**Python**
```python
def longest_palindrome(s):
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return r - l - 1
    start = best = 0
    for i in range(len(s)):
        L = max(expand(i, i), expand(i, i + 1))
        if L > best:
            best, start = L, i - (L - 1) // 2
    return s[start:start + best]
```

**Complexity:** time **O(n²)**, space **O(1)** — 2n − 1 centres, each expands O(n) at most; no table.

---

## Edge cases

- Length 1.
- No palindrome longer than 1 → first char.
- Whole string is a palindrome.
- Even-length answer (`cbbd`).
- All same char.

---

## Common mistakes

1. Only odd centres — misses `bb`.
2. `start = i − L / 2` — off by one for even lengths; use `(L − 1) / 2`.
3. Longest common substring of `s` and `reverse(s)` — fails on `abacdfgdcaba` (matches `abacd`/`dcaba`) unless you check that the indices mirror.

---

## Follow-ups

1. Count palindromic substrings (LC 647).
2. Longest palindromic subsequence (LC 516).
3. Need O(n).

<details><summary>Answer sketches</summary>

**#1:** Same expansion; add 1 per successful step instead of tracking max.

**#2:** Different problem — interval DP or LCS(s, reverse(s)), O(n²).

**#3:** Manacher's algorithm, or hashing + binary search on length in O(n log n).
</details>

---

## Flashcards

**How many palindrome centres in a length-n string?** #flashcard
2n − 1: n characters and n − 1 gaps.

**Start index from centre i and length L?** #flashcard
i − (L − 1) / 2.

**Palindrome DP recurrence?** #flashcard
dp[i][j] = s[i] == s[j] and (j − i < 2 or dp[i+1][j−1]).

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String walkthroughs](../../04-practice/data-structures/03-string.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
