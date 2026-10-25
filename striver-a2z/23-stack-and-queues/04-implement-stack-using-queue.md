---
module: striver-a2z/23-stack-and-queues
lesson: 4
topic: Implement Stack using Queue
difficulty: Easy
source: https://takeuforward.org/learning/dsa/implement-stack-using-queue?category=implementation&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, queue, design]
---
# 4. Implement Stack using Queue

← [Implement Queue using Arrays](03-implement-queue-using-arrays.md) · [Part 23 index](README.md) · Next → [Implement Queue using Stack](05-implement-queue-using-stack.md)

> [!abstract] Problem at a glance
> **Task:** Implement a LIFO stack using only queue operations (push to back, pop from front, peek front, size).
> **Key insight:** Make **push** the expensive operation. After enqueuing `x`, rotate the `size − 1` older elements from the front to the back. `x` is now at the front, so `pop` and `top` are plain queue `pop` and `front`.
> **Difficulty:** Easy · **Pattern:** Rotate on push · **Also on:** [LC 225](https://leetcode.com/problems/implement-stack-using-queues/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/implement-stack-using-queue?category=implementation&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Two queues](#3-two-queues) · [4. One queue, rotate on push](#4-one-queue-rotate-on-push) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement `MyStack` with `push(x)`, `pop()`, `top()` and `empty()` using only standard queue operations. Calls to `pop`/`top` are valid (the stack is non-empty).

| Input | Output | Why |
|---|---|---|
| `push 1, push 2, top, pop, empty` | `2, 2, false` |  |

**Constraints:** `1 ≤ x ≤ 9`; at most 100 calls.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Two queues | push into q2, drain q1 into q2, swap | push O(n), pop O(1) | O(n) |
| One queue, rotate on push | enqueue x, then cycle size−1 elements behind it | push O(n), pop O(1) | O(n) |

> [!tip] Interview angle
> Say up front which operation you make O(n) and why. Rotating on push keeps `pop`/`top` O(1). The two-queue version is the textbook answer; the one-queue rotate is the cleaner follow-up.

---

## 3. Two queues

**Intuition.** Enqueue `x` into the empty `q2`, move everything from `q1` behind it, then swap names. `q1` always holds elements newest-first.

```python
from collections import deque
class TwoQueueStack:
    def __init__(self):
        self.q1, self.q2 = deque(), deque()
    def push(self, x):
        self.q2.append(x)
        while self.q1:
            self.q2.append(self.q1.popleft())
        self.q1, self.q2 = self.q2, self.q1
    def pop(self):
        return self.q1.popleft()
    def top(self):
        return self.q1[0]
    def empty(self):
        return not self.q1
```

**Complexity:** time **push O(n), pop O(1)**, space **O(n)**.

---

## 4. One queue, rotate on push

**Intuition.** After `q.push(x)`, the queue is `[older…, x]`. Popping from the front and re-pushing `size − 1` times gives `[x, older…]`, so the newest is at the front.

**Algorithm**

1. `push(x)`: enqueue; repeat `size−1` times: `q.push(q.front()); q.pop()`.
2. `pop()`: dequeue and return.
3. `top()`: front. `empty()`: queue empty.

**Dry run** — push 1 → [1]. push 2 → [1,2] → rotate 1 → [2,1]. top=2, pop=2 → [1]. push 3 → [1,3] → [3,1].

**C++**
```cpp
class MyStack {
    queue<int> q;
public:
    void push(int x) {
        q.push(x);
        for (int i = 0; i + 1 < (int)q.size(); i++) { q.push(q.front()); q.pop(); }
    }
    int pop() { int x = q.front(); q.pop(); return x; }
    int top() { return q.front(); }
    bool empty() { return q.empty(); }
};
```

**Java**
```java
static class MyStack {
    private Queue<Integer> q = new ArrayDeque<>();
    void push(int x) {
        q.offer(x);
        for (int i = 0; i + 1 < q.size(); i++) q.offer(q.poll());
    }
    int pop() { return q.poll(); }
    int top() { return q.peek(); }
    boolean empty() { return q.isEmpty(); }
}
```

**Python**
```python
from collections import deque
class MyStack:
    def __init__(self):
        self.q = deque()
    def push(self, x):
        self.q.append(x)
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())
    def pop(self):
        return self.q.popleft()
    def top(self):
        return self.q[0]
    def empty(self):
        return not self.q
```

**Complexity:** time **push O(n), pop O(1)**, space **O(n)** — push rotates n − 1 elements; pop/top touch only the front.

---

## Edge cases

- Single element: rotation count is 0.
- Interleaved push/pop keeps the invariant (front = newest).

---

## Common mistakes

1. Rotating `size` times instead of `size − 1`, which puts `x` back at the end.
2. Using deque operations from the wrong end (`pop()` from the back), which defeats the exercise.
3. Making both push and pop O(n) by rotating in both.

---

## Follow-ups

1. Make pop O(n) and push O(1) instead?
2. Which is better?

<details><summary>Answer sketches</summary>

**#1:** Push normally; on pop, rotate size − 1 to the back, then dequeue the front.

**#2:** Depends on the mix: rotate on the rarer operation.
</details>

---

## Flashcards

**Stack from one queue: what does push do?** #flashcard
Enqueue x, then move the size−1 older elements from front to back, so x is at the front.

**Complexities of the rotate-on-push stack?** #flashcard
push O(n), pop/top/empty O(1).

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
