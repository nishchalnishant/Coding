---
module: striver/19-linked-list
lesson: 15
topic: Delete Head of DLL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/delete-head-of-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, doubly-linked-list, deletion]
---
# 15. Delete Head of DLL

← [Convert Array to DLL](14-convert-array-to-dll.md) · [Part 19 index](README.md) · Next → [Delete Tail of DLL](16-delete-tail-of-dll.md)

> [!abstract] Problem at a glance
> **Task:** Remove the first node; return the new head.
> **Key insight:** `head = head.next`, then **clear the new head's `prev`** — the step singly lists don't have.
> **Difficulty:** Easy · **Pattern:** Head update
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/delete-head-of-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Advance + clear prev](#3-advance--clear-prev) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a doubly linked list, delete the head node and return the new head.

| Input | Output | Why |
|---|---|---|
| `1⇄2⇄3` | `2⇄3` |  |
| `5` | `null` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Advance + clear prev | head = head.next; head.prev = null | O(1) | O(1) |

> [!tip] Interview angle
> The dangling `prev` is the bug the interviewer is looking for: the old head is gone but `newHead.prev` still points at it.

---

## 3. Advance + clear prev

**Intuition.** Move the head, then sever the backward link (also unlink the old node's `next` for hygiene).

**C++**
```cpp
Node* deleteHead(Node* head) {
    if (!head) return nullptr;
    Node* newHead = head->next;
    if (newHead) newHead->prev = nullptr;
    delete head;
    return newHead;
}
```

**Java**
```java
static Node deleteHead(Node head) {
    if (head == null || head.next == null) return null;
    Node newHead = head.next;
    newHead.prev = null;
    head.next = null;
    return newHead;
}
```

**Python**
```python
def delete_head(head):
    if not head or not head.next:
        return None
    new_head = head.next
    new_head.prev = None
    head.next = None
    return new_head
```

**Complexity:** time **O(1)**, space **O(1)** — constant work.

---

## Edge cases

- Empty list.
- Single node → null.

---

## Common mistakes

1. Leaving `newHead.prev` pointing at the deleted node.

---

## Follow-ups

1. Deque pop-front with a DLL.

<details><summary>Answer sketches</summary>

**#1:** Exactly this, plus update `tail = null` when the list empties.
</details>

---

## Flashcards

**Extra step vs singly delete-head?** #flashcard
Set `newHead.prev = null`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
