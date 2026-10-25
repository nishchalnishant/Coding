---
module: striver-a2z/17-strings-basic-medium
lesson: 2
topic: Maximum Nesting Depth of the Parentheses
difficulty: Easy
source: https://takeuforward.org/learning/dsa/maximum-nesting-depth-of-the-parentheses?category=parentheses&source=strivers-a2z-dsa-sheet
tags: [striver, strings-basic-and-medium, string, stack]
---
# 2. Maximum Nesting Depth of the Parentheses

← [Remove Outermost Parentheses](01-remove-outermost-parentheses.md) · [Part 17 index](README.md) · Next → [Roman to Integer](03-roman-to-integer.md)

> [!abstract] Problem at a glance
> **Task:** Return the maximum nesting depth of parentheses in a valid expression containing digits, operators and parentheses.
> **Key insight:** Depth goes up on `(` and down on `)`; the answer is the highest value it reaches. Ignore every other character.
> **Difficulty:** Easy · **Pattern:** Depth counter · **Also on:** [LC 1614](https://leetcode.com/problems/maximum-nesting-depth-of-the-parentheses/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-nesting-depth-of-the-parentheses?category=parentheses&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Explicit stack](#3-explicit-stack) · [4. Running depth](#4-running-depth) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a valid parentheses string `s` (it may also contain digits and `+ - * /`), return its nesting depth: the maximum number of `(` that are open at the same time.

| Input | Output | Why |
|---|---|---|
| `s = "(1+(2*3)+((8)/4))+1"` | `3` | 8 sits inside three open parens |
| `s = "(1)+((2))+(((3)))"` | `3` |  |
| `s = "1+(2*3)/(2-1)"` | `1` |  |
| `s = "1"` | `0` | no parentheses |

**Constraints:** `1 ≤ |s| ≤ 100`, `s` is a valid parentheses string with digits and `+ - * / ( )`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Explicit stack | push on (, pop on ), answer = max stack size | O(n) | O(n) |
| Running depth | depth++ on ( and update max; depth-- on ) | O(n) | O(1) |

> [!tip] Interview angle
> Asked as a 5-minute opener. Do it in one pass, O(1) space, and update the max right after incrementing (the max happens on an opening paren).

---

## 3. Explicit stack

**Intuition.** Works and generalises to validation, but the stack holds only `(`, so its size is all you use.

```python
def max_depth_stack(s):
    st, best = [], 0
    for c in s:
        if c == '(':
            st.append(c)
            best = max(best, len(st))
        elif c == ')':
            st.pop()
    return best
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Running depth

**Intuition.** Replace the stack with its size. The maximum can only be reached right after a `(`, so update `best` there.

**Dry run** — `(1+(2*3)+((8)/4))`: depths 1, 2, 1, 2, 3, 2, 1, 0 → max 3.

**C++**
```cpp
int maxDepth(string s) {
    int depth = 0, best = 0;
    for (char c : s) {
        if (c == '(') best = max(best, ++depth);
        else if (c == ')') depth--;
    }
    return best;
}
```

**Java**
```java
static int maxDepth(String s) {
    int depth = 0, best = 0;
    for (char c : s.toCharArray()) {
        if (c == '(') best = Math.max(best, ++depth);
        else if (c == ')') depth--;
    }
    return best;
}
```

**Python**
```python
def max_depth(s):
    depth = best = 0
    for c in s:
        if c == '(':
            depth += 1
            best = max(best, depth)
        elif c == ')':
            depth -= 1
    return best
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, two integers.

---

## Edge cases

- No parentheses → 0.
- Depth reached early and never again.
- Non-paren characters between brackets.

---

## Common mistakes

1. Updating the max after `)` — you record a value one too low.
2. Treating digits as brackets (`else depth--`).

---

## Follow-ups

1. Split a VPS into two VPS minimising max depth (LC 1111).
2. String may be invalid — return −1.

<details><summary>Answer sketches</summary>

**#1:** Assign `(` at odd depth to A, even to B — alternate by depth parity.

**#2:** Return −1 if depth goes negative or ends non-zero.
</details>

---

## Flashcards

**Nesting depth in O(1) space?** #flashcard
Running counter: +1 on (, −1 on ), track max after each +1.

**Interview track →** [Strings deep-dive](../../01-data-structures/03-string.md) · [String walkthroughs](../../04-practice/data-structures/03-string.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
