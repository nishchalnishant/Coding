---
module: striver/19-linked-list
lesson: 22
topic: Insert Before Given Node in DLL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/insert-before-given-node-in-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, doubly-linked-list, insertion]
---
# 22. Insert Before Given Node in DLL

← [Insert Node Before Kth Node in DLL](21-insert-node-before-kth-node-in-dll.md) · [Part 19 index](README.md) · Next → [Reverse a Doubly Linked List](23-reverse-a-doubly-linked-list.md)

> [!abstract] Problem at a glance
> **Task:** Given a pointer to a node (not the head), insert `x` immediately before it.
> **Key insight:** No head needed: `node.prev` exists (not the head), so `p = node.prev; new = Node(x, next = node, prev = p); p.next = new; node.prev = new`. O(1).
> **Difficulty:** Easy · **Pattern:** Insert before a known node
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insert-before-given-node-in-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Splice between prev and node](#3-splice-between-prev-and-node) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

You are given a pointer `node` to a node of a doubly linked list (not the head) and a value `x`. Insert a node with value `x` before `node`.

| Input | Output | Why |
|---|---|---|
| `1⇄2⇄3, node = 2, x = 9` | `1⇄9⇄2⇄3` |  |

**Constraints:** `2 ≤ n ≤ 10⁵`; `node` is not the head.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Splice between prev and node | 4 link updates | O(1) | O(1) |

> [!tip] Interview angle
> The guarantee "not the head" is what makes this void: inserting before the head would change the head, which the caller couldn't see.

---

## 3. Splice between prev and node

**Intuition.** Build the node already pointing at both neighbours, then point both neighbours at it.

**C++**
```cpp
void insertBeforeNode(Node* node, int x) {
    Node* p = node->prev;
    Node* nw = new Node(x, node, p);
    p->next = nw;
    node->prev = nw;
}
```

**Java**
```java
static void insertBeforeNode(Node node, int x) {
    Node p = node.prev;
    Node nw = new Node(x, node, p);
    p.next = nw;
    node.prev = nw;
}
```

**Python**
```python
def insert_before_node(node, x):
    p = node.prev
    new = Node(x, node, p)
    p.next = new
    node.prev = new
```

**Complexity:** time **O(1)**, space **O(1)** — no traversal.

---

## Edge cases

- Node is the tail.

---

## Common mistakes

1. Updating `node.prev` first, then reading it as the predecessor.

---

## Follow-ups

1. Allow node == head.

<details><summary>Answer sketches</summary>

**#1:** Return the new head, or use a sentinel head so a predecessor always exists.
</details>

---

## Flashcards

**Why must the given node not be the head in a void insert-before?** #flashcard
The head would change and the caller couldn't observe it.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
