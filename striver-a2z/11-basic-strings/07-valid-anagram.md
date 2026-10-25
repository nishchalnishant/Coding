---
module: striver-a2z/11-basic-strings
lesson: 7
topic: Valid Anagram
difficulty: Easy
source: https://takeuforward.org/learning/dsa/valid-anagram?category=basic-strings&source=strivers-a2z-dsa-sheet
tags: [striver, basic-strings, strings, hashing]
---
# 7. Valid Anagram

← [Rotate String](06-rotate-string.md) · [Part 11 index](README.md) · Next → [Sort Characters by Frequency](08-sort-characters-by-frequency.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `t` is a rearrangement of `s`.
> **Key insight:** Anagrams have identical character counts. Increment for `s` and decrement for `t` in one `int[26]`, then check that it's all zero.
> **Difficulty:** Easy · **Pattern:** Count array · **Also on:** 242
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/valid-anagram?category=basic-strings&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — sort both](#3-brute--sort-both) · [4. Optimal — count array](#4-optimal--count-array) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given strings `s` and `t`, return `true` if `t` is an anagram of `s`: the same chars with the same multiplicities, in any order.

| Input | Output | Why |
|---|---|---|
| `s = "anagram", t = "nagaram"` | `true` |  |
| `s = "rat", t = "car"` | `false` |  |
| `s = "ab", t = "a"` | `false` | lengths differ |

**Constraints:** `1 ≤ n ≤ 5·10⁴`, lowercase English letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — sort both | `sorted(s) == sorted(t)` | O(n log n) | O(n) |
| Optimal — count array | +1 for s, −1 for t, all zero | O(n) | O(26) |

---

## 3. Brute — sort both

**Intuition.** Anagrams sort to the same string.

```python
def anagram_sort(s, t):
    return sorted(s) == sorted(t)
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. Optimal — count array

**Intuition.** Track the count differences between the two strings. A non-zero bucket means some char appears a different number of times. With unequal lengths there must be such a bucket, so exit early.

**Algorithm**

1. If lengths differ, return false.
2. For each `i`: `cnt[s[i]−'a']++`, `cnt[t[i]−'a']--`.
3. Return true iff every `cnt` is 0.

**Dry run** — `rat` / `car`: r +1 −1(r at t[2])… final cnt: t +1, c −1 → **false**.

**Unicode follow-up:** swap the array for a hashmap. The algorithm is unchanged.

**C++**
```cpp
bool anagramStrings(string& s, string& t) {
    if (s.size() != t.size()) return false;
    int cnt[26] = {0};
    for (size_t i = 0; i < s.size(); i++) { cnt[s[i] - 'a']++; cnt[t[i] - 'a']--; }
    for (int c : cnt) if (c) return false;
    return true;
}
```

**Java**
```java
static boolean anagramStrings(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] cnt = new int[26];
    for (int i = 0; i < s.length(); i++) { cnt[s.charAt(i) - 'a']++; cnt[t.charAt(i) - 'a']--; }
    for (int c : cnt) if (c != 0) return false;
    return true;
}
```

**Python**
```python
def anagram_strings(s, t):
    if len(s) != len(t):
        return False
    cnt = [0] * 26
    for a, b in zip(s, t):
        cnt[ord(a) - 97] += 1
        cnt[ord(b) - 97] -= 1
    return not any(cnt)
```

**Complexity:** time **O(n)**, space **O(26)**.

---

## Edge cases

- Different lengths → false immediately.
- Same chars, different multiplicities (`aacc` / `ccac`).

---

## Common mistakes

1. Comparing character *sets*, which ignores multiplicity.
2. Java `Arrays.sort` needs a `char[]` (`s.toCharArray()`); strings themselves can't be sorted.

---

## Follow-ups

1. Group anagrams (LC 49).
2. Find all anagram start indices of p in s (LC 438).

<details><summary>Answer sketches</summary>

**#1:** Key each word by its sorted form, or by its 26-count tuple; hashmap from key to list.

**#2:** Fixed sliding window of `len(p)` with a count array and a `matches` counter ([Part 22](../22-sliding-window-and-2-pointer/README.md)).
</details>

---

## Flashcards

**Anagram check in O(n)?** #flashcard
One int[26]: +1 for s, −1 for t, all zero.

**Anagram grouping key?** #flashcard
The sorted word, or its 26-count tuple.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String algorithms](../../02-algorithms/02-string-algorithms.md) · [Concept: basic strings](../07-concept-basics/04-basic-string.md)
