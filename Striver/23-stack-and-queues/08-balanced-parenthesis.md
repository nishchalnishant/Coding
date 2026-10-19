---
module: striver/23-stack-and-queues
lesson: 8
topic: Balanced Paranthesis
difficulty: Easy
source: https://takeuforward.org/learning/dsa/balanced-paranthesis?category=implementation&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, string, parentheses]
---
# 8. Balanced Paranthesis

← [Implement queue using Linkedlist](07-implement-queue-using-linkedlist.md) · [Part 23 index](README.md) · Next → [Infix to Postfix Conversion](09-infix-to-postfix-conversion.md)

> [!abstract] Problem at a glance
> **Task:** Is a string of `()[]{}` correctly opened, closed and nested?
> **Key insight:** The most recently opened bracket must close first, which is exactly LIFO. Push each opener. On a closer, the stack top must be its matching opener. At the end the stack must be empty.
> **Difficulty:** Easy · **Pattern:** Stack matching · **Also on:** [LC 20](https://leetcode.com/problems/valid-parentheses/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/balanced-paranthesis?category=implementation&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Repeatedly erase matched pairs](#3-repeatedly-erase-matched-pairs) · [4. Stack of openers](#4-stack-of-openers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `s` containing only `()[]{}`, return true if every bracket is closed by the same type, in the correct order, and every closer has a matching opener.

| Input | Output | Why |
|---|---|---|
| `s = "()[]{}"` | `true` |  |
| `s = "(]"` | `false` | type mismatch |
| `s = "([)]"` | `false` | wrong nesting order |
| `s = "{[]}"` | `true` |  |

**Constraints:** `1 ≤ s.length ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Repeatedly erase matched pairs | delete "()", "[]", "{}" until nothing changes | O(n²) | O(n) |
| Stack of openers | push openers; closer must match the top | O(n) | O(n) |

> [!tip] Interview angle
> Basic, but the three failure modes must all be handled: wrong type, a closer with an empty stack, and leftover openers. A quick early exit: odd length → false.

---

## 3. Repeatedly erase matched pairs

**Intuition.** Any valid string contains an adjacent matched pair. Erasing it leaves a valid string. Repeat until stable; the input is valid iff the result is empty.

```python
def is_valid_erase(s):
    prev = None
    while prev != s:
        prev = s
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Stack of openers

**Intuition.** Scan left to right. Push openers. For a closer, the stack must be non-empty and its top must be the matching opener; pop it. Valid iff the stack is empty at the end.

**Algorithm**

1. Map each closer to its opener.
2. For `c` in `s`: opener → push; closer → if stack empty or top ≠ match, return false; else pop.
3. Return `stack empty`.

**Dry run** — "{[]}": push {, push [, ] matches [ → pop, } matches { → pop, empty → true. "([)]": push (, push [, ) vs top [ → false.

**C++**
```cpp
bool isValid(string s) {
    vector<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') { st.push_back(c); continue; }
        char want = c == ')' ? '(' : c == ']' ? '[' : '{';
        if (st.empty() || st.back() != want) return false;
        st.pop_back();
    }
    return st.empty();
}
```

**Java**
```java
static boolean isValid(String s) {
    Deque<Character> st = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '[' || c == '{') { st.push(c); continue; }
        char want = c == ')' ? '(' : c == ']' ? '[' : '{';
        if (st.isEmpty() || st.peek() != want) return false;
        st.pop();
    }
    return st.isEmpty();
}
```

**Python**
```python
def is_valid(s):
    match = {')': '(', ']': '[', '}': '{'}
    st = []
    for c in s:
        if c in match:
            if not st or st[-1] != match[c]:
                return False
            st.pop()
        else:
            st.append(c)
    return not st
```

**Complexity:** time **O(n)**, space **O(n)** — one push/pop per character; worst case all openers.

---

## Edge cases

- Starts with a closer → false immediately.
- Only openers → false at the end.
- Odd length → false (shortcut).

---

## Common mistakes

1. Returning true without checking the stack is empty at the end.
2. Calling `top()` on an empty stack.
3. Counting each type separately: it accepts `([)]`.

---

## Follow-ups

1. Only one bracket type?
2. Minimum insertions/removals to make it valid?

<details><summary>Answer sketches</summary>

**#1:** A counter suffices: never negative, zero at the end. O(1) space.

**#2:** Track unmatched openers and unmatched closers (LC 921); or a stack of indices for removal (LC 1249).
</details>

---

## Flashcards

**Three ways a bracket string can be invalid?** #flashcard
Type mismatch, a closer with an empty stack, openers left over at the end.

**Why do separate counters per bracket type fail?** #flashcard
They ignore nesting order: `([)]` has balanced counts but is invalid.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
