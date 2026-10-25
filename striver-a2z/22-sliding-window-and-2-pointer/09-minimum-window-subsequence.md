---
module: striver-a2z/22-sliding-window-and-2-pointer
lesson: 9
topic: Minimum Window Subsequence
difficulty: Hard
source: https://takeuforward.org/learning/dsa/minimum-window-subsequence?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, two-pointers, strings, hard]
---
# 9. Minimum Window Subsequence

← [Minimum Window Substring](08-minimum-window-substring.md) · [Part 22 index](README.md) · Next → [Number of Substrings Containing All Three Characters](10-number-of-substrings-containing-all-three-characters.md)

> [!abstract] Problem at a glance
> **Task:** Shortest substring of `s1` that contains `s2` as a subsequence (leftmost if tied).
> **Key insight:** Scan forward matching `s2` in order; when the last character matches at `r`, scan **backwards** from `r` matching `s2` in reverse to find the latest start `l`. That gives the shortest window ending at `r`. Restart the forward scan at `l + 1`.
> **Difficulty:** Hard · **Pattern:** Forward match, backward shrink · **Also on:** [LC 727](https://leetcode.com/problems/minimum-window-subsequence/) (premium)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-window-subsequence?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: every start](#3-brute-force-every-start) · [4. Forward match + backward shrink](#4-forward-match--backward-shrink) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given strings `s1` and `s2`, return the minimum contiguous substring of `s1` such that `s2` is a subsequence of it. If there is no such window, return `""`. If there are several minimum-length windows, return the one with the left-most start.

| Input | Output | Why |
|---|---|---|
| `s1 = "abcdebdde", s2 = "bde"` | `"bcde"` | "bdde" also works but starts later |
| `s1 = "jmeqksfrsdcmsiwvaovztaqenprpvnbstl", s2 = "u"` | `""` |  |

**Constraints:** `1 ≤ s1.length ≤ 2·10⁴`, `1 ≤ s2.length ≤ 100`, lowercase letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: every start | greedy-match s2 from each start | O(n²) | O(1) |
| Forward match + backward shrink | find an end, walk back to the tightest start | O(n·m) | O(1) |

> [!tip] Interview angle
> Not a counting window: order matters, so the `need` counter doesn't work. The forward/backward scan is the expected answer; mention the O(n·m) DP as an alternative.

---

## 3. Brute force: every start

**Intuition.** For each start where `s1[i] == s2[0]`, match `s2` greedily forward. The earliest finishing index gives the shortest window from that start.

```python
def min_window_subseq_brute(s1, s2):
    best = ""
    for i in range(len(s1)):
        if s1[i] != s2[0]:
            continue
        j = 0
        for r in range(i, len(s1)):
            if s1[r] == s2[j]:
                j += 1
                if j == len(s2):
                    if not best or r - i + 1 < len(best):
                        best = s1[i:r + 1]
                    break
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Forward match + backward shrink

**Intuition.** Walk `r` forward advancing `j` on matches. When `j == m`, walk `l` back from `r` matching `s2` from its end to its start; the stop position is the tightest start for this end. Record `[l, r]`, then resume the forward scan from `l + 1` with `j = 0`.

**Algorithm**

1. `i = 0`, `best = (∞, −1)`.
2. Forward: from `i`, match `s2[0..m−1]`; let `r` be where the last match happens (stop if none).
3. Backward: from `r`, match `s2[m−1..0]`; let `l` be where `s2[0]` matches.
4. Update best with `(r − l + 1, l)` (strict `<` keeps the leftmost); set `i = l + 1`; repeat.

**Dry run** — abcdebdde / bde: forward finds end r=4 ('e') → backward: e(4), d(3), b(1) → l=1 → "bcde" (4). Resume at 2: forward reaches r=8 → backward e(8), d(7), b(5) → "bdde" (4), not shorter. Answer "bcde".

**C++**
```cpp
string minWindowSubsequence(string s1, string s2) {
    int n = s1.size(), m = s2.size(), bestLen = INT_MAX, start = -1, i = 0;
    while (i < n) {
        int j = 0;
        while (i < n) {
            if (s1[i] == s2[j] && ++j == m) break;
            i++;
        }
        if (i == n) break;
        int r = i;
        j = m - 1;
        while (j >= 0) {
            if (s1[i] == s2[j]) j--;
            i--;
        }
        int l = i + 1;
        if (r - l + 1 < bestLen) { bestLen = r - l + 1; start = l; }
        i = l + 1;
    }
    return start == -1 ? "" : s1.substr(start, bestLen);
}
```

**Java**
```java
static String minWindowSubsequence(String s1, String s2) {
    int n = s1.length(), m = s2.length(), bestLen = Integer.MAX_VALUE, start = -1, i = 0;
    while (i < n) {
        int j = 0;
        while (i < n) {
            if (s1.charAt(i) == s2.charAt(j) && ++j == m) break;
            i++;
        }
        if (i == n) break;
        int r = i;
        j = m - 1;
        while (j >= 0) {
            if (s1.charAt(i) == s2.charAt(j)) j--;
            i--;
        }
        int l = i + 1;
        if (r - l + 1 < bestLen) { bestLen = r - l + 1; start = l; }
        i = l + 1;
    }
    return start == -1 ? "" : s1.substring(start, start + bestLen);
}
```

**Python**
```python
def min_window_subsequence(s1, s2):
    n, m = len(s1), len(s2)
    best_len, start, i = float("inf"), -1, 0
    while i < n:
        j = 0
        while i < n:
            if s1[i] == s2[j]:
                j += 1
                if j == m:
                    break
            i += 1
        if i == n:
            break
        r, j = i, m - 1
        while j >= 0:
            if s1[i] == s2[j]:
                j -= 1
            i -= 1
        l = i + 1
        if r - l + 1 < best_len:
            best_len, start = r - l + 1, l
        i = l + 1
    return "" if start == -1 else s1[start:start + best_len]
```

**Complexity:** time **O(n·m)**, space **O(1)** — each backward scan covers at most the window just found, and each restart begins one past the previous start; the standard bound is O(n·m) time, O(1) extra space.

---

## Edge cases

- `s2` longer than `s1` → "".
- `s2` one character → that character if present.
- Ties → leftmost start (strict `<`).

---

## Common mistakes

1. Using the Minimum Window Substring counter, which ignores order.
2. Restarting at `r + 1` instead of `l + 1`, which skips overlapping windows.
3. Updating best with `≤`, which returns a later window on ties.

---

## Follow-ups

1. DP formulation.
2. Many queries `s2` on the same `s1`.

<details><summary>Answer sketches</summary>

**#1:** `dp[j][i]` = latest start such that `s2[0..j]` is a subsequence of `s1[start..i]`; O(n·m) time, O(n) space with rolling rows.

**#2:** Precompute `next[i][c]` (next occurrence of c at or after i) for O(m) forward matching per start.
</details>

---

## Flashcards

**Min Window Subsequence technique?** #flashcard
Forward-scan to the end of a match, backward-scan to the tightest start, restart at start + 1.

**Why doesn't the Min Window Substring counter work here?** #flashcard
It counts characters but ignores their order; a subsequence needs order.

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../04-practice/algorithms/04-sliding-window.md)
