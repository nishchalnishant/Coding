---
module: striver/19-linked-list
lesson: 41
topic: Sort LL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/sort-ll?category=faqs--hard&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, merge-sort, fast-slow]
---
# 41. Sort LL

← [Flattening of LL](40-flattening-of-ll.md) · [Part 19 index](README.md) · Next → [Clone a LL with Random and Next Pointer](42-clone-a-ll-with-random-and-next-pointer.md)

> [!abstract] Problem at a glance
> **Task:** Sort a linked list in O(n log n) time.
> **Key insight:** Merge sort is the natural fit: split at the **first** middle (fast/slow), sort halves recursively, merge. No random access needed, and merging lists needs no extra array.
> **Difficulty:** Medium · **Pattern:** Merge sort on list · **Also on:** 148
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sort-ll?category=faqs--hard&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Values to array](#3-values-to-array) · [4. Top-down merge sort](#4-top-down-merge-sort) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a linked list, return the list sorted in ascending order.

| Input | Output | Why |
|---|---|---|
| `4→2→1→3` | `1→2→3→4` |  |

**Constraints:** `0 ≤ n ≤ 5·10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Values to array | copy, sort, write back | O(n log n) | O(n) |
| Top-down merge sort | split at first middle; sort; merge | O(n log n) | O(log n) stack |

> [!tip] Interview angle
> Why not quicksort? Bad pivots on linked lists and no cheap random pivot. Why first middle? With the second middle, a 2-node list splits as 2 + 0 and recursion never terminates. Bottom-up merge sort gives true O(1) space.

---

## 3. Values to array

**Intuition.** Overwrites values; fine unless nodes must be relinked.

```python
def sort_list_arr(head):
    vals, t = [], head
    while t:
        vals.append(t.val)
        t = t.next
    vals.sort()
    t = head
    for v in vals:
        t.val, t = v, t.next
    return head
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. Top-down merge sort

**Intuition.** Fast/slow split + merge-two-sorted-lists.

**Algorithm**

1. Base: 0 or 1 node.
2. `mid` = first middle; `right = mid.next`; `mid.next = None`.
3. `merge(sort(head), sort(right))`.

**C++**
```cpp
ListNode* sortList(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode *slow = head, *fast = head->next;
    while (fast && fast->next) { slow = slow->next; fast = fast->next->next; }
    ListNode* right = slow->next;
    slow->next = nullptr;
    ListNode *a = sortList(head), *b = sortList(right);
    ListNode dummy;
    ListNode* t = &dummy;
    while (a && b) {
        if (a->val <= b->val) { t->next = a; a = a->next; }
        else { t->next = b; b = b->next; }
        t = t->next;
    }
    t->next = a ? a : b;
    return dummy.next;
}
```

**Java**
```java
static ListNode sortList(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode slow = head, fast = head.next;
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode right = slow.next;
    slow.next = null;
    ListNode a = sortList(head), b = sortList(right);
    ListNode dummy = new ListNode(), t = dummy;
    while (a != null && b != null) {
        if (a.val <= b.val) { t.next = a; a = a.next; }
        else { t.next = b; b = b.next; }
        t = t.next;
    }
    t.next = a != null ? a : b;
    return dummy.next;
}
```

**Python**
```python
def sort_list(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    right, slow.next = slow.next, None
    a, b = sort_list(head), sort_list(right)
    dummy = t = ListNode()
    while a and b:
        if a.val <= b.val:
            t.next, a = a, a.next
        else:
            t.next, b = b, b.next
        t = t.next
    t.next = a or b
    return dummy.next
```

**Complexity:** time **O(n log n)**, space **O(log n) stack** — O(n log n), stable, no array.

---

## Edge cases

- Empty / single.
- Duplicates.
- Already sorted / reversed.

---

## Common mistakes

1. Second middle split → infinite recursion on 2 nodes.
2. Not cutting `slow.next = None` before recursing.

---

## Follow-ups

1. O(1) extra space.
2. Insertion sort list (LC 147).

<details><summary>Answer sketches</summary>

**#1:** Bottom-up merge sort: merge runs of size 1, 2, 4, … iteratively.

**#2:** O(n²), dummy head, insert each node into the sorted prefix.
</details>

---

## Flashcards

**Why fast = head.next in list merge sort?** #flashcard
Gives the first middle so a 2-node list splits 1 + 1.

**Best sort for linked lists?** #flashcard
Merge sort — sequential access, O(1) merge space.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
