# String & Palindrome DP

String DP problems: palindromic structures, regex matching, and transformations. For the broader DP guide see [README.md](README.md).

---

## Theory & Mental Model

**Two flavors of string DP:**
1. **Single-string palindrome DP** — `dp[i][j]` represents a property of `s[i..j]`. Fill by increasing length of the interval.
2. **Two-string matching DP** — `dp[i][j]` represents matching/transforming `s1[:i]` and `s2[:j]`. Fill row by row.

**Palindrome key insight:** `s[i..j]` is a palindrome iff `s[i] == s[j]` AND `s[i+1..j-1]` is a palindrome.

---

## Part 1 — Palindrome Problems

### 1.1 Longest Palindromic Substring (LeetCode 5)

**State:** `dp[i][j]` = True if `s[i..j]` is a palindrome.

**Recurrence:** `dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]` (for `j - i >= 2`).

**Fill order:** By increasing length (short intervals before long).

```python
def longest_palindromic_substring(s: str) -> str:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1

    # All substrings of length 1 are palindromes
    for i in range(n):
        dp[i][i] = True

    # Length 2
    for i in range(n - 1):
        if s[i] == s[i+1]:
            dp[i][i+1] = True
            start, max_len = i, 2

    # Length 3 and above
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i+1][j-1]:
                dp[i][j] = True
                if length > max_len:
                    start, max_len = i, length

    return s[start:start + max_len]
```

> [!TIP]
> **Manacher's Algorithm** finds all palindromes in O(N) — much faster than O(N²) DP. For interviews, mention Manacher's as the optimal solution but implement the O(N²) DP unless asked for optimal. The "expand around center" approach is O(N²) time, O(1) space — preferred over the O(N²) space DP table.

```python
def longest_palindromic_substring_expand(s: str) -> str:
    def expand(l: int, r: int) -> tuple:
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return l + 1, r - 1

    start, end = 0, 0
    for i in range(len(s)):
        l1, r1 = expand(i, i)       # odd length
        l2, r2 = expand(i, i + 1)  # even length
        if r1 - l1 > end - start: start, end = l1, r1
        if r2 - l2 > end - start: start, end = l2, r2
    return s[start:end+1]
```

---

### 1.2 Longest Palindromic Subsequence (LeetCode 516)

**State:** `dp[i][j]` = length of longest palindromic subsequence in `s[i..j]`.

**Recurrence:**
- If `s[i] == s[j]`: `dp[i][j] = 2 + dp[i+1][j-1]`
- Else: `dp[i][j] = max(dp[i+1][j], dp[i][j-1])`

```python
def longest_palindromic_subsequence(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1   # single char is a palindromic subseq of length 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = 2 + (dp[i+1][j-1] if length > 2 else 0)
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])

    return dp[0][n-1]

# Equivalent: LCS(s, reversed(s))
def lps_via_lcs(s: str) -> int:
    t = s[::-1]
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = dp[i-1][j-1]+1 if s[i-1]==t[j-1] else max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

---

### 1.3 Minimum Insertions / Deletions for Palindrome

- **Min insertions to make palindrome (LeetCode 1312):** `len(s) - LPS(s)`
- **Min deletions to make palindrome:** same formula — `len(s) - LPS(s)`

```python
def min_insertions_palindrome(s: str) -> int:
    return len(s) - longest_palindromic_subsequence(s)
```

> [!TIP]
> Both insertion and deletion have the same minimum count — because each deletion corresponds to one insertion in the reverse direction. The LPS characters stay; all non-LPS characters need one operation each.

---

### 1.4 Count Palindromic Substrings (LeetCode 647)

**State:** same `dp[i][j]` palindrome table; count all True cells.

```python
def count_substrings(s: str) -> int:
    n = len(s)
    count = 0

    # Expand-around-center: O(N²) time, O(1) space
    def expand_count(l: int, r: int) -> int:
        cnt = 0
        while l >= 0 and r < n and s[l] == s[r]:
            cnt += 1; l -= 1; r += 1
        return cnt

    for i in range(n):
        count += expand_count(i, i)     # odd centers
        count += expand_count(i, i+1)  # even centers
    return count
```

---

### 1.5 Palindrome Partitioning II — Minimum Cuts (LeetCode 132)

**Goal:** Minimum number of cuts so every part is a palindrome.

**Approach:** Precompute `is_pal[i][j]` in O(N²); then `cut[i]` = min cuts for `s[:i+1]`.

```python
def min_cut(s: str) -> int:
    n = len(s)
    # Precompute palindrome table
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            is_pal[i][j] = (s[i] == s[j]) and (j - i < 2 or is_pal[i+1][j-1])

    # cut[i] = min cuts for s[:i+1]
    cut = list(range(n))  # worst case: cut before every char
    for i in range(1, n):
        if is_pal[0][i]:
            cut[i] = 0         # entire prefix is a palindrome
            continue
        for j in range(1, i + 1):
            if is_pal[j][i]:
                cut[i] = min(cut[i], cut[j-1] + 1)
    return cut[n-1]
