---
module: striver-a2z/23-stack-and-queues
lesson: 2
topic: Implement Stack using Arrays
difficulty: Easy
source: https://takeuforward.org/learning/dsa/implement-stack-using-arrays?category=implementation&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, array, design, amortised]
---
# 2. Implement Stack using Arrays

← [Stacks & Queues: Implementations, Monotonic Stacks and Design](01-stack-queue-implementation-theory.md) · [Part 23 index](README.md) · Next → [Implement Queue using Arrays](03-implement-queue-using-arrays.md)

> [!abstract] Problem at a glance
> **Task:** Build a LIFO stack on a raw array: `push`, `pop`, `top`, `size`, `isEmpty`, all O(1).
> **Key insight:** One index `t` marks the top element. `push` writes at `++t` and `pop` reads at `t--`. A fixed array overflows, so double the capacity when it is full. Each element is copied O(1) times on average, so push is **amortised** O(1).
> **Difficulty:** Easy · **Pattern:** Array + top index (+ doubling) · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/implement-stack-using-array/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/implement-stack-using-arrays?category=implementation&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Fixed-capacity array](#3-fixed-capacity-array) · [4. Growable array (capacity doubling)](#4-growable-array-capacity-doubling) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement a stack using an array with `push(x)`, `pop()` (removes and returns the top, or `-1` if empty), `top()` (returns the top or `-1`), `size()` and `isEmpty()`.

| Input | Output | Why |
|---|---|---|
| `push 5, push 10, top, pop, size` | `10, 10, 1` | 10 was pushed last, so it's on top |
| `pop on empty` | `-1` | sentinel instead of an exception |

**Constraints:** Up to `10⁵` operations; values fit in `int`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Fixed-capacity array | t = index of top; overflow when full | O(1) per op | O(cap) |
| Growable array (capacity doubling) | when full, copy into an array twice the size | O(1) amortised | O(n) |

> [!tip] Interview angle
> A warm-up. What the interviewer checks: the empty/full guards, consistent `t` semantics (index of the top, not one past it), and whether you can explain why doubling (not +1) gives amortised O(1).

---

## 3. Fixed-capacity array

**Intuition.** Preallocate `cap` slots and keep `t = -1` for empty. Simple and cache-friendly, but the capacity has to be known in advance, and `push` on a full stack fails.

```python
class FixedStack:
    def __init__(self, cap=1000):
        self.a, self.t = [0] * cap, -1
    def push(self, x):
        if self.t + 1 == len(self.a):
            raise OverflowError("stack full")
        self.t += 1
        self.a[self.t] = x
    def pop(self):
        if self.t < 0:
            return -1
        self.t -= 1
        return self.a[self.t + 1]
    def top(self):
        return self.a[self.t] if self.t >= 0 else -1
    def size(self):
        return self.t + 1
    def isEmpty(self):
        return self.t < 0
```

**Complexity:** time **O(1) per op**, space **O(cap)**.

---

## 4. Growable array (capacity doubling)

**Intuition.** Same top index, but when `t + 1 == cap`, allocate `2·cap` and copy. Copies cost 1 + 2 + 4 + … + n/2 < n over n pushes, so each push costs O(1) on average. This is how `std::vector`, `ArrayList` and Python `list` work.

**Algorithm**

1. `push(x)`: if full, grow to `2·cap`; then `a[++t] = x`.
2. `pop()`: if `t < 0` return −1; else return `a[t--]`.
3. `top()`: `a[t]` or −1; `size() = t + 1`; `isEmpty() = t < 0`.

**Dry run** — cap 4: push 1..4 fills it → push 5 grows to 8 → push 6. top=6, pop=6, pop=5, size=4.

**C++**
```cpp
class ArrayStack {
    int* a; int cap, t;
    void grow() {
        int* b = new int[cap * 2];
        for (int i = 0; i <= t; i++) b[i] = a[i];
        delete[] a; a = b; cap *= 2;
    }
public:
    ArrayStack() : a(new int[4]), cap(4), t(-1) {}
    ~ArrayStack() { delete[] a; }
    void push(int x) { if (t + 1 == cap) grow(); a[++t] = x; }
    int pop() { return t < 0 ? -1 : a[t--]; }
    int top() { return t < 0 ? -1 : a[t]; }
    int size() { return t + 1; }
    bool isEmpty() { return t < 0; }
};
```

**Java**
```java
static class ArrayStack {
    private int[] a = new int[4];
    private int t = -1;
    void push(int x) {
        if (t + 1 == a.length) a = Arrays.copyOf(a, a.length * 2);
        a[++t] = x;
    }
    int pop() { return t < 0 ? -1 : a[t--]; }
    int top() { return t < 0 ? -1 : a[t]; }
    int size() { return t + 1; }
    boolean isEmpty() { return t < 0; }
}
```

**Python**
```python
class ArrayStack:
    def __init__(self):
        self.a, self.t = [0] * 4, -1
    def push(self, x):
        if self.t + 1 == len(self.a):
            self.a += [0] * len(self.a)        # double capacity
        self.t += 1
        self.a[self.t] = x
    def pop(self):
        if self.t < 0:
            return -1
        self.t -= 1
        return self.a[self.t + 1]
    def top(self):
        return self.a[self.t] if self.t >= 0 else -1
    def size(self):
        return self.t + 1
    def isEmpty(self):
        return self.t < 0
```

**Complexity:** time **O(1) amortised**, space **O(n)** — every op touches one slot; growth copies total < 2n over n pushes.

---

## Edge cases

- `pop` / `top` on an empty stack → −1 (or throw; state your choice).
- Push exactly at capacity triggers growth.
- Interleaved push/pop around the resize boundary.

---

## Common mistakes

1. Mixing up `t` as top index and as size, which causes off-by-one on `top()`.
2. Growing by +1 (or +k) instead of ×2, making n pushes O(n²).
3. Reading `a[t]` before checking `t ≥ 0`.

---

## Follow-ups

1. Shrink when sparse?
2. Two stacks in one array?

<details><summary>Answer sketches</summary>

**#1:** Halve when size drops to cap/4 (not cap/2), otherwise alternating push/pop at the boundary thrashes.

**#2:** Grow one from the left end and one from the right; full when the tops meet.
</details>

---

## Flashcards

**Why does capacity doubling give amortised O(1) push?** #flashcard
Copies total 1+2+…+n/2 < n over n pushes, so O(1) each on average.

**Why shrink at 1/4 full, not 1/2?** #flashcard
Halving at 1/2 lets a push/pop pair at the boundary trigger repeated O(n) resizes.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
