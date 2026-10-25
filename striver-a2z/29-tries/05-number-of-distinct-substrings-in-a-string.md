---
module: striver-a2z/29-tries
lesson: 5
topic: Number of distinct substrings in a string
difficulty: Hard
source: https://takeuforward.org/learning/dsa/number-of-distinct-substrings-in-a-string?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, tries, trie, string, suffix]
---
# 5. Number of distinct substrings in a string

← [Longest word with all prefixes (complete string)](04-longest-word-with-all-prefixes-complete-string.md) · [Part 29 index](README.md) · Next → [Maximum XOR of two numbers in an array](06-maximum-xor-of-two-numbers-in-an-array.md)

> [!abstract] Problem at a glance
> **Task:** Count the distinct substrings of `s`, including the empty string.
> **Key insight:** Every substring is a prefix of some suffix. Insert all suffixes into a trie: each **new node** created is a distinct substring that was not seen before. So the answer is the number of trie nodes, plus 1 for the empty string (Striver's convention).
> **Difficulty:** Hard · **Pattern:** Trie of all suffixes, count nodes · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/count-of-distinct-substrings/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-distinct-substrings-in-a-string?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash set of all substrings](#3-hash-set-of-all-substrings) · [4. Suffix trie, count new nodes](#4-suffix-trie-count-new-nodes) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s`, return the number of distinct substrings of `s`, counting the empty string.

| Input | Output | Why |
|---|---|---|
| `ab` | `4` | "", a, b, ab |
| `aba` | `6` | "", a, b, ab, ba, aba |
| `aaa` | `4` | "", a, aa, aaa |

**Constraints:** `1 ≤ |s| ≤ 1000`, lowercase letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash set of all substrings | generate O(n²) substrings into a set | O(n³) | O(n³) |
| Suffix trie, count new nodes | for each start i, walk/extend from root | O(n²) | O(n² · 26) worst |

> [!tip] Interview angle
> Confirm whether the empty string counts (the GfG/Striver version does; many others don't). The trie approach is O(n²) time and nodes. Mention suffix arrays/automata (O(n) or O(n log n)) as the scalable answer, but only as a follow-up.

---

## 3. Hash set of all substrings

**Intuition.** Enumerate every `s[i:j]` into a set. There are O(n²) substrings, each up to O(n) long to build and hash.

```python
def distinct_set(s):
    return len({s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)}) + 1
```

**Complexity:** time **O(n³)**, space **O(n³)**.

---

## 4. Suffix trie, count new nodes

**Intuition.** For each start `i`, walk from the root along `s[i], s[i+1], …`. Every time a child is missing, create it and increment the count. Extending a walk by one character is O(1), so no substring is rebuilt.

**Algorithm**

1. `count = 0`.
2. For `i = 0..n−1`: `node = root`; for `j = i..n−1`: if `child[s[j]]` is missing, create it and `count++`; move to it.
3. Return `count + 1`.

**Dry run** — aba: i=0 adds a, ab, aba (3); i=1 adds b, ba (2); i=2 'a' exists (0). 5 + 1 = 6.

**C++**
```cpp
int countDistinctSubstrings(string s) {
    vector<array<int, 26>> t(1);
    t[0].fill(0);
    int cnt = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        int n = 0;
        for (int j = i; j < (int)s.size(); j++) {
            int c = s[j] - 'a';
            if (!t[n][c]) {
                t[n][c] = t.size();
                t.emplace_back();
                t.back().fill(0);
                cnt++;
            }
            n = t[n][c];
        }
    }
    return cnt + 1;
}
```

**Java**
```java
static int countDistinctSubstrings(String s) {
    java.util.List<int[]> t = new java.util.ArrayList<>();
    t.add(new int[26]);
    int cnt = 0;
    for (int i = 0; i < s.length(); i++) {
        int n = 0;
        for (int j = i; j < s.length(); j++) {
            int c = s.charAt(j) - 'a';
            if (t.get(n)[c] == 0) {
                t.add(new int[26]);
                t.get(n)[c] = t.size() - 1;
                cnt++;
            }
            n = t.get(n)[c];
        }
    }
    return cnt + 1;
}
```

**Python**
```python
def count_distinct_substrings(s):
    root, cnt = {}, 0
    for i in range(len(s)):
        n = root
        for j in range(i, len(s)):
            c = s[j]
            if c not in n:
                n[c] = {}
                cnt += 1
            n = n[c]
    return cnt + 1
```

**Complexity:** time **O(n²)**, space **O(n² · 26) worst** — n suffixes, each walked in O(n); each node is created once.

---

## Edge cases

- All the same letter: only n + 1 distinct.
- All letters distinct: n(n+1)/2 + 1.
- Empty-string convention (+1).

---

## Common mistakes

1. Forgetting the `+ 1` for the empty string, or adding it when the problem doesn't want it.
2. Counting nodes visited instead of nodes created.
3. Rebuilding substrings with slicing inside the trie loop (back to O(n³)).

---

## Follow-ups

1. n = 10⁵?
2. Count distinct substrings of length k?

<details><summary>Answer sketches</summary>

**#1:** Suffix array + LCP: answer = n(n+1)/2 − Σ LCP (+1). Or the suffix automaton: Σ (len[v] − len[link[v]]).

**#2:** Rolling hash over the windows into a set (O(n) expected).
</details>

---

## Flashcards

**Distinct substrings via trie?** #flashcard
Insert every suffix; the number of created nodes is the number of distinct non-empty substrings.

**Why does a suffix trie see every substring?** #flashcard
Every substring is a prefix of some suffix.

**Interview track →** [Trie deep-dive](../../01-data-structures/09-trie.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md) · [Trie walkthroughs](../../04-practice/data-structures/09-trie.md)
