---
module: striver-a2z/19-linked-list
lesson: 29
topic: Add One to a Number Represented by LL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/add-one-to-a-number-represented-by-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, math, recursion]
---
# 29. Add One to a Number Represented by LL

← [Reverse a LL](28-reverse-a-ll.md) · [Part 19 index](README.md) · Next → [Find Middle of Linked List](30-find-middle-of-linked-list.md)

> [!abstract] Problem at a glance
> **Task:** Digits stored most-significant first; add 1 and return the head.
> **Key insight:** The carry starts at the **tail** but the list only goes forward. Either reverse → add → reverse, or recurse to the end and return the carry upward. All-9s needs a new head.
> **Difficulty:** Medium · **Pattern:** Recursion returns carry
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/add-one-to-a-number-represented-by-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Reverse, add, reverse](#3-reverse-add-reverse) · [4. Recursion returns carry](#4-recursion-returns-carry) · [5. Rightmost non-9](#5-rightmost-non-9) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a linked list representing a non-negative integer (most significant digit first, no leading zeros), add 1 to it and return the head.

| Input | Output | Why |
|---|---|---|
| `1→2→3` | `1→2→4` |  |
| `9→9` | `1→0→0` | new head |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Reverse, add, reverse | reverse; propagate carry; reverse back | O(n) | O(1) |
| Recursion returns carry | carry = helper(next); val += carry | O(n) | O(n) stack |
| Rightmost non-9 | find last digit ≠ 9; ++ it; zero the rest | O(n) | O(1) |

> [!tip] Interview angle
> Three answers in increasing elegance: reverse twice (O(1) space), recursion (O(n) stack), and the "last non-9" trick — find the rightmost digit ≠ 9, increment it and zero everything after.

---

## 3. Reverse, add, reverse

**Intuition.** Reversal turns this into Add Two Numbers with a single 1.

```python
def add_one_reverse(head):
    def rev(h):
        p = None
        while h:
            h.next, p, h = p, h, h.next
        return p
    head = rev(head)
    cur, carry = head, 1
    while cur and carry:
        s = cur.val + carry
        cur.val, carry = s % 10, s // 10
        last, cur = cur, cur.next
    head = rev(head)
    return ListNode(1, head) if carry else head
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Recursion returns carry

**Intuition.** The recursion unwinds from the tail — exactly the order addition needs.

```python
def add_one_rec(head):
    def go(node):
        if not node:
            return 1
        s = node.val + go(node.next)
        node.val = s % 10
        return s // 10
    return ListNode(1, head) if go(head) else head
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## 5. Rightmost non-9

**Intuition.** Adding 1 only changes the suffix of trailing 9s and the digit before it. A dummy 0 in front handles all-9s.

**Dry run** — 1→9→9: last non-9 is 1 → 2, then 9s → 0: 2→0→0. 9→9: only the dummy is non-9 → 1→0→0.

**C++**
```cpp
ListNode* addOne(ListNode* head) {
    ListNode* dummy = new ListNode(0, head);
    ListNode* last = dummy;
    for (ListNode* c = head; c; c = c->next) if (c->val != 9) last = c;
    last->val++;
    for (ListNode* c = last->next; c; c = c->next) c->val = 0;
    if (dummy->val) return dummy;
    delete dummy;
    return head;
}
```

**Java**
```java
static ListNode addOne(ListNode head) {
    ListNode dummy = new ListNode(0, head), last = dummy;
    for (ListNode c = head; c != null; c = c.next) if (c.val != 9) last = c;
    last.val++;
    for (ListNode c = last.next; c != null; c = c.next) c.val = 0;
    return dummy.val != 0 ? dummy : head;
}
```

**Python**
```python
def add_one(head):
    dummy = ListNode(0, head)
    last = dummy
    cur = head
    while cur:
        if cur.val != 9:
            last = cur
        cur = cur.next
    last.val += 1
    cur = last.next
    while cur:
        cur.val = 0
        cur = cur.next
    return dummy if dummy.val else head
```

**Complexity:** time **O(n)**, space **O(1)** — two short passes, no stack, no reversal.

---

## Edge cases

- All 9s → length grows.
- Single digit 9.
- Last digit not 9 (no carry).

---

## Common mistakes

1. Forgetting the new head on overflow.
2. Recursive version: 10⁵ deep overflows Python's stack.

---

## Follow-ups

1. Add two forward-order numbers (LC 445).

<details><summary>Answer sketches</summary>

**#1:** Stacks or reverse both, add, reverse.
</details>

---

## Flashcards

**O(1)-space add-one without reversal?** #flashcard
Find the rightmost non-9 (dummy 0 in front), increment it, zero the rest.

**Why does recursion fit add-one?** #flashcard
It processes nodes tail-first on unwind — the order carries propagate.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
