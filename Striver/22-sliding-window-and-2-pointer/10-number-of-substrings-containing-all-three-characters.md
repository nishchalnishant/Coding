---
module: striver/22-sliding-window-and-2-pointer
lesson: 10
topic: Number of Substrings Containing All Three Characters
difficulty: Medium
source: https://takeuforward.org/learning/dsa/number-of-substrings-containing-all-three-characters?category=counting-subarrays-and-substrings-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, counting, strings]
---
# 10. Number of Substrings Containing All Three Characters

← [Minimum Window Subsequence](09-minimum-window-subsequence.md) · [Part 22 index](README.md) · Next → [Binary Subarrays With Sum](11-binary-subarrays-with-sum.md)

> [!abstract] Problem at a glance
> **Task:** Count substrings of a string over {a, b, c} that contain at least one of each letter.
> **Key insight:** For each right end `r`, the substring `s[l..r]` contains all three letters iff `l ≤ min(last[a], last[b], last[c])`. So the number of valid substrings ending at `r` is `1 + min(last)` (0 if a letter hasn't appeared).
> **Difficulty:** Medium · **Pattern:** Count by right end (last-seen positions) · **Also on:** [LC 1358](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-substrings-containing-all-three-characters?category=counting-subarrays-and-substrings-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: every start](#3-brute-force-every-start) · [4. Last-seen positions](#4-last-seen-positions) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s` consisting only of the characters `a`, `b` and `c`, return the number of substrings containing at least one occurrence of all three characters.

| Input | Output | Why |
|---|---|---|
| `s = "abcabc"` | `10` |  |
| `s = "aaacb"` | `3` | "aaacb", "aacb", "acb" |
| `s = "abc"` | `1` |  |

**Constraints:** `3 ≤ s.length ≤ 5·10⁴`, `s` only `a`, `b`, `c`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: every start | extend until all three; add n − j | O(n²) | O(1) |
| Last-seen positions | add 1 + min(last) per right end | O(n) | O(1) |

> [!tip] Interview angle
> "At least" counting. Two accepted answers: the last-seen trick (count by right end) or the window that adds `n − r` for each valid left. Show you know why `+1 + min(last)` counts starts 0..min.

---

## 3. Brute force: every start

**Intuition.** For each start, extend right until all three letters appear at `j`. Every extension `j..n−1` also works, so add `n − j` and move to the next start.

```python
def count_abc_brute(s):
    n, total = len(s), 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            seen.add(s[j])
            if len(seen) == 3:
                total += n - j
                break
    return total
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Last-seen positions

**Intuition.** Track the last index of `a`, `b` and `c` (−1 if not seen). A substring ending at `r` contains all three iff it starts at or before the smallest of those three indices, giving `min + 1` choices of start.

**Algorithm**

1. `last = [-1, -1, -1]`, `total = 0`.
2. For each `r`: `last[s[r] − 'a'] = r`.
3. `total += 1 + min(last)` (adds 0 while any is −1).

**Dry run** — "aaacb": r=0..2 → min = −1 → +0; r=3 'c' → last = [2, −1, 3] → +0; r=4 'b' → last = [2, 4, 3] → +3. Total 3.

**C++**
```cpp
int numberOfSubstrings(string s) {
    int last[3] = {-1, -1, -1}, total = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        last[s[r] - 'a'] = r;
        total += 1 + min({last[0], last[1], last[2]});
    }
    return total;
}
```

**Java**
```java
static int numberOfSubstrings(String s) {
    int[] last = {-1, -1, -1};
    int total = 0;
    for (int r = 0; r < s.length(); r++) {
        last[s.charAt(r) - 'a'] = r;
        total += 1 + Math.min(last[0], Math.min(last[1], last[2]));
    }
    return total;
}
```

**Python**
```python
def number_of_substrings(s):
    last = [-1, -1, -1]
    total = 0
    for r, c in enumerate(s):
        last[ord(c) - 97] = r
        total += 1 + min(last)
    return total
```

**Complexity:** time **O(n)**, space **O(1)** — O(1) per character.

---

## Edge cases

- A letter never appears → 0.
- Minimum length string "abc" → 1.

---

## Common mistakes

1. Adding `min(last)` without the `+1` (starts are 0-indexed, so there are `min + 1` of them).
2. Counting at-most windows and forgetting to complement.
3. Overflow is not an issue at n = 5·10⁴ (max ≈ 1.25·10⁹ fits in int, barely); use `long` for larger n.

---

## Follow-ups

1. At least one of each of K letters.
2. Exactly one of each letter.

<details><summary>Answer sketches</summary>

**#1:** Track the K last positions; min over them (or a window with a distinct counter, adding `n − r`).

**#2:** Different problem: window where each count ≤ 1 and all three present.
</details>

---

## Flashcards

**Substrings with all of a, b, c ending at r?** #flashcard
1 + min(last[a], last[b], last[c]) — every start ≤ the oldest needed letter.

**General 'at least' trick for windows?** #flashcard
Once [l, r] is valid, every extension to the right is valid: add n − r.

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../coding/algorithms/04-sliding-window.md)
