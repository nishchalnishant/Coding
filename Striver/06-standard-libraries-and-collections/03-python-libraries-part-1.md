---
module: striver/06-standard-libraries-and-collections
lesson: 3
topic: Python built-ins for DSA — list, tuple, set, dict, str, sorting
source: https://takeuforward.org/learning/dsa/python-libraries-part-1?category=standard-libraries-and-collections&source=strivers-a2z-dsa-sheet
tags: [striver, python, list, dict, set, tuple, slicing, sorting, comprehension]
---
# 3. Python Libraries: Part 1 (Built-ins)

← [Java Collections](02-java-collections.md) · [Part 6 index](README.md) · Next → [Python Libraries Part 2](04-python-libraries-part-2.md)

> [!abstract] What this covers
> **Core idea:** Python's built-in `list`, `tuple`, `set`, `dict` and `str` cover most DSA needs without imports. They're expressive, but their costs are hidden: `in` on a list is O(n), `pop(0)` is O(n), slicing copies, and `str` is immutable. Know the costs and the idioms.
> **You'll be able to:** use each built-in with correct complexity, write slices and comprehensions, sort with `key=`, avoid aliasing bugs, and handle Python's integers, recursion limit and fast I/O.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/python-libraries-part-1?category=standard-libraries-and-collections&source=strivers-a2z-dsa-sheet) · **Time:** 90 min

