---
module: striver/23-stack-and-queues
lesson: 22
topic: Implement Min Stack
difficulty: Medium
source: https://takeuforward.org/learning/dsa/implement-min-stack?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, design]
---
# 22. Implement Min Stack

← [Next Smaller Element](21-next-smaller-element.md) · [Part 23 index](README.md) · Next → [Sliding Window Maximum](23-sliding-window-maximum.md)

> [!abstract] Problem at a glance
> **Task:** Stack with `push`, `pop`, `top` and `getMin`, all O(1).
> **Key insight:** The minimum only changes on push or pop, so **remember it per level**. Store `(x, min so far)` pairs. For O(1) extra space: when pushing `x < min`, store the **encoded** value `2x − min` (always `< x`) and set `min = x`. A popped value below `min` signals that the min must be restored: `min = 2·min − stored`.
> **Difficulty:** Medium · **Pattern:** Augmented stack / value encoding · **Also on:** [LC 155](https://leetcode.com/problems/min-stack/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/implement-min-stack?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Stack of (value, min) pairs](#3-stack-of-value-min-pairs) · [4. Single stack + encoded values](#4-single-stack--encoded-values) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Design `MinStack` supporting `push(val)`, `pop()`, `top()` and `getMin()` in O(1) time each. `pop`, `top` and `getMin` are only called on a non-empty stack.

| Input | Output | Why |
|---|---|---|
| `push -2, push 0, push -3, getMin, pop, top, getMin` | `-3, 0, -2` |  |

**Constraints:** `−2³¹ ≤ val ≤ 2³¹ − 1`; up to `3·10⁴` calls.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Stack of (value, min) pairs | each level stores the min of everything at or below it | O(1) all ops | O(n) extra (2 ints per level) |
| Single stack + encoded values | push 2x − min when x is a new min | O(1) all ops | O(1) extra beyond the values |

> [!tip] Interview angle
> Lead with the pair stack; it's clear and obviously correct. Offer the `2x − min` encoding as the space follow-up, and mention it needs 64-bit arithmetic because `2x − min` can overflow `int`.

---

## 3. Stack of (value, min) pairs

**Intuition.** When you push `x`, the new minimum is `min(x, previous min)`. Store it alongside `x`. Popping restores the previous level, and with it the previous minimum.

```python
class PairMinStack:
    def __init__(self):
        self.st = []
    def push(self, x):
        self.st.append((x, min(x, self.st[-1][1]) if self.st else x))
    def pop(self):
        self.st.pop()
    def top(self):
        return self.st[-1][0]
    def getMin(self):
        return self.st[-1][1]
```

**Complexity:** time **O(1) all ops**, space **O(n) extra (2 ints per level)**.

---

## 4. Single stack + encoded values

**Intuition.** Keep `mn` in a variable. Pushing `x ≥ mn`: store `x`. Pushing `x < mn`: store `y = 2x − mn` and set `mn = x`. Since `x < mn`, `y = x + (x − mn) < x = mn`, so any stored value `< mn` is a flag. On pop of a flagged `y`, the old min is `2·mn − y`. On top, a flagged entry means the real value is `mn`.

**Algorithm**

1. `push(x)`: empty → push `x`, `mn = x`. Else if `x ≥ mn` push `x`; else push `2x − mn`, `mn = x`.
2. `pop()`: `y = pop()`; if `y < mn`, `mn = 2·mn − y`.
3. `top()`: `y = top()`; return `mn` if `y < mn` else `y`.
4. `getMin()`: `mn`.

**Dry run** — push −2 → st[−2], mn −2. push 0 → st[−2,0]. push −3 → store 2·(−3)−(−2) = −4, mn −3. getMin −3. pop −4 < −3 → mn = 2·(−3)−(−4) = −2. top 0. getMin −2.

**C++**
```cpp
class MinStack {
    vector<long long> st;
    long long mn = 0;
public:
    void push(int v) {
        long long x = v;
        if (st.empty()) { st.push_back(x); mn = x; }
        else if (x >= mn) st.push_back(x);
        else { st.push_back(2 * x - mn); mn = x; }
    }
    void pop() {
        long long y = st.back(); st.pop_back();
        if (y < mn) mn = 2 * mn - y;
    }
    int top() { long long y = st.back(); return (int)(y < mn ? mn : y); }
    int getMin() { return (int)mn; }
};
```

**Java**
```java
static class MinStack {
    private final Deque<Long> st = new ArrayDeque<>();
    private long mn = 0;
    void push(int v) {
        long x = v;
        if (st.isEmpty()) { st.push(x); mn = x; }
        else if (x >= mn) st.push(x);
        else { st.push(2 * x - mn); mn = x; }
    }
    void pop() {
        long y = st.pop();
        if (y < mn) mn = 2 * mn - y;
    }
    int top() { long y = st.peek(); return (int) (y < mn ? mn : y); }
    int getMin() { return (int) mn; }
}
```

**Python**
```python
class MinStack:
    def __init__(self):
        self.st, self.mn = [], 0
    def push(self, x):
        if not self.st:
            self.st.append(x)
            self.mn = x
        elif x >= self.mn:
            self.st.append(x)
        else:
            self.st.append(2 * x - self.mn)
            self.mn = x
    def pop(self):
        y = self.st.pop()
        if y < self.mn:
            self.mn = 2 * self.mn - y
    def top(self):
        y = self.st[-1]
        return self.mn if y < self.mn else y
    def getMin(self):
        return self.mn
```

**Complexity:** time **O(1) all ops**, space **O(1) extra beyond the values** — every operation does a constant amount of arithmetic and one stack operation.

---

## Edge cases

- Duplicate minimums: push `x == mn` as a plain value (the `≥` branch), so popping one copy keeps the min.
- Values near `INT_MIN`/`INT_MAX`: `2x − mn` overflows 32-bit.
- Popping back to empty, then pushing again: reset `mn` on the first push.

---

## Common mistakes

1. Separate min-stack that only pushes on `x < min`: then popping a duplicate minimum loses it. Push on `≤`.
2. Encoding with `int`: `2·(−2³¹) − x` overflows.
3. Returning the encoded value from `top()`.

---

## Follow-ups

1. Max stack with popMax (LC 716)?
2. Min queue?

<details><summary>Answer sketches</summary>

**#1:** Needs a sorted structure (TreeMap / two heaps with lazy deletion) plus a DLL; O(log n).

**#2:** Two min-stacks as a queue (amortised O(1)), or a monotonic deque.
</details>

---

## Flashcards

**Min stack with O(1) extra space: what do you push when x < min?** #flashcard
2x − min, then set min = x.

**How do you detect an encoded entry in the O(1)-space min stack?** #flashcard
Stored value < current min.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
