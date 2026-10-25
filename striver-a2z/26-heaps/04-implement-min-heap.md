---
module: striver-a2z/26-heaps
lesson: 4
topic: Implement Min Heap
difficulty: Medium
source: https://takeuforward.org/learning/dsa/implement-min-heap?category=theory-and-implementation&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, design]
---
# 4. Implement Min Heap

← [Build heap from a given Array](03-build-heap-from-a-given-array.md) · [Part 26 index](README.md) · Next → [Implement Max Heap](05-implement-max-heap.md)

> [!abstract] Problem at a glance
> **Task:** Implement a min-priority queue with `push`, `pop` (return the min), `top` and `size` on a dynamic array.
> **Key insight:** Complete-tree shape lives in an array: `push` = append at the end + sift up, `pop` = move the last element to the root + sift down. Both touch one path, so O(log n). `top` is `a[0]`.
> **Difficulty:** Medium · **Pattern:** Array-backed binary heap
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/implement-min-heap?category=theory-and-implementation&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sorted list](#3-sorted-list) · [4. Binary heap on an array](#4-binary-heap-on-an-array) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Design `MinHeap`: `push(x)` inserts `x`; `pop()` removes and returns the smallest element; `top()` returns it without removing; `size()` returns the count. `pop`/`top` are only called on a non-empty heap.

| Input | Output | Why |
|---|---|---|
| `push 5, 3, 8; top; push 1; pop; pop` | `3, 1, 3` |  |

**Constraints:** Up to `10⁵` operations.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sorted list | insert in order, pop from the front | push O(n), pop O(1)· | O(n) |
| Binary heap on an array | append+siftUp · swap last to root+siftDown | push/pop O(log n), top/size O(1) | O(n) |

> [!tip] Interview angle
> Write `siftUp` and `siftDown` as helpers first, then each public method is 2–3 lines. Mention `changeKey(i, v)` = assign + (sift up or down) and that it needs an index map if callers refer to items rather than positions.

---

## 3. Sorted list

**Intuition.** Keep the list sorted descending so the min is at the end (`pop()` is O(1)); `bisect.insort` finds the spot in O(log n) but shifting is O(n). Fine for small n, quadratic for n operations.

```python
import bisect
class SortedMinHeap:
    def __init__(self):
        self.a = []                       # ascending; negate for descending
    def push(self, x):
        bisect.insort(self.a, -x)         # store negatives: smallest x at the end
    def pop(self):
        return -self.a.pop()
    def top(self):
        return -self.a[-1]
    def size(self):
        return len(self.a)
```

**Complexity:** time **push O(n), pop O(1)·**, space **O(n)**.

---

## 4. Binary heap on an array

**Intuition.** The array is a complete binary tree in level order, so there are no pointers and no holes. The heap property (parent ≤ children) puts the min at index 0. Mutations break it along one path only, and a sift repairs that path.

**Algorithm**

1. `push(x)`: append; sift up the last index.
2. `pop()`: save `a[0]`; move `a.back()` to index 0; pop back; sift down 0; return the saved value.
3. `top()`: `a[0]`. `size()`: array length.

**Dry run** — push 5,3,8 → [3,5,8]. push 1 → append [3,5,8,1], 1 < parent 5 → [3,1,8,5], 1 < 3 → [1,3,8,5]. pop → returns 1; last 5 to root [5,3,8] → sift: 3 < 5 → [3,5,8].

**C++**
```cpp
class MinHeap {
    vector<int> a;
    void up(int i) {
        while (i > 0 && a[(i - 1) / 2] > a[i]) { swap(a[i], a[(i - 1) / 2]); i = (i - 1) / 2; }
    }
    void down(int i) {
        int n = a.size();
        while (true) {
            int s = i, l = 2 * i + 1, r = 2 * i + 2;
            if (l < n && a[l] < a[s]) s = l;
            if (r < n && a[r] < a[s]) s = r;
            if (s == i) return;
            swap(a[i], a[s]); i = s;
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
static class MinHeap {
    private final ArrayList<Integer> a = new ArrayList<>();
    private void swap(int i, int j) { int t = a.get(i); a.set(i, a.get(j)); a.set(j, t); }
    private void up(int i) {
        while (i > 0 && a.get((i - 1) / 2) > a.get(i)) { swap(i, (i - 1) / 2); i = (i - 1) / 2; }
    }
    private void down(int i) {
        int n = a.size();
        while (true) {
            int s = i, l = 2 * i + 1, r = 2 * i + 2;
            if (l < n && a.get(l) < a.get(s)) s = l;
            if (r < n && a.get(r) < a.get(s)) s = r;
            if (s == i) return;
            swap(i, s); i = s;
        }
    }
    void push(int x) { a.add(x); up(a.size() - 1); }
    int pop() {
        int v = a.get(0), last = a.remove(a.size() - 1);
        if (!a.isEmpty()) { a.set(0, last); down(0); }
        return v;
    }
    int top() { return a.get(0); }
    int size() { return a.size(); }
}
```

**Python**
```python
class MinHeap:
    def __init__(self):
        self.a = []
    def _up(self, i):
        a = self.a
        while i > 0 and a[(i - 1) // 2] > a[i]:
            p = (i - 1) // 2
            a[i], a[p] = a[p], a[i]
            i = p
    def _down(self, i):
        a, n = self.a, len(self.a)
        while True:
            s, l, r = i, 2 * i + 1, 2 * i + 2
            if l < n and a[l] < a[s]: s = l
            if r < n and a[r] < a[s]: s = r
            if s == i:
                return
            a[i], a[s] = a[s], a[i]
            i = s
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

**Complexity:** time **push/pop O(log n), top/size O(1)**, space **O(n)** — height of a complete tree is ⌊log₂ n⌋ and each sift walks one path.

---

## Edge cases

- Pop down to empty: skip the sift (Java's `remove` returns the last element, which *was* the root).
- Duplicate minimums: strict comparisons keep them stable enough; any copy is a valid answer.
- Negative values.

---

## Common mistakes

1. `pop` moves the last element to the root **after** removing it: with one element you'd write it back into an empty array.
2. Sifting down toward the left child unconditionally.
3. Forgetting to sift up after `push` (the heap becomes a plain list).

---

## Follow-ups

1. `changeKey(i, v)` / decrease-key.
2. Library equivalents?

<details><summary>Answer sketches</summary>

**#1:** Assign and run whichever sift applies. With item handles you also need `pos[item]` updated on every swap (Dijkstra with decrease-key).

**#2:** C++ `priority_queue<int, vector<int>, greater<int>>`; Java `PriorityQueue<Integer>` (min by default); Python `heapq` on a list.
</details>

---

## Flashcards

**Heap push / pop recipe?** #flashcard
Push: append + sift up. Pop: last → root, shrink, sift down.

**Why an array, not nodes?** #flashcard
A complete tree has no holes, so index arithmetic replaces pointers.

**Default order: C++ priority_queue / Java PriorityQueue / heapq?** #flashcard
Max / min / min.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