**Sections:** [1. Overview](#1-overview) · [2. list](#2-list) · [3. Slicing](#3-slicing) · [4. tuple](#4-tuple) · [5. set](#5-set) · [6. dict](#6-dict) · [7. str](#7-str) · [8. Comprehensions](#8-comprehensions) · [9. Sorting](#9-sorting) · [10. Handy built-ins](#10-handy-built-ins) · [11. Aliasing & copies](#11-aliasing-and-copies) · [12. Python-specific gotchas](#12-python-specific-gotchas) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Overview

| Type | Mutable | Ordered | Duplicates | Hashable (usable as key) | Backed by |
|---|---|---|---|---|---|
| `list` | ✅ | ✅ | ✅ | ❌ | dynamic array |
| `tuple` | ❌ | ✅ | ✅ | ✅ (if items are) | fixed array |
| `set` | ✅ | ❌ | ❌ | ❌ (`frozenset` ✅) | hash table |
| `dict` | ✅ | ✅ insertion (3.7+) | keys unique | ❌ | hash table |
| `str` | ❌ | ✅ | ✅ | ✅ | array of code points |

---

## 2. list

```python
a = []                     # or list()
a = [0] * n                # n zeros
grid = [[0] * m for _ in range(n)]      # ✅ n independent rows
bad  = [[0] * m] * n                    # ❌ n references to ONE row
a.append(x); a.pop(); a.pop(i); a.insert(i, x)
a.extend([4, 5]); a + [6]; a.remove(x)  # remove first x, ValueError if absent
a.index(x); a.count(x); x in a; len(a)
a.reverse(); a[::-1]; a.sort(); sorted(a)
```

| Operation | Cost |
|---|---|
| `a[i]`, `a[i] = x`, `len`, `append`, `pop()` | O(1) (append amortised) |
| `pop(0)`, `insert(0, x)`, `pop(i)`, `insert(i, x)` | **O(n)** |
| `x in a`, `index`, `count`, `remove` | **O(n)** |
| `a[l:r]` (slice) | O(r − l), creates a copy |
| `a + b` | O(len a + len b) new list |
| `sort` | O(n log n) |

> [!warning] `pop(0)` in BFS is O(n)
> A queue built on `list.pop(0)` turns BFS into O(V²). Use `collections.deque` and `popleft()` ([Part 2](04-python-libraries-part-2.md#2-collectionsdeque)).

---

## 3. Slicing

`a[start:stop:step]` — start inclusive, stop exclusive, any part optional, negatives count from the end.

| Expression | Result for `a = [0,1,2,3,4,5]` |
|---|---|
| `a[1:4]` | `[1, 2, 3]` |
| `a[:3]` | `[0, 1, 2]` |
| `a[3:]` | `[3, 4, 5]` |
| `a[-1]` | `5` |
| `a[-3:]` | `[3, 4, 5]` |
| `a[::2]` | `[0, 2, 4]` |
| `a[::-1]` | `[5, 4, 3, 2, 1, 0]` |
| `a[4:1:-1]` | `[4, 3, 2]` |
| `a[10:]` | `[]` (slices never raise IndexError) |

Slice assignment edits in place: `a[1:3] = [9]` → `[0, 9, 3, 4, 5]`. `a[:] = …` replaces contents without rebinding (matters when `a` is shared).

> [!tip] Slices in recursion cost O(n)
> `solve(a[1:])` copies n − 1 elements per call → O(n²) total. Pass indices: `solve(a, i + 1)`.

---

## 4. tuple

```python
t = (1, 2, 3); single = (1,)       # trailing comma for a 1-tuple
x, y = 3, 4                        # tuple packing/unpacking
x, y = y, x                        # swap
first, *rest = [1, 2, 3]           # rest = [2, 3]
seen = {(r, c)}                    # tuples as set/dict keys (grid cells, states)
memo[(i, j)] = val
```

Tuples compare lexicographically, which is why `heapq` with `(priority, item)` tuples and `sorted(list_of_tuples)` work naturally.

---

## 5. set

```python
s = set()                  # NOT {} — that's an empty dict
s = {1, 2, 3}; s = set(arr)
s.add(x); s.remove(x)      # KeyError if absent
s.discard(x)               # no error
x in s; len(s)
a | b; a & b; a - b; a ^ b # union, intersection, difference, symmetric difference
a <= b                     # subset
```

| Operation | Cost |
|---|---|
| `add`, `discard`, `in` | O(1) average |
| `a | b`, `a & b` | O(len a + len b), O(min(len a, len b)) |
| Iteration | O(n), **arbitrary order** |

Only **hashable** items go in a set: no lists, no sets. Convert: `tuple(lst)`, `frozenset(s)`.

---

## 6. dict

```python
d = {}; d = {'a': 1}; d = dict(zip(keys, vals))
d[k] = v; d[k]                    # KeyError if absent
d.get(k, 0)                       # default instead of error
d[x] = d.get(x, 0) + 1            # frequency count
d.setdefault(k, []).append(v)     # map of lists
k in d; del d[k]; d.pop(k, None)
for k, v in d.items(): ...
for k in d: ...; d.keys(); d.values()
max(d, key=d.get)                 # key with the largest value
{k: v for k, v in pairs}          # dict comprehension
```

| Operation | Cost |
|---|---|
| get / set / `in` / `del` | O(1) average, O(n) worst |
| Iteration | O(n), **insertion order** (3.7+) |

> [!warning] Don't modify a dict while iterating it
> Adding/removing keys during `for k in d` raises `RuntimeError: dictionary changed size during iteration`. Iterate over `list(d)` instead.

---

## 7. str

Strings are **immutable**: every "modification" builds a new string.

```python
s[i]; s[l:r]; len(s); s[::-1]
s.lower(); s.upper(); s.strip(); s.split(); s.split(',')
' '.join(words); ''.join(chars)
s.find(sub)        # index or -1
s.index(sub)       # ValueError if absent
s.count(sub); s.startswith(p); s.endswith(p); s.replace(a, b)
s.isdigit(); s.isalpha(); s.isalnum(); s.isspace()
ord('a') == 97; chr(97) == 'a'
ord(c) - ord('a')                     # letter → 0..25
f"{x} and {y:.2f}"
```

> [!danger] `s += c` in a loop
> CPython sometimes optimises it, but it's O(n²) in the worst case and in other interpreters. Build a list and `''.join(parts)` once: O(n).

To edit characters in place: `chars = list(s)`, modify, then `''.join(chars)`.

---

## 8. Comprehensions

```python
squares = [x * x for x in range(n)]
evens   = [x for x in a if x % 2 == 0]
pairs   = [(i, j) for i in range(n) for j in range(i + 1, n)]   # outer loop first
grid    = [[0] * m for _ in range(n)]
freq    = {c: s.count(c) for c in set(s)}       # O(n · k) — prefer Counter
uniq    = {x % 10 for x in a}
total   = sum(x for x in a if x > 0)            # generator: no intermediate list
```

Comprehensions are faster than equivalent `append` loops, and clearer for one-step transforms. Avoid them for side effects or deep nesting.

---

## 9. Sorting

```python
a.sort()                          # in place, returns None
b = sorted(a)                     # new list; works on any iterable
a.sort(reverse=True)
words.sort(key=len)
pts.sort(key=lambda p: (p[1], -p[0]))      # by y asc, then x desc
people.sort(key=lambda p: (-p.age, p.name))
```

- **Timsort**: O(n log n), **stable** (equal keys keep their order). Stability lets you sort by multiple keys in passes: sort by the secondary key first, then by the primary.
- `key=` is called once per element (O(n) calls) — much faster than a comparator.
- Need a true two-argument comparator? `functools.cmp_to_key` ([Part 2](04-python-libraries-part-2.md#7-functools)) — e.g. "largest number" from concatenations.
- Negating a key works for numbers only. For descending strings inside a tuple key, sort in two stable passes.

> [!warning] `a = a.sort()` sets a to None
> `list.sort()` returns `None`. Use `sorted(a)` if you need the result as a value.

---

## 10. Handy built-ins

| Built-in | Example | Notes |
|---|---|---|
| `range(a, b, step)` | `range(n - 1, -1, -1)` | reverse loop |
| `enumerate(a, start=0)` | `for i, x in enumerate(a)` | index + value |
| `zip(a, b)` | `for x, y in zip(a, b)` | stops at the shorter |
| `reversed(a)` | iterator, no copy | |
| `min/max(a, key=…, default=…)` | `max(d, key=d.get)` | `default` avoids error on empty |
| `sum(a)`, `any(…)`, `all(…)` | `all(x > 0 for x in a)` | short-circuit |
| `abs`, `pow(b, e, m)` | `pow(2, 10**18, 10**9+7)` | fast modular power |
| `divmod(a, b)` | `q, r = divmod(17, 5)` | |
| `map(int, input().split())` | parse a line of ints | |
| `float('inf')`, `-float('inf')` | sentinels | `math.inf` also works |
| `int(s, 2)`, `bin(x)`, `hex(x)` | `bin(5) == '0b101'` | `bin(x).count('1')` = popcount |
| `isinstance(x, int)` | type check | |

---

## 11. Aliasing and copies

Variables are **names bound to objects**. Assignment never copies.

```python
a = [1, 2, 3]
b = a           # same object
b.append(4)     # a is now [1, 2, 3, 4]
c = a[:]        # or list(a), a.copy() — shallow copy
import copy
g2 = copy.deepcopy(grid)       # nested lists need a deep copy (or [row[:] for row in grid])
```

| Situation | Bug | Fix |
|---|---|---|
| `[[0]*m]*n` | all rows alias one list | `[[0]*m for _ in range(n)]` |
| `res.append(path)` in backtracking | stored lists change later | `res.append(path[:])` |
| Default arg `def f(x, memo={})` | memo persists across calls | `memo=None`, then create inside |
| Function mutates argument | caller's list changes | copy first, or document it |

---

## 12. Python-specific gotchas

| Topic | Fact | Consequence |
|---|---|---|
| Integers | Arbitrary precision — no overflow | Great for big factorials; but still apply `% MOD` when asked, and be aware big ints are slower |
| `/` vs `//` | `/` is float division, `//` is floor division | `-7 // 2 == -4` (floors toward −∞), C++/Java give −3 |
| `%` with negatives | `-7 % 3 == 2` | Always non-negative for a positive modulus (unlike C++/Java) |
| Recursion limit | default ≈ 1000 | `sys.setrecursionlimit(10**6)`; deep DFS may still crash → iterate |
| Speed | ~10–50× slower than C++ | ~10⁷ simple ops/s; prefer built-ins and comprehensions |
| Fast input | `input()` is slow for 10⁵+ lines | `import sys; input = sys.stdin.readline` (strip the `\n`) |
| Truthiness | `0`, `''`, `[]`, `{}`, `None` are falsy | `if node:` vs `if node is not None:` differ when the value can be 0 |
| `is` vs `==` | `is` = identity | Use `is` only for `None` |

---

## Common mistakes

1. `[[0]*m]*n` for a grid.
2. `list.pop(0)` as a queue.
3. `x in list` inside a loop → O(n²); convert to a set first.
4. `s = {}` expecting an empty set.
5. `a = a.sort()`.
6. String concatenation in a loop.
7. Appending a mutable `path` without copying.
8. Integer division `//` with negatives behaving differently from C++/Java.
9. Hitting the recursion limit on 10⁴-deep recursion.

---

## Practice

1. Rotate a list right by k in one line.
2. Check whether two strings are anagrams in O(n) without importing anything.
3. Build the transpose of an n × m matrix using a comprehension (and with `zip`).
4. Sort a list of strings by length descending, ties alphabetically ascending.
5. Why is `for x in a: if x in b:` slow when b is a list of 10⁵ items? Fix it.
6. What does `print(-7 // 2, -7 % 2, int(-7 / 2))` print?

<details><summary>Answer sketches</summary>

**#1:** `k %= len(a); a[:] = a[-k:] + a[:-k]`. k = 0 is safe: `a[-0:]` is the whole list and `a[:-0]` is empty. Guard `len(a) == 0` before the `%`.

**#2:** a dict of counts: `d[c] = d.get(c, 0) + 1` for s, decrement for t, check all zero; or `sorted(s) == sorted(t)` in O(n log n).

**#3:** `[[g[i][j] for i in range(n)] for j in range(m)]`; `[list(col) for col in zip(*g)]`.

**#4:** `words.sort(key=lambda w: (-len(w), w))`.

**#5:** each `in` scans the list: O(|a| · |b|). Use `bs = set(b)` once → O(|a| + |b|).

**#6:** `-4 1 -3`.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Mutable / immutable | Can / cannot be changed in place |
| Hashable | Has a fixed hash; required for set elements and dict keys |
| Slice | `a[start:stop:step]`, creates a shallow copy |
| Shallow vs deep copy | Copies the outer container only vs recursively copies everything |
| Comprehension | `[expr for x in it if cond]` — builds a list/set/dict in one expression |
| Stable sort | Equal keys keep their original relative order |

---

## Flashcards

**Why is `[[0]*m]*n` wrong for a grid?** #flashcard
It creates n references to the same row; changing one cell changes the whole column. Use `[[0]*m for _ in range(n)]`.

**Cost of `list.pop(0)` and the fix?** #flashcard
O(n). Use `collections.deque.popleft()`, O(1).

**Cost of `x in list` vs `x in set`?** #flashcard
O(n) vs O(1) average.

**How do you sort by y ascending then x descending?** #flashcard
`pts.sort(key=lambda p: (p[1], -p[0]))`.

**What does `list.sort()` return?** #flashcard
`None` — it sorts in place. `sorted()` returns a new list.

**`-7 // 2` and `-7 % 2` in Python?** #flashcard
`-4` and `1` — floor division rounds toward −∞.

**How do you build a string efficiently?** #flashcard
Append pieces to a list, then `''.join(parts)` once.

**Why copy `path[:]` in backtracking?** #flashcard
Appending `path` stores a reference; later pushes/pops would change every stored result.

**Interview track →** [L3 Cheatsheet](../../00-L3-EXECUTION-META/L3_CHEATSHEET.md) · [Array deep-dive](../../01-data-structures/01-array.md) · [String deep-dive](../../01-data-structures/03-string.md)
