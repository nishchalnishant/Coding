---
module: striver-a2z/19-linked-list
lesson: 20
topic: Insert Node Before Tail in DLL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/insert-node-before-tail-in-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, doubly-linked-list, insertion]
---
# 20. Insert Node Before Tail in DLL

← [Insert Node Before Head in DLL](19-insert-node-before-head-in-dll.md) · [Part 19 index](README.md) · Next → [Insert Node Before Kth Node in DLL](21-insert-node-before-kth-node-in-dll.md)

> [!abstract] Problem at a glance
> **Task:** Insert `x` immediately before the last node (the new node becomes the second-last). Empty list → just `x`.
> **Key insight:** Walk to the tail; then the generic "insert before node `t`": `node = Node(x, next = t, prev = t.prev)`, `t.prev.next = node` (or new head), `t.prev = node`.
> **Difficulty:** Easy · **Pattern:** Insert before a known node
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insert-node-before-tail-in-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Walk to tail + insert before](#3-walk-to-tail--insert-before) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a doubly linked list and a value `x`, insert a node with value `x` before the tail and return the head. If the list has one node, `x` becomes the head.

| Input | Output | Why |
|---|---|---|
| `1⇄2⇄3, x = 9` | `1⇄2⇄9⇄3` |  |
| `5, x = 1` | `1⇄5` | tail is also head |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Walk to tail + insert before | node(next = t, prev = t.prev); fix both neighbours | O(n) | O(1) |

> [!tip] Interview angle
> Write a helper `insertBefore(t, x)` once and reuse it for the next three problems — interviewers like seeing the shared primitive.

---

## 3. Walk to tail + insert before

**Intuition.** Four links: new node's two, plus `t.prev.next` and `t.prev`. If `t` is the head, the new node becomes the head.

**C++**
```cpp
Node* insertBeforeTail(Node* head, int x) {
    if (!head) return new Node(x);
    Node* t = head;
    while (t->next) t = t->next;
    Node* node = new Node(x, t, t->prev);
    if (t->prev) t->prev->next = node; else head = node;
    t->prev = node;
    return head;
}
```

**Java**
```java
static Node insertBeforeTail(Node head, int x) {
    if (head == null) return new Node(x);
    Node t = head;
    while (t.next != null) t = t.next;
    Node node = new Node(x, t, t.prev);
    if (t.prev != null) t.prev.next = node; else head = node;
    t.prev = node;
    return head;
}
```

**Python**
```python
def insert_before_tail(head, x):
    if not head:
        return Node(x)
    t = head
    while t.next:
        t = t.next
    node = Node(x, t, t.prev)
    if t.prev:
        t.prev.next = node
    else:
        head = node
    t.prev = node
    return head
```

**Complexity:** time **O(n)**, space **O(1)** — one walk.

---

## Edge cases

- Empty list.
- Single node (tail is head).

---

## Common mistakes

1. Setting `t.prev = node` before reading `t.prev` for the new node.

---

## Follow-ups

1. Insert after the tail (append).

<details><summary>Answer sketches</summary>

**#1:** `node.prev = tail; tail.next = node`.
</details>

---

## Flashcards

**Four links when inserting node before t in a DLL?** #flashcard
`node.next = t`, `node.prev = t.prev`, `t.prev.next = node` (or head), `t.prev = node`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
