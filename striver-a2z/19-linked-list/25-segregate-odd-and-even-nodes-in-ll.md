---
module: striver-a2z/19-linked-list
lesson: 25
topic: Segregate Odd and Even Nodes in LL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/segregate-odd-and-even-nodes-in-ll?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, rearrangement]
---
# 25. Segregate Odd and Even Nodes in LL

← [Add Two Numbers in LL](24-add-two-numbers-in-ll.md) · [Part 19 index](README.md) · Next → [Sort a LL of 0's, 1's and 2's](26-sort-a-ll-of-0-s-1-s-and-2-s.md)

> [!abstract] Problem at a glance
> **Task:** Group nodes at odd positions (1st, 3rd, …) first, then even positions, keeping relative order. O(1) extra space.
> **Key insight:** Two chains woven out of one list: `odd.next = even.next; odd = odd.next; even.next = odd.next; even = even.next`. Remember `evenHead` and attach it after the last odd.
> **Difficulty:** Medium · **Pattern:** Split into chains + join · **Also on:** 328
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/segregate-odd-and-even-nodes-in-ll?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Collect values, rewrite](#3-collect-values-rewrite) · [4. Weave two chains](#4-weave-two-chains) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list, group all nodes at odd indices together followed by the nodes at even indices (1-indexed positions, not values). Return the reordered list.

| Input | Output | Why |
|---|---|---|
| `1→2→3→4→5` | `1→3→5→2→4` |  |
| `2→1→3→5→6→4→7` | `2→3→6→7→1→5→4` | positions, not values |

**Constraints:** `0 ≤ n ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Collect values, rewrite | odd-index values then even-index values; overwrite | O(n) | O(n) |
| Weave two chains | odd/even pointers leapfrog; odd.next = evenHead | O(n) | O(1) |

> [!tip] Interview angle
> Clarify **positions vs values** first (Striver's version and LC 328 are positional). Loop condition `while even and even.next` covers both odd and even lengths.

---

## 3. Collect values, rewrite

**Intuition.** Easy baseline that changes data, not links.

```python
def odd_even_values(head):
    vals, cur = [], head
    while cur:
        vals.append(cur.val)
        cur = cur.next
    vals = vals[0::2] + vals[1::2]
    cur = head
    for v in vals:
        cur.val = v
        cur = cur.next
    return head
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Weave two chains

**Intuition.** Each pointer skips the other's node. When `even` runs out, `odd` is the last odd node.

**Dry run** — 1→2→3→4→5: odd 1→3, even 2→4, odd 3→5, even 4→null; stop; 5.next = 2.

**C++**
```cpp
ListNode* oddEvenList(ListNode* head) {
    if (!head) return head;
    ListNode *odd = head, *even = head->next, *evenHead = even;
    while (even && even->next) {
        odd = odd->next = even->next;
        even = even->next = odd->next;
    }
    odd->next = evenHead;
    return head;
}
```

**Java**
```java
static ListNode oddEvenList(ListNode head) {
    if (head == null) return head;
    ListNode odd = head, even = head.next, evenHead = even;
    while (even != null && even.next != null) {
        odd.next = even.next;
        odd = odd.next;
        even.next = odd.next;
        even = even.next;
    }
    odd.next = evenHead;
    return head;
}
```

**Python**
```python
def odd_even_list(head):
    if not head:
        return head
    odd, even = head, head.next
    even_head = even
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, relinks only.

---

## Edge cases

- 0, 1, 2 nodes.
- Odd and even lengths.

---

## Common mistakes

1. Not saving `evenHead` before weaving.
2. `while odd.next` — crashes or misses the last even.

---

## Follow-ups

1. Segregate by value parity (evens first).

<details><summary>Answer sketches</summary>

**#1:** Two dummy chains appended by `val % 2`, then join.
</details>

---

## Flashcards

**Odd-even list loop condition?** #flashcard
`while even and even.next`.

**What must you save before weaving?** #flashcard
`evenHead = head.next`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
