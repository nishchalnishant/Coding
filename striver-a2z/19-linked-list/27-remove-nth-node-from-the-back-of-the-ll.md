---
module: striver-a2z/19-linked-list
lesson: 27
topic: Remove Nth Node from the Back of the LL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/remove-nth-node-from-the-back-of-the-ll?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, two-pointers, dummy-node]
---
# 27. Remove Nth Node from the Back of the LL

← [Sort a LL of 0's, 1's and 2's](26-sort-a-ll-of-0-s-1-s-and-2-s.md) · [Part 19 index](README.md) · Next → [Reverse a LL](28-reverse-a-ll.md)

> [!abstract] Problem at a glance
> **Task:** Delete the n-th node from the end (`1 ≤ n ≤ length`) in one pass.
> **Key insight:** Gap of n between two pointers: move `fast` n steps ahead, then move both until `fast.next` is null — `slow` is the predecessor. Starting both at a dummy covers deleting the head.
> **Difficulty:** Medium · **Pattern:** Fast/slow with fixed gap · **Also on:** 19
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/remove-nth-node-from-the-back-of-the-ll?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Two passes (length)](#3-two-passes-length) · [4. One pass, gap of n](#4-one-pass-gap-of-n) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a linked list, remove the n-th node from the end of the list and return its head.

| Input | Output | Why |
|---|---|---|
| `1→2→3→4→5, n = 2` | `1→2→3→5` |  |
| `1, n = 1` | `null` |  |
| `1→2→3, n = 3` | `2→3` | removes head |

**Constraints:** `1 ≤ n ≤ sz ≤ 30`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Two passes (length) | L = length; delete (L − n + 1)-th from front | O(n) | O(1) |
| One pass, gap of n | fast n ahead; move both until fast.next is null | O(n) | O(1) |

> [!tip] Interview angle
> Give the two-pass version (length, then `len − n` steps) first, then the one-pass gap trick — the follow-up is always "can you do it in one pass?"

---

## 3. Two passes (length)

**Intuition.** n-th from the end = (L − n + 1)-th from the start; its predecessor is L − n steps from a dummy.

```python
def remove_nth_two_pass(head, n):
    L, cur = 0, head
    while cur:
        L += 1
        cur = cur.next
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(L - n):
        prev = prev.next
    prev.next = prev.next.next
    return dummy.next
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. One pass, gap of n

**Intuition.** When `fast` sits on the last node, `slow` is exactly n + 1 nodes from the end — the predecessor of the target.

**Dry run** — dummy→1→2→3→4→5, n=2: fast → 2; move both until fast = 5: slow = 3; 3.next = 5.

**C++**
```cpp
ListNode* removeNthFromEnd(ListNode* head, int n) {
    ListNode dummy(0, head);
    ListNode *slow = &dummy, *fast = &dummy;
    while (n--) fast = fast->next;
    while (fast->next) { slow = slow->next; fast = fast->next; }
    ListNode* del = slow->next;
    slow->next = del->next;
    delete del;
    return dummy.next;
}
```

**Java**
```java
static ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode dummy = new ListNode(0, head), slow = dummy, fast = dummy;
    while (n-- > 0) fast = fast.next;
    while (fast.next != null) { slow = slow.next; fast = fast.next; }
    slow.next = slow.next.next;
    return dummy.next;
}
```

**Python**
```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    return dummy.next
```

**Complexity:** time **O(n)**, space **O(1)** — single pass.

---

## Edge cases

- n = length (remove head).
- Single node.
- n = 1 (remove tail).

---

## Common mistakes

1. Starting at `head` instead of a dummy → can't remove the head.
2. `while fast` instead of `while fast.next` → slow lands on the target, not its predecessor.

---

## Follow-ups

1. Return the n-th node from the end.

<details><summary>Answer sketches</summary>

**#1:** Same gap; start at head and loop `while fast`.
</details>

---

## Flashcards

**One-pass n-th from end trick?** #flashcard
Advance fast n steps, then move both until fast.next is null; slow is the predecessor.

**Why start at a dummy?** #flashcard
Removing the head needs a predecessor.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
