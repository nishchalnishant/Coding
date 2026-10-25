---
module: striver-a2z/19-linked-list
lesson: 37
topic: Reverse LL in Group of Given Size K
difficulty: Hard
source: https://takeuforward.org/learning/dsa/reverse-ll-in-group-of-given-size-k?category=faqs--hard&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, reversal]
---
# 37. Reverse LL in Group of Given Size K

← [Length of Loop in LL](36-length-of-loop-in-ll.md) · [Part 19 index](README.md) · Next → [Rotate a LL](38-rotate-a-ll.md)

> [!abstract] Problem at a glance
> **Task:** Reverse every block of k nodes; a final block shorter than k stays as is.
> **Key insight:** Loop: find the k-th node from the current group start (null → stop). Detach the group, reverse it, then reconnect: previous group's tail → new head, old head (now tail) → next group. Track `prev_tail`.
> **Difficulty:** Hard · **Pattern:** Reverse sublist + reconnect · **Also on:** 25
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-ll-in-group-of-given-size-k?category=faqs--hard&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive](#3-recursive) · [4. Iterative with k-th node finder](#4-iterative-with-k-th-node-finder) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a linked list and an integer `k`, reverse the nodes `k` at a time and return the modified list. Nodes left over at the end (fewer than k) remain in order. Only node links may change.

| Input | Output | Why |
|---|---|---|
| `1→2→3→4→5, k = 2` | `2→1→4→3→5` |  |
| `1→2→3→4→5, k = 3` | `3→2→1→4→5` | leftover 4→5 untouched |

**Constraints:** `1 ≤ k ≤ n ≤ 5000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive | check k nodes exist; reverse k; head.next = recurse(rest) | O(n) | O(n/k) stack |
| Iterative with k-th node finder | kth = walk k−1; detach; reverse; reconnect | O(n) | O(1) |

> [!tip] Interview angle
> This is all bookkeeping — name the four pointers aloud (group start, k-th node, next group, prev tail) and draw one group before coding. A dummy head removes the "first group" special case.

---

## 3. Recursive

**Intuition.** After reversing the first k nodes, the original head becomes the group's tail; attach the recursively processed remainder to it.

```python
def reverse_k_rec(head, k):
    cur, cnt = head, 0
    while cur and cnt < k:
        cur, cnt = cur.next, cnt + 1
    if cnt < k:
        return head
    prev, cur = reverse_k_rec(cur, k), head
    for _ in range(k):
        cur.next, prev, cur = prev, cur, cur.next
    return prev
```

**Complexity:** time **O(n)**, space **O(n/k) stack**.

---

## 4. Iterative with k-th node finder

**Intuition.** Each group is visited twice (find + reverse).

**Algorithm**

1. `temp` = group start; `kth = get_kth(temp, k)`; if null, attach `temp` to `prev_tail` and stop.
2. `nxt = kth.next`; `kth.next = None` (detach).
3. `reverse(temp)` → new head is `kth`.
4. If first group, `head = kth`, else `prev_tail.next = kth`.
5. `prev_tail = temp`; `temp = nxt`.

**Dry run** — 1→2→3→4→5, k=2: group [1,2] → 2→1, head=2, prev_tail=1. Group [3,4] → 4→3, 1.next=4, prev_tail=3. Group [5]: kth null → 3.next=5. Result 2→1→4→3→5.

**C++**
```cpp
ListNode* revList(ListNode* h) {
    ListNode* p = nullptr;
    while (h) { ListNode* n = h->next; h->next = p; p = h; h = n; }
    return p;
}
ListNode* kthNode(ListNode* t, int k) {
    while (t && --k) t = t->next;
    return t;
}
ListNode* reverseKGroup(ListNode* head, int k) {
    ListNode *temp = head, *prevTail = nullptr;
    while (temp) {
        ListNode* kth = kthNode(temp, k);
        if (!kth) { if (prevTail) prevTail->next = temp; break; }
        ListNode* nxt = kth->next;
        kth->next = nullptr;
        revList(temp);
        if (temp == head) head = kth; else prevTail->next = kth;
        prevTail = temp;
        temp = nxt;
    }
    return head;
}
```

**Java**
```java
static ListNode revList(ListNode h) {
    ListNode p = null;
    while (h != null) { ListNode n = h.next; h.next = p; p = h; h = n; }
    return p;
}
static ListNode kthNode(ListNode t, int k) {
    while (t != null && --k > 0) t = t.next;
    return t;
}
static ListNode reverseKGroup(ListNode head, int k) {
    ListNode temp = head, prevTail = null;
    while (temp != null) {
        ListNode kth = kthNode(temp, k);
        if (kth == null) { if (prevTail != null) prevTail.next = temp; break; }
        ListNode nxt = kth.next;
        kth.next = null;
        revList(temp);
        if (temp == head) head = kth; else prevTail.next = kth;
        prevTail = temp;
        temp = nxt;
    }
    return head;
}
```

**Python**
```python
def reverse_k_group(head, k):
    def kth_node(t, k):
        k -= 1
        while t and k:
            t, k = t.next, k - 1
        return t
    def rev(h):
        p = None
        while h:
            h.next, p, h = p, h, h.next
        return p
    temp, prev_tail = head, None
    while temp:
        kth = kth_node(temp, k)
        if not kth:
            if prev_tail:
                prev_tail.next = temp
            break
        nxt = kth.next
        kth.next = None
        rev(temp)
        if temp is head:
            head = kth
        else:
            prev_tail.next = kth
        prev_tail, temp = temp, nxt
    return head
```

**Complexity:** time **O(n)**, space **O(1)** — O(1) extra; each node touched ≤ 2×.

---

## Edge cases

- k = 1 → unchanged.
- k = n → full reverse.
- n not a multiple of k → tail untouched.

---

## Common mistakes

1. Reversing the short leftover group.
2. Forgetting to link the last reversed tail to the leftover.
3. Losing `nxt` before detaching.

---

## Follow-ups

1. Reverse the leftover too.
2. Reverse between positions l and r (LC 92).

<details><summary>Answer sketches</summary>

**#1:** Drop the null check — reverse whatever remains.

**#2:** Same detach/reverse/reconnect, once.
</details>

---

## Flashcards

**Four pointers in reverse-k-group?** #flashcard
group start (temp), k-th node, next group (nxt), previous group tail.

**After reversing a group, which node becomes its tail?** #flashcard
The original group start (`temp`).

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
