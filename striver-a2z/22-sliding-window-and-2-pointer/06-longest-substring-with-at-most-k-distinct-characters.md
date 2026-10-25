---
module: striver-a2z/22-sliding-window-and-2-pointer
lesson: 6
topic: Longest Substring With At Most K Distinct Characters
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-substring-with-at-most-k-distinct-characters?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, hashing, strings, at-most-k]
---
# 6. Longest Substring With At Most K Distinct Characters

← [Fruit Into Baskets](05-fruit-into-baskets.md) · [Part 22 index](README.md) · Next → [Longest Repeating Character Replacement](07-longest-repeating-character-replacement.md)

> [!abstract] Problem at a glance
> **Task:** Length of the longest substring of `s` with at most `k` distinct characters.
> **Key insight:** Same template as Fruit Into Baskets with a general `k`: expand, count, and shrink while the map holds more than `k` keys. With a fixed 26-letter alphabet, an array plus a running `distinct` counter avoids map overhead.
> **Difficulty:** Medium · **Pattern:** Variable window + frequency map (≤ K distinct) · **Also on:** [LC 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) (premium)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-substring-with-at-most-k-distinct-characters?category=longest-and-smallest-window-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: every start](#3-brute-force-every-start) · [4. Window with counts and a distinct counter](#4-window-with-counts-and-a-distinct-counter) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s` of lowercase letters and an integer `k`, return the length of the longest substring that contains at most `k` distinct characters.

| Input | Output | Why |
|---|---|---|
| `s = "aababbcaacc", k = 2` | `6` | "aababb" |
| `s = "abcddefg", k = 3` | `4` | "bcdd" or "cdde" |

**Constraints:** `1 ≤ s.length ≤ 10⁵`, `0 ≤ k ≤ 26`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: every start | extend while distinct ≤ k | O(n²) | O(Σ) |
| Window with counts and a distinct counter | shrink while distinct > k | O(n) | O(Σ) |

> [!tip] Interview angle
> The generalised template. Interviewers check the `distinct` counter maintenance (increment on 0 → 1, decrement on 1 → 0) and the `k = 0` edge.

---

## 3. Brute force: every start

**Intuition.** For each start, extend right with a set; stop when it would exceed `k` distinct.

```python
def k_distinct_brute(s, k):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            seen.add(s[j])
            if len(seen) > k:
                break
            best = max(best, j - i + 1)
    return best
```

**Complexity:** time **O(n²)**, space **O(Σ)**.

---

## 4. Window with counts and a distinct counter

**Intuition.** Counts in a 26-slot array. `distinct` increases when a count goes 0 → 1 and decreases when it goes 1 → 0. Shrink while `distinct > k`.

**Algorithm**

1. `cnt = [0]*26`, `l = distinct = best = 0`.
2. For each `r`: if `cnt[s[r]] == 0`, `distinct += 1`; `cnt[s[r]] += 1`.
3. While `distinct > k`: `cnt[s[l]] -= 1`; if it hits 0, `distinct -= 1`; `l += 1`.
4. `best = max(best, r − l + 1)`.

**Dry run** — "aababbcaacc", k=2: window grows to "aababb" (6); at 'c' distinct=3 → shrink until only b,c remain → "bbc"... never beats 6.

**C++**
```cpp
int kDistinctChar(string s, int k) {
    int cnt[26] = {0}, l = 0, distinct = 0, best = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        if (cnt[s[r] - 'a']++ == 0) distinct++;
        while (distinct > k) {
            if (--cnt[s[l] - 'a'] == 0) distinct--;
            l++;
        }
        best = max(best, r - l + 1);
    }
    return best;
}
```

**Java**
```java
static int kDistinctChar(String s, int k) {
    int[] cnt = new int[26];
    int l = 0, distinct = 0, best = 0;
    for (int r = 0; r < s.length(); r++) {
        if (cnt[s.charAt(r) - 'a']++ == 0) distinct++;
        while (distinct > k) {
            if (--cnt[s.charAt(l) - 'a'] == 0) distinct--;
            l++;
        }
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```

**Python**
```python
def k_distinct_char(s, k):
    cnt = [0] * 26
    l = distinct = best = 0
    for r, c in enumerate(s):
        i = ord(c) - 97
        if cnt[i] == 0:
            distinct += 1
        cnt[i] += 1
        while distinct > k:
            j = ord(s[l]) - 97
            cnt[j] -= 1
            if cnt[j] == 0:
                distinct -= 1
            l += 1
        best = max(best, r - l + 1)
    return best
```

**Complexity:** time **O(n)**, space **O(Σ)** — two pointers each move n times; the array is constant size.

---

## Edge cases

- `k = 0` → 0 (the while loop empties every window).
- `k ≥` number of distinct letters → n.

---

## Common mistakes

1. Incrementing `distinct` on every new character instead of on 0 → 1.
2. Using `if` with `best` updates (the non-shrinking trick needs the answer from the final size, not `best`).
3. Forgetting `k = 0`.

---

## Follow-ups

1. Exactly K distinct, longest.
2. Count substrings with exactly K distinct.

<details><summary>Answer sketches</summary>

**#1:** Same window, record only when `distinct == k`.

**#2:** atMost(k) − atMost(k − 1) — see Subarrays with K Different Integers.
</details>

---

## Flashcards

**At-most-K-distinct window: when does distinct change?** #flashcard
+1 when a count goes 0 → 1, −1 when it goes 1 → 0.

**Template condition to shrink?** #flashcard
while distinct > k.

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../04-practice/algorithms/04-sliding-window.md)
