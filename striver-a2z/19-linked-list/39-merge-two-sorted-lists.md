---
module: striver-a2z/19-linked-list
lesson: 39
topic: Merge Two Sorted Lists
difficulty: Easy
source: https://takeuforward.org/learning/dsa/merge-sorted-lists-?category=faqs--hard&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, merge]
---
# 39. Merge Two Sorted Lists

← [Rotate a LL](38-rotate-a-ll.md) · [Part 19 index](README.md) · Next → [Flattening of LL](40-flattening-of-ll.md)

> [!abstract] Problem at a glance
> **Task:** Splice two sorted lists into one sorted list.
> **Key insight:** Dummy node + tail pointer; attach the smaller head each step; attach the leftover list in one go at the end.
> **Difficulty:** Easy · **Pattern:** Dummy head merge · **Also on:** 21
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/merge-sorted-lists-?category=faqs--hard&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Collect, sort, rebuild](#3-collect-sort-rebuild) · [4. Recursive](#4-recursive) · [5. Dummy + tail splice](#5-dummy--tail-splice) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the heads of two sorted linked lists `list1` and `list2`, merge them into one sorted list by splicing their nodes, and return its head.

| Input | Output | Why |
|---|---|---|
| `1→2→4, 1→3→4` | `1→1→2→3→4→4` |  |
| `[], [0]` | `0` |  |

**Constraints:** `0 ≤ n, m ≤ 50`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Collect, sort, rebuild | values → sort → new list | O((n+m) log(n+m)) | O(n+m) |
| Recursive | smaller.next = merge(smaller.next, other) | O(n+m) | O(n+m) stack |
| Dummy + tail splice | attach smaller; advance; append leftover | O(n+m) | O(1) |

> [!tip] Interview angle
> The building block for Sort List, Merge K Lists, and Flattening. Use `<=` to keep it stable.

---

## 3. Collect, sort, rebuild

**Intuition.** Ignores sortedness; baseline only.

```python
def merge_brute(a, b):
    vals = []
    for h in (a, b):
        while h:
            vals.append(h.val)
            h = h.next
    dummy = t = ListNode()
    for v in sorted(vals):
        t.next = ListNode(v)
        t = t.next
    return dummy.next
```

**Complexity:** time **O((n+m) log(n+m))**, space **O(n+m)**.

---

## 4. Recursive

**Intuition.** The smaller head is the answer's head; the rest is a smaller merge.

```python
def merge_rec(a, b):
    if not a or not b:
        return a or b
    if a.val <= b.val:
        a.next = merge_rec(a.next, b)
        return a
    b.next = merge_rec(a, b.next)
    return b
```

**Complexity:** time **O(n+m)**, space **O(n+m) stack**.

---

## 5. Dummy + tail splice

**Intuition.** No new nodes — only relinks.

**C++**
```cpp
ListNode* mergeTwoLists(ListNode* a, ListNode* b) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (a && b) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = a ? a : b;
    return dummy.next;
}
```

**Java**
```java
static ListNode mergeTwoLists(ListNode a, ListNode b) {
    ListNode dummy = new ListNode(), tail = dummy;
    while (a != null && b != null) {
        if (a.val <= b.val) { tail.next = a; a = a.next; }
        else { tail.next = b; b = b.next; }
        tail = tail.next;
    }
    tail.next = a != null ? a : b;
    return dummy.next;
}
```

**Python**
```python
def merge_two_lists(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
```

**Complexity:** time **O(n+m)**, space **O(1)** — single pass, O(1) extra.

---

## Edge cases

- Either / both empty.
- All of one list smaller than the other.

---

## Common mistakes

1. Looping until both are null instead of appending the remainder.
2. Forgetting `tail = tail.next`.

---

## Follow-ups

1. Merge k sorted lists (LC 23).

<details><summary>Answer sketches</summary>

**#1:** Min-heap of heads → O(N log k), or pairwise divide & conquer.
</details>

---

## Flashcards

**Merge two sorted lists in O(1) space?** #flashcard
Dummy + tail; splice the smaller head; attach the leftover.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
