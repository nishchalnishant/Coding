---
module: striver/19-linked-list
lesson: 6
topic: Deletion of the Kth Element of LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/deletion-of-the-kth-element-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, deletion, dummy-node]
---
# 6. Deletion of the Kth Element of LL

← [Deletion of the Tail of LL](05-deletion-of-the-tail-of-ll.md) · [Part 19 index](README.md) · Next → [Delete the Element with Value X](07-delete-the-element-with-value-x.md)

> [!abstract] Problem at a glance
> **Task:** Delete the node at 1-indexed position `k`; if `k` exceeds the length, return the list unchanged.
> **Key insight:** `k = 1` is the head case. Otherwise walk with `prev` to node `k − 1` and bypass: `prev.next = prev.next.next`. A dummy node removes the special case.
> **Difficulty:** Easy · **Pattern:** Predecessor + bypass
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/deletion-of-the-kth-element-of-ll?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Count with prev](#3-count-with-prev) · [4. Dummy node](#4-dummy-node) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list and an integer `k` (1-indexed), delete the k-th node and return the head. If `k > n`, change nothing.

| Input | Output | Why |
|---|---|---|
| `1→2→3→4, k = 2` | `1→3→4` |  |
| `1→2→3→4, k = 1` | `2→3→4` | head deleted |
| `1→2→3, k = 5` | `1→2→3` | out of range |

**Constraints:** `0 ≤ n ≤ 10⁵`, `1 ≤ k`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Count with prev | special-case k = 1; walk prev to k − 1; bypass | O(k) | O(1) |
| Dummy node | dummy → head; step k − 1 from dummy; bypass | O(k) | O(1) |

> [!tip] Interview angle
> The dummy-node trick is the takeaway: point a sentinel at head, walk `k − 1` steps from the sentinel, bypass, return `dummy.next`. Head deletion stops being a special case.

---

## 3. Count with prev

**Intuition.** Track `cnt` and `prev`. When `cnt == k`, link `prev.next = cur.next`.

```python
def delete_kth_count(head, k):
    if not head:
        return None
    if k == 1:
        return head.next
    cnt, prev, cur = 0, None, head
    while cur:
        cnt += 1
        if cnt == k:
            prev.next = cur.next
            break
        prev, cur = cur, cur.next
    return head
```

**Complexity:** time **O(k)**, space **O(1)**.

---

## 4. Dummy node

**Intuition.** A dummy before the head means every real node, including the head, has a predecessor. Walk `k − 1` steps; if the next node exists, skip it.

**Algorithm**

1. `dummy.next = head`, `prev = dummy`.
2. Repeat `k − 1` times while `prev.next`: `prev = prev.next`.
3. If `prev.next`: `prev.next = prev.next.next`.
4. Return `dummy.next`.

**Dry run** — 1→2→3→4, k = 2: prev=dummy → 1 step → prev=1; bypass 2 → 1→3→4.

**C++**
```cpp
ListNode* deleteKth(ListNode* head, int k) {
    ListNode dummy(0, head);
    ListNode* prev = &dummy;
    for (int i = 0; i < k - 1 && prev->next; i++) prev = prev->next;
    if (prev->next) {
        ListNode* del = prev->next;
        prev->next = del->next;
        delete del;
    }
    return dummy.next;
}
```

**Java**
```java
static ListNode deleteKth(ListNode head, int k) {
    ListNode dummy = new ListNode(0, head), prev = dummy;
    for (int i = 0; i < k - 1 && prev.next != null; i++) prev = prev.next;
    if (prev.next != null) prev.next = prev.next.next;
    return dummy.next;
}
```

**Python**
```python
def delete_kth(head, k):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(k - 1):
        if not prev.next:
            break
        prev = prev.next
    if prev.next:
        prev.next = prev.next.next
    return dummy.next
```

**Complexity:** time **O(k)**, space **O(1)** — at most k steps.

---

## Edge cases

- `k = 1` (head).
- `k = n` (tail).
- `k > n` → unchanged.
- Empty list.

---

## Common mistakes

1. Walking to node k instead of k − 1.
2. Forgetting to return `dummy.next` (returning stale `head` after deleting it).

---

## Follow-ups

1. Delete the k-th node from the end.

<details><summary>Answer sketches</summary>

**#1:** Two pointers k apart — see Remove Nth Node from the back.
</details>

---

## Flashcards

**Why a dummy node?** #flashcard
Gives the head a predecessor so head deletion isn't a special case.

**Steps from dummy to reach node k's predecessor?** #flashcard
k − 1.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
