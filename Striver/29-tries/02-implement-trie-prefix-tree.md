---
module: striver/29-tries
lesson: 2
topic: Implement Trie (prefix tree)
difficulty: Medium
source: https://takeuforward.org/learning/dsa/trie-implementation-and-operations?category=triessubc&source=strivers-a2z-dsa-sheet
tags: [striver, tries, trie, design, string]
---
# 2. Implement Trie (prefix tree)

← [Tries and Binary Tries](01-trie-theory.md) · [Part 29 index](README.md) · Next → [Implement Trie II (count and erase)](03-implement-trie-ii-count-and-erase.md)

> [!abstract] Problem at a glance
> **Task:** Build a trie with `insert(word)`, `search(word)` and `startsWith(prefix)`, each O(L).
> **Key insight:** Each node holds up to 26 child pointers and an `end` flag. A word is a **path** from the root. `search` walks the path and checks `end`; `startsWith` only needs the path to exist. Shared prefixes share nodes, so a lookup costs O(L) however many words are stored.
> **Difficulty:** Medium · **Pattern:** Trie: walk / create a path of child pointers · **Also on:** [LC 208](https://leetcode.com/problems/implement-trie-prefix-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/trie-implementation-and-operations?category=triessubc&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash set of words + hash set of prefixes](#3-hash-set-of-words--hash-set-of-prefixes) · [4. Trie of child arrays](#4-trie-of-child-arrays) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement a `Trie` class: `insert(word)` adds the word, `search(word)` returns `true` if the exact word was inserted, `startsWith(prefix)` returns `true` if any inserted word starts with `prefix`. Words use lowercase `a–z`.

| Input | Output | Why |
|---|---|---|
| `insert apple; search apple; search app; startsWith app; insert app; search app` | `true, false, true, true` | `app` is only a prefix until it is inserted |

**Constraints:** `1 ≤ L ≤ 2000`, up to `3·10⁴` calls in total.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash set of words + hash set of prefixes | store every prefix at insert time | O(L²) insert, O(L) query (hash) | O(Σ L²) |
| Trie of child arrays | node = children[26] + end flag | O(L) per op | O(total chars · 26) |

> [!tip] Interview angle
> Draw the node first: `children[26]` + `end`. Then write a shared `walk(s)` helper that returns the last node or null. `search = walk(w) && walk(w).end`, `startsWith = walk(p) != null`. Mention the array vs hash-map trade-off for children (fast and fixed alphabet vs memory-light and any alphabet).

---

## 3. Hash set of words + hash set of prefixes

**Intuition.** On `insert`, add the word to `words` and each of its prefixes to `prefixes`. Queries are set lookups. Easy, but every prefix is stored as its own string, so both memory and insert time are quadratic in the length.

```python
class SetTrie:
    def __init__(self):
        self.words, self.prefixes = set(), set()
    def insert(self, word):
        self.words.add(word)
        for i in range(1, len(word) + 1):
            self.prefixes.add(word[:i])
    def search(self, word):
        return word in self.words
    def startsWith(self, prefix):
        return prefix in self.prefixes
```

**Complexity:** time **O(L²) insert, O(L) query (hash)**, space **O(Σ L²)**.

---

## 4. Trie of child arrays

**Intuition.** Walk the characters from the root, creating missing children on `insert`. Mark the last node `end = true`. Both queries reuse one walk: `search` also needs `end`, `startsWith` does not.

**Algorithm**

1. `insert(w)`: `node = root`; for each `c`, create `node.child[c]` if missing and move to it; set `node.end = true`.
2. `walk(s)`: follow `child[c]` for each `c`; return null as soon as one is missing.
3. `search(w) = walk(w) != null && walk(w).end`; `startsWith(p) = walk(p) != null`.

**Dry run** — insert apple → path a-p-p-l-e, end at e. search app → node at 2nd p, end=false → false. startsWith app → true. insert app → end at 2nd p → search app true.

**C++**
```cpp
class Trie {
    struct Node { Node* ch[26] = {}; bool end = false; };
    Node* root = new Node();
    Node* walk(const string& s) {
        Node* n = root;
        for (char c : s) {
            if (!n->ch[c - 'a']) return nullptr;
            n = n->ch[c - 'a'];
        }
        return n;
    }
public:
    void insert(const string& w) {
        Node* n = root;
        for (char c : w) {
            if (!n->ch[c - 'a']) n->ch[c - 'a'] = new Node();
            n = n->ch[c - 'a'];
        }
        n->end = true;
    }
    bool search(const string& w) { Node* n = walk(w); return n && n->end; }
    bool startsWith(const string& p) { return walk(p) != nullptr; }
};
```

**Java**
```java
static class Trie {
    static class Node { Node[] ch = new Node[26]; boolean end; }
    private final Node root = new Node();
    private Node walk(String s) {
        Node n = root;
        for (char c : s.toCharArray()) {
            if (n.ch[c - 'a'] == null) return null;
            n = n.ch[c - 'a'];
        }
        return n;
    }
    void insert(String w) {
        Node n = root;
        for (char c : w.toCharArray()) {
            if (n.ch[c - 'a'] == null) n.ch[c - 'a'] = new Node();
            n = n.ch[c - 'a'];
        }
        n.end = true;
    }
    boolean search(String w) { Node n = walk(w); return n != null && n.end; }
    boolean startsWith(String p) { return walk(p) != null; }
}
```

**Python**
```python
class Trie:
    def __init__(self):
        self.root = {}                       # dict children; '$' marks end of word
    def insert(self, word):
        n = self.root
        for c in word:
            n = n.setdefault(c, {})
        n['$'] = True
    def _walk(self, s):
        n = self.root
        for c in s:
            if c not in n:
                return None
            n = n[c]
        return n
    def search(self, word):
        n = self._walk(word)
        return n is not None and '$' in n
    def startsWith(self, prefix):
        return self._walk(prefix) is not None
```

**Complexity:** time **O(L) per op**, space **O(total chars · 26)** — each op follows at most L pointers; nodes are shared across common prefixes.

---

## Edge cases

- A query that is a strict prefix of a stored word: `search` false, `startsWith` true.
- A query longer than every stored word.
- Inserting the same word twice is a no-op.

---

## Common mistakes

1. Returning `true` from `search` just because the path exists (forgetting `end`).
2. Allocating a new root per insert.
3. Using `c - 'A'` on lowercase input.

---

## Follow-ups

1. Memory too high?
2. Autocomplete top-k?

<details><summary>Answer sketches</summary>

**#1:** Use a hash map per node (sparse), or a compressed radix trie that merges single-child chains.

**#2:** Store a count or top-k list at each node, or DFS from the prefix node.
</details>

---

## Flashcards

**Trie node fields?** #flashcard
children[26] (or map) + end-of-word flag.

**search vs startsWith?** #flashcard
Both walk the path; search also requires end == true.

**Trie op complexity?** #flashcard
O(L) in the key length, independent of the number of words.

**Interview track →** [Trie deep-dive](../../01-data-structures/09-trie.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md) · [Trie walkthroughs](../../coding/data-structures/09-trie.md)
