---
module: striver/19-linked-list
lesson: 44
topic: Remove Duplicates from Sorted DLL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/remove-duplicated-from-sorted-dll?category=faqs--dll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, doubly-linked-list]
---
# 44. Remove Duplicates from Sorted DLL

← [Delete All Occurrences of a Key in DLL](43-delete-all-occurrences-of-a-key-in-dll.md) · [Part 19 index](README.md) · Next → [Find Pairs with Given Sum in DLL](45-find-pairs-with-given-sum-in-dll.md)

> [!abstract] Problem at a glance
> **Task:** Keep one node per distinct value in a sorted doubly linked list.
> **Key insight:** Duplicates are adjacent. For each kept node, skip forward over equal values to `nxt`, then link `cur.next = nxt` and `nxt.prev = cur`.
> **Difficulty:** Medium · **Pattern:** Skip runs
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/remove-duplicated-from-sorted-dll?category=faqs--dll&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash set of seen values](#3-hash-set-of-seen-values) · [4. Skip equal run](#4-skip-equal-run) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a sorted doubly linked list, remove all duplicate nodes so each value appears once, and return the head.

| Input | Output | Why |
|---|---|---|
| `1⇄1⇄1⇄2⇄3⇄3⇄4` | `1⇄2⇄3⇄4` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash set of seen values | unlink any value already seen | O(n) | O(n) |
| Skip equal run | nxt = first node with different value; relink | O(n) | O(1) |

> [!tip] Interview angle
> One pass, two pointers. Same as LC 83 plus the `prev` fix-up.

---

## 3. Hash set of seen values

**Intuition.** Works even if unsorted.

```python
def remove_dups_set(head):
    seen, cur = set(), head
    while cur:
        nxt = cur.next
        if cur.val in seen:
            cur.prev.next = nxt
            if nxt:
                nxt.prev = cur.prev
        else:
            seen.add(cur.val)
        cur = nxt
    return head
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Skip equal run

**Intuition.** Sorted ⇒ duplicates are contiguous.

**C++**
```cpp
Node* removeDuplicates(Node* head) {
    Node* cur = head;
    while (cur) {
        Node* nxt = cur->next;
        while (nxt && nxt->val == cur->val) { Node* d = nxt; nxt = nxt->next; delete d; }
        cur->next = nxt;
        if (nxt) nxt->prev = cur;
        cur = nxt;
    }
    return head;
}
```

**Java**
```java
static Node removeDuplicates(Node head) {
    Node cur = head;
    while (cur != null) {
        Node nxt = cur.next;
        while (nxt != null && nxt.val == cur.val) nxt = nxt.next;
        cur.next = nxt;
        if (nxt != null) nxt.prev = cur;
        cur = nxt;
    }
    return head;
}
```

**Python**
```python
def remove_duplicates(head):
    cur = head
    while cur:
        nxt = cur.next
        while nxt and nxt.val == cur.val:
            nxt = nxt.next
        cur.next = nxt
        if nxt:
            nxt.prev = cur
        cur = nxt
    return head
```

**Complexity:** time **O(n)**, space **O(1)** — O(1) extra, single pass.

---

## Edge cases

- All equal → one node.
- No duplicates.
- Empty.

---

## Common mistakes

1. Forgetting `nxt.prev = cur`.

---

## Follow-ups

1. Remove all nodes that have duplicates (LC 82).

<details><summary>Answer sketches</summary>

**#1:** Dummy head; skip entire runs of length > 1.
</details>

---

## Flashcards

**Remove dups from sorted DLL in O(1)?** #flashcard
Skip the equal run, then `cur.next = nxt; nxt.prev = cur`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
