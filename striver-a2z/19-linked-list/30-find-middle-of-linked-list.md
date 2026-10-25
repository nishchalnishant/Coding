---
module: striver-a2z/19-linked-list
lesson: 30
topic: Find Middle of Linked List
difficulty: Easy
source: https://takeuforward.org/learning/dsa/find-middle-of-linked-list?category=faqs--medium&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, fast-slow]
---
# 30. Find Middle of Linked List

← [Add One to a Number Represented by LL](29-add-one-to-a-number-represented-by-ll.md) · [Part 19 index](README.md) · Next → [Delete the Middle Node in LL](31-delete-the-middle-node-in-ll.md)

> [!abstract] Problem at a glance
> **Task:** Return the middle node; for even length, the **second** middle.
> **Key insight:** Tortoise and hare: slow moves 1, fast moves 2; when fast can't move, slow is at the middle. `while fast and fast.next` → second middle; `while fast.next and fast.next.next` → first middle.
> **Difficulty:** Easy · **Pattern:** Fast/slow pointers · **Also on:** 876
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-middle-of-linked-list?category=faqs--medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Count then walk](#3-count-then-walk) · [4. Tortoise and hare](#4-tortoise-and-hare) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list, return the middle node. If there are two middle nodes, return the second one.

| Input | Output | Why |
|---|---|---|
| `1→2→3→4→5` | `node 3` |  |
| `1→2→3→4→5→6` | `node 4` | second middle |

**Constraints:** `1 ≤ n ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Count then walk | n = length; walk n // 2 | O(n) | O(1) |
| Tortoise and hare | slow += 1, fast += 2 while fast and fast.next | O(n) | O(1) |

> [!tip] Interview angle
> Know which loop condition gives which middle — merge sort on a list needs the **first** middle (so the left half is non-empty and smaller), this problem needs the second.

---

## 3. Count then walk

**Intuition.** Two passes; index n // 2 (0-based) is the second middle for even n.

```python
def middle_count(head):
    n, cur = 0, head
    while cur:
        n += 1
        cur = cur.next
    cur = head
    for _ in range(n // 2):
        cur = cur.next
    return cur
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Tortoise and hare

**Intuition.** Fast covers twice the distance, so when it reaches the end slow has covered half.

**C++**
```cpp
ListNode* middleNode(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) { slow = slow->next; fast = fast->next->next; }
    return slow;
}
```

**Java**
```java
static ListNode middleNode(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    return slow;
}
```

**Python**
```python
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow
```

**Complexity:** time **O(n)**, space **O(1)** — one pass (n/2 iterations).

---

## Edge cases

- One node.
- Two nodes → second.

---

## Common mistakes

1. Mixing up loop conditions → wrong middle for even lengths.

---

## Follow-ups

1. First middle instead.
2. Delete the middle.

<details><summary>Answer sketches</summary>

**#1:** `while fast.next and fast.next.next`.

**#2:** Next problem — need the node before it.
</details>

---

## Flashcards

**Loop for the second middle?** #flashcard
`while fast and fast.next`.

**Loop for the first middle?** #flashcard
`while fast.next and fast.next.next`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
