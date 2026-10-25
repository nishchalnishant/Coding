---
module: striver-a2z/23-stack-and-queues
lesson: 14
topic: Postfix to Prefix Conversion
difficulty: Medium
source: https://takeuforward.org/learning/dsa/postfix-to-prefix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, expression]
---
# 14. Postfix to Prefix Conversion

← [Postfix to Infix Conversion](13-postfix-to-infix-conversion.md) · [Part 23 index](README.md) · Next → [Next Greater Element](15-next-greater-element.md)

> [!abstract] Problem at a glance
> **Task:** Convert a postfix expression to prefix.
> **Key insight:** Scan **left to right**. An operator pops `b` (right) then `a` (left) and pushes `op + a + b`. This is the mirror of prefix → postfix.
> **Difficulty:** Medium · **Pattern:** Operand stack, scan left to right
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/postfix-to-prefix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursion (parse the tree directly)](#3-recursion-parse-the-tree-directly) · [4. Operand stack](#4-operand-stack) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a valid postfix expression with single-character operands and binary operators `+ - * / ^`, convert it to prefix.

| Input | Output | Why |
|---|---|---|
| `AB-DE+F*/` | `/-AB*+DEF` |  |
| `ab+` | `+ab` |  |

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
def postfix_to_prefix_rec(s):
    i = len(s) - 1
    def go():
        nonlocal i
        c = s[i]; i -= 1
        if c.isalnum():
            return c
        b = go(); a = go()
        return c + a + b
    return go()
```

**Complexity:** time **O(n²) with string concat**, space **O(n)**.

---

## 4. Operand stack

**Intuition.** Scan left to right. An operand is a complete sub-expression, so push it. An operator pops two finished sub-expressions, combines them, and pushes the result. At the end exactly one string remains.

**Algorithm**

1. Scan left to right.
2. Operand → push.
3. Operator → `b = pop()`, `a = pop()`, push `op + a + b`.
4. Return the top.

**Dry run** — AB-DE+F*/: A,B → −: -AB → D,E → +: +DE → F → *: *+DEF → /: /-AB*+DEF.

**C++**
```cpp
string postfixToPrefix(string s) {
    vector<string> st;
    for (char c : s) {
        if (isalnum((unsigned char)c)) { st.push_back(string(1, c)); continue; }
        string b = st.back(); st.pop_back();
        string a = st.back(); st.pop_back();
        st.push_back(string(1, c) + a + b);
    }
    return st.back();
}
```

**Java**
```java
static String postfixToPrefix(String s) {
    Deque<String> st = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (Character.isLetterOrDigit(c)) { st.push(String.valueOf(c)); continue; }
        String b = st.pop(), a = st.pop();
        st.push(c + a + b);
    }
    return st.peek();
}
```

**Python**
```python
def postfix_to_prefix(s):
    st = []
    for c in s:
        if c.isalnum():
            st.append(c)
        else:
            b = st.pop(); a = st.pop()
            st.append(c + a + b)
    return st[-1]
```

**Complexity:** time **O(n²) strings · O(n) with a tree**, space **O(n)** — n pushes/pops; string concatenation can copy O(n) per step, giving O(n²) in the worst case. Building tree nodes instead and printing once makes it O(n).

---

## Edge cases

- Single operand.
- Long left-nested chains.

---

## Common mistakes

1. Wrong pop order.
2. In Java, `c + a + b` with a `char c` first: fine here because `a` is a String, but `c + d + a` with two chars adds their codes.

---

## Follow-ups

1. Do it without building strings?
2. Which conversions are 'free' (no precedence)?

<details><summary>Answer sketches</summary>

**#1:** Build the expression tree once (O(n)) and print it pre-order.

**#2:** All four between prefix and postfix and to infix; only infix → X needs precedence and associativity.
</details>

---

## Flashcards

**Postfix → prefix combine rule?** #flashcard
Left-to-right; b = pop, a = pop, push op + a + b.

**Which conversions need precedence rules?** #flashcard
Only those starting from infix.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
