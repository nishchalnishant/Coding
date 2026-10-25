---
module: striver-a2z/23-stack-and-queues
lesson: 9
topic: Infix to Postfix Conversion
difficulty: Medium
source: https://takeuforward.org/learning/dsa/infix-to-postfix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, expression, shunting-yard]
---
# 9. Infix to Postfix Conversion

← [Balanced Paranthesis](08-balanced-parenthesis.md) · [Part 23 index](README.md) · Next → [Infix to Prefix Conversion](10-infix-to-prefix-conversion.md)

> [!abstract] Problem at a glance
> **Task:** Convert an infix expression (single-character operands, `+ − * / ^`, parentheses) to postfix (Reverse Polish).
> **Key insight:** This is **shunting-yard**. Operands go straight to the output. An operator first pops every stacked operator that binds at least as tightly, then pushes itself. `^` is right-associative, so on equal precedence it does **not** pop. A `)` pops back to the matching `(`.
> **Difficulty:** Medium · **Pattern:** Operator stack with precedence · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/infix-to-postfix-1587115620/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/infix-to-postfix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive descent (precedence climbing)](#3-recursive-descent-precedence-climbing) · [4. Shunting-yard (operator stack)](#4-shunting-yard-operator-stack) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an infix expression of single-letter/digit operands, the operators `+ - * / ^` and parentheses, return its postfix form. Precedence: `^` > `* /` > `+ -`. `^` associates right-to-left; the others left-to-right.

| Input | Output | Why |
|---|---|---|
| `a+b*(c^d-e)^(f+g*h)-i` | `abcd^e-fgh*+^*+i-` |  |
| `(a+b)*c` | `ab+c*` | parentheses override precedence |
| `a^b^c` | `abc^^` | right-associative: a^(b^c) |

**Constraints:** `1 ≤ |s| ≤ 10⁵`; the expression is valid.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive descent (precedence climbing) | parse expr(minPrec); emit left + right + op | O(n) | O(n) recursion |
| Shunting-yard (operator stack) | pop while top binds tighter, then push | O(n) | O(n) |

> [!tip] Interview angle
> The interviewer checks precedence and associativity. Write out the pop condition: `prec(top) > prec(c)`, or equal precedence and `c` is left-associative. Getting `a^b^c` right is the tell.

---

## 3. Recursive descent (precedence climbing)

**Intuition.** `expr(p)` parses an operand, then repeatedly consumes an operator with precedence ≥ `p`. It parses its right operand with `prec+1` for left-associative ops, or `prec` for `^`, and emits `left + right + op`. The grammar does the work, which makes this the natural way to build an expression tree.

```python
def infix_to_postfix_rd(s):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    i = 0
    def atom():
        nonlocal i
        if s[i] == '(':
            i += 1
            r = expr(1)
            i += 1                    # skip ')'
            return r
        i += 1
        return s[i - 1]
    def expr(min_p):
        nonlocal i
        left = atom()
        while i < len(s) and s[i] in prec and prec[s[i]] >= min_p:
            op = s[i]; i += 1
            right = expr(prec[op] if op == '^' else prec[op] + 1)
            left = left + right + op
        return left
    return expr(1)
```

**Complexity:** time **O(n)**, space **O(n) recursion**.

---

## 4. Shunting-yard (operator stack)

**Intuition.** The stack holds operators still waiting for their right operand, in increasing binding strength (`(` acts as a floor). When a new operator arrives, anything on the stack that binds at least as tightly has its right operand complete, so it goes to the output.

**Algorithm**

1. Operand → output.
2. `(` → push. `)` → pop to output until `(`, discard `(`.
3. Operator `c`: while top is an operator and (`prec(top) > prec(c)` or (`prec(top) == prec(c)` and `c ≠ '^'`)): pop to output. Push `c`.
4. At the end, pop everything to output.

**Dry run** — a+b*c-d: a → +push → b → * (prec 2 > 1, push) → c → − pops * then + (equal, left-assoc) → push − → d → pop −. Output abc*+d−.

**C++**
```cpp
int prec(char c) { return c == '^' ? 3 : (c == '*' || c == '/') ? 2 : (c == '+' || c == '-') ? 1 : 0; }
string infixToPostfix(string s) {
    string out; vector<char> st;
    for (char c : s) {
        if (isalnum((unsigned char)c)) out += c;
        else if (c == '(') st.push_back(c);
        else if (c == ')') {
            while (st.back() != '(') { out += st.back(); st.pop_back(); }
            st.pop_back();
        } else {
            while (!st.empty() && st.back() != '(' &&
                   (prec(st.back()) > prec(c) || (prec(st.back()) == prec(c) && c != '^'))) {
                out += st.back(); st.pop_back();
            }
            st.push_back(c);
        }
    }
    while (!st.empty()) { out += st.back(); st.pop_back(); }
    return out;
}
```

**Java**
```java
static int prec(char c) { return c == '^' ? 3 : (c == '*' || c == '/') ? 2 : (c == '+' || c == '-') ? 1 : 0; }
static String infixToPostfix(String s) {
    StringBuilder out = new StringBuilder();
    Deque<Character> st = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (Character.isLetterOrDigit(c)) out.append(c);
        else if (c == '(') st.push(c);
        else if (c == ')') {
            while (st.peek() != '(') out.append(st.pop());
            st.pop();
        } else {
            while (!st.isEmpty() && st.peek() != '(' &&
                   (prec(st.peek()) > prec(c) || (prec(st.peek()) == prec(c) && c != '^')))
                out.append(st.pop());
            st.push(c);
        }
    }
    while (!st.isEmpty()) out.append(st.pop());
    return out.toString();
}
```

**Python**
```python
def infix_to_postfix(s):
    prec = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
    out, st = [], []
    for c in s:
        if c.isalnum():
            out.append(c)
        elif c == '(':
            st.append(c)
        elif c == ')':
            while st[-1] != '(':
                out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != '(' and (prec[st[-1]] > prec[c] or (prec[st[-1]] == prec[c] and c != '^')):
                out.append(st.pop())
            st.append(c)
    while st:
        out.append(st.pop())
    return ''.join(out)
```

**Complexity:** time **O(n)**, space **O(n)** — each character is pushed and popped at most once.

---

## Edge cases

- Single operand.
- Redundant parentheses `((a))`.
- Chains of equal precedence: left vs right associativity.

---

## Common mistakes

1. Popping on equal precedence for `^`, which gives `ab^c^` for `a^b^c`.
2. Not stopping at `(` while popping for an operator.
3. Forgetting to flush the stack at the end.

---

## Follow-ups

1. Evaluate the expression instead?
2. Unary minus?

<details><summary>Answer sketches</summary>

**#1:** Two stacks (values + operators) with the same pop rule, or convert to postfix and evaluate with one value stack (LC 224/227).

**#2:** Detect `-` at the start or after `(`/an operator; push a distinct unary operator with the highest precedence (right-assoc).
</details>

---

## Flashcards

**Shunting-yard pop condition for an incoming operator c?** #flashcard
Top isn't `(` and (prec(top) > prec(c), or equal and c is left-associative).

**Postfix of a^b^c?** #flashcard
abc^^, because ^ is right-associative.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
