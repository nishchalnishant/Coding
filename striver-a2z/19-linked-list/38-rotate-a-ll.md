---
module: striver-a2z/19-linked-list
lesson: 38
topic: Rotate a LL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/rotate-a-ll?category=faqs--hard&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list]
---
# 38. Rotate a LL

← [Reverse LL in Group of Given Size K](37-reverse-ll-in-group-of-given-size-k.md) · [Part 19 index](README.md) · Next → [Merge Two Sorted Lists](39-merge-two-sorted-lists.md)

> [!abstract] Problem at a glance
> **Task:** Rotate the list right by k places.
> **Key insight:** k %= n. Make it a ring (tail.next = head), walk to the new tail at index n − k − 1, cut after it. Never rotate k times one step at a time.
> **Difficulty:** Medium · **Pattern:** Length + ring + cut · **Also on:** 61
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/rotate-a-ll?category=faqs--hard&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Rotate one step k times](#3-rotate-one-step-k-times) · [4. Ring and cut](#4-ring-and-cut) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a linked list, rotate the list to the right by `k` places.

| Input | Output | Why |
|---|---|---|
| `1→2→3→4→5, k = 2` | `4→5→1→2→3` |  |
| `0→1→2, k = 4` | `2→0→1` | k mod 3 = 1 |

**Constraints:** `0 ≤ n ≤ 500`, `0 ≤ k ≤ 2·10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Rotate one step k times | move tail to front, k mod n times | O(n · (k mod n)) | O(1) |
| Ring and cut | tail.next = head; walk n − k%n − 1; cut | O(n) | O(1) |

> [!tip] Interview angle
> k can be 2·10⁹ — saying "k mod n" up front is the signal. The ring trick avoids a separate re-attach step.

---

## 3. Rotate one step k times

**Intuition.** Each step: find second-last, detach tail, put it in front.

```python
def rotate_brute(head, k):
    if not head or not head.next:
        return head
    n, t = 0, head
    while t:
        n, t = n + 1, t.next
    for _ in range(k % n):
        prev, cur = None, head
        while cur.next:
            prev, cur = cur, cur.next
        prev.next, cur.next, head = None, head, cur
    return head
```

**Complexity:** time **O(n · (k mod n))**, space **O(1)**.

---

## 4. Ring and cut

**Intuition.** Rotating right by k means the last k nodes come first; the new tail is at index n − k − 1.

**C++**
```cpp
ListNode* rotateRight(ListNode* head, int k) {
    if (!head || !head->next) return head;
    int n = 1;
    ListNode* tail = head;
    while (tail->next) { tail = tail->next; n++; }
    k %= n;
    if (k == 0) return head;
    tail->next = head;
    ListNode* nt = head;
    for (int i = 0; i < n - k - 1; i++) nt = nt->next;
    head = nt->next;
    nt->next = nullptr;
    return head;
}
```

**Java**
```java
static ListNode rotateRight(ListNode head, int k) {
    if (head == null || head.next == null) return head;
    int n = 1;
    ListNode tail = head;
    while (tail.next != null) { tail = tail.next; n++; }
    k %= n;
    if (k == 0) return head;
    tail.next = head;
    ListNode nt = head;
    for (int i = 0; i < n - k - 1; i++) nt = nt.next;
    head = nt.next;
    nt.next = null;
    return head;
}
```

**Python**
```python
def rotate_right(head, k):
    if not head or not head.next:
        return head
    n, tail = 1, head
    while tail.next:
        n, tail = n + 1, tail.next
    k %= n
    if k == 0:
        return head
    tail.next = head
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next
    head, new_tail.next = new_tail.next, None
    return head
```

**Complexity:** time **O(n)**, space **O(1)** — two passes regardless of k.

---

## Edge cases

- Empty / single node.
- k multiple of n → unchanged.
- k ≫ n.

---

## Common mistakes

1. Not reducing k mod n → TLE.
2. Forming the ring when k % n == 0 and forgetting to break it.

---

## Follow-ups

1. Rotate left by k.

<details><summary>Answer sketches</summary>

**#1:** Rotate right by n − k%n.
</details>

---

## Flashcards

**Index of the new tail when rotating right by k?** #flashcard
n − (k mod n) − 1.

**Rotate-list trick to avoid re-attaching?** #flashcard
Link tail→head into a ring, then cut at the new tail.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
