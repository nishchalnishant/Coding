---
module: striver/19-linked-list
lesson: 33
topic: Find the Intersection Point of Y LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/find-the-intersection-point-of-y-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, two-pointers]
---
# 33. Find the Intersection Point of Y LL

← [Check if LL is Palindrome or Not](32-check-if-ll-is-palindrome-or-not.md) · [Part 19 index](README.md) · Next → [Detect a Loop in LL](34-detect-a-loop-in-ll.md)

> [!abstract] Problem at a glance
> **Task:** Return the first node shared by two lists (by identity, not value), or null.
> **Key insight:** Two pointers that switch to the other list's head on reaching the end each walk `a + c + b` nodes — they meet at the junction (or both reach null together).
> **Difficulty:** Easy · **Pattern:** Pointer switching · **Also on:** 160
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-the-intersection-point-of-y-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash set of A's nodes](#3-hash-set-of-as-nodes) · [4. Align by length difference](#4-align-by-length-difference) · [5. Pointer switching](#5-pointer-switching) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the heads of two singly linked lists `headA` and `headB`, return the node at which they intersect, or `null`. The lists have no cycles and must keep their structure.

| Input | Output | Why |
|---|---|---|
| `A: 4→1→8→4→5, B: 5→6→1→8→4→5 (shared from 8)` | `node 8` |  |
| `no shared tail` | `null` |  |

**Constraints:** `1 ≤ m, n ≤ 3·10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash set of A's nodes | store A's nodes; first B node in set | O(m + n) | O(m) |
| Align by length difference | advance longer list by |m − n|, then step together | O(m + n) | O(1) |
| Pointer switching | p = p.next or headB; q = q.next or headA; until p is q | O(m + n) | O(1) |

> [!tip] Interview angle
> Equal values don't mean intersection — it's node identity. Walk through all three solutions: hash set, length difference, pointer switching. The switching one is the expected final answer.

---

## 3. Hash set of A's nodes

**Intuition.** Identity hashing (`id` / pointer).

```python
def intersect_set(a, b):
    seen = set()
    while a:
        seen.add(id(a))
        a = a.next
    while b:
        if id(b) in seen:
            return b
        b = b.next
    return None
```

**Complexity:** time **O(m + n)**, space **O(m)**.

---

## 4. Align by length difference

**Intuition.** After alignment, both pointers are the same distance from the end; they meet at the junction.

```python
def intersect_len(a, b):
    def ln(h):
        n = 0
        while h:
            n, h = n + 1, h.next
        return n
    m, n = ln(a), ln(b)
    for _ in range(m - n):
        a = a.next
    for _ in range(n - m):
        b = b.next
    while a is not b:
        a, b = a.next, b.next
    return a
```

**Complexity:** time **O(m + n)**, space **O(1)**.

---

## 5. Pointer switching

**Intuition.** A's private part `a`, B's `b`, shared `c`. p walks a + c + b, q walks b + c + a — same length, so they arrive together. No intersection → both null after m + n.

**C++**
```cpp
ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
    ListNode *p = headA, *q = headB;
    while (p != q) {
        p = p ? p->next : headB;
        q = q ? q->next : headA;
    }
    return p;
}
```

**Java**
```java
static ListNode getIntersectionNode(ListNode headA, ListNode headB) {
    ListNode p = headA, q = headB;
    while (p != q) {
        p = p != null ? p.next : headB;
        q = q != null ? q.next : headA;
    }
    return p;
}
```

**Python**
```python
def get_intersection_node(head_a, head_b):
    p, q = head_a, head_b
    while p is not q:
        p = p.next if p else head_b
        q = q.next if q else head_a
    return p
```

**Complexity:** time **O(m + n)**, space **O(1)** — each pointer walks at most m + n.

---

## Edge cases

- No intersection → both reach null together.
- One list is entirely the shared part.
- Intersection at the first node.

---

## Common mistakes

1. Comparing values instead of node identity.
2. Switching on `p.next is None` instead of `p is None` → infinite loop with no intersection.

---

## Follow-ups

1. Lists may contain cycles.

<details><summary>Answer sketches</summary>

**#1:** Find each loop start; same loop or disjoint loops determine the answer.
</details>

---

## Flashcards

**Why do switching pointers meet at the junction?** #flashcard
Both walk a + b + c nodes in total.

**No-intersection termination?** #flashcard
Both become null simultaneously after m + n steps.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
