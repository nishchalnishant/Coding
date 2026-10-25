---
module: striver-a2z/19-linked-list
lesson: 7
topic: Delete the Element with Value X
difficulty: Easy
source: https://takeuforward.org/learning/dsa/delete-the-element-with-value-x?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, deletion, dummy-node]
---
# 7. Delete the Element with Value X

← [Deletion of the Kth Element of LL](06-deletion-of-the-kth-element-of-ll.md) · [Part 19 index](README.md) · Next → [Insertion at the Head of LL](08-insertion-at-the-head-of-ll.md)

> [!abstract] Problem at a glance
> **Task:** Delete the first node whose value equals `x`; unchanged if `x` is absent.
> **Key insight:** Same bypass as deleting by position, but the stop condition is `prev.next.val == x`. A dummy node covers the case where the head holds `x`.
> **Difficulty:** Easy · **Pattern:** Predecessor + bypass
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/delete-the-element-with-value-x?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Dummy + search predecessor](#3-dummy--search-predecessor) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list and a value `x`, remove the first node with value `x` and return the head.

| Input | Output | Why |
|---|---|---|
| `1→2→3→2, x = 2` | `1→3→2` | only the first 2 |
| `1→2→3, x = 9` | `1→2→3` | absent |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Dummy + search predecessor | prev from dummy until prev.next.val == x; bypass | O(n) | O(1) |

> [!tip] Interview angle
> Ask: first occurrence or all? All occurrences is LC 203 — the same loop without `break`, and you must **not** advance `prev` after a deletion.

---

## 3. Dummy + search predecessor

**Intuition.** Scan with `prev` one step behind the candidate. When `prev.next.val == x`, unlink it and stop.

**C++**
```cpp
ListNode* deleteValue(ListNode* head, int x) {
    ListNode dummy(0, head);
    for (ListNode* prev = &dummy; prev->next; prev = prev->next) {
        if (prev->next->val == x) {
            ListNode* del = prev->next;
            prev->next = del->next;
            delete del;
            break;
        }
    }
    return dummy.next;
}
```

**Java**
```java
static ListNode deleteValue(ListNode head, int x) {
    ListNode dummy = new ListNode(0, head);
    for (ListNode prev = dummy; prev.next != null; prev = prev.next) {
        if (prev.next.val == x) { prev.next = prev.next.next; break; }
    }
    return dummy.next;
}
```

**Python**
```python
def delete_value(head, x):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next:
        if prev.next.val == x:
            prev.next = prev.next.next
            break
        prev = prev.next
    return dummy.next
```

**Complexity:** time **O(n)**, space **O(1)** — one scan.

---

## Edge cases

- `x` at the head.
- `x` at the tail.
- `x` absent.
- Duplicates — only the first goes.

---

## Common mistakes

1. Comparing `cur.val` with no predecessor kept.
2. For delete-all: advancing `prev` after a removal skips consecutive matches.

---

## Follow-ups

1. Remove all nodes equal to x (LC 203).

<details><summary>Answer sketches</summary>

**#1:** Drop the `break`; advance `prev` only when no deletion happened.
</details>

---

## Flashcards

**Delete-first vs delete-all difference?** #flashcard
Delete-all: no break, and don't advance prev after unlinking.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
