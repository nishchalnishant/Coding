---
module: striver/26-heaps
lesson: 5
topic: Implement Max Heap
difficulty: Medium
source: https://takeuforward.org/learning/dsa/implement-max-heap?category=theory-and-implementation&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, design]
---
# 5. Implement Max Heap

← [Implement Min Heap](04-implement-min-heap.md) · [Part 26 index](README.md) · Next → [Check if an array represents a min heap](06-check-if-an-array-represents-a-min-heap.md)

> [!abstract] Problem at a glance
> **Task:** Implement a max-priority queue with `push`, `pop` (return the max), `top` and `size`.
> **Key insight:** Identical to the min-heap with every key comparison flipped. Write it once around a single `higher(i, j)` predicate, and the same code becomes a min-heap, a max-heap or a custom-ordered heap.
> **Difficulty:** Medium · **Pattern:** Array-backed binary heap (comparator)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/implement-max-heap?category=theory-and-implementation&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Negated min-heap (heapq)](#3-negated-min-heap-heapq) · [4. Binary heap with a priority predicate](#4-binary-heap-with-a-priority-predicate) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Design `MaxHeap`: `push(x)`, `pop()` removes and returns the largest element, `top()` returns it, `size()` returns the count.

| Input | Output | Why |
|---|---|---|
| `push 5, 3, 8; top; push 10; pop; pop` | `8, 10, 8` |  |

**Constraints:** Up to `10⁵` operations.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Negated min-heap (heapq) | push −x, pop −heappop | O(log n) | O(n) |
| Binary heap with a priority predicate | higher(i, j) = a[i] > a[j] | push/pop O(log n) | O(n) |

> [!tip] Interview angle
> Ask whether they want a generic heap: one comparator (`less(a, b)` meaning 'a should be nearer the root') covers min, max and pair/tuple ordering. In Python, show the negation trick for `heapq` too.

---

## 3. Negated min-heap (heapq)

**Intuition.** Python only ships a min-heap. Store negatives: the smallest negative is the largest original. It's idiomatic for interviews, but it doesn't work for non-numeric keys (wrap them in a class with a reversed `__lt__`).

```python
import heapq
class NegMaxHeap:
    def __init__(self):
        self.h = []
    def push(self, x):
        heapq.heappush(self.h, -x)
    def pop(self):
        return -heapq.heappop(self.h)
    def top(self):
        return -self.h[0]
    def size(self):
        return len(self.h)
```

**Complexity:** time **O(log n)**, space **O(n)**.

---

## 4. Binary heap with a priority predicate

**Intuition.** Factor out `higher(i, j)`: true when `a[i]` belongs above `a[j]`. Sift up while the child is higher than its parent; sift down to the higher child while it's higher than the node.

**Algorithm**

1. `push`: append, sift up.
2. `pop`: save root, move last to root, sift down.
3. `higher(i, j) = a[i] > a[j]` (flip for a min-heap).

**Dry run** — push 5,3,8 → [8,3,5]. push 10 → [8,3,5,10] → 10 > 3 → [8,10,5,3] → 10 > 8 → [10,8,5,3]. pop → 10; last 3 to root [3,8,5] → higher child 8 → [8,3,5].

**C++**
```cpp
class MaxHeap {
    vector<int> a;
    bool higher(int i, int j) { return a[i] > a[j]; }
    void up(int i) {
        while (i > 0 && higher(i, (i - 1) / 2)) { swap(a[i], a[(i - 1) / 2]); i = (i - 1) / 2; }
    }
    void down(int i) {
        int n = a.size();
        while (true) {
            int b = i, l = 2 * i + 1, r = 2 * i + 2;
            if (l < n && higher(l, b)) b = l;
            if (r < n && higher(r, b)) b = r;
            if (b == i) return;
            swap(a[i], a[b]); i = b;
        }
    }
public:
    void push(int x) { a.push_back(x); up(a.size() - 1); }
    int pop() {
        int v = a[0];
        a[0] = a.back(); a.pop_back();
        if (!a.empty()) down(0);
        return v;
    }
    int top() { return a[0]; }
    int size() { return a.size(); }
};
```

**Java**
```java
static class MaxHeap {
    private int[] a = new int[16];
    private int n = 0;
    private boolean higher(int i, int j) { return a[i] > a[j]; }
    private void swap(int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
    private void up(int i) { while (i > 0 && higher(i, (i - 1) / 2)) { swap(i, (i - 1) / 2); i = (i - 1) / 2; } }
    private void down(int i) {
        while (true) {
            int b = i, l = 2 * i + 1, r = 2 * i + 2;
            if (l < n && higher(l, b)) b = l;
            if (r < n && higher(r, b)) b = r;
            if (b == i) return;
            swap(i, b); i = b;
        }
    }
    void push(int x) {
        if (n == a.length) a = Arrays.copyOf(a, 2 * n);
        a[n++] = x; up(n - 1);
    }
    int pop() { int v = a[0]; a[0] = a[--n]; down(0); return v; }
    int top() { return a[0]; }
    int size() { return n; }
}
```

**Python**
```python
class MaxHeap:
    def __init__(self):
        self.a = []
    def _higher(self, i, j):
        return self.a[i] > self.a[j]
    def _up(self, i):
        a = self.a
        while i > 0 and self._higher(i, (i - 1) // 2):
            p = (i - 1) // 2
            a[i], a[p] = a[p], a[i]
            i = p
    def _down(self, i):
        a, n = self.a, len(self.a)
        while True:
            b, l, r = i, 2 * i + 1, 2 * i + 2
            if l < n and self._higher(l, b): b = l
            if r < n and self._higher(r, b): b = r
            if b == i:
                return
            a[i], a[b] = a[b], a[i]
            i = b
    def push(self, x):
        self.a.append(x)
        self._up(len(self.a) - 1)
    def pop(self):
        a = self.a
        v, last = a[0], a.pop()
        if a:
            a[0] = last
            self._down(0)
        return v
    def top(self):
        return self.a[0]
    def size(self):
        return len(self.a)
```

**Complexity:** time **push/pop O(log n)**, space **O(n)** — same paths as the min-heap; only the predicate changed.

---

## Edge cases

- Negating `INT_MIN` overflows in C++/Java (the negation trick is safe in Python only).
- Pop to empty and push again.
- All equal keys.

---

## Common mistakes

1. Flipping only one of the two sift comparisons.
2. Using `-x` with `heapq` and forgetting to negate on `top`.
3. Java: `Collections.reverseOrder()` vs a lambda `(a, b) -> b - a`, where the lambda overflows for extreme ints. Use `Integer.compare(b, a)`.

---

## Follow-ups

1. Library max-heaps?
2. Heap of pairs ordered by (freq desc, key asc)?

<details><summary>Answer sketches</summary>

**#1:** C++ `priority_queue<int>` is max by default; Java `new PriorityQueue<>(Collections.reverseOrder())`; Python negate.

**#2:** Put the rule in the comparator (or push tuples `(-freq, key)` in Python).
</details>

---

## Flashcards

**Min-heap → max-heap: what changes?** #flashcard
Only the comparison predicate.

**Safe Java max-heap comparator?** #flashcard
`Collections.reverseOrder()` or `(a, b) -> Integer.compare(b, a)`; `b - a` can overflow.

**Python max-heap?** #flashcard
`heapq` with negated keys.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
