---
module: striver/19-linked-list
lesson: 45
topic: Find Pairs with Given Sum in DLL
difficulty: Medium
source: https://takeuforward.org/learning/dsa/find-pairs-with-given-sum-in-doubly-linked-list?category=faqs--dll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, doubly-linked-list, two-pointers]
---
# 45. Find Pairs with Given Sum in DLL

← [Remove Duplicates from Sorted DLL](44-remove-duplicates-from-sorted-dll.md) · [Part 19 index](README.md) · Next → [Part 20: Bit Manipulation](../20-bit-manipulation/README.md)

> [!abstract] Problem at a glance
> **Task:** Sorted DLL of distinct values: list all pairs (a, b), a < b, with a + b = target, ordered by a.
> **Key insight:** Two pointers from both ends — exactly the sorted-array 2-sum — because a DLL can walk backward. Stop when the pointers meet or cross.
> **Difficulty:** Medium · **Pattern:** Two pointers (opposite ends)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-pairs-with-given-sum-in-doubly-linked-list?category=faqs--dll&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash set](#3-hash-set) · [4. Two pointers from both ends](#4-two-pointers-from-both-ends) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `head` of a sorted doubly linked list of distinct positive integers and a `target`, return all pairs whose sum equals `target`, in increasing order of the first element.

| Input | Output | Why |
|---|---|---|
| `1⇄2⇄4⇄5⇄6⇄8⇄9, target 7` | `(1,6), (2,5)` |  |
| `1⇄2⇄3, target 10` | `[]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash set | for each x: target − x seen? | O(n) | O(n) |
| Two pointers from both ends | sum < t → left++; > t → right--; = → record, move both | O(n) | O(1) |

> [!tip] Interview angle
> Point out that `prev` is what makes the O(1)-space version possible; on a singly list you'd need a hash set or reverse a half. Stop condition: `left is not right and right.next is not left` (or compare values since distinct).

---

## 3. Hash set

**Intuition.** Each pair is found at its larger element; sort at the end to order by the smaller one.

```python
def pairs_set(head, target):
    seen, res = set(), []
    while head:
        if target - head.val in seen:
            res.append((target - head.val, head.val))
        seen.add(head.val)
        head = head.next
    return sorted(res)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Two pointers from both ends

**Intuition.** Sorted order: increasing left raises the sum, decreasing right lowers it. Distinct values ⇒ `left.val < right.val` is the loop guard.

**C++**
```cpp
vector<pair<int,int>> findPairsWithGivenSum(Node* head, int target) {
    vector<pair<int,int>> res;
    if (!head) return res;
    Node *left = head, *right = head;
    while (right->next) right = right->next;
    while (left->val < right->val) {
        int s = left->val + right->val;
        if (s == target) { res.push_back({left->val, right->val}); left = left->next; right = right->prev; }
        else if (s < target) left = left->next;
        else right = right->prev;
    }
    return res;
}
```

**Java**
```java
static List<int[]> findPairsWithGivenSum(Node head, int target) {
    List<int[]> res = new ArrayList<>();
    if (head == null) return res;
    Node left = head, right = head;
    while (right.next != null) right = right.next;
    while (left.val < right.val) {
        int s = left.val + right.val;
        if (s == target) { res.add(new int[]{left.val, right.val}); left = left.next; right = right.prev; }
        else if (s < target) left = left.next;
        else right = right.prev;
    }
    return res;
}
```

**Python**
```python
def find_pairs_with_given_sum(head, target):
    res = []
    if not head:
        return res
    left = right = head
    while right.next:
        right = right.next
    while left.val < right.val:
        s = left.val + right.val
        if s == target:
            res.append((left.val, right.val))
            left, right = left.next, right.prev
        elif s < target:
            left = left.next
        else:
            right = right.prev
    return res
```

**Complexity:** time **O(n)**, space **O(1)** — O(n): one walk to the tail + one two-pointer sweep.

---

## Edge cases

- No pairs.
- Single node.
- Pair uses adjacent nodes.

---

## Common mistakes

1. Loop guard `left is not right` alone — after moving both on a match they can cross and continue.
2. Not finding the tail first.

---

## Follow-ups

1. Triplets with given sum in sorted DLL.
2. Values not distinct.

<details><summary>Answer sketches</summary>

**#1:** Fix one node, two-pointer the rest → O(n²).

**#2:** Guard with node identity: stop when `left is right` or `left.prev is right`.
</details>

---

## Flashcards

**Why can a DLL do sorted 2-sum in O(1) space?** #flashcard
`prev` lets the right pointer walk backward.

**Loop guard with distinct values?** #flashcard
`left.val < right.val`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
