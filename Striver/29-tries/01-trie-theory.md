---
module: striver/29-tries
lesson: 1
topic: Tries (node design, insert/search/startsWith/erase, counters) and binary tries (bit prerequisites, greedy max XOR, offline queries)
source: https://takeuforward.org/learning/dsa/bit-prerequisites-for-trie-problems?category=triessubc&source=strivers-a2z-dsa-sheet
tags: [striver, trie, binary-trie, bit-manipulation, xor, theory]
---
# 1. Tries and Binary Tries

← [Part 29 index](README.md) · Next → [Implement Trie (prefix tree)](02-implement-trie-prefix-tree.md)

> [!abstract] What this covers
> **Core idea:** A trie stores keys as **paths** from a root. Each edge is one symbol, and keys with a common prefix share the nodes for that prefix.
> - Lookups cost O(L) in the key length, however many keys are stored.
> - Counters on the nodes turn the trie into a prefix-count index.
> - With the alphabet `{0, 1}` and keys written MSB first, a **binary trie** answers "which stored number maximises XOR with x?" greedily in 31 steps.
>
> **You'll be able to:** design a trie node (array vs map children, `end` flag, `pass`/`end` counters); write insert, search, startsWith and erase from memory; use the bit operations a binary trie needs; prove the greedy max-XOR rule; and answer constrained XOR queries offline.
> **Source:** [Striver: Trie lessons](https://takeuforward.org/learning/dsa/bit-prerequisites-for-trie-problems?category=triessubc&source=strivers-a2z-dsa-sheet) · **Time:** 45 min

**Sections:** [1. What a trie is](#1-what-a-trie-is) · [2. Node design](#2-node-design) · [3. Core operations](#3-core-operations) · [4. Counters and erase](#4-counters-and-erase) · [5. Complexity and memory](#5-complexity-and-memory) · [6. Trie vs hash set](#6-trie-vs-hash-set) · [7. Bit prerequisites](#7-bit-prerequisites) · [8. Binary trie and greedy max XOR](#8-binary-trie-and-greedy-max-xor) · [9. Offline queries](#9-offline-queries) · [10. Trie patterns](#10-trie-patterns) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Key terms](#key-terms) · [Flashcards](#flashcards)

---

## 1. What a trie is

A **trie** (from re*trie*val, also called a prefix tree) is a rooted tree where:
- the root is the empty string;
- each edge is labelled with one character;
- the path from the root to a node spells a **prefix**;
- a node is marked as a word end if some inserted key finishes there.

```
insert: app, apple, apt, bat

        (root)
        /    \
       a      b
       |      |
       p      a
      / \     |
     p*  t*   t*
     |
     l
     |
     e*          * = end of a word
```

| Property | Consequence |
|---|---|
| Common prefixes share nodes | `app` and `apple` reuse 3 nodes; memory grows with **distinct prefixes**, not total keys |
| Depth = key length | Every operation is O(L) |
| Children are ordered by symbol | A DFS that visits children `a → z` lists keys in **lexicographic order** |
| A node's subtree = all keys with that prefix | Prefix queries (count, list, autocomplete) start from one node |

---

## 2. Node design

| Choice | Pros | Cons | Use when |
|---|---|---|---|
| `children[26]` array | O(1) child access, simple, cache-friendly | 26 pointers per node, even when they are empty | Lowercase-only interview problems |
| Hash map per node | Memory ∝ actual children; any alphabet | Hashing overhead; unordered (sort to get lex order) | Unicode, large or sparse alphabets |
| Flat arrays `t[node][c]` with int ids | No pointers, fast, easy to reset | Must pre-size or grow a vector | Competitive / bulk-insert problems (binary tries) |

Fields to add as the problem needs them:

| Field | Meaning | Needed for |
|---|---|---|
| `end` (bool) | Some word finishes here | search, complete string |
| `end` (int) | How many copies finish here | duplicates, `countWordsEqualTo`, erase |
| `pass` (int) | How many words go through here | `countWordsStartingWith`, safe deletion |
| `word` (string / id) | The key stored at this end | Word Search II (avoid rebuilding the path) |
| `min` / `max` | Extremes of the values in this subtree | Online constrained XOR queries |

---

## 3. Core operations

All three share one loop: **walk the characters from the root**.

```python
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, w):
        n = self.root
        for c in w:
            n = n.setdefault(c, {})   # create the child if missing
        n['$'] = True                  # mark end of word

    def _walk(self, s):                # last node of s, or None
        n = self.root
        for c in s:
            if c not in n:
                return None
            n = n[c]
        return n

    def search(self, w):
        n = self._walk(w)
        return n is not None and '$' in n

    def startsWith(self, p):
        return self._walk(p) is not None
```

| Operation | Walk | Then |
|---|---|---|
| `insert(w)` | Create missing children | Set `end` on the last node |
| `search(w)` | Fail on a missing child | Return the last node's `end` |
| `startsWith(p)` | Fail on a missing child | Return true (the path exists) |
| List keys with prefix `p` | Walk to `p` | DFS the subtree, collecting ends |

> [!tip] Interview move
> Write `_walk` first. `search` and `startsWith` are then one line each, and it's obvious they differ only in the `end` check.

---

## 4. Counters and erase

Duplicates and prefix counts need integer counters:
- `insert`: walk the path, do `pass++` on each node, then `end++` on the last node.
- `countWordsEqualTo(w)`: read `end` at the last node of `w`, or 0 if the path breaks.
- `countWordsStartingWith(p)`: read `pass` at the last node of `p`, or 0.
- `erase(w)`: walk the same path, do `pass--` on each node, then `end--` on the last node.

```
insert apple ×2, apps        pass shown on each node, end in [ ]

root → a:3 → p:3 → p:3 → l:2 → e:2[2]
                       ↘ s:1[1]

countWordsStartingWith("app") = 3
erase("apple")  → l:1, e:1[1]
```

**Physical deletion:** once a child's `pass` drops to 0, nothing passes through it any more, so you can set the pointer to null and free the subtree. Without a `pass` counter, you have to delete recursively bottom-up, removing a node only if it has no children and is not an end.

---

## 5. Complexity and memory

| Operation | Time | Notes |
|---|---|---|
| insert / search / startsWith / erase | O(L) | Independent of the number of keys `N` |
| Build from `N` keys | O(Σ L) | |
| List all keys with a prefix | O(L + size of the subtree) | |
| Memory | O(total distinct prefixes × alphabet) for arrays | Worst case O(Σ L · 26) when there is no sharing |

A suffix trie of a string with `n` characters has O(n²) nodes. That's fine for `n ≤ 10³`. Above that, use suffix arrays or automata (beyond the interview bar).

---

## 6. Trie vs hash set

| Need | Hash set | Trie |
|---|---|---|
| Exact membership | O(L) expected, simpler | O(L) |
| "Is any key a prefix of / prefixed by x?" | O(L) lookups of every prefix, each O(L), so O(L²) | O(L), one walk |
| Count / list keys with a prefix | Scan all keys | One subtree |
| Lexicographic order | Sort separately | DFS order |
| Many patterns against a grid / text | Re-check each word | Prune a DFS as soon as no key has the current path as a prefix (Word Search II) |
| Memory | Lower for few, long, unrelated keys | Lower when keys share prefixes |

**Rule:** reach for a trie when the problem talks about **prefixes** or when many keys are matched **character by character simultaneously**.

---

## 7. Bit prerequisites

A binary trie stores each integer as a fixed-length bit string, most significant bit first.

| Operation | Expression | Example (`x = 13 = 1101₂`) |
|---|---|---|
| Bit `i` of `x` | `(x >> i) & 1` | bit 2 → 1 |
| Is bit `i` set? | `x & (1 << i)` ≠ 0 | |
| Set bit `i` | `x \| (1 << i)` | set bit 1 → 1111₂ = 15 |
| Clear bit `i` | `x & ~(1 << i)` | clear bit 3 → 0101₂ = 5 |
| Toggle bit `i` | `x ^ (1 << i)` | toggle bit 0 → 1100₂ = 12 |
| Flip a single bit value `b` | `b ^ 1` or `1 − b` | the "opposite" child |

XOR identities used in trie problems:

| Identity | Use |
|---|---|
| `a ^ a = 0`, `a ^ 0 = a` | Prefix XOR: `XOR(l..r) = P[r+1] ^ P[l]` |
| Commutative and associative | Order doesn't matter |
| Bit `i` of `a ^ b` is 1 ⇔ bit `i` of `a` ≠ bit `i` of `b` | The greedy wants **different** bits |
| `a ^ b = c` ⇔ `a ^ c = b` | "Is there a pair with XOR = c?" turns into a hash-set lookup |

**Width:** values `< 2³¹` need bits 30 down to 0 (31 levels). Values up to `10⁹ < 2³⁰` would fit in 30 bits, but 31 is the safe default. Use a fixed width for every number, so that bit `i` lands at the same depth for all keys.

---

## 8. Binary trie and greedy max XOR

**Problem:** given a set `S` of integers and a query `x`, find `max(x ^ a)` over `a ∈ S`.

**Greedy claim:** walk from the MSB. At each bit, go to the child whose bit is **opposite** to `x`'s bit if it exists; otherwise go to the same-bit child.

**Why it's optimal:** taking the opposite bit at level `b` makes bit `b` of the result 1. Any candidate that gives up bit `b` has a result of at most `2^b − 1` in the lower bits, and `2^b − 1 < 2^b`. So no choice in lower bits can make up for losing a higher bit. This is the same exchange argument as comparing numbers lexicographically by their binary digits.

```python
def max_xor(t, x):              # t[node] = [child0, child1]; 0 = missing
    n = cur = 0
    for b in range(30, -1, -1):
        want = ((x >> b) & 1) ^ 1
        if t[n][want]:
            cur |= 1 << b
            n = t[n][want]
        else:
            n = t[n][want ^ 1]   # must exist: every stored path has full length
    return cur
```

| Variant | Reduction |
|---|---|
| Max XOR of two array elements | Insert all; query each element |
| Max XOR subarray | Insert prefix XORs; query each `P[i]` against `P[0..i−1]` |
| Min XOR pair | Prefer the **same** bit (or: sort, then the answer is the min over adjacent pairs) |
| Count pairs with XOR `< k` | Store `pass` counts; at each bit, add the subtree that keeps the result below `k` |
| Max XOR with `a ≤ m` | Offline (§9) or keep subtree minima (online) |

---

## 9. Offline queries

When each query restricts **which stored elements are allowed**, and the restriction is monotone (for example `a ≤ m`), you don't need to delete from the trie:

1. Sort the data ascending.
2. Sort the queries by their limit, **remembering each query's original index**.
3. Sweep: before answering a query, insert every data element `≤ m` that hasn't been inserted yet.
4. Answer it with a normal query, and store the result at the original index.

Each element is inserted once, so the total cost is O((n + q) log(n + q) + 31(n + q)).

> [!note] Online alternative
> Store `min` of the subtree in every node. During a query, refuse any child whose `min > m`. If the root's `min > m`, the answer is −1. This is O(31) per query with no sorting, at the cost of one extra field per node.

The same "sort queries, sweep data" pattern appears with DSU (connectivity under weight limits) and Fenwick trees (offline counts).

---

## 10. Trie patterns

| Signal in the problem | Pattern | Example |
|---|---|---|
| "starts with", autocomplete, prefix count | Walk to the prefix node; read a counter or DFS | Trie II, search suggestions |
| "every prefix is also a word" | Every node on the path is an end | Complete string, longest word in dictionary |
| Count distinct substrings | Insert all suffixes; count the nodes created | Distinct substrings |
| Match many words in a grid | Trie of words + DFS on the grid, pruning on a missing child | Word Search II |
| Word with wildcards `.` | DFS branches over all children at a `.` | Add and search word |
| Replace words by their shortest root | Walk until the first end | Replace words |
| Maximise / count XOR | Binary trie, MSB first | Max XOR pair, max XOR with limit |

---

## Common mistakes

| Mistake | Fix |
|---|---|
| `search` returns true because the path exists | Also check `end` on the last node |
| New root created per insert | One root, created in the constructor |
| Boolean `end` when duplicates matter | Integer `end` (and `pass`) counters |
| Binary trie walked LSB first | MSB first; the greedy depends on it |
| Different bit widths for different numbers | Fixed width (bits 30..0) for every key |
| Querying an empty binary trie | Guard: insert first, or return −1 / 0 |
| Offline answers returned in sorted order | Store each answer at its original index |
| Rebuilding substrings inside a suffix-trie loop | Extend the walk by one character, O(1) per step |

---

## Practice

<details><summary>1. Why is trie lookup O(L) and not O(L log N)?</summary>

Each step follows one child pointer chosen by the next character, in O(1) with an array (expected O(1) with a hash map). The number of keys stored never enters the cost; only the path length does.
</details>

<details><summary>2. Insert "car", "card", "care", "cat". How many nodes, excluding the root?</summary>

c, a, r, d, e, t gives **6**. `c-a` is shared by everything, `r` is shared by car/card/care, and `d`, `e`, `t` are leaves.
</details>

<details><summary>3. After those inserts, what is `pass` at the node for "car"?</summary>

3 (car, card, care pass through it), and its `end` is 1.
</details>

<details><summary>4. Max XOR of x = 6 (110) with S = {1 (001), 4 (100), 3 (011)}?</summary>

Bit 2: x has 1, so we want 0: the subtrees of 1 and 3 qualify → result bit 2 = 1. Bit 1: x has 1, want 0: 1 (001) has 0 there → take it. Bit 0: x has 0, want 1: 1 has 1. Result `111 = 7` (6 ^ 1).
</details>

<details><summary>5. Distinct substrings of "abab" (including the empty string)?</summary>

Suffixes abab, bab, ab, b. Inserting abab creates 4 nodes; bab creates 3; ab and b create 0. So 7 + 1 = **8**.
</details>

<details><summary>6. How would you find the maximum XOR of any subarray?</summary>

Insert `P[0] = 0`. For each `i`, query `P[i+1]` against the trie, then insert `P[i+1]`. `XOR(l..r) = P[r+1] ^ P[l]`, so the best pair of prefixes gives the answer. O(31·n).
</details>

<details><summary>7. When does a hash set beat a trie?</summary>

When only exact membership is needed and the keys share few prefixes. Then the trie's per-node overhead (26 pointers) costs memory without any benefit.
</details>

<details><summary>8. Queries (x, m) arrive one at a time. How do you answer max XOR with a ≤ m?</summary>

Store the minimum value of each node's subtree. While walking, only take a child whose `min ≤ m`, preferring the opposite bit. If the root's `min > m`, the answer is −1.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Trie / prefix tree | Tree where each root-to-node path spells a prefix |
| End flag / end count | Marks how many inserted keys finish at a node |
| Pass count | Number of inserted keys whose path goes through a node |
| Suffix trie | Trie of all suffixes of one string; its nodes are the distinct substrings |
| Binary trie | Trie over bits (alphabet {0, 1}), keys stored MSB first at a fixed width |
| Radix / compressed trie | Trie where chains of single-child nodes merge into one edge |
| Offline queries | Answering queries in a chosen order and restoring the original order at the end |

---

## Flashcards

**What does a trie node store?** #flashcard
Child pointers (26-array or map) plus an end-of-word flag or counter.

**search vs startsWith?** #flashcard
Both walk the path; search also requires `end` at the last node.

**Trie operation cost?** #flashcard
O(L) in the key length, independent of the number of keys.

**What are pass and end counters for?** #flashcard
pass = words through the node (prefix count); end = words ending there (exact count, duplicates).

**How do you erase from a counting trie?** #flashcard
Walk the path decrementing pass, then decrement end at the last node.

**Distinct substrings with a trie?** #flashcard
Insert every suffix and count the nodes created (+1 if the empty string counts).

**Complete-string test?** #flashcard
Every node on the word's path has end = true.

**Get bit i of x?** #flashcard
`(x >> i) & 1`.

**Why is max XOR greedy from the MSB?** #flashcard
Bit b (worth 2^b) beats all lower bits combined (2^b − 1).

**Binary trie max-XOR step?** #flashcard
Take the child with the opposite bit if it exists (set that result bit); else the same bit.

**Why fix the bit width in a binary trie?** #flashcard
So bit i sits at the same depth for every key, and paths are comparable.

**Max XOR with a ≤ m, offline?** #flashcard
Sort nums and queries by m; insert nums ≤ m before each query; answer by original index.

**Max XOR with a ≤ m, online?** #flashcard
Store the subtree minimum per node; skip children whose min > m.

**Max XOR subarray?** #flashcard
Binary trie of prefix XORs; query each P[i] against the earlier ones.

**Interview track →** [Trie deep-dive](../../01-data-structures/09-trie.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md) · [Trie walkthroughs](../../coding/data-structures/09-trie.md)
