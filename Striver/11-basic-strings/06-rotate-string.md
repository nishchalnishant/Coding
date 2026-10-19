---
module: striver/11-basic-strings
lesson: 6
topic: Rotate String
difficulty: Easy
source: https://takeuforward.org/learning/dsa/rotate-string?category=basic-strings&source=strivers-a2z-dsa-sheet
tags: [striver, basic-strings, strings]
---
# 6. Rotate String

← [Isomorphic Strings](05-isomorphic-strings.md) · [Part 11 index](README.md) · Next → [Valid Anagram](07-valid-anagram.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `goal` can be obtained from `s` by some number of left rotations.
> **Key insight:** Every rotation of `s` is a length-n window of `s + s`. So the answer is `len(s) == len(goal) and goal in s + s`.
> **Difficulty:** Easy · **Pattern:** Doubling trick · **Also on:** 796
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/rotate-string?category=basic-strings&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — try every shift](#3-brute--try-every-shift) · [4. Optimal — substring of s + s](#4-optimal--substring-of-s--s) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A shift moves the leftmost char of `s` to the end. Return `true` iff `s` becomes `goal` after some number of shifts.

| Input | Output | Why |
|---|---|---|
| `s = "abcde", goal = "cdeab"` | `true` | two shifts |
| `s = "abcde", goal = "abced"` | `false` |  |
| `s = "aa", goal = "a"` | `false` | lengths differ |

**Constraints:** `1 ≤ len(s), len(goal) ≤ 100`, lowercase.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — try every shift | compare goal with each of the n rotations | O(n²) | O(n) |
| Optimal — substring of s + s | `goal in s + s` | O(n) with KMP; O(n²) worst case naive | O(n) |

---

## 3. Brute — try every shift

**Intuition.** Build `s[k:] + s[:k]` for each `k` and compare it to `goal`.

```python
def rotate_brute(s, goal):
    if len(s) != len(goal):
        return False
    return any(s[k:] + s[:k] == goal for k in range(len(s)))
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Optimal — substring of s + s

**Intuition.** `s + s = s[0..n-1] s[0..n-1]`, so the window starting at `k` is `s[k..n-1] s[0..k-1]`, the k-th rotation. Every rotation appears and nothing else of length n does. The length check rules out shorter `goal`s that are mere substrings.

**Algorithm**

1. If `len(s) != len(goal)` return false.
2. Return `goal` is a substring of `s + s`.

**Dry run** — `abcde` → `abcdeabcde`; `cdeab` starts at index 2 → **true**.

The library `find` / `contains` / `in` is fine in an interview. If asked for a guaranteed O(n), run KMP with `goal` as the pattern over `s + s` ([Part 30](../30-strings-advanced/README.md)).

**C++**
```cpp
bool rotateString(string& s, string& goal) {
    return s.size() == goal.size() && (s + s).find(goal) != string::npos;
}
```

**Java**
```java
static boolean rotateString(String s, String goal) {
    return s.length() == goal.length() && (s + s).contains(goal);
}
```

**Python**
```python
def rotate_string(s, goal):
    return len(s) == len(goal) and goal in s + s
```

**Complexity:** time **O(n) with KMP; O(n²) worst case naive**, space **O(n)**.

---

## Edge cases

- Different lengths → false (`aa` / `a` would otherwise pass).
- Zero shifts: `s == goal` → true.

---

## Common mistakes

1. Dropping the length check.
2. Rotating by repeated string concatenation inside a loop, which is O(n²) in allocations.

---

## Follow-ups

1. Minimum number of shifts.
2. Lexicographically smallest rotation.

<details><summary>Answer sketches</summary>

**#1:** The first index where `goal` occurs in `s + s` (with KMP for O(n)).

**#2:** Booth's algorithm, O(n), or the O(n²) brute force at interview level.
</details>

---

## Flashcards

**Rotation check in one line?** #flashcard
len(s) == len(goal) and goal in s + s.

**Why the length check in rotate-string?** #flashcard
Otherwise any substring of s + s would pass.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String algorithms](../../02-algorithms/02-string-algorithms.md) · [Concept: basic strings](../07-concept-basics/04-basic-string.md)
