---
module: striver-a2z/29-tries
lesson: 4
topic: Longest word with all prefixes (complete string)
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-word-with-all-prefixes?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, tries, trie, string]
---
# 4. Longest word with all prefixes (complete string)

← [Implement Trie II (count and erase)](03-implement-trie-ii-count-and-erase.md) · [Part 29 index](README.md) · Next → [Number of distinct substrings in a string](05-number-of-distinct-substrings-in-a-string.md)

> [!abstract] Problem at a glance
> **Task:** Longest word whose every prefix is also in the list; lexicographically smallest on ties; `"None"` if none.
> **Key insight:** Insert every word into a trie. A word is **complete** when every node along its path has `end = true`. Check each word in O(L) by walking it and stopping at the first node that is not a word end. LC 720 is the same problem.
> **Difficulty:** Medium · **Pattern:** Trie + all-prefix check · **Also on:** [LC 720](https://leetcode.com/problems/longest-word-in-dictionary/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-word-with-all-prefixes?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash set, check every prefix](#3-hash-set-check-every-prefix) · [4. Trie: every node on the path is an end](#4-trie-every-node-on-the-path-is-an-end) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `n` strings, return the longest string such that every prefix of it is also in the array. If several have the maximum length, return the lexicographically smallest. If none exist, return `"None"`.

| Input | Output | Why |
|---|---|---|
| `[n, ni, nin, ninj, ninja, ninga]` | `ninja` | n, ni, nin, ninj all present; ninga lacks ning |
| `[ab, bc]` | `None` | a and b are missing |
| `[a, b, ab, ba]` | `ab` | tie between ab and ba → ab |

**Constraints:** `1 ≤ n ≤ 10⁵`, total length `≤ 10⁵`, lowercase letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash set, check every prefix | set lookups for each prefix of each word | O(Σ L²) | O(Σ L) |
| Trie: every node on the path is an end | insert all, then walk each word checking end | O(Σ L) | O(Σ L · 26) |

> [!tip] Interview angle
> State that a single-letter word is complete if it is in the list (its only prefix is itself). Then: build the trie, check each word, keep the best by (length desc, lexicographic asc). A sort + hash-set solution also works and is worth mentioning as the alternative.

---

## 3. Hash set, check every prefix

**Intuition.** Put the words in a set. For each word, check `w[:i] in set` for `i = 1..L`. Building each slice costs O(i), so a word costs O(L²).

```python
def complete_string_set(words):
    s = set(words)
    best = ""
    for w in words:
        if all(w[:i] in s for i in range(1, len(w) + 1)):
            if len(w) > len(best) or (len(w) == len(best) and w < best):
                best = w
    return best or "None"
```

**Complexity:** time **O(Σ L²)**, space **O(Σ L)**.

---

## 4. Trie: every node on the path is an end

**Intuition.** After inserting all words, walking word `w` visits exactly the nodes for its prefixes. If every visited node has `end = true`, all prefixes are present.

**Algorithm**

1. Insert every word.
2. For each word, walk it; fail at the first node with `end = false`.
3. If it passes, compare with the best: longer wins; on equal length, the smaller string wins.
4. Return the best, or `"None"`.

**Dry run** — ninja: n✓ ni✓ nin✓ ninj✓ ninja✓ → complete. ninga: ning ✗.

**C++**
```cpp
string completeString(vector<string>& words) {
    struct Node { Node* ch[26] = {}; bool end = false; };
    Node* root = new Node();
    for (auto& w : words) {
        Node* n = root;
        for (char c : w) {
            if (!n->ch[c - 'a']) n->ch[c - 'a'] = new Node();
            n = n->ch[c - 'a'];
        }
        n->end = true;
    }
    string best = "";
    for (auto& w : words) {
        Node* n = root;
        bool ok = true;
        for (char c : w) {
            n = n->ch[c - 'a'];
            if (!n->end) { ok = false; break; }
        }
        if (ok && (w.size() > best.size() || (w.size() == best.size() && w < best))) best = w;
    }
    return best.empty() ? "None" : best;
}
```

**Java**
```java
static String completeString(String[] words) {
    java.util.List<int[]> kids = new java.util.ArrayList<>();
    java.util.List<Boolean> end = new java.util.ArrayList<>();
    kids.add(new int[26]); end.add(false);
    for (String w : words) {
        int n = 0;
        for (char c : w.toCharArray()) {
            if (kids.get(n)[c - 'a'] == 0) {
                kids.add(new int[26]); end.add(false);
                kids.get(n)[c - 'a'] = kids.size() - 1;
            }
            n = kids.get(n)[c - 'a'];
        }
        end.set(n, true);
    }
    String best = "";
    for (String w : words) {
        int n = 0;
        boolean ok = true;
        for (char c : w.toCharArray()) {
            n = kids.get(n)[c - 'a'];
            if (!end.get(n)) { ok = false; break; }
        }
        if (ok && (w.length() > best.length() || (w.length() == best.length() && w.compareTo(best) < 0))) best = w;
    }
    return best.isEmpty() ? "None" : best;
}
```

**Python**
```python
def complete_string(words):
    root = {}
    for w in words:
        n = root
        for c in w:
            n = n.setdefault(c, {})
        n['$'] = True
    best = ""
    for w in words:
        n = root
        for c in w:
            n = n[c]
            if '$' not in n:
                break
        else:
            if len(w) > len(best) or (len(w) == len(best) and w < best):
                best = w
    return best or "None"
```

**Complexity:** time **O(Σ L)**, space **O(Σ L · 26)** — every word is walked twice (insert, check), O(L) each.

---

## Edge cases

- No complete word at all → `"None"`.
- A single-letter word is always complete.
- Ties at the maximum length → lexicographically smallest.

---

## Common mistakes

1. Only checking `end` at the last node (that is just `search`).
2. Forgetting the tie-break.
3. Returning `""` instead of `"None"`.

---

## Follow-ups

1. Without a trie?
2. Stream of words?

<details><summary>Answer sketches</summary>

**#1:** Sort the words by length, then lexicographically; keep a set of accepted words; accept `w` if `w[:-1]` was accepted. O(Σ L log n).

**#2:** Keep the trie; a new word is complete if its parent node is a complete word end. Track the best incrementally.
</details>

---

## Flashcards

**Complete-string check in a trie?** #flashcard
Every node on the word's path must have end = true.

**Complete string tie-break?** #flashcard
Longer first, then lexicographically smaller.

**Interview track →** [Trie deep-dive](../../01-data-structures/09-trie.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md) · [Trie walkthroughs](../../04-practice/data-structures/09-trie.md)
