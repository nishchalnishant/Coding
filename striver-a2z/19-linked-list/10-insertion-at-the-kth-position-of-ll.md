---
module: striver-a2z/19-linked-list
lesson: 10
topic: Insertion at the Kth Position of LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/insertion-at-the-kth-position-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, insertion, dummy-node]
---
# 10. Insertion at the Kth Position of LL

← [Insertion at the Tail of LL](09-insertion-at-the-tail-of-ll.md) · [Part 19 index](README.md) · Next → [Insertion Before the Value X in LL](11-insertion-before-the-value-x-in-ll.md)

> [!abstract] Problem at a glance
> **Task:** Insert `x` so it becomes the k-th node (1-indexed, `1 ≤ k ≤ n + 1`); ignore invalid `k`.
> **Key insight:** Reach node `k − 1` (the predecessor) and splice: `node.next = prev.next; prev.next = node`. From a dummy, that's `k − 1` steps; `k = 1` is not special.
> **Difficulty:** Easy · **Pattern:** Predecessor + splice
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insertion-at-the-kth-position-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Dummy + splice](#3-dummy--splice) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `head`, a position `k` (1-indexed) and a value `x`, insert a node with value `x` at position `k` and return the head. `k = n + 1` appends; `k > n + 1` leaves the list unchanged.

| Input | Output | Why |
|---|---|---|
| `1→2→3, k = 2, x = 9` | `1→9→2→3` |  |
| `1→2→3, k = 1, x = 9` | `9→1→2→3` | new head |
| `1→2→3, k = 4, x = 9` | `1→2→3→9` | append |

**Constraints:** `0 ≤ n ≤ 10⁵`, `1 ≤ k`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Dummy + splice | step k − 1 from dummy; node.next = prev.next; prev.next = node | O(k) | O(1) |

> [!tip] Interview angle
> The splice order matters: link the new node to the rest **before** redirecting the predecessor, or you lose the tail.

---

## 3. Dummy + splice

**Intuition.** Walk `k − 1` steps from the dummy; if you fall off the list before that, `k` is invalid.

**Algorithm**

1. `prev = dummy`.
2. Repeat `k − 1` times: if `prev` is null → return unchanged; `prev = prev.next`.
3. If `prev` is null → unchanged.
4. `node.next = prev.next; prev.next = node`.

**C++**
```cpp
ListNode* insertAtK(ListNode* head, int k, int x) {
    ListNode dummy(0, head);
    ListNode* prev = &dummy;
    for (int i = 0; i < k - 1; i++) {
        prev = prev->next;
        if (!prev) return head;
    }
    prev->next = new ListNode(x, prev->next);
    return dummy.next;
}
```

**Java**
```java
static ListNode insertAtK(ListNode head, int k, int x) {
    ListNode dummy = new ListNode(0, head), prev = dummy;
    for (int i = 0; i < k - 1; i++) {
        prev = prev.next;
        if (prev == null) return head;
    }
    prev.next = new ListNode(x, prev.next);
    return dummy.next;
}
```

**Python**
```python
def insert_at_k(head, k, x):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(k - 1):
        prev = prev.next
        if not prev:
            return head
    prev.next = ListNode(x, prev.next)
    return dummy.next
```

**Complexity:** time **O(k)**, space **O(1)** — k − 1 steps.

---

## Edge cases

- `k = 1` → new head.
- `k = n + 1` → append.
- `k > n + 1` → unchanged.
- Empty list with `k = 1`.

---

## Common mistakes

1. `prev.next = node; node.next = prev.next` — node points to itself.
2. Off-by-one: walking k steps inserts at k + 1.

---

## Follow-ups

1. Insert into a sorted list.

<details><summary>Answer sketches</summary>

**#1:** Advance while `prev.next.val < x`, then splice.
</details>

---

## Flashcards

**Splice order?** #flashcard
`node.next = prev.next` first, then `prev.next = node`.

**Steps from dummy to insert at position k?** #flashcard
k − 1.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
