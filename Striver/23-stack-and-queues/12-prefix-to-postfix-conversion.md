---
module: striver/23-stack-and-queues
lesson: 12
topic: Prefix to Postfix Conversion
difficulty: Medium
source: https://takeuforward.org/learning/dsa/prefix-to-postfix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, expression]
---
# 12. Prefix to Postfix Conversion

← [Prefix to Infix Conversion](11-prefix-to-infix-conversion.md) · [Part 23 index](README.md) · Next → [Postfix to Infix Conversion](13-postfix-to-infix-conversion.md)

> [!abstract] Problem at a glance
> **Task:** Convert a prefix expression to postfix.
> **Key insight:** Scan **right to left** with a stack of finished sub-expressions. An operator pops `a` (left) and `b` (right) and pushes `a + b + op`. Both notations are parenthesis-free, so no precedence is involved.
> **Difficulty:** Medium · **Pattern:** Operand stack, scan right to left
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/prefix-to-postfix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursion (parse the tree directly)](#3-recursion-parse-the-tree-directly) · [4. Operand stack](#4-operand-stack) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a valid prefix expression with single-character operands and binary operators `+ - * / ^`, convert it to postfix.

| Input | Output | Why |
|---|---|---|
| `*-A/BC-/AKL` | `ABC/-AK/L-*` |  |
| `*+AB-CD` | `AB+CD-*` |  |

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
def prefix_to_postfix_rec(s):
    i = 0
    def go():
        nonlocal i
        c = s[i]; i += 1
        if c.isalnum():
            return c
        a = go(); b = go()
        return a + b + c
    return go()
```

**Complexity:** time **O(n²) with string concat**, space **O(n)**.

---

## 4. Operand stack

**Intuition.** Scan right to left. An operand is a complete sub-expression, so push it. An operator pops two finished sub-expressions, combines them, and pushes the result. At the end exactly one string remains.

**Algorithm**

1. Scan right to left.
2. Operand → push.
3. Operator → `a = pop()`, `b = pop()`, push `a + b + op`.
4. Return the top.

**Dry run** — *+AB-CD: D, C → −: CD- → B, A → +: AB+ → *: AB+ CD- * → AB+CD-*.

**C++**
```cpp
string prefixToPostfix(string s) {
    vector<string> st;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        char c = s[i];
        if (isalnum((unsigned char)c)) { st.push_back(string(1, c)); continue; }
        string a = st.back(); st.pop_back();
        string b = st.back(); st.pop_back();
        st.push_back(a + b + c);
    }
    return st.back();
}
```

**Java**
```java
static String prefixToPostfix(String s) {
    Deque<String> st = new ArrayDeque<>();
    for (int i = s.length() - 1; i >= 0; i--) {
        char c = s.charAt(i);
        if (Character.isLetterOrDigit(c)) { st.push(String.valueOf(c)); continue; }
        String a = st.pop(), b = st.pop();
        st.push(a + b + c);
    }
    return st.peek();
}
```

**Python**
```python
def prefix_to_postfix(s):
    st = []
    for c in reversed(s):
        if c.isalnum():
            st.append(c)
        else:
            a = st.pop(); b = st.pop()
            st.append(a + b + c)
    return st[-1]
```

**Complexity:** time **O(n²) strings · O(n) with a tree**, space **O(n)** — n pushes/pops; string concatenation can copy O(n) per step, giving O(n²) in the worst case. Building tree nodes instead and printing once makes it O(n).

---

## Edge cases

- Single operand.
- Operator chains like `^a^bc`.

---

## Common mistakes

1. Reversing the operand order.
2. Reversing the whole string as a 'shortcut': the prefix reversed is not the postfix (operand order flips).

---

## Follow-ups

1. Postfix → prefix?
2. Validate a prefix string?

<details><summary>Answer sketches</summary>

**#1:** Mirror: scan left to right, `b = pop()`, `a = pop()`, push `op + a + b`.

**#2:** Scan right to left counting: operand +1, operator needs ≥ 2 then −1; valid iff the final count is 1.
</details>

---

## Flashcards

**Prefix → postfix combine rule?** #flashcard
Right-to-left scan; operator: a = pop, b = pop, push a + b + op.

**Is reversed prefix equal to postfix?** #flashcard
No; reversal also reverses operand order (+ab → ba+).

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
