---
module: striver/19-linked-list
lesson: 17
topic: Delete Kth Element of DLL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/delete-kth-element-of-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, doubly-linked-list, deletion]
---
# 17. Delete Kth Element of DLL

← [Delete Tail of DLL](16-delete-tail-of-dll.md) · [Part 19 index](README.md) · Next → [Removing Given Node in DLL](18-removing-given-node-in-dll.md)

> [!abstract] Problem at a glance
> **Task:** Delete the k-th node (1-indexed); unchanged if `k > n`.
> **Key insight:** Walk **to** the k-th node (no predecessor needed). Then four cases by whether `prev`/`next` are null: only, head, tail, middle. Middle: `prev.next = next; next.prev = prev`.
> **Difficulty:** Easy · **Pattern:** Locate + unlink both sides
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/delete-kth-element-of-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Locate + unlink](#3-locate--unlink) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a doubly linked list and `k` (1-indexed), delete the k-th node and return the head.

| Input | Output | Why |
|---|---|---|
| `1⇄2⇄3, k = 2` | `1⇄3` |  |
| `1⇄2⇄3, k = 1` | `2⇄3` | head |
| `1⇄2⇄3, k = 4` | `unchanged` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`, `k ≥ 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Locate + unlink | fix prev.next and next.prev, each if present | O(k) | O(1) |

> [!tip] Interview angle
> Narrate the 4-case table — it's the template for every DLL unlink (LRU cache `remove(node)` included). A sentinel head + tail collapses all four to the middle case.

---

## 3. Locate + unlink

**Intuition.** Find the node, then rewire whichever neighbours exist. If there's no `prev`, the head moves.

**Algorithm**

1. Walk `k − 1` steps from head; if null → unchanged.
2. `p, n = node.prev, node.next`.
3. If `p`: `p.next = n`, else `head = n`.
4. If `n`: `n.prev = p`.

**C++**
```cpp
Node* deleteKth(Node* head, int k) {
    Node* node = head;
    for (int i = 1; node && i < k; i++) node = node->next;
    if (!node) return head;
    Node *p = node->prev, *n = node->next;
    if (p) p->next = n; else head = n;
    if (n) n->prev = p;
    delete node;
    return head;
}
```

**Java**
```java
static Node deleteKth(Node head, int k) {
    Node node = head;
    for (int i = 1; node != null && i < k; i++) node = node.next;
    if (node == null) return head;
    Node p = node.prev, n = node.next;
    if (p != null) p.next = n; else head = n;
    if (n != null) n.prev = p;
    node.next = node.prev = null;
    return head;
}
```

**Python**
```python
def delete_kth(head, k):
    node = head
    for _ in range(k - 1):
        if not node:
            break
        node = node.next
    if not node:
        return head
    p, n = node.prev, node.next
    if p:
        p.next = n
    else:
        head = n
    if n:
        n.prev = p
    node.next = node.prev = None
    return head
```

**Complexity:** time **O(k)**, space **O(1)** — k − 1 steps; O(1) unlink.

---

## Edge cases

- k = 1 (head).
- k = n (tail).
- k > n.
- Single node.

---

## Common mistakes

1. Fixing `p.next` but not `n.prev`.
2. Not moving `head` when the head is deleted.

---

## Follow-ups

1. LRU cache remove(node).

<details><summary>Answer sketches</summary>

**#1:** Same unlink, O(1) because the hash map gives the node directly; sentinels remove the null checks.
</details>

---

## Flashcards

**DLL unlink of node x?** #flashcard
`if p: p.next = n else head = n`; `if n: n.prev = p`.

**What do sentinel head/tail nodes buy?** #flashcard
Every real node has both neighbours → no null-check cases.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
