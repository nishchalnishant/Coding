---
module: striver/19-linked-list
lesson: 43
topic: Delete All Occurrences of a Key in DLL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/delete-all-occurrences-of-a-key-in-dll?category=faqs--dll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, doubly-linked-list]
---
# 43. Delete All Occurrences of a Key in DLL

← [Clone a LL with Random and Next Pointer](42-clone-a-ll-with-random-and-next-pointer.md) · [Part 19 index](README.md) · Next → [Remove Duplicates from Sorted DLL](44-remove-duplicates-from-sorted-dll.md)

> [!abstract] Problem at a glance
> **Task:** Remove every node with value `key` from a doubly linked list; return the new head.
> **Key insight:** With `prev` available, deleting a node is local: `prev.next = nxt`, `nxt.prev = prev`. Only special case: deleting the head moves `head`.
> **Difficulty:** Medium · **Pattern:** DLL unlink
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/delete-all-occurrences-of-a-key-in-dll?category=faqs--dll&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Rebuild from kept values](#3-rebuild-from-kept-values) · [4. In-place unlink](#4-in-place-unlink) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a doubly linked list and an integer `key`, delete all nodes whose value is `key` and return the head.

| Input | Output | Why |
|---|---|---|
| `10⇄4⇄10⇄10⇄6⇄10, key = 10` | `4⇄6` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Rebuild from kept values | filter values; build new DLL | O(n) | O(n) |
| In-place unlink | match → link prev ⇄ next; move head if needed | O(n) | O(1) |

> [!tip] Interview angle
> Save `nxt` before unlinking. Mention fixing `nxt.prev` — forgetting it silently corrupts backward traversal, which a forward-only check won't catch.

---

## 3. Rebuild from kept values

**Intuition.** Doesn't relink original nodes; baseline.

```python
def delete_all_rebuild(head, key):
    vals = []
    while head:
        if head.val != key:
            vals.append(head.val)
        head = head.next
    dummy = t = Node()
    for v in vals:
        t.next = Node(v, None, t)
        t = t.next
    if dummy.next:
        dummy.next.prev = None
    return dummy.next
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. In-place unlink

**Intuition.** Single pass; each deletion is O(1).

**C++**
```cpp
Node* deleteAllOccurrences(Node* head, int key) {
    Node* cur = head;
    while (cur) {
        Node* nxt = cur->next;
        if (cur->val == key) {
            if (cur == head) head = nxt;
            if (cur->prev) cur->prev->next = nxt;
            if (nxt) nxt->prev = cur->prev;
            delete cur;
        }
        cur = nxt;
    }
    return head;
}
```

**Java**
```java
static Node deleteAllOccurrences(Node head, int key) {
    Node cur = head;
    while (cur != null) {
        Node nxt = cur.next;
        if (cur.val == key) {
            if (cur == head) head = nxt;
            if (cur.prev != null) cur.prev.next = nxt;
            if (nxt != null) nxt.prev = cur.prev;
        }
        cur = nxt;
    }
    return head;
}
```

**Python**
```python
def delete_all_occurrences(head, key):
    cur = head
    while cur:
        nxt = cur.next
        if cur.val == key:
            if cur is head:
                head = nxt
            if cur.prev:
                cur.prev.next = nxt
            if nxt:
                nxt.prev = cur.prev
        cur = nxt
    return head
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, O(1) per deletion.

---

## Edge cases

- All nodes match → empty.
- Key at head / tail.
- Key absent.

---

## Common mistakes

1. Not updating `nxt.prev`.
2. Reading `cur.next` after freeing `cur` (C++).

---

## Follow-ups

1. Same on a singly list (LC 203).

<details><summary>Answer sketches</summary>

**#1:** Dummy head + `prev` pointer.
</details>

---

## Flashcards

**Two links to fix when unlinking a DLL node?** #flashcard
`prev.next = next` and `next.prev = prev` (guard nulls).

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
