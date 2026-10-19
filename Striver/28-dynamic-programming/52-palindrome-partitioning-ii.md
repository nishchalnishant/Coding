---
module: striver/28-dynamic-programming
lesson: 52
topic: Palindrome partitioning II
difficulty: Hard
source: https://takeuforward.org/learning/dsa/palindrome-partitioning-ii-?category=mcm-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, partition-dp, palindrome, strings]
---
# 52. Palindrome partitioning II

← [Evaluate boolean expression to true](51-evaluate-boolean-expression-to-true.md) · [Part 28 index](README.md) · Next → [Partition array for maximum sum](53-partition-array-for-maximum-sum.md)

> [!abstract] Problem at a glance
> **Task:** Fewest cuts so every piece of `s` is a palindrome.
> **Key insight:** This is **front partitioning**, not interval DP. `f(i)` = minimum pieces for the suffix `s[i..]` = `1 + min f(j+1)` over `j ≥ i` where `s[i..j]` is a palindrome. Cuts = pieces − 1. Precompute `isPal[i][j]` in O(n²) so each check is O(1), giving O(n²) overall.
> **Difficulty:** Hard · **Pattern:** Front partition DP · **Also on:** LC 132
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/palindrome-partitioning-ii-?category=mcm-dp&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Front partition, palindrome check inline](#3-front-partition-palindrome-check-inline) · [4. Front partition + isPal table](#4-front-partition--ispal-table) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `s`, return the minimum number of cuts needed to partition it so every substring is a palindrome.

| Input | Output | Why |
|---|---|---|
| `"aab"` | `1` | aa | b |
| `"a"` | `0` |  |
| `"bababcbadcede"` | `4` | bab | abcba | d | c | ede |

**Constraints:** `1 ≤ |s| ≤ 2000`, lowercase.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Front partition, palindrome check inline | f(i) = 1 + min f(j+1) | O(n³) | O(n) |
| Front partition + isPal table | O(1) palindrome lookups | O(n²) | O(n²) |

> [!tip] Interview angle
> Note that the MCM-style O(n³) `f(i, j)` works but is too slow for n = 2000. The front-partition view ("where does the first piece end?") is the intended solution. Build the palindrome table with `isPal[i][j] = s[i] == s[j] && isPal[i+1][j−1]`.

---

## 3. Front partition, palindrome check inline

**Intuition.** Each palindrome check is O(n), giving O(n³) total.

```python
def pp_inline(s):
    n = len(s)
    dp = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        dp[i] = min(1 + dp[j + 1] for j in range(i, n) if s[i:j + 1] == s[i:j + 1][::-1])
    return dp[0] - 1
```

**Complexity:** time **O(n³)**, space **O(n)**.

---

## 4. Front partition + isPal table

**Intuition.** Fill `isPal` with `i` descending, then compute `dp[i]` in the same loop.

**Algorithm**

1. For `i = n−1..0`, `j = i..n−1`: `isPal[i][j] = s[i] == s[j] && (j − i < 2 || isPal[i+1][j−1])`.
2. In the same `i` loop: `dp[i] = min over palindromic s[i..j]` of `1 + dp[j+1]`, with `dp[n] = 0`.
3. Return `dp[0] − 1`.

**Dry run** — "aab": dp[2] = 1, dp[1] = 2 (a|b), dp[0] = 1 + dp[2] = 2 ("aa" + "b") → 1 cut.

**C++**
```cpp
int minCut(string s) {
    int n = s.size();
    vector<vector<bool>> isPal(n, vector<bool>(n, false));
    vector<int> dp(n + 1, 0);
    for (int i = n - 1; i >= 0; i--) {
        dp[i] = INT_MAX;
        for (int j = i; j < n; j++) {
            if (s[i] == s[j] && (j - i < 2 || isPal[i + 1][j - 1])) {
                isPal[i][j] = true;
                dp[i] = min(dp[i], 1 + dp[j + 1]);
            }
        }
    }
    return dp[0] - 1;
}
```

**Java**
```java
static int minCut(String s) {
    int n = s.length();
    boolean[][] isPal = new boolean[n][n];
    int[] dp = new int[n + 1];
    for (int i = n - 1; i >= 0; i--) {
        dp[i] = Integer.MAX_VALUE;
        for (int j = i; j < n; j++) {
            if (s.charAt(i) == s.charAt(j) && (j - i < 2 || isPal[i + 1][j - 1])) {
                isPal[i][j] = true;
                dp[i] = Math.min(dp[i], 1 + dp[j + 1]);
            }
        }
    }
    return dp[0] - 1;
}
```

**Python**
```python
def min_cut(s):
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    dp = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        dp[i] = n + 1
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True
                dp[i] = min(dp[i], 1 + dp[j + 1])
    return dp[0] - 1
```

**Complexity:** time **O(n²)**, space **O(n²)** — n² table cells, each O(1).

---

## Edge cases

- Already a palindrome: 0.
- All distinct: n − 1.

---

## Common mistakes

1. Returning pieces instead of cuts (off by one).
2. O(n³) interval DP for n = 2000.

---

## Follow-ups

1. List all palindrome partitions (LC 131)?
2. O(n) extra space?

<details><summary>Answer sketches</summary>

**#1:** Backtracking with the same `isPal` table.

**#2:** Expand around each centre, updating `cuts[r+1] = min(cuts[r+1], cuts[l] + 1)`.
</details>

---

## Flashcards

**Palindrome partitioning II state?** #flashcard
dp[i] = min pieces for suffix s[i..]; answer dp[0] − 1.

**Why front partition, not MCM?** #flashcard
O(n²) vs O(n³); only the first piece's end matters.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
