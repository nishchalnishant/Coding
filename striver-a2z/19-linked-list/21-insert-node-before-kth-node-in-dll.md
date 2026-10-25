---
module: striver-a2z/19-linked-list
lesson: 21
topic: Insert Node Before Kth Node in DLL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/insert-node-before-kth-node-in-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, doubly-linked-list, insertion]
---
# 21. Insert Node Before Kth Node in DLL

← [Insert Node Before Tail in DLL](20-insert-node-before-tail-in-dll.md) · [Part 19 index](README.md) · Next → [Insert Before Given Node in DLL](22-insert-before-given-node-in-dll.md)

> [!abstract] Problem at a glance
> **Task:** Insert `x` before the k-th node (1-indexed, `1 ≤ k ≤ n`); unchanged if `k > n`.
> **Key insight:** Walk to the k-th node `t`, then the same insert-before-`t` primitive. `k = 1` is the `t.prev == null` branch.
> **Difficulty:** Easy · **Pattern:** Insert before a known node
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insert-node-before-kth-node-in-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Locate k-th + insert before](#3-locate-k-th--insert-before) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a doubly linked list, a position `k` and a value `x`, insert a node with value `x` before the k-th node and return the head.

| Input | Output | Why |
|---|---|---|
| `1⇄2⇄3, k = 3, x = 9` | `1⇄2⇄9⇄3` |  |
| `1⇄2⇄3, k = 1, x = 9` | `9⇄1⇄2⇄3` | new head |

**Constraints:** `1 ≤ n ≤ 10⁵`, `k ≥ 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Locate k-th + insert before | walk k − 1; node(next = t, prev = t.prev) | O(k) | O(1) |

> [!tip] Interview angle
> Same helper as Insert Before Tail — only the locate step changes.

---

## 3. Locate k-th + insert before

**Intuition.** Walking stops on the target itself; the DLL gives its predecessor for free.

**C++**
```cpp
Node* insertBeforeKth(Node* head, int k, int x) {
    Node* t = head;
    for (int i = 1; t && i < k; i++) t = t->next;
    if (!t) return head;
    Node* node = new Node(x, t, t->prev);
    if (t->prev) t->prev->next = node; else head = node;
    t->prev = node;
    return head;
}
```

**Java**
```java
static Node insertBeforeKth(Node head, int k, int x) {
    Node t = head;
    for (int i = 1; t != null && i < k; i++) t = t.next;
    if (t == null) return head;
    Node node = new Node(x, t, t.prev);
    if (t.prev != null) t.prev.next = node; else head = node;
    t.prev = node;
    return head;
}
```

**Python**
```python
def insert_before_kth(head, k, x):
    t = head
    for _ in range(k - 1):
        if not t:
            break
        t = t.next
    if not t:
        return head
    node = Node(x, t, t.prev)
    if t.prev:
        t.prev.next = node
    else:
        head = node
    t.prev = node
    return head
```

**Complexity:** time **O(k)**, space **O(1)** — k − 1 steps.

---

## Edge cases

- k = 1.
- k = n (before tail).
- k > n.

---

## Common mistakes

1. Walking k steps instead of k − 1.

---

## Follow-ups

1. Insert after the k-th node.

<details><summary>Answer sketches</summary>

**#1:** Symmetric: `node(next = t.next, prev = t)`; fix `t.next.prev` if present.
</details>

---

## Flashcards

**Does DLL insert-before need the predecessor while walking?** #flashcard
No — `t.prev` provides it.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
