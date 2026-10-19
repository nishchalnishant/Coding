---
module: striver/29-tries
lesson: 3
topic: Implement Trie II (count and erase)
difficulty: Medium
source: https://takeuforward.org/learning/dsa/trie-implementation-and-advanced-operations?category=triessubc&source=strivers-a2z-dsa-sheet
tags: [striver, tries, trie, design, counting]
---
# 3. Implement Trie II (count and erase)

← [Implement Trie (prefix tree)](02-implement-trie-prefix-tree.md) · [Part 29 index](README.md) · Next → [Longest word with all prefixes (complete string)](04-longest-word-with-all-prefixes-complete-string.md)

> [!abstract] Problem at a glance
> **Task:** Trie with `insert`, `countWordsEqualTo`, `countWordsStartingWith` and `erase`, duplicates allowed.
> **Key insight:** Replace the `end` flag with two counters per node: `pass` = how many inserted words go **through** this node, `end` = how many **finish** here. Then `countWordsStartingWith(p)` is `pass` at the end of `p`, `countWordsEqualTo(w)` is `end` at the end of `w`, and `erase` decrements both along the path.
> **Difficulty:** Medium · **Pattern:** Trie with prefix / end counters · **Also on:** [LC 1804](https://leetcode.com/problems/implement-trie-ii-prefix-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/trie-implementation-and-advanced-operations?category=triessubc&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash map of word counts](#3-hash-map-of-word-counts) · [4. Trie with pass / end counters](#4-trie-with-pass--end-counters) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement a `Trie` that supports duplicates: `insert(word)`, `countWordsEqualTo(word)` (copies of `word` stored), `countWordsStartingWith(prefix)` (stored words with that prefix, counting copies) and `erase(word)` (removes one copy; `word` is guaranteed to be present).

| Input | Output | Why |
|---|---|---|
| `insert apple ×2; countWordsEqualTo apple; countWordsStartingWith app; erase apple; countWordsEqualTo apple; countWordsStartingWith app; erase apple; countWordsStartingWith app` | `2, 2, 1, 1, 0` |  |

**Constraints:** `1 ≤ L ≤ 2000`, up to `3·10⁴` calls; `erase` is only called on a word that is present.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash map of word counts | counter; prefix count scans all keys | O(1) equal, O(N·L) prefix | O(Σ L) |
| Trie with pass / end counters | pass++ along the path, end++ at the last node | O(L) per op | O(total chars · 26) |

> [!tip] Interview angle
> The interviewer wants the `pass` counter. Without it, prefix counting needs a DFS over the subtree. With it, every op is O(L). Ask whether to free nodes whose `pass` drops to 0 (optional, and it saves memory).

---

## 3. Hash map of word counts

**Intuition.** Keep `cnt[word]`. Equal and erase are O(L) for hashing, but `countWordsStartingWith` has to scan every distinct word, which is too slow when there are many prefix queries.

```python
class MapTrie:
    def __init__(self):
        self.cnt = {}
    def insert(self, word):
        self.cnt[word] = self.cnt.get(word, 0) + 1
    def countWordsEqualTo(self, word):
        return self.cnt.get(word, 0)
    def countWordsStartingWith(self, prefix):
        return sum(v for w, v in self.cnt.items() if w.startswith(prefix))
    def erase(self, word):
        self.cnt[word] -= 1
```

**Complexity:** time **O(1) equal, O(N·L) prefix**, space **O(Σ L)**.

---

## 4. Trie with pass / end counters

**Intuition.** `insert` increments `pass` on every node it visits (excluding the root) and `end` on the last node. `erase` walks the same path decrementing. Queries read one counter at the end of the walk, or return 0 if the path breaks.

**Algorithm**

1. `insert(w)`: walk/create; `++pass` on each node; `++end` on the last.
2. `countWordsEqualTo(w)`: walk; return `end` or 0.
3. `countWordsStartingWith(p)`: walk; return `pass` or 0.
4. `erase(w)`: walk; `--pass` on each node; `--end` on the last.

**Dry run** — insert apple ×2 → pass(a..e) = 2, end(e) = 2. erase apple → pass 1, end 1. countWordsStartingWith app = pass(2nd p) = 1.

**C++**
```cpp
class Trie {
    struct Node { Node* ch[26] = {}; int pass = 0, end = 0; };
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
            n->pass++;
        }
        n->end++;
    }
    int countWordsEqualTo(const string& w) { Node* n = walk(w); return n ? n->end : 0; }
    int countWordsStartingWith(const string& p) { Node* n = walk(p); return n ? n->pass : 0; }
    void erase(const string& w) {
        Node* n = root;
        for (char c : w) {
            n = n->ch[c - 'a'];
            n->pass--;
        }
        n->end--;
    }
};
```

**Java**
```java
static class Trie {
    static class Node { Node[] ch = new Node[26]; int pass, end; }
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
            n.pass++;
        }
        n.end++;
    }
    int countWordsEqualTo(String w) { Node n = walk(w); return n == null ? 0 : n.end; }
    int countWordsStartingWith(String p) { Node n = walk(p); return n == null ? 0 : n.pass; }
    void erase(String w) {
        Node n = root;
        for (char c : w.toCharArray()) {
            n = n.ch[c - 'a'];
            n.pass--;
        }
        n.end--;
    }
}
```

**Python**
```python
class CountTrie:
    class Node:
        __slots__ = ("ch", "pass_", "end")
        def __init__(self):
            self.ch, self.pass_, self.end = {}, 0, 0
    def __init__(self):
        self.root = self.Node()
    def _walk(self, s):
        n = self.root
        for c in s:
            n = n.ch.get(c)
            if n is None:
                return None
        return n
    def insert(self, word):
        n = self.root
        for c in word:
            n = n.ch.setdefault(c, self.Node())
            n.pass_ += 1
        n.end += 1
    def countWordsEqualTo(self, word):
        n = self._walk(word)
        return n.end if n else 0
    def countWordsStartingWith(self, prefix):
        n = self._walk(prefix)
        return n.pass_ if n else 0
    def erase(self, word):
        n = self.root
        for c in word:
            n = n.ch[c]
            n.pass_ -= 1
        n.end -= 1
```

**Complexity:** time **O(L) per op**, space **O(total chars · 26)** — each op is one walk of length L; counters make prefix counts O(1) at the end node.

---

## Edge cases

- Erasing the last copy leaves nodes with `pass = 0`; queries must still return 0 for them.
- A prefix that is itself a stored word counts once in `countWordsStartingWith`.
- Duplicates: counts, not flags.

---

## Common mistakes

1. Incrementing `pass` on the root (then the root's `pass` is the total count, which is harmless, but off-by-one if you read it as a prefix).
2. Using a boolean `end`, which loses duplicates.
3. Decrementing `end` on every node during erase.

---

## Follow-ups

1. Free memory on erase?
2. Count distinct words with a prefix?

<details><summary>Answer sketches</summary>

**#1:** When a child's `pass` hits 0, set the pointer to null; that subtree is empty.

**#2:** Keep a second counter that only changes when `end` goes 0 → 1 or 1 → 0.
</details>

---

## Flashcards

**pass vs end counter?** #flashcard
pass = words through the node (prefix count); end = words ending there (exact count).

**Trie erase?** #flashcard
Walk the path decrementing pass, then decrement end at the last node.

**Interview track →** [Trie deep-dive](../../01-data-structures/09-trie.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md) · [Trie walkthroughs](../../coding/data-structures/09-trie.md)
