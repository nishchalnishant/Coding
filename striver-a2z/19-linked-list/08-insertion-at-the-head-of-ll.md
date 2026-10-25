---
module: striver-a2z/19-linked-list
lesson: 8
topic: Insertion at the Head of LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/insertion-at-the-head-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, insertion]
---
# 8. Insertion at the Head of LL

← [Delete the Element with Value X](07-delete-the-element-with-value-x.md) · [Part 19 index](README.md) · Next → [Insertion at the Tail of LL](09-insertion-at-the-tail-of-ll.md)

> [!abstract] Problem at a glance
> **Task:** Insert a new node with value `x` before the head; return the new head.
> **Key insight:** `return new Node(x, head)` — one allocation, one pointer. Works for an empty list too.
> **Difficulty:** Easy · **Pattern:** Head update
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insertion-at-the-head-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. New node points at old head](#3-new-node-points-at-old-head) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list and a value `x`, insert `x` at the front and return the new head.

| Input | Output | Why |
|---|---|---|
| `2→3, x = 1` | `1→2→3` |  |
| `null, x = 5` | `5` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| New node points at old head | node(x).next = head; return node | O(1) | O(1) |

> [!tip] Interview angle
> O(1) — this is how a linked-list stack pushes. Set the new node's `next` before moving the head.

---

## 3. New node points at old head

**Intuition.** Create the node with `next = head`; it becomes the head.

**C++**
```cpp
ListNode* insertHead(ListNode* head, int x) {
    return new ListNode(x, head);
}
```

**Java**
```java
static ListNode insertHead(ListNode head, int x) {
    return new ListNode(x, head);
}
```

**Python**
```python
def insert_head(head, x):
    return ListNode(x, head)
```

**Complexity:** time **O(1)**, space **O(1)** — constant pointer work.

---

## Edge cases

- Empty list → single node.

---

## Common mistakes

1. `head = node; node.next = head` — order reversed creates a self-loop.

---

## Follow-ups

1. Implement a stack with a linked list.

<details><summary>Answer sketches</summary>

**#1:** push = insert at head, pop = delete head; both O(1).
</details>

---

## Flashcards

**Insert at head in one line?** #flashcard
`return new Node(x, head)`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
