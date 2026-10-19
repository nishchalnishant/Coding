---
module: striver/19-linked-list
lesson: 9
topic: Insertion at the Tail of LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/insertion-at-the-tail-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, insertion]
---
# 9. Insertion at the Tail of LL

← [Insertion at the Head of LL](08-insertion-at-the-head-of-ll.md) · [Part 19 index](README.md) · Next → [Insertion at the Kth Position of LL](10-insertion-at-the-kth-position-of-ll.md)

> [!abstract] Problem at a glance
> **Task:** Append a node with value `x` after the last node; return the head.
> **Key insight:** Walk to the node whose `next` is null and hang the new node there. Empty list → the new node is the head. A stored tail pointer makes it O(1).
> **Difficulty:** Easy · **Pattern:** Walk to tail
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insertion-at-the-tail-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Walk to the tail](#3-walk-to-the-tail) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list and a value `x`, append `x` at the end and return the head.

| Input | Output | Why |
|---|---|---|
| `1→2, x = 3` | `1→2→3` |  |
| `null, x = 5` | `5` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Walk to the tail | while cur.next: advance; cur.next = node(x) | O(n) | O(1) |

> [!tip] Interview angle
> Note that you need `while cur.next` here (stop **on** the tail) — contrast with traversal's `while cur`. Mention that queues keep a tail pointer to make this O(1).

---

## 3. Walk to the tail

**Intuition.** Stop on the tail, link the new node.

**C++**
```cpp
ListNode* insertTail(ListNode* head, int x) {
    ListNode* node = new ListNode(x);
    if (!head) return node;
    ListNode* cur = head;
    while (cur->next) cur = cur->next;
    cur->next = node;
    return head;
}
```

**Java**
```java
static ListNode insertTail(ListNode head, int x) {
    ListNode node = new ListNode(x);
    if (head == null) return node;
    ListNode cur = head;
    while (cur.next != null) cur = cur.next;
    cur.next = node;
    return head;
}
```

**Python**
```python
def insert_tail(head, x):
    node = ListNode(x)
    if not head:
        return node
    cur = head
    while cur.next:
        cur = cur.next
    cur.next = node
    return head
```

**Complexity:** time **O(n)**, space **O(1)** — one walk.

---

## Edge cases

- Empty list.

---

## Common mistakes

1. `while cur` overshoots to null; `cur.next` then crashes.

---

## Follow-ups

1. Make appends O(1).

<details><summary>Answer sketches</summary>

**#1:** Keep a `tail` reference and update it on every append (linked-list queue).
</details>

---

## Flashcards

**Loop condition to stop on the tail?** #flashcard
`while cur.next:`

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
