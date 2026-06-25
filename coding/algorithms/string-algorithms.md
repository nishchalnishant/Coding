---
tags: [coding, algorithms, string-algorithms]
topic: String Algorithms
difficulty: mixed
---

# String Algorithms — Amazon SDE-2

---

## Sliding Window on Strings

---

### Longest Substring Without Repeating Characters

> [!example] Problem
> Given a string s, find the length of the longest substring without repeating characters. LeetCode 3.

> [!info] Approach
> Classic variable-size sliding window. Maintain a set (or last-seen index map) of characters in the current window. Expand right always; when a duplicate is found, shrink left until the duplicate is removed. Using a map of last-seen indices lets you jump `left` directly to `last[s[right]] + 1` instead of shrinking one by one — O(n) with no inner loop.

> [!note]- Python Solution
> ```python
> def length_of_longest_substring(s):
>     last_seen = {}
>     left = result = 0
>     for right, c in enumerate(s):
>         if c in last_seen and last_seen[c] >= left:
>             left = last_seen[c] + 1
>         last_seen[c] = right
>         result = max(result, right - left + 1)
>     return result
> ```

> [!success] Complexity
> Time O(n) | Space O(min(n, alphabet)).

---

### Minimum Window Substring

> [!example] Problem
> Given strings s and t, return the minimum window substring of s such that every character in t (including duplicates) is included. LeetCode 76.

> [!info] Approach
> Variable-size sliding window with a frequency map. Track `need` (char → count needed) and a `have` counter = number of chars whose window frequency meets the required count. Expand right, updating `have` when a char's window count reaches its needed count. When `have == len(need)`, try to shrink left to minimize window, updating result. Shrink left until the window is invalid again, then continue expanding.

> [!note]- Python Solution
> ```python
> def min_window(s, t):
>     from collections import Counter
>     need = Counter(t)
>     have, total = 0, len(need)
>     freq = {}
>     left = 0
>     res = ""
>     for right, c in enumerate(s):
>         freq[c] = freq.get(c, 0) + 1
>         if c in need and freq[c] == need[c]:
>             have += 1
>         while have == total:
>             if not res or right - left + 1 < len(res):
>                 res = s[left:right + 1]
>             lc = s[left]
>             freq[lc] -= 1
>             if lc in need and freq[lc] < need[lc]:
>                 have -= 1
>             left += 1
>     return res
> ```

> [!success] Complexity
> Time O(|s| + |t|) | Space O(|t|).

---

### Find All Anagrams in a String

> [!example] Problem
> Given strings s and p, return all start indices of p's anagrams in s. LeetCode 438.

> [!info] Approach
> Fixed-size sliding window of length `len(p)`. Compare character frequency arrays. Track `matches` = number of characters (out of 26) where window frequency equals p frequency. Slide window one step: add right char, remove left char, update `matches` accordingly. When `matches == 26`, record start index.

> [!note]- Python Solution
> ```python
> def find_anagrams(s, p):
>     if len(p) > len(s):
>         return []
>     need = [0] * 26
>     have = [0] * 26
>     for c in p:
>         need[ord(c) - ord('a')] += 1
>     matches = sum(1 for i in range(26) if need[i] == 0)
>     result = []
>     k = len(p)
>
>     def update(c, delta):
>         nonlocal matches
>         idx = ord(c) - ord('a')
>         if have[idx] == need[idx]:
>             matches -= 1
>         have[idx] += delta
>         if have[idx] == need[idx]:
>             matches += 1
>
>     for i in range(k):
>         update(s[i], 1)
>     if matches == 26:
>         result.append(0)
>     for i in range(k, len(s)):
>         update(s[i], 1)
>         update(s[i - k], -1)
>         if matches == 26:
>             result.append(i - k + 1)
>     return result
> ```

> [!success] Complexity
> Time O(|s| + |p|) | Space O(1) (26-element arrays).

---

### Longest Substring with K Distinct Characters

> [!example] Problem
> Find the length of the longest substring containing at most K distinct characters. LeetCode 340.

> [!info] Approach
> Variable-size sliding window. Maintain a frequency map. Window is valid iff `len(freq) <= K`. Expand right always; when `K+1` distinct chars, shrink left until valid. When `freq[s[left]] == 0`, delete from map to keep distinct count accurate.

