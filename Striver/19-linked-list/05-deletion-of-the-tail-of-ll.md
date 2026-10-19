---
module: striver/19-linked-list
lesson: 5
topic: Deletion of the Tail of LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/deletion-of-the-tail-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, deletion]
---
# 5. Deletion of the Tail of LL

← [Deletion of the Head of LL](04-deletion-of-the-head-of-ll.md) · [Part 19 index](README.md) · Next → [Deletion of the Kth Element of LL](06-deletion-of-the-kth-element-of-ll.md)

> [!abstract] Problem at a glance
> **Task:** Remove the last node and return the head.
> **Key insight:** Stop at the **second-to-last** node (`cur.next.next == null`) and set `cur.next = null`. Lists of length 0 or 1 become empty.
> **Difficulty:** Easy · **Pattern:** Stop one before
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/deletion-of-the-tail-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Walk to the second-last node](#3-walk-to-the-second-last-node) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list, delete its last node and return the head.

| Input | Output | Why |
|---|---|---|
| `1 → 2 → 3` | `1 → 2` |  |
| `7` | `null` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Walk to the second-last node | while cur.next.next: cur = cur.next; cur.next = null | O(n) | O(1) |

> [!tip] Interview angle
> Tests the "stop one node early" habit — to remove a node in a singly list you need its predecessor. O(n) because there is no back pointer; a DLL with a tail pointer makes it O(1).

---

## 3. Walk to the second-last node

**Intuition.** The tail has no back-link, so reach its predecessor by checking two nodes ahead. Handle `n ≤ 1` first so `cur.next.next` is safe.

**Algorithm**

1. If `head` or `head.next` is null → return null.
2. `cur = head`; while `cur.next.next`: advance.
3. Free `cur.next`; set `cur.next = null`.

**C++**
```cpp
ListNode* deleteTail(ListNode* head) {
    if (!head || !head->next) { delete head; return nullptr; }
    ListNode* cur = head;
    while (cur->next->next) cur = cur->next;
    delete cur->next;
    cur->next = nullptr;
    return head;
}
```

**Java**
```java
static ListNode deleteTail(ListNode head) {
    if (head == null || head.next == null) return null;
    ListNode cur = head;
    while (cur.next.next != null) cur = cur.next;
    cur.next = null;
    return head;
}
```

**Python**
```python
def delete_tail(head):
    if not head or not head.next:
        return None
    cur = head
    while cur.next.next:
        cur = cur.next
    cur.next = None
    return head
```

**Complexity:** time **O(n)**, space **O(1)** — one walk to the end.

---

## Edge cases

- Empty → null.
- One node → null.
- Two nodes → head only.

---

## Common mistakes

1. Walking to the tail itself — then you can't unlink it.
2. Missing the single-node case → null dereference on `cur.next.next`.

---

## Follow-ups

1. O(1) tail delete?

<details><summary>Answer sketches</summary>

**#1:** Doubly linked list with a tail pointer: tail = tail.prev; tail.next = null.
</details>

---

## Flashcards

**Loop to reach the second-last node?** #flashcard
`while cur.next.next:`

**Why O(n) in a singly list?** #flashcard
Need the predecessor; no back pointer.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
