---
module: striver/11-basic-strings
lesson: 4
topic: Longest Common Prefix
difficulty: Easy
source: https://takeuforward.org/learning/dsa/longest-common-prefix?category=basic-strings&source=strivers-a2z-dsa-sheet
tags: [striver, basic-strings, strings]
---
# 4. Longest Common Prefix

← [Largest Odd Number in a String](03-largest-odd-number-in-a-string.md) · [Part 11 index](README.md) · Next → [Isomorphic Strings](05-isomorphic-strings.md)

> [!abstract] Problem at a glance
> **Task:** Return the longest string that is a prefix of every string in `strs`.
> **Key insight:** Scan column by column (vertical scan). Stop at the first column where any string ends or has a different char than `strs[0]`.
> **Difficulty:** Easy · **Pattern:** Vertical scan · **Also on:** 14
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-common-prefix?category=basic-strings&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — horizontal shrink](#3-brute--horizontal-shrink) · [4. Optimal — vertical scan](#4-optimal--vertical-scan) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array of strings `strs`, return their longest common prefix, or `""` if there is none.

| Input | Output | Why |
|---|---|---|
| `strs = ["flower","flow","flight"]` | `"fl"` |  |
| `strs = ["dog","racecar","car"]` | `""` | first chars differ |
| `strs = ["apple"]` | `"apple"` |  |

**Constraints:** `1 ≤ len(strs) ≤ 200`, `0 ≤ len(strs[i]) ≤ 200`, lowercase.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — horizontal shrink | start with strs[0], trim until it prefixes each string | O(S · m) | O(m) |
| Optimal — vertical scan | compare column i across all strings | O(S) total chars | O(1) extra |

---

## 3. Brute — horizontal shrink

**Intuition.** Take `strs[0]` as the candidate and, for each other string, chop characters off the end until the candidate is a prefix of that string. It's correct, but `startswith` is re-run after each chop.

```python
def lcp_shrink(strs):
    pre = strs[0]
    for s in strs[1:]:
        while not s.startswith(pre):
            pre = pre[:-1]
    return pre
```

**Complexity:** time **O(S · m)**, space **O(m)**.

---

## 4. Optimal — vertical scan

**Intuition.** The prefix grows one column at a time. Column `i` survives only if every string has an `i`-th char equal to `strs[0][i]`. The scan stops at the first column that fails, so no char beyond the answer + 1 column is read.

**Algorithm**

1. For `i` in `0 .. len(strs[0]) − 1`:
2.   For each `s` in `strs`: if `i == len(s)` or `s[i] != strs[0][i]`, return `strs[0][:i]`.
3. Return `strs[0]`.

**Dry run** — `flower, flow, flight`: column 0 f f f ✓, column 1 l l l ✓, column 2 o o i ✗ → **fl**.

**Sort trick:** after sorting, the LCP of the whole array equals the LCP of the first and last strings, because they are the most different. That's O(S log n) with a short proof; the vertical scan is simpler and faster.

**C++**
```cpp
string longestCommonPrefix(vector<string>& strs) {
    for (size_t i = 0; i < strs[0].size(); i++)
        for (auto& s : strs)
            if (i == s.size() || s[i] != strs[0][i]) return strs[0].substr(0, i);
    return strs[0];
}
```

**Java**
```java
static String longestCommonPrefix(String[] strs) {
    for (int i = 0; i < strs[0].length(); i++)
        for (String s : strs)
            if (i == s.length() || s.charAt(i) != strs[0].charAt(i)) return strs[0].substring(0, i);
    return strs[0];
}
```

**Python**
```python
def longest_common_prefix(strs):
    for i, ch in enumerate(strs[0]):
        for s in strs:
            if i == len(s) or s[i] != ch:
                return strs[0][:i]
    return strs[0]
```

**Complexity:** time **O(S) total chars**, space **O(1) extra** — each char is read at most once, plus one failing column.

---

## Edge cases

- A single string → itself.
- An empty string anywhere → `""`.
- One string is a prefix of another (`ab`, `a`): the bounds check `i == len(s)` fires.

---

## Common mistakes

1. Indexing `s[i]` before checking `i < len(s)`.
2. Using the shortest string's length but forgetting that its chars still have to match.

---

## Follow-ups

1. LCP for many queries against a fixed set.
2. Longest common prefix of a pair, repeated (e.g. suffix-array LCP).

<details><summary>Answer sketches</summary>

**#1:** Build a trie; the LCP is the path from the root while nodes have one child and aren't word ends ([Part 29](../29-tries/README.md)).

**#2:** Kasai's algorithm: out of scope at L3/L4.
</details>

---

## Flashcards

**LCP vertical scan stop condition?** #flashcard
i == len(s) or s[i] != strs[0][i].

**LCP via sorting?** #flashcard
LCP(first, last) after sorting.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String algorithms](../../02-algorithms/02-string-algorithms.md) · [Concept: basic strings](../07-concept-basics/04-basic-string.md)
