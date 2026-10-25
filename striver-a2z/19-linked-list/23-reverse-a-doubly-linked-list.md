---
module: striver-a2z/19-linked-list
lesson: 23
topic: Reverse a Doubly Linked List
difficulty: Easy
source: https://takeuforward.org/learning/dsa/reverse-a-doubly-linked-list?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, doubly-linked-list, reversal]
---
# 23. Reverse a Doubly Linked List

← [Insert Before Given Node in DLL](22-insert-before-given-node-in-dll.md) · [Part 19 index](README.md) · Next → [Add Two Numbers in LL](24-add-two-numbers-in-ll.md)

> [!abstract] Problem at a glance
> **Task:** Reverse the DLL in place; return the new head.
> **Key insight:** Swap `prev` and `next` in every node. After the swap, the old `next` is in `prev`, so advance with `cur = cur.prev`. The last node visited is the new head.
> **Difficulty:** Easy · **Pattern:** Swap links
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-a-doubly-linked-list?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Stack of values](#3-stack-of-values) · [4. Swap prev/next in place](#4-swap-prevnext-in-place) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a doubly linked list, reverse it in place and return the new head.

| Input | Output | Why |
|---|---|---|
| `1⇄2⇄3` | `3⇄2⇄1` |  |
| `null` | `null` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Stack of values | push all values; pop back in order | O(n) | O(n) |
| Swap prev/next in place | swap; advance via cur.prev; last visited = head | O(n) | O(1) |

> [!tip] Interview angle
> Lead with the brute force (stack of values, rewrite) to show you can, then do the O(1)-space swap. Name the trick: "after swapping, `prev` is my forward pointer."

---

## 3. Stack of values

**Intuition.** Reverses data, not links — fine if values are cheap to copy.

```python
def reverse_dll_stack(head):
    st, cur = [], head
    while cur:
        st.append(cur.val)
        cur = cur.next
    cur = head
    while cur:
        cur.val = st.pop()
        cur = cur.next
    return head
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Swap prev/next in place

**Intuition.** Reversing a DLL means every node's `next` and `prev` trade places.

**Dry run** — 1⇄2⇄3: at 1 swap → next=None, prev=2; move to 2: swap → next=1, prev=3; move to 3: swap → next=2, prev=None; head=3.

**C++**
```cpp
Node* reverseDLL(Node* head) {
    Node *cur = head, *last = nullptr;
    while (cur) {
        swap(cur->prev, cur->next);
        last = cur;
        cur = cur->prev;
    }
    return last;
}
```

**Java**
```java
static Node reverseDLL(Node head) {
    Node cur = head, last = null;
    while (cur != null) {
        Node t = cur.prev;
        cur.prev = cur.next;
        cur.next = t;
        last = cur;
        cur = cur.prev;
    }
    return last;
}
```

**Python**
```python
def reverse_dll(head):
    cur, last = head, None
    while cur:
        cur.prev, cur.next = cur.next, cur.prev
        last = cur
        cur = cur.prev
    return last
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, O(1) extra.

---

## Edge cases

- Empty.
- Single node.

---

## Common mistakes

1. Advancing with `cur.next` after the swap — goes backwards and loops.
2. Returning `cur` (null) instead of the last visited node.

---

## Follow-ups

1. Reverse a singly list.

<details><summary>Answer sketches</summary>

**#1:** Three pointers prev/cur/next — see Logic Building.
</details>

---

## Flashcards

**After swapping links in DLL reverse, how to advance?** #flashcard
`cur = cur.prev` (holds the old next).

**New head after DLL reverse?** #flashcard
The last non-null node visited.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
