---
module: striver/19-linked-list
lesson: 4
topic: Deletion of the Head of LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/deletion-of-the-head-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, deletion]
---
# 4. Deletion of the Head of LL

← [Traversal in Linked List](03-traversal-in-linked-list.md) · [Part 19 index](README.md) · Next → [Deletion of the Tail of LL](05-deletion-of-the-tail-of-ll.md)

> [!abstract] Problem at a glance
> **Task:** Remove the first node and return the new head.
> **Key insight:** The new head is `head.next`. In C++ free the old node; in Java/Python it is garbage-collected once unreferenced.
> **Difficulty:** Easy · **Pattern:** Head update
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/deletion-of-the-head-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Advance the head](#3-advance-the-head) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list, delete the head node and return the head of the remaining list.

| Input | Output | Why |
|---|---|---|
| `1 → 2 → 3` | `2 → 3` |  |
| `7` | `null` | list becomes empty |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Advance the head | tmp = head; head = head.next; free tmp | O(1) | O(1) |

> [!tip] Interview angle
> O(1) — the reason linked lists beat arrays for front deletion (array shift is O(n)). Mention returning the new head; void functions can't change the caller's pointer in C++ unless passed by reference.

---

## 3. Advance the head

**Intuition.** Guard the empty list, remember the old head, move `head` forward, release the old node.

**C++**
```cpp
ListNode* deleteHead(ListNode* head) {
    if (!head) return nullptr;
    ListNode* tmp = head;
    head = head->next;
    delete tmp;
    return head;
}
```

**Java**
```java
static ListNode deleteHead(ListNode head) {
    if (head == null) return null;
    return head.next;
}
```

**Python**
```python
def delete_head(head):
    if not head:
        return None
    return head.next
```

**Complexity:** time **O(1)**, space **O(1)** — pointer updates only.

---

## Edge cases

- Empty list → null.
- Single node → null.

---

## Common mistakes

1. Dereferencing `head.next` without the null check.
2. Freeing the node before reading `next` (C++).

---

## Follow-ups

1. Delete the head of a circular list.

<details><summary>Answer sketches</summary>

**#1:** Also update the tail's `next` to the new head — needs the tail pointer.
</details>

---

## Flashcards

**Delete head cost?** #flashcard
O(1): head = head.next.

**C++ order of operations?** #flashcard
Save tmp, advance head, then delete tmp.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
