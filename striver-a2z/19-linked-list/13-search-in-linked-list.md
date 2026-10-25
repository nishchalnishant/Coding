---
module: striver-a2z/19-linked-list
lesson: 13
topic: Search in Linked List
difficulty: Easy
source: https://takeuforward.org/learning/dsa/search-in-linked-list?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, search]
---
# 13. Search in Linked List

← [Find the Length of the Linked List](12-find-the-length-of-the-linked-list.md) · [Part 19 index](README.md) · Next → [Convert Array to DLL](14-convert-array-to-dll.md)

> [!abstract] Problem at a glance
> **Task:** Return whether `key` occurs in the list.
> **Key insight:** Linear scan with early exit. No binary search on linked lists, even sorted ones — there's no O(1) access to the middle.
> **Difficulty:** Easy · **Pattern:** Pointer walk
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/search-in-linked-list?category=fundamentals-single-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear scan](#3-linear-scan) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list and an integer `key`, return `true` if some node holds `key`.

| Input | Output | Why |
|---|---|---|
| `1→2→3, key = 2` | `true` |  |
| `1→2→3, key = 4` | `false` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear scan | return true on match | O(n) | O(1) |

> [!tip] Interview angle
> Follow-up you may get: "can you binary search a sorted linked list?" — no, finding the middle costs O(n), so the total is O(n log n) without benefit. Skip lists add express lanes to make it O(log n).

---

## 3. Linear scan

**Intuition.** Compare each node's value; stop at the first match.

**C++**
```cpp
bool searchKey(ListNode* head, int key) {
    for (; head; head = head->next)
        if (head->val == key) return true;
    return false;
}
```

**Java**
```java
static boolean searchKey(ListNode head, int key) {
    for (; head != null; head = head.next)
        if (head.val == key) return true;
    return false;
}
```

**Python**
```python
def search_key(head, key):
    while head:
        if head.val == key:
            return True
        head = head.next
    return False
```

**Complexity:** time **O(n)**, space **O(1)** — worst case visits all nodes.

---

## Edge cases

- Empty list → false.
- Key at head or tail.

---

## Common mistakes

1. Returning false inside the loop on the first mismatch.

---

## Follow-ups

1. Return the index of the key.

<details><summary>Answer sketches</summary>

**#1:** Keep a counter; return −1 if not found.
</details>

---

## Flashcards

**Binary search on a sorted linked list?** #flashcard
No — reaching the middle is O(n). Skip lists solve this.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
