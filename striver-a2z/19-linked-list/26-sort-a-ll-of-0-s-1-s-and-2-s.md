---
module: striver-a2z/19-linked-list
lesson: 26
topic: Sort a LL of 0's, 1's and 2's
difficulty: Medium
source: https://takeuforward.org/learning/dsa/sort-a-ll-of-0's-1's-and-2's?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, partition, dummy-node]
---
# 26. Sort a LL of 0's, 1's and 2's

← [Segregate Odd and Even Nodes in LL](25-segregate-odd-and-even-nodes-in-ll.md) · [Part 19 index](README.md) · Next → [Remove Nth Node from the Back of the LL](27-remove-nth-node-from-the-back-of-the-ll.md)

> [!abstract] Problem at a glance
> **Task:** Sort a list containing only 0, 1, 2 in one pass by relinking.
> **Key insight:** Three dummy-headed chains (zeros, ones, twos); append each node to its chain, then join `zero → one → two`. Join carefully: if the ones chain is empty, zeros link straight to twos.
> **Difficulty:** Medium · **Pattern:** Partition into chains
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sort-a-ll-of-0's-1's-and-2's?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Count and overwrite](#3-count-and-overwrite) · [4. Three chains](#4-three-chains) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a linked list whose values are 0, 1 or 2, sort it and return the head.

| Input | Output | Why |
|---|---|---|
| `1→0→2→1→0→2→1` | `0→0→1→1→1→2→2` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Count and overwrite | count 0/1/2, rewrite values | O(n) | O(1) |
| Three chains | append to zero/one/two dummies; join; cut tail | O(n) | O(1) |

> [!tip] Interview angle
> Counting (two passes, rewrite values) is acceptable and simple — mention it, then do the one-pass relink. The tricky line is the join: `zt.next = oneH.next or twoH.next`.

---

## 3. Count and overwrite

**Intuition.** Two passes; modifies data rather than links.

```python
def sort012_count(head):
    cnt, cur = [0, 0, 0], head
    while cur:
        cnt[cur.val] += 1
        cur = cur.next
    cur = head
    for v in range(3):
        for _ in range(cnt[v]):
            cur.val = v
            cur = cur.next
    return head
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Three chains

**Intuition.** Stable partition with three tails. Terminate the two-chain to avoid a stale `next`.

**C++**
```cpp
ListNode* sortList012(ListNode* head) {
    ListNode h[3], *t[3] = {&h[0], &h[1], &h[2]};
    for (; head; head = head->next) t[head->val] = t[head->val]->next = head;
    t[0]->next = h[1].next ? h[1].next : h[2].next;
    t[1]->next = h[2].next;
    t[2]->next = nullptr;
    return h[0].next ? h[0].next : h[1].next ? h[1].next : h[2].next;
}
```

**Java**
```java
static ListNode sortList012(ListNode head) {
    ListNode[] h = {new ListNode(), new ListNode(), new ListNode()};
    ListNode[] t = {h[0], h[1], h[2]};
    for (; head != null; head = head.next) { t[head.val].next = head; t[head.val] = head; }
    t[0].next = h[1].next != null ? h[1].next : h[2].next;
    t[1].next = h[2].next;
    t[2].next = null;
    return h[0].next != null ? h[0].next : h[1].next != null ? h[1].next : h[2].next;
}
```

**Python**
```python
def sort_list012(head):
    heads = [ListNode() for _ in range(3)]
    tails = heads[:]
    while head:
        tails[head.val].next = head
        tails[head.val] = head
        head = head.next
    tails[0].next = heads[1].next or heads[2].next
    tails[1].next = heads[2].next
    tails[2].next = None
    return heads[0].next or heads[1].next or heads[2].next
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, relinks only.

---

## Edge cases

- Some colours missing (e.g. no 1s).
- Empty list.

---

## Common mistakes

1. `zeroTail.next = oneHead.next` when there are no ones → twos lost.
2. Not nulling the last tail → cycle.

---

## Follow-ups

1. Partition list around x (LC 86).

<details><summary>Answer sketches</summary>

**#1:** Two chains: < x and ≥ x, then join.
</details>

---

## Flashcards

**Why null the final tail in chain partitioning?** #flashcard
Its old `next` may point back into an earlier chain → cycle.

**Join zeros to what if no ones?** #flashcard
Directly to the twos chain.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../04-practice/data-structures/07-linked-list.md)
