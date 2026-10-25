---
module: striver-a2z/19-linked-list
lesson: 24
topic: Add Two Numbers in LL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/add-two-numbers-in-ll?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, math, dummy-node]
---
# 24. Add Two Numbers in LL

← [Reverse a Doubly Linked List](23-reverse-a-doubly-linked-list.md) · [Part 19 index](README.md) · Next → [Segregate Odd and Even Nodes in LL](25-segregate-odd-and-even-nodes-in-ll.md)

> [!abstract] Problem at a glance
> **Task:** Two non-negative numbers are stored as digit lists, least significant digit first. Return their sum as a list in the same form.
> **Key insight:** Grade-school addition read left to right: `s = d1 + d2 + carry`, emit `s % 10`, carry `s // 10`. Loop while **either list or the carry** remains.
> **Difficulty:** Medium · **Pattern:** Dummy + carry · **Also on:** 2
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/add-two-numbers-in-ll?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Simultaneous walk with carry](#3-simultaneous-walk-with-carry) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two non-empty linked lists `l1`, `l2` representing non-negative integers with digits in reverse order, return the sum as a linked list in reverse order.

| Input | Output | Why |
|---|---|---|
| `2→4→3 + 5→6→4` | `7→0→8` | 342 + 465 = 807 |
| `9→9→9→9 + 9→9` | `8→9→0→0→1` | final carry |

**Constraints:** Up to 100 nodes each; no leading zeros except 0 itself.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Simultaneous walk with carry | while l1 or l2 or carry: s = …; tail.next = node(s % 10) | O(max(m, n)) | O(1) extra (output aside) |

> [!tip] Interview angle
> Converting to integers overflows (100 digits) — say so and reject it. The single loop `while l1 or l2 or carry` handles unequal lengths and the final carry in one place.

---

## 3. Simultaneous walk with carry

**Intuition.** Missing digits count as 0; the carry is at most 1.

**Dry run** — 2+5=7 c0 · 4+6=10 → 0 c1 · 3+4+1=8 → 7→0→8.

**C++**
```cpp
ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
    ListNode dummy, *tail = &dummy;
    int carry = 0;
    while (l1 || l2 || carry) {
        int s = carry;
        if (l1) { s += l1->val; l1 = l1->next; }
        if (l2) { s += l2->val; l2 = l2->next; }
        carry = s / 10;
        tail = tail->next = new ListNode(s % 10);
    }
    return dummy.next;
}
```

**Java**
```java
static ListNode addTwoNumbers(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(), tail = dummy;
    int carry = 0;
    while (l1 != null || l2 != null || carry != 0) {
        int s = carry;
        if (l1 != null) { s += l1.val; l1 = l1.next; }
        if (l2 != null) { s += l2.val; l2 = l2.next; }
        carry = s / 10;
        tail = tail.next = new ListNode(s % 10);
    }
    return dummy.next;
}
```

**Python**
```python
def add_two_numbers(l1, l2):
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:
        s = carry
        if l1:
            s += l1.val
            l1 = l1.next
        if l2:
            s += l2.val
            l2 = l2.next
        carry, d = divmod(s, 10)
        tail.next = ListNode(d)
        tail = tail.next
    return dummy.next
```

**Complexity:** time **O(max(m, n))**, space **O(1) extra (output aside)** — one node per output digit.

---

## Edge cases

- Different lengths.
- Final carry creates a new digit.
- Both are 0.

---

## Common mistakes

1. Dropping the final carry (999 + 1).
2. Converting to int — overflows in C++/Java.

---

## Follow-ups

1. Digits stored most-significant first (LC 445).
2. Add one to a number (forward order).

<details><summary>Answer sketches</summary>

**#1:** Reverse both, add, reverse result — or push digits onto two stacks.

**#2:** See FAQs: recursion returns carry.
</details>

---

## Flashcards

**Loop condition for add-two-numbers?** #flashcard
`while l1 or l2 or carry`.

**Why not convert to integers?** #flashcard
Up to 100 digits — overflows fixed-width ints.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
