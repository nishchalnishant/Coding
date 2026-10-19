---
module: striver/19-linked-list
lesson: 16
topic: Delete Tail of DLL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/delete-tail-of-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, doubly-linked-list, deletion]
---
# 16. Delete Tail of DLL

← [Delete Head of DLL](15-delete-head-of-dll.md) · [Part 19 index](README.md) · Next → [Delete Kth Element of DLL](17-delete-kth-element-of-dll.md)

> [!abstract] Problem at a glance
> **Task:** Remove the last node; return the head.
> **Key insight:** Walk to the tail itself (not its predecessor — `tail.prev` gives that), then `tail.prev.next = null`.
> **Difficulty:** Easy · **Pattern:** Walk to tail
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/delete-tail-of-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Walk to tail, cut via prev](#3-walk-to-tail-cut-via-prev) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a doubly linked list, delete the last node and return the head.

| Input | Output | Why |
|---|---|---|
| `1⇄2⇄3` | `1⇄2` |  |
| `5` | `null` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Walk to tail, cut via prev | tail.prev.next = null | O(n) | O(1) |

> [!tip] Interview angle
> With a stored tail pointer this is O(1) — that's why a DLL makes a deque: both ends pop in O(1), which a singly list can't do at the tail.

---

## 3. Walk to tail, cut via prev

**Intuition.** The tail knows its predecessor, so stop **on** the tail.

**C++**
```cpp
Node* deleteTail(Node* head) {
    if (!head || !head->next) { delete head; return nullptr; }
    Node* tail = head;
    while (tail->next) tail = tail->next;
    tail->prev->next = nullptr;
    delete tail;
    return head;
}
```

**Java**
```java
static Node deleteTail(Node head) {
    if (head == null || head.next == null) return null;
    Node tail = head;
    while (tail.next != null) tail = tail.next;
    tail.prev.next = null;
    tail.prev = null;
    return head;
}
```

**Python**
```python
def delete_tail(head):
    if not head or not head.next:
        return None
    tail = head
    while tail.next:
        tail = tail.next
    tail.prev.next = None
    tail.prev = None
    return head
```

**Complexity:** time **O(n)**, space **O(1)** — one walk; O(1) with a tail pointer.

---

## Edge cases

- Empty list.
- Single node.

---

## Common mistakes

1. Single node: `tail.prev` is null → crash. Handle it first.

---

## Follow-ups

1. O(1) tail delete.

<details><summary>Answer sketches</summary>

**#1:** Maintain a `tail` field; `tail = tail.prev; tail.next = null`.
</details>

---

## Flashcards

**Why can a DLL pop its tail in O(1) and a singly list can't?** #flashcard
The tail's `prev` gives the new tail without a walk (given a tail pointer).

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
