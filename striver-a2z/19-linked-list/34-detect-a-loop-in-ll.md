---
module: striver-a2z/19-linked-list
lesson: 34
topic: Detect a Loop in LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/detect-a-loop-in-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, fast-slow, cycle]
---
# 34. Detect a Loop in LL

← [Find the Intersection Point of Y LL](33-find-the-intersection-point-of-y-ll.md) · [Part 19 index](README.md) · Next → [Find the Starting Point in LL](35-find-the-starting-point-in-ll.md)

> [!abstract] Problem at a glance
> **Task:** Return whether the list contains a cycle.
> **Key insight:** Floyd: slow moves 1, fast moves 2. Inside a cycle the gap shrinks by 1 each step, so they must meet; without a cycle fast reaches null.
> **Difficulty:** Easy · **Pattern:** Floyd cycle detection · **Also on:** 141
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/detect-a-loop-in-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash set of visited nodes](#3-hash-set-of-visited-nodes) · [4. Floyd tortoise and hare](#4-floyd-tortoise-and-hare) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `head`, return `true` if some node can be reached again by following `next` pointers. (`pos` in the input marks where the tail links; it isn't passed to you.)

| Input | Output | Why |
|---|---|---|
| `3→2→0→-4 → back to 2` | `true` |  |
| `1` | `false` |  |

**Constraints:** `0 ≤ n ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash set of visited nodes | seen node again → cycle | O(n) | O(n) |
| Floyd tortoise and hare | slow 1, fast 2; meet → cycle | O(n) | O(1) |

> [!tip] Interview angle
> Prove it: once both are in the cycle, the distance from fast to slow (going forward) drops by exactly 1 per step, so it hits 0 — fast can't jump over slow.

---

## 3. Hash set of visited nodes

**Intuition.** First revisit proves a cycle.

```python
def has_cycle_set(head):
    seen = set()
    while head:
        if id(head) in seen:
            return True
        seen.add(id(head))
        head = head.next
    return False
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Floyd tortoise and hare

**Intuition.** Relative speed 1 inside the loop guarantees a meeting within one lap.

**C++**
```cpp
bool hasCycle(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}
```

**Java**
```java
static boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}
```

**Python**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False
```

**Complexity:** time **O(n)**, space **O(1)** — slow takes < n + loop length steps.

---

## Edge cases

- Empty list.
- Self-loop on one node.
- Cycle back to head.

---

## Common mistakes

1. Checking `slow == fast` before moving (they start equal).
2. Checking only `fast.next` → null dereference.

---

## Follow-ups

1. Where does the loop start?
2. Find the duplicate number (LC 287).

<details><summary>Answer sketches</summary>

**#1:** Next problem.

**#2:** Array as a functional graph `i → nums[i]`; Floyd finds the duplicate.
</details>

---

## Flashcards

**Why can't fast skip over slow in Floyd?** #flashcard
The gap shrinks by exactly 1 per step.

**Floyd loop condition?** #flashcard
`while fast and fast.next`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
