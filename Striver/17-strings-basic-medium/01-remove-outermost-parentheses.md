---
module: striver/17-strings-basic-medium
lesson: 1
topic: Remove Outermost Parentheses
difficulty: Easy
source: https://takeuforward.org/learning/dsa/remove-outermost-parentheses?category=parentheses&source=strivers-a2z-dsa-sheet
tags: [striver, strings-basic-and-medium, string, stack]
---
# 1. Remove Outermost Parentheses

← [Part 17 index](README.md) · Next → [Maximum Nesting Depth of the Parentheses](02-maximum-nesting-depth-of-the-parentheses.md)

> [!abstract] Problem at a glance
> **Task:** Split a valid parentheses string into primitive parts and strip the outer pair of each.
> **Key insight:** Track depth. A `(` that takes depth 0 → 1 opens a primitive, and a `)` that takes depth 1 → 0 closes it. Those are the only chars to drop; keep everything else.
> **Difficulty:** Easy · **Pattern:** Depth counter (implicit stack) · **Also on:** [LC 1021](https://leetcode.com/problems/remove-outermost-parentheses/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/remove-outermost-parentheses?category=parentheses&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Split into primitives, then strip](#3-split-into-primitives-then-strip) · [4. Depth counter](#4-depth-counter) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A valid parentheses string is **primitive** if it is non-empty and cannot be split into two non-empty valid strings. Every valid string `s` decomposes uniquely as `P₁P₂…Pₖ` of primitives. Return `s` after removing the outermost parentheses of every primitive.

| Input | Output | Why |
|---|---|---|
| `s = "(()())(())"` | `"()()()"` | primitives (()()) and (()) → ()() + () |
| `s = "(()())(())(()(()))"` | `"()()()()(())"` |  |
| `s = "()()"` | `""` | each primitive is just () |

**Constraints:** `1 ≤ |s| ≤ 10⁵`, `s[i] ∈ {'(', ')'}`, `s` is valid.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Split into primitives, then strip | find each primitive's end via balance, slice [start+1, end) | O(n) | O(n) |
| Depth counter | drop ( at depth 0 and ) back to depth 0 | O(n) | O(n) output |

> [!tip] Interview angle
> Easy warm-up that checks whether you reach for a stack by reflex. With one bracket type, the stack only ever holds `(`, so its size is all that matters — an int. Mention that a stack is the general tool for mixed brackets (`([{`).

---

## 3. Split into primitives, then strip

**Intuition.** Walk with a balance counter. When it returns to 0 at index `i`, the primitive is `s[start..i]`; append `s[start+1:i]` and set `start = i + 1`. Same complexity, but slicing makes the logic explicit.

```python
def remove_outer_split(s):
    out, bal, start = [], 0, 0
    for i, c in enumerate(s):
        bal += 1 if c == '(' else -1
        if bal == 0:
            out.append(s[start + 1:i])
            start = i + 1
    return "".join(out)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Depth counter

**Intuition.** For `(`: if depth > 0 before incrementing, it's inner — keep it. For `)`: decrement first; if depth > 0 after, it's inner — keep it. Ordering the increment/decrement around the check is the whole trick.

**Algorithm**

1. `depth = 0`.
2. `(`: if `depth > 0` append; `depth++`.
3. `)`: `depth--`; if `depth > 0` append.
4. Return the built string.

**Dry run** — `(()())`: `(` d0 skip→1; `(` keep→2; `)` →1 keep; `(` keep→2; `)` →1 keep; `)` →0 skip. Output `()()`.

**C++**
```cpp
string removeOuterParentheses(string s) {
    string res;
    int depth = 0;
    for (char c : s) {
        if (c == '(') {
            if (depth > 0) res += c;
            depth++;
        } else {
            depth--;
            if (depth > 0) res += c;
        }
    }
    return res;
}
```

**Java**
```java
static String removeOuterParentheses(String s) {
    StringBuilder res = new StringBuilder();
    int depth = 0;
    for (char c : s.toCharArray()) {
        if (c == '(') {
            if (depth > 0) res.append(c);
            depth++;
        } else {
            depth--;
            if (depth > 0) res.append(c);
        }
    }
    return res.toString();
}
```

**Python**
```python
def remove_outer(s):
    res, depth = [], 0
    for c in s:
        if c == '(':
            if depth > 0:
                res.append(c)
            depth += 1
        else:
            depth -= 1
            if depth > 0:
                res.append(c)
    return "".join(res)
```

**Complexity:** time **O(n)**, space **O(n) output** — one pass; output holds at most n − 2 chars.

---

## Edge cases

- Every primitive is `()` → empty output.
- One primitive covering the whole string.
- Deep nesting `((((...))))`.

---

## Common mistakes

1. Checking depth after incrementing on `(` — drops nothing, or the wrong chars.
2. Building with `+=` on an immutable string in a loop (Java/Python) — O(n²).
3. Using a full stack of chars when an int suffices.

---

## Follow-ups

1. Input may be invalid — validate first.
2. Return the number of primitives.
3. Mixed brackets `()[]{}`.

<details><summary>Answer sketches</summary>

**#1:** Depth must never go negative and must end at 0.

**#2:** Count how many times depth returns to 0.

**#3:** Now you need a real stack to check matching types (LC 20).
</details>

---

## Flashcards

**When does one bracket type not need a stack?** #flashcard
Always — the stack's size (an int depth) carries all the information.

**Which chars does remove-outermost drop?** #flashcard
( seen at depth 0 and ) that brings depth back to 0.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String walkthroughs](../../coding/data-structures/03-string.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