> [!note]- Python Solution
> ```python
> def length_of_longest_substring_k_distinct(s, k):
>     if k == 0:
>         return 0
>     freq = {}
>     left = result = 0
>     for right in range(len(s)):
>         freq[s[right]] = freq.get(s[right], 0) + 1
>         while len(freq) > k:
>             freq[s[left]] -= 1
>             if freq[s[left]] == 0:
>                 del freq[s[left]]
>             left += 1
>         result = max(result, right - left + 1)
>     return result
> ```

> [!success] Complexity
> Time O(n) | Space O(k).

---

## Anagram Check

---

### Valid Anagram

> [!example] Problem
> Given two strings s and t, return true if t is an anagram of s. LeetCode 242.

> [!info] Approach
> Two strings are anagrams iff they have identical character frequency distributions. Count characters in s (increment) and t (decrement) in the same array. If all 26 counts are 0, they're anagrams. Early exit if lengths differ.

> [!note]- Python Solution
> ```python
> def is_anagram(s, t):
>     if len(s) != len(t):
>         return False
>     count = [0] * 26
>     for a, b in zip(s, t):
>         count[ord(a) - ord('a')] += 1
>         count[ord(b) - ord('a')] -= 1
>     return all(c == 0 for c in count)
> ```

> [!success] Complexity
> Time O(n) | Space O(1).

---

## Palindrome

---

### Longest Palindromic Substring — Expand Around Center

> [!example] Problem
> Given a string s, return the longest palindromic substring. LeetCode 5.

> [!info] Approach
> Structural invariant: every palindrome has a center. There are `2n - 1` possible centers (n single characters + n-1 gaps). For each center, expand outward while `s[l] == s[r]`. Try both odd `(i, i)` and even `(i, i+1)` centers. Track the longest expansion. No extra space needed.

> [!note]- Python Solution
> ```python
> def longest_palindrome(s):
>     best_l = best_r = 0
>     for i in range(len(s)):
>         for l, r in [(i, i), (i, i + 1)]:   # odd and even centers
>             while l >= 0 and r < len(s) and s[l] == s[r]:
>                 l -= 1
>                 r += 1
>             if r - l - 1 > best_r - best_l:
>                 best_l, best_r = l + 1, r
>     return s[best_l:best_r]
> ```

> [!success] Complexity
> Time O(n²) | Space O(1).

> [!tip] Alternatives
> Manacher's algorithm: O(n) — useful if n > 10⁵ or explicitly asked. DP `dp[i][j]`: O(n²) time and space — no benefit over expand-around-center.

---

### Palindromic Substrings — Count

> [!example] Problem
> Given a string s, return the number of palindromic substrings in it. LeetCode 647.

> [!info] Approach
> Same `2n - 1` centers as longest palindrome. For each center, count each valid expansion as one palindromic substring.

> [!note]- Python Solution
> ```python
> def count_substrings(s):
>     count = 0
>     for i in range(len(s)):
>         for l, r in [(i, i), (i, i + 1)]:
>             while l >= 0 and r < len(s) and s[l] == s[r]:
>                 count += 1
>                 l -= 1
>                 r += 1
>     return count
> ```

> [!success] Complexity
> Time O(n²) | Space O(1).

---

### Valid Palindrome II

> [!example] Problem
> Given a string s, return true if it can be a palindrome after deleting at most one character. LeetCode 680.

> [!info] Approach
> Two-pointer from both ends. When `s[l] != s[r]`, try skipping one character: check if `s[l+1..r]` or `s[l..r-1]` is a palindrome. If either is, return true.

> [!note]- Python Solution
> ```python
> def valid_palindrome(s):
>     def is_pal(l, r):
>         while l < r:
>             if s[l] != s[r]:
>                 return False
>             l += 1; r -= 1
>         return True
>
>     l, r = 0, len(s) - 1
>     while l < r:
>         if s[l] != s[r]:
>             return is_pal(l + 1, r) or is_pal(l, r - 1)
>         l += 1; r -= 1
>     return True
> ```

> [!success] Complexity
> Time O(n) | Space O(1).

---

## KMP Awareness

KMP (Knuth-Morris-Pratt) achieves O(n + m) pattern matching by preprocessing the pattern into an **LPS (Longest Proper Prefix which is also Suffix)** array. On mismatch at pattern position `j`, jump to `lps[j-1]` instead of restarting — the text pointer never moves backward.

