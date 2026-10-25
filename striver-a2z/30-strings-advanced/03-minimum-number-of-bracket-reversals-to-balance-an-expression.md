---
module: striver-a2z/30-strings-advanced
lesson: 3
topic: Minimum number of bracket reversals to balance an expression
difficulty: Medium
source: https://takeuforward.org/learning/dsa/minimum-number-of-bracket-reversals-to-make-an-expression-balanced?category=medium-problems&source=strivers-a2z-dsa-sheet
tags: [striver, strings--advanced-algo, string, greedy, stack]
---
# 3. Minimum number of bracket reversals to balance an expression

← [Reverse every word in a string](02-reverse-every-word-in-a-string.md) · [Part 30 index](README.md) · Next → [Count and say](04-count-and-say.md)

> [!abstract] Problem at a glance
> **Task:** Count the fewest `{`↔`}` flips that make a curly-bracket string balanced, or `-1` if impossible.
> **Key insight:** Cancel matched pairs greedily. What's left looks like `}}}…{{{`: `c` unmatched closers followed by `o` unmatched openers. Two closers `}}` need 1 flip, two openers `{{` need 1, and a leftover `}{` needs 2. So the answer is `⌈c/2⌉ + ⌈o/2⌉`. An odd length can never balance.
> **Difficulty:** Medium · **Pattern:** Greedy matching with counters · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/count-the-reversals0401/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-number-of-bracket-reversals-to-make-an-expression-balanced?category=medium-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Stack of unmatched brackets](#3-stack-of-unmatched-brackets) · [4. Two counters](#4-two-counters) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a string `s` of only `{` and `}`, return the minimum number of reversals (turning `{` into `}` or vice versa) needed to make it balanced, or `-1` if that is impossible.

| Input | Output | Why |
|---|---|---|
| `"}{{}}{{{"` | `3` | after cancelling: `}{{{` → c=1, o=3 → 1 + 2 |
| `"{{}{{{}{{}}{{"` | `-1` | odd length |
| `"}}}}"` | `2` |  |

**Constraints:** `1 ≤ |s| ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Stack of unmatched brackets | push, pop on a match, count what remains | O(n) | O(n) |
| Two counters | open = unmatched '{', close = unmatched '}' | O(n) | O(1) |

> [!tip] Interview angle
> Say the odd-length check first. Then explain why matched pairs can be removed safely (flipping inside a matched pair never helps), and derive `⌈c/2⌉ + ⌈o/2⌉` from the `}}}{{{` shape. Note that `c` and `o` have the same parity when n is even.

---

## 3. Stack of unmatched brackets

**Intuition.** Push each bracket; if it is `}` and the top is `{`, pop instead. The stack ends as `}…}{…{`. Count both kinds and apply the formula.

```python
def count_rev_stack(s):
    if len(s) % 2:
        return -1
    st = []
    for c in s:
        if c == '}' and st and st[-1] == '{':
            st.pop()
        else:
            st.append(c)
    o = st.count('{')
    c = len(st) - o
    return (o + 1) // 2 + (c + 1) // 2
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Two counters

**Intuition.** The stack only ever holds `}`s below `{`s, so two counters replace it: on `{` do `open++`; on `}` cancel an open if there is one, otherwise `close++`.

**Algorithm**

1. If `n` is odd, return `-1`.
2. For each char: `{` → `open++`; `}` → `open > 0 ? open-- : close++`.
3. Return `(open + 1) / 2 + (close + 1) / 2`.

**Dry run** — }{{}}{{{: } close=1; { o=1; { o=2; } o=1; } o=0; { { { o=3. ⌈3/2⌉ + ⌈1/2⌉ = 2 + 1 = 3.

**C++**
```cpp
int countRev(const string& s) {
    if (s.size() % 2) return -1;
    int open = 0, close = 0;
    for (char c : s) {
        if (c == '{') open++;
        else if (open) open--;
        else close++;
    }
    return (open + 1) / 2 + (close + 1) / 2;
}
```

**Java**
```java
static int countRev(String s) {
    if (s.length() % 2 == 1) return -1;
    int open = 0, close = 0;
    for (char c : s.toCharArray()) {
        if (c == '{') open++;
        else if (open > 0) open--;
        else close++;
    }
    return (open + 1) / 2 + (close + 1) / 2;
}
```

**Python**
```python
def count_rev(s):
    if len(s) % 2:
        return -1
    open_ = close = 0
    for c in s:
        if c == '{':
            open_ += 1
        elif open_:
            open_ -= 1
        else:
            close += 1
    return (open_ + 1) // 2 + (close + 1) // 2
```

**Complexity:** time **O(n)**, space **O(1)** — one pass with two integers.

---

## Edge cases

- Already balanced → 0.
- `}{` → 2.
- Odd length → -1.

---

## Common mistakes

1. Missing the odd-length check.
2. Returning `(o + c) / 2`, which undercounts `}{` (needs 2, not 1).
3. Cancelling `}{` as if it were a pair.

---

## Follow-ups

1. Brackets of three types with replacements allowed?
2. Minimum additions instead of reversals (LC 921)?

<details><summary>Answer sketches</summary>

**#1:** A different problem: count unmatched with a stack, and replacements fix mismatched types.

**#2:** Answer = open + close (unmatched counts).
</details>

---

## Flashcards

**Bracket reversals formula?** #flashcard
⌈open/2⌉ + ⌈close/2⌉ after cancelling matched pairs; -1 if the length is odd.

**Why does `}{` cost 2?** #flashcard
Each of the two brackets has to be flipped to give `{}`.

**Interview track →** [String algorithms deep-dive](../../02-algorithms/02-string-algorithms.md) · [String algorithm walkthroughs](../../04-practice/algorithms/02-string-algorithms.md)
