---
module: striver/19-linked-list
lesson: 40
topic: Flattening of LL
difficulty: Hard
source: https://takeuforward.org/learning/dsa/flattening-of-ll?category=faqs--hard&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, merge, heap]
---
# 40. Flattening of LL

← [Merge Two Sorted Lists](39-merge-two-sorted-lists.md) · [Part 19 index](README.md) · Next → [Sort LL](41-sort-ll.md)

> [!abstract] Problem at a glance
> **Task:** Each top node heads a sorted `child` chain; merge all chains into one sorted chain via `child` (all `next` = null).
> **Key insight:** It's merge-k-sorted-lists on the `child` pointer. Recursively flatten `head.next`, then merge it with `head`'s column — or pour all heads into a min-heap.
> **Difficulty:** Hard · **Pattern:** Merge k sorted lists
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/flattening-of-ll?category=faqs--hard&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Collect, sort, rebuild](#3-collect-sort-rebuild) · [4. Min-heap of column heads](#4-min-heap-of-column-heads) · [5. Recursive merge from the right](#5-recursive-merge-from-the-right) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a linked list where every node has `next` (to the next column head) and `child` (down its sorted column), flatten it so all nodes appear in a single sorted list linked by `child`, with every `next` set to null.

| Input | Output | Why |
|---|---|---|
| `columns [5,7,8,30] [10,20] [19,22,50] [28,35,40,45]` | `5→7→8→10→19→20→22→28→30→35→40→45→50 (via child)` |  |

**Constraints:** `0 ≤ total nodes ≤ 50·50`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Collect, sort, rebuild | all values → sort → child chain | O(N log N) | O(N) |
| Min-heap of column heads | pop min; push its child | O(N log k) | O(k) |
| Recursive merge from the right | head.next = flatten(head.next); merge(head, head.next) | O(N · k) | O(k) stack |

> [!tip] Interview angle
> Name it immediately: "this is merge k sorted lists along child". Then pick recursion (O(N·k)) or a heap (O(N log k)); mention the trade-off.

---

## 3. Collect, sort, rebuild

**Intuition.** Throws away the structure; baseline.

```python
def flatten_brute(head):
    vals, col = [], head
    while col:
        t = col
        while t:
            vals.append(t.val)
            t = t.child
        col = col.next
    vals.sort()
    dummy = t = Node(0)
    for v in vals:
        t.child = Node(v)
        t = t.child
    return dummy.child
```

**Complexity:** time **O(N log N)**, space **O(N)**.

---

## 4. Min-heap of column heads

**Intuition.** Standard k-way merge.

```python
import heapq
def flatten_heap(head):
    h, i = [], 0
    while head:
        heapq.heappush(h, (head.val, i, head))
        i += 1
        head = head.next
    dummy = t = Node(0)
    while h:
        _, _, n = heapq.heappop(h)
        if n.child:
            heapq.heappush(h, (n.child.val, i, n.child))
            i += 1
        n.next = None
        t.child = n
        t = n
    t.child = None
    return dummy.child
```

**Complexity:** time **O(N log k)**, space **O(k)**.

---

## 5. Recursive merge from the right

**Intuition.** Flatten everything to the right, then it's a two-list merge on `child`.

**C++**
```cpp
Node* mergeChild(Node* a, Node* b) {
    Node dummy(0);
    Node* t = &dummy;
    while (a && b) {
        if (a->val <= b->val) { t->child = a; a = a->child; }
        else { t->child = b; b = b->child; }
        t = t->child;
        t->next = nullptr;
    }
    t->child = a ? a : b;
    if (t->child) t->child->next = nullptr;
    return dummy.child;
}
Node* flatten(Node* head) {
    if (!head || !head->next) return head;
    Node* rest = flatten(head->next);
    head->next = nullptr;
    return mergeChild(head, rest);
}
```

**Java**
```java
static Node mergeChild(Node a, Node b) {
    Node dummy = new Node(0), t = dummy;
    while (a != null && b != null) {
        if (a.val <= b.val) { t.child = a; a = a.child; }
        else { t.child = b; b = b.child; }
        t = t.child;
        t.next = null;
    }
    t.child = a != null ? a : b;
    if (t.child != null) t.child.next = null;
    return dummy.child;
}
static Node flatten(Node head) {
    if (head == null || head.next == null) return head;
    Node rest = flatten(head.next);
    head.next = null;
    return mergeChild(head, rest);
}
```

**Python**
```python
def flatten(head):
    def merge(a, b):
        dummy = t = Node(0)
        while a and b:
            if a.val <= b.val:
                t.child, a = a, a.child
            else:
                t.child, b = b, b.child
            t = t.child
            t.next = None
        t.child = a or b
        if t.child:
            t.child.next = None
        return dummy.child
    if not head or not head.next:
        return head
    rest = flatten(head.next)
    head.next = None
    return merge(head, rest)
```

**Complexity:** time **O(N · k)**, space **O(k) stack** — simple; heap version is asymptotically better for many columns.

---

## Edge cases

- Single column.
- Every column has one node.
- Empty input.

---

## Common mistakes

1. Leaving stale `next` pointers in the result.
2. Merging along `next` instead of `child`.

---

## Follow-ups

1. Flatten a multilevel DLL (LC 430).

<details><summary>Answer sketches</summary>

**#1:** DFS: splice child list between node and node.next; different problem (no sorting).
</details>

---

## Flashcards

**Flattening a linked list is really…?** #flashcard
Merge k sorted lists along `child`.

**Recursive flatten complexity?** #flashcard
O(N·k) — each merge rescans the accumulated list.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
