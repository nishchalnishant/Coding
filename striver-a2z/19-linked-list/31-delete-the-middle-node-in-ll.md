---
module: striver-a2z/19-linked-list
lesson: 31
topic: Delete the Middle Node in LL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/delete-the-middle-node-in-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, fast-slow]
---
# 31. Delete the Middle Node in LL

← [Find Middle of Linked List](30-find-middle-of-linked-list.md) · [Part 19 index](README.md) · Next → [Check if LL is Palindrome or Not](32-check-if-ll-is-palindrome-or-not.md)

> [!abstract] Problem at a glance
> **Task:** Delete the node at index ⌊n/2⌋ (0-based); single node → empty list.
> **Key insight:** You need the node **before** the middle. Give fast a head start: `slow = head, fast = head.next.next`, loop `while fast and fast.next` — slow stops on the predecessor.
> **Difficulty:** Medium · **Pattern:** Fast/slow pointers · **Also on:** 2095
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/delete-the-middle-node-in-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Count then delete](#3-count-then-delete) · [4. Fast with a head start](#4-fast-with-a-head-start) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a linked list, delete the middle node (index ⌊n/2⌋, 0-based) and return the head.

| Input | Output | Why |
|---|---|---|
| `1→3→4→7→1→2→6` | `1→3→4→1→2→6` | index 3 |
| `1→2→3→4` | `1→2→4` | index 2 |
| `1` | `null` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Count then delete | walk n//2 − 1, bypass | O(n) | O(1) |
| Fast with a head start | slow = head, fast = head.next.next; bypass slow.next | O(n) | O(1) |

> [!tip] Interview angle
> Explain why the head start works: shifting fast two steps ahead makes slow lag one node behind where it would be — the predecessor.

---

## 3. Count then delete

**Intuition.** Two passes.

```python
def delete_middle_count(head):
    n, cur = 0, head
    while cur:
        n += 1
        cur = cur.next
    if n == 1:
        return None
    cur = head
    for _ in range(n // 2 - 1):
        cur = cur.next
    cur.next = cur.next.next
    return head
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Fast with a head start

**Intuition.** Same tortoise and hare, offset by one step so slow ends on the predecessor.

**C++**
```cpp
ListNode* deleteMiddle(ListNode* head) {
    if (!head || !head->next) { delete head; return nullptr; }
    ListNode *slow = head, *fast = head->next->next;
    while (fast && fast->next) { slow = slow->next; fast = fast->next->next; }
    ListNode* del = slow->next;
    slow->next = del->next;
    delete del;
    return head;
}
```

**Java**
```java
static ListNode deleteMiddle(ListNode head) {
    if (head == null || head.next == null) return null;
    ListNode slow = head, fast = head.next.next;
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    slow.next = slow.next.next;
    return head;
}
```

**Python**
```python
def delete_middle(head):
    if not head or not head.next:
        return None
    slow, fast = head, head.next.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    slow.next = slow.next.next
    return head
```

**Complexity:** time **O(n)**, space **O(1)** — one pass.

---

## Edge cases

- Single node.
- Two nodes → delete second.

---

## Common mistakes

1. Landing on the middle itself — can't delete it without its predecessor.

---

## Follow-ups

1. Using a prev pointer instead.

<details><summary>Answer sketches</summary>

**#1:** Track `prev = slow` before each slow step; also works.
</details>

---

## Flashcards

**Fast/slow start to land on the node before the middle?** #flashcard
`slow = head, fast = head.next.next`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
