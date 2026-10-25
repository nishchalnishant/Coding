---
module: striver-a2z/23-stack-and-queues
lesson: 6
topic: Implement stack using Linkedlist
difficulty: Easy
source: https://takeuforward.org/learning/dsa/implement-stack-using-linkedlist?category=implementation&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, linked-list, design]
---
# 6. Implement stack using Linkedlist

← [Implement Queue using Stack](05-implement-queue-using-stack.md) · [Part 23 index](README.md) · Next → [Implement queue using Linkedlist](07-implement-queue-using-linkedlist.md)

> [!abstract] Problem at a glance
> **Task:** Build a stack whose storage is a singly linked list; all ops O(1), no capacity limit.
> **Key insight:** The **head** of the list is the top. Push allocates a node pointing to the old head; pop unlinks the head. No resizing and no wasted capacity, at the cost of one pointer per element and worse cache locality.
> **Difficulty:** Easy · **Pattern:** Linked list, insert/delete at head · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/implement-stack-using-linked-list/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/implement-stack-using-linkedlist?category=implementation&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Head = top](#3-head--top) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement a stack using a singly linked list with `push(x)`, `pop()` (returns the top or `-1`), `top()` (or `-1`), `size()` and `isEmpty()`.

| Input | Output | Why |
|---|---|---|
| `push 2, push 3, pop, top` | `3, 2` |  |

**Constraints:** Up to `10⁵` operations.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Head = top | push: new node → old head; pop: head = head.next | O(1) per op | O(n) |

> [!tip] Interview angle
> Expect the follow-up: array or linked list, which is better? The answer covers amortised vs worst-case O(1), memory overhead per node, and cache locality. Also free the popped node in C++.

---

## 3. Head = top

**Intuition.** Keep `head` and a `count`. Inserting and deleting at the head of a singly linked list are both O(1), which matches LIFO exactly. Using the tail as the top would make pop O(n), because you can't find the previous node.

**Algorithm**

1. `push(x)`: `head = Node(x, head)`; `count++`.
2. `pop()`: if `head` null return −1; save value, `head = head.next`, free old node, `count--`.
3. `top()`: `head.val` or −1.

**Dry run** — push 2 → 2. push 3 → 3→2. pop → 3, head=2. top → 2. size → 1.

**C++**
```cpp
class LinkedStack {
    struct Node { int val; Node* next; Node(int v, Node* n) : val(v), next(n) {} };
    Node* head = nullptr; int cnt = 0;
public:
    ~LinkedStack() { while (head) { Node* t = head; head = head->next; delete t; } }
    void push(int x) { head = new Node(x, head); cnt++; }
    int pop() {
        if (!head) return -1;
        Node* t = head; int v = t->val;
        head = head->next; delete t; cnt--;
        return v;
    }
    int top() { return head ? head->val : -1; }
    int size() { return cnt; }
    bool isEmpty() { return head == nullptr; }
};
```

**Java**
```java
static class LinkedStack {
    private static class Node { int val; Node next; Node(int v, Node n) { val = v; next = n; } }
    private Node head; private int cnt;
    void push(int x) { head = new Node(x, head); cnt++; }
    int pop() {
        if (head == null) return -1;
        int v = head.val; head = head.next; cnt--;
        return v;
    }
    int top() { return head == null ? -1 : head.val; }
    int size() { return cnt; }
    boolean isEmpty() { return head == null; }
}
```

**Python**
```python
class LinkedStack:
    class Node:
        __slots__ = ("val", "next")
        def __init__(self, val, nxt):
            self.val, self.next = val, nxt
    def __init__(self):
        self.head, self.cnt = None, 0
    def push(self, x):
        self.head = self.Node(x, self.head)
        self.cnt += 1
    def pop(self):
        if not self.head:
            return -1
        v = self.head.val
        self.head = self.head.next
        self.cnt -= 1
        return v
    def top(self):
        return self.head.val if self.head else -1
    def size(self):
        return self.cnt
    def isEmpty(self):
        return self.head is None
```

**Complexity:** time **O(1) per op**, space **O(n)** — every op rewires one pointer; one node per element.

---

## Edge cases

- Pop on empty → −1.
- Push after emptying (head was null).

---

## Common mistakes

1. Using the tail as top: pop then needs the predecessor, so it's O(n).
2. Forgetting to `delete` the popped node in C++ (a leak).
3. Recomputing size by walking the list.

---

## Follow-ups

1. Array vs linked-list stack?
2. Lock-free stack?

<details><summary>Answer sketches</summary>

**#1:** Array: amortised O(1), contiguous and cache-friendly, occasional O(n) resize. List: worst-case O(1), but 8–16 B pointer overhead per element and scattered allocations.

**#2:** The Treiber stack: CAS on head; watch for the ABA problem.
</details>

---

## Flashcards

**Which end of a singly linked list is the top of a stack?** #flashcard
The head: insert and delete there are O(1).

**Linked-list stack vs array stack: one advantage each?** #flashcard
List: worst-case O(1) and no capacity. Array: cache locality and no per-node pointer.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
