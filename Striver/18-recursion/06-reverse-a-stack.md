---
module: striver/18-recursion
lesson: 6
topic: Reverse a Stack
difficulty: Medium
source: https://takeuforward.org/learning/dsa/reverse-a-stack?category=implementation-problems&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, stack]
---
# 6. Reverse a Stack

← [Count Good Numbers](05-count-good-numbers.md) · [Part 18 index](README.md) · Next → [Check if There Exists a Subsequence with Sum K](07-subsequence-sum-k-exists.md)

> [!abstract] Problem at a glance
> **Task:** Reverse a stack in place using only recursion and stack operations (no extra container).
> **Key insight:** Two recursions: `reverse` pops the top, reverses the rest, then pushes the saved element to the *bottom*. `insertAtBottom` pops everything, pushes the element, and restores. The call stack is the auxiliary storage.
> **Difficulty:** Medium · **Pattern:** Recursion with the call stack as storage · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/reverse-a-stack/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-a-stack?category=implementation-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Pop into a list, push back](#3-pop-into-a-list-push-back) · [4. Recursion with insert-at-bottom](#4-recursion-with-insert-at-bottom) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a stack `st`, reverse it so the bottom element becomes the top. You may only use `push`, `pop`, `top`/`peek` and `empty` on the stack, plus recursion — no arrays or second stack.

| Input | Output | Why |
|---|---|---|
| `st (bottom → top) = [1, 2, 3, 4]` | `[4, 3, 2, 1]` | old bottom 1 is now on top |
| `st = [3, 2, 1, 7, 6]` | `[6, 7, 1, 2, 3]` |  |

**Constraints:** `1 ≤ |st| ≤ 10⁴` (recursion depth n — fine in C++/Java with default stacks at this size).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Pop into a list, push back | drain into an array, push in the same order | O(n) | O(n) extra |
| Recursion with insert-at-bottom | pop top, reverse rest, insert top at bottom | O(n²) | O(n) call stack |

> [!tip] Interview angle
> Tests whether you can design two mutually-layered recursions with clean contracts: `insertAtBottom(st, x)` places x under everything, and `reverse(st)` assumes it works on the smaller stack. Expect the follow-up "sort a stack using recursion" — same shape with `sortedInsert`.

---

## 3. Pop into a list, push back

**Intuition.** Popping yields top-first; pushing those values back in that order puts the old top at the bottom. Violates the "no extra container" rule — the baseline the interviewer asks you to improve.

```python
def reverse_aux(st):
    buf = []
    while st:
        buf.append(st.pop())
    for x in buf:
        st.append(x)
```

**Complexity:** time **O(n)**, space **O(n) extra**.

---

## 4. Recursion with insert-at-bottom

**Intuition.** `insertAtBottom(x)`: if empty, push x; else pop `t`, recurse, push `t` back — O(size). `reverse()`: if empty, return; pop `t`, `reverse()`, `insertAtBottom(t)`. Each of n insertions costs O(n) → O(n²).

**Algorithm**

1. `reverse(st)`: if empty return; `t = pop`; `reverse(st)`; `insertAtBottom(st, t)`.
2. `insertAtBottom(st, x)`: if empty → push x; else `t = pop`; `insertAtBottom(st, x)`; push t.

**Dry run** — [1, 2, 3] (top 3): pop 3 → reverse [1, 2] → pop 2 → reverse [1] → pop 1 → reverse [] → insertBottom 1 → [1] → insertBottom 2 → [2, 1] → insertBottom 3 → [3, 2, 1].

**C++**
```cpp
void insertAtBottom(stack<int>& st, int x) {
    if (st.empty()) { st.push(x); return; }
    int t = st.top(); st.pop();
    insertAtBottom(st, x);
    st.push(t);
}
void reverseStack(stack<int>& st) {
    if (st.empty()) return;
    int t = st.top(); st.pop();
    reverseStack(st);
    insertAtBottom(st, t);
}
```

**Java**
```java
static void insertAtBottom(Stack<Integer> st, int x) {
    if (st.isEmpty()) { st.push(x); return; }
    int t = st.pop();
    insertAtBottom(st, x);
    st.push(t);
}
static void reverseStack(Stack<Integer> st) {
    if (st.isEmpty()) return;
    int t = st.pop();
    reverseStack(st);
    insertAtBottom(st, t);
}
```

**Python**
```python
def reverse_stack(st):
    def insert_at_bottom(x):
        if not st:
            st.append(x)
            return
        t = st.pop()
        insert_at_bottom(x)
        st.append(t)
    if not st:
        return
    t = st.pop()
    reverse_stack(st)
    insert_at_bottom(t)
```

**Complexity:** time **O(n²)**, space **O(n) call stack** — n insertions, each walking the current stack; recursion depth ≤ n.

---

## Edge cases

- Single element / empty stack.
- Deep stacks — recursion depth n (raise the stack limit for 10⁵+).

---

## Common mistakes

1. Pushing the popped top back on top instead of at the bottom.
2. Using a vector/second stack — breaks the constraint.
3. Forgetting to restore `t` in insertAtBottom.

---

## Follow-ups

1. Sort a stack with recursion.
2. Reverse a queue with recursion.

<details><summary>Answer sketches</summary>

**#1:** `sort`: pop t, sort rest, `sortedInsert(t)` — pop while top > t, push t, restore. O(n²).

**#2:** Dequeue x, reverse the rest, enqueue x — O(n), no helper needed.
</details>

---

## Flashcards

**Reverse a stack recursively — two functions?** #flashcard
reverse: pop, reverse rest, insertAtBottom(top). insertAtBottom: pop all, push x, restore.

**Complexity of recursive stack reversal?** #flashcard
O(n²) time, O(n) call stack.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