```

---

### 1.6 Palindrome Partitioning III (LeetCode 1278)

**Problem:** Partition string into exactly K palindromes, changing minimum characters.

**State:** `dp[i][k]` = min changes to partition `s[:i]` into `k` palindromes.

```python
def palindrome_partition_iii(s: str, k: int) -> int:
    n = len(s)

    def cost(l: int, r: int) -> int:
        """Min chars to change s[l..r] to a palindrome."""
        changes = 0
        while l < r:
            if s[l] != s[r]: changes += 1
            l += 1; r -= 1
        return changes

    # Memoize cost
    from functools import lru_cache
    cost = lru_cache(maxsize=None)(cost)

    # dp[i][j] = min changes for s[:i] split into j parts
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            for m in range(j - 1, i):
                dp[i][j] = min(dp[i][j], dp[m][j-1] + cost(m, i-1))
    return dp[n][k]
```

---

## Part 2 — Pattern Matching DP

### 2.1 Regular Expression Matching (LeetCode 10)

**Pattern:** `.` matches any single char. `*` matches zero or more of the preceding char.

**State:** `dp[i][j]` = True if `s[:i]` matches `p[:j]`.

```python
def is_match_regex(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # p[:j] matches empty string only if it's like "a*b*c*"
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]   # '*' = zero occurrences of preceding

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # Zero occurrences of p[j-2]
                dp[i][j] = dp[i][j-2]
                # One or more: p[j-2] must match s[i-1]
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]  # single char match

    return dp[m][n]
```

> [!CAUTION]
> **`*` means zero OR MORE of the preceding char.** `*` alone is illegal. Always look at `p[j-2]` when `p[j-1] == '*'`. The "zero occurrences" case (`dp[i][j-2]`) is what makes this tricky — it skips both `*` AND the preceding char.

---

### 2.2 Wildcard Matching (LeetCode 44)

**Pattern:** `?` matches any single char. `*` matches any sequence (including empty).

**State:** `dp[i][j]` = True if `s[:i]` matches `p[:j]`.

```python
def is_match_wildcard(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Leading '*' can match empty string
    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[i][j] = dp[i-1][j] or dp[i][j-1]
                #           use '*' to match s[i]  | '*' matches empty
            elif p[j-1] == '?' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]

    return dp[m][n]
```

> [!TIP]
> **Regex vs Wildcard:** In regex, `*` requires a preceding char to repeat. In wildcard, `*` is standalone and matches any sequence. The transitions differ: regex checks `p[j-2]`; wildcard uses `dp[i-1][j] or dp[i][j-1]`.

---

### 2.3 Distinct Subsequences (LeetCode 115)

**Problem:** Count distinct ways `s` contains `t` as a subsequence.

**Recurrence:**
- `s[i] == t[j]`: `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]` (use or skip `s[i]`)
- `s[i] != t[j]`: `dp[i][j] = dp[i-1][j]` (must skip `s[i]`)

```python
def num_distinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1   # empty t is always a subsequence

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j]                          # skip s[i]
            if s[i-1] == t[j-1]:
                dp[i][j] += dp[i-1][j-1]                   # use s[i]
    return dp[m][n]
```

---

### 2.4 Interleaving String (LeetCode 97)

**Problem:** Can `s3` be formed by interleaving `s1` and `s2`?

**State:** `dp[i][j]` = can `s1[:i] + s2[:j]` form `s3[:i+j]`.

```python
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3): return False
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] and s1[i-1] == s3[i-1]
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] and s2[j-1] == s3[j-1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or \
                       (dp[i][j-1] and s2[j-1] == s3[i+j-1])
    return dp[m][n]
```

---

## Interview Questions — Logic & Trickiness

| Problem | LC # | Pattern | Click Moment | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| **Longest Palindromic Substring** | 5 | Interval / Expand | `is_pal[i][j]` filled by length | Expand-around-center is O(1) space; prefer it |
| **Longest Palindromic Subsequence** | 516 | Interval DP | LCS(s, rev(s)) shortcut | Single chars: `dp[i][i] = 1` base case |
| **Min Insertions for Palindrome** | 1312 | LPS reduction | `len - LPS` | Equivalent to min deletions |
| **Count Palindromic Substrings** | 647 | Expand-center | Count from each center | 2n-1 centers for odd and even palindromes |
| **Palindrome Partitioning II** | 132 | Interval + linear | Precompute `is_pal`; linear `cut[]` | If `is_pal[0][i]`, no cut needed for prefix |
| **Palindrome Partitioning III** | 1278 | 2D DP + cost | `cost(l, r)` = chars to fix | `cost` function is O(N) per call; memoize |
| **Regular Expression Matching** | 10 | 2D string DP | `*` = zero-or-more of PRECEDING char | Base case: leading `a*b*` matches `""` |
| **Wildcard Matching** | 44 | 2D string DP | `*` = any sequence | `dp[i-1][j]`: `*` matches s[i]; `dp[i][j-1]`: `*` empty |
| **Distinct Subsequences** | 115 | 2D DP, counting | Add ways when chars match | `dp[i][0] = 1` (empty t always subseq) |
| **Interleaving String** | 97 | 2D DP, bool | Two sources for each `s3` char | Check `m+n == len(s3)` first |

---

## Key Differences: Substring vs Subsequence

| Property | Substring | Subsequence |
| :--- | :--- | :--- |
| Contiguous? | Yes | No |
| DP reset on mismatch? | Yes (`dp[i][j] = 0`) | No (`dp[i][j] = max(up, left)`) |
| Answer | `max over all dp[i][j]` | `dp[m][n]` |
| Palindrome: expand? | Yes — expand from center | No — interval DP or LCS(s, rev(s)) |

---

## See also

- [README.md](README.md) — LCS family overview
- [dp-aditya-verma.md](dp-aditya-verma.md) — LCS pattern full code
- [questions-bank.md](questions-bank.md) — String DP drill problems
