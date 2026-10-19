---
module: striver/19-linked-list
lesson: 36
topic: Length of Loop in LL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/length-of-loop-in-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, linked-list, fast-slow, cycle]
---
# 36. Length of Loop in LL

← [Find the Starting Point in LL](35-find-the-starting-point-in-ll.md) · [Part 19 index](README.md) · Next → [Reverse LL in Group of Given Size K](37-reverse-ll-in-group-of-given-size-k.md)

> [!abstract] Problem at a glance
> **Task:** Return the number of nodes in the cycle, or 0 if none.
> **Key insight:** Floyd's meeting point is inside the cycle; keep one pointer there and walk the other around until it returns, counting steps.
> **Difficulty:** Easy · **Pattern:** Floyd cycle detection
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/length-of-loop-in-ll?category=faqs--medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Map node → step index](#3-map-node--step-index) · [4. Floyd + one lap](#4-floyd--one-lap) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `head`, return the length of the loop if the list contains one, else 0.

| Input | Output | Why |
|---|---|---|
| `1→2→3→4→5 → back to 2` | `4` |  |
| `1→2→3` | `0` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Map node → step index | on revisit: i − first[i] | O(n) | O(n) |
| Floyd + one lap | meet; walk until back at meeting point | O(n) | O(1) |

> [!tip] Interview angle
> Same Floyd phase 1, different phase 2. Alternative: hash map node → index; on revisit, length = current index − stored index.

---

## 3. Map node → step index

**Intuition.** Timestamps: the gap between first and second visits is the loop length.

```python
def loop_length_map(head):
    first, i = {}, 0
    while head:
        if id(head) in first:
            return i - first[id(head)]
        first[id(head)] = i
        i += 1
        head = head.next
    return 0
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Floyd + one lap

**Intuition.** Any node inside the cycle returns to itself after exactly C steps.

**C++**
```cpp
int lengthOfLoop(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            int cnt = 1;
            for (ListNode* c = slow->next; c != slow; c = c->next) cnt++;
            return cnt;
        }
    }
    return 0;
}
```

**Java**
```java
static int lengthOfLoop(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            int cnt = 1;
            for (ListNode c = slow.next; c != slow; c = c.next) cnt++;
            return cnt;
        }
    }
    return 0;
}
```

**Python**
```python
def length_of_loop(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            cnt, cur = 1, slow.next
            while cur is not slow:
                cnt, cur = cnt + 1, cur.next
            return cnt
    return 0
```

**Complexity:** time **O(n)**, space **O(1)** — detect O(n) + one lap O(C).

---

## Edge cases

- Self-loop → 1.
- No loop → 0.

---

## Common mistakes

1. Starting count at 0 with `cur = slow` and loop `while cur is not slow` — never enters.

---

## Follow-ups

1. Total distinct nodes in a cyclic list.

<details><summary>Answer sketches</summary>

**#1:** L + C: loop start distance plus loop length.
</details>

---

## Flashcards

**Loop length after Floyd meets?** #flashcard
Hold one pointer, walk the other one lap, count.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
