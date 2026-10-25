---
module: striver-a2z/22-sliding-window-and-2-pointer
lesson: 8
topic: Minimum Window Substring
difficulty: Hard
source: https://takeuforward.org/learning/dsa/minimum-window-substring-?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, hashing, strings, hard]
---
# 8. Minimum Window Substring

← [Longest Repeating Character Replacement](07-longest-repeating-character-replacement.md) · [Part 22 index](README.md) · Next → [Minimum Window Subsequence](09-minimum-window-subsequence.md)

> [!abstract] Problem at a glance
> **Task:** Smallest substring of `s` that contains every character of `t` (with multiplicity).
> **Key insight:** Expand right until the window covers `t`, then shrink left as long as it still covers, recording each covering window. Track coverage with one integer, `need` = characters of `t` still missing, so the cover test is O(1).
> **Difficulty:** Hard · **Pattern:** Expand to valid, shrink to minimal · **Also on:** [LC 76](https://leetcode.com/problems/minimum-window-substring/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-window-substring-?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: every substring](#3-brute-force-every-substring) · [4. Window with a deficit counter](#4-window-with-a-deficit-counter) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return `""`. The answer is unique when it exists.

| Input | Output | Why |
|---|---|---|
| `s = "ADOBECODEBANC", t = "ABC"` | `"BANC"` |  |
| `s = "a", t = "aa"` | `""` | t needs two a's |

**Constraints:** `1 ≤ s.length, t.length ≤ 10⁵`, upper- and lowercase English letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: every substring | check coverage for each (i, j) | O(n²·Σ) | O(Σ) |
| Window with a deficit counter | expand until need == 0, then shrink | O(|s| + |t|) | O(Σ) |

> [!tip] Interview angle
> The hardest standard window. Explain the `need` counter: decrement it only when a character fills a real deficit (`cnt[c] > 0` before decrementing); increment only when removing a character creates one.

---

## 3. Brute force: every substring

**Intuition.** For each start, extend right with counts until it covers `t`; that's the shortest window from this start. Keep the overall shortest.

```python
from collections import Counter
def min_window_brute(s, t):
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        have = Counter()
        for j in range(i, len(s)):
            have[s[j]] += 1
            if all(have[c] >= v for c, v in need.items()):
                if not best or j - i + 1 < len(best):
                    best = s[i:j + 1]
                break
    return best
```

**Complexity:** time **O(n²·Σ)**, space **O(Σ)**.

---

## 4. Window with a deficit counter

**Intuition.** `cnt[c]` = how many more of `c` the window needs (negative = surplus). `need` = total still missing. Expanding with `c`: if `cnt[c] > 0`, `need -= 1`; then `cnt[c] -= 1`. While `need == 0`, record the window, then remove `s[l]`: `cnt[s[l]] += 1`, and if it becomes positive, `need += 1`.

**Algorithm**

1. `cnt` from `t`, `need = len(t)`, `l = 0`, `best = (∞, 0)`.
2. For each `r`: if `cnt[s[r]] > 0`, `need -= 1`; `cnt[s[r]] -= 1`.
3. While `need == 0`: update best with `(r − l + 1, l)`; `cnt[s[l]] += 1`; if `cnt[s[l]] > 0`, `need += 1`; `l += 1`.
4. Return `s[start:start+len]` or `""`.

**Dry run** — ADOBECODEBANC / ABC: first cover at r=5 "ADOBEC" (6) → shrinking drops A → need=1 → expand to r=10 (A) → shrink to "CODEBA" (6) → r=12 (C) → shrink to "BANC" (4).

**C++**
```cpp
string minWindow(string s, string t) {
    vector<int> cnt(128, 0);
    for (char c : t) cnt[c]++;
    int need = t.size(), l = 0, bestLen = INT_MAX, start = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        if (cnt[s[r]]-- > 0) need--;
        while (need == 0) {
            if (r - l + 1 < bestLen) { bestLen = r - l + 1; start = l; }
            if (++cnt[s[l]] > 0) need++;
            l++;
        }
    }
    return bestLen == INT_MAX ? "" : s.substr(start, bestLen);
}
```

**Java**
```java
static String minWindow(String s, String t) {
    int[] cnt = new int[128];
    for (char c : t.toCharArray()) cnt[c]++;
    int need = t.length(), l = 0, bestLen = Integer.MAX_VALUE, start = 0;
    for (int r = 0; r < s.length(); r++) {
        if (cnt[s.charAt(r)]-- > 0) need--;
        while (need == 0) {
            if (r - l + 1 < bestLen) { bestLen = r - l + 1; start = l; }
            if (++cnt[s.charAt(l)] > 0) need++;
            l++;
        }
    }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(start, start + bestLen);
}
```

**Python**
```python
def min_window(s, t):
    cnt = {}
    for c in t:
        cnt[c] = cnt.get(c, 0) + 1
    need, l = len(t), 0
    best_len, start = float("inf"), 0
    for r, c in enumerate(s):
        if cnt.get(c, 0) > 0:
            need -= 1
        cnt[c] = cnt.get(c, 0) - 1
        while need == 0:
            if r - l + 1 < best_len:
                best_len, start = r - l + 1, l
            cnt[s[l]] += 1
            if cnt[s[l]] > 0:
                need += 1
            l += 1
    return "" if best_len == float("inf") else s[start:start + best_len]
```

**Complexity:** time **O(|s| + |t|)**, space **O(Σ)** — each index is added once and removed once; the cover test is `need == 0`.

---

## Edge cases

- `t` longer than `s` → "".
- Duplicate characters in `t`.
- Answer is the whole string.

---

## Common mistakes

1. Checking coverage by comparing two maps each step (O(Σ) per step, and easy to get wrong with duplicates).
2. Decrementing `need` for surplus characters (when `cnt[c] ≤ 0` already).
3. Recording the window after shrinking instead of before removing `s[l]`.

---

## Follow-ups

1. Characters of `t` must appear in order.
2. Return all minimal windows.

<details><summary>Answer sketches</summary>

**#1:** That's Minimum Window Subsequence — a different, two-pass or DP technique.

**#2:** Record every window with length == best during the shrink phase.
</details>

---

## Flashcards

**Min Window Substring: what does `need` count?** #flashcard
Characters of t (with multiplicity) still missing from the window.

**When does `need` change?** #flashcard
−1 when adding c fills a deficit (cnt[c] > 0 before); +1 when removing c creates one (cnt[c] > 0 after).

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../04-practice/algorithms/04-sliding-window.md)
