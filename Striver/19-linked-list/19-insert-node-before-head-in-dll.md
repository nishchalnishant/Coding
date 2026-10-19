---
module: striver/19-linked-list
lesson: 19
topic: Insert Node Before Head in DLL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/insert-node-before-head-in-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, doubly-linked-list, insertion]
---
# 19. Insert Node Before Head in DLL

← [Removing Given Node in DLL](18-removing-given-node-in-dll.md) · [Part 19 index](README.md) · Next → [Insert Node Before Tail in DLL](20-insert-node-before-tail-in-dll.md)

> [!abstract] Problem at a glance
> **Task:** Insert `x` as the new head.
> **Key insight:** `node = Node(x, next = head)`; then `head.prev = node` if head exists. Two links instead of one.
> **Difficulty:** Easy · **Pattern:** Head update
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insert-node-before-head-in-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Link both ways](#3-link-both-ways) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a doubly linked list and a value `x`, insert a node with value `x` before the head and return the new head.

| Input | Output | Why |
|---|---|---|
| `2⇄3, x = 1` | `1⇄2⇄3` |  |
| `null, x = 5` | `5` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Link both ways | node.next = head; head.prev = node | O(1) | O(1) |

> [!tip] Interview angle
> O(1). Mention the null check on the old head — the singly version doesn't need it.

---

## 3. Link both ways

**Intuition.** New node's `prev` is null; the old head's `prev` becomes the new node.

**C++**
```cpp
Node* insertBeforeHead(Node* head, int x) {
    Node* node = new Node(x, head, nullptr);
    if (head) head->prev = node;
    return node;
}
```

**Java**
```java
static Node insertBeforeHead(Node head, int x) {
    Node node = new Node(x, head, null);
    if (head != null) head.prev = node;
    return node;
}
```

**Python**
```python
def insert_before_head(head, x):
    node = Node(x, head, None)
    if head:
        head.prev = node
    return node
```

**Complexity:** time **O(1)**, space **O(1)** — constant.

---

## Edge cases

- Empty list.

---

## Common mistakes

1. Forgetting `head.prev = node`.

---

## Follow-ups

1. Deque push-front.

<details><summary>Answer sketches</summary>

**#1:** This, plus set `tail = node` if the list was empty.
</details>

---

## Flashcards

**DLL insert at head — links touched?** #flashcard
`node.next = head`, `head.prev = node` (if head).

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
