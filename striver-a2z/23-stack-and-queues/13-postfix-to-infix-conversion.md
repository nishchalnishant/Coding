---
module: striver-a2z/23-stack-and-queues
lesson: 13
topic: Postfix to Infix Conversion
difficulty: Medium
source: https://takeuforward.org/learning/dsa/postfix-to-infix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, expression]
---
# 13. Postfix to Infix Conversion

← [Prefix to Postfix Conversion](12-prefix-to-postfix-conversion.md) · [Part 23 index](README.md) · Next → [Postfix to Prefix Conversion](14-postfix-to-prefix-conversion.md)

> [!abstract] Problem at a glance
> **Task:** Convert a postfix expression to fully parenthesised infix.
> **Key insight:** Scan **left to right**. An operator pops `b` first (the **right** operand, pushed last), then `a`, and pushes `(a op b)`.
> **Difficulty:** Medium · **Pattern:** Operand stack, scan left to right
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/postfix-to-infix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursion (parse the tree directly)](#3-recursion-parse-the-tree-directly) · [4. Operand stack](#4-operand-stack) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a valid postfix expression with single-character operands and binary operators `+ - * / ^`, convert it to infix. Wrap every binary sub-expression in parentheses.

| Input | Output | Why |
|---|---|---|
| `ab*c+` | `((a*b)+c)` |  |
| `abc/-ak/l-*` | `((a-(b/c))*((a/k)-l))` |  |

**Constraints:** `1 ≤ |s| ≤ 10⁴`; valid input.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursion (parse the tree directly) | each operator consumes two sub-expressions | O(n²) with string concat | O(n) |
| Operand stack | scan left to right; operator combines the top two | O(n²) strings · O(n) with a tree | O(n) |

> [!tip] Interview angle
> These conversions all use one idea: an **operand stack** of finished sub-expressions. Know the scan direction (prefix → right-to-left, postfix → left-to-right) and which pop is the left operand.

---

## 3. Recursion (parse the tree directly)

**Intuition.** The expression is a tree written in pre-/post-order. A recursive reader consumes one operator, then its two operands, and builds the output. Concatenation copies strings, so this is O(n²) worst case, same as the stack version without builders.

```python
def postfix_to_infix_rec(s):
    i = len(s) - 1
    def go():
        nonlocal i
        c = s[i]; i -= 1
        if c.isalnum():
            return c
        b = go(); a = go()          # right operand is read first from the end
        return '(' + a + c + b + ')'
    return go()
```

**Complexity:** time **O(n²) with string concat**, space **O(n)**.

---

## 4. Operand stack

**Intuition.** Scan left to right. An operand is a complete sub-expression, so push it. An operator pops two finished sub-expressions, combines them, and pushes the result. At the end exactly one string remains.

**Algorithm**

1. Scan left to right.
2. Operand → push.
3. Operator → `b = pop()` (right), `a = pop()` (left); push `(a op b)`.
4. Return the top.

**Dry run** — ab+cd-*: a, b → +: (a+b) → c, d → −: (c-d) → *: b=(c-d), a=(a+b) → ((a+b)*(c-d)).

**C++**
```cpp
string postfixToInfix(string s) {
    vector<string> st;
    for (char c : s) {
        if (isalnum((unsigned char)c)) { st.push_back(string(1, c)); continue; }
        string b = st.back(); st.pop_back();
        string a = st.back(); st.pop_back();
        st.push_back("(" + a + c + b + ")");
    }
    return st.back();
}
```

**Java**
```java
static String postfixToInfix(String s) {
    Deque<String> st = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (Character.isLetterOrDigit(c)) { st.push(String.valueOf(c)); continue; }
        String b = st.pop(), a = st.pop();
        st.push("(" + a + c + b + ")");
    }
    return st.peek();
}
```

**Python**
```python
def postfix_to_infix(s):
    st = []
    for c in s:
        if c.isalnum():
            st.append(c)
        else:
            b = st.pop(); a = st.pop()
            st.append('(' + a + c + b + ')')
    return st[-1]
```

**Complexity:** time **O(n²) strings · O(n) with a tree**, space **O(n)** — n pushes/pops; string concatenation can copy O(n) per step, giving O(n²) in the worst case. Building tree nodes instead and printing once makes it O(n).

---

## Edge cases

- Single operand.
- Non-commutative operators reveal pop-order bugs.

---

## Common mistakes

1. `a = pop()` first: `ab-` becomes `(b-a)`.
2. Leaving more than one item on the stack, which means the input was invalid.

---

## Follow-ups

1. Evaluate postfix (LC 150)?
2. Build an expression tree?

<details><summary>Answer sketches</summary>

**#1:** Same scan with integers; note truncation toward zero for division.

**#2:** Push leaf nodes; an operator node takes right = pop, left = pop.
</details>

---

## Flashcards

**Postfix → infix: which pop is the right operand?** #flashcard
The first pop.

**Postfix scan direction?** #flashcard
Left to right: operands come before their operator.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
