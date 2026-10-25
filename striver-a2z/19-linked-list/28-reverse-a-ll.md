---
module: striver-a2z/19-linked-list
lesson: 28
topic: Reverse a LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/reverse-a-ll?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, reversal, recursion]
---
# 28. Reverse a LL

← [Remove Nth Node from the Back of the LL](27-remove-nth-node-from-the-back-of-the-ll.md) · [Part 19 index](README.md) · Next → [Add One to a Number Represented by LL](29-add-one-to-a-number-represented-by-ll.md)

> [!abstract] Problem at a glance
> **Task:** Reverse a singly linked list; return the new head.
> **Key insight:** Three pointers: save `nxt = cur.next`, flip `cur.next = prev`, advance `prev = cur; cur = nxt`. `prev` ends on the new head. Recursive: reverse the rest, then `head.next.next = head; head.next = null`.
> **Difficulty:** Easy · **Pattern:** In-place reversal · **Also on:** 206
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-a-ll?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Stack of values](#3-stack-of-values) · [4. Recursive](#4-recursive) · [5. Iterative three pointers](#5-iterative-three-pointers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list, reverse the list and return the reversed list.

| Input | Output | Why |
|---|---|---|
| `1→2→3→4→5` | `5→4→3→2→1` |  |
| `null` | `null` |  |

**Constraints:** `0 ≤ n ≤ 5000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Stack of values | push values, pop back into nodes | O(n) | O(n) |
| Recursive | new_head = rev(head.next); head.next.next = head; head.next = None | O(n) | O(n) stack |
| Iterative three pointers | nxt = cur.next; cur.next = prev; prev, cur = cur, nxt | O(n) | O(1) |

> [!tip] Interview angle
> The single most reused linked-list primitive (palindrome, reorder, k-group, add-one). Be ready to write both versions cold and state the recursive one's O(n) stack.

---

## 3. Stack of values

**Intuition.** Reverses data; mention only as baseline.

```python
def reverse_stack(head):
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

## 4. Recursive

**Intuition.** Trust the recursion to reverse `head.next…`; `head.next` is now the tail of that reversed part, so hang `head` after it.

```python
def reverse_rec(head):
    if not head or not head.next:
        return head
    new_head = reverse_rec(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## 5. Iterative three pointers

**Intuition.** Flip one arrow per step; save the forward link before you lose it.

**Dry run** — prev=∅ cur=1 → 1→∅, prev=1 cur=2 → 2→1, … prev=5.

**C++**
```cpp
ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    while (head) {
        ListNode* nxt = head->next;
        head->next = prev;
        prev = head;
        head = nxt;
    }
    return prev;
}
```

**Java**
```java
static ListNode reverseList(ListNode head) {
    ListNode prev = null;
    while (head != null) {
        ListNode nxt = head.next;
        head.next = prev;
        prev = head;
        head = nxt;
    }
    return prev;
}
```

**Python**
```python
def reverse_list(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev, head = head, nxt
    return prev
```

**Complexity:** time **O(n)**, space **O(1)** — each arrow flipped once.

---

## Edge cases

- Empty.
- Single node.

---

## Common mistakes

1. Overwriting `cur.next` before saving it.
2. Recursive: forgetting `head.next = None` → 2-cycle at the end.
3. Returning `head` (now null) instead of `prev`.

---

## Follow-ups

1. Reverse between positions m and n (LC 92).
2. Reverse in groups of k.

<details><summary>Answer sketches</summary>

**#1:** Walk to m−1, reverse n−m+1 nodes, reconnect both ends.

**#2:** See FAQs (Hard).
</details>

---

## Flashcards

**Iterative reverse — 4 lines?** #flashcard
`nxt = cur.next; cur.next = prev; prev = cur; cur = nxt`.

**Recursive reverse key lines?** #flashcard
`head.next.next = head; head.next = None`.

**Return value of iterative reverse?** #flashcard
`prev`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
