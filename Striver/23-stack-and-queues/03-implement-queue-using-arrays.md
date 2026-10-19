---
module: striver/23-stack-and-queues
lesson: 3
topic: Implement Queue using Arrays
difficulty: Easy
source: https://takeuforward.org/learning/dsa/implement-queue-using-arrays?category=implementation&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, queue, array, circular-buffer, design]
---
# 3. Implement Queue using Arrays

← [Implement Stack using Arrays](02-implement-stack-using-arrays.md) · [Part 23 index](README.md) · Next → [Implement Stack using Queue](04-implement-stack-using-queue.md)

> [!abstract] Problem at a glance
> **Task:** Build a FIFO queue on an array: `push`, `pop`, `peek`, `size`, `isEmpty`, all O(1).
> **Key insight:** Use a **circular buffer**. Keep `front` and `count`; the back slot is `(front + count) % cap`. Both ends move forward modulo `cap`, so nothing ever shifts. When it's full, copy into a 2× buffer in queue order.
> **Difficulty:** Easy · **Pattern:** Circular buffer · **Also on:** [LC 622](https://leetcode.com/problems/design-circular-queue/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/implement-queue-using-arrays?category=implementation&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Shift on dequeue](#3-shift-on-dequeue) · [4. Circular buffer (with doubling)](#4-circular-buffer-with-doubling) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement a queue using an array with `push(x)` (enqueue), `pop()` (dequeue and return the front, or `-1` if empty), `peek()` (front or `-1`), `size()` and `isEmpty()`.

| Input | Output | Why |
|---|---|---|
| `push 1, push 2, pop, peek` | `1, 2` | 1 entered first, leaves first |
| `pop on empty` | `-1` |  |

**Constraints:** Up to `10⁵` operations.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Shift on dequeue | front is always index 0; pop shifts everything left | push O(1), pop O(n) | O(n) |
| Circular buffer (with doubling) | front + count, indices mod cap | O(1) amortised | O(n) |

> [!tip] Interview angle
> The trap is the naive `pop(0)` / shifting version, which makes dequeue O(n). Also, `front == rear` alone can't tell full from empty. Keep a `count` (or waste one slot) and say which convention you chose.

---

## 3. Shift on dequeue

**Intuition.** Append at the end and remove from index 0. Correct and short, but every dequeue moves all remaining elements.

```python
class ShiftQueue:
    def __init__(self):
        self.a = []
    def push(self, x):
        self.a.append(x)
    def pop(self):
        return self.a.pop(0) if self.a else -1     # O(n) shift
    def peek(self):
        return self.a[0] if self.a else -1
    def size(self):
        return len(self.a)
    def isEmpty(self):
        return not self.a
```

**Complexity:** time **push O(1), pop O(n)**, space **O(n)**.

---

## 4. Circular buffer (with doubling)

**Intuition.** The live elements occupy `front, front+1, …, front+count−1` modulo `cap`. Enqueue writes at `(front + count) % cap`; dequeue reads `a[front]` and advances `front`. When `count == cap`, unroll the ring into a new array of size `2·cap` starting at index 0.

**Algorithm**

1. `push(x)`: if `count == cap`, copy `a[(front+i) % cap]` for `i < count` into a 2× array and set `front = 0`. Then `a[(front+count) % cap] = x`, `count++`.
2. `pop()`: if `count == 0` return −1; `x = a[front]`, `front = (front+1) % cap`, `count--`.
3. `peek()`: `a[front]` or −1.

**Dry run** — cap 4: push 1,2,3 → pop=1 (front=1) → push 4 (slot 0... no: slot (1+2)%4=3), push 5 (slot (1+3)%4=0, wrapped) → push 6 full → unroll [2,3,4,5] into cap 8, append 6.

**C++**
```cpp
class ArrayQueue {
    vector<int> a; int f = 0, n = 0;
public:
    ArrayQueue() : a(4) {}
    void push(int x) {
        if (n == (int)a.size()) {
            vector<int> b(2 * a.size());
            for (int i = 0; i < n; i++) b[i] = a[(f + i) % a.size()];
            a = b; f = 0;
        }
        a[(f + n) % a.size()] = x;
        n++;
    }
    int pop() {
        if (n == 0) return -1;
        int x = a[f];
        f = (f + 1) % a.size(); n--;
        return x;
    }
    int peek() { return n ? a[f] : -1; }
    int size() { return n; }
    bool isEmpty() { return n == 0; }
};
```

**Java**
```java
static class ArrayQueue {
    private int[] a = new int[4];
    private int f = 0, n = 0;
    void push(int x) {
        if (n == a.length) {
            int[] b = new int[2 * a.length];
            for (int i = 0; i < n; i++) b[i] = a[(f + i) % a.length];
            a = b; f = 0;
        }
        a[(f + n) % a.length] = x;
        n++;
    }
    int pop() {
        if (n == 0) return -1;
        int x = a[f];
        f = (f + 1) % a.length; n--;
        return x;
    }
    int peek() { return n > 0 ? a[f] : -1; }
    int size() { return n; }
    boolean isEmpty() { return n == 0; }
}
```

**Python**
```python
class ArrayQueue:
    def __init__(self):
        self.a, self.f, self.n = [0] * 4, 0, 0
    def push(self, x):
        cap = len(self.a)
        if self.n == cap:
            self.a = [self.a[(self.f + i) % cap] for i in range(self.n)] + [0] * cap
            self.f, cap = 0, 2 * cap
        self.a[(self.f + self.n) % cap] = x
        self.n += 1
    def pop(self):
        if self.n == 0:
            return -1
        x = self.a[self.f]
        self.f = (self.f + 1) % len(self.a)
        self.n -= 1
        return x
    def peek(self):
        return self.a[self.f] if self.n else -1
    def size(self):
        return self.n
    def isEmpty(self):
        return self.n == 0
```

**Complexity:** time **O(1) amortised**, space **O(n)** — each op touches O(1) slots; unrolling on growth is amortised like vector doubling.

---

## Edge cases

- Wrap-around: the back index passes the end of the array.
- Grow while wrapped: copy in queue order, not array order.
- Dequeue on empty.

---

## Common mistakes

1. `front == rear` used for both empty and full. Keep a count or leave one slot unused.
2. Copying the raw array on growth while the ring is wrapped, which scrambles the order.
3. Using `list.pop(0)` in Python. It's O(n); use `collections.deque`.

---

## Follow-ups

1. Fixed capacity, reject when full (LC 622)?
2. Double-ended queue?

<details><summary>Answer sketches</summary>

**#1:** Same ring; `enQueue` returns false when `count == cap`; `Rear` is `a[(front + count − 1) % cap]`.

**#2:** Allow `front = (front − 1 + cap) % cap` for push-front; LC 641.
</details>

---

## Flashcards

**How do you tell a full circular buffer from an empty one?** #flashcard
Track `count` (or keep one slot always empty, so full is `(rear+1)%cap == front`).

**Back slot of a circular queue with front f and count n?** #flashcard
`(f + n) % cap`.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
