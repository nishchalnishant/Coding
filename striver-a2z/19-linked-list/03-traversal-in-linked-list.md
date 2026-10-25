---
module: striver-a2z/19-linked-list
lesson: 3
topic: Traversal in Linked List
difficulty: Easy
source: https://takeuforward.org/learning/dsa/traversal-in-linked-list?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, traversal]
---
# 3. Traversal in Linked List

← [Doubly Linked List](02-doubly-linked-list.md) · [Part 19 index](README.md) · Next → [Deletion of the Head of LL](04-deletion-of-the-head-of-ll.md)

> [!abstract] Problem at a glance
> **Task:** Visit every node from the head and return the values in order.
> **Key insight:** Copy the head into a moving pointer `cur` and advance `cur = cur.next` until it is null. Never advance `head` itself if the caller still needs it.
> **Difficulty:** Easy · **Pattern:** Pointer walk
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/traversal-in-linked-list?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Iterative walk](#3-iterative-walk) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list, return a list of all node values from head to tail.

| Input | Output | Why |
|---|---|---|
| `1 → 2 → 3` | `[1, 2, 3]` |  |
| `null` | `[]` | empty list |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Iterative walk | cur = head; while cur: visit; cur = cur.next | O(n) | O(1) extra |

> [!tip] Interview angle
> Warm-up that checks you know the loop condition: `while cur` visits every node; `while cur.next` stops on the tail and is what you use when you need the last node itself.

---

## 3. Iterative walk

**Intuition.** A linked list has no indices — the only way to reach node `i` is to follow `i` next-pointers from the head. One pass, one pointer.

**Algorithm**

1. `cur = head`.
2. While `cur != null`: record `cur.val`, then `cur = cur.next`.

**Dry run** — 1→2→3: cur=1 rec 1 → cur=2 rec 2 → cur=3 rec 3 → cur=null stop.

**C++**
```cpp
vector<int> traverse(ListNode* head) {
    vector<int> out;
    for (ListNode* cur = head; cur; cur = cur->next) out.push_back(cur->val);
    return out;
}
```

**Java**
```java
static List<Integer> traverse(ListNode head) {
    List<Integer> out = new ArrayList<>();
    for (ListNode cur = head; cur != null; cur = cur.next) out.add(cur.val);
    return out;
}
```

**Python**
```python
def traverse(head):
    out, cur = [], head
    while cur:
        out.append(cur.val)
        cur = cur.next
    return out
```

**Complexity:** time **O(n)**, space **O(1) extra** — each node visited once.

---

## Edge cases

- Empty list → `[]`.
- Single node.
- Duplicate values — order still matters.

---

## Common mistakes

1. Moving `head` and losing the list.
2. `while cur.next` skips the tail's value.

---

## Follow-ups

1. Print recursively in reverse.
2. Traverse a circular list.

<details><summary>Answer sketches</summary>

**#1:** Recurse on `next` first, then visit — O(n) stack.

**#2:** Stop when `cur` returns to `head` (do-while).
</details>

---

## Flashcards

**Loop to visit every node?** #flashcard
`while cur:` — `while cur.next:` stops at the tail.

**Why copy head into cur?** #flashcard
So the caller's head pointer still points at the list.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
