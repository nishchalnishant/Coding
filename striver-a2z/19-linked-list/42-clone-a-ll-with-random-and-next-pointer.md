---
module: striver-a2z/19-linked-list
lesson: 42
topic: Clone a LL with Random and Next Pointer
difficulty: Medium
source: https://takeuforward.org/learning/dsa/clone-a-ll-with-random-and-next-pointer?category=faqs--hard&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, hashing]
---
# 42. Clone a LL with Random and Next Pointer

← [Sort LL](41-sort-ll.md) · [Part 19 index](README.md) · Next → [Delete All Occurrences of a Key in DLL](43-delete-all-occurrences-of-a-key-in-dll.md)

> [!abstract] Problem at a glance
> **Task:** Deep-copy a list whose nodes also have a `random` pointer; no copy may point into the original.
> **Key insight:** The hard part is mapping old → new for `random`. Hash map does it in O(n) space; **interleaving** (A→A'→B→B'…) makes `old.next` the map, so `old.next.random = old.random.next` — then unweave.
> **Difficulty:** Medium · **Pattern:** Interleave copies · **Also on:** 138
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/clone-a-ll-with-random-and-next-pointer?category=faqs--hard&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash map old → new](#3-hash-map-old--new) · [4. Interleave, wire random, unweave](#4-interleave-wire-random-unweave) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A linked list of length n has nodes with `next` and `random` (any node or null). Construct a deep copy and return its head. The original must be left unchanged.

| Input | Output | Why |
|---|---|---|
| `[[7,null],[13,0],[11,4],[10,2],[1,0]]` | `same structure, new nodes` | pairs are [val, random index] |

**Constraints:** `0 ≤ n ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash map old → new | pass 1: create copies; pass 2: wire next/random via map | O(n) | O(n) |
| Interleave, wire random, unweave | A→A'→B→B'; A'.random = A.random.next; split | O(n) | O(1) extra |

> [!tip] Interview angle
> Hash map first (clear and correct), then interleaving for O(1) extra. Emphasize restoring the original in pass 3 — a common bug the grader checks.

---

## 3. Hash map old → new

**Intuition.** `m[None] = None` avoids null checks.

```python
def copy_random_map(head):
    m = {None: None}
    t = head
    while t:
        m[t] = Node(t.val)
        t = t.next
    t = head
    while t:
        m[t].next, m[t].random = m[t.next], m[t.random]
        t = t.next
    return m[head]
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Interleave, wire random, unweave

**Intuition.** Each copy sits right after its original, so the original's random's `next` is the copy's random.

**Algorithm**

1. Insert copy after each node.
2. For each original `t`: `t.next.random = t.random.next if t.random else None`.
3. Split: restore `t.next = t.next.next`, copy chain likewise.

**C++**
```cpp
Node* copyRandomList(Node* head) {
    for (Node* t = head; t; t = t->next->next) {
        Node* c = new Node(t->val);
        c->next = t->next;
        t->next = c;
    }
    for (Node* t = head; t; t = t->next->next)
        t->next->random = t->random ? t->random->next : nullptr;
    Node dummy(0);
    Node* c = &dummy;
    for (Node* t = head; t; t = t->next) {
        c->next = t->next;
        c = c->next;
        t->next = c->next;
    }
    return dummy.next;
}
```

**Java**
```java
static Node copyRandomList(Node head) {
    for (Node t = head; t != null; t = t.next.next) {
        Node c = new Node(t.val);
        c.next = t.next;
        t.next = c;
    }
    for (Node t = head; t != null; t = t.next.next)
        t.next.random = t.random != null ? t.random.next : null;
    Node dummy = new Node(0), c = dummy;
    for (Node t = head; t != null; t = t.next) {
        c.next = t.next;
        c = c.next;
        t.next = c.next;
    }
    return dummy.next;
}
```

**Python**
```python
def copy_random_list(head):
    t = head
    while t:
        t.next = Node(t.val, t.next)
        t = t.next.next
    t = head
    while t:
        t.next.random = t.random.next if t.random else None
        t = t.next.next
    dummy = c = Node(0)
    t = head
    while t:
        c.next = t.next
        c = c.next
        t.next = c.next
        t = t.next
    return dummy.next
```

**Complexity:** time **O(n)**, space **O(1) extra** — three linear passes, no map.

---

## Edge cases

- Empty list.
- random → self.
- Duplicate values (identity matters, not value).

---

## Common mistakes

1. Setting `random` in the same pass as inserting copies — later copies don't exist yet.
2. Not restoring the original's `next` pointers.

---

## Follow-ups

1. Clone a graph (LC 133).
2. Clone a binary tree with random pointers.

<details><summary>Answer sketches</summary>

**#1:** Same hash-map idea with DFS/BFS.

**#2:** Map old → new via DFS.
</details>

---

## Flashcards

**O(1)-space random-list clone?** #flashcard
Interleave copies; copy.random = orig.random.next; unweave.

**Why a separate pass for random?** #flashcard
The target copy must already exist.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
