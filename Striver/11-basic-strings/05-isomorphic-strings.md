---
module: striver/11-basic-strings
lesson: 5
topic: Isomorphic Strings
difficulty: Easy
source: https://takeuforward.org/learning/dsa/isomorphic-string?category=basic-strings&source=strivers-a2z-dsa-sheet
tags: [striver, basic-strings, strings, hashing]
---
# 5. Isomorphic Strings

← [Longest Common Prefix](04-longest-common-prefix.md) · [Part 11 index](README.md) · Next → [Rotate String](06-rotate-string.md)

> [!abstract] Problem at a glance
> **Task:** Return true if the characters of `s` can be replaced to get `t` by a consistent one-to-one mapping.
> **Key insight:** The mapping must be a bijection. Recording the last-seen index of each char in both strings, and requiring the two to agree at every step, checks both directions at once.
> **Difficulty:** Easy · **Pattern:** Bijection via two maps · **Also on:** 205
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/isomorphic-string?category=basic-strings&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — pairwise structure](#3-brute--pairwise-structure) · [4. Better — two hashmaps](#4-better--two-hashmaps) · [5. Optimal — last-seen index arrays](#5-optimal--last-seen-index-arrays) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Two strings `s` and `t` of equal length are isomorphic if every occurrence of each char in `s` can be replaced by one char to get `t`. The order is preserved, and no two chars of `s` may map to the same char of `t`. A char may map to itself.

| Input | Output | Why |
|---|---|---|
| `s = "egg", t = "add"` | `true` | e→a, g→d |
| `s = "foo", t = "bar"` | `false` | o maps to both a and r |
| `s = "badc", t = "baba"` | `false` | b→b and d→b collide, so the check must run both ways |
| `s = "paper", t = "title"` | `true` |  |

**Constraints:** `1 ≤ n ≤ 5·10⁴`, `len(s) == len(t)`, ASCII.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — pairwise structure | for every i < j: s[i]==s[j] ⇔ t[i]==t[j] | O(n²) | O(1) |
| Better — two hashmaps | s→t and t→s maps must stay consistent | O(n) | O(Σ) |
| Optimal — last-seen index arrays | `last_s[s[i]] == last_t[t[i]]` at every i | O(n) | O(256) |

> [!tip] Interview angle
> The `badc` / `baba` case is what interviewers check. A one-direction map passes it wrongly, so say "bijection, check both directions" before coding.

---

## 3. Brute — pairwise structure

**Intuition.** Two strings are isomorphic iff they have the same equality pattern: positions equal in one are equal in the other. This checks that pattern pair by pair.

```python
def iso_brute(s, t):
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n):
            if (s[i] == s[j]) != (t[i] == t[j]):
                return False
    return True
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Better — two hashmaps

**Intuition.** Keep `m1: s-char → t-char` and `m2: t-char → s-char`. At each index, both existing entries must agree with the current pair. Then record the pair.

```python
def iso_maps(s, t):
    m1, m2 = {}, {}
    for a, b in zip(s, t):
        if m1.get(a, b) != b or m2.get(b, a) != a:
            return False
        m1[a], m2[b] = b, a
    return True
```

**Complexity:** time **O(n)**, space **O(Σ)**.

---

## 5. Optimal — last-seen index arrays

**Intuition.** Store for each char the index + 1 at which it was last seen (0 = never). If `s[i]` and `t[i]` are a valid pair, they were last seen at the same position, or both never. Any disagreement means one side reused a char the other didn't. This is the equality pattern again, in O(1) per step.

**Algorithm**

1. `ls = [0]*256`, `lt = [0]*256`.
2. For each `i`: if `ls[s[i]] != lt[t[i]]` return false; set both to `i + 1`.
3. Return true.

**Dry run** — `badc` / `baba`

| i | pair | ls[s_i] | lt[t_i] | ok? |
|---|---|---|---|---|
| 0 | b,b | 0 | 0 | ✓ |
| 1 | a,a | 0 | 0 | ✓ |
| 2 | d,b | 0 | 1 | ✗ |

→ **false**.

**C++**
```cpp
bool isomorphicString(string& s, string& t) {
    int ls[256] = {0}, lt[256] = {0};
    for (int i = 0; i < (int)s.size(); i++) {
        unsigned char a = s[i], b = t[i];
        if (ls[a] != lt[b]) return false;
        ls[a] = lt[b] = i + 1;
    }
    return true;
}
```

**Java**
```java
static boolean isomorphicString(String s, String t) {
    int[] ls = new int[256], lt = new int[256];
    for (int i = 0; i < s.length(); i++) {
        char a = s.charAt(i), b = t.charAt(i);
        if (ls[a] != lt[b]) return false;
        ls[a] = lt[b] = i + 1;
    }
    return true;
}
```

**Python**
```python
def isomorphic_string(s, t):
    ls, lt = [0] * 256, [0] * 256
    for i, (a, b) in enumerate(zip(s, t)):
        a, b = ord(a), ord(b)
        if ls[a] != lt[b]:
            return False
        ls[a] = lt[b] = i + 1
    return True
```

**Complexity:** time **O(n)**, space **O(256)** — i + 1 rather than i, so that 0 can mean "never seen".

---

## Edge cases

- Self-mapping is allowed (`a → a`).
- Many-to-one in either direction must fail (`ab` / `aa`, `aa` / `ab`).

---

## Common mistakes

1. Only one map (s → t), which accepts `badc` / `baba`.
2. Storing `i` instead of `i + 1`, so index 0 can't be told apart from never seen.
3. A negative `char` index in C++ for non-ASCII bytes; cast to `unsigned char`.

---

## Follow-ups

1. Word Pattern (LC 290): pattern chars ↔ words.
2. Group strings by isomorphism class.

<details><summary>Answer sketches</summary>

**#1:** The same bijection with two hashmaps; split the sentence first and check the counts match.

**#2:** Canonicalise each string to its first-occurrence pattern (`paper` → `0.1.0.2.3`) and group by that key.
</details>

---

## Flashcards

**Why does isomorphic need two maps?** #flashcard
It's a bijection; one map misses two chars of s collapsing onto one char of t.

**Last-seen-index trick for isomorphism?** #flashcard
ls[s[i]] == lt[t[i]] at every i; store i + 1.

**Canonical form of a string's pattern?** #flashcard
Replace each char by the index of its first occurrence.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String algorithms](../../02-algorithms/02-string-algorithms.md) · [Concept: basic strings](../07-concept-basics/04-basic-string.md)
