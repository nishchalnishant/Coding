---
module: striver-a2z/23-stack-and-queues
lesson: 7
topic: Implement queue using Linkedlist
difficulty: Easy
source: https://takeuforward.org/learning/dsa/implement-queue-using-linkedlist?category=implementation&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, queue, linked-list, design]
---
# 7. Implement queue using Linkedlist

← [Implement stack using Linkedlist](06-implement-stack-using-linkedlist.md) · [Part 23 index](README.md) · Next → [Balanced Paranthesis](08-balanced-parenthesis.md)

> [!abstract] Problem at a glance
> **Task:** Build a FIFO queue on a singly linked list with O(1) enqueue and dequeue.
> **Key insight:** Keep **two** pointers: dequeue at `head`, enqueue after `tail`. In a singly linked list, removal is O(1) only at the head and insertion is O(1) at either end (with a tail pointer). That forces head = front and tail = back.
> **Difficulty:** Easy · **Pattern:** Linked list with head + tail · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/implement-queue-using-linked-list/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/implement-queue-using-linkedlist?category=implementation&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Head = front, tail = back](#3-head--front-tail--back) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement a queue using a singly linked list with `push(x)`, `pop()` (front or `-1`), `peek()` (front or `-1`), `size()` and `isEmpty()`.

| Input | Output | Why |
|---|---|---|
| `push 2, push 3, pop, peek` | `2, 3` |  |

**Constraints:** Up to `10⁵` operations.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Head = front, tail = back | enqueue: tail.next = node; dequeue: head = head.next | O(1) per op | O(n) |

> [!tip] Interview angle
> The bug they're looking for: after popping the last node, `tail` still points to the freed node. Reset `tail = null` when `head` becomes null.

---

## 3. Head = front, tail = back

**Intuition.** Enqueue links the new node after `tail` (or sets both pointers if empty). Dequeue advances `head`. When the queue becomes empty, clear `tail` too.

**Algorithm**

1. `push(x)`: `n = Node(x)`; if empty `head = tail = n` else `tail.next = n; tail = n`.
2. `pop()`: if empty −1; `v = head.val; head = head.next`; if `head` null, `tail = null`.
3. `peek()`: `head.val` or −1.

**Dry run** — push 2, push 3 → 2→3 (head 2, tail 3). pop → 2. pop → 3, head=null → tail=null. push 5 → head=tail=5.

**C++**
```cpp
class LinkedQueue {
    struct Node { int val; Node* next; Node(int v) : val(v), next(nullptr) {} };
    Node *head = nullptr, *tail = nullptr; int cnt = 0;
public:
    ~LinkedQueue() { while (head) { Node* t = head; head = head->next; delete t; } }
    void push(int x) {
        Node* n = new Node(x);
        if (!tail) head = tail = n;
        else { tail->next = n; tail = n; }
        cnt++;
    }
    int pop() {
        if (!head) return -1;
        Node* t = head; int v = t->val;
        head = head->next;
        if (!head) tail = nullptr;
        delete t; cnt--;
        return v;
    }
    int peek() { return head ? head->val : -1; }
    int size() { return cnt; }
    bool isEmpty() { return head == nullptr; }
};
```

**Java**
```java
static class LinkedQueue {
    private static class Node { int val; Node next; Node(int v) { val = v; } }
    private Node head, tail; private int cnt;
    void push(int x) {
        Node n = new Node(x);
        if (tail == null) head = tail = n;
        else { tail.next = n; tail = n; }
        cnt++;
    }
    int pop() {
        if (head == null) return -1;
        int v = head.val; head = head.next;
        if (head == null) tail = null;
        cnt--;
        return v;
    }
    int peek() { return head == null ? -1 : head.val; }
    int size() { return cnt; }
    boolean isEmpty() { return head == null; }
}
```

**Python**
```python
class LinkedQueue:
    class Node:
        __slots__ = ("val", "next")
        def __init__(self, val):
            self.val, self.next = val, None
    def __init__(self):
        self.head = self.tail = None
        self.cnt = 0
    def push(self, x):
        n = self.Node(x)
        if self.tail is None:
            self.head = self.tail = n
        else:
            self.tail.next = n
            self.tail = n
        self.cnt += 1
    def pop(self):
        if self.head is None:
            return -1
        v = self.head.val
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.cnt -= 1
        return v
    def peek(self):
        return self.head.val if self.head else -1
    def size(self):
        return self.cnt
    def isEmpty(self):
        return self.head is None
```

**Complexity:** time **O(1) per op**, space **O(n)** — one pointer update at each end.

---

## Edge cases

- Pop the only element: both pointers become null.
- Push into an empty queue sets both pointers.

---

## Common mistakes

1. Not resetting `tail` after the last pop, so the next push links onto a dead node.
2. Dequeuing at the tail, which is O(n) in a singly linked list.
3. Forgetting the empty-queue branch in push.

---

## Follow-ups

1. Circular linked list with only a tail pointer?
2. Sentinel (dummy) head?

<details><summary>Answer sketches</summary>

**#1:** `tail.next` is the head: enqueue after tail and advance it; dequeue `tail.next`.

**#2:** Removes the empty-case branches: head is always the dummy; front is `dummy.next`.
</details>

---

## Flashcards

**Linked-list queue: which end is the front?** #flashcard
The head (O(1) delete); enqueue after the tail.

**Classic linked-list queue bug?** #flashcard
Not nulling `tail` when the last node is dequeued.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
