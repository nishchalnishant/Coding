---
module: striver-a2z/19-linked-list
lesson: 18
topic: Removing Given Node in DLL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/removing-given-node-in-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, doubly-linked-list, deletion]
---
# 18. Removing Given Node in DLL

← [Delete Kth Element of DLL](17-delete-kth-element-of-dll.md) · [Part 19 index](README.md) · Next → [Insert Node Before Head in DLL](19-insert-node-before-head-in-dll.md)

> [!abstract] Problem at a glance
> **Task:** Given only a pointer to a node (guaranteed not the head), unlink it from the list.
> **Key insight:** A DLL node knows both neighbours, so no head and no walk are needed: `node.prev.next = node.next`, and if `node.next` exists, `node.next.prev = node.prev`. O(1).
> **Difficulty:** Easy · **Pattern:** O(1) unlink
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/removing-given-node-in-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Rewire neighbours](#3-rewire-neighbours) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

You are given a pointer `node` to a node of a doubly linked list. It is not the head. Remove it from the list in place.

| Input | Output | Why |
|---|---|---|
| `1⇄2⇄3, node = 2` | `1⇄3` |  |
| `1⇄2⇄3, node = 3` | `1⇄2` | tail |

**Constraints:** `2 ≤ n ≤ 10⁵`; `node` is not the head.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Rewire neighbours | prev.next = next; next.prev = prev (if next) | O(1) | O(1) |

> [!tip] Interview angle
> Contrast with LC 237 (singly): there you must copy the next value and delete the next node instead, and it fails for the tail. This O(1) unlink is why LRU caches use a DLL.

---

## 3. Rewire neighbours

**Intuition.** Because it isn't the head, `prev` always exists; only `next` may be null (the tail).

**C++**
```cpp
void deleteNode(Node* node) {
    node->prev->next = node->next;
    if (node->next) node->next->prev = node->prev;
    delete node;
}
```

**Java**
```java
static void deleteNode(Node node) {
    node.prev.next = node.next;
    if (node.next != null) node.next.prev = node.prev;
    node.next = node.prev = null;
}
```

**Python**
```python
def delete_node(node):
    node.prev.next = node.next
    if node.next:
        node.next.prev = node.prev
    node.next = node.prev = None
```

**Complexity:** time **O(1)**, space **O(1)** — no traversal.

---

## Edge cases

- Node is the tail (`next` null).

---

## Common mistakes

1. Clearing `node.next` before reading it.

---

## Follow-ups

1. Singly-list version (LC 237).

<details><summary>Answer sketches</summary>

**#1:** Copy `node.next.val` into node, then bypass `node.next`. Can't delete the tail.
</details>

---

## Flashcards

**Delete a given node in O(1) — DLL vs SLL?** #flashcard
DLL: rewire prev/next. SLL: copy next's value then delete next (fails at tail).

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
