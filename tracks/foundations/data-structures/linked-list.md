# Linked List — SDE-2+ Level

A linear data structure where nodes are stored in non-contiguous memory, connected via pointers. SDE-3 expects clean in-place operations, cycle handling, and trade-offs vs arrays.

---

## 1. Concept Overview

### Problem Space
- **Reversal**: Full, in k-groups, reorder (L0→Ln→L1→Ln-1…).
- **Finding**: Middle, cycle, cycle entry, intersection.
- **Merge**: Two sorted, K sorted, reorder.
- **Copy**: Copy with random pointer.

### When to Use
| Technique | Purpose |
| :--- | :--- |
| **Dummy Node** | Operation might change head (delete head, merge). |
| **Fast & Slow** | Find middle, detect cycle, find cycle entry. |
| **In-place Reversal** | Minimize space to O(1); `prev/curr/next`. |

---

## 2. Core Algorithms & Click Moments

### In-Place Reversal
> [!IMPORTANT]
> **The Click Moment**: "Reverse the order", "Palindrome check (second half)", "Reorder list".

```python
prev, curr = None, head
while curr:
    nxt = curr.next
    curr.next = prev
    prev, curr = curr, nxt
return prev
```

### Find Middle (Fast & Slow)
> [!IMPORTANT]
> **The Click Moment**: "Find middle node", "Split list", "Even/Odd length check".

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow
```

### Floyd's Cycle Detection
> [!IMPORTANT]
> **The Click Moment**: "Detect cycle", "Find loop start", "Intersection of two lists".

- **Detect**: If `slow == fast`, there is a cycle.
- **Entry**: Reset `slow` to `head`, keep `fast` at meeting point. Move both 1 step. Meet at entry.

---

## 3. Advanced Variations

- **Reverse in K-Group**: Reverse each k-block; connect tails.
- **Copy List with Random Pointer**: Use a map for `old_node → new_node`.
- **LRU Cache**: Doubly linked list + Hash Map.

---

## 4. Common Interview Problems

### Easy
- [Reverse Linked List](../google-sde2/PROBLEM_DETAILS.md#reverse-linked-list) — Iterative vs recursive.
- **Linked List Cycle** — Fast & slow pointers.

### Medium
- [Remove Nth From End](../google-sde2/PROBLEM_DETAILS.md#remove-nth-from-end) — Fast pointer advances `n` steps first.
- [Copy List with Random Pointer](../google-sde2/PROBLEM_DETAILS.md#copy-list-with-random-pointer) — Map or interleave.

### Hard
- [Merge K Sorted Lists](../google-sde2/PROBLEM_DETAILS.md#merge-k-sorted-lists) — Min-heap of size K.
- [LRU Cache](../google-sde2/PROBLEM_DETAILS.md#lru-cache) — DLL + Map.

---

## 5. Pattern Recognition

- **"Change Head"** → Dummy node.
- **"Middle/Cycle"** → Fast & slow.
- **"O(1) Space Reversal"** → Pointer manipulation.
- **"Random Pointer"** → Hash map for nodes.

---

## 6. Interview Strategy

- **Dummy Node**: Always use a dummy node to simplify head deletions or insertions.
- **Null Checks**: Fast pointer check `while fast and fast.next`.
- **In-place**: If space is constrained, avoid using a stack or recursion.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Reverse List](../google-sde2/PROBLEM_DETAILS.md#reverse-linked-list)** | "Flip pointers" | `curr.next = prev` | Don't lose the `next` node. |
| **[Remove Nth Node](../google-sde2/PROBLEM_DETAILS.md#remove-nth-from-end)** | "Offset pointers" | Fast advances `n` ahead | Removing the **head** node. |
| **[Merge K Lists](../google-sde2/PROBLEM_DETAILS.md#merge-k-sorted-lists)** | "Smallest among K" | Min-heap of size K | Handling empty lists. |
| **[LRU Cache](../google-sde2/PROBLEM_DETAILS.md#lru-cache)** | "Recent access" | DLL + Map | Capacity 1 edge case. |

---

## See also

- [Heap](heap.md) — merge K sorted lists  
- [Hashing](hashing.md) — copy with random pointer  
- [Patterns Master](../../../reference/patterns/patterns-master.md)
- [Stack](stack.md) — recursion uses call stack
