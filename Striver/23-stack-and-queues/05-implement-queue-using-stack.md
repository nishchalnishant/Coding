---
module: striver/23-stack-and-queues
lesson: 5
topic: Implement Queue using Stack
difficulty: Easy
source: https://takeuforward.org/learning/dsa/implement-queue-using-stack?category=implementation&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, queue, stack, design, amortised]
---
# 5. Implement Queue using Stack

← [Implement Stack using Queue](04-implement-stack-using-queue.md) · [Part 23 index](README.md) · Next → [Implement stack using Linkedlist](06-implement-stack-using-linkedlist.md)

> [!abstract] Problem at a glance
> **Task:** Implement a FIFO queue using only stack operations.
> **Key insight:** Use two stacks: `in` for pushes and `out` for pops. When `out` is empty, pour all of `in` into it, which reverses the order so the oldest is on top. Each element is moved **at most once**, so every operation is amortised O(1).
> **Difficulty:** Easy · **Pattern:** Two stacks, lazy transfer · **Also on:** [LC 232](https://leetcode.com/problems/implement-queue-using-stacks/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/implement-queue-using-stack?category=implementation&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Transfer on every push](#3-transfer-on-every-push) · [4. Two stacks, lazy transfer](#4-two-stacks-lazy-transfer) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement `MyQueue` with `push(x)`, `pop()`, `peek()` and `empty()` using only push-to-top, peek/pop-from-top, size and is-empty stack operations. `pop`/`peek` calls are valid.

| Input | Output | Why |
|---|---|---|
| `push 1, push 2, peek, pop, empty` | `1, 1, false` |  |

**Constraints:** `1 ≤ x ≤ 9`; at most 100 calls. Follow-up: amortised O(1) per operation.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Transfer on every push | keep oldest on top of s1 by moving s1 → s2 → s1 | push O(n), pop O(1) | O(n) |
| Two stacks, lazy transfer | pour in → out only when out is empty | O(1) amortised | O(n) |

> [!tip] Interview angle
> This is an amortised-analysis question. Explain why the transfer is lazy (only when `out` is empty) and why each element crosses at most once. Transferring back and forth on every op is the common O(n) mistake.

---

## 3. Transfer on every push

**Intuition.** To push `x`, move all of `s1` onto `s2`, push `x` onto `s1`, then move everything back. The oldest element stays on top of `s1`.

```python
class EagerQueue:
    def __init__(self):
        self.s1, self.s2 = [], []
    def push(self, x):
        while self.s1:
            self.s2.append(self.s1.pop())
        self.s1.append(x)
        while self.s2:
            self.s1.append(self.s2.pop())
    def pop(self):
        return self.s1.pop()
    def peek(self):
        return self.s1[-1]
    def empty(self):
        return not self.s1
```

**Complexity:** time **push O(n), pop O(1)**, space **O(n)**.

---

## 4. Two stacks, lazy transfer

**Intuition.** `out`'s top is always the queue front, as long as `out` is non-empty. New elements wait in `in`. Pouring reverses `in`, so the oldest waiting element lands on top. Elements already in `out` are older than everything in `in`, which is why you must not pour while `out` still has items.

**Algorithm**

1. `push(x)`: `in.push(x)`.
2. `peek()`: if `out` empty, move all of `in` onto `out`; return `out.top()`.
3. `pop()`: `peek()`, then `out.pop()`.
4. `empty()`: both empty.

**Dry run** — push 1,2 → in=[1,2]. peek: out=[2,1] → 1. pop → 1, out=[2]. push 3 → in=[3]. pop → 2 (out non-empty, no pour). pop → pour → out=[3] → 3.

**C++**
```cpp
class MyQueue {
    stack<int> in, out;
    void pour() { if (out.empty()) while (!in.empty()) { out.push(in.top()); in.pop(); } }
public:
    void push(int x) { in.push(x); }
    int peek() { pour(); return out.top(); }
    int pop() { pour(); int x = out.top(); out.pop(); return x; }
    bool empty() { return in.empty() && out.empty(); }
};
```

**Java**
```java
static class MyQueue {
    private Deque<Integer> in = new ArrayDeque<>(), out = new ArrayDeque<>();
    private void pour() { if (out.isEmpty()) while (!in.isEmpty()) out.push(in.pop()); }
    void push(int x) { in.push(x); }
    int peek() { pour(); return out.peek(); }
    int pop() { pour(); return out.pop(); }
    boolean empty() { return in.isEmpty() && out.isEmpty(); }
}
```

**Python**
```python
class MyQueue:
    def __init__(self):
        self.inn, self.out = [], []
    def _pour(self):
        if not self.out:
            while self.inn:
                self.out.append(self.inn.pop())
    def push(self, x):
        self.inn.append(x)
    def peek(self):
        self._pour()
        return self.out[-1]
    def pop(self):
        self._pour()
        return self.out.pop()
    def empty(self):
        return not self.inn and not self.out
```

**Complexity:** time **O(1) amortised**, space **O(n)** — each element is pushed to `in` once, moved to `out` once, popped once: 3 stack ops per element over its lifetime.

---

## Edge cases

- Push after a partial drain: new items must wait behind `out`.
- Alternating push/pop: one pour per element.

---

## Common mistakes

1. Pouring when `out` is non-empty, which puts newer elements above older ones.
2. Moving everything back to `in` after each pop, which makes it O(n) per op.
3. Using `peek` without the pour.

---

## Follow-ups

1. Worst-case (not amortised) O(1)?
2. Where is this used?

<details><summary>Answer sketches</summary>

**#1:** Not with plain stacks in the simple scheme; real-time queues use incremental rebuilding (Hood–Melville).

**#2:** Functional/persistent queues (Okasaki), and as the basis of the two-stack sliding-window aggregate.
</details>

---

## Flashcards

**When do you transfer in → out in the two-stack queue?** #flashcard
Only when `out` is empty; otherwise you'd break FIFO order.

**Why is the two-stack queue amortised O(1)?** #flashcard
Each element moves from `in` to `out` at most once.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