**When it matters at Amazon**: string search problems that explicitly ask for O(n + m), or problems reducible to pattern matching (e.g., shortest palindrome, repeated string match).

**Key insight**: `lps[i]` = length of longest proper prefix of `pattern[0..i]` that is also a suffix. Build it in O(m); search in O(n).

```python
def build_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length, i = 0, 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps
```

---

### Shortest Palindrome (KMP application)

> [!example] Problem
> Given string s, find the shortest palindrome formed by adding characters in front of s. LeetCode 214.

> [!info] Approach
> We need the longest palindromic prefix of s. Concatenate `s + '#' + reverse(s)`. The LPS value at the last position = length of longest palindromic prefix. Prepend the reverse of the remaining suffix.

> [!note]- Python Solution
> ```python
> def shortest_palindrome(s):
>     rev = s[::-1]
>     t = s + "#" + rev
>     lps = [0] * len(t)
>     for i in range(1, len(t)):
>         j = lps[i - 1]
>         while j > 0 and t[i] != t[j]:
>             j = lps[j - 1]
>         if t[i] == t[j]:
>             j += 1
>         lps[i] = j
>     return rev[:len(s) - lps[-1]] + s
> ```

> [!success] Complexity
> Time O(n) | Space O(n).

---

## Rabin-Karp Awareness

Rabin-Karp uses a **rolling hash** to compare a sliding window against the pattern in O(1) per step. Useful when KMP implementation is verbose or for multi-pattern search (hash all patterns into a set, O(1) lookup per window).

**Complexity**: O(n + m) average, O(nm) worst case (hash collisions). Always verify character-by-character on hash match to rule out collisions.

**Rolling hash formula**: `hash(new) = (hash(old) - text[i] * BASE^(m-1)) * BASE + text[i+m]`

**When to prefer over KMP**: simpler code acceptable, or searching for multiple patterns simultaneously.

---

## String DP (Bonus — Amazon Frequently Tests)

---

### Regular Expression Matching (LC 10)

> [!info] Approach
> `dp[i][j]` = True if `s[:i]` matches `p[:j]`.
> - `'.'` matches any single char.
> - `'*'` matches zero or more of the preceding element.
> - If `p[j-1] == '*'`: `dp[i][j] = dp[i][j-2]` (zero uses) OR `dp[i-1][j]` if `p[j-2]` matches `s[i-1]`.

> [!note]- Python Solution
> ```python
> def is_match(s, p):
>     m, n = len(s), len(p)
>     dp = [[False] * (n + 1) for _ in range(m + 1)]
>     dp[0][0] = True
>     for j in range(2, n + 1):
>         if p[j - 1] == '*':
>             dp[0][j] = dp[0][j - 2]
>     for i in range(1, m + 1):
>         for j in range(1, n + 1):
>             if p[j - 1] in {s[i - 1], '.'}:
>                 dp[i][j] = dp[i - 1][j - 1]
>             elif p[j - 1] == '*':
>                 dp[i][j] = dp[i][j - 2]
>                 if p[j - 2] in {s[i - 1], '.'}:
>                     dp[i][j] = dp[i][j] or dp[i - 1][j]
>     return dp[m][n]
> ```

> [!success] Complexity
> Time O(m·n) | Space O(m·n), reducible to O(n) with rolling row.

---

### Distinct Subsequences (LC 115)

> [!info] Approach
> `dp[i][j]` = number of ways to form `t[:j]` from `s[:i]`.
> - If `s[i-1] == t[j-1]`: `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]` (use or skip).
> - Else: `dp[i][j] = dp[i-1][j]` (skip).

> [!note]- Python Solution
> ```python
> def num_distinct(s, t):
>     m, n = len(s), len(t)
>     dp = [0] * (n + 1)
>     dp[0] = 1
>     for i in range(1, m + 1):
>         for j in range(n, 0, -1):
>             if s[i - 1] == t[j - 1]:
>                 dp[j] += dp[j - 1]
>     return dp[n]
> ```

> [!success] Complexity
> Time O(m·n) | Space O(n).

---

## See Also

[[string]] | [[sliding-window]] | [[dynamic-programming]] | [[trie]]
