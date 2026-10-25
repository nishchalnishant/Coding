---
module: striver-a2z/26-heaps
lesson: 12
topic: Merge K sorted Lists
difficulty: Hard
source: https://takeuforward.org/learning/dsa/merge-k-sorted-lists?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, heaps, heap, linked-list, k-way-merge]
---
# 12. Merge K sorted Lists

← [Sort K sorted array](11-sort-k-sorted-array.md) · [Part 26 index](README.md) · Next → [Replace elements by its rank in the array](13-replace-elements-by-rank.md)

> [!abstract] Problem at a glance
> **Task:** Merge `k` sorted linked lists into one sorted list.
> **Key insight:** The next output node is the smallest of the k current heads. A min-heap of heads gives it in O(log k): pop the min, append it, push its `next`. Total O(N log k) for N nodes. Divide-and-conquer pairwise merging gets the same bound with O(1) extra space.
> **Difficulty:** Hard · **Pattern:** K-way merge (heap of heads) · **Also on:** [LC 23](https://leetcode.com/problems/merge-k-sorted-lists/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/merge-k-sorted-lists?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Collect and sort](#3-collect-and-sort) · [4. Divide and conquer](#4-divide-and-conquer) · [5. Min-heap of heads](#5-min-heap-of-heads) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array of `k` linked lists, each sorted ascending, merge them into one sorted linked list and return its head.

| Input | Output | Why |
|---|---|---|
| `lists = [[1,4,5],[1,3,4],[2,6]]` | `[1,1,2,3,4,4,5,6]` |  |
| `lists = []` | `[]` |  |
| `lists = [[]]` | `[]` |  |

**Constraints:** `0 ≤ k ≤ 10⁴`, total nodes `N ≤ 10⁴`, `−10⁴ ≤ val ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Collect and sort | dump all values, sort, rebuild | O(N log N) | O(N) |
| Divide and conquer | merge pairs, halving the number of lists | O(N log k) | O(1) (iterative) |
| Min-heap of heads | pop smallest head, append, push its next | O(N log k) | O(k) |

> [!tip] Interview angle
> Present heap and divide-and-conquer; both are O(N log k). The heap version is the template for external sorting and the Twitter feed. Watch out for comparing nodes directly in Python (use `(val, idx, node)` tuples) and for null lists in the input.

---

## 3. Collect and sort

**Intuition.** Ignores the sortedness. Fine as a baseline.

```python
def merge_k_collect(lists):
    vals = []
    for h in lists:
        while h:
            vals.append(h.val); h = h.next
    d = t = ListNode()
    for v in sorted(vals):
        t.next = ListNode(v); t = t.next
    return d.next
```

**Complexity:** time **O(N log N)**, space **O(N)**.

---

## 4. Divide and conquer

**Intuition.** Merge lists `i` and `i + step` for step = 1, 2, 4, …. Every node takes part in ⌈log₂ k⌉ merges. (Merging one-by-one into an accumulator is O(Nk).)

```python
def merge_k_dc(lists):
    def merge2(a, b):
        d = t = ListNode()
        while a and b:
            if a.val <= b.val:
                t.next, a = a, a.next
            else:
                t.next, b = b, b.next
            t = t.next
        t.next = a or b
        return d.next
    lists, step = list(lists), 1
    while step < len(lists):
        for i in range(0, len(lists) - step, 2 * step):
            lists[i] = merge2(lists[i], lists[i + step])
        step *= 2
    return lists[0] if lists else None
```

**Complexity:** time **O(N log k)**, space **O(1) (iterative)**.

---

## 5. Min-heap of heads

**Intuition.** The heap holds at most one node per list: the current front. The global minimum is always one of the fronts.

**Algorithm**

1. Push every non-null head.
2. While the heap isn't empty: pop the min node, append it to the tail, push its `next` if non-null.
3. Return `dummy.next`.

**Dry run** — Heads {1a,1b,2}. Pop 1a, push 4a → {1b,2,4a}. Pop 1b, push 3 → {2,3,4a}. Pop 2, push 6 … output 1,1,2,3,4,4,5,6.

**C++**
```cpp
ListNode* mergeKLists(vector<ListNode*>& lists) {
    auto cmp = [](ListNode* a, ListNode* b) { return a->val > b->val; };
    priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> pq(cmp);
    for (ListNode* h : lists) if (h) pq.push(h);
    ListNode dummy, *tail = &dummy;
    while (!pq.empty()) {
        ListNode* x = pq.top(); pq.pop();
        tail->next = x; tail = x;
        if (x->next) pq.push(x->next);
    }
    tail->next = nullptr;
    return dummy.next;
}
```

**Java**
```java
static ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));
    for (ListNode h : lists) if (h != null) pq.offer(h);
    ListNode dummy = new ListNode(0), tail = dummy;
    while (!pq.isEmpty()) {
        ListNode x = pq.poll();
        tail.next = x; tail = x;
        if (x.next != null) pq.offer(x.next);
    }
    tail.next = null;
    return dummy.next;
}
```

**Python**
```python
import heapq
def merge_k_lists(lists):
    h = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(h)
    dummy = tail = ListNode()
    while h:
        _, i, node = heapq.heappop(h)
        tail.next = tail = node
        if node.next:
            heapq.heappush(h, (node.next.val, i, node.next))
    tail.next = None
    return dummy.next
```

**Complexity:** time **O(N log k)**, space **O(k)** — N pops and ≤ N pushes on a heap of size ≤ k.

---

## Edge cases

- Empty array / all lists empty → null.
- One list → returned as is.
- Lists of very different lengths.

---

## Common mistakes

1. Python: heap of bare `ListNode`s raises `TypeError` on ties (no `<`); add an index tie-breaker.
2. Pushing null heads.
3. Sequential merging into one accumulator: O(Nk).

---

## Follow-ups

1. Lists too big for memory (external sort)?
2. Merge k sorted arrays / find the smallest range covering all k lists?

<details><summary>Answer sketches</summary>

**#1:** Same k-way merge with buffered readers; the heap holds one record per run.

**#2:** Heap of `(val, list, idx)`; for smallest range also track the current max of the fronts (LC 632).
</details>

---

## Flashcards

**Merge k sorted lists complexity?** #flashcard
O(N log k): heap of heads, or divide-and-conquer.

**Python heap tie-breaker for nodes?** #flashcard
`(val, index, node)` tuples.

**Interview track →** [Heap deep-dive](../../01-data-structures/10-heap.md)
