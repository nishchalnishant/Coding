---
module: striver-a2z/18-recursion
lesson: 16
topic: Palindrome Partitioning
difficulty: Medium
source: https://takeuforward.org/learning/dsa/palindrome-partitioning?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking, string, dp]
---
# 16. Palindrome Partitioning

← [Letter Combinations of a Phone Number](15-letter-combinations-of-a-phone-number.md) · [Part 18 index](README.md) · Next → [Word Search](17-word-search.md)

> [!abstract] Problem at a glance
> **Task:** Return every way to split a string into substrings that are all palindromes.
> **Key insight:** Recurse on the start index: for every end `e ≥ start` where `s[start..e]` is a palindrome, cut there and recurse on `e + 1`. Precompute `isPal[i][j]` in O(n²) so each check is O(1).
> **Difficulty:** Medium · **Pattern:** Partition backtracking (choose the next cut) · **Also on:** [LC 131](https://leetcode.com/problems/palindrome-partitioning/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/palindrome-partitioning?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Backtracking with on-the-fly palindrome check](#3-backtracking-with-on-the-fly-palindrome-check) · [4. Backtracking + palindrome table](#4-backtracking--palindrome-table) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s`, partition it so that every substring of the partition is a palindrome. Return all possible palindrome partitions, in any order.

| Input | Output | Why |
|---|---|---|
| `s = "aab"` | `[["a", "a", "b"], ["aa", "b"]]` |  |
| `s = "a"` | `[["a"]]` |  |

**Constraints:** `1 ≤ |s| ≤ 16`, lowercase letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Backtracking with on-the-fly palindrome check | for end in start..n−1: if s[start..end] is a palindrome, cut and recurse | O(n · 2ⁿ) | O(n) |
| Backtracking + palindrome table | isPal[i][j] DP, then the same backtracking with O(1) checks | O(n · 2ⁿ) | O(n²) |

> [!tip] Interview angle
> The "partition" family template: the recursion variable is the start of the remaining suffix, the loop chooses where the next piece ends. Worst case is `"aaaa…"` with 2ⁿ⁻¹ partitions, so O(n · 2ⁿ). Follow-up is Palindrome Partitioning II (min cuts) — a 1D DP, not backtracking.

---

## 3. Backtracking with on-the-fly palindrome check

**Intuition.** Check each candidate piece with two pointers. Each check is O(n), each leaf is O(n) to copy — still O(n · 2ⁿ) overall, just a bigger constant.

```python
def partition_basic(s):
    out, cur = [], []
    def go(start):
        if start == len(s):
            out.append(cur[:])
            return
        for end in range(start, len(s)):
            piece = s[start:end + 1]
            if piece == piece[::-1]:
                cur.append(piece)
                go(end + 1)
                cur.pop()
    go(0)
    return out
```

**Complexity:** time **O(n · 2ⁿ)**, space **O(n)**.

---

## 4. Backtracking + palindrome table

**Intuition.** `isPal[i][j] = s[i] == s[j] && (j − i < 2 || isPal[i+1][j−1])`, filled for i from n−1 down. The backtracking then never rescans characters.

**Algorithm**

1. Fill `isPal` (i descending, j ascending).
2. `go(start)`: if start == n → record.
3. For end = start … n−1: if isPal[start][end] → push s[start..end], `go(end + 1)`, pop.

**Dry run** — "aab": start 0 → "a" → start 1 → "a" → "b" ✓; start 1 → "ab" ✗. start 0 → "aa" → "b" ✓. "aab" ✗.

**C++**
```cpp
void go(int start, const string& s, vector<vector<bool>>& pal, vector<string>& cur, vector<vector<string>>& out) {
    int n = s.size();
    if (start == n) { out.push_back(cur); return; }
    for (int end = start; end < n; end++) {
        if (!pal[start][end]) continue;
        cur.push_back(s.substr(start, end - start + 1));
        go(end + 1, s, pal, cur, out);
        cur.pop_back();
    }
}
vector<vector<string>> partition(string s) {
    int n = s.size();
    vector<vector<bool>> pal(n, vector<bool>(n, false));
    for (int i = n - 1; i >= 0; i--)
        for (int j = i; j < n; j++)
            pal[i][j] = s[i] == s[j] && (j - i < 2 || pal[i + 1][j - 1]);
    vector<vector<string>> out;
    vector<string> cur;
    go(0, s, pal, cur, out);
    return out;
}
```

**Java**
```java
static void go(int start, String s, boolean[][] pal, List<String> cur, List<List<String>> out) {
    int n = s.length();
    if (start == n) { out.add(new ArrayList<>(cur)); return; }
    for (int end = start; end < n; end++) {
        if (!pal[start][end]) continue;
        cur.add(s.substring(start, end + 1));
        go(end + 1, s, pal, cur, out);
        cur.remove(cur.size() - 1);
    }
}
static List<List<String>> partition(String s) {
    int n = s.length();
    boolean[][] pal = new boolean[n][n];
    for (int i = n - 1; i >= 0; i--)
        for (int j = i; j < n; j++)
            pal[i][j] = s.charAt(i) == s.charAt(j) && (j - i < 2 || pal[i + 1][j - 1]);
    List<List<String>> out = new ArrayList<>();
    go(0, s, pal, new ArrayList<>(), out);
    return out;
}
```

**Python**
```python
def partition(s):
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])
    out, cur = [], []
    def go(start):
        if start == n:
            out.append(cur[:])
            return
        for end in range(start, n):
            if pal[start][end]:
                cur.append(s[start:end + 1])
                go(end + 1)
                cur.pop()
    go(0)
    return out
```

**Complexity:** time **O(n · 2ⁿ)**, space **O(n²)** — ≤ 2ⁿ⁻¹ partitions, O(n) copy each; O(n²) table.

---

## Edge cases

- All same letters → 2ⁿ⁻¹ partitions.
- No repeated letters → only single characters.

---

## Common mistakes

1. Filling `isPal` with i ascending — `pal[i+1][j−1]` not ready yet.
2. Recursing on `start + 1` instead of `end + 1`.

---

## Follow-ups

1. Minimum cuts (LC 132).
2. Count palindromic substrings (LC 647).

<details><summary>Answer sketches</summary>

**#1:** `cut[j] = min(cut[i − 1] + 1)` over palindromes s[i..j]; O(n²).

**#2:** Expand around 2n − 1 centres.
</details>

---

## Flashcards

**Partition backtracking: what is the recursion variable?** #flashcard
The start index of the unpartitioned suffix; the loop picks the end of the next piece.

**isPal recurrence?** #flashcard
s[i] == s[j] and (j − i < 2 or isPal[i+1][j−1]), i descending.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../04-practice/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../04-practice/algorithms/12-backtracking.md)
