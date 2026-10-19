---
module: striver/19-linked-list
lesson: 11
topic: Insertion Before the Value X in LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/insertion-before-the-value-x-in-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, insertion, dummy-node]
---
# 11. Insertion Before the Value X in LL

← [Insertion at the Kth Position of LL](10-insertion-at-the-kth-position-of-ll.md) · [Part 19 index](README.md) · Next → [Find the Length of the Linked List](12-find-the-length-of-the-linked-list.md)

> [!abstract] Problem at a glance
> **Task:** Insert `val` immediately before the first node whose value is `x`; unchanged if `x` is absent.
> **Key insight:** Search with the predecessor: stop when `prev.next.val == x`, then splice. From a dummy, `x` at the head needs no special case.
> **Difficulty:** Easy · **Pattern:** Predecessor + splice
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insertion-before-the-value-x-in-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Dummy + search predecessor](#3-dummy--search-predecessor) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `head`, a target value `x` and a new value `val`, insert `val` before the first occurrence of `x` and return the head.

| Input | Output | Why |
|---|---|---|
| `1→2→3, x = 3, val = 9` | `1→2→9→3` |  |
| `1→2→3, x = 1, val = 9` | `9→1→2→3` | new head |
| `1→2→3, x = 7` | `unchanged` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Dummy + search predecessor | prev.next.val == x → splice | O(n) | O(1) |

> [!tip] Interview angle
> Same predecessor pattern as Delete Value X — in a singly list you can only insert **after** a node you hold, so "before X" means "after X's predecessor".

---

## 3. Dummy + search predecessor

**Intuition.** Look one ahead so that when the match is found you already hold its predecessor.

**C++**
```cpp
ListNode* insertBeforeValue(ListNode* head, int x, int val) {
    ListNode dummy(0, head);
    for (ListNode* prev = &dummy; prev->next; prev = prev->next) {
        if (prev->next->val == x) { prev->next = new ListNode(val, prev->next); break; }
    }
    return dummy.next;
}
```

**Java**
```java
static ListNode insertBeforeValue(ListNode head, int x, int val) {
    ListNode dummy = new ListNode(0, head);
    for (ListNode prev = dummy; prev.next != null; prev = prev.next) {
        if (prev.next.val == x) { prev.next = new ListNode(val, prev.next); break; }
    }
    return dummy.next;
}
```

**Python**
```python
def insert_before_value(head, x, val):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next:
        if prev.next.val == x:
            prev.next = ListNode(val, prev.next)
            break
        prev = prev.next
    return dummy.next
```

**Complexity:** time **O(n)**, space **O(1)** — one scan.

---

## Edge cases

- `x` at the head.
- `x` absent.
- Duplicates of `x` — only the first.

---

## Common mistakes

1. Not breaking after inserting — loops forever if `val == x`.

---

## Follow-ups

1. Insert before a node you hold, without the head.

<details><summary>Answer sketches</summary>

**#1:** Insert a copy after it and swap values (O(1) trick).
</details>

---

## Flashcards

**How to insert before a node in a singly list?** #flashcard
Insert after its predecessor — search with prev.next.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
