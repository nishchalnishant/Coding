---
module: striver-a2z/19-linked-list
lesson: 35
topic: Find the Starting Point in LL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/find-the-starting-point-in-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, fast-slow, cycle]
---
# 35. Find the Starting Point in LL

← [Detect a Loop in LL](34-detect-a-loop-in-ll.md) · [Part 19 index](README.md) · Next → [Length of Loop in LL](36-length-of-loop-in-ll.md)

> [!abstract] Problem at a glance
> **Task:** Return the node where the cycle begins, or null.
> **Key insight:** After Floyd's meeting, reset one pointer to head; move both one step at a time — they meet at the loop start. Because `L = kC − d`: the head-to-start distance equals the meeting-point-to-start distance modulo the cycle.
> **Difficulty:** Medium · **Pattern:** Floyd cycle detection · **Also on:** 142
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-the-starting-point-in-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash set](#3-hash-set) · [4. Floyd + reset to head](#4-floyd--reset-to-head) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `head`, return the node where the cycle begins. If there is no cycle, return `null`. Do not modify the list.

| Input | Output | Why |
|---|---|---|
| `3→2→0→-4 → back to 2` | `node 2` |  |
| `1 (no cycle)` | `null` |  |

**Constraints:** `0 ≤ n ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash set | first revisited node is the start | O(n) | O(n) |
| Floyd + reset to head | meet; p = head; step both by 1 until equal | O(n) | O(1) |

> [!tip] Interview angle
> The derivation is what's graded. L = distance head→start, d = start→meeting, C = cycle length. Slow walked L + d, fast walked 2(L + d) = L + d + kC ⇒ L + d = kC ⇒ L = kC − d. From the meeting point, walking L steps lands on the start.

---

## 3. Hash set

**Intuition.** The first node seen twice is where the tail re-enters.

```python
def detect_cycle_set(head):
    seen = set()
    while head:
        if id(head) in seen:
            return head
        seen.add(id(head))
        head = head.next
    return None
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Floyd + reset to head

**Intuition.** L = kC − d, so a pointer from the head and one from the meeting point arrive at the start together.

**C++**
```cpp
ListNode* detectCycle(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            ListNode* p = head;
            while (p != slow) { p = p->next; slow = slow->next; }
            return p;
        }
    }
    return nullptr;
}
```

**Java**
```java
static ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            ListNode p = head;
            while (p != slow) { p = p.next; slow = slow.next; }
            return p;
        }
    }
    return null;
}
```

**Python**
```python
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            p = head
            while p is not slow:
                p, slow = p.next, slow.next
            return p
    return None
```

**Complexity:** time **O(n)**, space **O(1)** — linear in n.

---

## Edge cases

- Cycle starts at head (L = 0).
- Self-loop.
- No cycle.

---

## Common mistakes

1. Resetting **both** pointers.
2. Moving fast by 2 in the second phase.

---

## Follow-ups

1. Remove the loop.

<details><summary>Answer sketches</summary>

**#1:** From the start, walk to the node whose next is the start; set its next = null.
</details>

---

## Flashcards

**Floyd phase 2?** #flashcard
Reset one pointer to head; move both by 1; they meet at the loop start.

**Key equation for loop start?** #flashcard
L = kC − d.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
