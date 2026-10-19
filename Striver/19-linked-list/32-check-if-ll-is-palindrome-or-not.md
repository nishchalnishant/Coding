---
module: striver/19-linked-list
lesson: 32
topic: Check if LL is Palindrome or Not
difficulty: Medium
source: https://takeuforward.org/learning/dsa/check-if-ll-is-palindrome-or-not?category=faqs--medium&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, fast-slow, reversal]
---
# 32. Check if LL is Palindrome or Not

← [Delete the Middle Node in LL](31-delete-the-middle-node-in-ll.md) · [Part 19 index](README.md) · Next → [Find the Intersection Point of Y LL](33-find-the-intersection-point-of-y-ll.md)

> [!abstract] Problem at a glance
> **Task:** Return whether the list reads the same forwards and backwards, in O(1) extra space.
> **Key insight:** Find the middle, reverse the second half, compare the halves node by node, then (politely) reverse it back. Combines the two core primitives.
> **Difficulty:** Medium · **Pattern:** Middle + reverse half · **Also on:** 234
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-ll-is-palindrome-or-not?category=faqs--medium&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Copy to array](#3-copy-to-array) · [4. Reverse second half](#4-reverse-second-half) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a singly linked list, return `true` if it is a palindrome.

| Input | Output | Why |
|---|---|---|
| `1→2→2→1` | `true` |  |
| `1→2` | `false` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Copy to array | vals == vals[::-1] | O(n) | O(n) |
| Reverse second half | first middle → reverse after it → compare → restore | O(n) | O(1) |

> [!tip] Interview angle
> Start with the stack/array version (O(n) space), then the O(1) version. Mention restoring the list — modifying input silently is a code-review red flag.

---

## 3. Copy to array

**Intuition.** Random access makes it trivial.

```python
def is_palindrome_arr(head):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    return vals == vals[::-1]
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Reverse second half

**Intuition.** Use the **first** middle so the second half is never longer than the first; compare until the second half runs out.

**Algorithm**

1. `slow` = first middle (`while fast.next and fast.next.next`).
2. `second = reverse(slow.next)`.
3. Walk `p = head`, `q = second`, compare values.
4. `slow.next = reverse(second)` to restore.

**C++**
```cpp
ListNode* rev(ListNode* h) {
    ListNode* p = nullptr;
    while (h) { ListNode* n = h->next; h->next = p; p = h; h = n; }
    return p;
}
bool isPalindrome(ListNode* head) {
    if (!head || !head->next) return true;
    ListNode *slow = head, *fast = head;
    while (fast->next && fast->next->next) { slow = slow->next; fast = fast->next->next; }
    ListNode* second = rev(slow->next);
    bool ok = true;
    for (ListNode *p = head, *q = second; q; p = p->next, q = q->next)
        if (p->val != q->val) { ok = false; break; }
    slow->next = rev(second);
    return ok;
}
```

**Java**
```java
static ListNode rev(ListNode h) {
    ListNode p = null;
    while (h != null) { ListNode n = h.next; h.next = p; p = h; h = n; }
    return p;
}
static boolean isPalindrome(ListNode head) {
    if (head == null || head.next == null) return true;
    ListNode slow = head, fast = head;
    while (fast.next != null && fast.next.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode second = rev(slow.next);
    boolean ok = true;
    for (ListNode p = head, q = second; q != null; p = p.next, q = q.next)
        if (p.val != q.val) { ok = false; break; }
    slow.next = rev(second);
    return ok;
}
```

**Python**
```python
def is_palindrome(head):
    if not head or not head.next:
        return True
    def rev(h):
        p = None
        while h:
            h.next, p, h = p, h, h.next
        return p
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    second = rev(slow.next)
    p, q, ok = head, second, True
    while q:
        if p.val != q.val:
            ok = False
            break
        p, q = p.next, q.next
    slow.next = rev(second)
    return ok
```

**Complexity:** time **O(n)**, space **O(1)** — three linear passes, O(1) extra.

---

## Edge cases

- Odd length (middle ignored).
- Single node.
- Two nodes.

---

## Common mistakes

1. Using the second middle — odd lengths then compare the middle against nothing, fine, but even lengths misalign if you also iterate the first half fully.
2. Not restoring the list.

---

## Follow-ups

1. Recursive O(n)-stack version.
2. Reorder list L0→Ln→L1→Ln−1 (LC 143).

<details><summary>Answer sketches</summary>

**#1:** Keep a `front` pointer outside; recursion compares on unwind.

**#2:** Same split + reverse, then merge alternately.
</details>

---

## Flashcards

**O(1) palindrome check on a linked list?** #flashcard
Middle → reverse second half → compare → reverse back.

**Which middle for palindrome split?** #flashcard
First middle; compare while the second half has nodes.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
