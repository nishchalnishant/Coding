---
module: striver-a2z/23-stack-and-queues
lesson: 10
topic: Infix to Prefix Conversion
difficulty: Medium
source: https://takeuforward.org/learning/dsa/infix-to-prefix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, expression]
---
# 10. Infix to Prefix Conversion

← [Infix to Postfix Conversion](09-infix-to-postfix-conversion.md) · [Part 23 index](README.md) · Next → [Prefix to Infix Conversion](11-prefix-to-infix-conversion.md)

> [!abstract] Problem at a glance
> **Task:** Convert an infix expression to prefix (Polish) notation.
> **Key insight:** Reverse the string and swap `(` with `)`. Run shunting-yard with **flipped associativity**: pop on equal precedence only for `^`. Then reverse the output. Reversal turns left-associative chains into right-associative ones, which is why the tie rule flips.
> **Difficulty:** Medium · **Pattern:** Reverse + shunting-yard + reverse · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/infix-to-prefix-notation/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/infix-to-prefix-conversion?category=expression-conversions&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive descent (precedence climbing)](#3-recursive-descent-precedence-climbing) · [4. Reverse, convert, reverse](#4-reverse-convert-reverse) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a valid infix expression with single-character operands, `+ - * / ^` and parentheses, return its prefix form. Same precedence and associativity rules as infix-to-postfix.

| Input | Output | Why |
|---|---|---|
| `(a-b/c)*(a/k-l)` | `*-a/bc-/akl` |  |
| `a-b-c` | `--abc` | (a−b)−c |
| `a^b^c` | `^a^bc` | a^(b^c) |

**Constraints:** `1 ≤ |s| ≤ 10⁵`; valid input.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive descent (precedence climbing) | same parser as postfix, emit op + left + right | O(n) | O(n) |
| Reverse, convert, reverse | mirror the string, postfix with flipped ties, mirror back | O(n) | O(n) |

> [!tip] Interview angle
> Most candidates remember the reverse trick but get the tie-break wrong, so test `a-b-c` out loud. The recursive-descent version avoids the trick entirely and is easier to defend.

---

## 3. Recursive descent (precedence climbing)

**Intuition.** Parse exactly as for postfix, but build `op + left + right`. Associativity comes from the grammar: the right operand of a left-associative op is parsed at `prec+1`.

```python
def infix_to_prefix_rd(s):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    i = 0
    def atom():
        nonlocal i
        if s[i] == '(':
            i += 1
            r = expr(1)
            i += 1
            return r
        i += 1
        return s[i - 1]
    def expr(min_p):
        nonlocal i
        left = atom()
        while i < len(s) and s[i] in prec and prec[s[i]] >= min_p:
            op = s[i]; i += 1
            right = expr(prec[op] if op == '^' else prec[op] + 1)
            left = op + left + right
        return left
    return expr(1)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Reverse, convert, reverse

**Intuition.** Prefix of E is the reverse of the postfix of the mirrored E. Mirroring flips associativity. Left-assoc operators now need **no** pop on ties (they become right-assoc), and `^` now needs to pop on ties.

**Algorithm**

1. Reverse `s`, swapping `(` ↔ `)`.
2. Shunting-yard, but pop while `prec(top) > prec(c)` or (`prec(top) == prec(c)` and `c == '^'`).
3. Reverse the result.

**Dry run** — a-b-c → c-b-a → c, push −, b, − (equal, no pop) push, a → flush: cba−− → reverse: −−abc.

**C++**
```cpp
int prec(char c) { return c == '^' ? 3 : (c == '*' || c == '/') ? 2 : (c == '+' || c == '-') ? 1 : 0; }
string infixToPrefix(string s) {
    reverse(s.begin(), s.end());
    for (char& c : s) c = c == '(' ? ')' : c == ')' ? '(' : c;
    string out; vector<char> st;
    for (char c : s) {
        if (isalnum((unsigned char)c)) out += c;
        else if (c == '(') st.push_back(c);
        else if (c == ')') {
            while (st.back() != '(') { out += st.back(); st.pop_back(); }
            st.pop_back();
        } else {
            while (!st.empty() && st.back() != '(' &&
                   (prec(st.back()) > prec(c) || (prec(st.back()) == prec(c) && c == '^'))) {
                out += st.back(); st.pop_back();
            }
            st.push_back(c);
        }
    }
    while (!st.empty()) { out += st.back(); st.pop_back(); }
    reverse(out.begin(), out.end());
    return out;
}
```

**Java**
```java
static int prec(char c) { return c == '^' ? 3 : (c == '*' || c == '/') ? 2 : (c == '+' || c == '-') ? 1 : 0; }
static String infixToPrefix(String s) {
    StringBuilder out = new StringBuilder();
    Deque<Character> st = new ArrayDeque<>();
    for (int i = s.length() - 1; i >= 0; i--) {
        char c = s.charAt(i);
        if (c == '(') c = ')'; else if (c == ')') c = '(';
        if (Character.isLetterOrDigit(c)) out.append(c);
        else if (c == '(') st.push(c);
        else if (c == ')') {
            while (st.peek() != '(') out.append(st.pop());
            st.pop();
        } else {
            while (!st.isEmpty() && st.peek() != '(' &&
                   (prec(st.peek()) > prec(c) || (prec(st.peek()) == prec(c) && c == '^')))
                out.append(st.pop());
            st.push(c);
        }
    }
    while (!st.isEmpty()) out.append(st.pop());
    return out.reverse().toString();
}
```

**Python**
```python
def infix_to_prefix(s):
    prec = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
    flip = {'(': ')', ')': '('}
    out, st = [], []
    for c in reversed(s):
        c = flip.get(c, c)
        if c.isalnum():
            out.append(c)
        elif c == '(':
            st.append(c)
        elif c == ')':
            while st[-1] != '(':
                out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != '(' and (prec[st[-1]] > prec[c] or (prec[st[-1]] == prec[c] and c == '^')):
                out.append(st.pop())
            st.append(c)
    while st:
        out.append(st.pop())
    return ''.join(reversed(out))
```

**Complexity:** time **O(n)**, space **O(n)** — two reversals plus one shunting-yard pass.

---

## Edge cases

- Left-associative chains (`a-b-c`).
- Right-associative chains (`a^b^c`).
- Fully parenthesised input.

---

## Common mistakes

1. Keeping the postfix tie rule after reversing, which turns `a-b-c` into `-a-bc` (that's a−(b−c)).
2. Forgetting to swap parentheses after reversing.
3. Reversing only the operands.

---

## Follow-ups

1. Prefix → value?
2. Why is prefix/postfix parenthesis-free?

<details><summary>Answer sketches</summary>

**#1:** Scan right to left with a value stack: operand push; operator pops a (first) and b, pushes a op b.

**#2:** Operator position fixes the arity grouping, so the parse is unique without precedence rules.
</details>

---

## Flashcards

**Infix → prefix trick?** #flashcard
Reverse and swap parens, shunting-yard with flipped tie rule (pop on equal only for ^), reverse.

**Prefix of a−b−c?** #flashcard
−−abc.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
