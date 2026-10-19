---
module: striver/19-linked-list
lesson: 14
topic: Convert Array to DLL
difficulty: Easy
source: https://takeuforward.org/learning/dsa/convert-array-to-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet
tags: [striver, linked-list, doubly-linked-list, construction]
---
# 14. Convert Array to DLL

← [Search in Linked List](13-search-in-linked-list.md) · [Part 19 index](README.md) · Next → [Delete Head of DLL](15-delete-head-of-dll.md)

> [!abstract] Problem at a glance
> **Task:** Build a doubly linked list from an array; return its head.
> **Key insight:** Keep a `tail`; each new node gets `prev = tail`, then `tail.next = node; tail = node`. Two links per node, both set at creation.
> **Difficulty:** Easy · **Pattern:** Tail-append build
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/convert-array-to-dll?category=fundamentals-doubly-ll&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Tail pointer](#3-tail-pointer) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `arr`, build a doubly linked list containing its elements in order and return the head.

| Input | Output | Why |
|---|---|---|
| `[1, 2, 3]` | `1⇄2⇄3` |  |
| `[]` | `null` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Tail pointer | node(prev = tail); tail.next = node; tail = node | O(n) | O(n) output |

> [!tip] Interview angle
> Say the invariant out loud: after each step, `tail.next == null` and every `node.next.prev == node`. Interviewers watch for the forgotten `prev`.

---

## 3. Tail pointer

**Intuition.** Same as the singly build, but every new node also points back at the tail.

**C++**
```cpp
Node* arrayToDLL(const vector<int>& arr) {
    if (arr.empty()) return nullptr;
    Node* head = new Node(arr[0]);
    Node* tail = head;
    for (size_t i = 1; i < arr.size(); i++) {
        Node* node = new Node(arr[i], nullptr, tail);
        tail->next = node;
        tail = node;
    }
    return head;
}
```

**Java**
```java
static Node arrayToDLL(int[] arr) {
    if (arr.length == 0) return null;
    Node head = new Node(arr[0]), tail = head;
    for (int i = 1; i < arr.length; i++) {
        Node node = new Node(arr[i], null, tail);
        tail.next = node;
        tail = node;
    }
    return head;
}
```

**Python**
```python
def array_to_dll(arr):
    if not arr:
        return None
    head = tail = Node(arr[0])
    for v in arr[1:]:
        node = Node(v, None, tail)
        tail.next = node
        tail = node
    return head
```

**Complexity:** time **O(n)**, space **O(n) output** — one node per element.

---

## Edge cases

- Empty array → null.
- Single element: both links null.

---

## Common mistakes

1. Setting `tail.next` but not `node.prev` — forward traversal works, backward breaks.

---

## Follow-ups

1. Build a circular DLL.

<details><summary>Answer sketches</summary>

**#1:** After the loop: `tail.next = head; head.prev = tail`.
</details>

---

## Flashcards

**Two links set per appended DLL node?** #flashcard
`node.prev = tail` and `tail.next = node`.

**Interview track →** [Linked-list deep-dive](../../01-data-structures/07-linked-list.md) · [Linked-list walkthroughs](../../coding/data-structures/07-linked-list.md)
