---
module: striver-a2z/23-stack-and-queues
lesson: 11
topic: Prefix to Infix Conversion
difficulty: Medium
source: https://takeuforward.org/learning/dsa/prefix-to-infix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, expression]
---
# 11. Prefix to Infix Conversion

← [Infix to Prefix Conversion](10-infix-to-prefix-conversion.md) · [Part 23 index](README.md) · Next → [Prefix to Postfix Conversion](12-prefix-to-postfix-conversion.md)

> [!abstract] Problem at a glance
> **Task:** Convert a prefix expression to a fully parenthesised infix expression.
> **Key insight:** Scan **right to left**. Operands are pushed. An operator pops `a` (top = left operand) then `b`, and pushes `(a op b)`. Right-to-left order means the left operand is the one pushed last.
> **Difficulty:** Medium · **Pattern:** Operand stack, scan right to left
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/prefix-to-infix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursion (parse the tree directly)](#3-recursion-parse-the-tree-directly) · [4. Operand stack](#4-operand-stack) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a valid prefix expression with single-character operands and binary operators `+ - * / ^`, convert it to infix. Wrap every binary sub-expression in parentheses.

| Input | Output | Why |
|---|---|---|
| `*-A/BC-/AKL` | `((A-(B/C))*((A/K)-L))` |  |
| `+ab` | `(a+b)` |  |

**Constraints:** `1 ≤ |s| ≤ 10⁴`; valid input.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursion (parse the tree directly) | each operator consumes two sub-expressions | O(n²) with string concat | O(n) |
| Operand stack | scan right to left; operator combines the top two | O(n²) strings · O(n) with a tree | O(n) |

> [!tip] Interview angle
> These conversions all use one idea: an **operand stack** of finished sub-expressions. Know the scan direction (prefix → right-to-left, postfix → left-to-right) and which pop is the left operand.

---

## 3. Recursion (parse the tree directly)

**Intuition.** The expression is a tree written in pre-/post-order. A recursive reader consumes one operator, then its two operands, and builds the output. Concatenation copies strings, so this is O(n²) worst case, same as the stack version without builders.

```python
def prefix_to_infix_rec(s):
    i = 0
    def go():
        nonlocal i
        c = s[i]; i += 1
        if c.isalnum():
            return c
        a = go(); b = go()
        return '(' + a + c + b + ')'
    return go()
```

**Complexity:** time **O(n²) with string concat**, space **O(n)**.

---

## 4. Operand stack

**Intuition.** Scan right to left. An operand is a complete sub-expression, so push it. An operator pops two finished sub-expressions, combines them, and pushes the result. At the end exactly one string remains.

**Algorithm**

1. For `i` from `n−1` down to 0:
2. Operand → push `s[i]`.
3. Operator → `a = pop()` (left), `b = pop()` (right); push `(a s[i] b)`.
4. Return the single remaining string.

**Dry run** — *+ab-cd from the right: d, c → − : (c-d) → b, a → + : (a+b) → * : a=(a+b), b=(c-d) → ((a+b)*(c-d)).

**C++**
```cpp
string prefixToInfix(string s) {
    vector<string> st;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        char c = s[i];
        if (isalnum((unsigned char)c)) { st.push_back(string(1, c)); continue; }
        string a = st.back(); st.pop_back();
        string b = st.back(); st.pop_back();
        st.push_back("(" + a + c + b + ")");
    }
    return st.back();
}
```

**Java**
```java
static String prefixToInfix(String s) {
    Deque<String> st = new ArrayDeque<>();
    for (int i = s.length() - 1; i >= 0; i--) {
        char c = s.charAt(i);
        if (Character.isLetterOrDigit(c)) { st.push(String.valueOf(c)); continue; }
        String a = st.pop(), b = st.pop();
        st.push("(" + a + c + b + ")");
    }
    return st.peek();
}
```

**Python**
```python
def prefix_to_infix(s):
    st = []
    for c in reversed(s):
        if c.isalnum():
            st.append(c)
        else:
            a = st.pop(); b = st.pop()
            st.append('(' + a + c + b + ')')
    return st[-1]
```

**Complexity:** time **O(n²) strings · O(n) with a tree**, space **O(n)** — n pushes/pops; string concatenation can copy O(n) per step, giving O(n²) in the worst case. Building tree nodes instead and printing once makes it O(n).

---

## Edge cases

- A single operand: return it unchanged.
- Deep right-nesting like `^a^bc`.

---

## Common mistakes

1. Popping in the wrong order (`b` first), which mirrors non-commutative operators like − and /.
2. Scanning left to right: a prefix operator's operands aren't built yet.

---

## Follow-ups

1. Minimal parentheses?
2. Evaluate prefix directly?

<details><summary>Answer sketches</summary>

**#1:** Build a tree, then print a child in parentheses only if its precedence is lower than the parent's (or equal on the non-associative side).

**#2:** Same right-to-left stack with numbers.
</details>

---

## Flashcards

**Prefix → infix: scan direction and pop order?** #flashcard
Right to left; first pop is the LEFT operand.

**Why is right-to-left right for prefix?** #flashcard
An operator's operands appear after it, so they're already on the stack when scanning backwards.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
