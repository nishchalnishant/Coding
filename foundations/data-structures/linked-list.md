# Linked List — SDE-3 Level

A linear data structure where elements (nodes) are stored in non-contiguous memory, connected via pointers. SDE-3 expects clean in-place operations, correct cycle handling, and trade-offs vs arrays.

---

## 1. Concept Overview

### Problem Space
- Reversal (full, in k-groups), reorder (e.g., L0→Ln→L1→Ln-1…).
- Finding middle, detecting cycle, finding cycle entry.
- Merge (two sorted, K sorted), copy with random pointer.
- Dummy node for unified head handling; fast/slow for middle and cycle.

### When to Use
- **Dummy node**: Insert/delete at head; merging lists (avoid null checks).
- **Fast & slow**: Middle (slow 1, fast 2); cycle (Floyd: meet then reset one to head, same step).
- **In-place reversal**: prev/curr/next; O(N) time, O(1) space.

---

## 2. Core Algorithms

### In-Place Reversal
```
prev = null, curr = head
while curr:
  next = curr.next
  curr.next = prev
  prev, curr = curr, next
return prev
```
Time O(N), Space O(1).

### Find Middle (Fast & Slow)
```
slow = fast = head
while fast and fast.next:
  slow = slow.next; fast = fast.next.next
return slow
```
Time O(N), Space O(1).

### Floyd Cycle Detection + Entry
- Phase 1: slow 1 step, fast 2 steps; if they meet → cycle.
- Phase 2: reset one to head; both move 1 step; meeting point = cycle entry.
- Time O(N), Space O(1).

---

## 3. Advanced Variations

- **Reverse in K-Group**: Reverse each k-block; connect tails; handle remainder.
- **Merge K Sorted Lists**: Min-heap of size K (first node of each list); pop min, append, push next. O(N log K).
- **Copy List with Random Pointer**: Old node → new node map; two passes (create nodes, then set next/random).
- **LRU Cache**: HashMap + doubly linked list (head = recent, tail = evict). Get: move to head; Put: add at head, evict tail if over capacity.

### Edge Cases
- Empty list; single node; two nodes; cycle at head; no cycle; even/odd length for middle.

---

## 4. Common Interview Problems

**Easy**: Reverse Linked List, Middle of Linked List, Merge Two Sorted Lists, Linked List Cycle.  
**Medium**: Add Two Numbers, Copy List with Random Pointer, Remove Nth Node From End, Reorder List.  
**Hard**: Reverse Nodes in k-Group, Merge k Sorted Lists, LRU Cache.

---

## 5. Pattern Recognition

- **Dummy node**: Any operation that might change head (delete head, merge).
- **Fast & slow**: Middle, cycle detection, palindrome (reverse second half and compare).
- **In-place reversal**: Full reverse, reverse k-group, reorder list (reverse second half then weave).
- **HashMap for copy**: Random pointer, deep copy with cycles.

---

## 6. Code Implementations

```python
def reverse_list(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev, head = head, nxt
    return prev

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow == fast:
            return True
    return False

def detect_cycle_entry(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow == fast:
            p = head
            while p != slow:
                p, slow = p.next, slow.next
            return p
    return None
```

---

## 7. SDE-3 Level Thinking

- **Trade-offs**: Linked list vs array — list: O(1) insert/delete at known node, no random access; array: O(1) access, cache-friendly. Use list when insertions/deletions in middle are dominant (e.g., LRU).
- **Memory**: In-place reversal avoids extra list; dummy node uses one extra node (negligible). Copy structures (random pointer) need O(N) map.
- **Concurrency**: Lock-free linked structures (CAS) for queues; mention if asked.

---

## 8. Interview Strategy

- **Identify**: "Reverse", "middle", "cycle", "merge" → standard patterns. "Random pointer" → copy with map.
- **Approach**: Always consider null/one node. Use dummy when head might change. For cycle, state Floyd and then find entry.
- **Common mistakes**: Off-by-one in k-group reversal; forgetting to set tail.next to None; losing reference to next before rewiring.

---

## 9. Quick Revision

- **Formulas**: Middle: fast 2x, slow 1x. Cycle entry: meet then head + meet both step 1.
- **Tricks**: Dummy node; prev/curr/next for reversal; heap for merge K.
- **Edge cases**: Empty, single node, cycle at head, k > length.
- **Pattern tip**: "From end" → two pointers (advance first by n) or stack; "random" → HashMap copy.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness |
|----------|------------|------------|
| **Reverse List** | `prev, curr, next` iterative | Recursive O(n) stack; null head |
| **Merge Two Sorted** | Dummy head; compare and append smaller | In-place vs new list; exhaust one list |
| **Cycle II (entry)** | Floyd meet; reset one ptr to head; same speed to entry | Why math works; confusing “restart fast only” |
| **Merge K Lists** | Min-heap of heads; pop min, push next | O(N log k); tie-break list id |
| **Copy with Random** | Map old→new; two passes wire `next`/`random` | O(1) space interleaving is bonus |

---

## See also

- [Heap](heap.md) — merge K sorted lists  
- [Hashing](hashing.md) — copy with random pointer  
- [Stack](stack.md) — recursion uses call stack
