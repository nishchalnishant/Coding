---
module: striver/19-linked-list
lesson: 12
topic: Find the Length of the Linked List
difficulty: Easy
source: https://takeuforward.org/learning/dsa/find-the-length-of-the-linked-list?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, traversal]
---
# 12. Find the Length of the Linked List

← [Insertion Before the Value X in LL](11-insertion-before-the-value-x-in-ll.md) · [Part 19 index](README.md) · Next → [Search in Linked List](13-search-in-linked-list.md)

> [!abstract] Problem at a glance
> **Task:** Count the nodes.
> **Key insight:** Traverse and count. Many medium problems (rotate, remove n-th from end, intersection) start with this pass.
> **Difficulty:** Easy · **Pattern:** Pointer walk
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-the-length-of-the-linked-list?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive](#3-recursive) · [4. Iterative count](#4-iterative-count) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list, return the number of nodes.

| Input | Output | Why |
|---|---|---|
| `1→2→3` | `3` |  |
| `null` | `0` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive | 0 if null else 1 + len(next) | O(n) | O(n) stack |
| Iterative count | cnt++ per node | O(n) | O(1) |

> [!tip] Interview angle
> Trivial — but know both versions: iterative O(1) space, recursive `1 + len(next)` O(n) stack (overflows for 10⁵ nodes in Python).

---

## 3. Recursive

**Intuition.** Length of a list is one more than the length of its tail.

```python
def length_rec(head):
    return 0 if not head else 1 + length_rec(head.next)
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## 4. Iterative count

**Intuition.** Walk once, increment a counter.

**C++**
```cpp
int getLength(ListNode* head) {
    int cnt = 0;
    for (; head; head = head->next) cnt++;
    return cnt;
}
```

**Java**
```java
static int getLength(ListNode head) {
    int cnt = 0;
    for (; head != null; head = head.next) cnt++;
    return cnt;
}
```

**Python**
```python
def get_length(head):
    cnt = 0
    while head:
        cnt += 1
        head = head.next
    return cnt
```

**Complexity:** time **O(n)**, space **O(1)** — one pass.

---

## Edge cases

- Empty → 0.

---

## Common mistakes

1. Starting the count at 1 and double counting on empty lists.

---

## Follow-ups

1. Length of a list that may contain a cycle.

<details><summary>Answer sketches</summary>

**#1:** Detect the cycle first (Floyd); the infinite loop otherwise never ends.
</details>

---

## Flashcards

**Recursive length space?** #flashcard
O(n) call stack.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
