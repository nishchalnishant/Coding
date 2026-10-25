---
module: striver-a2z/22-sliding-window-and-2-pointer
lesson: 7
topic: Longest Repeating Character Replacement
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-repeating-character-replacement?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, strings, counting]
---
# 7. Longest Repeating Character Replacement

← [Longest Substring With At Most K Distinct Characters](06-longest-substring-with-at-most-k-distinct-characters.md) · [Part 22 index](README.md) · Next → [Minimum Window Substring](08-minimum-window-substring.md)

> [!abstract] Problem at a glance
> **Task:** Longest substring that can be made of one repeated letter by changing at most `k` characters.
> **Key insight:** A window is fixable iff `len − maxFreq ≤ k`: keep the most common letter, change the rest. `maxFreq` never needs to decrease: the answer only grows when a window with a larger `maxFreq` appears, so a stale (too high) value only stops the window from shrinking when it shouldn't grow anyway.
> **Difficulty:** Medium · **Pattern:** Variable window, validity = len − maxFreq ≤ k · **Also on:** [LC 424](https://leetcode.com/problems/longest-repeating-character-replacement/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-repeating-character-replacement?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: every substring](#3-brute-force-every-substring) · [4. Shrinking window, recompute max](#4-shrinking-window-recompute-max) · [5. Window with a stale maxFreq](#5-window-with-a-stale-maxfreq) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an uppercase string `s` and an integer `k`, you may change any character to any other uppercase letter at most `k` times. Return the length of the longest substring containing a single repeated letter after these operations.

| Input | Output | Why |
|---|---|---|
| `s = "ABAB", k = 2` | `4` | change both As or both Bs |
| `s = "AABABBA", k = 1` | `4` | "AABA" → "AAAA" |

**Constraints:** `1 ≤ s.length ≤ 10⁵`, `s` uppercase, `0 ≤ k ≤ s.length`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: every substring | check len − maxFreq ≤ k per substring | O(n²) | O(Σ) |
| Shrinking window, recompute max | while invalid: shrink, max(cnt) | O(26·n) | O(Σ) |
| Window with a stale maxFreq | maxFreq only increases; shrink by one | O(n) | O(Σ) |

> [!tip] Interview angle
> Asked to test the stale-`maxFreq` insight. Give the O(26n) version (recompute max on shrink) first if unsure, then explain why `maxFreq` can stay stale.

---

## 3. Brute force: every substring

**Intuition.** For each start, extend right with a count array, tracking the max frequency. The window is valid while `len − maxFreq ≤ k`.

```python
def char_replace_brute(s, k):
    best = 0
    for i in range(len(s)):
        cnt = [0] * 26
        mx = 0
        for j in range(i, len(s)):
            c = ord(s[j]) - 65
            cnt[c] += 1
            mx = max(mx, cnt[c])
            if j - i + 1 - mx <= k:
                best = max(best, j - i + 1)
    return best
```

**Complexity:** time **O(n²)**, space **O(Σ)**.

---

## 4. Shrinking window, recompute max

**Intuition.** Expand `r`. While `len − max(cnt) > k`, drop `s[l]`. Recomputing `max(cnt)` costs 26 per check — fine, and obviously correct.

```python
def char_replace_recompute(s, k):
    cnt = [0] * 26
    l = best = 0
    for r, c in enumerate(s):
        cnt[ord(c) - 65] += 1
        while r - l + 1 - max(cnt) > k:
            cnt[ord(s[l]) - 65] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best
```

**Complexity:** time **O(26·n)**, space **O(Σ)**.

---

## 5. Window with a stale maxFreq

**Intuition.** Track `maxFreq` as the highest count ever seen in any window. If `len − maxFreq > k`, slide `l` by one. A longer answer requires a window whose real max frequency exceeds the old `maxFreq`, and at that moment `maxFreq` is updated correctly, so the stale value never yields a wrong answer.

**Algorithm**

1. `cnt = [0]*26`, `l = maxf = best = 0`.
2. For each `r`: `cnt[s[r]] += 1`; `maxf = max(maxf, cnt[s[r]])`.
3. If `r − l + 1 − maxf > k`: `cnt[s[l]] -= 1`, `l += 1`.
4. `best = max(best, r − l + 1)`.

**Dry run** — "AABABBA", k=1: windows grow to "AABA" (maxf 3, len 4) → 'B' makes len 5, 5−3 > 1 → slide → … best stays 4.

**C++**
```cpp
int characterReplacement(string s, int k) {
    int cnt[26] = {0}, l = 0, maxf = 0, best = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        maxf = max(maxf, ++cnt[s[r] - 'A']);
        if (r - l + 1 - maxf > k) {
            cnt[s[l] - 'A']--;
            l++;
        }
        best = max(best, r - l + 1);
    }
    return best;
}
```

**Java**
```java
static int characterReplacement(String s, int k) {
    int[] cnt = new int[26];
    int l = 0, maxf = 0, best = 0;
    for (int r = 0; r < s.length(); r++) {
        maxf = Math.max(maxf, ++cnt[s.charAt(r) - 'A']);
        if (r - l + 1 - maxf > k) {
            cnt[s.charAt(l) - 'A']--;
            l++;
        }
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```

**Python**
```python
def character_replacement(s, k):
    cnt = [0] * 26
    l = maxf = best = 0
    for r, c in enumerate(s):
        i = ord(c) - 65
        cnt[i] += 1
        maxf = max(maxf, cnt[i])
        if r - l + 1 - maxf > k:
            cnt[ord(s[l]) - 65] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best
```

**Complexity:** time **O(n)**, space **O(Σ)** — one pass, O(1) work per step.

---

## Edge cases

- `k = 0` → longest run of one letter.
- `k ≥ n − 1` → n.

---

## Common mistakes

1. Validity check `len − maxFreq < k` (should be `≤ k`, i.e. shrink when `> k`).
2. Thinking `maxFreq` must be decremented on shrink and writing a buggy update.
3. Using a set of distinct chars instead of the max-frequency rule.

---

## Follow-ups

1. Lowercase + uppercase + digits.
2. Return the actual letter and substring.

<details><summary>Answer sketches</summary>

**#1:** Bigger count array; same logic.

**#2:** Record `l`, `r` and the argmax letter when `best` improves.
</details>

---

## Flashcards

**When is a window fixable with k changes?** #flashcard
len − maxFreq ≤ k.

**Why can maxFreq stay stale?** #flashcard
The answer only improves when a window's true max frequency beats the old maxFreq, at which point maxFreq is updated.

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../04-practice/algorithms/04-sliding-window.md)
