---
module: striver/22-sliding-window-and-2-pointer
lesson: 3
topic: Longest Substring Without Repeating Characters
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-substring-without-repeating-characters?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, hashing, strings]
---
# 3. Longest Substring Without Repeating Characters

← [Maximum Points You Can Obtain from Cards](02-maximum-points-you-can-obtain-from-cards.md) · [Part 22 index](README.md) · Next → [Max Consecutive Ones III](04-max-consecutive-ones-iii.md)

> [!abstract] Problem at a glance
> **Task:** Length of the longest substring of `s` with all distinct characters.
> **Key insight:** Keep a window `[l, r]` with no repeats. When `s[r]` was last seen at index `j ≥ l`, jump `l` to `j + 1`. Storing the last index (instead of a set) lets `l` jump in one step rather than shrinking character by character.
> **Difficulty:** Medium · **Pattern:** Variable window + last-seen index map · **Also on:** [LC 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-substring-without-repeating-characters?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: every start](#3-brute-force-every-start) · [4. Window with a set (shrink one by one)](#4-window-with-a-set-shrink-one-by-one) · [5. Window with last-seen index (jump)](#5-window-with-last-seen-index-jump) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s`, return the length of the longest substring without repeating characters.

| Input | Output | Why |
|---|---|---|
| `s = "abcabcbb"` | `3` | "abc" |
| `s = "bbbbb"` | `1` | "b" |
| `s = "pwwkew"` | `3` | "wke"; "pwke" is a subsequence, not a substring |

**Constraints:** `0 ≤ s.length ≤ 5·10⁴`; `s` has letters, digits, symbols and spaces.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: every start | extend each start until a repeat | O(n²) | O(Σ) |
| Window with a set (shrink one by one) | remove s[l] until s[r] fits | O(n) | O(Σ) |
| Window with last-seen index (jump) | l = max(l, last[c] + 1) | O(n) | O(Σ) |

> [!tip] Interview angle
> The canonical variable window. Expect to explain the invariant (window has no duplicates), why `l` never moves left (`max(l, last[c] + 1)`), and the O(1) alphabet space.

---

## 3. Brute force: every start

**Intuition.** For each start index, extend right with a set until a character repeats. Records the longest run. Quadratic because each start rescans.

```python
def longest_unique_brute(s):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
        best = max(best, len(seen))
    return best
```

**Complexity:** time **O(n²)**, space **O(Σ)**.

---

## 4. Window with a set (shrink one by one)

**Intuition.** Expand `r`. While `s[r]` is already in the window's set, remove `s[l]` and advance `l`. Each index enters and leaves at most once, so it's O(2n).

```python
def longest_unique_set(s):
    seen, l, best = set(), 0, 0
    for r, c in enumerate(s):
        while c in seen:
            seen.remove(s[l])
            l += 1
        seen.add(c)
        best = max(best, r - l + 1)
    return best
```

**Complexity:** time **O(n)**, space **O(Σ)**.

---

## 5. Window with last-seen index (jump)

**Intuition.** Store the last index of each character. On `s[r]`, if its last index is inside the window, move `l` straight past it. The `max` matters: a stale last index from before `l` must not pull `l` backwards.

**Algorithm**

1. `last = {}`, `l = best = 0`.
2. For each `r`: if `s[r]` in `last` and `last[s[r]] ≥ l`, set `l = last[s[r]] + 1`.
3. `last[s[r]] = r`; `best = max(best, r − l + 1)`.

**Dry run** — "abba": a(0) l=0 → b(1) → b(2): last b=1 ≥ 0 → l=2 → a(3): last a=0 < l=2, stays 2 → window "ba" len 2. Best 2.

**C++**
```cpp
int lengthOfLongestSubstring(string s) {
    vector<int> last(256, -1);
    int l = 0, best = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        unsigned char c = s[r];
        if (last[c] >= l) l = last[c] + 1;
        last[c] = r;
        best = max(best, r - l + 1);
    }
    return best;
}
```

**Java**
```java
static int lengthOfLongestSubstring(String s) {
    int[] last = new int[256];
    Arrays.fill(last, -1);
    int l = 0, best = 0;
    for (int r = 0; r < s.length(); r++) {
        char c = s.charAt(r);
        if (last[c] >= l) l = last[c] + 1;
        last[c] = r;
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```

**Python**
```python
def length_of_longest_substring(s):
    last, l, best = {}, 0, 0
    for r, c in enumerate(s):
        if last.get(c, -1) >= l:
            l = last[c] + 1
        last[c] = r
        best = max(best, r - l + 1)
    return best
```

**Complexity:** time **O(n)**, space **O(Σ)** — single pass; the array has one slot per possible byte.

---

## Edge cases

- Empty string → 0.
- All same character → 1.
- Stale last index before `l` ("abba").

---

## Common mistakes

1. `l = last[c] + 1` without the `≥ l` check, which moves `l` backwards on inputs like "abba".
2. Updating `best` before moving `l`.
3. Confusing substring with subsequence.

---

## Follow-ups

1. Return the substring itself.
2. At most 2 repeats per character allowed.

<details><summary>Answer sketches</summary>

**#1:** Track the `l` at which `best` was set.

**#2:** Keep counts; shrink while `count[c] > 2`.
</details>

---

## Flashcards

**Longest unique substring: how does l move?** #flashcard
l = max(l, last[c] + 1): jump past the previous occurrence if it's inside the window.

**Why the max?** #flashcard
A last-seen index before l is stale; without max, l would move left ("abba").

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../coding/algorithms/04-sliding-window.md)
